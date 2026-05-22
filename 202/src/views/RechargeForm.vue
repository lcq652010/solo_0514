<template>
  <div class="page-container">
    <div class="page-header">
      <div class="page-title">水电充值</div>
      <div class="page-subtitle">为您的宿舍进行水费和电费充值</div>
    </div>

    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="mb-20">
          <div slot="header">
            <span>当前余额</span>
          </div>
          <div class="balance-display">
            <div class="balance-item water">
              <div class="icon-wrapper">
                <i class="el-icon-water-cup"></i>
              </div>
              <div class="info">
                <div class="label">水费余额</div>
                <div class="value" :class="balance.water < 30 ? 'text-danger' : 'text-success'">
                  {{ balance.water.toFixed(2) }} <span class="unit">元</span>
                </div>
              </div>
            </div>
            <div class="balance-item electricity">
              <div class="icon-wrapper">
                <i class="el-icon-lightning"></i>
              </div>
              <div class="info">
                <div class="label">电费余额</div>
                <div class="value" :class="balance.electricity < 50 ? 'text-danger' : 'text-success'">
                  {{ balance.electricity.toFixed(2) }} <span class="unit">元</span>
                </div>
              </div>
            </div>
          </div>
        </el-card>

        <el-card>
          <div slot="header">
            <span>快速充值</span>
          </div>
          <div class="quick-amount">
            <div class="amount-label">选择充值金额：</div>
            <div class="amount-buttons">
              <el-button
                v-for="amount in quickAmounts"
                :key="amount"
                :type="form.amount === amount ? 'primary' : ''"
                @click="form.amount = amount"
              >
                {{ amount }}元
              </el-button>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="16">
        <el-card>
          <div slot="header">
            <span>充值表单</span>
          </div>
          <el-form :model="form" :rules="rules" ref="rechargeForm" label-width="100px" class="recharge-form">
            <el-form-item label="选择宿舍" prop="dormitory">
              <el-select v-model="form.dormitory" placeholder="请选择宿舍" style="width: 300px;">
                <el-option
                  v-for="dorm in dormitoryList"
                  :key="dorm"
                  :label="dorm"
                  :value="dorm"
                ></el-option>
              </el-select>
            </el-form-item>

            <el-form-item label="充值类型" prop="type">
              <el-radio-group v-model="form.type">
                <el-radio label="water">
                  <i class="el-icon-water-cup"></i> 水费
                </el-radio>
                <el-radio label="electricity">
                  <i class="el-icon-lightning"></i> 电费
                </el-radio>
              </el-radio-group>
            </el-form-item>

            <el-form-item label="充值金额" prop="amount">
              <el-input-number
                v-model="form.amount"
                :min="1"
                :max="maxAmount"
                :step="1"
                :precision="0"
                style="width: 300px;"
                placeholder="请输入充值金额（整数）"
              ></el-input-number>
              <span style="margin-left: 10px; color: #909399;">元（单笔最高{{ maxAmount }}元）</span>
            </el-form-item>

            <el-form-item label="支付方式" prop="payMethod">
              <el-radio-group v-model="form.payMethod">
                <el-radio label="微信支付">
                  <i class="el-icon-chat-dot-round" style="color: #07c160;"></i> 微信支付
                </el-radio>
                <el-radio label="支付宝">
                  <i class="el-icon-mobile-phone" style="color: #1677ff;"></i> 支付宝
                </el-radio>
                <el-radio label="校园卡">
                  <i class="el-icon-credit-pay"></i> 校园卡
                </el-radio>
              </el-radio-group>
            </el-form-item>

            <el-form-item label="联系手机" prop="phone">
              <el-input v-model="form.phone" placeholder="请输入手机号码" style="width: 300px;"></el-input>
            </el-form-item>

            <el-form-item label="备注">
              <el-input
                v-model="form.remark"
                type="textarea"
                :rows="3"
                placeholder="选填，如有特殊需求请备注"
                style="width: 400px;"
              ></el-input>
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="submitForm" :loading="submitting">确认充值</el-button>
              <el-button @click="resetForm">重置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog
      title="充值确认"
      :visible.sync="confirmDialogVisible"
      width="400px"
      @close="confirmDialogVisible = false"
    >
      <div class="confirm-content">
        <p>您即将进行以下充值操作：</p>
        <el-descriptions :column="1" border size="small">
          <el-descriptions-item label="宿舍">{{ form.dormitory }}</el-descriptions-item>
          <el-descriptions-item label="类型">{{ form.type === 'water' ? '水费' : '电费' }}</el-descriptions-item>
          <el-descriptions-item label="金额">
            <span class="text-primary" style="font-size: 18px; font-weight: 600;">{{ form.amount }} 元</span>
          </el-descriptions-item>
          <el-descriptions-item label="支付方式">{{ form.payMethod }}</el-descriptions-item>
        </el-descriptions>
      </div>
      <div slot="footer">
        <el-button @click="confirmDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmRecharge">确认支付</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getDormitoryList, getBalance, recharge, getCurrentDormitory, checkDuplicateRecharge } from '@/utils/mockData'
