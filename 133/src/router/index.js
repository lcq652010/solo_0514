import Vue from 'vue'
import Router from 'vue-router'
import OrderList from '@/views/OrderList.vue'
import KitchenSchedule from '@/views/KitchenSchedule.vue'
import ServeConfirm from '@/views/ServeConfirm.vue'
import CookingStatus from '@/views/CookingStatus.vue'
import UrgentReminder from '@/views/UrgentReminder.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      redirect: '/order-list'
    },
    {
      path: '/order-list',
      name: 'OrderList',
      component: OrderList
    },
    {
      path: '/kitchen-schedule',
      name: 'KitchenSchedule',
      component: KitchenSchedule
    },
    {
      path: '/serve-confirm',
      name: 'ServeConfirm',
      component: ServeConfirm
    },
    {
      path: '/cooking-status',
      name: 'CookingStatus',
      component: CookingStatus
    },
    {
      path: '/urgent-reminder',
      name: 'UrgentReminder',
      component: UrgentReminder
    }
  ]
})
