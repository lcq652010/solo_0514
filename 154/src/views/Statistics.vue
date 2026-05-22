<template>
  <div class="statistics-page">
    <div class="page-header">
      <h1 class="page-title">客流统计</h1>
      <p class="page-subtitle">实时监控景区客流数据</p>
    </div>

    <div class="stat-cards">
      <el-card class="stat-card visitors">
        <div class="stat-content">
          <div class="stat-icon">
            <i class="el-icon-user"></i>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ statistics.todayVisitors }}</div>
            <div class="stat-label">今日游客</div>
          </div>
        </div>
        <div class="stat-trend up">
          <i class="el-icon-top"></i>
          <span>12.5%</span>
          <span class="trend-label">较昨日</span>
        </div>
      </el-card>

      <el-card class="stat-card orders">
        <div class="stat-content">
          <div class="stat-icon">
            <i class="el-icon-document"></i>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ statistics.todayOrders }}</div>
            <div class="stat-label">今日订单</div>
          </div>
        </div>
        <div class="stat-trend up">
          <i class="el-icon-top"></i>
          <span>8.3%</span>
          <span class="trend-label">较昨日</span>
        </div>
      </el-card>

      <el-card class="stat-card revenue">
        <div class="stat-content">
          <div class="stat-icon">
            <i class="el-icon-money"></i>
          </div>
          <div class="stat-info">
            <div class="stat-value">¥{{ statistics.totalRevenue.toLocaleString() }}</div>
            <div class="stat-label">今日营收</div>
          </div>
        </div>
        <div class="stat-trend up">
          <i class="el-icon-top"></i>
          <span>15.2%</span>
          <span class="trend-label">较昨日</span>
        </div>
      </el-card>

      <el-card class="stat-card tickets">
        <div class="stat-content">
          <div class="stat-icon">
            <i class="el-icon-tickets"></i>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ statistics.remainingTickets.toLocaleString() }}</div>
            <div class="stat-label">剩余门票</div>
          </div>
        </div>
        <div class="stat-trend down">
          <i class="el-icon-bottom"></i>
          <span>3.1%</span>
          <span class="trend-label">较昨日</span>
        </div>
      </el-card>
    </div>

    <div class="chart-section">
      <el-card class="chart-card">
        <div slot="header" class="card-header">
          <span>本周客流趋势</span>
        </div>
        <div class="chart-container">
          <table class="weekly-table">
            <thead>
              <tr>
                <th>日期</th>
                <th>游客数</th>
                <th>订单数</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in statistics.weeklyData" :key="index">
                <td>{{ item.date }}</td>
                <td>
                  <div class="progress-wrapper">
                    <div
                      class="progress-bar"
                      :style="{ width: (item.visitors / maxVisitors * 100) + '%' }"
                    ></div>
                    <span class="progress-text">{{ item.visitors }}</span>
                  </div>
                </td>
                <td>
                  <div class="progress-wrapper">
                    <div
                      class="progress-bar orders"
                      :style="{ width: (item.orders / maxOrders * 100) + '%' }"
                    ></div>
                    <span class="progress-text">{{ item.orders }}</span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </el-card>

      <el-card class="chart-card">
        <div slot="header" class="card-header">
          <span>门票类型销量分布</span>
        </div>
        <div class="ticket-distribution">
          <div
            v-for="(ticket, index) in ticketDistribution"
            :key="index"
            class="distribution-item"
          >
            <div class="item-header">
              <span class="ticket-name">{{ ticket.name }}</span>
              <span class="ticket-count">{{ ticket.count }}张</span>
            </div>
            <div class="distribution-bar-wrapper">
              <div
                class="distribution-bar"
                :style="{
                  width: (ticket.count / maxDistributionCount * 100) + '%',
                  background: ticket.color
                }"
              ></div>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <el-card class="real-time-card">
      <div slot="header" class="card-header">
        <span>实时客流监控</span>
        <el-tag type="success" size="small">运行正常</el-tag>
      </div>
      <div class="real-time-content">
        <div class="monitor-item">
          <div class="monitor-icon entrance">
            <i class="el-icon-right"></i>
          </div>
          <div class="monitor-info">
            <div class="monitor-value">156</div>
            <div class="monitor-label">当前在园人数</div>
          </div>
        </div>
        <div class="monitor-item">
          <div class="monitor-icon exit">
            <i class="el-icon-left"></i>
          </div>
          <div class="monitor-info">
            <div class="monitor-value">892</div>
            <div class="monitor-label">今日已入园</div>
          </div>
        </div>
        <div class="monitor-item">
          <div class="monitor-icon peak">
            <i class="el-icon-c-scale-to-original"></i>
          </div>
          <div class="monitor-info">
            <div class="monitor-value">14:30</div>
            <div class="monitor-label">客流高峰时间</div>
          </div>
        </div>
        <div class="monitor-item">
          <div class="monitor-icon avg">
            <i class="el-icon-data-line"></i>
          </div>
          <div class="monitor-info">
            <div class="monitor-value">2.5h</div>
            <div class="monitor-label">平均游玩时长</div>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { statistics } from '@/mock/data';

