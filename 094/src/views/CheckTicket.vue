<template>
  <div class="page-container">
    <h2 class="page-title">
      <i class="el-icon-check"></i>
      检票核销
    </h2>
    
    <el-row :gutter="40">
      <el-col :xs="24" :md="12">
        <el-card class="check-card">
          <div slot="header" class="card-header">
            <span>扫码检票</span>
          </div>
          
          <div class="scan-area">
            <div class="qr-placeholder">
              <i class="el-icon-camera"></i>
              <p>扫描门票二维码</p>
            </div>
          </div>
          
          <el-divider content-position="center">或手动输入</el-divider>
          
          <el-form :model="checkForm" :inline="true" class="check-form">
            <el-form-item>
              <el-input 
                v-model="checkForm.ticketCode" 
                placeholder="请输入取票码" 
                maxlength="12"
                clearable
                style="width: 250px;"
              >
                <template slot="prepend">TCK</template>
              </el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleCheck" :loading="checking">检票核销</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :md="12">
        <el-card class="result-card">
          <div slot="header" class="card-header">
            <span>检票结果</span>
          </div>
          
          <div v-if="checkResult" class="result-content">
            <div class="result-status" :class="checkResult.status">
              <i :class="checkResult.icon"></i>
              <h3>{{ checkResult.message }}</h3>
            </div>
            
            <el-descriptions :column="1" border v-if="checkResult.order" class="order-info">
              <el-descriptions-item label="订单号">{{ checkResult.order.id }}</el-descriptions-item>
              <el-descriptions-item label="门票类型">{{ checkResult.order.ticketName }}</el-descriptions-item>
              <el-descriptions-item label="购票数量">{{ checkResult.order.quantity }}张</el-descriptions-item>
              <el-descriptions-item label="游客姓名">{{ checkResult.order.visitorName }}</el-descriptions-item>
              <el-descriptions-item label="入园日期">{{ checkResult.order.visitDate }}</el-descriptions-item>
              <el-descriptions-item label="检票时间">{{ checkResult.checkTime }}</el-descriptions-item>
            </el-descriptions>
            
            <el-button type="primary" class="continue-btn" @click="resetCheck">继续检票</el-button>
          </div>
          
          <div v-else class="empty-result">
            <i class="el-icon-document-checked"></i>
            <p>等待检票...</p>
          </div>
        </el-card>
        
        <el-card class="history-card" style="margin-top: 20px;">
          <div slot="header" class="card-header">
            <span>今日检票记录</span>
            <el-badge :value="checkHistory.length" class="item" style="margin-left: 10px;"></el-badge>
          </div>
          
          <el-table :data="checkHistory.slice(0, 5)" size="small" row-class-name="checked-row">
            <el-table-column prop="ticketCode" label="取票码" width="120" class-name="checked-column">
              <template slot-scope="scope">
                <span class="checked-code">{{ scope.row.ticketCode }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="ticketName" label="门票类型"></el-table-column>
            <el-table-column prop="checkTime" label="检票时间"></el-table-column>
            <el-table-column label="状态" width="80">
              <template slot-scope="scope">
                <el-tag type="danger" size="mini" icon="el-icon-check">已核销</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { orders } from '@/data/mockData'
import { EventBus } from '@/utils/eventBus'

export default {
  name: 'CheckTicket',
  data() {
    return {
      checkForm: {
        ticketCode: ''
      },
      checking: false,
      checkResult: null,
      checkHistory: []
    }
  },
  methods: {
    handleCheck() {
      if (!this.checkForm.ticketCode) {
        this.$message.warning('请输入取票码')
        return
      }
      
      const fullCode = 'TCK' + this.checkForm.ticketCode
      const historyItem = this.checkHistory.find(h => h.ticketCode === fullCode)
      if (historyItem) {
        this.$message.error('该门票已在当前会话核销，禁止重复操作！')
        return
      }
      
      this.checking = true
      
      setTimeout(() => {
        const order = orders.find(o => o.ticketCode === fullCode)
        
        if (order) {
          if (order.status === 'used') {
            this.$message.error({
              message: '该门票已核销使用，禁止重复操作！',
              duration: 3000,
              showClose: true
            })
            this.checkResult = {
              status: 'blocked',
              icon: 'el-icon-circle-close',
              message: '已拦截 - 该门票已核销',
              order: order,
              blocked: true
            }
          } else if (order.status === 'cancelled') {
            this.checkResult = {
              status: 'error',
              icon: 'el-icon-error',
              message: '该订单已取消！',
              order: order
            }
          } else {
            order.status = 'used'
            const now = new Date()
            const checkTime = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')} ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`
            
            this.checkResult = {
              status: 'success',
              icon: 'el-icon-success',
              message: '检票成功！',
              order: order,
              checkTime: checkTime
            }
            
            this.checkHistory.unshift({
              ticketCode: order.ticketCode,
              ticketName: order.ticketName,
              checkTime: checkTime
            })
            
            EventBus.$emit('order-checked', {
              orderId: order.id,
              ticketCode: order.ticketCode
            })
          }
        } else {
          this.checkResult = {
            status: 'error',
            icon: 'el-icon-warning',
            message: '无效的取票码！'
          }
        }
        
        this.checking = false
      }, 1000)
    },
    resetCheck() {
      this.checkForm.ticketCode = ''
      this.checkResult = null
    }
  }
}
</script>

<style scoped>
.card-header {
  font-weight: bold;
  font-size: 16px;
}

.scan-area {
  text-align: center;
  padding: 40px 20px;
}

.qr-placeholder {
  display: inline-block;
  width: 200px;
  height: 200px;
  border: 2px dashed #dcdfe6;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #909399;
  background: #f5f7fa;
}

.qr-placeholder i {
  font-size: 48px;
  margin-bottom: 15px;
}

.qr-placeholder p {
  margin: 0;
  font-size: 14px;
}

.check-form {
  justify-content: center;
  margin: 0;
}

.result-content {
  text-align: center;
}

.result-status {
  padding: 30px 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.result-status.success {
  background: #f0f9eb;
  color: #67c23a;
}

.result-status.error {
  background: #fef0f0;
  color: #f56c6c;
}

.result-status.blocked {
  background: #fff1f0;
  color: #cf1322;
  border: 2px solid #ff4d4f;
  animation: shake 0.5s ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

.result-status i {
  font-size: 64px;
  display: block;
  margin-bottom: 15px;
}

.result-status h3 {
  margin: 0;
  font-size: 24px;
}

.order-info {
  text-align: left;
}

.continue-btn {
  margin-top: 20px;
}

.empty-result {
  text-align: center;
  padding: 60px 20px;
  color: #909399;
}

.empty-result i {
  font-size: 64px;
  margin-bottom: 15px;
  display: block;
}

.empty-result p {
  margin: 0;
  font-size: 16px;
}

.history-card .el-table {
  margin-top: 10px;
}

.checked-row {
  background-color: #fef0f0 !important;
}

.checked-code {
  color: #f56c6c;
  font-weight: bold;
  text-decoration: line-through;
}

.checked-row .el-table__cell {
  color: #909399;
}
</style>
