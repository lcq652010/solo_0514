<template>
  <div class="booking-form-page">
    <div class="page-header">
      <h1 class="page-title">在线预订</h1>
      <p class="page-subtitle">填写预订信息，完成门票购买</p>
    </div>

    <div class="booking-content">
      <el-card class="ticket-info-card" v-if="selectedTicket">
        <div slot="header" class="card-header">
          <span>门票信息</span>
        </div>
        <div class="ticket-info-content">
          <img :src="selectedTicket.image" class="ticket-thumb" />
          <div class="ticket-details">
            <h3>{{ selectedTicket.name }}</h3>
            <p>{{ selectedTicket.description }}</p>
            <div class="price-info">
              <span class="current-price">¥{{ selectedTicket.price }}</span>
              <span class="original-price">¥{{ selectedTicket.originalPrice }}</span>
            </div>
          </div>
        </div>
      </el-card>

      <el-card class="form-card">
        <div slot="header" class="card-header">
          <span>预订信息</span>
        </div>
        <el-form
          ref="bookingForm"
          :model="formData"
          :rules="rules"
          label-width="100px"
          class="booking-form"
        >
          <el-form-item label="门票类型" prop="ticketId">
            <el-select
              v-model="formData.ticketId"
              placeholder="请选择门票类型"
              style="width: 100%"
              @change="onTicketChange"
            >
              <el-option
                v-for="ticket in ticketTypes"
                :key="ticket.id"
                :label="ticket.name + ' - ¥' + ticket.price"
                :value="ticket.id"
              >
                <span style="float: left">{{ ticket.name }}</span>
                <span style="float: right; color: #F56C6C; font-weight: 600">
                  ¥{{ ticket.price }}
                </span>
              </el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="出游日期" prop="visitDate">
            <el-date-picker
              v-model="formData.visitDate"
              type="date"
              placeholder="选择出游日期"
              style="width: 100%"
              :picker-options="datePickerOptions"
              value-format="yyyy-MM-dd"
            />
          </el-form-item>

          <el-form-item label="购买数量" prop="quantity">
            <el-input-number
              v-model="formData.quantity"
              :min="1"
              :max="maxQuantity"
              style="width: 100%"
              @change="onQuantityChange"
            />
            <span class="limit-tip" v-if="selectedTicket">
              限购{{ selectedTicket.maxPurchase }}张，当日剩余{{ dailyRemaining }}张
            </span>
            <el-alert
              v-if="dailyLimitExceeded"
              title="当日门票已达销售上限"
              type="warning"
              size="small"
              show-icon
              :closable="false"
              style="margin-top: 10px"
            >
              <span slot="description">
                {{ selectedTicket?.name }} {{ formData.visitDate }} 当日已售{{ dailySales }}张，剩余{{ dailyRemaining }}张
              </span>
            </el-alert>
          </el-form-item>

          <el-form-item label="游客姓名" prop="visitorName">
            <el-input
              v-model="formData.visitorName"
              placeholder="请输入真实姓名"
              clearable
            />
          </el-form-item>

          <el-form-item label="手机号码" prop="visitorPhone">
            <el-input
              v-model="formData.visitorPhone"
              placeholder="请输入手机号码"
              clearable
              maxlength="11"
            />
          </el-form-item>

          <el-form-item label="身份证号" prop="idCard">
            <el-input
              v-model="formData.idCard"
              placeholder="请输入身份证号码"
              clearable
              maxlength="18"
            />
          </el-form-item>

          <el-form-item label="备注">
            <el-input
              v-model="formData.remark"
              type="textarea"
              :rows="3"
              placeholder="选填，可填写特殊需求"
            />
          </el-form-item>

          <el-divider />

          <div class="price-summary">
            <div class="summary-row">
              <span>门票单价：</span>
              <span>¥{{ selectedTicket ? selectedTicket.price : 0 }}</span>
            </div>
            <div class="summary-row">
              <span>购买数量：</span>
              <span>× {{ formData.quantity }}</span>
            </div>
            <div class="summary-row total">
              <span>应付金额：</span>
              <span class="total-price">¥{{ totalPrice }}</span>
            </div>
          </div>

          <el-form-item class="form-actions">
            <el-button type="primary" size="large" @click="submitForm" :loading="submitting">
              提交订单
            </el-button>
            <el-button size="large" @click="resetForm">
              重置
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ticketTypes, generateOrderId, generateTicketCode, formatDateTime, checkDailyLimit } from '@/mock/data';

