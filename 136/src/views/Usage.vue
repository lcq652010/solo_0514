<template>
  <div class="usage-page">
    <div class="page-header">
      <div class="page-title">水电用量查询</div>
      <div class="page-subtitle">当前宿舍：{{ dormitoryInfo.building }} {{ dormitoryInfo.room }}</div>
    </div>

    <el-row :gutter="20" class="mb-20">
      <el-col :span="6">
        <div class="stat-card blue" :class="{ 'balance-warning': dormitoryInfo.waterBalance <= reminderSettings.waterThreshold }">
          <div class="stat-value" :class="{ 'text-danger': dormitoryInfo.waterBalance <= reminderSettings.waterThreshold }">¥{{ dormitoryInfo.waterBalance }}</div>
          <div class="stat-label">水费余额</div>
          <div v-if="dormitoryInfo.waterBalance <= reminderSettings.waterThreshold" class="warning-tip">
            <i class="el-icon-warning"></i>余额不足
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card green" :class="{ 'balance-warning': dormitoryInfo.electricBalance <= reminderSettings.electricThreshold }">
          <div class="stat-value" :class="{ 'text-danger': dormitoryInfo.electricBalance <= reminderSettings.electricThreshold }">¥{{ dormitoryInfo.electricBalance }}</div>
          <div class="stat-label">电费余额</div>
          <div v-if="dormitoryInfo.electricBalance <= reminderSettings.electricThreshold" class="warning-tip">
            <i class="el-icon-warning"></i>余额不足
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-value">{{ usageData.water.monthly }} 吨</div>
          <div class="stat-label">本月用水量</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card orange">
          <div class="stat-value">{{ usageData.electric.monthly }} 度</div>
          <div class="stat-label">本月用电量</div>
        </div>
      </el-col>
    </el-row>

    <el-tabs v-model="activeTab" class="usage-tabs">
      <el-tab-pane label="用水明细" name="water">
        <div class="card-wrapper">
          <div class="card-header">
            <span class="card-title">近7日用水趋势</span>
            <div>
              <span>累计用水：{{ usageData.water.total }} 吨</span>
            </div>
          </div>
          <el-table :data="usageData.water.daily" border style="width: 100%">
            <el-table-column prop="date" label="日期" width="180" align="center" />
            <el-table-column prop="usage" label="用水量（吨）" align="center">
              <template slot-scope="scope">
                <span :class="scope.row.usage > 1.2 ? 'text-warning' : ''">{{ scope.row.usage }}</span>
              </template>
            </el-table-column>
            <el-table-column label="状态" align="center">
              <template slot-scope="scope">
                <el-tag :type="scope.row.usage > 1.2 ? 'warning' : 'success'" size="small">
                  {{ scope.row.usage > 1.2 ? '偏高' : '正常' }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-tab-pane>

      <el-tab-pane label="用电明细" name="electric">
        <div class="card-wrapper">
          <div class="card-header">
            <span class="card-title">近7日用电趋势</span>
            <div>
              <span>累计用电：{{ usageData.electric.total }} 度</span>
            </div>
          </div>
          <el-table :data="usageData.electric.daily" border style="width: 100%">
            <el-table-column prop="date" label="日期" width="180" align="center" />
            <el-table-column prop="usage" label="用电量（度）" align="center">
              <template slot-scope="scope">
                <span :class="scope.row.usage > 6.5 ? 'text-warning' : ''">{{ scope.row.usage }}</span>
              </template>
            </el-table-column>
            <el-table-column label="状态" align="center">
              <template slot-scope="scope">
                <el-tag :type="scope.row.usage > 6.5 ? 'warning' : 'success'" size="small">
                  {{ scope.row.usage > 6.5 ? '偏高' : '正常' }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-tab-pane>
    </el-tabs>

    <div class="card-wrapper">
      <div class="card-header">
        <span class="card-title">用量统计</span>
      </div>
      <el-row :gutter="20">
        <el-col :span="12">
          <div style="padding: 20px; background: #f5f7fa; border-radius: 4px;">
            <h4 style="margin-bottom: 15px; color: #303133;">用水统计</h4>
            <el-descriptions :column="2" border>
              <el-descriptions-item label="日平均用量">{{ (usageData.water.total / 30).toFixed(2) }} 吨</el-descriptions-item>
              <el-descriptions-item label="月用量">{{ usageData.water.monthly }} 吨</el-descriptions-item>
              <el-descriptions-item label="累计用量">{{ usageData.water.total }} 吨</el-descriptions-item>
              <el-descriptions-item label="人均用量">{{ (usageData.water.monthly / 4).toFixed(2) }} 吨</el-descriptions-item>
            </el-descriptions>
          </div>
        </el-col>
        <el-col :span="12">
          <div style="padding: 20px; background: #f5f7fa; border-radius: 4px;">
            <h4 style="margin-bottom: 15px; color: #303133;">用电统计</h4>
            <el-descriptions :column="2" border>
              <el-descriptions-item label="日平均用量">{{ (usageData.electric.total / 30).toFixed(2) }} 度</el-descriptions-item>
              <el-descriptions-item label="月用量">{{ usageData.electric.monthly }} 度</el-descriptions-item>
              <el-descriptions-item label="累计用量">{{ usageData.electric.total }} 度</el-descriptions-item>
              <el-descriptions-item label="人均用量">{{ (usageData.electric.monthly / 4).toFixed(2) }} 度</el-descriptions-item>
            </el-descriptions>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import { dormitoryInfo, usageData, reminderSettings } from '@/data/mock.js'

export default {
  name: 'Usage',
  data() {
    return {
      activeTab: 'water',
      dormitoryInfo,
      usageData,
      reminderSettings
    }
  }
}
</script>

<style scoped>
.usage-page {
  width: 100%;
}

.text-warning {
  color: #E6A23C;
  font-weight: 600;
}

.text-danger {
  color: #F56C6C !important;
  font-weight: 700 !important;
}

.balance-warning {
  animation: pulse 2s infinite;
  border: 2px solid #F56C6C !important;
}

.warning-tip {
  font-size: 12px;
  color: #F56C6C;
  background: rgba(245, 108, 108, 0.15);
  padding: 4px 8px;
  border-radius: 4px;
  margin-top: 5px;
  display: inline-block;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(245, 108, 108, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(245, 108, 108, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(245, 108, 108, 0);
  }
}

.usage-tabs {
  margin-bottom: 20px;
}

.usage-tabs ::v-deep .el-tabs__content {
  padding-top: 20px;
}
</style>
