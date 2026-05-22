import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/packages'
  },
  {
    path: '/packages',
    name: 'Packages',
    component: () => import('../views/Packages.vue')
  },
  {
    path: '/reserve',
    name: 'Reserve',
    component: () => import('../views/Reserve.vue')
  },
  {
    path: '/records',
    name: 'Records',
    component: () => import('../views/Records.vue')
  },
  {
    path: '/progress',
    name: 'Progress',
    component: () => import('../views/Progress.vue')
  },
  {
    path: '/evaluate',
    name: 'Evaluate',
    component: () => import('../views/Evaluate.vue')
  }
]

const router = new VueRouter({
  mode: 'hash',
  routes
})

export default router
