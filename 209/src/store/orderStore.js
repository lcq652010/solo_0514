const PROCESS_STEPS = [
  { id: 0, name: '揉泥', icon: 'el-icon-document-copy' },
  { id: 1, name: '拉坯', icon: 'el-icon-edit' },
  { id: 2, name: '利坯', icon: 'el-icon-crop' },
  { id: 3, name: '施釉', icon: 'el-icon-brush' },
  { id: 4, name: '绘饰', icon: 'el-icon-edit-outline' },
  { id: 5, name: '烧制', icon: 'el-icon-sunny' },
  { id: 6, name: '打磨', icon: 'el-icon-connection' },
  { id: 7, name: '完工', icon: 'el-icon-check-circle' }
]

const CLAY_TYPES = [
  { value: 'purple', label: '紫砂泥', desc: '宜兴紫砂，透气性佳' },
  { value: 'zhuni', label: '朱泥', desc: '色泽红润，质地细腻' },
  { value: 'duanni', label: '段泥', desc: '素雅温润，泡养效果好' },
  { value: 'qinghui', label: '青灰泥', desc: '古朴典雅，颗粒感强' },
  { value: 'heimiao', label: '黑泥', desc: '深沉厚重，沉稳大气' }
]

const GLAZE_STYLES = [
  { value: 'tianmu', label: '天目釉', desc: '油滴兔毫，变幻万千' },
  { value: 'jun', label: '钧釉', desc: '入窑一色，出窑万彩' },
  { value: 'ru', label: '汝釉', desc: '雨过天青，温润如玉' },
  { value: 'ge', label: '哥釉', desc: '金丝铁线，开片自然' },
  { value: 'ding', label: '定釉', desc: '白釉素洁，典雅高贵' },
  { value: 'celadon', label: '青瓷釉', desc: '千峰翠色，温润典雅' }
]

const PATTERNS = [
  { value: 'none', label: '无纹饰', desc: '素面朝天，返璞归真' },
  { value: 'yunwen', label: '云纹', desc: '祥云缭绕，吉祥如意' },
  { value: 'lianwen', label: '莲纹', desc: '出淤泥而不染' },
  { value: 'zhuwentie', label: '竹纹', desc: '高风亮节，君子之风' },
  { value: 'meiwen', label: '梅纹', desc: '凌寒独自开，暗香浮动' },
  { value: 'shanshui', label: '山水纹', desc: '意境悠远，诗情画意' }
]

const SHAPES = [
  { value: 'zhong', label: '钟型', desc: '稳重端庄，握感舒适' },
  { value: 'dou', label: '斗笠型', desc: '撇口斜壁，形似斗笠' },
  { value: 'gang', label: '缸型', desc: '圆润饱满，容量适中' },
  { value: 'hua', label: '花口型', desc: '口沿如花，雅致精巧' },
  { value: 'jingping', label: '净瓶型', desc: '线条优美，典雅脱俗' },
  { value: 'fang', label: '方型', desc: '方正不阿，棱角分明' }
]

const QUICK_SIZES = [
  { size: 6.5, label: '小品', desc: '6.5cm 品茗把玩' },
  { size: 8, label: '常规', desc: '8cm 日常使用' },
  { size: 9, label: '推荐', desc: '9cm 黄金尺寸' },
  { size: 10, label: '大容量', desc: '10cm 冲泡利器' },
  { size: 11, label: '大盏', desc: '11cm 茶席主角' }
]

function formatTime(date) {
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  }).replace(/\//g, '-')
}

function generateStepTimes(currentStep) {
  const stepTimes = []
  const baseTime = new Date()
  for (let i = 0; i <= 7; i++) {
    if (i <= currentStep) {
      const time = new Date(baseTime.getTime() - (7 - i) * 3600000 - Math.random() * 1800000)
      stepTimes.push(formatTime(time))
    } else {
      stepTimes.push('')
    }
  }
  return stepTimes
}

function getRecentTime(hoursAgo) {
  const time = new Date(Date.now() - hoursAgo * 3600000)
  return formatTime(time)
}

const mockOrders = [
  {
    id: 'ORD2024001',
    customerName: '张先生',
    phone: '138****1234',
    clayType: '紫砂泥',
    size: 9,
    glazeStyle: '天目釉',
    pattern: '云纹',
    shape: '钟型',
    currentStep: 3,
    stepTimes: generateStepTimes(3),
    createTime: getRecentTime(2),
    remark: '希望釉色稍深一些',
    price: 688
  },
  {
    id: 'ORD2024002',
    customerName: '李女士',
    phone: '139****5678',
    clayType: '朱泥',
    size: 8,
    glazeStyle: '汝釉',
    pattern: '莲纹',
    shape: '斗笠型',
    currentStep: 7,
    stepTimes: generateStepTimes(7),
    createTime: getRecentTime(12),
    remark: '礼品包装',
    price: 888
  },
  {
    id: 'ORD2024003',
    customerName: '王先生',
    phone: '137****9012',
    clayType: '段泥',
    size: 10,
    glazeStyle: '钧釉',
    pattern: '山水纹',
    shape: '缸型',
    currentStep: 1,
    stepTimes: generateStepTimes(1),
    createTime: getRecentTime(48),
    remark: '',
    price: 768
  },
  {
    id: 'ORD2024004',
    customerName: '陈女士',
    phone: '136****3456',
    clayType: '青灰泥',
    size: 7.5,
    glazeStyle: '青瓷釉',
    pattern: '竹纹',
    shape: '花口型',
    currentStep: 5,
    stepTimes: generateStepTimes(5),
    createTime: getRecentTime(72),
    remark: '做工精细些',
    price: 998
  }
]

const orderStore = {
  orders: [...mockOrders],

  getOrders() {
    return this.orders
  },

  addOrder(order) {
    const newOrder = {
      ...order,
      id: 'ORD' + new Date().getFullYear() + String(this.orders.length + 1).padStart(3, '0'),
      currentStep: 0,
      stepTimes: ['', '', '', '', '', '', '', ''],
      createTime: new Date().toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      }).replace(/\//g, '-')
    }
    newOrder.stepTimes[0] = newOrder.createTime
    this.orders.unshift(newOrder)
    return newOrder
  },

  updateStep(orderId, step) {
    const order = this.orders.find(o => o.id === orderId)
    if (!order) return false
    if (step < order.currentStep) {
      return { success: false, message: '工序状态不可逆向回退，请按顺序推进生产流程' }
    }
    if (step > 7) {
      return { success: false, message: '工序状态无效' }
    }
    if (step === order.currentStep) {
      return { success: true, message: '当前已是该工序状态' }
    }
    for (let i = order.currentStep + 1; i <= step; i++) {
      order.stepTimes[i] = formatTime(new Date())
    }
    order.currentStep = step
    return { success: true, message: '工序状态更新成功' }
  },

  getStepName(step) {
    return PROCESS_STEPS[step]?.name || '未知'
  }
}

export { PROCESS_STEPS, CLAY_TYPES, GLAZE_STYLES, PATTERNS, SHAPES, QUICK_SIZES, orderStore }
