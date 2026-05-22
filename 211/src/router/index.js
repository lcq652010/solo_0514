window.router = new VueRouter({
  mode: 'hash',
  routes: [
    { path: '/', redirect: '/packages' },
    { path: '/packages', component: window.Packages, meta: { title: '摄影套餐' } },
    { path: '/booking', component: window.Booking, meta: { title: '预订表单' } },
    { path: '/schedule', component: window.Schedule, meta: { title: '摄影师档期' } },
    { path: '/orders', component: window.Orders, meta: { title: '订单列表' } },
    { path: '/customers', component: window.Customers, meta: { title: '客户档案' } }
  ]
});
