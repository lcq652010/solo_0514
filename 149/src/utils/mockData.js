export function initMockData() {
  const existingOrders = localStorage.getItem('umbrellaOrders')
  if (existingOrders) return

  const mockOrders = [
    {
      id: 1715000000001,
      customerName: '张三',
      phone: '13800138001',
      frameMaterial: '紫竹',
      diameter: 84,
      pattern: '山水',
      handleStyle: '直柄',
      tasselColor: '#ff0000',
      remark: '请在伞面题字',
      status: 5,
      createTime: '2024/5/6 10:30:00'
    },
    {
      id: 1715000000002,
      customerName: '李四',
      phone: '13800138002',
      frameMaterial: '毛竹',
      diameter: 70,
      pattern: '花鸟',
      handleStyle: '弯柄',
      tasselColor: '#ffd700',
      remark: '',
      status: 2,
      createTime: '2024/5/6 14:20:00'
    },
    {
      id: 1715000000003,
      customerName: '王五',
      phone: '13800138003',
      frameMaterial: '罗汉竹',
      diameter: 100,
      pattern: '龙凤',
      handleStyle: '龙头柄',
      tasselColor: '#00ffff',
      remark: '需要精美包装',
      status: 7,
      createTime: '2024/5/5 09:15:00'
    },
    {
      id: 1715000000004,
      customerName: '赵六',
      phone: '13800138004',
      frameMaterial: '湘妃竹',
      diameter: 84,
      pattern: '梅兰竹菊',
      handleStyle: '如意柄',
      tasselColor: '#008000',
      remark: '',
      status: 0,
      createTime: '2024/5/6 16:45:00'
    }
  ]

  localStorage.setItem('umbrellaOrders', JSON.stringify(mockOrders))
}
