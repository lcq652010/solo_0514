export const categories = [
  { id: 1, name: '热销推荐' },
  { id: 2, name: '主食' },
  { id: 3, name: '小吃' },
  { id: 4, name: '饮料' },
  { id: 5, name: '甜点' }
]

export const dishes = [
  {
    id: 1,
    name: '宫保鸡丁',
    categoryId: 1,
    price: 28,
    description: '经典川菜，鸡肉嫩滑，花生酥脆',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=delicious%20kung%20pao%20chicken%20chinese%20food&image_size=square',
    sales: 156,
    rating: 4.8,
    stock: 50
  },
  {
    id: 2,
    name: '红烧肉',
    categoryId: 1,
    price: 38,
    description: '肥而不腻，入口即化的经典红烧肉',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=braised%20pork%20belly%20chinese%20cuisine&image_size=square',
    sales: 203,
    rating: 4.9,
    stock: 30
  },
  {
    id: 3,
    name: '麻婆豆腐',
    categoryId: 1,
    price: 18,
    description: '麻辣鲜香，豆腐嫩滑',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=mapo%20tofu%20spicy%20sichuan%20dish&image_size=square',
    sales: 178,
    rating: 4.7,
    stock: 0
  },
  {
    id: 4,
    name: '扬州炒饭',
    categoryId: 2,
    price: 22,
    description: '配料丰富，粒粒分明',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=yangzhou%20fried%20rice%20chinese%20food&image_size=square',
    sales: 245,
    rating: 4.6,
    stock: 40
  },
  {
    id: 5,
    name: '牛肉面',
    categoryId: 2,
    price: 25,
    description: '牛肉软烂，汤底浓郁',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=beef%20noodle%20soup%20chinese&image_size=square',
    sales: 312,
    rating: 4.8,
    stock: 25
  },
  {
    id: 6,
    name: '小笼包',
    categoryId: 3,
    price: 16,
    description: '皮薄馅大，汤汁鲜美',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=xiaolongbao%20soup%20dumplings%20chinese&image_size=square',
    sales: 189,
    rating: 4.9,
    stock: 60
  },
  {
    id: 7,
    name: '春卷',
    categoryId: 3,
    price: 12,
    description: '外酥里嫩，香脆可口',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=spring%20rolls%20crispy%20chinese%20appetizer&image_size=square',
    sales: 134,
    rating: 4.5,
    stock: 0
  },
  {
    id: 8,
    name: '珍珠奶茶',
    categoryId: 4,
    price: 15,
    description: 'Q弹珍珠，香浓奶茶',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=bubble%20tea%20pearl%20milk%20tea&image_size=square',
    sales: 456,
    rating: 4.7,
    stock: 100
  },
  {
    id: 9,
    name: '柠檬茶',
    categoryId: 4,
    price: 12,
    description: '清新柠檬，解渴消暑',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=lemon%20iced%20tea%20refreshing&image_size=square',
    sales: 287,
    rating: 4.6,
    stock: 80
  },
  {
    id: 10,
    name: '芒果布丁',
    categoryId: 5,
    price: 14,
    description: '香甜芒果，丝滑布丁',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=mango%20pudding%20dessert&image_size=square',
    sales: 156,
    rating: 4.8,
    stock: 35
  },
  {
    id: 11,
    name: '提拉米苏',
    categoryId: 5,
    price: 28,
    description: '意式经典，浓郁咖啡香',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=tiramisu%20italian%20dessert&image_size=square',
    sales: 123,
    rating: 4.9,
    stock: 20
  },
  {
    id: 12,
    name: '水煮鱼',
    categoryId: 1,
    price: 48,
    description: '麻辣鲜香，鱼肉嫩滑',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=Sichuan%20boiled%20fish%20spicy&image_size=square',
    sales: 167,
    rating: 4.8,
    stock: 15
  }
]

export const riders = [
  { id: 1, name: '张师傅', phone: '13800138001', status: '空闲', orders: 0, rating: 4.9 },
  { id: 2, name: '李师傅', phone: '13800138002', status: '配送中', orders: 2, rating: 4.8 },
  { id: 3, name: '王师傅', phone: '13800138003', status: '空闲', orders: 0, rating: 4.7 },
  { id: 4, name: '赵师傅', phone: '13800138004', status: '配送中', orders: 1, rating: 4.6 },
  { id: 5, name: '刘师傅', phone: '13800138005', status: '空闲', orders: 0, rating: 4.9 }
]

export const merchants = [
  { id: 1, name: '川味轩餐厅' },
  { id: 2, name: '老北京面馆' },
  { id: 3, name: '港式茶餐厅' },
  { id: 4, name: '甜品小站' }
]

export const districts = [
  { id: 1, name: '朝阳区' },
  { id: 2, name: '海淀区' },
  { id: 3, name: '西城区' },
  { id: 4, name: '东城区' },
  { id: 5, name: '丰台区' }
]

