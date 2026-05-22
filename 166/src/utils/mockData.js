export const bookCategories = [
  '文学小说',
  '科技计算机',
  '经济管理',
  '历史传记',
  '教育教材',
  '艺术设计',
  '生活娱乐',
  '其他'
]

export const bookConditions = [
  { label: '全新', value: 'new', discount: 0.8 },
  { label: '九成新', value: 'like_new', discount: 0.7 },
  { label: '八成新', value: 'good', discount: 0.6 },
  { label: '七成新', value: 'fair', discount: 0.5 },
  { label: '六成新及以下', value: 'poor', discount: 0.3 }
]

export const mockBooks = [
  {
    id: 1,
    bookName: '三体',
    author: '刘慈欣',
    isbn: '9787536692938',
    category: '文学小说',
    condition: 'like_new',
    originalPrice: 68,
    recyclePrice: 47.6,
    sellPrice: 58,
    stock: 3,
    description: '科幻经典之作，获得雨果奖',
    status: 'on_sale',
    createTime: '2024-01-15 10:30:00'
  },
  {
    id: 2,
    bookName: 'JavaScript高级程序设计',
    author: 'Nicholas C. Zakas',
    isbn: '9787115545381',
    category: '科技计算机',
    condition: 'good',
    originalPrice: 129,
    recyclePrice: 77.4,
    sellPrice: 99,
    stock: 5,
    description: '前端开发必备经典书籍',
    status: 'on_sale',
    createTime: '2024-01-16 14:20:00'
  },
  {
    id: 3,
    bookName: '经济学原理',
    author: '曼昆',
    isbn: '9787301150894',
    category: '经济管理',
    condition: 'fair',
    originalPrice: 89,
    recyclePrice: 44.5,
    sellPrice: 59,
    stock: 0,
    description: '经济学入门经典教材',
    status: 'sold',
    createTime: '2024-01-17 09:15:00'
  },
  {
    id: 4,
    bookName: '明朝那些事儿',
    author: '当年明月',
    isbn: '9787505722460',
    category: '历史传记',
    condition: 'good',
    originalPrice: 358,
    recyclePrice: 214.8,
    sellPrice: 268,
    stock: 2,
    description: '全套7册，历史普及读物',
    status: 'on_sale',
    createTime: '2024-01-18 16:45:00'
  },
  {
    id: 5,
    bookName: '高等数学',
    author: '同济大学数学系',
    isbn: '9787040396622',
    category: '教育教材',
    condition: 'poor',
    originalPrice: 45,
    recyclePrice: 13.5,
    sellPrice: 20,
    stock: 1,
    description: '有笔记划线，不影响阅读',
    status: 'pending',
    createTime: '2024-01-19 11:00:00'
  }
]

export const mockOrders = [
  {
    id: 1,
    orderNo: 'ORD202401200001',
    bookName: '经济学原理',
    buyerName: '张三',
    buyerPhone: '13800138001',
    buyerAddress: '北京市朝阳区xxx街道xxx号',
    price: 59,
    status: 'completed',
    createTime: '2024-01-20 10:30:00',
    completeTime: '2024-01-21 15:00:00'
  },
  {
    id: 2,
    orderNo: 'ORD202401210002',
    bookName: '三体',
    buyerName: '李四',
    buyerPhone: '13900139002',
    buyerAddress: '上海市浦东新区xxx路xxx号',
    price: 58,
    status: 'shipped',
    createTime: '2024-01-21 09:20:00',
    shipTime: '2024-01-21 14:00:00'
  },
  {
    id: 3,
    orderNo: 'ORD202401220003',
    bookName: 'JavaScript高级程序设计',
    buyerName: '王五',
    buyerPhone: '13700137003',
    buyerAddress: '广州市天河区xxx路xxx号',
    price: 99,
    status: 'pending',
    createTime: '2024-01-22 11:45:00'
  }
]

export const mockRecycleRecords = [
  {
    id: 1,
    bookName: '三体',
    author: '刘慈欣',
    sellerName: '赵六',
    sellerPhone: '13600136001',
    condition: 'like_new',
    originalPrice: 68,
    recyclePrice: 47.6,
    status: 'completed',
    createTime: '2024-01-15 10:30:00',
    completeTime: '2024-01-15 16:00:00'
  },
  {
    id: 2,
    bookName: 'JavaScript高级程序设计',
    author: 'Nicholas C. Zakas',
    sellerName: '孙七',
    sellerPhone: '13500135002',
    condition: 'good',
    originalPrice: 129,
    recyclePrice: 77.4,
    status: 'completed',
    createTime: '2024-01-16 14:20:00',
    completeTime: '2024-01-16 18:30:00'
  },
  {
    id: 3,
    bookName: '经济学原理',
    author: '曼昆',
    sellerName: '周八',
    sellerPhone: '13400134003',
    condition: 'fair',
    originalPrice: 89,
    recyclePrice: 44.5,
    status: 'pending',
    createTime: '2024-01-17 09:15:00'
  },
  {
    id: 4,
    bookName: '明朝那些事儿',
    author: '当年明月',
    sellerName: '吴九',
    sellerPhone: '13300133004',
    condition: 'good',
    originalPrice: 358,
    recyclePrice: 214.8,
    status: 'completed',
    createTime: '2024-01-18 16:45:00',
    completeTime: '2024-01-18 20:00:00'
  },
  {
    id: 5,
    bookName: '高等数学',
    author: '同济大学数学系',
    sellerName: '郑十',
    sellerPhone: '13200132005',
    condition: 'poor',
    originalPrice: 45,
    recyclePrice: 13.5,
    status: 'rejected',
    createTime: '2024-01-19 11:00:00',
    rejectReason: '书籍破损严重，影响阅读'
  }
]

export const orderStatusMap = {
  pending: { label: '待发货', type: 'warning' },
  shipped: { label: '已发货', type: 'primary' },
  completed: { label: '已完成', type: 'success' },
  cancelled: { label: '已取消', type: 'danger' }
}

export const recycleStatusMap = {
  pending: { label: '待审核', type: 'warning' },
  completed: { label: '已完成', type: 'success' },
  rejected: { label: '已拒绝', type: 'danger' }
}

export const bookStatusMap = {
  pending: { label: '待上架', type: 'info' },
  on_sale: { label: '售卖中', type: 'success' },
  sold: { label: '已售出', type: 'primary' },
  off_shelf: { label: '已下架', type: 'danger' }
}
