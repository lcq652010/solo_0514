Vue.use(ELEMENT);
Vue.prototype.$moment = moment;

Vue.config.productionTip = false;

new Vue({
  router: window.router,
  store: window.store,
  render: h => h(window.App)
}).$mount('#app');
