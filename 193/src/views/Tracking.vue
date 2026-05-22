<template>
  <div class="page-container">
    <el-card>
      <div slot="header" class="clearfix">
        <span>在途运单状态</span>
        <el-tag type="success" style="float: right">{{ trackingList.length }} 车在途</el-tag>
      </div>

      <el-row :gutter="20">
        <el-col :span="8" v-for="item in trackingList" :key="item.orderId">
          <el-card shadow="hover" class="tracking-card">
            <div slot="header" class="card-header">
              <span class="order-no">{{ item.orderNo }}</span>
              <el-tag type="success" size="small">运输中</el-tag>
            </div>
            
            <div class="map-container">
              <div class="map-placeholder">
                <i class="el-icon-location-outline"></i>
                <div class="location-text">当前位置: {{ item.currentLocation }}</div>
              </div>
              <el-progress :percentage="item.progress" :status="item.progress >= 100 ? 'success' : ''" class="progress-bar"></el-progress>
            </div>

            <div class="info-section">
              <el-row :gutter="10">
                <el-col :span="12">
                  <div class="info-item">
                    <span class="label">预计到达</span>
                    <span class="value">{{ item.estimatedArrival }}</span>
                  </div>
                </el-col>
                <el-col :span="12">
                  <div class="info-item">
                    <span class="label">运输进度</span>
                    <span class="value highlight">{{ item.progress }}%</span>
                  </div>
                </el-col>
              </el-row>
              <el-row :gutter="10" style="margin-top: 10px">
                <el-col :span="12">
                  <div class="info-item">
                    <span class="label">车内温度</span>
                    <span class="value">{{ item.temperature }}°C</span>
                  </div>
                </el-col>
                <el-col :span="12">
                  <div class="info-item">
                    <span class="label">车内湿度</span>
                    <span class="value">{{ item.humidity }}%</span>
                  </div>
                </el-col>
              </el-row>
            </div>

            <el-divider></el-divider>

            <div class="timeline-section">
              <div class="timeline-title">
                <i class="el-icon-time"></i> 运输轨迹
              </div>
              <el-timeline>
                <el-timeline-item
                  v-for="(node, index) in item.timeline"
                  :key="index"
                  :timestamp="node.time"
                  :type="index === 0 ? 'primary' : ''"
                  placement="top">
                  <el-card>
                    <h4>{{ node.status }}</h4>
                    <p>{{ node.location }}</p>
                    <p style="font-size: 12px; color: #909399">{{ node.description }}</p>
                  </el-card>
                </el-timeline-item>
              </el-timeline>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <el-empty v-if="trackingList.length === 0" description="暂无在途运单"></el-empty>
    </el-card>

    <el-card style="margin-top: 20px">
      <div slot="header" class="clearfix">
        <span>实时车辆位置</span>
      </div>
      <div class="big-map-container">
        <div class="map-content">
          <div class="map-grid">
            <div class="map-grid-header">
              <span>北京</span>
              <span>天津</span>
              <span>济南</span>
              <span>徐州</span>
              <span>南京</span>
              <span>上海</span>
            </div>
            <div class="map-grid-row" v-for="row in 5" :key="row">
              <div class="map-grid-cell" v-for="col in 6" :key="col">
                <div class="vehicle-marker" v-if="getVehicleAtPosition(row, col)" :title="getVehicleAtPosition(row, col)">
                  <i class="el-icon-location"></i>
                  <span>{{ getVehicleAtPosition(row, col) }}</span>
                </div>
              </div>
            </div>
          </div>
          <div class="map-legend">
            <el-tag type="primary" size="small">
              <i class="el-icon-location"></i> 在途车辆
            </el-tag>
            <el-tag type="success" size="small" style="margin-left: 10px">
              <i class="el-icon-check"></i> 已到达
            </el-tag>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { trackingApi, mockVehicles } from '../api/mockData'

export default {
  name: 'Tracking',
  data() {
    return {
      trackingList: [],
      vehicles: []
    }
  },
  mounted() {
    this.loadTrackingData()
    this.vehicles = mockVehicles.filter(v => v.status === '在途')
  },
  methods: {
    async loadTrackingData() {
      try {
        this.trackingList = await trackingApi.getList()
      } catch (error) {
        this.$message.error('加载追踪数据失败')
      }
    },
    getVehicleAtPosition(row, col) {
      const positions = {
        '1-2': this.vehicles[0]?.plateNumber,
        '2-3': this.vehicles[1]?.plateNumber,
        '3-1': this.vehicles[2]?.plateNumber
      }
      return positions[`${row}-${col}`] || null
    }
  }
}
</script>

<style scoped>
.tracking-card {
  margin-bottom: 20px;
  height: 100%;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.order-no {
  font-weight: bold;
  font-size: 16px;
  color: #303133;
}
.map-container {
  padding: 15px 0;
}
.map-placeholder {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  padding: 30px 20px;
  text-align: center;
  color: #fff;
  margin-bottom: 15px;
}
.map-placeholder i {
  font-size: 40px;
  margin-bottom: 10px;
  display: block;
}
.location-text {
  font-size: 14px;
  font-weight: 500;
}
.progress-bar {
  margin-top: 10px;
}
.info-section {
  padding: 10px 0;
}
.info-item {
  display: flex;
  flex-direction: column;
}
.info-item .label {
  font-size: 12px;
  color: #909399;
  margin-bottom: 5px;
}
.info-item .value {
  font-size: 15px;
  font-weight: 500;
  color: #303133;
}
.info-item .value.highlight {
  color: #409EFF;
}
.timeline-section {
  max-height: 300px;
  overflow-y: auto;
}
.timeline-title {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 15px;
}
.timeline-title i {
  margin-right: 5px;
  color: #409EFF;
}
.big-map-container {
  min-height: 400px;
  background: #f5f7fa;
  border-radius: 8px;
  padding: 20px;
}
.map-content {
  height: 100%;
}
.map-grid {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #ebeef5;
}
.map-grid-header {
  display: flex;
  justify-content: space-around;
  padding: 10px 0;
  border-bottom: 2px solid #ebeef5;
  margin-bottom: 10px;
  font-weight: 500;
  color: #606266;
}
.map-grid-row {
  display: flex;
}
.map-grid-cell {
  flex: 1;
  height: 60px;
  border-right: 1px dashed #ebeef5;
  border-bottom: 1px dashed #ebeef5;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}
.map-grid-cell:last-child {
  border-right: none;
}
.vehicle-marker {
  text-align: center;
  color: #409EFF;
  font-size: 12px;
}
.vehicle-marker i {
  font-size: 20px;
  display: block;
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.1);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}
.map-legend {
  margin-top: 20px;
  text-align: center;
}
</style>
