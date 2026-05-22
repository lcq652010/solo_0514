<template>
  <div class="delivery-page">
    <div class="page-container">
      <div class="page-header">
        <h2 class="page-title">配送状态</h2>
        <div class="header-actions">
          <el-tooltip content="手动刷新">
            <el-button type="primary" icon="el-icon-refresh" :loading="refreshing" @click="manualRefresh">
              刷新
            </el-button>
          </el-tooltip>
          <el-switch
            v-model="autoRefresh"
            active-text="自动刷新"
            inactive-text="手动"
            @change="toggleAutoRefresh"
          />
          <el-select v-model="refreshInterval" size="small" style="width: 120px" @change="resetAutoRefresh">
            <el-option label="3秒" :value="3000" />
            <el-option label="5秒" :value="5000" />
            <el-option label="10秒" :value="10000" />
            <el-option label="30秒" :value="30000" />
          </el-select>
          <span v-if="lastRefreshTime" class="refresh-time">
            上次刷新：{{ lastRefreshTime }}
          </span>
        </div>
      </div>

      <el-card class="mb-24">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="订单号">
            <el-input
              v-model="searchForm.orderId"
              placeholder="请输入订单号查询"
              clearable
              style="width: 280px"
              prefix-icon="el-icon-search"
            />
          </el-form-item>
          <el-form-item label="订单状态">
            <el-select
              v-model="searchForm.status"
              placeholder="全部状态"
              clearable
              style="width: 140px"
            >
              <el-option label="待接单" value="pending" />
              <el-option label="备餐中" value="preparing" />
              <el-option label="配送中" value="delivering" />
              <el-option label="已送达" value="delivered" />
              <el-option label="已取消" value="cancelled" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <div v-if="selectedOrder" class="delivery-detail">
        <el-row :gutter="24">
          <el-col :span="10">
            <el-card>
              <div slot="header" class="card-header">
                <span><i class="el-icon-document"></i> 订单信息</span>
                <div class="header-tags">
                  <el-tag :type="getStatusType(selectedOrder.paymentStatus)" size="mini">
                    {{ getPaymentStatusText(selectedOrder.paymentStatus) }}
                  </el-tag>
                  <el-tag :type="getStatusType(selectedOrder.status)" size="small">
                    {{ getStatusText(selectedOrder.status) }}
                  </el-tag>
                </div>
              </div>
              <div class="order-info-item">
                <span class="label">订单号：</span>
                <span class="value">{{ selectedOrder.id }}</span>
              </div>
              <div class="order-info-item">
                <span class="label">商家：</span>
                <span class="value">{{ selectedOrder.merchantName }}</span>
              </div>
              <div class="order-info-item">
                <span class="label">区域：</span>
                <span class="value">{{ selectedOrder.districtName }}</span>
              </div>
              <div class="order-info-item">
                <span class="label">下单时间：</span>
                <span class="value">{{ selectedOrder.createTime }}</span>
              </div>
              <div class="order-info-item">
                <span class="label">收货人：</span>
                <span class="value">{{ selectedOrder.customerName }}</span>
              </div>
              <div class="order-info-item">
                <span class="label">联系电话：</span>
                <span class="value">{{ selectedOrder.phone }}</span>
              </div>
              <div class="order-info-item">
                <span class="label">收货地址：</span>
                <span class="value address">{{ selectedOrder.address }}</span>
              </div>
              <div class="order-info-item" v-if="selectedOrder.riderName">
                <span class="label">配送骑手：</span>
                <span class="value">
                  <i class="el-icon-bicycle"></i> {{ selectedOrder.riderName }}
                </span>
              </div>
              <div class="order-info-item" v-if="selectedOrder.remark">
                <span class="label">备注：</span>
                <span class="value">{{ selectedOrder.remark }}</span>
              </div>
              <div class="order-info-item" v-if="selectedOrder.finishTime">
                <span class="label">送达时间：</span>
                <span class="value">{{ selectedOrder.finishTime }}</span>
              </div>

              <div class="order-divider"></div>

              <h4 class="section-title">商品清单</h4>
              <div v-for="(dish, index) in selectedOrder.dishes" :key="index" class="dish-item">
                <span class="dish-name">{{ dish.name }}</span>
                <span class="dish-quantity">x {{ dish.quantity }}</span>
                <span class="dish-price">¥ {{ (dish.price * dish.quantity).toFixed(2) }}</span>
              </div>
              <div class="order-total">
                <span>合计：</span>
                <span class="total-price">¥ {{ selectedOrder.totalPrice.toFixed(2) }}</span>
              </div>
            </el-card>
          </el-col>

          <el-col :span="14">
            <el-card>
              <div slot="header" class="card-header">
                <span><i class="el-icon-location"></i> 配送进度</span>
                <span v-if="autoRefresh && selectedOrder.status !== 'delivered' && selectedOrder.status !== 'cancelled'" class="auto-refresh-indicator">
                  <i class="el-icon-loading"></i> 实时更新中
                </span>
              </div>
              <div v-if="selectedOrder.status === 'cancelled'" class="cancelled-state">
                <i class="el-icon-circle-close"></i>
                <p>订单已取消</p>
                <p class="cancel-reason" v-if="selectedOrder.cancelReason">
                  原因：{{ selectedOrder.cancelReason }}
                </p>
                <p class="cancel-time" v-if="selectedOrder.cancelTime">
                  取消时间：{{ selectedOrder.cancelTime }}
                </p>
              </div>
              <div v-else>
                <el-steps
                  :active="getStepIndex(selectedOrder.status)"
                  finish-status="success"
                  direction="vertical"
                  class="delivery-timeline"
                >
                  <el-step title="订单已提交" :description="selectedOrder.createTime">
                    <div slot="icon" class="step-icon">
                      <i class="el-icon-document"></i>
                    </div>
                  </el-step>
                  <el-step title="商家已接单" description="正在备餐中">
                    <div slot="icon" class="step-icon">
                      <i class="el-icon-check"></i>
                    </div>
                  </el-step>
                  <el-step
                    title="骑手取餐"
                    :description="selectedOrder.riderName ? `骑手 ${selectedOrder.riderName} 已取餐` : '等待骑手取餐'"
                  >
                    <div slot="icon" class="step-icon">
                      <i class="el-icon-bicycle"></i>
                    </div>
                  </el-step>
                  <el-step
                    title="配送中"
                    :description="selectedOrder.riderName ? `骑手 ${selectedOrder.riderName} 正在配送` : ''"
                  >
                    <div slot="icon" class="step-icon">
                      <i class="el-icon-location-outline"></i>
                    </div>
                  </el-step>
                  <el-step
                    title="已送达"
                    :description="selectedOrder.finishTime || ''"
                  >
                    <div slot="icon" class="step-icon">
                      <i class="el-icon-circle-check"></i>
                    </div>
                  </el-step>
                </el-steps>

                <div v-if="selectedOrder.status === 'delivering'" class="delivery-map">
                  <div class="map-placeholder">
                    <i class="el-icon-map-location"></i>
                    <p>骑手正在前往目的地</p>
                    <p class="estimate-time">预计 15 分钟内送达</p>
                  </div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <div v-else>
        <el-card>
          <el-table :data="filteredOrders" border stripe v-loading="refreshing">
            <el-table-column prop="id" label="订单号" width="170" />
            <el-table-column prop="merchantName" label="商家" width="120" />
            <el-table-column prop="districtName" label="区域" width="90" />
            <el-table-column prop="customerName" label="收货人" width="90" />
            <el-table-column label="收货地址" min-width="200">
              <template slot-scope="scope">
                <span class="address-text">{{ scope.row.address }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="riderName" label="骑手" width="90" />
            <el-table-column label="支付状态" width="90" align="center">
              <template slot-scope="scope">
                <el-tag :type="getStatusType(scope.row.paymentStatus)" size="mini">
                  {{ getPaymentStatusText(scope.row.paymentStatus) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="配送状态" width="90" align="center">
              <template slot-scope="scope">
                <el-tag :type="getStatusType(scope.row.status)" size="mini">
                  {{ getStatusText(scope.row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="createTime" label="下单时间" width="160" />
            <el-table-column label="操作" width="100" align="center">
              <template slot-scope="scope">
                <el-button type="text" @click="viewDelivery(scope.row)">
                  查看详情
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </div>

      <div v-if="selectedOrder" class="back-btn-wrapper">
        <el-button type="primary" @click="selectedOrder = null">
          <i class="el-icon-arrow-left"></i> 返回列表
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { deliveryStatusMap, paymentStatusMap } from '@/mock/data'

export default {
  name: 'Delivery',
  data() {
    return {
      searchForm: {
        orderId: '',
        status: ''
      },
      selectedOrder: null,
      autoRefresh: false,
      refreshInterval: 5000,
      lastRefreshTime: '',
      refreshing: false,
      refreshTimer: null
    }
  },
  computed: {
    ...mapState(['orders']),
    filteredOrders() {
      let result = this.orders
      if (this.searchForm.orderId) {
        result = result.filter(o =>
          o.id.toLowerCase().includes(this.searchForm.orderId.toLowerCase())
        )
      }
      if (this.searchForm.status) {
        result = result.filter(o => o.status === this.searchForm.status)
      }
      return result
    }
  },
  mounted() {
    this.updateLastRefreshTime()
  },
  beforeDestroy() {
    this.clearRefreshTimer()
  },
  methods: {
    getStatusText(status) {
      return deliveryStatusMap[status]?.text || status
    },
    getPaymentStatusText(status) {
      return paymentStatusMap[status]?.text || status
    },
    getStatusType(status) {
      const typeMap = {
        pending: 'info',
        preparing: 'warning',
        delivering: 'primary',
        delivered: 'success',
        cancelled: 'danger',
        unpaid: 'warning',
        paid: 'success',
        refunded: 'info'
      }
      return typeMap[status] || 'info'
    },
    getStepIndex(status) {
      const stepMap = {
        pending: 0,
        preparing: 1,
        delivering: 3,
        delivered: 4
      }
      return stepMap[status] || 0
    },
    handleSearch() {
      if (this.searchForm.orderId) {
        const order = this.orders.find(o =>
          o.id.toLowerCase().includes(this.searchForm.orderId.toLowerCase())
        )
        if (order) {
          this.selectedOrder = order
        } else {
          this.$message.warning('未找到该订单')
        }
      }
    },
    handleReset() {
      this.searchForm = {
        orderId: '',
        status: ''
      }
      this.selectedOrder = null
    },
    viewDelivery(order) {
      this.selectedOrder = order
    },
    toggleAutoRefresh(val) {
      if (val) {
        this.startAutoRefresh()
        this.$message.success(`已开启自动刷新，每 ${this.refreshInterval / 1000} 秒刷新一次`)
      } else {
        this.clearRefreshTimer()
        this.$message.info('已关闭自动刷新')
      }
    },
    resetAutoRefresh() {
      if (this.autoRefresh) {
        this.clearRefreshTimer()
        this.startAutoRefresh()
      }
    },
    startAutoRefresh() {
      this.refreshTimer = setInterval(() => {
        this.doRefresh()
      }, this.refreshInterval)
    },
    clearRefreshTimer() {
      if (this.refreshTimer) {
        clearInterval(this.refreshTimer)
        this.refreshTimer = null
      }
    },
    manualRefresh() {
      this.doRefresh()
    },
    doRefresh() {
      this.refreshing = true
      setTimeout(() => {
        this.refreshing = false
        this.updateLastRefreshTime()
        if (this.selectedOrder) {
          const updatedOrder = this.orders.find(o => o.id === this.selectedOrder.id)
          if (updatedOrder) {
            const oldStatus = this.selectedOrder.status
            this.selectedOrder = { ...updatedOrder }
            if (oldStatus !== updatedOrder.status) {
              this.$message({
                message: `订单状态已更新：${this.getStatusText(updatedOrder.status)}`,
                type: 'success'
              })
              if (updatedOrder.status === 'delivered' || updatedOrder.status === 'cancelled') {
                this.clearRefreshTimer()
                this.autoRefresh = false
              }
            }
          }
        }
      }, 500)
    },
    updateLastRefreshTime() {
      this.lastRefreshTime = new Date().toLocaleTimeString('zh-CN', { hour12: false })
    }
  }
}
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}
.refresh-time {
  font-size: 12px;
  color: #909399;
}
.card-header {
  font-weight: 600;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.header-tags {
  display: flex;
  gap: 8px;
}
.auto-refresh-indicator {
  font-size: 12px;
  color: #67c23a;
  font-weight: normal;
}
.auto-refresh-indicator i {
  margin-right: 4px;
}
.delivery-detail {
  margin-bottom: 24px;
}
.order-info-item {
  display: flex;
  margin-bottom: 12px;
  font-size: 14px;
}
.order-info-item .label {
  width: 80px;
  color: #909399;
  flex-shrink: 0;
}
.order-info-item .value {
  color: #303133;
  flex: 1;
}
.order-info-item .address {
  line-height: 1.5;
}
.order-divider {
  border-top: 1px solid #ebeef5;
  margin: 20px 0;
}
.section-title {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 12px;
}
.dish-item {
  display: flex;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px dashed #ebeef5;
}
.dish-item:last-child {
  border-bottom: none;
}
.dish-name {
  flex: 1;
}
.dish-quantity {
  color: #909399;
  margin-right: 20px;
}
.dish-price {
  color: #f56c6c;
  font-weight: 600;
}
.order-total {
  margin-top: 16px;
  text-align: right;
  font-size: 16px;
}
.order-total .total-price {
  font-size: 24px;
  font-weight: bold;
  color: #f56c6c;
  margin-left: 8px;
}
.delivery-timeline {
  padding: 20px 0;
}
.step-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #409eff;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}
.cancelled-state {
  text-align: center;
  padding: 60px 20px;
  color: #909399;
}
.cancelled-state i {
  font-size: 60px;
  color: #f56c6c;
  margin-bottom: 16px;
}
.cancelled-state p {
  margin: 8px 0;
}
.cancel-reason {
  color: #606266;
}
.cancel-time {
  font-size: 12px;
}
.delivery-map {
  margin-top: 20px;
  border: 1px dashed #ebeef5;
  border-radius: 8px;
  padding: 40px;
  text-align: center;
}
.map-placeholder {
  color: #909399;
}
.map-placeholder i {
  font-size: 48px;
  color: #409eff;
  margin-bottom: 12px;
}
.map-placeholder p {
  margin: 4px 0;
}
.estimate-time {
  color: #409eff;
  font-weight: 600;
}
.address-text {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.back-btn-wrapper {
  margin-top: 24px;
  text-align: center;
}
</style>
