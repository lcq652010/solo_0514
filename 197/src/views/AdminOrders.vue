<template>
  <div class="admin-page">
    <div class="admin-header">
      <div class="logo">
        <i class="el-icon-menu"></i> 宣纸笺定制管理系统
      </div>
      <div class="user-info">
        <span class="username">
          <i class="el-icon-user"></i> {{ adminInfo ? adminInfo.username : '管理员' }}
        </span>
        <el-button class="logout-btn" type="text" @click="handleLogout">
          退出登录
        </el-button>
      </div>
    </div>

    <div class="admin-content">
      <div class="page-title-section">
        <h2>订单管理</h2>
        <div class="filter-bar">
          <el-radio-group v-model="filterStatus" size="small" @change="handleFilterChange">
            <el-radio-button label="all">全部订单</el-radio-button>
            <el-radio-button label="pending">待处理</el-radio-button>
            <el-radio-button label="processing">生产中</el-radio-button>
            <el-radio-button label="completed">已完成</el-radio-button>
          </el-radio-group>
          <el-button
            :type="sortOrder === 'desc' ? 'primary' : 'default'"
            size="small"
            @click="toggleSort"
            class="sort-btn"
          >
            <i :class="sortOrder === 'desc' ? 'el-icon-arrow-down' : 'el-icon-arrow-up'"></i>
            {{ sortOrder === 'desc' ? '最新优先' : '最早优先' }}
          </el-button>
          <el-button type="primary" size="small" @click="refreshOrders">
            <i class="el-icon-refresh"></i> 刷新
          </el-button>
        </div>
      </div>

      <div class="new-orders-section card" v-if="pinnedOrders.length > 0">
        <div class="section-header">
          <span class="new-badge">
            <i class="el-icon-bell"></i> 新订单
            <span class="badge-count">{{ pinnedOrders.length }}</span>
          </span>
          <el-button type="text" size="mini" @click="clearAllNewFlags">
            <i class="el-icon-check"></i> 全部标记为已读
          </el-button>
        </div>
        <div class="new-orders-list">
          <div
            v-for="order in pinnedOrders"
            :key="order.id"
            class="new-order-item"
            @click="goToOrder(order)"
          >
            <div class="order-main">
              <span class="order-id">
                <i class="el-icon-star-on"></i>
                {{ order.id }}
              </span>
              <span class="order-customer">{{ order.customerName }}</span>
              <span class="order-product">{{ order.category }} · {{ order.curtainPattern }}</span>
              <span class="order-size">{{ order.size.width }}×{{ order.size.height }}cm · {{ order.quantity }}张</span>
            </div>
            <div class="order-meta">
              <el-tag :type="getStatusType(order.status)" size="mini">
                {{ getStatusText(order.status) }}
              </el-tag>
              <span class="order-time">{{ order.createdAt }}</span>
            </div>
            <el-button type="text" size="mini" class="read-btn" @click.stop="clearNewFlag(order)">
              标为已读
            </el-button>
          </div>
        </div>
      </div>

      <div class="stats-card card">
        <el-row :gutter="20">
          <el-col :span="6">
            <div class="stat-item">
              <div class="stat-value all">{{ orders.length }}</div>
              <div class="stat-label">全部订单</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-item">
              <div class="stat-value pending">{{ pendingCount }}</div>
              <div class="stat-label">待处理</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-item">
              <div class="stat-value processing">{{ processingCount }}</div>
              <div class="stat-label">生产中</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-item">
              <div class="stat-value completed">{{ completedCount }}</div>
              <div class="stat-label">已完成</div>
            </div>
          </el-col>
        </el-row>
      </div>

      <div class="order-list card">
        <div class="table-header">
          <h3>全部订单</h3>
        </div>
        <el-table
          :data="filteredOrders"
          style="width: 100%"
          v-loading="loading"
          :row-class-name="getRowClassName"
          :expand-row-keys="expandRowKeys"
          @expand-change="handleExpandChange"
        >
          <el-table-column type="expand">
            <template slot-scope="props">
              <div class="order-detail">
                <el-row :gutter="20">
                  <el-col :span="8">
                    <div class="detail-block">
                      <h4>客户信息</h4>
                      <p><span>姓名：</span>{{ props.row.customerName }}</p>
                      <p><span>电话：</span>{{ props.row.customerPhone }}</p>
                      <p><span>下单时间：</span>{{ props.row.createdAt }}</p>
                    </div>
                  </el-col>
                  <el-col :span="8">
                    <div class="detail-block">
                      <h4>产品信息</h4>
                      <p><span>品类：</span>{{ props.row.category }}</p>
                      <p><span>尺寸：</span>{{ props.row.size.width }}cm × {{ props.row.size.height }}cm</p>
                      <p><span>帘纹：</span>{{ props.row.curtainPattern }}</p>
                      <p><span>数量：</span>{{ props.row.quantity }}张</p>
                    </div>
                  </el-col>
                  <el-col :span="8">
                    <div class="detail-block">
                      <h4>工艺与包装</h4>
                      <p>
                        <span>描金：</span>
                        <span v-if="props.row.goldProcesses.length > 0">
                          {{ props.row.goldProcesses.join('、') }}
                        </span>
                        <span v-else>无</span>
                      </p>
                      <p><span>包装：</span>{{ props.row.packaging }}</p>
                      <p v-if="props.row.remark"><span>备注：</span>{{ props.row.remark }}</p>
                    </div>
                  </el-col>
                </el-row>

                <div class="process-section">
                  <h4>生产工序进度时间线</h4>
                  <div class="process-timeline">
                    <div
                      v-for="(step, index) in props.row.steps"
                      :key="index"
                      class="timeline-item"
                      :class="{
                        'is-completed': step.completed,
                        'is-current': index === props.row.currentStep && !step.completed,
                        'is-pending': index > props.row.currentStep
                      }"
                    >
                      <div class="timeline-dot">
                        <i v-if="step.completed" class="el-icon-check"></i>
                        <span v-else>{{ index + 1 }}</span>
                      </div>
                      <div class="timeline-content">
                        <div class="timeline-header">
                          <span class="step-name">{{ step.name }}</span>
                          <el-tag
                            v-if="step.completed"
                            type="success"
                            size="mini"
                            effect="dark"
                          >
                            已完成
                          </el-tag>
                          <el-tag
                            v-else-if="index === props.row.currentStep"
                            type="warning"
                            size="mini"
                            effect="dark"
                          >
                            进行中
                          </el-tag>
                          <el-tag
                            v-else
                            type="info"
                            size="mini"
                          >
                            待处理
                          </el-tag>
                        </div>
                        <div class="timeline-time" v-if="step.time">
                          <i class="el-icon-time"></i> {{ step.time }}
                        </div>
                        <div class="timeline-time" v-else>
                          <i class="el-icon-clock"></i> 预计处理
                        </div>
                      </div>
                      <div
                        v-if="index < props.row.steps.length - 1"
                        class="timeline-connector"
                        :class="{ 'is-done': step.completed }"
                      ></div>
                    </div>
                  </div>

                  <div class="process-actions">
                    <template v-if="props.row.status !== 'completed'">
                      <el-button
                        v-if="props.row.currentStep < 8"
                        type="primary"
                        size="small"
                        @click="completeStep(props.row)"
                      >
                        <i class="el-icon-check"></i>
                        完成「{{ getCurrentStepName(props.row) }}」工序
                      </el-button>
                      <el-button
                        type="warning"
                        size="small"
                        @click="showResetConfirm(props.row)"
                        :disabled="props.row.currentStep === 0"
                      >
                        <i class="el-icon-refresh-left"></i> 重置工序
                      </el-button>
                    </template>
                    <el-tag v-else type="success" size="large">
                      <i class="el-icon-circle-check"></i> 订单已完成
                    </el-tag>
                  </div>
                </div>
              </div>
            </template>
          </el-table-column>

          <el-table-column prop="id" label="订单编号" width="180">
            <template slot-scope="scope">
              <span class="order-id">{{ scope.row.id }}</span>
            </template>
          </el-table-column>

          <el-table-column prop="customerName" label="客户" width="100"></el-table-column>

          <el-table-column label="产品信息" min-width="200">
            <template slot-scope="scope">
              <div class="product-info">
                <p>{{ scope.row.category }} · {{ scope.row.curtainPattern }}</p>
                <p class="sub-info">
                  {{ scope.row.size.width }}×{{ scope.row.size.height }}cm · {{ scope.row.quantity }}张
                </p>
              </div>
            </template>
          </el-table-column>

          <el-table-column label="工艺包装" min-width="150">
            <template slot-scope="scope">
              <div class="process-info">
                <p v-if="scope.row.goldProcesses.length > 0">
                  <el-tag size="mini" type="warning" effect="plain">
                    {{ scope.row.goldProcesses.join('、') }}
                  </el-tag>
                </p>
                <p class="sub-info">{{ scope.row.packaging }}</p>
              </div>
            </template>
          </el-table-column>

          <el-table-column prop="status" label="状态" width="100">
            <template slot-scope="scope">
              <el-tag :type="getStatusType(scope.row.status)" size="small">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>

          <el-table-column label="工序进度" width="120">
            <template slot-scope="scope">
              <el-progress
                :percentage="Math.round(scope.row.currentStep / 8 * 100)"
                :show-text="false"
                :stroke-width="8"
                color="#C41E3A"
              ></el-progress>
              <span class="progress-text">{{ scope.row.currentStep }}/8</span>
            </template>
          </el-table-column>

          <el-table-column prop="createdAt" label="下单时间" width="160"></el-table-column>

          <el-table-column label="操作" width="120" fixed="right">
            <template slot-scope="scope">
              <el-button
                type="text"
                size="small"
                @click="toggleExpand(scope.row)"
              >
                {{ isExpanded(scope.row) ? '收起' : '详情' }}
              </el-button>
              <el-button
                v-if="scope.row.status !== 'completed'"
                type="text"
                size="small"
                @click="showDeleteConfirm(scope.row)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <div v-if="filteredOrders.length === 0" class="empty-state">
          <i class="el-icon-document"></i>
          <p>暂无订单数据</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getOrders, updateOrder, logout, isLoggedIn, getCurrentAdmin, formatDateTime } from '@/utils/storage.js'

