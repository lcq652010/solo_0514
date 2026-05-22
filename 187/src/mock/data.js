export const products = [
  { id: 1, name: '32.5普通硅酸盐水泥', category: '水泥', unit: '吨', price: 450, stock: 150, minStock: 50, maxOrder: 100, spec: 'P.O 32.5', brand: '海螺' },
  { id: 2, name: '42.5普通硅酸盐水泥', category: '水泥', unit: '吨', price: 520, stock: 85, minStock: 50, maxOrder: 80, spec: 'P.O 42.5', brand: '海螺' },
  { id: 3, name: '52.5普通硅酸盐水泥', category: '水泥', unit: '吨', price: 680, stock: 32, minStock: 30, maxOrder: 50, spec: 'P.O 52.5', brand: '海螺' },
  { id: 4, name: 'HRB400螺纹钢φ12', category: '钢材', unit: '吨', price: 4800, stock: 68, minStock: 40, maxOrder: 50, spec: 'φ12mm', brand: '宝钢' },
  { id: 5, name: 'HRB400螺纹钢φ16', category: '钢材', unit: '吨', price: 4650, stock: 45, minStock: 40, maxOrder: 40, spec: 'φ16mm', brand: '宝钢' },
  { id: 6, name: 'HRB400螺纹钢φ20', category: '钢材', unit: '吨', price: 4500, stock: 25, minStock: 30, maxOrder: 30, spec: 'φ20mm', brand: '宝钢' },
  { id: 7, name: '中砂（河沙）', category: '砂石', unit: '立方米', price: 120, stock: 280, minStock: 100, maxOrder: 200, spec: '中粗', brand: '本地' },
  { id: 8, name: '碎石（5-20mm）', category: '砂石', unit: '立方米', price: 95, stock: 18, minStock: 80, maxOrder: 100, spec: '5-20mm', brand: '本地' },
  { id: 9, name: '红砖（标准）', category: '砖瓦', unit: '块', price: 0.55, stock: 50000, minStock: 20000, maxOrder: 50000, spec: '240×115×53', brand: '本地' },
  { id: 10, name: '加气混凝土砌块', category: '砖瓦', unit: '立方米', price: 280, stock: 450, minStock: 100, maxOrder: 300, spec: '600×300×200', brand: '本地' }
]

export const orders = [
  {
    id: 'ORD20240517001',
    customerName: '张三',
    customerPhone: '13800138001',
    address: '北京市朝阳区建设工地A区',
    items: [
      { productId: 1, productName: '32.5普通硅酸盐水泥', quantity: 20, price: 450, unit: '吨' },
      { productId: 7, productName: '中砂（河沙）', quantity: 50, price: 120, unit: '立方米' }
    ],
    totalAmount: 15000,
    status: 'pending',
    isShipped: false,
    createTime: '2024-05-17 09:30:00',
    remark: '请上午送货'
  },
  {
    id: 'ORD20240517002',
    customerName: '李四',
    customerPhone: '13800138002',
    address: '北京市海淀区工地B区',
    items: [
      { productId: 4, productName: 'HRB400螺纹钢φ12', quantity: 5, price: 4800, unit: '吨' },
      { productId: 5, productName: 'HRB400螺纹钢φ16', quantity: 8, price: 4650, unit: '吨' }
    ],
    totalAmount: 61200,
    status: 'shipped',
    isShipped: true,
    createTime: '2024-05-16 14:20:00',
    shipTime: '2024-05-17 08:00:00',
    logistics: '顺丰物流',
    trackingNo: 'SF1234567890',
    remark: ''
  },
  {
    id: 'ORD20240517003',
    customerName: '王五',
    customerPhone: '13800138003',
    address: '北京市丰台区工地C区',
    items: [
      { productId: 9, productName: '红砖（标准）', quantity: 10000, price: 0.55, unit: '块' }
    ],
    totalAmount: 5500,
    status: 'completed',
    isShipped: true,
    createTime: '2024-05-15 10:00:00',
    shipTime: '2024-05-15 15:00:00',
    receiveTime: '2024-05-16 09:00:00',
    logistics: '本地配送',
    trackingNo: 'BD20240515001',
    remark: '已签收'
  },
  {
    id: 'ORD20240517004',
    customerName: '赵六',
    customerPhone: '13800138004',
    address: '北京市通州区工地D区',
    items: [
      { productId: 2, productName: '42.5普通硅酸盐水泥', quantity: 30, price: 520, unit: '吨' },
      { productId: 8, productName: '碎石（5-20mm）', quantity: 60, price: 95, unit: '立方米' }
    ],
    totalAmount: 21300,
    status: 'processing',
    isShipped: false,
    createTime: '2024-05-17 11:00:00',
    remark: '紧急订单，请优先处理'
  }
]
