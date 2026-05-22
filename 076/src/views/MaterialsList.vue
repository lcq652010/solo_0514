<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">
        <i class="el-icon-goods" style="margin-right: 10px; color: #409eff;"></i>
        物资列表
      </h2>
    </div>

    <div class="search-bar">
      <el-form :inline="true" :model="searchForm" class="demo-form-inline">
        <el-form-item label="物资名称">
          <el-input v-model="searchForm.name" placeholder="请输入物资名称" clearable></el-input>
        </el-form-item>
        <el-form-item label="物资类别">
          <el-select v-model="searchForm.category" placeholder="请选择类别" clearable>
            <el-option
              v-for="item in categoryOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
          <el-button icon="el-icon-refresh" @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="table-container">
      <el-table
        :data="filteredMaterials"
        border
        stripe
        style="width: 100%"
        :row-class-name="tableRowClassName"
      >
        <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
        <el-table-column prop="name" label="物资名称" min-width="150" align="center"></el-table-column>
        <el-table-column prop="category" label="物资类别" width="120" align="center">
          <template slot-scope="scope">
            <el-tag size="small" type="info">{{ scope.row.category }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="specification" label="规格型号" min-width="150" align="center"></el-table-column>
        <el-table-column prop="unit" label="单位" width="80" align="center"></el-table-column>
        <el-table-column prop="quantity" label="库存总量" width="100" align="center"></el-table-column>
        <el-table-column prop="available" label="可用数量" width="100" align="center">
          <template slot-scope="scope">
            <span :class="getStatusClass(scope.row.available, scope.row.quantity)">
              {{ scope.row.available }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="location" label="存放位置" min-width="130" align="center"></el-table-column>
        <el-table-column label="库存状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag
              :type="getStockStatusType(scope.row.status)"
              size="small"
            >
              {{ getStockStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button
              type="primary"
              size="mini"
              icon="el-icon-edit-outline"
              @click="handleApply(scope.row)"
              :disabled="scope.row.available === 0"
            >
              领用
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="filteredMaterials.length"
        style="margin-top: 20px; text-align: right;"
      ></el-pagination>
    </div>
  </div>
</template>

<script>
import { materials, categoryOptions } from '@/mock/data.js'

export default {
  name: 'MaterialsList',
  data() {
    return {
      searchForm: {
        name: '',
        category: ''
      },
      categoryOptions,
      materialsList: materials,
      currentPage: 1,
      pageSize: 10
    }
  },
  computed: {
    filteredMaterials() {
      let list = [...this.materialsList]
      
      if (this.searchForm.name) {
        list = list.filter(item => 
          item.name.includes(this.searchForm.name)
        )
      }
      
      if (this.searchForm.category) {
        list = list.filter(item => 
          item.category === this.searchForm.category
        )
      }
      
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return list.slice(start, end)
    }
  },
  methods: {
    tableRowClassName({ rowIndex }) {
      return rowIndex % 2 === 0 ? 'light-row' : ''
    },
    getStatusClass(available, total) {
      const ratio = available / total
      if (ratio === 0) return 'status-empty'
      if (ratio <= 0.2) return 'status-low'
      return 'status-normal'
    },
    getStockStatusType(status) {
      const typeMap = {
        normal: 'success',
        low: 'warning',
        empty: 'danger'
      }
      return typeMap[status] || 'info'
    },
    getStockStatusText(status) {
      const textMap = {
        normal: '正常',
        low: '库存低',
        empty: '无库存'
      }
      return textMap[status] || '未知'
    },
    handleSearch() {
      this.currentPage = 1
      this.$message.success('搜索完成')
    },
    handleReset() {
      this.searchForm = {
        name: '',
        category: ''
      }
      this.currentPage = 1
    },
    handleApply(row) {
      this.$router.push({
        path: '/apply',
        query: { materialId: row.id }
      })
    },
    handleSizeChange(val) {
      this.pageSize = val
    },
    handleCurrentChange(val) {
      this.currentPage = val
    }
  }
}
</script>

<style lang="scss" scoped>
.status-empty {
  color: #f56c6c;
  font-weight: 600;
}

.status-low {
  color: #e6a23c;
  font-weight: 600;
}

.status-normal {
  color: #67c23a;
  font-weight: 600;
}

.el-table {
  :deep(.el-table__header-wrapper th) {
    background-color: #f5f7fa;
    color: #303133;
    font-weight: 600;
  }
  
  :deep(.el-table__row:hover) {
    background-color: #ecf5ff !important;
  }
}
</style>
