<template>
  <div class="page-container">
    <div class="page-header">
      <div class="page-title">用量统计</div>
      <div class="page-subtitle">查看宿舍水电用量的历史数据和趋势分析</div>
    </div>

    <el-card class="mb-20">
      <el-form :inline="true">
        <el-form-item label="选择宿舍">
          <el-select v-model="selectedDormitory" placeholder="请选择宿舍" style="width: 200px;" @change="loadData">
            <el-option
              v-for="dorm in dormitoryList"
              :key="dorm"
              :label="dorm"
              :value="dorm"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="统计类型">
          <el-radio-group v-model="statsType" @change="loadData">
            <el-radio label="all">全部</el-radio>
            <el-radio label="water">水费</el-radio>
            <el-radio label="electricity">电费</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
    </el-card>

    <el-row :gutter="20" class="mb-20">
      <el-col :span="6">
        <div class="stat-card">
          <div class="label">今日用水量</div>
          <div class="value">
            {{ todayWater }} <span class="unit">吨</span>
          </div>
          <div class="trend" :class="waterTrend > 0 ? 'up' : 'down'">
            <i :class="waterTrend > 0 ? 'el-icon-top' : 'el-icon-bottom'"></i>
            {{ Math.abs(waterTrend).toFixed(1) }}% 较昨日
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="label">今日用电量</div>
          <div class="value">
            {{ todayElectricity }} <span class="unit">度</span>
          </div>
          <div class="trend" :class="electricityTrend > 0 ? 'up' : 'down'">
            <i :class="electricityTrend > 0 ? 'el-icon-top' : 'el-icon-bottom'"></i>
            {{ Math.abs(electricityTrend).toFixed(1) }}% 较昨日
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="label">本月水费</div>
          <div class="value text-primary">
            {{ monthWaterFee.toFixed(2) }} <span class="unit">元</span>
          </div>
          <div class="sub-info">共 {{ monthWaterTotal.toFixed(1) }} 吨</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="label">本月电费</div>
          <div class="value text-warning">
            {{ monthElectricityFee.toFixed(2) }} <span class="unit">元</span>
          </div>
          <div class="sub-info">共 {{ monthElectricityTotal.toFixed(1) }} 度</div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="12" v-if="statsType === 'all' || statsType === 'water'">
        <el-card class="mb-20">
          <div slot="header">
            <span>
              <i class="el-icon-water-cup text-primary"></i> 用水量趋势
            </span>
          </div>
          <div ref="waterChart" class="chart-container"></div>
        </el-card>
      </el-col>
      <el-col :span="12" v-if="statsType === 'all' || statsType === 'electricity'">
        <el-card class="mb-20">
          <div slot="header">
            <span>
              <i class="el-icon-lightning text-warning"></i> 用电量趋势
            </span>
          </div>
          <div ref="electricityChart" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="24">
        <el-card>
          <div slot="header">
            <span>用量对比分析</span>
          </div>
          <div ref="compareChart" class="chart-container" style="height: 350px;"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { getDormitoryList, getUsageHistory, getCurrentDormitory } from '@/utils/mockData'
import { EventBus } from '@/utils/eventBus'

