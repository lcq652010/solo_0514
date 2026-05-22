<template>
  <div class="orders-page">
    <div class="page-card">
      <div class="page-title">
        <i class="el-icon-document"></i>
        订单记录
      </div>
      
      <div class="search-form">
        <el-input
          v-model="searchForm.orderId"
          placeholder="订单号"
          clearable
          style="width: 180px"
        />
        <el-input
          v-model="searchForm.customerName"
          placeholder="客户姓名"
          clearable
          style="width: 120px"
        />
        <el-select
          v-model="searchForm.category"
          placeholder="建材类型"
          clearable
          style="width: 130px"
        >
          <el-option label="水泥" value="水泥" />
          <el-option label="钢材" value="钢材" />
          <el-option label="砂石" value="砂石" />
          <el-option label="砖瓦" value="砖瓦" />
        </el-select>
        <el-select
          v-model="searchForm.status"
          placeholder="订单状态"
          clearable
          style="width: 120px"
        >
          <el-option label="待处理" value="pending" />
          <el-option label="处理中" value="processing" />
          <el-option label="已发货" value="shipped" />
          <el-option label="已完成" value="completed" />
        </el-select>
        <el-select
          v-model="searchForm.shipStatus"
          placeholder="发货状态"
          clearable
          style="width: 120px"
        >
          <el-option label="未发货" value="unshipped" />
          <el-option label="已发货" value="shipped" />
        </el-select>
        <el-date-picker
          v-model="searchForm.dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          style="width: 280px"
        />
        <el-button type="primary" @click="handleSearch">
          <i class="el-icon-search"></i>
          搜索
        </el-button>
        <el-button @click="handleReset">
          <i class="el-icon-refresh"></i>
          重置
        </el-button>
      </div>
      
      <el-table
        :data="tableData"
        border
        stripe
        style="width: 100%"
      >
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="id" label="订单号" width="180" />
        <el-table-column prop="customerName" label="客户姓名" width="100" align="center" />
        <el-table-column prop="customerPhone" label="联系电话" width="130" align="center" />
        <el-table-column prop="address" label="送货地址" min-width="180" show-overflow-tooltip />
        <el-table-column prop="totalAmount" label="订单金额" width="120" align="center">
          <template slot-scope="scope">
            <span style="color: #f56c6c; font-weight: 600;">{{ scope.row.totalAmount.toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="small">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="下单时间" width="160" align="center" />
        <el-table-column prop="shipTime" label="发货时间" width="160" align="center">
          <template slot-scope="scope">
            <span v-if="scope.row.shipTime">{{ scope.row.shipTime }}</span>
            <span v-else style="color: #c0c4cc;">-</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="handleView(scope.row)">
              详情
            </el-button>
            <el-button
              v-if="scope.row.status === 'shipped'"
              type="text"
              size="small"
              @click="handleComplete(scope.row)"
            >
              完成
            </el-button>
            <el-button
              v-if="scope.row.status === 'pending' || scope.row.status === 'processing'"
              type="text"
              size="small"
              @click="handleCancel(scope.row)"
            >
              取消
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div style="margin-top: 20px; text-align: right;">
        <el-pagination
          :current-page="pagination.page"
          :page-size="pagination.size"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </div>
    
    <el-dialog title="订单详情" :visible.sync="detailDialogVisible" width="750px">
      <el-descriptions :column="2" border style="margin-bottom: 20px;">
        <el-descriptions-item label="订单号" :span="2">{{ currentOrder.id }}</el-descriptions-item>
        <el-descriptions-item label="客户姓名">{{ currentOrder.customerName }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ currentOrder.customerPhone }}</el-descriptions-item>
        <el-descriptions-item label="送货地址" :span="2">{{ currentOrder.address }}</el-descriptions-item>
        <el-descriptions-item label="订单金额">
          <span style="color: #f56c6c; font-weight: 600; font-size: 18px;">{{ currentOrder.totalAmount.toFixed(2) }} 元</span>
        </el-descriptions-item>
        <el-descriptions-item label="订单状态">
          <el-tag :type="getStatusType(currentOrder.status)" size="small">
            {{ getStatusText(currentOrder.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="下单时间" :span="2">{{ currentOrder.createTime }}</el-descriptions-item>
        <el-descriptions-item v-if="currentOrder.shipTime" label="发货时间" :span="2">{{ currentOrder.shipTime }}</el-descriptions-item>
        <el-descriptions-item v-if="currentOrder.logistics" label="物流公司">{{ currentOrder.logistics }}</el-descriptions-item>
        <el-descriptions-item v-if="currentOrder.trackingNo" label="运单号">{{ currentOrder.trackingNo }}</el-descriptions-item>
        <el-descriptions-item v-if="currentOrder.receiveTime" label="签收时间" :span="2">{{ currentOrder.receiveTime }}</el-descriptions-item>
      </el-descriptions>
      
      <el-divider content-position="left">商品明细</el-divider>
      
      <el-table :data="currentOrder.items || []" border style="width: 100%; margin-bottom: 20px;">
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="productName" label="商品名称" min-width="180" />
        <el-table-column prop="spec" label="规格" width="120" align="center" />
        <el-table-column prop="unit" label="单位" width="80" align="center" />
        <el-table-column prop="price" label="单价" width="100" align="center" />
        <el-table-column prop="quantity" label="数量" width="100" align="center" />
        <el-table-column label="小计" width="120" align="center">
          <template slot-scope="scope">
            <span style="color: #f56c6c; font-weight: 600;">{{ (scope.row.price * scope.row.quantity).toFixed(2) }}</span>
          </template>
        </el-table-column>
      </el-table>
      
      <el-divider v-if="currentOrder.remark" content-position="left">备注</el-divider>
      <p v-if="currentOrder.remark" style="color: #606266; padding: 0 10px;">{{ currentOrder.remark }}</p>
    </el-dialog>
  </div>
</template>

<script>
import { orders } from '@/mock/data'

export default {
  name: 'Orders',
  data() {
    return {
      searchForm: {
        orderId: '',
        customerName: '',
        category: '',
        status: '',
        shipStatus: '',
        dateRange: []
      },
      tableData: [],
      pagination: {
        page: 1,
        size: 10,
        total: 0
      },
      detailDialogVisible: false,
      currentOrder: {}
    }
  },
  created() {
    this.loadData()
  },
  activated() {
    this.loadData()
  },
  methods: {
    loadData() {
      let data = [...orders]
      
      if (this.searchForm.orderId) {
        data = data.filter(item => item.id.includes(this.searchForm.orderId))
      }
      
      if (this.searchForm.customerName) {
        data = data.filter(item => item.customerName.includes(this.searchForm.customerName))
      }
      
      if (this.searchForm.category) {
        data = data.filter(item => 
          item.items.some(subItem => subItem.productName.includes(this.searchForm.category))
        )
      }
      
      if (this.searchForm.status) {
        data = data.filter(item => item.status === this.searchForm.status)
      }
      
      if (this.searchForm.shipStatus) {
        if (this.searchForm.shipStatus === 'shipped') {
          data = data.filter(item => item.isShipped)
        } else {
          data = data.filter(item => !item.isShipped)
        }
      }
      
      if (this.searchForm.dateRange && this.searchForm.dateRange.length === 2) {
        const startDate = this.searchForm.dateRange[0].toISOString().slice(0, 10)
        const endDate = this.searchForm.dateRange[1].toISOString().slice(0, 10)
        data = data.filter(item => {
          const itemDate = item.createTime.slice(0, 10)
          return itemDate >= startDate && itemDate <= endDate
        })
      }
      
      this.pagination.total = data.length
      
      const start = (this.pagination.page - 1) * this.pagination.size
      const end = start + this.pagination.size
      this.tableData = data.slice(start, end)
    },
    handleSearch() {
      this.pagination.page = 1
      this.loadData()
    },
    handleReset() {
      this.searchForm = {
        orderId: '',
        customerName: '',
        category: '',
        status: '',
        shipStatus: '',
        dateRange: []
      }
      this.pagination.page = 1
      this.loadData()
    },
    handleSizeChange(size) {
      this.pagination.size = size
      this.loadData()
    },
    handlePageChange(page) {
      this.pagination.page = page
      this.loadData()
    },
    handleView(row) {
      this.currentOrder = { ...row }
      this.detailDialogVisible = true
    },
    handleComplete(row) {
      this.$confirm('确认该订单已完成签收吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = orders.findIndex(item => item.id === row.id)
        if (index !== -1) {
          orders[index].status = 'completed'
          orders[index].receiveTime = new Date().toLocaleString('zh-CN', { hour12: false }).replace(/\//g, '-')
          
          this.$message.success('订单已完成！')
          this.loadData()
        }
      }).catch(() => {})
    },
    handleCancel(row) {
      this.$confirm('确认取消该订单吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = orders.findIndex(item => item.id === row.id)
        if (index !== -1) {
          orders.splice(index, 1)
          
          this.$message.success('订单已取消！')
          this.loadData()
        }
      }).catch(() => {})
    },
    getStatusType(status) {
      const types = {
        pending: 'info',
        processing: 'warning',
        shipped: 'success',
        completed: '',
        cancelled: 'danger'
      }
      return types[status] || ''
    },
    getStatusText(status) {
      const texts = {
        pending: '待处理',
        processing: '处理中',
        shipped: '已发货',
        completed: '已完成',
        cancelled: '已取消'
      }
      return texts[status] || status
    }
  }
}
</script>

<style lang="less" scoped>
.orders-page {
  .el-descriptions {
    /deep/ .el-descriptions__label {
      background: #f5f7fa;
      width: 120px;
    }
  }
}
</style>
