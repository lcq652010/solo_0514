import VueRouter from 'vue-router'
import OrderPage from '../views/OrderPage.vue'
import AdminPage from '../views/AdminPage.vue'

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
  mode: 'hash',
  routes
})

export default router
