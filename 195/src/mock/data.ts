export interface Device {
  id: number
  deviceCode: string
  community: string
  location: string
  status: 'running' | 'fault' | 'offline' | 'maintenance'
  statusText: string
  lastOnline: string
  installDate: string
}

export interface WorkOrder {
  id: number
  workOrderNo: string
  deviceCode: string
  community: string
  faultDescription: string
  reportTime: string
  status: 'pending' | 'processing' | 'completed'
  statusText: string
}

const communities = [
  '阳光花园社区', '绿城社区', '锦绣社区', '和谐社区', '幸福社区',
  '新华社区', '和平社区', '胜利社区', '友谊社区', '光明社区',
  '新兴社区', '永安社区', '康乐社区', '福安社区', '德馨社区'
]

const locations = [
  '社区服务中心大厅', '小区东门岗亭', '小区西门岗亭', '物业管理处',
  '老年活动中心', '文化活动站', '健身广场旁', '社区卫生站',
  '1号楼大堂', '2号楼大堂', '3号楼大堂', '5号楼大堂',
  '地下车库入口', '社区公园入口', '学校门口'
]

const statuses: Array<{ value: Device['status']; text: string }> = [
  { value: 'running', text: '运行中' },
  { value: 'fault', text: '故障' },
  { value: 'offline', text: '离线' },
  { value: 'maintenance', text: '维护中' }
]

function randomDate(start: Date, end: Date): string {
  const date = new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()))
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}

function generateDeviceCode(index: number): string {
  const prefix = 'SQT'
  const year = 2024
  const seq = String(index).padStart(5, '0')
  return `${prefix}${year}${seq}`
}

export const mockDevices: Device[] = Array.from({ length: 86 }, (_, i) => {
  const statusObj = statuses[Math.floor(Math.random() * statuses.length)]
  return {
    id: i + 1,
    deviceCode: generateDeviceCode(i + 1),
    community: communities[Math.floor(Math.random() * communities.length)],
    location: locations[Math.floor(Math.random() * locations.length)],
    status: statusObj.value,
    statusText: statusObj.text,
    lastOnline: randomDate(new Date('2026-05-01'), new Date('2026-05-18')),
    installDate: randomDate(new Date('2023-01-01'), new Date('2025-12-31')).split(' ')[0]
  }
})

export const mockWorkOrders: WorkOrder[] = [
  {
    id: 1,
    workOrderNo: 'WO202605180930250001',
    deviceCode: 'SQT202400003',
    community: '阳光花园社区',
    faultDescription: '触摸屏无响应，无法正常操作',
    reportTime: '2026-05-18 09:30:25',
    status: 'processing',
    statusText: '处理中'
  },
  {
    id: 2,
    workOrderNo: 'WO202605171420150002',
    deviceCode: 'SQT202400015',
    community: '绿城社区',
    faultDescription: '打印机卡纸，无法打印回执',
    reportTime: '2026-05-17 14:20:15',
    status: 'completed',
    statusText: '已完成'
  },
  {
    id: 3,
    workOrderNo: 'WO202605171015330003',
    deviceCode: 'SQT202400028',
    community: '锦绣社区',
    faultDescription: '身份证读卡器识别失败',
    reportTime: '2026-05-17 10:15:33',
    status: 'pending',
    statusText: '待处理'
  }
]
