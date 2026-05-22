import Vue from 'vue'
import VueRouter from 'vue-router'
import DeviceList from '@/views/DeviceList.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'DeviceList',
    component: DeviceList
  }
]

const router = new VueRouter({
  mode: 'hash',
  routes
})

export default router
