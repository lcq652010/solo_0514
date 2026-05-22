import Vue from 'vue'
import VueRouter from 'vue-router'
import OrderForm from '../components/OrderForm.vue'
import OrderAdmin from '../components/OrderAdmin.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'OrderForm',
    component: OrderForm
  },
  {
    path: '/admin',
    name: 'OrderAdmin',
    component: OrderAdmin
  }
]

const router = new VueRouter({
  mode: 'hash',
  routes
})

export default router
