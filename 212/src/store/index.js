import Vue from 'vue'
import Vuex from 'vuex'
import { mockOrders } from '../mock/orders'

Vue.use(Vuex)

const STORAGE_KEY = 'rattan_basket_orders'

export default new Vuex.Store({
  state: {
    orders: [],
    processes: [
      { id: 0, name: '选藤', icon: 'el-icon-box', description: '挑选优质藤条材料' },
      { id: 1, name: '软化', icon: 'el-icon-water-cup', description: '蒸汽软化藤条' },
      { id: 2, name: '打底', icon: 'el-icon-edit-outline', description: '编织果篮底部' },
      { id: 3, name: '编身', icon: 'el-icon-c-scale-to-original', description: '编织果篮主体' },
      { id: 4, name: '收口', icon: 'el-icon-circle-check', description: '收边处理' },
      { id: 5, name: '装提手', icon: 'el-icon-set-up', description: '安装提手' },
      { id: 6, name: '修整', icon: 'el-icon-brush', description: '打磨修整' },
      { id: 7, name: '完工', icon: 'el-icon-present', description: '成品检验' }
    ]
  },
  mutations: {
    SET_ORDERS(state, orders) {
      state.orders = orders
    },
    ADD_ORDER(state, order) {
      state.orders.unshift(order)
      this.commit('SAVE_TO_STORAGE')
    },
    UPDATE_PROCESS(state, { orderId, processIndex }) {
      const order = state.orders.find(o => o.id === orderId)
      if (order && processIndex >= 0 && processIndex <= 7) {
        order.currentProcess = processIndex
        order.processTimes[processIndex] = new Date().toISOString()
        if (processIndex === 7) {
          order.status = 'completed'
        } else {
          order.status = 'processing'
        }
        this.commit('SAVE_TO_STORAGE')
      }
    },
    SAVE_TO_STORAGE(state) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state.orders))
    },
    LOAD_FROM_STORAGE(state) {
      const stored = localStorage.getItem(STORAGE_KEY)
      if (stored) {
        state.orders = JSON.parse(stored)
      } else {
        state.orders = mockOrders
        this.commit('SAVE_TO_STORAGE')
      }
    }
  },
  actions: {
    createOrder({ commit }, orderData) {
      const order = {
        id: 'ORD' + Date.now() + Math.floor(Math.random() * 1000),
        ...orderData,
        currentProcess: 0,
        status: 'pending',
        createdAt: new Date().toISOString(),
        processTimes: [new Date().toISOString(), null, null, null, null, null, null, null]
      }
      commit('ADD_ORDER', order)
      return order
    },
    advanceProcess({ commit, state }, orderId) {
      const order = state.orders.find(o => o.id === orderId)
      if (order && order.currentProcess < 7) {
        commit('UPDATE_PROCESS', {
          orderId,
          processIndex: order.currentProcess + 1
        })
      }
    }
  },
  getters: {
    getOrderById: (state) => (id) => {
      return state.orders.find(o => o.id === id)
    },
    pendingOrders: (state) => {
      return state.orders.filter(o => o.status === 'pending')
    },
    processingOrders: (state) => {
      return state.orders.filter(o => o.status === 'processing')
    },
    completedOrders: (state) => {
      return state.orders.filter(o => o.status === 'completed')
    }
  }
})
