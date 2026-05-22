const levelDiscountConfig = {
  '钻石会员': 0.8,
  '金卡会员': 0.85,
  '银卡会员': 0.9,
  '普通会员': 0.95
}

export function getDiscountByLevel(level) {
  return levelDiscountConfig[level] || 1
}

export function getDiscountInfoByLevel(level) {
  const discount = getDiscountByLevel(level)
  const discountText = discount === 1 ? '无折扣' : `${discount * 10}折`
  return {
    discount,
    discountText,
    level
  }
}

const mockMembers = [
  {
    id: 1,
    memberNo: 'VIP000001',
    name: '张三',
    phone: '13800138001',
    email: 'zhangsan@example.com',
    gender: 1,
    birthday: '1990-05-15',
    balance: 2580.50,
    totalRecharge: 5000,
    totalConsume: 2419.50,
    point: 2580,
    level: '金卡会员',
    status: 1,
    registerTime: '2024-01-15 10:30:00',
    lastConsumeTime: '2024-05-10 14:20:00',
    address: '北京市朝阳区某某街道123号',
    remark: '优质客户'
  },
  {
    id: 2,
    memberNo: 'VIP000002',
    name: '李四',
    phone: '13800138002',
    email: 'lisi@example.com',
    gender: 2,
    birthday: '1985-08-22',
    balance: 1200.00,
    totalRecharge: 3000,
    totalConsume: 1800,
    point: 1200,
    level: '银卡会员',
    status: 1,
    registerTime: '2024-02-20 09:15:00',
    lastConsumeTime: '2024-05-08 16:45:00',
    address: '上海市浦东新区某某路456号',
    remark: ''
  },
  {
    id: 3,
    memberNo: 'VIP000003',
    name: '王五',
    phone: '13800138003',
    email: 'wangwu@example.com',
    gender: 1,
    birthday: '1992-11-30',
    balance: 500.00,
    totalRecharge: 1500,
    totalConsume: 1000,
    point: 500,
    level: '普通会员',
    status: 1,
    registerTime: '2024-03-10 14:00:00',
    lastConsumeTime: '2024-04-25 11:30:00',
    address: '广州市天河区某某大道789号',
    remark: ''
  },
  {
    id: 4,
    memberNo: 'VIP000004',
    name: '赵六',
    phone: '13800138004',
    email: 'zhaoliu@example.com',
    gender: 2,
    birthday: '1988-03-12',
    balance: 0,
    totalRecharge: 800,
    totalConsume: 800,
    point: 800,
    level: '普通会员',
    status: 0,
    registerTime: '2024-01-25 16:20:00',
    lastConsumeTime: '2024-03-15 09:00:00',
    address: '深圳市南山区某某科技园',
    remark: '已暂停'
  },
  {
    id: 5,
    memberNo: 'VIP000005',
    name: '陈七',
    phone: '13800138005',
    email: 'chenqi@example.com',
    gender: 1,
    birthday: '1995-07-08',
    balance: 8888.88,
    totalRecharge: 15000,
    totalConsume: 6111.12,
    point: 8888,
    level: '钻石会员',
    status: 1,
    registerTime: '2023-12-01 10:00:00',
    lastConsumeTime: '2024-05-15 18:30:00',
    address: '杭州市西湖区某某商圈',
    remark: 'VIP大客户'
  }
]

