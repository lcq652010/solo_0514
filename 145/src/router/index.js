import Vue from 'vue';
import VueRouter from 'vue-router';
import ClassType from '@/views/ClassType.vue';
import StudentReg from '@/views/StudentReg.vue';
import CoachList from '@/views/CoachList.vue';
import Reservation from '@/views/Reservation.vue';
import ReservationList from '@/views/ReservationList.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    redirect: '/class-type'
  },
  {
    path: '/class-type',
    name: 'ClassType',
    component: ClassType
  },
  {
    path: '/student-reg',
    name: 'StudentReg',
    component: StudentReg
  },
  {
    path: '/coach-list',
    name: 'CoachList',
    component: CoachList
  },
  {
    path: '/reservation',
    name: 'Reservation',
    component: Reservation
  },
  {
    path: '/reservation-list',
    name: 'ReservationList',
    component: ReservationList
  }
];

const router = new VueRouter({
  mode: 'history',
  routes
});

export default router;
