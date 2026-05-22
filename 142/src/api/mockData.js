import moment from 'moment'

export const mockProducts = [
  { id: 1, name: '农夫山泉矿泉水', code: 'SKU001', category: '饮料', price: 2.00, stock: 150, minStock: 50, unit: '瓶', createTime: '2024-01-01 10:00:00' },
  { id: 2, name: '可口可乐', code: 'SKU002', category: '饮料', price: 3.50, stock: 200, minStock: 60, unit: '瓶', createTime: '2024-01-02 11:30:00' },
  { id: 3, name: '康师傅红烧牛肉面', code: 'SKU003', category: '食品', price: 4.50, stock: 80, minStock: 30, unit: '包', createTime: '2024-01-03 09:15:00' },
  { id: 4, name: '蒙牛纯牛奶', code: 'SKU004', category: '乳制品', price: 5.50, stock: 120, minStock: 40, unit: '盒', createTime: '2024-01-04 14:20:00' },
  { id: 5, name: '金龙鱼调和油', code: 'SKU005', category: '粮油', price: 68.00, stock: 25, minStock: 20, unit: '桶', createTime: '2024-01-05 16:45:00' },
  { id: 6, name: '洁柔抽纸', code: 'SKU006', category: '日用品', price: 12.00, stock: 15, minStock: 25, unit: '提', createTime: '2024-01-06 08:30:00' },
  { id: 7, name: '旺仔牛奶', code: 'SKU007', category: '乳制品', price: 4.00, stock: 45, minStock: 50, unit: '罐', createTime: '2024-01-07 13:00:00' },
  { id: 8, name: '乐事薯片', code: 'SKU008', category: '食品', price: 8.50, stock: 60, minStock: 20, unit: '袋', createTime: '2024-01-08 10:30:00' },
  { id: 9, name: '海天酱油', code: 'SKU009', category: '粮油', price: 15.00, stock: 10, minStock: 15, unit: '瓶', createTime: '2024-01-09 15:20:00' },
  { id: 10, name: '伊利酸奶', code: 'SKU010', category: '乳制品', price: 6.00, stock: 5, minStock: 30, unit: '杯', createTime: '2024-01-10 09:45:00' }
]

export const mockInventoryRecords = [
  { id: 1, productId: 1, productName: '农夫山泉矿泉水', category: '饮料', type: 'in', quantity: 50, operator: '张三', remark: '正常补货', createTime: '2024-01-15 09:00:00' },
  { id: 2, productId: 2, productName: '可口可乐', category: '饮料', type: 'in', quantity: 30, operator: '张三', remark: '正常补货', createTime: '2024-01-15 10:30:00' },
  { id: 3, productId: 3, productName: '康师傅红烧牛肉面', category: '食品', type: 'out', quantity: 10, operator: '李四', remark: '销售出库', createTime: '2024-01-15 14:00:00' },
  { id: 4, productId: 4, productName: '蒙牛纯牛奶', category: '乳制品', type: 'in', quantity: 40, operator: '张三', remark: '正常补货', createTime: '2024-01-16 08:30:00' },
  { id: 5, productId: 5, productName: '金龙鱼调和油', category: '粮油', type: 'out', quantity: 5, operator: '李四', remark: '销售出库', createTime: '2024-01-16 11:15:00' },
  { id: 6, productId: 1, productName: '农夫山泉矿泉水', category: '饮料', type: 'out', quantity: 20, operator: '李四', remark: '销售出库', createTime: '2024-01-16 15:45:00' },
  { id: 7, productId: 6, productName: '洁柔抽纸', category: '日用品', type: 'in', quantity: 20, operator: '张三', remark: '正常补货', createTime: '2024-01-17 09:30:00' },
  { id: 8, productId: 7, productName: '旺仔牛奶', category: '乳制品', type: 'in', quantity: 25, operator: '张三', remark: '正常补货', createTime: '2024-01-17 13:00:00' },
  { id: 9, productId: 8, productName: '乐事薯片', category: '食品', type: 'out', quantity: 15, operator: '李四', remark: '销售出库', createTime: '2024-01-18 10:00:00' },
  { id: 10, productId: 9, productName: '海天酱油', category: '粮油', type: 'in', quantity: 15, operator: '张三', remark: '紧急补货', createTime: '2024-01-18 16:30:00' }
]

export const categories = ['饮料', '食品', '乳制品', '粮油', '日用品', '零食']

let products = [...mockProducts]
let records = [...mockInventoryRecords]

class EventBus {
  constructor() {
    this.events = {}
  }
  on(event, callback) {
    if (!this.events[event]) {
      this.events[event] = []
    }
    this.events[event].push(callback)
  }
  emit(event, data) {
    if (this.events[event]) {
      this.events[event].forEach(callback => callback(data))
    }
  }
}

export const eventBus = new EventBus()

export const api = {
  getProducts(params = {}) {
    return new Promise(resolve => {
      let result = [...products]
      
      if (params.name) {
        result = result.filter(item => item.name.includes(params.name))
      }
      if (params.code) {
        result = result.filter(item => item.code.includes(params.code))
      }
      if (params.category) {
        result = result.filter(item => item.category === params.category)
      }
      
      const page = params.page || 1
      const pageSize = params.pageSize || 10
      const start = (page - 1) * pageSize
      const end = start + pageSize
      
      setTimeout(() => {
        resolve({
          code: 200,
          data: {
            list: result.slice(start, end),
            total: result.length,
            page,
            pageSize
          }
        })
      }, 300)
    })
  },

  getProductById(id) {
    return new Promise(resolve => {
      const product = products.find(item => item.id === id)
      setTimeout(() => {
        resolve({
          code: 200,
          data: product
        })
      }, 200)
    })
  },

  addStockIn(data) {
    return new Promise(resolve => {
      const product = products.find(item => item.id === data.productId)
      if (product) {
        product.stock += data.quantity
      }
      
      const newRecord = {
        id: records.length + 1,
        productId: data.productId,
        productName: product ? product.name : '',
        category: product ? product.category : '',
        type: 'in',
        quantity: data.quantity,
        operator: data.operator || '管理员',
        remark: data.remark || '',
        createTime: moment().format('YYYY-MM-DD HH:mm:ss')
      }
      records.unshift(newRecord)
      
      eventBus.emit('stock-updated')
      
      setTimeout(() => {
        resolve({
          code: 200,
          message: '入库成功',
          data: newRecord
        })
      }, 500)
    })
  },

  getWarningProducts() {
    return new Promise(resolve => {
      const warningProducts = products.filter(item => item.stock < item.minStock)
      setTimeout(() => {
        resolve({
          code: 200,
          data: warningProducts
        })
      }, 300)
    })
  },

  getInventoryRecords(params = {}) {
    return new Promise(resolve => {
      let result = [...records]
      
      if (params.type) {
        result = result.filter(item => item.type === params.type)
      }
      if (params.productName) {
        result = result.filter(item => item.productName.includes(params.productName))
      }
      if (params.category) {
        result = result.filter(item => item.category === params.category)
      }
      if (params.startTime) {
        result = result.filter(item => item.createTime >= params.startTime)
      }
      if (params.endTime) {
        result = result.filter(item => item.createTime <= params.endTime + ' 23:59:59')
      }
      
      const page = params.page || 1
      const pageSize = params.pageSize || 10
      const start = (page - 1) * pageSize
      const end = start + pageSize
      
      setTimeout(() => {
        resolve({
          code: 200,
          data: {
            list: result.slice(start, end),
            total: result.length,
            page,
            pageSize
          }
        })
      }, 300)
    })
  }
}
