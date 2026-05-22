<template>
  <div class="order-list-container">
    <el-card class="list-card" shadow="hover">
      <div slot="header" class="card-header">
        <div class="header-left">
          <i class="el-icon-s-order"></i>
          <span>订单管理列表</span>
        </div>
        <div class="header-right">
          <el-button type="primary" size="small" @click="refreshOrders">
            <i class="el-icon-refresh"></i> 刷新
          </el-button>
        </div>
      </div>

      <div class="stats-row">
        <el-row :gutter="20">
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon" style="background: #e6f7ff;">
                <i class="el-icon-document" style="color: #1890ff;"></i>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ orders.length }}</div>
                <div class="stat-label">总订单数</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon" style="background: #fff7e6;">
                <i class="el-icon-time" style="color: #fa8c16;"></i>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ processingCount }}</div>
                <div class="stat-label">制作中</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon" style="background: #f6ffed;">
                <i class="el-icon-success" style="color: #52c41a;"></i>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ completedCount }}</div>
                <div class="stat-label">已完工</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon" style="background: #fff0f6;">
                <i class="el-icon-wallet" style="color: #eb2f96;"></i>
              </div>
              <div class="stat-info">
                <div class="stat-value">¥{{ totalAmount }}</div>
                <div class="stat-label">总金额</div>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>

      <el-table 
        :data="orders" 
        border 
        style="width: 100%"
        v-loading="loading"
        empty-text="暂无订单数据">
        <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
        <el-table-column prop="id" label="订单编号" width="160" align="center">
          <template slot-scope="scope">
            <span style="color: #8B4513; font-weight: bold;">WD{{ scope.row.id }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="customerName" label="客户姓名" width="100" align="center"></el-table-column>
        <el-table-column prop="phone" label="联系电话" width="120" align="center"></el-table-column>
        <el-table-column prop="woodType" label="木料类型" width="100" align="center">
          <template slot-scope="scope">
            <el-tag size="small" type="warning">{{ scope.row.woodType }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="pattern" label="雕刻图案" width="100" align="center">
          <template slot-scope="scope">
            <el-tag size="small" type="info">{{ scope.row.pattern }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="totalPrice" label="订单金额" width="100" align="center">
          <template slot-scope="scope">
            <span style="color: #ff6600; font-weight: bold;">¥{{ scope.row.totalPrice }}</span>
          </template>
        </el-table-column>
        <el-table-column label="制作进度" width="280" align="center">
          <template slot-scope="scope">
            <div class="progress-wrapper">
              <el-steps :active="getStepIndex(scope.row.status)" size="small" finish-status="success">
                <el-step v-for="step in progressSteps" :key="step" :title="step"></el-step>
              </el-steps>
            </div>
            <el-select 
              v-model="scope.row.status" 
              size="small" 
              style="width: 120px; margin-top: 10px;"
              @change="newStatus => updateStatus(scope.row, newStatus)">
              <el-option 
                v-for="step in progressSteps" 
                :key="step" 
                :label="step" 
                :value="step"
                :disabled="!canSelectStatus(scope.row, step)">
              </el-option>
            </el-select>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="下单时间" width="160" align="center"></el-table-column>
        <el-table-column label="操作" width="180" align="center">
          <template slot-scope="scope">
            <el-button type="primary" size="small" icon="el-icon-view" @click="viewDetail(scope.row)">
              详情
            </el-button>
            <el-button type="danger" size="small" icon="el-icon-delete" @click="deleteOrder(scope.row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrapper" v-if="orders.length > 0">
        <el-pagination
          background
          layout="total, prev, pager, next, jumper"
          :total="orders.length"
          :page-size="10"
          style="justify-content: center;">
        </el-pagination>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'OrderList',
  data() {
    return {
      loading: false,
      orders: [],
      progressSteps: ['选料', '开料', '雕刻', '打磨', '烫金', '上油', '完工']
    }
  },
  computed: {
    processingCount() {
      return this.orders.filter(o => o.status !== '完工').length
    },
    completedCount() {
      return this.orders.filter(o => o.status === '完工').length
    },
    totalAmount() {
      return this.orders.reduce((sum, o) => sum + (o.totalPrice || 0), 0)
    }
  },
  mounted() {
    this.loadOrders()
    window.addEventListener('storage', this.loadOrders)
  },
  beforeDestroy() {
    window.removeEventListener('storage', this.loadOrders)
  },
  methods: {
    loadOrders() {
      this.loading = true
      setTimeout(() => {
        const orders = JSON.parse(localStorage.getItem('woodOrders') || '[]')
        this.orders = orders.sort((a, b) => new Date(b.createTime) - new Date(a.createTime))
        this.loading = false
      }, 300)
    },
    refreshOrders() {
      this.loadOrders()
      this.$message.success('订单列表已刷新')
    },
    getStepIndex(status) {
      return this.progressSteps.indexOf(status)
    },
    updateStatus(order, newStatus) {
      const currentIndex = this.getStepIndex(order.status)
      const newIndex = this.getStepIndex(newStatus)
      
      if (newIndex > currentIndex + 1) {
        this.$message.error(`进度修改失败！当前进度为「${order.status}」，只能直接修改为「${this.progressSteps[currentIndex + 1]}」`)
        this.$nextTick(() => {
          order.status = this.progressSteps[currentIndex]
        })
        return
      }
      
      if (newIndex < currentIndex) {
        this.$message.error('进度不能回退！')
        this.$nextTick(() => {
          order.status = this.progressSteps[currentIndex]
        })
        return
      }
      
      const index = this.orders.findIndex(o => o.id === order.id)
      if (index > -1) {
        localStorage.setItem('woodOrders', JSON.stringify(this.orders))
        this.$message.success(`订单状态已更新为：${order.status}`)
      }
    },
    canSelectStatus(order, status) {
      const currentIndex = this.getStepIndex(order.status)
      const statusIndex = this.getStepIndex(status)
      return statusIndex === currentIndex || statusIndex === currentIndex + 1
    },
    viewDetail(order) {
      this.$router.push(`/detail/${order.id}`)
    },
    deleteOrder(order) {
      this.$confirm('确定要删除该订单吗？删除后无法恢复！', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.orders.findIndex(o => o.id === order.id)
        if (index > -1) {
          this.orders.splice(index, 1)
          localStorage.setItem('woodOrders', JSON.stringify(this.orders))
          this.$message.success('订单已删除')
        }
      }).catch(() => {})
    }
  }
}
</script>

<style scoped>
.order-list-container {
  max-width: 1400px;
  margin: 0 auto;
}

.list-card {
  border-radius: 8px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  font-size: 20px;
  font-weight: bold;
  color: #8B4513;
}

.header-left i {
  margin-right: 10px;
  font-size: 24px;
}

.stats-row {
  margin-bottom: 25px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 15px;
  background: #fff;
  border-radius: 8px;
  border: 1px solid #e8e8e8;
  transition: all 0.3s;
}

.stat-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  transform: translateY(-2px);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin-right: 15px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #999;
}

.progress-wrapper {
  padding: 10px 0;
}

.pagination-wrapper {
  margin-top: 20px;
  text-align: center;
}
</style>
