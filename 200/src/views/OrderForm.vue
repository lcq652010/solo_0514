<template>
  <div class="order-form-container">
    <div class="form-card">
      <div class="form-header">
        <h2>石砚定制订单</h2>
        <p class="subtitle">精心定制属于您的专属砚台</p>
      </div>
      
      <el-form ref="orderForm" :model="formData" :rules="rules" label-width="120px">
        <el-form-item label="砚石材选择" prop="stoneType">
          <el-select v-model="formData.stoneType" placeholder="请选择砚石材">
            <el-option v-for="stone in stoneTypes" :key="stone.value" :label="stone.label" :value="stone.value" />
          </el-select>
        </el-form-item>

        <el-form-item label="尺寸规格" class="size-row">
          <el-form-item prop="length" class="size-item">
            <el-input-number 
              v-model="formData.length" 
              :min="1" 
              :max="80" 
              :step="0.5"
              :precision="1"
              placeholder="长度(cm)"
              @blur="validateNumber('length')"
            />
          </el-form-item>
          <span class="size-separator">×</span>
          <el-form-item prop="width" class="size-item">
            <el-input-number 
              v-model="formData.width" 
              :min="1" 
              :max="60" 
              :step="0.5"
              :precision="1"
              placeholder="宽度(cm)"
              @blur="validateNumber('width')"
            />
          </el-form-item>
          <span class="size-unit">厘米</span>
        </el-form-item>
        
        <el-form-item label="常用尺寸" class="size-presets">
          <div class="preset-tags">
            <el-tag 
              v-for="preset in sizePresets" 
              :key="preset.label"
              :closable="false"
              :type="isPresetActive(preset) ? 'primary' : 'info'"
              @click="applySizePreset(preset)"
              class="preset-tag"
            >
              {{ preset.label }}
            </el-tag>
          </div>
        </el-form-item>

        <el-form-item label="雕刻样式" prop="carvingStyle">
          <el-select v-model="formData.carvingStyle" placeholder="请选择雕刻样式">
            <el-option v-for="style in carvingStyles" :key="style.value" :label="style.label" :value="style.value" />
          </el-select>
        </el-form-item>

        <el-form-item label="砚池形制" prop="inkPoolShape">
          <el-select v-model="formData.inkPoolShape" placeholder="请选择砚池形制">
            <el-option v-for="shape in inkPoolShapes" :key="shape.value" :label="shape.label" :value="shape.value" />
          </el-select>
        </el-form-item>

        <el-form-item>
          <div class="preview-card">
            <h4>订单预览</h4>
            <div class="preview-content">
              <div class="preview-item">
                <span class="preview-label">砚石材：</span>
                <span>{{ getLabel(stoneTypes, formData.stoneType) }}</span>
              </div>
              <div class="preview-item">
                <span class="preview-label">尺寸：</span>
                <span>{{ formData.length }} × {{ formData.width }} cm</span>
              </div>
              <div class="preview-item">
                <span class="preview-label">雕刻样式：</span>
                <span>{{ getLabel(carvingStyles, formData.carvingStyle) }}</span>
              </div>
              <div class="preview-item">
                <span class="preview-label">砚池形制：</span>
                <span>{{ getLabel(inkPoolShapes, formData.inkPoolShape) }}</span>
              </div>
            </div>
          </div>
        </el-form-item>

        <el-form-item class="form-actions">
          <el-button type="primary" @click="submitForm" :loading="loading">
            <i class="el-icon-check"></i>
            提交订单
          </el-button>
          <el-button @click="resetForm">
            <i class="el-icon-refresh"></i>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <el-dialog title="下单成功" :visible.sync="showSuccessDialog" width="400px">
      <div class="success-content">
        <div class="success-icon">
          <i class="el-icon-check-circle"></i>
        </div>
        <p>恭喜您，订单提交成功！</p>
        <p class="order-id">订单编号：{{ newOrderId }}</p>
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button @click="showSuccessDialog = false">确定</el-button>
        <el-button type="primary" @click="continueOrder">继续下单</el-button>
        <el-button type="success" @click="printOrder">
          <i class="el-icon-printer"></i>
          打印订单
        </el-button>
      </div>
    </el-dialog>

    <el-dialog title="订单详情单" :visible.sync="showPrintDialog" width="600px">
      <div class="print-content" id="print-order">
        <div class="print-header">
          <h2>石砚定制订单详情单</h2>
          <p class="print-date">下单时间：{{ submittedOrder?.createdAt }}</p>
        </div>
        <div class="print-info">
          <div class="print-row">
            <span class="print-label">订单编号：</span>
            <span class="print-value">{{ submittedOrder?.id }}</span>
          </div>
          <div class="print-row">
            <span class="print-label">砚石材：</span>
            <span class="print-value">{{ getLabel(stoneTypes, submittedOrder?.stoneType) }}</span>
          </div>
          <div class="print-row">
            <span class="print-label">尺寸规格：</span>
            <span class="print-value">{{ submittedOrder?.length }} × {{ submittedOrder?.width }} 厘米</span>
          </div>
          <div class="print-row">
            <span class="print-label">雕刻样式：</span>
            <span class="print-value">{{ getLabel(carvingStyles, submittedOrder?.carvingStyle) }}</span>
          </div>
          <div class="print-row">
            <span class="print-label">砚池形制：</span>
            <span class="print-value">{{ getLabel(inkPoolShapes, submittedOrder?.inkPoolShape) }}</span>
          </div>
          <div class="print-row">
            <span class="print-label">当前状态：</span>
            <span class="print-value">待处理</span>
          </div>
        </div>
        <div class="print-footer">
          <p>感谢您的订购！我们将尽快为您制作。</p>
          <p class="print-note">订单查询：管理员可在订单管理页面查看进度</p>
        </div>
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button @click="closePrintDialog">关闭</el-button>
        <el-button type="primary" @click="handlePrint">
          <i class="el-icon-printer"></i>
          打印
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import { stoneTypes, carvingStyles, inkPoolShapes } from '../data/mockData'

