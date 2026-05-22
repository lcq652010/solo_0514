<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">采购订单列表</h2>
      <el-button type="primary" icon="el-icon-shopping-cart-2" @click="$router.push('/purchase')">新建采购单</el-button>
    </div>

    <div class="search-bar">
      <el-form :inline="true" :model="searchForm" size="small">
        <el-form-item label="订单号">
          <el-input v-model="searchForm.orderId" placeholder="请输入订单号" clearable style="width: 180px"></el-input>
        </el-form-item>
        <el-form-item label="农产品类型">
          <el-select v-model="searchForm.category" placeholder="请选择类型" clearable style="width: 140px">
            <el-option
              v-for="item in productCategories"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="供应商">
          <el-select v-model="searchForm.supplierId" placeholder="请选择供应商" clearable style="width: 180px" filterable>
            <el-option
              v-for="item in suppliers"
              :key="item.id"
              :label="item.name"
              :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="采购日期">
          <el-date-picker
            v-model="searchForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="yyyy-MM-dd"
            style="width: 240px">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="结算状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable style="width: 140px">
            <el-option label="待确认" value="pending"></el-option>
            <el-option label="已确认" value="confirmed"></el-option>
            <el-option label="已入库" value="stocked"></el-option>
            <el-option label="已取消" value="cancelled"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
          <el-button icon="el-icon-refresh" @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="table-card">
      <el-table :data="tableData" border stripe style="width: 100%">
        <el-table-column prop="id" label="订单号" min-width="160"></el-table-column>
        <el-table-column prop="supplierName" label="供应商" min-width="160"></el-table-column>
        <el-table-column prop="totalAmount" label="订单金额(元)" width="140" align="center">
          <template slot-scope="scope">
            <span style="color: #f56c6c; font-weight: 500">{{ scope.row.totalAmount | formatCurrency }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <span :class="['status-tag', statusMap[scope.row.status].class]">
              {{ statusMap[scope.row.status].label }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="下单时间" min-width="160" align="center">
          <template slot-scope="scope">
            {{ scope.row.createTime | formatDate }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="280" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button size="mini" type="info" icon="el-icon-view" @click="handleView(scope.row)">查看</el-button>
            <el-button 
              size="mini" 
              type="success" 
              icon="el-icon-check" 
              @click="handleConfirm(scope.row)"
              :disabled="scope.row.status !== 'pending'">
              确认
            </el-button>
            <el-button 
              size="mini" 
              type="danger" 
              icon="el-icon-close" 
              @click="handleCancel(scope.row)"
              :disabled="scope.row.status !== 'pending'">
              取消
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.page"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pagination.size"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total">
        </el-pagination>
      </div>
    </div>

    <el-dialog
      title="订单详情"
      :visible.sync="detailVisible"
      width="700px">
      <div v-if="currentOrder" class="order-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="订单号">{{ currentOrder.id }}</el-descriptions-item>
          <el-descriptions-item label="供应商">{{ currentOrder.supplierName }}</el-descriptions-item>
          <el-descriptions-item label="订单金额">
            <span style="color: #f56c6c; font-weight: 600">{{ currentOrder.totalAmount | formatCurrency }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="订单状态">
            <span :class="['status-tag', statusMap[currentOrder.status].class]">
              {{ statusMap[currentOrder.status].label }}
            </span>
          </el-descriptions-item>
          <el-descriptions-item label="下单时间" :span="2">
            {{ currentOrder.createTime | formatDate }}
          </el-descriptions-item>
          <el-descriptions-item v-if="currentOrder.stockInTime" label="入库时间" :span="2">
            {{ currentOrder.stockInTime | formatDate }}
          </el-descriptions-item>
        </el-descriptions>

        <div class="detail-section">
          <h4>采购明细</h4>
          <el-table :data="currentOrder.items" border size="small" style="width: 100%">
            <el-table-column prop="productName" label="农产品名称"></el-table-column>
            <el-table-column prop="unit" label="单位" width="80" align="center"></el-table-column>
            <el-table-column prop="price" label="单价(元)" width="120" align="center"></el-table-column>
            <el-table-column prop="quantity" label="数量" width="100" align="center"></el-table-column>
            <el-table-column prop="amount" label="金额(元)" width="120" align="center"></el-table-column>
          </el-table>
        </div>
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button @click="detailVisible = false">关 闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { orders, statusMap, productCategories, suppliers, products } from '../mock/data.js'

export default {
  name: 'Orders',
  data() {
    return {
      allData: [...orders],
      tableData: [],
      productCategories,
      suppliers,
      products,
      searchForm: {
        orderId: '',
        category: '',
        supplierId: '',
        status: '',
        dateRange: []
      },
      pagination: {
        page: 1,
        size: 10,
        total: 0
      },
      detailVisible: false,
      currentOrder: null,
      statusMap
    }
  },
  created() {
    this.loadData()
  },
  methods: {
    getProductCategory(productId) {
      const product = this.products.find(p => p.id === productId)
      return product ? product.category : ''
    },
    loadData() {
      let data = [...this.allData]
      
      if (this.searchForm.orderId) {
        data = data.filter(item => item.id.includes(this.searchForm.orderId))
      }
      if (this.searchForm.category) {
        data = data.filter(item => {
          return item.items.some(subItem => {
            return this.getProductCategory(subItem.productId) === this.searchForm.category
          })
        })
      }
      if (this.searchForm.supplierId) {
        data = data.filter(item => item.supplierId === this.searchForm.supplierId)
      }
      if (this.searchForm.status) {
        data = data.filter(item => item.status === this.searchForm.status)
      }
      if (this.searchForm.dateRange && this.searchForm.dateRange.length === 2) {
        const [start, end] = this.searchForm.dateRange
        data = data.filter(item => {
          const itemDate = item.createTime.split(' ')[0]
          return itemDate >= start && itemDate <= end
        })
      }
      
      this.pagination.total = data.length
      const startIdx = (this.pagination.page - 1) * this.pagination.size
      const endIdx = startIdx + this.pagination.size
      this.tableData = data.slice(startIdx, endIdx)
    },
    handleSearch() {
      this.pagination.page = 1
      this.loadData()
    },
    handleReset() {
      this.searchForm = { orderId: '', category: '', supplierId: '', status: '', dateRange: [] }
      this.pagination.page = 1
      this.loadData()
    },
    handleSizeChange(val) {
      this.pagination.size = val
      this.loadData()
    },
    handleCurrentChange(val) {
      this.pagination.page = val
      this.loadData()
    },
    handleView(row) {
      this.currentOrder = row
      this.detailVisible = true
    },
    handleConfirm(row) {
      this.$confirm(`确定要确认订单"${row.id}"吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'success'
      }).then(() => {
        const index = this.allData.findIndex(item => item.id === row.id)
        if (index > -1) {
          this.allData[index].status = 'confirmed'
          this.loadData()
          this.$message.success('订单确认成功')
        }
      }).catch(() => {})
    },
    handleCancel(row) {
      this.$confirm(`确定要取消订单"${row.id}"吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.allData.findIndex(item => item.id === row.id)
        if (index > -1) {
          this.allData[index].status = 'cancelled'
          this.loadData()
          this.$message.success('订单已取消')
        }
      }).catch(() => {})
    }
  }
}
</script>

<style scoped lang="scss">
.order-detail {
  .detail-section {
    margin-top: 20px;
    
    h4 {
      margin-bottom: 12px;
      font-size: 16px;
      font-weight: 500;
      color: #303133;
    }
  }
}
</style>
