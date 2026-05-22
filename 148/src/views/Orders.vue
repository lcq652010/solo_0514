<template>
  <div class="orders-page">
    <h1 class="page-title">我的订单</h1>
    
    <el-card class="filter-card card-shadow mb-20">
      <el-form :inline="true" :model="filters" class="filter-form">
        <el-form-item label="电影名称">
          <el-select 
            v-model="filters.movieTitle" 
            placeholder="请选择电影" 
            clearable 
            style="width: 200px"
            filterable
          >
            <el-option
              v-for="title in movieTitles"
              :key="title"
              :label="title"
              :value="title"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="场次时间">
          <el-input 
            v-model="filters.sessionTime" 
            placeholder="搜索场次" 
            style="width: 200px"
            clearable
          ></el-input>
        </el-form-item>
        <el-form-item label="支付状态">
          <el-select v-model="filters.status" placeholder="请选择" style="width: 150px" clearable>
            <el-option label="全部" value="all"></el-option>
            <el-option label="待使用" value="paid"></el-option>
            <el-option label="已完成" value="completed"></el-option>
            <el-option label="已退票" value="refunded"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="applyFilter">查询</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-card class="card-shadow">
      <el-table :data="paginatedOrders" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="订单号" width="200" show-overflow-tooltip>
          <template slot-scope="scope">
            <span style="color: #409eff">{{ scope.row.id }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="movieTitle" label="电影名称" min-width="150" show-overflow-tooltip>
        </el-table-column>
        <el-table-column prop="cinemaName" label="影院" min-width="180" show-overflow-tooltip>
        </el-table-column>
        <el-table-column prop="sessionTime" label="场次" width="180" show-overflow-tooltip>
        </el-table-column>
        <el-table-column prop="seats" label="座位" width="150" show-overflow-tooltip>
          <template slot-scope="scope">
            {{ scope.row.seats.join('、') }}
          </template>
        </el-table-column>
        <el-table-column prop="quantity" label="数量" width="80" align="center">
        </el-table-column>
        <el-table-column prop="totalPrice" label="金额" width="100" align="center">
          <template slot-scope="scope">
            <span style="color: #f56c6c; font-weight: 600">¥{{ scope.row.totalPrice }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="small">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="下单时间" width="180" show-overflow-tooltip>
        </el-table-column>
        <el-table-column label="操作" width="150" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button 
              v-if="scope.row.status === 'paid'"
              type="text" 
              size="small" 
              @click="viewTicket(scope.row)"
            >
              查看票券
            </el-button>
            <el-button 
              v-if="scope.row.status === 'paid'"
              type="text" 
              size="small" 
              style="color: #f56c6c"
              @click="refundTicket(scope.row)"
            >
              退票
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-wrapper">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[5, 10, 20]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="filteredOrders.length"
        >
        </el-pagination>
      </div>
    </el-card>
    
    <el-dialog
      title="电影票详情"
      :visible.sync="ticketDialogVisible"
      width="500px"
    >
      <div v-if="currentOrder" class="ticket-detail">
        <div class="ticket-header">
          <h3>{{ currentOrder.movieTitle }}</h3>
          <el-tag type="success">购票成功</el-tag>
        </div>
        <div class="ticket-info">
          <p><span>影院：</span>{{ currentOrder.cinemaName }}</p>
          <p><span>影厅：</span>{{ currentOrder.hall }}</p>
          <p><span>场次：</span>{{ currentOrder.sessionTime }}</p>
          <p><span>座位：</span>{{ currentOrder.seats.join('、') }}</p>
          <p><span>数量：</span>{{ currentOrder.quantity }}张</p>
          <p><span>金额：</span><span class="price">¥{{ currentOrder.totalPrice }}</span></p>
          <p><span>手机号：</span>{{ currentOrder.phone }}</p>
          <p><span>订单号：</span>{{ currentOrder.id }}</p>
          <p><span>下单时间：</span>{{ currentOrder.createTime }}</p>
        </div>
        <div class="qr-code">
          <div class="qr-placeholder">
            <i class="el-icon-picture-outline"></i>
            <p>二维码</p>
          </div>
          <p class="qr-tip">请提前15分钟到影院取票</p>
        </div>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="ticketDialogVisible = false">关闭</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import orderStore from '@/store/orderStore.js'

export default {
  name: 'Orders',
  data() {
    return {
      orders: [],
      movieTitles: [],
      loading: false,
      currentPage: 1,
      pageSize: 10,
      ticketDialogVisible: false,
      currentOrder: null,
      filters: {
        movieTitle: '',
        sessionTime: '',
        status: 'all'
      },
      refreshTimer: null,
      unsubscribe: null
    }
  },
  computed: {
    filteredOrders() {
      return orderStore.filterOrders(this.filters)
    },
    paginatedOrders() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredOrders.slice(start, end)
    }
  },
  mounted() {
    this.loadOrders()
    this.startAutoRefresh()
    this.unsubscribe = orderStore.subscribe(() => {
      this.orders = orderStore.getOrders()
      this.updateMovieTitles()
    })
  },
  beforeDestroy() {
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer)
    }
    if (this.unsubscribe) {
      this.unsubscribe()
    }
  },
  methods: {
    loadOrders() {
      this.loading = true
      setTimeout(() => {
        this.orders = orderStore.getOrders()
        this.updateMovieTitles()
        this.loading = false
      }, 300)
    },
    updateMovieTitles() {
      this.movieTitles = orderStore.getUniqueMovieTitles()
    },
    startAutoRefresh() {
      this.refreshTimer = setInterval(() => {
        this.loadOrders()
      }, 10000)
    },
    applyFilter() {
      this.currentPage = 1
    },
    resetFilter() {
      this.filters = {
        movieTitle: '',
        sessionTime: '',
        status: 'all'
      }
      this.currentPage = 1
    },
    getStatusType(status) {
      const map = {
        paid: 'success',
        completed: 'info',
        refunded: 'warning'
      }
      return map[status] || 'info'
    },
    getStatusText(status) {
      const map = {
        paid: '待使用',
        completed: '已完成',
        refunded: '已退票'
      }
      return map[status] || status
    },
    handleSizeChange(val) {
      this.pageSize = val
    },
    handleCurrentChange(val) {
      this.currentPage = val
    },
    viewTicket(order) {
      this.currentOrder = order
      this.ticketDialogVisible = true
    },
    refundTicket(order) {
      this.$confirm('确定要退票吗？退票后金额将原路返回。', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        orderStore.updateOrderStatus(order.id, 'refunded')
        this.$message.success('退票成功！')
      }).catch(() => {})
    }
  }
}
</script>

<style scoped>
.filter-card {
  padding: 15px 20px;
}

.filter-form {
  margin-bottom: 0;
}

.pagination-wrapper {
  margin-top: 20px;
  text-align: right;
}

.ticket-detail {
  padding: 10px 0;
}

.ticket-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
  margin-bottom: 15px;
}

.ticket-header h3 {
  margin: 0;
  font-size: 20px;
}

.ticket-info p {
  margin: 12px 0;
  line-height: 1.6;
}

.ticket-info p span:first-child {
  display: inline-block;
  width: 80px;
  color: #909399;
}

.ticket-info .price {
  color: #f56c6c;
  font-weight: 600;
  font-size: 18px;
}

.qr-code {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px dashed #ebeef5;
  text-align: center;
}

.qr-placeholder {
  width: 150px;
  height: 150px;
  margin: 0 auto 10px;
  background: #f5f7fa;
  border: 1px dashed #dcdfe6;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #c0c4cc;
}

.qr-placeholder i {
  font-size: 48px;
  margin-bottom: 10px;
}

.qr-placeholder p {
  margin: 0;
}

.qr-tip {
  color: #909399;
  font-size: 12px;
}
</style>