export default {
  name: 'AdminOrders',
  data() {
    return {
      orders: [],
      loading: false,
      filterStatus: 'all',
      expandRowKeys: [],
      adminInfo: null,
      sortOrder: 'desc',
      newOrderIds: []
    }
  },
  computed: {
    sortedOrders() {
      const sorted = [...this.orders].sort((a, b) => {
        const timeA = new Date(a.createdAt).getTime()
        const timeB = new Date(b.createdAt).getTime()
        return this.sortOrder === 'desc' ? timeB - timeA : timeA - timeB
      })
      return sorted
    },
    filteredOrders() {
      let orders = this.sortedOrders.filter(o => !this.newOrderIds.includes(o.id))
      if (this.filterStatus !== 'all') {
        orders = orders.filter(o => o.status === this.filterStatus)
      }
      return orders
    },
    pinnedOrders() {
      return this.sortedOrders.filter(o => this.newOrderIds.includes(o.id))
    },
    pendingCount() {
      return this.orders.filter(o => o.status === 'pending').length
    },
    processingCount() {
      return this.orders.filter(o => o.status === 'processing').length
    },
    completedCount() {
      return this.orders.filter(o => o.status === 'completed').length
    }
  },
  created() {
    if (!isLoggedIn()) {
      this.$router.replace('/admin/login')
      return
    }
    this.adminInfo = getCurrentAdmin()
    this.loadNewOrderIds()
    this.loadOrders()
  },
  methods: {
    loadOrders() {
      this.loading = true
      setTimeout(() => {
        this.orders = getOrders()
        this.checkNewOrders()
        this.loading = false
      }, 300)
    },
    refreshOrders() {
      this.loadOrders()
      this.$message.success('刷新成功')
    },
    handleFilterChange() {
      this.expandRowKeys = []
    },
    toggleExpand(row) {
      const index = this.expandRowKeys.indexOf(row.id)
      if (index > -1) {
        this.expandRowKeys.splice(index, 1)
      } else {
        this.expandRowKeys.push(row.id)
      }
    },
    isExpanded(row) {
      return this.expandRowKeys.indexOf(row.id) > -1
    },
    handleExpandChange(row, expandedRows) {
      this.expandRowKeys = expandedRows.map(r => r.id)
    },
    toggleSort() {
      this.sortOrder = this.sortOrder === 'desc' ? 'asc' : 'desc'
    },
    getRowClassName({ row }) {
      if (this.newOrderIds.includes(row.id)) {
        return 'new-order-row'
      }
      return ''
    },
    clearNewFlag(order) {
      const index = this.newOrderIds.indexOf(order.id)
      if (index > -1) {
        this.newOrderIds.splice(index, 1)
        this.saveNewOrderIds()
        this.$message.success('已标记为已读')
      }
    },
    clearAllNewFlags() {
      this.newOrderIds = []
      this.saveNewOrderIds()
      this.$message.success('全部标记为已读')
    },
    goToOrder(order) {
      this.expandRowKeys = [order.id]
    },
    loadNewOrderIds() {
      const saved = localStorage.getItem('xuanzhi_new_orders')
      if (saved) {
        this.newOrderIds = JSON.parse(saved)
      }
    },
    saveNewOrderIds() {
      localStorage.setItem('xuanzhi_new_orders', JSON.stringify(this.newOrderIds))
    },
    checkNewOrders() {
      const lastCheckTime = localStorage.getItem('xuanzhi_last_check_time')
      const now = Date.now()
      
      this.orders.forEach(order => {
        const orderTime = new Date(order.createdAt).getTime()
        if (!lastCheckTime || orderTime > lastCheckTime) {
          if (!this.newOrderIds.includes(order.id)) {
            this.newOrderIds.push(order.id)
          }
        }
      })
      
      this.saveNewOrderIds()
      localStorage.setItem('xuanzhi_last_check_time', String(now))
    },
    getStatusType(status) {
      const map = {
        pending: 'info',
        processing: 'warning',
        completed: 'success'
      }
      return map[status] || 'info'
    },
    getStatusText(status) {
      const map = {
        pending: '待处理',
        processing: '生产中',
        completed: '已完成'
      }
      return map[status] || status
    },
    getCurrentStepName(order) {
      if (order.currentStep < 8 && order.steps[order.currentStep]) {
        return order.steps[order.currentStep].name
      }
      return ''
    },
    completeStep(order) {
      const stepIndex = order.currentStep
      if (stepIndex >= 8) return

      const newSteps = [...order.steps]
      newSteps[stepIndex] = {
        ...newSteps[stepIndex],
        completed: true,
        time: formatDateTime(new Date())
      }

      const newCurrentStep = stepIndex + 1
      const newStatus = newCurrentStep >= 8 ? 'completed' : 'processing'

      updateOrder(order.id, {
        steps: newSteps,
        currentStep: newCurrentStep,
        status: newStatus
      })

      this.loadOrders()
      this.$message.success(`「${newSteps[stepIndex].name}」工序完成！`)
    },
    showResetConfirm(order) {
      this.$confirm('确定要重置该订单的所有工序吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const newSteps = order.steps.map(s => ({
          ...s,
          completed: false,
          time: null
        }))
        updateOrder(order.id, {
          steps: newSteps,
          currentStep: 0,
          status: 'pending'
        })
        this.loadOrders()
        this.$message.success('工序已重置')
      }).catch(() => {})
    },
    showDeleteConfirm(order) {
      this.$confirm(`确定要删除订单 ${order.id} 吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const orders = getOrders().filter(o => o.id !== order.id)
        localStorage.setItem('xuanzhi_orders', JSON.stringify(orders))
        this.loadOrders()
        this.$message.success('订单已删除')
      }).catch(() => {})
    },
    handleLogout() {
      this.$confirm('确定要退出登录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      }).then(() => {
        logout()
        this.$router.push('/admin/login')
        this.$message.success('已退出登录')
      }).catch(() => {})
    }
  }
}
</script>

<style lang="scss" scoped>
.admin-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.page-title-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;

  h2 {
    margin: 0;
    font-size: 22px;
    color: #1A1A1A;
    font-weight: 600;
  }

  .filter-bar {
    display: flex;
    gap: 15px;
    align-items: center;
  }
}

.stats-card {
  padding: 25px;
  margin-bottom: 20px;

  .stat-item {
    text-align: center;

    .stat-value {
      font-size: 32px;
      font-weight: 600;
      margin-bottom: 8px;

      &.all { color: #5D4E37; }
      &.pending { color: #909399; }
      &.processing { color: #E6A23C; }
      &.completed { color: #67C23A; }
    }

    .stat-label {
      color: #909399;
      font-size: 14px;
    }
  }
}

.order-list {
  padding: 20px;

  .order-id {
    font-family: 'Consolas', monospace;
    color: #C41E3A;
    font-weight: 500;
  }

  .product-info {
    p {
      margin: 0;
      color: #1A1A1A;
      font-weight: 500;
    }
    .sub-info {
      color: #909399;
      font-size: 12px;
      font-weight: normal;
      margin-top: 4px;
    }
  }

  .process-info {
    p {
      margin: 0;
    }
    .sub-info {
      color: #909399;
      font-size: 12px;
      margin-top: 4px;
    }
  }

  .progress-text {
    display: block;
    text-align: center;
    font-size: 12px;
    color: #909399;
    margin-top: 4px;
  }
}

.order-detail {
  padding: 10px 20px 20px;

  .detail-block {
    h4 {
      font-size: 14px;
      color: #1A1A1A;
      margin-bottom: 12px;
      padding-bottom: 8px;
      border-bottom: 1px solid #ebeef5;
    }

    p {
      margin: 6px 0;
      color: #606266;
      font-size: 13px;

      span:first-child {
        color: #909399;
      }
    }
  }

  .process-section {
    margin-top: 25px;
    padding-top: 20px;
    border-top: 1px solid #ebeef5;

    h4 {
      font-size: 14px;
      color: #1A1A1A;
      margin-bottom: 20px;
    }

    .process-timeline {
      display: flex;
      justify-content: space-between;
      position: relative;
      margin-bottom: 25px;
      padding: 0 10px;

      .timeline-item {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;

        .timeline-dot {
          width: 36px;
          height: 36px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 14px;
          font-weight: 600;
          z-index: 2;
          transition: all 0.3s ease;
          background: #f0f2f5;
          color: #909399;
          border: 2px solid #dcdfe6;
        }

        &.is-completed .timeline-dot {
          background: #67C23A;
          border-color: #67C23A;
          color: #fff;
          animation: pulse 0.5s ease;
        }

        &.is-current .timeline-dot {
          background: #E6A23C;
          border-color: #E6A23C;
          color: #fff;
          animation: pulse 0.5s ease;
        }

        @keyframes pulse {
          0% { transform: scale(1); }
          50% { transform: scale(1.15); }
          100% { transform: scale(1); }
        }

        .timeline-content {
          margin-top: 10px;
          text-align: center;

          .timeline-header {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 6px;

            .step-name {
              font-weight: 600;
              color: #1A1A1A;
              font-size: 13px;
            }
          }

          .timeline-time {
            margin-top: 6px;
            font-size: 11px;
            color: #909399;

            i {
              margin-right: 2px;
            }
          }
        }

        &.is-pending {
          .step-name {
            color: #909399;
            font-weight: 400;
          }
        }

        .timeline-connector {
          position: absolute;
          top: 18px;
          left: 50%;
          width: 100%;
          height: 2px;
          background: #dcdfe6;
          z-index: 1;

          &.is-done {
            background: #67C23A;
          }
        }
      }
    }

    .process-actions {
      display: flex;
      gap: 10px;
      align-items: center;
      justify-content: center;
    }
  }
}

.empty-state {
  text-align: center;
  padding: 60px 0;
  color: #909399;

  i {
    font-size: 48px;
    display: block;
    margin-bottom: 15px;
  }

  p {
    margin: 0;
    font-size: 14px;
  }
}

.filter-bar {
  .sort-btn {
    margin-left: 10px;

    i {
      margin-right: 4px;
    }
  }
}

.new-orders-section {
  margin-bottom: 20px;
  background: #FFF5F5;
  border: 1px solid #FFD1D1;

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;

    .new-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-weight: 600;
      color: #C41E3A;
      font-size: 16px;

      i {
        font-size: 18px;
      }

      .badge-count {
        background: #C41E3A;
        color: #fff;
        font-size: 12px;
        padding: 2px 8px;
        border-radius: 10px;
        font-weight: 600;
      }
    }
  }

  .new-orders-list {
    display: flex;
    flex-direction: column;
    gap: 10px;

    .new-order-item {
      display: flex;
      align-items: center;
      background: #fff;
      border: 1px solid #FFE0E0;
      border-left: 4px solid #C41E3A;
      border-radius: 6px;
      padding: 12px 16px;
      cursor: pointer;
      transition: all 0.3s ease;

      &:hover {
        background: #FFF8F8;
        box-shadow: 0 2px 8px rgba(196, 30, 58, 0.1);
      }

      .order-main {
        flex: 1;
        display: flex;
        align-items: center;
        gap: 20px;

        .order-id {
          font-weight: 600;
          color: #C41E3A;
          display: flex;
          align-items: center;
          gap: 4px;

          i {
            font-size: 14px;
          }
        }

        .order-customer {
          color: #1A1A1A;
        }

        .order-product {
          color: #606266;
        }

        .order-size {
          color: #909399;
          font-size: 13px;
        }
      }

      .order-meta {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-right: 15px;

        .order-time {
          color: #909399;
          font-size: 12px;
        }
      }

      .read-btn {
        color: #909399;

        &:hover {
          color: #67C23A;
        }
      }
    }
  }
}

.table-header {
  margin-bottom: 15px;

  h3 {
    font-size: 14px;
    color: #1A1A1A;
    margin: 0;
    padding-bottom: 10px;
    border-bottom: 1px solid #ebeef5;
  }
}

::v-deep .el-table .new-order-row {
  background: #FFF5F5;

  &:hover > td {
    background: #FFF0F0 !important;
  }

  td {
    border-top: 1px solid #FFE0E0;
    border-bottom: 1px solid #FFE0E0;

    &:first-child {
      border-left: 3px solid #C41E3A;
    }

    &:last-child {
      border-right: 1px solid #FFE0E0;
    }
  }

  .order-id {
    color: #C41E3A;
    font-weight: 600;
  }
}
</style>
