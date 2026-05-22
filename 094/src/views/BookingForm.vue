<template>
  <div class="page-container">
    <h2 class="page-title">
      <i class="el-icon-document"></i>
      在线预订
    </h2>
    
    <el-row :gutter="40">
      <el-col :xs="24" :md="14">
        <el-form 
          :model="bookingForm" 
          :rules="rules" 
          ref="bookingForm" 
          label-width="100px"
          class="booking-form"
        >
          <el-form-item label="门票类型" prop="ticketId">
            <el-select v-model="bookingForm.ticketId" placeholder="请选择门票类型" style="width: 100%" @change="onTicketChange">
              <el-option 
                v-for="ticket in ticketList" 
                :key="ticket.id" 
                :label="ticket.name + ' - ¥' + ticket.price" 
                :value="ticket.id"
              ></el-option>
            </el-select>
          </el-form-item>
          
          <el-form-item label="购票数量" prop="quantity">
            <el-input-number v-model="bookingForm.quantity" :min="1" :max="10" @change="calculateTotal"></el-input-number>
            <span class="stock-tip" v-if="selectedTicket">库存: {{ selectedTicket.stock }}张</span>
            <span class="daily-limit-tip" v-if="dailyBookedQuantity > 0">
              该日期已购: {{ dailyBookedQuantity }}张 (单日上限: 10张)
            </span>
          </el-form-item>
          
          <el-form-item label="入园日期" prop="visitDate">
            <el-date-picker
              v-model="bookingForm.visitDate"
              type="date"
              placeholder="选择入园日期"
              style="width: 100%"
              :picker-options="pickerOptions"
              @change="onDateChange"
            ></el-date-picker>
          </el-form-item>
          
          <el-form-item label="游客姓名" prop="visitorName">
            <el-input v-model="bookingForm.visitorName" placeholder="请输入真实姓名"></el-input>
          </el-form-item>
          
          <el-form-item label="手机号码" prop="visitorPhone">
            <el-input v-model="bookingForm.visitorPhone" placeholder="请输入手机号码" maxlength="11"></el-input>
          </el-form-item>
          
          <el-form-item label="身份证号" prop="visitorIdCard">
            <el-input v-model="bookingForm.visitorIdCard" placeholder="请输入身份证号码" maxlength="18"></el-input>
          </el-form-item>
          
          <el-form-item label="备注">
            <el-input type="textarea" v-model="bookingForm.remark" :rows="3" placeholder="选填"></el-input>
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="submitForm" size="large">提交订单</el-button>
            <el-button @click="resetForm" size="large">重置</el-button>
          </el-form-item>
        </el-form>
      </el-col>
      
      <el-col :xs="24" :md="10">
        <el-card class="order-summary">
          <div slot="header" class="summary-header">
            <span>订单摘要</span>
          </div>
          
          <div class="summary-content" v-if="selectedTicket">
            <div class="ticket-preview">
              <img :src="selectedTicket.image" :alt="selectedTicket.name">
              <div class="ticket-basic">
                <h4>{{ selectedTicket.name }}</h4>
                <p>{{ selectedTicket.description }}</p>
              </div>
            </div>
            
            <el-divider></el-divider>
            
            <div class="price-detail">
              <div class="price-item">
                <span>门票单价</span>
                <span class="text-right">¥{{ selectedTicket.price }}</span>
              </div>
              <div class="price-item">
                <span>购票数量</span>
                <span class="text-right">× {{ bookingForm.quantity }}</span>
              </div>
              <div class="price-item discount" v-if="selectedTicket.originalPrice > selectedTicket.price">
                <span>优惠减免</span>
                <span class="text-right">- ¥{{ (selectedTicket.originalPrice - selectedTicket.price) * bookingForm.quantity }}</span>
              </div>
            </div>
            
            <el-divider></el-divider>
            
            <div class="total-price">
              <span>应付总额</span>
              <span class="price">¥{{ totalPrice }}</span>
            </div>
            
            <div class="tips">
              <el-alert
                title="温馨提示"
                type="info"
                :closable="false"
                show-icon
              >
                <p>1. 请在预订后30分钟内完成支付</p>
                <p>2. 凭身份证或取票码入园</p>
                <p>3. 如需退票请提前一天申请</p>
              </el-alert>
            </div>
          </div>
          
          <div v-else class="empty-tip">
            <i class="el-icon-tickets"></i>
            <p>请选择门票类型</p>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ticketTypes, orders } from '@/data/mockData'

