<template>
  <div class="dispatch-page">
    <div class="page-container">
      <div class="page-header">
        <h2 class="page-title">骑手派单</h2>
      </div>

      <el-row :gutter="24">
        <el-col :span="14">
          <el-card>
            <div slot="header" class="card-header">
              <span><i class="el-icon-document"></i> 待配送订单</span>
              <el-tag type="warning" size="small">{{ pendingOrders.length }} 单待分配</el-tag>
            </div>
            <div v-if="pendingOrders.length === 0" class="empty-state">
              <i class="el-icon-circle-check"></i>
              <p>暂无待配送订单</p>
            </div>
            <div v-else>
              <div
                v-for="order in pendingOrders"
                :key="order.id"
                class="order-card"
                :class="{ active: selectedOrder?.id === order.id }"
                @click="selectOrder(order)"
              >
                <div class="order-card-header">
                  <span class="order-id">{{ order.id }}</span>
                  <el-tag type="warning">待派单</el-tag>
                </div>
                <div class="order-card-body">
                  <div class="order-info">
                    <i class="el-icon-user"></i>
                    <span>{{ order.customerName }}</span>
                    <span class="phone">{{ order.phone }}</span>
                  </div>
                  <div class="order-info">
                    <i class="el-icon-location"></i>
                    <span class="address">{{ order.address }}</span>
                  </div>
                  <div class="order-info">
                    <i class="el-icon-goods"></i>
                    <span>{{ order.dishes.length }} 件商品</span>
                    <span class="amount">¥ {{ order.totalPrice.toFixed(2) }}</span>
                  </div>
                  <div class="order-info">
                    <i class="el-icon-time"></i>
                    <span>{{ order.createTime }}</span>
                  </div>
                </div>
                <div class="order-dishes">
                  <div v-for="(dish, index) in order.dishes" :key="index" class="dish-item">
                    {{ dish.name }} x {{ dish.quantity }}
                  </div>
                </div>
                <div class="order-card-footer" v-if="selectedOrder?.id === order.id">
                  <el-button
                    type="primary"
                    size="small"
                    :disabled="!selectedRider"
                    @click.stop="assignRiderToOrder(order)"
                  >
                    <i class="el-icon-check"></i>
                    分配给 {{ selectedRider?.name || '请选择骑手' }}
                  </el-button>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>

        <el-col :span="10">
          <el-card class="rider-card">
            <div slot="header" class="card-header">
              <span><i class="el-icon-bicycle"></i> 骑手列表</span>
              <el-tag type="success" size="small">{{ availableRiders.length }} 人空闲</el-tag>
            </div>
            <div class="rider-tabs">
              <el-radio-group v-model="riderFilter" size="small">
                <el-radio-button label="all">全部</el-radio-button>
                <el-radio-button label="available">空闲</el-radio-button>
                <el-radio-button label="busy">配送中</el-radio-button>
              </el-radio-group>
            </div>
            <div
              v-for="rider in filteredRiders"
              :key="rider.id"
              class="rider-item"
              :class="{ active: selectedRider?.id === rider.id, disabled: rider.status !== '空闲', 'has-conflict': hasRiderConflict(rider.id) }"
              @click="selectRider(rider)"
            >
              <div class="rider-avatar">
                <i class="el-icon-user-solid"></i>
              </div>
              <div class="rider-info">
                <div class="rider-name">
                  {{ rider.name }}
                  <el-tag :type="rider.status === '空闲' ? 'success' : 'warning'" size="mini">
                    {{ rider.status }}
                  </el-tag>
                  <el-tag v-if="hasRiderConflict(rider.id)" type="danger" size="mini" class="conflict-tag">
                    <i class="el-icon-warning"></i> 配送冲突
                  </el-tag>
                </div>
                <div class="rider-phone">
                  <i class="el-icon-phone"></i> {{ rider.phone }}
                </div>
                <div class="rider-stats">
                  <span><i class="el-icon-document"></i> 当前 {{ rider.orders }} 单</span>
                  <span><i class="el-icon-star-on"></i> {{ rider.rating }} 分</span>
                </div>
                <div v-if="hasRiderConflict(rider.id)" class="rider-conflict">
                  <i class="el-icon-warning"></i>
                  该骑手当前有配送中的订单，无法同时派单
                </div>
              </div>
              <div class="rider-select" v-if="rider.status === '空闲' && !hasRiderConflict(rider.id)">
                <el-radio :label="rider.id" v-model="selectedRiderId">
                </el-radio>
              </div>
              <div class="rider-select" v-else-if="rider.status !== '空闲' || hasRiderConflict(rider.id)">
                <i class="el-icon-circle-close disabled-icon"></i>
              </div>
            </div>
          </el-card>

          <el-card class="mt-24">
            <div slot="header" class="card-header">
              <span><i class="el-icon-location"></i> 配送中订单</span>
            </div>
            <div v-if="deliveringOrders.length === 0" class="empty-state">
              <p>暂无配送中订单</p>
            </div>
            <div v-else>
              <div
                v-for="order in deliveringOrders"
                :key="order.id"
                class="delivering-item"
              >
                <div class="delivering-header">
                  <span class="order-id">{{ order.id }}</span>
                  <el-tag type="primary">配送中</el-tag>
                </div>
                <div class="delivering-info">
                  <div>
                    <i class="el-icon-bicycle"></i>
                    <span>骑手：{{ order.riderName }}</span>
                  </div>
                  <div>
                    <i class="el-icon-user"></i>
                    <span>{{ order.customerName }}</span>
                  </div>
                  <div class="address">
                    <i class="el-icon-location"></i>
                    {{ order.address }}
                  </div>
                </div>
                <el-button
                  type="success"
                  size="small"
                  @click="completeDelivery(order.id)"
                >
                  <i class="el-icon-check"></i> 确认送达
                </el-button>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'