export default {
  name: 'OrderForm',
  data() {
    return {
      stoneTypes,
      carvingStyles,
      inkPoolShapes,
      sizePresets: [
        { label: '小巧 15×10', length: 15, width: 10 },
        { label: '适中 20×14', length: 20, width: 14 },
        { label: '标准 25×18', length: 25, width: 18 },
        { label: '大号 30×20', length: 30, width: 20 },
        { label: '精品 35×25', length: 35, width: 25 },
        { label: '珍藏 40×30', length: 40, width: 30 }
      ],
      formData: {
        stoneType: '',
        length: null,
        width: null,
        carvingStyle: '',
        inkPoolShape: ''
      },
      rules: {
        stoneType: [
          { required: true, message: '请选择砚石材', trigger: 'change' }
        ],
        length: [
          { required: true, message: '请输入长度', trigger: 'blur' },
          { validator: this.validateSize, trigger: 'blur' }
        ],
        width: [
          { required: true, message: '请输入宽度', trigger: 'blur' },
          { validator: this.validateSize, trigger: 'blur' }
        ],
        carvingStyle: [
          { required: true, message: '请选择雕刻样式', trigger: 'change' }
        ],
        inkPoolShape: [
          { required: true, message: '请选择砚池形制', trigger: 'change' }
        ]
      },
      loading: false,
      showSuccessDialog: false,
      showPrintDialog: false,
      newOrderId: '',
      submittedOrder: null
    }
  },
  methods: {
    ...mapActions(['addOrder']),
    getLabel(list, value) {
      const item = list.find(item => item.value === value)
      return item ? item.label : '未选择'
    },
    applySizePreset(preset) {
      this.formData.length = preset.length
      this.formData.width = preset.width
    },
    isPresetActive(preset) {
      return this.formData.length === preset.length && this.formData.width === preset.width
    },
    validateSize(rule, value, callback) {
      const fieldName = rule.field === 'length' ? '长度' : '宽度'
      const min = rule.field === 'length' ? 10 : 8
      const max = rule.field === 'length' ? 80 : 60
      
      if (value === null || value === undefined || value === '') {
        callback()
        return
      }
      
      if (!/^\d+(\.\d{1})?$/.test(value.toString())) {
        callback(new Error(`${fieldName}必须为数字，最多保留1位小数`))
        return
      }
      
      const numValue = parseFloat(value)
      if (numValue <= 0) {
        callback(new Error(`${fieldName}必须大于0`))
        return
      }
      
      if (numValue < min || numValue > max) {
        callback(new Error(`${fieldName}应在${min}-${max}厘米之间`))
        return
      }
      
      callback()
    },
    validateNumber(field) {
      const value = this.formData[field]
      if (value === null || value === undefined) return
      
      const numValue = parseFloat(value)
      if (isNaN(numValue) || numValue <= 0) {
        this.formData[field] = null
        this.$message.warning(`${field === 'length' ? '长度' : '宽度'}必须为正数字`)
      }
    },
    submitForm() {
      this.$refs.orderForm.validate(async (valid) => {
        if (valid) {
          this.loading = true
          try {
            const order = await this.addOrder({
              stoneType: this.formData.stoneType,
              length: this.formData.length,
              width: this.formData.width,
              carvingStyle: this.formData.carvingStyle,
              inkPoolShape: this.formData.inkPoolShape
            })
            this.newOrderId = order.id
            this.submittedOrder = order
            this.showSuccessDialog = true
          } catch (error) {
            this.$message.error('提交失败，请重试')
          } finally {
            this.loading = false
          }
        }
      })
    },
    resetForm() {
      this.$refs.orderForm.resetFields()
      this.formData = {
        stoneType: '',
        length: null,
        width: null,
        carvingStyle: '',
        inkPoolShape: ''
      }
    },
    continueOrder() {
      this.showSuccessDialog = false
      this.resetForm()
    },
    printOrder() {
      this.showSuccessDialog = false
      this.showPrintDialog = true
    },
    handlePrint() {
      window.print()
    },
    closePrintDialog() {
      this.showPrintDialog = false
      this.submittedOrder = null
      this.resetForm()
    }
  }
}
</script>

