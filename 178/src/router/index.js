import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    redirect: '/books'
  },
  {
    path: '/books',
    name: 'Books',
    component: () => import('@/views/Books.vue')
  },
  {
    path: '/borrow/apply',
    name: 'BorrowApply',
    component: () => import('@/views/BorrowApply.vue')
  },
  {
    path: '/borrow/records',
    name: 'BorrowRecords',
    component: () => import('@/views/BorrowRecords.vue')
  },
  {
    path: '/return',
    name: 'BookReturn',
    component: () => import('@/views/BookReturn.vue')
  },
  {
    path: '/overdue',
    name: 'OverdueReminder',
    component: () => import('@/views/OverdueReminder.vue')
  }
];

const router = new VueRouter({
  mode: 'hash',
  routes
});

export default router;