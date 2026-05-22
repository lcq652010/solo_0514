const PROCESS_STEPS = [
  { id: 1, name: '熔锡', completed: false, completedTime: null, operator: null },
  { id: 2, name: '锻打', completed: false, completedTime: null, operator: null },
  { id: 3, name: '车旋', completed: false, completedTime: null, operator: null },
  { id: 4, name: '錾刻', completed: false, completedTime: null, operator: null },
  { id: 5, name: '抛光', completed: false, completedTime: null, operator: null },
  { id: 6, name: '密封装配', completed: false, completedTime: null, operator: null },
  { id: 7, name: '质检', completed: false, completedTime: null, operator: null },
  { id: 8, name: '完工', completed: false, completedTime: null, operator: null }
]

let orderIdCounter = 1001

const OPERATORS = [
  { id: 'admin', name: '管理员' },
  { id: 'worker_01', name: '张师傅' },
  { id: 'worker_02', name: '李师傅' },
  { id: 'worker_03', name: '王师傅' }
]

function generateOrderId() {
  return 'ORD' + orderIdCounter++
}

function getCurrentTime() {
  return new Date().toLocaleString('zh-CN')
}

const orderStore = {
  orders: [],
  listeners: [],
  currentOperator: OPERATORS[0],
  
  subscribe(callback) {
    this.listeners.push(callback)
    return () => {
      this.listeners = this.listeners.filter(l => l !== callback)
    }
  },
  
  notify() {
    this.listeners.forEach(callback => callback())
  },
  
  getOperators() {
    return OPERATORS
  },
  
  setCurrentOperator(operator) {
    this.currentOperator = operator
  },
  
  getCurrentOperator() {
    return this.currentOperator
  },
  
  addOrder(orderData) {
    const newOrder = {
      id: generateOrderId(),
      ...orderData,
      createTime: getCurrentTime(),
      isNew: true,
      status: '生产中',
      currentStep: 0,
      processSteps: JSON.parse(JSON.stringify(PROCESS_STEPS))
    }
    this.orders.push(newOrder)
    this.notify()
    return newOrder
  },
  
  getOrders() {
    return this.orders
  },
  
  getLatestOrderId() {
    if (this.orders.length === 0) return null
    return this.orders[this.orders.length - 1].id
  },
  
  markOrderAsRead(orderId) {
    const order = this.orders.find(o => o.id === orderId)
    if (order) {
      order.isNew = false
      this.notify()
      return true
    }
    return false
  },
  
  advanceProcess(orderId) {
    const order = this.orders.find(o => o.id === orderId)
    if (order && order.currentStep < order.processSteps.length) {
      const currentStepData = order.processSteps[order.currentStep]
      
      if (currentStepData.completed) {
        return false
      }
      
      currentStepData.completed = true
      currentStepData.completedTime = getCurrentTime()
      currentStepData.operator = { ...this.currentOperator }
      order.currentStep++
      
      if (order.currentStep === order.processSteps.length) {
        order.status = '已完成'
      }
      
      this.notify()
      return true
    }
    return false
  },
  
  resetProcess(orderId) {
    const order = this.orders.find(o => o.id === orderId)
    if (order) {
      order.currentStep = 0
      order.status = '生产中'
      order.processSteps.forEach(step => {
        step.completed = false
        step.completedTime = null
        step.operator = null
      })
      this.notify()
      return true
    }
    return false
  }
}

export default orderStore
