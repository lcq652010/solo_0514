<template>
  <div class="admin-panel">
    <el-card class="panel-card" shadow="hover">
      <div slot="header" class="card-header">
        <span>订单管理 - 生产工序流程</span>
        <div class="header-right">
          <el-select v-model="currentOperator" placeholder="请选择操作员" size="small" style="width: 150px; margin-right: 10px;">
            <el-option v-for="op in operators" :key="op" :label="op" :value="op"></el-option>
          </el-select>
          <el-button type="primary" size="small" icon="el-icon-refresh" @click="loadOrders">刷新</el-button>
        </div>
      </div>
      
      <el-table :data="orders" border style="width: 100%" v-loading="loading" ref="orderTable" row-key="id" :row-class-name="getRowClassName">
        <el-table-column prop="id" label="订单号" width="150" align="center">
          <template slot-scope="scope">
            <div class="order-id-cell">
              <el-badge v-if="scope.row.isNew" :value="'新'" type="danger" class="new-badge">
                <span class="order-id">#{{ scope.row.id }}</span>
              </el-badge>
              <span v-else class="order-id">#{{ scope.row.id }}</span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="customerName" label="客户" width="100" align="center"></el-table-column>
        
        <el-table-column label="佛珠配置" min-width="220" align="center">
          <template slot-scope="scope">
            <div class="beads-config">
              <span>{{ scope.row.woodType }}</span>
              <span class="sep">|</span>
              <span>{{ scope.row.beadDiameter }}mm</span>
              <span class="sep">|</span>
              <span>{{ scope.row.beadCount }}颗</span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column label="工艺配置" min-width="180" align="center">
          <template slot-scope="scope">
            <div class="craft-config">
              <el-tag size="mini" type="warning">{{ scope.row.lacquerTechnique }}</el-tag>
              <el-tag size="mini" type="success" style="margin-left: 5px;">{{ scope.row.tasselStyle }}</el-tag>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column label="生产进度" min-width="450" align="center">
          <template slot-scope="scope">
            <div class="process-steps">
              <div 
                v-for="(step, index) in processSteps" 
                :key="index"
                class="step-item"
                :class="{ 
                  active: scope.row.status > index,
                  current: scope.row.status === index 
                }"
              >
                <div class="step-dot">
                  <i v-if="scope.row.status > index" class="el-icon-check"></i>
                  <span v-else>{{ index + 1 }}</span>
                </div>
                <div class="step-name">{{ step }}</div>
                <div v-if="index < processSteps.length - 1" class="step-line"></div>
              </div>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column label="操作记录" min-width="250" align="center">
          <template slot-scope="scope">
            <div class="process-time">
              <div v-if="scope.row.processRecords && scope.row.processRecords.length > 0">
                <el-popover 
                  v-for="(record, idx) in scope.row.processRecords" 
                  :key="idx"
                  placement="top"
                  width="200"
                  trigger="hover"
                >
                  <div class="record-detail">
                    <p><strong>工序：</strong>{{ record.step }}</p>
                    <p><strong>操作员：</strong>{{ record.operator }}</p>
                    <p><strong>时间：</strong>{{ record.time }}</p>
                  </div>
                  <el-tag slot="reference" size="mini" type="info" style="margin: 2px;">
                    {{ record.step }}
                  </el-tag>
                </el-popover>
              </div>
              <span v-else class="no-time">暂无记录</span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="createTime" label="下单时间" width="160" align="center"></el-table-column>
        
        <el-table-column label="操作" width="200" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button 
              v-if="scope.row.status < processSteps.length" 
              type="primary" 
              size="small" 
              @click="nextStep(scope.row, scope.$index)"
              :loading="processingIndex === scope.$index"
              :disabled="processingIndex !== -1 && processingIndex !== scope.$index"
            >
              下一工序
            </el-button>
            <el-tag v-else type="success" size="small">已完工</el-tag>
            <el-button 
              v-if="scope.row.isNew"
              type="info" 
              size="small" 
              icon="el-icon-view" 
              style="margin-left: 5px;"
              @click="markAsViewed(scope.$index)"
              title="标记为已查看"
            ></el-button>
            <el-button 
              type="danger" 
              size="small" 
              icon="el-icon-delete" 
              style="margin-left: 5px;"
              @click="deleteOrder(scope.$index)"
              :disabled="processingIndex !== -1"
            ></el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <el-empty v-if="orders.length === 0 && !loading" description="暂无订单数据"></el-empty>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'AdminPanel',
  data() {
    return {
      loading: false,
      orders: [],
      processingIndex: -1,
      lastOrderId: null,
      currentOperator: localStorage.getItem('lastOperator') || '',
      operators: ['张师傅', '李师傅', '王师傅', '赵师傅', '陈师傅'],
      processSteps: [
        '开珠',
        '粗磨',
        '上漆',
        '推光',
        '串珠',
        '配流苏',
        '质检',
        '完工'
      ]
    }
  },
  watch: {
    currentOperator(newVal) {
      localStorage.setItem('lastOperator', newVal)
    }
  },
  mounted() {
    this.loadOrders()
    window.addEventListener('orderUpdated', this.handleOrderUpdate)
  },
  beforeDestroy() {
    window.removeEventListener('orderUpdated', this.handleOrderUpdate)
  },
  methods: {
    handleOrderUpdate() {
      const oldFirstId = this.orders.length > 0 ? this.orders[0].id : null
      this.loadOrders(true).then(() => {
        if (this.orders.length > 0 && this.orders[0].id !== oldFirstId) {
          this.$nextTick(() => {
            this.scrollToNewOrder()
          })
        }
      })
    },
    scrollToNewOrder() {
      const table = this.$refs.orderTable
      if (table && table.$el) {
        const firstRow = table.$el.querySelector('.el-table__body-wrapper tr:first-child')
        if (firstRow) {
          firstRow.scrollIntoView({ behavior: 'smooth', block: 'center' })
          firstRow.classList.add('highlight-row')
          setTimeout(() => {
            firstRow.classList.remove('highlight-row')
          }, 3000)
        }
      }
    },
    loadOrders(silent = false) {
      if (!silent) {
        this.loading = true
      }
      return new Promise((resolve) => {
        setTimeout(() => {
          const storedOrders = JSON.parse(localStorage.getItem('beadsOrders') || '[]')
          this.orders = storedOrders.map(order => ({
            ...order,
            processRecords: order.processRecords || [],
            isNew: order.isNew !== undefined ? order.isNew : true
          }))
          this.loading = false
          resolve()
        }, silent ? 100 : 500)
      })
    },
    nextStep(order, index) {
      if (this.processingIndex !== -1) {
        this.$message.warning('正在处理其他订单，请稍候')
        return
      }
      
      if (!this.currentOperator) {
        this.$message.warning('请先选择当前操作人员')
        return
      }
      
      this.$confirm(
        `确认将订单 #${order.id} 推进到「${this.processSteps[order.status + 1]}」工序？`,
        '工序推进确认',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(() => {
        this.processingIndex = index
        const nextStatus = order.status + 1
        
        setTimeout(() => {
          if (!this.orders[index].processRecords) {
            this.$set(this.orders[index], 'processRecords', [])
          }
          
          this.orders[index].status = nextStatus
          this.orders[index].processRecords.push({
            step: this.processSteps[nextStatus],
            operator: this.currentOperator,
            time: new Date().toLocaleString()
          })
          
          localStorage.setItem('beadsOrders', JSON.stringify(this.orders))
          
          const currentStep = this.processSteps[this.orders[index].status]
          this.$message({
            type: 'success',
            message: `订单 #${order.id} 已进入「${currentStep}」工序！`
          })
          this.processingIndex = -1
        }, 500)
      }).catch(() => {})
    },
    getRowClassName({ row }) {
      return row.isNew ? 'new-order-row' : ''
    },
    markAsViewed(index) {
      this.orders[index].isNew = false
      localStorage.setItem('beadsOrders', JSON.stringify(this.orders))
      this.$message({
        type: 'success',
        message: '已标记为已查看'
      })
    },
    deleteOrder(index) {
      if (this.processingIndex !== -1) {
        this.$message.warning('正在处理订单，请稍候再删除')
        return
      }
      
      this.$confirm('确定要删除该订单吗？', '删除确认', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'error'
      }).then(() => {
        this.orders.splice(index, 1)
        localStorage.setItem('beadsOrders', JSON.stringify(this.orders))
        this.$message({
          type: 'success',
          message: '订单已删除'
        })
      }).catch(() => {})
    }
  }
}
</script>

