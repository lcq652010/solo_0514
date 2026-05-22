<template>
  <div class="violations-page">
    <el-card>
      <div slot="header">
        <span>⚠️ 违规记录</span>
      </div>

      <el-alert
        title="违规政策说明"
        type="warning"
        :closable="false"
        show-icon
        style="margin-bottom: 30px;"
      >
        <ul style="margin: 10px 0 0 20px; list-style: disc;">
          <li>累计3次违约，将暂停预约权限7天</li>
          <li>累计5次违约，将暂停预约权限30天</li>
          <li>累计10次违约，将永久取消预约权限</li>
          <li>若无法履约，请提前30分钟取消预约</li>
        </ul>
      </el-alert>

      <el-row :gutter="20" style="margin-bottom: 30px;">
        <el-col :span="6">
          <el-statistic title="累计违约次数" :value="totalViolations">
            <template slot="suffix">次</template>
          </el-statistic>
        </el-col>
        <el-col :span="6">
          <el-statistic title="本月违约次数" :value="monthViolations">
            <template slot="suffix">次</template>
          </el-statistic>
        </el-col>
        <el-col :span="6">
          <el-statistic title="当前状态" value-generator>
            <template slot="formatter">
              <el-tag :type="currentStatus.type" size="medium">{{ currentStatus.text }}</el-tag>
            </template>
          </el-statistic>
        </el-col>
        <el-col :span="6">
          <el-statistic title="恢复时间" :value="recoveryDays">
            <template slot="suffix">天后</template>
          </el-statistic>
        </el-col>
      </el-row>

      <h3 style="margin-bottom: 20px; color: #606266;">违约记录详情</h3>
      <el-table
        :data="violations"
        border
        style="width: 100%;"
        v-loading="loading"
      >
        <el-table-column prop="id" label="违约编号" width="140" align="center"></el-table-column>
        <el-table-column prop="seat" label="座位信息" width="140" align="center"></el-table-column>
        <el-table-column prop="date" label="预约日期" width="120" align="center"></el-table-column>
        <el-table-column prop="time" label="预约时段" width="150" align="center"></el-table-column>
        <el-table-column prop="reason" label="违约原因" align="center"></el-table-column>
        <el-table-column prop="recordTime" label="记录时间" width="180" align="center"></el-table-column>
        <el-table-column label="处理状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag type="info" size="small">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          background
          layout="total, prev, pager, next"
          :total="total"
          :page-size="pageSize"
          @current-change="handleCurrentChange"
        ></el-pagination>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'Violations',
  data() {
    return {
      loading: false,
      violations: [],
      totalViolations: 0,
      monthViolations: 0,
      total: 0,
      pageSize: 10,
      currentPage: 1
    };
  },
  computed: {
    currentStatus() {
      if (this.totalViolations >= 10) {
        return { type: 'danger', text: '永久封禁' };
      } else if (this.totalViolations >= 5) {
        return { type: 'danger', text: '暂停30天' };
      } else if (this.totalViolations >= 3) {
        return { type: 'warning', text: '暂停7天' };
      } else {
        return { type: 'success', text: '正常' };
      }
    },
    recoveryDays() {
      if (this.totalViolations >= 10) return '∞';
      if (this.totalViolations >= 5) return 30;
      if (this.totalViolations >= 3) return 7;
      return 0;
    }
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      this.loading = true;
      setTimeout(() => {
        this.violations = [
          {
            id: 'VIO2024001',
            seat: '一楼 A03',
            date: '2024-05-10',
            time: '09:00 - 12:00',
            reason: '未签到且未取消预约',
            recordTime: '2024-05-10 12:00:00',
            status: '已记录'
          },
          {
            id: 'VIO2024002',
            seat: '二楼 B05',
            date: '2024-05-08',
            time: '14:00 - 17:00',
            reason: '未签到且未取消预约',
            recordTime: '2024-05-08 17:00:00',
            status: '已记录'
          }
        ];
        this.total = this.violations.length;
        this.totalViolations = 2;
        this.monthViolations = 2;
        this.loading = false;
      }, 500);
    },
    handleCurrentChange(val) {
      this.currentPage = val;
    }
  }
};
</script>

<style scoped>
.violations-page {
  padding: 0;
}

.el-statistic {
  text-align: center;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}
</style>
