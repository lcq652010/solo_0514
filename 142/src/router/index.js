import Vue from 'vue'
import VueRouter from 'vue-router'
import Layout from '../views/Layout.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: Layout,
    redirect: '/stock-in',
    children: [
      {
        path: 'stock-in',
        name: 'StockIn',
        component: () => import('../views/StockIn.vue'),
        meta: { title: '商品入库' }
      },
      {
        path: 'product-list',
        name: 'ProductList',
        component: () => import('../views/ProductList.vue'),
        meta: { title: '商品列表' }
      },
      {
        path: 'stock-query',
        name: 'StockQuery',
        component: () => import('../views/StockQuery.vue'),
        meta: { title: '库存查询' }
      },
      {
        path: 'stock-warning',
        name: 'StockWarning',
        component: () => import('../views/StockWarning.vue'),
        meta: { title: '库存预警' }
      },
      {
        path: 'inventory-records',
        name: 'InventoryRecords',
        component: () => import('../views/InventoryRecords.vue'),
        meta: { title: '出入库记录' }
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'hash',
  routes
})

export default router
