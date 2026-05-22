const orderStore = {
  listeners: [],

  onOrderAdded(callback) {
    this.listeners.push(callback)
  },

  notifyOrderAdded() {
    this.listeners.forEach(callback => callback())
  },

  sizeRules: {
    length: { min: 5, max: 50, step: 0.5 },
    width: { min: 2, max: 20, step: 0.5 },
    height: { min: 1, max: 10, step: 0.5 }
  },

  orders: [
    {
      id: 'ORD001',
      woodType: '紫檀木',
      beastStyle: '麒麟',
      length: 15,
      width: 5,
      height: 3,
      isGilded: true,
      remark: '希望雕刻要精细',
      status: 3,
      createTime: '2024-01-15 10:30:00',
      statusUpdateTime: '2024-01-15 14:20:00'
    },
    {
      id: 'ORD002',
      woodType: '黄花梨',
      beastStyle: '貔貅',
      length: 12,
      width: 4,
      height: 2.5,
      isGilded: false,
      remark: '',
      status: 5,
      createTime: '2024-01-16 14:20:00',
      statusUpdateTime: '2024-01-17 09:15:00'
    }
  ],

  statusOptions: [
    { value: 0, label: '选料' },
    { value: 1, label: '开坯' },
    { value: 2, label: '粗雕' },
    { value: 3, label: '细雕' },
    { value: 4, label: '打磨' },
    { value: 5, label: '打蜡' },
    { value: 6, label: '完工' }
  ],

  woodTypes: [
    { value: '紫檀木', label: '紫檀木', price: 800 },
    { value: '黄花梨', label: '黄花梨', price: 600 },
    { value: '酸枝木', label: '酸枝木', price: 400 },
    { value: '鸡翅木', label: '鸡翅木', price: 300 },
    { value: '楠木', label: '楠木', price: 250 },
    { value: '樟木', label: '樟木', price: 200 }
  ],

  beastStyles: [
    { value: '麒麟', label: '麒麟', desc: '祥瑞之兽，招财纳福' },
    { value: '貔貅', label: '貔貅', desc: '招财进宝，只进不出' },
    { value: '龙', label: '龙', desc: '权势尊贵，吉祥如意' },
    { value: '凤', label: '凤', desc: '百鸟之王，美丽祥瑞' },
    { value: '狮子', label: '狮子', desc: '勇猛威严，镇宅辟邪' },
    { value: '大象', label: '大象', desc: '吉祥如意，万象更新' }
  ],

  getOrders() {
    return this.orders
  },

  addOrder(order) {
    const newOrder = {
      ...order,
      id: 'ORD' + String(this.orders.length + 1).padStart(3, '0'),
      status: 0,
      createTime: new Date().toLocaleString('zh-CN'),
      statusUpdateTime: new Date().toLocaleString('zh-CN')
    }
    this.orders.unshift(newOrder)
    this.notifyOrderAdded()
    return newOrder
  },

  updateStatus(orderId, status) {
    const order = this.orders.find(o => o.id === orderId)
    if (order) {
      order.status = status
      order.statusUpdateTime = new Date().toLocaleString('zh-CN')
    }
    return order
  },

  getStatusLabel(statusValue) {
    const status = this.statusOptions.find(s => s.value === statusValue)
    return status ? status.label : '未知'
  },

  getWoodPrice(woodType) {
    const wood = this.woodTypes.find(w => w.value === woodType)
    return wood ? wood.price : 0
  }
}

export default orderStore
