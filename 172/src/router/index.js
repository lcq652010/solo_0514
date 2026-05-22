import Vue from 'vue'
import VueRouter from 'vue-router'
import SubjectList from '@/views/SubjectList.vue'
import ApplyForm from '@/views/ApplyForm.vue'
import ReviewPage from '@/views/ReviewPage.vue'
import TicketPage from '@/views/TicketPage.vue'
import RecordList from '@/views/RecordList.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'SubjectList',
    component: SubjectList
  },
  {
    path: '/apply',
    name: 'ApplyForm',
    component: ApplyForm
  },
  {
    path: '/review',
    name: 'ReviewPage',
    component: ReviewPage
  },
  {
    path: '/ticket',
    name: 'TicketPage',
    component: TicketPage
  },
  {
    path: '/records',
    name: 'RecordList',
    component: RecordList
  }
]

const router = new VueRouter({
  mode: 'hash',
  routes
})

export default router
