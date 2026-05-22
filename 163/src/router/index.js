import Vue from 'vue'
import VueRouter from 'vue-router'
import GoodsList from '../views/GoodsList.vue'
import OrderForm from '../views/OrderForm.vue'
import LeaderManage from '../views/LeaderManage.vue'
import Verify from '../views/Verify.vue'
import Progress from '../views/Progress.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'GoodsList',
    component: GoodsList
  },
  {
    path: '/order',
    name: 'OrderForm',
    component: OrderForm
  },
  {
    path: '/leader',
    name: 'LeaderManage',
    component: LeaderManage
  },
  {
    path: '/verify',
    name: 'Verify',
    component: Verify
  },
  {
    path: '/progress',
    name: 'Progress',
    component: Progress
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router