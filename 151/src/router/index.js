import Vue from 'vue'
import VueRouter from 'vue-router'
import TrainerList from '@/views/TrainerList.vue'
import Booking from '@/views/Booking.vue'
import Classes from '@/views/Classes.vue'
import MyBookings from '@/views/MyBookings.vue'
import CourseHours from '@/views/CourseHours.vue'

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
    name: 'Booking',
    component: Booking
  },
  {
    path: '/classes',
    name: 'Classes',
    component: Classes
  },
  {
    path: '/my-bookings',
    name: 'MyBookings',
    component: MyBookings
  },
  {
    path: '/course-hours',
    name: 'CourseHours',
    component: CourseHours
  }
]

const router = new VueRouter({
  mode: 'hash',
  routes
})

export default router
