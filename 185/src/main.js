import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App.vue'
import router from './router'

Vue.use(ElementUI)
Vue.config.productionTip = false

Vue.prototype.$eventBus = new Vue()
Vue.prototype.$currentUser = {
  account: 'admin',
  name: '管理员'
}

Vue.prototype.$getClientIP = async function() {
  return new Promise((resolve) => {
    const ip = '192.168.1.' + Math.floor(Math.random() * 255)
    resolve(ip)
  })
}

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
