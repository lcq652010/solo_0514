<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">
        <i class="el-icon-document" style="margin-right: 10px; color: #409eff;"></i>
        领用记录
      </h2>
    </div>

    <el-row :gutter="20" style="margin-bottom: 20px;">
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon pending">
              <i class="el-icon-time"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ pendingCount }}</div>
              <div class="stat-label">待审批</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon approved">
              <i class="el-icon-check"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ approvedCount }}</div>
              <div class="stat-label">已批准</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon returned">
              <i class="el-icon-circle-check"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ returnedCount }}</div>
              <div class="stat-label">已归还</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon rejected">
              <i class="el-icon-close"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ rejectedCount }}</div>
              <div class="stat-label">已拒绝</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <div class="search-bar">
      <el-form :inline="true" :model="searchForm" class="demo-form-inline">
        <el-form-item label="物资名称">
          <el-input 
            v-model="searchForm.materialName" 
            placeholder="请输入物资名称" 
            clearable
            @input="debouncedSearch"
          ></el-input>
        </el-form-item>
        <el-form-item label="状态">
          <el-select 
            v-model="searchForm.status" 
            placeholder="请选择状态" 
            clearable
            @change="handleFilterChange"
          >
            <el-option label="待审批" value="pending"></el-option>
            <el-option label="已批准" value="approved"></el-option>
            <el-option label="已拒绝" value="rejected"></el-option>
            <el-option label="已归还" value="returned"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="申请日期">
          <el-date-picker
            v-model="searchForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="yyyy-MM-dd"
            @change="handleFilterChange"
          ></el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
          <el-button icon="el-icon-refresh" @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="table-container">
      <div class="table-info">
        <span v-if="totalRecords > 0" class="result-count">
          共找到 <strong>{{ totalRecords }}</strong> 条记录，当前显示第 <strong>{{ (currentPage - 1) * pageSize + 1 }}</strong> - <strong>{{ Math.min(currentPage * pageSize, totalRecords) }}</strong> 条
        </span>
        <span v-else class="result-empty">暂无匹配记录</span>
      </div>
      <el-table
        :data="paginatedRecords"
        border
        stripe
        style="width: 100%"
        v-loading="loading"
        element-loading-text="数据加载中..."
        @sort-change="handleSortChange"
      >
        <el-table-column type="index" label="序号" width="70" align="center" :index="indexMethod"></el-table-column>
        <el-table-column prop="materialName" label="物资名称" min-width="150" align="center" sortable="custom"></el-table-column>
        <el-table-column prop="specification" label="规格型号" min-width="150" align="center"></el-table-column>
        <el-table-column prop="applicant" label="申请人" width="100" align="center"></el-table-column>
        <el-table-column prop="department" label="部门" width="100" align="center"></el-table-column>
        <el-table-column prop="applyQuantity" label="数量" width="80" align="center" sortable="custom"></el-table-column>
        <el-table-column prop="applyDate" label="申请日期" width="130" align="center" sortable="custom"></el-table-column>
        <el-table-column prop="expectReturnDate" label="预计归还" width="130" align="center"></el-table-column>
        <el-table-column label="状态" width="120" align="center">
          <template slot-scope="scope">
            <el-tag
              :class="getStatusClass(scope.row.status)"
              :type="getStatusType(scope.row.status)"
              :effect="getStatusEffect(scope.row.status)"
              size="small"
            >
              <i :class="getStatusIcon(scope.row.status)" style="margin-right: 4px;"></i>
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="审批人" width="100" align="center">
          <template slot-scope="scope">
            {{ scope.row.approver || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="实际归还" width="110" align="center">
          <template slot-scope="scope">
            {{ scope.row.actualReturnDate || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button
              type="info"
              size="mini"
              icon="el-icon-view"
              @click="handleView(scope.row)"
            >
              详情
            </el-button>
            <el-button
              v-if="scope.row.status === 'pending'"
              type="warning"
              size="mini"
              icon="el-icon-delete"
              @click="handleCancel(scope.row)"
            >
              撤销
            </el-button>
            <el-button
              v-if="scope.row.status === 'approved'"
              type="success"
              size="mini"
              icon="el-icon-refresh-left"
              @click="handleReturn(scope.row)"
            >
              归还
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 50, 100, 200, 500]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper, slot"
        :total="totalRecords"
        background
        style="margin-top: 20px; justify-content: flex-end;"
      >
        <span class="page-jump-tip" style="margin-left: 10px; color: #606266;">
          跳至
          <el-input-number
            v-model="jumpPage"
            :min="1"
            :max="Math.ceil(totalRecords / pageSize) || 1"
            size="small"
            style="width: 100px; margin: 0 5px;"
            @change="handleJumpPage"
          ></el-input-number>
          页
        </span>
      </el-pagination>
    </div>

    <el-dialog
      title="领用详情"
      :visible.sync="detailDialogVisible"
      width="600px"
    >
      <el-descriptions :column="2" border v-if="currentRecord">
        <el-descriptions-item label="物资名称">{{ currentRecord.materialName }}</el-descriptions-item>
        <el-descriptions-item label="规格型号">{{ currentRecord.specification }}</el-descriptions-item>
        <el-descriptions-item label="申请人">{{ currentRecord.applicant }}</el-descriptions-item>
        <el-descriptions-item label="所属部门">{{ currentRecord.department }}</el-descriptions-item>
        <el-descriptions-item label="领用数量">{{ currentRecord.applyQuantity }}</el-descriptions-item>
        <el-descriptions-item label="申请日期">{{ currentRecord.applyDate }}</el-descriptions-item>
        <el-descriptions-item label="预计归还">{{ currentRecord.expectReturnDate }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag
            :class="getStatusClass(currentRecord.status)"
            :type="getStatusType(currentRecord.status)"
            :effect="getStatusEffect(currentRecord.status)"
            size="small"
          >
            <i :class="getStatusIcon(currentRecord.status)" style="margin-right: 4px;"></i>
            {{ getStatusText(currentRecord.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="领用用途" :span="2">{{ currentRecord.purpose }}</el-descriptions-item>
        <el-descriptions-item v-if="currentRecord.approver" label="审批人">{{ currentRecord.approver }}</el-descriptions-item>
        <el-descriptions-item v-if="currentRecord.approveDate" label="审批日期">{{ currentRecord.approveDate }}</el-descriptions-item>
        <el-descriptions-item v-if="currentRecord.actualReturnDate" label="实际归还">{{ currentRecord.actualReturnDate }}</el-descriptions-item>
        <el-descriptions-item v-if="currentRecord.rejectReason" label="拒绝原因" :span="2">{{ currentRecord.rejectReason }}</el-descriptions-item>
      </el-descriptions>
      <span slot="footer" class="dialog-footer">
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { applyRecords } from '@/mock/data.js'

export default {
  name: 'MyRecords',
  data() {
    return {
      recordsList: applyRecords,
      searchForm: {
        materialName: '',
        status: '',
        dateRange: []
      },
      currentPage: 1,
      pageSize: 10,
      jumpPage: 1,
      detailDialogVisible: false,
      currentRecord: null,
      loading: false,
      sort: {
        prop: '',
        order: ''
      },
      searchTimer: null,
      cachedFilteredList: null,
      cacheKey: ''
    }
  },
  computed: {
    pendingCount() {
      return this.recordsList.filter(item => item.status === 'pending').length
    },
    approvedCount() {
      return this.recordsList.filter(item => item.status === 'approved').length
    },
    returnedCount() {
      return this.recordsList.filter(item => item.status === 'returned').length
    },
    rejectedCount() {
      return this.recordsList.filter(item => item.status === 'rejected').length
    },
    totalPages() {
      return Math.ceil(this.totalRecords / this.pageSize) || 1
    },
    filteredRecords() {
      const newCacheKey = `${this.searchForm.materialName}-${this.searchForm.status}-${this.searchForm.dateRange?.join(',')}-${this.sort.prop}-${this.sort.order}`
      
      if (this.cachedFilteredList && this.cacheKey === newCacheKey) {
        return this.cachedFilteredList
      }
      
      this.cacheKey = newCacheKey
      let list = [...this.recordsList]

      if (this.searchForm.materialName) {
        const keyword = this.searchForm.materialName.toLowerCase()
        list = list.filter(item => 
          item.materialName.toLowerCase().includes(keyword)
        )
      }

      if (this.searchForm.status) {
        list = list.filter(item => item.status === this.searchForm.status)
      }

      if (this.searchForm.dateRange && this.searchForm.dateRange.length === 2) {
        const [startDate, endDate] = this.searchForm.dateRange
        list = list.filter(item => 
          item.applyDate >= startDate && item.applyDate <= endDate
        )
      }

      if (this.sort.prop && this.sort.order) {
        list.sort((a, b) => {
          let aVal = a[this.sort.prop]
          let bVal = b[this.sort.prop]
          
          if (this.sort.prop === 'applyQuantity') {
            aVal = Number(aVal)
            bVal = Number(bVal)
          }
          
          if (this.sort.order === 'ascending') {
            return aVal > bVal ? 1 : -1
          } else {
            return aVal < bVal ? 1 : -1
          }
        })
      }

      this.cachedFilteredList = list
      return list
    },
    paginatedRecords() {
      const list = this.filteredRecords
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return list.slice(start, end)
    },
    totalRecords() {
      return this.filteredRecords.length
    }
  },
  watch: {
    currentPage(newVal) {
      this.jumpPage = newVal
    }
  },
  methods: {
    getStatusType(status) {
      const typeMap = {
        pending: 'warning',
        approved: 'primary',
        rejected: 'danger',
        returned: 'success'
      }
      return typeMap[status] || 'info'
    },
    getStatusEffect(status) {
      const effectMap = {
        pending: 'light',
        approved: 'dark',
        rejected: 'light',
        returned: 'plain'
      }
      return effectMap[status] || 'light'
    },
    getStatusClass(status) {
      const classMap = {
        pending: 'status-tag-pending',
        approved: 'status-tag-approved',
        rejected: 'status-tag-rejected',
        returned: 'status-tag-returned'
      }
      return classMap[status] || ''
    },
    getStatusIcon(status) {
      const iconMap = {
        pending: 'el-icon-time',
        approved: 'el-icon-check',
        rejected: 'el-icon-close',
        returned: 'el-icon-circle-check'
      }
      return iconMap[status] || ''
    },
    getStatusText(status) {
      const textMap = {
        pending: '待审批',
        approved: '已批准',
        rejected: '已拒绝',
        returned: '已归还'
      }
      return textMap[status] || '未知'
    },
    indexMethod(index) {
      return (this.currentPage - 1) * this.pageSize + index + 1
    },
    debouncedSearch() {
      if (this.searchTimer) {
        clearTimeout(this.searchTimer)
      }
      this.searchTimer = setTimeout(() => {
        this.handleFilterChange()
      }, 300)
    },
    handleFilterChange() {
      this.loading = true
      this.currentPage = 1
      this.cachedFilteredList = null
      setTimeout(() => {
        this.loading = false
      }, 100)
    },
    handleSearch() {
      this.loading = true
      this.currentPage = 1
      this.cachedFilteredList = null
      setTimeout(() => {
        this.loading = false
        this.$message.success(`搜索完成，共找到 ${this.totalRecords} 条记录`)
      }, 200)
    },
    handleReset() {
      this.searchForm = {
        materialName: '',
        status: '',
        dateRange: []
      }
      this.sort = {
        prop: '',
        order: ''
      }
      this.currentPage = 1
      this.cachedFilteredList = null
    },
    handleSortChange({ prop, order }) {
      this.sort = { prop, order }
      this.cachedFilteredList = null
    },
    handleView(row) {
      this.currentRecord = row
      this.detailDialogVisible = true
    },
    handleCancel(row) {
      this.$confirm('确认要撤销该领用申请吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.recordsList.findIndex(item => item.id === row.id)
        if (index > -1) {
          this.recordsList.splice(index, 1)
        }
        this.cachedFilteredList = null
        this.$message.success('撤销成功！')
      }).catch(() => {})
    },
    handleReturn(row) {
      this.$router.push({
        path: '/return',
        query: { recordId: row.id }
      })
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.currentPage = 1
      this.$nextTick(() => {
        if (this.jumpPage > this.totalPages) {
          this.jumpPage = this.totalPages
        }
      })
    },
    handleCurrentChange(val) {
      this.currentPage = val
    },
    handleJumpPage(val) {
      if (val >= 1 && val <= this.totalPages) {
        this.currentPage = val
      }
    }
  },
  beforeDestroy() {
    if (this.searchTimer) {
      clearTimeout(this.searchTimer)
    }
  }
}
</script>

<style lang="scss" scoped>
.stat-card {
  border-radius: 8px;
  height: 100%;

  :deep(.el-card__body) {
    padding: 20px;
  }
}

.table-info {
  padding: 12px 0;
  font-size: 14px;
  color: #606266;
  display: flex;
  justify-content: space-between;
  align-items: center;

  .result-count {
    strong {
      color: #409eff;
      font-weight: 600;
    }
  }

  .result-empty {
    color: #909399;
  }
}

.el-pagination {
  display: flex;
  align-items: center;
  padding: 15px 0;
}

.page-jump-tip {
  display: flex;
  align-items: center;
  font-size: 14px;

  :deep(.el-input-number .el-input__inner) {
    text-align: center;
  }
}

.stat-content {
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: #fff;
  margin-right: 20px;

  &.pending {
    background: linear-gradient(135deg, #e6a23c 0%, #f5a623 100%);
  }

  &.approved {
    background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  }

  &.returned {
    background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
  }

  &.rejected {
    background: linear-gradient(135deg, #f56c6c 0%, #f78989 100%);
  }
}

.stat-info {
  flex: 1;

  .stat-value {
    font-size: 28px;
    font-weight: 600;
    color: #303133;
    margin-bottom: 5px;
  }

  .stat-label {
    font-size: 14px;
    color: #909399;
  }
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

.status-tag-pending {
  :deep(.el-tag) {
    background: linear-gradient(135deg, #fef3e6 0%, #fdf6ec 100%);
    border-color: #e6a23c;
    color: #e6a23c;
    font-weight: 500;
    padding: 4px 12px;
  }
}

.status-tag-approved {
  :deep(.el-tag) {
    background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
    border: none;
    color: #fff;
    font-weight: 500;
    padding: 4px 12px;
    box-shadow: 0 2px 8px rgba(64, 158, 255, 0.3);
  }
}

.status-tag-rejected {
  :deep(.el-tag) {
    background: linear-gradient(135deg, #fef0f0 0%, #fef2f2 100%);
    border-color: #f56c6c;
    color: #f56c6c;
    font-weight: 500;
    padding: 4px 12px;
  }
}

.status-tag-returned {
  :deep(.el-tag) {
    background: linear-gradient(135deg, #f0f9ff 0%, #f0f9eb 100%);
    border-color: #67c23a;
    color: #67c23a;
    font-weight: 500;
    padding: 4px 12px;
  }
}
</style>
