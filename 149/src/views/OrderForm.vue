<template>
  <div class="order-form">
    <div class="page-header">
      <h1>传统手工油纸伞定制</h1>
      <p>匠心传承 · 手工精制</p>
    </div>
    
    <el-card class="form-card">
      <el-form :model="form" :rules="rules" ref="form" label-width="120px">
        <el-form-item label="客户姓名" prop="customerName">
          <el-input v-model="form.customerName" placeholder="请输入您的姓名"></el-input>
        </el-form-item>
        
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入联系电话"></el-input>
        </el-form-item>
        
        <el-form-item label="伞骨材质" prop="frameMaterial">
          <el-select v-model="form.frameMaterial" placeholder="请选择伞骨材质" style="width: 100%">
            <el-option label="紫竹" value="紫竹"></el-option>
            <el-option label="毛竹" value="毛竹"></el-option>
            <el-option label="罗汉竹" value="罗汉竹"></el-option>
            <el-option label="湘妃竹" value="湘妃竹"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="伞面直径(cm)" prop="diameter">
          <el-input-number v-model="form.diameter" :min="50" :max="120" :step="5" @change="onDiameterChange"></el-input-number>
          <span :style="diameterTipStyle" style="margin-left: 10px;">{{ diameterTip }}</span>
        </el-form-item>
        
        <el-form-item label="伞面图案" prop="pattern">
          <el-radio-group v-model="form.pattern">
            <el-radio label="山水">山水</el-radio>
            <el-radio label="花鸟">花鸟</el-radio>
            <el-radio label="龙凤">龙凤</el-radio>
            <el-radio label="梅兰竹菊">梅兰竹菊</el-radio>
            <el-radio label="纯色">纯色</el-radio>
            <el-radio label="定制">定制图案</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="伞柄款式" prop="handleStyle">
          <el-select v-model="form.handleStyle" placeholder="请选择伞柄款式" style="width: 100%">
            <el-option label="直柄" value="直柄"></el-option>
            <el-option label="弯柄" value="弯柄"></el-option>
            <el-option label="龙头柄" value="龙头柄"></el-option>
            <el-option label="如意柄" value="如意柄"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="流苏配色" prop="tasselColor">
          <el-color-picker v-model="form.tasselColor" show-alpha></el-color-picker>
          <span style="margin-left: 10px;">常用配色：大红、金黄、湖蓝、墨绿</span>
        </el-form-item>
        
        <el-form-item label="备注">
          <el-input
            type="textarea"
            :rows="4"
            placeholder="如有特殊要求请在此说明"
            v-model="form.remark">
          </el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="submitForm" size="large" style="width: 200px;">提交订单</el-button>
          <el-button @click="resetForm" size="large" style="margin-left: 20px;">重置</el-button>
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
      form: {
        customerName: '',
        phone: '',
        frameMaterial: '',
        diameter: 84,
        pattern: '',
        handleStyle: '',
        tasselColor: '#ff0000',
        remark: ''
      },
      rules: {
        customerName: [
          { required: true, message: '请输入客户姓名', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
        ],
        frameMaterial: [
          { required: true, message: '请选择伞骨材质', trigger: 'change' }
        ],
        pattern: [
          { required: true, message: '请选择伞面图案', trigger: 'change' }
        ],
        handleStyle: [
          { required: true, message: '请选择伞柄款式', trigger: 'change' }
        ],
        diameter: [
          { required: true, message: '请输入伞面直径', trigger: 'change' },
          { type: 'number', min: 50, max: 120, message: '直径必须在50-120cm之间', trigger: 'change' }
        ]
      }
    }
  },
  computed: {
    diameterTip() {
      const d = this.form.diameter
      if (d < 60) {
        return '⚠️ 尺寸较小，适合儿童使用'
      } else if (d >= 60 && d < 75) {
        return 'ℹ️ 尺寸适中，适合便携使用'
      } else if (d >= 75 && d <= 90) {
        return '✅ 标准尺寸，适合大多数场景'
      } else if (d > 90 && d <= 105) {
        return 'ℹ️ 尺寸较大，遮阳效果更佳'
      } else {
        return '⚠️ 超大尺寸，适合特定场合'
      }
    },
    diameterTipStyle() {
      const d = this.form.diameter
      if (d < 60 || d > 105) {
        return { color: '#E6A23C' }
      } else if (d >= 75 && d <= 90) {
        return { color: '#67C23A' }
      } else {
        return { color: '#909399' }
      }
    }
  },
  methods: {
    onDiameterChange() {
    },
    submitForm() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          const orders = JSON.parse(localStorage.getItem('umbrellaOrders') || '[]')
          const newOrder = {
            id: Date.now(),
            ...this.form,
            status: 0,
            createTime: new Date().toLocaleString()
          }
          orders.unshift(newOrder)
          localStorage.setItem('umbrellaOrders', JSON.stringify(orders))
          
          this.$message({
            type: 'success',
            message: '订单提交成功！我们将尽快为您制作'
          })
          this.resetForm()
        }
      })
    },
    resetForm() {
      this.$refs.form.resetFields()
      this.form.diameter = 84
      this.form.tasselColor = '#ff0000'
    }
  }
}
</script>

<style scoped>
.order-form {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 40px 0;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  font-size: 36px;
  color: #303133;
  margin-bottom: 10px;
  font-family: '楷体', serif;
}

.page-header p {
  font-size: 18px;
  color: #606266;
}

.form-card {
  max-width: 800px;
  margin: 0 auto;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #303133;
}
</style>
