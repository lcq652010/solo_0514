export function generateWorkOrderNo() {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  const timestamp = String(now.getTime()).slice(-6)
  const random = String(Math.floor(Math.random() * 1000)).padStart(3, '0')
  return `WO${year}${month}${day}${timestamp}${random}`
}

export function formatDate(date) {
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hours = String(d.getHours()).padStart(2, '0')
  const minutes = String(d.getMinutes()).padStart(2, '0')
  const seconds = String(d.getSeconds()).padStart(2, '0')
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}

export function getStatusText(status) {
  const statusMap = {
    online: '在线',
    offline: '离线',
    fault: '故障'
  }
  return statusMap[status] || status
}

export function getStatusType(status) {
  const typeMap = {
    online: 'success',
    offline: 'warning',
    fault: 'danger'
  }
  return typeMap[status] || 'info'
}

export function getWorkOrderStatusText(status) {
  const statusMap = {
    pending: '待处理',
    processing: '处理中',
    resolved: '已解决',
    closed: '已关闭'
  }
  return statusMap[status] || status
}

export function getWorkOrderStatusType(status) {
  const typeMap = {
    pending: 'warning',
    processing: 'primary',
    resolved: 'success',
    closed: 'info'
  }
  return typeMap[status] || 'info'
}

export function getModuleStatusText(status) {
  const statusMap = {
    normal: '正常',
    warning: '异常',
    error: '故障'
  }
  return statusMap[status] || status
}

export function getModuleStatusType(status) {
  const typeMap = {
    normal: 'success',
    warning: 'warning',
    error: 'danger'
  }
  return typeMap[status] || 'info'
}
