<template>
  <div class="stock-warning-page">
    <div class="page-card">
      <div class="page-title">
        <i class="el-icon-warning"></i>
        库存预警
      </div>
      
      <div class="statistics-row">
        <el-card class="stat-card">
          <div class="stat-content warning">
            <div class="stat-icon">
              <i class="el-icon-warning"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ warningCount }}</div>
              <div class="stat-label">预警商品</div>
            </div>
          </div>
        </el-card>
        
        <el-card class="stat-card">
          <div class="stat-content normal">
            <div class="stat-icon">
              <i class="el-icon-success"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ normalCount }}</div>
              <div class="stat-label">正常库存</div>
            </div>
          </div>
        </el-card>
        
        <el-card class="stat-card">
          <div class="stat-content primary">
            <div class="stat-icon">
              <i class="el-icon-goods"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ totalCount }}</div>
              <div class="stat-label">商品总数</div>
            </div>
          </div>
        </el-card>
        
        <el-card class="stat-card">
          <div class="stat-content danger">
            <div class="stat-icon">
              <i class="el-icon-close"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ zeroStockCount }}</div>
              <div class="stat-label">缺货商品</div>
            </div>
          </div>
        </el-card>
      </div>
      
      <el-tabs v-model="activeTab" style="margin-top: 20px;">
        <el-tab-pane label="预警商品" name="warning">
          <el-alert
            title="以下商品库存已低于最低库存警戒线，请及时补货！"
            type="warning"
            :closable="false"
            style="margin-bottom: 20px;"
          />
          
          <el-table :data="warningProducts" border stripe style="width: 100%">
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
            <el-table-column prop="stock" label="当前库存" width="120" align="center">
              <template slot-scope="scope">
                <el-tag type="danger" size="small">{{ scope.row.stock }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="minStock" label="最低库存" width="100" align="center" />
            <el-table-column label="库存缺口" width="120" align="center">
              <template slot-scope="scope">
                <span style="color: #f56c6c; font-weight: 600;">{{ scope.row.minStock - scope.row.stock }}</span>
              </template>
            </el-table-column>
            <el-table-column label="预警等级" width="100" align="center">
              <template slot-scope="scope">
                <el-tag :type="getWarningLevel(scope.row).type" size="small">
                  {{ getWarningLevel(scope.row).text }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
          
          <el-empty v-if="warningProducts.length === 0" description="暂无预警商品" style="padding: 40px 0;" />
        </el-tab-pane>
        
        <el-tab-pane label="全部商品库存" name="all">
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
          </div>
          
          <el-table :data="filteredProducts" border stripe style="width: 100%">
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
            <el-table-column prop="stock" label="当前库存" width="120" align="center">
              <template slot-scope="scope">
                <el-tag :type="scope.row.stock <= scope.row.minStock ? 'danger' : 'success'" size="small">
                  {{ scope.row.stock }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="minStock" label="最低库存" width="100" align="center" />
            <el-table-column label="库存状态" width="100" align="center">
              <template slot-scope="scope">
                <el-tag :type="scope.row.stock <= scope.row.minStock ? 'danger' : 'success'" size="small">
                  {{ scope.row.stock <= scope.row.minStock ? '库存不足' : '库存正常' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="库存进度" width="200" align="center">
              <template slot-scope="scope">
                <el-progress
                  :percentage="Math.min(100, Math.round((scope.row.stock / (scope.row.minStock * 3)) * 100))"
                  :color="getProgressColor(scope.row)"
                  :stroke-width="12"
                />
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
import { products } from '@/mock/data'

export default {
  name: 'StockWarning',
  data() {
    return {
      activeTab: 'warning',
      searchForm: {
        name: '',
        category: ''
      }
    }
  },
  computed: {
    warningProducts() {
      return products.filter(item => item.stock <= item.minStock)
    },
    filteredProducts() {
      let data = [...products]
      
      if (this.searchForm.name) {
        data = data.filter(item => item.name.includes(this.searchForm.name))
      }
      
      if (this.searchForm.category) {
        data = data.filter(item => item.category === this.searchForm.category)
      }
      
      return data
    },
    warningCount() {
      return this.warningProducts.length
    },
    normalCount() {
      return products.filter(item => item.stock > item.minStock).length
    },
    totalCount() {
      return products.length
    },
    zeroStockCount() {
      return products.filter(item => item.stock <= 0).length
    }
  },
  methods: {
    handleSearch() {
    },
    getWarningLevel(product) {
      const gap = product.minStock - product.stock
      const ratio = gap / product.minStock
      
      if (product.stock <= 0) {
        return { type: 'danger', text: '严重' }
      } else if (ratio >= 0.5) {
        return { type: 'danger', text: '紧急' }
      } else {
        return { type: 'warning', text: '一般' }
      }
    },
    getProgressColor(product) {
      if (product.stock <= 0) {
        return '#f56c6c'
      } else if (product.stock <= product.minStock) {
        return '#e6a23c'
      } else {
        return '#67c23a'
      }
    }
  }
}
</script>

<style lang="less" scoped>
.stock-warning-page {
  .statistics-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 20px;
    
    .stat-card {
      /deep/ .el-card__body {
        padding: 20px;
      }
      
      .stat-content {
        display: flex;
        align-items: center;
        gap: 15px;
        
        .stat-icon {
          width: 60px;
          height: 60px;
          border-radius: 10px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 28px;
          
          &.warning {
            background: #fdf6ec;
            color: #e6a23c;
          }
          
          &.normal {
            background: #f0f9eb;
            color: #67c23a;
          }
          
          &.primary {
            background: #ecf5ff;
            color: #409eff;
          }
          
          &.danger {
            background: #fef0f0;
            color: #f56c6c;
          }
        }
        
        .stat-info {
          .stat-value {
            font-size: 28px;
            font-weight: 600;
            color: #303133;
            line-height: 1.2;
          }
          
          .stat-label {
            font-size: 14px;
            color: #909399;
            margin-top: 5px;
          }
        }
      }
    }
  }
  
  .search-form {
    display: flex;
    gap: 15px;
    margin-bottom: 20px;
  }
}
</style>
