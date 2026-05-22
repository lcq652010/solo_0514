import Vue from 'vue'
import VueRouter from 'vue-router'
import DeviceList from '@/views/DeviceList.vue'
import WorkOrder from '@/views/WorkOrder.vue'
import Statistics from '@/views/Statistics.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/device'
  },
  {
    path: '/device',
    name: 'DeviceList',
    component: DeviceList
  },
  {
    path: '/workorder',
    name: 'WorkOrder',
    component: WorkOrder
  },
  {
    path: '/statistics',
    name: 'Statistics',
    component: Statistics
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
