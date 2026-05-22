<template>
  <div class="admin-dashboard">
    <div class="page-header">
      <h1>订单管理后台</h1>
      <p>传统手工油纸伞生产流程管理</p>
    </div>
    
    <el-card class="stats-card">
      <el-row :gutter="20">
        <el-col :span="5">
          <div class="stat-item">
            <div class="stat-value">{{ orders.length }}</div>
            <div class="stat-label">总订单数</div>
          </div>
        </el-col>
        <el-col :span="5">
          <div class="stat-item">
            <div class="stat-value">{{ pendingCount }}</div>
            <div class="stat-label">待处理</div>
          </div>
        </el-col>
        <el-col :span="5">
          <div class="stat-item">
            <div class="stat-value">{{ processingCount }}</div>
            <div class="stat-label">生产中</div>
          </div>
        </el-col>
        <el-col :span="5">
          <div class="stat-item">
            <div class="stat-value">{{ completedCount }}</div>
            <div class="stat-label">已完工</div>
          </div>
        </el-col>
        <el-col :span="4">
          <div class="operator-select">
            <span class="operator-label">当前操作员：</span>
            <el-select v-model="currentOperator" placeholder="请选择" size="small" style="width: 100px;">
              <el-option label="张师傅" value="张师傅"></el-option>
              <el-option label="李师傅" value="李师傅"></el-option>
              <el-option label="王师傅" value="王师傅"></el-option>
              <el-option label="赵师傅" value="赵师傅"></el-option>
              <el-option label="管理员" value="管理员"></el-option>
            </el-select>
          </div>
        </el-col>
      </el-row>
    </el-card>
    
    <el-card class="table-card">
      <div class="table-toolbar">
        <el-button type="primary" icon="el-icon-refresh" @click="manualRefresh">
          刷新列表
        </el-button>
        <el-switch 
          v-model="autoRefresh" 
          active-text="自动刷新"
          inactive-text="关闭刷新">
        </el-switch>
        <span style="margin-left: 10px; color: #909399;">
          {{ autoRefresh ? `每 ${refreshInterval/1000} 秒自动刷新` : '' }}
        </span>
      </div>
      
      <el-table 
        :data="orders" 
        border 
        style="width: 100%"
        ref="orderTable"
        row-key="id"
        :row-class-name="tableRowClassName"
        :expand-row-keys="expandRowKeys"
        @expand-change="handleExpandChange">
        <el-table-column type="expand" width="60">
          <template slot-scope="scope">
            <div class="operation-log">
              <h4>操作记录</h4>
              <div v-if="!scope.row.operationLogs || scope.row.operationLogs.length === 0" class="no-log">
                暂无操作记录
              </div>
              <div v-else class="log-list">
                <div v-for="(log, index) in scope.row.operationLogs" :key="index" class="log-item">
                  <span class="log-time">{{ log.time }}</span>
                  <span class="log-operator">{{ log.operator }}</span>
                  <span class="log-action">{{ log.action }}</span>
                </div>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="id" label="订单号" width="180">
          <template slot-scope="scope">
            <span v-if="scope.row.isNew" class="new-order-badge">
              最新
            </span>
            {{ scope.row.id }}
          </template>
        </el-table-column>
        <el-table-column prop="customerName" label="客户姓名" width="100"></el-table-column>
        <el-table-column prop="phone" label="联系电话" width="120"></el-table-column>
        <el-table-column label="定制详情" width="250">
          <template slot-scope="scope">
            <div class="detail-item">伞骨: {{ scope.row.frameMaterial }}</div>
            <div class="detail-item">直径: {{ scope.row.diameter }}cm</div>
            <div class="detail-item">图案: {{ scope.row.pattern }}</div>
            <div class="detail-item">伞柄: {{ scope.row.handleStyle }}</div>
          </template>
        </el-table-column>
        <el-table-column label="生产进度" width="400">
          <template slot-scope="scope">
            <el-steps :active="scope.row.status" finish-status="success" size="small" direction="vertical" align-center>
              <el-step title="选材" description="选择优质竹材"></el-step>
              <el-step title="制骨" description="制作伞骨骨架"></el-step>
              <el-step title="裱纸" description="粘贴伞面纸张"></el-step>
              <el-step title="绘纹" description="绘制图案纹饰"></el-step>
              <el-step title="上油" description="涂刷防护桐油"></el-step>
              <el-step title="装柄" description="安装伞柄流苏"></el-step>
              <el-step title="质检" description="质量检查验收"></el-step>
              <el-step title="完工" description="订单完成"></el-step>
            </el-steps>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="280">
          <template slot-scope="scope">
            <div class="action-buttons">
              <el-select 
                v-if="scope.row.status < 7"
                v-model="jumpTarget[scope.row.id]" 
                placeholder="跳转到" 
                size="small" 
                style="width: 100px; margin-right: 5px;"
                @change="handleJump(scope.row, $event)">
                <el-option 
                  v-for="i in getAvailableSteps(scope.row.status)" 
                  :key="i" 
                  :label="stepLabels[i]" 
                  :value="i">
                </el-option>
              </el-select>
              <el-button 
                v-if="scope.row.status < 7" 
                type="primary" 
                size="small" 
                @click="nextStep(scope.row)">
                下一工序
              </el-button>
              <el-tag v-else type="success" size="small">已完工</el-tag>
              <el-button 
                type="danger" 
                size="small" 
                style="margin-left: 5px;"
                @click="deleteOrder(scope.$index, scope.row.id)">
                删除
              </el-button>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="下单时间" width="180"></el-table-column>
      </el-table>
      
      <el-empty v-if="orders.length === 0" description="暂无订单"></el-empty>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'AdminDashboard',
  data() {
    return {
      orders: [],
      autoRefresh: true,
      refreshInterval: 5000,
      refreshTimer: null,
      jumpTarget: {},
      currentOperator: '管理员',
      stepLabels: {
        0: '选材',
        1: '制骨',
        2: '裱纸',
        3: '绘纹',
        4: '上油',
        5: '装柄',
        6: '质检',
        7: '完工'
      },
      latestOrderId: null,
      expandRowKeys: []
    }
  },
  computed: {
    pendingCount() {
      return this.orders.filter(o => o.status === 0).length
    },
    processingCount() {
      return this.orders.filter(o => o.status > 0 && o.status < 7).length
    },
    completedCount() {
      return this.orders.filter(o => o.status === 7).length
    }
  },
  mounted() {
    this.loadOrders()
    this.startAutoRefresh()
  },
  beforeDestroy() {
    this.stopAutoRefresh()
  },
  methods: {
    tableRowClassName({ row }) {
      return row.isNew ? 'new-order-row' : ''
    },
    getAvailableSteps(currentStatus) {
      const steps = []
      for (let i = currentStatus + 1; i <= 7; i++) {
        steps.push(i)
      }
      return steps
    },
    handleExpandChange(row, expandedRows) {
      this.expandRowKeys = expandedRows.map(item => item.id)
    },
    addOperationLog(order, action) {
      if (!order.operationLogs) {
        order.operationLogs = []
      }
      order.operationLogs.unshift({
        time: new Date().toLocaleString(),
        operator: this.currentOperator,
        action: action
      })
    },
    loadOrders() {
      const storedOrders = JSON.parse(localStorage.getItem('umbrellaOrders') || '[]')
      
      if (storedOrders.length > 0 && storedOrders[0].id !== this.latestOrderId) {
        this.latestOrderId = storedOrders[0].id
        storedOrders[0].isNew = true
        
        setTimeout(() => {
          this.$nextTick(() => {
            const idx = this.orders.findIndex(o => o.id === this.latestOrderId)
            if (idx !== -1) {
              this.orders[idx].isNew = false
            }
          })
        }, 8000)
      }
      
      this.orders = storedOrders
    },
    manualRefresh() {
      this.loadOrders()
      this.$message({
        type: 'success',
        message: '列表已刷新'
      })
      
      if (this.orders.length > 0) {
        this.$nextTick(() => {
          const table = this.$refs.orderTable
          if (table) {
            table.setCurrentRow(this.orders[0])
          }
        })
      }
    },
    startAutoRefresh() {
      this.stopAutoRefresh()
      if (this.autoRefresh) {
        this.refreshTimer = setInterval(() => {
          this.loadOrders()
        }, this.refreshInterval)
      }
    },
    stopAutoRefresh() {
      if (this.refreshTimer) {
        clearInterval(this.refreshTimer)
        this.refreshTimer = null
      }
    },
    nextStep(order) {
      const index = this.orders.findIndex(o => o.id === order.id)
      if (index !== -1 && order.status < 7) {
        const oldStatus = this.orders[index].status
        this.orders[index].status += 1
        const newStatus = this.orders[index].status
        this.addOperationLog(
          this.orders[index], 
          `工序变更: ${this.stepLabels[oldStatus]} → ${this.stepLabels[newStatus]}`
        )
        localStorage.setItem('umbrellaOrders', JSON.stringify(this.orders))
        this.$message({
          type: 'success',
          message: `已进入下一工序: ${this.stepLabels[newStatus]}`
        })
      }
    },
    handleJump(order, targetStatus) {
      const index = this.orders.findIndex(o => o.id === order.id)
      if (index !== -1) {
        const oldStatus = this.orders[index].status
        this.orders[index].status = targetStatus
        this.addOperationLog(
          this.orders[index], 
          `工序跳转: ${this.stepLabels[oldStatus]} → ${this.stepLabels[targetStatus]}`
        )
        localStorage.setItem('umbrellaOrders', JSON.stringify(this.orders))
        this.$message({
          type: 'success',
          message: `已跳转到工序: ${this.stepLabels[targetStatus]}`
        })
        this.jumpTarget[order.id] = ''
      }
    },
    deleteOrder(index, id) {
      this.$confirm('确认删除该订单吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.addOperationLog(this.orders[index], '删除订单')
        this.orders.splice(index, 1)
        localStorage.setItem('umbrellaOrders', JSON.stringify(this.orders))
        this.$message({
          type: 'success',
          message: '删除成功'
        })
      }).catch(() => {})
    }
  },
  watch: {
    autoRefresh(val) {
      if (val) {
        this.startAutoRefresh()
      } else {
        this.stopAutoRefresh()
      }
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 40px 0;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 32px;
  color: #303133;
  margin-bottom: 10px;
}

.page-header p {
  font-size: 16px;
  color: #606266;
}

.stats-card {
  max-width: 1300px;
  margin: 0 auto 20px;
}

.stat-item {
  text-align: center;
  padding: 20px;
}

.stat-value {
  font-size: 36px;
  font-weight: bold;
  color: #409EFF;
}

.stat-label {
  font-size: 14px;
  color: #606266;
  margin-top: 8px;
}

.operator-select {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.operator-label {
  font-size: 14px;
  color: #606266;
  margin-right: 10px;
}

.table-card {
  max-width: 1400px;
  margin: 0 auto;
}

.table-toolbar {
  margin-bottom: 15px;
  display: flex;
  align-items: center;
}

.detail-item {
  font-size: 12px;
  color: #606266;
  line-height: 1.6;
}

.action-buttons {
  display: flex;
  align-items: center;
}

.new-order-badge {
  display: inline-block;
  background: #67C23A;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: bold;
  margin-right: 8px;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.05);
  }
}

