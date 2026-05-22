<template>
  <div class="order-form-page">
    <div class="page-container">
      <h1 class="page-title">
        <i class="el-icon-edit-outline"></i>
        定制您的专属藤编果篮
      </h1>

      <el-row :gutter="24">
        <el-col :xs="24" :md="14">
          <el-form
            ref="orderForm"
            :model="form"
            :rules="rules"
            label-width="100px"
            class="card order-form"
          >
            <div class="section-title">
              <i class="el-icon-set-up"></i>
              基础配置
            </div>

            <el-form-item label="藤条材质" prop="material">
              <el-select v-model="form.material" placeholder="请选择藤条材质" style="width: 100%">
                <el-option
                  v-for="item in materialOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                >
                  <span style="float: left">{{ item.label }}</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">
                    {{ item.desc }}
                    <span v-if="item.price > 0" class="price-tag">+¥{{ item.price }}</span>
                  </span>
                </el-option>
              </el-select>
            </el-form-item>

            <el-row :gutter="16">
              <el-col :span="12">
                <el-form-item label="果篮高度" prop="height">
                  <el-input-number
                    v-model="form.height"
                    :min="10"
                    :max="60"
                    :step="5"
                    controls-position="right"
                    style="width: 100%"
                  ></el-input-number>
                  <span class="unit">cm</span>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="口径大小" prop="diameter">
                  <el-input-number
                    v-model="form.diameter"
                    :min="15"
                    :max="80"
                    :step="5"
                    controls-position="right"
                    style="width: 100%"
                  ></el-input-number>
                  <span class="unit">cm</span>
                </el-form-item>
              </el-col>
            </el-row>

            <div class="section-title">
              <i class="el-icon-brush"></i>
              款式选择
            </div>

            <el-form-item label="编织款式" prop="style">
              <el-radio-group v-model="form.style" class="style-radio-group">
                <el-radio-button
                  v-for="item in styleOptions"
                  :key="item.value"
                  :label="item.value"
                >
                  <div class="radio-content">
                    <span class="radio-label">{{ item.label }}</span>
                    <span class="radio-desc">{{ item.desc }}</span>
                  </div>
                </el-radio-button>
              </el-radio-group>
            </el-form-item>

            <el-form-item label="提手配置" prop="handle">
              <el-radio-group v-model="form.handle" class="style-radio-group">
                <el-radio-button
                  v-for="item in handleOptions"
                  :key="item.value"
                  :label="item.value"
                >
                  <div class="radio-content">
                    <span class="radio-label">{{ item.label }}</span>
                    <span v-if="item.price > 0" class="radio-price">+¥{{ item.price }}</span>
                  </div>
                </el-radio-button>
              </el-radio-group>
            </el-form-item>

            <div class="section-title">
              <i class="el-icon-phone"></i>
              联系方式
            </div>

            <el-form-item label="手机号码" prop="contact">
              <el-input
                v-model="form.contact"
                placeholder="请输入您的手机号码"
                maxlength="11"
                clearable
              ></el-input>
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                size="large"
                :loading="submitting"
                @click="handleSubmit"
                class="submit-btn"
              >
                <i class="el-icon-check"></i>
                提交定制订单
              </el-button>
              <el-button size="large" @click="handleReset">
                重置
              </el-button>
            </el-form-item>
          </el-form>
        </el-col>

        <el-col :xs="24" :md="10">
          <div class="card preview-card">
            <div class="section-title">
              <i class="el-icon-view"></i>
              定制预览
            </div>

            <div class="basket-preview">
              <div class="basket-svg">
                <svg viewBox="0 0 200 220" width="100%" height="100%">
                  <defs>
                    <linearGradient :id="basketGradId" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" :style="`stop-color:${basketColor.light}`" />
                      <stop offset="100%" :style="`stop-color:${basketColor.dark}`" />
                    </linearGradient>
                  </defs>
                  
                  <ellipse cx="100" cy="180" :rx="basketWidth" :ry="20" :fill="`url(#${basketGradId})`" opacity="0.8"/>
                  
                  <path
                    :d="basketPath"
                    :fill="`url(#${basketGradId})`"
                    stroke="#5D4037"
                    stroke-width="1"
                  />
                  
                  <path
                    v-for="(line, idx) in weaveLines"
                    :key="idx"
                    :d="line"
                    fill="none"
                    :stroke="basketColor.dark"
                    stroke-width="0.8"
                    opacity="0.4"
                  />
                  
                  <ellipse cx="100" cy="50" :rx="basketWidth" :ry="15" fill="none" :stroke="basketColor.dark" stroke-width="2"/>
                  
                  <path
                    v-if="hasHandle"
                    :d="handlePath"
                    fill="none"
                    :stroke="basketColor.dark"
                    stroke-width="4"
                    stroke-linecap="round"
                  />
                </svg>
              </div>

              <div class="preview-info">
                <div class="info-item">
                  <span class="label">材质</span>
                  <span class="value">{{ form.material || '未选择' }}</span>
                </div>
                <div class="info-item">
                  <span class="label">尺寸</span>
                  <span class="value">{{ form.height || '-' }}cm × {{ form.diameter || '-' }}cm</span>
                </div>
                <div class="info-item">
                  <span class="label">款式</span>
                  <span class="value">{{ form.style || '未选择' }}</span>
                </div>
                <div class="info-item">
                  <span class="label">提手</span>
                  <span class="value">{{ form.handle || '未选择' }}</span>
                </div>
              </div>
            </div>

            <div class="price-section">
              <div class="price-row">
                <span>基础价格</span>
                <span>¥99</span>
              </div>
              <div class="price-row" v-if="materialPrice > 0">
                <span>材质加价</span>
                <span class="add">+¥{{ materialPrice }}</span>
              </div>
              <div class="price-row" v-if="handlePrice > 0">
                <span>提手加价</span>
                <span class="add">+¥{{ handlePrice }}</span>
              </div>
              <div class="price-row total">
                <span>预估总价</span>
                <span class="total-price">¥{{ totalPrice }}</span>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>

    <el-dialog
      :visible.sync="successVisible"
      title="订单提交成功"
      width="500px"
      :close-on-click-modal="false"
      class="success-dialog"
    >
      <div class="success-content">
        <div class="success-icon">
          <i class="el-icon-circle-check"></i>
        </div>
        <p class="success-text">您的定制订单已提交成功！</p>
        <div class="order-info-box">
          <p>订单号：<span class="order-id">{{ createdOrder && createdOrder.id }}</span></p>
          <p>我们将尽快为您安排生产，请保持手机畅通。</p>
        </div>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="goToAdmin">
          <i class="el-icon-setting"></i>
          查看生产进度
        </el-button>
        <el-button @click="successVisible = false; handleReset()">
          继续定制
        </el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { materialOptions, styleOptions, handleOptions } from '../mock/orders'

