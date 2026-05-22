import Vue from 'vue'
import VueRouter from 'vue-router'
import OrderPage from '../views/OrderPage.vue'
import AdminPage from '../views/AdminPage.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Order',
    component: OrderPage
  },
  {
    path: '/admin',
    name: 'Admin',
    component: AdminPage
  }
]

const router = new VueRouter({
  mode: 'hash',
  routes
})

export default router
