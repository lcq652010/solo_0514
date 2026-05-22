<template>
  <div class="order-detail-container">
    <el-card class="detail-card" shadow="hover" v-loading="loading">
      <div slot="header" class="card-header">
        <div class="header-left">
          <i class="el-icon-document"></i>
          <span>订单详情</span>
        </div>
        <div class="header-right">
          <el-button type="primary" size="small" @click="goBack">
            <i class="el-icon-back"></i> 返回
          </el-button>
        </div>
      </div>

      <div v-if="order">
        <div class="order-status-bar">
          <div class="order-id">
            <span class="label">订单编号：</span>
            <span class="value">WD{{ order.id }}</span>
          </div>
          <el-tag :type="getOrderStatusType(order.status)" size="medium">
            当前状态：{{ order.status }}
          </el-tag>
        </div>

        <el-steps :active="getStepIndex(order.status)" size="small" finish-status="success" class="progress-steps">
          <el-step v-for="step in progressSteps" :key="step" :title="step"></el-step>
        </el-steps>

        <el-divider></el-divider>

        <el-row :gutter="40">
          <el-col :span="12">
            <div class="section-title">
              <i class="el-icon-user"></i> 客户信息
            </div>
            <el-descriptions :column="1" border>
              <el-descriptions-item label="客户姓名">
                {{ order.customerName }}
              </el-descriptions-item>
              <el-descriptions-item label="联系电话">
                {{ order.phone }}
              </el-descriptions-item>
              <el-descriptions-item label="下单时间">
                {{ order.createTime }}
              </el-descriptions-item>
            </el-descriptions>
          </el-col>
          <el-col :span="12">
            <div class="section-title">
              <i class="el-icon-goods"></i> 产品规格
            </div>
            <el-descriptions :column="1" border>
              <el-descriptions-item label="木料类型">
                <el-tag type="warning" size="small">{{ order.woodType }}</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="尺寸规格">
                {{ order.length }}mm × {{ order.width }}mm × {{ order.thickness }}mm
              </el-descriptions-item>
              <el-descriptions-item label="雕刻图案">
                <el-tag type="info" size="small">{{ order.pattern }}</el-tag>
              </el-descriptions-item>
            </el-descriptions>
          </el-col>
        </el-row>

        <el-divider></el-divider>

        <el-row :gutter="40">
          <el-col :span="12">
            <div class="section-title">
              <i class="el-icon-edit"></i> 刻字信息
            </div>
            <el-descriptions :column="1" border>
              <el-descriptions-item label="刻字内容">
                <span v-if="order.engravingText">{{ order.engravingText }}</span>
                <span v-else style="color: #999;">无</span>
              </el-descriptions-item>
              <el-descriptions-item label="字体样式">
                <span v-if="order.fontStyle">{{ order.fontStyle }}</span>
                <span v-else style="color: #999;">无</span>
              </el-descriptions-item>
              <el-descriptions-item label="刻字位置">
                <span v-if="order.engravingPosition">{{ order.engravingPosition }}</span>
                <span v-else style="color: #999;">无</span>
              </el-descriptions-item>
            </el-descriptions>
          </el-col>
          <el-col :span="12">
            <div class="section-title">
              <i class="el-icon-set-up"></i> 附加工艺
            </div>
            <el-descriptions :column="1" border>
              <el-descriptions-item label="工艺选择">
                <div v-if="order.additionalProcess && order.additionalProcess.length > 0">
                  <el-tag v-for="process in order.additionalProcess" :key="process" size="small" style="margin-right: 5px;">
                    {{ process }}
                  </el-tag>
                </div>
                <span v-else style="color: #999;">无</span>
              </el-descriptions-item>
            </el-descriptions>
          </el-col>
        </el-row>

        <el-divider></el-divider>

        <div class="price-section">
          <div class="section-title">
            <i class="el-icon-wallet"></i> 费用明细
          </div>
          <div class="price-details">
            <el-row :gutter="20">
              <el-col :span="8">
                <div class="price-item">
                  <span class="price-label">木料基础价</span>
                  <span class="price-value">¥{{ getWoodPrice(order.woodType) }}</span>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="price-item">
                  <span class="price-label">刻字费用</span>
                  <span class="price-value">¥{{ getEngravingPrice(order.engravingText) }}</span>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="price-item">
                  <span class="price-label">附加工艺费</span>
                  <span class="price-value">¥{{ getAdditionalPrice(order.additionalProcess) }}</span>
                </div>
              </el-col>
            </el-row>
            <div class="total-price">
              <span class="total-label">订单总价</span>
              <span class="total-value">¥{{ order.totalPrice }}</span>
            </div>
          </div>
        </div>

        <el-divider></el-divider>

        <div class="action-section">
          <el-button type="primary" size="large" @click="printOrder">
            <i class="el-icon-printer"></i> 打印订单
          </el-button>
          <el-button type="success" size="large" @click="updateStatusDialogVisible = true">
            <i class="el-icon-edit"></i> 更新进度
          </el-button>
          <el-button type="danger" size="large" @click="goBack">
            <i class="el-icon-back"></i> 返回列表
          </el-button>
        </div>
      </div>

      <div v-else class="empty-state">
        <i class="el-icon-document-delete"></i>
        <p>订单不存在或已被删除</p>
        <el-button type="primary" @click="goBack">返回订单列表</el-button>
      </div>
    </el-card>

    <el-dialog
      title="更新制作进度"
      :visible.sync="updateStatusDialogVisible"
      width="400px"
      @close="updateStatusDialogVisible = false">
      <el-select v-model="newStatus" style="width: 100%;">
        <el-option 
          v-for="step in progressSteps" 
          :key="step" 
          :label="step" 
          :value="step"
          :disabled="!canSelectStatus(step)">
        </el-option>
      </el-select>
      <span slot="footer" class="dialog-footer">
        <el-button @click="updateStatusDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="confirmUpdateStatus">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'OrderDetail',
  data() {
    return {
      loading: false,
      order: null,
      updateStatusDialogVisible: false,
      newStatus: '',
      progressSteps: ['选料', '开料', '雕刻', '打磨', '烫金', '上油', '完工'],
      woodOptions: [
        { value: '紫檀', price: 128 },
        { value: '黄花梨', price: 168 },
        { value: '酸枝', price: 98 },
        { value: '檀木', price: 88 }
      ]
    }
  },
  mounted() {
    this.loadOrderDetail()
  },
  methods: {
    loadOrderDetail() {
      this.loading = true
      const orderId = parseInt(this.$route.params.id)
      setTimeout(() => {
        const orders = JSON.parse(localStorage.getItem('woodOrders') || '[]')
        this.order = orders.find(o => o.id === orderId)
        if (this.order) {
          this.newStatus = this.order.status
        }
        this.loading = false
      }, 300)
    },
    getStepIndex(status) {
      return this.progressSteps.indexOf(status)
    },
    getOrderStatusType(status) {
      if (status === '完工') return 'success'
      if (status === '选料') return 'info'
      return 'warning'
    },
    getWoodPrice(woodType) {
      const wood = this.woodOptions.find(w => w.value === woodType)
      return wood ? wood.price : 0
    },
    getEngravingPrice(text) {
      if (!text) return 0
      return text.length * 2
    },
    getAdditionalPrice(processes) {
      if (!processes || processes.length === 0) return 0
      let price = 0
      if (processes.includes('烫金')) price += 30
      if (processes.includes('上油')) price += 20
      if (processes.includes('挂绳')) price += 10
      if (processes.includes('礼盒')) price += 50
      return price
    },
    goBack() {
      this.$router.push('/admin')
    },
    printOrder() {
      this.$message.success('打印功能待开发')
    },
    canSelectStatus(status) {
      if (!this.order) return false
      const currentIndex = this.getStepIndex(this.order.status)
      const statusIndex = this.getStepIndex(status)
      return statusIndex === currentIndex || statusIndex === currentIndex + 1
    },
    confirmUpdateStatus() {
      if (this.order && this.newStatus) {
        const currentIndex = this.getStepIndex(this.order.status)
        const newIndex = this.getStepIndex(this.newStatus)
        
        if (newIndex > currentIndex + 1) {
          this.$message.error(`进度修改失败！当前进度为「${this.order.status}」，只能直接修改为「${this.progressSteps[currentIndex + 1]}」`)
          return
        }
        
        if (newIndex < currentIndex) {
          this.$message.error('进度不能回退！')
          return
        }
        
        const orders = JSON.parse(localStorage.getItem('woodOrders') || '[]')
        const index = orders.findIndex(o => o.id === this.order.id)
        if (index > -1) {
          orders[index].status = this.newStatus
          localStorage.setItem('woodOrders', JSON.stringify(orders))
          this.order.status = this.newStatus
          this.updateStatusDialogVisible = false
          this.$message.success(`订单状态已更新为：${this.newStatus}`)
        }
      }
    }
  }
}
</script>