.operation-log {
  padding: 15px;
  background: #f8f9fa;
  border-radius: 4px;
}

.operation-log h4 {
  margin: 0 0 12px 0;
  color: #303133;
  font-size: 14px;
}

.no-log {
  color: #909399;
  font-size: 12px;
  text-align: center;
  padding: 20px;
}

.log-list {
  max-height: 200px;
  overflow-y: auto;
}

.log-item {
  display: flex;
  padding: 8px 12px;
  background: white;
  border-radius: 4px;
  margin-bottom: 8px;
  border-left: 3px solid #409EFF;
}

.log-time {
  color: #909399;
  font-size: 12px;
  min-width: 160px;
}

.log-operator {
  color: #67C23A;
  font-size: 12px;
  font-weight: bold;
  min-width: 80px;
}

.log-action {
  color: #303133;
  font-size: 12px;
  flex: 1;
}

:deep(.el-step__title) {
  font-size: 12px;
}

:deep(.el-step__description) {
  font-size: 11px;
}

:deep(.new-order-row) {
  background-color: #e6f7ff !important;
  animation: highlightPulse 2s ease-in-out infinite;
}

:deep(.new-order-row:hover) {
  background-color: #bae7ff !important;
}

:deep(.new-order-row > td) {
  background-color: inherit !important;
}

@keyframes highlightPulse {
  0%, 100% {
    background-color: #e6f7ff;
  }
  50% {
    background-color: #bae7ff;
  }
}
</style>
