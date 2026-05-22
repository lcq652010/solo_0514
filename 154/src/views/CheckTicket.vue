<template>
  <div class="check-ticket-page">
    <div class="page-header">
      <h1 class="page-title">检票核销</h1>
      <p class="page-subtitle">验证并核销游客门票</p>
    </div>

    <div class="check-content">
      <el-card class="check-card">
        <div slot="header" class="card-header">
          <span>门票验证</span>
        </div>
        <div class="check-form">
          <el-form :model="checkForm" label-width="100px">
            <el-form-item label="取票码">
              <el-input
                v-model="checkForm.ticketCode"
                placeholder="请输入取票码"
                size="large"
                clearable
                maxlength="14"
                @keyup.enter.native="checkTicket"
                style="width: 300px"
              >
                <template slot="append">
                  <el-button type="primary" @click="checkTicket" :loading="checking">
                    验证
                  </el-button>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item label="或扫描二维码">
              <div class="qr-placeholder">
                <i class="el-icon-picture-outline"></i>
                <p>二维码扫描功能</p>
                <span class="tip">请对准二维码进行扫描</span>
              </div>
            </el-form-item>
          </el-form>
        </div>
      </el-card>

      <el-card class="result-card" v-if="ticketInfo">
        <div slot="header" class="card-header">
          <span>门票信息</span>
          <el-tag
            :type="ticketInfo.status === 'paid' ? 'success' : ticketInfo.status === 'used' ? 'info' : 'danger'"
            size="small"
          >
            {{ ticketInfo.status === 'paid' ? '可使用' : ticketInfo.status === 'used' ? '已使用' : '已失效' }}
          </el-tag>
        </div>
        <div class="ticket-detail">
          <div class="detail-row">
            <span class="label">订单编号：</span>
            <span class="value">{{ ticketInfo.id }}</span>
          </div>
          <div class="detail-row">
            <span class="label">门票类型：</span>
            <span class="value">{{ ticketInfo.ticketName }}</span>
          </div>
          <div class="detail-row">
            <span class="label">购买数量：</span>
            <span class="value">{{ ticketInfo.quantity }}张</span>
          </div>
          <div class="detail-row">
            <span class="label">游客姓名：</span>
            <span class="value">{{ ticketInfo.visitorName }}</span>
          </div>
          <div class="detail-row">
            <span class="label">手机号码：</span>
            <span class="value">{{ ticketInfo.visitorPhone }}</span>
          </div>
          <div class="detail-row">
            <span class="label">出游日期：</span>
            <span class="value">{{ ticketInfo.visitDate }}</span>
          </div>
          <div class="detail-row">
            <span class="label">取票码：</span>
            <span class="value code">{{ ticketInfo.ticketCode }}</span>
          </div>
          <div class="detail-row">
            <span class="label">购票时间：</span>
            <span class="value">{{ ticketInfo.createTime }}</span>
          </div>
          <div class="detail-row" v-if="ticketInfo.useTime">
            <span class="label">使用时间：</span>
            <span class="value">{{ ticketInfo.useTime }}</span>
          </div>
        </div>
        <div class="action-buttons" v-if="ticketInfo.status === 'paid'">
          <el-button type="primary" size="large" @click="confirmUse" :loading="using">
            <i class="el-icon-check"></i>
            确认核销
          </el-button>
        </div>
        <div class="used-badge" v-else-if="ticketInfo.status === 'used'">
          <i class="el-icon-success"></i>
          <span>该门票已核销</span>
        </div>
      </el-card>

      <el-card class="history-card">
        <div slot="header" class="card-header">
          <span>今日核销记录</span>
          <el-badge :value="todayCheckCount" class="item" />
        </div>
        <el-table
          :data="todayCheckList"
          border
          stripe
          style="width: 100%"
        >
          <el-table-column prop="id" label="订单编号" width="180" />
          <el-table-column prop="ticketName" label="门票类型" width="120" />
          <el-table-column prop="visitorName" label="游客姓名" width="100" />
          <el-table-column prop="ticketCode" label="取票码" width="130" align="center">
            <template slot-scope="scope">
              <span class="ticket-code">{{ scope.row.ticketCode }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="useTime" label="核销时间" width="160" />
          <el-table-column prop="quantity" label="数量" width="80" align="center" />
        </el-table>
      </el-card>
    </div>
  </div>
</template>

<script>
import { orders, formatDateTime, checkTicketUsed } from '@/mock/data';

export default {
  name: 'CheckTicket',
  data() {
    return {
      checkForm: {
        ticketCode: ''
      },
      checking: false,
      using: false,
      ticketInfo: null
    };
  },
  computed: {
    todayCheckList() {
      const today = formatDateTime(new Date()).split(' ')[0];
      const allOrders = this.getAllOrders();
      return allOrders.filter(order =>
        order.status === 'used' && order.useTime && order.useTime.startsWith(today)
      );
    },
    todayCheckCount() {
      return this.todayCheckList.length;
    }
  },
  methods: {
    getAllOrders() {
      const localOrders = JSON.parse(localStorage.getItem('orders') || '[]');
      return [...localOrders, ...orders];
    },
    checkTicket() {
      if (!this.checkForm.ticketCode.trim()) {
        this.$message.warning('请输入取票码');
        return;
      }

      this.checking = true;
      setTimeout(() => {
        const ticketCode = this.checkForm.ticketCode.trim().toUpperCase();
        const ticketStatus = checkTicketUsed(ticketCode);

        if (!ticketStatus.exists) {
          this.ticketInfo = null;
          this.$message.error('未找到该取票码对应的订单');
          this.checking = false;
          return;
        }

        if (ticketStatus.used) {
          this.ticketInfo = { ...ticketStatus.order };
          this.$message({
            type: 'warning',
            message: `该门票已于 ${ticketStatus.order.useTime} 核销，请勿重复核销！`,
            duration: 4000
          });
        } else {
          this.ticketInfo = { ...ticketStatus.order };
          this.$message.success('验证成功，请确认核销');
        }

        this.checking = false;
      }, 800);
    },
    confirmUse() {
      const ticketCode = this.ticketInfo.ticketCode;
      const ticketStatus = checkTicketUsed(ticketCode);
      
      if (ticketStatus.used) {
        this.ticketInfo = { ...ticketStatus.order };
        this.$message.error('该门票已核销，请勿重复核销！');
        return;
      }

      this.$confirm('确认核销该门票吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'success'
      }).then(() => {
        this.using = true;
        setTimeout(() => {
          const latestStatus = checkTicketUsed(ticketCode);
          if (latestStatus.used) {
            this.ticketInfo = { ...latestStatus.order };
            this.using = false;
            this.$message.error('该门票已核销，请勿重复核销！');
            return;
          }

          this.ticketInfo.status = 'used';
          this.ticketInfo.useTime = formatDateTime(new Date());
          this.updateOrderStatus();

          this.using = false;
          this.$message({
            type: 'success',
            message: '核销成功！'
          });
        }, 1000);
      }).catch(() => {});
    },
    updateOrderStatus() {
      let localOrders = JSON.parse(localStorage.getItem('orders') || '[]');
      const index = localOrders.findIndex(o => o.id === this.ticketInfo.id);

      if (index > -1) {
        localOrders[index] = { ...this.ticketInfo };
      } else {
        localOrders.push({ ...this.ticketInfo });
      }

      localStorage.setItem('orders', JSON.stringify(localOrders));
    }
  }
};
</script>

