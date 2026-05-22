<template>
  <div class="admin-container">
    <el-card class="admin-card" shadow="hover">
      <div slot="header" class="card-header">
        <span>传统漆雕墨盒定制 - 订单管理</span>
        <el-button style="float: right; padding: 3px 0" type="text" @click="goToOrder">返回下单页</el-button>
      </div>

      <el-table :data="orders" style="width: 100%" border v-loading="loading">
        <el-table-column prop="orderNo" label="订单号" width="150" align="center"></el-table-column>
        <el-table-column prop="customerName" label="客户姓名" width="100" align="center"></el-table-column>
        <el-table-column prop="phone" label="联系电话" width="120" align="center"></el-table-column>
        <el-table-column label="规格信息" align="center">
          <template slot-scope="scope">
            <div>{{ scope.row.material }} | 边长:{{ scope.row.sideLength }}mm | 高:{{ scope.row.height }}mm</div>
            <div style="color: #909399; font-size: 12px">{{ scope.row.layers }} | {{ scope.row.pattern }}</div>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="下单时间" width="180" align="center"></el-table-column>
        <el-table-column label="生产工序" width="450" align="center">
          <template slot-scope="scope">
            <el-steps :active="scope.row.status" finish-status="success" align-center size="small">
              <el-step title="制胎"></el-step>
              <el-step title="刮灰"></el-step>
              <el-step title="髹漆"></el-step>
              <el-step title="雕刻"></el-step>
              <el-step title="推光"></el-step>
              <el-step title="装配"></el-step>
              <el-step title="完工"></el-step>
            </el-steps>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="280" align="center">
          <template slot-scope="scope">
            <el-button
              size="small"
              type="primary"
              @click="nextStep(scope.row)"
              :disabled="scope.row.status >= 6"
              v-if="scope.row.status < 6">
              下一工序
            </el-button>
            <el-button
              size="small"
              type="success"
              disabled
              v-else>
              已完成
            </el-button>
            <el-button
              size="small"
              type="info"
              @click="showHistory(scope.row)">
              操作历史
            </el-button>
            <el-button
              size="small"
              type="danger"
              @click="deleteOrder(scope.row.id)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-empty v-if="orders.length === 0" description="暂无订单数据"></el-empty>

      <el-dialog title="工序操作历史" :visible.sync="historyDialogVisible" width="600px">
        <el-timeline v-if="currentOrder.operationHistory && currentOrder.operationHistory.length > 0">
          <el-timeline-item
            v-for="(item, index) in currentOrder.operationHistory"
            :key="index"
            :timestamp="item.operateTime"
            placement="top">
            <el-card>
              <h4>{{ item.statusText }}</h4>
              <p>操作人：{{ item.operator }}</p>
              <p style="color: #909399; font-size: 12px">{{ item.remark }}</p>
            </el-card>
          </el-timeline-item>
        </el-timeline>
        <el-empty v-else description="暂无操作记录"></el-empty>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>
const statusMap = ['制胎', '刮灰', '髹漆', '雕刻', '推光', '装配', '完工']

export default {
  name: 'AdminPanel',
  data() {
    return {
      loading: false,
      orders: [],
      storageListener: null,
      currentOperator: '管理员',
      historyDialogVisible: false,
      currentOrder: {}
    }
  },
  created() {
    this.loadOrders()
    this.setupStorageListener()
  },
  beforeDestroy() {
    if (this.storageListener) {
      window.removeEventListener('storage', this.storageListener)
    }
  },
  methods: {
    setupStorageListener() {
      this.storageListener = (e) => {
        if (e.key === 'lacquerOrders') {
          this.loadOrders()
        }
      }
      window.addEventListener('storage', this.storageListener)
    },
    loadOrders() {
      this.orders = JSON.parse(localStorage.getItem('lacquerOrders') || '[]')
    },
    nextStep(order) {
      const currentStatus = order.status
      const nextStatus = currentStatus + 1
      
      if (nextStatus > 6) {
        this.$message.warning('订单已完成所有工序')
        return
      }
      
      this.$confirm(`确认将订单 ${order.orderNo} 从「${statusMap[currentStatus]}」推进到「${statusMap[nextStatus]}」吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const orders = JSON.parse(localStorage.getItem('lacquerOrders') || '[]')
        const target = orders.find(item => item.id === order.id)
        
        if (!target) {
          this.$message.error('订单不存在')
          return
        }
        
        if (target.status !== currentStatus) {
          this.$message.warning('订单状态已变更，请刷新后重试')
          this.loadOrders()
          return
        }
        
        if (target.status >= 6) {
          this.$message.warning('订单已完成所有工序')
          return
        }
        
        target.status = nextStatus
        target.statusText = statusMap[target.status]
        
        if (!target.operationHistory) {
          target.operationHistory = []
        }
        target.operationHistory.push({
          status: nextStatus,
          statusText: statusMap[nextStatus],
          operator: this.currentOperator,
          operateTime: new Date().toLocaleString(),
          remark: `从「${statusMap[currentStatus]}」推进到「${statusMap[nextStatus]}」`
        })
        
        localStorage.setItem('lacquerOrders', JSON.stringify(orders))
        this.loadOrders()
        this.$message.success('已成功推进到：' + target.statusText)
      }).catch(() => {})
    },
    deleteOrder(id) {
      this.$confirm('确认删除该订单吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        let orders = JSON.parse(localStorage.getItem('lacquerOrders') || '[]')
        orders = orders.filter(item => item.id !== id)
        localStorage.setItem('lacquerOrders', JSON.stringify(orders))
        this.loadOrders()
        this.$message.success('删除成功')
      }).catch(() => {})
    },
    goToOrder() {
      this.$router.push('/')
    },
    showHistory(order) {
      this.currentOrder = order
      this.historyDialogVisible = true
    }
  }
}
</script>

<style scoped>
.admin-container {
  padding: 40px 20px;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  min-height: 100vh;
}
.admin-card {
  max-width: 1400px;
  margin: 0 auto;
  border-radius: 8px;
}
.card-header {
  font-size: 20px;
  font-weight: bold;
  color: #303133;
}
</style>
