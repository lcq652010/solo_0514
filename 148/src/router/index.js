import Vue from 'vue'
import VueRouter from 'vue-router'
import MovieList from '@/views/MovieList.vue'
import Schedule from '@/views/Schedule.vue'
import SeatSelection from '@/views/SeatSelection.vue'
import Orders from '@/views/Orders.vue'
import Refund from '@/views/Refund.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'MovieList',
    component: MovieList
  },
  {
    path: '/schedule/:movieId',
    name: 'Schedule',
    component: Schedule
  },
  {
    path: '/seats/:scheduleId',
    name: 'SeatSelection',
    component: SeatSelection
  },
  {
    path: '/orders',
    name: 'Orders',
    component: Orders
  },
  {
    path: '/refund',
    name: 'Refund',
    component: Refund
  }
]

const router = new VueRouter({
  mode: 'hash',
  routes
})

export default router
