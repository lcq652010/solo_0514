<template>
  <div class="page-container">
    <h2 class="page-title">
      <i class="el-icon-edit-outline"></i>
      定制您的专属茶盏
    </h2>

    <el-row :gutter="20">
      <el-col :span="16">
        <el-card class="card-shadow">
          <div slot="header" class="form-header">
            <span>订单信息填写</span>
          </div>

          <el-form
            ref="orderForm"
            :model="orderForm"
            :rules="rules"
            label-width="100px"
            label-position="right"
          >
            <el-divider content-position="left">
              <i class="el-icon-user"></i> 客户信息
            </el-divider>

            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="客户姓名" prop="customerName">
                  <el-input v-model="orderForm.customerName" placeholder="请输入姓名" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="联系电话" prop="phone">
                  <el-input v-model="orderForm.phone" placeholder="请输入手机号码" />
                </el-form-item>
              </el-col>
            </el-row>

            <el-divider content-position="left">
              <i class="el-icon-goods"></i> 定制参数
            </el-divider>

            <el-form-item label="泥料类型" prop="clayType">
              <el-radio-group v-model="orderForm.clayType">
                <el-radio
                  v-for="clay in clayTypes"
                  :key="clay.value"
                  :label="clay.label"
                  class="option-radio"
                >
                  <div class="option-content">
                    <span class="option-label">{{ clay.label }}</span>
                    <span class="option-desc">{{ clay.desc }}</span>
                  </div>
                </el-radio>
              </el-radio-group>
            </el-form-item>

            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="盏径尺寸" prop="size">
                  <el-input-number
                    v-model="orderForm.size"
                    :min="6"
                    :max="12"
                    :step="0.5"
                    :precision="1"
                    size="large"
                    style="width: 100%"
                    @change="handleSizeChange"
                  />
                  <span class="unit-label">厘米 (cm)</span>
                  <div class="quick-sizes">
                    <span class="quick-label">常用尺寸：</span>
                    <el-button
                      v-for="qs in quickSizes"
                      :key="qs.size"
                      size="mini"
                      :type="orderForm.size === qs.size ? 'primary' : 'default'"
                      @click="selectQuickSize(qs.size)"
                    >
                      {{ qs.label }} ({{ qs.size }}cm)
                    </el-button>
                  </div>
                  <div class="size-validation" :class="{ 'is-valid': sizeValid, 'is-invalid': !sizeValid }">
                    <i :class="sizeValid ? 'el-icon-circle-check' : 'el-icon-circle-close'"></i>
                    <span>{{ sizeTip }}</span>
                  </div>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <div class="size-preview">
                  <div class="size-circle" :style="{ width: previewSize + 'px', height: previewSize + 'px' }">
                    <span>{{ orderForm.size }} cm</span>
                  </div>
                  <span class="size-hint">尺寸预览</span>
                </div>
              </el-col>
            </el-row>

            <el-form-item label="釉色风格" prop="glazeStyle">
              <el-select v-model="orderForm.glazeStyle" placeholder="请选择釉色风格" size="large">
                <el-option
                  v-for="glaze in glazeStyles"
                  :key="glaze.value"
                  :label="glaze.label"
                  :value="glaze.label"
                >
                  <span style="float: left">{{ glaze.label }}</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">{{ glaze.desc }}</span>
                </el-option>
              </el-select>
            </el-form-item>

            <el-form-item label="纹饰绘制" prop="pattern">
              <el-radio-group v-model="orderForm.pattern" class="pattern-group">
                <el-radio-button
                  v-for="pattern in patterns"
                  :key="pattern.value"
                  :label="pattern.label"
                >
                  {{ pattern.label }}
                </el-radio-button>
              </el-radio-group>
              <p class="pattern-desc" v-if="selectedPatternDesc">
                <i class="el-icon-information"></i> {{ selectedPatternDesc }}
              </p>
            </el-form-item>

            <el-form-item label="器型款式" prop="shape">
              <el-radio-group v-model="orderForm.shape">
                <el-radio
                  v-for="shape in shapes"
                  :key="shape.value"
                  :label="shape.label"
                  class="option-radio"
                >
                  <div class="option-content">
                    <span class="option-label">{{ shape.label }}</span>
                    <span class="option-desc">{{ shape.desc }}</span>
                  </div>
                </el-radio>
              </el-radio-group>
            </el-form-item>

            <el-form-item label="特殊要求">
              <el-input
                v-model="orderForm.remark"
                type="textarea"
                :rows="3"
                placeholder="如有特殊要求请在此说明..."
              />
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                size="large"
                @click="submitOrder"
                :loading="submitting"
                class="submit-btn"
              >
                <i class="el-icon-check"></i>
                提交定制订单
              </el-button>
              <el-button size="large" @click="resetForm">
                <i class="el-icon-refresh-left"></i>
                重置表单
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card class="card-shadow summary-card">
          <div slot="header">
            <span><i class="el-icon-document"></i> 订单预览</span>
          </div>

          <div class="preview-content">
            <div class="preview-item">
              <span class="preview-label">客户姓名</span>
              <span class="preview-value">{{ orderForm.customerName || '未填写' }}</span>
            </div>
            <div class="preview-item">
              <span class="preview-label">联系电话</span>
              <span class="preview-value">{{ orderForm.phone || '未填写' }}</span>
            </div>

            <el-divider></el-divider>

            <div class="preview-item">
              <span class="preview-label">泥料类型</span>
              <span class="preview-value highlight">{{ orderForm.clayType || '未选择' }}</span>
            </div>
            <div class="preview-item">
              <span class="preview-label">盏径尺寸</span>
              <span class="preview-value highlight">{{ orderForm.size }} cm</span>
            </div>
            <div class="preview-item">
              <span class="preview-label">釉色风格</span>
              <span class="preview-value highlight">{{ orderForm.glazeStyle || '未选择' }}</span>
            </div>
            <div class="preview-item">
              <span class="preview-label">纹饰绘制</span>
              <span class="preview-value highlight">{{ orderForm.pattern || '未选择' }}</span>
            </div>
            <div class="preview-item">
              <span class="preview-label">器型款式</span>
              <span class="preview-value highlight">{{ orderForm.shape || '未选择' }}</span>
            </div>

            <el-divider></el-divider>

            <div class="preview-total">
              <span class="total-label">预估价格</span>
              <span class="total-value">¥ {{ estimatedPrice }}</span>
            </div>

            <div class="preview-tips">
              <el-alert
                title="温馨提示"
                type="info"
                :closable="false"
                description="定制周期约15-20天，完工后我们将第一时间通知您取货。"
              />
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { CLAY_TYPES, GLAZE_STYLES, PATTERNS, SHAPES, QUICK_SIZES, orderStore } from '../store/orderStore'
import { EventBus } from '../store/eventBus'

