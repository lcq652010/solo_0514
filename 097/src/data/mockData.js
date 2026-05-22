export const mockCategories = [
  { id: 1, name: '热菜', sort: 1, status: 1, createTime: '2024-01-01 10:00:00' },
  { id: 2, name: '凉菜', sort: 2, status: 1, createTime: '2024-01-01 10:05:00' },
  { id: 3, name: '主食', sort: 3, status: 1, createTime: '2024-01-01 10:10:00' },
  { id: 4, name: '汤品', sort: 4, status: 1, createTime: '2024-01-01 10:15:00' },
  { id: 5, name: '饮品', sort: 5, status: 0, createTime: '2024-01-01 10:20:00' }
]

export const mockDishes = [
  { id: 1, name: '宫保鸡丁', categoryId: 1, price: 38, originalPrice: 48, image: '', description: '经典川菜，鸡肉嫩滑', status: 1, sort: 1, stock: 50, createTime: '2024-01-01 11:00:00' },
  { id: 2, name: '麻婆豆腐', categoryId: 1, price: 28, originalPrice: 35, image: '', description: '麻辣鲜香，下饭神器', status: 1, sort: 2, stock: 35, createTime: '2024-01-01 11:05:00' },
  { id: 3, name: '凉拌黄瓜', categoryId: 2, price: 18, originalPrice: 22, image: '', description: '清爽解腻', status: 1, sort: 1, stock: 20, createTime: '2024-01-01 11:10:00' },
  { id: 4, name: '米饭', categoryId: 3, price: 3, originalPrice: 3, image: '', description: '东北大米', status: 1, sort: 1, stock: 100, createTime: '2024-01-01 11:15:00' },
  { id: 5, name: '西红柿鸡蛋汤', categoryId: 4, price: 15, originalPrice: 18, image: '', description: '营养美味', status: 1, sort: 1, stock: 0, createTime: '2024-01-01 11:20:00' },
  { id: 6, name: '可乐', categoryId: 5, price: 5, originalPrice: 6, image: '', description: '冰镇可乐', status: 0, sort: 1, stock: 0, createTime: '2024-01-01 11:25:00' }
]

export const mockOrders = [
  { id: 'ORD202405160001', customerName: '张三', phone: '13800138001', address: '北京市朝阳区xxx街道123号', totalPrice: 56, status: 1, type: 1, remark: '不要辣', createTime: '2024-05-16 12:00:00', dishes: [{ name: '宫保鸡丁', price: 38, quantity: 1 }, { name: '米饭', price: 3, quantity: 2 }] },
  { id: 'ORD202405160002', customerName: '李四', phone: '13800138002', address: '北京市海淀区xxx路456号', totalPrice: 46, status: 2, type: 1, remark: '', createTime: '2024-05-16 12:10:00', dishes: [{ name: '麻婆豆腐', price: 28, quantity: 1 }, { name: '米饭', price: 3, quantity: 2 }, { name: '凉拌黄瓜', price: 18, quantity: 1 }] },
  { id: 'ORD202405160003', customerName: '王五', phone: '13800138003', address: '北京市西城区xxx胡同789号', totalPrice: 38, status: 3, type: 2, remark: '多放香菜', createTime: '2024-05-16 12:20:00', dishes: [{ name: '宫保鸡丁', price: 38, quantity: 1 }] },
  { id: 'ORD202405160004', customerName: '赵六', phone: '13800138004', address: '北京市东城区xxx大街012号', totalPrice: 33, status: 4, type: 1, remark: '', createTime: '2024-05-16 12:30:00', dishes: [{ name: '西红柿鸡蛋汤', price: 15, quantity: 1 }, { name: '凉拌黄瓜', price: 18, quantity: 1 }] },
  { id: 'ORD202405160005', customerName: '孙七', phone: '13800138005', address: '北京市丰台区xxx路345号', totalPrice: 76, status: 5, type: 2, remark: '尽快送达', createTime: '2024-05-16 12:40:00', dishes: [{ name: '宫保鸡丁', price: 38, quantity: 2 }] }
]

export const orderStatusMap = {
  1: { label: '待接单', type: 'warning' },
  2: { label: '已接单', type: 'primary' },
  3: { label: '制作中', type: 'info' },
  4: { label: '待配送', type: 'success' },
  5: { label: '已完成', type: 'success' },
  6: { label: '已取消', type: 'danger' }
}

export const orderTypeMap = {
  1: '外卖',
  2: '堂食'
}