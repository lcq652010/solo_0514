<template>
  <div class="page-card">
    <div class="page-title">派件跟踪</div>
    
    <el-form :inline="true" :model="searchForm" class="search-form">
      <el-form-item label="订单号">
        <el-input v-model="searchForm.orderNo" placeholder="请输入订单号" clearable style="width: 300px"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="search">查询</el-button>
      </el-form-item>
    </el-form>

    <div v-if="packageInfo" class="tracking-container">
      <el-card shadow="never" class="package-info">
        <div slot="header">
          <span>包裹信息</span>
          <el-tag :type="statusMap[packageInfo.status].type" size="small">
            {{ statusMap[packageInfo.status].label }}
          </el-tag>
        </div>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="订单号">{{ packageInfo.orderNo }}</el-descriptions-item>
          <el-descriptions-item label="包裹名称">{{ packageInfo.packageName }}</el-descriptions-item>
          <el-descriptions-item label="寄件人">{{ packageInfo.senderName }}</el-descriptions-item>
          <el-descriptions-item label="收件人">{{ packageInfo.receiverName }}</el-descriptions-item>
          <el-descriptions-item label="寄件地址" :span="2">{{ packageInfo.senderAddress }}</el-descriptions-item>
          <el-descriptions-item label="收件地址" :span="2">{{ packageInfo.receiverAddress }}</el-descriptions-item>
        </el-descriptions>
      </el-card>

      <el-card shadow="never" class="timeline-card" style="margin-top: 20px">
        <div slot="header">
          <span>物流轨迹</span>
          <span style="float: right; color: #909399; font-size: 12px;">共 {{ trackingData.length }} 条物流信息</span>
        </div>
        <el-timeline>
          <el-timeline-item
            v-for="(track, index) in trackingData"
            :key="index"
            :timestamp="track.time"
            placement="top"
            :type="getTimelineType(track.status, index)"
            :color="getTimelineColor(track.status, index)"
            :icon="getTimelineIcon(track.status)"
          >
            <el-card :shadow="index === 0 ? 'hover' : 'never'" :class="['track-card', { 'track-card-latest': index === 0 }]">
              <div class="track-header">
                <h4 :class="['track-status', getStatusClass(track.status)]">{{ track.status }}</h4>
                <el-tag v-if="index === 0" type="success" size="mini">最新</el-tag>
              </div>
              <div class="track-content">
                <p class="track-location">
                  <i class="el-icon-location-outline"></i>
                  <span>{{ track.location }}</span>
                </p>
                <p class="track-operator">
                  <i class="el-icon-user-outline"></i>
                  <span>{{ track.operator }}</span>
                </p>
                <p v-if="track.remark" class="track-remark">
                  <i class="el-icon-info-outline"></i>
                  <span>{{ track.remark }}</span>
                </p>
              </div>
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </el-card>
    </div>

    <el-empty v-else description="请输入订单号查询物流信息" :image-size="100"></el-empty>
  </div>
</template>

<script>
import { mockPackages, mockTracking, statusMap } from '@/mock/data.js';
import { EventBus } from '@/utils/eventBus.js';

export default {
  name: 'TrackingPage',
  data() {
    return {
      searchForm: {
        orderNo: ''
      },
      packageInfo: null,
      trackingData: [],
      statusMap: statusMap
    };
  },
  created() {
    EventBus.$on('packageStatusUpdated', (data) => {
      if (this.packageInfo && this.packageInfo.orderNo === data.orderNo) {
        this.search();
      }
    });
  },
  mounted() {
    if (this.$route.query.orderNo) {
      this.searchForm.orderNo = this.$route.query.orderNo;
      this.search();
    }
  },
  beforeDestroy() {
    EventBus.$off('packageStatusUpdated');
  },
  methods: {
    getTimelineType(status, index) {
      if (index === 0) return 'primary';
      if (status.includes('签收')) return 'success';
      if (status.includes('揽收')) return 'warning';
      return '';
    },
    getTimelineColor(status, index) {
      if (index === 0) return '#409EFF';
      if (status.includes('签收')) return '#67C23A';
      if (status.includes('揽收')) return '#E6A23C';
      if (status.includes('派送')) return '#409EFF';
      if (status.includes('运输')) return '#909399';
      return '#C0C4CC';
    },
    getTimelineIcon(status) {
      if (status.includes('签收')) return 'el-icon-check';
      if (status.includes('揽收')) return 'el-icon-box';
      if (status.includes('派送')) return 'el-icon-location';
      if (status.includes('运输')) return 'el-icon-truck';
      if (status.includes('到达')) return 'el-icon-place';
      return 'el-icon-circle-check';
    },
    getStatusClass(status) {
      if (status.includes('签收')) return 'status-signed';
      if (status.includes('揽收')) return 'status-pickup';
      if (status.includes('派送')) return 'status-delivering';
      if (status.includes('运输')) return 'status-transit';
      if (status.includes('到达')) return 'status-arrived';
      return '';
    },
    search() {
      if (!this.searchForm.orderNo) {
        this.$message.warning('请输入订单号');
        return;
      }

      const pkg = mockPackages.find(p => p.orderNo === this.searchForm.orderNo);
      if (!pkg) {
        this.$message.error('未找到该订单信息');
        this.packageInfo = null;
        this.trackingData = [];
        return;
      }

      this.packageInfo = pkg;
      
      const tracking = mockTracking.find(t => t.orderNo === pkg.orderNo);
      if (tracking) {
        this.trackingData = tracking.tracks;
      } else {
        this.trackingData = [
          {
            time: pkg.createTime,
            status: '已下单',
            location: pkg.senderAddress,
            operator: '系统',
            remark: '订单已创建成功，等待快递员揽收'
          }
        ];
      }
    }
  }
};
</script>

<style scoped>
.search-form {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.package-info {
  border: 1px solid #ebeef5;
}

.timeline-card {
  border: 1px solid #ebeef5;
}

.track-card {
  max-width: 550px;
  margin-bottom: 15px;
  border: 1px solid #ebeef5;
  transition: all 0.3s;
}

.track-card-latest {
  border-color: #409EFF;
  background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%);
}

.track-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.track-status {
  margin: 0;
  font-size: 15px;
  font-weight: 600;
}

.status-signed {
  color: #67C23A;
}

.status-pickup {
  color: #E6A23C;
}

.status-delivering {
  color: #409EFF;
}

.status-transit {
  color: #909399;
}

.status-arrived {
  color: #67C23A;
}

.track-content {
  margin-top: 8px;
}

.track-location,
.track-operator,
.track-remark {
  margin: 6px 0;
  font-size: 13px;
  color: #606266;
  display: flex;
  align-items: flex-start;
}

.track-location i,
.track-operator i,
.track-remark i {
  margin-right: 8px;
  color: #909399;
  margin-top: 2px;
}

.track-remark {
  color: #909399;
  font-size: 12px;
  padding-top: 5px;
  border-top: 1px dashed #ebeef5;
  margin-top: 8px;
}

.el-timeline-item__timestamp {
  color: #909399;
  font-size: 12px;
  font-weight: 500;
}

.el-timeline-item__icon {
  font-size: 16px !important;
}
</style>
