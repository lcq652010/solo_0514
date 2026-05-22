import Vue from 'vue'
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App.vue'
import routes from './router'

Vue.use(VueRouter)
Vue.use(ElementUI)

const router = new VueRouter({
  mode: 'hash',
  routes
})

Vue.config.productionTip = false

function initMockData() {
  const orders = localStorage.getItem('jadeOrders')
  if (!orders || orders === '[]') {
    const mockOrders = [
      {
        id: 'ORD20240001',
        customerName: '张三',
        phone: '13800138001',
        address: '北京市朝阳区建国路88号',
        jadeType: 'hetian',
        outerDiameter: 45,
        thickness: 10,
        pattern: 'yunwen',
        ropeStyle: 'red',
        remark: '请尽量选用优质玉料',
        status: 3,
        createTime: '2024/5/10 10:30:25'
      },
      {
        id: 'ORD20240002',
        customerName: '李四',
        phone: '13900139002',
        address: '上海市浦东新区陆家嘴金融中心',
        jadeType: 'feicui',
        outerDiameter: 50,
        thickness: 12,
        pattern: 'longwen',
        ropeStyle: 'brown',
        remark: '雕刻要精细',
        status: 6,
        createTime: '2024/5/12 14:20:15'
      },
      {
        id: 'ORD20240003',
        customerName: '王五',
        phone: '13700137003',
        address: '广州市天河区珠江新城',
        jadeType: 'nanhong',
        outerDiameter: 38,
        thickness: 8,
        pattern: 'plain',
        ropeStyle: 'black',
        remark: '',
        status: 0,
        createTime: '2024/5/15 09:15:30'
      }
    ]
    localStorage.setItem('jadeOrders', JSON.stringify(mockOrders))
  }
}

initMockData()

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
