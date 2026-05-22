const STORAGE_KEY = 'kesi_fan_orders'

export function getOrders() {
  const data = localStorage.getItem(STORAGE_KEY)
  return data ? JSON.parse(data) : []
}

export function saveOrders(orders) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(orders))
}

export function addOrder(order) {
  const orders = getOrders()
  orders.unshift(order)
  saveOrders(orders)
  return order
}

export function updateOrder(orderId, updates) {
  const orders = getOrders()
  const index = orders.findIndex(o => o.id === orderId)
  if (index !== -1) {
    orders[index] = { ...orders[index], ...updates }
    saveOrders(orders)
    return orders[index]
  }
  return null
}

export function generateOrderNo() {
  const date = new Date()
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const random = String(Math.floor(Math.random() * 1000)).padStart(3, '0')
  return `KS${year}${month}${day}${random}`
}

export function formatTime(timestamp) {
  if (!timestamp) return '-'
  const date = new Date(timestamp)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

export function getStatusText(status) {
  const map = {
    pending: '待生产',
    processing: '生产中',
    completed: '已完工'
  }
  return map[status] || status
}

export function getStatusType(status) {
  const map = {
    pending: 'warning',
    processing: 'primary',
    completed: 'success'
  }
  return map[status] || 'info'
}
