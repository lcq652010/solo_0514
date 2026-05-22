import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/menu'
  },
  {
    path: '/menu',
    name: 'Menu',
    component: () => import('@/views/Menu.vue')
  },
  {
    path: '/orders',
    name: 'Orders',
    component: () => import('@/views/Orders.vue')
  },
  {
    path: '/production',
    name: 'Production',
    component: () => import('@/views/Production.vue')
  },
  {
    path: '/statistics',
    name: 'Statistics',
    component: () => import('@/views/Statistics.vue')
  }
]

const router = new VueRouter({
  mode: 'hash',
  routes
})

export default router
