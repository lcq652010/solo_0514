import Vue from 'vue'
import Router from 'vue-router'
import OrderForm from '../views/OrderForm.vue'
import OrderList from '../views/OrderList.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'OrderForm',
      component: OrderForm
    },
    {
      path: '/admin',
      name: 'OrderList',
      component: OrderList
    }
  ]
})
