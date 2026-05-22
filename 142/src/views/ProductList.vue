<template>
  <div class="page-container">
    <div class="page-header">
      <h2>商品列表</h2>
    </div>
    <div class="page-content">
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm" class="demo-form-inline">
          <el-form-item label="商品名称">
            <el-input v-model="searchForm.name" placeholder="请输入商品名称" clearable />
          </el-form-item>
          <el-form-item label="商品编码">
            <el-input v-model="searchForm.code" placeholder="请输入商品编码" clearable />
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
            <el-button type="primary" @click="handleSearch">查询</el-button>
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
          :row-class-name="getTableRowClassName"
        >
          <el-table-column prop="id" label="ID" width="80" align="center" />
          <el-table-column prop="code" label="商品编码" width="120" align="center" />
          <el-table-column prop="name" label="商品名称" min-width="150" />
          <el-table-column prop="category" label="分类" width="100" align="center" />
          <el-table-column prop="price" label="单价(元)" width="100" align="center">
            <template slot-scope="scope">
              ¥{{ scope.row.price.toFixed(2) }}
            </template>
          </el-table-column>
          <el-table-column prop="stock" label="库存数量" width="100" align="center">
            <template slot-scope="scope">
              <span :style="{ color: scope.row.stock < scope.row.minStock ? '#f56c6c' : '' }">
                {{ scope.row.stock }}{{ scope.row.unit }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="minStock" label="最低库存" width="100" align="center" />
          <el-table-column prop="createTime" label="创建时间" width="180" align="center" />
          <el-table-column label="操作" width="150" align="center" fixed="right">
            <template slot-scope="scope">
              <el-button type="text" size="small" @click="handleView(scope.row)">
                查看
              </el-button>
              <el-button type="text" size="small" @click="handleStockIn(scope.row)">
                入库
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

    <el-dialog title="商品详情" :visible.sync="dialogVisible" width="500px">
      <el-descriptions :column="2" border v-if="currentProduct">
        <el-descriptions-item label="商品编码">{{ currentProduct.code }}</el-descriptions-item>
        <el-descriptions-item label="商品名称">{{ currentProduct.name }}</el-descriptions-item>
        <el-descriptions-item label="商品分类">{{ currentProduct.category }}</el-descriptions-item>
        <el-descriptions-item label="单价">¥{{ currentProduct.price.toFixed(2) }}</el-descriptions-item>
        <el-descriptions-item label="当前库存">{{ currentProduct.stock }}{{ currentProduct.unit }}</el-descriptions-item>
        <el-descriptions-item label="最低库存">{{ currentProduct.minStock }}{{ currentProduct.unit }}</el-descriptions-item>
        <el-descriptions-item label="创建时间" :span="2">{{ currentProduct.createTime }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script>
import { api, categories, eventBus } from '../api/mockData'

export default {
  name: 'ProductList',
  data() {
    return {
      loading: false,
      categories,
      searchForm: {
        name: '',
        code: '',
        category: ''
      },
      tableData: [],
      pagination: {
        page: 1,
        pageSize: 10,
        total: 0
      },
      dialogVisible: false,
      currentProduct: null
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
          ...this.searchForm,
          page: this.pagination.page,
          pageSize: this.pagination.pageSize
        }
        const res = await api.getProducts(params)
        if (res.code === 200) {
          this.tableData = res.data.list
          this.pagination.total = res.data.total
        }
      } catch (error) {
        this.$message.error('获取数据失败')
      } finally {
        this.loading = false
      }
    },
    handleSearch() {
      this.pagination.page = 1
      this.fetchData()
    },
    handleReset() {
      this.searchForm = {
        name: '',
        code: '',
        category: ''
      }
      this.pagination.page = 1
      this.fetchData()
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.pagination.page = 1
      this.fetchData()
    },
    handleCurrentChange(val) {
      this.pagination.page = val
      this.fetchData()
    },
    handleView(row) {
      this.currentProduct = row
      this.dialogVisible = true
    },
    handleStockIn(row) {
      this.$router.push({
        path: '/stock-in',
        query: { productId: row.id }
      })
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
