export const dormitoryInfo = {
  building: '1号楼',
  room: '302',
  waterBalance: 8.50,
  electricBalance: 15.30
}

export const usageData = {
  water: {
    daily: [
      { date: '05-10', usage: 0.8 },
      { date: '05-11', usage: 1.2 },
      { date: '05-12', usage: 0.9 },
      { date: '05-13', usage: 1.5 },
      { date: '05-14', usage: 1.1 },
      { date: '05-15', usage: 0.7 },
      { date: '05-16', usage: 1.0 }
    ],
    monthly: 32.5,
    total: 156.8
  },
  electric: {
    daily: [
      { date: '05-10', usage: 5.2 },
      { date: '05-11', usage: 6.8 },
      { date: '05-12', usage: 4.5 },
      { date: '05-13', usage: 7.2 },
      { date: '05-14', usage: 5.9 },
      { date: '05-15', usage: 6.3 },
      { date: '05-16', usage: 5.5 }
    ],
    monthly: 128.6,
    total: 586.3
  }
}

export const rechargeRecords = [
  {
    id: 'RC20240516001',
    type: 'electric',
    amount: 50.00,
    paymentMethod: '支付宝',
    status: 'success',
    createTime: '2024-05-16 14:30:25',
    dormitory: '1号楼302'
  },
  {
    id: 'RC20240515002',
    type: 'water',
    amount: 30.00,
    paymentMethod: '微信',
    status: 'success',
    createTime: '2024-05-15 09:15:33',
    dormitory: '1号楼302'
  },
  {
    id: 'RC20240514003',
    type: 'electric',
    amount: 100.00,
    paymentMethod: '银行卡',
    status: 'success',
    createTime: '2024-05-14 16:45:12',
    dormitory: '1号楼302'
  },
  {
    id: 'RC20240513004',
    type: 'water',
    amount: 20.00,
    paymentMethod: '支付宝',
    status: 'failed',
    createTime: '2024-05-13 11:22:45',
    dormitory: '1号楼302'
  },
  {
    id: 'RC20240512005',
    type: 'electric',
    amount: 50.00,
    paymentMethod: '微信',
    status: 'success',
    createTime: '2024-05-12 08:30:00',
    dormitory: '1号楼302'
  }
]

export const reminderSettings = {
  waterThreshold: 10,
  electricThreshold: 20,
  enableNotification: true,
  notificationMethod: 'sms',
  phone: '138****8888',
  email: 'student@campus.edu.cn'
}

export const buildingList = [
  { value: '1号楼', label: '1号楼（男生宿舍）' },
  { value: '2号楼', label: '2号楼（男生宿舍）' },
  { value: '3号楼', label: '3号楼（女生宿舍）' },
  { value: '4号楼', label: '4号楼（女生宿舍）' },
  { value: '5号楼', label: '5号楼（研究生宿舍）' },
  { value: '6号楼', label: '6号楼（研究生宿舍）' }
]

export const roomList = {
  '1号楼': ['101', '102', '103', '104', '105', '201', '202', '203', '204', '205', '301', '302', '303', '304', '305'],
  '2号楼': ['101', '102', '103', '104', '105', '201', '202', '203', '204', '205', '301', '302', '303', '304', '305'],
  '3号楼': ['101', '102', '103', '104', '105', '201', '202', '203', '204', '205', '301', '302', '303', '304', '305'],
  '4号楼': ['101', '102', '103', '104', '105', '201', '202', '203', '204', '205', '301', '302', '303', '304', '305'],
  '5号楼': ['101', '102', '103', '104', '201', '202', '203', '204', '301', '302', '303', '304'],
  '6号楼': ['101', '102', '103', '104', '201', '202', '203', '204', '301', '302', '303', '304']
}

export const bindingDormitories = [
  {
    id: 1,
    building: '1号楼',
    room: '302',
    isDefault: true,
    bindTime: '2024-02-15 10:30:00'
  },
  {
    id: 2,
    building: '5号楼',
    room: '203',
    isDefault: false,
    bindTime: '2024-03-20 14:20:00'
  }
]
