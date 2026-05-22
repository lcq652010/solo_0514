<template>
  <div class="order-form">
    <div class="page-header">
      <h1>琉璃吊坠定制</h1>
      <p>选择您喜欢的样式，打造独一无二的琉璃吊坠</p>
    </div>
    
    <el-card class="form-card">
      <el-form :model="form" :rules="rules" ref="form" label-width="120px">
        <el-divider content-position="left">基本信息</el-divider>
        
        <el-form-item label="客户姓名" prop="customerName">
          <el-input v-model="form.customerName" placeholder="请输入您的姓名"></el-input>
        </el-form-item>
        
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入联系电话"></el-input>
        </el-form-item>
        
        <el-divider content-position="left">琉璃色料</el-divider>
        
        <el-form-item label="色料选择" prop="color">
          <el-radio-group v-model="form.color" @change="validateField('color')">
            <el-radio-button v-for="color in colorOptions" :key="color.value" :label="color.value">
              <span class="color-preview" :style="{ backgroundColor: color.value }"></span>
              {{ color.label }}
            </el-radio-button>
          </el-radio-group>
        </el-form-item>
        
        <el-divider content-position="left">吊坠形状</el-divider>
        
        <el-form-item label="形状选择" prop="shape">
          <el-select v-model="form.shape" placeholder="请选择吊坠形状" style="width: 100%" @blur="validateField('shape')" @change="validateField('shape')">
            <el-option v-for="shape in shapeOptions" :key="shape.value" :label="shape.label" :value="shape.value">
            </el-option>
          </el-select>
        </el-form-item>
        
        <el-divider content-position="left">尺寸规格</el-divider>
        
        <el-alert title="制作规范提示" type="info" :closable="false" show-icon style="margin-bottom: 15px;">
          <ul slot="description" style="margin: 5px 0; padding-left: 20px;">
            <li>推荐制作区间：长度 30-60mm，宽度 20-40mm</li>
            <li>心形吊坠建议长宽比 1.2:1，佩戴效果最佳</li>
            <li>圆形吊坠建议长宽尺寸一致，直径 30-45mm</li>
            <li>水滴形吊坠建议长宽比 1.5:1，线条更流畅</li>
          </ul>
        </el-alert>
        
        <el-form-item label="长度 (mm)" prop="length">
          <el-input-number v-model="form.length" :min="20" :max="100" :step="1" @blur="validateField('length')" @change="validateField('length')"></el-input-number>
          <span v-if="form.length < 30 || form.length > 60" style="color: #e6a23c; margin-left: 10px; font-size: 12px;">
            ⚠️ 超出推荐区间 (30-60mm)
          </span>
        </el-form-item>
        
        <el-form-item label="宽度 (mm)" prop="width">
          <el-input-number v-model="form.width" :min="15" :max="80" :step="1" @blur="validateField('width')" @change="validateField('width')"></el-input-number>
          <span v-if="form.width < 20 || form.width > 40" style="color: #e6a23c; margin-left: 10px; font-size: 12px;">
            ⚠️ 超出推荐区间 (20-40mm)
          </span>
        </el-form-item>
        
        <el-divider content-position="left">内包花纹</el-divider>
        
        <el-form-item label="花纹选择" prop="pattern">
          <el-radio-group v-model="form.pattern" @change="validateField('pattern')">
            <el-radio v-for="pattern in patternOptions" :key="pattern.value" :label="pattern.value">
              {{ pattern.label }}
            </el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-divider content-position="left">挂扣类型</el-divider>
        
        <el-form-item label="挂扣选择" prop="clasp">
          <el-select v-model="form.clasp" placeholder="请选择挂扣类型" style="width: 100%">
            <el-option v-for="clasp in claspOptions" :key="clasp.value" :label="clasp.label" :value="clasp.value">
            </el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="备注">
          <el-input type="textarea" v-model="form.remark" :rows="3" placeholder="其他特殊要求"></el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="submitOrder" :loading="submitting">提交订单</el-button>
          <el-button @click="resetForm">重置</el-button>
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
      form: {
        customerName: '',
        phone: '',
        color: '',
        shape: '',
        length: 40,
        width: 25,
        pattern: '',
        clasp: '',
        remark: ''
      },
      rules: {
        customerName: [{ required: true, message: '请输入客户姓名', trigger: 'blur' }],
        phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }],
        color: [{ required: true, message: '请选择琉璃色料', trigger: 'blur' }],
        shape: [{ required: true, message: '请选择吊坠形状', trigger: 'blur' }],
        length: [
          { required: true, message: '请输入长度', trigger: 'blur' },
          { type: 'number', min: 20, max: 100, message: '长度范围为20-100mm', trigger: 'blur' }
        ],
        width: [
          { required: true, message: '请输入宽度', trigger: 'blur' },
          { type: 'number', min: 15, max: 80, message: '宽度范围为15-80mm', trigger: 'blur' }
        ],
        pattern: [{ required: true, message: '请选择内包花纹', trigger: 'blur' }],
        clasp: [{ required: true, message: '请选择挂扣类型', trigger: 'blur' }]
      },
      colorOptions: [
        { label: '宝石红', value: '#E74C3C' },
        { label: '天空蓝', value: '#3498DB' },
        { label: '翡翠绿', value: '#2ECC71' },
        { label: '皇家紫', value: '#9B59B6' },
        { label: '琥珀金', value: '#F39C12' },
        { label: '水晶透明', value: '#ECF0F1' }
      ],
      shapeOptions: [
        { label: '心形', value: 'heart' },
        { label: '圆形', value: 'circle' },
        { label: '椭圆形', value: 'oval' },
        { label: '水滴形', value: 'drop' },
        { label: '方形', value: 'square' },
        { label: '菱形', value: 'diamond' }
      ],
      patternOptions: [
        { label: '祥云纹', value: 'cloud' },
        { label: '莲花纹', value: 'lotus' },
        { label: '龙凤纹', value: 'dragon' },
        { label: '水波纹', value: 'wave' },
        { label: '无花纹', value: 'none' }
      ],
      claspOptions: [
        { label: '银质龙虾扣', value: 'silver_lobster' },
        { label: '金色弹簧扣', value: 'gold_spring' },
        { label: '玫瑰金卡扣', value: 'rose_gold' },
        { label: '编织绳结', value: 'rope' }
      ]
    }
  },
  methods: {
    validateField(field) {
      this.$refs.form.validateField(field)
    },
    submitOrder() {
      this.$refs.form.validate(valid => {
        if (valid) {
          this.submitting = true
          setTimeout(() => {
            const now = new Date().toLocaleString()
            const order = {
              id: Date.now(),
              ...this.form,
              status: 0,
              createTime: now,
              statusTimestamps: {
                '0': now
              },
              statusOperators: {
                '0': { id: 'SYS', name: '系统', role: '下单', time: now }
              },
              isNew: true
            }
            const orders = JSON.parse(localStorage.getItem('glassOrders') || '[]')
            orders.unshift(order)
            localStorage.setItem('glassOrders', JSON.stringify(orders))
            this.submitting = false
            this.$message.success('订单提交成功！')
            this.resetForm()
            this.$router.push({ path: '/admin', query: { newOrderId: order.id } })
          }, 1000)
        }
      })
    },
    resetForm() {
      this.$refs.form.resetFields()
    }
  }
}
</script>

<style scoped>
.order-form {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
.page-header {
  text-align: center;
  margin-bottom: 30px;
}
.page-header h1 {
  color: #333;
  margin-bottom: 10px;
}
.page-header p {
  color: #666;
}
.form-card {
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}
.color-preview {
  display: inline-block;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  margin-right: 5px;
  vertical-align: middle;
  border: 1px solid #ddd;
}
</style>