export default {
  name: 'BookingForm',
  data() {
    return {
      ticketTypes,
      formData: {
        ticketId: '',
        visitDate: '',
        quantity: 1,
        visitorName: '',
        visitorPhone: '',
        idCard: '',
        remark: ''
      },
      rules: {
        ticketId: [
          { required: true, message: '请选择门票类型', trigger: 'change' }
        ],
        visitDate: [
          { required: true, message: '请选择出游日期', trigger: 'change' }
        ],
        quantity: [
          { required: true, message: '请输入购买数量', trigger: 'blur' }
        ],
        visitorName: [
          { required: true, message: '请输入游客姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '姓名长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        visitorPhone: [
          { required: true, message: '请输入手机号码', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ],
        idCard: [
          { required: true, message: '请输入身份证号', trigger: 'blur' },
          { pattern: /(^\d{18}$)|(^\d{17}(\d|X|x)$)/, message: '请输入正确的身份证号码', trigger: 'blur' }
        ]
      },
      submitting: false,
      totalPrice: 0,
      dailySales: 0,
      dailyRemaining: 0,
      dailyLimit: 0,
      dailyLimitExceeded: false
    };
  },
  computed: {
    selectedTicket() {
      return this.ticketTypes.find(t => t.id === this.formData.ticketId);
    },
    maxQuantity() {
      if (!this.selectedTicket) return 10;
      const perOrderLimit = this.selectedTicket.maxPurchase;
      const dailyRemaining = this.dailyRemaining > 0 ? this.dailyRemaining : 1;
      return Math.min(perOrderLimit, dailyRemaining);
    },
    datePickerOptions() {
      return {
        disabledDate(time) {
          return time.getTime() < Date.now() - 8.64e7;
        }
      };
    }
  },
  watch: {
    'formData.ticketId'() {
      this.checkDailyLimit();
    },
    'formData.visitDate'() {
      this.checkDailyLimit();
    }
  },
  mounted() {
    const ticketId = this.$route.params.ticketId;
    if (ticketId) {
      this.formData.ticketId = parseInt(ticketId);
      this.calculateTotal();
    }
  },
  methods: {
    onTicketChange() {
      this.formData.quantity = 1;
      this.checkDailyLimit();
      this.calculateTotal();
    },
    onQuantityChange() {
      this.checkDailyLimit();
      this.calculateTotal();
    },
    checkDailyLimit() {
      if (!this.formData.ticketId || !this.formData.visitDate) {
        this.dailyLimitExceeded = false;
        this.dailyRemaining = 0;
        this.dailySales = 0;
        this.dailyLimit = 0;
        return;
      }
      
      const result = checkDailyLimit(
        this.formData.ticketId, 
        this.formData.visitDate, 
        this.formData.quantity
      );
      
      this.dailySales = result.current;
      this.dailyRemaining = result.remaining;
      this.dailyLimit = result.limit;
      this.dailyLimitExceeded = result.exceeded;
    },
    calculateTotal() {
      if (this.selectedTicket) {
        this.totalPrice = this.selectedTicket.price * this.formData.quantity;
      }
    },
    submitForm() {
      this.$refs.bookingForm.validate(valid => {
        if (valid) {
          this.checkDailyLimit();
          
          if (this.dailyLimitExceeded) {
            this.$message.error(`当日门票已达销售上限！${this.selectedTicket.name} 剩余${this.dailyRemaining}张`);
            return false;
          }
          
          this.submitting = true;
          setTimeout(() => {
            const newOrder = {
              id: generateOrderId(),
              ticketName: this.selectedTicket.name,
              quantity: this.formData.quantity,
              totalPrice: this.totalPrice,
              visitorName: this.formData.visitorName,
              visitorPhone: this.formData.visitorPhone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2'),
              visitDate: this.formData.visitDate,
              status: 'paid',
              createTime: formatDateTime(new Date()),
              ticketCode: generateTicketCode(this.formData.visitDate)
            };

            let orders = JSON.parse(localStorage.getItem('orders') || '[]');
            orders.unshift(newOrder);
            localStorage.setItem('orders', JSON.stringify(orders));

            this.submitting = false;
            this.$message({
              type: 'success',
              message: '订单提交成功！',
              duration: 2000
            });

            setTimeout(() => {
              this.$router.push('/orders');
            }, 1000);
          }, 1500);
        } else {
          this.$message.error('请检查并完善预订信息');
          return false;
        }
      });
    },
    resetForm() {
      this.$refs.bookingForm.resetFields();
      this.totalPrice = 0;
      this.dailyLimitExceeded = false;
      this.dailyRemaining = 0;
      this.dailySales = 0;
      this.dailyLimit = 0;
    }
  }
};
</script>

<style scoped>
.booking-form-page {
  padding: 0;
}

.booking-content {
  display: grid;
  grid-template-columns: 350px 1fr;
  gap: 24px;
}

.card-header {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.ticket-info-content {
  display: flex;
  gap: 16px;
}

.ticket-thumb {
  width: 120px;
  height: 90px;
  object-fit: cover;
  border-radius: 8px;
}

.ticket-details h3 {
  margin: 0 0 8px 0;
  font-size: 18px;
  color: #303133;
}

.ticket-details p {
  margin: 0 0 10px 0;
  font-size: 13px;
  color: #606266;
  line-height: 1.5;
}

.price-info {
  display: flex;
  align-items: baseline;
  gap: 10px;
}

.current-price {
  font-size: 24px;
  font-weight: 700;
  color: #F56C6C;
}

.original-price {
  font-size: 14px;
  color: #C0C4CC;
  text-decoration: line-through;
}

.booking-form {
  max-width: 600px;
}

.limit-tip {
  margin-left: 12px;
  font-size: 12px;
  color: #909399;
}

.price-summary {
  background: #F5F7FA;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  font-size: 14px;
  color: #606266;
}

.summary-row.total {
  border-top: 1px solid #E4E7ED;
  margin-top: 8px;
  padding-top: 16px;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.total-price {
  font-size: 28px;
  color: #F56C6C;
}

.form-actions {
  text-align: center;
  margin-bottom: 0;
}

.form-actions /deep/ .el-form-item__content {
  margin-left: 0 !important;
}

@media (max-width: 900px) {
  .booking-content {
    grid-template-columns: 1fr;
  }
}
</style>
