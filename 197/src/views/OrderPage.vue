<template>
  <div class="page-container">
    <div class="page-header">
      <h1>宣纸笺定制</h1>
      <p class="subtitle">传承千年工艺，定制专属宣纸</p>
      <div class="decoration"></div>
    </div>

    <div class="order-content">
      <el-form
        ref="orderForm"
        :model="formData"
        :rules="rules"
        label-width="100px"
        class="order-form"
      >
        <div class="form-section card">
          <div class="section-title">
            <span class="title-icon">📜</span>
            <h3>基础信息</h3>
          </div>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="客户姓名" prop="customerName">
                <el-input v-model="formData.customerName" placeholder="请输入您的姓名" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="联系电话" prop="customerPhone">
                <el-input v-model="formData.customerPhone" placeholder="请输入联系电话" />
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <div class="form-section card">
          <div class="section-title">
            <span class="title-icon">📄</span>
            <h3>宣纸品类</h3>
          </div>
          <el-form-item prop="category">
            <el-select v-model="formData.category" placeholder="请选择宣纸品类" class="full-width">
              <el-option
                v-for="item in paperCategories"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              >
                <span style="float: left">{{ item.label }}</span>
                <span style="float: right; color: #8492a6; font-size: 13px">
                  ¥{{ item.price }}/张 - {{ item.desc }}
                </span>
              </el-option>
            </el-select>
          </el-form-item>
        </div>

        <div class="form-section card">
          <div class="section-title">
            <span class="title-icon">📐</span>
            <h3>尺寸规格</h3>
          </div>
          <el-form-item label="常用规格" class="preset-item">
            <div class="preset-buttons">
              <el-tooltip
                v-for="preset in sizePresets"
                :key="preset.name"
                :content="preset.width + 'cm × ' + preset.height + 'cm'"
                placement="top"
              >
                <el-button
                  :type="selectedPreset === preset.name ? 'primary' : 'default'"
                  size="small"
                  :class="{ 'is-active': selectedPreset === preset.name }"
                  @click="selectPreset(preset.name)"
                >
                  <span class="preset-name">{{ preset.name }}</span>
                  <span class="preset-size">{{ preset.width }}×{{ preset.height }}</span>
                </el-button>
              </el-tooltip>
            </div>
          </el-form-item>
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="宽度(cm)" prop="size.width">
                <el-input-number
                  v-model="formData.size.width"
                  :min="10"
                  :max="300"
                  :step="0.5"
                  class="full-width"
                />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="高度(cm)" prop="size.height">
                <el-input-number
                  v-model="formData.size.height"
                  :min="10"
                  :max="300"
                  :step="0.5"
                  class="full-width"
                />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="数量" prop="quantity">
                <el-input-number
                  v-model="formData.quantity"
                  :min="1"
                  :max="1000"
                  class="full-width"
                />
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <div class="form-section card">
          <div class="section-title">
            <span class="title-icon">🎨</span>
            <h3>帘纹款式</h3>
          </div>
          <el-form-item prop="curtainPattern">
            <el-radio-group v-model="formData.curtainPattern" class="pattern-group">
              <el-radio v-for="item in curtainPatterns" :key="item.value" :label="item.value" border>
                {{ item.label }}
              </el-radio>
            </el-radio-group>
          </el-form-item>
        </div>

        <div class="form-section card">
          <div class="section-title">
            <span class="title-icon">✨</span>
            <h3>描金工艺</h3>
          </div>
          <el-form-item prop="goldProcesses">
            <el-checkbox-group v-model="formData.goldProcesses" class="process-group">
              <el-checkbox
                v-for="item in goldProcessOptions"
                :key="item.value"
                :label="item.value"
                border
              >
                {{ item.label }} <span class="price-tag">+¥{{ item.price }}</span>
              </el-checkbox>
            </el-checkbox-group>
          </el-form-item>
        </div>

        <div class="form-section card">
          <div class="section-title">
            <span class="title-icon">🎁</span>
            <h3>包装方式</h3>
          </div>
          <el-form-item prop="packaging">
            <el-radio-group v-model="formData.packaging" class="packaging-group">
              <el-radio
                v-for="item in packagingOptions"
                :key="item.value"
                :label="item.value"
                border
              >
                <div class="packaging-item">
                  <span class="packaging-name">{{ item.label }}</span>
                  <span class="packaging-price">+¥{{ item.price }}</span>
                  <span class="packaging-desc">{{ item.desc }}</span>
                </div>
              </el-radio>
            </el-radio-group>
          </el-form-item>
        </div>

        <div class="form-section card">
          <div class="section-title">
            <span class="title-icon">📝</span>
            <h3>备注信息</h3>
          </div>
          <el-form-item label="特殊要求" prop="remark">
            <el-input
              v-model="formData.remark"
              type="textarea"
              :rows="3"
              placeholder="请填写特殊要求或说明"
            />
          </el-form-item>
        </div>

        <div class="submit-section card">
          <div class="price-preview">
            <div class="price-detail">
              <div class="price-row">
                <span>纸张费用</span>
                <span>¥{{ paperPrice.toFixed(2) }}</span>
              </div>
              <div class="price-row" v-if="goldPrice > 0">
                <span>描金工艺</span>
                <span>¥{{ goldPrice.toFixed(2) }}</span>
              </div>
              <div class="price-row">
                <span>包装费用</span>
                <span>¥{{ packagingPrice.toFixed(2) }}</span>
              </div>
              <div class="price-row total">
                <span>总计</span>
                <span class="total-price">¥{{ totalPrice.toFixed(2) }}</span>
              </div>
            </div>
          </div>
          <div class="submit-buttons">
            <el-button type="primary" size="large" :loading="submitting" @click="submitOrder">
              提交订单
            </el-button>
            <el-button size="large" @click="resetForm">重置</el-button>
          </div>
        </div>
      </el-form>
    </div>

    <el-dialog
      :visible.sync="showSuccess"
      width="600px"
      :close-on-click-modal="false"
      class="success-dialog"
    >
      <div class="success-content">
        <div class="success-icon">✓</div>
        <h3>订单提交成功！</h3>
        <p class="order-no">订单编号：{{ newOrderId }}</p>

        <div class="order-receipt" v-if="submittedOrder && submittedOrder.id">
          <div class="receipt-header">
            <span class="receipt-title">订单详情回执</span>
            <span class="receipt-time">{{ submittedOrder.createdAt }}</span>
          </div>
          <div class="receipt-body">
            <div class="receipt-row">
              <span class="label">客户姓名</span>
              <span class="value">{{ submittedOrder.customerName }}</span>
            </div>
            <div class="receipt-row">
              <span class="label">联系电话</span>
              <span class="value">{{ submittedOrder.customerPhone }}</span>
            </div>
            <div class="receipt-row">
              <span class="label">宣纸品类</span>
              <span class="value">{{ submittedOrder.category }}</span>
            </div>
            <div class="receipt-row">
              <span class="label">尺寸规格</span>
              <span class="value">
                {{ submittedOrder.size.width }}cm × {{ submittedOrder.size.height }}cm
                <span v-if="submittedOrder.size.name">（{{ submittedOrder.size.name }}）</span>
              </span>
            </div>
            <div class="receipt-row">
              <span class="label">帘纹款式</span>
              <span class="value">{{ submittedOrder.curtainPattern }}</span>
            </div>
            <div class="receipt-row">
              <span class="label">描金工艺</span>
              <span class="value">
                {{ submittedOrder.goldProcesses && submittedOrder.goldProcesses.length > 0 ? submittedOrder.goldProcesses.join('、') : '无' }}
              </span>
            </div>
            <div class="receipt-row">
              <span class="label">包装方式</span>
              <span class="value">{{ submittedOrder.packaging }}</span>
            </div>
            <div class="receipt-row">
              <span class="label">购买数量</span>
              <span class="value">{{ submittedOrder.quantity }}张</span>
            </div>
            <div class="receipt-row total-row">
              <span class="label">订单总价</span>
              <span class="value total-price">¥{{ totalPrice.toFixed(2) }}</span>
            </div>
          </div>
        </div>

        <p class="success-tip">我们将尽快为您安排生产，请耐心等待</p>
        <div class="success-buttons">
          <el-button type="primary" @click="goAdmin">进入管理后台</el-button>
          <el-button @click="continueOrder">继续下单</el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import {
  paperCategories,
  sizePresets,
  curtainPatterns,
  goldProcessOptions,
  packagingOptions
} from '@/mock/data.js'
import { addOrder, generateOrderId, formatDateTime, createEmptySteps } from '@/utils/storage.js'

