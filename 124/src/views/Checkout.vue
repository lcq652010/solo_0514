<template>
  <div class="checkout">
    <div class="page-title">结算收银</div>
    <el-row :gutter="20">
      <el-col :span="14">
        <div class="card-wrapper">
          <div style="margin-bottom: 20px;">
            <span style="font-weight: bold; font-size: 16px;">服务清单</span>
          </div>
          
          <el-table :data="serviceList" border stripe style="width: 100%;">
            <el-table-column prop="name" label="服务项目"></el-table-column>
            <el-table-column prop="price" label="单价(元)" width="120">
              <template slot-scope="scope">
                ¥{{ scope.row.price }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="100">
              <template slot-scope="scope">
                <el-button size="small" type="danger" @click="removeService(scope.$index)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>

          <el-divider></el-divider>
          
          <div style="margin-bottom: 20px;">
            <el-select v-model="selectedService" placeholder="选择添加服务" style="width: 300px; margin-right: 10px;">
              <el-option label="基础洗护套餐 - ¥88" :value="{ name: '基础洗护套餐', price: 88 }"></el-option>
              <el-option label="精致洗护套餐 - ¥168" :value="{ name: '精致洗护套餐', price: 168 }"></el-option>
              <el-option label="豪华美容套餐 - ¥298" :value="{ name: '豪华美容套餐', price: 298 }"></el-option>
              <el-option label="医疗洗护套餐 - ¥198" :value="{ name: '医疗洗护套餐', price: 198 }"></el-option>
              <el-option label="猫咪专属套餐 - ¥128" :value="{ name: '猫咪专属套餐', price: 128 }"></el-option>
              <el-option label="大型犬洗护 - ¥258" :value="{ name: '大型犬洗护', price: 258 }"></el-option>
              <el-option label="指甲修剪 - ¥20" :value="{ name: '指甲修剪', price: 20 }"></el-option>
              <el-option label="耳道清洁 - ¥30" :value="{ name: '耳道清洁', price: 30 }"></el-option>
            </el-select>
            <el-button type="primary" @click="addService">添加服务</el-button>
          </div>

          <div class="amount-section">
            <div class="amount-row">
              <span>商品金额：</span>
              <span>¥{{ subtotal }}</span>
            </div>
            <div class="amount-row">
              <span>折扣：</span>
              <el-input-number 
                v-model="discount" 
                :min="0" 
                :max="100" 
                :step="5" 
                style="width: 150px;"
              ></el-input-number>
              <span style="margin-left: 10px;">%</span>
              <span v-if="memberInfo.level" class="discount-hint">
                ({{ memberInfo.level }}专享)
              </span>
            </div>
            <div class="amount-row">
              <span>折扣金额：</span>
              <span style="color: #67C23A;">-¥{{ discountAmount }}</span>
            </div>
            <el-divider></el-divider>
            <div class="amount-row total">
              <span>应收金额：</span>
              <span style="color: #F56C6C; font-size: 24px; font-weight: bold;">¥{{ totalAmount }}</span>
            </div>
          </div>
        </div>
      </el-col>

      <el-col :span="10">
        <div class="card-wrapper">
          <div style="margin-bottom: 20px;">
            <span style="font-weight: bold; font-size: 16px;">客户信息</span>
          </div>
          
          <el-form :model="customerInfo" label-width="100px">
            <el-form-item label="客户姓名">
              <el-input v-model="customerInfo.name" placeholder="请输入客户姓名"></el-input>
            </el-form-item>
            <el-form-item label="联系电话">
              <el-input v-model="customerInfo.phone" placeholder="请输入联系电话"></el-input>
            </el-form-item>
            <el-form-item label="宠物名称">
              <el-input v-model="customerInfo.petName" placeholder="请输入宠物名称"></el-input>
            </el-form-item>
            <el-form-item label="是否会员">
              <el-switch v-model="customerInfo.isMember" active-text="是" inactive-text="否" @change="handleMemberChange"></el-switch>
            </el-form-item>
            <el-form-item label="会员卡号" v-if="customerInfo.isMember">
              <el-input v-model="customerInfo.memberCardNo" placeholder="请输入会员卡号"></el-input>
              <el-button type="primary" size="small" style="margin-top: 10px;" @click="searchMember">查询会员</el-button>
            </el-form-item>
            <el-form-item label="会员等级" v-if="memberInfo.level">
              <el-tag :type="getLevelType(memberInfo.level)">{{ memberInfo.level }}</el-tag>
              <span style="margin-left: 10px; color: #67C23A;">账户余额：¥{{ memberInfo.balance }}</span>
            </el-form-item>
          </el-form>

          <el-divider></el-divider>

          <div style="margin-bottom: 20px;">
            <span style="font-weight: bold; font-size: 16px;">支付方式</span>
          </div>

          <el-radio-group v-model="paymentMethod" style="width: 100%;">
            <el-radio label="现金" border style="width: 48%; margin-bottom: 10px;">现金支付</el-radio>
            <el-radio label="微信" border style="width: 48%; margin-bottom: 10px;">微信支付</el-radio>
            <el-radio label="支付宝" border style="width: 48%; margin-bottom: 10px;">支付宝</el-radio>
            <el-radio label="会员卡" border style="width: 48%; margin-bottom: 10px;" v-if="customerInfo.isMember">会员卡</el-radio>
          </el-radio-group>

          <el-divider></el-divider>

          <el-form :model="paymentInfo" label-width="100px">
            <el-form-item label="实收金额">
              <el-input-number v-model="paymentInfo.paidAmount" :min="0" :step="10" style="width: 100%;"></el-input-number>
            </el-form-item>
            <el-form-item label="找零">
              <span style="color: #F56C6C; font-size: 18px; font-weight: bold;">¥{{ changeAmount }}</span>
            </el-form-item>
            <el-form-item label="备注">
              <el-input type="textarea" v-model="paymentInfo.remark" :rows="2" placeholder="请输入备注信息"></el-input>
            </el-form-item>
          </el-form>

          <el-button type="primary" size="large" style="width: 100%; margin-top: 20px;" @click="handleCheckout" :loading="loading">
            <i class="el-icon-finished"></i> 确认收款
          </el-button>
        </div>
      </el-col>
    </el-row>

    <el-dialog
      title="收款成功"
      :visible.sync="successDialogVisible"
      width="500px"
    >
      <div style="text-align: center; padding: 20px;">
        <i class="el-icon-circle-check" style="font-size: 64px; color: #67C23A;"></i>
        <p style="font-size: 18px; margin: 20px 0;">收款成功！</p>
        <el-descriptions :column="1" border>
          <el-descriptions-item label="应收金额">¥{{ totalAmount }}</el-descriptions-item>
          <el-descriptions-item label="实收金额">¥{{ paymentInfo.paidAmount }}</el-descriptions-item>
          <el-descriptions-item label="找零">¥{{ changeAmount }}</el-descriptions-item>
          <el-descriptions-item label="支付方式">{{ paymentMethod }}</el-descriptions-item>
          <el-descriptions-item label="交易时间">{{ transactionTime }}</el-descriptions-item>
        </el-descriptions>
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button @click="printReceipt">打印小票</el-button>
        <el-button type="primary" @click="newOrder">新订单</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'Checkout',
  data() {
    return {
      loading: false,
      successDialogVisible: false,
      transactionTime: '',
      selectedService: null,
      discount: 0,
      paymentMethod: '现金',
      serviceList: [
        { name: '基础洗护套餐', price: 88 }
      ],
      customerInfo: {
        name: '',
        phone: '',
        petName: '',
        isMember: false,
        memberCardNo: ''
      },
      memberInfo: {
        level: '',
        balance: 0
      },
      paymentInfo: {
        paidAmount: 0,
        remark: ''
      }
    }
  },
  computed: {
    subtotal() {
      return this.serviceList.reduce((sum, item) => sum + item.price, 0)
    },
    discountAmount() {
      return Math.round(this.subtotal * this.discount / 100 * 100) / 100
    },
    totalAmount() {
      return this.subtotal - this.discountAmount
    },
    changeAmount() {
      return Math.max(0, this.paymentInfo.paidAmount - this.totalAmount)
    }
  },
  watch: {
    totalAmount(newVal) {
      if (this.paymentInfo.paidAmount < newVal) {
        this.paymentInfo.paidAmount = newVal
      }
    },
    serviceList: {
      handler() {
        this.$nextTick(() => {
          if (this.paymentInfo.paidAmount < this.totalAmount) {
            this.paymentInfo.paidAmount = this.totalAmount
          }
        })
      },
      deep: true
    },
    'memberInfo.level'(newLevel) {
      if (newLevel) {
        const discountMap = {
          '普通会员': 0,
          '银卡会员': 5,
          '金卡会员': 10,
          '钻石会员': 15
        }
        const newDiscount = discountMap[newLevel] || 0
        if (this.discount < newDiscount) {
          this.discount = newDiscount
        }
      }
    }
  },
  methods: {
    getLevelType(level) {
      const typeMap = {
        '普通会员': 'info',
        '银卡会员': '',
        '金卡会员': 'warning',
        '钻石会员': 'danger'
      }
      return typeMap[level] || ''
    },
    addService() {
      if (this.selectedService) {
        this.serviceList.push({ ...this.selectedService })
        this.selectedService = null
      } else {
        this.$message.warning('请选择要添加的服务')
      }
    },
    removeService(index) {
      this.serviceList.splice(index, 1)
    },
    handleMemberChange(val) {
      if (!val) {
        this.memberInfo = { level: '', balance: 0 }
        this.discount = 0
      }
    },
    getMemberList() {
      const defaultMembers = [
        { cardNo: 'VIP20240001', name: '张三', phone: '13800138001', level: '金卡会员', balance: 1580, points: 3200 },
        { cardNo: 'VIP20240002', name: '李四', phone: '13800138002', level: '银卡会员', balance: 680, points: 1500 },
        { cardNo: 'VIP20240003', name: '王五', phone: '13800138003', level: '钻石会员', balance: 3200, points: 8500 }
      ]
      const stored = localStorage.getItem('memberList')
      if (stored) {
        return JSON.parse(stored)
      }
      localStorage.setItem('memberList', JSON.stringify(defaultMembers))
      return defaultMembers
    },
    saveMemberList(memberList) {
      localStorage.setItem('memberList', JSON.stringify(memberList))
    },
    searchMember() {
      if (!this.customerInfo.memberCardNo) {
        this.$message.warning('请输入会员卡号')
        return
      }
      
      const memberList = this.getMemberList()
      const member = memberList.find(m => m.cardNo === this.customerInfo.memberCardNo)
      
      if (member) {
        this.memberInfo = { ...member }
        this.customerInfo.name = member.name
        this.customerInfo.phone = member.phone
        
        const discountMap = {
          '普通会员': 0,
          '银卡会员': 5,
          '金卡会员': 10,
          '钻石会员': 15
        }
        this.discount = discountMap[member.level] || 0
        
        this.$message.success('会员信息查询成功')
      } else {
        this.$message.error('未找到该会员信息')
      }
    },
    handleCheckout() {
      if (this.serviceList.length === 0) {
        this.$message.warning('请添加服务项目')
        return
      }
      
      if (!this.customerInfo.name) {
        this.$message.warning('请输入客户姓名')
        return
      }
      
      if (this.paymentInfo.paidAmount < this.totalAmount) {
        this.$message.error('实收金额不能小于应收金额')
        return
      }
      
      if (this.paymentMethod === '会员卡') {
        if (!this.memberInfo.balance || this.memberInfo.balance < this.totalAmount) {
          this.$message.error('会员卡余额不足')
          return
        }
      }
      
      this.loading = true
      setTimeout(() => {
        this.loading = false
        
        if (this.paymentMethod === '会员卡' && this.customerInfo.memberCardNo) {
          const memberList = this.getMemberList()
          const memberIndex = memberList.findIndex(m => m.cardNo === this.customerInfo.memberCardNo)
          if (memberIndex > -1) {
            memberList[memberIndex].balance = Math.round((memberList[memberIndex].balance - this.totalAmount) * 100) / 100
            memberList[memberIndex].points = (memberList[memberIndex].points || 0) + Math.floor(this.totalAmount)
            this.saveMemberList(memberList)
            this.memberInfo.balance = memberList[memberIndex].balance
            this.$message.success(`会员卡已自动抵扣 ¥${this.totalAmount}，余额 ¥${this.memberInfo.balance}`)
          }
        }
        
        this.transactionTime = new Date().toLocaleString()
        this.successDialogVisible = true
      }, 1000)
    },
    printReceipt() {
      this.$message.success('小票打印成功')
    },
    newOrder() {
      this.successDialogVisible = false
      this.serviceList = []
      this.customerInfo = {
        name: '',
        phone: '',
        petName: '',
        isMember: false,
        memberCardNo: ''
      }
      this.memberInfo = { level: '', balance: 0 }
      this.discount = 0
      this.paymentInfo.paidAmount = 0
      this.paymentInfo.remark = ''
      this.$message.success('已创建新订单')
    }
  }
}
</script>

<style scoped>
.amount-section {
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.amount-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  font-size: 14px;
}

.amount-row.total {
  font-size: 16px;
  font-weight: bold;
}

.discount-hint {
  color: #67C23A;
  font-size: 12px;
  margin-left: 5px;
}
</style>
