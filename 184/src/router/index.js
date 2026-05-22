import Vue from 'vue';
import Router from 'vue-router';
import Layout from '@/views/Layout.vue';
import StudentList from '@/views/StudentList.vue';
import Attendance from '@/views/Attendance.vue';
import DeductionRecords from '@/views/DeductionRecords.vue';
import Schedule from '@/views/Schedule.vue';
import RechargeForm from '@/views/RechargeForm.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      component: Layout,
      redirect: '/students',
      children: [
        {
          path: 'students',
          name: 'StudentList',
          component: StudentList,
          meta: { title: '学员列表' }
        },
        {
          path: 'attendance',
          name: 'Attendance',
          component: Attendance,
          meta: { title: '考勤签到' }
        },
        {
          path: 'deductions',
          name: 'DeductionRecords',
          component: DeductionRecords,
          meta: { title: '课时扣费记录' }
        },
        {
          path: 'schedule',
          name: 'Schedule',
          component: Schedule,
          meta: { title: '班级课程表' }
        },
        {
          path: 'recharge',
          name: 'RechargeForm',
          component: RechargeForm,
          meta: { title: '续费充值' }
        }
      ]
    }
  ]
});
