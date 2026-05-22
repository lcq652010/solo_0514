import Vue from 'vue'
import VueRouter from 'vue-router'
import DeviceList from '@/views/DeviceList.vue'
import WorkOrderList from '@/views/WorkOrderList.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'DeviceList',
    component: DeviceList,
    meta: { title: '设备管理' }
  },
  {
    path: '/workorder',
    name: 'WorkOrderList',
    component: WorkOrderList,
    meta: { title: '工单管理' }
  }
]

const router = new VueRouter({
  mode: 'hash',
  routes
})

export default router
