<template>
  <v-app>
    <!-- 全局加载状态 -->
    <v-overlay v-model="globalLoading" class="align-center justify-center">
      <v-progress-circular indeterminate size="64"></v-progress-circular>
    </v-overlay>

    <!-- 全局通知 -->
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="3000">
      {{ snackbar.message }}
    </v-snackbar>

    <!-- 路由视图 -->
    <router-view />

    <!-- 在顶部导航栏最右侧添加下拉菜单 -->
    <v-menu offset-y>
      <template v-slot:activator="{ props }">
        <v-btn icon v-bind="props">
          <v-icon>mdi-account-circle</v-icon>
        </v-btn>
      </template>
      <v-list>
        <v-list-item @click="logout">
          <v-list-item-title>退出登录</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-app>
</template>

<script setup>
import { ref, provide, onMounted, onUnmounted } from "vue";
import { environmentService } from "./services/environment";
import { useRouter } from 'vue-router'

const router = useRouter()

// 全局状态管理
const globalLoading = ref(false);
const snackbar = ref({
  show: false,
  message: "",
  color: "success",
});

// 全局方法
const showLoading = (show) => {
  globalLoading.value = show;
};

const showMessage = (message, color = "success") => {
  snackbar.value = {
    show: true,
    message,
    color,
  };
};

// 提供全局方法给所有组件
provide("showLoading", showLoading);
provide("showMessage", showMessage);

// 环境数据
const environmentData = ref({
  temperature: 23.5,
  dissolvedOxygen: 6.5,
  ph: 7.8,
  waterFlow: 1.2,
});

provide("environmentData", environmentData);

// 获取实时环境数据
const fetchEnvironmentData = async () => {
  try {
    const response = await environmentService.getRealTimeData();
    if (response && response.success && response.data) {
      environmentData.value = response.data;
    }
  } catch (error) {
    console.error("获取环境数据失败:", error);
    // 不显示错误消息以避免频繁提示
  }
};

// 定时器引用
let updateTimer = null;

// 组件挂载时获取数据并设置定时更新
onMounted(() => {
  fetchEnvironmentData();
  // 每30秒更新一次环境数据
  updateTimer = setInterval(fetchEnvironmentData, 30000);
});

// 组件卸载时清除定时器
onUnmounted(() => {
  if (updateTimer) {
    clearInterval(updateTimer);
  }
});

// 退出登录
const logout = async () => {
  try {
    // 调用后端退出接口
    const { authService } = await import('./services/auth');
    await authService.logout();
  } catch (error) {
    console.error('退出登录失败:', error);
  } finally {
    // 清除登录状态
    localStorage.removeItem('authToken');
    localStorage.removeItem('username');
    // 跳转到登录页
    router.push('/login');
  }
};
</script>
