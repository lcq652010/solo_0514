const organizations = [
  '北京市人才服务中心',
  '上海市人才服务中心',
  '广州市人才服务中心',
  '深圳市人才服务中心',
  '杭州市人才服务中心',
  '南京市人才服务中心',
  '成都市人才服务中心',
  '武汉市人才服务中心',
  '西安市人才服务中心',
  '重庆市人才服务中心'
]

const locations = [
  '一楼大厅',
  '二楼办事区',
  '自助服务区A区',
  '自助服务区B区',
  '政务服务中心',
  '人才市场大厅',
  '行政服务中心',
  '公共服务大厅'
]

const statuses = ['online', 'online', 'online', 'online', 'online', 'offline', 'fault']

function generateDevice(index) {
  const orgIndex = Math.floor(Math.random() * organizations.length)
  const locIndex = Math.floor(Math.random() * locations.length)
  const statusIndex = Math.floor(Math.random() * statuses.length)
  const org = organizations[orgIndex]
  const location = locations[locIndex]
  const status = statuses[statusIndex]
  
  const now = new Date()
  const lastOnline = new Date(now.getTime() - Math.random() * 7 * 24 * 60 * 60 * 1000)
  const createTime = new Date(now.getTime() - Math.random() * 365 * 24 * 60 * 60 * 1000)
  
  const moduleStatuses = ['normal', 'normal', 'normal', 'warning', 'error']
  const identityVerifyStatus = status === 'online' 
    ? moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)]
    : 'error'
  const printStatus = status === 'online'
    ? moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)]
    : 'error'
  const networkQueryStatus = status === 'online'
    ? moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)]
    : 'error'
  
  return {
    id: `DEV${String(index).padStart(6, '0')}`,
    deviceNo: `TS${orgIndex + 1}${String(index).padStart(4, '0')}`,
    organization: org,
    location: location,
    status: status,
    identityVerifyStatus: identityVerifyStatus,
    printStatus: printStatus,
    networkQueryStatus: networkQueryStatus,
    lastOnlineTime: lastOnline.toISOString(),
    createTime: createTime.toISOString()
  }
}

const devices = []
for (let i = 1; i <= 56; i++) {
  devices.push(generateDevice(i))
}

export default devices
