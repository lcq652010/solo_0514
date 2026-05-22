import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/packages'
  },
  {
    path: '/packages',
    name: 'Packages',
    component: () => import('@/views/Packages.vue')
  },
  {
    path: '/appointment',
    name: 'Appointment',
    component: () => import('@/views/Appointment.vue')
  },
  {
    path: '/schedule',
    name: 'Schedule',
    component: () => import('@/views/Schedule.vue')
  },
  {
    path: '/records',
    name: 'Records',
    component: () => import('@/views/Records.vue')
  },
  {
    path: '/customers',
    name: 'Customers',
    component: () => import('@/views/Customers.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
