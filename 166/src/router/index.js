import VueRouter from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/book-list'
  },
  {
    path: '/book-entry',
    name: 'BookEntry',
    component: () => import('../views/BookEntry.vue')
  },
  {
    path: '/pricing',
    name: 'Pricing',
    component: () => import('../views/Pricing.vue')
  },
  {
    path: '/book-list',
    name: 'BookList',
    component: () => import('../views/BookList.vue')
  },
  {
    path: '/order',
    name: 'Order',
    component: () => import('../views/Order.vue')
  },
  {
    path: '/recycle-records',
    name: 'RecycleRecords',
    component: () => import('../views/RecycleRecords.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
