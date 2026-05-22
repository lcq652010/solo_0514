<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">入库确认</h2>
    </div>

    <div class="search-bar">
      <el-form :inline="true" :model="searchForm" size="small">
        <el-form-item label="订单号">
          <el-input v-model="searchForm.orderId" placeholder="请输入订单号" clearable style="width: 180px"></el-input>
        </el-form-item>
        <el-form-item label="供应商">
          <el-input v-model="searchForm.supplierName" placeholder="请输入供应商" clearable style="width: 180px"></el-input>
        </el-form-item>
        <el-form-item label="入库状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable style="width: 140px">
            <el-option label="待入库" value="confirmed"></el-option>
            <el-option label="已入库" value="stocked"></el-option>
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
        <el-table-column prop="status" label="入库状态" width="100" align="center">
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
        <el-table-column prop="stockInTime" label="入库时间" min-width="160" align="center">
          <template slot-scope="scope">
            {{ scope.row.stockInTime ? (scope.row.stockInTime | formatDate) : '-' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button size="mini" type="info" icon="el-icon-view" @click="handleView(scope.row)">查看</el-button>
            <el-button 
              size="mini" 
              type="success" 
              icon="el-icon-check" 
              @click="handleStockIn(scope.row)"
              :disabled="scope.row.status !== 'confirmed'">
              入库确认
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
      title="入库确认"
      :visible.sync="stockInVisible"
      width="800px"
      :close-on-click-modal="false">
      <div v-if="currentOrder" class="stock-in-detail">
        <el-descriptions :column="2" border size="small">
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
        </el-descriptions>

        <div class="detail-section">
          <h4>入库明细 <span class="tip">（请核对实际入库数量，可修改实际入库数量）</span></h4>
          <el-table :data="currentOrder.items" border style="width: 100%">
            <el-table-column prop="productName" label="农产品名称" min-width="140"></el-table-column>
            <el-table-column prop="unit" label="单位" width="80" align="center"></el-table-column>
            <el-table-column prop="price" label="单价(元)" width="120" align="center"></el-table-column>
            <el-table-column prop="quantity" label="采购数量" width="120" align="center"></el-table-column>
            <el-table-column label="实际入库数量" width="160" align="center">
              <template slot-scope="scope">
                <el-input-number 
                  v-model="scope.row.actualQuantity" 
                  :min="0" 
                  :max="scope.row.quantity"
                  style="width: 100%">
                </el-input-number>
              </template>
            </el-table-column>
            <el-table-column label="差异" width="100" align="center">
              <template slot-scope="scope">
                <span :style="{ color: (scope.row.actualQuantity || scope.row.quantity) < scope.row.quantity ? '#f56c6c' : '#67c23a' }">
                  {{ (scope.row.actualQuantity || scope.row.quantity) - scope.row.quantity }}
                </span>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <el-form :model="stockInForm" :rules="stockInRules" ref="stockInForm" label-width="100px" class="stock-in-form">
          <el-form-item label="入库单号" prop="stockInNo">
            <el-input v-model="stockInForm.stockInNo" disabled></el-input>
          </el-form-item>
          <el-form-item label="入库日期" prop="stockInDate">
            <el-date-picker
              v-model="stockInForm.stockInDate"
              type="date"
              placeholder="选择入库日期"
              style="width: 100%"
              value-format="yyyy-MM-dd">
            </el-date-picker>
          </el-form-item>
          <el-form-item label="仓库" prop="warehouse">
            <el-select v-model="stockInForm.warehouse" placeholder="请选择仓库" style="width: 100%">
              <el-option label="一号仓库" value="warehouse1"></el-option>
              <el-option label="二号仓库" value="warehouse2"></el-option>
              <el-option label="三号仓库" value="warehouse3"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="经办人" prop="operator">
            <el-input v-model="stockInForm.operator" placeholder="请输入经办人姓名"></el-input>
          </el-form-item>
          <el-form-item label="备注">
            <el-input 
              v-model="stockInForm.remark" 
              type="textarea" 
              :rows="2" 
              placeholder="请输入备注信息">
            </el-input>
          </el-form-item>
        </el-form>
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button @click="stockInVisible = false">取 消</el-button>
        <el-button type="primary" @click="confirmStockIn">确认入库</el-button>
      </div>
    </el-dialog>

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
import { orders, statusMap } from '../mock/data.js'

export default {
  name: 'StockIn',
  data() {
    return {
      allData: [...orders],
      tableData: [],
      searchForm: {
        orderId: '',
        supplierName: '',
        status: ''
      },
      pagination: {
        page: 1,
        size: 10,
        total: 0
      },
      stockInVisible: false,
      detailVisible: false,
      currentOrder: null,
      stockInForm: {
        stockInNo: '',
        stockInDate: '',
        warehouse: '',
        operator: '',
        remark: ''
      },
      stockInRules: {
        stockInDate: [{ required: true, message: '请选择入库日期', trigger: 'change' }],
        warehouse: [{ required: true, message: '请选择仓库', trigger: 'change' }],
        operator: [{ required: true, message: '请输入经办人', trigger: 'blur' }]
      },
      statusMap
    }
  },
  computed: {
    filteredOrders() {
      return this.allData.filter(item => item.status === 'confirmed' || item.status === 'stocked')
    }
  },
  created() {
    this.loadData()
  },
  methods: {
    loadData() {
      let data = [...this.filteredOrders]
      
      if (this.searchForm.orderId) {
        data = data.filter(item => item.id.includes(this.searchForm.orderId))
      }
      if (this.searchForm.supplierName) {
        data = data.filter(item => item.supplierName.includes(this.searchForm.supplierName))
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
      this.searchForm = { orderId: '', supplierName: '', status: '' }
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
    handleStockIn(row) {
      this.currentOrder = JSON.parse(JSON.stringify(row))
      this.currentOrder.items.forEach(item => {
        item.actualQuantity = item.quantity
      })
      
      const stockInNo = 'RK' + new Date().toISOString().slice(0, 10).replace(/-/g, '') + 
        String(Math.floor(Math.random() * 10000)).padStart(4, '0')
      
      this.stockInForm = {
        stockInNo,
        stockInDate: new Date().toISOString().slice(0, 10),
        warehouse: '',
        operator: '',
        remark: ''
      }
      
      this.stockInVisible = true
      this.$nextTick(() => {
        this.$refs.stockInForm && this.$refs.stockInForm.clearValidate()
      })
    },
    confirmStockIn() {
      this.$refs.stockInForm.validate((valid) => {
        if (valid) {
          this.$confirm('确认入库后将更新库存，是否继续？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'success'
          }).then(() => {
            const index = this.allData.findIndex(item => item.id === this.currentOrder.id)
            if (index > -1) {
              this.allData[index].status = 'stocked'
              this.allData[index].stockInTime = new Date().toLocaleString()
              this.loadData()
              this.stockInVisible = false
              this.$message.success('入库确认成功，库存已更新')
            }
          }).catch(() => {})
        }
      })
    }
  }
}
</script>

<style scoped lang="scss">
.stock-in-detail {
  .detail-section {
    margin-top: 20px;
    
    h4 {
      margin-bottom: 12px;
      font-size: 16px;
      font-weight: 500;
      color: #303133;
      
      .tip {
        font-size: 12px;
        color: #909399;
        font-weight: normal;
        margin-left: 8px;
      }
    }
  }
  
  .stock-in-form {
    margin-top: 20px;
  }
}

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
