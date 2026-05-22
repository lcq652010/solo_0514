let vehicleId = 10
let orderId = 100

export const mockVehicles = [
  { id: 1, plateNumber: '京A12345', type: '4.2米厢式货车', capacity: '5吨', driver: '张三', phone: '13800138001', status: '空闲', currentLocation: '北京朝阳' },
  { id: 2, plateNumber: '京B67890', type: '6.8米厢式货车', capacity: '10吨', driver: '李四', phone: '13800138002', status: '在途', currentLocation: '天津西青' },
  { id: 3, plateNumber: '京C11111', type: '9.6米平板车', capacity: '15吨', driver: '王五', phone: '13800138003', status: '维修中', currentLocation: '北京通州' },
  { id: 4, plateNumber: '京D22222', type: '4.2米厢式货车', capacity: '5吨', driver: '赵六', phone: '13800138004', status: '空闲', currentLocation: '北京海淀' },
  { id: 5, plateNumber: '京E33333', type: '13米半挂车', capacity: '30吨', driver: '孙七', phone: '13800138005', status: '在途', currentLocation: '河北石家庄' },
  { id: 6, plateNumber: '京F44444', type: '6.8米厢式货车', capacity: '10吨', driver: '周八', phone: '13800138006', status: '空闲', currentLocation: '北京丰台' },
  { id: 7, plateNumber: '京G55555', type: '4.2米冷藏车', capacity: '5吨', driver: '吴九', phone: '13800138007', status: '在途', currentLocation: '山东济南' },
  { id: 8, plateNumber: '京H66666', type: '9.6米厢式货车', capacity: '18吨', driver: '郑十', phone: '13800138008', status: '空闲', currentLocation: '北京大兴' },
  { id: 9, plateNumber: '京I77777', type: '6.8米平板车', capacity: '10吨', driver: '陈一', phone: '13800138009', status: '维修中', currentLocation: '北京顺义' },
  { id: 10, plateNumber: '京J88888', type: '13米厢式货车', capacity: '30吨', driver: '刘二', phone: '13800138010', status: '在途', currentLocation: '河南郑州' }
]

export const routeList = [
  { id: 1, name: '北京-上海', distance: 1200, basePrice: 1500 },
  { id: 2, name: '北京-天津', distance: 120, basePrice: 300 },
  { id: 3, name: '北京-广州', distance: 2100, basePrice: 2500 },
  { id: 4, name: '北京-济南', distance: 400, basePrice: 600 },
  { id: 5, name: '北京-深圳', distance: 2200, basePrice: 2600 },
  { id: 6, name: '北京-郑州', distance: 700, basePrice: 900 },
  { id: 7, name: '北京-杭州', distance: 1300, basePrice: 1600 },
  { id: 8, name: '上海-北京', distance: 1200, basePrice: 1500 },
  { id: 9, name: '广州-北京', distance: 2100, basePrice: 2500 },
  { id: 10, name: '天津-北京', distance: 120, basePrice: 300 }
]

export const calculateFreight = (goodsWeight, goodsVolume, routeId) => {
  const route = routeList.find(r => r.id === routeId)
  if (!route) return 0
  
  const weightPrice = goodsWeight * 50
  const volumePrice = goodsVolume * 10
  const distancePrice = route.distance * 0.8
  
  return Math.round(route.basePrice + Math.max(weightPrice, volumePrice) + distancePrice)
}

