<template>
  <div class="recharge-page">
    <div class="page-header">
      <div class="page-title">在线充值</div>
      <div class="page-subtitle">为宿舍充值水电费，方便快捷</div>
    </div>

    <el-row :gutter="20">
      <el-col :span="16">
        <div class="card-wrapper">
          <div class="card-header">
            <span class="card-title">充值信息填写</span>
          </div>
          <el-form
            ref="rechargeForm"
            :model="rechargeForm"
            :rules="rules"
            label-width="100px"
            class="recharge-form"
          >
            <el-form-item label="选择宿舍">
              <el-select
                v-model="rechargeForm.dormitoryId"
                placeholder="请选择宿舍"
                style="width: 100%"
              >
                <el-option
                  v-for="item in dormitoryList"
                  :key="item.id"
                  :label="`${item.building} ${item.room}`"
                  :value="item.id"
                >
                  <span>{{ item.building }} {{ item.room }}</span>
                  <span v-if="item.isDefault" style="color: #409EFF; margin-left: 8px;">(默认)</span>
                </el-option>
              </el-select>
            </el-form-item>

            <el-form-item label="充值类型" prop="type">
              <el-radio-group v-model="rechargeForm.type">
                <el-radio label="water">
                  <i class="el-icon-water-cup" style="margin-right: 5px;"></i>水费
                </el-radio>
                <el-radio label="electric">
                  <i class="el-icon-lightning" style="margin-right: 5px;"></i>电费
                </el-radio>
              </el-radio-group>
            </el-form-item>

            <el-form-item label="当前余额">
              <span v-if="rechargeForm.type === 'water'" class="balance-text" :class="{ 'text-danger': dormitoryInfo.waterBalance <= reminderSettings.waterThreshold }">
                ¥{{ dormitoryInfo.waterBalance }}
                <el-tag v-if="dormitoryInfo.waterBalance <= reminderSettings.waterThreshold" type="danger" size="mini" style="margin-left: 10px;">余额不足</el-tag>
              </span>
              <span v-else class="balance-text" :class="{ 'text-danger': dormitoryInfo.electricBalance <= reminderSettings.electricThreshold }">
                ¥{{ dormitoryInfo.electricBalance }}
                <el-tag v-if="dormitoryInfo.electricBalance <= reminderSettings.electricThreshold" type="danger" size="mini" style="margin-left: 10px;">余额不足</el-tag>
              </span>
            </el-form-item>

            <el-form-item label="充值金额" prop="amount">
              <div class="amount-buttons">
                <el-button
                  v-for="amount in amountOptions"
                  :key="amount"
                  :type="rechargeForm.amount === amount ? 'primary' : ''"
                  @click="rechargeForm.amount = amount"
                >
                  ¥{{ amount }}
                </el-button>
              </div>
              <div style="margin-top: 15px;">
                <el-input-number
                  v-model="rechargeForm.amount"
                  :min="10"
                  :max="1000"
                  :step="10"
                  style="width: 200px;"
                />
                <span style="margin-left: 10px; color: #909399;">元</span>
              </div>
            </el-form-item>

            <el-form-item label="支付方式" prop="paymentMethod">
              <el-radio-group v-model="rechargeForm.paymentMethod">
                <el-radio label="alipay">
                  <i class="el-icon-ali-pay" style="margin-right: 5px;"></i>支付宝
                </el-radio>
                <el-radio label="wechat">
                  <i class="el-icon-wechat" style="margin-right: 5px;"></i>微信
                </el-radio>
                <el-radio label="bank">
                  <i class="el-icon-postcard" style="margin-right: 5px;"></i>银行卡
                </el-radio>
              </el-radio-group>
            </el-form-item>

            <el-form-item label="联系手机" prop="phone">
              <el-input
                v-model="rechargeForm.phone"
                placeholder="请输入手机号，用于接收通知"
                maxlength="11"
              />
            </el-form-item>

            <el-form-item label="备注">
              <el-input
                v-model="rechargeForm.remark"
                type="textarea"
                :rows="3"
                placeholder="请输入备注信息（选填）"
              />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" size="large" @click="submitRecharge" :loading="loading">
                确认充值
              </el-button>
              <el-button size="large" @click="resetForm">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-col>

      <el-col :span="8">
        <div class="card-wrapper">
          <div class="card-header">
            <span class="card-title">充值信息确认</span>
          </div>
          <div class="confirm-info">
            <el-descriptions :column="1" border>
              <el-descriptions-item label="宿舍">
                {{ selectedDormitory }}
              </el-descriptions-item>
              <el-descriptions-item label="充值类型">
                {{ rechargeForm.type === 'water' ? '水费' : '电费' }}
              </el-descriptions-item>
              <el-descriptions-item label="充值金额">
                <span class="amount-highlight">¥{{ rechargeForm.amount || 0 }}</span>
              </el-descriptions-item>
              <el-descriptions-item label="支付方式">
                {{ getPaymentMethodText(rechargeForm.paymentMethod) }}
              </el-descriptions-item>
              <el-descriptions-item label="联系手机">
                {{ rechargeForm.phone || '未填写' }}
              </el-descriptions-item>
            </el-descriptions>

            <div class="tips-box">
              <div class="tips-title">
                <i class="el-icon-info"></i>温馨提示
              </div>
              <ul class="tips-list">
                <li>充值金额将实时到账，请确认信息无误后提交</li>
                <li>最低充值金额为10元，最高为1000元</li>
                <li>充值成功后将发送短信通知到您的手机</li>
                <li>如有问题请联系宿管中心</li>
              </ul>
            </div>
          </div>
        </div>

        <div class="card-wrapper" style="margin-top: 20px;">
          <div class="card-header">
            <span class="card-title">快捷充值</span>
          </div>
          <div class="quick-recharge">
            <el-button
              type="primary"
              plain
              style="width: 100%; margin-bottom: 10px;"
              @click="quickRecharge('water', 50)"
            >
              水费快速充值 ¥50
            </el-button>
            <el-button
              type="success"
              plain
              style="width: 100%; margin-bottom: 10px;"
              @click="quickRecharge('electric', 50)"
            >
              电费快速充值 ¥50
            </el-button>
            <el-button
              type="warning"
              plain
              style="width: 100%;"
              @click="quickRechargeBoth(100)"
            >
              水电各充值 ¥100
            </el-button>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { dormitoryInfo, bindingDormitories, reminderSettings, rechargeRecords } from '@/data/mock.js'

