<template>
  <div class="delivery-page">
    <div class="page-card">
      <div class="page-title">
        <i class="el-icon-truck"></i>
        发货登记
      </div>
      
      <div class="search-form">
        <el-input
          v-model="searchForm.orderId"
          placeholder="订单号"
          clearable
          style="width: 200px"
        />
        <el-input
          v-model="searchForm.customerName"
          placeholder="客户姓名"
          clearable
          style="width: 150px"
        />
        <el-select
          v-model="searchForm.status"
          placeholder="订单状态"
          clearable
          style="width: 150px"
        >
          <el-option label="待处理" value="pending" />
          <el-option label="处理中" value="processing" />
        </el-select>
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
        <el-table-column prop="address" label="送货地址" min-width="200" show-overflow-tooltip />
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
        <el-table-column label="操作" width="120" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button
              v-if="scope.row.status === 'pending' || scope.row.status === 'processing'"
              type="primary"
              size="small"
              @click="handleShip(scope.row)"
            >
              发货
            </el-button>
            <el-button type="text" size="small" @click="handleView(scope.row)">
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div style="margin-top: 20px; text-align: right;">
        <el-pagination
          :current-page="pagination.page"
          :page-size="pagination.size"
          :total="pagination.total"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </div>
    
    <el-dialog title="发货登记" :visible.sync="shipDialogVisible" width="600px">
      <el-form
        ref="shipForm"
        :model="shipForm"
        :rules="shipRules"
        label-width="100px"
      >
        <el-form-item label="订单号">
          <span style="color: #409EFF; font-weight: 600;">{{ shipForm.orderId }}</span>
        </el-form-item>
        <el-form-item label="客户姓名">
          <span>{{ shipForm.customerName }}</span>
        </el-form-item>
        <el-form-item label="物流公司" prop="logistics">
          <el-select v-model="shipForm.logistics" placeholder="请选择物流公司" style="width: 100%;">
            <el-option label="顺丰物流" value="顺丰物流" />
            <el-option label="京东物流" value="京东物流" />
            <el-option label="德邦物流" value="德邦物流" />
            <el-option label="本地配送" value="本地配送" />
            <el-option label="自提" value="自提" />
          </el-select>
        </el-form-item>
        <el-form-item label="运单号" prop="trackingNo">
          <el-input v-model="shipForm.trackingNo" placeholder="请输入运单号" />
        </el-form-item>
        <el-form-item label="发货备注">
          <el-input
            v-model="shipForm.remark"
            type="textarea"
            :rows="3"
            placeholder="请输入发货备注（选填）"
          />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="shipDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmShip">确认发货</el-button>
      </div>
    </el-dialog>
    
    <el-dialog title="订单详情" :visible.sync="detailDialogVisible" width="700px">
      <el-descriptions :column="2" border style="margin-bottom: 20px;">
        <el-descriptions-item label="订单号" :span="2">{{ currentOrder.id }}</el-descriptions-item>
        <el-descriptions-item label="客户姓名">{{ currentOrder.customerName }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ currentOrder.customerPhone }}</el-descriptions-item>
        <el-descriptions-item label="送货地址" :span="2">{{ currentOrder.address }}</el-descriptions-item>
        <el-descriptions-item label="订单金额">
          <span style="color: #f56c6c; font-weight: 600;">{{ currentOrder.totalAmount.toFixed(2) }} 元</span>
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
      </el-descriptions>
      
      <el-divider content-position="left">商品明细</el-divider>
      
      <el-table :data="currentOrder.items || []" border style="width: 100%">
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="productName" label="商品名称" min-width="180" />
        <el-table-column prop="spec" label="规格" width="120" align="center" />
        <el-table-column prop="unit" label="单位" width="80" align="center" />
        <el-table-column prop="price" label="单价" width="100" align="center" />
        <el-table-column prop="quantity" label="数量" width="100" align="center" />
        <el-table-column label="小计" width="120" align="center">
          <template slot-scope="scope">
            <span style="color: #f56c6c;">{{ (scope.row.price * scope.row.quantity).toFixed(2) }}</span>
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
  name: 'Delivery',
  data() {
    return {
      searchForm: {
        orderId: '',
        customerName: '',
        status: ''
      },
      tableData: [],
      pagination: {
        page: 1,
        size: 10,
        total: 0
      },
      shipDialogVisible: false,
      detailDialogVisible: false,
      shipForm: {
        orderId: '',
        customerName: '',
        logistics: '',
        trackingNo: '',
        remark: ''
      },
      shipRules: {
        logistics: [
          { required: true, message: '请选择物流公司', trigger: 'change' }
        ],
        trackingNo: [
          { required: true, message: '请输入运单号', trigger: 'blur' }
        ]
      },
      currentOrder: {},
      currentOrderIndex: -1
    }
  },
  created() {
    this.loadData()
  },
  methods: {
    loadData() {
      let data = [...orders].filter(item => 
        item.status === 'pending' || item.status === 'processing'
      )
      
      if (this.searchForm.orderId) {
        data = data.filter(item => item.id.includes(this.searchForm.orderId))
      }
      
      if (this.searchForm.customerName) {
        data = data.filter(item => item.customerName.includes(this.searchForm.customerName))
      }
      
      if (this.searchForm.status) {
        data = data.filter(item => item.status === this.searchForm.status)
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
        status: ''
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
    handleShip(row) {
      if (row.isShipped) {
        this.$message.error('该订单已发货，请勿重复操作！')
        return
      }
      
      this.currentOrderIndex = orders.findIndex(item => item.id === row.id)
      this.shipForm = {
        orderId: row.id,
        customerName: row.customerName,
        logistics: '',
        trackingNo: '',
        remark: ''
      }
      this.shipDialogVisible = true
    },
    confirmShip() {
      this.$refs.shipForm.validate(valid => {
        if (valid) {
          if (this.currentOrderIndex !== -1) {
            const currentOrder = orders[this.currentOrderIndex]
            
            if (currentOrder.isShipped) {
              this.$message.error('该订单已发货，请勿重复操作！')
              this.shipDialogVisible = false
              return
            }
            
            orders[this.currentOrderIndex].status = 'shipped'
            orders[this.currentOrderIndex].isShipped = true
            orders[this.currentOrderIndex].shipTime = new Date().toLocaleString('zh-CN', { hour12: false }).replace(/\//g, '-')
            orders[this.currentOrderIndex].logistics = this.shipForm.logistics
            orders[this.currentOrderIndex].trackingNo = this.shipForm.trackingNo
            
            this.$message.success('发货登记成功！')
            this.shipDialogVisible = false
            
            setTimeout(() => {
              this.$router.push('/orders')
            }, 500)
          }
        } else {
          return false
        }
      })
    },
    handleView(row) {
      this.currentOrder = { ...row }
      this.detailDialogVisible = true
    },
    getStatusType(status) {
      const types = {
        pending: 'info',
        processing: 'warning',
        shipped: 'success',
        completed: ''
      }
      return types[status] || ''
    },
    getStatusText(status) {
      const texts = {
        pending: '待处理',
        processing: '处理中',
        shipped: '已发货',
        completed: '已完成'
      }
      return texts[status] || status
    }
  }
}
</script>

<style lang="less" scoped>
.delivery-page {
  .el-descriptions {
    /deep/ .el-descriptions__label {
      background: #f5f7fa;
      width: 120px;
    }
  }
}
</style>
