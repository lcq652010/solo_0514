import Vue from 'vue'
import VueRouter from 'vue-router'
import Layout from '@/views/Layout.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: Layout,
    redirect: '/items',
    children: [
      {
        path: 'items',
        name: 'Items',
        component: () => import('@/views/ItemsList.vue')
      },
      {
        path: 'appointment',
        name: 'Appointment',
        component: () => import('@/views/Appointment.vue')
      },
      {
        path: 'ticket',
        name: 'Ticket',
        component: () => import('@/views/Ticket.vue')
      },
      {
        path: 'calling',
        name: 'Calling',
        component: () => import('@/views/Calling.vue')
      },
      {
        path: 'records',
        name: 'Records',
        component: () => import('@/views/Records.vue')
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'hash',
  routes
})

export default router
