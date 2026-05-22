<template>
  <div class="ledger">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>个人加班台账</span>
      </div>
      <el-form :inline="true" :model="searchForm" class="demo-form-inline">
        <el-form-item label="年份">
          <el-select v-model="searchForm.year" placeholder="请选择">
            <el-option
              v-for="year in yearOptions"
              :key="year"
              :label="year"
              :value="year"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="月份">
          <el-select v-model="searchForm.month" placeholder="请选择" clearable>
            <el-option
              v-for="month in monthOptions"
              :key="month.value"
              :label="month.label"
              :value="month.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">查询</el-button>
          <el-button @click="exportData">导出</el-button>
        </el-form-item>
      </el-form>

      <el-row :gutter="20" style="margin-bottom: 20px">
        <el-col :span="6">
          <div class="summary-card">
            <div class="summary-label">总加班次数</div>
            <div class="summary-value">{{ summary.totalCount }}</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="summary-card">
            <div class="summary-label">总加班时长</div>
            <div class="summary-value">{{ summary.totalHours }} 小时</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="summary-card">
            <div class="summary-label">已通过</div>
            <div class="summary-value approved">{{ summary.approvedCount }}</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="summary-card">
            <div class="summary-label">待审批</div>
            <div class="summary-value pending">{{ summary.pendingCount }}</div>
          </div>
        </el-col>
      </el-row>

      <el-table :data="tableData" border style="width: 100%" v-loading="loading">
        <el-table-column prop="date" label="日期" width="120"></el-table-column>
        <el-table-column prop="type" label="加班类型" width="120">
          <template slot-scope="scope">
            <span>{{ getTypeLabel(scope.row.type) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="duration" label="时长(小时)" width="100"></el-table-column>
        <el-table-column prop="reason" label="加班原因"></el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)">{{ getStatusLabel(scope.row.status) }}</el-tag>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="pagination.page"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pagination.pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="pagination.total"
        style="margin-top: 20px; text-align: right"
      ></el-pagination>
    </el-card>
  </div>
</template>

<script>
import { getLedger } from '@/api/overtime';

export default {
  name: 'Ledger',
  data() {
    return {
      searchForm: {
        year: new Date().getFullYear().toString(),
        month: ''
      },
      tableData: [],
      loading: false,
      pagination: {
        page: 1,
        pageSize: 10,
        total: 0
      },
      summary: {
        totalCount: 0,
        totalHours: 0,
        approvedCount: 0,
        pendingCount: 0
      },
      yearOptions: [],
      monthOptions: [
        { label: '1月', value: '1' },
        { label: '2月', value: '2' },
        { label: '3月', value: '3' },
        { label: '4月', value: '4' },
        { label: '5月', value: '5' },
        { label: '6月', value: '6' },
        { label: '7月', value: '7' },
        { label: '8月', value: '8' },
        { label: '9月', value: '9' },
        { label: '10月', value: '10' },
        { label: '11月', value: '11' },
        { label: '12月', value: '12' }
      ]
    };
  },
  created() {
    this.initYearOptions();
    this.fetchData();
  },
  methods: {
    initYearOptions() {
      const currentYear = new Date().getFullYear();
      for (let i = currentYear - 2; i <= currentYear; i++) {
        this.yearOptions.push(i.toString());
      }
    },
    async fetchData() {
      this.loading = true;
      try {
        const params = {
          page: this.pagination.page,
          pageSize: this.pagination.pageSize,
          ...this.searchForm
        };
        const res = await getLedger(params);
        if (res.data.code === 200) {
          this.tableData = res.data.data.list;
          this.pagination.total = res.data.data.total;
          this.calculateSummary(res.data.data.list);
        }
      } catch (error) {
        this.$message.error('获取数据失败');
      } finally {
        this.loading = false;
      }
    },
    calculateSummary(data) {
      this.summary.totalCount = data.length;
      this.summary.totalHours = data.reduce((sum, item) => sum + item.duration, 0).toFixed(1);
      this.summary.approvedCount = data.filter(item => item.status === 'approved').length;
      this.summary.pendingCount = data.filter(item => item.status === 'pending').length;
    },
    exportData() {
      this.$message.info('导出功能开发中...');
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val;
      this.pagination.page = 1;
      this.fetchData();
    },
    handleCurrentChange(val) {
      this.pagination.page = val;
      this.fetchData();
    },
    getTypeLabel(type) {
      const map = {
        weekday: '工作日加班',
        weekend: '周末加班',
        holiday: '节假日加班'
      };
      return map[type] || type;
    },
    getStatusLabel(status) {
      const map = {
        pending: '待审批',
        approved: '已通过',
        rejected: '已驳回'
      };
      return map[status] || status;
    },
    getStatusType(status) {
      const map = {
        pending: 'warning',
        approved: 'success',
        rejected: 'danger'
      };
      return map[status] || 'info';
    }
  }
};
</script>

<style scoped>
.ledger {
  padding: 20px;
}

.box-card {
  width: 100%;
}

.summary-card {
  background: #f5f7fa;
  padding: 20px;
  border-radius: 4px;
  text-align: center;
}

.summary-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 10px;
}

.summary-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.summary-value.approved {
  color: #67C23A;
}

.summary-value.pending {
  color: #E6A23C;
}
</style>