export const paymentStatusMap = {
  unpaid: { text: '待支付', color: '#E6A23C' },
  paid: { text: '已支付', color: '#67C23A' },
  refunded: { text: '已退款', color: '#909399' }
}

export const orders = [
  {
    id: 'DD202401150001',
    customerName: '张三',
    phone: '13800138101',
    address: '北京市朝阳区建国路88号SOHO现代城A座1201',
    dishes: [
      { id: 1, name: '宫保鸡丁', price: 28, quantity: 2 },
      { id: 8, name: '珍珠奶茶', price: 15, quantity: 2 }
    ],
    totalPrice: 86,
    status: 'pending',
    paymentStatus: 'paid',
    merchantId: 1,
    merchantName: '川味轩餐厅',
    districtId: 1,
    districtName: '朝阳区',
    createTime: '2024-01-15 10:30:00',
    remark: '少放辣'
  },
  {
    id: 'DD202401150002',
    customerName: '李四',
    phone: '13800138102',
    address: '北京市海淀区中关村大街1号海龙大厦8层',
    dishes: [
      { id: 5, name: '牛肉面', price: 25, quantity: 1 },
      { id: 6, name: '小笼包', price: 16, quantity: 1 }
    ],
    totalPrice: 41,
    status: 'preparing',
    paymentStatus: 'paid',
    merchantId: 2,
    merchantName: '老北京面馆',
    districtId: 2,
    districtName: '海淀区',
    createTime: '2024-01-15 10:25:00',
    remark: '面多煮一会儿'
  },
  {
    id: 'DD202401150003',
    customerName: '王五',
    phone: '13800138103',
    address: '北京市西城区金融街15号',
    dishes: [
      { id: 2, name: '红烧肉', price: 38, quantity: 1 },
      { id: 4, name: '扬州炒饭', price: 22, quantity: 1 }
    ],
    totalPrice: 60,
    status: 'delivering',
    paymentStatus: 'paid',
    merchantId: 1,
    merchantName: '川味轩餐厅',
    districtId: 3,
    districtName: '西城区',
    createTime: '2024-01-15 10:15:00',
    remark: '',
    riderId: 2,
    riderName: '李师傅'
  },
  {
    id: 'DD202401150004',
    customerName: '赵六',
    phone: '13800138104',
    address: '北京市东城区王府井大街138号',
    dishes: [
      { id: 12, name: '水煮鱼', price: 48, quantity: 1 },
      { id: 9, name: '柠檬茶', price: 12, quantity: 2 }
    ],
    totalPrice: 72,
    status: 'delivered',
    paymentStatus: 'paid',
    merchantId: 1,
    merchantName: '川味轩餐厅',
    districtId: 4,
    districtName: '东城区',
    createTime: '2024-01-15 09:50:00',
    finishTime: '2024-01-15 10:35:00',
    remark: '不要香菜',
    riderId: 4,
    riderName: '赵师傅'
  },
  {
    id: 'DD202401150005',
    customerName: '孙七',
    phone: '13800138105',
    address: '北京市丰台区方庄小区1号楼',
    dishes: [
      { id: 3, name: '麻婆豆腐', price: 18, quantity: 1 },
      { id: 7, name: '春卷', price: 12, quantity: 1 },
      { id: 10, name: '芒果布丁', price: 14, quantity: 1 }
    ],
    totalPrice: 44,
    status: 'cancelled',
    paymentStatus: 'refunded',
    merchantId: 3,
    merchantName: '港式茶餐厅',
    districtId: 5,
    districtName: '丰台区',
    createTime: '2024-01-15 09:30:00',
    cancelTime: '2024-01-15 09:35:00',
    remark: '用户取消'
  },
  {
    id: 'DD202401150006',
    customerName: '周八',
    phone: '13800138106',
    address: '北京市朝阳区三里屯太古里北区',
    dishes: [
      { id: 11, name: '提拉米苏', price: 28, quantity: 1 },
      { id: 10, name: '芒果布丁', price: 14, quantity: 2 }
    ],
    totalPrice: 56,
    status: 'preparing',
    paymentStatus: 'paid',
    merchantId: 4,
    merchantName: '甜品小站',
    districtId: 1,
    districtName: '朝阳区',
    createTime: '2024-01-15 10:40:00',
    remark: ''
  },
  {
    id: 'DD202401150007',
    customerName: '吴九',
    phone: '13800138107',
    address: '北京市海淀区北京大学燕园',
    dishes: [
      { id: 5, name: '牛肉面', price: 25, quantity: 2 },
      { id: 8, name: '珍珠奶茶', price: 15, quantity: 2 }
    ],
    totalPrice: 80,
    status: 'delivering',
    paymentStatus: 'paid',
    merchantId: 2,
    merchantName: '老北京面馆',
    districtId: 2,
    districtName: '海淀区',
    createTime: '2024-01-15 10:05:00',
    remark: '送北门',
    riderId: 1,
    riderName: '张师傅'
  },
  {
    id: 'DD202401150008',
    customerName: '郑十',
    phone: '13800138108',
    address: '北京市西城区西单大悦城',
    dishes: [
      { id: 6, name: '小笼包', price: 16, quantity: 3 },
      { id: 7, name: '春卷', price: 12, quantity: 2 }
    ],
    totalPrice: 72,
    status: 'pending',
    paymentStatus: 'unpaid',
    merchantId: 3,
    merchantName: '港式茶餐厅',
    districtId: 3,
    districtName: '西城区',
    createTime: '2024-01-15 10:45:00',
    remark: ''
  },
  {
    id: 'DD202401150009',
    customerName: '钱十一',
    phone: '13800138109',
    address: '北京市东城区天安门广场东侧',
    dishes: [
      { id: 1, name: '宫保鸡丁', price: 28, quantity: 1 },
      { id: 2, name: '红烧肉', price: 38, quantity: 1 },
      { id: 4, name: '扬州炒饭', price: 22, quantity: 1 }
    ],
    totalPrice: 88,
    status: 'delivered',
    paymentStatus: 'paid',
    merchantId: 1,
    merchantName: '川味轩餐厅',
    districtId: 4,
    districtName: '东城区',
    createTime: '2024-01-15 09:00:00',
    finishTime: '2024-01-15 09:40:00',
    remark: '',
    riderId: 3,
    riderName: '王师傅'
  },
  {
    id: 'DD202401150010',
    customerName: '孙十二',
    phone: '13800138110',
    address: '北京市丰台区北京西站南广场',
    dishes: [
      { id: 9, name: '柠檬茶', price: 12, quantity: 5 }
    ],
    totalPrice: 60,
    status: 'cancelled',
    paymentStatus: 'refunded',
    merchantId: 3,
    merchantName: '港式茶餐厅',
    districtId: 5,
    districtName: '丰台区',
    createTime: '2024-01-15 08:30:00',
    cancelTime: '2024-01-15 08:32:00',
    remark: '用户取消，买多了'
  },
  {
    id: 'DD202401150011',
    customerName: '李十三',
    phone: '13800138111',
    address: '北京市朝阳区望京SOHO',
    dishes: [
      { id: 12, name: '水煮鱼', price: 48, quantity: 1 },
      { id: 3, name: '麻婆豆腐', price: 18, quantity: 1 }
    ],
    totalPrice: 66,
    status: 'preparing',
    paymentStatus: 'paid',
    merchantId: 1,
    merchantName: '川味轩餐厅',
    districtId: 1,
    districtName: '朝阳区',
    createTime: '2024-01-15 10:50:00',
    remark: '微辣'
  },
  {
    id: 'DD202401150012',
    customerName: '王十四',
    phone: '13800138112',
    address: '北京市海淀区清华大学东门',
    dishes: [
      { id: 11, name: '提拉米苏', price: 28, quantity: 2 }
    ],
    totalPrice: 56,
    status: 'delivered',
    paymentStatus: 'paid',
    merchantId: 4,
    merchantName: '甜品小站',
    districtId: 2,
    districtName: '海淀区',
    createTime: '2024-01-15 08:00:00',
    finishTime: '2024-01-15 08:35:00',
    remark: '',
    riderId: 5,
    riderName: '刘师傅'
  }
]