export default {
  name: 'OrderPage',
  data() {
    return {
      submitting: false,
      sizeValid: true,
      sizeTip: '尺寸在合法范围内 (6-12cm)',
      clayTypes: CLAY_TYPES,
      glazeStyles: GLAZE_STYLES,
      patterns: PATTERNS,
      shapes: SHAPES,
      quickSizes: QUICK_SIZES,
      orderForm: {
        customerName: '',
        phone: '',
        clayType: '',
        size: 9,
        glazeStyle: '',
        pattern: '',
        shape: '',
        remark: ''
      },
      rules: {
        customerName: [
          { required: true, message: '请输入客户姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '姓名长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ],
        clayType: [
          { required: true, message: '请选择泥料类型', trigger: 'change' }
        ],
        size: [
          { required: true, message: '请输入盏径尺寸', trigger: 'change' }
        ],
        glazeStyle: [
          { required: true, message: '请选择釉色风格', trigger: 'change' }
        ],
        pattern: [
          { required: true, message: '请选择纹饰绘制', trigger: 'change' }
        ],
        shape: [
          { required: true, message: '请选择器型款式', trigger: 'change' }
        ]
      }
    }
  },
  computed: {
    previewSize() {
      return 60 + (this.orderForm.size - 6) * 20
    },
    selectedPatternDesc() {
      const pattern = this.patterns.find(p => p.label === this.orderForm.pattern)
      return pattern ? pattern.desc : ''
    },
    estimatedPrice() {
      let price = 388
      if (this.orderForm.size > 9) price += 100
      if (this.orderForm.pattern && this.orderForm.pattern !== '无纹饰') price += 80
      if (this.orderForm.glazeStyle === '天目釉' || this.orderForm.glazeStyle === '钧釉') price += 120
      return price
    }
  },
  methods: {
    selectQuickSize(size) {
      this.orderForm.size = size
      this.handleSizeChange(size)
    },
    handleSizeChange(value) {
      if (value < 6 || value > 12) {
        this.sizeValid = false
        this.sizeTip = '尺寸超出范围！请输入 6-12cm 之间的数值'
      } else if (value < 7) {
        this.sizeValid = true
        this.sizeTip = '适合小品茶盏，适合品茗把玩'
      } else if (value > 10) {
        this.sizeValid = true
        this.sizeTip = '较大尺寸，适合大容量冲泡'
      } else {
        this.sizeValid = true
        this.sizeTip = '常规尺寸，适合日常品茗'
      }
    },
    submitOrder() {
      this.$refs.orderForm.validate(valid => {
        if (valid) {
          this.submitting = true
          setTimeout(() => {
            const newOrder = orderStore.addOrder({
              ...this.orderForm,
              price: this.estimatedPrice
            })
            this.submitting = false
            this.$message.success(`订单提交成功！订单号：${newOrder.id}`)
            EventBus.$emit('orderCreated', newOrder)
            this.showSuccessDialog(newOrder)
          }, 800)
        } else {
          this.$message.warning('请完善订单信息')
          return false
        }
      })
    },
    showSuccessDialog(order) {
      this.$alert(
        `您的定制订单已提交成功！\n\n订单号：${order.id}\n泥料：${order.clayType}\n尺寸：${order.size}cm\n釉色：${order.glazeStyle}\n纹饰：${order.pattern}\n器型：${order.shape}\n预估价格：¥${order.price}\n\n我们将尽快开始制作，预计15-20天完工。`,
        '提交成功',
        {
          confirmButtonText: '好的',
          callback: () => {
            this.resetForm()
          }
        }
      )
    },
    resetForm() {
      this.$refs.orderForm.resetFields()
      this.orderForm.size = 9
    }
  }
}
</script>

<style scoped>
.form-header {
  font-size: 18px;
  font-weight: bold;
  color: #5D4037;
}

.option-radio {
  display: block;
  margin-bottom: 12px;
  padding: 12px 16px;
  border: 1px solid #D7CCC8;
  border-radius: 6px;
  transition: all 0.3s;
}

.option-radio:hover {
  border-color: #8D6E63;
  background-color: #EFEBE9;
}

.option-radio >>> .el-radio__label {
  display: block;
  padding-left: 10px;
}

.option-content {
  display: flex;
  flex-direction: column;
}

.option-label {
  font-weight: 500;
  color: #3E2723;
  font-size: 15px;
}

.option-desc {
  color: #8D6E63;
  font-size: 13px;
  margin-top: 4px;
}

.unit-label {
  color: #8D6E63;
  margin-left: 10px;
  font-size: 14px;
}

.quick-sizes {
  margin-top: 10px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.quick-label {
  color: #8D6E63;
  font-size: 13px;
  margin-right: 4px;
}

.size-validation {
  margin-top: 8px;
  font-size: 13px;
  display: flex;
  align-items: center;
}

.size-validation i {
  margin-right: 6px;
  font-size: 14px;
}

.size-validation.is-valid {
  color: #2E7D32;
}

.size-validation.is-invalid {
  color: #C62828;
}

.size-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  background: #F5F5F5;
  border-radius: 8px;
}

.size-circle {
  border: 3px dashed #8D6E63;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: #5D4037;
  font-weight: bold;
  background: #FFF;
  transition: all 0.3s;
}

.size-hint {
  margin-top: 8px;
  font-size: 12px;
  color: #8D6E63;
}

.pattern-group >>> .el-radio-button__inner {
  padding: 12px 20px;
}

.pattern-desc {
  margin-top: 12px;
  color: #8D6E63;
  font-size: 13px;
  padding: 8px 12px;
  background: #F5F5F5;
  border-radius: 4px;
}

.pattern-desc i {
  margin-right: 6px;
  color: #FF9800;
}

.submit-btn {
  background: linear-gradient(135deg, #5D4037 0%, #795548 100%);
  border: none;
  padding: 0 30px;
}

.submit-btn:hover {
  background: linear-gradient(135deg, #6D4C41 0%, #8D6E63 100%);
}

.summary-card {
  position: sticky;
  top: 20px;
}

.preview-content {
  font-size: 14px;
}

.preview-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  align-items: center;
}

.preview-label {
  color: #8D6E63;
}

.preview-value {
  color: #3E2723;
  font-weight: 500;
}

.preview-value.highlight {
  color: #5D4037;
  font-weight: bold;
}

.preview-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.total-label {
  font-size: 16px;
  color: #5D4037;
  font-weight: 500;
}

.total-value {
  font-size: 28px;
  color: #E65100;
  font-weight: bold;
}

.preview-tips {
  margin-top: 16px;
}
</style>
