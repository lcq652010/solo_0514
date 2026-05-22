<template>
  <div class="check-in-page">
    <el-card>
      <div slot="header">
        <span>✅ 签到确认</span>
      </div>

      <el-alert
        title="签到说明"
        type="info"
        :closable="false"
        show-icon
        style="margin-bottom: 30px;"
      >
        <p>请在预约开始时间前30分钟内进行签到</p>
        <p>签到时请确保您在图书馆内，系统会自动验证您的位置</p>
        <p>未按时签到将记为违约一次</p>
      </el-alert>

      <div v-if="pendingReservations.length > 0" class="check-in-content">
        <h3 style="margin-bottom: 20px; color: #606266;">待签到的预约</h3>
        
        <el-table :data="pendingReservations" border style="width: 100%;">
          <el-table-column prop="id" label="预约编号" width="140" align="center"></el-table-column>
          <el-table-column prop="seat" label="座位信息" width="140" align="center"></el-table-column>
          <el-table-column prop="date" label="预约日期" width="120" align="center"></el-table-column>
          <el-table-column prop="time" label="预约时段" width="160" align="center"></el-table-column>
          <el-table-column label="剩余时间" align="center">
            <template slot-scope="scope">
              <span :class="getTimeClass(scope.row)">{{ getCountdownText(scope.row) }}</span>
            </template>
          </el-table-column>
          <el-table-column label="签到操作" width="150" align="center">
            <template slot-scope="scope">
              <el-button
                type="primary"
                size="small"
                :disabled="!canCheckIn(scope.row)"
                @click="handleCheckIn(scope.row)"
              >
                {{ canCheckIn(scope.row) ? '立即签到' : '未到签到时间' }}
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div v-else class="empty-state">
        <el-empty description="暂无待签到的预约记录">
          <el-button type="primary" @click="$router.push('/reservation')">去预约座位</el-button>
        </el-empty>
      </div>

      <div v-if="showSuccess" class="success-card">
        <el-result
          icon="success"
          title="签到成功"
          sub-title="您已成功签到，请按预约时段使用座位"
        >
          <template slot="extra">
            <el-button type="primary" @click="showSuccess = false">确定</el-button>
          </template>
        </el-result>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'CheckIn',
  data() {
    return {
      pendingReservations: [],
      showSuccess: false,
      currentTime: new Date()
    };
  },
  mounted() {
    this.fetchPendingReservations();
    this.timer = setInterval(() => {
      this.currentTime = new Date();
    }, 1000);
  },
  beforeDestroy() {
    if (this.timer) {
      clearInterval(this.timer);
    }
  },
  methods: {
    fetchPendingReservations() {
      this.pendingReservations = [
        {
          id: 'RES2024001',
          seat: '一楼 A05',
          date: this.formatDate(new Date()),
          time: '09:00 - 12:00',
          startTime: '09:00',
          purpose: '自习'
        },
        {
          id: 'RES2024005',
          seat: '二楼 B12',
          date: this.formatDate(new Date(Date.now() + 86400000)),
          time: '15:00 - 18:00',
          startTime: '15:00',
          purpose: '自习'
        }
      ];
    },
    formatDate(date) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    },
    canCheckIn(row) {
      const now = this.currentTime;
      const todayStr = this.formatDate(now);
      if (row.date !== todayStr) return false;
      
      const [hours, minutes] = row.startTime.split(':').map(Number);
      const startTime = new Date(now);
      startTime.setHours(hours, minutes, 0, 0);
      
      const diffMinutes = (startTime - now) / 1000 / 60;
      return diffMinutes <= 30 && diffMinutes >= -60;
    },
    getCountdownText(row) {
      const now = this.currentTime;
      const todayStr = this.formatDate(now);
      
      if (row.date !== todayStr) {
        return row.date;
      }
      
      const [hours, minutes] = row.startTime.split(':').map(Number);
      const startTime = new Date(now);
      startTime.setHours(hours, minutes, 0, 0);
      
      const diffMs = startTime - now;
      const diffMins = Math.floor(diffMs / 1000 / 60);
      
      if (diffMins > 0) {
        const h = Math.floor(diffMins / 60);
        const m = diffMins % 60;
        return h > 0 ? `${h}小时${m}分钟后开始` : `${m}分钟后开始`;
      } else if (diffMins > -60) {
        return '签到进行中';
      } else {
        return '已过签到时间';
      }
    },
    getTimeClass(row) {
      const now = this.currentTime;
      const todayStr = this.formatDate(now);
      if (row.date !== todayStr) return '';
      
      const [hours, minutes] = row.startTime.split(':').map(Number);
      const startTime = new Date(now);
      startTime.setHours(hours, minutes, 0, 0);
      
      const diffMins = (startTime - now) / 1000 / 60;
      
      if (diffMins <= 30 && diffMins > 0) {
        return 'text-warning';
      } else if (diffMins <= 0 && diffMins > -60) {
        return 'text-success';
      } else if (diffMins <= -60) {
        return 'text-danger';
      }
      return '';
    },
    handleCheckIn(row) {
      this.$confirm('确认签到吗？签到后请准时使用该座位。', '签到确认', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.pendingReservations.findIndex(item => item.id === row.id);
        if (index > -1) {
          this.pendingReservations.splice(index, 1);
        }
        this.showSuccess = true;
        this.$message.success('签到成功！');
      }).catch(() => {});
    }
  }
};
</script>

<style scoped>
.check-in-page {
  padding: 0;
}

.check-in-content {
  margin-bottom: 30px;
}

.text-warning {
  color: #e6a23c;
  font-weight: bold;
}

.text-success {
  color: #67c23a;
  font-weight: bold;
}

.text-danger {
  color: #f56c6c;
  font-weight: bold;
}

.empty-state {
  padding: 40px 0;
}

.success-card {
  margin-top: 30px;
}
</style>
