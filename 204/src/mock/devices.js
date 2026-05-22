const branches = [
  '总馆',
  '东区分馆',
  '西区分馆',
  '南区分馆',
  '北区分馆',
  '高新区分馆',
  '科技园分馆',
  '文化中心分馆'
]

const floors = ['1楼', '2楼', '3楼', '4楼', '5楼', 'B1层']

const statuses = ['online', 'offline', 'fault', 'maintaining']

const moduleStatuses = ['normal', 'warning', 'error']

function generateDevice(id) {
  const branchIndex = Math.floor(Math.random() * branches.length)
  const branch = branches[branchIndex]
  const floor = floors[Math.floor(Math.random() * floors.length)]
  const status = statuses[Math.floor(Math.random() * statuses.length)]
  
  const now = new Date()
  const lastHeartbeat = new Date(now.getTime() - Math.random() * 3600000 * 24)
  const createTime = new Date(now.getTime() - Math.random() * 3600000 * 24 * 365)
  
  const idRecognition = moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)]
  const ebookDownload = moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)]
  const printOutput = moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)]
  const networkComm = moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)]
  
  return {
    id,
    deviceCode: `TERM-${String(id).padStart(4, '0')}`,
    branchName: branch,
    floor,
    status,
    lastHeartbeat: formatDate(lastHeartbeat),
    createTime: formatDate(createTime),
    modules: {
      idRecognition,
      ebookDownload,
      printOutput,
      networkComm
    }
  }
}

function formatDate(date) {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}

const devices = []
for (let i = 1; i <= 56; i++) {
  devices.push(generateDevice(i))
}

export default devices
