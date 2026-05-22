import Vue from 'vue'
import VueRouter from 'vue-router'
import RepairApply from '../views/RepairApply.vue'
import MyRepairs from '../views/MyRepairs.vue'
import Dispatch from '../views/Dispatch.vue'
import Progress from '../views/Progress.vue'
import Evaluation from '../views/Evaluation.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/apply'
  },
  {
    path: '/apply',
    name: 'RepairApply',
    component: RepairApply
  },
  {
    path: '/my-repairs',
    name: 'MyRepairs',
    component: MyRepairs
  },
  {
    path: '/dispatch',
    name: 'Dispatch',
    component: Dispatch
  },
  {
    path: '/progress/:id',
    name: 'Progress',
    component: Progress
  },
  {
    path: '/evaluation/:id',
    name: 'Evaluation',
    component: Evaluation
  }
]

const router = new VueRouter({
  mode: 'hash',
  routes
})

export default router
