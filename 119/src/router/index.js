import Vue from 'vue'
import VueRouter from 'vue-router'
import OrderForm from '../views/OrderForm.vue'
import AdminDashboard from '../views/AdminDashboard.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'OrderForm',
    component: OrderForm
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
