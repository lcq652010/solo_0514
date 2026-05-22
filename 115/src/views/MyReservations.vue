<template>
  <div class="my-reservations-page">
    <el-card>
      <div slot="header" class="clearfix">
        <span>📋 我的预约记录</span>
        <el-button style="float: right; padding: 3px 0;" type="text" @click="fetchData">
          <i class="el-icon-refresh"></i> 刷新
        </el-button>
      </div>

      <el-tabs v-model="activeTab" @tab-click="handleTabClick">
        <el-tab-pane label="全部预约" name="all"></el-tab-pane>
        <el-tab-pane label="待签到" name="pending"></el-tab-pane>
        <el-tab-pane label="已完成" name="completed"></el-tab-pane>
        <el-tab-pane label="已取消" name="cancelled"></el-tab-pane>
      </el-tabs>

      <el-table
        :data="filteredReservations"
        border
        style="width: 100%;"
        v-loading="loading"
      >
        <el-table-column prop="id" label="预约编号" width="120" align="center"></el-table-column>
        <el-table-column prop="seat" label="座位信息" width="150" align="center"></el-table-column>
        <el-table-column prop="date" label="预约日期" width="120" align="center"></el-table-column>
        <el-table-column prop="time" label="预约时段" width="150" align="center"></el-table-column>
        <el-table-column prop="purpose" label="用途" align="center"></el-table-column>
        <el-table-column label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" align="center">
          <template slot-scope="scope">
            <el-button
              v-if="scope.row.status === '待签到'"
              type="primary"
              size="small"
              @click="goCheckIn(scope.row)"
            >
              前往签到
            </el-button>
            <el-button
              v-if="scope.row.status === '待签到'"
              type="danger"
              size="small"
              @click="cancelReservation(scope.row)"
            >
              取消预约
            </el-button>
            <el-button
              v-if="scope.row.status === '已完成'"
              type="info"
              size="small"
              @click="viewDetail(scope.row)"
            >
              查看详情
            </el-button>
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
  name: 'MyReservations',
  data() {
    return {
      activeTab: 'all',
      loading: false,
      reservations: [],
      total: 0,
      pageSize: 10,
      currentPage: 1
    };
  },
  computed: {
    filteredReservations() {
      if (this.activeTab === 'all') {
        return this.reservations;
      }
      return this.reservations.filter(item => item.status === this.getStatusText(this.activeTab));
    }
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    getStatusText(tab) {
      const map = {
        pending: '待签到',
        completed: '已完成',
        cancelled: '已取消'
      };
      return map[tab] || tab;
    },
    getStatusType(status) {
      const map = {
        '待签到': 'warning',
        '已完成': 'success',
        '已取消': 'info',
        '已违约': 'danger'
      };
      return map[status] || 'info';
    },
    handleTabClick(tab, event) {
      this.currentPage = 1;
    },
    fetchData() {
      this.loading = true;
      setTimeout(() => {
        this.reservations = [
          {
            id: 'RES2024001',
            seat: '一楼 A05',
            date: '2024-05-16',
            time: '09:00 - 12:00',
            purpose: '自习',
            status: '待签到'
          },
          {
            id: 'RES2024002',
            seat: '二楼 B08',
            date: '2024-05-15',
            time: '14:00 - 17:00',
            purpose: '阅读',
            status: '已完成'
          },
          {
            id: 'RES2024003',
            seat: '三楼 C03',
            date: '2024-05-14',
            time: '08:00 - 11:00',
            purpose: '小组讨论',
            status: '已取消'
          },
          {
            id: 'RES2024004',
            seat: '一楼 A10',
            date: '2024-05-13',
            time: '10:00 - 13:00',
            purpose: '自习',
            status: '已完成'
          },
          {
            id: 'RES2024005',
            seat: '二楼 B12',
            date: '2024-05-17',
            time: '15:00 - 18:00',
            purpose: '自习',
            status: '待签到'
          }
        ];
        this.total = this.reservations.length;
        this.loading = false;
      }, 500);
    },
    goCheckIn(row) {
      this.$router.push({
        path: '/check-in',
        query: { id: row.id }
      });
    },
    cancelReservation(row) {
      this.$confirm('确认取消该预约吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.reservations.findIndex(item => item.id === row.id);
        if (index > -1) {
          this.reservations[index].status = '已取消';
        }
        this.$message({
          type: 'success',
          message: '预约已取消'
        });
      }).catch(() => {});
    },
    viewDetail(row) {
      this.$alert(`
        预约编号：${row.id}\n座位信息：${row.seat}\n预约日期：${row.date}\n预约时段：${row.time}\n用途：${row.purpose}
      `, '预约详情');
    },
    handleCurrentChange(val) {
      this.currentPage = val;
    }
  }
};
</script>

<style scoped>
.my-reservations-page {
  padding: 0;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}
</style>
