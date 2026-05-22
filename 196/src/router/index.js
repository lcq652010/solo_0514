import Vue from 'vue'
import VueRouter from 'vue-router'
import RoomList from '@/views/RoomList.vue'
import BookingForm from '@/views/BookingForm.vue'
import MeetingRecords from '@/views/MeetingRecords.vue'
import EquipmentBorrow from '@/views/EquipmentBorrow.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/rooms'
  },
  {
    path: '/rooms',
    name: 'RoomList',
    component: RoomList
  },
  {
    path: '/booking',
    name: 'BookingForm',
    component: BookingForm
  },
  {
    path: '/records',
    name: 'MeetingRecords',
    component: MeetingRecords
  },
  {
    path: '/equipment',
    name: 'EquipmentBorrow',
    component: EquipmentBorrow
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
