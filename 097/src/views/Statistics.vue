<template>
  <div class="statistics-container">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="stat-card today-sales">
          <div class="stat-content">
            <div class="stat-icon">
              <i class="el-icon-s-finance"></i>
            </div>
            <div class="stat-info">
              <p class="stat-label">今日营业额</p>
              <p class="stat-value">¥{{ todaySales.toFixed(2) }}</p>
              <p class="stat-trend up">
                <i class="el-icon-top"></i> 12.5%
              </p>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card order-count">
          <div class="stat-content">
            <div class="stat-icon">
              <i class="el-icon-s-order"></i>
            </div>
            <div class="stat-info">
              <p class="stat-label">今日订单数</p>
              <p class="stat-value">{{ todayOrders }}</p>
              <p class="stat-trend up">
                <i class="el-icon-top"></i> 8.3%
              </p>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card avg-price">
          <div class="stat-content">
            <div class="stat-icon">
              <i class="el-icon-goods"></i>
            </div>
            <div class="stat-info">
              <p class="stat-label">客单价</p>
              <p class="stat-value">¥{{ avgPrice.toFixed(2) }}</p>
              <p class="stat-trend up">
                <i class="el-icon-top"></i> 3.2%
              </p>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card dish-count">
          <div class="stat-content">
            <div class="stat-icon">
              <i class="el-icon-shopping-cart-2"></i>
            </div>
            <div class="stat-info">
              <p class="stat-label">菜品销量</p>
              <p class="stat-value">{{ dishSalesCount }}</p>
              <p class="stat-trend down">
                <i class="el-icon-bottom"></i> 2.1%
              </p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="16">
        <el-card>
          <div slot="header" class="card-header">
            <span>近7日营业额趋势</span>
          </div>
          <div class="chart-container">
            <el-table :data="weekData" border stripe style="width: 100%">
              <el-table-column prop="date" label="日期" align="center"></el-table-column>
              <el-table-column prop="sales" label="营业额" align="center">
                <template slot-scope="scope">
                  <span style="color: #f56c6c; font-weight: bold;">¥{{ scope.row.sales }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="orders" label="订单数" align="center"></el-table-column>
              <el-table-column prop="avgPrice" label="客单价" align="center">
                <template slot-scope="scope">¥{{ scope.row.avgPrice }}</template>
              </el-table-column>
              <el-table-column label="趋势" width="120" align="center">
                <template slot-scope="scope">
                  <el-tag :type="scope.row.trend > 0 ? 'success' : 'danger'" size="small">
                    {{ scope.row.trend > 0 ? '+' : '' }}{{ scope.row.trend }}%
                  </el-tag>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card>
          <div slot="header" class="card-header">
            <span>热销菜品TOP5</span>
          </div>
          <div class="top-dishes">
            <div v-for="(dish, index) in topDishes" :key="index" class="top-dish-item">
              <div class="dish-rank" :class="`rank-${index + 1}`">{{ index + 1 }}</div>
              <div class="dish-info">
                <p class="dish-name">{{ dish.name }}</p>
                <p class="dish-sales">销量：{{ dish.sales }}份</p>
              </div>
              <div class="dish-revenue">
                ¥{{ dish.revenue }}
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12">
        <el-card>
          <div slot="header" class="card-header">
            <span>分类销售占比</span>
          </div>
          <div class="category-stats">
            <div v-for="(item, index) in categoryStats" :key="index" class="category-item">
              <div class="category-header">
                <span class="category-name">{{ item.name }}</span>
                <span class="category-percent">{{ item.percent }}%</span>
              </div>
              <el-progress :percentage="item.percent" :color="item.color"></el-progress>
              <div class="category-detail">
                <span>销售额：¥{{ item.sales }}</span>
                <span>订单：{{ item.orders }}单</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card>
          <div slot="header" class="card-header">
            <span>订单时段分布</span>
          </div>
          <div class="time-distribution">
            <div v-for="(item, index) in timeDistribution" :key="index" class="time-item">
              <div class="time-label">{{ item.time }}</div>
              <div class="time-bar-container">
                <div class="time-bar" :style="{ width: item.percent + '%', backgroundColor: item.color }"></div>
              </div>
              <div class="time-value">{{ item.count }}单</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'Statistics',
  data() {
    return {
      todaySales: 2586.50,
      todayOrders: 47,
      avgPrice: 55.03,
      dishSalesCount: 132,
      weekData: [
        { date: '05-10', sales: 1856, orders: 35, avgPrice: 53.03, trend: 5.2 },
        { date: '05-11', sales: 2120, orders: 38, avgPrice: 55.79, trend: 14.2 },
        { date: '05-12', sales: 1980, orders: 36, avgPrice: 55.00, trend: -6.6 },
        { date: '05-13', sales: 2350, orders: 42, avgPrice: 55.95, trend: 18.7 },
        { date: '05-14', sales: 2680, orders: 48, avgPrice: 55.83, trend: 14.0 },
        { date: '05-15', sales: 2450, orders: 45, avgPrice: 54.44, trend: -8.6 },
        { date: '05-16', sales: 2586.5, orders: 47, avgPrice: 55.03, trend: 5.6 }
      ],
      topDishes: [
        { name: '宫保鸡丁', sales: 45, revenue: 1710 },
        { name: '麻婆豆腐', sales: 38, revenue: 1064 },
        { name: '凉拌黄瓜', sales: 32, revenue: 576 },
        { name: '西红柿鸡蛋汤', sales: 28, revenue: 420 },
        { name: '米饭', sales: 86, revenue: 258 }
      ],
      categoryStats: [
        { name: '热菜', sales: 3850, orders: 78, percent: 45, color: '#67c23a' },
        { name: '凉菜', sales: 1650, orders: 52, percent: 19, color: '#409eff' },
        { name: '主食', sales: 1200, orders: 95, percent: 14, color: '#e6a23c' },
        { name: '汤品', sales: 980, orders: 45, percent: 11, color: '#909399' },
        { name: '饮品', sales: 920, orders: 68, percent: 11, color: '#f56c6c' }
      ],
      timeDistribution: [
        { time: '09-11', count: 5, percent: 10, color: '#e6a23c' },
        { time: '11-13', count: 22, percent: 47, color: '#67c23a' },
        { time: '13-15', count: 8, percent: 17, color: '#409eff' },
        { time: '15-17', count: 3, percent: 6, color: '#909399' },
        { time: '17-19', count: 18, percent: 38, color: '#67c23a' },
        { time: '19-21', count: 12, percent: 25, color: '#409eff' },
        { time: '21-23', count: 4, percent: 8, color: '#909399' }
      ]
    }
  }
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.statistics-container {
  padding: 0;
}

.stat-card {
  cursor: pointer;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.stat-content {
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
}

.stat-icon i {
  font-size: 28px;
  color: #fff;
}

.today-sales .stat-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.order-count .stat-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.avg-price .stat-icon {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.dish-count .stat-icon {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.stat-info .stat-label {
  font-size: 14px;
  color: #909399;
  margin: 0 0 5px 0;
}

.stat-info .stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  margin: 0 0 5px 0;
}

.stat-trend {
  font-size: 12px;
  margin: 0;
}

.stat-trend.up {
  color: #67c23a;
}

.stat-trend.down {
  color: #f56c6c;
}

.chart-container {
  min-height: 300px;
}

.top-dishes {
  padding: 10px 0;
}

.top-dish-item {
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.top-dish-item:last-child {
  border-bottom: none;
}

.dish-rank {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: bold;
  margin-right: 15px;
}

.rank-1 {
  background: linear-gradient(135deg, #ffd700 0%, #ffaa00 100%);
}

.rank-2 {
  background: linear-gradient(135deg, #c0c0c0 0%, #a0a0a0 100%);
}

.rank-3 {
  background: linear-gradient(135deg, #cd7f32 0%, #b87333 100%);
}

.rank-4,
.rank-5 {
  background: #909399;
}

.dish-info {
  flex: 1;
}

.dish-name {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  margin: 0 0 3px 0;
}

.dish-sales {
  font-size: 12px;
  color: #909399;
  margin: 0;
}

.dish-revenue {
  font-size: 16px;
  font-weight: bold;
  color: #f56c6c;
}

.category-stats {
  padding: 10px 0;
}

.category-item {
  padding: 15px 0;
  border-bottom: 1px solid #f0f0f0;
}

.category-item:last-child {
  border-bottom: none;
}

.category-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.category-name {
  font-weight: 500;
  color: #303133;
}

.category-percent {
  font-weight: bold;
  color: #409eff;
}

.category-detail {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  font-size: 12px;
  color: #909399;
}

.time-distribution {
  padding: 10px 0;
}

.time-item {
  display: flex;
  align-items: center;
  padding: 10px 0;
}

.time-label {
  width: 60px;
  font-size: 13px;
  color: #606266;
}

.time-bar-container {
  flex: 1;
  height: 20px;
  background-color: #f5f7fa;
  border-radius: 10px;
  margin: 0 10px;
  overflow: hidden;
}

.time-bar {
  height: 100%;
  border-radius: 10px;
  transition: width 0.3s;
}

.time-value {
  width: 50px;
  text-align: right;
  font-size: 13px;
  color: #409eff;
  font-weight: 500;
}
</style>