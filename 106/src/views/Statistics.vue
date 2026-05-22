<template>
  <div class="page-container">
    <div class="card-wrapper">
      <div class="filter-bar mb-20">
        <el-form :inline="true" :model="filterForm">
          <el-form-item label="选择班级">
            <el-select v-model="filterForm.classId" placeholder="全部班级" style="width: 180px" clearable>
              <el-option v-for="item in classList" :key="item.id" :label="item.className" :value="item.id"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="时间范围">
            <el-date-picker
              v-model="filterForm.dateRange"
              type="monthrange"
              range-separator="至"
              start-placeholder="开始月份"
              end-placeholder="结束月份"
              style="width: 280px"
              value-format="yyyy-MM"
            ></el-date-picker>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" icon="el-icon-search" @click="loadStatistics">查询统计</el-button>
            <el-button icon="el-icon-refresh" @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <div class="summary-cards mb-20">
        <el-row :gutter="20">
          <el-col :span="6">
            <div class="stat-card total">
              <div class="card-icon">
                <i class="el-icon-s-custom"></i>
              </div>
              <div class="card-content">
                <div class="card-value">{{ summaryData.totalStudents }}</div>
                <div class="card-label">学员总数</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card present">
              <div class="card-icon">
                <i class="el-icon-check"></i>
              </div>
              <div class="card-content">
                <div class="card-value">{{ summaryData.totalPresent }}</div>
                <div class="card-label">总出勤人次</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card rate">
              <div class="card-icon">
                <i class="el-icon-data-line"></i>
              </div>
              <div class="card-content">
                <div class="card-value">{{ summaryData.avgRate }}%</div>
                <div class="card-label">平均出勤率</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card class">
              <div class="card-icon">
                <i class="el-icon-notebook-2"></i>
              </div>
              <div class="card-content">
                <div class="card-value">{{ summaryData.totalClasses }}</div>
                <div class="card-label">已上课次</div>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>

      <el-row :gutter="20" class="mb-20">
        <el-col :span="12">
          <el-card shadow="never" class="chart-card">
            <div slot="header" class="card-header">
              <span>月度考勤趋势</span>
            </div>
            <div class="chart-container">
              <table class="trend-table">
                <thead>
                  <tr>
                    <th>月份</th>
                    <th>出勤人次</th>
                    <th>迟到人次</th>
                    <th>缺勤人次</th>
                    <th>出勤率</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(item, index) in monthlyTrend" :key="index">
                    <td>{{ item.month }}</td>
                    <td><span style="color: #67C23A">{{ item.present }}</span></td>
                    <td><span style="color: #E6A23C">{{ item.late }}</span></td>
                    <td><span style="color: #F56C6C">{{ item.absent }}</span></td>
                    <td><el-progress :percentage="item.rate" :stroke-width="8" style="width: 100px"></el-progress></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card shadow="never" class="chart-card">
            <div slot="header" class="card-header">
              <span>考勤状态分布</span>
            </div>
            <div class="chart-container pie-chart">
              <div class="pie-item" v-for="(item, index) in statusDistribution" :key="index">
                <div class="pie-label">
                  <span class="color-dot" :style="{ background: item.color }"></span>
                  {{ item.name }}
                </div>
                <div class="pie-value">
                  <el-progress :percentage="item.value" :stroke-width="10" :color="item.color" style="width: 150px"></el-progress>
                  <span class="value-text">{{ item.count }}人</span>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <el-card shadow="never" class="ranking-card">
        <div slot="header" class="card-header">
          <span>学员考勤排行榜</span>
          <el-radio-group v-model="rankType" size="small">
            <el-radio-button label="rate">按出勤率</el-radio-button>
            <el-radio-button label="present">按出勤次数</el-radio-button>
          </el-radio-group>
        </div>
        <el-table :data="studentRanking" border stripe style="width: 100%">
          <el-table-column type="index" label="排名" width="80" align="center">
            <template slot-scope="scope">
              <span v-if="scope.$index === 0" class="rank-badge gold">1</span>
              <span v-else-if="scope.$index === 1" class="rank-badge silver">2</span>
              <span v-else-if="scope.$index === 2" class="rank-badge bronze">3</span>
              <span v-else>{{ scope.$index + 1 }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="studentNo" label="学号" width="120" align="center"></el-table-column>
          <el-table-column prop="studentName" label="姓名" width="120" align="center"></el-table-column>
          <el-table-column prop="className" label="所属班级" width="180" align="center"></el-table-column>
          <el-table-column prop="presentCount" label="出勤次数" width="120" align="center">
            <template slot-scope="scope">
              <span style="color: #67C23A; font-weight: bold">{{ scope.row.presentCount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="lateCount" label="迟到次数" width="120" align="center">
            <template slot-scope="scope">
              <span style="color: #E6A23C">{{ scope.row.lateCount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="absentCount" label="缺勤次数" width="120" align="center">
            <template slot-scope="scope">
              <span style="color: #F56C6C">{{ scope.row.absentCount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="attendanceRate" label="出勤率" width="150" align="center">
            <template slot-scope="scope">
              <el-progress 
                :percentage="scope.row.attendanceRate" 
                :stroke-width="12"
                :color="getRateColor(scope.row.attendanceRate)"
                style="width: 120px"
              ></el-progress>
              <span style="margin-left: 8px; font-weight: bold">{{ scope.row.attendanceRate }}%</span>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Statistics',
  data() {
    return {
      filterForm: {
        classId: '',
        dateRange: []
      },
      rankType: 'rate',
      classList: [
        { id: 1, className: 'Java全栈01班' },
        { id: 2, className: 'Java全栈02班' },
        { id: 3, className: 'Python01班' },
        { id: 4, className: 'UI设计01班' },
        { id: 5, className: '商务英语01班' },
        { id: 6, className: '前端开发01班' }
      ],
      summaryData: {
        totalStudents: 35,
        totalPresent: 892,
        avgRate: 92,
        totalClasses: 128
      },
      monthlyTrend: [
        { month: '2024-01', present: 156, late: 12, absent: 8, rate: 95 },
        { month: '2024-02', present: 142, late: 15, absent: 10, rate: 93 },
        { month: '2024-03', present: 168, late: 8, absent: 5, rate: 96 },
        { month: '2024-04', present: 158, late: 18, absent: 12, rate: 91 },
        { month: '2024-05', present: 145, late: 22, absent: 15, rate: 88 },
        { month: '2024-06', present: 123, late: 5, absent: 3, rate: 97 }
      ],
      statusDistribution: [
        { name: '全勤学员', value: 65, count: 23, color: '#67C23A' },
        { name: '偶有迟到', value: 25, count: 9, color: '#E6A23C' },
        { name: '缺勤较少', value: 8, count: 3, color: '#F56C6C' },
        { name: '需要关注', value: 2, count: 0, color: '#909399' }
      ],
      studentRanking: [
        { studentNo: 'S20240004', studentName: '赵六', className: 'UI设计01班', presentCount: 45, lateCount: 0, absentCount: 0, attendanceRate: 100 },
        { studentNo: 'S20240006', studentName: '周八', className: '前端开发01班', presentCount: 44, lateCount: 1, absentCount: 0, attendanceRate: 98 },
        { studentNo: 'S20240001', studentName: '张三', className: 'Java全栈01班', presentCount: 43, lateCount: 2, absentCount: 0, attendanceRate: 96 },
        { studentNo: 'S20240003', studentName: '王五', className: 'Python01班', presentCount: 42, lateCount: 3, absentCount: 0, attendanceRate: 93 },
        { studentNo: 'S20240008', studentName: '郑十', className: 'Python01班', presentCount: 40, lateCount: 4, absentCount: 1, attendanceRate: 89 },
        { studentNo: 'S20240002', studentName: '李四', className: 'Java全栈01班', presentCount: 38, lateCount: 5, absentCount: 2, attendanceRate: 84 },
        { studentNo: 'S20240007', studentName: '吴九', className: 'Java全栈02班', presentCount: 36, lateCount: 6, absentCount: 3, attendanceRate: 80 },
        { studentNo: 'S20240005', studentName: '孙七', className: '商务英语01班', presentCount: 30, lateCount: 8, absentCount: 7, attendanceRate: 67 }
      ]
    }
  },
  methods: {
    getRateColor(rate) {
      if (rate >= 95) return '#67C23A'
      if (rate >= 85) return '#409EFF'
      if (rate >= 70) return '#E6A23C'
      return '#F56C6C'
    },
    loadStatistics() {
      this.$message.success('统计数据已刷新')
    },
    handleReset() {
      this.filterForm = {
        classId: '',
        dateRange: []
      }
    }
  },
  watch: {
    rankType(val) {
      if (val === 'rate') {
        this.studentRanking.sort((a, b) => b.attendanceRate - a.attendanceRate)
      } else {
        this.studentRanking.sort((a, b) => b.presentCount - a.presentCount)
      }
    }
  }
}
</script>

<style scoped lang="scss">
.filter-bar {
  padding: 15px;
  background: #f5f7fa;
  border-radius: 4px;
}

.summary-cards {
  .stat-card {
    display: flex;
    align-items: center;
    padding: 20px;
    border-radius: 8px;
    color: #fff;
    
    &.total {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    &.present {
      background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    
    &.rate {
      background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    &.class {
      background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    }
    
    .card-icon {
      font-size: 40px;
      margin-right: 15px;
      opacity: 0.8;
    }
    
    .card-content {
      flex: 1;
      
      .card-value {
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 5px;
      }
      
      .card-label {
        font-size: 14px;
        opacity: 0.9;
      }
    }
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  font-size: 16px;
}

.chart-card {
  height: 100%;
  
  .chart-container {
    min-height: 300px;
  }
  
  .trend-table {
    width: 100%;
    border-collapse: collapse;
    
    th, td {
      padding: 12px 8px;
      text-align: center;
      border-bottom: 1px solid #EBEEF5;
    }
    
    th {
      background: #f5f7fa;
      font-weight: 600;
      color: #606266;
    }
  }
  
  .pie-chart {
    padding: 20px 0;
    
    .pie-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 25px;
      padding: 0 20px;
      
      .pie-label {
        display: flex;
        align-items: center;
        
        .color-dot {
          width: 12px;
          height: 12px;
          border-radius: 50%;
          margin-right: 10px;
        }
      }
      
      .pie-value {
        display: flex;
        align-items: center;
        
        .value-text {
          margin-left: 10px;
          font-weight: bold;
          min-width: 50px;
        }
      }
    }
  }
}

.ranking-card {
  .rank-badge {
    display: inline-block;
    width: 24px;
    height: 24px;
    line-height: 24px;
    border-radius: 50%;
    color: #fff;
    font-weight: bold;
    font-size: 12px;
    
    &.gold {
      background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
    }
    
    &.silver {
      background: linear-gradient(135deg, #C0C0C0 0%, #A9A9A9 100%);
    }
    
    &.bronze {
      background: linear-gradient(135deg, #CD7F32 0%, #8B4513 100%);
    }
  }
}
</style>