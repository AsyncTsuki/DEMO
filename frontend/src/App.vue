<template>
  <v-app class="app-background">
    <!-- 侧边导航栏 - 仅在非登录/注册页显示 -->
    <v-navigation-drawer
      v-if="showLayout"
      v-model="drawer"
      permanent
      elevation="0"
      color="white"
      class="main-drawer"
      width="280"
    >
      <!-- Logo 区域 -->
      <div class="d-flex align-center pa-6 mb-2">
        <v-avatar color="primary" size="40" class="mr-3 elevation-2">
          <v-icon color="white" size="24">mdi-fish</v-icon>
        </v-avatar>
        <div>
          <div class="text-h6 font-weight-bold text-primary">智慧渔业平台</div>
          <div class="text-caption text-grey">Smart Fishery System</div>
        </div>
      </div>

      <v-divider class="mx-4 mb-4"></v-divider>

      <!-- 导航菜单 -->
      <v-list nav class="px-4">
        <v-list-item
          @click.stop="navigateTo('/dashboard')"
          :active="route.path === '/dashboard'"
          prepend-icon="mdi-view-dashboard-outline"
          title="系统概览"
          class="mb-2 rounded-lg"
          active-class="primary white--text elevation-2"
        ></v-list-item>
        
        <v-list-item
          @click.stop="navigateTo('/monitoring')"
          :active="route.path === '/monitoring'"
          prepend-icon="mdi-water-outline"
          title="环境监测"
          class="mb-2 rounded-lg"
          active-class="primary white--text elevation-2"
        ></v-list-item>
        
        <v-list-item
          @click.stop="navigateTo('/feeding')"
          :active="route.path === '/feeding'"
          prepend-icon="mdi-bowl-mix-outline"
          title="智能投喂"
          class="mb-2 rounded-lg"
          active-class="primary white--text elevation-2"
        ></v-list-item>
        
        <v-list-item
          @click.stop="navigateTo('/alerts')"
          :active="route.path === '/alerts'"
          prepend-icon="mdi-bell-outline"
          title="系统告警"
          class="mb-2 rounded-lg"
          active-class="primary white--text elevation-2"
        ></v-list-item>
        
        <v-list-item
          @click.stop="navigateTo('/statistics')"
          :active="route.path === '/statistics'"
          prepend-icon="mdi-chart-box-outline"
          title="数据统计"
          class="mb-2 rounded-lg"
          active-class="primary white--text elevation-2"
        ></v-list-item>
      </v-list>

      <!-- 底部用户区域 -->
      <template v-slot:append>
        <div class="pa-4">
          <v-menu location="top start" origin="bottom start" transition="scale-transition">
            <template v-slot:activator="{ props }">
              <v-card
                v-bind="props"
                class="user-card d-flex align-center pa-3 cursor-pointer"
                elevation="0"
                border
              >
                <v-avatar color="primary lighten-4" size="40">
                  <span class="text-primary font-weight-bold">{{ username.charAt(0).toUpperCase() }}</span>
                </v-avatar>
                <div class="ml-3 overflow-hidden">
                  <div class="text-subtitle-2 font-weight-bold text-truncate">{{ username }}</div>
                  <div class="text-caption text-medium-emphasis">管理员</div>
                </div>
                <v-spacer></v-spacer>
                <v-icon size="small" color="grey">mdi-chevron-up</v-icon>
              </v-card>
            </template>
            <v-list class="rounded-lg elevation-4 mb-2" width="248">
              <v-list-item 
                @click="logout" 
                prepend-icon="mdi-logout" 
                title="退出登录"
                color="error"
              ></v-list-item>
            </v-list>
          </v-menu>
        </div>
      </template>
    </v-navigation-drawer>

    <!-- 主内容区域 -->
    <v-main class="bg-grey-lighten-4">
      <!-- 顶部状态栏 (仅显示在非全屏页面) -->
      <v-app-bar v-if="showLayout" flat color="transparent" class="px-4 mt-2">
        <div class="text-h5 font-weight-bold text-grey-darken-3">{{ pageTitle }}</div>
        <v-spacer></v-spacer>
        <div class="text-body-2 text-grey-darken-1 mr-2">{{ currentDate }}</div>
      </v-app-bar>

      <!-- 全局加载状态 -->
      <v-overlay v-model="globalLoading" class="align-center justify-center">
        <v-progress-circular indeterminate size="64" color="primary"></v-progress-circular>
      </v-overlay>

      <!-- 全局通知 -->
      <v-snackbar 
        v-model="snackbar.show" 
        :color="snackbar.color" 
        timeout="3000"
        location="top right"
      >
        {{ snackbar.message }}
        <template v-slot:actions>
          <v-btn variant="text" @click="snackbar.show = false">关闭</v-btn>
        </template>
      </v-snackbar>

      <!-- 路由视图 -->
      <v-container fluid class="pa-6">
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, provide, onMounted, onUnmounted, computed, watch } from "vue";
import { environmentService } from "./services/environment";
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

// 侧边栏控制
const drawer = ref(true)
const username = ref(localStorage.getItem('username') || 'Admin')
const showLayout = computed(() => !['/login', '/register', '/'].includes(route.path))

// 页面标题映射
const pageTitle = computed(() => {
  const titleMap = {
    '/dashboard': '系统概览',
    '/monitoring': '环境监测',
    '/feeding': '智能投喂',
    '/alerts': '系统告警',
    '/statistics': '数据统计'
  }
  return titleMap[route.path] || '智慧渔业平台'
})

// 当前日期
const currentDate = ref(new Date().toLocaleDateString())

// 全局状态管理
const globalLoading = ref(false);
const snackbar = ref({
  show: false,
  message: "",
  color: "success",
});

// ... (keep existing methods)

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

// 导航方法
const navigateTo = (path) => {
  console.log('导航到:', path);
  router.push(path).catch(err => {
    console.error('路由跳转失败:', err);
  });
};
</script>

<style scoped>
.app-background {
  background-color: #f3f4f6;
}

.main-drawer {
  border-right: none !important;
  box-shadow: 4px 0 24px rgba(0,0,0,0.02) !important;
}

.user-card {
  transition: all 0.2s ease;
}

.user-card:hover {
  background-color: rgba(0,0,0,0.03);
}

:deep(.v-list-item--active) {
  box-shadow: 0 4px 12px rgba(var(--v-theme-primary), 0.3);
}
</style>
