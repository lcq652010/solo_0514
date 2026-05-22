<template>
  <div class="page-container">
    <h2 class="page-title">
      <i class="el-icon-setting"></i>
      订单管理中心
    </h2>

    <el-card class="card-shadow">
      <div slot="header" class="card-header">
        <span>订单列表</span>
        <div class="header-right">
          <el-select v-model="searchType" style="width: 120px; margin-right: 8px">
            <el-option label="订单号" value="id"></el-option>
            <el-option label="客户名" value="customer"></el-option>
            <el-option label="全部" value="all"></el-option>
          </el-select>
          <el-input
            v-model="searchKeyword"
            :placeholder="searchPlaceholder"
            style="width: 220px; margin-right: 16px"
            clearable
            @clear="handleSearch"
            @keyup.enter.native="handleSearch"
          >
            <i slot="prefix" class="el-input__icon el-icon-search" @click="handleSearch"></i>
          </el-input>
          <el-select v-model="filterStatus" placeholder="状态筛选" style="width: 140px; margin-right: 16px" clearable @change="handleSearch">
            <el-option label="待生产" value="0"></el-option>
            <el-option label="生产中" value="processing"></el-option>
            <el-option label="已完工" value="7"></el-option>
          </el-select>
          <el-button type="primary" icon="el-icon-refresh" @click="refreshOrders">
            刷新
          </el-button>
        </div>
      </div>

      <el-table
        ref="orderTable"
        :data="filteredOrders"
        border
        stripe
        style="width: 100%"
        @row-click="handleRowClick"
        highlight-current-row
        :row-class-name="getRowClass"
      >
        <el-table-column prop="id" label="订单号" width="160" fixed="left">
          <template slot-scope="scope">
            <div class="order-id-wrapper">
              <span class="order-id">{{ scope.row.id }}</span>
              <el-badge
                v-if="isNewOrder(scope.row)"
                class="new-order-badge"
                value="NEW"
                type="success"
                :hidden="!isNewOrder(scope.row)"
              >
              </el-badge>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="customerName" label="客户" width="100">
          <template slot-scope="scope">
            <el-tag type="info" size="small">{{ scope.row.customerName }}</el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="phone" label="联系电话" width="130"></el-table-column>

        <el-table-column label="定制信息" min-width="320">
          <template slot-scope="scope">
            <div class="order-detail">
              <div class="detail-item">
                <span class="detail-label">泥料：</span>
                <span class="detail-value">{{ scope.row.clayType }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">尺寸：</span>
                <span class="detail-value">{{ scope.row.size }}cm</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">釉色：</span>
                <span class="detail-value">{{ scope.row.glazeStyle }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">纹饰：</span>
                <span class="detail-value">{{ scope.row.pattern }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">器型：</span>
                <span class="detail-value">{{ scope.row.shape }}</span>
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="price" label="价格" width="100" align="right">
          <template slot-scope="scope">
            <span class="price">¥{{ scope.row.price }}</span>
          </template>
        </el-table-column>

        <el-table-column label="生产进度" width="280">
          <template slot-scope="scope">
            <span :class="getStatusClass(scope.row.currentStep)">
              {{ getStatusText(scope.row.currentStep) }}
            </span>
            <el-progress
              :percentage="Math.round((scope.row.currentStep / 7) * 100)"
              :status="getProgressStatus(scope.row.currentStep)"
              :stroke-width="8"
              style="margin-top: 8px"
            ></el-progress>
          </template>
        </el-table-column>

        <el-table-column prop="createTime" label="下单时间" width="160"></el-table-column>

        <el-table-column label="操作" width="160" fixed="right">
          <template slot-scope="scope">
            <el-button
              type="primary"
              size="small"
              icon="el-icon-s-operation"
              @click.stop="openProcessDialog(scope.row)"
            >
              工序管理
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="table-footer">
        <span class="order-count">共 {{ filteredOrders.length }} 条订单记录</span>
      </div>
    </el-card>

    <el-dialog
      title="订单详情与工序管理"
      :visible.sync="processDialogVisible"
      width="900px"
      :close-on-click-modal="false"
    >
      <div v-if="currentOrder" class="dialog-content">
        <el-descriptions :column="2" border size="small">
          <el-descriptions-item label="订单号">
            <span class="highlight-text">{{ currentOrder.id }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="客户姓名">
            {{ currentOrder.customerName }}
          </el-descriptions-item>
          <el-descriptions-item label="联系电话">
            {{ currentOrder.phone }}
          </el-descriptions-item>
          <el-descriptions-item label="下单时间">
            {{ currentOrder.createTime }}
          </el-descriptions-item>
          <el-descriptions-item label="泥料类型">
            {{ currentOrder.clayType }}
          </el-descriptions-item>
          <el-descriptions-item label="盏径尺寸">
            {{ currentOrder.size }} cm
          </el-descriptions-item>
          <el-descriptions-item label="釉色风格">
            {{ currentOrder.glazeStyle }}
          </el-descriptions-item>
          <el-descriptions-item label="器型款式">
            {{ currentOrder.shape }}
          </el-descriptions-item>
          <el-descriptions-item label="纹饰绘制" :span="2">
            {{ currentOrder.pattern }}
          </el-descriptions-item>
          <el-descriptions-item label="特殊要求" :span="2">
            {{ currentOrder.remark || '无' }}
          </el-descriptions-item>
          <el-descriptions-item label="订单价格">
            <span class="price-highlight">¥ {{ currentOrder.price }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="当前状态">
            <span :class="getStatusClass(currentOrder.currentStep)">
              {{ getStatusText(currentOrder.currentStep) }}
            </span>
          </el-descriptions-item>
        </el-descriptions>

        <el-divider content-position="left">
          <i class="el-icon-time"></i> 生产工序流程
        </el-divider>

        <el-steps
          :active="currentOrder.currentStep"
          finish-status="success"
          process-status="process"
          align-center
          class="process-steps"
        >
          <el-step
            v-for="step in processSteps"
            :key="step.id"
            :title="step.name"
            :icon="step.icon"
          >
            <template slot="description" v-if="currentOrder.stepTimes && currentOrder.stepTimes[step.id]">
              <span class="step-time">{{ currentOrder.stepTimes[step.id] }}</span>
            </template>
          </el-step>
        </el-steps>

        <div class="step-actions">
          <el-alert
            title="生产工序按顺序推进，不可逆向回退"
            type="warning"
            :closable="false"
            show-icon
            class="step-warning"
          />
          <div class="action-buttons">
            <el-button
              type="primary"
              size="large"
              :disabled="currentOrder.currentStep >= 7"
              @click="advanceStep"
              icon="el-icon-arrow-right"
            >
              {{ currentOrder.currentStep >= 7 ? '已全部完成' : '推进到下一工序' }}
            </el-button>
            <el-button
              type="success"
              size="large"
              :disabled="currentOrder.currentStep >= 7"
              @click="completeAll"
              icon="el-icon-check"
            >
              标记完工
            </el-button>
          </div>
        </div>
      </div>

      <div slot="footer" class="dialog-footer">
        <el-button @click="processDialogVisible = false">关闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { PROCESS_STEPS, orderStore } from '../store/orderStore'
import { EventBus } from '../store/eventBus'

export default {
  name: 'AdminPage',
  data() {
    return {
      processSteps: PROCESS_STEPS,
      orders: [],
      searchKeyword: '',
      searchType: 'all',
      filterStatus: '',
      processDialogVisible: false,
      currentOrder: null,
      highlightOrderId: null
    }
  },
  computed: {
    searchPlaceholder() {
      if (this.searchType === 'id') return '请输入订单号，如：ORD2024'
      if (this.searchType === 'customer') return '请输入客户姓名'
      return '搜索订单号或客户名'
    },
    filteredOrders() {
      let result = [...this.orders]

      if (this.searchKeyword) {
        const keyword = this.searchKeyword.toLowerCase()
        if (this.searchType === 'id') {
          result = result.filter(o => o.id.toLowerCase().includes(keyword))
        } else if (this.searchType === 'customer') {
          result = result.filter(o => o.customerName.includes(keyword))
        } else {
          result = result.filter(
            o => o.id.toLowerCase().includes(keyword) ||
                 o.customerName.includes(keyword)
          )
        }
      }

      if (this.filterStatus !== '') {
        if (this.filterStatus === 'processing') {
          result = result.filter(o => o.currentStep > 0 && o.currentStep < 7)
        } else {
          result = result.filter(o => o.currentStep === parseInt(this.filterStatus))
        }
      }

      return result
    }
  },
  created() {
    this.refreshOrders()
    EventBus.$on('orderCreated', (newOrder) => {
      this.refreshOrders()
      this.highlightOrderId = newOrder.id
      this.$message.success(`收到新订单：${newOrder.id}，已自动刷新列表`)
      setTimeout(() => {
        const table = this.$el.querySelector('.el-table__body-wrapper')
        if (table) {
          table.scrollTop = 0
        }
      }, 100)
      setTimeout(() => {
        this.highlightOrderId = null
      }, 5000)
    })
  },
  beforeDestroy() {
    EventBus.$off('orderCreated')
  },
  methods: {
    refreshOrders() {
      this.orders = orderStore.getOrders()
    },
    handleSearch() {
    },
    handleRowClick(row) {
      this.openProcessDialog(row)
    },
    openProcessDialog(order) {
      this.currentOrder = { ...order }
      this.processDialogVisible = true
    },
    isNewOrder(order) {
      if (!order.createTime) return false
      const createTime = new Date(order.createTime.replace(/-/g, '/'))
      const now = new Date()
      const diffMs = now - createTime
      const diffHours = diffMs / (1000 * 60 * 60)
      return diffHours <= 24
    },
    getRowClass(row) {
      if (row.id === this.highlightOrderId) return 'highlight-row'
      if (this.isNewOrder(row)) return 'new-order-row'
      return ''
    },
    getStatusClass(step) {
      if (step === 0) return 'status-badge status-pending'
      if (step >= 7) return 'status-badge status-completed'
      return 'status-badge status-processing'
    },
    getStatusText(step) {
      if (step === 0) return '待生产'
      if (step >= 7) return '已完工'
      return `生产中：${this.processSteps[step].name}`
    },
    getProgressStatus(step) {
      if (step >= 7) return 'success'
      if (step > 0) return ''
      return 'exception'
    },
    advanceStep() {
      if (this.currentOrder.currentStep < 7) {
        const nextStep = this.currentOrder.currentStep + 1
        const result = orderStore.updateStep(this.currentOrder.id, nextStep)
        if (result.success) {
          const updatedOrder = this.orders.find(o => o.id === this.currentOrder.id)
          this.currentOrder = { ...updatedOrder }
          this.refreshOrders()
          if (nextStep >= 7) {
            this.$message.success('订单已全部完工！')
          } else {
            this.$message.success(`已推进到「${this.processSteps[nextStep].name}」工序，操作时间已记录`)
          }
        } else {
          this.$message.error(result.message)
        }
      }
    },
    completeAll() {
      this.$confirm('确定要标记此订单为全部完工吗？', '确认完工', {
        confirmButtonText: '确定完工',
        cancelButtonText: '取消',
        type: 'success'
      }).then(() => {
        const result = orderStore.updateStep(this.currentOrder.id, 7)
        if (result.success) {
          const updatedOrder = this.orders.find(o => o.id === this.currentOrder.id)
          this.currentOrder = { ...updatedOrder }
          this.refreshOrders()
          this.$message.success('订单已标记为完工！各工序操作时间已记录')
        } else {
          this.$message.error(result.message)
        }
      }).catch(() => {})
    }
  }
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
  color: #5D4037;
}

.header-right {
  display: flex;
  align-items: center;
}

.order-id {
  font-family: 'Courier New', monospace;
  font-weight: bold;
  color: #5D4037;
}

.order-detail {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 20px;
}

.detail-item {
  display: flex;
  align-items: center;
  font-size: 13px;
}

.detail-label {
  color: #8D6E63;
}

.detail-value {
  color: #3E2723;
  font-weight: 500;
}

.price {
  color: #E65100;
  font-weight: bold;
  font-size: 15px;
}

.table-footer {
  margin-top: 16px;
  text-align: right;
  color: #8D6E63;
  font-size: 14px;
}

.order-count {
  font-weight: 500;
}

.dialog-content {
  padding: 10px 0;
}

.highlight-text {
  font-family: 'Courier New', monospace;
  font-weight: bold;
  color: #5D4037;
}

.price-highlight {
  color: #E65100;
  font-weight: bold;
  font-size: 18px;
}

.process-steps {
  margin: 30px 0;
}

.process-steps >>> .el-step__icon {
  font-size: 18px;
}

.process-steps >>> .el-step__title.is-process {
  color: #5D4037;
  font-weight: bold;
}

.process-steps >>> .el-step__title.is-finish {
  color: #2E7D32;
  font-weight: bold;
}

.process-steps >>> .el-step__description {
  margin-top: 4px;
}

.step-time {
  font-size: 12px;
  color: #8D6E63;
  font-family: 'Courier New', monospace;
}

.step-warning {
  margin-bottom: 20px;
}

.step-actions {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  margin-top: 20px;
}

.action-buttons {
  display: flex;
  gap: 16px;
}

.dialog-footer {
  text-align: center;
}

.order-id-wrapper {
  display: flex;
  align-items: center;
  position: relative;
}

.new-order-badge {
  margin-left: 8px;
}

::v-deep .highlight-row {
  background-color: #FFF9C4 !important;
  animation: highlightPulse 2s ease-in-out infinite;
}

::v-deep .new-order-row {
  background-color: #E8F5E9 !important;
}

::v-deep .new-order-row:hover > td {
  background-color: #C8E6C9 !important;
}

@keyframes highlightPulse {
  0%, 100% {
    background-color: #FFF9C4;
  }
  50% {
    background-color: #FFF59D;
  }
}
</style>
