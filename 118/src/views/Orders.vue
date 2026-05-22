<template>
  <div class="orders-page">
    <el-card>
      <div slot="header" class="clearfix">
        <span class="card-title">订单列表</span>
      </div>
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="订单号">
          <el-input v-model="searchForm.orderNo" placeholder="请输入订单号" clearable style="width: 150px;"></el-input>
        </el-form-item>
        <el-form-item label="顾客姓名">
          <el-input v-model="searchForm.customerName" placeholder="请输入姓名" clearable style="width: 120px;"></el-input>
        </el-form-item>
        <el-form-item label="制作状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable style="width: 120px;">
            <el-option label="待制作" value="pending"></el-option>
            <el-option label="制作中" value="making"></el-option>
            <el-option label="已完成" value="completed"></el-option>
            <el-option label="已取消" value="cancelled"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="支付状态">
          <el-select v-model="searchForm.paymentStatus" placeholder="请选择" clearable style="width: 120px;">
            <el-option label="已支付" value="paid"></el-option>
            <el-option label="未支付" value="unpaid"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="下单时间">
          <el-date-picker
            v-model="searchForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            style="width: 240px;"
          ></el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="searchOrders">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
      <el-table :data="filteredOrders" border stripe style="width: 100%">
        <el-table-column prop="orderNo" label="订单号" width="160"></el-table-column>
        <el-table-column prop="customerName" label="顾客姓名" width="100"></el-table-column>
        <el-table-column prop="phone" label="联系电话" width="120"></el-table-column>
        <el-table-column prop="takeType" label="取餐方式" width="90">
          <template slot-scope="scope">
            <el-tag :type="scope.row.takeType === '堂食' ? '' : 'warning'" size="mini">{{ scope.row.takeType }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="paymentStatus" label="支付状态" width="90">
          <template slot-scope="scope">
            <el-tag :type="scope.row.paymentStatus === 'paid' ? 'success' : 'danger'" size="mini">
              {{ scope.row.paymentStatus === 'paid' ? '已支付' : '未支付' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="totalAmount" label="订单金额" width="100">
          <template slot-scope="scope">
            <span class="amount">¥{{ scope.row.totalAmount }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="制作状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="mini">{{ getStatusText(scope.row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="下单时间" width="170"></el-table-column>
        <el-table-column label="操作" fixed="right" width="200">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="viewOrder(scope.row)">查看</el-button>
            <el-button
              size="mini"
              type="success"
              @click="updateStatus(scope.row, 'making')"
              v-if="scope.row.status === 'pending'"
            >
              开始制作
            </el-button>
            <el-button
              size="mini"
              type="success"
              @click="updateStatus(scope.row, 'completed')"
              v-if="scope.row.status === 'making'"
            >
              制作完成
            </el-button>
            <el-button
              size="mini"
              type="danger"
              @click="cancelOrder(scope.row)"
              v-if="scope.row.status === 'pending'"
            >
              取消订单
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-empty v-if="filteredOrders.length === 0 && pagination.total === 0" description="暂无订单数据" style="margin-top: 50px;"></el-empty>
      <div class="pagination-container" v-if="pagination.total > 0">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pagination.pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
        ></el-pagination>
      </div>
    </el-card>

    <el-dialog title="订单详情" :visible.sync="detailDialogVisible" width="600px">
      <el-descriptions :column="2" border v-if="currentOrder">
        <el-descriptions-item label="订单号">{{ currentOrder.orderNo }}</el-descriptions-item>
        <el-descriptions-item label="顾客姓名">{{ currentOrder.customerName }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ currentOrder.phone }}</el-descriptions-item>
        <el-descriptions-item label="取餐方式">
          <el-tag :type="currentOrder.takeType === '堂食' ? '' : 'warning'" size="mini">{{ currentOrder.takeType }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="支付状态">
          <el-tag :type="currentOrder.paymentStatus === 'paid' ? 'success' : 'danger'" size="mini">
            {{ currentOrder.paymentStatus === 'paid' ? '已支付' : '未支付' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="制作状态">
          <el-tag :type="getStatusType(currentOrder.status)" size="mini">{{ getStatusText(currentOrder.status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="下单时间" :span="2">{{ currentOrder.createTime }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentOrder.remark || '无' }}</el-descriptions-item>
      </el-descriptions>
      <div class="order-items" style="margin-top: 20px;">
        <h4>订单明细</h4>
        <el-table :data="currentOrder.items" size="small" border>
          <el-table-column prop="name" label="商品" width="120"></el-table-column>
          <el-table-column prop="specsText" label="规格"></el-table-column>
          <el-table-column prop="quantity" label="数量" width="80"></el-table-column>
          <el-table-column prop="unitPrice" label="单价" width="80"></el-table-column>
          <el-table-column prop="totalPrice" label="小计" width="80"></el-table-column>
        </el-table>
        <div class="order-total" style="text-align: right; margin-top: 15px;">
          订单总计：<span class="total-amount">¥{{ currentOrder.totalAmount }}</span>
        </div>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { EventBus } from '@/utils/eventBus'
export default {
  name: 'Orders',
  data() {
    return {
      searchForm: {
        orderNo: '',
        customerName: '',
        status: '',
        paymentStatus: '',
        dateRange: []
      },
      orders: [],
      detailDialogVisible: false,
      currentOrder: null,
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      }
    }
  },
  computed: {
    filteredOrders() {
      let result = [...this.orders]
      if (this.searchForm.orderNo) {
        result = result.filter(o => o.orderNo.includes(this.searchForm.orderNo))
      }
      if (this.searchForm.customerName) {
        result = result.filter(o => o.customerName.includes(this.searchForm.customerName))
      }
      if (this.searchForm.status) {
        result = result.filter(o => o.status === this.searchForm.status)
      }
      if (this.searchForm.paymentStatus) {
        result = result.filter(o => o.paymentStatus === this.searchForm.paymentStatus)
      }
      if (this.searchForm.dateRange && this.searchForm.dateRange.length === 2) {
        const startDate = new Date(this.searchForm.dateRange[0]).setHours(0, 0, 0, 0)
        const endDate = new Date(this.searchForm.dateRange[1]).setHours(23, 59, 59, 999)
        result = result.filter(o => {
          const orderTime = new Date(o.timestamp || o.createTime).getTime()
          return orderTime >= startDate && orderTime <= endDate
        })
      }
      this.pagination.total = result.length
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      return result.slice(start, end)
    }
  },
  created() {
    this.loadOrders()
    EventBus.$on('orderStatusChanged', () => {
      this.loadOrders()
    })
  },
  beforeDestroy() {
    EventBus.$off('orderStatusChanged')
  },
  methods: {
    loadOrders() {
      this.orders = JSON.parse(localStorage.getItem('milkTeaOrders') || '[]')
    },
    searchOrders() {
      this.pagination.currentPage = 1
      this.loadOrders()
    },
    resetSearch() {
      this.searchForm = {
        orderNo: '',
        customerName: '',
        status: '',
        paymentStatus: '',
        dateRange: []
      }
      this.pagination.currentPage = 1
      this.loadOrders()
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.pagination.currentPage = 1
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
    },
    getStatusType(status) {
      const types = {
        pending: 'warning',
        making: 'primary',
        completed: 'success',
        cancelled: 'danger'
      }
      return types[status] || 'info'
    },
    getStatusText(status) {
      const texts = {
        pending: '待制作',
        making: '制作中',
        completed: '已完成',
        cancelled: '已取消'
      }
      return texts[status] || status
    },
    viewOrder(order) {
      this.currentOrder = order
      this.detailDialogVisible = true
    },
    updateStatus(order, status) {
      const index = this.orders.findIndex(o => o.id === order.id)
      if (index !== -1) {
        this.orders[index].status = status
        localStorage.setItem('milkTeaOrders', JSON.stringify(this.orders))
        EventBus.$emit('orderStatusChanged')
        this.$message.success(`订单状态已更新为${this.getStatusText(status)}`)
      }
    },
    cancelOrder(order) {
      this.$confirm('确定要取消该订单吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.updateStatus(order, 'cancelled')
      }).catch(() => {})
    }
  }
}
</script>

<style lang="scss" scoped>
.orders-page {
  .search-form {
    margin-bottom: 20px;
  }
  .amount {
    font-weight: bold;
    color: #f56c6c;
  }
}
.order-items {
    h4 {
      margin-bottom: 10px;
      color: #303133;
    }
    .order-total {
      font-size: 16px;
      .total-amount {
        font-size: 24px;
        font-weight: bold;
        color: #f56c6c;
      }
    }
  }
  .pagination-container {
    margin-top: 20px;
    text-align: right;
  }
}
</style>
