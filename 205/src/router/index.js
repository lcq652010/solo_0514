import Vue from 'vue'
import VueRouter from 'vue-router'
import Layout from '@/layout/index.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: Layout,
    redirect: '/jobs',
    children: [
      {
        path: 'jobs',
        name: 'Jobs',
        component: () => import('@/views/jobs/index.vue'),
        meta: { title: '岗位列表', icon: 'el-icon-suitcase' }
      },
      {
        path: 'resume',
        name: 'Resume',
        component: () => import('@/views/resume/index.vue'),
        meta: { title: '简历投递', icon: 'el-icon-document' }
      },
      {
        path: 'interview',
        name: 'Interview',
        component: () => import('@/views/interview/index.vue'),
        meta: { title: '面试安排', icon: 'el-icon-time' }
      },
      {
        path: 'applications',
        name: 'Applications',
        component: () => import('@/views/applications/index.vue'),
        meta: { title: '应聘记录', icon: 'el-icon-notebook-2' }
      },
      {
        path: 'offer',
        name: 'Offer',
        component: () => import('@/views/offer/index.vue'),
        meta: { title: '录用管理', icon: 'el-icon-medal-1' }
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
