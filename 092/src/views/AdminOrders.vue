<template>
  <div class="admin-orders-container">
    <el-card class="orders-card" shadow="hover">
      <div slot="header" class="card-header">
        <span>订单管理</span>
        <el-button type="primary" size="small" @click="refreshOrders">刷新订单</el-button>
      </div>

      <el-table :data="orders" style="width: 100%" border>
        <el-table-column prop="id" label="订单号" width="120" align="center"></el-table-column>
        <el-table-column prop="woodType" label="木料" width="100" align="center"></el-table-column>
        <el-table-column prop="beastStyle" label="款式" width="100" align="center"></el-table-column>
        <el-table-column label="尺寸" width="180" align="center">
          <template slot-scope="scope">
            <span>长{{ scope.row.length }}×宽{{ scope.row.width }}×高{{ scope.row.height }}cm</span>
          </template>
        </el-table-column>
        <el-table-column label="鎏金" width="80" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.isGilded ? 'success' : 'info'" size="mini">
              {{ scope.row.isGilded ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" min-width="150" show-overflow-tooltip></el-table-column>
        <el-table-column label="生产工序" min-width="350">
          <template slot-scope="scope">
            <div class="process-steps">
              <div
                v-for="(step, index) in statusOptions"
                :key="step.value"
                :class="['step-item', { active: scope.row.status >= step.value, current: scope.row.status === step.value, clickable: step.value <= scope.row.status + 1 }]"
                @click="updateProcess(scope.row, step.value)">
                <span class="step-dot"></span>
                <span class="step-label">{{ step.label }}</span>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="下单时间" width="180" align="center"></el-table-column>
        <el-table-column label="操作" width="120" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button
              type="success"
              size="mini"
              @click="nextStep(scope.row)"
              :disabled="scope.row.status >= 6">
              下一步
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="order-stats" v-if="orders.length > 0">
        <el-row :gutter="20">
          <el-col :span="6">
            <div class="stat-item">
              <p class="stat-label">总订单数</p>
              <p class="stat-value">{{ orders.length }}</p>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-item">
              <p class="stat-label">待选料</p>
              <p class="stat-value">{{ getStatusCount(0) }}</p>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-item">
              <p class="stat-label">进行中</p>
              <p class="stat-value">{{ getStatusCount(1, 5) }}</p>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-item">
              <p class="stat-label">已完工</p>
              <p class="stat-value">{{ getStatusCount(6) }}</p>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script>
import orderStore from '../store/orderStore'

export default {
  name: 'AdminOrders',
  data() {
    return {
      orders: [],
      statusOptions: orderStore.statusOptions
    }
  },
  created() {
    this.refreshOrders()
    orderStore.onOrderAdded(() => {
      this.refreshOrders()
    })
  },
  methods: {
    refreshOrders() {
      this.orders = orderStore.getOrders()
    },
    updateProcess(order, status) {
      if (status > order.status + 1) {
        this.$message({
          type: 'warning',
          message: '请按顺序推进工序，不允许跳步！'
        })
        return
      }
      if (status === order.status) {
        return
      }
      orderStore.updateStatus(order.id, status)
      this.$message({
        type: 'success',
        message: `订单 ${order.id} 已更新为：${orderStore.getStatusLabel(status)}`
      })
    },
    nextStep(order) {
      if (order.status < 6) {
        const nextStatus = order.status + 1
        this.updateProcess(order, nextStatus)
      }
    },
    getStatusCount(min, max = null) {
      if (max === null) {
        return this.orders.filter(o => o.status === min).length
      }
      return this.orders.filter(o => o.status >= min && o.status <= max).length
    }
  }
}
</script>

<style scoped>
.admin-orders-container {
  max-width: 1400px;
  margin: 0 auto;
}

.orders-card {
  border-radius: 12px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 20px;
  font-weight: 600;
  color: #8B4513;
}

.process-steps {
  display: flex;
  align-items: center;
  padding: 10px 0;
}

.step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: not-allowed;
  position: relative;
  flex: 1;
}

.step-item.clickable {
  cursor: pointer;
}

.step-item:not(:last-child)::after {
  content: '';
  position: absolute;
  top: 8px;
  left: 50%;
  width: 100%;
  height: 2px;
  background: #E4E7ED;
  z-index: 0;
}

.step-item.active:not(:last-child)::after {
  background: #67C23A;
}

.step-dot {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #E4E7ED;
  z-index: 1;
  margin-bottom: 5px;
}

.step-item.active .step-dot {
  background: #67C23A;
}

.step-item.current .step-dot {
  background: #409EFF;
  box-shadow: 0 0 0 3px rgba(64, 158, 255, 0.2);
}

.step-label {
  font-size: 12px;
  color: #909399;
  white-space: nowrap;
}

.step-item.active .step-label {
  color: #67C23A;
}

.step-item.current .step-label {
  color: #409EFF;
  font-weight: 600;
}

.order-stats {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #EBEEF5;
}

.stat-item {
  text-align: center;
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7ed 100%);
  border-radius: 8px;
}

.stat-label {
  margin: 0 0 10px 0;
  font-size: 14px;
  color: #606266;
}

.stat-value {
  margin: 0;
  font-size: 32px;
  font-weight: 600;
  color: #8B4513;
}

.el-table {
  border-radius: 8px;
  overflow: hidden;
}
</style>
