import Vue from 'vue'
import VueRouter from 'vue-router'
import Layout from '@/views/Layout.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: Layout,
    redirect: '/send-order',
    children: [
      {
        path: 'send-order',
        name: 'SendOrder',
        component: () => import('@/views/SendOrder.vue'),
        meta: { title: '寄件下单' }
      },
      {
        path: 'pickup-verify',
        name: 'PickupVerify',
        component: () => import('@/views/PickupVerify.vue'),
        meta: { title: '取件核销' }
      },
      {
        path: 'package-inbound',
        name: 'PackageInbound',
        component: () => import('@/views/PackageInbound.vue'),
        meta: { title: '包裹入库' }
      },
      {
        path: 'package-list',
        name: 'PackageList',
        component: () => import('@/views/PackageList.vue'),
        meta: { title: '包裹列表' }
      },
      {
        path: 'member-manage',
        name: 'MemberManage',
        component: () => import('@/views/MemberManage.vue'),
        meta: { title: '会员管理' }
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'hash',
  routes
})

export default router
