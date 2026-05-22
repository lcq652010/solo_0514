<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">会员充值</h2>
      <div>
        <el-button @click="goBack">
          <i class="el-icon-back"></i> 返回
        </el-button>
      </div>
    </div>

    <div class="form-container">
      <el-card v-loading="loading">
        <div v-if="member.id" class="member-info-panel">
          <el-descriptions :column="2" border size="small">
            <el-descriptions-item label="会员编号">{{ member.memberNo }}</el-descriptions-item>
            <el-descriptions-item label="会员姓名">{{ member.name }}</el-descriptions-item>
            <el-descriptions-item label="会员等级">{{ member.level }}</el-descriptions-item>
            <el-descriptions-item label="当前余额">
              <span class="balance-text">¥{{ member.balance | formatMoney }}</span>
            </el-descriptions-item>
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
                :label="`${item.memberNo} - ${item.name}`"
                :value="item.id"
              ></el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="充值金额" prop="amount">
            <el-input-number
              v-model="form.amount"
              :min="0.01"
              :max="100000"
              :precision="2"
              :step="100"
              style="width: 100%;"
              placeholder="请输入充值金额"
            ></el-input-number>
          </el-form-item>

          <el-form-item label="快捷金额">
            <el-button-group>
              <el-button @click="setQuickAmount(100)">¥100</el-button>
              <el-button @click="setQuickAmount(200)">¥200</el-button>
              <el-button @click="setQuickAmount(500)">¥500</el-button>
              <el-button @click="setQuickAmount(1000)">¥1000</el-button>
              <el-button @click="setQuickAmount(2000)">¥2000</el-button>
            </el-button-group>
          </el-form-item>

          <el-form-item label="支付方式" prop="paymentMethod">
            <el-radio-group v-model="form.paymentMethod">
              <el-radio label="现金支付">现金支付</el-radio>
              <el-radio label="微信支付">微信支付</el-radio>
              <el-radio label="支付宝支付">支付宝支付</el-radio>
              <el-radio label="银行转账">银行转账</el-radio>
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
            <div v-if="previewAmount" style="margin-bottom: 15px; padding: 15px; background: #f0f9eb; border-radius: 4px;">
              <p style="margin: 0; color: #67c23a;">
                <strong>充值后余额：</strong>
                <span style="font-size: 20px;">¥{{ previewAmount | formatMoney }}</span>
              </p>
            </div>
            <el-button type="primary" size="large" @click="handleSubmit" style="width: 150px;" :loading="submitting">
              <i class="el-icon-check"></i> {{ submitting ? '提交中...' : '确认充值' }}
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
import { getMembers, getMemberById, recharge } from '@/mock/data'
import { EventBus } from '@/utils/eventBus'

export default {
  name: 'RechargeForm',
  data() {
    return {
      submitting: false,
      memberOptions: [],
      member: {},
      form: {
        memberId: null,
        amount: null,
        paymentMethod: '微信支付',
        remark: ''
      },
      rules: {
        memberId: [
          { required: true, message: '请选择会员', trigger: 'change' }
        ],
        amount: [
          { required: true, message: '请输入充值金额', trigger: 'blur' },
          { type: 'number', min: 0.01, message: '充值金额必须大于0', trigger: 'blur' }
        ],
        paymentMethod: [
          { required: true, message: '请选择支付方式', trigger: 'change' }
        ]
      }
    }
  },
  computed: {
    previewAmount() {
      if (this.member.balance !== undefined && this.form.amount) {
        return this.member.balance + this.form.amount
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
    handleMemberChange(memberId) {
      if (memberId) {
        this.member = getMemberById(memberId) || {}
      } else {
        this.member = {}
      }
    },
    setQuickAmount(amount) {
      this.form.amount = amount
    },
    handleSubmit() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.$confirm(`确认为 ${this.member.name} 充值 ¥${this.form.amount} 元？`, '充值确认', {
            confirmButtonText: '确定充值',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            this.submitting = true
            setTimeout(() => {
              const result = recharge(
                this.form.memberId,
                this.form.amount,
                this.form.paymentMethod,
                this.form.remark
              )
              this.submitting = false
              if (result.success) {
                EventBus.$emit('refreshTransactions')
                this.$message({
                  type: 'success',
                  message: `充值成功！已为 ${this.member.name} 充值 ¥${this.form.amount} 元`,
                  duration: 3000,
                  showClose: true
                })
                this.handleMemberChange(this.form.memberId)
                this.$router.push('/transactions')
              } else {
                this.$message({
                  type: 'error',
                  message: result.message || '充值失败，请稍后重试',
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
      }
    },
    goBack() {
      this.$router.back()
    }
  }
}
</script>
