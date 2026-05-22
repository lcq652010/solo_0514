<template>
  <div>
    <h2 class="page-title">催单提醒</h2>
    
    <el-alert 
      title="温馨提示" 
      type="warning" 
      :closable="false"
      style="margin-bottom: 20px;"
    >
      <span>当前共有 <strong style="color: #f56c6c;">{{ urgentOrders.length }}</strong> 笔加急订单，请优先处理</span>
    </el-alert>

    <el-row :gutter="20">
      <el-col :span="8" v-for="order in urgentOrders" :key="order.id">
        <el-card class="urgent-card" shadow="hover">
          <div slot="header" class="card-header-urgent">
            <div class="header-left">
              <i class="el-icon-warning" style="color: #f56c6c; margin-right: 8px;"></i>
              <span>{{ order.tableNo }}号桌</span>
              <el-tag size="mini" type="danger" style="margin-left: 10px;">加急</el-tag>
            </div>
            <div class="order-time">
              <i class="el-icon-time"></i> {{ order.orderTime }}
            </div>
          </div>
          
          <div class="order-info">
            <p><i class="el-icon-document"></i> 订单号：{{ order.id }}</p>
            <p><i class="el-icon-user"></i> 顾客：{{ order.customerName }}</p>
          </div>

          <div class="wait-time">
            <div class="wait-label">已等待时长</div>
            <div class="wait-duration" :class="getWaitClass(order.orderTime)">
              {{ calculateWaitTime(order.orderTime) }}
            </div>
          </div>

          <el-divider content-position="left">
            <i class="el-icon-dish-1"></i> 菜品列表
          </el-divider>

          <div class="dish-list">
            <div v-for="item in order.items" :key="item.id" class="dish-item">
              <div class="dish-name">{{ item.name }} × {{ item.quantity }}</div>
              <el-tag :type="getDishStatusType(item.status)" size="mini">
                {{ getDishStatusText(item.status) }}
              </el-tag>
            </div>
          </div>

          <div v-if="order.remark" class="remark-box">
            <i class="el-icon-chat-dot-round"></i> {{ order.remark }}
          </div>

          <div class="card-actions">
            <el-button type="primary" size="small" @click="handlePrint(order)" icon="el-icon-printer">
              打印小票
            </el-button>
            <el-button type="success" size="small" @click="handleNotify(order)" icon="el-icon-bell">
              通知后厨
            </el-button>
            <el-button type="info" size="small" @click="handleComplete(order)" icon="el-icon-check">
              已处理
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-empty v-if="urgentOrders.length === 0" description="暂无加急订单" style="padding: 60px 0;">
      <i class="el-icon-success" style="font-size: 60px; color: #67c23a;"></i>
    </el-empty>

    <el-card style="margin-top: 20px;">
      <div slot="header" class="card-header">
        <i class="el-icon-s-data"></i>
        <span style="margin-left: 8px;">加急订单统计</span>
      </div>
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="stat-item">
            <div class="stat-icon" style="background: #f56c6c;">
              <i class="el-icon-warning"></i>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ urgentOrders.length }}</div>
              <div class="stat-label">待处理加急</div>
            </div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="stat-item">
            <div class="stat-icon" style="background: #e6a23c;">
              <i class="el-icon-time"></i>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ over15Count }}</div>
              <div class="stat-label">超时15分钟</div>
            </div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="stat-item">
            <div class="stat-icon" style="background: #67c23a;">
              <i class="el-icon-check"></i>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ todayHandled }}</div>
              <div class="stat-label">今日已处理</div>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import { mockOrders } from '@/mock/data'

export default {
  name: 'UrgentReminder',
  data() {
    return {
      orders: [],
      handledToday: 0
    }
  },
  computed: {
    urgentOrders() {
      return this.orders.filter(o => o.urgency && o.status !== 'done').sort((a, b) => {
        return new Date(a.orderTime) - new Date(b.orderTime)
      })
    },
    over15Count() {
      return this.urgentOrders.filter(o => {
        const waitMinutes = this.getWaitMinutes(o.orderTime)
        return waitMinutes >= 15
      }).length
    },
    todayHandled() {
      return this.handledToday + 3
    }
  },
  created() {
    this.orders = JSON.parse(JSON.stringify(mockOrders))
  },
  methods: {
    calculateWaitTime(orderTime) {
      const waitMinutes = this.getWaitMinutes(orderTime)
      if (waitMinutes < 60) {
        return `${waitMinutes} 分钟`
      }
      const hours = Math.floor(waitMinutes / 60)
      const mins = waitMinutes % 60
      return `${hours} 小时 ${mins} 分钟`
    },
    getWaitMinutes(orderTime) {
      const now = new Date()
      const order = new Date(orderTime.replace(/(\d{4})-(\d{2})-(\d{2})/, '$1/$2/$3'))
      return Math.floor((now - order) / 60000)
    },
    getWaitClass(orderTime) {
      const waitMinutes = this.getWaitMinutes(orderTime)
      if (waitMinutes >= 30) return 'wait-danger'
      if (waitMinutes >= 15) return 'wait-warning'
      return 'wait-normal'
    },
    getDishStatusType(status) {
      const map = { waiting: 'info', cooking: 'primary', done: 'success' }
      return map[status] || 'info'
    },
    getDishStatusText(status) {
      const map = { waiting: '等待中', cooking: '制作中', done: '已完成' }
      return map[status] || status
    },
    handlePrint(order) {
      this.$message.success(`正在打印 ${order.tableNo}号桌 小票`)
    },
    handleNotify(order) {
      this.$message({
        message: `已通知后厨优先处理 ${order.tableNo}号桌`,
        type: 'success',
        duration: 2000
      })
    },
    handleComplete(order) {
      this.$confirm(`确认 ${order.tableNo}号桌 加急订单已处理完成？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        order.urgency = false
        this.handledToday++
        this.$message.success('加急订单已处理完成')
      }).catch(() => {})
    }
  }
}
</script>

<style scoped>
.urgent-card {
  margin-bottom: 20px;
  border: 1px solid #f56c6c;
}

.card-header-urgent {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.header-left {
  display: flex;
  align-items: center;
}

.order-time {
  font-size: 13px;
  color: #909399;
}

.order-info {
  font-size: 14px;
  color: #606266;
  margin-bottom: 15px;
}

.order-info p {
  margin: 5px 0;
}

.wait-time {
  text-align: center;
  padding: 15px;
  background: #fef0f0;
  border-radius: 8px;
  margin-bottom: 15px;
}

.wait-label {
  font-size: 13px;
  color: #909399;
  margin-bottom: 5px;
}

.wait-duration {
  font-size: 28px;
  font-weight: 600;
}

.wait-normal {
  color: #e6a23c;
}

.wait-warning {
  color: #f56c6c;
}

.wait-danger {
  color: #f56c6c;
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

.dish-list {
  max-height: 180px;
  overflow-y: auto;
}

.dish-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.dish-item:last-child {
  border-bottom: none;
}

.dish-name {
  font-size: 14px;
  color: #303133;
}

.remark-box {
  margin-top: 15px;
  padding: 10px 15px;
  background: #fdf6ec;
  border-left: 4px solid #e6a23c;
  border-radius: 4px;
  font-size: 13px;
  color: #e6a23c;
}

.card-actions {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
}

.stat-item {
  display: flex;
  align-items: center;
  padding: 15px;
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
  margin-right: 15px;
}

.stat-number {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}
</style>