export default {
  name: 'StatisticsChart',
  data() {
    return {
      dormitoryList: [],
      selectedDormitory: '',
      statsType: 'all',
      usageData: { water: [], electricity: [], dates: [] },
      waterChart: null,
      electricityChart: null,
      compareChart: null,
      waterPrice: 5.0,
      electricityPrice: 0.8
    }
  },
  computed: {
    todayWater() {
      if (this.usageData.water.length === 0) return 0
      return this.usageData.water[this.usageData.water.length - 1]
    },
    todayElectricity() {
      if (this.usageData.electricity.length === 0) return 0
      return this.usageData.electricity[this.usageData.electricity.length - 1]
    },
    waterTrend() {
      if (this.usageData.water.length < 2) return 0
      const today = this.usageData.water[this.usageData.water.length - 1]
      const yesterday = this.usageData.water[this.usageData.water.length - 2]
      if (yesterday === 0) return 0
      return ((today - yesterday) / yesterday) * 100
    },
    electricityTrend() {
      if (this.usageData.electricity.length < 2) return 0
      const today = this.usageData.electricity[this.usageData.electricity.length - 1]
      const yesterday = this.usageData.electricity[this.usageData.electricity.length - 2]
      if (yesterday === 0) return 0
      return ((today - yesterday) / yesterday) * 100
    },
    monthWaterTotal() {
      return this.usageData.water.reduce((sum, val) => sum + val, 0)
    },
    monthElectricityTotal() {
      return this.usageData.electricity.reduce((sum, val) => sum + val, 0)
    },
    monthWaterFee() {
      return this.monthWaterTotal * this.waterPrice
    },
    monthElectricityFee() {
      return this.monthElectricityTotal * this.electricityPrice
    }
  },
  created() {
    this.dormitoryList = getDormitoryList()
    const currentDorm = getCurrentDormitory()
    if (currentDorm) {
      this.selectedDormitory = currentDorm
      this.loadData()
    }
    EventBus.$on('recharge-success', (data) => {
      if (data.dormitory === this.selectedDormitory) {
        this.loadData()
      }
    })
  },
  beforeDestroy() {
    EventBus.$off('recharge-success')
    window.removeEventListener('resize', this.handleResize)
    if (this.waterChart) this.waterChart.dispose()
    if (this.electricityChart) this.electricityChart.dispose()
    if (this.compareChart) this.compareChart.dispose()
  },
  mounted() {
    this.$nextTick(() => {
      this.initCharts()
    })
    window.addEventListener('resize', this.handleResize)
  },
  methods: {
    loadData() {
      if (!this.selectedDormitory) return
      this.usageData = getUsageHistory(this.selectedDormitory)
      this.$nextTick(() => {
        this.updateCharts()
      })
    },
    initCharts() {
      if (this.$refs.waterChart) {
        this.waterChart = echarts.init(this.$refs.waterChart)
      }
      if (this.$refs.electricityChart) {
        this.electricityChart = echarts.init(this.$refs.electricityChart)
      }
      if (this.$refs.compareChart) {
        this.compareChart = echarts.init(this.$refs.compareChart)
      }
      this.updateCharts()
    },
    updateCharts() {
      this.updateWaterChart()
      this.updateElectricityChart()
      this.updateCompareChart()
    },
    updateWaterChart() {
      if (!this.waterChart) return
      const option = {
        tooltip: {
          trigger: 'axis',
          formatter: '{b}<br/>用水量: {c} 吨'
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: this.usageData.dates,
          boundaryGap: false
        },
        yAxis: {
          type: 'value',
          name: '吨',
          min: 0
        },
        series: [
          {
            name: '用水量',
            type: 'line',
            smooth: true,
            data: this.usageData.water,
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgba(64, 158, 255, 0.5)' },
                { offset: 1, color: 'rgba(64, 158, 255, 0.1)' }
              ])
            },
            lineStyle: {
              color: '#409EFF',
              width: 2
            },
            itemStyle: {
              color: '#409EFF'
            }
          }
        ]
      }
      this.waterChart.setOption(option)
    },
    updateElectricityChart() {
      if (!this.electricityChart) return
      const option = {
        tooltip: {
          trigger: 'axis',
          formatter: '{b}<br/>用电量: {c} 度'
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: this.usageData.dates,
          boundaryGap: false
        },
        yAxis: {
          type: 'value',
          name: '度',
          min: 0
        },
        series: [
          {
            name: '用电量',
            type: 'line',
            smooth: true,
            data: this.usageData.electricity,
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgba(230, 162, 60, 0.5)' },
                { offset: 1, color: 'rgba(230, 162, 60, 0.1)' }
              ])
            },
            lineStyle: {
              color: '#E6A23C',
              width: 2
            },
            itemStyle: {
              color: '#E6A23C'
            }
          }
        ]
      }
      this.electricityChart.setOption(option)
    },
    updateCompareChart() {
      if (!this.compareChart) return
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: ['用水量(吨)', '用电量(度)']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: this.usageData.dates
        },
        yAxis: [
          {
            type: 'value',
            name: '水(吨)',
            position: 'left'
          },
          {
            type: 'value',
            name: '电(度)',
            position: 'right'
          }
        ],
        series: [
          {
            name: '用水量(吨)',
            type: 'bar',
            data: this.usageData.water,
            itemStyle: {
              color: '#409EFF'
            }
          },
          {
            name: '用电量(度)',
            type: 'bar',
            yAxisIndex: 1,
            data: this.usageData.electricity,
            itemStyle: {
              color: '#E6A23C'
            }
          }
        ]
      }
      this.compareChart.setOption(option)
    },
    handleResize() {
      if (this.waterChart) this.waterChart.resize()
      if (this.electricityChart) this.electricityChart.resize()
      if (this.compareChart) this.compareChart.resize()
    }
  }
}
</script>

<style scoped>
.stat-card {
  background: #fff;
  border-radius: 4px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stat-card .label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 10px;
}

.stat-card .value {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
}

.stat-card .unit {
  font-size: 14px;
  font-weight: normal;
  color: #909399;
  margin-left: 5px;
}

.stat-card .trend {
  font-size: 12px;
  margin-top: 8px;
}

.stat-card .trend.up {
  color: #F56C6C;
}

.stat-card .trend.down {
  color: #67C23A;
}

.stat-card .sub-info {
  font-size: 12px;
  color: #909399;
  margin-top: 8px;
}

.chart-container {
  width: 100%;
  height: 300px;
}
</style>
