import Vue from 'vue'
import VueRouter from 'vue-router'
import OrderPage from '@/views/OrderPage.vue'
import AdminPage from '@/views/AdminPage.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'order',
    component: OrderPage
  },
  {
    path: '/admin',
    name: 'admin',
    component: AdminPage
  }
]

const router = new VueRouter({
  mode: 'hash',
  routes
})

export default router