<style scoped>
.check-ticket-page {
  padding: 0;
}

.check-content {
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 24px;
}

.card-header {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.check-form {
  padding: 20px 0;
}

.qr-placeholder {
  width: 300px;
  height: 200px;
  border: 2px dashed #DCDFE6;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #FAFAFA;
}

.qr-placeholder i {
  font-size: 48px;
  color: #C0C4CC;
  margin-bottom: 10px;
}

.qr-placeholder p {
  margin: 0 0 5px 0;
  color: #909399;
  font-size: 14px;
}

.qr-placeholder .tip {
  font-size: 12px;
  color: #C0C4CC;
}

.ticket-detail {
  padding: 10px 0;
}

.detail-row {
  display: flex;
  padding: 10px 0;
  border-bottom: 1px solid #F5F7FA;
}

.detail-row:last-child {
  border-bottom: none;
}

.label {
  width: 100px;
  color: #909399;
  flex-shrink: 0;
}

.value {
  color: #303133;
  flex: 1;
}

.value.code {
  color: #409EFF;
  font-family: monospace;
  font-weight: 600;
  font-size: 16px;
}

.action-buttons {
  padding: 20px 0 0;
  text-align: center;
  border-top: 1px solid #EBEEF5;
  margin-top: 10px;
}

.used-badge {
  padding: 30px 0 10px;
  text-align: center;
  border-top: 1px solid #EBEEF5;
  margin-top: 10px;
  color: #67C23A;
  font-size: 16px;
  font-weight: 600;
}

.used-badge i {
  font-size: 24px;
  margin-right: 8px;
  vertical-align: middle;
}

.history-card {
  grid-column: 1 / -1;
}

.ticket-code {
  color: #409EFF;
  font-family: monospace;
  font-weight: 600;
}

@media (max-width: 900px) {
  .check-content {
    grid-template-columns: 1fr;
  }
}
</style>
