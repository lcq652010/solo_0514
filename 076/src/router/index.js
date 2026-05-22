import Vue from 'vue'
import VueRouter from 'vue-router'
import MaterialsList from '@/views/MaterialsList.vue'
import ApplyForm from '@/views/ApplyForm.vue'
import ReturnForm from '@/views/ReturnForm.vue'
import MyRecords from '@/views/MyRecords.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/materials'
  },
  {
    path: '/materials',
    name: 'MaterialsList',
    component: MaterialsList
  },
  {
    path: '/apply',
    name: 'ApplyForm',
    component: ApplyForm
  },
  {
    path: '/return',
    name: 'ReturnForm',
    component: ReturnForm
  },
  {
    path: '/records',
    name: 'MyRecords',
    component: MyRecords
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
