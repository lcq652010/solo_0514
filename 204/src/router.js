import Vue from 'vue'
import Router from 'vue-router'
import DeviceManagement from './views/DeviceManagement.vue'

Vue.use(Router)

const router = new Router({
  mode: 'hash',
  routes: [
    {
      path: '/',
      redirect: '/device-management'
    },
    {
      path: '/device-management',
      name: 'DeviceManagement',
      component: DeviceManagement,
      meta: {
        title: '设备管理'
      }
    }
  ]
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || '图书馆自助终端运维管理后台'
  next()
})

export default router
