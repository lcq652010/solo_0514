export const mockOrders = [
  {
    id: 'ORD001',
    tableNo: 'A01',
    customerName: '张先生',
    orderTime: '2024-01-15 12:30:00',
    status: 'cooking',
    items: [
      { id: 1, name: '宫保鸡丁', quantity: 2, price: 38, status: 'cooking', category: '热菜' },
      { id: 2, name: '麻婆豆腐', quantity: 1, price: 22, status: 'waiting', category: '热菜' },
      { id: 3, name: '米饭', quantity: 3, price: 3, status: 'done', category: '主食' }
    ],
    remark: '少辣',
    urgency: false
  },
  {
    id: 'ORD002',
    tableNo: 'B05',
    customerName: '李女士',
    orderTime: '2024-01-15 12:35:00',
    status: 'waiting',
    items: [
      { id: 4, name: '红烧肉', quantity: 1, price: 58, status: 'waiting', category: '热菜' },
      { id: 5, name: '清蒸鲈鱼', quantity: 1, price: 88, status: 'waiting', category: '海鲜' },
      { id: 6, name: '凉拌黄瓜', quantity: 1, price: 18, status: 'done', category: '凉菜' }
    ],
    remark: '',
    urgency: false
  },
  {
    id: 'ORD003',
    tableNo: 'C02',
    customerName: '王先生',
    orderTime: '2024-01-15 12:25:00',
    status: 'urgent',
    items: [
      { id: 7, name: '水煮肉片', quantity: 2, price: 48, status: 'cooking', category: '热菜' },
      { id: 8, name: '担担面', quantity: 2, price: 16, status: 'waiting', category: '主食' }
    ],
    remark: '赶时间，请加快',
    urgency: true
  },
  {
    id: 'ORD004',
    tableNo: 'A03',
    customerName: '赵女士',
    orderTime: '2024-01-15 12:40:00',
    status: 'done',
    items: [
      { id: 9, name: '糖醋里脊', quantity: 1, price: 42, status: 'done', category: '热菜' },
      { id: 10, name: '番茄炒蛋', quantity: 1, price: 26, status: 'done', category: '热菜' }
    ],
    remark: '',
    urgency: false
  },
  {
    id: 'ORD005',
    tableNo: 'D08',
    customerName: '刘先生',
    orderTime: '2024-01-15 12:45:00',
    status: 'waiting',
    items: [
      { id: 11, name: '干锅牛蛙', quantity: 1, price: 68, status: 'waiting', category: '热菜' },
      { id: 12, name: '炒时蔬', quantity: 1, price: 28, status: 'waiting', category: '素菜' },
      { id: 13, name: '紫菜蛋花汤', quantity: 1, price: 18, status: 'waiting', category: '汤品' }
    ],
    remark: '不要香菜',
    urgency: false
  }
]

export const dishes = [
  { id: 1, name: '宫保鸡丁', category: '热菜', price: 38 },
  { id: 2, name: '麻婆豆腐', category: '热菜', price: 22 },
  { id: 3, name: '红烧肉', category: '热菜', price: 58 },
  { id: 4, name: '清蒸鲈鱼', category: '海鲜', price: 88 },
  { id: 5, name: '凉拌黄瓜', category: '凉菜', price: 18 },
  { id: 6, name: '水煮肉片', category: '热菜', price: 48 },
  { id: 7, name: '糖醋里脊', category: '热菜', price: 42 },
  { id: 8, name: '番茄炒蛋', category: '热菜', price: 26 },
  { id: 9, name: '干锅牛蛙', category: '热菜', price: 68 },
  { id: 10, name: '炒时蔬', category: '素菜', price: 28 },
  { id: 11, name: '紫菜蛋花汤', category: '汤品', price: 18 },
  { id: 12, name: '米饭', category: '主食', price: 3 },
  { id: 13, name: '担担面', category: '主食', price: 16 }
]
