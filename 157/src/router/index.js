import Vue from 'vue'
import VueRouter from 'vue-router'
import Categories from '@/views/Categories.vue'
import Apply from '@/views/Apply.vue'
import Records from '@/views/Records.vue'
import Inventory from '@/views/Inventory.vue'
import StockIn from '@/views/StockIn.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/categories'
  },
  {
    path: '/categories',
    name: 'Categories',
    component: Categories
  },
  {
    path: '/apply',
    name: 'Apply',
    component: Apply
  },
  {
    path: '/records',
    name: 'Records',
    component: Records
  },
  {
    path: '/inventory',
    name: 'Inventory',
    component: Inventory
  },
  {
    path: '/stock-in',
    name: 'StockIn',
    component: StockIn
  }
]

const router = new VueRouter({
  mode: 'hash',
  routes
})

export default router