<style scoped>
.admin-panel {
  width: 100%;
}

.panel-card {
  border-radius: 8px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 20px;
  font-weight: 600;
  color: #8B4513;
}

.header-right {
  display: flex;
  align-items: center;
}

.order-id-cell {
  position: relative;
  display: inline-block;
}

.order-id {
  font-family: 'Courier New', monospace;
  color: #8B4513;
  font-weight: 600;
}

.new-badge {
  display: inline-block;
}

.new-badge .el-badge__content {
  transform: translateX(10px);
}

.beads-config {
  font-size: 13px;
  line-height: 1.5;
}

.beads-config .sep {
  color: #dcdfe6;
  margin: 0 5px;
}

.craft-config {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

.process-steps {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 5px;
}

.step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  flex: 1;
}

.step-dot {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: #909399;
  font-weight: 600;
  transition: all 0.3s;
  z-index: 1;
}

.step-item.active .step-dot {
  background: #67C23A;
  color: white;
}

.step-item.current .step-dot {
  background: #409EFF;
  color: white;
  box-shadow: 0 0 0 4px rgba(64, 158, 255, 0.2);
}

.step-name {
  font-size: 12px;
  margin-top: 5px;
  color: #909399;
  transition: all 0.3s;
  white-space: nowrap;
}

.step-item.active .step-name,
.step-item.current .step-name {
  color: #303133;
  font-weight: 600;
}

.step-line {
  position: absolute;
  top: 14px;
  left: 50%;
  width: 100%;
  height: 2px;
  background: #f0f0f0;
  transition: all 0.3s;
}

.step-item.active .step-line {
  background: #67C23A;
}

.process-time {
  max-height: 80px;
  overflow-y: auto;
}

.process-time .no-time {
  color: #909399;
  font-size: 12px;
}
</style>

<style>
.highlight-row {
  animation: highlightPulse 3s ease-in-out;
}

@keyframes highlightPulse {
  0%, 100% {
    background-color: transparent;
  }
  25%, 75% {
    background-color: #ecf5ff;
  }
  50% {
    background-color: #d9ecff;
  }
}

.new-order-row > td {
  background-color: #fef0f0 !important;
}

.new-order-row:hover > td {
  background-color: #fde2e2 !important;
}

.record-detail p {
  margin: 5px 0;
  font-size: 13px;
}
</style>
