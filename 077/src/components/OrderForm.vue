<template>
  <div class="order-form-container">
    <el-card class="form-card" shadow="hover">
      <div slot="header" class="card-header">
        <i class="el-icon-brush"></i>
        <span>木雕书签定制订单</span>
      </div>
      
      <el-form :model="orderForm" :rules="rules" ref="orderForm" label-width="120px" size="medium">
        <el-divider content-position="left">
          <span class="divider-title"><i class="el-icon-user"></i> 客户信息</span>
        </el-divider>
        
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
        
        <el-divider content-position="left">
          <span class="divider-title"><i class="el-icon-picture"></i> 木料选择</span>
        </el-divider>
        
        <el-form-item label="木料类型" prop="woodType">
          <el-radio-group v-model="orderForm.woodType">
            <el-row :gutter="20">
              <el-col :span="6" v-for="wood in woodOptions" :key="wood.value">
                <div class="wood-option">
                  <el-radio :label="wood.value">
                    <div class="wood-card" :style="{ backgroundColor: wood.color }">
                      <div class="wood-name">{{ wood.label }}</div>
                      <div class="wood-price">¥{{ wood.price }}</div>
                    </div>
                  </el-radio>
                </div>
              </el-col>
            </el-row>
          </el-radio-group>
        </el-form-item>
        
        <el-divider content-position="left">
          <span class="divider-title"><i class="el-icon-rank"></i> 尺寸规格</span>
        </el-divider>
        
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="长度 (mm)" prop="length">
              <el-input-number v-model="orderForm.length" :min="100" :max="200" :step="5" style="width: 100%;"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="宽度 (mm)" prop="width">
              <el-input-number v-model="orderForm.width" :min="20" :max="50" :step="1" style="width: 100%;"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="厚度 (mm)" prop="thickness">
              <el-input-number v-model="orderForm.thickness" :min="2" :max="10" :step="1" style="width: 100%;"></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-divider content-position="left">
          <span class="divider-title"><i class="el-icon-image"></i> 雕刻图案</span>
        </el-divider>
        
        <el-form-item label="图案选择" prop="pattern">
          <el-radio-group v-model="orderForm.pattern">
            <el-row :gutter="20">
              <el-col :span="6" v-for="pattern in patternOptions" :key="pattern.value">
                <div class="pattern-option">
                  <el-radio :label="pattern.value">
                    <div class="pattern-card">
                      <div class="pattern-icon">{{ pattern.icon }}</div>
                      <div class="pattern-name">{{ pattern.label }}</div>
                    </div>
                  </el-radio>
                </div>
              </el-col>
            </el-row>
          </el-radio-group>
        </el-form-item>
        
        <el-divider content-position="left">
          <span class="divider-title"><i class="el-icon-edit-outline"></i> 刻字内容</span>
        </el-divider>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="刻字内容" prop="engravingText">
              <el-input 
                v-model="orderForm.engravingText" 
                type="textarea" 
                :rows="3" 
                placeholder="请输入需要雕刻的文字（最多20字，不允许特殊字符）"
                maxlength="20"
                show-word-limit
                @input="filterEngravingText">
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="字体样式" prop="fontStyle">
              <el-select v-model="orderForm.fontStyle" placeholder="请选择字体" style="width: 100%;">
                <el-option label="楷书" value="楷书"></el-option>
                <el-option label="行书" value="行书"></el-option>
                <el-option label="草书" value="草书"></el-option>
                <el-option label="隶书" value="隶书"></el-option>
                <el-option label="篆书" value="篆书"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="刻字位置" prop="engravingPosition">
              <el-select v-model="orderForm.engravingPosition" placeholder="请选择刻字位置" style="width: 100%;">
                <el-option label="正面" value="正面"></el-option>
                <el-option label="背面" value="背面"></el-option>
                <el-option label="双面" value="双面"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-divider content-position="left">
          <span class="divider-title"><i class="el-icon-set-up"></i> 附加工艺</span>
        </el-divider>
        
        <el-form-item label="附加工艺">
          <el-checkbox-group v-model="orderForm.additionalProcess">
            <el-checkbox label="烫金">烫金工艺 +¥30</el-checkbox>
            <el-checkbox label="上油">古法上油 +¥20</el-checkbox>
            <el-checkbox label="挂绳">精美挂绳 +¥10</el-checkbox>
            <el-checkbox label="礼盒">高档礼盒 +¥50</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        
        <el-divider></el-divider>
        
        <div class="price-summary">
          <div class="price-item">
            <span>木料基础价：</span>
            <span class="price-value">¥{{ woodPrice }}</span>
          </div>
          <div class="price-item">
            <span>刻字费用：</span>
            <span class="price-value">¥{{ engravingPrice }}</span>
          </div>
          <div class="price-item">
            <span>附加工艺：</span>
            <span class="price-value">¥{{ additionalPrice }}</span>
          </div>
          <div class="price-total">
            <span>订单总价：</span>
            <span class="total-value">¥{{ totalPrice }}</span>
          </div>
        </div>
        
        <el-form-item>
          <el-button type="primary" size="large" @click="submitOrder" :loading="submitting" style="width: 200px;">
            <i class="el-icon-check"></i> 提交订单
          </el-button>
          <el-button size="large" @click="resetForm" style="margin-left: 20px;">
            <i class="el-icon-refresh"></i> 重置表单
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'OrderForm',
  data() {
    return {
      submitting: false,
      orderForm: {
        customerName: '',
        phone: '',
        woodType: '紫檀',
        length: 150,
        width: 30,
        thickness: 3,
        pattern: '山水',
        engravingText: '',
        fontStyle: '楷书',
        engravingPosition: '正面',
        additionalProcess: []
      },
      woodOptions: [
        { value: '紫檀', label: '紫檀木', color: '#4A2C2A', price: 128 },
        { value: '黄花梨', label: '黄花梨', color: '#D4A574', price: 168 },
        { value: '酸枝', label: '酸枝木', color: '#8B4513', price: 98 },
        { value: '檀木', label: '绿檀木', color: '#2E8B57', price: 88 }
      ],
      patternOptions: [
        { value: '山水', label: '山水图案', icon: '🏔️' },
        { value: '花鸟', label: '花鸟图案', icon: '🌸' },
        { value: '龙凤', label: '龙凤呈祥', icon: '🐉' },
        { value: '祥云', label: '祥云瑞气', icon: '☁️' }
      ],
      rules: {
        customerName: [
          { required: true, message: '请输入客户姓名', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
        ],
        woodType: [
          { required: true, message: '请选择木料类型', trigger: 'change' }
        ],
        length: [
          { required: true, message: '请输入长度', trigger: 'blur' },
          { type: 'number', min: 100, max: 200, message: '长度范围为100-200mm', trigger: 'blur' }
        ],
        width: [
          { required: true, message: '请输入宽度', trigger: 'blur' },
          { type: 'number', min: 20, max: 50, message: '宽度范围为20-50mm', trigger: 'blur' }
        ],
        thickness: [
          { required: true, message: '请输入厚度', trigger: 'blur' },
          { type: 'number', min: 2, max: 10, message: '厚度范围为2-10mm', trigger: 'blur' }
        ],
        pattern: [
          { required: true, message: '请选择雕刻图案', trigger: 'change' }
        ],
        engravingText: [
          { required: true, message: '请输入刻字内容', trigger: 'blur' },
          { min: 1, max: 20, message: '刻字内容长度为1-20字', trigger: 'blur' },
          { pattern: /^[\u4e00-\u9fa5a-zA-Z0-9\s，。！？、；：""''（）]+$/, message: '刻字内容不允许特殊字符', trigger: 'blur' }
        ],
        fontStyle: [
          { required: true, message: '请选择字体样式', trigger: 'change' }
        ],
        engravingPosition: [
          { required: true, message: '请选择刻字位置', trigger: 'change' }
        ]
      }
    }
  },
  computed: {
    woodPrice() {
      const wood = this.woodOptions.find(w => w.value === this.orderForm.woodType)
      return wood ? wood.price : 0
    },
    engravingPrice() {
      if (!this.orderForm.engravingText) return 0
      const charCount = this.orderForm.engravingText.length
      return charCount * 2
    },
    additionalPrice() {
      let price = 0
      if (this.orderForm.additionalProcess.includes('烫金')) price += 30
      if (this.orderForm.additionalProcess.includes('上油')) price += 20
      if (this.orderForm.additionalProcess.includes('挂绳')) price += 10
      if (this.orderForm.additionalProcess.includes('礼盒')) price += 50
      return price
    },
    totalPrice() {
      return this.woodPrice + this.engravingPrice + this.additionalPrice
    }
  },
  methods: {
    submitOrder() {
      this.$refs.orderForm.validate((valid) => {
        if (valid) {
          this.submitting = true
          setTimeout(() => {
            const orders = JSON.parse(localStorage.getItem('woodOrders') || '[]')
            const newOrder = {
              id: Date.now(),
              ...this.orderForm,
              totalPrice: this.totalPrice,
              status: '选料',
              createTime: new Date().toLocaleString()
            }
            orders.unshift(newOrder)
            localStorage.setItem('woodOrders', JSON.stringify(orders))
            
            this.submitting = false
            this.showSuccessDialog(newOrder)
          }, 1000)
        } else {
          this.$message.error('请完善订单信息')
          return false
        }
      })
    },
    showSuccessDialog(order) {
      this.$alert(
        `<div style="text-align: left; padding: 10px;">
          <p style="margin: 8px 0;"><strong>订单编号：</strong>WD${order.id}</p>
          <p style="margin: 8px 0;"><strong>客户姓名：</strong>${order.customerName}</p>
          <p style="margin: 8px 0;"><strong>木料类型：</strong>${order.woodType}</p>
          <p style="margin: 8px 0;"><strong>订单总价：</strong><span style="color: #ff6600; font-weight: bold;">¥${order.totalPrice}</span></p>
          <p style="margin: 8px 0; color: #67C23A;"><strong>订单已成功提交，我们将尽快为您安排制作！</strong></p>
        </div>`,
        '🎉 订单提交成功',
        {
          dangerouslyUseHTMLString: true,
          confirmButtonText: '确定',
          callback: action => {
            this.resetForm()
            this.$router.push('/admin')
          }
        }
      )
    },
    resetForm() {
      this.$refs.orderForm.resetFields()
      this.orderForm.additionalProcess = []
    },
    filterEngravingText(value) {
      const validPattern = /^[\u4e00-\u9fa5a-zA-Z0-9\s，。！？、；：""''（）]*$/
      if (!validPattern.test(value)) {
        this.$message.warning('刻字内容不允许特殊字符，已自动过滤')
        this.orderForm.engravingText = value.replace(/[^\u4e00-\u9fa5a-zA-Z0-9\s，。！？、；：""''（）]/g, '')
      }
    }
  }
}
</script>

