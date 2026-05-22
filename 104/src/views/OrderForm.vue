<template>
  <div class="order-form-container">
    <el-card class="order-card" shadow="hover">
      <div slot="header" class="card-header">
        <i class="el-icon-goods"></i>
        <span>定制您的专属锡制茶叶罐</span>
      </div>

      <el-form
        ref="orderForm"
        :model="orderForm"
        :rules="formRules"
        label-width="120px"
        label-position="left"
      >
        <el-divider content-position="left">
          <span class="divider-title"><i class="el-icon-user"></i> 客户信息</span>
        </el-divider>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="客户姓名" prop="customerName">
              <el-input v-model="orderForm.customerName" placeholder="请输入姓名" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="orderForm.phone" placeholder="请输入手机号" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">
          <span class="divider-title"><i class="el-icon-s-cooperation"></i> 材质与规格</span>
        </el-divider>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="锡料纯度" prop="tinPurity">
              <el-select v-model="orderForm.tinPurity" placeholder="请选择锡料纯度" style="width: 100%" @change="calculatePrice">
                <el-option
                  v-for="item in tinPurityOptions"
                  :key="item.value"
                  :label="item.label + ' (+' + item.price + '元/个)'"
                  :value="item.value"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="罐体高度 (mm)" prop="height">
              <el-input-number
                v-model="orderForm.height"
                :min="60"
                :max="250"
                :step="10"
                style="width: 100%"
                @change="calculatePrice"
              ></el-input-number>
              <div style="font-size: 12px; color: #909399; margin-top: 5px;">
                <i class="el-icon-info"></i> 建议范围：60-250mm（常规茶罐高度）
              </div>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="罐身直径 (mm)" prop="diameter">
              <el-input-number
                v-model="orderForm.diameter"
                :min="50"
                :max="180"
                :step="5"
                style="width: 100%"
                @change="calculatePrice"
              ></el-input-number>
              <div style="font-size: 12px; color: #909399; margin-top: 5px;">
                <i class="el-icon-info"></i> 建议范围：50-180mm（常规茶罐直径）
              </div>
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">
          <span class="divider-title"><i class="el-icon-picture"></i> 样式选择</span>
        </el-divider>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="盖型样式" prop="lidStyle">
              <el-radio-group v-model="orderForm.lidStyle" @change="calculatePrice">
                <el-radio-button
                  v-for="item in lidStyleOptions"
                  :key="item.value"
                  :label="item.value"
                >
                  {{ item.label }}
                  <span v-if="item.price > 0" class="price-tag">+{{ item.price }}元</span>
                </el-radio-button>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="錾刻花纹" prop="pattern">
          <el-radio-group v-model="orderForm.pattern" @change="calculatePrice">
            <el-radio
              v-for="item in patternOptions"
              :key="item.value"
              :label="item.value"
              border
            >
              <span class="pattern-label">{{ item.label }}</span>
              <span v-if="item.price > 0" class="price-tag-small">+{{ item.price }}元</span>
            </el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="备注说明">
          <el-input
            v-model="orderForm.remark"
            type="textarea"
            :rows="3"
            placeholder="如有特殊要求请在此说明，如刻字内容、定制需求等..."
          ></el-input>
        </el-form-item>

        <el-divider></el-divider>

        <div class="price-section">
          <div class="price-label">预估总价：</div>
          <div class="price-value">¥ {{ totalPrice }}</div>
        </div>

        <el-form-item class="submit-section">
          <el-button type="primary" size="large" @click="submitOrder" :loading="submitting">
            <i class="el-icon-check"></i>
            提交订单
          </el-button>
          <el-button size="large" @click="resetForm">
            <i class="el-icon-refresh"></i>
            重置表单
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import orderStore from '../store/orderStore'

