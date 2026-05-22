import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/products'
  },
  {
    path: '/products',
    name: 'Products',
    component: () => import('@/views/Products.vue')
  },
  {
    path: '/order-create',
    name: 'OrderCreate',
    component: () => import('@/views/OrderCreate.vue')
  },
  {
    path: '/delivery',
    name: 'Delivery',
    component: () => import('@/views/Delivery.vue')
  },
  {
    path: '/orders',
    name: 'Orders',
    component: () => import('@/views/Orders.vue')
  },
  {
    path: '/stock-warning',
    name: 'StockWarning',
    component: () => import('@/views/StockWarning.vue')
  }
]

const router = new VueRouter({
  mode: 'hash',
  routes
})

export default router
