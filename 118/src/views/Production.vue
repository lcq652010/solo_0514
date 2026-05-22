<template>
  <div class="production-page">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="status-card pending-card">
          <div slot="header">
            <div class="card-header">
              <span class="status-title">待制作</span>
              <el-badge :value="pendingOrders.length" class="badge-item" type="warning"></el-badge>
            </div>
          </div>
          <div class="order-list">
            <div
              v-for="order in pendingOrders"
              :key="order.id"
              class="order-item"
            >
              <div class="order-header">
                <span class="order-no">{{ order.orderNo }}</span>
                <div class="header-tags">
                  <el-tag size="mini" type="success" v-if="order.paymentStatus === 'paid'">已支付</el-tag>
                  <el-tag size="mini" type="danger" v-else>未支付</el-tag>
                  <el-tag size="mini" type="warning">{{ order.takeType }}</el-tag>
                </div>
              </div>
              <div class="order-customer">
                <i class="el-icon-user"></i> {{ order.customerName }}
              </div>
              <div class="order-items-list">
                <div v-for="(item, idx) in order.items" :key="idx" class="order-item-row">
                  <span>{{ item.name }} x{{ item.quantity }}</span>
                  <span class="specs">{{ item.specsText }}</span>
                </div>
              </div>
              <div class="order-remark" v-if="order.remark">
                <i class="el-icon-document"></i> 备注：{{ order.remark }}
              </div>
              <div class="order-footer">
                <span class="order-time">{{ order.createTime }}</span>
                <el-button type="primary" size="mini" @click="startMaking(order)">开始制作</el-button>
              </div>
            </div>
            <el-empty v-if="pendingOrders.length === 0" description="暂无待制作订单" :image-size="80"></el-empty>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="status-card making-card">
          <div slot="header">
            <div class="card-header">
              <span class="status-title">制作中</span>
              <el-badge :value="makingOrders.length" class="badge-item" type="primary"></el-badge>
            </div>
          </div>
          <div class="order-list">
            <div
              v-for="order in makingOrders"
              :key="order.id"
              class="order-item"
            >
              <div class="order-header">
                <span class="order-no">{{ order.orderNo }}</span>
                <div class="header-tags">
                  <el-tag size="mini" type="success" v-if="order.paymentStatus === 'paid'">已支付</el-tag>
                  <el-tag size="mini" type="danger" v-else>未支付</el-tag>
                  <el-tag size="mini" type="primary">{{ order.takeType }}</el-tag>
                </div>
              </div>
              <div class="order-customer">
                <i class="el-icon-user"></i> {{ order.customerName }}
              </div>
              <div class="order-items-list">
                <div v-for="(item, idx) in order.items" :key="idx" class="order-item-row">
                  <span>{{ item.name }} x{{ item.quantity }}</span>
                  <span class="specs">{{ item.specsText }}</span>
                </div>
              </div>
              <div class="order-remark" v-if="order.remark">
                <i class="el-icon-document"></i> 备注：{{ order.remark }}
              </div>
              <div class="order-footer">
                <span class="order-time">{{ order.createTime }}</span>
                <el-button type="success" size="mini" @click="completeOrder(order)">制作完成</el-button>
              </div>
            </div>
            <el-empty v-if="makingOrders.length === 0" description="暂无制作中订单" :image-size="80"></el-empty>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="status-card completed-card">
          <div slot="header">
            <div class="card-header">
              <span class="status-title">已完成</span>
              <el-badge :value="completedOrders.length" class="badge-item" type="success"></el-badge>
            </div>
          </div>
          <div class="order-list">
            <div
              v-for="order in completedOrders"
              :key="order.id"
              class="order-item"
            >
              <div class="order-header">
                <span class="order-no">{{ order.orderNo }}</span>
                <div class="header-tags">
                  <el-tag size="mini" type="success" v-if="order.paymentStatus === 'paid'">已支付</el-tag>
                  <el-tag size="mini" type="danger" v-else>未支付</el-tag>
                  <el-tag size="mini" type="success">{{ order.takeType }}</el-tag>
                </div>
              </div>
              <div class="order-customer">
                <i class="el-icon-user"></i> {{ order.customerName }}
              </div>
              <div class="order-items-list">
                <div v-for="(item, idx) in order.items" :key="idx" class="order-item-row">
                  <span>{{ item.name }} x{{ item.quantity }}</span>
                  <span class="specs">{{ item.specsText }}</span>
                </div>
              </div>
              <div class="order-footer">
                <span class="order-time">{{ order.createTime }}</span>
                <span class="completed-tag"><i class="el-icon-check"></i> 已完成</span>
              </div>
            </div>
            <el-empty v-if="completedOrders.length === 0" description="暂无已完成订单" :image-size="80"></el-empty>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog
      title="新订单提醒"
      :visible.sync="newOrderDialogVisible"
      width="450px"
      :close-on-click-modal="false"
      custom-class="new-order-dialog"
    >
      <div class="new-order-content">
        <div class="new-order-icon">
          <i class="el-icon-bell"></i>
        </div>
        <div class="new-order-info">
          <h3>您有新的订单！</h3>
          <p class="order-no">订单号：{{ latestOrder?.orderNo }}</p>
          <p class="customer-info">
            <i class="el-icon-user"></i> {{ latestOrder?.customerName }}
            <span class="take-type-tag" :class="latestOrder?.takeType === '堂食' ? '' : 'take-out'">
              {{ latestOrder?.takeType }}
            </span>
          </p>
          <div class="order-items-preview">
            <div v-for="(item, idx) in latestOrder?.items" :key="idx" class="item-row">
              <span>{{ item.name }} x{{ item.quantity }}</span>
            </div>
          </div>
          <p class="order-amount">
            订单金额：<span class="amount">¥{{ latestOrder?.totalAmount }}</span>
          </p>
          <p v-if="latestOrder?.remark" class="order-remark">
            <i class="el-icon-document"></i> 备注：{{ latestOrder.remark }}
          </p>
        </div>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="newOrderDialogVisible = false">知道了</el-button>
        <el-button type="success" @click="startMaking(latestOrder); newOrderDialogVisible = false">开始制作</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { EventBus, playNewOrderSound } from '@/utils/eventBus'
