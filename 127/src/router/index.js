import Vue from 'vue';
import Router from 'vue-router';
import OvertimeApply from '@/views/OvertimeApply.vue';
import MyRecords from '@/views/MyRecords.vue';
import ApprovalList from '@/views/ApprovalList.vue';
import Statistics from '@/views/Statistics.vue';
import Ledger from '@/views/Ledger.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      redirect: '/apply'
    },
    {
      path: '/apply',
      name: 'OvertimeApply',
      component: OvertimeApply
    },
    {
      path: '/my-records',
      name: 'MyRecords',
      component: MyRecords
    },
    {
      path: '/approval-list',
      name: 'ApprovalList',
      component: ApprovalList
    },
    {
      path: '/statistics',
      name: 'Statistics',
      component: Statistics
    },
    {
      path: '/ledger',
      name: 'Ledger',
      component: Ledger
    }
  ]
});
