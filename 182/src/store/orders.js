const PROCESSES = [
  { id: 1, name: '裁布', icon: 'el-icon-scissors' },
  { id: 2, name: '缝纫', icon: 'el-icon-reading' },
  { id: 3, name: '填香', icon: 'el-icon-goods' },
  { id: 4, name: '收口', icon: 'el-icon-lock' },
  { id: 5, name: '串珠', icon: 'el-icon-coin' },
  { id: 6, name: '挂绳装配', icon: 'el-icon-connection' },
  { id: 7, name: '质检', icon: 'el-icon-check' },
  { id: 8, name: '完工', icon: 'el-icon-box' }
]

const MOCK_ORDERS = [
  {
    id: 'ORD001',
    customerName: '张三',
    phone: '13800138001',
    fabric: '棉麻',
    shape: '圆形',
    size: '8cm',
    formula: '薰衣草',
    rope: '中国结',
    quantity: 5,
    remark: '希望颜色淡雅一些',
    currentProcess: 3,
    createTime: '2024-01-15 10:30:00',
    processTimestamps: {
      1: '2024-01-15 10:35:00',
      2: '2024-01-15 11:00:00',
      3: '2024-01-15 11:30:00'
    },
    processOperators: {
      1: '李师傅',
      2: '王师傅',
      3: '张师傅'
    }
  },
  {
    id: 'ORD002',
    customerName: '李四',
    phone: '13800138002',
    fabric: '丝绸',
    shape: '心形',
    size: '10cm',
    formula: '艾草',
    rope: '流苏',
    quantity: 10,
    remark: '加急订单',
    currentProcess: 6,
    createTime: '2024-01-15 11:20:00',
    processTimestamps: {
      1: '2024-01-15 11:25:00',
      2: '2024-01-15 11:50:00',
      3: '2024-01-15 12:20:00',
      4: '2024-01-15 14:00:00',
      5: '2024-01-15 14:30:00',
      6: '2024-01-15 15:00:00'
    },
    processOperators: {
      1: '赵师傅',
      2: '钱师傅',
      3: '孙师傅',
      4: '李师傅',
      5: '王师傅',
      6: '张师傅'
    }
  },
  {
    id: 'ORD003',
    customerName: '王五',
    phone: '13800138003',
    fabric: '绸缎',
    shape: '方形',
    size: '7cm',
    formula: '檀香',
    rope: '皮绳',
    quantity: 3,
    remark: '',
    currentProcess: 8,
    createTime: '2024-01-14 15:45:00',
    processTimestamps: {
      1: '2024-01-14 15:50:00',
      2: '2024-01-14 16:20:00',
      3: '2024-01-14 16:50:00',
      4: '2024-01-14 17:20:00',
      5: '2024-01-14 17:50:00',
      6: '2024-01-15 09:00:00',
      7: '2024-01-15 09:30:00',
      8: '2024-01-15 10:00:00'
    },
    processOperators: {
      1: '陈师傅',
      2: '刘师傅',
      3: '杨师傅',
      4: '赵师傅',
      5: '钱师傅',
      6: '孙师傅',
      7: '李师傅',
      8: '王师傅'
    }
  }
]

let orders = [...MOCK_ORDERS]

export default {
  getProcesses() {
    return PROCESSES
  },
  
  getOrders() {
    return orders
  },
  
  addOrder(order) {
    const newOrder = {
      id: 'ORD' + String(orders.length + 1).padStart(3, '0'),
      ...order,
      currentProcess: 0,
      createTime: new Date().toLocaleString('zh-CN'),
      processTimestamps: {},
      processOperators: {}
    }
    orders.unshift(newOrder)
    return newOrder
  },
  
  updateProcess(orderId, processId, operator) {
    const order = orders.find(o => o.id === orderId)
    if (order) {
      order.currentProcess = processId
      if (!order.processTimestamps) {
        order.processTimestamps = {}
      }
      if (!order.processOperators) {
        order.processOperators = {}
      }
      order.processTimestamps[processId] = new Date().toLocaleString('zh-CN')
      order.processOperators[processId] = operator || '管理员'
    }
    return order
  },
  
  deleteOrder(orderId) {
    const index = orders.findIndex(o => o.id === orderId)
    if (index > -1) {
      orders.splice(index, 1)
      return true
    }
    return false
  }
}
