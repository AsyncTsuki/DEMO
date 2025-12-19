/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'

// Styles
import 'unfonts.css'

const app = createApp(App)

registerPlugins(app)

// 添加全局错误处理
app.config.errorHandler = (err, instance, info) => {
  console.error('全局错误捕获:', err, info)
  
  // 如果是模块加载错误，提示用户并自动刷新
  if (err.message && err.message.includes('Failed to fetch')) {
    console.log('检测到资源加载失败，将自动刷新...')
    setTimeout(() => {
      window.location.reload()
    }, 1000)
  }
}

app.mount('#app')
