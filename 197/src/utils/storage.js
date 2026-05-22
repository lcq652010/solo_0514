import { mockOrders } from '@/mock/data.js'

const ORDERS_KEY = 'xuanzhi_orders'
const ADMIN_KEY = 'xuanzhi_admin'

export function initOrders() {
  const orders = localStorage.getItem(ORDERS_KEY)
  if (!orders) {
    localStorage.setItem(ORDERS_KEY, JSON.stringify(mockOrders))
  }
}

export function getOrders() {
  initOrders()
  const data = localStorage.getItem(ORDERS_KEY)
  return data ? JSON.parse(data) : []
}

export function saveOrders(orders) {
  localStorage.setItem(ORDERS_KEY, JSON.stringify(orders))
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

export function getOrderById(orderId) {
  const orders = getOrders()
  return orders.find(o => o.id === orderId)
}

export function generateOrderId() {
  const date = new Date()
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const random = String(Math.floor(Math.random() * 10000)).padStart(4, '0')
  return `XZ${year}${month}${day}${random}`
}

export function formatDateTime(date) {
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hours = String(d.getHours()).padStart(2, '0')
  const minutes = String(d.getMinutes()).padStart(2, '0')
  const seconds = String(d.getSeconds()).padStart(2, '0')
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}

export function createEmptySteps() {
  return [
    { name: '选纸', completed: false, time: null },
    { name: '裁切', completed: false, time: null },
    { name: '水印', completed: false, time: null },
    { name: '描金', completed: false, time: null },
    { name: '压平', completed: false, time: null },
    { name: '包装', completed: false, time: null },
    { name: '质检', completed: false, time: null },
    { name: '完工', completed: false, time: null }
  ]
}

export function login(username, password) {
  if (username === 'admin' && password === 'admin123') {
    localStorage.setItem(ADMIN_KEY, JSON.stringify({ username, loginTime: Date.now() }))
    return true
  }
  return false
}

export function logout() {
  localStorage.removeItem(ADMIN_KEY)
}

export function isLoggedIn() {
  const admin = localStorage.getItem(ADMIN_KEY)
  return !!admin
}

export function getCurrentAdmin() {
  const data = localStorage.getItem(ADMIN_KEY)
  return data ? JSON.parse(data) : null
}