export default {
  name: 'Dispatch',
  data() {
    return {
      selectedOrder: null,
      selectedRiderId: null,
      riderFilter: 'all'
    }
  },
  computed: {
    ...mapState(['orders', 'riders']),
    ...mapGetters(['availableRiders']),
    pendingOrders() {
      return this.orders.filter(o => o.status === 'preparing')
    },
    deliveringOrders() {
      return this.orders.filter(o => o.status === 'delivering')
    },
    filteredRiders() {
      if (this.riderFilter === 'available') {
        return this.riders.filter(r => r.status === '空闲')
      } else if (this.riderFilter === 'busy') {
        return this.riders.filter(r => r.status === '配送中')
      }
      return this.riders
    },
    selectedRider() {
      return this.riders.find(r => r.id === this.selectedRiderId)
    }
  },
  methods: {
    ...mapActions(['assignRider', 'completeDelivery']),
    hasRiderConflict(riderId) {
      const activeOrders = this.orders.filter(o => o.riderId === riderId && o.status === 'delivering')
      return activeOrders.length > 0
    },
    selectOrder(order) {
      this.selectedOrder = order
    },
    selectRider(rider) {
      if (rider.status !== '空闲') {
        this.$message.warning(`骑手 ${rider.name} 当前不处于空闲状态`)
        return
      }
      if (this.hasRiderConflict(rider.id)) {
        this.$message.warning(`骑手 ${rider.name} 当前有配送中的订单，无法同时派单`)
        return
      }
      this.selectedRiderId = rider.id
    },
    async assignRiderToOrder(order) {
      if (!this.selectedRider) {
        this.$message.warning('请先选择骑手')
        return
      }
      if (this.hasRiderConflict(this.selectedRider.id)) {
        this.$message.error(`骑手 ${this.selectedRider.name} 当前有配送中的订单，同一时段不能重复派单`)
        return
      }
      this.$confirm(
        `确定将订单 ${order.id} 分配给骑手 ${this.selectedRider.name} 吗？`,
        '确认派单',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(async () => {
        const result = await this.assignRider({
          orderId: order.id,
          riderId: this.selectedRider.id,
          riderName: this.selectedRider.name
        })
        if (result.success) {
          this.$message.success('派单成功！')
          this.selectedOrder = null
          this.selectedRiderId = null
        } else {
          this.$message.error(result.message)
        }
      }).catch(() => {})
    },
    completeDelivery(orderId) {
      this.$confirm('确认订单已送达吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.completeDelivery(orderId)
        this.$message.success('配送完成！')
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
  font-weight: 600;
}
.order-card {
  border: 1px solid #ebeef5;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}
.order-card:hover {
  border-color: #409eff;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.15);
}
.order-card.active {
  border-color: #409eff;
  background-color: #ecf5ff;
}
.order-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.order-id {
  font-weight: 600;
  color: #303133;
}
.order-card-body {
  margin-bottom: 12px;
}
.order-info {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
  font-size: 13px;
  color: #606266;
}
.order-info .phone {
  color: #909399;
}
.order-info .address {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.order-info .amount {
  color: #f56c6c;
  font-weight: 600;
  margin-left: auto;
}
.order-dishes {
  padding-top: 12px;
  border-top: 1px dashed #ebeef5;
}
.dish-item {
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}
.order-card-footer {
  margin-top: 12px;
  text-align: right;
}
.rider-card {
  position: sticky;
  top: 20px;
}
.rider-tabs {
  margin-bottom: 16px;
}
.rider-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  margin-bottom: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}
.rider-item:hover {
  border-color: #409eff;
}
.rider-item.active {
  border-color: #409eff;
  background-color: #ecf5ff;
}
.rider-item.disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.rider-item.has-conflict {
  border-color: #f56c6c;
  background-color: #fef0f0;
}
.conflict-tag {
  margin-left: 8px;
}
.rider-conflict {
  font-size: 12px;
  color: #f56c6c;
  margin-top: 4px;
}
.rider-conflict i {
  margin-right: 2px;
}
.disabled-icon {
  color: #c0c4cc;
  font-size: 20px;
}
.rider-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 20px;
  flex-shrink: 0;
}
.rider-info {
  flex: 1;
}
.rider-name {
  font-weight: 600;
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.rider-phone {
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}
.rider-stats {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: #606266;
}
.rider-stats i {
  margin-right: 4px;
}
.rider-stats .el-icon-star-on {
  color: #f5d742;
}
.delivering-item {
  border: 1px solid #ebeef5;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 12px;
}
.delivering-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.delivering-info {
  font-size: 13px;
  color: #606266;
  margin-bottom: 12px;
}
.delivering-info div {
  margin-bottom: 4px;
}
.delivering-info .address {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.delivering-info i {
  margin-right: 4px;
}
</style>
