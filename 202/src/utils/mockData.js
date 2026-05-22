const dormitories = [
  { id: 1, building: '1号楼', room: '101', capacity: 4, currentResidents: ['张三', '李四', '王五', '赵六'] },
  { id: 2, building: '1号楼', room: '102', capacity: 4, currentResidents: ['小明', '小红', '小刚', '小丽'] },
  { id: 3, building: '1号楼', room: '201', capacity: 4, currentResidents: ['张伟', '李娜', '王磊', '赵敏'] },
  { id: 4, building: '2号楼', room: '101', capacity: 4, currentResidents: ['刘强', '陈静', '杨帆', '周杰'] },
  { id: 5, building: '2号楼', room: '102', capacity: 4, currentResidents: ['吴芳', '郑浩', '孙悦', '马超'] },
  { id: 6, building: '2号楼', room: '201', capacity: 4, currentResidents: ['黄磊', '罗志祥', '周杰伦', '王力宏'] },
  { id: 7, building: '3号楼', room: '101', capacity: 4, currentResidents: ['刘亦菲', '杨幂', '范冰冰', '赵丽颖'] },
  { id: 8, building: '3号楼', room: '102', capacity: 4, currentResidents: ['胡歌', '霍建华', '彭于晏', '王凯'] }
]

const balanceData = {
  '1号楼-101': { water: 125.50, electricity: 89.30, waterLastUpdate: '2026-05-15', electricityLastUpdate: '2026-05-15' },
  '1号楼-102': { water: 45.20, electricity: 28.60, waterLastUpdate: '2026-05-15', electricityLastUpdate: '2026-05-15' },
  '1号楼-201': { water: 78.90, electricity: 156.80, waterLastUpdate: '2026-05-15', electricityLastUpdate: '2026-05-15' },
  '2号楼-101': { water: 23.40, electricity: 67.50, waterLastUpdate: '2026-05-15', electricityLastUpdate: '2026-05-15' },
  '2号楼-102': { water: 156.70, electricity: 234.20, waterLastUpdate: '2026-05-15', electricityLastUpdate: '2026-05-15' },
  '2号楼-201': { water: 89.10, electricity: 45.30, waterLastUpdate: '2026-05-15', electricityLastUpdate: '2026-05-15' },
  '3号楼-101': { water: 12.80, electricity: 18.90, waterLastUpdate: '2026-05-15', electricityLastUpdate: '2026-05-15' },
  '3号楼-102': { water: 210.50, electricity: 178.40, waterLastUpdate: '2026-05-15', electricityLastUpdate: '2026-05-15' }
}

const usageHistory = {
  '1号楼-101': {
    water: [12, 15, 18, 14, 16, 20, 22],
    electricity: [85, 92, 78, 88, 95, 102, 98],
    dates: ['5月1日', '5月2日', '5月3日', '5月4日', '5月5日', '5月6日', '5月7日']
  },
  '1号楼-102': {
    water: [8, 10, 12, 9, 11, 13, 10],
    electricity: [45, 52, 48, 55, 60, 58, 50],
    dates: ['5月1日', '5月2日', '5月3日', '5月4日', '5月5日', '5月6日', '5月7日']
  },
  '1号楼-201': {
    water: [15, 18, 20, 17, 19, 21, 18],
    electricity: [120, 135, 128, 142, 150, 155, 148],
    dates: ['5月1日', '5月2日', '5月3日', '5月4日', '5月5日', '5月6日', '5月7日']
  },
  '2号楼-101': {
    water: [5, 7, 6, 8, 9, 10, 8],
    electricity: [35, 42, 38, 45, 48, 52, 46],
    dates: ['5月1日', '5月2日', '5月3日', '5月4日', '5月5日', '5月6日', '5月7日']
  },
  '2号楼-102': {
    water: [18, 22, 25, 20, 23, 26, 21],
    electricity: [150, 165, 172, 158, 168, 175, 162],
    dates: ['5月1日', '5月2日', '5月3日', '5月4日', '5月5日', '5月6日', '5月7日']
  },
  '2号楼-201': {
    water: [10, 12, 14, 11, 13, 15, 12],
    electricity: [60, 68, 72, 65, 70, 75, 68],
    dates: ['5月1日', '5月2日', '5月3日', '5月4日', '5月5日', '5月6日', '5月7日']
  },
  '3号楼-101': {
    water: [3, 4, 5, 3, 4, 6, 4],
    electricity: [15, 18, 16, 20, 22, 25, 20],
    dates: ['5月1日', '5月2日', '5月3日', '5月4日', '5月5日', '5月6日', '5月7日']
  },
  '3号楼-102': {
    water: [25, 28, 30, 27, 29, 32, 28],
    electricity: [180, 195, 200, 188, 198, 210, 192],
    dates: ['5月1日', '5月2日', '5月3日', '5月4日', '5月5日', '5月6日', '5月7日']
  }
}

