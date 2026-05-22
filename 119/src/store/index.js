import Vue from 'vue'

export const store = Vue.observable({
  orders: [
    {
      id: 'ORD001',
      customerName: '张三',
      phone: '13800138001',
      clayType: '紫砂泥',
      shape: '貔貅',
      height: 12,
      width: 8,
      glazeEffect: '哑光釉',
      status: 3,
      createTime: '2024-01-15 10:30:00'
    },
    {
      id: 'ORD002',
      customerName: '李四',
      phone: '13800138002',
      clayType: '陶泥',
      shape: '金蟾',
      height: 10,
      width: 10,
      glazeEffect: '亮面釉',
      status: 5,
      createTime: '2024-01-16 14:20:00'
    },
    {
      id: 'ORD003',
      customerName: '王五',
      phone: '13800138003',
      clayType: '紫砂泥',
      shape: '麒麟',
      height: 15,
      width: 10,
      glazeEffect: '窑变釉',
      status: 7,
      createTime: '2024-01-17 09:15:00'
    }
  ],
  processSteps: ['揉泥', '拉坯', '塑形', '晾干', '施釉', '烧制', '质检', '完工']
})

export const mutations = {
  addOrder(order) {
    const newOrder = {
      ...order,
      id: 'ORD' + String(store.orders.length + 1).padStart(3, '0'),
      status: 0,
      createTime: new Date().toLocaleString('zh-CN')
    }
    store.orders.unshift(newOrder)
  },
  updateOrderStatus(orderId, status) {
    const order = store.orders.find(o => o.id === orderId)
    if (order) {
      order.status = status
    }
  }
}
