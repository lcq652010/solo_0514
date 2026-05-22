<template>
  <div class="admin-page">
    <h2 class="page-title">订单管理中心</h2>

    <el-card class="filter-card">
      <div class="filter-section">
        <el-select v-model="statusFilter" placeholder="订单状态" style="width: 150px;">
          <el-option label="全部" value="" />
          <el-option label="待生产" value="pending" />
          <el-option label="生产中" value="processing" />
          <el-option label="已完工" value="completed" />
        </el-select>
        <el-input
          v-model="searchKeyword"
          placeholder="搜索订单号/客户姓名"
          style="width: 250px; margin-left: 16px;"
          clearable
        />
        <el-button type="primary" style="margin-left: 16px;" @click="loadOrders">
          <i class="el-icon-refresh"></i> 刷新
        </el-button>
        <el-button style="margin-left: 16px;" @click="initMockData" :disabled="hasData">
          <i class="el-icon-document-add"></i> 初始化示例数据
        </el-button>
      </div>
      <div class="stats-section">
        <div class="stat-item">
          <span class="stat-label">总订单</span>
          <span class="stat-value total">{{ orders.length }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">待生产</span>
          <span class="stat-value pending">{{ pendingCount }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">生产中</span>
          <span class="stat-value processing">{{ processingCount }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">已完工</span>
          <span class="stat-value completed">{{ completedCount }}</span>
        </div>
      </div>
    </el-card>

    <el-table
      :data="filteredOrders"
      style="width: 100%;"
      v-loading="loading"
      :row-key="row => row.id"
      :row-class-name="tableRowClassName"
      class="order-table"
    >
      <el-table-column prop="orderNo" label="订单编号" width="180">
        <template slot-scope="scope">
          <div class="order-no-cell">
            <span>{{ scope.row.orderNo }}</span>
            <el-tag
              v-if="isNewOrder(scope.row)"
              type="danger"
              size="mini"
              effect="light"
              class="new-tag"
            >
              新订单
            </el-tag>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="customerName" label="客户姓名" width="100" />
      <el-table-column prop="customerPhone" label="联系电话" width="130" />
      <el-table-column label="定制信息" min-width="280">
        <template slot-scope="scope">
          <div class="order-detail">
            <p><span>材质：</span>{{ scope.row.materialLabel }}</p>
            <p><span>尺寸：</span>{{ scope.row.sizeWidth }} × {{ scope.row.sizeHeight }} cm</p>
            <p><span>纹样：</span>{{ scope.row.patternLabel }}</p>
            <p><span>密度：</span>{{ scope.row.densityLabel }}</p>
            <p><span>包边：</span>{{ scope.row.edgeTypeLabel }}</p>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="price" label="金额" width="100">
        <template slot-scope="scope">
          <span class="price-text">¥{{ scope.row.price }}</span>
        </template>
      </el-table-column>
      <el-table-column label="状态" width="100">
        <template slot-scope="scope">
          <el-tag :type="getStatusType(scope.row.status)" size="small">
            {{ getStatusText(scope.row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="createTime" label="创建时间" width="160">
        <template slot-scope="scope">
          {{ formatTime(scope.row.createTime) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="140" fixed="right">
        <template slot-scope="scope">
          <el-button
            type="primary"
            size="small"
            icon="el-icon-view"
            @click="viewDetail(scope.row)"
          >
            查看详情
          </el-button>
        </template>
      </el-table-column>
      <el-table-column type="expand">
        <template slot-scope="props">
          <div class="expand-content">
            <div class="expand-header">
              <h4>生产工序进度</h4>
              <el-progress
                :percentage="Math.round((props.row.currentStep + (props.row.status === 'completed' ? 1 : 0)) / 8 * 100)"
                :status="props.row.status === 'completed' ? 'success' : ''"
                style="width: 300px;"
              />
            </div>
            <el-steps :active="props.row.currentStep" finish-status="success" class="process-steps">
              <el-step
                v-for="(step, index) in props.row.steps"
                :key="index"
                :title="step.name"
                :icon="step.completed ? 'el-icon-circle-check' : ''"
              />
            </el-steps>
            <div class="step-times">
              <div
                v-for="(step, index) in props.row.steps"
                :key="index"
                class="step-time-item"
                :class="{ completed: step.completed }"
              >
                <span>{{ step.name }}：</span>
                <span>{{ step.completed ? formatTime(step.time) : '未开始' }}</span>
              </div>
            </div>
            <div class="remark-section">
              <span>备注：</span>
              <span>{{ props.row.remark || '无' }}</span>
            </div>
          </div>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-if="filteredOrders.length > 0"
      class="pagination"
      background
      layout="total, prev, pager, next, jumper"
      :total="filteredOrders.length"
      :page-size="10"
      :current-page.sync="currentPage"
    />

    <el-dialog
      title="订单详情"
      :visible.sync="detailVisible"
      width="800px"
      :close-on-click-modal="false"
    >
      <div v-if="currentOrder" class="detail-content">
        <el-descriptions :column="2" border class="detail-desc">
          <el-descriptions-item label="订单编号">{{ currentOrder.orderNo }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ formatTime(currentOrder.createTime) }}</el-descriptions-item>
          <el-descriptions-item label="客户姓名">{{ currentOrder.customerName }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ currentOrder.customerPhone }}</el-descriptions-item>
          <el-descriptions-item label="订单状态">
            <el-tag :type="getStatusType(currentOrder.status)" size="small">
              {{ getStatusText(currentOrder.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="订单金额">
            <span class="price-text">¥{{ currentOrder.price }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="丝线材质">{{ currentOrder.materialLabel }}</el-descriptions-item>
          <el-descriptions-item label="扇面尺寸">{{ currentOrder.sizeWidth }} × {{ currentOrder.sizeHeight }} cm</el-descriptions-item>
          <el-descriptions-item label="纹样题材">{{ currentOrder.patternLabel }}</el-descriptions-item>
          <el-descriptions-item label="织造密度">{{ currentOrder.densityLabel }}</el-descriptions-item>
          <el-descriptions-item label="包边方式">{{ currentOrder.edgeTypeLabel }}</el-descriptions-item>
          <el-descriptions-item label="备注说明">{{ currentOrder.remark || '无' }}</el-descriptions-item>
        </el-descriptions>

        <div class="process-section">
          <h4>生产工序管理</h4>
          <div class="process-progress">
            <span>当前进度：</span>
            <el-progress
              :percentage="Math.round((currentOrder.currentStep + (currentOrder.status === 'completed' ? 1 : 0)) / 8 * 100)"
              :status="currentOrder.status === 'completed' ? 'success' : ''"
              style="flex: 1; margin: 0 16px;"
            />
            <span>{{ getCurrentStepText(currentOrder) }}</span>
          </div>
          <el-steps
            :active="currentOrder.currentStep"
            finish-status="success"
            direction="vertical"
            class="vertical-steps"
          >
            <el-step
              v-for="(step, index) in currentOrder.steps"
              :key="index"
              :title="step.name"
              :description="step.completed ? formatTime(step.time) : '未开始'"
              :icon="step.completed ? 'el-icon-circle-check' : ''"
            >
              <div v-if="canUpdateStep(currentOrder, index)" slot="custom" class="step-action">
                <el-button
                  type="primary"
                  size="small"
                  :icon="step.completed ? 'el-icon-refresh-left' : 'el-icon-check'"
                  @click="updateStep(index)"
                >
                  {{ step.completed ? '撤销' : '完成' }}
                </el-button>
              </div>
            </el-step>
          </el-steps>
        </div>
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button @click="detailVisible = false">关闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mockOrders } from '../mock/data'
import { getOrders, saveOrders, updateOrder, formatTime, getStatusText, getStatusType } from '../utils/storage'

export default {
  name: 'AdminPage',
  data() {
    return {
      orders: [],
      loading: false,
      statusFilter: '',
      searchKeyword: '',
      currentPage: 1,
      detailVisible: false,
      currentOrder: null,
      highlightTimer: null
    }
  },
  computed: {
    filteredOrders() {
      let result = [...this.orders]
      if (this.statusFilter) {
        result = result.filter(o => o.status === this.statusFilter)
      }
      if (this.searchKeyword) {
        const keyword = this.searchKeyword.toLowerCase()
        result = result.filter(o =>
          o.orderNo.toLowerCase().includes(keyword) ||
          o.customerName.toLowerCase().includes(keyword)
        )
      }
      return result
    },
    pendingCount() {
      return this.orders.filter(o => o.status === 'pending').length
    },
    processingCount() {
      return this.orders.filter(o => o.status === 'processing').length
    },
    completedCount() {
      return this.orders.filter(o => o.status === 'completed').length
    },
    hasData() {
      return this.orders.length > 0
    }
  },
  created() {
    this.loadOrders()
    this.checkScrollTo()
  },
  mounted() {
    this.startHighlightTimer()
  },
  beforeDestroy() {
    if (this.highlightTimer) {
      clearInterval(this.highlightTimer)
    }
  },
  watch: {
    '$route.query': {
      handler() {
        this.checkScrollTo()
      },
      immediate: false
    }
  },
  methods: {
    loadOrders() {
      this.loading = true
      setTimeout(() => {
        this.orders = getOrders()
        this.loading = false
      }, 300)
    },
    initMockData() {
      this.$confirm('确定要初始化示例数据吗？这将覆盖现有数据。', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        saveOrders(mockOrders)
        this.loadOrders()
        this.$message.success('示例数据初始化成功！')
      }).catch(() => {})
    },
    viewDetail(row) {
      this.currentOrder = JSON.parse(JSON.stringify(row))
      this.detailVisible = true
    },
    canUpdateStep(order, stepIndex) {
      if (order.status === 'completed') {
        return stepIndex === 7
      }
      if (stepIndex === 0) {
        return true
      }
      return order.steps[stepIndex - 1].completed
    },
    getCurrentStepText(order) {
      if (order.status === 'completed') {
        return '已全部完成'
      }
      if (order.status === 'pending') {
        return '待开始'
      }
      return `当前：${order.steps[order.currentStep].name}`
    },
    updateStep(stepIndex) {
      if (!this.currentOrder) return

      const step = this.currentOrder.steps[stepIndex]
      const wasCompleted = step.completed
      const actionText = wasCompleted ? '撤销' : '完成'

      this.$confirm(
        `确定要${actionText}「${step.name}」工序吗？`,
        '操作确认',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(() => {
        if (wasCompleted) {
          step.completed = false
          step.time = null
          if (stepIndex === 7) {
            this.currentOrder.status = 'processing'
          }
          if (stepIndex < this.currentOrder.currentStep) {
            this.currentOrder.currentStep = stepIndex
          }
        } else {
          step.completed = true
          step.time = Date.now()
          if (stepIndex === this.currentOrder.currentStep) {
            this.currentOrder.currentStep = Math.min(stepIndex + 1, 7)
          }
          if (this.currentOrder.currentStep === 0 && this.currentOrder.steps[0].completed) {
            this.currentOrder.status = 'processing'
          }
          if (stepIndex === 7) {
            this.currentOrder.status = 'completed'
          }
        }

        const allCompleted = this.currentOrder.steps.every(s => s.completed)
        if (allCompleted) {
          this.currentOrder.status = 'completed'
          this.currentOrder.currentStep = 7
        } else if (this.currentOrder.steps.some(s => s.completed)) {
          this.currentOrder.status = 'processing'
        } else {
          this.currentOrder.status = 'pending'
          this.currentOrder.currentStep = 0
        }

        updateOrder(this.currentOrder.id, {
          steps: this.currentOrder.steps,
          currentStep: this.currentOrder.currentStep,
          status: this.currentOrder.status
        })

        this.loadOrders()
        this.$message.success(wasCompleted ? '已撤销该工序' : '工序已完成！')
      }).catch(() => {})
    },
    checkScrollTo() {
      if (this.$route.query.scrollTo === 'list') {
        this.$nextTick(() => {
          const tableEl = document.querySelector('.order-table')
          if (tableEl) {
            tableEl.scrollIntoView({ behavior: 'smooth', block: 'start' })
          }
          this.$router.replace({ query: {} })
        })
      }
    },
    isNewOrder(order) {
      const twelveHours = 12 * 60 * 60 * 1000
      return Date.now() - order.createTime < twelveHours
    },
    tableRowClassName({ row }) {
      if (this.isNewOrder(row)) {
        return 'new-order-row'
      }
      return ''
    },
    startHighlightTimer() {
      this.highlightTimer = setInterval(() => {
        this.$forceUpdate()
      }, 60000)
    },
    formatTime,
    getStatusText,
    getStatusType
  }
}
</script>

<style scoped>
.admin-page {
  max-width: 1400px;
  margin: 0 auto;
}

.filter-card {
  margin-bottom: 20px;
}

.filter-section {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 16px;
}

.stats-section {
  display: flex;
  gap: 40px;
  padding-top: 16px;
  border-top: 1px solid var(--border-color);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.stat-label {
  font-size: 14px;
  color: var(--text-secondary);
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
}

.stat-value.total {
  color: var(--primary-dark);
}

.stat-value.pending {
  color: #E6A23C;
}

.stat-value.processing {
  color: var(--primary-color);
}

.stat-value.completed {
  color: #67C23A;
}

.order-table {
  margin-bottom: 20px;
}

.order-no-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.new-tag {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

::v-deep .el-table .new-order-row {
  background-color: #FFF0F0 !important;
}

::v-deep .el-table .new-order-row:hover > td {
  background-color: #FFE8E8 !important;
}

.order-detail {
  font-size: 13px;
  line-height: 1.8;
}

.order-detail p {
  margin: 0;
}

.order-detail span:first-child {
  color: var(--text-secondary);
}

.price-text {
  color: var(--primary-color);
  font-weight: bold;
  font-size: 16px;
}

.expand-content {
  padding: 10px 20px;
}

.expand-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.expand-header h4 {
  margin: 0;
  color: var(--primary-dark);
}

.process-steps {
  margin-bottom: 20px;
}

.step-times {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-bottom: 16px;
  font-size: 12px;
}

.step-time-item {
  padding: 8px;
  background-color: var(--bg-color);
  border-radius: 4px;
  color: var(--text-secondary);
}

.step-time-item.completed {
  background-color: #F0F9EB;
  color: #67C23A;
}

.remark-section {
  padding: 12px;
  background-color: var(--bg-color);
  border-radius: 4px;
  font-size: 13px;
}

.remark-section span:first-child {
  color: var(--text-secondary);
}

.pagination {
  display: flex;
  justify-content: center;
  padding: 20px 0;
}

.detail-content {
  padding: 10px 0;
}

.detail-desc {
  margin-bottom: 24px;
}

.process-section h4 {
  margin: 0 0 16px 0;
  color: var(--primary-dark);
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border-color);
}

.process-progress {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.process-progress span:first-child {
  color: var(--text-secondary);
  white-space: nowrap;
}

.process-progress span:last-child {
  color: var(--primary-color);
  font-weight: 500;
  white-space: nowrap;
}

.vertical-steps {
  padding: 0 20px;
}

::v-deep .el-step.is-vertical {
  padding-bottom: 20px;
}

::v-deep .el-step.is-vertical:last-child {
  padding-bottom: 0;
}

.step-action {
  padding: 8px 0;
}

.dialog-footer {
  text-align: center;
}
</style>
