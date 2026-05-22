import Vue from 'vue'
import VueRouter from 'vue-router'
import OrderPage from '@/views/OrderPage.vue'
import Login from '@/views/Login.vue'
import AdminOrders from '@/views/AdminOrders.vue'
import { isLoggedIn } from '@/utils/storage.js'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'OrderPage',
    component: OrderPage
  },
  {
    path: '/admin/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/admin/orders',
    name: 'AdminOrders',
    component: AdminOrders,
    beforeEnter: (to, from, next) => {
      if (isLoggedIn()) {
        next()
      } else {
        next('/admin/login')
      }
    }
  }
]

const router = new VueRouter({
  mode: 'hash',
  routes
})

export default router
