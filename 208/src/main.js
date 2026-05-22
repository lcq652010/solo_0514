import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import './assets/styles/global.scss'
import moment from 'moment'

Vue.config.productionTip = false
Vue.use(ElementUI)

Vue.filter('formatDate', function(value) {
  if (value) {
    return moment(value).format('YYYY-MM-DD HH:mm:ss')
  }
  return ''
})

Vue.filter('formatCurrency', function(value) {
  if (value !== undefined && value !== null) {
    return '¥' + Number(value).toFixed(2)
  }
  return ''
})

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