export default {
  name: 'Statistics',
  data() {
    return {
      statistics,
      ticketDistribution: [
        { name: '成人票', count: 680, color: '#409EFF' },
        { name: '儿童票', count: 320, color: '#67C23A' },
        { name: '老年票', count: 180, color: '#E6A23C' },
        { name: '学生票', count: 240, color: '#909399' },
        { name: '家庭套票', count: 150, color: '#F56C6C' },
        { name: '两日通票', count: 90, color: '#606266' }
      ]
    };
  },
  computed: {
    maxVisitors() {
      return Math.max(...this.statistics.weeklyData.map(item => item.visitors));
    },
    maxOrders() {
      return Math.max(...this.statistics.weeklyData.map(item => item.orders));
    },
    maxDistributionCount() {
      return Math.max(...this.ticketDistribution.map(item => item.count));
    }
  }
};
</script>

<style scoped>
.statistics-page {
  padding: 0;
}

.stat-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  border: none;
  border-radius: 12px;
  overflow: hidden;
}

.stat-card.visitors {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-card.orders {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}

.stat-card.revenue {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.stat-card.tickets {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 20px;
  color: #fff;
}

.stat-icon {
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon i {
  font-size: 28px;
  color: #fff;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
}

.stat-trend {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  gap: 8px;
  color: #fff;
}

.stat-trend.up {
  color: #67C23A;
}

.stat-trend.down {
  color: #F56C6C;
}

.stat-trend span {
  font-size: 14px;
}

.trend-label {
  color: rgba(255, 255, 255, 0.8);
  margin-left: auto;
}

.chart-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 24px;
}

.card-header {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-container {
  padding: 10px 0;
}

.weekly-table {
  width: 100%;
  border-collapse: collapse;
}

.weekly-table th,
.weekly-table td {
  padding: 12px 0;
  text-align: left;
  border-bottom: 1px solid #F5F7FA;
}

.weekly-table th {
  font-weight: 600;
  color: #909399;
  font-size: 13px;
}

.weekly-table tr:last-child td {
  border-bottom: none;
}

.progress-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
}

.progress-bar {
  height: 8px;
  background: #409EFF;
  border-radius: 4px;
  min-width: 10%;
  transition: width 0.3s;
}

.progress-bar.orders {
  background: #67C23A;
}

.progress-text {
  font-size: 14px;
  color: #606266;
  min-width: 60px;
}

.ticket-distribution {
  padding: 10px 0;
}

.distribution-item {
  margin-bottom: 20px;
}

.distribution-item:last-child {
  margin-bottom: 0;
}

.item-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.ticket-name {
  font-size: 14px;
  color: #303133;
}

.ticket-count {
  font-size: 14px;
  font-weight: 600;
  color: #409EFF;
}

.distribution-bar-wrapper {
  width: 100%;
  height: 12px;
  background: #F5F7FA;
  border-radius: 6px;
  overflow: hidden;
}

.distribution-bar {
  height: 100%;
  border-radius: 6px;
  transition: width 0.3s;
}

.real-time-content {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 30px;
  padding: 10px 0;
}

.monitor-item {
  display: flex;
  align-items: center;
  gap: 15px;
}

.monitor-icon {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.monitor-icon.entrance {
  background: #ECF5FF;
}

.monitor-icon.entrance i {
  color: #409EFF;
}

.monitor-icon.exit {
  background: #f0f9eb;
}

.monitor-icon.exit i {
  color: #67C23A;
}

.monitor-icon.peak {
  background: #fdf6ec;
}

.monitor-icon.peak i {
  color: #E6A23C;
}

.monitor-icon.avg {
  background: #f4f4f5;
}

.monitor-icon.avg i {
  color: #909399;
}

.monitor-icon i {
  font-size: 24px;
}

.monitor-value {
  font-size: 24px;
  font-weight: 700;
  color: #303133;
  margin-bottom: 5px;
}

.monitor-label {
  font-size: 14px;
  color: #909399;
}

@media (max-width: 1200px) {
  .stat-cards {
    grid-template-columns: repeat(2, 1fr);
  }

  .real-time-content {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .stat-cards {
    grid-template-columns: 1fr;
  }

  .chart-section {
    grid-template-columns: 1fr;
  }

  .real-time-content {
    grid-template-columns: 1fr;
  }
}
</style>
