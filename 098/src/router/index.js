import Vue from 'vue'
import VueRouter from 'vue-router'
import OrderPage from '../views/OrderPage.vue'
import AdminPage from '../views/AdminPage.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'OrderPage',
    component: OrderPage
  },
  {
    path: '/admin',
    name: 'AdminPage',
    component: AdminPage
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
