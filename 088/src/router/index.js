import Vue from 'vue'
import VueRouter from 'vue-router'
import TrainerList from '@/views/TrainerList.vue'
import BookingForm from '@/views/BookingForm.vue'
import MyBookings from '@/views/MyBookings.vue'
import VerifyLesson from '@/views/VerifyLesson.vue'
import Schedule from '@/views/Schedule.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/trainers'
  },
  {
    path: '/trainers',
    name: 'TrainerList',
    component: TrainerList
  },
  {
    path: '/booking',
    name: 'BookingForm',
    component: BookingForm
  },
  {
    path: '/my-bookings',
    name: 'MyBookings',
    component: MyBookings
  },
  {
    path: '/verify',
    name: 'VerifyLesson',
    component: VerifyLesson
  },
  {
    path: '/schedule',
    name: 'Schedule',
    component: Schedule
  }
]

const router = new VueRouter({
  mode: 'hash',
  routes
})

export default router
