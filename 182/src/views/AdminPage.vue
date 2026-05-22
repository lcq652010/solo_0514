<template>
  <div class="admin-page">
    <el-card shadow="hover">
      <div slot="header" class="card-header">
        <span>订单管理</span>
        <el-button type="primary" size="small" @click="refreshOrders">
          <i class="el-icon-refresh"></i> 刷新
        </el-button>
      </div>

      <el-tabs v-model="activeTab" type="card">
        <el-tab-pane label="全部订单" name="all">
          <div class="order-stats">
            <el-row :gutter="20">
              <el-col :span="6" v-for="(stat, index) in orderStats" :key="index">
                <div class="stat-card" :style="{ background: stat.color }">
                  <div class="stat-number">{{ stat.count }}</div>
                  <div class="stat-label">{{ stat.label }}</div>
                </div>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>
        <el-tab-pane label="工序跟踪" name="process">
          <div class="process-timeline">
            <div class="process-bar">
              <div 
                v-for="process in processes" 
                :key="process.id"
                class="process-step"
                :class="{ active: currentProcessFilter === process.id }"
                @click="filterByProcess(process.id)"
              >
                <i :class="process.icon"></i>
                <span>{{ process.name }}</span>
              </div>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>

      <el-table 
        :data="filteredOrders" 
        style="width: 100%; margin-top: 20px" 
        border
        ref="orderTable"
        row-key="id"
        :row-class-name="getNewOrderClass"
      >
        <el-table-column label="订单号" width="130" fixed>
          <template slot-scope="scope">
            <div class="order-id-cell">
              <span class="order-id">{{ scope.row.id }}</span>
              <el-tag v-if="scope.row.currentProcess === 0" type="danger" size="mini" class="new-badge">新订单</el-tag>
              <el-tag v-else-if="scope.row.id === newOrderId" type="warning" size="mini" class="new-badge">刚提交</el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="customerName" label="客户" width="90"></el-table-column>
        <el-table-column prop="phone" label="电话" width="120"></el-table-column>
        <el-table-column label="定制详情" width="250">
          <template slot-scope="scope">
            <div class="order-detail">
              <el-tag size="small" type="info">{{ scope.row.fabric }}</el-tag>
              <el-tag size="small" type="success">{{ scope.row.shape }}</el-tag>
              <el-tag size="small" type="warning">{{ scope.row.size }}cm</el-tag>
              <div class="formula-tags">
                <el-tag size="mini" type="danger" v-for="f in scope.row.formula.split('、')" :key="f">{{ f }}</el-tag>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="rope" label="挂绳" width="90"></el-table-column>
        <el-table-column prop="quantity" label="数量" width="70" align="center"></el-table-column>
        <el-table-column label="工序进度" min-width="350">
          <template slot-scope="scope">
            <div class="process-progress">
              <el-steps :active="scope.row.currentProcess" finish-status="success" align-center size="small">
                <el-step 
                  v-for="process in processes" 
                  :key="process.id"
                  :title="process.name"
                ></el-step>
              </el-steps>
              <div class="process-timestamps">
                <span 
                  v-for="process in processes" 
                  :key="process.id"
                  class="timestamp"
                  :class="{ active: scope.row.processTimestamps && scope.row.processTimestamps[process.id] }"
                >
                  <i v-if="scope.row.processTimestamps && scope.row.processTimestamps[process.id]" class="el-icon-time"></i>
                  {{ scope.row.processTimestamps && scope.row.processTimestamps[process.id] ? scope.row.processTimestamps[process.id].split(' ')[1] : '--:--:--' }}
                </span>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.currentProcess)" size="small">
              {{ getStatusText(scope.row.currentProcess) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="160"></el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template slot-scope="scope">
            <el-button 
              type="primary" 
              size="mini" 
              @click="nextProcess(scope.row)"
              :disabled="scope.row.currentProcess >= 8"
            >
              <i class="el-icon-arrow-right"></i> 下一道
            </el-button>
            <el-button type="danger" size="mini" @click="deleteOrder(scope.row.id)">
              <i class="el-icon-delete"></i> 删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog title="更新工序" :visible.sync="processDialogVisible" width="550px">
      <div class="process-dialog">
        <div class="order-info">
          <p><strong>订单号：</strong>{{ currentOrder?.id }}</p>
          <p><strong>客户：</strong>{{ currentOrder?.customerName }}</p>
        </div>
        
        <el-form v-if="currentOrder && currentOrder.currentProcess < 8" class="operator-form">
          <el-form-item label="当前操作员">
            <el-select v-model="operatorName" placeholder="请选择或输入操作员" style="width: 100%" filterable allow-create>
              <el-option v-for="op in operatorList" :key="op" :label="op" :value="op"></el-option>
            </el-select>
          </el-form-item>
          <el-alert 
            :title="nextProcessInfo" type="info" :closable="false" size="small" show-icon>
          </el-alert>
        </el-form>

        <div class="process-steps-with-time">
          <div 
            v-for="process in processes" 
            :key="process.id"
            class="process-step-item"
            :class="{ completed: currentOrder && currentOrder.currentProcess >= process.id, next: currentOrder && currentOrder.currentProcess + 1 === process.id }"
          >
            <div class="process-icon">
              <i :class="process.icon"></i>
            </div>
            <div class="process-content">
              <div class="process-name">
                {{ process.name }}
                <el-tag v-if="currentOrder && currentOrder.currentProcess + 1 === process.id" size="mini" type="warning" class="next-tag">下一道</el-tag>
              </div>
              <div class="process-time" v-if="currentOrder && currentOrder.processTimestamps && currentOrder.processTimestamps[process.id]">
                <span><i class="el-icon-time"></i> {{ currentOrder.processTimestamps[process.id] }}</span>
                <span class="operator-name">
                  <i class="el-icon-user"></i> {{ currentOrder.processOperators && currentOrder.processOperators[process.id] }}
                </span>
              </div>
              <div class="process-time pending" v-else>
                <i class="el-icon-clock"></i> 待完成
              </div>
            </div>
          </div>
        </div>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="processDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmNextProcess" :disabled="currentOrder?.currentProcess >= 8 || !operatorName">
          确认完成下一道工序
        </el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import orderStore from '../store/orders'

export default {
  name: 'AdminPage',
  data() {
    return {
      activeTab: 'all',
      currentProcessFilter: null,
      processDialogVisible: false,
      currentOrder: null,
      processes: [],
      newOrderId: null,
      operatorName: '',
      operatorList: ['李师傅', '王师傅', '张师傅', '赵师傅', '钱师傅', '孙师傅', '陈师傅', '刘师傅', '杨师傅']
    }
  },
  computed: {
    orders() {
      return orderStore.getOrders()
    },
    filteredOrders() {
      if (this.currentProcessFilter !== null) {
        return this.orders.filter(o => o.currentProcess === this.currentProcessFilter)
      }
      return this.orders
    },
    orderStats() {
      return [
        { label: '待开始', count: this.orders.filter(o => o.currentProcess === 0).length, color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' },
        { label: '生产中', count: this.orders.filter(o => o.currentProcess > 0 && o.currentProcess < 8).length, color: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' },
        { label: '已完工', count: this.orders.filter(o => o.currentProcess === 8).length, color: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)' },
        { label: '总订单', count: this.orders.length, color: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)' }
      ]
    },
    nextProcessInfo() {
      if (!this.currentOrder || this.currentOrder.currentProcess >= 8) return ''
      const nextProcessId = this.currentOrder.currentProcess + 1
      const nextProcess = this.processes.find(p => p.id === nextProcessId)
      return `即将完成：${nextProcess?.name || ''}，请确认操作员信息`
    }
  },
  mounted() {
    this.processes = orderStore.getProcesses()
    if (this.$route.query.newOrderId) {
      this.newOrderId = this.$route.query.newOrderId
      this.$nextTick(() => {
        this.scrollToNewOrder()
      })
    }
  },
  methods: {
    getNewOrderClass({ row }) {
      if (row.currentProcess === 0) return 'new-order-row'
      if (row.id === this.newOrderId) return 'new-order-row'
      return ''
    },
    scrollToNewOrder() {
      if (!this.newOrderId) return
      const table = this.$refs.orderTable
      if (table) {
        const rows = table.$el.querySelectorAll('.el-table__row')
        rows.forEach((row, index) => {
          if (row.textContent.includes(this.newOrderId)) {
            row.scrollIntoView({ behavior: 'smooth', block: 'center' })
            row.classList.add('highlight-flash')
            setTimeout(() => {
              row.classList.remove('highlight-flash')
            }, 3000)
          }
        })
      }
    },
    refreshOrders() {
      this.$message.success('数据已刷新')
    },
    filterByProcess(processId) {
      if (this.currentProcessFilter === processId) {
        this.currentProcessFilter = null
      } else {
        this.currentProcessFilter = processId
      }
    },
    getStatusType(process) {
      if (process === 0) return 'info'
      if (process === 8) return 'success'
      return 'warning'
    },
    getStatusText(process) {
      if (process === 0) return '待开始'
      if (process === 8) return '已完工'
      return '生产中'
    },
    nextProcess(order) {
      this.currentOrder = order
      this.operatorName = ''
      this.processDialogVisible = true
    },
    confirmNextProcess() {
      if (this.currentOrder && this.currentOrder.currentProcess < 8 && this.operatorName) {
        const newProcess = this.currentOrder.currentProcess + 1
        orderStore.updateProcess(this.currentOrder.id, newProcess, this.operatorName)
        this.currentOrder.currentProcess = newProcess
        if (!this.currentOrder.processTimestamps) {
          this.$set(this.currentOrder, 'processTimestamps', {})
        }
        if (!this.currentOrder.processOperators) {
          this.$set(this.currentOrder, 'processOperators', {})
        }
        this.$set(this.currentOrder.processTimestamps, newProcess, new Date().toLocaleString('zh-CN'))
        this.$set(this.currentOrder.processOperators, newProcess, this.operatorName)
        this.processDialogVisible = false
        this.$message.success(`工序已更新为：${this.processes[newProcess - 1].name}，操作员：${this.operatorName}`)
      }
    },
    deleteOrder(orderId) {
      this.$confirm('确认删除该订单吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        orderStore.deleteOrder(orderId)
        this.$message.success('订单已删除')
      }).catch(() => {})
    }
  }
}
</script>

<style scoped>
.admin-page {
  max-width: 1200px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 20px;
  font-weight: 500;
  color: #667eea;
}

.order-stats {
  padding: 20px 0;
}

.stat-card {
  padding: 20px;
  border-radius: 8px;
  color: white;
  text-align: center;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
}

.process-timeline {
  padding: 20px 0;
}

.process-bar {
  display: flex;
  justify-content: space-between;
  background: #f5f7fa;
  padding: 15px;
  border-radius: 8px;
}

.process-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  padding: 10px 20px;
  border-radius: 6px;
  transition: all 0.3s;
}

.process-step:hover {
  background: #e6f7ff;
}

.process-step.active {
  background: #667eea;
  color: white;
}

.process-step i {
  font-size: 24px;
  margin-bottom: 8px;
}

.order-detail {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.formula-tags {
  width: 100%;
  margin-top: 5px;
  display: flex;
  flex-wrap: wrap;
  gap: 3px;
}

.process-progress {
  padding: 10px 0;
}

.process-timestamps {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  padding: 0 5px;
}

.process-timestamps .timestamp {
  font-size: 10px;
  color: #909399;
  text-align: center;
  flex: 1;
}

.process-timestamps .timestamp.active {
  color: #67c23a;
}

.process-timestamps .timestamp i {
  margin-right: 2px;
}

.process-dialog {
  padding: 20px 0;
}

.order-info {
  margin-bottom: 20px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 6px;
}

.order-info p {
  margin: 5px 0;
}

.process-steps-with-time {
  max-height: 400px;
  overflow-y: auto;
}

.process-step-item {
  display: flex;
  align-items: flex-start;
  padding: 12px 0;
  border-bottom: 1px solid #ebeef5;
}

.process-step-item:last-child {
  border-bottom: none;
}

.process-step-item .process-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  color: #909399;
}

.process-step-item.completed .process-icon {
  background: #67c23a;
  color: white;
}

.process-step-item .process-content {
  flex: 1;
}

.process-step-item .process-name {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
}

.process-step-item.completed .process-name {
  color: #67c23a;
}

.process-step-item .process-time {
  font-size: 12px;
  color: #67c23a;
  margin-top: 4px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.process-step-item .process-time.pending {
  color: #909399;
}

.process-step-item .process-time .operator-name {
  color: #409eff;
}

.process-step-item.next {
  background: #fdf6ec;
  border-radius: 6px;
  padding: 12px;
  margin: 4px 0;
}

.process-step-item.next .process-icon {
  background: #e6a23c;
  color: white;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.next-tag {
  margin-left: 8px;
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.operator-form {
  margin-bottom: 20px;
  padding: 15px;
  background: #f0f9ff;
  border-radius: 6px;
  border: 1px solid #b3d8ff;
}

.new-order-row {
  background: #fef0f0 !important;
}

.el-table__row.new-order-row:hover > td {
  background: #fde2e2 !important;
}

.highlight-flash {
  animation: flashHighlight 1s ease-in-out 3;
}

@keyframes flashHighlight {
  0%, 100% {
    background-color: transparent;
  }
  50% {
    background-color: #667eea40;
  }
}

.order-id-cell {
  display: flex;
  align-items: center;
  gap: 6px;
}

.order-id {
  font-weight: 600;
  color: #303133;
}

.new-badge {
  animation: badgePulse 1.5s infinite;
  margin-left: auto;
}

@keyframes badgePulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(245, 108, 108, 0.4);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 0 0 4px rgba(245, 108, 108, 0);
  }
}
</style>
