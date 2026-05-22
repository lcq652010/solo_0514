import Vue from 'vue'
import VueRouter from 'vue-router'
import Statistics from '../views/Statistics.vue'
import Categories from '../views/Categories.vue'
import Dishes from '../views/Dishes.vue'
import Orders from '../views/Orders.vue'
import OrderOperations from '../views/OrderOperations.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/statistics'
  },
  {
    path: '/statistics',
    name: 'Statistics',
    component: Statistics
  },
  {
    path: '/categories',
    name: 'Categories',
    component: Categories
  },
  {
    path: '/dishes',
    name: 'Dishes',
    component: Dishes
  },
  {
    path: '/orders',
    name: 'Orders',
    component: Orders
  },
  {
    path: '/order-operations',
    name: 'OrderOperations',
    component: OrderOperations
  }
]

const router = new VueRouter({
  mode: 'hash',
  routes
})

export default router