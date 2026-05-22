import Vue from 'vue'
import VueRouter from 'vue-router'
import OrderForm from '../views/OrderForm.vue'
import AdminOrders from '../views/AdminOrders.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/order'
  },
  {
    path: '/order',
    name: 'OrderForm',
    component: OrderForm
  },
  {
    path: '/admin',
    name: 'AdminOrders',
    component: AdminOrders
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
