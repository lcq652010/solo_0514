<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">消费扣款</h2>
      <div>
        <el-button @click="goBack">
          <i class="el-icon-back"></i> 返回
        </el-button>
      </div>
    </div>

    <div class="form-container">
      <el-card v-loading="loading">
        <div v-if="member.id" class="member-info-panel">
          <el-descriptions :column="3" border size="small">
            <el-descriptions-item label="会员编号">{{ member.memberNo }}</el-descriptions-item>
            <el-descriptions-item label="会员姓名">{{ member.name }}</el-descriptions-item>
            <el-descriptions-item label="会员等级">
              <el-tag :type="getLevelTagType(member.level)" size="small">{{ member.level }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="当前余额">
              <span class="balance-text">¥{{ member.balance | formatMoney }}</span>
            </el-descriptions-item>
            <el-descriptions-item label="会员折扣">
              <span style="color: #e6a23c; font-weight: bold;">{{ discountInfo.discountText }}</span>
            </el-descriptions-item>
            <el-descriptions-item label="会员积分">{{ member.point }}</el-descriptions-item>
          </el-descriptions>
        </div>

        <el-form
          ref="form"
          :model="form"
          :rules="rules"
          label-width="100px"
          style="margin-top: 20px;"
        >
          <el-form-item label="选择会员" prop="memberId">
            <el-select
              v-model="form.memberId"
              placeholder="请选择会员"
              filterable
              style="width: 100%;"
              @change="handleMemberChange"
              :disabled="!!$route.params.memberId"
            >
              <el-option
                v-for="item in memberOptions"
                :key="item.id"
                :label="`${item.memberNo} - ${item.name} (${item.level})`"
                :value="item.id"
              ></el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="消费金额" prop="originalAmount">
            <el-input-number
              v-model="form.originalAmount"
              :min="0.01"
              :max="100000"
              :precision="2"
              :step="50"
              style="width: 100%;"
              placeholder="请输入消费金额"
              @change="calculateDiscount"
            ></el-input-number>
          </el-form-item>

          <el-form-item label="快捷金额">
            <el-button-group>
              <el-button @click="setQuickAmount(50)">¥50</el-button>
              <el-button @click="setQuickAmount(100)">¥100</el-button>
              <el-button @click="setQuickAmount(200)">¥200</el-button>
              <el-button @click="setQuickAmount(500)">¥500</el-button>
              <el-button @click="setQuickAmount(1000)">¥1000</el-button>
            </el-button-group>
          </el-form-item>

          <el-form-item label="折扣计算">
            <div class="discount-calc-panel">
              <div class="calc-row">
                <span class="calc-label">原价金额：</span>
                <span class="calc-value">¥{{ form.originalAmount | formatMoney }}</span>
              </div>
              <div class="calc-row">
                <span class="calc-label">会员折扣：</span>
                <span class="calc-value discount">{{ discountInfo.discountText }}</span>
              </div>
              <div class="calc-row">
                <span class="calc-label">优惠金额：</span>
                <span class="calc-value discount"> -¥{{ discountAmount | formatMoney }}</span>
              </div>
              <div class="calc-row total">
                <span class="calc-label">实付金额：</span>
                <span class="calc-value total">¥{{ form.amount | formatMoney }}</span>
              </div>
            </div>
          </el-form-item>

          <el-form-item label="支付方式" prop="paymentMethod">
            <el-radio-group v-model="form.paymentMethod" @change="calculateDiscount">
              <el-radio label="余额支付">余额支付</el-radio>
              <el-radio label="现金支付">现金支付</el-radio>
              <el-radio label="微信支付">微信支付</el-radio>
              <el-radio label="支付宝支付">支付宝支付</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item label="备注信息">
            <el-input
              v-model="form.remark"
              type="textarea"
              :rows="3"
              placeholder="请输入备注信息（可选）"
            ></el-input>
          </el-form-item>

          <el-form-item>
            <div v-if="previewAmount !== null" class="preview-panel">
              <p style="margin: 0;">
                <strong>消费后余额：</strong>
                <span :class="previewAmount < 0 ? 'text-danger' : 'text-success'" style="font-size: 20px;">
                  ¥{{ previewAmount | formatMoney }}
                </span>
                <span v-if="previewAmount < 0" class="text-danger" style="margin-left: 10px;">（余额不足）</span>
              </p>
            </div>
            <el-button type="danger" size="large" @click="handleSubmit" style="width: 150px;" :loading="submitting">
              <i class="el-icon-check"></i> {{ submitting ? '提交中...' : '确认扣款' }}
            </el-button>
            <el-button size="large" @click="handleReset" style="margin-left: 20px;">
              <i class="el-icon-refresh"></i> 重置
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script>
import { getMembers, getMemberById, consume, getDiscountInfoByLevel } from '@/mock/data'
import { EventBus } from '@/utils/eventBus'

export default {
  name: 'ConsumeForm',
  data() {
    return {
      submitting: false,
      memberOptions: [],
      member: {},
      discountInfo: {
        discount: 1,
        discountText: '无折扣'
      },
      form: {
        memberId: null,
        originalAmount: null,
        amount: null,
        paymentMethod: '余额支付',
        remark: ''
      },
      rules: {
        memberId: [
          { required: true, message: '请选择会员', trigger: 'change' }
        ],
        originalAmount: [
          { required: true, message: '请输入消费金额', trigger: 'blur' },
          { type: 'number', min: 0.01, message: '消费金额必须大于0', trigger: 'blur' }
        ],
        paymentMethod: [
          { required: true, message: '请选择支付方式', trigger: 'change' }
        ]
      }
    }
  },
  computed: {
    discountAmount() {
      if (this.form.originalAmount && this.discountInfo.discount) {
        return parseFloat((this.form.originalAmount * (1 - this.discountInfo.discount)).toFixed(2))
      }
      return 0
    },
    previewAmount() {
      if (this.member.balance !== undefined && this.form.amount && this.form.paymentMethod === '余额支付') {
        return parseFloat((this.member.balance - this.form.amount).toFixed(2))
      }
      return null
    }
  },
  created() {
    this.memberOptions = getMembers()
    const memberId = this.$route.params.memberId
    if (memberId) {
      this.form.memberId = parseInt(memberId)
      this.handleMemberChange(this.form.memberId)
    }
  },
  methods: {
    getLevelTagType(level) {
      const typeMap = {
        '钻石会员': 'danger',
        '金卡会员': 'warning',
        '银卡会员': 'success',
        '普通会员': 'info'
      }
      return typeMap[level] || ''
    },
    handleMemberChange(memberId) {
      if (memberId) {
        this.member = getMemberById(memberId) || {}
        this.discountInfo = getDiscountInfoByLevel(this.member.level)
        this.calculateDiscount()
      } else {
        this.member = {}
        this.discountInfo = { discount: 1, discountText: '无折扣' }
      }
    },
    calculateDiscount() {
      if (this.form.originalAmount && this.discountInfo.discount) {
        this.form.amount = parseFloat((this.form.originalAmount * this.discountInfo.discount).toFixed(2))
      } else {
        this.form.amount = null
      }
    },
    setQuickAmount(amount) {
      this.form.originalAmount = amount
      this.calculateDiscount()
    },
    handleSubmit() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          const discountRemark = this.discountAmount > 0 ? `，优惠${this.discountAmount}元，${this.discountInfo.discountText}` : ''
          this.$confirm(`确认 ${this.member.name} 消费 ¥${this.form.amount} 元？\n原价 ¥${this.form.originalAmount} 元${discountRemark}`, '消费确认', {
            confirmButtonText: '确认扣款',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            this.submitting = true
            setTimeout(() => {
              const remark = this.form.remark || `消费，原价${this.form.originalAmount}元，实付${this.form.amount}元${this.discountAmount > 0 ? `，${this.discountInfo.discountText}优惠${this.discountAmount}元` : ''}`
              const result = consume(
                this.form.memberId,
                this.form.amount,
                this.form.paymentMethod,
                remark
              )
              this.submitting = false
              if (result.success) {
                EventBus.$emit('refreshTransactions')
                this.$message({
                  type: 'success',
                  message: `消费成功！${this.member.name} 消费 ¥${this.form.amount} 元${this.discountAmount > 0 ? `，优惠 ¥${this.discountAmount} 元` : ''}`,
                  duration: 3000,
                  showClose: true
                })
                this.handleMemberChange(this.form.memberId)
                this.$router.push('/transactions')
              } else {
                this.$message({
                  type: 'error',
                  message: result.message || '消费失败，请稍后重试',
                  duration: 3000,
                  showClose: true
                })
              }
            }, 500)
          }).catch(() => {})
        }
      })
    },
    handleReset() {
      this.$refs.form.resetFields()
      const memberId = this.$route.params.memberId
      if (memberId) {
        this.form.memberId = parseInt(memberId)
        this.handleMemberChange(this.form.memberId)
      } else {
        this.discountInfo = { discount: 1, discountText: '无折扣' }
      }
    },
    goBack() {
      this.$router.back()
    }
  }
}
</script>

<style scoped lang="scss">
.discount-calc-panel {
  background: #f5f7fa;
  border-radius: 4px;
  padding: 15px;
  width: 100%;

  .calc-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px dashed #dcdfe6;

    &:last-child {
      border-bottom: none;
    }

    &.total {
      padding-top: 12px;
      margin-top: 5px;
      border-top: 2px solid #dcdfe6;
      border-bottom: none;
    }

    .calc-label {
      color: #606266;
      font-size: 14px;
    }

    .calc-value {
      font-size: 16px;
      font-weight: 500;

      &.discount {
        color: #f56c6c;
      }

      &.total {
        color: #e6a23c;
        font-size: 20px;
        font-weight: bold;
      }
    }
  }
}

.preview-panel {
  margin-bottom: 15px;
  padding: 15px;
  background: #fef0f0;
  border-radius: 4px;
}

.text-danger {
  color: #f56c6c;
  font-weight: bold;
}

.text-success {
  color: #67c23a;
  font-weight: bold;
}
</style>
