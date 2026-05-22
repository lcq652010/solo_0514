import Vue from 'vue'
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App.vue'
import OrderForm from './components/OrderForm.vue'
import OrderList from './components/OrderList.vue'
import OrderDetail from './components/OrderDetail.vue'

Vue.use(VueRouter)
Vue.use(ElementUI)

const routes = [
  { path: '/', redirect: '/order' },
  { path: '/order', component: OrderForm },
  { path: '/admin', component: OrderList },
  { path: '/detail/:id', component: OrderDetail }
]

const router = new VueRouter({
  routes
})

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