export default {
  name: 'Production',
  data() {
    return {
      orders: [],
      newOrderDialogVisible: false,
      latestOrder: null
    }
  },
  computed: {
    pendingOrders() {
      return this.orders.filter(o => o.status === 'pending')
    },
    makingOrders() {
      return this.orders.filter(o => o.status === 'making')
    },
    completedOrders() {
      return this.orders.filter(o => o.status === 'completed').slice(0, 10)
    }
  },
  created() {
    this.loadOrders()
    EventBus.$on('orderStatusChanged', () => {
      this.loadOrders()
    })
    EventBus.$on('newOrder', (order) => {
      this.handleNewOrder(order)
    })
  },
  beforeDestroy() {
    EventBus.$off('orderStatusChanged')
    EventBus.$off('newOrder')
  },
  methods: {
    loadOrders() {
      this.orders = JSON.parse(localStorage.getItem('milkTeaOrders') || '[]')
    },
    updateStatus(order, status) {
      const index = this.orders.findIndex(o => o.id === order.id)
      if (index !== -1) {
        this.orders[index].status = status
        localStorage.setItem('milkTeaOrders', JSON.stringify(this.orders))
        EventBus.$emit('orderStatusChanged')
      }
    },
    startMaking(order) {
      this.updateStatus(order, 'making')
      this.$message.success('已开始制作')
    },
    completeOrder(order) {
      this.updateStatus(order, 'completed')
      this.$message.success('制作完成，可通知顾客取餐')
    },
    handleNewOrder(order) {
      this.latestOrder = order
      this.newOrderDialogVisible = true
      playNewOrderSound()
    }
  }
}
</script>

