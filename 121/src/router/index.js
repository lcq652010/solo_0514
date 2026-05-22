import Vue from 'vue';
import Router from 'vue-router';
import OrderForm from '@/views/OrderForm.vue';
import PickupList from '@/views/PickupList.vue';
import TrackingPage from '@/views/TrackingPage.vue';
import SignConfirm from '@/views/SignConfirm.vue';
import PackageQuery from '@/views/PackageQuery.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      redirect: '/order'
    },
    {
      path: '/order',
      name: 'OrderForm',
      component: OrderForm
    },
    {
      path: '/pickup',
      name: 'PickupList',
      component: PickupList
    },
    {
      path: '/tracking',
      name: 'TrackingPage',
      component: TrackingPage
    },
    {
      path: '/sign',
      name: 'SignConfirm',
      component: SignConfirm
    },
    {
      path: '/query',
      name: 'PackageQuery',
      component: PackageQuery
    }
  ]
});
