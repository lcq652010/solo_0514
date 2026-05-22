<template>
  <div class="order-page">
    <el-card class="card-shadow order-card">
      <div slot="header" class="card-header">
        <span>篆刻印章定制</span>
      </div>
      
      <el-form :model="orderForm" :rules="rules" ref="orderForm" label-width="120px" class="order-form">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="客户姓名" prop="customerName">
              <el-input v-model="orderForm.customerName" placeholder="请输入您的姓名"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="orderForm.phone" placeholder="请输入联系电话"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">印章配置</el-divider>

        <el-form-item label="印石材质" prop="stoneMaterial">
          <el-select v-model="orderForm.stoneMaterial" placeholder="请选择印石材质" style="width: 100%;" @change="calculatePrice">
            <el-option
              v-for="item in stoneMaterials"
              :key="item.value"
              :label="item.label + ' (¥' + item.price + ')'"
              :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="印章尺寸(cm)" prop="size">
              <el-input-number 
                v-model="orderForm.size" 
                :min="1.5" 
                :max="5" 
                :step="0.5" 
                style="width: 100%;"
                @change="handleSizeChange">
              </el-input-number>
              <div class="size-tip" :class="sizeTipClass">
                <i class="el-icon-info"></i>
                {{ sizeTipText }}
              </div>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="字体风格" prop="fontStyle">
              <el-select v-model="orderForm.fontStyle" placeholder="请选择字体风格" style="width: 100%;">
                <el-option
                  v-for="item in fontStyles"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="印文内容" prop="sealContent">
          <el-input 
            v-model="orderForm.sealContent" 
            placeholder="请输入印章文字（建议2-4字）"
            maxlength="8"
            show-word-limit>
          </el-input>
          <div class="content-tip">常用：姓名、字号、斋馆名、吉语等</div>
        </el-form-item>

        <el-form-item label="边款需求" prop="sideOption">
          <el-radio-group v-model="orderForm.sideOption" @change="handleSideChange">
            <el-radio-button v-for="item in sideOptions" :key="item.value" :label="item.value">
              {{ item.label }}
            </el-radio-button>
          </el-radio-group>
        </el-form-item>

        <el-form-item v-if="showSideContent" label="边款内容" prop="sideContent">
          <el-input
            type="textarea"
            :rows="3"
            v-model="orderForm.sideContent"
            placeholder="请输入边款内容"
            maxlength="50"
            show-word-limit>
          </el-input>
        </el-form-item>

        <el-divider></el-divider>

        <div class="price-section">
          <span class="price-label">预估价格：</span>
          <span class="price-value">¥{{ totalPrice }}</span>
        </div>

        <el-form-item class="submit-section">
          <el-button type="primary" size="large" @click="submitOrder" :loading="submitting">
            提交订单
          </el-button>
          <el-button size="large" @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { stoneMaterials, fontStyles, sideOptions } from '../data/mockData'