export default {
  name: 'OrderPage',
  data() {
    return {
      paperCategories,
      sizePresets,
      curtainPatterns,
      goldProcessOptions,
      packagingOptions,
      selectedPreset: '',
      submitting: false,
      showSuccess: false,
      newOrderId: '',
      submittedOrder: {},
      formData: {
        customerName: '',
        customerPhone: '',
        category: '',
        size: {
          width: 138,
          height: 69,
          name: ''
        },
        curtainPattern: '',
        goldProcesses: [],
        packaging: '',
        quantity: 10,
        remark: ''
      },
      rules: {
        customerName: [
          { required: true, message: '请输入客户姓名', trigger: 'blur' }
        ],
        customerPhone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ],
        category: [
          { required: true, message: '请选择宣纸品类', trigger: 'change' }
        ],
        curtainPattern: [
          { required: true, message: '请选择帘纹款式', trigger: 'change' }
        ],
        packaging: [
          { required: true, message: '请选择包装方式', trigger: 'change' }
        ],
        'size.width': [
          { required: true, message: '请输入宽度', trigger: 'blur' },
          { type: 'number', message: '请输入有效的数字', trigger: 'blur' },
          { validator: this.validatePositiveNumber, trigger: 'blur' }
        ],
        'size.height': [
          { required: true, message: '请输入高度', trigger: 'blur' },
          { type: 'number', message: '请输入有效的数字', trigger: 'blur' },
          { validator: this.validatePositiveNumber, trigger: 'blur' }
        ],
        quantity: [
          { required: true, message: '请输入数量', trigger: 'blur' },
          { type: 'number', message: '请输入有效的数字', trigger: 'blur' },
          { validator: this.validatePositiveInteger, trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    paperPrice() {
      const category = this.paperCategories.find(c => c.value === this.formData.category)
      const price = category ? category.price : 0
      return price * this.formData.quantity
    },
    goldPrice() {
      return this.formData.goldProcesses.reduce((total, process) => {
        const item = this.goldProcessOptions.find(p => p.value === process)
        return total + (item ? item.price * this.formData.quantity : 0)
      }, 0)
    },
    packagingPrice() {
      const packaging = this.packagingOptions.find(p => p.value === this.formData.packaging)
      return packaging ? packaging.price * this.formData.quantity : 0
    },
    totalPrice() {
      return this.paperPrice + this.goldPrice + this.packagingPrice
    }
  },
  methods: {
    validatePositiveNumber(rule, value, callback) {
      if (value === '' || value === null || value === undefined) {
        callback(new Error('请输入数值'))
      } else if (typeof value !== 'number' || isNaN(value)) {
        callback(new Error('请输入有效的数字'))
      } else if (value <= 0) {
        callback(new Error('请输入大于0的数值'))
      } else {
        callback()
      }
    },
    validatePositiveInteger(rule, value, callback) {
      if (value === '' || value === null || value === undefined) {
        callback(new Error('请输入数量'))
      } else if (!Number.isInteger(value)) {
        callback(new Error('请输入整数'))
      } else if (value <= 0) {
        callback(new Error('请输入大于0的整数'))
      } else {
        callback()
      }
    },
    selectPreset(presetName) {
      if (this.selectedPreset === presetName) {
        this.selectedPreset = ''
        this.formData.size.name = ''
      } else {
        this.selectedPreset = presetName
        const preset = this.sizePresets.find(p => p.name === presetName)
        if (preset) {
          this.formData.size.width = preset.width
          this.formData.size.height = preset.height
          this.formData.size.name = preset.name
        }
      }
    },
    submitOrder() {
      this.$refs.orderForm.validate(valid => {
        if (valid) {
          this.submitting = true
          setTimeout(() => {
            const orderId = generateOrderId()
            const order = {
              id: orderId,
              category: this.formData.category,
              size: { ...this.formData.size },
              curtainPattern: this.formData.curtainPattern,
              goldProcesses: [...this.formData.goldProcesses],
              packaging: this.formData.packaging,
              quantity: this.formData.quantity,
              remark: this.formData.remark,
              status: 'pending',
              currentStep: 0,
              customerName: this.formData.customerName,
              customerPhone: this.formData.customerPhone,
              createdAt: formatDateTime(new Date()),
              steps: createEmptySteps()
            }
            addOrder(order)
            this.newOrderId = orderId
            this.submittedOrder = { ...order }
            this.submitting = false
            this.showSuccess = true
            this.markAsNewOrder(orderId)
          }, 800)
        }
      })
    },
    resetForm() {
      this.$refs.orderForm.resetFields()
      this.selectedPreset = ''
      this.formData.size = { width: 138, height: 69, name: '' }
      this.formData.goldProcesses = []
    },
    goAdmin() {
      this.showSuccess = false
      this.$router.push('/admin/login')
    },
    continueOrder() {
      this.showSuccess = false
      this.resetForm()
    },
    markAsNewOrder(orderId) {
      const newOrders = JSON.parse(localStorage.getItem('xuanzhi_new_orders') || '[]')
      if (!newOrders.includes(orderId)) {
        newOrders.push(orderId)
        localStorage.setItem('xuanzhi_new_orders', JSON.stringify(newOrders))
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.order-content {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 20px 60px;
  position: relative;
  z-index: 1;
}

.order-form {
  .form-section {
    padding: 25px;
    margin-bottom: 20px;

    .section-title {
      display: flex;
      align-items: center;
      margin-bottom: 20px;
      padding-bottom: 15px;
      border-bottom: 1px solid rgba(196, 30, 58, 0.1);

      .title-icon {
        font-size: 24px;
        margin-right: 10px;
      }

      h3 {
        font-family: "KaiTi", "楷体", serif;
        font-size: 20px;
        color: #1A1A1A;
        margin: 0;
      }
    }
  }

  .full-width {
    width: 100%;
  }

  .preset-item {
    .preset-buttons {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;

      .el-button {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 10px 16px;
        height: auto;
        border-radius: 8px;
        transition: all 0.3s ease;
        background: #fff;
        border: 1px solid #dcdfe6;

        .preset-name {
          font-weight: 600;
          font-size: 13px;
          color: #1A1A1A;
        }

        .preset-size {
          font-size: 11px;
          color: #909399;
          margin-top: 2px;
        }

        &:hover {
          border-color: #C41E3A;
          color: #C41E3A;
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(196, 30, 58, 0.15);
        }

        &.is-active,
        &.el-button--primary {
          background: linear-gradient(135deg, #C41E3A 0%, #A01830 100%);
          border-color: #C41E3A;
          color: #fff;
          box-shadow: 0 4px 12px rgba(196, 30, 58, 0.3);

          .preset-name,
          .preset-size {
            color: #fff;
          }
        }
      }
    }
  }

  .pattern-group {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }

  .process-group {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;

    .price-tag {
      color: #C41E3A;
      font-size: 12px;
    }
  }

  .packaging-group {
    >>> .el-radio {
      margin-right: 15px;
      margin-bottom: 15px;
    }

    .packaging-item {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      padding: 5px 0;

      .packaging-name {
        font-weight: 600;
        color: #1A1A1A;
      }

      .packaging-price {
        color: #C41E3A;
        font-size: 14px;
      }

      .packaging-desc {
        color: #8B7355;
        font-size: 12px;
      }
    }
  }
}

.submit-section {
  padding: 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 30px;

  .price-preview {
    flex: 1;

    .price-detail {
      .price-row {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        font-size: 14px;

        &.total {
          border-top: 1px solid rgba(196, 30, 58, 0.2);
          margin-top: 10px;
          padding-top: 15px;
          font-size: 16px;
          font-weight: 600;

          .total-price {
            color: #C41E3A;
            font-size: 24px;
          }
        }
      }
    }
  }

  .submit-buttons {
    display: flex;
    gap: 15px;
  }
}

.success-dialog {
  >>> .el-dialog__body {
    padding: 40px;
    text-align: center;
  }

  .success-content {
    .success-icon {
      width: 80px;
      height: 80px;
      line-height: 80px;
      border-radius: 50%;
      background: #67C23A;
      color: #fff;
      font-size: 40px;
      margin: 0 auto 20px;
      animation: scaleIn 0.5s ease;
    }

    @keyframes scaleIn {
      0% { transform: scale(0); }
      50% { transform: scale(1.2); }
      100% { transform: scale(1); }
    }

    h3 {
      font-size: 24px;
      color: #1A1A1A;
      margin-bottom: 15px;
    }

    .order-no {
      font-size: 18px;
      color: #C41E3A;
      margin-bottom: 20px;
      font-weight: 600;
    }

    .order-receipt {
      background: #F8F5EE;
      border: 1px solid rgba(196, 30, 58, 0.15);
      border-radius: 8px;
      margin-bottom: 20px;
      text-align: left;

      .receipt-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 20px;
        border-bottom: 1px dashed rgba(196, 30, 58, 0.2);
        background: rgba(196, 30, 58, 0.03);
        border-radius: 8px 8px 0 0;

        .receipt-title {
          font-weight: 600;
          color: #5D4E37;
        }

        .receipt-time {
          font-size: 12px;
          color: #8B7355;
        }
      }

      .receipt-body {
        padding: 15px 20px;

        .receipt-row {
          display: flex;
          justify-content: space-between;
          padding: 8px 0;
          font-size: 14px;
          border-bottom: 1px solid rgba(93, 78, 55, 0.05);

          &:last-child {
            border-bottom: none;
          }

          .label {
            color: #8B7355;
          }

          .value {
            color: #1A1A1A;
            font-weight: 500;
          }

          &.total-row {
            margin-top: 8px;
            padding-top: 12px;
            border-top: 1px dashed rgba(196, 30, 58, 0.2);
            border-bottom: none;

            .label {
              font-weight: 600;
              font-size: 15px;
            }

            .total-price {
              color: #C41E3A;
              font-size: 20px;
              font-weight: 600;
            }
          }
        }
      }
    }

    .success-tip {
      color: #8B7355;
      margin-bottom: 20px;
    }

    .success-buttons {
      .el-button + .el-button {
        margin-left: 15px;
      }
    }
  }
}

@media (max-width: 768px) {
  .submit-section {
    flex-direction: column;
  }
}
</style>