export default {
  name: 'OrderForm',
  data() {
    return {
      submitting: false,
      successVisible: false,
      createdOrder: null,
      basketGradId: 'basketGradient_' + Date.now(),
      form: {
        material: '',
        height: null,
        diameter: null,
        style: '',
        handle: '',
        contact: ''
      },
      rules: {
        material: [
          { required: true, message: '请选择藤条材质', trigger: 'change' }
        ],
        height: [
          { required: true, message: '请输入果篮高度', trigger: 'blur' }
        ],
        diameter: [
          { required: true, message: '请输入口径大小', trigger: 'blur' }
        ],
        style: [
          { required: true, message: '请选择编织款式', trigger: 'change' }
        ],
        handle: [
          { required: true, message: '请选择提手配置', trigger: 'change' }
        ],
        contact: [
          { required: true, message: '请输入手机号码', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ]
      },
      materialOptions,
      styleOptions,
      handleOptions
    }
  },
  computed: {
    materialPrice() {
      const item = this.materialOptions.find(m => m.value === this.form.material)
      return item ? item.price : 0
    },
    handlePrice() {
      const item = this.handleOptions.find(h => h.value === this.form.handle)
      return item ? item.price : 0
    },
    totalPrice() {
      return 99 + this.materialPrice + this.handlePrice
    },
    basketColor() {
      const colorMap = {
        '白藤': { light: '#F5F5DC', dark: '#D2B48C' },
        '红藤': { light: '#CD853F', dark: '#8B4513' },
        '黄藤': { light: '#DAA520', dark: '#B8860B' },
        '紫竹藤': { light: '#4A4A4A', dark: '#2D2D2D' }
      }
      return colorMap[this.form.material] || { light: '#F5F5DC', dark: '#D2B48C' }
    },
    basketWidth() {
      const diameter = this.form.diameter || 30
      return Math.min(90, 50 + (diameter - 30) * 1.5)
    },
    basketHeight() {
      const height = this.form.height || 25
      return Math.min(130, 100 + (height - 25) * 2)
    },
    basketPath() {
      const w = this.basketWidth
      const h = this.basketHeight
      const bottomY = 180
      const topY = bottomY - h
      return `M ${100 - w} ${topY} 
              Q ${100 - w * 1.1} ${topY + h * 0.3} ${100 - w * 0.9} ${bottomY}
              L ${100 + w * 0.9} ${bottomY}
              Q ${100 + w * 1.1} ${topY + h * 0.3} ${100 + w} ${topY}
              Z`
    },
    hasHandle() {
      return this.form.handle && this.form.handle !== '无提手'
    },
    handlePath() {
      const w = this.basketWidth
      const topY = 50
      if (this.form.handle === '单提手') {
        return `M ${100 - w * 0.5} ${topY} Q 100 ${topY - 60} ${100 + w * 0.5} ${topY}`
      } else if (this.form.handle === '双提手') {
        return `M ${100 - w * 0.8} ${topY} Q ${100 - w * 0.6} ${topY - 40} ${100 - w * 0.3} ${topY}
                M ${100 + w * 0.3} ${topY} Q ${100 + w * 0.6} ${topY - 40} ${100 + w * 0.8} ${topY}`
      } else {
        return `M ${100 - w * 0.6} ${topY} Q 100 ${topY - 50} ${100 + w * 0.6} ${topY}
                M ${100 - w * 0.3} ${topY - 25} Q 100 ${topY - 15} ${100 + w * 0.3} ${topY - 25}`
      }
    },
    weaveLines() {
      const lines = []
      const w = this.basketWidth
      const h = this.basketHeight
      const bottomY = 180
      const topY = bottomY - h
      
      const count = 6
      for (let i = 1; i < count; i++) {
        const y = topY + (h / count) * i
        const curveOffset = w * 0.1 * Math.sin(i)
        lines.push(`M ${100 - w + curveOffset} ${y} Q 100 ${y + 5} ${100 + w - curveOffset} ${y}`)
      }
      
      for (let i = 0; i < 8; i++) {
        const xRatio = -1 + (i / 7) * 2
        const x = 100 + w * xRatio
        lines.push(`M ${x} ${topY} Q ${x + 5} ${topY + h * 0.5} ${x} ${bottomY}`)
      }
      
      return lines
    }
  },
  methods: {
    handleSubmit() {
      this.$refs.orderForm.validate(async (valid) => {
        if (valid) {
          this.submitting = true
          setTimeout(async () => {
            const order = await this.$store.dispatch('createOrder', { ...this.form })
            this.createdOrder = order
            this.submitting = false
            this.successVisible = true
          }, 800)
        }
      })
    },
    handleReset() {
      this.$refs.orderForm.resetFields()
      this.form = {
        material: '',
        height: null,
        diameter: null,
        style: '',
        handle: '',
        contact: ''
      }
    },
    goToAdmin() {
      this.successVisible = false
      this.$router.push('/admin')
    }
  }
}
</script>

<style lang="scss" scoped>
.order-form-page {
  .order-form {
    ::v-deep .el-form-item {
      margin-bottom: 24px;
    }
  }

  .unit {
    margin-left: 8px;
    color: #8D6E63;
  }

  .style-radio-group {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;

    ::v-deep .el-radio-button__inner {
      padding: 12px 20px;
      border-radius: 8px !important;
      height: auto;
      line-height: 1.4;
    }

    .radio-content {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;

      .radio-label {
        font-weight: 600;
        color: #5D4037;
      }

      .radio-desc {
        font-size: 12px;
        color: #8D6E63;
      }

      .radio-price {
        font-size: 12px;
        color: #E65100;
      }
    }
  }

  .price-tag {
    margin-left: 8px;
    color: #E65100;
  }

  .submit-btn {
    min-width: 160px;
    padding: 12px 32px;
    font-size: 16px;
  }
}

.preview-card {
  position: sticky;
  top: 24px;

  .basket-preview {
    text-align: center;
    padding: 16px 0;
  }

  .basket-svg {
    width: 100%;
    max-width: 280px;
    margin: 0 auto 20px;
    transition: all 0.3s ease;
  }

  .preview-info {
    background: #FDF5E6;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 16px;

    .info-item {
      display: flex;
      justify-content: space-between;
      padding: 6px 0;

      .label {
        color: #8D6E63;
      }

      .value {
        color: #5D4037;
        font-weight: 500;
      }
    }
  }

  .price-section {
    border-top: 1px dashed #D7CCC8;
    padding-top: 16px;

    .price-row {
      display: flex;
      justify-content: space-between;
      padding: 6px 0;
      color: #5D4037;

      &.total {
        margin-top: 12px;
        padding-top: 12px;
        border-top: 1px solid #D7CCC8;
        font-size: 16px;
        font-weight: 600;

        .total-price {
          color: #E65100;
          font-size: 24px;
        }
      }

      .add {
        color: #E65100;
      }
    }
  }
}

.success-dialog {
  .success-content {
    text-align: center;
    padding: 20px 0;

    .success-icon {
      font-size: 80px;
      color: #228B22;
      margin-bottom: 16px;
    }

    .success-text {
      font-size: 20px;
      font-weight: 600;
      color: #5D4037;
      margin-bottom: 16px;
    }

    .order-info-box {
      background: #FDF5E6;
      border-radius: 8px;
      padding: 20px;
      color: #5D4037;
      line-height: 1.8;

      .order-id {
        font-weight: 600;
        color: #8B4513;
      }
    }
  }
}
</style>
