export const roomTypes = [
  {
    id: 1,
    name: '标准单人间',
    price: 199,
    originalPrice: 299,
    area: 25,
    bedType: '单人床',
    capacity: 1,
    floor: '3-5层',
    facilities: ['WiFi', '空调', '电视', '独立卫浴', '24小时热水'],
    description: '温馨舒适的单人间，适合商务出行或独自旅行',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=modern%20hotel%20single%20room%20with%20single%20bed%20minimalist%20style&image_size=square_hd',
    totalRooms: 15,
    availableRooms: 8
  },
  {
    id: 2,
    name: '标准双人间',
    price: 299,
    originalPrice: 399,
    area: 30,
    bedType: '双人床',
    capacity: 2,
    floor: '2-6层',
    facilities: ['WiFi', '空调', '电视', '独立卫浴', '24小时热水', '迷你吧'],
    description: '宽敞明亮的双人间，适合情侣或朋友出行',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=modern%20hotel%20double%20room%20with%20king%20bed%20elegant%20style&image_size=square_hd',
    totalRooms: 20,
    availableRooms: 12
  },
  {
    id: 3,
    name: '豪华大床房',
    price: 499,
    originalPrice: 699,
    area: 40,
    bedType: '特大床',
    capacity: 2,
    floor: '7-10层',
    facilities: ['WiFi', '空调', '智能电视', '独立卫浴', '24小时热水', '迷你吧', '保险箱', '浴缸'],
    description: '豪华配置的大床房，享受尊贵入住体验',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=luxury%20hotel%20king%20bed%20room%20elegant%20decoration&image_size=square_hd',
    totalRooms: 10,
    availableRooms: 5
  },
  {
    id: 4,
    name: '家庭套房',
    price: 699,
    originalPrice: 899,
    area: 60,
    bedType: '双床',
    capacity: 4,
    floor: '8-12层',
    facilities: ['WiFi', '空调', '智能电视', '独立卫浴', '24小时热水', '迷你吧', '保险箱', '浴缸', '客厅'],
    description: '宽敞的家庭套房，适合全家出行入住',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=luxury%20hotel%20family%20suite%20with%20living%20room&image_size=square_hd',
    totalRooms: 8,
    availableRooms: 3
  },
  {
    id: 5,
    name: '总统套房',
    price: 1999,
    originalPrice: 2599,
    area: 120,
    bedType: '特大床',
    capacity: 2,
    floor: '顶层',
    facilities: ['WiFi', '中央空调', '智能电视', '独立卫浴', '24小时热水', '迷你吧', '保险箱', '按摩浴缸', '独立客厅', '书房', '管家服务'],
    description: '顶级尊享总统套房，尽享奢华体验',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=luxury%20presidential%20suite%20hotel%20room%20opulent&image_size=square_hd',
    totalRooms: 2,
    availableRooms: 1
  }
]

export const rooms = [
  { id: 101, number: '101', type: '标准单人间', floor: 1, status: 'available', price: 199 },
  { id: 102, number: '102', type: '标准单人间', floor: 1, status: 'occupied', price: 199 },
  { id: 103, number: '103', type: '标准单人间', floor: 1, status: 'cleaning', price: 199 },
  { id: 104, number: '104', type: '标准单人间', floor: 1, status: 'maintenance', price: 199 },
  { id: 201, number: '201', type: '标准双人间', floor: 2, status: 'available', price: 299 },
  { id: 202, number: '202', type: '标准双人间', floor: 2, status: 'occupied', price: 299 },
  { id: 203, number: '203', type: '标准双人间', floor: 2, status: 'available', price: 299 },
  { id: 204, number: '204', type: '标准双人间', floor: 2, status: 'cleaning', price: 299 },
  { id: 301, number: '301', type: '豪华大床房', floor: 3, status: 'available', price: 499 },
  { id: 302, number: '302', type: '豪华大床房', floor: 3, status: 'occupied', price: 499 },
  { id: 303, number: '303', type: '豪华大床房', floor: 3, status: 'available', price: 499 },
  { id: 401, number: '401', type: '家庭套房', floor: 4, status: 'available', price: 699 },
  { id: 402, number: '402', type: '家庭套房', floor: 4, status: 'occupied', price: 699 },
  { id: 501, number: '501', type: '总统套房', floor: 5, status: 'available', price: 1999 }
]

export const orders = [
  {
    id: 'ORD202401001',
    guestName: '张三',
    phone: '13800138001',
    idCard: '110101199001011234',
    roomType: '标准双人间',
    roomNumber: '202',
    checkInDate: '2024-01-15',
    checkOutDate: '2024-01-18',
    days: 3,
    totalPrice: 897,
    status: 'checked_in',
    createTime: '2024-01-14 10:30:00'
  },
  {
    id: 'ORD202401002',
    guestName: '李四',
    phone: '13800138002',
    idCard: '110101199002025678',
    roomType: '豪华大床房',
    roomNumber: '302',
    checkInDate: '2024-01-16',
    checkOutDate: '2024-01-20',
    days: 4,
    totalPrice: 1996,
    status: 'confirmed',
    createTime: '2024-01-15 14:20:00'
  },
  {
    id: 'ORD202401003',
    guestName: '王五',
    phone: '13800138003',
    idCard: '110101199003039012',
    roomType: '家庭套房',
    roomNumber: '402',
    checkInDate: '2024-01-10',
    checkOutDate: '2024-01-14',
    days: 4,
    totalPrice: 2796,
    status: 'completed',
    createTime: '2024-01-09 09:15:00'
  },
  {
    id: 'ORD202401004',
    guestName: '赵六',
    phone: '13800138004',
    idCard: '110101199004043456',
    roomType: '标准单人间',
    roomNumber: '102',
    checkInDate: '2024-01-17',
    checkOutDate: '2024-01-19',
    days: 2,
    totalPrice: 398,
    status: 'pending',
    createTime: '2024-01-16 16:45:00'
  },
  {
    id: 'ORD202401005',
    guestName: '孙七',
    phone: '13800138005',
    idCard: '110101199005057890',
    roomType: '总统套房',
    roomNumber: '501',
    checkInDate: '2024-01-20',
    checkOutDate: '2024-01-22',
    days: 2,
    totalPrice: 3998,
    status: 'cancelled',
    createTime: '2024-01-12 11:00:00'
  }
]

export const statusMap = {
  available: { label: '空闲', type: 'success' },
  occupied: { label: '已入住', type: 'danger' },
  cleaning: { label: '清洁中', type: 'warning' },
  maintenance: { label: '维护中', type: 'info' }
}

export const orderStatusMap = {
  pending: { label: '待确认', type: 'warning' },
  confirmed: { label: '已确认', type: 'primary' },
  checked_in: { label: '已入住', type: 'success' },
  completed: { label: '已完成', type: 'info' },
  cancelled: { label: '已取消', type: 'danger' }
}
