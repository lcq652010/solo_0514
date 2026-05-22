<template>
  <div class="orders-container" ref="container">
    <el-card>
      <div slot="header" class="card-header">
        <span>订单列表</span>
        <el-button type="primary" icon="el-icon-refresh" @click="refreshOrders">刷新订单</el-button>
      </div>
      
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="订单号">
          <el-input v-model="searchForm.orderId" placeholder="请输入订单号" clearable style="width: 160px;"></el-input>
        </el-form-item>
        <el-form-item label="订单状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable style="width: 140px;">
            <el-option label="全部" value=""></el-option>
            <el-option v-for="(item, key) in orderStatusMap" :key="key" :label="item.label" :value="parseInt(key)"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="订单类型">
          <el-select v-model="searchForm.type" placeholder="请选择类型" clearable style="width: 120px;">
            <el-option label="全部" value=""></el-option>
            <el-option label="外卖" :value="1"></el-option>
            <el-option label="堂食" :value="2"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="下单时间">
          <el-date-picker
            v-model="searchForm.dateRange"
            type="datetimerange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            value-format="yyyy-MM-dd HH:mm:ss"
            style="width: 320px;">
          </el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
          <el-button icon="el-icon-refresh" @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
      
      <el-table :data="paginatedOrders" border stripe style="width: 100%" row-class-name="getRowClassName" ref="orderTable">
        <el-table-column prop="id" label="订单号" width="180" align="center"></el-table-column>
        <el-table-column prop="customerName" label="顾客姓名" width="100" align="center"></el-table-column>
        <el-table-column prop="phone" label="联系电话" width="120" align="center"></el-table-column>
        <el-table-column prop="address" label="收货地址" min-width="200" align="center" show-overflow-tooltip></el-table-column>
        <el-table-column prop="totalPrice" label="订单金额" width="100" align="center">
          <template slot-scope="scope">
            <span style="color: #f56c6c; font-weight: bold;">¥{{ scope.row.totalPrice }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="type" label="订单类型" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.type === 1 ? 'success' : 'primary'">
              {{ orderTypeMap[scope.row.type] }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="订单状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="orderStatusMap[scope.row.status].type">
              {{ orderStatusMap[scope.row.status].label }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" width="120" align="center" show-overflow-tooltip></el-table-column>
        <el-table-column prop="createTime" label="下单时间" width="180" align="center"></el-table-column>
        <el-table-column label="操作" width="150" align="center">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" icon="el-icon-view" @click="handleView(scope.row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-container">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.currentPage"
          :page-sizes="[5, 10, 20, 50]"
          :page-size="pagination.pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total">
        </el-pagination>
      </div>
    </el-card>

    <el-dialog title="订单详情" :visible.sync="detailDialogVisible" width="600px">
      <div v-if="currentOrder">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="订单号">{{ currentOrder.id }}</el-descriptions-item>
          <el-descriptions-item label="下单时间">{{ currentOrder.createTime }}</el-descriptions-item>
          <el-descriptions-item label="顾客姓名">{{ currentOrder.customerName }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ currentOrder.phone }}</el-descriptions-item>
          <el-descriptions-item label="收货地址" :span="2">{{ currentOrder.address }}</el-descriptions-item>
          <el-descriptions-item label="订单类型">
            <el-tag :type="currentOrder.type === 1 ? 'success' : 'primary'">
              {{ orderTypeMap[currentOrder.type] }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="订单状态">
            <el-tag :type="orderStatusMap[currentOrder.status].type">
              {{ orderStatusMap[currentOrder.status].label }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="备注" :span="2">{{ currentOrder.remark || '无' }}</el-descriptions-item>
        </el-descriptions>
        
        <h4 style="margin: 20px 0 10px;">订单菜品</h4>
        <el-table :data="currentOrder.dishes" border size="small">
          <el-table-column prop="name" label="菜品名称" align="center"></el-table-column>
          <el-table-column prop="price" label="单价" width="100" align="center">
            <template slot-scope="scope">¥{{ scope.row.price }}</template>
          </el-table-column>
          <el-table-column prop="quantity" label="数量" width="100" align="center"></el-table-column>
          <el-table-column label="小计" width="100" align="center">
            <template slot-scope="scope">¥{{ scope.row.price * scope.row.quantity }}</template>
          </el-table-column>
        </el-table>
        
        <div style="text-align: right; margin-top: 15px; font-size: 18px;">
          订单总计：<span style="color: #f56c6c; font-weight: bold;">¥{{ currentOrder.totalPrice }}</span>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mockOrders, orderStatusMap, orderTypeMap } from '../data/mockData'

export default {
  name: 'Orders',
  data() {
    return {
      orders: [],
      orderStatusMap,
      orderTypeMap,
      searchForm: {
        orderId: '',
        status: '',
        type: '',
        dateRange: []
      },
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      detailDialogVisible: false,
      currentOrder: null,
      highlightedOrderId: null
    }
  },
  computed: {
    filteredOrders() {
      return this.orders.filter(order => {
        const matchOrderId = !this.searchForm.orderId || order.id.includes(this.searchForm.orderId)
        const matchStatus = this.searchForm.status === '' || order.status === this.searchForm.status
        const matchType = this.searchForm.type === '' || order.type === this.searchForm.type
        
        let matchDate = true
        if (this.searchForm.dateRange && this.searchForm.dateRange.length === 2) {
          const orderDate = new Date(order.createTime)
          const startDate = new Date(this.searchForm.dateRange[0])
          const endDate = new Date(this.searchForm.dateRange[1])
          matchDate = orderDate >= startDate && orderDate <= endDate
        }
        
        return matchOrderId && matchStatus && matchType && matchDate
      })
    },
    paginatedOrders() {
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      return this.filteredOrders.slice(start, end)
    }
  },
  created() {
    this.orders = [...mockOrders]
    this.pagination.total = this.orders.length
    this.$bus.$on('orderStatusChanged', this.handleOrderStatusChange)
    this.$bus.$on('newOrderReceived', this.handleNewOrder)
  },
  beforeDestroy() {
    this.$bus.$off('orderStatusChanged', this.handleOrderStatusChange)
    this.$bus.$off('newOrderReceived', this.handleNewOrder)
  },
  methods: {
    getRowClassName({ row }) {
      return row.id === this.highlightedOrderId ? 'highlight-row' : ''
    },
    handleSearch() {
      this.pagination.currentPage = 1
      this.pagination.total = this.filteredOrders.length
      this.$message.success('搜索完成')
    },
    handleReset() {
      this.searchForm = {
        orderId: '',
        status: '',
        type: '',
        dateRange: []
      }
      this.pagination.currentPage = 1
      this.pagination.total = this.orders.length
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.pagination.currentPage = 1
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
    },
    handleView(row) {
      this.currentOrder = { ...row }
      this.detailDialogVisible = true
    },
    refreshOrders() {
      this.pagination.total = this.filteredOrders.length
      this.$message.success('订单列表已刷新')
    },
    handleOrderStatusChange(orderId) {
      const order = this.orders.find(o => o.id === orderId)
      if (order) {
        this.highlightedOrderId = orderId
        setTimeout(() => {
          this.highlightedOrderId = null
        }, 3000)
      }
      this.pagination.total = this.filteredOrders.length
    },
    handleNewOrder(order) {
      this.orders.unshift(order)
      this.pagination.total = this.filteredOrders.length
      this.pagination.currentPage = 1
      this.highlightedOrderId = order.id
      
      this.$nextTick(() => {
        const table = this.$refs.orderTable
        if (table && table.$el) {
          table.$el.scrollIntoView({ behavior: 'smooth', block: 'start' })
        }
      })
      
      setTimeout(() => {
        this.highlightedOrderId = null
      }, 5000)
    }
  }
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.orders-container {
  padding: 0;
}

.search-form {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style>

<style>
.el-table .highlight-row {
  background-color: #fff7e6 !important;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    background-color: #fff7e6;
  }
  50% {
    background-color: #ffecd2;
  }
}
</style>