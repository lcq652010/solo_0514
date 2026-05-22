<template>
  <div class="order-form-container">
    <el-card class="order-card" shadow="never">
      <div slot="header" class="card-header">
        <h2>平安扣定制下单</h2>
        <p class="subtitle">匠心传承 · 精工细作</p>
      </div>

      <el-form :model="orderForm" :rules="rules" ref="orderForm" label-width="120px" class="order-form">
        <el-divider content-position="left">基本信息</el-divider>
        
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

        <el-form-item label="收货地址" prop="address">
          <el-input v-model="orderForm.address" type="textarea" :rows="2" placeholder="请输入详细收货地址"></el-input>
        </el-form-item>

        <el-divider content-position="left">玉料选择</el-divider>
        
        <el-form-item label="玉料种类" prop="jadeType">
          <el-select v-model="orderForm.jadeType" placeholder="请选择玉料种类" style="width: 100%">
            <el-option
              v-for="item in jadeTypes"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
              <span style="float: left">{{ item.label }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">¥{{ item.price }}/g</span>
            </el-option>
          </el-select>
        </el-form-item>

        <el-divider content-position="left">规格尺寸</el-divider>
        
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="外径(mm)" prop="outerDiameter">
              <el-input-number v-model="orderForm.outerDiameter" :min="20" :max="80" :step="1" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="厚度(mm)" prop="thickness">
              <el-input-number v-model="orderForm.thickness" :min="5" :max="20" :step="1" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="内径(mm)">
              <el-input :value="innerDiameter" disabled style="width: 100%"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">雕刻纹饰</el-divider>
        
        <el-form-item label="纹饰选择" prop="pattern">
          <el-radio-group v-model="orderForm.pattern">
            <el-row :gutter="20">
              <el-col :span="6" v-for="item in patterns" :key="item.value">
                <el-radio :label="item.value" class="pattern-radio">
                  <div class="pattern-item">
                    <div class="pattern-icon">{{ item.icon }}</div>
                    <span>{{ item.label }}</span>
                  </div>
                </el-radio>
              </el-col>
            </el-row>
          </el-radio-group>
        </el-form-item>

        <el-divider content-position="left">挂绳款式</el-divider>
        
        <el-form-item label="挂绳款式" prop="ropeStyle">
          <el-radio-group v-model="orderForm.ropeStyle">
            <el-row :gutter="20">
              <el-col :span="6" v-for="item in ropeStyles" :key="item.value">
                <el-radio :label="item.value" class="rope-radio">
                  <div class="rope-item">
                    <div class="rope-color" :style="{ background: item.color }"></div>
                    <span>{{ item.label }}</span>
                  </div>
                </el-radio>
              </el-col>
            </el-row>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="备注信息">
          <el-input v-model="orderForm.remark" type="textarea" :rows="3" placeholder="如有特殊要求请在此说明"></el-input>
        </el-form-item>

        <el-divider></el-divider>

        <el-form-item>
          <div class="form-actions">
            <div class="price-summary">
              <span>预估价格：</span>
              <span class="price">¥{{ estimatedPrice }}</span>
            </div>
            <el-button type="primary" size="large" @click="submitOrder" :loading="submitting">
              提交订单
            </el-button>
            <el-button size="large" @click="resetForm">重置</el-button>
          </div>
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
        address: '',
        jadeType: '',
        outerDiameter: null,
        thickness: null,
        pattern: '',
        ropeStyle: '',
        remark: ''
      },
      rules: {
        customerName: [
          { required: true, message: '请输入客户姓名', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ],
        address: [
          { required: true, message: '请输入收货地址', trigger: 'blur' }
        ],
        jadeType: [
          { required: true, message: '请选择玉料种类', trigger: 'change' }
        ],
        outerDiameter: [
          { required: true, message: '请输入外径', trigger: 'blur' },
          { type: 'number', min: 25, max: 60, message: '外径需在25-60mm之间', trigger: 'blur' }
        ],
        thickness: [
          { required: true, message: '请输入厚度', trigger: 'blur' },
          { type: 'number', min: 6, max: 15, message: '厚度需在6-15mm之间', trigger: 'blur' }
        ],
        pattern: [
          { required: true, message: '请选择雕刻纹饰', trigger: 'change' }
        ],
        ropeStyle: [
          { required: true, message: '请选择挂绳款式', trigger: 'change' }
        ]
      },
      jadeTypes: [
        { value: 'hetian', label: '和田玉', price: 80 },
        { value: 'xiuyu', label: '岫玉', price: 30 },
        { value: 'dushan', label: '独山玉', price: 50 },
        { value: 'nanhong', label: '南红玛瑙', price: 100 },
        { value: 'feicui', label: '翡翠', price: 150 }
      ],
      patterns: [
        { value: 'plain', label: '素面无纹', icon: '○' },
        { value: 'yunwen', label: '云纹', icon: '☁' },
        { value: 'huawen', label: '花纹', icon: '✿' },
        { value: 'longwen', label: '龙纹', icon: '龙' }
      ],
      ropeStyles: [
        { value: 'red', label: '中国红', color: '#C41E3A' },
        { value: 'black', label: '典雅黑', color: '#2C2C2C' },
        { value: 'brown', label: '咖啡棕', color: '#8B4513' },
        { value: 'green', label: '翡翠绿', color: '#228B22' }
      ]
    }
  },
  computed: {
    innerDiameter() {
      if (!this.orderForm.outerDiameter) return '-'
      return Math.round(this.orderForm.outerDiameter * 0.4)
    },
    estimatedPrice() {
      if (!this.orderForm.jadeType || !this.orderForm.outerDiameter || !this.orderForm.thickness) {
        return 0
      }
      const jadeType = this.jadeTypes.find(item => item.value === this.orderForm.jadeType)
      const jadePrice = jadeType ? jadeType.price : 50
      const volume = Math.PI * Math.pow(this.orderForm.outerDiameter / 2, 2) * this.orderForm.thickness * 0.001
      const basePrice = volume * jadePrice
      const patternPrice = this.orderForm.pattern === 'plain' ? 0 : 100
      return Math.round(basePrice + patternPrice + 50)
    }
  },
  methods: {
    submitOrder() {
      this.$refs.orderForm.validate((valid) => {
        if (valid) {
          this.submitting = true
          const order = {
            id: 'ORD' + Date.now(),
            ...this.orderForm,
            status: 0,
            createTime: new Date().toLocaleString()
          }
          
          const orders = JSON.parse(localStorage.getItem('jadeOrders') || '[]')
          orders.unshift(order)
          localStorage.setItem('jadeOrders', JSON.stringify(orders))
          
          setTimeout(() => {
            this.submitting = false
            this.$message({
              message: '订单提交成功！',
              type: 'success',
              duration: 2000,
              showClose: true
            })
            this.resetForm()
          }, 1000)
        } else {
          this.$message.error('请填写完整信息')
          return false
        }
      })
    },
    resetForm() {
      this.$refs.orderForm.resetFields()
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
  border-radius: 8px;
}

.card-header {
  text-align: center;
}

.card-header h2 {
  color: #8B4513;
  margin-bottom: 5px;
}

.subtitle {
  color: #999;
  font-size: 14px;
  letter-spacing: 2px;
}

.order-form {
  padding: 20px 0;
}

.pattern-radio,
.rope-radio {
  width: 100%;
  margin: 10px 0;
}

.pattern-item,
.rope-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  transition: all 0.3s;
}

.pattern-item:hover,
.rope-item:hover {
  border-color: #8B4513;
}

.pattern-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.rope-color {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-bottom: 8px;
  border: 2px solid #e8e8e8;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.price-summary {
  font-size: 18px;
}

.price {
  color: #F56C6C;
  font-weight: bold;
  font-size: 24px;
}
</style>
