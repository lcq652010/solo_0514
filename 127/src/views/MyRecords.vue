<template>
  <div class="my-records">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>我的加班记录</span>
      </div>
      <el-form :inline="true" :model="searchForm" class="demo-form-inline">
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="searchForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="yyyy-MM-dd"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择" clearable>
            <el-option label="待审批" value="pending"></el-option>
            <el-option label="已通过" value="approved"></el-option>
            <el-option label="已驳回" value="rejected"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">查询</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
      <el-table :data="tableData" border style="width: 100%" v-loading="loading">
        <el-table-column prop="type" label="加班类型" width="120">
          <template slot-scope="scope">
            <span>{{ getTypeLabel(scope.row.type) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="startTime" label="开始时间" width="160"></el-table-column>
        <el-table-column prop="endTime" label="结束时间" width="160"></el-table-column>
        <el-table-column prop="duration" label="时长(小时)" width="100"></el-table-column>
        <el-table-column prop="reason" label="加班原因"></el-table-column>
        <el-table-column prop="createTime" label="申请时间" width="160"></el-table-column>
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
import { getMyOvertimeRecords } from '@/api/overtime';

export default {
  name: 'MyRecords',
  data() {
    return {
      searchForm: {
        dateRange: [],
        status: ''
      },
      tableData: [],
      loading: false,
      pagination: {
        page: 1,
        pageSize: 10,
        total: 0
      }
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      this.loading = true;
      try {
        const params = {
          page: this.pagination.page,
          pageSize: this.pagination.pageSize,
          status: this.searchForm.status
        };
        if (this.searchForm.dateRange && this.searchForm.dateRange.length === 2) {
          params.startDate = this.searchForm.dateRange[0];
          params.endDate = this.searchForm.dateRange[1];
        }
        const res = await getMyOvertimeRecords(params);
        if (res.data.code === 200) {
          this.tableData = res.data.data.list;
          this.pagination.total = res.data.data.total;
        }
      } catch (error) {
        this.$message.error('获取数据失败');
      } finally {
        this.loading = false;
      }
    },
    resetSearch() {
      this.searchForm.dateRange = [];
      this.searchForm.status = '';
      this.pagination.page = 1;
      this.fetchData();
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
.my-records {
  padding: 20px;
}

.box-card {
  width: 100%;
}
</style>
