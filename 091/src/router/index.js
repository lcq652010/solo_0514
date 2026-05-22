import Vue from 'vue'
import VueRouter from 'vue-router'
import PackageList from '@/views/PackageList.vue'
import Appointment from '@/views/Appointment.vue'
import ExamRecords from '@/views/ExamRecords.vue'
import ReportUpload from '@/views/ReportUpload.vue'
import ReportQuery from '@/views/ReportQuery.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/packages'
  },
  {
    path: '/packages',
    name: 'PackageList',
    component: PackageList
  },
  {
    path: '/appointment',
    name: 'Appointment',
    component: Appointment
  },
  {
    path: '/records',
    name: 'ExamRecords',
    component: ExamRecords
  },
  {
    path: '/report-upload',
    name: 'ReportUpload',
    component: ReportUpload
  },
  {
    path: '/report-query',
    name: 'ReportQuery',
    component: ReportQuery
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
