<template>
  <div class="admin-page">
    <el-card class="card-shadow">
      <div slot="header" class="card-header">
        <span>订单管理</span>
        <el-button type="primary" size="small" @click="refreshOrders">刷新订单</el-button>
      </div>

      <el-table :data="orders" border stripe style="width: 100%" v-loading="loading" :row-class-name="tableRowClassName" ref="orderTable">
        <el-table-column label="" width="60" class-name="badge-column">
          <template slot-scope="scope">
            <div v-if="isNewOrder(scope.row)" class="new-order-badge">
              <span class="badge-text">新</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="id" label="订单号" width="120"></el-table-column>
        <el-table-column prop="customerName" label="客户姓名" width="100"></el-table-column>
        <el-table-column prop="phone" label="联系电话" width="130"></el-table-column>
        <el-table-column prop="stoneMaterialLabel" label="印石材质" width="100"></el-table-column>
        <el-table-column prop="size" label="尺寸" width="80">
          <template slot-scope="scope">
            {{ scope.row.size }}cm
          </template>
        </el-table-column>
        <el-table-column prop="fontStyleLabel" label="字体" width="80"></el-table-column>
        <el-table-column prop="sealContent" label="印文" width="120"></el-table-column>
        <el-table-column prop="sideOptionLabel" label="边款" width="100"></el-table-column>
        <el-table-column prop="price" label="价格" width="80">
          <template slot-scope="scope">
            ¥{{ scope.row.price }}
          </template>
        </el-table-column>
        <el-table-column label="生产进度" min-width="280">
          <template slot-scope="scope">
            <el-steps :active="scope.row.currentStep - 1" finish-status="success" align-center size="small">
              <el-step v-for="step in processSteps" :key="step.id" :title="step.name"></el-step>
            </el-steps>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template slot-scope="scope">
            <el-button 
              v-if="!isOrderCompleted(scope.row)" 
              type="primary" 
              size="mini" 
              @click="nextStep(scope.row)"
              :disabled="isCurrentStepCompleted(scope.row)">
              {{ getCurrentStepName(scope.row) }}
            </el-button>
            <el-button v-else type="success" size="mini" disabled>
              已完工
            </el-button>
            <el-button size="mini" @click="viewDetail(scope.row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-empty v-if="orders.length === 0 && !loading" description="暂无订单数据"></el-empty>
    </el-card>

    <el-dialog title="订单详情" :visible.sync="detailVisible" width="700px">
      <el-descriptions :column="2" border v-if="currentOrder" class="detail-section">
        <el-descriptions-item label="订单号">{{ currentOrder.id }}</el-descriptions-item>
        <el-descriptions-item label="下单时间">{{ currentOrder.createTime }}</el-descriptions-item>
        <el-descriptions-item label="客户姓名">{{ currentOrder.customerName }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ currentOrder.phone }}</el-descriptions-item>
        <el-descriptions-item label="印石材质">{{ currentOrder.stoneMaterialLabel }}</el-descriptions-item>
        <el-descriptions-item label="印章尺寸">{{ currentOrder.size }}cm</el-descriptions-item>
        <el-descriptions-item label="字体风格">{{ currentOrder.fontStyleLabel }}</el-descriptions-item>
        <el-descriptions-item label="订单价格">¥{{ currentOrder.price }}</el-descriptions-item>
        <el-descriptions-item label="印文内容" :span="2">{{ currentOrder.sealContent }}</el-descriptions-item>
        <el-descriptions-item label="边款需求" :span="2">{{ currentOrder.sideOptionLabel }}</el-descriptions-item>
        <el-descriptions-item v-if="currentOrder.sideContent" label="边款内容" :span="2">{{ currentOrder.sideContent }}</el-descriptions-item>
      </el-descriptions>
      
      <div v-if="currentOrder && currentOrder.stepLogs && currentOrder.stepLogs.length > 0" class="logs-section">
        <h4 class="logs-title"><i class="el-icon-time"></i> 工序操作记录</h4>
        <el-timeline>
          <el-timeline-item
            v-for="(log, index) in currentOrder.stepLogs"
            :key="index"
            :timestamp="log.time"
            placement="top"
            type="success"
            color="#67c23a">
            <div class="log-content">
              <span class="log-step">{{ log.step }}</span>
              <span class="log-divider">|</span>
              <span class="log-operator">操作人：{{ log.operator }}</span>
              <el-tag size="mini" type="info" class="log-terminal">{{ log.terminal }}</el-tag>
            </div>
          </el-timeline-item>
        </el-timeline>
      </div>
      
      <div slot="footer" class="dialog-footer">
        <el-button @click="detailVisible = false">关闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { processSteps, orders as mockOrders } from '../data/mockData'