export default {
  name: 'OrderForm',
  data() {
    return {
      tinPurityOptions: orderStore.getTinPurityOptions(),
      lidStyleOptions: orderStore.getLidStyleOptions(),
      patternOptions: orderStore.getPatternOptions(),
      orderForm: {
        customerName: '',
        phone: '',
        tinPurity: '999',
        height: 100,
        diameter: 70,
        lidStyle: 'flat',
        pattern: 'none',
        remark: ''
      },
      formRules: {
        customerName: [
          { required: true, message: '请输入客户姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '姓名长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ],
        tinPurity: [
          { required: true, message: '请选择锡料纯度', trigger: 'change' }
        ],
        height: [
          { required: true, message: '请输入罐体高度', trigger: 'blur' },
          { type: 'number', min: 60, max: 250, message: '罐体高度需在 60-250mm 之间', trigger: 'blur' }
        ],
        diameter: [
          { required: true, message: '请输入罐身直径', trigger: 'blur' },
          { type: 'number', min: 50, max: 180, message: '罐身直径需在 50-180mm 之间', trigger: 'blur' }
        ],
        lidStyle: [
          { required: true, message: '请选择盖型样式', trigger: 'change' }
        ],
        pattern: [
          { required: true, message: '请选择錾刻花纹', trigger: 'change' }
        ]
      },
      submitting: false
    }
  },
  computed: {
    totalPrice() {
      let price = 0

      const purityOption = this.tinPurityOptions.find(p => p.value === this.orderForm.tinPurity)
      if (purityOption) {
        price += purityOption.price
      }

      const baseSizePrice = Math.round((this.orderForm.height * this.orderForm.diameter) / 200)
      price += baseSizePrice

      const lidOption = this.lidStyleOptions.find(l => l.value === this.orderForm.lidStyle)
      if (lidOption) {
        price += lidOption.price
      }

      const patternOption = this.patternOptions.find(p => p.value === this.orderForm.pattern)
      if (patternOption) {
        price += patternOption.price
      }

      return price
    }
  },
  methods: {
    calculatePrice() {
    },
    submitOrder() {
      this.$refs.orderForm.validate((valid) => {
        if (valid) {
          this.submitting = true

          const tinPurityOption = this.tinPurityOptions.find(p => p.value === this.orderForm.tinPurity)
          const lidStyleOption = this.lidStyleOptions.find(l => l.value === this.orderForm.lidStyle)
          const patternOption = this.patternOptions.find(p => p.value === this.orderForm.pattern)

          const orderData = {
            customerName: this.orderForm.customerName,
            phone: this.orderForm.phone,
            tinPurity: this.orderForm.tinPurity,
            tinPurityLabel: tinPurityOption ? tinPurityOption.label : '',
            height: this.orderForm.height,
            diameter: this.orderForm.diameter,
            lidStyle: this.orderForm.lidStyle,
            lidStyleLabel: lidStyleOption ? lidStyleOption.label : '',
            pattern: this.orderForm.pattern,
            patternLabel: patternOption ? patternOption.label : '',
            totalPrice: this.totalPrice,
            remark: this.orderForm.remark
          }

          const newOrder = orderStore.addOrder(orderData)

          setTimeout(() => {
            this.submitting = false
            this.$alert(
              `<div style="text-align: center;">
                <p style="font-size: 16px; margin-bottom: 10px;">订单提交成功！</p>
                <p style="color: #606266;">订单编号：<strong style="color: #d4af37;">${newOrder.id}</strong></p>
                <p style="color: #606266; margin-top: 5px;">我们将尽快为您安排生产</p>
              </div>`,
              '提交成功',
              {
                confirmButtonText: '确定',
                dangerouslyUseHTMLString: true,
                type: 'success'
              }
            ).then(() => {
              this.resetForm()
            })
          }, 1000)
        } else {
          this.$message.error('请完善表单信息')
          return false
        }
      })
    },
    resetForm() {
      this.$refs.orderForm.resetFields()
      this.orderForm.tinPurity = '999'
      this.orderForm.height = 100
      this.orderForm.diameter = 70
      this.orderForm.lidStyle = 'flat'
      this.orderForm.pattern = 'none'
      this.orderForm.remark = ''
      this.$message.success('表单已重置')
    }
  }
}
</script>

<style scoped>
.order-form-container {
  max-width: 900px;
  margin: 0 auto;
}

.order-card {
  border-radius: 12px;
}

.card-header {
  display: flex;
  align-items: center;
  font-size: 20px;
  font-weight: bold;
  color: #2c3e50;
}

.card-header i {
  font-size: 24px;
  margin-right: 10px;
  color: #d4af37;
}

.divider-title {
  font-size: 16px;
  font-weight: 600;
  color: #34495e;
}

.divider-title i {
  margin-right: 6px;
  color: #d4af37;
}

.price-tag {
  font-size: 12px;
  color: #e74c3c;
  margin-left: 4px;
}

.price-tag-small {
  font-size: 12px;
  color: #e74c3c;
  margin-left: 8px;
}

.pattern-label {
  font-size: 14px;
}

.price-section {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 20px;
  background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 8px;
  margin-bottom: 20px;
}

.price-label {
  font-size: 18px;
  color: #6c757d;
  margin-right: 10px;
}

.price-value {
  font-size: 32px;
  font-weight: bold;
  color: #e74c3c;
}

.submit-section {
  text-align: center;
  margin-top: 20px;
}

.submit-section .el-button {
  margin: 0 10px;
  min-width: 150px;
}

.el-form-item {
  margin-bottom: 22px;
}

.el-radio {
  margin-right: 15px;
  margin-bottom: 10px;
}
</style>
