<template>
  <div class="page-container">
    <div class="page-header">
      <h2>出入库记录</h2>
    </div>
    <div class="page-content">
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm" class="demo-form-inline">
          <el-form-item label="商品分类">
            <el-select v-model="searchForm.category" placeholder="请选择" clearable>
              <el-option
                v-for="item in categories"
                :key="item"
                :label="item"
                :value="item"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="操作类型">
            <el-select v-model="searchForm.type" placeholder="请选择" clearable>
              <el-option label="入库" value="in" />
              <el-option label="出库" value="out" />
            </el-select>
          </el-form-item>
          <el-form-item label="商品名称">
            <el-input v-model="searchForm.productName" placeholder="请输入" clearable />
          </el-form-item>
          <el-form-item label="操作时间">
            <el-date-picker
              v-model="dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              value-format="yyyy-MM-dd"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <div class="stats-overview">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card shadow="hover">
              <div class="stat-item">
                <div class="stat-label">总记录数</div>
                <div class="stat-value">{{ stats.totalRecords }}</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <div class="stat-item in">
                <div class="stat-label">入库次数</div>
                <div class="stat-value">{{ stats.inCount }}</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <div class="stat-item out">
                <div class="stat-label">出库次数</div>
                <div class="stat-value">{{ stats.outCount }}</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <div class="stat-item">
                <div class="stat-label">净入库量</div>
                <div class="stat-value">{{ stats.netInQuantity }}</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <div class="table-container mt20">
        <el-table
          :data="tableData"
          border
          style="width: 100%"
          :loading="loading"
          row-key="id"
        >
          <el-table-column type="index" label="序号" width="60" align="center" />
          <el-table-column prop="id" label="记录ID" width="80" align="center" />
          <el-table-column prop="productName" label="商品名称" min-width="150" />
          <el-table-column prop="category" label="商品分类" width="100" align="center" />
          <el-table-column prop="type" label="操作类型" width="100" align="center">
            <template slot-scope="scope">
              <el-tag :type="scope.row.type === 'in' ? 'success' : 'danger'">
                {{ scope.row.type === 'in' ? '入库' : '出库' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="quantity" label="数量" width="100" align="center">
            <template slot-scope="scope">
              <span :style="{ color: scope.row.type === 'in' ? '#67c23a' : '#f56c6c' }">
                {{ scope.row.type === 'in' ? '+' : '-' }}{{ scope.row.quantity }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="operator" label="操作人" width="100" align="center" />
          <el-table-column prop="remark" label="备注" min-width="150" show-overflow-tooltip />
          <el-table-column prop="createTime" label="操作时间" width="180" align="center" />
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
  name: 'InventoryRecords',
  data() {
    return {
      loading: false,
      categories,
      searchForm: {
        type: '',
        productName: '',
        category: ''
      },
      dateRange: null,
      allData: [],
      tableData: [],
      pagination: {
        page: 1,
        pageSize: 10,
        total: 0
      },
      stats: {
        totalRecords: 0,
        inCount: 0,
        outCount: 0,
        netInQuantity: 0
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
          type: this.searchForm.type,
          productName: this.searchForm.productName,
          category: this.searchForm.category,
          startTime: this.dateRange ? this.dateRange[0] : '',
          endTime: this.dateRange ? this.dateRange[1] : '',
          page: 1,
          pageSize: 1000
        }
        const res = await api.getInventoryRecords(params)
        if (res.code === 200) {
          this.allData = res.data.list
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
      this.stats.totalRecords = this.allData.length
      this.stats.inCount = this.allData.filter(item => item.type === 'in').length
      this.stats.outCount = this.allData.filter(item => item.type === 'out').length
      
      const inQuantity = this.allData
        .filter(item => item.type === 'in')
        .reduce((sum, item) => sum + item.quantity, 0)
      const outQuantity = this.allData
        .filter(item => item.type === 'out')
        .reduce((sum, item) => sum + item.quantity, 0)
      this.stats.netInQuantity = inQuantity - outQuantity
    },
    updateTableData() {
      const start = (this.pagination.page - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      this.tableData = this.allData.slice(start, end)
      this.pagination.total = this.allData.length
    },
    handleSearch() {
      this.pagination.page = 1
      this.fetchData()
    },
    handleReset() {
      this.searchForm = {
        type: '',
        productName: '',
        category: ''
      }
      this.dateRange = null
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
    }
  }
}
</script>

<style scoped>
.stats-overview {
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

.stat-item.in .stat-value {
  color: #67c23a;
}

.stat-item.out .stat-value {
  color: #f56c6c;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style>
