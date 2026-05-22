<template>
  <div class="page-container">
    <div class="page-header">
      <h2>库存预警</h2>
    </div>
    <div class="page-content">
      <div class="warning-summary" v-if="warningList.length > 0">
        <el-alert
          title="库存预警提示"
          :message="`当前共有 ${warningList.length} 种商品库存低于安全库存，请及时补货！`"
          type="warning"
          show-icon
          :closable="false"
        />
      </div>

      <div class="stats-overview">
        <el-row :gutter="20">
          <el-col :span="8">
            <div class="stat-card danger">
              <div class="stat-icon">
                <i class="el-icon-warning-outline"></i>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ severeWarningCount }}</div>
                <div class="stat-text">严重预警（<50%）</div>
              </div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="stat-card warning">
              <div class="stat-icon">
                <i class="el-icon-info"></i>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ mediumWarningCount }}</div>
                <div class="stat-text">中等预警（50%-80%）</div>
              </div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="stat-card mild">
              <div class="stat-icon">
                <i class="el-icon-remove-outline"></i>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ mildWarningCount }}</div>
                <div class="stat-text">轻度预警（80%-100%）</div>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>

      <div class="search-bar mt20">
        <el-form :inline="true" :model="searchForm" class="demo-form-inline">
          <el-form-item label="预警等级">
            <el-select v-model="searchForm.level" placeholder="请选择" clearable>
              <el-option label="严重预警" value="severe" />
              <el-option label="中等预警" value="medium" />
              <el-option label="轻度预警" value="mild" />
            </el-select>
          </el-form-item>
          <el-form-item label="商品分类">
            <el-select v-model="searchForm.category" placeholder="请选择分类" clearable>
              <el-option
                v-for="item in categories"
                :key="item"
                :label="item"
                :value="item"
              />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">筛选</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <div class="table-container">
        <el-table
          :data="tableData"
          border
          style="width: 100%"
          :loading="loading"
          row-key="id"
          :row-class-name="getTableRowClassName"
        >
          <el-table-column type="index" label="序号" width="60" align="center" />
          <el-table-column prop="code" label="商品编码" width="120" align="center" />
          <el-table-column prop="name" label="商品名称" min-width="150" />
          <el-table-column prop="category" label="分类" width="100" align="center" />
          <el-table-column prop="stock" label="当前库存" width="100" align="center">
            <template slot-scope="scope">
              <span style="color: #f56c6c; font-weight: bold;">
                {{ scope.row.stock }}{{ scope.row.unit }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="minStock" label="安全库存" width="100" align="center" />
          <el-table-column label="缺口数量" width="100" align="center">
            <template slot-scope="scope">
              <span style="color: #f56c6c;">
                {{ scope.row.minStock - scope.row.stock }}{{ scope.row.unit }}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="库存占比" width="120" align="center">
            <template slot-scope="scope">
              <el-progress
                :percentage="Math.round((scope.row.stock / scope.row.minStock) * 100)"
                :color="getProgressColor(scope.row)"
                :stroke-width="12"
              />
            </template>
          </el-table-column>
          <el-table-column label="预警等级" width="120" align="center">
            <template slot-scope="scope">
              <el-tag :type="getWarningTagType(scope.row)" size="medium">
                {{ getWarningLevelText(scope.row) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="180" align="center" fixed="right">
            <template slot-scope="scope">
              <el-button type="primary" size="small" @click="handleQuickIn(scope.row)">
                快速入库
              </el-button>
              <el-button type="text" size="small" @click="handleIgnore(scope.row)">
                忽略
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination-container" v-if="tableData.length > 0">
          <el-pagination
            background
            :current-page="pagination.page"
            :page-sizes="[10, 20, 50]"
            :page-size="pagination.pageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="pagination.total"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>

        <div class="empty-state" v-else-if="!loading">
          <el-empty description="暂无预警商品" />
        </div>
      </div>
    </div>

    <el-dialog title="快速入库" :visible.sync="stockInDialogVisible" width="400px">
      <el-form :model="quickInForm" :rules="quickInRules" ref="quickInForm" label-width="100px">
        <el-form-item label="商品名称">
          <span>{{ currentProduct ? currentProduct.name : '-' }}</span>
        </el-form-item>
        <el-form-item label="当前库存">
          <span>{{ currentProduct ? currentProduct.stock + currentProduct.unit : '-' }}</span>
        </el-form-item>
        <el-form-item label="入库数量" prop="quantity">
          <el-input-number
            v-model="quickInForm.quantity"
            :min="1"
            :max="9999"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="入库后库存">
          <span style="color: #67c23a; font-weight: bold;">
            {{ (currentProduct ? currentProduct.stock : 0) + quickInForm.quantity }}
            {{ currentProduct ? currentProduct.unit : '' }}
          </span>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="stockInDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmQuickIn" :loading="submitting">
          确认入库
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { api, categories, eventBus } from '../api/mockData'

export default {
  name: 'StockWarning',
  data() {
    return {
      loading: false,
      submitting: false,
      categories,
      searchForm: {
        level: '',
        category: ''
      },
      warningList: [],
      filteredList: [],
      tableData: [],
      pagination: {
        page: 1,
        pageSize: 10,
        total: 0
      },
      stockInDialogVisible: false,
      currentProduct: null,
      quickInForm: {
        quantity: 1
      },
      quickInRules: {
        quantity: [
          { required: true, message: '请输入入库数量', trigger: 'blur' },
          { type: 'number', min: 1, max: 9999, message: '入库数量必须在1-9999之间', trigger: 'blur' },
          {
            validator: (rule, value, callback) => {
              if (!Number.isInteger(value)) {
                callback(new Error('入库数量必须为正整数'))
              } else if (value > 9999) {
                callback(new Error('入库数量上限为9999'))
              } else {
                callback()
              }
            },
            trigger: 'blur'
          }
        ]
      }
    }
  },
  computed: {
    severeWarningCount() {
      return this.warningList.filter(item => (item.stock / item.minStock) < 0.5).length
    },
    mediumWarningCount() {
      return this.warningList.filter(item => {
        const ratio = item.stock / item.minStock
        return ratio >= 0.5 && ratio < 0.8
      }).length
    },
    mildWarningCount() {
      return this.warningList.filter(item => {
        const ratio = item.stock / item.minStock
        return ratio >= 0.8 && ratio < 1
      }).length
    }
  },
  mounted() {
    this.fetchData()
    eventBus.on('stock-updated', () => {
      this.fetchData()
    })
  },
  methods: {
    async fetchData() {
      this.loading = true
      try {
        const res = await api.getWarningProducts()
        if (res.code === 200) {
          this.warningList = res.data
          this.applyFilters()
        }
      } catch (error) {
        this.$message.error('获取数据失败')
      } finally {
        this.loading = false
      }
    },
    applyFilters() {
      this.filteredList = [...this.warningList]
      
      if (this.searchForm.category) {
        this.filteredList = this.filteredList.filter(
          item => item.category === this.searchForm.category
        )
      }
      
      if (this.searchForm.level) {
        this.filteredList = this.filteredList.filter(item => {
          const ratio = item.stock / item.minStock
          switch (this.searchForm.level) {
            case 'severe':
              return ratio < 0.5
            case 'medium':
              return ratio >= 0.5 && ratio < 0.8
            case 'mild':
              return ratio >= 0.8 && ratio < 1
            default:
              return true
          }
        })
      }
      
      this.updateTableData()
    },
    updateTableData() {
      const start = (this.pagination.page - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      this.tableData = this.filteredList.slice(start, end)
      this.pagination.total = this.filteredList.length
    },
    getWarningLevelText(row) {
      const ratio = row.stock / row.minStock
      if (ratio < 0.5) return '严重预警'
      if (ratio < 0.8) return '中等预警'
      return '轻度预警'
    },
    getWarningTagType(row) {
      const ratio = row.stock / row.minStock
      if (ratio < 0.5) return 'danger'
      if (ratio < 0.8) return 'warning'
      return 'info'
    },
    getProgressColor(row) {
      const ratio = row.stock / row.minStock
      if (ratio < 0.5) return '#f56c6c'
      if (ratio < 0.8) return '#e6a23c'
      return '#909399'
    },
    handleSearch() {
      this.pagination.page = 1
      this.applyFilters()
    },
    handleReset() {
      this.searchForm = {
        level: '',
        category: ''
      }
      this.pagination.page = 1
      this.applyFilters()
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.pagination.page = 1
      this.updateTableData()
    },
    handleCurrentChange(val) {
      this.pagination.page = val
      this.updateTableData()
    },
    handleQuickIn(row) {
      this.currentProduct = row
      this.quickInForm.quantity = row.minStock - row.stock + 10
      this.stockInDialogVisible = true
    },
    async confirmQuickIn() {
      this.$refs.quickInForm.validate(async (valid) => {
        if (valid) {
          this.submitting = true
          try {
            const res = await api.addStockIn({
              productId: this.currentProduct.id,
              quantity: this.quickInForm.quantity,
              operator: '管理员'
            })
            if (res.code === 200) {
              this.$message.success('入库成功！')
              this.stockInDialogVisible = false
              this.fetchData()
            }
          } catch (error) {
            this.$message.error('入库失败')
          } finally {
            this.submitting = false
          }
        }
      })
    },
    handleIgnore(row) {
      this.$message.info(`已忽略 ${row.name} 的预警`)
    },
    getTableRowClassName({ row }) {
      const ratio = row.stock / row.minStock
      if (ratio < 0.5) {
        return 'stock-severe-warning-row'
      } else if (ratio < 0.8) {
        return 'stock-medium-warning-row'
      } else {
        return 'stock-mild-warning-row'
      }
    }
  }
}
</script>

<style scoped>
.warning-summary {
  margin-bottom: 20px;
}

.stats-overview {
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
  border-radius: 8px;
  color: #fff;
}

.stat-card.danger {
  background: linear-gradient(135deg, #f56c6c 0%, #ff6b6b 100%);
}

.stat-card.warning {
  background: linear-gradient(135deg, #e6a23c 0%, #f7ba2a 100%);
}

.stat-card.mild {
  background: linear-gradient(135deg, #909399 0%, #b4b4b4 100%);
}

.stat-icon {
  font-size: 36px;
  margin-right: 20px;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-text {
  font-size: 14px;
  opacity: 0.9;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}

.empty-state {
  padding: 60px 0;
}

::v-deep .el-table .stock-severe-warning-row {
  background-color: #fef0f0 !important;
}

::v-deep .el-table .stock-severe-warning-row:hover > td {
  background-color: #fde2e2 !important;
}

::v-deep .el-table .stock-medium-warning-row {
  background-color: #fdf6ec !important;
}

::v-deep .el-table .stock-medium-warning-row:hover > td {
  background-color: #faecd8 !important;
}

::v-deep .el-table .stock-mild-warning-row {
  background-color: #f4f4f5 !important;
}

::v-deep .el-table .stock-mild-warning-row:hover > td {
  background-color: #e9e9eb !important;
}
</style>