export const mockOrders = [
  { id: 101, orderNo: 'WD20240101001', sender: '北京某电子公司', senderPhone: '010-12345678', senderAddress: '北京市朝阳区科技园A座', receiver: '上海某贸易公司', receiverPhone: '021-87654321', receiverAddress: '上海市浦东新区张江高科技园区B栋', goodsName: '电子元器件', goodsWeight: 3.5, goodsVolume: 8, requireTime: '2024-01-05', status: '已调度', vehicleId: 2, createTime: '2024-01-01 09:30:00', routeId: 1, routeName: '北京-上海', freight: 2875 },
  { id: 102, orderNo: 'WD20240101002', sender: '天津某食品厂', senderPhone: '022-11112222', senderAddress: '天津市西青区食品工业园', receiver: '北京某超市连锁', receiverPhone: '010-33334444', receiverAddress: '北京市海淀区超市配送中心', goodsName: '休闲食品', goodsWeight: 8, goodsVolume: 20, requireTime: '2024-01-04', status: '在途', vehicleId: 5, createTime: '2024-01-01 10:15:00', routeId: 10, routeName: '天津-北京', freight: 996 },
  { id: 103, orderNo: 'WD20240101003', sender: '广州某服装厂', senderPhone: '020-55556666', senderAddress: '广州市白云区服装工业园', receiver: '北京某服装批发市场', receiverPhone: '010-77778888', receiverAddress: '北京市丰台区服装批发市场', goodsName: '秋冬季服装', goodsWeight: 12, goodsVolume: 35, requireTime: '2024-01-06', status: '待调度', vehicleId: null, createTime: '2024-01-01 11:00:00', routeId: 9, routeName: '广州-北京', freight: 4280 },
  { id: 104, orderNo: 'WD20240101004', sender: '北京某医药公司', senderPhone: '010-99990000', senderAddress: '北京市亦庄经济开发区', receiver: '济南某医院', receiverPhone: '0531-12345678', receiverAddress: '山东省济南市历下区某医院', goodsName: '医用药品', goodsWeight: 2, goodsVolume: 5, requireTime: '2024-01-03', status: '在途', vehicleId: 7, createTime: '2024-01-01 14:20:00', routeId: 4, routeName: '北京-济南', freight: 1120 },
  { id: 105, orderNo: 'WD20240101005', sender: '深圳某科技公司', senderPhone: '0755-11223344', senderAddress: '深圳市南山区科技园', receiver: '北京某电商仓库', receiverPhone: '010-55667788', receiverAddress: '北京市通州区电商物流园', goodsName: '智能手机', goodsWeight: 25, goodsVolume: 60, requireTime: '2024-01-07', status: '待调度', vehicleId: null, createTime: '2024-01-01 15:45:00', routeId: 5, routeName: '北京-深圳', freight: 5210 },
  { id: 106, orderNo: 'WD20240101006', sender: '北京某家具厂', senderPhone: '010-22334455', senderAddress: '北京市昌平区家具产业园', receiver: '郑州某家具城', receiverPhone: '0371-99887766', receiverAddress: '河南省郑州市金水区家具城', goodsName: '办公家具', goodsWeight: 18, goodsVolume: 45, requireTime: '2024-01-08', status: '在途', vehicleId: 10, createTime: '2024-01-01 16:30:00', routeId: 6, routeName: '北京-郑州', freight: 2360 },
  { id: 107, orderNo: 'WD20240101007', sender: '上海某化工公司', senderPhone: '021-66778899', senderAddress: '上海市嘉定区化工园区', receiver: '北京某化工厂', receiverPhone: '010-11223344', receiverAddress: '北京市房山区化工区', goodsName: '化工原料', goodsWeight: 28, goodsVolume: 70, requireTime: '2024-01-09', status: '已完成', vehicleId: 2, createTime: '2023-12-28 08:00:00', routeId: 8, routeName: '上海-北京', freight: 3860 },
  { id: 108, orderNo: 'WD20240101008', sender: '杭州某茶叶公司', senderPhone: '0571-99887766', senderAddress: '杭州市西湖区茶叶产区', receiver: '北京某茶叶市场', receiverPhone: '010-55443322', receiverAddress: '北京市马连道茶叶市场', goodsName: '西湖龙井', goodsWeight: 1.5, goodsVolume: 4, requireTime: '2024-01-05', status: '已完成', vehicleId: 4, createTime: '2023-12-29 10:30:00', routeId: 7, routeName: '北京-杭州', freight: 2715 }
]

