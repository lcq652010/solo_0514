<template>
  <div class="check-in">
    <div class="page-header">
      <h1 class="page-title">入住登记</h1>
    </div>
    
    <el-card class="mb-20">
      <el-form :inline="true" :model="searchForm" class="demo-form-inline">
        <el-form-item label="订单号">
          <el-input v-model="searchForm.orderId" placeholder="请输入订单号" clearable></el-input>
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="searchForm.phone" placeholder="请输入手机号" clearable></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="searchOrder">查询</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-card v-if="orderInfo" class="mb-20">
      <div slot="header" class="card-header">
        <span>订单信息</span>
        <el-tag :type="orderStatusMap[orderInfo.status].type">
          {{ orderStatusMap[orderInfo.status].label }}
        </el-tag>
      </div>
      
      <el-descriptions :column="2" border>
        <el-descriptions-item label="订单号">{{ orderInfo.id }}</el-descriptions-item>
        <el-descriptions-item label="下单时间">{{ orderInfo.createTime }}</el-descriptions-item>
        <el-descriptions-item label="客人姓名">{{ orderInfo.guestName }}</el-descriptions-item>
        <el-descriptions-item label="手机号">{{ orderInfo.phone }}</el-descriptions-item>
        <el-descriptions-item label="身份证号">{{ orderInfo.idCard }}</el-descriptions-item>
        <el-descriptions-item label="房型">{{ orderInfo.roomType }}</el-descriptions-item>
        <el-descriptions-item label="房间号">{{ orderInfo.roomNumber }}</el-descriptions-item>
        <el-descriptions-item label="入住天数">{{ orderInfo.days }} 天</el-descriptions-item>
        <el-descriptions-item label="入住日期">{{ orderInfo.checkInDate }}</el-descriptions-item>
        <el-descriptions-item label="退房日期">{{ orderInfo.checkOutDate }}</el-descriptions-item>
        <el-descriptions-item label="订单金额" :span="2">
          <span style="font-size: 24px; color: #f56c6c; font-weight: bold;">¥{{ orderInfo.totalPrice }}</span>
        </el-descriptions-item>
      </el-descriptions>
      
      <div class="action-buttons mt-20" v-if="orderInfo.status === 'confirmed'">
        <el-button type="primary" size="large" @click="checkIn" :loading="loading">
          <i class="el-icon-s-check"></i> 确认入住
        </el-button>
      </div>
      <div class="action-buttons mt-20" v-else-if="orderInfo.status === 'checked_in'">
        <el-button type="success" size="large" @click="checkOut" :loading="loading">
          <i class="el-icon-finished"></i> 办理退房
        </el-button>
      </div>
    </el-card>
    
    <el-card v-else>
      <el-empty description="请输入订单号或手机号查询订单"></el-empty>
    </el-card>
    
    <el-dialog title="办理入住" :visible.sync="checkInDialogVisible" width="500px">
      <el-form :model="checkInForm" label-width="100px">
        <el-form-item label="实际入住日期">
          <el-date-picker
            v-model="checkInForm.actualCheckInDate"
            type="date"
            placeholder="选择日期"
            style="width: 100%;"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="押金">
          <el-input-number v-model="checkInForm.deposit" :min="0" :step="100"></el-input-number>
          <span style="margin-left: 10px;">元</span>
        </el-form-item>
        <el-form-item label="备注">
          <el-input type="textarea" v-model="checkInForm.remark" rows="3"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="checkInDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="confirmCheckIn">确 定</el-button>
      </span>
    </el-dialog>
    
    <el-dialog title="办理退房" :visible.sync="checkOutDialogVisible" width="500px">
      <el-form :model="checkOutForm" label-width="100px">
        <el-form-item label="实际退房日期">
          <el-date-picker
            v-model="checkOutForm.actualCheckOutDate"
            type="date"
            placeholder="选择日期"
            style="width: 100%;"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="房间检查">
          <el-radio-group v-model="checkOutForm.roomStatus">
            <el-radio :label="true">正常</el-radio>
            <el-radio :label="false">有损坏</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="赔偿费用" v-if="!checkOutForm.roomStatus">
          <el-input-number v-model="checkOutForm.compensationFee" :min="0" :step="50"></el-input-number>
          <span style="margin-left: 10px;">元</span>
        </el-form-item>
        <el-form-item label="退还押金">
          <span style="font-size: 18px; color: #67c23a; font-weight: bold;">¥{{ checkOutForm.depositRefund }}</span>
        </el-form-item>
        <el-form-item label="备注">
          <el-input type="textarea" v-model="checkOutForm.remark" rows="3"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="checkOutDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="confirmCheckOut">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { orders, orderStatusMap } from '../mock/data'

export default {
  name: 'CheckIn',
  data() {
    return {
      searchForm: {
        orderId: '',
        phone: ''
      },
      orderInfo: null,
      orderStatusMap: orderStatusMap,
      loading: false,
      checkInDialogVisible: false,
      checkOutDialogVisible: false,
      checkInForm: {
        actualCheckInDate: '',
        deposit: 200,
        remark: ''
      },
      checkOutForm: {
        actualCheckOutDate: '',
        roomStatus: true,
        compensationFee: 0,
        depositRefund: 200,
        remark: ''
      }
    }
  },
  watch: {
    'checkOutForm.roomStatus'(newVal) {
      if (newVal) {
        this.checkOutForm.compensationFee = 0
      }
      this.checkOutForm.depositRefund = this.checkInForm.deposit - this.checkOutForm.compensationFee
    },
    'checkOutForm.compensationFee'(newVal) {
      this.checkOutForm.depositRefund = this.checkInForm.deposit - newVal
    }
  },
  methods: {
    searchOrder() {
      if (!this.searchForm.orderId && !this.searchForm.phone) {
        this.$message.warning('请输入订单号或手机号')
        return
      }
      
      const found = orders.find(order => 
        order.id === this.searchForm.orderId || 
        order.phone === this.searchForm.phone
      )
      
      if (found) {
        this.orderInfo = { ...found }
      } else {
        this.orderInfo = null
        this.$message.error('未找到相关订单')
      }
    },
    resetSearch() {
      this.searchForm.orderId = ''
      this.searchForm.phone = ''
      this.orderInfo = null
    },
    checkIn() {
      this.checkInForm.actualCheckInDate = this.orderInfo.checkInDate
      this.checkInDialogVisible = true
    },
    confirmCheckIn() {
      this.loading = true
      setTimeout(() => {
        this.loading = false
        this.orderInfo.status = 'checked_in'
        this.checkInDialogVisible = false
        this.$message.success('入住登记成功！')
      }, 1000)
    },
    checkOut() {
      this.checkOutForm.actualCheckOutDate = this.orderInfo.checkOutDate
      this.checkOutForm.depositRefund = this.checkInForm.deposit
      this.checkOutDialogVisible = true
    },
    confirmCheckOut() {
      this.loading = true
      setTimeout(() => {
        this.loading = false
        this.orderInfo.status = 'completed'
        this.checkOutDialogVisible = false
        this.$message.success('退房成功！欢迎下次光临！')
      }, 1000)
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

.action-buttons {
  text-align: center;
}
</style>
