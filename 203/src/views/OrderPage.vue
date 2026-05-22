<template>
  <div class="order-page">
    <h2 class="page-title">缂丝扇面定制</h2>
    
    <el-form
      ref="orderForm"
      :model="formData"
      :rules="rules"
      label-width="120px"
      label-position="right"
    >
      <el-card class="form-card">
        <div slot="header">
          <span>丝线材质选择</span>
        </div>
        <el-form-item label="丝线材质" prop="material">
          <el-radio-group v-model="formData.material" class="material-group">
            <el-radio
              v-for="item in materials"
              :key="item.value"
              :label="item.value"
              border
              class="material-radio"
            >
              <div class="material-content">
                <div class="material-name">{{ item.label }}</div>
                <div class="material-price">¥{{ item.price }}/平方尺</div>
                <div class="material-desc">{{ item.desc }}</div>
              </div>
            </el-radio>
          </el-radio-group>
        </el-form-item>
      </el-card>

      <el-card class="form-card">
        <div slot="header">
          <span>扇面尺寸</span>
        </div>
        <el-form-item label="常用规格">
          <div class="size-presets">
            <el-button
              v-for="preset in sizePresets"
              :key="preset.label"
              size="small"
              :type="isPresetActive(preset) ? 'primary' : 'default'"
              @click="selectPreset(preset)"
            >
              {{ preset.label }}
            </el-button>
          </div>
        </el-form-item>
        <el-form-item label="扇面宽度" prop="sizeWidth">
          <el-input-number
            v-model="formData.sizeWidth"
            :min="15"
            :max="60"
            :step="1"
            :precision="0"
          >
            <template slot="append">cm</template>
          </el-input-number>
          <span class="form-tip">建议范围：15cm - 60cm</span>
        </el-form-item>
        <el-form-item label="扇面高度" prop="sizeHeight">
          <el-input-number
            v-model="formData.sizeHeight"
            :min="10"
            :max="40"
            :step="1"
            :precision="0"
          >
            <template slot="append">cm</template>
          </el-input-number>
          <span class="form-tip">建议范围：10cm - 40cm</span>
        </el-form-item>
      </el-card>

      <el-card class="form-card">
        <div slot="header">
          <span>纹样题材选择</span>
        </div>
        <el-form-item label="纹样题材" prop="pattern">
          <el-select v-model="formData.pattern" placeholder="请选择纹样题材" style="width: 300px;">
            <el-option
              v-for="item in patterns"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
              <span>{{ item.label }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px;">{{ item.desc }}</span>
            </el-option>
          </el-select>
        </el-form-item>
      </el-card>

      <el-card class="form-card">
        <div slot="header">
          <span>织造工艺</span>
        </div>
        <el-form-item label="织造密度" prop="density">
          <el-radio-group v-model="formData.density">
            <el-radio-button
              v-for="item in densities"
              :key="item.value"
              :label="item.value"
            >
              {{ item.label }}
              <span v-if="item.priceMultiplier > 1" class="price-multiplier">
                (×{{ item.priceMultiplier }})
              </span>
            </el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="包边方式" prop="edgeType">
          <el-radio-group v-model="formData.edgeType">
            <el-radio-button
              v-for="item in edgeTypes"
              :key="item.value"
              :label="item.value"
            >
              {{ item.label }} (+¥{{ item.price }})
            </el-radio-button>
          </el-radio-group>
        </el-form-item>
      </el-card>

      <el-card class="form-card">
        <div slot="header">
          <span>客户信息</span>
        </div>
        <el-form-item label="客户姓名" prop="customerName">
          <el-input v-model="formData.customerName" placeholder="请输入您的姓名" style="width: 300px;" />
        </el-form-item>
        <el-form-item label="联系电话" prop="customerPhone">
          <el-input v-model="formData.customerPhone" placeholder="请输入联系电话" style="width: 300px;" />
        </el-form-item>
        <el-form-item label="备注说明">
          <el-input
            v-model="formData.remark"
            type="textarea"
            :rows="3"
            placeholder="如有特殊要求请在此说明"
            style="width: 500px;"
          />
        </el-form-item>
      </el-card>

      <el-card class="price-card">
        <div class="price-preview">
          <div class="price-detail">
            <div class="price-row">
              <span>材质价格：</span>
              <span>¥{{ materialPrice }}</span>
            </div>
            <div class="price-row">
              <span>扇面面积：</span>
              <span>{{ area }} 平方尺</span>
            </div>
            <div class="price-row">
              <span>密度系数：</span>
              <span>×{{ densityMultiplier }}</span>
            </div>
            <div class="price-row">
              <span>包边费用：</span>
              <span>¥{{ edgePrice }}</span>
            </div>
          </div>
          <div class="price-total">
            <span class="total-label">预估总价：</span>
            <span class="total-price">¥{{ totalPrice }}</span>
          </div>
        </div>
      </el-card>

      <div class="submit-section">
        <el-button type="primary" size="large" @click="submitOrder" :loading="submitting">
          提交订单
        </el-button>
        <el-button size="large" @click="resetForm">
          重置表单
        </el-button>
      </div>
    </el-form>

    <el-dialog
      title="订单提交成功"
      :visible.sync="dialogVisible"
      width="500px"
      :close-on-click-modal="false"
    >
      <div class="success-content">
        <i class="el-icon-circle-check success-icon"></i>
        <p class="success-text">您的定制订单已提交成功！</p>
        <div class="order-info">
          <p><span>订单编号：</span>{{ newOrder.orderNo }}</p>
          <p><span>客户姓名：</span>{{ newOrder.customerName }}</p>
          <p><span>联系电话：</span>{{ newOrder.customerPhone }}</p>
          <p><span>订单金额：</span><span class="highlight">¥{{ newOrder.price }}</span></p>
        </div>
        <p class="tip-text">我们的工匠将尽快为您开始制作，您可以在管理员后台查看订单进度</p>
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="goToAdmin">查看订单列表</el-button>
        <el-button @click="continueOrder">继续下单</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { materials, patterns, densities, edgeTypes, stepNames } from '../mock/data'
import { addOrder, generateOrderNo } from '../utils/storage'

export default {
  name: 'OrderPage',
  data() {
    return {
      materials,
      patterns,
      densities,
      edgeTypes,
      sizePresets: [
        { label: '小扇 (20×15cm)', width: 20, height: 15 },
        { label: '标准扇 (30×20cm)', width: 30, height: 20 },
        { label: '中扇 (40×25cm)', width: 40, height: 25 },
        { label: '大扇 (50×30cm)', width: 50, height: 30 },
        { label: '特大扇 (60×35cm)', width: 60, height: 35 }
      ],
      submitting: false,
      dialogVisible: false,
      newOrder: {},
      formData: {
        material: '',
        sizeWidth: 30,
        sizeHeight: 20,
        pattern: '',
        density: 'normal',
        edgeType: 'normal',
        customerName: '',
        customerPhone: '',
        remark: ''
      },
      rules: {
        material: [
          { required: true, message: '请选择丝线材质', trigger: 'change' }
        ],
        sizeWidth: [
          { required: true, message: '请输入扇面宽度', trigger: 'blur' },
          { type: 'number', min: 15, max: 60, message: '宽度范围为 15-60 cm', trigger: 'blur' }
        ],
        sizeHeight: [
          { required: true, message: '请输入扇面高度', trigger: 'blur' },
          { type: 'number', min: 10, max: 40, message: '高度范围为 10-40 cm', trigger: 'blur' }
        ],
        pattern: [
          { required: true, message: '请选择纹样题材', trigger: 'change' }
        ],
        density: [
          { required: true, message: '请选择织造密度', trigger: 'change' }
        ],
        edgeType: [
          { required: true, message: '请选择包边方式', trigger: 'change' }
        ],
        customerName: [
          { required: true, message: '请输入客户姓名', trigger: 'blur' }
        ],
        customerPhone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    materialPrice() {
      const item = this.materials.find(m => m.value === this.formData.material)
      return item ? item.price : 0
    },
    area() {
      const width = this.formData.sizeWidth || 0
      const height = this.formData.sizeHeight || 0
      return (width * height / 10000 * 9).toFixed(2)
    },
    densityMultiplier() {
      const item = this.densities.find(d => d.value === this.formData.density)
      return item ? item.priceMultiplier : 1
    },
    edgePrice() {
      const item = this.edgeTypes.find(e => e.value === this.formData.edgeType)
      return item ? item.price : 0
    },
    totalPrice() {
      const basePrice = this.materialPrice * parseFloat(this.area) * this.densityMultiplier
      return Math.round(basePrice + this.edgePrice)
    }
  },
  methods: {
    submitOrder() {
      this.$refs.orderForm.validate((valid) => {
        if (valid) {
          this.submitting = true
          setTimeout(() => {
            const materialItem = this.materials.find(m => m.value === this.formData.material)
            const patternItem = this.patterns.find(p => p.value === this.formData.pattern)
            const densityItem = this.densities.find(d => d.value === this.formData.density)
            const edgeItem = this.edgeTypes.find(e => e.value === this.formData.edgeType)

            const order = {
              id: 'ORD' + Date.now(),
              orderNo: generateOrderNo(),
              material: this.formData.material,
              materialLabel: materialItem ? materialItem.label : '',
              sizeWidth: this.formData.sizeWidth,
              sizeHeight: this.formData.sizeHeight,
              pattern: this.formData.pattern,
              patternLabel: patternItem ? patternItem.label : '',
              density: this.formData.density,
              densityLabel: densityItem ? densityItem.label : '',
              edgeType: this.formData.edgeType,
              edgeTypeLabel: edgeItem ? edgeItem.label : '',
              customerName: this.formData.customerName,
              customerPhone: this.formData.customerPhone,
              remark: this.formData.remark,
              status: 'pending',
              currentStep: 0,
              createTime: Date.now(),
              price: this.totalPrice,
              steps: stepNames.map(name => ({
                name,
                completed: false,
                time: null
              }))
            }

            addOrder(order)
            this.newOrder = order
            this.submitting = false
            this.dialogVisible = true
          }, 800)
        }
      })
    },
    resetForm() {
      this.$refs.orderForm.resetFields()
      this.formData.sizeWidth = 30
      this.formData.sizeHeight = 20
      this.formData.density = 'normal'
      this.formData.edgeType = 'normal'
    },
    goToAdmin() {
      this.dialogVisible = false
      this.$router.push({ path: '/admin', query: { scrollTo: 'list' } })
    },
    continueOrder() {
      this.dialogVisible = false
      this.resetForm()
    },
    selectPreset(preset) {
      this.formData.sizeWidth = preset.width
      this.formData.sizeHeight = preset.height
    },
    isPresetActive(preset) {
      return this.formData.sizeWidth === preset.width && this.formData.sizeHeight === preset.height
    }
  }
}
</script>

<style scoped>
.order-page {
  max-width: 900px;
  margin: 0 auto;
}

.form-card {
  margin-bottom: 24px;
}

.size-presets {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.material-group {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.material-radio {
  margin-right: 0;
  margin-bottom: 0;
}

.material-content {
  padding: 8px 12px;
  min-width: 180px;
}

.material-name {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.material-price {
  color: var(--primary-color);
  font-size: 14px;
  margin-bottom: 4px;
}

.material-desc {
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.4;
}

.price-multiplier {
  color: var(--primary-color);
  font-size: 12px;
  margin-left: 4px;
}

.form-tip {
  margin-left: 12px;
  color: var(--text-secondary);
  font-size: 13px;
}

.price-card {
  margin-bottom: 24px;
  background: linear-gradient(135deg, rgba(218, 165, 32, 0.08) 0%, rgba(139, 69, 19, 0.05) 100%);
  border: 1px dashed var(--accent-color);
}

.price-preview {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
}

.price-detail {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.price-row {
  font-size: 14px;
  color: var(--text-secondary);
}

.price-row span:last-child {
  color: var(--text-primary);
  font-weight: 500;
}

.price-total {
  text-align: right;
}

.total-label {
  font-size: 16px;
  color: var(--text-secondary);
}

.total-price {
  font-size: 32px;
  font-weight: bold;
  color: var(--primary-color);
  margin-left: 12px;
}

.submit-section {
  display: flex;
  justify-content: center;
  gap: 20px;
  padding: 20px 0 40px;
}

.submit-section .el-button {
  min-width: 160px;
  font-size: 16px;
  padding: 12px 30px;
}

.success-content {
  text-align: center;
  padding: 20px 0;
}

.success-icon {
  font-size: 64px;
  color: #67c23a;
  margin-bottom: 16px;
}

.success-text {
  font-size: 18px;
  color: var(--text-primary);
  margin-bottom: 24px;
}

.order-info {
  background-color: var(--bg-color);
  padding: 20px;
  border-radius: 8px;
  text-align: left;
  margin-bottom: 20px;
}

.order-info p {
  margin: 8px 0;
  color: var(--text-secondary);
}

.order-info span:first-child {
  display: inline-block;
  width: 80px;
}

.highlight {
  color: var(--primary-color);
  font-weight: bold;
  font-size: 18px;
}

.tip-text {
  color: var(--text-secondary);
  font-size: 13px;
}

.dialog-footer {
  text-align: center;
}
</style>