export const mockTracking = [
  {
    orderId: 102,
    orderNo: 'WD20240101002',
    currentLocation: '河北沧州',
    progress: 45,
    estimatedArrival: '2024-01-03 18:00',
    temperature: 25,
    humidity: 60,
    timeline: [
      { time: '2024-01-01 10:15', location: '天津西青', status: '货物已装车', description: '货物已从发货人仓库装车，准备出发' },
      { time: '2024-01-01 12:30', location: '天津静海', status: '运输中', description: '车辆正在正常行驶' },
      { time: '2024-01-01 18:00', location: '河北沧州', status: '运输中', description: '途经沧州服务区短暂休息' },
      { time: '2024-01-02 08:00', location: '河北沧州', status: '运输中', description: '继续前往目的地' }
    ]
  },
  {
    orderId: 104,
    orderNo: 'WD20240101004',
    currentLocation: '山东德州',
    progress: 60,
    estimatedArrival: '2024-01-02 20:00',
    temperature: 5,
    humidity: 45,
    timeline: [
      { time: '2024-01-01 14:20', location: '北京亦庄', status: '货物已装车', description: '冷链货物已装车，温控正常' },
      { time: '2024-01-01 16:00', location: '北京大兴', status: '运输中', description: '车辆正在正常行驶' },
      { time: '2024-01-01 20:00', location: '河北沧州', status: '运输中', description: '途经沧州' },
      { time: '2024-01-02 06:00', location: '山东德州', status: '运输中', description: '已进入山东省界' }
    ]
  },
  {
    orderId: 106,
    orderNo: 'WD20240101006',
    currentLocation: '河北邯郸',
    progress: 35,
    estimatedArrival: '2024-01-04 12:00',
    temperature: 18,
    humidity: 55,
    timeline: [
      { time: '2024-01-01 16:30', location: '北京昌平', status: '货物已装车', description: '家具已装车，固定完毕' },
      { time: '2024-01-01 19:00', location: '北京房山', status: '运输中', description: '车辆正在正常行驶' },
      { time: '2024-01-02 07:00', location: '河北保定', status: '运输中', description: '途经保定' },
      { time: '2024-01-02 11:00', location: '河北邯郸', status: '运输中', description: '继续向南行驶' }
    ]
  }
]

export const vehicleApi = {
  getList: () => {
    return Promise.resolve([...mockVehicles])
  },
  add: (data) => {
    vehicleId++
    const newVehicle = { ...data, id: vehicleId }
    mockVehicles.push(newVehicle)
    return Promise.resolve(newVehicle)
  },
  update: (id, data) => {
    const index = mockVehicles.findIndex(v => v.id === id)
    if (index > -1) {
      mockVehicles[index] = { ...mockVehicles[index], ...data }
      return Promise.resolve(mockVehicles[index])
    }
    return Promise.reject(new Error('车辆不存在'))
  },
  delete: (id) => {
    const index = mockVehicles.findIndex(v => v.id === id)
    if (index > -1) {
      mockVehicles.splice(index, 1)
      return Promise.resolve()
    }
    return Promise.reject(new Error('车辆不存在'))
  }
}

export const orderApi = {
  getList: () => {
    return Promise.resolve([...mockOrders])
  },
  add: (data) => {
    orderId++
    const now = new Date()
    const route = routeList.find(r => r.id === data.routeId)
    const freight = calculateFreight(data.goodsWeight, data.goodsVolume, data.routeId)
    const newOrder = {
      ...data,
      id: orderId,
      orderNo: `WD${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}${String(orderId).padStart(3, '0')}`,
      status: '待调度',
      vehicleId: null,
      createTime: now.toLocaleString(),
      routeName: route ? route.name : '',
      freight: freight
    }
    mockOrders.push(newOrder)
    return Promise.resolve(newOrder)
  },
  dispatch: (orderId, vehicleId) => {
    const index = mockOrders.findIndex(o => o.id === orderId)
    if (index > -1) {
      mockOrders[index].vehicleId = vehicleId
      mockOrders[index].status = '已调度'
      return Promise.resolve(mockOrders[index])
    }
    return Promise.reject(new Error('运单不存在'))
  },
  updateStatus: (id, status) => {
    const index = mockOrders.findIndex(o => o.id === id)
    if (index > -1) {
      mockOrders[index].status = status
      return Promise.resolve(mockOrders[index])
    }
    return Promise.reject(new Error('运单不存在'))
  }
}

export const trackingApi = {
  getList: () => {
    return Promise.resolve([...mockTracking])
  },
  getByOrderId: (orderId) => {
    const tracking = mockTracking.find(t => t.orderId === orderId)
    return Promise.resolve(tracking || null)
  }
}
