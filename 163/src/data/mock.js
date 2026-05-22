export const goodsList = [
  {
    id: 1,
    name: '新鲜草莓 500g 盒装',
    category: '水果',
    image: 'https://images.unsplash.com/photo-1464965911861-746a04b4bca7?w=400&h=300&fit=crop',
    groupPrice: 19.9,
    originalPrice: 39.9,
    stock: 50,
    limitBuy: 2,
    needCount: 5,
    currentCount: 3,
    status: 'going',
    endTime: '2024-01-20 23:59:59',
    leader: '张阿姨',
    address: '幸福小区1号楼'
  },
  {
    id: 2,
    name: '进口车厘子 JJ级 1kg',
    category: '水果',
    image: 'https://images.unsplash.com/photo-1528821128474-27f963b4db05?w=400&h=300&fit=crop',
    groupPrice: 59.9,
    originalPrice: 99.9,
    stock: 20,
    limitBuy: 1,
    needCount: 10,
    currentCount: 10,
    status: 'success',
    endTime: '2024-01-18 23:59:59',
    leader: '李大姐',
    address: '阳光花园3号楼'
  },
  {
    id: 3,
    name: '有机蔬菜套餐 6种蔬菜',
    category: '蔬菜',
    image: 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop',
    groupPrice: 29.9,
    originalPrice: 49.9,
    stock: 0,
    limitBuy: 3,
    needCount: 8,
    currentCount: 2,
    status: 'going',
    endTime: '2024-01-22 23:59:59',
    leader: '王叔叔',
    address: '和平小区5号楼'
  },
  {
    id: 4,
    name: '散养土鸡蛋 30枚',
    category: '蛋奶',
    image: 'https://images.unsplash.com/photo-1582722882960-6ac87ca7c144?w=400&h=300&fit=crop',
    groupPrice: 35.0,
    originalPrice: 55.0,
    stock: 3,
    limitBuy: 2,
    needCount: 6,
    currentCount: 1,
    status: 'going',
    endTime: '2024-01-21 23:59:59',
    leader: '刘阿姨',
    address: '绿地小区2号楼'
  },
  {
    id: 5,
    name: '精选五花肉 500g',
    category: '肉类',
    image: 'https://images.unsplash.com/photo-1602473812169-ede48e0ae66f?w=400&h=300&fit=crop',
    groupPrice: 25.9,
    originalPrice: 45.9,
    stock: 100,
    limitBuy: 5,
    needCount: 7,
    currentCount: 4,
    status: 'going',
    endTime: '2024-01-19 23:59:59',
    leader: '陈大哥',
    address: '锦绣家园1号楼'
  },
  {
    id: 6,
    name: '东北大米 5kg袋装',
    category: '粮油',
    image: 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=300&fit=crop',
    groupPrice: 39.9,
    originalPrice: 69.9,
    stock: 80,
    limitBuy: 4,
    needCount: 10,
    currentCount: 3,
    status: 'going',
    endTime: '2024-01-23 23:59:59',
    leader: '赵阿姨',
    address: '东方明珠4号楼'
  },
  {
    id: 7,
    name: '鲜榨花生油 1L',
    category: '粮油',
    image: 'https://images.unsplash.com/photo-1474979266404-7eaac8384e39?w=400&h=300&fit=crop',
    groupPrice: 45.0,
    originalPrice: 75.0,
    stock: 15,
    limitBuy: 3,
    needCount: 5,
    currentCount: 5,
    status: 'success',
    endTime: '2024-01-17 23:59:59',
    leader: '孙大姐',
    address: '金色阳光2号楼'
  },
  {
    id: 8,
    name: '新鲜牛奶 1L*6盒',
    category: '蛋奶',
    image: 'https://images.unsplash.com/photo-1563636619-e9143da7973b?w=400&h=300&fit=crop',
    groupPrice: 49.9,
    originalPrice: 79.9,
    stock: 1,
    limitBuy: 2,
    needCount: 4,
    currentCount: 0,
    status: 'fail',
    endTime: '2024-01-15 23:59:59',
    leader: '周阿姨',
    address: '西湖花园5号楼'
  }
]

export const categories = ['全部', '水果', '蔬菜', '肉类', '蛋奶', '粮油']

