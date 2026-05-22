import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/dormitory'
  },
  {
    path: '/dormitory',
    name: 'Dormitory',
    component: () => import('@/views/DormitorySelect.vue')
  },
  {
    path: '/recharge',
    name: 'Recharge',
    component: () => import('@/views/RechargeForm.vue')
  },
  {
    path: '/statistics',
    name: 'Statistics',
    component: () => import('@/views/StatisticsChart.vue')
  },
  {
    path: '/records',
    name: 'Records',
    component: () => import('@/views/RechargeRecords.vue')
  },
  {
    path: '/warning',
    name: 'Warning',
    component: () => import('@/views/BalanceWarning.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
