<template>
  <div class="admin-panel">
    <div class="page-container">
      <h1 class="page-title">
        <i class="el-icon-setting"></i>
        订单管理后台
      </h1>

      <el-row :gutter="24" class="stats-row">
        <el-col :xs="12" :md="6">
          <div class="stat-card pending">
            <div class="stat-icon">
              <i class="el-icon-time"></i>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ pendingCount }}</div>
              <div class="stat-label">待生产</div>
            </div>
          </div>
        </el-col>
        <el-col :xs="12" :md="6">
          <div class="stat-card processing">
            <div class="stat-icon">
              <i class="el-icon-loading"></i>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ processingCount }}</div>
              <div class="stat-label">生产中</div>
            </div>
          </div>
        </el-col>
        <el-col :xs="12" :md="6">
          <div class="stat-card completed">
            <div class="stat-icon">
              <i class="el-icon-circle-check"></i>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ completedCount }}</div>
              <div class="stat-label">已完工</div>
            </div>
          </div>
        </el-col>
        <el-col :xs="12" :md="6">
          <div class="stat-card total">
            <div class="stat-icon">
              <i class="el-icon-document"></i>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ orders.length }}</div>
              <div class="stat-label">总订单</div>
            </div>
          </div>
        </el-col>
      </el-row>

      <div class="card filter-card">
        <el-row :gutter="16" type="flex" align="middle">
          <el-col :span="12">
            <span class="filter-label">订单状态：</span>
            <el-radio-group v-model="filterStatus" size="small">
              <el-radio-button label="all">全部</el-radio-button>
              <el-radio-button label="pending">待生产</el-radio-button>
              <el-radio-button label="processing">生产中</el-radio-button>
              <el-radio-button label="completed">已完工</el-radio-button>
            </el-radio-group>
          </el-col>
          <el-col :span="12" style="text-align: right">
            <el-input
              v-model="searchKeyword"
              placeholder="搜索订单号或手机号"
              prefix-icon="el-icon-search"
              style="width: 280px"
              clearable
            ></el-input>
          </el-col>
        </el-row>
      </div>

      <div class="order-list">
        <el-empty
          v-if="filteredOrders.length === 0"
          description="暂无订单数据"
          :image-size="100"
        ></el-empty>

        <el-collapse v-else accordion>
          <el-collapse-item
            v-for="order in filteredOrders"
            :key="order.id"
            :name="order.id"
          >
            <template slot="title">
              <div class="collapse-title">
                <div class="title-left">
                  <i class="el-icon-document"></i>
                  <span class="order-id">{{ order.id }}</span>
                  <el-tag :type="getStatusTagType(order.status)" size="small" class="status-tag">
                    {{ getStatusText(order.status) }}
                  </el-tag>
                </div>
                <div class="title-right">
                  <span class="order-meta">
                    {{ order.material }} · {{ order.style }} · {{ order.handle }}
                  </span>
                  <i class="el-icon-arrow-right collapse-arrow"></i>
                </div>
              </div>
            </template>

            <div class="order-detail">
              <el-row :gutter="24">
                <el-col :md="10">
                  <div class="detail-section">
                    <h4>订单信息</h4>
                    <div class="detail-grid">
                      <div class="detail-item">
                        <span class="label">藤条材质</span>
                        <span class="value">{{ order.material }}</span>
                      </div>
                      <div class="detail-item">
                        <span class="label">果篮高度</span>
                        <span class="value">{{ order.height }} cm</span>
                      </div>
                      <div class="detail-item">
                        <span class="label">口径大小</span>
                        <span class="value">{{ order.diameter }} cm</span>
                      </div>
                      <div class="detail-item">
                        <span class="label">编织款式</span>
                        <span class="value">{{ order.style }}</span>
                      </div>
                      <div class="detail-item">
                        <span class="label">提手配置</span>
                        <span class="value">{{ order.handle }}</span>
                      </div>
                      <div class="detail-item">
                        <span class="label">联系方式</span>
                        <span class="value">{{ order.contact }}</span>
                      </div>
                      <div class="detail-item full-width">
                        <span class="label">下单时间</span>
                        <span class="value">{{ formatDate(order.createdAt) }}</span>
                      </div>
                    </div>
                  </div>
                </el-col>

                <el-col :md="14">
                  <div class="detail-section">
                    <h4>
                      生产进度
                      <span class="progress-text">
                        {{ Math.round((order.currentProcess / 7) * 100) }}%
                      </span>
                    </h4>

                    <ProcessSteps
                      :current-process="order.currentProcess"
                      :process-times="order.processTimes"
                    />

                    <div class="process-info">
                      <div class="current-process">
                        <span class="label">当前工序：</span>
                        <span class="value">
                          <el-tag v-if="order.currentProcess < 7" type="primary" size="small">
                            {{ processes[order.currentProcess].name }}
                          </el-tag>
                          <el-tag v-else type="success" size="small">
                            已完工
                          </el-tag>
                        </span>
                      </div>
                      <div class="next-process" v-if="order.currentProcess < 7">
                        <span class="label">下一道工序：</span>
                        <span class="value">{{ processes[order.currentProcess + 1].name }}</span>
                      </div>
                    </div>

                    <div class="action-buttons">
                      <el-button
                        type="primary"
                        :disabled="order.currentProcess >= 7"
                        @click="handleAdvance(order.id)"
                      >
                        <i class="el-icon-arrow-right"></i>
                        {{ order.currentProcess >= 7 ? '已完工' : `推进到「${getNextProcessName(order)}」` }}
                      </el-button>
                      <el-button
                        v-if="order.currentProcess === 7"
                        type="success"
                        disabled
                      >
                        <i class="el-icon-present"></i>
                        订单已完成
                      </el-button>
                    </div>
                  </div>
                </el-col>
              </el-row>
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>
    </div>
  </div>
