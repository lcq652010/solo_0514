import Vue from 'vue'
import VueRouter from 'vue-router'
import ServicePackages from '../views/ServicePackages.vue'
import AppointmentForm from '../views/AppointmentForm.vue'
import MemberInfo from '../views/MemberInfo.vue'
import AppointmentList from '../views/AppointmentList.vue'
import Checkout from '../views/Checkout.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/services'
  },
  {
    path: '/services',
    name: 'ServicePackages',
    component: ServicePackages
  },
  {
    path: '/appointment',
    name: 'AppointmentForm',
    component: AppointmentForm
  },
  {
    path: '/members',
    name: 'MemberInfo',
    component: MemberInfo
  },
  {
    path: '/appointments',
    name: 'AppointmentList',
    component: AppointmentList
  },
  {
    path: '/checkout',
    name: 'Checkout',
    component: Checkout
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
