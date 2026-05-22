import { orders as mockOrders } from '@/data/mock.js'

class OrderStore {
  constructor() {
    this.orders = [...mockOrders]
    this.subscribers = []
  }

  subscribe(callback) {
    this.subscribers.push(callback)
    return () => {
      const index = this.subscribers.indexOf(callback)
      if (index > -1) {
        this.subscribers.splice(index, 1)
      }
    }
  }

  notify() {
    this.subscribers.forEach(callback => callback(this.orders))
  }

  getOrders() {
    return [...this.orders]
  }

  addOrder(order) {
    this.orders.unshift(order)
    this.notify()
    return order
  }

  updateOrderStatus(orderId, status) {
    const order = this.orders.find(o => o.id === orderId)
    if (order) {
      order.status = status
      this.notify()
      return true
    }
    return false
  }

  getOrderById(orderId) {
    return this.orders.find(o => o.id === orderId)
  }

  filterOrders(filters) {
    let result = [...this.orders]
    
    if (filters.movieTitle && filters.movieTitle.trim()) {
      result = result.filter(o => 
        o.movieTitle.includes(filters.movieTitle.trim())
      )
    }
    
    if (filters.sessionTime && filters.sessionTime.trim()) {
      result = result.filter(o => 
        o.sessionTime.includes(filters.sessionTime.trim())
      )
    }
    
    if (filters.status && filters.status !== 'all') {
      result = result.filter(o => o.status === filters.status)
    }
    
    return result
  }

  getUniqueMovieTitles() {
    const titles = new Set()
    this.orders.forEach(o => titles.add(o.movieTitle))
    return Array.from(titles)
  }
}

export default new OrderStore()
