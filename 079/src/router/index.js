import Vue from 'vue'
import VueRouter from 'vue-router'
import MemberList from '@/views/MemberList'
import MemberDetail from '@/views/MemberDetail'
import RechargeForm from '@/views/RechargeForm'
import ConsumeForm from '@/views/ConsumeForm'
import TransactionList from '@/views/TransactionList'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/members'
  },
  {
    path: '/members',
    name: 'MemberList',
    component: MemberList
  },
  {
    path: '/member/:id',
    name: 'MemberDetail',
    component: MemberDetail
  },
  {
    path: '/recharge/:memberId?',
    name: 'RechargeForm',
    component: RechargeForm
  },
  {
    path: '/consume/:memberId?',
    name: 'ConsumeForm',
    component: ConsumeForm
  },
  {
    path: '/transactions',
    name: 'TransactionList',
    component: TransactionList
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
