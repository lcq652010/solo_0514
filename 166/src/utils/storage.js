import { mockBooks, mockOrders, mockRecycleRecords } from './mockData'

const BOOKS_KEY = 'used_books'
const ORDERS_KEY = 'orders'
const RECYCLE_RECORDS_KEY = 'recycle_records'

function initData(key, data) {
  if (!localStorage.getItem(key)) {
    localStorage.setItem(key, JSON.stringify(data))
  }
}

export function initStorage() {
  initData(BOOKS_KEY, mockBooks)
  initData(ORDERS_KEY, mockOrders)
  initData(RECYCLE_RECORDS_KEY, mockRecycleRecords)
}

export function getBooks() {
  const data = localStorage.getItem(BOOKS_KEY)
  return data ? JSON.parse(data) : []
}

export function checkIsbnExists(isbn, excludeId = null) {
  const books = getBooks()
  return books.some(b => b.isbn === isbn && b.id !== excludeId)
}

export function saveBook(book) {
  const books = getBooks()
  if (book.id) {
    const index = books.findIndex(b => b.id === book.id)
    if (index !== -1) {
      books[index] = book
    }
  } else {
    book.id = books.length > 0 ? Math.max(...books.map(b => b.id)) + 1 : 1
    book.stock = book.stock || 1
    book.createTime = new Date().toLocaleString('zh-CN', { 
      year: 'numeric', 
      month: '2-digit', 
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    }).replace(/\//g, '-')
    books.push(book)
  }
  localStorage.setItem(BOOKS_KEY, JSON.stringify(books))
  return book
}

export function updateBookStatus(id, status) {
  const books = getBooks()
  const book = books.find(b => b.id === id)
  if (book) {
    book.status = status
    localStorage.setItem(BOOKS_KEY, JSON.stringify(books))
  }
  return book
}

export function deleteBook(id) {
  const books = getBooks()
  const index = books.findIndex(b => b.id === id)
  if (index !== -1) {
    books.splice(index, 1)
    localStorage.setItem(BOOKS_KEY, JSON.stringify(books))
    return true
  }
  return false
}

export function getOrders() {
  const data = localStorage.getItem(ORDERS_KEY)
  return data ? JSON.parse(data) : []
}

export function decreaseBookStock(bookId, quantity = 1) {
  const books = getBooks()
  const book = books.find(b => b.id === bookId)
  if (book && book.stock >= quantity) {
    book.stock -= quantity
    if (book.stock === 0) {
      book.status = 'sold'
    }
    localStorage.setItem(BOOKS_KEY, JSON.stringify(books))
    return true
  }
  return false
}

export function saveOrder(order) {
  if (order.bookId) {
    const success = decreaseBookStock(order.bookId, order.quantity || 1)
    if (!success) {
      throw new Error('库存不足')
    }
  }
  const orders = getOrders()
  order.id = orders.length > 0 ? Math.max(...orders.map(o => o.id)) + 1 : 1
  order.orderNo = 'ORD' + Date.now()
  order.createTime = new Date().toLocaleString('zh-CN', { 
    year: 'numeric', 
    month: '2-digit', 
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  }).replace(/\//g, '-')
  order.status = 'pending'
  orders.push(order)
  localStorage.setItem(ORDERS_KEY, JSON.stringify(orders))
  return order
}

export function updateOrderStatus(id, status) {
  const orders = getOrders()
  const order = orders.find(o => o.id === id)
  if (order) {
    order.status = status
    if (status === 'shipped') {
      order.shipTime = new Date().toLocaleString('zh-CN', { 
        year: 'numeric', 
        month: '2-digit', 
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      }).replace(/\//g, '-')
    } else if (status === 'completed') {
      order.completeTime = new Date().toLocaleString('zh-CN', { 
        year: 'numeric', 
        month: '2-digit', 
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      }).replace(/\//g, '-')
    }
    localStorage.setItem(ORDERS_KEY, JSON.stringify(orders))
  }
  return order
}

export function getRecycleRecords() {
  const data = localStorage.getItem(RECYCLE_RECORDS_KEY)
  return data ? JSON.parse(data) : []
}

export function saveRecycleRecord(record) {
  const records = getRecycleRecords()
  record.id = records.length > 0 ? Math.max(...records.map(r => r.id)) + 1 : 1
  record.createTime = new Date().toLocaleString('zh-CN', { 
    year: 'numeric', 
    month: '2-digit', 
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  }).replace(/\//g, '-')
  record.status = 'pending'
  records.push(record)
  localStorage.setItem(RECYCLE_RECORDS_KEY, JSON.stringify(records))
  return record
}

export function updateRecycleRecordStatus(id, status, rejectReason = '') {
  const records = getRecycleRecords()
  const record = records.find(r => r.id === id)
  if (record) {
    record.status = status
    if (status === 'completed') {
      record.completeTime = new Date().toLocaleString('zh-CN', { 
        year: 'numeric', 
        month: '2-digit', 
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      }).replace(/\//g, '-')
    } else if (status === 'rejected') {
      record.rejectReason = rejectReason
    }
    localStorage.setItem(RECYCLE_RECORDS_KEY, JSON.stringify(records))
  }
  return record
}
