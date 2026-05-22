import Vue from 'vue'
import VueRouter from 'vue-router'
import Layout from '../views/Layout.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: Layout,
    redirect: '/room-types',
    children: [
      {
        path: 'room-types',
        name: 'RoomTypes',
        component: () => import('../views/RoomTypes.vue')
      },
      {
        path: 'booking',
        name: 'Booking',
        component: () => import('../views/Booking.vue')
      },
      {
        path: 'check-in',
        name: 'CheckIn',
        component: () => import('../views/CheckIn.vue')
      },
      {
        path: 'orders',
        name: 'Orders',
        component: () => import('../views/Orders.vue')
      },
      {
        path: 'room-status',
        name: 'RoomStatus',
        component: () => import('../views/RoomStatus.vue')
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
