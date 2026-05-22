import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import moment from 'moment'

Vue.config.productionTip = false

Vue.use(ElementUI)

Vue.filter('formatDate', function(value, format = 'YYYY-MM-DD HH:mm:ss') {
  if (value) {
    return moment(value).format(format)
  }
  return ''
})

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
