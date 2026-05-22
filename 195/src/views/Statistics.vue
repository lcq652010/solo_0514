<template>
  <div class="statistics">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="stat-card total-card">
          <div class="stat-content">
            <div class="stat-icon">
              <i class="el-icon-s-platform"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ totalDevices }}</div>
              <div class="stat-label">设备总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card running-card">
          <div class="stat-content">
            <div class="stat-icon">
              <i class="el-icon-circle-check"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ runningCount }}</div>
              <div class="stat-label">运行中</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card fault-card">
          <div class="stat-content">
            <div class="stat-icon">
              <i class="el-icon-circle-close"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ faultCount }}</div>
              <div class="stat-label">故障</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card offline-card">
          <div class="stat-content">
            <div class="stat-icon">
              <i class="el-icon-time"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ offlineCount }}</div>
              <div class="stat-label">离线</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card class="chart-card">
          <div class="card-header">
            <span class="card-title">设备状态分布</span>
          </div>
          <div class="chart-placeholder">
            <div class="placeholder-content">
              <i class="el-icon-pie-chart"></i>
              <p>饼图占位 - 设备状态分布图表</p>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="chart-card">
          <div class="card-header">
            <span class="card-title">工单趋势</span>
          </div>
          <div class="chart-placeholder">
            <div class="placeholder-content">
              <i class="el-icon-data-line"></i>
              <p>折线图占位 - 近7天工单趋势图表</p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row style="margin-top: 20px">
      <el-col :span="24">
        <el-card class="table-card">
          <div class="card-header">
            <span class="card-title">社区设备统计</span>
          </div>
          <el-table :data="communityStats" border stripe style="width: 100%">
            <el-table-column prop="community" label="社区名称" min-width="180" align="center"></el-table-column>
            <el-table-column prop="total" label="设备总数" width="120" align="center"></el-table-column>
            <el-table-column prop="running" label="运行中" width="100" align="center">
              <template slot-scope="scope">
                <span class="status-running">{{ scope.row.running }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="fault" label="故障" width="100" align="center">
              <template slot-scope="scope">
                <span class="status-fault">{{ scope.row.fault }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="offline" label="离线" width="100" align="center">
              <template slot-scope="scope">
                <span class="status-offline">{{ scope.row.offline }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="maintenance" label="维护中" width="100" align="center">
              <template slot-scope="scope">
                <span class="status-maintenance">{{ scope.row.maintenance }}</span>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { mockDevices, type Device } from '@/mock/data'

interface CommunityStat {
  community: string
  total: number
  running: number
  fault: number
  offline: number
  maintenance: number
}

export default Vue.extend({
  name: 'Statistics',
  data() {
    return {
      devices: [] as Device[]
    }
  },
  computed: {
    totalDevices(): number {
      return this.devices.length
    },
    runningCount(): number {
      return this.devices.filter(d => d.status === 'running').length
    },
    faultCount(): number {
      return this.devices.filter(d => d.status === 'fault').length
    },
    offlineCount(): number {
      return this.devices.filter(d => d.status === 'offline').length
    },
    communityStats(): CommunityStat[] {
      const statMap: Record<string, CommunityStat> = {}
      this.devices.forEach(device => {
        if (!statMap[device.community]) {
          statMap[device.community] = {
            community: device.community,
            total: 0,
            running: 0,
            fault: 0,
            offline: 0,
            maintenance: 0
          }
        }
        statMap[device.community].total++
        if (device.status in statMap[device.community]) {
          ;(statMap[device.community] as any)[device.status]++
        }
      })
      return Object.values(statMap).sort((a, b) => b.total - a.total)
    }
  },
  mounted() {
    this.devices = mockDevices
  }
})
</script>

<style scoped>
.statistics {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.stat-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  overflow: hidden;
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  color: #fff;
}

.total-card .stat-icon {
  background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%);
}

.running-card .stat-icon {
  background: linear-gradient(135deg, #52c41a 0%, #389e0d 100%);
}

.fault-card .stat-icon {
  background: linear-gradient(135deg, #ff4d4f 0%, #cf1322 100%);
}

.offline-card .stat-icon {
  background: linear-gradient(135deg, #8c8c8c 0%, #595959 100%);
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #303133;
  line-height: 1.2;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

.chart-card,
.table-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.card-header {
  margin-bottom: 20px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.chart-placeholder {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fafafa;
  border-radius: 8px;
  border: 1px dashed #d9d9d9;
}

.placeholder-content {
  text-align: center;
  color: #909399;
}

.placeholder-content i {
  font-size: 48px;
  display: block;
  margin-bottom: 10px;
}

.placeholder-content p {
  margin: 0;
  font-size: 14px;
}

.status-running {
  color: #52c41a;
  font-weight: 600;
}

.status-fault {
  color: #ff4d4f;
  font-weight: 600;
}

.status-offline {
  color: #8c8c8c;
  font-weight: 600;
}

.status-maintenance {
  color: #fa8c16;
  font-weight: 600;
}

::v-deep .el-table .cell {
  text-align: center;
}
</style>
