import Vue from 'vue'
import Router from 'vue-router'
import Layout from '@/layout/index.vue'

Vue.use(Router)

const routes = [
  {
    path: '/',
    component: Layout,
    redirect: '/usage',
    children: [
      {
        path: 'usage',
        name: 'Usage',
        component: () => import('@/views/Usage.vue'),
        meta: { title: '水电用量', icon: 'el-icon-data-line' }
      },
      {
        path: 'recharge',
        name: 'Recharge',
        component: () => import('@/views/Recharge.vue'),
        meta: { title: '在线充值', icon: 'el-icon-wallet' }
      },
      {
        path: 'records',
        name: 'Records',
        component: () => import('@/views/Records.vue'),
        meta: { title: '充值记录', icon: 'el-icon-document' }
      },
      {
        path: 'reminder',
        name: 'Reminder',
        component: () => import('@/views/Reminder.vue'),
        meta: { title: '余额提醒', icon: 'el-icon-bell' }
      },
      {
        path: 'binding',
        name: 'Binding',
        component: () => import('@/views/Binding.vue'),
        meta: { title: '宿舍绑定', icon: 'el-icon-house' }
      }
    ]
  }
]

const router = new Router({
  mode: 'hash',
  routes
})

export default router
