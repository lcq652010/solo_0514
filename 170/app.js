new Vue({
  el: '#app',
  data: {
    activeMenu: 'order',
    orders: [],
    latestOrderId: null,
    currentOperator: '',
    operatorList: ['张师傅', '李师傅', '王师傅', '赵师傅', '管理员']
  },
  methods: {
    handleMenuSelect(index) {
      this.activeMenu = index
    },
    handleSubmitOrder(order) {
      this.orders.unshift(order)
      this.latestOrderId = order.id
      this.activeMenu = 'admin'
      this.$message.success('订单提交成功，已自动跳转至订单管理页面！')
    },
    handleUpdateStatus(orderId, newStatus, historyItem) {
      const order = this.orders.find(o => o.id === orderId)
      if (order) {
        order.status = newStatus
        if (!order.statusHistory) {
          order.statusHistory = []
        }
        if (historyItem) {
          order.statusHistory.push(historyItem)
        }
      }
    }
  },
  watch: {
    activeMenu(newVal) {
      if (newVal === 'admin') {
        this.$nextTick(() => {
          if (this.$refs.adminPage) {
            this.$refs.adminPage.scrollToFirstRow()
          }
        })
      }
    }
  },
  mounted() {
    this.currentOperator = this.operatorList[0]
  }
})
