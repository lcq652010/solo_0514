import Vue from 'vue'
import VueRouter from 'vue-router'
import Layout from '@/layout/Index.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: Layout,
    redirect: '/courses',
    children: [
      {
        path: 'courses',
        name: 'Courses',
        component: () => import('@/views/Courses.vue'),
        meta: { title: '课程列表' }
      },
      {
        path: 'schedule',
        name: 'Schedule',
        component: () => import('@/views/Schedule.vue'),
        meta: { title: '班级排课' }
      },
      {
        path: 'students',
        name: 'Students',
        component: () => import('@/views/Students.vue'),
        meta: { title: '学员花名册' }
      },
      {
        path: 'attendance',
        name: 'Attendance',
        component: () => import('@/views/Attendance.vue'),
        meta: { title: '考勤打卡' }
      },
      {
        path: 'statistics',
        name: 'Statistics',
        component: () => import('@/views/Statistics.vue'),
        meta: { title: '考勤统计' }
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'hash',
  routes
})

export default router