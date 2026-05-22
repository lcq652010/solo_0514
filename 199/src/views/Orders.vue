<template>
  <div class="orders-page">
    <div class="page-container">
      <div class="page-header">
        <h2 class="page-title">订单管理</h2>
        <div class="header-actions">
          <el-button type="primary" @click="showDetailVisible = false">
            <i class="el-icon-document"></i> 订单列表
          </el-button>
        </div>
      </div>

      <div v-if="!showDetailVisible">
        <el-card>
          <div class="filter-bar">
            <el-form :inline="true" :model="filterForm" label-width="80px">
              <el-row :gutter="16">
                <el-col :span="6">
                  <el-form-item label="订单号">
                    <el-input
                      v-model="filterForm.orderId"
                      placeholder="请输入订单号"
                      clearable
                      style="width: 100%"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="6">
                  <el-form-item label="商家">
                    <el-select
                      v-model="filterForm.merchantId"
                      placeholder="全部商家"
                      clearable
                      style="width: 100%"
                    >
                      <el-option
                        v-for="m in merchants"
                        :key="m.id"
                        :label="m.name"
                        :value="m.id"
                      />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="6">
                  <el-form-item label="区域">
                    <el-select
                      v-model="filterForm.districtId"
                      placeholder="全部区域"
                      clearable
                      style="width: 100%"
                    >
                      <el-option
                        v-for="d in districts"
                        :key="d.id"
                        :label="d.name"
                        :value="d.id"
                      />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="6">
                  <el-form-item label="配送状态">
                    <el-select
                      v-model="filterForm.status"
                      placeholder="全部状态"
                      clearable
                      style="width: 100%"
                    >
                      <el-option label="待接单" value="pending" />
                      <el-option label="备餐中" value="preparing" />
                      <el-option label="配送中" value="delivering" />
                      <el-option label="已送达" value="delivered" />
                      <el-option label="已取消" value="cancelled" />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="6">
                  <el-form-item label="支付状态">
                    <el-select
                      v-model="filterForm.paymentStatus"
                      placeholder="全部状态"
                      clearable
                      style="width: 100%"
                    >
                      <el-option label="待支付" value="unpaid" />
                      <el-option label="已支付" value="paid" />
                      <el-option label="已退款" value="refunded" />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="6">
                  <el-form-item label="下单时间">
                    <el-date-picker
                      v-model="filterForm.date"
                      type="date"
                      placeholder="选择日期"
                      value-format="yyyy-MM-dd"
                      style="width: 100%"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item>
                    <el-button type="primary" @click="handleSearch">
                      <i class="el-icon-search"></i> 搜索
                    </el-button>
                    <el-button @click="handleReset">
                      <i class="el-icon-refresh"></i> 重置
                    </el-button>
                    <span class="result-count">
                      共 <strong>{{ filteredOrders.length }}</strong> 条记录
                    </span>
                  </el-form-item>
                </el-col>
              </el-row>
            </el-form>
          </div>

          <el-table :data="paginatedOrders" border stripe v-loading="loading">
            <el-table-column prop="id" label="订单号" width="170" fixed="left" />
            <el-table-column prop="merchantName" label="商家" width="120" />
            <el-table-column prop="districtName" label="区域" width="90" />
            <el-table-column prop="customerName" label="收货人" width="90" />
            <el-table-column prop="phone" label="联系电话" width="120" />
            <el-table-column label="商品信息" min-width="180">
              <template slot-scope="scope">
                <div class="dish-info">
                  <div v-for="(dish, index) in scope.row.dishes.slice(0, 2)" :key="index">
                    {{ dish.name }} x {{ dish.quantity }}
                  </div>
                  <div v-if="scope.row.dishes.length > 2" class="more-dishes">
                    等 {{ scope.row.dishes.length }} 件商品
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="totalPrice" label="金额" width="90" align="right">
              <template slot-scope="scope">
                <span class="price">¥ {{ scope.row.totalPrice.toFixed(2) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="支付状态" width="90" align="center">
              <template slot-scope="scope">
                <el-tag :type="getPaymentStatusType(scope.row.paymentStatus)" size="mini">
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
            <el-table-column label="操作" width="260" align="center" fixed="right">
              <template slot-scope="scope">
                <el-button type="text" @click="viewDetail(scope.row)">查看</el-button>
                <el-button
                  type="text"
                  @click="confirmOrder(scope.row)"
                  v-if="scope.row.status === 'pending'"
                >
                  接单
                </el-button>
                <el-button
                  type="text"
                  @click="startPrepare(scope.row)"
                  v-if="scope.row.status === 'preparing'"
                >
                  开始配送
                </el-button>
                <el-button
                  type="text"
                  @click="completeOrder(scope.row)"
                  v-if="scope.row.status === 'delivering'"
                >
                  完成配送
                </el-button>
                <el-button
                  type="text"
                  @click="cancelOrder(scope.row)"
                  v-if="scope.row.status === 'pending'"
                >
                  取消
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <div class="pagination-wrapper">
            <el-pagination
              :current-page.sync="currentPage"
              :page-size="pageSize"
              :page-sizes="[5, 10, 20, 50]"
              :total="filteredOrders.length"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleSizeChange"
              @current-change="handlePageChange"
            />
          </div>
        </el-card>
      </div>

      <div v-else>
        <el-card>
          <div class="order-detail-header">
            <el-button @click="showDetailVisible = false">
              <i class="el-icon-arrow-left"></i> 返回列表
            </el-button>
            <h3>订单详情</h3>
          </div>
          <el-descriptions :column="2" border class="mt-24">
            <el-descriptions-item label="订单号">
              {{ currentOrder.id }}
            </el-descriptions-item>
            <el-descriptions-item label="商家">
              {{ currentOrder.merchantName }}
            </el-descriptions-item>
            <el-descriptions-item label="区域">
              {{ currentOrder.districtName }}
            </el-descriptions-item>
            <el-descriptions-item label="订单状态">
              <el-tag :type="getStatusType(currentOrder.status)">
                {{ getStatusText(currentOrder.status) }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="支付状态">
              <el-tag :type="getPaymentStatusType(currentOrder.paymentStatus)">
                {{ getPaymentStatusText(currentOrder.paymentStatus) }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="收货人">
              {{ currentOrder.customerName }}
            </el-descriptions-item>
            <el-descriptions-item label="联系电话">
              {{ currentOrder.phone }}
            </el-descriptions-item>
            <el-descriptions-item label="下单时间">
              {{ currentOrder.createTime }}
            </el-descriptions-item>
            <el-descriptions-item label="收货地址" :span="2">
              {{ currentOrder.address }}
            </el-descriptions-item>
            <el-descriptions-item label="骑手" v-if="currentOrder.riderName">
              {{ currentOrder.riderName }}
            </el-descriptions-item>
            <el-descriptions-item label="完成时间" v-if="currentOrder.finishTime">
              {{ currentOrder.finishTime }}
            </el-descriptions-item>
            <el-descriptions-item label="备注" v-if="currentOrder.remark" :span="2">
              {{ currentOrder.remark }}
            </el-descriptions-item>
          </el-descriptions>

          <h4 class="section-title">商品清单</h4>
          <el-table :data="currentOrder.dishes" border class="mt-16">
            <el-table-column prop="name" label="商品名称" />
            <el-table-column prop="price" label="单价" width="120" align="right">
              <template slot-scope="scope">
                ¥ {{ scope.row.price.toFixed(2) }}
              </template>
            </el-table-column>
            <el-table-column prop="quantity" label="数量" width="100" align="center" />
            <el-table-column label="小计" width="120" align="right">
              <template slot-scope="scope">
                ¥ {{ (scope.row.price * scope.row.quantity).toFixed(2) }}
              </template>
            </el-table-column>
          </el-table>

          <div class="order-total">
            <span>订单金额：</span>
            <span class="total-price">¥ {{ currentOrder.totalPrice.toFixed(2) }}</span>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { deliveryStatusMap, paymentStatusMap, merchants, districts } from '@/mock/data'

export default {
  name: 'Orders',
  data() {
    return {
      merchants,
      districts,
      filterForm: {
        orderId: '',
        merchantId: '',
        districtId: '',
        status: '',
        paymentStatus: '',
        date: ''
      },
      currentPage: 1,
      pageSize: 10,
      showDetailVisible: false,
      currentOrder: {},
      loading: false
    }
  },
  computed: {
    ...mapState(['orders']),
    filteredOrders() {
      let result = this.orders
      if (this.filterForm.orderId) {
        result = result.filter(o => o.id.toLowerCase().includes(this.filterForm.orderId.toLowerCase()))
      }
      if (this.filterForm.merchantId) {
        result = result.filter(o => o.merchantId === this.filterForm.merchantId)
      }
      if (this.filterForm.districtId) {
        result = result.filter(o => o.districtId === this.filterForm.districtId)
      }
      if (this.filterForm.status) {
        result = result.filter(o => o.status === this.filterForm.status)
      }
      if (this.filterForm.paymentStatus) {
        result = result.filter(o => o.paymentStatus === this.filterForm.paymentStatus)
      }
      if (this.filterForm.date) {
        result = result.filter(o => o.createTime.startsWith(this.filterForm.date))
      }
      return result
    },
    paginatedOrders() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredOrders.slice(start, end)
    }
  },
  methods: {
    ...mapActions(['updateOrderStatus', 'cancelOrder']),
    getStatusText(status) {
      return deliveryStatusMap[status]?.text || status
    },
    getStatusType(status) {
      const typeMap = {
        pending: 'info',
        preparing: 'warning',
        delivering: 'primary',
        delivered: 'success',
        cancelled: 'danger'
      }
      return typeMap[status] || 'info'
    },
    getPaymentStatusText(status) {
      return paymentStatusMap[status]?.text || status
    },
    getPaymentStatusType(status) {
      const typeMap = {
        unpaid: 'warning',
        paid: 'success',
        refunded: 'info'
      }
      return typeMap[status] || 'info'
    },
    handleSearch() {
      this.currentPage = 1
      this.loading = true
      setTimeout(() => {
        this.loading = false
      }, 300)
    },
    handleReset() {
      this.filterForm = {
        orderId: '',
        merchantId: '',
        districtId: '',
        status: '',
        paymentStatus: '',
        date: ''
      }
      this.currentPage = 1
    },
    handlePageChange(page) {
      this.currentPage = page
    },
    handleSizeChange(size) {
      this.pageSize = size
      this.currentPage = 1
    },
    viewDetail(order) {
      this.currentOrder = order
      this.showDetailVisible = true
    },
    confirmOrder(order) {
      this.$confirm('确认接单吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.updateOrderStatus({ orderId: order.id, status: 'preparing' })
        this.$message.success('接单成功！')
      }).catch(() => {})
    },
    startPrepare(order) {
      this.$confirm('订单已备餐完成，可以开始配送了吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message.success('请前往骑手派单页面分配骑手！')
        this.$router.push('/dispatch')
      }).catch(() => {})
    },
    completeOrder(order) {
      this.$confirm('确认订单已送达吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.updateOrderStatus({
          orderId: order.id,
          status: 'delivered',
          extra: { finishTime: new Date().toLocaleString('zh-CN', { hour12: false }).replace(/\//g, '-') }
        })
        this.$message.success('订单已完成！')
      }).catch(() => {})
    },
    cancelOrder(order) {
      this.$prompt('请输入取消原因', '取消订单', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPattern: /.+/,
        inputErrorMessage: '请输入取消原因'
      }).then(({ value }) => {
        this.cancelOrder({ orderId: order.id, reason: value })
        this.$message.success('订单已取消！')
      }).catch(() => {})
    }
  }
}
</script>

<style scoped>
.filter-bar {
  margin-bottom: 20px;
  padding: 16px;
  background-color: #f5f7fa;
  border-radius: 4px;
}
.filter-bar :deep(.el-form-item) {
  margin-bottom: 12px;
}
.result-count {
  margin-left: 16px;
  color: #909399;
  font-size: 13px;
}
.result-count strong {
  color: #409eff;
  font-size: 16px;
  margin: 0 4px;
}
.price {
  color: #f56c6c;
  font-weight: 600;
}
.dish-info {
  font-size: 12px;
  color: #606266;
}
.dish-info div {
  margin-bottom: 2px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.more-dishes {
  color: #909399;
}
.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
.order-detail-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #ebeef5;
}
.order-detail-header h3 {
  margin: 0;
}
.section-title {
  margin-top: 24px;
  font-size: 16px;
  font-weight: 600;
}
.order-total {
  margin-top: 24px;
  text-align: right;
  font-size: 16px;
}
.order-total .total-price {
  font-size: 24px;
  font-weight: bold;
  color: #f56c6c;
  margin-left: 8px;
}
</style>
