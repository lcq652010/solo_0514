<template>
  <div class="page-container">
    <div class="page-header">
      <h2>库存查询</h2>
    </div>
    <div class="page-content">
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm" class="demo-form-inline">
          <el-form-item label="商品名称">
            <el-input v-model="searchForm.name" placeholder="请输入商品名称" clearable />
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
          <el-form-item label="库存状态">
            <el-select v-model="searchForm.stockStatus" placeholder="请选择" clearable>
              <el-option label="库存充足" value="normal" />
              <el-option label="库存不足" value="low" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button @click="handleReset">重置</el-button>
            <el-button type="success" @click="handleExport">导出</el-button>
          </el-form-item>
        </el-form>
      </div>

      <div class="stats-bar">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card shadow="hover">
              <div class="stat-item">
                <div class="stat-label">商品总数</div>
                <div class="stat-value">{{ stats.totalProducts }}</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <div class="stat-item">
                <div class="stat-label">库存总量</div>
                <div class="stat-value">{{ stats.totalStock }}</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <div class="stat-item">
                <div class="stat-label">库存总价值</div>
                <div class="stat-value">¥{{ stats.totalValue.toFixed(2) }}</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <div class="stat-item warning">
                <div class="stat-label">预警商品</div>
                <div class="stat-value">{{ stats.warningCount }}</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <div class="table-container">
        <el-table
          :data="tableData"
          border
          style="width: 100%"
          :loading="loading"
          :row-class-name="getTableRowClassName"
        >
          <el-table-column type="index" label="序号" width="60" align="center" />
          <el-table-column prop="code" label="商品编码" width="120" align="center" />
          <el-table-column prop="name" label="商品名称" min-width="150" />
          <el-table-column prop="category" label="分类" width="100" align="center" />
          <el-table-column prop="price" label="单价(元)" width="100" align="center">
            <template slot-scope="scope">
              ¥{{ scope.row.price.toFixed(2) }}
            </template>
          </el-table-column>
          <el-table-column prop="stock" label="库存数量" width="110" align="center">
            <template slot-scope="scope">
              <el-tag :type="getStockTagType(scope.row)">
                {{ scope.row.stock }}{{ scope.row.unit }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="minStock" label="安全库存" width="100" align="center" />
          <el-table-column label="库存价值" width="120" align="center">
            <template slot-scope="scope">
              ¥{{ (scope.row.price * scope.row.stock).toFixed(2) }}
            </template>
          </el-table-column>
          <el-table-column label="库存状态" width="100" align="center">
            <template slot-scope="scope">
              <el-tag :type="scope.row.stock < scope.row.minStock ? 'danger' : 'success'">
                {{ scope.row.stock < scope.row.minStock ? '库存不足' : '库存充足' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="120" align="center" fixed="right">
            <template slot-scope="scope">
              <el-button type="text" size="small" @click="handleStockIn(scope.row)">
                立即入库
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination-container">
          <el-pagination
            background
            :current-page="pagination.page"
            :page-sizes="[10, 20, 50, 100]"
            :page-size="pagination.pageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="pagination.total"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { api, categories, eventBus } from '../api/mockData'

export default {
  name: 'StockQuery',
  data() {
    return {
      loading: false,
      categories,
      searchForm: {
        name: '',
        category: '',
        stockStatus: ''
      },
      tableData: [],
      allData: [],
      pagination: {
        page: 1,
        pageSize: 10,
        total: 0
      },
      stats: {
        totalProducts: 0,
        totalStock: 0,
        totalValue: 0,
        warningCount: 0
      }
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
        const params = {
          name: this.searchForm.name,
          category: this.searchForm.category,
          page: 1,
          pageSize: 1000
        }
        const res = await api.getProducts(params)
        if (res.code === 200) {
          this.allData = res.data.list
          
          if (this.searchForm.stockStatus === 'low') {
            this.allData = this.allData.filter(item => item.stock < item.minStock)
          } else if (this.searchForm.stockStatus === 'normal') {
            this.allData = this.allData.filter(item => item.stock >= item.minStock)
          }
          
          this.calculateStats()
          this.updateTableData()
        }
      } catch (error) {
        this.$message.error('获取数据失败')
      } finally {
        this.loading = false
      }
    },
    calculateStats() {
      this.stats.totalProducts = this.allData.length
      this.stats.totalStock = this.allData.reduce((sum, item) => sum + item.stock, 0)
      this.stats.totalValue = this.allData.reduce((sum, item) => sum + item.price * item.stock, 0)
      this.stats.warningCount = this.allData.filter(item => item.stock < item.minStock).length
    },
    updateTableData() {
      const start = (this.pagination.page - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      this.tableData = this.allData.slice(start, end)
      this.pagination.total = this.allData.length
    },
    getStockTagType(row) {
      const ratio = row.stock / row.minStock
      if (ratio < 0.5) return 'danger'
      if (ratio < 1) return 'warning'
      return 'success'
    },
    handleSearch() {
      this.pagination.page = 1
      this.fetchData()
    },
    handleReset() {
      this.searchForm = {
        name: '',
        category: '',
        stockStatus: ''
      }
      this.pagination.page = 1
      this.fetchData()
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
    handleStockIn(row) {
      this.$router.push({
        path: '/stock-in',
        query: { productId: row.id }
      })
    },
    handleExport() {
      this.$message.success('导出成功！')
    },
    getTableRowClassName({ row }) {
      if (row.stock < row.minStock) {
        return 'stock-warning-row'
      }
      return ''
    }
  }
}
</script>

<style scoped>
.stats-bar {
  margin-bottom: 20px;
}

.stat-item {
  text-align: center;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.stat-item.warning .stat-value {
  color: #f56c6c;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}

::v-deep .el-table .stock-warning-row {
  background-color: #fef0f0 !important;
}

::v-deep .el-table .stock-warning-row:hover > td {
  background-color: #fde2e2 !important;
}
</style>
