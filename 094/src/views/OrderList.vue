<template>
  <div class="page-container">
    <h2 class="page-title">
      <i class="el-icon-s-order"></i>
      订单列表
    </h2>
    
    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="订单号">
          <el-input v-model="filterForm.orderId" placeholder="请输入订单号" clearable></el-input>
        </el-form-item>
        <el-form-item label="门票类型">
          <el-select v-model="filterForm.ticketId" placeholder="请选择门票类型" clearable>
            <el-option 
              v-for="ticket in ticketTypes" 
              :key="ticket.id" 
              :label="ticket.name" 
              :value="ticket.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="订单状态">
          <el-select v-model="filterForm.status" placeholder="请选择状态" clearable>
            <el-option label="已支付" value="paid"></el-option>
            <el-option label="待使用" value="unused"></el-option>
            <el-option label="已使用" value="used"></el-option>
            <el-option label="已取消" value="cancelled"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="核销状态">
          <el-select v-model="filterForm.checkedStatus" placeholder="请选择核销状态" clearable>
            <el-option label="已核销" value="checked"></el-option>
            <el-option label="未核销" value="unchecked"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="预订日期">
          <el-date-picker
            v-model="filterForm.bookDateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            clearable
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="入园日期">
          <el-date-picker
            v-model="filterForm.visitDate"
            type="date"
            placeholder="选择日期"
            clearable
          ></el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleFilter" icon="el-icon-search">查询</el-button>
          <el-button @click="handleReset" icon="el-icon-refresh">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-card class="table-card" style="margin-top: 20px;">
      <el-table :data="filteredOrders" border style="width: 100%" v-loading="loading" row-class-name="getRowClassName">
        <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
        <el-table-column prop="id" label="订单号" width="180" show-overflow-tooltip></el-table-column>
        <el-table-column prop="ticketName" label="门票类型" width="120"></el-table-column>
        <el-table-column prop="quantity" label="数量" width="80" align="center"></el-table-column>
        <el-table-column prop="totalPrice" label="金额" width="100" align="center">
          <template slot-scope="scope">
            <span style="color: #f56c6c; font-weight: bold;">¥{{ scope.row.totalPrice }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="visitorName" label="游客姓名" width="100"></el-table-column>
        <el-table-column prop="visitDate" label="入园日期" width="120"></el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === 'used' ? 'danger' : statusMap[scope.row.status].type" size="small">
              <i v-if="scope.row.status === 'used'" class="el-icon-check"></i>
              {{ statusMap[scope.row.status].label }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="预订时间" width="160"></el-table-column>
        <el-table-column label="操作" width="220" fixed="right">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="handleView(scope.row)">详情</el-button>
            <el-button 
              size="mini" 
              :type="scope.row.status === 'used' ? 'info' : 'warning'" 
              @click="handleCancel(scope.row)"
              :disabled="scope.row.status === 'used' || scope.row.status === 'cancelled'"
            >
              {{ scope.row.status === 'used' ? '已核销' : '取消' }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <el-pagination
        class="pagination"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="pagination.currentPage"
        :page-sizes="[5, 10, 20, 50]"
        :page-size="pagination.pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="pagination.total"
      ></el-pagination>
    </el-card>
    
    <el-dialog title="订单详情" :visible.sync="dialogVisible" width="600px">
      <div v-if="currentOrder" class="order-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="订单号">{{ currentOrder.id }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ currentOrder.createTime }}</el-descriptions-item>
          <el-descriptions-item label="门票类型">{{ currentOrder.ticketName }}</el-descriptions-item>
          <el-descriptions-item label="购票数量">{{ currentOrder.quantity }}</el-descriptions-item>
          <el-descriptions-item label="订单金额">
            <span style="color: #f56c6c; font-weight: bold;">¥{{ currentOrder.totalPrice }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="入园日期">{{ currentOrder.visitDate }}</el-descriptions-item>
          <el-descriptions-item label="游客姓名">{{ currentOrder.visitorName }}</el-descriptions-item>
          <el-descriptions-item label="手机号码">{{ currentOrder.visitorPhone }}</el-descriptions-item>
          <el-descriptions-item label="身份证号">{{ currentOrder.visitorIdCard }}</el-descriptions-item>
          <el-descriptions-item label="取票码">{{ currentOrder.ticketCode }}</el-descriptions-item>
          <el-descriptions-item label="订单状态" :span="2">
            <el-tag :type="statusMap[currentOrder.status].type" size="small">
              {{ statusMap[currentOrder.status].label }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">关闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { orders, statusMap, ticketTypes } from '@/data/mockData'
import { EventBus } from '@/utils/eventBus'

export default {
  name: 'OrderList',
  data() {
    return {
      orderList: orders,
      statusMap: statusMap,
      ticketTypes: ticketTypes,
      filterForm: {
        orderId: '',
        ticketId: '',
        status: '',
        checkedStatus: '',
        bookDateRange: [],
        visitDate: ''
      },
      loading: false,
      dialogVisible: false,
      currentOrder: null,
      lastCheckedOrder: null,
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: orders.length
      }
    }
  },
  computed: {
    filteredOrders() {
      let list = [...this.orderList]
      
      if (this.filterForm.orderId) {
        list = list.filter(item => item.id.includes(this.filterForm.orderId))
      }
      
      if (this.filterForm.ticketId) {
        list = list.filter(item => item.ticketId === this.filterForm.ticketId)
      }
      
      if (this.filterForm.status) {
        list = list.filter(item => item.status === this.filterForm.status)
      }
      
      if (this.filterForm.checkedStatus) {
        if (this.filterForm.checkedStatus === 'checked') {
          list = list.filter(item => item.status === 'used')
        } else if (this.filterForm.checkedStatus === 'unchecked') {
          list = list.filter(item => item.status !== 'used' && item.status !== 'cancelled')
        }
      }
      
      if (this.filterForm.bookDateRange && this.filterForm.bookDateRange.length === 2) {
        const startDate = this.formatDate(this.filterForm.bookDateRange[0])
        const endDate = this.formatDate(this.filterForm.bookDateRange[1])
        list = list.filter(item => {
          const createDate = item.createTime.split(' ')[0]
          return createDate >= startDate && createDate <= endDate
        })
      }
      
      if (this.filterForm.visitDate) {
        const dateStr = this.formatDate(this.filterForm.visitDate)
        list = list.filter(item => item.visitDate === dateStr)
      }
      
      this.pagination.total = list.length
      
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      return list.slice(start, end)
    }
  },
  mounted() {
    EventBus.$on('order-checked', (data) => {
      this.handleOrderChecked(data)
    })
  },
  beforeDestroy() {
    EventBus.$off('order-checked')
  },
  methods: {
    handleOrderChecked(data) {
      this.lastCheckedOrder = data.orderId
      this.$message.success({
        message: `订单 ${data.orderId} 已核销，列表已自动刷新`,
        duration: 3000
      })
      this.loading = true
      setTimeout(() => {
        this.loading = false
      }, 500)
    },
    getRowClassName({ row }) {
      if (row.status === 'used') {
        return 'checked-row'
      }
      if (row.id === this.lastCheckedOrder) {
        return 'highlight-row'
      }
      return ''
    },
    formatDate(date) {
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    },
    handleFilter() {
      this.loading = true
      this.pagination.currentPage = 1
      setTimeout(() => {
        this.loading = false
        this.$message.success(`查询到 ${this.pagination.total} 条记录`)
      }, 500)
    },
    handleReset() {
      this.filterForm = {
        orderId: '',
        ticketId: '',
        status: '',
        checkedStatus: '',
        bookDateRange: [],
        visitDate: ''
      }
      this.pagination.currentPage = 1
      this.lastCheckedOrder = null
      this.$message.info('筛选条件已重置')
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
    },
    handleView(row) {
      this.currentOrder = row
      this.dialogVisible = true
    },
    handleCancel(row) {
      if (row.status === 'used') {
        this.$message.error('已核销订单无法取消！')
        return
      }
      this.$confirm('确定要取消该订单吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        row.status = 'cancelled'
        this.$message.success('订单已取消')
      }).catch(() => {})
    }
  }
}
</script>

<style scoped>
.filter-card {
  margin-bottom: 20px;
}

.filter-form {
  margin: 0;
}

.filter-form .el-form-item {
  margin-bottom: 15px;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.order-detail {
  padding: 10px 0;
}

.checked-row {
  background-color: #fff1f0 !important;
}

.checked-row .el-table__cell {
  color: #909399;
}

.highlight-row {
  animation: highlight-fade 3s ease-out;
}

@keyframes highlight-fade {
  0% {
    background-color: #67c23a;
    color: #fff;
  }
  50% {
    background-color: #f0f9eb;
  }
  100% {
    background-color: #fff1f0;
  }
}
</style>