export default {
  name: 'BookingForm',
  data() {
    const validatePhone = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入手机号码'))
      } else if (!/^1[3-9]\d{9}$/.test(value)) {
        callback(new Error('请输入正确的手机号码'))
      } else {
        callback()
      }
    }
    
    const validateIdCard = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入身份证号码'))
      } else if (!/^\d{17}[\dXx]$/.test(value)) {
        callback(new Error('请输入正确的身份证号码'))
      } else {
        callback()
      }
    }
    
    return {
      ticketList: ticketTypes,
      bookingForm: {
        ticketId: '',
        quantity: 1,
        visitDate: '',
        visitorName: '',
        visitorPhone: '',
        visitorIdCard: '',
        remark: ''
      },
      rules: {
        ticketId: [
          { required: true, message: '请选择门票类型', trigger: 'change' }
        ],
        quantity: [
          { required: true, message: '请选择购票数量', trigger: 'change' }
        ],
        visitDate: [
          { required: true, message: '请选择入园日期', trigger: 'change' }
        ],
        visitorName: [
          { required: true, message: '请输入游客姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        visitorPhone: [
          { validator: validatePhone, trigger: 'blur' }
        ],
        visitorIdCard: [
          { validator: validateIdCard, trigger: 'blur' }
        ]
      },
      pickerOptions: {
        disabledDate(time) {
          return time.getTime() < Date.now() - 8.64e7
        }
      },
      totalPrice: 0,
      dailyBookedQuantity: 0,
      DAILY_LIMIT: 10
    }
  },
  computed: {
    selectedTicket() {
      return this.ticketList.find(t => t.id === this.bookingForm.ticketId)
    }
  },
  mounted() {
    const ticketId = this.$route.params.ticketId
    if (ticketId) {
      this.bookingForm.ticketId = parseInt(ticketId)
      this.calculateTotal()
    }
  },
  methods: {
    onTicketChange() {
      this.calculateTotal()
      this.calculateDailyBooked()
    },
    onDateChange() {
      this.calculateDailyBooked()
    },
    calculateDailyBooked() {
      if (!this.bookingForm.visitDate || !this.bookingForm.ticketId) {
        this.dailyBookedQuantity = 0
        return
      }
      
      const dateStr = this.formatDate(this.bookingForm.visitDate)
      const bookedQuantity = orders.reduce((sum, order) => {
        if (order.visitDate === dateStr && order.ticketId === this.bookingForm.ticketId && order.status !== 'cancelled') {
          return sum + order.quantity
        }
        return sum
      }, 0)
      
      this.dailyBookedQuantity = bookedQuantity
    },
    formatDate(date) {
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    },
    calculateTotal() {
      if (this.selectedTicket) {
        this.totalPrice = this.selectedTicket.price * this.bookingForm.quantity
      }
    },
    submitForm() {
      this.$refs.bookingForm.validate((valid) => {
        if (valid) {
          if (this.selectedTicket && this.bookingForm.quantity > this.selectedTicket.stock) {
            this.$message.error('库存不足')
            return
          }
          
          const totalQuantity = this.dailyBookedQuantity + this.bookingForm.quantity
          if (totalQuantity > this.DAILY_LIMIT) {
            this.$message.error(`单日购票数量已达上限！该日期已购${this.dailyBookedQuantity}张，最多还可购买${this.DAILY_LIMIT - this.dailyBookedQuantity}张`)
            return
          }
          
          this.$message.success('订单提交成功！')
          setTimeout(() => {
            this.$router.push('/orders')
          }, 1000)
        } else {
          this.$message.error('请检查表单信息')
          return false
        }
      })
    },
    resetForm() {
      this.$refs.bookingForm.resetFields()
      this.totalPrice = 0
    }
  }
}
</script>

<style scoped>
.booking-form {
  padding: 20px 0;
}

.stock-tip {
  margin-left: 15px;
  color: #909399;
  font-size: 14px;
}

.daily-limit-tip {
  margin-left: 15px;
  color: #e6a23c;
  font-size: 14px;
}

.order-summary {
  position: sticky;
  top: 20px;
}

.summary-header {
  font-weight: bold;
  font-size: 16px;
}

.ticket-preview {
  display: flex;
  gap: 15px;
}

.ticket-preview img {
  width: 100px;
  height: 75px;
  object-fit: cover;
  border-radius: 4px;
}

.ticket-basic h4 {
  font-size: 16px;
  color: #303133;
  margin-bottom: 5px;
}

.ticket-basic p {
  font-size: 12px;
  color: #606266;
  line-height: 1.4;
}

.price-detail {
  padding: 10px 0;
}

.price-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 14px;
  color: #606266;
}

.price-item.discount span:last-child {
  color: #67c23a;
}

.total-price {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
}

.total-price .price {
  font-size: 28px;
  color: #f56c6c;
}

.tips {
  margin-top: 20px;
}

.tips p {
  font-size: 12px;
  line-height: 1.8;
  margin: 0;
}

.empty-tip {
  text-align: center;
  padding: 60px 20px;
  color: #909399;
}

.empty-tip i {
  font-size: 48px;
  margin-bottom: 15px;
  display: block;
}
</style>
