const PRODUCTION_STAGES = [
  { id: 0, name: '熔锡', icon: 'el-icon-fire' },
  { id: 1, name: '制模', icon: 'el-icon-s-grid' },
  { id: 2, name: '冲压', icon: 'el-icon-c-scale-to-original' },
  { id: 3, name: '修边', icon: 'el-icon-scissors' },
  { id: 4, name: '錾刻', icon: 'el-icon-edit' },
  { id: 5, name: '抛光', icon: 'el-icon-star-on' },
  { id: 6, name: '密封检测', icon: 'el-icon-check' },
  { id: 7, name: '完工', icon: 'el-icon-box' }
]

const TIN_PURITY_OPTIONS = [
  { value: '999', label: '999纯锡', price: 280 },
  { value: '970', label: '970锡料', price: 220 },
  { value: '950', label: '950锡料', price: 180 }
]

const LID_STYLE_OPTIONS = [
  { value: 'flat', label: '平盖', price: 0 },
  { value: 'dome', label: '拱盖', price: 30 },
  { value: 'carved', label: '浮雕盖', price: 60 },
  { value: 'animal', label: '兽钮盖', price: 100 }
]

const PATTERN_OPTIONS = [
  { value: 'none', label: '无花纹', price: 0 },
  { value: 'cloud', label: '祥云纹', price: 50 },
  { value: 'dragon', label: '龙凤纹', price: 120 },
  { value: 'floral', label: '花卉纹', price: 80 },
  { value: 'landscape', label: '山水纹', price: 150 },
  { value: 'bamboo', label: '竹节纹', price: 70 }
]

const formatTime = () => {
  return new Date().toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  }).replace(/\//g, '-')
}

let orders = [
  {
    id: 'ORD202405001',
    customerName: '张三',
    phone: '13800138001',
    tinPurity: '999',
    tinPurityLabel: '999纯锡',
    height: 120,
    diameter: 80,
    lidStyle: 'dome',
    lidStyleLabel: '拱盖',
    pattern: 'dragon',
    patternLabel: '龙凤纹',
    currentStage: 3,
    stageUpdateTime: '2024-05-12 10:30:00',
    totalPrice: 860,
    orderTime: '2024-05-10 14:30:00',
    remark: '加急订单'
  },
  {
    id: 'ORD202405002',
    customerName: '李四',
    phone: '13900139002',
    tinPurity: '970',
    tinPurityLabel: '970锡料',
    height: 100,
    diameter: 70,
    lidStyle: 'flat',
    lidStyleLabel: '平盖',
    pattern: 'cloud',
    patternLabel: '祥云纹',
    currentStage: 5,
    stageUpdateTime: '2024-05-14 15:20:00',
    totalPrice: 490,
    orderTime: '2024-05-12 09:15:00',
    remark: ''
  },
  {
    id: 'ORD202405003',
    customerName: '王五',
    phone: '13700137003',
    tinPurity: '950',
    tinPurityLabel: '950锡料',
    height: 150,
    diameter: 90,
    lidStyle: 'carved',
    lidStyleLabel: '浮雕盖',
    pattern: 'landscape',
    patternLabel: '山水纹',
    currentStage: 1,
    stageUpdateTime: '2024-05-15 17:00:00',
    totalPrice: 720,
    orderTime: '2024-05-15 16:45:00',
    remark: '罐身刻字：茶香四溢'
  }
]

export default {
  getOrders() {
    return orders
  },

  addOrder(order) {
    const newOrder = {
      ...order,
      id: 'ORD' + new Date().toISOString().slice(0, 10).replace(/-/g, '') + String(orders.length + 1).padStart(3, '0'),
      currentStage: 0,
      stageUpdateTime: formatTime(),
      orderTime: formatTime()
    }
    orders.unshift(newOrder)
    return newOrder
  },

  updateStage(orderId, stageId) {
    const order = orders.find(o => o.id === orderId)
    if (order) {
      order.currentStage = stageId
      order.stageUpdateTime = formatTime()
    }
  },

  getProductionStages() {
    return PRODUCTION_STAGES
  },

  getTinPurityOptions() {
    return TIN_PURITY_OPTIONS
  },

  getLidStyleOptions() {
    return LID_STYLE_OPTIONS
  },

  getPatternOptions() {
    return PATTERN_OPTIONS
  }
}
