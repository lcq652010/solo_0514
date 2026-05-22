import Vue from 'vue'
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App.vue'
import router from './router'
import { EventBus } from './utils/eventBus'

Vue.use(VueRouter)
Vue.use(ElementUI)

Vue.config.productionTip = false
Vue.prototype.$bus = EventBus

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')