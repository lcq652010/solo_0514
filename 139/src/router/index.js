import Vue from 'vue'
import VueRouter from 'vue-router'
import CourseList from '@/views/CourseList.vue'
import EnrollForm from '@/views/EnrollForm.vue'
import LearningProgress from '@/views/LearningProgress.vue'
import HomeworkSubmit from '@/views/HomeworkSubmit.vue'
import MyCourses from '@/views/MyCourses.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/courses'
  },
  {
    path: '/courses',
    name: 'CourseList',
    component: CourseList
  },
  {
    path: '/enroll',
    name: 'EnrollForm',
    component: EnrollForm
  },
  {
    path: '/progress',
    name: 'LearningProgress',
    component: LearningProgress
  },
  {
    path: '/homework',
    name: 'HomeworkSubmit',
    component: HomeworkSubmit
  },
  {
    path: '/my-courses',
    name: 'MyCourses',
    component: MyCourses
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