const rechargeRecords = [
  { id: 1, dormitory: '1号楼-101', type: 'water', amount: 50, payMethod: '微信支付', time: '2026-05-10 14:30:25', status: 'success' },
  { id: 2, dormitory: '1号楼-101', type: 'electricity', amount: 100, payMethod: '支付宝', time: '2026-05-08 09:15:42', status: 'success' },
  { id: 3, dormitory: '1号楼-102', type: 'water', amount: 30, payMethod: '微信支付', time: '2026-05-12 16:45:33', status: 'success' },
  { id: 4, dormitory: '1号楼-201', type: 'electricity', amount: 80, payMethod: '校园卡', time: '2026-05-11 11:20:18', status: 'success' },
  { id: 5, dormitory: '2号楼-101', type: 'water', amount: 40, payMethod: '微信支付', time: '2026-05-09 08:55:47', status: 'success' },
  { id: 6, dormitory: '2号楼-102', type: 'electricity', amount: 150, payMethod: '支付宝', time: '2026-05-07 13:40:52', status: 'success' },
  { id: 7, dormitory: '3号楼-101', type: 'water', amount: 20, payMethod: '校园卡', time: '2026-05-06 17:25:10', status: 'success' },
  { id: 8, dormitory: '3号楼-102', type: 'electricity', amount: 200, payMethod: '微信支付', time: '2026-05-05 10:10:35', status: 'success' },
  { id: 9, dormitory: '1号楼-101', type: 'water', amount: 60, payMethod: '支付宝', time: '2026-05-04 15:30:18', status: 'success' },
  { id: 10, dormitory: '1号楼-101', type: 'electricity', amount: 75, payMethod: '微信支付', time: '2026-05-03 09:45:22', status: 'success' },
  { id: 11, dormitory: '2号楼-201', type: 'water', amount: 35, payMethod: '校园卡', time: '2026-05-02 14:20:45', status: 'pending' },
  { id: 12, dormitory: '3号楼-101', type: 'electricity', amount: 50, payMethod: '微信支付', time: '2026-05-01 16:55:30', status: 'success' }
]

const warningThreshold = {
  water: 30,
  electricity: 50
}

export function getDormitories() {
  return dormitories
}

export function getDormitoryList() {
  return dormitories.map(d => `${d.building}-${d.room}`)
}

export function getBalance(dormitory) {
  return balanceData[dormitory] || { water: 0, electricity: 0, waterLastUpdate: '', electricityLastUpdate: '' }
}

export function getUsageHistory(dormitory) {
  return usageHistory[dormitory] || { water: [], electricity: [], dates: [] }
}

export function getRechargeRecords(dormitory = null) {
  if (dormitory) {
    return rechargeRecords.filter(r => r.dormitory === dormitory)
  }
  return rechargeRecords
}

export function getWarningList() {
  const warnings = []
  Object.keys(balanceData).forEach(dormitory => {
    const balance = balanceData[dormitory]
    if (balance.water < warningThreshold.water) {
      warnings.push({
      dormitory,
      type: 'water',
      balance: balance.water,
      threshold: warningThreshold.water,
      level: balance.water < 10 ? 'danger' : 'warning'
    })
    }
    if (balance.electricity < warningThreshold.electricity) {
      warnings.push({
      dormitory,
      type: 'electricity',
      balance: balance.electricity,
      threshold: warningThreshold.electricity,
      level: balance.electricity < 20 ? 'danger' : 'warning'
    })
    }
  })
  return warnings
}

export function recharge(dormitory, type, amount, payMethod) {
  balanceData[dormitory][type] += amount
  rechargeRecords.unshift({
    id: rechargeRecords.length + 1,
    dormitory,
    type,
    amount,
    payMethod,
    time: new Date().toLocaleString('zh-CN'),
    status: 'success'
  })
  return true
}

export function checkDuplicateRecharge(dormitory, type, amount) {
  const now = new Date()
  const fiveMinutesAgo = new Date(now.getTime() - 5 * 60 * 1000)
  
  return rechargeRecords.some(record => {
    if (record.dormitory !== dormitory || record.type !== type || record.amount !== amount) {
      return false
    }
    const recordTime = new Date(record.time)
    return recordTime >= fiveMinutesAgo && recordTime <= now
  })
}

export function setCurrentDormitory(dormitory) {
  localStorage.setItem('currentDormitory', dormitory)
}

export function getCurrentDormitory() {
  return localStorage.getItem('currentDormitory') || ''
}
