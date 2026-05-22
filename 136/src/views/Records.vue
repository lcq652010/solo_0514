<template>
  <div class="records-page">
    <div class="page-header">
      <div class="page-title">充值记录查询</div>
      <div class="page-subtitle">查看历史充值记录和交易详情</div>
    </div>

    <div class="card-wrapper search-form">
      <el-form :inline="true" :model="searchForm" class="demo-form-inline">
        <el-form-item label="充值类型">
          <el-select v-model="searchForm.type" placeholder="请选择" clearable>
            <el-option label="水费" value="water" />
            <el-option label="电费" value="electric" />
          </el-select>
        </el-form-item>
        <el-form-item label="支付方式">
          <el-select v-model="searchForm.paymentMethod" placeholder="请选择" clearable>
            <el-option label="支付宝" value="alipay" />
            <el-option label="微信" value="wechat" />
            <el-option label="银行卡" value="bank" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择" clearable>
            <el-option label="成功" value="success" />
            <el-option label="失败" value="failed" />
          </el-select>
        </el-form-item>
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="searchForm.dateRange"
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

    <div class="card-wrapper">
      <div class="card-header">
        <span class="card-title">充值记录列表</span>
        <el-button type="text" icon="el-icon-download" @click="handleExport">导出记录</el-button>
      </div>

      <el-table
        :data="tableData"
        border
        style="width: 100%"
        v-loading="loading"
      >
        <el-table-column
          type="index"
          label="序号"
          width="60"
          align="center"
        />
        <el-table-column
          prop="id"
          label="订单号"
          min-width="180"
          show-overflow-tooltip
        />
        <el-table-column
          prop="dormitory"
          label="宿舍"
          width="120"
          align="center"
        />
        <el-table-column
          prop="type"
          label="充值类型"
          width="100"
          align="center"
        >
          <template slot-scope="scope">
            <el-tag :type="scope.row.type === 'water' ? 'primary' : 'success'" size="small">
              {{ scope.row.type === 'water' ? '水费' : '电费' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="amount"
          label="充值金额"
          width="120"
          align="center"
        >
          <template slot-scope="scope">
            <span class="amount-text">¥{{ scope.row.amount.toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column
          prop="paymentMethod"
          label="支付方式"
          width="100"
          align="center"
        >
          <template slot-scope="scope">
            <span v-if="scope.row.paymentMethod === 'alipay'">支付宝</span>
            <span v-else-if="scope.row.paymentMethod === 'wechat'">微信</span>
            <span v-else>银行卡</span>
          </template>
        </el-table-column>
        <el-table-column
          prop="status"
          label="状态"
          width="100"
          align="center"
        >
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === 'success' ? 'success' : 'danger'" size="small">
              {{ scope.row.status === 'success' ? '成功' : '失败' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="createTime"
          label="充值时间"
          min-width="180"
          align="center"
        />
        <el-table-column
          label="操作"
          width="120"
          align="center"
          fixed="right"
        >
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="handleViewDetail(scope.row)">
              详情
            </el-button>
            <el-button
              v-if="scope.row.status === 'success'"
              type="text"
              size="small"
              @click="handlePrint(scope.row)"
            >
              打印
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrapper">
        <span class="total-text">共 {{ total }} 条记录</span>
        <el-pagination
          background
          layout="prev, pager, next, jumper"
          :total="total"
          :page-size="pageSize"
          :current-page="currentPage"
          @current-change="handlePageChange"
        />
      </div>
    </div>

    <el-dialog
      title="充值详情"
      :visible.sync="detailVisible"
      width="500px"
    >
      <el-descriptions :column="1" border v-if="currentRecord">
        <el-descriptions-item label="订单号">
          {{ currentRecord.id }}
        </el-descriptions-item>
        <el-descriptions-item label="宿舍">
          {{ currentRecord.dormitory }}
        </el-descriptions-item>
        <el-descriptions-item label="充值类型">
          {{ currentRecord.type === 'water' ? '水费' : '电费' }}
        </el-descriptions-item>
        <el-descriptions-item label="充值金额">
          <span style="color: #F56C6C; font-weight: 600; font-size: 18px;">
            ¥{{ currentRecord.amount.toFixed(2) }}
          </span>
        </el-descriptions-item>
        <el-descriptions-item label="支付方式">
          <span v-if="currentRecord.paymentMethod === 'alipay'">支付宝</span>
          <span v-else-if="currentRecord.paymentMethod === 'wechat'">微信</span>
          <span v-else>银行卡</span>
        </el-descriptions-item>
        <el-descriptions-item label="交易状态">
          <el-tag :type="currentRecord.status === 'success' ? 'success' : 'danger'" size="small">
            {{ currentRecord.status === 'success' ? '交易成功' : '交易失败' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="充值时间">
          {{ currentRecord.createTime }}
        </el-descriptions-item>
      </el-descriptions>
      <div slot="footer" class="dialog-footer">
        <el-button @click="detailVisible = false">关闭</el-button>
        <el-button type="primary" @click="handlePrint(currentRecord)">打印凭证</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { rechargeRecords } from '@/data/mock.js'

export default {
  name: 'Records',
  data() {
    return {
      loading: false,
      detailVisible: false,
      currentRecord: null,
      searchForm: {
        type: '',
        paymentMethod: '',
        status: '',
        dateRange: []
      },
      filteredData: [],
      tableData: [],
      total: 0,
      currentPage: 1,
      pageSize: 10
    }
  },
  created() {
    this.loadData()
  },
  methods: {
    loadData() {
      this.loading = true
      setTimeout(() => {
        let data = [...rechargeRecords]
        
        if (this.searchForm.type) {
          data = data.filter(item => item.type === this.searchForm.type)
        }
        
        if (this.searchForm.paymentMethod) {
          data = data.filter(item => item.paymentMethod === this.searchForm.paymentMethod)
        }
        
        if (this.searchForm.status) {
          data = data.filter(item => item.status === this.searchForm.status)
        }
        
        if (this.searchForm.dateRange && this.searchForm.dateRange.length === 2) {
          const [startDate, endDate] = this.searchForm.dateRange
          data = data.filter(item => {
            const itemDate = item.createTime.split(' ')[0].replace(/\//g, '-')
            return itemDate >= startDate && itemDate <= endDate
          })
        }
        
        this.filteredData = data
        this.total = data.length
        this.updateTableData()
        this.loading = false
      }, 500)
    },
    updateTableData() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      this.tableData = this.filteredData.slice(start, end)
    },
    handleSearch() {
      this.currentPage = 1
      this.loadData()
    },
    handleReset() {
      this.searchForm = {
        type: '',
        paymentMethod: '',
        status: '',
        dateRange: []
      }
      this.currentPage = 1
      this.loadData()
    },
    handlePageChange(page) {
      this.currentPage = page
      this.updateTableData()
    },
    handleViewDetail(record) {
      this.currentRecord = record
      this.detailVisible = true
    },
    handlePrint(record) {
      this.$message.success('正在准备打印凭证...')
    },
    handleExport() {
      this.$message.success('记录已导出，请注意查收！')
    }
  }
}
</script>

<style scoped>
.records-page {
  width: 100%;
}

.amount-text {
  font-weight: 600;
  color: #E6A23C;
}

.pagination-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}

.total-text {
  color: #606266;
  font-size: 14px;
}

.demo-form-inline {
  display: flex;
  flex-wrap: wrap;
}

.demo-form-inline .el-form-item {
  margin-right: 20px;
  margin-bottom: 0;
}
</style>