export default {
  name: 'OrderPage',
  data() {
    return {
      stoneMaterials,
      fontStyles,
      sideOptions,
      submitting: false,
      orderForm: {
        customerName: '',
        phone: '',
        stoneMaterial: '',
        size: 2.5,
        fontStyle: '',
        sealContent: '',
        sideOption: 'none',
        sideContent: ''
      },
      rules: {
        customerName: [
          { required: true, message: '请输入客户姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '姓名长度在2-20个字符之间', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
        ],
        stoneMaterial: [
          { required: true, message: '请选择印石材质', trigger: 'change' },
          {
            validator: (rule, value, callback) => {
              const validMaterials = this.stoneMaterials.map(m => m.value)
              if (value && !validMaterials.includes(value)) {
                callback(new Error('请选择有效的印石材质'))
              } else {
                callback()
              }
            },
            trigger: 'change'
          }
        ],
        size: [
          { required: true, message: '请输入印章尺寸', trigger: 'change' },
          { type: 'number', min: 1.5, max: 5, message: '印章尺寸需在1.5cm - 5cm之间', trigger: 'change' },
          {
            validator: (rule, value, callback) => {
              if (value && (value * 10) % 5 !== 0) {
                callback(new Error('印章尺寸需为0.5cm的整数倍'))
              } else {
                callback()
              }
            },
            trigger: 'change'
          }
        ],
        fontStyle: [
          { required: true, message: '请选择字体风格', trigger: 'change' },
          {
            validator: (rule, value, callback) => {
              const validFonts = this.fontStyles.map(f => f.value)
              if (value && !validFonts.includes(value)) {
                callback(new Error('请选择有效的字体风格'))
              } else {
                callback()
              }
            },
            trigger: 'change'
          }
        ],
        sealContent: [
          { required: true, message: '请输入印文内容', trigger: 'blur' },
          { min: 1, max: 8, message: '印文内容在1-8个字之间', trigger: 'blur' },
          { pattern: /^[^\s]+$/, message: '印文内容不能包含空格', trigger: 'blur' }
        ],
        sideContent: [
          {
            validator: (rule, value, callback) => {
              if (this.showSideContent && !value?.trim()) {
                callback(new Error('请输入边款内容'))
              } else {
                callback()
              }
            },
            trigger: 'blur'
          }
        ]
      }
    }
  },
  computed: {
    showSideContent() {
      return this.orderForm.sideOption !== 'none'
    },
    totalPrice() {
      const material = this.stoneMaterials.find(m => m.value === this.orderForm.stoneMaterial)
      const basePrice = material ? material.price : 0
      const sizePrice = (this.orderForm.size - 2) * 50
      const sidePrice = this.orderForm.sideOption === 'none' ? 0 : 
                        this.orderForm.sideOption === 'simple' ? 30 :
                        this.orderForm.sideOption === 'poem' ? 80 : 50
      return Math.max(0, basePrice + sizePrice + sidePrice)
    },
    sizeTipText() {
      const size = this.orderForm.size
      if (size < 2) {
        return '尺寸较小，适合制作小印章，建议2.0cm以上'
      } else if (size > 3.5) {
        return '尺寸较大，雕刻难度增加，价格会相应提高'
      } else if (size >= 2 && size <= 3) {
        return '尺寸适中，是最常用的印章规格'
      } else {
        return '尺寸合理，适合制作稍大的印章'
      }
    },
    sizeTipClass() {
      const size = this.orderForm.size
      if (size < 2 || size > 3.5) {
        return 'size-warning'
      }
      return 'size-normal'
    }
  },
  methods: {
    handleSideChange() {
      if (this.orderForm.sideOption === 'none') {
        this.orderForm.sideContent = ''
      }
    },
    handleSizeChange() {
    },
    calculatePrice() {
    },
    submitOrder() {
      this.$refs.orderForm.validate((valid) => {
        if (valid) {
          this.submitting = true
          
          setTimeout(() => {
            this.submitting = false
            
            const order = {
              ...this.orderForm,
              id: 'ORD' + Date.now().toString().slice(-6),
              stoneMaterialLabel: this.stoneMaterials.find(m => m.value === this.orderForm.stoneMaterial)?.label,
              fontStyleLabel: this.fontStyles.find(f => f.value === this.orderForm.fontStyle)?.label,
              sideOptionLabel: this.sideOptions.find(s => s.value === this.orderForm.sideOption)?.label,
              currentStep: 1,
              stepUpdated: [false, false, false, false, false, false, false, false],
              createTime: new Date().toLocaleString('zh-CN'),
              createTimestamp: Date.now(),
              price: this.totalPrice,
              status: 'processing'
            }
            
            let orders = JSON.parse(localStorage.getItem('sealOrders') || '[]')
            orders.unshift(order)
            localStorage.setItem('sealOrders', JSON.stringify(orders))
            
            this.$message.success('订单提交成功！订单号：' + order.id)
            this.resetForm()
            
            this.$router.push({ path: '/admin', query: { newOrderId: order.id } })
          }, 1000)
        }
      })
    },
    resetForm() {
      this.$refs.orderForm.resetFields()
      this.orderForm.sideOption = 'none'
      this.orderForm.sideContent = ''
      this.orderForm.size = 2.5
    }
  }
}
</script>

<style scoped>
.order-page {
  max-width: 700px;
  margin: 0 auto;
}

.order-card {
  border-radius: 12px;
}

.card-header {
  font-size: 20px;
  font-weight: 600;
  color: #8B4513;
}

.order-form {
  padding: 10px 0;
}

.size-tip,
.content-tip {
  font-size: 12px;
  margin-top: 5px;
  padding: 4px 8px;
  border-radius: 4px;
}

.size-normal {
  color: #67c23a;
  background-color: #f0f9eb;
}

.size-warning {
  color: #e6a23c;
  background-color: #fdf6ec;
}

.size-tip i {
  margin-right: 4px;
}

.price-section {
  text-align: center;
  padding: 20px 0;
  background: linear-gradient(135deg, #fdf6e3 0%, #fef5e7 100%);
  border-radius: 8px;
  margin-bottom: 20px;
}

.price-label {
  font-size: 16px;
  color: #606266;
}

.price-value {
  font-size: 28px;
  font-weight: 700;
  color: #e6a23c;
  margin-left: 10px;
}

.submit-section {
  text-align: center;
  margin-top: 20px;
}

.submit-section .el-button {
  margin: 0 10px;
  min-width: 120px;
}
</style>
