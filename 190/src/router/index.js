import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/schedule'
  },
  {
    path: '/schedule',
    name: 'Schedule',
    component: () => import('@/views/Schedule.vue')
  },
  {
    path: '/appointment',
    name: 'Appointment',
    component: () => import('@/views/Appointment.vue')
  },
  {
    path: '/medical-record',
    name: 'MedicalRecord',
    component: () => import('@/views/MedicalRecord.vue')
  },
  {
    path: '/appointment-list',
    name: 'AppointmentList',
    component: () => import('@/views/AppointmentList.vue')
  },
  {
    path: '/vaccine-reminder',
    name: 'VaccineReminder',
    component: () => import('@/views/VaccineReminder.vue')
  }
]

const router = new VueRouter({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes
})

export default router
