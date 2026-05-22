<template>
  <div class="admin-page" ref="adminPage">
    <el-card class="admin-card">
      <div slot="header" class="card-header">
        <h2>订单管理中心</h2>
        <el-tag :type="orderCount > 0 ? 'success' : 'info'">
          当前订单：{{ orderCount }} 个
        </el-tag>
      </div>

      <el-empty v-if="orders.length === 0" description="暂无订单数据">
        <el-button type="primary" @click="goToOrder">去下单</el-button>
      </el-empty>

      <div v-else class="order-list" ref="orderList">
        <el-collapse v-model="activeNames" @change="handleCollapseChange">
          <el-collapse-item 
            v-for="order in orders" 
            :key="order.id" 
            :name="order.id"
            :ref="'orderItem-' + order.id"
            :class="{'new-order-item': order.isNew}"
          >
            <template slot="title">
              <div class="order-title">
                <span class="order-id">
                  {{ order.id }}
                  <el-badge v-if="order.isNew" :value="'NEW'" class="new-order-badge" type="danger"></el-badge>
                </span>
                <span class="customer-name">{{ order.customerName }}</span>
                <el-tag :type="order.status === '已完成' ? 'success' : 'warning'" size="small">
                  {{ order.status }}
                </el-tag>
                <span class="create-time">{{ order.createTime }}</span>
              </div>
            </template>

            <div class="order-detail">
              <el-descriptions :column="3" border size="small">
                <el-descriptions-item label="锡料纯度">{{ order.purity }}</el-descriptions-item>
                <el-descriptions-item label="罐身高度">{{ order.height }}mm</el-descriptions-item>
                <el-descriptions-item label="口径尺寸">{{ order.diameter }}mm</el-descriptions-item>
                <el-descriptions-item label="纹饰风格">{{ order.pattern }}</el-descriptions-item>
                <el-descriptions-item label="密封配置">{{ order.sealType }}</el-descriptions-item>
                <el-descriptions-item label="联系电话">{{ order.phone }}</el-descriptions-item>
              </el-descriptions>

              <el-divider content-position="left">
                <span class="divider-title">生产工序</span>
              </el-divider>

              <div class="operator-selector">
                <span class="operator-label">当前操作员：</span>
                <el-select v-model="currentOperatorId" size="small" @change="changeOperator">
                  <el-option 
                    v-for="op in operators" 
                    :key="op.id" 
                    :label="op.name" 
                    :value="op.id"
                  ></el-option>
                </el-select>
              </div>

              <div class="process-steps">
                <el-steps :active="order.currentStep" finish-status="success" align-center>
                  <el-step 
                    v-for="step in order.processSteps" 
                    :key="step.id" 
                    :title="step.name"
                  ></el-step>
                </el-steps>
              </div>

              <div class="process-timestamps">
                <el-table :data="order.processSteps" size="small" border>
                  <el-table-column prop="name" label="工序名称" width="120"></el-table-column>
                  <el-table-column label="完成状态" width="100">
                    <template slot-scope="scope">
                      <el-tag :type="scope.row.completed ? 'success' : 'info'" size="mini">
                        {{ scope.row.completed ? '已完成' : '未完成' }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作员" width="100">
                    <template slot-scope="scope">
                      {{ scope.row.operator ? scope.row.operator.name : '-' }}
                    </template>
                  </el-table-column>
                  <el-table-column prop="completedTime" label="完成时间">
                    <template slot-scope="scope">
                      {{ scope.row.completedTime || '-' }}
                    </template>
                  </el-table-column>
                </el-table>
              </div>

              <div class="process-actions" v-if="order.status !== '已完成'">
                <el-button 
                  type="primary" 
                  size="small" 
                  @click="advanceStep(order.id)"
                  :disabled="order.currentStep >= order.processSteps.length"
                >
                  完成当前工序
                </el-button>
                <el-button 
                  size="small" 
                  @click="resetProcess(order.id)"
                >
                  重置工序
                </el-button>
              </div>

              <div v-else class="completed-badge">
                <el-result icon="success" title="订单已完成" sub-title="所有工序已顺利完成">
                </el-result>
              </div>
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>
    </el-card>
  </div>
</template>

<script>
import orderStore from '@/store/orderStore'

export default {
  name: 'AdminPage',
  data() {
    return {
      activeNames: [],
      unsubscribe: null,
      currentOperatorId: 'admin'
    }
  },
  computed: {
    orders() {
      return orderStore.getOrders()
    },
    orderCount() {
      return this.orders.length
    },
    operators() {
      return orderStore.getOperators()
    }
  },
  created() {
    if (this.orders.length > 0) {
      this.activeNames = [this.orders[0].id]
    }
    this.currentOperatorId = orderStore.getCurrentOperator().id
    this.unsubscribe = orderStore.subscribe(() => {
      this.$nextTick(() => {
        this.scrollToLatestOrder()
      })
    })
  },
  beforeDestroy() {
    if (this.unsubscribe) {
      this.unsubscribe()
    }
  },
  methods: {
    changeOperator(operatorId) {
      const operator = this.operators.find(op => op.id === operatorId)
      if (operator) {
        orderStore.setCurrentOperator(operator)
      }
    },
    handleCollapseChange(activeNames) {
      activeNames.forEach(orderId => {
        orderStore.markOrderAsRead(orderId)
      })
    },
    advanceStep(orderId) {
      const result = orderStore.advanceProcess(orderId)
      if (result) {
        this.$message.success('工序已更新')
      } else {
        this.$message.warning('该工序已完成，请勿重复操作')
      }
    },
    resetProcess(orderId) {
      this.$confirm('确定要重置该订单的工序吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        orderStore.resetProcess(orderId)
        this.$message.success('工序已重置')
      }).catch(() => {})
    },
    goToOrder() {
      this.$router.push('/')
    },
    scrollToLatestOrder() {
      const latestOrderId = orderStore.getLatestOrderId()
      if (latestOrderId) {
        if (!this.activeNames.includes(latestOrderId)) {
          this.activeNames.push(latestOrderId)
        }
        this.$nextTick(() => {
          const orderItem = this.$refs['orderItem-' + latestOrderId]
          if (orderItem && orderItem[0] && orderItem[0].$el) {
            orderItem[0].$el.scrollIntoView({ behavior: 'smooth', block: 'start' })
          }
        })
      }
    }
  }
}
</script>