export const deliveryStatusMap = {
  pending: { text: '待接单', color: '#909399' },
  preparing: { text: '备餐中', color: '#E6A23C' },
  delivering: { text: '配送中', color: '#409EFF' },
  delivered: { text: '已送达', color: '#67C23A' },
  cancelled: { text: '已取消', color: '#F56C6C' }
}

export const deliveryTimeline = {
  pending: [
    { status: 'pending', text: '订单已提交', time: '', done: true },
    { status: 'preparing', text: '商家接单中', time: '', done: false },
    { status: 'delivering', text: '骑手配送中', time: '', done: false },
    { status: 'delivered', text: '已送达', time: '', done: false }
  ],
  preparing: [
    { status: 'pending', text: '订单已提交', time: '', done: true },
    { status: 'preparing', text: '商家正在备餐', time: '', done: true },
    { status: 'delivering', text: '等待骑手取餐', time: '', done: false },
    { status: 'delivered', text: '已送达', time: '', done: false }
  ],
  delivering: [
    { status: 'pending', text: '订单已提交', time: '', done: true },
    { status: 'preparing', text: '商家备餐完成', time: '', done: true },
    { status: 'delivering', text: '骑手正在配送', time: '', done: true },
    { status: 'delivered', text: '已送达', time: '', done: false }
  ],
  delivered: [
    { status: 'pending', text: '订单已提交', time: '', done: true },
    { status: 'preparing', text: '商家备餐完成', time: '', done: true },
    { status: 'delivering', text: '骑手配送完成', time: '', done: true },
    { status: 'delivered', text: '已送达', time: '', done: true }
  ]
}
