import OrderForm from '../views/OrderForm.vue'
import AdminPanel from '../views/AdminPanel.vue'

export default [
  {
    path: '/',
    redirect: '/order'
  },
  {
    path: '/order',
    name: 'OrderForm',
    component: OrderForm
  },
  {
    path: '/admin',
    name: 'AdminPanel',
    component: AdminPanel
  }
]
