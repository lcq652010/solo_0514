<template>
  <div class="products-page">
    <div class="page-card">
      <div class="page-title">
        <i class="el-icon-goods"></i>
        建材商品列表
      </div>
      
      <div class="search-form">
        <el-input
          v-model="searchForm.name"
          placeholder="商品名称"
          clearable
          style="width: 200px"
        />
        <el-select
          v-model="searchForm.category"
          placeholder="商品分类"
          clearable
          style="width: 150px"
        >
          <el-option label="水泥" value="水泥" />
          <el-option label="钢材" value="钢材" />
          <el-option label="砂石" value="砂石" />
          <el-option label="砖瓦" value="砖瓦" />
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
        <el-table-column prop="name" label="商品名称" min-width="180" />
        <el-table-column prop="category" label="分类" width="100" align="center" />
        <el-table-column prop="brand" label="品牌" width="100" align="center" />
        <el-table-column prop="spec" label="规格" width="120" align="center" />
        <el-table-column prop="unit" label="单位" width="80" align="center" />
        <el-table-column prop="price" label="单价（元）" width="120" align="center">
          <template slot-scope="scope">
            <span style="color: #f56c6c; font-weight: 600;">{{ scope.row.price.toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="stock" label="库存" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.stock <= scope.row.minStock ? 'danger' : 'success'" size="small">
              {{ scope.row.stock }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="minStock" label="最低库存" width="100" align="center" />
        <el-table-column label="操作" width="120" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="handleView(scope.row)">
              查看
            </el-button>
            <el-button type="text" size="small" @click="handleOrder(scope.row)">
              下单
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
    
    <el-dialog title="商品详情" :visible.sync="detailDialogVisible" width="500px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="商品名称">{{ currentProduct.name }}</el-descriptions-item>
        <el-descriptions-item label="分类">{{ currentProduct.category }}</el-descriptions-item>
        <el-descriptions-item label="品牌">{{ currentProduct.brand }}</el-descriptions-item>
        <el-descriptions-item label="规格">{{ currentProduct.spec }}</el-descriptions-item>
        <el-descriptions-item label="单位">{{ currentProduct.unit }}</el-descriptions-item>
        <el-descriptions-item label="单价">{{ currentProduct.price }} 元</el-descriptions-item>
        <el-descriptions-item label="当前库存">{{ currentProduct.stock }}</el-descriptions-item>
        <el-descriptions-item label="最低库存">{{ currentProduct.minStock }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script>
import { products } from '@/mock/data'

export default {
  name: 'Products',
  data() {
    return {
      searchForm: {
        name: '',
        category: ''
      },
      tableData: [],
      pagination: {
        page: 1,
        size: 10,
        total: 0
      },
      detailDialogVisible: false,
      currentProduct: {}
    }
  },
  created() {
    this.loadData()
  },
  methods: {
    loadData() {
      let data = [...products]
      
      if (this.searchForm.name) {
        data = data.filter(item => item.name.includes(this.searchForm.name))
      }
      
      if (this.searchForm.category) {
        data = data.filter(item => item.category === this.searchForm.category)
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
        name: '',
        category: ''
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
      this.currentProduct = { ...row }
      this.detailDialogVisible = true
    },
    handleOrder(row) {
      this.$router.push({
        path: '/order-create',
        query: { productId: row.id }
      })
    }
  }
}
</script>

<style lang="less" scoped>
.products-page {
  .el-descriptions {
    /deep/ .el-descriptions__label {
      background: #f5f7fa;
      width: 120px;
    }
  }
}
</style>
