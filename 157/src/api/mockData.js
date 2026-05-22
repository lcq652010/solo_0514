export const categories = [
  { id: 1, name: '书写工具', description: '笔类用品', sort: 1, status: 1, createTime: '2024-01-01' },
  { id: 2, name: '纸制品', description: '纸张、笔记本等', sort: 2, status: 1, createTime: '2024-01-02' },
  { id: 3, name: '办公文具', description: '文件夹、订书机等', sort: 3, status: 1, createTime: '2024-01-03' },
  { id: 4, name: '办公设备', description: '打印机、扫描仪等', sort: 4, status: 1, createTime: '2024-01-04' },
  { id: 5, name: '清洁用品', description: '清洁工具', sort: 5, status: 0, createTime: '2024-01-05' }
]

export const supplies = [
  { id: 1, name: '黑色中性笔', categoryId: 1, categoryName: '书写工具', spec: '0.5mm', unit: '支', stock: 500, minStock: 50, price: 2.5, status: 1 },
  { id: 2, name: 'A4打印纸', categoryId: 2, categoryName: '纸制品', spec: '70g', unit: '包', stock: 200, minStock: 30, price: 25.0, status: 1 },
  { id: 3, name: '文件夹', categoryId: 3, categoryName: '办公文具', spec: 'A4', unit: '个', stock: 150, minStock: 20, price: 5.0, status: 1 },
  { id: 4, name: '订书机', categoryId: 3, categoryName: '办公文具', spec: '标准型', unit: '个', stock: 30, minStock: 5, price: 15.0, status: 1 },
  { id: 5, name: '打印机墨盒', categoryId: 4, categoryName: '办公设备', spec: '标准', unit: '个', stock: 25, minStock: 10, price: 80.0, status: 1 },
  { id: 6, name: '橡皮擦', categoryId: 1, categoryName: '书写工具', spec: '大号', unit: '个', stock: 10, minStock: 20, price: 1.5, status: 0 }
]

export const departments = [
  { id: 1, name: '行政部' },
  { id: 2, name: '技术部' },
  { id: 3, name: '市场部' },
  { id: 4, name: '财务部' },
  { id: 5, name: '人事部' }
]

export const applyRecords = [
  { id: 1, applyNo: 'AP20240501001', departmentId: 1, departmentName: '行政部', applicant: '张三', applyTime: '2024-05-01 09:30:00', status: 2, items: [
    { supplyId: 1, supplyName: '黑色中性笔', quantity: 10, unit: '支' }
  ], remark: '日常办公使用' },
  { id: 2, applyNo: 'AP20240502001', departmentId: 2, departmentName: '技术部', applicant: '李四', applyTime: '2024-05-02 14:20:00', status: 1, items: [
    { supplyId: 2, supplyName: 'A4打印纸', quantity: 5, unit: '包' },
    { supplyId: 3, supplyName: '文件夹', quantity: 20, unit: '个' }
  ], remark: '项目资料整理' },
  { id: 3, applyNo: 'AP20240503001', departmentId: 3, departmentName: '市场部', applicant: '王五', applyTime: '2024-05-03 10:15:00', status: 0, items: [
    { supplyId: 4, supplyName: '订书机', quantity: 2, unit: '个' }
  ], remark: '活动筹备' },
  { id: 4, applyNo: 'AP20240504001', departmentId: 4, departmentName: '财务部', applicant: '赵六', applyTime: '2024-05-04 16:45:00', status: 2, items: [
    { supplyId: 1, supplyName: '黑色中性笔', quantity: 5, unit: '支' },
    { supplyId: 6, supplyName: '橡皮擦', quantity: 10, unit: '个' }
  ], remark: '财务记账' }
]

export const stockInRecords = [
  { id: 1, inNo: 'IN20240501001', supplyId: 1, supplyName: '黑色中性笔', quantity: 200, unit: '支', price: 2.5, totalPrice: 500, operator: '管理员', inTime: '2024-05-01 08:30:00', remark: '常规补货' },
  { id: 2, inNo: 'IN20240502001', supplyId: 2, supplyName: 'A4打印纸', quantity: 100, unit: '包', price: 25.0, totalPrice: 2500, operator: '管理员', inTime: '2024-05-02 09:00:00', remark: '季度采购' },
  { id: 3, inNo: 'IN20240503001', supplyId: 3, supplyName: '文件夹', quantity: 50, unit: '个', price: 5.0, totalPrice: 250, operator: '管理员', inTime: '2024-05-03 14:30:00', remark: '补充库存' }
]

export const statusMap = {
  0: { label: '待审批', type: 'warning' },
  1: { label: '已通过', type: 'success' },
  2: { label: '已拒绝', type: 'danger' }
}
