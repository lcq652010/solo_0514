import Vue from 'vue'
import Vuex from 'vuex'
import { dishes, orders, riders } from '@/mock/data'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    dishes: [...dishes],
    orders: [...orders],
    riders: [...riders],
    cart: []
  },
  mutations: {
    DEDUCT_STOCK(state, dishes) {
      dishes.forEach(item => {
        const dish = state.dishes.find(d => d.id === item.id)
        if (dish) {
          dish.stock = Math.max(0, dish.stock - item.quantity)
        }
      })
    },
    RESTORE_STOCK(state, dishes) {
      dishes.forEach(item => {
        const dish = state.dishes.find(d => d.id === item.id)
        if (dish) {
          dish.stock += item.quantity
        }
      })
    },
    ADD_TO_CART(state, dish) {
      const dishInStock = state.dishes.find(d => d.id === dish.id)
      if (!dishInStock || dishInStock.stock <= 0) {
        return
      }
      const existing = state.cart.find(item => item.id === dish.id)
      const currentQuantity = existing ? existing.quantity : 0
      if (currentQuantity >= dishInStock.stock) {
        return
      }
      if (existing) {
        existing.quantity++
      } else {
        state.cart.push({ ...dish, quantity: 1 })
      }
    },
    REMOVE_FROM_CART(state, dishId) {
      const index = state.cart.findIndex(item => item.id === dishId)
      if (index > -1) {
        if (state.cart[index].quantity > 1) {
          state.cart[index].quantity--
        } else {
          state.cart.splice(index, 1)
        }
      }
    },
    CLEAR_CART(state) {
      state.cart = []
    },
    UPDATE_CART_ITEM_QUANTITY(state, { dishId, quantity }) {
      const item = state.cart.find(item => item.id === dishId)
      if (item) {
        if (quantity <= 0) {
          const index = state.cart.findIndex(i => i.id === dishId)
          state.cart.splice(index, 1)
        } else {
          item.quantity = quantity
        }
      }
    },
    PLACE_ORDER(state, order) {
      state.orders.unshift(order)
    },
    UPDATE_ORDER_STATUS(state, { orderId, status, extra = {} }) {
      const order = state.orders.find(o => o.id === orderId)
      if (order) {
        order.status = status
        Object.assign(order, extra)
      }
    },
    ASSIGN_RIDER(state, { orderId, riderId, riderName }) {
      const order = state.orders.find(o => o.id === orderId)
      if (order) {
        order.riderId = riderId
        order.riderName = riderName
        order.status = 'delivering'
      }
      const rider = state.riders.find(r => r.id === riderId)
      if (rider) {
        rider.status = '配送中'
        rider.orders++
      }
    },
    COMPLETE_DELIVERY(state, orderId) {
      const order = state.orders.find(o => o.id === orderId)
      if (order) {
        order.status = 'delivered'
        order.finishTime = new Date().toLocaleString('zh-CN', { hour12: false }).replace(/\//g, '-')
        const rider = state.riders.find(r => r.id === order.riderId)
        if (rider) {
          rider.orders--
          if (rider.orders <= 0) {
            rider.status = '空闲'
          }
        }
      }
    },
    CANCEL_ORDER(state, { orderId, reason }) {
      const order = state.orders.find(o => o.id === orderId)
      if (order && order.status !== 'cancelled' && order.status !== 'delivered') {
        order.status = 'cancelled'
        order.cancelTime = new Date().toLocaleString('zh-CN', { hour12: false }).replace(/\//g, '-')
        order.cancelReason = reason
        if (order.dishes) {
          order.dishes.forEach(item => {
            const dish = state.dishes.find(d => d.id === item.id)
            if (dish) {
              dish.stock += item.quantity
            }
          })
        }
      }
    }
  },
  actions: {
    addToCart({ commit }, dish) {
      commit('ADD_TO_CART', dish)
    },
    removeFromCart({ commit }, dishId) {
      commit('REMOVE_FROM_CART', dishId)
    },
    clearCart({ commit }) {
      commit('CLEAR_CART')
    },
    updateCartItemQuantity({ commit }, payload) {
      commit('UPDATE_CART_ITEM_QUANTITY', payload)
    },
    placeOrder({ commit, state }, orderData) {
      const stockValidation = []
      orderData.dishes.forEach(item => {
        const dish = state.dishes.find(d => d.id === item.id)
        if (!dish || dish.stock < item.quantity) {
          stockValidation.push(item.name)
        }
      })
      if (stockValidation.length > 0) {
        return { success: false, message: `以下菜品库存不足：${stockValidation.join('、')}` }
      }
      const merchantMap = {
        1: { id: 1, name: '川味轩餐厅' },
        2: { id: 2, name: '老北京面馆' },
        3: { id: 3, name: '港式茶餐厅' },
        4: { id: 4, name: '甜品小站' }
      }
      const districtMap = {
        1: { id: 1, name: '朝阳区' },
        2: { id: 2, name: '海淀区' },
        3: { id: 3, name: '西城区' },
        4: { id: 4, name: '东城区' },
        5: { id: 5, name: '丰台区' }
      }
      const randomMerchant = merchantMap[Math.floor(Math.random() * 4) + 1]
      const randomDistrict = districtMap[Math.floor(Math.random() * 5) + 1]
      const order = {
        id: 'DD' + Date.now(),
        ...orderData,
        status: 'pending',
        paymentStatus: 'paid',
        merchantId: randomMerchant.id,
        merchantName: randomMerchant.name,
        districtId: randomDistrict.id,
        districtName: randomDistrict.name,
        createTime: new Date().toLocaleString('zh-CN', { hour12: false }).replace(/\//g, '-')
      }
      commit('DEDUCT_STOCK', orderData.dishes)
      commit('PLACE_ORDER', order)
      commit('CLEAR_CART')
      return { success: true, order }
    },
    updateOrderStatus({ commit }, payload) {
      commit('UPDATE_ORDER_STATUS', payload)
    },
    assignRider({ commit, state }, payload) {
      const { orderId, riderId, riderName } = payload
      const rider = state.riders.find(r => r.id === riderId)
      if (!rider) {
        return { success: false, message: '骑手不存在' }
      }
      if (rider.status === '配送中') {
        return { success: false, message: `骑手 ${rider.name} 当前正在配送中，无法同时派单` }
      }
      const activeOrders = state.orders.filter(o => o.riderId === riderId && o.status === 'delivering')
      if (activeOrders.length > 0) {
        return { success: false, message: `骑手 ${rider.name} 已有配送中的订单，同一时段不能重复派单` }
      }
      commit('ASSIGN_RIDER', { orderId, riderId, riderName })
      return { success: true }
    },
    completeDelivery({ commit }, orderId) {
      commit('COMPLETE_DELIVERY', orderId)
    },
    cancelOrder({ commit }, payload) {
      commit('CANCEL_ORDER', payload)
    }
  },
  getters: {
    cartTotal: state => {
      return state.cart.reduce((sum, item) => sum + item.price * item.quantity, 0)
    },
    cartCount: state => {
      return state.cart.reduce((sum, item) => sum + item.quantity, 0)
    },
    getDishesByCategory: state => categoryId => {
      if (categoryId === 1) return state.dishes
      return state.dishes.filter(d => d.categoryId === categoryId)
    },
    getOrderById: state => orderId => {
      return state.orders.find(o => o.id === orderId)
    },
    getAvailableRiders: state => {
      return state.riders.filter(r => r.status === '空闲')
    },
    getPendingOrders: state => {
      return state.orders.filter(o => o.status === 'pending' || o.status === 'preparing')
    }
  }
})

export default store
