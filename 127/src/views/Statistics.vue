<template>
  <div class="statistics">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <i class="el-icon-time"></i>
            <div class="stat-content">
              <div class="stat-value">{{ statisticsData.total || 0 }}</div>
              <div class="stat-label">总加班时长(小时)</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <i class="el-icon-data-line"></i>
            <div class="stat-content">
              <div class="stat-value">{{ statisticsData.average || 0 }}</div>
              <div class="stat-label">月均加班时长(小时)</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <div style="text-align: center; color: #409EFF; font-size: 18px; font-weight: bold">
            温馨提示：合理安排工作时间，注意身体健康
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card>
          <div slot="header">月度加班趋势</div>
          <div ref="lineChart" style="height: 350px"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <div slot="header">加班类型分布</div>
          <div ref="pieChart" style="height: 350px"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import { getStatistics } from '@/api/overtime';

export default {
  name: 'Statistics',
  data() {
    return {
      statisticsData: {},
      lineChart: null,
      pieChart: null
    };
  },
  async created() {
    await this.fetchData();
  },
  mounted() {
    this.$nextTick(() => {
      this.initCharts();
    });
  },
  methods: {
    async fetchData() {
      try {
        const res = await getStatistics();
        if (res.data.code === 200) {
          this.statisticsData = res.data.data;
          if (this.lineChart && this.pieChart) {
            this.updateCharts();
          }
        }
      } catch (error) {
        this.$message.error('获取统计数据失败');
      }
    },
    initCharts() {
      this.lineChart = echarts.init(this.$refs.lineChart);
      this.pieChart = echarts.init(this.$refs.pieChart);
      this.updateCharts();

      window.addEventListener('resize', () => {
        this.lineChart.resize();
        this.pieChart.resize();
      });
    },
    updateCharts() {
      const { monthly, byType } = this.statisticsData;

      const lineOption = {
        tooltip: {
          trigger: 'axis'
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: monthly && monthly.months ? monthly.months : []
        },
        yAxis: {
          type: 'value',
          name: '小时'
        },
        series: [
          {
            name: '加班时长',
            type: 'line',
            smooth: true,
            data: monthly && monthly.hours ? monthly.hours : [],
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgba(64, 158, 255, 0.5)' },
                { offset: 1, color: 'rgba(64, 158, 255, 0.1)' }
              ])
            },
            itemStyle: {
              color: '#409EFF'
            }
          }
        ]
      };

      const pieOption = {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c}小时 ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            name: '加班类型',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 2
            },
            label: {
              show: true,
              formatter: '{b}: {c}小时'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: '16',
                fontWeight: 'bold'
              }
            },
            data: byType || []
          }
        ],
        color: ['#409EFF', '#67C23A', '#E6A23C']
      };

      this.lineChart.setOption(lineOption);
      this.pieChart.setOption(pieOption);
    }
  },
  beforeDestroy() {
    if (this.lineChart) {
      this.lineChart.dispose();
    }
    if (this.pieChart) {
      this.pieChart.dispose();
    }
  }
};
</script>

<style scoped>
.statistics {
  padding: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-item i {
  font-size: 48px;
  color: #409EFF;
  margin-right: 20px;
}

.stat-content {
  text-align: left;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}
</style>