export default {
  name: 'Recharge',
  data() {
    return {
      loading: false,
      amountOptions: [10, 20, 50, 100, 200, 500],
      dormitoryList: bindingDormitories,
      dormitoryInfo,
      reminderSettings,
      rechargeForm: {
        dormitoryId: 1,
        type: 'electric',
        amount: 50,
        paymentMethod: 'alipay',
        phone: '',
        remark: ''
      },
      rules: {
        type: [
          { required: true, message: '请选择充值类型', trigger: 'change' }
        ],
        amount: [
          { required: true, message: '请输入充值金额', trigger: 'blur' },
          { type: 'number', min: 10, max: 1000, message: '充值金额在10-1000元之间', trigger: 'blur' },
          { validator: (rule, value, callback) => {
              if (!Number.isInteger(value)) {
                callback(new Error('充值金额必须为正整数'))
              } else if (value < 10) {
                callback(new Error('最低充值金额为10元'))
              } else {
                callback()
              }
            }, trigger: 'blur' }
        ],
        paymentMethod: [
          { required: true, message: '请选择支付方式', trigger: 'change' }
        ],
        phone: [
          { required: true, message: '请输入手机号', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    selectedDormitory() {
      const dorm = this.dormitoryList.find(d => d.id === this.rechargeForm.dormitoryId)
      return dorm ? `${dorm.building} ${dorm.room}` : ''
    }
  },
  methods: {
    getPaymentMethodText(method) {
      const map = {
        alipay: '支付宝',
        wechat: '微信',
        bank: '银行卡'
      }
      return map[method] || '未选择'
    },
    submitRecharge() {
      if (!Number.isInteger(this.rechargeForm.amount) || this.rechargeForm.amount < 10) {
        this.$message.error('充值金额必须为正整数且不低于10元')
        return
      }
      this.$refs.rechargeForm.validate(valid => {
        if (valid) {
          this.loading = true
          setTimeout(() => {
            this.loading = false
            if (this.rechargeForm.type === 'water') {
              this.dormitoryInfo.waterBalance += this.rechargeForm.amount
            } else {
              this.dormitoryInfo.electricBalance += this.rechargeForm.amount
            }
            const newRecord = {
              id: `RC${Date.now()}`,
              type: this.rechargeForm.type,
              amount: this.rechargeForm.amount,
              paymentMethod: this.rechargeForm.paymentMethod,
              status: 'success',
              createTime: new Date().toLocaleString().replace(/\//g, '-'),
              dormitory: this.selectedDormitory
            }
            rechargeRecords.unshift(newRecord)
            this.$message.success(`充值成功！已为${this.selectedDormitory}充值¥${this.rechargeForm.amount}`)
            this.$router.push('/records')
          }, 1500)
        } else {
          this.$message.error('请完善表单信息')
          return false
        }
      })
    },
    resetForm() {
      this.$refs.rechargeForm.resetFields()
    },
    quickRecharge(type, amount) {
      if (!Number.isInteger(amount) || amount < 10) {
        this.$message.error('充值金额必须为正整数且不低于10元')
        return
      }
      this.rechargeForm.type = type
      this.rechargeForm.amount = amount
      this.$message.info(`已选择${type === 'water' ? '水费' : '电费'}快速充值¥${amount}`)
    },
    quickRechargeBoth(amount) {
      if (!Number.isInteger(amount) || amount < 10) {
        this.$message.error('充值金额必须为正整数且不低于10元')
        return
      }
      this.$confirm(`确定要为水费和电费各充值¥${amount}吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.dormitoryInfo.waterBalance += amount
        this.dormitoryInfo.electricBalance += amount
        const newRecord1 = {
          id: `RC${Date.now()}`,
          type: 'water',
          amount: amount,
          paymentMethod: 'alipay',
          status: 'success',
          createTime: new Date().toLocaleString().replace(/\//g, '-'),
          dormitory: this.selectedDormitory
        }
        const newRecord2 = {
          id: `RC${Date.now() + 1}`,
          type: 'electric',
          amount: amount,
          paymentMethod: 'alipay',
          status: 'success',
          createTime: new Date().toLocaleString().replace(/\//g, '-'),
          dormitory: this.selectedDormitory
        }
        rechargeRecords.unshift(newRecord1, newRecord2)
        this.$message.success(`水电各充值¥${amount}成功！`)
        this.$router.push('/records')
      }).catch(() => {})
    }
  }
}
</script>

<style scoped>
.recharge-page {
  width: 100%;
}

.recharge-form {
  padding: 20px 0;
}

.balance-text {
  font-size: 18px;
  font-weight: 600;
  color: #409EFF;
}

.balance-text.text-danger {
  color: #F56C6C !important;
}

.amount-buttons .el-button {
  margin-right: 10px;
  margin-bottom: 10px;
}

.confirm-info {
  padding: 10px 0;
}

.amount-highlight {
  font-size: 24px;
  font-weight: 600;
  color: #F56C6C;
}

.tips-box {
  margin-top: 20px;
  padding: 15px;
  background: #ecf5ff;
  border-radius: 4px;
  border: 1px solid #b3d8ff;
}

.tips-title {
  color: #409EFF;
  font-weight: 600;
  margin-bottom: 10px;
}

.tips-list {
  margin: 0;
  padding-left: 20px;
  color: #606266;
  font-size: 13px;
}

.tips-list li {
  margin-bottom: 5px;
  line-height: 1.6;
}

.quick-recharge {
  padding: 10px 0;
}
</style>