<style scoped>
.admin-page {
  max-width: 1000px;
  margin: 0 auto;
}

.admin-card {
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-header h2 {
  color: #303133;
  font-size: 24px;
}

.order-title {
  display: flex;
  align-items: center;
  gap: 15px;
  flex-wrap: wrap;
}

.order-id {
  font-weight: 600;
  color: #409eff;
  font-size: 16px;
}

.customer-name {
  color: #606266;
}

.create-time {
  color: #909399;
  font-size: 13px;
  margin-left: auto;
}

.order-detail {
  padding: 10px 0;
}

.divider-title {
  font-size: 14px;
  font-weight: 600;
  color: #67c23a;
}

.process-steps {
  padding: 20px 0;
}

.process-timestamps {
  margin-top: 15px;
  padding: 0 10px;
}

.process-actions {
  text-align: center;
  padding: 20px 0;
}

.completed-badge {
  padding: 20px 0;
}

.operator-selector {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 0;
  margin-bottom: 10px;
}

.operator-label {
  font-size: 14px;
  color: #606266;
  font-weight: 500;
}

.new-order-item {
  background: linear-gradient(90deg, #fff0f0 0%, #ffffff 100%);
  border-left: 4px solid #f56c6c;
  animation: pulse-highlight 2s ease-in-out infinite;
}

.new-order-item >>> .el-collapse-item__header {
  background: linear-gradient(90deg, #fff5f5 0%, #ffffff 100%);
}

.new-order-badge {
  margin-left: 8px;
}

@keyframes pulse-highlight {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}
</style>
