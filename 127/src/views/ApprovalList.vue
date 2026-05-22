<template>
  <div class="approval-list">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>部门审批列表</span>
      </div>
      <el-form :inline="true" :model="searchForm" class="demo-form-inline">
        <el-form-item label="部门">
          <el-select v-model="searchForm.department" placeholder="请选择" clearable>
            <el-option label="技术部" value="技术部"></el-option>
            <el-option label="产品部" value="产品部"></el-option>
            <el-option label="运营部" value="运营部"></el-option>
            <el-option label="市场部" value="市场部"></el-option>
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
        <el-table-column prop="applicant" label="申请人" width="100"></el-table-column>
        <el-table-column prop="department" label="部门" width="100"></el-table-column>
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
        <el-table-column label="操作" width="180" fixed="right">
          <template slot-scope="scope">
            <el-button
              v-if="scope.row.status === 'pending'"
              type="success"
              size="small"
              @click="handleApprove(scope.row)"
            >通过</el-button>
            <el-button
              v-if="scope.row.status === 'pending'"
              type="danger"
              size="small"
              @click="handleReject(scope.row)"
            >驳回</el-button>
            <el-button size="small" @click="handleView(scope.row)">查看</el-button>
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

    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="500px">
      <el-form :model="approvalForm" label-width="100px">
        <el-form-item label="申请人">{{ currentRecord.applicant }}</el-form-item>
        <el-form-item label="加班类型">{{ getTypeLabel(currentRecord.type) }}</el-form-item>
        <el-form-item label="加班时间">
          {{ currentRecord.startTime }} ~ {{ currentRecord.endTime }}
        </el-form-item>
        <el-form-item label="加班原因">{{ currentRecord.reason }}</el-form-item>
        <el-form-item v-if="!isView" label="审批意见">
          <el-input
            type="textarea"
            v-model="approvalForm.approvalRemark"
            placeholder="请输入审批意见"
            rows="3"
          ></el-input>
        </el-form-item>
        <el-form-item v-if="isView && currentRecord.approvalRemark" label="审批意见">
          {{ currentRecord.approvalRemark }}
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button v-if="!isView" type="primary" :disabled="!canSubmitApproval" @click="confirmApproval">确认</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getApprovalList, approveOvertime } from '@/api/overtime';

export default {
  name: 'ApprovalList',
  data() {
    return {
      searchForm: {
        department: '',
        dateRange: [],
        status: ''
      },
      tableData: [],
      loading: false,
      pagination: {
        page: 1,
        pageSize: 10,
        total: 0
      },
      dialogVisible: false,
      dialogTitle: '',
      isView: false,
      currentRecord: {},
      approvalForm: {
        status: '',
        approvalRemark: ''
      }
    };
  },
  computed: {
    canSubmitApproval() {
      const remark = this.approvalForm.approvalRemark;
      return remark && remark.trim().length >= 2;
    }
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
          department: this.searchForm.department,
          status: this.searchForm.status
        };
        if (this.searchForm.dateRange && this.searchForm.dateRange.length === 2) {
          params.startDate = this.searchForm.dateRange[0];
          params.endDate = this.searchForm.dateRange[1];
        }
        const res = await getApprovalList(params);
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
      this.searchForm.department = '';
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
    handleApprove(row) {
      this.isView = false;
      this.dialogTitle = '审批通过';
      this.currentRecord = row;
      this.approvalForm = {
        status: 'approved',
        approvalRemark: ''
      };
      this.dialogVisible = true;
    },
    handleReject(row) {
      this.isView = false;
      this.dialogTitle = '审批驳回';
      this.currentRecord = row;
      this.approvalForm = {
        status: 'rejected',
        approvalRemark: ''
      };
      this.dialogVisible = true;
    },
    handleView(row) {
      this.isView = true;
      this.dialogTitle = '查看详情';
      this.currentRecord = row;
      this.dialogVisible = true;
    },
    async confirmApproval() {
      if (!this.approvalForm.approvalRemark || this.approvalForm.approvalRemark.trim() === '') {
        this.$message.error('请填写审批意见');
        return;
      }
      if (this.approvalForm.approvalRemark.trim().length < 2) {
        this.$message.error('审批意见不能少于2个字');
        return;
      }
      try {
        const res = await approveOvertime({
          id: this.currentRecord.id,
          status: this.approvalForm.status,
          approvalRemark: this.approvalForm.approvalRemark
        });
        if (res.data.code === 200) {
          this.$message.success('审批成功');
          this.dialogVisible = false;
          this.fetchData();
        }
      } catch (error) {
        this.$message.error('审批失败');
      }
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
.approval-list {
  padding: 20px;
}

.box-card {
  width: 100%;
}
</style>
