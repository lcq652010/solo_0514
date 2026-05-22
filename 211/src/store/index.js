window.store = new Vuex.Store({
  state: {
    packages: window.mockData.packages,
    photographers: window.mockData.photographers,
    orders: window.mockData.orders,
    customers: window.mockData.customers,
    schedule: window.mockData.schedule
  },
  mutations: {
    ADD_ORDER(state, order) {
      state.orders.unshift(order);
    },
    UPDATE_ORDER(state, payload) {
      const order = state.orders.find(o => o.id === payload.id);
      if (order) {
        order.status = payload.status;
      }
    },
    DELETE_ORDER(state, id) {
      state.orders = state.orders.filter(o => o.id !== id);
    },
    ADD_CUSTOMER(state, customer) {
      state.customers.unshift(customer);
    },
    UPDATE_CUSTOMER(state, customer) {
      const index = state.customers.findIndex(c => c.id === customer.id);
      if (index !== -1) {
        state.customers.splice(index, 1, customer);
      }
    },
    DELETE_CUSTOMER(state, id) {
      state.customers = state.customers.filter(c => c.id !== id);
    },
    ADD_SCHEDULE(state, schedule) {
      state.schedule.push(schedule);
    }
  },
  actions: {
    addOrder({ commit }, order) {
      commit('ADD_ORDER', order);
    },
    updateOrder({ commit }, payload) {
      commit('UPDATE_ORDER', payload);
    },
    deleteOrder({ commit }, id) {
      commit('DELETE_ORDER', id);
    },
    addCustomer({ commit }, customer) {
      commit('ADD_CUSTOMER', customer);
    },
    updateCustomer({ commit }, customer) {
      commit('UPDATE_CUSTOMER', customer);
    },
    deleteCustomer({ commit }, id) {
      commit('DELETE_CUSTOMER', id);
    },
    addSchedule({ commit }, schedule) {
      commit('ADD_SCHEDULE', schedule);
    }
  },
  getters: {
    getPackageById: state => id => state.packages.find(p => p.id === id),
    getPhotographerById: state => id => state.photographers.find(p => p.id === id),
    getCustomerOrders: state => customerId => state.orders.filter(o => o.customerId === customerId),
    getPhotographerSchedule: state => photographerId => state.schedule.filter(s => s.photographerId === photographerId)
  }
});