<style scoped>
.order-detail-container {
  max-width: 1200px;
  margin: 0 auto;
}

.detail-card {
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

.order-status-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: linear-gradient(135deg, #fff8f0 0%, #fff 100%);
  border-radius: 8px;
  margin-bottom: 20px;
}

.order-id .label {
  color: #666;
  margin-right: 10px;
}

.order-id .value {
  font-size: 18px;
  font-weight: bold;
  color: #8B4513;
}

.progress-steps {
  margin: 20px 0;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  color: #8B4513;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
}

.section-title i {
  margin-right: 8px;
}

.price-section {
  margin-top: 20px 0;
}

.price-details {
  background: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
}

.price-item {
  text-align: center;
  padding: 15px;
  background: white;
  border-radius: 8px;
}

.price-label {
  display: block;
  color: #666;
  font-size: 14px;
  margin-bottom: 8px;
}

.price-value {
  display: block;
  font-size: 20px;
  font-weight: bold;
  color: #8B4513;
}

.total-price {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 2px dashed #e8d5c4;
  text-align: center;
}

.total-label {
  font-size: 16px;
  color: #333;
  margin-right: 20px;
}

.total-value {
  font-size: 32px;
  font-weight: bold;
  color: #ff6600;
}

.action-section {
  text-align: center;
  padding: 20px 0;
}

.action-section .el-button {
  margin: 0 10px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-state i {
  font-size: 80px;
  color: #d9d9d9;
  display: block;
  margin-bottom: 20px;
}

.empty-state p {
  font-size: 16px;
  color: #999;
  margin-bottom: 20px;
}
</style>
