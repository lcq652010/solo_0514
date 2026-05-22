import Vue from 'vue';
import Router from 'vue-router';
import SeatMap from '@/views/SeatMap.vue';
import Reservation from '@/views/Reservation.vue';
import MyReservations from '@/views/MyReservations.vue';
import CheckIn from '@/views/CheckIn.vue';
import Violations from '@/views/Violations.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'SeatMap',
      component: SeatMap
    },
    {
      path: '/reservation',
      name: 'Reservation',
      component: Reservation
    },
    {
      path: '/my-reservations',
      name: 'MyReservations',
      component: MyReservations
    },
    {
      path: '/check-in',
      name: 'CheckIn',
      component: CheckIn
    },
    {
      path: '/violations',
      name: 'Violations',
      component: Violations
    }
  ]
});
