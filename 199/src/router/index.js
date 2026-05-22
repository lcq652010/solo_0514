import Vue from 'vue'
import VueRouter from 'vue-router'
import Layout from '@/layout/Layout.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: Layout,
    redirect: '/dishes',
    children: [
      {
        path: 'dishes',
        name: 'Dishes',
        component: () => import('@/views/Dishes.vue'),
        meta: { title: '菜品列表', icon: 'el-icon-goods' }
      },
      {
        path: 'checkout',
        name: 'Checkout',
        component: () => import('@/views/Checkout.vue'),
        meta: { title: '下单结算', icon: 'el-icon-shopping-cart-2' }
      },
      {
        path: 'orders',
        name: 'Orders',
        component: () => import('@/views/Orders.vue'),
        meta: { title: '订单管理', icon: 'el-icon-document' }
      },
      {
        path: 'dispatch',
        name: 'Dispatch',
        component: () => import('@/views/Dispatch.vue'),
        meta: { title: '骑手派单', icon: 'el-icon-bicycle' }
      },
      {
        path: 'delivery',
        name: 'Delivery',
        component: () => import('@/views/Delivery.vue'),
        meta: { title: '配送状态', icon: 'el-icon-location' }
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
