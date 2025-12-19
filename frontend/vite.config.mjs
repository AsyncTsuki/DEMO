// Plugins
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import Fonts from 'unplugin-fonts/vite'
import Layouts from 'vite-plugin-vue-layouts-next'
import Vue from '@vitejs/plugin-vue'
import VueRouter from 'unplugin-vue-router/vite'
import { VueRouterAutoImports } from 'unplugin-vue-router'
import Vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'

// Utilities
import { defineConfig } from 'vite'
import { fileURLToPath, URL } from 'node:url'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    VueRouter(),
    Layouts(),
    Vue({
      template: { transformAssetUrls },
    }),
    // https://github.com/vuetifyjs/vuetify-loader/tree/master/packages/vite-plugin#readme
    Vuetify({
      autoImport: true,
      styles: {
        configFile: 'src/styles/settings.scss',
      },
    }),
    Components(),
    Fonts({
      google: {
        families: [{
          name: 'Roboto',
          styles: 'wght@100;300;400;500;700;900',
        }],
      },
    }),
    AutoImport({
      imports: [
        'vue',
        VueRouterAutoImports,
        {
          pinia: ['defineStore', 'storeToRefs'],
        },
      ],
      eslintrc: {
        enabled: true,
      },
      vueTemplate: true,
    }),
  ],
  optimizeDeps: {
    include: [
      'vue',
      'vue-router',
      'pinia',
      'axios',
      'apexcharts',
      'vue3-apexcharts'
    ],
    exclude: [
      'vuetify',
      'unplugin-vue-router/runtime',
      'unplugin-vue-router/data-loaders',
      'unplugin-vue-router/data-loaders/basic',
    ],
  },
  define: { 'process.env': {} },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('src', import.meta.url)),
    },
    extensions: [
      '.js',
      '.json',
      '.jsx',
      '.mjs',
      '.ts',
      '.tsx',
      '.vue',
    ],
  },
  /* server: {
    port: 3000,
  }, */
  server: {
    open: '/', // ← 启动时自动打开首页
    warmup: {
      // 预热所有页面和常用模块，避免首次加载404错误
      clientFiles: [
        // 核心文件
        './src/App.vue',
        './src/main.js',
        './src/router/index.js',
        
        // 所有页面
        './src/pages/Landing.vue',
        './src/pages/index.vue',
        './src/pages/monitoring.vue',
        './src/pages/feeding.vue',
        './src/pages/devices.vue',
        './src/pages/alerts.vue',
        './src/pages/logs.vue',
        './src/pages/statistics.vue',
        
        // 布局和组件
        './src/layouts/default.vue',
        './src/components/**/*.vue',
        
        // 所有服务
        './src/services/api.js',
        './src/services/auth.js',
        './src/services/devices.js',
        './src/services/environment.js',
        './src/services/feeding.js',
        './src/services/alerts.js',
        './src/services/logs.js',
        './src/services/statistics.js',
        
        // 状态管理
        './src/stores/app.js',
        './src/stores/index.js',
        
        // 插件
        './src/plugins/index.js',
        './src/plugins/vuetify.js'
      ]
    }
  }
})