<style lang="scss" scoped>
.production-page {
  .status-card {
    height: calc(100vh - 100px);
    ::v-deep .el-card__body {
      height: calc(100% - 57px);
      overflow-y: auto;
    }
    .card-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      .status-title {
        font-size: 18px;
        font-weight: 600;
      }
    }
    .order-list {
      .order-item {
        background: #f5f7fa;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        &:last-child {
          margin-bottom: 0;
        }
        .order-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 10px;
          .order-no {
            font-weight: bold;
            color: #303133;
          }
          .header-tags {
            .el-tag {
              margin-left: 5px;
            }
          }
        }
        .order-customer {
          font-size: 14px;
          color: #606266;
          margin-bottom: 10px;
        }
        .order-items-list {
          background: #fff;
          border-radius: 4px;
          padding: 10px;
          margin-bottom: 10px;
          .order-item-row {
            font-size: 13px;
            color: #606266;
            margin-bottom: 5px;
            &:last-child {
              margin-bottom: 0;
            }
            .specs {
              display: block;
              font-size: 12px;
              color: #909399;
              margin-top: 2px;
            }
          }
        }
        .order-remark {
          font-size: 12px;
          color: #e6a23c;
          margin-bottom: 10px;
          padding: 5px 8px;
          background: #fdf6ec;
          border-radius: 4px;
        }
        .order-footer {
          display: flex;
          justify-content: space-between;
          align-items: center;
          .order-time {
            font-size: 12px;
            color: #909399;
          }
          .completed-tag {
            font-size: 12px;
            color: #67c23a;
          }
        }
      }
    }
  }
  .pending-card {
    ::v-deep .el-card__header {
      border-bottom: 2px solid #e6a23c;
    }
  }
  .making-card {
    ::v-deep .el-card__header {
      border-bottom: 2px solid #409eff;
    }
  }
  .completed-card {
    ::v-deep .el-card__header {
      border-bottom: 2px solid #67c23a;
    }
  }
}
.new-order-dialog {
  ::v-deep .el-dialog__header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    .el-dialog__title {
      color: #fff;
      font-weight: bold;
    }
    .el-dialog__headerbtn .el-dialog__close {
      color: #fff;
    }
  }
  .new-order-content {
    display: flex;
    .new-order-icon {
      width: 60px;
      height: 60px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-right: 20px;
      i {
        font-size: 30px;
        color: #fff;
      }
    }
    .new-order-info {
      flex: 1;
      h3 {
        margin: 0 0 10px 0;
        font-size: 20px;
        color: #303133;
      }
      .order-no {
        font-size: 14px;
        color: #909399;
        margin-bottom: 10px;
      }
      .customer-info {
        font-size: 14px;
        color: #606266;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        .take-type-tag {
          margin-left: 10px;
          padding: 2px 8px;
          border-radius: 4px;
          background: #ecf5ff;
          color: #409eff;
          font-size: 12px;
          &.take-out {
            background: #fef0f0;
            color: #f56c6c;
          }
        }
      }
      .order-items-preview {
        background: #f5f7fa;
        border-radius: 4px;
        padding: 10px;
        margin-bottom: 10px;
        .item-row {
          font-size: 14px;
          color: #606266;
          margin-bottom: 5px;
          &:last-child {
            margin-bottom: 0;
          }
        }
      }
      .order-amount {
        font-size: 16px;
        margin-bottom: 10px;
        .amount {
          font-weight: bold;
          color: #f56c6c;
          font-size: 20px;
        }
      }
      .order-remark {
        font-size: 12px;
        color: #e6a23c;
        padding: 8px;
        background: #fdf6ec;
        border-radius: 4px;
        margin: 0;
      }
    }
  }
}
</style>
