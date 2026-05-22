import Vue from 'vue';
import VueRouter from 'vue-router';
import DepartmentList from '@/views/DepartmentList.vue';
import DoctorSchedule from '@/views/DoctorSchedule.vue';
import RegistrationForm from '@/views/RegistrationForm.vue';
import RegistrationRecord from '@/views/RegistrationRecord.vue';
import CheckIn from '@/views/CheckIn.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    redirect: '/departments'
  },
  {
    path: '/departments',
    name: 'DepartmentList',
    component: DepartmentList,
    meta: { title: '科室列表' }
  },
  {
    path: '/schedule',
    name: 'DoctorSchedule',
    component: DoctorSchedule,
    meta: { title: '医生排班' }
  },
  {
    path: '/register',
    name: 'RegistrationForm',
    component: RegistrationForm,
    meta: { title: '在线挂号' }
  },
  {
    path: '/records',
    name: 'RegistrationRecord',
    component: RegistrationRecord,
    meta: { title: '挂号记录' }
  },
  {
    path: '/checkin',
    name: 'CheckIn',
    component: CheckIn,
    meta: { title: '就诊签到' }
  }
];

const router = new VueRouter({
  mode: 'hash',
  routes
});

export default router;