import { EventBus } from '@/utils/eventBus'

export default {
  name: 'RechargeForm',
  data() {
    const maxAmount = 1000
    const validatePositiveInteger = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入充值金额'))
      } else if (!Number.isInteger(value) || value <= 0) {
        callback(new Error('充值金额必须为正整数'))
      } else if (value > maxAmount) {
        callback(new Error(`单笔充值金额不能超过${maxAmount}元`))
      } else {
        callback()
      }
    }
    return {
      maxAmount,
      dormitoryList: [],
      balance: { water: 0, electricity: 0 },
      quickAmounts: [10, 20, 50, 100, 200, 500],
      submitting: false,
      confirmDialogVisible: false,
      form: {
        dormitory: '',
        type: 'water',
        amount: 50,
        payMethod: '微信支付',
        phone: '',
        remark: ''
      },
      rules: {
        dormitory: [
          { required: true, message: '请选择宿舍', trigger: 'change' }
        ],
        type: [
          { required: true, message: '请选择充值类型', trigger: 'change' }
        ],
        amount: [
          { required: true, validator: validatePositiveInteger, trigger: 'blur' }
        ],
        payMethod: [
          { required: true, message: '请选择支付方式', trigger: 'change' }
        ],
        phone: [
          { required: true, message: '请输入手机号码', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ]
      }
    }
  },
  watch: {
    'form.dormitory': function(val) {
      if (val) {
        this.balance = getBalance(val)
      }
    }
  },
  created() {
    this.dormitoryList = getDormitoryList()
    const currentDorm = getCurrentDormitory()
    if (currentDorm) {
      this.form.dormitory = currentDorm
      this.balance = getBalance(currentDorm)
    }
  },
  methods: {
    submitForm() {
      this.$refs.rechargeForm.validate((valid) => {
        if (valid) {
          this.confirmDialogVisible = true
        }
      })
    },
    confirmRecharge() {
      const isDuplicate = checkDuplicateRecharge(
        this.form.dormitory,
        this.form.type,
        this.form.amount
      )
      if (isDuplicate) {
        this.$confirm(
          '检测到该宿舍在5分钟内有相同金额的充值记录，是否确认继续充值？',
          '重复充值提醒',
          {
            confirmButtonText: '继续充值',
            cancelButtonText: '取消',
            type: 'warning'
          }
        ).then(() => {
          this.doRecharge()
        }).catch(() => {})
        return
      }
      this.doRecharge()
    },
    doRecharge() {
      this.submitting = true
      setTimeout(() => {
        recharge(this.form.dormitory, this.form.type, this.form.amount, this.form.payMethod)
        this.balance = getBalance(this.form.dormitory)
        this.submitting = false
        this.confirmDialogVisible = false
        this.$message.success('充值成功！')
        EventBus.$emit('recharge-success', {
          dormitory: this.form.dormitory,
          type: this.form.type,
          amount: this.form.amount
        })
        this.$refs.rechargeForm.resetFields()
        this.form.amount = 50
        this.form.type = 'water'
        this.form.payMethod = '微信支付'
        const currentDorm = getCurrentDormitory()
        if (currentDorm) {
          this.form.dormitory = currentDorm
        }
      }, 1000)
    },
    resetForm() {
      this.$refs.rechargeForm.resetFields()
      this.form.amount = 50
      this.form.type = 'water'
      this.form.payMethod = '微信支付'
      const currentDorm = getCurrentDormitory()
      if (currentDorm) {
        this.form.dormitory = currentDorm
      }
    }
  }
}
</script>

<style scoped>
.balance-display {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.balance-item {
  display: flex;
  align-items: center;
  padding: 15px;
  border-radius: 4px;
  background: #f5f7fa;
}

.balance-item .icon-wrapper {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin-right: 15px;
}

.balance-item.water .icon-wrapper {
  background: #ecf5ff;
  color: #409EFF;
}

.balance-item.electricity .icon-wrapper {
  background: #fdf6ec;
  color: #E6A23C;
}

.balance-item .info .label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 5px;
}

.balance-item .info .value {
  font-size: 24px;
  font-weight: 600;
}

.balance-item .info .unit {
  font-size: 14px;
  font-weight: normal;
  color: #909399;
}

.quick-amount .amount-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 10px;
}

.amount-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.amount-buttons .el-button {
  width: 70px;
}

.recharge-form {
  max-width: 600px;
}

.confirm-content {
  margin-bottom: 20px;
}

.confirm-content p {
  margin-bottom: 15px;
  color: #606266;
}
</style>