export default {
  name: 'AdminPage',
  data() {
    return {
      processSteps,
      orders: [],
      loading: false,
      detailVisible: false,
      currentOrder: null,
      newOrderId: null,
      highlightingRow: null
    }
  },
  mounted() {
    this.newOrderId = this.$route.query.newOrderId
    this.loadOrders()
  },
  watch: {
    '$route.query'(query) {
      if (query.newOrderId && query.newOrderId !== this.newOrderId) {
        this.newOrderId = query.newOrderId
        this.loadOrders()
      }
    }
  },
  methods: {
    tableRowClassName({ row }) {
      let classes = []
      if (row.id === this.highlightingRow) {
        classes.push('highlight-row')
      }
      if (this.isNewOrder(row)) {
        classes.push('new-order-row')
      }
      return classes.join(' ')
    },
    loadOrders() {
      this.loading = true
      setTimeout(() => {
        const localOrders = JSON.parse(localStorage.getItem('sealOrders') || '[]')
        this.orders = localOrders.length > 0 ? localOrders.map(order => ({
          ...order,
          stepUpdated: order.stepUpdated || [false, false, false, false, false, false, false, false],
          createTimestamp: order.createTimestamp || Date.now() - 12 * 60 * 60 * 1000
        })) : [...mockOrders].map(order => ({
          ...order,
          stepUpdated: [false, false, false, false, false, false, false, false],
          createTimestamp: Date.now() - 12 * 60 * 60 * 1000
        }))
        
        this.loading = false
        
        this.$nextTick(() => {
          if (this.newOrderId) {
            this.highlightNewOrder(this.newOrderId)
          }
        })
      }, 500)
    },
    highlightNewOrder(orderId) {
      const index = this.orders.findIndex(order => order.id === orderId)
      if (index !== -1) {
        this.highlightingRow = orderId
        
        const table = this.$refs.orderTable
        if (table) {
          const tbody = table.$el.querySelector('.el-table__body-wrapper')
          if (tbody) {
            const rows = tbody.querySelectorAll('.el-table__row')
            if (rows[index]) {
              rows[index].scrollIntoView({ behavior: 'smooth', block: 'center' })
            }
          }
        }
        
        setTimeout(() => {
          this.highlightingRow = null
        }, 3000)
        
        this.$message.info(`已定位到新订单：${orderId}`)
      }
    },
    refreshOrders() {
      this.loadOrders()
      this.$message.success('订单已刷新')
    },
    getOperatorInfo() {
      return {
        operator: '管理员',
        terminal: navigator.userAgent.includes('Mobile') ? '移动端' : 'PC端',
        time: new Date().toLocaleString('zh-CN')
      }
    },
    nextStep(order) {
      if (!order.stepUpdated) {
        this.$set(order, 'stepUpdated', [false, false, false, false, false, false, false, false])
      }
      
      if (!order.stepLogs) {
        this.$set(order, 'stepLogs', [])
      }
      
      const currentStepIndex = order.currentStep - 1
      
      if (order.stepUpdated.every(step => step === true)) {
        this.$message.warning('该订单已全部完工')
        return
      }
      
      if (order.stepUpdated[currentStepIndex]) {
        this.$message.warning(`「${this.processSteps[currentStepIndex].name}」工序已完成，请勿重复操作`)
        return
      }
      
      if (currentStepIndex > 0 && !order.stepUpdated[currentStepIndex - 1]) {
        this.$message.warning(`请先完成「${this.processSteps[currentStepIndex - 1].name}」工序`)
        return
      }
      
      this.$set(order.stepUpdated, currentStepIndex, true)
      
      const operatorInfo = this.getOperatorInfo()
      order.stepLogs.push({
        step: this.processSteps[currentStepIndex].name,
        stepIndex: currentStepIndex,
        ...operatorInfo
      })
      
      if (currentStepIndex < 7) {
        order.currentStep++
      }
      
      if (order.stepUpdated.every(step => step === true)) {
        order.status = 'completed'
      }
      
      localStorage.setItem('sealOrders', JSON.stringify(this.orders))
      
      const stepName = this.processSteps[currentStepIndex]?.name
      this.$message.success(`订单 ${order.id}「${stepName}」工序已完成（${operatorInfo.terminal}）`)
    },
    viewDetail(order) {
      this.currentOrder = order
      this.detailVisible = true
    },
    isOrderCompleted(order) {
      return order.stepUpdated && order.stepUpdated.every(step => step === true)
    },
    isCurrentStepCompleted(order) {
      const stepIndex = order.currentStep - 1
      return order.stepUpdated && order.stepUpdated[stepIndex]
    },
    getCurrentStepName(order) {
      const stepIndex = order.currentStep - 1
      return this.processSteps[stepIndex]?.name || '下一工序'
    },
    isNewOrder(order) {
      if (!order.createTimestamp) {
        const parsedTime = Date.parse(order.createTime.replace(/\//g, '-'))
        return !isNaN(parsedTime) && (Date.now() - parsedTime < 24 * 60 * 60 * 1000)
      }
      return Date.now() - order.createTimestamp < 24 * 60 * 60 * 1000
    }
  }
}
</script>

<style scoped>
.admin-page {
  overflow-x: auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 20px;
  font-weight: 600;
  color: #8B4513;
}

.el-table {
  font-size: 13px;
}

.el-table /deep/ .el-step__title {
  font-size: 12px;
}

.el-table /deep/ .highlight-row {
  background-color: #fff7e6 !important;
  animation: pulse 1.5s ease-in-out infinite;
}

.el-table /deep/ .new-order-row {
  background: linear-gradient(90deg, #f0f9ff 0%, #e6f7ff 50%, #f0f9ff 100%) !important;
  background-size: 200% 100% !important;
  animation: gradientMove 3s ease infinite !important;
}

@keyframes pulse {
  0%, 100% {
    background-color: #fff7e6;
  }
  50% {
    background-color: #ffe7ba;
  }
}

@keyframes gradientMove {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.new-order-badge {
  position: relative;
  width: 36px;
  height: 36px;
  margin: 0 auto;
}

.badge-text {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
  color: white;
  font-weight: bold;
  font-size: 14px;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(255, 107, 107, 0.4);
  animation: badgePulse 2s ease-in-out infinite;
}

@keyframes badgePulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 2px 8px rgba(255, 107, 107, 0.4);
  }
  50% {
    transform: scale(1.1);
    box-shadow: 0 4px 16px rgba(255, 107, 107, 0.6);
  }
}

.dialog-footer {
  text-align: right;
}

.logs-section {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}

.logs-title {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 15px;
}

.logs-title i {
  color: #409eff;
  margin-right: 6px;
}

.log-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.log-step {
  font-weight: 600;
  color: #67c23a;
}

.log-divider {
  color: #dcdfe6;
}

.log-operator {
  color: #606266;
  font-size: 13px;
}

.log-terminal {
  margin-left: auto;
}
</style>
