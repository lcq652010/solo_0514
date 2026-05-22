import Vue from 'vue'
import VueRouter from 'vue-router'
import OrderForm from '../views/OrderForm.vue'
import AdminPanel from '../views/AdminPanel.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'OrderForm',
    component: OrderForm
  },
  {
    path: '/admin',
    name: 'AdminPanel',
    component: AdminPanel
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
