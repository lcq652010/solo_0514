import Vue from 'vue'
import VueRouter from 'vue-router'
import OrderForm from '../components/OrderForm.vue'
import AdminPanel from '../components/AdminPanel.vue'

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
