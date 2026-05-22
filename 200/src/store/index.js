import Vue from 'vue'
import Vuex from 'vuex'
import { mockOrders } from '../data/mockData'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    orders: mockOrders
  },
  mutations: {
    ADD_ORDER(state, order) {
      state.orders.unshift(order)
    },
    UPDATE_STATUS(state, { orderId, status }) {
      const order = state.orders.find(o => o.id === orderId)
      if (order) {
        order.status = status
        order.processSteps.push({
          status,
          time: new Date().toLocaleString('zh-CN')
        })
      }
    }
  },
  actions: {
    addOrder({ commit }, order) {
      const newOrder = {
        ...order,
        id: 'ORD' + Date.now(),
        status: 'pending',
        createdAt: new Date().toLocaleString('zh-CN'),
        processSteps: []
      }
      commit('ADD_ORDER', newOrder)
      return newOrder
    },
    updateStatus({ commit }, payload) {
      commit('UPDATE_STATUS', payload)
    }
  },
  getters: {
    getOrders: state => state.orders,
    getOrderById: state => id => state.orders.find(o => o.id === id)
  }
})
