<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">交易流水记录</h2>
      <div>
        <el-button type="primary" size="small" icon="el-icon-download">导出数据</el-button>
      </div>
    </div>

    <el-form :model="searchForm" class="search-form">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-form-item label="交易单号">
            <el-input v-model="searchForm.orderNo" placeholder="请输入交易单号" clearable></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="会员编号">
            <el-input v-model="searchForm.memberNo" placeholder="请输入会员编号" clearable></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="会员姓名">
            <el-input v-model="searchForm.memberName" placeholder="请输入会员姓名" clearable></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="手机号码">
            <el-input v-model="searchForm.phone" placeholder="请输入手机号码" clearable></el-input>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="6">
          <el-form-item label="交易类型">
            <el-select v-model="searchForm.type" placeholder="请选择交易类型" clearable style="width: 100%;">
              <el-option label="全部" :value="null"></el-option>
              <el-option label="充值" :value="1"></el-option>
              <el-option label="消费" :value="2"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="支付方式">
            <el-select v-model="searchForm.paymentMethod" placeholder="请选择支付方式" clearable style="width: 100%;">
              <el-option label="全部" value=""></el-option>
              <el-option label="现金支付" value="现金支付"></el-option>
              <el-option label="微信支付" value="微信支付"></el-option>
              <el-option label="支付宝支付" value="支付宝支付"></el-option>
              <el-option label="银行转账" value="银行转账"></el-option>
              <el-option label="余额支付" value="余额支付"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="交易时间">
            <el-date-picker
              v-model="searchForm.dateRange"
              type="datetimerange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              value-format="yyyy-MM-dd HH:mm:ss"
              style="width: 100%;"
            ></el-date-picker>
          </el-form-item>
        </el-col>
        <el-col :span="4">
          <el-form-item>
            <el-button type="primary" @click="handleSearch" style="width: 80px;">
              <i class="el-icon-search"></i> 搜索
            </el-button>
            <el-button @click="handleReset" style="width: 80px; margin-left: 8px;">
              <i class="el-icon-refresh"></i> 重置
            </el-button>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <el-card shadow="never" style="margin-bottom: 15px;">
      <div class="stats-panel">
        <div class="stat-item">
          <span class="stat-label">交易笔数</span>
          <span class="stat-value">{{ pagination.total }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">充值总金额</span>
          <span class="stat-value income">¥{{ rechargeTotal | formatMoney }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">消费总金额</span>
          <span class="stat-value expense">¥{{ consumeTotal | formatMoney }}</span>
        </div>
      </div>
    </el-card>

    <el-table :data="tableData" border stripe style="width: 100%" v-loading="loading">
      <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
      <el-table-column prop="orderNo" label="交易单号" width="180" align="center" show-overflow-tooltip></el-table-column>
      <el-table-column prop="memberNo" label="会员编号" width="100" align="center"></el-table-column>
      <el-table-column prop="memberName" label="会员姓名" width="100" align="center"></el-table-column>
      <el-table-column prop="phone" label="手机号码" width="130" align="center"></el-table-column>
      <el-table-column prop="type" label="交易类型" width="100" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.type === 1 ? 'success' : 'danger'" size="small">
            {{ scope.row.type === 1 ? '充值' : '消费' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="amount" label="交易金额" width="120" align="center">
        <template slot-scope="scope">
          <span :style="{ color: scope.row.type === 1 ? '#67c23a' : '#f56c6c', fontWeight: 'bold' }">
            {{ scope.row.type === 1 ? '+' : '-' }}¥{{ scope.row.amount | formatMoney }}
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="beforeBalance" label="交易前余额" width="120" align="center">
        <template slot-scope="scope">
          ¥{{ scope.row.beforeBalance | formatMoney }}
        </template>
      </el-table-column>
      <el-table-column prop="afterBalance" label="交易后余额" width="120" align="center">
        <template slot-scope="scope">
          ¥{{ scope.row.afterBalance | formatMoney }}
        </template>
      </el-table-column>
      <el-table-column prop="paymentMethod" label="支付方式" width="120" align="center"></el-table-column>
      <el-table-column prop="operator" label="操作员" width="100" align="center"></el-table-column>
      <el-table-column prop="remark" label="备注" align="center" show-overflow-tooltip min-width="150"></el-table-column>
      <el-table-column prop="createTime" label="交易时间" width="170" align="center"></el-table-column>
    </el-table>

    <div class="pagination-container">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="pagination.page"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pagination.size"
        layout="total, sizes, prev, pager, next, jumper"
        :total="pagination.total"
      >
      </el-pagination>
    </div>
  </div>
</template>

<script>
import { getTransactionsWithMemberInfo } from '@/mock/data'
import { EventBus } from '@/utils/eventBus'

export default {
  name: 'TransactionList',
  data() {
    return {
      loading: false,
      searchForm: {
        orderNo: '',
        memberNo: '',
        memberName: '',
        phone: '',
        type: null,
        paymentMethod: '',
        dateRange: null
      },
      allTransactions: [],
      tableData: [],
      pagination: {
        page: 1,
        size: 10,
        total: 0,
        sizes: [10, 20, 50, 100]
      }
    }
  },
  computed: {
    rechargeTotal() {
      return this.allTransactions
        .filter(t => t.type === 1)
        .reduce((sum, t) => sum + t.amount, 0)
    },
    consumeTotal() {
      return this.allTransactions
        .filter(t => t.type === 2)
        .reduce((sum, t) => sum + t.amount, 0)
    }
  },
  created() {
    this.loadData()
    EventBus.$on('refreshTransactions', () => {
      this.loadData()
    })
  },
  beforeDestroy() {
    EventBus.$off('refreshTransactions')
  },
  methods: {
    loadData() {
      this.loading = true
      setTimeout(() => {
        this.allTransactions = getTransactionsWithMemberInfo()
        this.filterData()
        this.loading = false
      }, 300)
    },
    filterData() {
      let filtered = [...this.allTransactions]

      if (this.searchForm.orderNo) {
        filtered = filtered.filter(t => t.orderNo.toLowerCase().includes(this.searchForm.orderNo.toLowerCase()))
      }
      if (this.searchForm.memberNo) {
        filtered = filtered.filter(t => t.memberNo.toLowerCase().includes(this.searchForm.memberNo.toLowerCase()))
      }
      if (this.searchForm.memberName) {
        filtered = filtered.filter(t => t.memberName.includes(this.searchForm.memberName))
      }
      if (this.searchForm.phone) {
        filtered = filtered.filter(t => t.phone && t.phone.includes(this.searchForm.phone))
      }
      if (this.searchForm.type !== null && this.searchForm.type !== undefined) {
        filtered = filtered.filter(t => t.type === this.searchForm.type)
      }
      if (this.searchForm.paymentMethod) {
        filtered = filtered.filter(t => t.paymentMethod === this.searchForm.paymentMethod)
      }
      if (this.searchForm.dateRange && this.searchForm.dateRange.length === 2) {
        filtered = filtered.filter(t => {
          return t.createTime >= this.searchForm.dateRange[0] && t.createTime <= this.searchForm.dateRange[1]
        })
      }

      this.pagination.total = filtered.length
      const start = (this.pagination.page - 1) * this.pagination.size
      const end = start + this.pagination.size
      this.tableData = filtered.slice(start, end)
    },
    handleSearch() {
      this.pagination.page = 1
      this.filterData()
    },
    handleReset() {
      this.searchForm = {
        orderNo: '',
        memberNo: '',
        memberName: '',
        phone: '',
        type: null,
        paymentMethod: '',
        dateRange: null
      }
      this.pagination.page = 1
      this.filterData()
    },
    handleSizeChange(val) {
      this.pagination.size = val
      this.pagination.page = 1
      this.filterData()
    },
    handleCurrentChange(val) {
      this.pagination.page = val
      this.filterData()
    }
  }
}
</script>

<style scoped lang="scss">
.stats-panel {
  display: flex;
  gap: 40px;

  .stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;

    .stat-label {
      color: #909399;
      font-size: 14px;
      margin-bottom: 8px;
    }

    .stat-value {
      font-size: 24px;
      font-weight: bold;
      color: #303133;

      &.income {
        color: #67c23a;
      }

      &.expense {
        color: #f56c6c;
      }
    }
  }
}

.search-form {
  .el-form-item {
    margin-bottom: 12px;
  }
}
</style>
