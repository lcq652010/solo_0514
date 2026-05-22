import InboundForm from '../components/InboundForm.vue';
import OutboundSign from '../components/OutboundSign.vue';
import SendRegister from '../components/SendRegister.vue';
import ExpressList from '../components/ExpressList.vue';
import PickupCode from '../components/PickupCode.vue';

export default [
  {
    path: '/',
    redirect: '/inbound'
  },
  {
    path: '/inbound',
    name: 'InboundForm',
    component: InboundForm,
    meta: { title: '快递入库' }
  },
  {
    path: '/outbound',
    name: 'OutboundSign',
    component: OutboundSign,
    meta: { title: '快递出库签收' }
  },
  {
    path: '/send',
    name: 'SendRegister',
    component: SendRegister,
    meta: { title: '寄件登记' }
  },
  {
    path: '/list',
    name: 'ExpressList',
    component: ExpressList,
    meta: { title: '快递查询' }
  },
  {
    path: '/pickup',
    name: 'PickupCode',
    component: PickupCode,
    meta: { title: '取件码展示' }
  }
];