export const ordersList = [
  {
    id: 'ORD20240116001',
    goodsName: '新鲜草莓 500g 盒装',
    category: '水果',
    groupStatus: 'going',
    buyerName: '张三',
    phone: '13800138001',
    quantity: 2,
    totalPrice: 39.8,
    orderTime: '2024-01-16 10:30:00',
    pickUpDate: '2024-01-18',
    status: 'pending',
    pickUpCode: 'A12345'
  },
  {
    id: 'ORD20240116002',
    goodsName: '进口车厘子 JJ级 1kg',
    category: '水果',
    groupStatus: 'success',
    buyerName: '李四',
    phone: '13800138002',
    quantity: 1,
    totalPrice: 59.9,
    orderTime: '2024-01-16 11:20:00',
    pickUpDate: '2024-01-19',
    status: 'paid',
    pickUpCode: 'B12346'
  },
  {
    id: 'ORD20240116003',
    goodsName: '有机蔬菜套餐 6种蔬菜',
    category: '蔬菜',
    groupStatus: 'going',
    buyerName: '王五',
    phone: '13800138003',
    quantity: 3,
    totalPrice: 89.7,
    orderTime: '2024-01-16 14:15:00',
    pickUpDate: '2024-01-20',
    status: 'shipped',
    pickUpCode: 'C12347'
  },
  {
    id: 'ORD20240116004',
    goodsName: '散养土鸡蛋 30枚',
    category: '蛋奶',
    groupStatus: 'going',
    buyerName: '赵六',
    phone: '13800138004',
    quantity: 1,
    totalPrice: 35.0,
    orderTime: '2024-01-16 15:45:00',
    pickUpDate: '2024-01-17',
    status: 'picked',
    pickUpCode: 'D12348'
  },
  {
    id: 'ORD20240116005',
    goodsName: '精选五花肉 500g',
    category: '肉类',
    groupStatus: 'going',
    buyerName: '钱七',
    phone: '13800138005',
    quantity: 2,
    totalPrice: 51.8,
    orderTime: '2024-01-16 16:30:00',
    pickUpDate: '2024-01-18',
    status: 'completed',
    pickUpCode: 'E12349'
  },
  {
    id: 'ORD20240116006',
    goodsName: '东北大米 5kg袋装',
    category: '粮油',
    groupStatus: 'going',
    buyerName: '孙八',
    phone: '13800138006',
    quantity: 2,
    totalPrice: 79.8,
    orderTime: '2024-01-16 17:00:00',
    pickUpDate: '2024-01-21',
    status: 'paid',
    pickUpCode: 'F12350'
  },
  {
    id: 'ORD20240116007',
    goodsName: '鲜榨花生油 1L',
    category: '粮油',
    groupStatus: 'success',
    buyerName: '周九',
    phone: '13800138007',
    quantity: 1,
    totalPrice: 45.0,
    orderTime: '2024-01-16 17:30:00',
    pickUpDate: '2024-01-19',
    status: 'shipped',
    pickUpCode: 'G12351'
  },
  {
    id: 'ORD20240116008',
    goodsName: '新鲜牛奶 1L*6盒',
    category: '蛋奶',
    groupStatus: 'fail',
    buyerName: '吴十',
    phone: '13800138008',
    quantity: 1,
    totalPrice: 49.9,
    orderTime: '2024-01-16 18:00:00',
    pickUpDate: '2024-01-20',
    status: 'pending',
    pickUpCode: 'H12352'
  }
]

export const groupProgressList = [
  {
    id: 1,
    goodsName: '新鲜草莓 500g 盒装',
    image: 'https://images.unsplash.com/photo-1464965911861-746a04b4bca7?w=200&h=150&fit=crop',
    needCount: 5,
    currentCount: 3,
    endTime: '2024-01-20 23:59:59',
    members: [
      { name: '张阿姨', isLeader: true },
      { name: '李四', isLeader: false },
      { name: '王五', isLeader: false }
    ]
  },
  {
    id: 2,
    goodsName: '有机蔬菜套餐 6种蔬菜',
    image: 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=200&h=150&fit=crop',
    needCount: 8,
    currentCount: 2,
    endTime: '2024-01-22 23:59:59',
    members: [
      { name: '王叔叔', isLeader: true },
      { name: '赵六', isLeader: false }
    ]
  },
  {
    id: 3,
    goodsName: '精选五花肉 500g',
    image: 'https://images.unsplash.com/photo-1602473812169-ede48e0ae66f?w=200&h=150&fit=crop',
    needCount: 7,
    currentCount: 4,
    endTime: '2024-01-19 23:59:59',
    members: [
      { name: '陈大哥', isLeader: true },
      { name: '钱七', isLeader: false },
      { name: '孙八', isLeader: false },
      { name: '周九', isLeader: false }
    ]
  },
  {
    id: 4,
    goodsName: '东北大米 5kg袋装',
    image: 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=200&h=150&fit=crop',
    needCount: 10,
    currentCount: 3,
    endTime: '2024-01-23 23:59:59',
    members: [
      { name: '赵阿姨', isLeader: true },
      { name: '吴十', isLeader: false },
      { name: '郑十一', isLeader: false }
    ]
  }
]