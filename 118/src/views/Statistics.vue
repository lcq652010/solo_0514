<template>
  <div class="statistics-page">
    <el-row :gutter="20" class="mb-20">
      <el-col :span="6">
        <el-card class="stat-card total-orders-card">
          <div class="stat-content">
            <div class="stat-icon">
              <i class="el-icon-document"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ statistics.totalOrders }}</div>
              <div class="stat-label">总订单数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card total-amount-card">
          <div class="stat-content">
            <div class="stat-icon">
              <i class="el-icon-money"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">¥{{ statistics.totalAmount }}</div>
              <div class="stat-label">总营业额</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card today-orders-card">
          <div class="stat-content">
            <div class="stat-icon">
              <i class="el-icon-date"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ statistics.todayOrders }}</div>
              <div class="stat-label">今日订单</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card today-amount-card">
          <div class="stat-content">
            <div class="stat-icon">
              <i class="el-icon-wallet"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">¥{{ statistics.todayAmount }}</div>
              <div class="stat-label">今日营业额</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mb-20">
      <el-col :span="12">
        <el-card class="chart-card">
          <div slot="header">
            <span class="card-title">订单状态统计</span>
          </div>
          <div class="status-statistics">
            <div class="status-item pending">
              <div class="status-icon"><i class="el-icon-time"></i></div>
              <div class="status-info">
                <div class="status-count">{{ statistics.pendingOrders }}</div>
                <div class="status-label">待制作</div>
              </div>
            </div>
            <div class="status-item making">
              <div class="status-icon"><i class="el-icon-loading"></i></div>
              <div class="status-info">
                <div class="status-count">{{ statistics.makingOrders }}</div>
                <div class="status-label">制作中</div>
              </div>
            </div>
            <div class="status-item completed">
              <div class="status-icon"><i class="el-icon-check"></i></div>
              <div class="status-info">
                <div class="status-count">{{ statistics.completedOrders }}</div>
                <div class="status-label">已完成</div>
              </div>
            </div>
            <div class="status-item paid">
              <div class="status-icon"><i class="el-icon-success"></i></div>
              <div class="status-info">
                <div class="status-count">{{ statistics.paidOrders }}</div>
                <div class="status-label">已支付</div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="chart-card">
          <div slot="header">
            <span class="card-title">热销商品 TOP5</span>
          </div>
          <div class="hot-products">
            <div
              v-for="(product, index) in hotProducts"
              :key="index"
              class="product-rank-item"
            >
              <div class="rank-number" :class="'rank-' + (index + 1)">{{ index + 1 }}</div>
              <div class="product-name">{{ product.name }}</div>
              <div class="product-sales">销量：{{ product.quantity }} 杯</div>
            </div>
            <el-empty v-if="hotProducts.length === 0" description="暂无数据" :image-size="80"></el-empty>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="table-card">
      <div slot="header">
        <span class="card-title">近期订单明细</span>
      </div>
      <el-table :data="recentOrders" border stripe style="width: 100%">
        <el-table-column prop="orderNo" label="订单号" width="160"></el-table-column>
        <el-table-column prop="customerName" label="顾客姓名" width="100"></el-table-column>
        <el-table-column prop="takeType" label="取餐方式" width="90">
          <template slot-scope="scope">
            <el-tag :type="scope.row.takeType === '堂食' ? '' : 'warning'" size="mini">{{ scope.row.takeType }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="paymentStatus" label="支付状态" width="90">
          <template slot-scope="scope">
            <el-tag :type="scope.row.paymentStatus === 'paid' ? 'success' : 'danger'" size="mini">
              {{ scope.row.paymentStatus === 'paid' ? '已支付' : '未支付' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="totalAmount" label="订单金额" width="100">
          <template slot-scope="scope">
            <span class="amount">¥{{ scope.row.totalAmount }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="制作状态" width="90">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="mini">{{ getStatusText(scope.row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="下单时间"></el-table-column>
      </el-table>
      <el-empty v-if="recentOrders.length === 0" description="暂无订单数据" :image-size="80" style="margin-top: 30px;"></el-empty>
    </el-card>
  </div>
</template>

<script>
import { EventBus } from '@/utils/eventBus'
export default {
  name: 'Statistics',
  data() {
    return {
      orders: []
    }
  },
  computed: {
    statistics() {
      const today = new Date().toLocaleDateString()
      const completedOrders = this.orders.filter(o => o.status === 'completed')
      const todayOrdersList = this.orders.filter(o => {
        const orderDate = new Date(o.createTime).toLocaleDateString()
        return orderDate === today
      })
      const todayCompleted = todayOrdersList.filter(o => o.status === 'completed')
      return {
        totalOrders: this.orders.length,
        totalAmount: completedOrders.reduce((sum, o) => sum + o.totalAmount, 0),
        todayOrders: todayOrdersList.length,
        todayAmount: todayCompleted.reduce((sum, o) => sum + o.totalAmount, 0),
        pendingOrders: this.orders.filter(o => o.status === 'pending').length,
        makingOrders: this.orders.filter(o => o.status === 'making').length,
        completedOrders: completedOrders.length,
        cancelledOrders: this.orders.filter(o => o.status === 'cancelled').length,
        paidOrders: this.orders.filter(o => o.paymentStatus === 'paid').length,
        unpaidOrders: this.orders.filter(o => o.paymentStatus === 'unpaid').length
      }
    },
    hotProducts() {
      const productMap = {}
      this.orders.filter(o => o.status !== 'cancelled').forEach(order => {
        order.items.forEach(item => {
          if (productMap[item.name]) {
            productMap[item.name].quantity += item.quantity
          } else {
            productMap[item.name] = { name: item.name, quantity: item.quantity }
          }
        })
      })
      return Object.values(productMap)
        .sort((a, b) => b.quantity - a.quantity)
        .slice(0, 5)
    },
    recentOrders() {
      return this.orders.slice(0, 10)
    }
  },
  created() {
    this.loadOrders()
    EventBus.$on('orderStatusChanged', () => {
      this.loadOrders()
    })
  },
  beforeDestroy() {
    EventBus.$off('orderStatusChanged')
  },
  methods: {
    loadOrders() {
      this.orders = JSON.parse(localStorage.getItem('milkTeaOrders') || '[]')
    },
    getStatusType(status) {
      const types = {
        pending: 'warning',
        making: 'primary',
        completed: 'success',
        cancelled: 'danger'
      }
      return types[status] || 'info'
    },
    getStatusText(status) {
      const texts = {
        pending: '待制作',
        making: '制作中',
        completed: '已完成',
        cancelled: '已取消'
      }
      return texts[status] || status
    }
  }
}
</script>

<style lang="scss" scoped>
.statistics-page {
  .stat-card {
    .stat-content {
      display: flex;
      align-items: center;
      .stat-icon {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 20px;
        i {
          font-size: 28px;
          color: #fff;
        }
      }
      .stat-info {
        flex: 1;
        .stat-value {
          font-size: 28px;
          font-weight: bold;
          color: #303133;
          margin-bottom: 5px;
        }
        .stat-label {
          font-size: 14px;
          color: #909399;
        }
      }
    }
    &.total-orders-card .stat-icon {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    &.total-amount-card .stat-icon {
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    &.today-orders-card .stat-icon {
      background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    &.today-amount-card .stat-icon {
      background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
    }
  }
  .chart-card {
    height: 280px;
    ::v-deep .el-card__body {
      height: calc(100% - 57px);
    }
  }
  .status-statistics {
    display: flex;
    justify-content: space-around;
    align-items: center;
    height: 100%;
    .status-item {
      text-align: center;
      .status-icon {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 15px;
        i {
          font-size: 28px;
          color: #fff;
        }
      }
      .status-info {
        .status-count {
          font-size: 24px;
          font-weight: bold;
          margin-bottom: 5px;
        }
        .status-label {
          font-size: 14px;
          color: #909399;
        }
      }
      &.pending .status-icon {
        background: #e6a23c;
        .status-count { color: #e6a23c; }
      }
      &.making .status-icon {
        background: #409eff;
        .status-count { color: #409eff; }
      }
      &.completed .status-icon {
        background: #67c23a;
        .status-count { color: #67c23a; }
      }
      &.cancelled .status-icon {
        background: #f56c6c;
        .status-count { color: #f56c6c; }
      }
      &.paid .status-icon {
        background: #67c23a;
        .status-count { color: #67c23a; }
      }
    }
  }
  .hot-products {
    height: 100%;
    .product-rank-item {
      display: flex;
      align-items: center;
      padding: 10px 0;
      border-bottom: 1px solid #ebeef5;
      &:last-child {
        border-bottom: none;
      }
      .rank-number {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #fff;
        font-weight: bold;
        margin-right: 15px;
        &.rank-1 {
          background: linear-gradient(135deg, #ffd700 0%, #ffaa00 100%);
        }
        &.rank-2 {
          background: linear-gradient(135deg, #c0c0c0 0%, #a0a0a0 100%);
        }
        &.rank-3 {
          background: linear-gradient(135deg, #cd7f32 0%, #b87333 100%);
        }
        &.rank-4, &.rank-5 {
          background: #909399;
        }
      }
      .product-name {
        flex: 1;
        font-size: 14px;
        color: #303133;
      }
      .product-sales {
        font-size: 14px;
        color: #f56c6c;
        font-weight: bold;
      }
    }
  }
  .amount {
    font-weight: bold;
    color: #f56c6c;
  }
}
</style>