<style scoped>
.order-form-container {
  max-width: 1000px;
  margin: 0 auto;
}

.form-card {
  border-radius: 8px;
}

.card-header {
  display: flex;
  align-items: center;
  font-size: 20px;
  font-weight: bold;
  color: #8B4513;
}

.card-header i {
  margin-right: 10px;
  font-size: 24px;
}

.divider-title {
  font-size: 16px;
  font-weight: bold;
  color: #8B4513;
  display: flex;
  align-items: center;
}

.divider-title i {
  margin-right: 8px;
}

.wood-option {
  text-align: center;
  margin-bottom: 20px;
}

.wood-card {
  width: 100%;
  height: 80px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: white;
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  transition: transform 0.3s;
}

.wood-card:hover {
  transform: scale(1.05);
}

.wood-name {
  font-size: 14px;
  margin-bottom: 5px;
}

.wood-price {
  font-size: 16px;
}

.pattern-option {
  text-align: center;
  margin-bottom: 20px;
}

.pattern-card {
  width: 100%;
  height: 100px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: #fafafa;
  transition: all 0.3s;
}

.pattern-card:hover {
  border-color: #8B4513;
  background: #fff8f0;
}

.pattern-icon {
  font-size: 36px;
  margin-bottom: 8px;
}

.pattern-name {
  font-size: 14px;
  color: #666;
}

.price-summary {
  background: linear-gradient(135deg, #fff8f0 0%, #fff 100%);
  border: 1px solid #e8d5c4;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.price-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  font-size: 14px;
  color: #666;
}

.price-value {
  color: #8B4513;
  font-weight: bold;
}

.price-total {
  display: flex;
  justify-content: space-between;
  padding-top: 15px;
  border-top: 2px dashed #e8d5c4;
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.total-value {
  color: #ff6600;
  font-size: 24px;
}
</style>
