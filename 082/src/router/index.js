import Vue from 'vue'
import VueRouter from 'vue-router'
import ActivityList from '../views/ActivityList.vue'
import ActivityDetail from '../views/ActivityDetail.vue'
import ActivityRegister from '../views/ActivityRegister.vue'
import ActivityCheckIn from '../views/ActivityCheckIn.vue'
import MyRegistrations from '../views/MyRegistrations.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'ActivityList',
    component: ActivityList
  },
  {
    path: '/activity/:id',
    name: 'ActivityDetail',
    component: ActivityDetail
  },
  {
    path: '/register/:id',
    name: 'ActivityRegister',
    component: ActivityRegister
  },
  {
    path: '/checkin/:id',
    name: 'ActivityCheckIn',
    component: ActivityCheckIn
  },
  {
    path: '/my-registrations',
    name: 'MyRegistrations',
    component: MyRegistrations
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
