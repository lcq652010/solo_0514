import Vue from 'vue'
import VueRouter from 'vue-router'
import TicketList from '@/views/TicketList.vue'
import BookingForm from '@/views/BookingForm.vue'
import OrderList from '@/views/OrderList.vue'
import CheckTicket from '@/views/CheckTicket.vue'
import UserCenter from '@/views/UserCenter.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/tickets'
  },
  {
    path: '/tickets',
    name: 'TicketList',
    component: TicketList
  },
  {
    path: '/booking/:ticketId?',
    name: 'BookingForm',
    component: BookingForm
  },
  {
    path: '/orders',
    name: 'OrderList',
    component: OrderList
  },
  {
    path: '/check',
    name: 'CheckTicket',
    component: CheckTicket
  },
  {
    path: '/user',
    name: 'UserCenter',
    component: UserCenter
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
