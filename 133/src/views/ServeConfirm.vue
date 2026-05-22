<template>
  <div>
    <h2 class="page-title">出餐确认</h2>
    
    <el-row :gutter="20">
      <el-col :span="16">
        <el-card style="margin-bottom: 20px;">
          <div slot="header" class="card-header">
            <i class="el-icon-dish"></i>
            <span style="margin-left: 8px;">待出餐订单</span>
            <el-badge :value="pendingOrders.length" class="item" type="warning" style="float: right;"></el-badge>
          </div>
          
          <div v-for="order in pendingOrders" :key="order.id" class="order-card">
            <div class="order-header">
              <div class="order-title">
                <el-tag size="medium" :type="order.urgency ? 'danger' : 'info'">
                  {{ order.tableNo }}号桌
                </el-tag>
                <span class="order-id">{{ order.id }}</span>
                <el-tag size="mini" type="danger" v-if="order.urgency">
                  <i class="el-icon-bell"></i> 加急
                </el-tag>
              </div>
              <div class="order-time">
                <i class="el-icon-time"></i> {{ order.orderTime }}
              </div>
            </div>
            
            <div class="order-customer">
              <i class="el-icon-user"></i> {{ order.customerName }}
            </div>
            
            <el-table :data="order.items" size="small" style="margin: 15px 0;">
              <el-table-column prop="name" label="菜品名称"></el-table-column>
              <el-table-column prop="category" label="分类" width="80"></el-table-column>
              <el-table-column prop="quantity" label="数量" width="60"></el-table-column>
              <el-table-column label="状态" width="80">
                <template slot-scope="scope">
                  <el-tag :type="scope.row.status === 'done' ? 'success' : 'warning'" size="mini">
                    {{ scope.row.status === 'done' ? '已完成' : '制作中' }}
                  </el-tag>
                </template>
              </el-table-column>
            </el-table>
            
            <div v-if="order.remark" class="order-remark">
              <i class="el-icon-chat-dot-round"></i> 备注：{{ order.remark }}
            </div>
            
            <div class="order-actions">
              <span class="ready-count">
                已完成 {{ order.items.filter(i => i.status === 'done').length }} / {{ order.items.length }} 道菜品
              </span>
              <div>
                <el-button size="small" @click="viewDetail(order)">查看详情</el-button>
                <el-button 
                  size="small" 
                  type="success" 
                  @click="confirmServe(order)"
                  :disabled="order.items.some(i => i.status !== 'done')"
                >
                  <i class="el-icon-check"></i> 确认出餐
                </el-button>
              </div>
            </div>
          </div>
          
          <el-empty v-if="pendingOrders.length === 0" description="暂无待出餐订单" style="padding: 40px;"></el-empty>
        </el-card>

        <el-card>
          <div slot="header" class="card-header">
            <i class="el-icon-check-circle" style="color: #67c23a;"></i>
            <span style="margin-left: 8px;">已出餐订单</span>
            <el-badge :value="servedOrders.length" class="item" type="success" style="float: right;"></el-badge>
          </div>
          
          <div v-for="order in servedOrders" :key="order.id" class="order-card served">
            <div class="order-header">
              <div class="order-title">
                <el-tag size="medium" type="success">
                  {{ order.tableNo }}号桌
                </el-tag>
                <span class="order-id">{{ order.id }}</span>
                <el-tag size="mini" type="success">已出餐</el-tag>
              </div>
              <div class="order-time">
                <i class="el-icon-time"></i> 出餐时间：{{ order.serveTime }}
              </div>
            </div>
            
            <div class="order-customer">
              <i class="el-icon-user"></i> {{ order.customerName }}
            </div>
            
            <el-table :data="order.items" size="small" style="margin: 15px 0;">
              <el-table-column prop="name" label="菜品名称"></el-table-column>
              <el-table-column prop="category" label="分类" width="80"></el-table-column>
              <el-table-column prop="quantity" label="数量" width="60"></el-table-column>
            </el-table>
          </div>
          
          <el-empty v-if="servedOrders.length === 0" description="暂无已出餐订单" style="padding: 40px;"></el-empty>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card style="margin-bottom: 20px;">
          <div slot="header" class="card-header">
            <i class="el-icon-data-line"></i>
            <span style="margin-left: 8px;">今日出餐统计</span>
          </div>
          <div class="stat-grid">
            <div class="stat-box">
              <div class="stat-num" style="color: #67c23a;">{{ servedCount }}</div>
              <div class="stat-text">已出餐</div>
            </div>
            <div class="stat-box">
              <div class="stat-num" style="color: #e6a23c;">{{ pendingOrders.length }}</div>
              <div class="stat-text">待出餐</div>
            </div>
            <div class="stat-box">
              <div class="stat-num" style="color: #f56c6c;">{{ urgentCount }}</div>
              <div class="stat-text">加急</div>
            </div>
          </div>
        </el-card>
        
        <el-card>
          <div slot="header" class="card-header">
            <i class="el-icon-date"></i>
            <span style="margin-left: 8px;">最近已出餐</span>
          </div>
          <div class="recent-list">
            <div v-for="order in recentServed" :key="order.id" class="recent-item">
              <div class="recent-info">
                <el-tag size="mini" type="success">{{ order.tableNo }}号桌</el-tag>
                <span class="recent-id">{{ order.id }}</span>
              </div>
              <div class="recent-time">
                <i class="el-icon-time"></i> {{ order.serveTime }}
              </div>
            </div>
            <el-empty v-if="recentServed.length === 0" description="暂无记录" :image-size="60" style="padding: 20px;"></el-empty>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog title="订单详情" :visible.sync="detailVisible" width="600px">
      <el-descriptions :column="2" border v-if="currentOrder">
        <el-descriptions-item label="订单号">{{ currentOrder.id }}</el-descriptions-item>
        <el-descriptions-item label="桌号">{{ currentOrder.tableNo }}</el-descriptions-item>
        <el-descriptions-item label="顾客姓名">{{ currentOrder.customerName }}</el-descriptions-item>
        <el-descriptions-item label="下单时间">{{ currentOrder.orderTime }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentOrder.remark || '无' }}</el-descriptions-item>
      </el-descriptions>
      <el-table :data="currentOrder?.items || []" border style="margin-top: 20px;">
        <el-table-column prop="name" label="菜品名称"></el-table-column>
        <el-table-column prop="category" label="分类" width="100"></el-table-column>
        <el-table-column prop="quantity" label="数量" width="80"></el-table-column>
        <el-table-column prop="price" label="单价" width="80"></el-table-column>
        <el-table-column label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === 'done' ? 'success' : 'warning'" size="small">
              {{ scope.row.status === 'done' ? '已完成' : '制作中' }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-button @click="detailVisible = false">关闭</el-button>
        <el-button 
          type="primary" 
          @click="confirmServe(currentOrder)"
          :disabled="currentOrder?.items.some(i => i.status !== 'done')"
        >
          确认出餐
        </el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { mockOrders } from '@/mock/data'

export default {
  name: 'ServeConfirm',
  data() {
    return {
      orders: [],
      servedOrders: [],
      detailVisible: false,
      currentOrder: null
    }
  },
  computed: {
    pendingOrders() {
      return this.orders.filter(o => o.status !== 'served').sort((a, b) => {
        if (a.urgency && !b.urgency) return -1
        if (!a.urgency && b.urgency) return 1
        return 0
      })
    },
    servedCount() {
      return this.servedOrders.length
    },
    urgentCount() {
      return this.pendingOrders.filter(o => o.urgency).length
    },
    recentServed() {
      return this.servedOrders.slice(0, 5)
    }
  },
  created() {
    this.orders = JSON.parse(JSON.stringify(mockOrders)).filter(o => o.status !== 'done')
    this.servedOrders = [
      { id: 'ORD000', tableNo: 'A05', serveTime: '12:30' },
      { id: 'ORD001', tableNo: 'B02', serveTime: '12:25' }
    ]
  },
  methods: {
    viewDetail(order) {
      this.currentOrder = order
      this.detailVisible = true
    },
    confirmServe(order) {
      this.$confirm(`确认 ${order.tableNo}号桌 出餐吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.orders.findIndex(o => o.id === order.id)
        if (index > -1) {
          const served = this.orders.splice(index, 1)[0]
          served.serveTime = new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
          served.status = 'served'
          this.servedOrders.unshift(served)
          
          this.$nextTick(() => {
            this.$forceUpdate()
          })
        }
        this.detailVisible = false
        this.$message.success(`出餐确认成功！${order.tableNo}号桌已出餐`)
      }).catch(() => {})
    }
  }
}
</script>

<style scoped>
.order-card {
  border: 1px solid #ebeef5;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 15px;
  background: #fafafa;
}

.order-card:hover {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.order-card.served {
  background: #f0f9eb;
  border: 1px solid #e1f3d8;
  opacity: 0.75;
}

.order-card.served:hover {
  opacity: 0.85;
}

.order-card.served .order-title {
  opacity: 0.8;
}

.order-card.served .order-id {
  text-decoration: line-through;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.order-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.order-id {
  font-size: 14px;
  color: #606266;
  font-weight: 500;
}

.order-time {
  font-size: 13px;
  color: #909399;
}

.order-customer {
  font-size: 14px;
  color: #303133;
  margin-bottom: 10px;
}

.order-remark {
  font-size: 13px;
  color: #f56c6c;
  background: #fef0f0;
  padding: 8px 12px;
  border-radius: 4px;
  margin-bottom: 15px;
}

.order-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid #ebeef5;
}

.ready-count {
  font-size: 14px;
  color: #67c23a;
  font-weight: 500;
}

.stat-grid {
  display: flex;
  justify-content: space-around;
  padding: 10px 0;
}

.stat-box {
  text-align: center;
}

.stat-num {
  font-size: 32px;
  font-weight: 600;
  margin-bottom: 5px;
}

.stat-text {
  font-size: 13px;
  color: #606266;
}

.recent-list {
  max-height: 300px;
  overflow-y: auto;
}

.recent-item {
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.recent-item:last-child {
  border-bottom: none;
}

.recent-info {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 5px;
}

.recent-id {
  font-size: 13px;
  color: #606266;
}

.recent-time {
  font-size: 12px;
  color: #909399;
  text-align: right;
}
</style>
