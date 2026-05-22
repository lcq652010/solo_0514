export const ticketTypes = [
  {
    id: 1,
    name: '成人票',
    price: 120,
    originalPrice: 150,
    description: '适用于身高1.4米以上成人游客',
    stock: 500,
    validDays: 7,
    tags: ['热门', '推荐'],
    image: 'https://picsum.photos/400/300?random=1'
  },
  {
    id: 2,
    name: '儿童票',
    price: 60,
    originalPrice: 80,
    description: '适用于身高1.2-1.4米儿童',
    stock: 300,
    validDays: 7,
    tags: ['优惠'],
    image: 'https://picsum.photos/400/300?random=2'
  },
  {
    id: 3,
    name: '学生票',
    price: 80,
    originalPrice: 100,
    description: '凭有效学生证入园',
    stock: 200,
    validDays: 7,
    tags: ['学生专享'],
    image: 'https://picsum.photos/400/300?random=3'
  },
  {
    id: 4,
    name: '老年票',
    price: 50,
    originalPrice: 70,
    description: '60岁以上老人凭身份证',
    stock: 150,
    validDays: 7,
    tags: ['优惠'],
    image: 'https://picsum.photos/400/300?random=4'
  },
  {
    id: 5,
    name: '家庭套票',
    price: 280,
    originalPrice: 350,
    description: '含2成人+1儿童',
    stock: 100,
    validDays: 7,
    tags: ['超值', '推荐'],
    image: 'https://picsum.photos/400/300?random=5'
  },
  {
    id: 6,
    name: 'VIP通票',
    price: 299,
    originalPrice: 399,
    description: '含所有项目+快速通道',
    stock: 50,
    validDays: 30,
    tags: ['VIP', '尊享'],
    image: 'https://picsum.photos/400/300?random=6'
  }
]

export const orders = [
  {
    id: 'ORD202605010001',
    ticketName: '成人票',
    ticketId: 1,
    quantity: 2,
    totalPrice: 240,
    visitorName: '张三',
    visitorPhone: '13800138001',
    visitorIdCard: '110101199001011234',
    visitDate: '2026-05-10',
    status: 'paid',
    createTime: '2026-05-01 10:30:00',
    ticketCode: 'TCK00123456'
  },
  {
    id: 'ORD202605020002',
    ticketName: '家庭套票',
    ticketId: 5,
    quantity: 1,
    totalPrice: 280,
    visitorName: '李四',
    visitorPhone: '13800138002',
    visitorIdCard: '310101199002025678',
    visitDate: '2026-05-15',
    status: 'unused',
    createTime: '2026-05-02 14:20:00',
    ticketCode: 'TCK00123457'
  },
  {
    id: 'ORD202605030003',
    ticketName: '学生票',
    ticketId: 3,
    quantity: 3,
    totalPrice: 240,
    visitorName: '王五',
    visitorPhone: '13800138003',
    visitorIdCard: '440101199503039012',
    visitDate: '2026-05-08',
    status: 'used',
    createTime: '2026-05-03 09:15:00',
    ticketCode: 'TCK00123458'
  },
  {
    id: 'ORD202605040004',
    ticketName: 'VIP通票',
    ticketId: 6,
    quantity: 1,
    totalPrice: 299,
    visitorName: '赵六',
    visitorPhone: '13800138004',
    visitorIdCard: '510101198804043456',
    visitDate: '2026-05-20',
    status: 'cancelled',
    createTime: '2026-05-04 16:45:00',
    ticketCode: 'TCK00123459'
  }
]

export const userInfo = {
  username: 'tourist001',
  nickname: '快乐旅行者',
  avatar: 'https://picsum.photos/100/100?random=10',
  phone: '138****8000',
  email: 'user@example.com',
  registerTime: '2025-12-01 10:00:00',
  totalOrders: 15,
  totalSpent: 3280,
  level: '黄金会员'
}

export const statusMap = {
  paid: { label: '已支付', type: 'success' },
  unused: { label: '待使用', type: 'warning' },
  used: { label: '已使用', type: 'info' },
  cancelled: { label: '已取消', type: 'danger' }
}
