import Vue from 'vue';
import VueRouter from 'vue-router';
import Layout from '@/views/Layout.vue';
import TicketList from '@/views/TicketList.vue';
import BookingForm from '@/views/BookingForm.vue';
import OrderList from '@/views/OrderList.vue';
import CheckTicket from '@/views/CheckTicket.vue';
import Statistics from '@/views/Statistics.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    component: Layout,
    redirect: '/tickets',
    children: [
      {
        path: 'tickets',
        name: 'TicketList',
        component: TicketList,
        meta: { title: '门票类型' }
      },
      {
        path: 'booking/:ticketId?',
        name: 'BookingForm',
        component: BookingForm,
        meta: { title: '在线预订' }
      },
      {
        path: 'orders',
        name: 'OrderList',
        component: OrderList,
        meta: { title: '订单列表' }
      },
      {
        path: 'check',
        name: 'CheckTicket',
        component: CheckTicket,
        meta: { title: '检票核销' }
      },
      {
        path: 'statistics',
        name: 'Statistics',
        component: Statistics,
        meta: { title: '客流统计' }
      }
    ]
  }
];

const router = new VueRouter({
  mode: 'hash',
  routes
});

export default router;
