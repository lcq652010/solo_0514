import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/order-form'
  },
  {
    path: '/order-form',
    name: 'OrderForm',
    component: () => import('../views/OrderForm.vue')
  },
  {
    path: '/vehicle-list',
    name: 'VehicleList',
    component: () => import('../views/VehicleList.vue')
  },
  {
    path: '/dispatch',
    name: 'Dispatch',
    component: () => import('../views/Dispatch.vue')
  },
  {
    path: '/order-list',
    name: 'OrderList',
    component: () => import('../views/OrderList.vue')
  },
  {
    path: '/tracking',
    name: 'Tracking',
    component: () => import('../views/Tracking.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