<style scoped>
.order-form-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.form-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 30px;
}

.form-header {
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.form-header h2 {
  font-size: 24px;
  color: #8B4513;
  margin-bottom: 5px;
}

.subtitle {
  color: #999;
  font-size: 14px;
}

.size-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.size-item {
  flex: 1;
  margin-bottom: 0;
}

.size-separator {
  font-size: 20px;
  color: #999;
}

.size-unit {
  color: #666;
  font-size: 14px;
}

.size-presets {
  margin-bottom: 20px;
}

.preset-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.preset-tag {
  cursor: pointer;
  transition: all 0.3s ease;
}

.preset-tag:hover {
  transform: scale(1.05);
}

.preview-card {
  background: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
}

.preview-card h4 {
  margin-bottom: 15px;
  color: #333;
  font-size: 16px;
}

.preview-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.preview-item {
  display: flex;
  flex-direction: column;
}

.preview-label {
  font-size: 12px;
  color: #999;
  margin-bottom: 2px;
}

.preview-item span:last-child {
  font-size: 14px;
  color: #333;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.form-actions button {
  min-width: 120px;
}

.success-content {
  text-align: center;
  padding: 20px;
}

.success-icon {
  font-size: 64px;
  color: #67C23A;
  margin-bottom: 20px;
}

.success-content p {
  font-size: 16px;
  color: #333;
  margin-bottom: 10px;
}

.order-id {
  font-size: 14px;
  color: #666;
  background: #f5f5f5;
  padding: 10px;
  border-radius: 4px;
  display: inline-block;
}

.dialog-footer {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.print-content {
  background: #fff;
  padding: 30px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.print-header {
  text-align: center;
  padding-bottom: 20px;
  border-bottom: 2px solid #8B4513;
  margin-bottom: 20px;
}

.print-header h2 {
  color: #8B4513;
  font-size: 20px;
  margin-bottom: 10px;
}

.print-date {
  color: #666;
  font-size: 14px;
}

.print-info {
  margin-bottom: 20px;
}

.print-row {
  display: flex;
  padding: 10px 0;
  border-bottom: 1px dashed #eee;
}

.print-label {
  width: 120px;
  color: #666;
  font-weight: bold;
}

.print-value {
  color: #333;
}

.print-footer {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #ddd;
  color: #666;
  font-size: 14px;
}

.print-note {
  font-size: 12px;
  margin-top: 5px;
  color: #999;
}

@media print {
  body * {
    visibility: hidden;
  }
  #print-order,
  #print-order * {
    visibility: visible;
  }
  #print-order {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    margin: 0;
    padding: 20px;
  }
}
</style>