const mockTransactions = [
  {
    id: 1,
    orderNo: 'TX202405150001',
    memberId: 1,
    memberName: '张三',
    memberNo: 'VIP000001',
    type: 1,
    amount: 500,
    beforeBalance: 2080.50,
    afterBalance: 2580.50,
    paymentMethod: '微信支付',
    operator: '管理员',
    remark: '充值500元',
    createTime: '2024-05-15 10:30:00'
  },
  {
    id: 2,
    orderNo: 'TX202405100002',
    memberId: 1,
    memberName: '张三',
    memberNo: 'VIP000001',
    type: 2,
    amount: 280,
    beforeBalance: 2360.50,
    afterBalance: 2080.50,
    paymentMethod: '余额支付',
    operator: '收银员A',
    remark: '购买商品消费',
    createTime: '2024-05-10 14:20:00'
  },
  {
    id: 3,
    orderNo: 'TX202405080003',
    memberId: 2,
    memberName: '李四',
    memberNo: 'VIP000002',
    type: 2,
    amount: 150,
    beforeBalance: 1350,
    afterBalance: 1200,
    paymentMethod: '余额支付',
    operator: '收银员B',
    remark: '服务消费',
    createTime: '2024-05-08 16:45:00'
  },
  {
    id: 4,
    orderNo: 'TX202405010004',
    memberId: 5,
    memberName: '陈七',
    memberNo: 'VIP000005',
    type: 1,
    amount: 5000,
    beforeBalance: 3888.88,
    afterBalance: 8888.88,
    paymentMethod: '银行转账',
    operator: '财务',
    remark: '大额充值',
    createTime: '2024-05-01 09:00:00'
  },
  {
    id: 5,
    orderNo: 'TX202404250005',
    memberId: 3,
    memberName: '王五',
    memberNo: 'VIP000003',
    type: 2,
    amount: 200,
    beforeBalance: 700,
    afterBalance: 500,
    paymentMethod: '余额支付',
    operator: '收银员A',
    remark: '产品消费',
    createTime: '2024-04-25 11:30:00'
  },
  {
    id: 6,
    orderNo: 'TX202403150006',
    memberId: 4,
    memberName: '赵六',
    memberNo: 'VIP000004',
    type: 2,
    amount: 300,
    beforeBalance: 300,
    afterBalance: 0,
    paymentMethod: '余额支付',
    operator: '收银员C',
    remark: '最后一笔消费',
    createTime: '2024-03-15 09:00:00'
  }
]

export function getMembers() {
  return [...mockMembers]
}

export function getMemberById(id) {
  return mockMembers.find(m => m.id === parseInt(id))
}

export function getTransactions() {
  return [...mockTransactions]
}

export function getTransactionsWithMemberInfo() {
  return mockTransactions.map(t => {
    const member = mockMembers.find(m => m.id === t.memberId)
    return {
      ...t,
      phone: member ? member.phone : ''
    }
  })
}

export function getTransactionsByMemberId(memberId) {
  return mockTransactions.filter(t => t.memberId === parseInt(memberId))
}

export function recharge(memberId, amount, paymentMethod, remark) {
  const member = mockMembers.find(m => m.id === parseInt(memberId))
  if (!member) {
    return { success: false, message: '会员不存在' }
  }
  const beforeBalance = member.balance
  member.balance += parseFloat(amount)
  member.totalRecharge += parseFloat(amount)
  member.point += Math.floor(parseFloat(amount))

  const newTransaction = {
    id: mockTransactions.length + 1,
    orderNo: 'TX' + new Date().toISOString().slice(0, 10).replace(/-/g, '') + String(mockTransactions.length + 1).padStart(4, '0'),
    memberId: parseInt(memberId),
    memberName: member.name,
    memberNo: member.memberNo,
    type: 1,
    amount: parseFloat(amount),
    beforeBalance: beforeBalance,
    afterBalance: member.balance,
    paymentMethod: paymentMethod,
    operator: '当前操作员',
    remark: remark || '充值',
    createTime: new Date().toISOString().slice(0, 19).replace('T', ' ')
  }
  mockTransactions.unshift(newTransaction)

  return { success: true, message: '充值成功', data: newTransaction }
}

export function consume(memberId, amount, paymentMethod, remark) {
  const member = mockMembers.find(m => m.id === parseInt(memberId))
  if (!member) {
    return { success: false, message: '会员不存在' }
  }
  if (member.status !== 1) {
    return { success: false, message: '会员状态异常，无法消费' }
  }
  if (paymentMethod === '余额支付' && member.balance < parseFloat(amount)) {
    return { success: false, message: '余额不足' }
  }

  const beforeBalance = member.balance
  if (paymentMethod === '余额支付') {
    member.balance -= parseFloat(amount)
  }
  member.totalConsume += parseFloat(amount)

  const newTransaction = {
    id: mockTransactions.length + 1,
    orderNo: 'TX' + new Date().toISOString().slice(0, 10).replace(/-/g, '') + String(mockTransactions.length + 1).padStart(4, '0'),
    memberId: parseInt(memberId),
    memberName: member.name,
    memberNo: member.memberNo,
    type: 2,
    amount: parseFloat(amount),
    beforeBalance: beforeBalance,
    afterBalance: member.balance,
    paymentMethod: paymentMethod,
    operator: '当前操作员',
    remark: remark || '消费',
    createTime: new Date().toISOString().slice(0, 19).replace('T', ' ')
  }
  mockTransactions.unshift(newTransaction)

  return { success: true, message: '消费成功', data: newTransaction }
}
