import Vue from 'vue'
import VueRouter from 'vue-router'
import Layout from '../layout/Index.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: Layout,
    redirect: '/products',
    children: [
      {
        path: 'products',
        name: 'Products',
        component: () => import('../views/Products.vue'),
        meta: { title: '农产品列表', icon: 'el-icon-goods' }
      },
      {
        path: 'suppliers',
        name: 'Suppliers',
        component: () => import('../views/Suppliers.vue'),
        meta: { title: '供应商管理', icon: 'el-icon-office-building' }
      },
      {
        path: 'purchase',
        name: 'Purchase',
        component: () => import('../views/Purchase.vue'),
        meta: { title: '采购下单', icon: 'el-icon-shopping-cart-2' }
      },
      {
        path: 'orders',
        name: 'Orders',
        component: () => import('../views/Orders.vue'),
        meta: { title: '采购订单列表', icon: 'el-icon-document' }
      },
      {
        path: 'stock-in',
        name: 'StockIn',
        component: () => import('../views/StockIn.vue'),
        meta: { title: '入库确认', icon: 'el-icon-box' }
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
