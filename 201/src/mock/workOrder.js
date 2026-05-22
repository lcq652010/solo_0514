const workOrders = [
  {
    id: 'WO001',
    workOrderNo: 'WO20260515123456001',
    deviceId: 'DEV000003',
    deviceNo: 'TS100003',
    organization: '北京市人才服务中心',
    problemDesc: '设备打印卡纸，纸张无法正常输出，需要更换打印头。',
    status: 'processing',
    createTime: '2026-05-15T09:30:00.000Z',
    updateTime: '2026-05-15T14:20:00.000Z'
  },
  {
    id: 'WO002',
    workOrderNo: 'WO20260514123456002',
    deviceId: 'DEV000007',
    deviceNo: 'TS200007',
    organization: '上海市人才服务中心',
    problemDesc: '触摸屏无响应，重启后仍然无法正常操作，可能是触摸屏硬件故障。',
    status: 'pending',
    createTime: '2026-05-14T16:45:00.000Z',
    updateTime: '2026-05-14T16:45:00.000Z'
  },
  {
    id: 'WO003',
    workOrderNo: 'WO20260513123456003',
    deviceId: 'DEV000012',
    deviceNo: 'TS300012',
    organization: '广州市人才服务中心',
    problemDesc: '身份证读卡器无法识别，所有证件都读不出来，已检查连接线正常。',
    status: 'resolved',
    createTime: '2026-05-13T11:20:00.000Z',
    updateTime: '2026-05-14T08:30:00.000Z'
  },
  {
    id: 'WO004',
    workOrderNo: 'WO20260512123456004',
    deviceId: 'DEV000018',
    deviceNo: 'TS400018',
    organization: '深圳市人才服务中心',
    problemDesc: '系统启动缓慢，经常卡在启动界面超过5分钟，需要多次重启才能正常使用。',
    status: 'closed',
    createTime: '2026-05-12T14:00:00.000Z',
    updateTime: '2026-05-13T10:15:00.000Z'
  },
  {
    id: 'WO005',
    workOrderNo: 'WO20260511123456005',
    deviceId: 'DEV000022',
    deviceNo: 'TS500022',
    organization: '杭州市人才服务中心',
    problemDesc: '打印机缺纸报警，添加纸张后仍然提示缺纸，可能是纸张传感器故障。',
    status: 'processing',
    createTime: '2026-05-11T10:30:00.000Z',
    updateTime: '2026-05-11T15:45:00.000Z'
  }
]

export default workOrders