</template>

<script>
import ProcessSteps from '../components/ProcessSteps.vue'

export default {
  name: 'AdminPanel',
  components: {
    ProcessSteps
  },
  data() {
    return {
      filterStatus: 'all',
      searchKeyword: ''
    }
  },
  computed: {
    orders() {
      return this.$store.state.orders
    },
    processes() {
      return this.$store.state.processes
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
    filteredOrders() {
      let result = [...this.orders]
      
      if (this.filterStatus !== 'all') {
        result = result.filter(o => o.status === this.filterStatus)
      }
      
      if (this.searchKeyword) {
        const keyword = this.searchKeyword.toLowerCase()
        result = result.filter(o =>
          o.id.toLowerCase().includes(keyword) ||
          o.contact.includes(keyword)
        )
      }
      
      return result
    }
  },
  created() {
    this.$store.commit('LOAD_FROM_STORAGE')
  },
  methods: {
    getStatusTagType(status) {
      const map = {
        pending: 'warning',
        processing: 'primary',
        completed: 'success'
      }
      return map[status] || 'info'
    },
    getStatusText(status) {
      const map = {
        pending: '待生产',
        processing: '生产中',
        completed: '已完工'
      }
      return map[status] || '未知'
    },
    formatDate(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
    },
    getNextProcessName(order) {
      const nextIndex = order.currentProcess + 1
      if (nextIndex < this.processes.length) {
        return this.processes[nextIndex].name
      }
      return '完工'
    },
    handleAdvance(orderId) {
      const order = this.orders.find(o => o.id === orderId)
      if (order && order.currentProcess < 7) {
        this.$store.dispatch('advanceProcess', orderId)
        this.$message.success(`已推进到「${this.processes[order.currentProcess + 1].name}」工序`)
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.admin-panel {
  .stats-row {
    margin-bottom: 24px;
  }

  .stat-card {
    background: #fff;
    border-radius: 12px;
    padding: 20px;
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: 0 2px 12px rgba(139, 69, 19, 0.1);
    transition: all 0.3s;

    &:hover {
      transform: translateY(-4px);
      box-shadow: 0 6px 20px rgba(139, 69, 19, 0.15);
    }

    .stat-icon {
      width: 56px;
      height: 56px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 28px;

      i {
        font-size: 28px;
      }
    }

    &.pending .stat-icon {
      background: #FFF3E0;
      color: #FB8C00;
    }

    &.processing .stat-icon {
      background: #E3F2FD;
      color: #1976D2;
    }

    &.completed .stat-icon {
      background: #E8F5E9;
      color: #388E3C;
    }

    &.total .stat-icon {
      background: #F3E5F5;
      color: #7B1FA2;
    }

    .stat-number {
      font-size: 28px;
      font-weight: 700;
      color: #5D4037;
      line-height: 1.2;
    }

    .stat-label {
      font-size: 14px;
      color: #8D6E63;
    }
  }

  .filter-card {
    ::v-deep .el-radio-button__orig-radio:checked + .el-radio-button__inner {
      background-color: #8B4513;
      border-color: #8B4513;
    }
  }

  .filter-label {
    margin-right: 12px;
    color: #5D4037;
    font-weight: 500;
  }

  .order-list {
    ::v-deep .el-collapse {
      border: none;
      background: transparent;
    }

    ::v-deep .el-collapse-item {
      border: none;
      margin-bottom: 16px;
    }

    ::v-deep .el-collapse-item__header {
      background: #fff;
      border-radius: 12px;
      padding: 0 20px;
      height: 60px;
      line-height: 60px;
      box-shadow: 0 2px 12px rgba(139, 69, 19, 0.1);
      border: none;
    }

    ::v-deep .el-collapse-item__wrap {
      background: #fff;
      border-radius: 0 0 12px 12px;
      margin-top: 4px;
      box-shadow: 0 4px 16px rgba(139, 69, 19, 0.1);
      border: none;
    }

    ::v-deep .el-collapse-item__content {
      padding-bottom: 0;
    }
  }

  .collapse-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;

    .title-left {
      display: flex;
      align-items: center;
      gap: 12px;

      .order-id {
        font-weight: 600;
        color: #5D4037;
        font-size: 15px;
      }

      i {
        color: #8B4513;
        font-size: 18px;
      }
    }

    .title-right {
      display: flex;
      align-items: center;
      gap: 16px;

      .order-meta {
        color: #8D6E63;
        font-size: 14px;
      }

      .collapse-arrow {
        color: #8D6E63;
        transition: transform 0.3s;
      }
    }
  }

  ::v-deep .el-collapse-item.is-active .collapse-arrow {
    transform: rotate(90deg);
  }

  .order-detail {
    padding: 20px;

    .detail-section {
      h4 {
        font-size: 16px;
        font-weight: 600;
        color: #5D4037;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid #EFEBE9;
        display: flex;
        justify-content: space-between;
        align-items: center;

        .progress-text {
          font-size: 18px;
          color: #8B4513;
        }
      }
    }

    .detail-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;

      .detail-item {
        display: flex;
        flex-direction: column;
        gap: 4px;
        padding: 12px;
        background: #FDF5E6;
        border-radius: 8px;

        &.full-width {
          grid-column: span 2;
        }

        .label {
          font-size: 12px;
          color: #8D6E63;
        }

        .value {
          font-size: 15px;
          font-weight: 600;
          color: #5D4037;
        }
      }
    }

    .process-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin: 16px 0;
    }

    .process-info {
      background: #FDF5E6;
      border-radius: 8px;
      padding: 16px;
      margin: 16px 0;

      .current-process,
      .next-process {
        display: flex;
        align-items: center;
        margin-bottom: 8px;

        &:last-child {
          margin-bottom: 0;
        }

        .label {
          color: #8D6E63;
          min-width: 90px;
          font-size: 14px;
        }

        .value {
          color: #5D4037;
          font-weight: 600;
          font-size: 15px;
        }
      }
    }

    .action-buttons {
      display: flex;
      justify-content: flex-end;
      gap: 12px;
      padding-top: 16px;
      border-top: 1px solid #EFEBE9;
    }
  }
}
</style>
