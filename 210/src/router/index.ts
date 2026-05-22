import Vue from 'vue'
import VueRouter from 'vue-router'
import HomePage from '@/pages/HomePage.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomePage,
  },
]

const router = new VueRouter({
  mode: 'history',
  routes,
})

export default router
