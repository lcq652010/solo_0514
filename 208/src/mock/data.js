export const productCategories = [
  { value: '蔬菜', label: '蔬菜' },
  { value: '水果', label: '水果' },
  { value: '肉类', label: '肉类' },
  { value: '水产', label: '水产' },
  { value: '粮油', label: '粮油' },
  { value: '干货', label: '干货' }
]

export const products = [
  { id: 1, name: '西红柿', category: '蔬菜', unit: '斤', price: 3.5, stock: 500, spec: '一级', createTime: '2024-01-15 09:30:00' },
  { id: 2, name: '黄瓜', category: '蔬菜', unit: '斤', price: 2.8, stock: 300, spec: '新鲜', createTime: '2024-01-15 09:31:00' },
  { id: 3, name: '苹果', category: '水果', unit: '斤', price: 5.5, stock: 800, spec: '红富士', createTime: '2024-01-15 09:32:00' },
  { id: 4, name: '香蕉', category: '水果', unit: '斤', price: 4.2, stock: 400, spec: '海南', createTime: '2024-01-15 09:33:00' },
  { id: 5, name: '猪肉', category: '肉类', unit: '斤', price: 25.0, stock: 200, spec: '五花肉', createTime: '2024-01-15 09:34:00' },
  { id: 6, name: '牛肉', category: '肉类', unit: '斤', price: 45.0, stock: 150, spec: '牛腩', createTime: '2024-01-15 09:35:00' },
  { id: 7, name: '草鱼', category: '水产', unit: '斤', price: 12.0, stock: 100, spec: '鲜活', createTime: '2024-01-15 09:36:00' },
  { id: 8, name: '大米', category: '粮油', unit: '袋', price: 120.0, stock: 60, spec: '10kg装', createTime: '2024-01-15 09:37:00' },
  { id: 9, name: '面粉', category: '粮油', unit: '袋', price: 85.0, stock: 45, spec: '5kg装', createTime: '2024-01-15 09:38:00' },
  { id: 10, name: '香菇', category: '干货', unit: '斤', price: 35.0, stock: 80, spec: '干香菇', createTime: '2024-01-15 09:39:00' }
]

export const suppliers = [
  { id: 1, name: '绿源蔬菜基地', contact: '张三', phone: '13800138001', address: '北京市海淀区蔬菜基地A区', type: '蔬菜', status: 1, createTime: '2024-01-10 10:00:00',
    products: [
      { productId: 1, productName: '西红柿', availableQuantity: 1000 },
      { productId: 2, productName: '黄瓜', availableQuantity: 800 }
    ]
  },
  { id: 2, name: '鲜果水果批发', contact: '李四', phone: '13800138002', address: '北京市朝阳区水果市场B栋', type: '水果', status: 1, createTime: '2024-01-11 10:00:00',
    products: [
      { productId: 3, productName: '苹果', availableQuantity: 500 },
      { productId: 4, productName: '香蕉', availableQuantity: 300 }
    ]
  },
  { id: 3, name: '诚信肉业', contact: '王五', phone: '13800138003', address: '北京市丰台区肉类加工厂', type: '肉类', status: 1, createTime: '2024-01-12 10:00:00',
    products: [
      { productId: 5, productName: '猪肉', availableQuantity: 200 },
      { productId: 6, productName: '牛肉', availableQuantity: 100 }
    ]
  },
  { id: 4, name: '水产直供中心', contact: '赵六', phone: '13800138004', address: '北京市通州区水产市场', type: '水产', status: 0, createTime: '2024-01-13 10:00:00',
    products: [
      { productId: 7, productName: '草鱼', availableQuantity: 150 }
    ]
  },
  { id: 5, name: '金龙粮油批发', contact: '钱七', phone: '13800138005', address: '北京市大兴区粮油仓库', type: '粮油', status: 1, createTime: '2024-01-14 10:00:00',
    products: [
      { productId: 8, productName: '大米', availableQuantity: 100 },
      { productId: 9, productName: '面粉', availableQuantity: 80 },
      { productId: 10, productName: '香菇', availableQuantity: 200 }
    ]
  }
]

export const orders = [
  {
    id: 'PO202401150001',
    supplierId: 1,
    supplierName: '绿源蔬菜基地',
    totalAmount: 1850.0,
    status: 'pending',
    createTime: '2024-01-15 10:30:00',
    items: [
      { productId: 1, productName: '西红柿', quantity: 200, unit: '斤', price: 3.5, amount: 700.0 },
      { productId: 2, productName: '黄瓜', quantity: 150, unit: '斤', price: 2.8, amount: 420.0 },
      { productId: 9, productName: '面粉', quantity: 6, unit: '袋', price: 85.0, amount: 510.0 }
    ]
  },
  {
    id: 'PO202401150002',
    supplierId: 2,
    supplierName: '鲜果水果批发',
    totalAmount: 1670.0,
    status: 'confirmed',
    createTime: '2024-01-15 11:00:00',
    items: [
      { productId: 3, productName: '苹果', quantity: 200, unit: '斤', price: 5.5, amount: 1100.0 },
      { productId: 4, productName: '香蕉', quantity: 100, unit: '斤', price: 4.2, amount: 420.0 }
    ]
  },
  {
    id: 'PO202401140001',
    supplierId: 3,
    supplierName: '诚信肉业',
    totalAmount: 5750.0,
    status: 'stocked',
    createTime: '2024-01-14 09:00:00',
    stockInTime: '2024-01-15 08:30:00',
    items: [
      { productId: 5, productName: '猪肉', quantity: 150, unit: '斤', price: 25.0, amount: 3750.0 },
      { productId: 6, productName: '牛肉', quantity: 50, unit: '斤', price: 45.0, amount: 2250.0 }
    ]
  },
  {
    id: 'PO202401140002',
    supplierId: 5,
    supplierName: '金龙粮油批发',
    totalAmount: 3300.0,
    status: 'cancelled',
    createTime: '2024-01-14 14:00:00',
    items: [
      { productId: 8, productName: '大米', quantity: 25, unit: '袋', price: 120.0, amount: 3000.0 },
      { productId: 9, productName: '面粉', quantity: 3, unit: '袋', price: 85.0, amount: 255.0 }
    ]
  }
]

export const statusMap = {
  pending: { label: '待确认', class: 'status-pending' },
  confirmed: { label: '已确认', class: 'status-confirmed' },
  stocked: { label: '已入库', class: 'status-stocked' },
  cancelled: { label: '已取消', class: 'status-cancelled' }
}
