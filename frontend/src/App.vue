<template>
  <v-app>
    <!-- 侧边导航栏 - 仅在非登录/注册页显示 -->
    <v-navigation-drawer
      v-if="showLayout"
      v-model="drawer"
      permanent
      elevation="2"
    >
      <div class="d-flex align-center pa-4">
        <v-icon color="primary" size="32" class="mr-2">mdi-fish</v-icon>
        <span class="text-h6 font-weight-bold">智能投喂系统</span>
      </div>

      <v-divider></v-divider>

      <v-list nav class="mt-2">
        <v-list-item
          to="/"
          prepend-icon="mdi-view-dashboard"
          title="系统概览"
          active-class="text-primary"
        ></v-list-item>
        <v-list-item
          to="/monitoring"
          prepend-icon="mdi-water"
          title="环境监测"
          active-class="text-primary"
        ></v-list-item>
        <v-list-item
          to="/feeding"
          prepend-icon="mdi-bowl-mix"
          title="智能投喂"
          active-class="text-primary"
        ></v-list-item>
        <v-list-item
          to="/alerts"
          prepend-icon="mdi-alert"
          title="系统告警"
          active-class="text-primary"
        ></v-list-item>
        <v-list-item
          to="/statistics"
          prepend-icon="mdi-chart-line"
          title="统计图表"
          active-class="text-primary"
        ></v-list-item>
      </v-list>

      <template v-slot:append>
        <div class="pa-4">
          <v-menu location="top">
            <template v-slot:activator="{ props }">
              <v-card
                v-bind="props"
                class="d-flex align-center pa-2 cursor-pointer"
                flat
                variant="tonal"
              >
                <v-avatar color="primary" size="32">
                  <span class="text-white text-subtitle-2">{{ username.charAt(0).toUpperCase() }}</span>
                </v-avatar>
                <div class="ml-3 overflow-hidden">
                  <div class="text-subtitle-2 text-truncate">{{ username }}</div>
                  <div class="text-caption text-medium-emphasis">管理员</div>
                </div>
                <v-spacer></v-spacer>
                <v-icon size="small">mdi-chevron-up</v-icon>
              </v-card>
            </template>
            <v-list>
              <v-list-item @click="logout" prepend-icon="mdi-logout" title="退出登录"></v-list-item>
            </v-list>
          </v-menu>
        </div>
      </template>
    </v-navigation-drawer>

    <!-- 主内容区域 -->
    <v-main>
      <!-- 全局加载状态 -->
      <v-overlay v-model="globalLoading" class="align-center justify-center">
        <v-progress-circular indeterminate size="64"></v-progress-circular>
      </v-overlay>

      <!-- 全局通知 -->
      <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="3000">
        {{ snackbar.message }}
      </v-snackbar>

      <!-- 路由视图 -->
      <v-container fluid class="pa-6">
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, provide, onMounted, onUnmounted, computed } from "vue";
import { environmentService } from "./services/environment";
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

// 侧边栏控制
const drawer = ref(true)
const username = ref(localStorage.getItem('username') || 'Admin')
const showLayout = computed(() => !['/login', '/register'].includes(route.path))

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
