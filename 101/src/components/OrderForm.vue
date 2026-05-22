<template>
  <div class="order-form-container">
    <el-card class="order-card" shadow="hover">
      <div slot="header" class="card-header">
        <span>传统漆雕墨盒定制 - 客户下单</span>
      </div>
      
      <el-form :model="orderForm" :rules="rules" ref="orderForm" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="胎体材质" prop="material">
              <el-select v-model="orderForm.material" placeholder="请选择胎体材质" style="width: 100%">
                <el-option label="紫铜" value="紫铜"></el-option>
                <el-option label="黄铜" value="黄铜"></el-option>
                <el-option label="木胎" value="木胎"></el-option>
                <el-option label="脱胎" value="脱胎"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="客户姓名" prop="customerName">
              <el-input v-model="orderForm.customerName" placeholder="请输入客户姓名"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="墨盒边长(mm)" prop="sideLength">
              <el-input-number v-model="orderForm.sideLength" :min="50" :max="300" :step="5" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="盒高(mm)" prop="height">
              <el-input-number v-model="orderForm.height" :min="20" :max="100" :step="5" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="雕漆层数" prop="layers">
              <el-select v-model="orderForm.layers" placeholder="请选择雕漆层数" style="width: 100%">
                <el-option label="10层" value="10层"></el-option>
                <el-option label="15层" value="15层"></el-option>
                <el-option label="20层" value="20层"></el-option>
                <el-option label="30层" value="30层"></el-option>
                <el-option label="50层" value="50层"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="orderForm.phone" placeholder="请输入联系电话"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="纹饰图案" prop="pattern">
          <el-radio-group v-model="orderForm.pattern">
            <el-radio label="云龙纹">云龙纹</el-radio>
            <el-radio label="花卉纹">花卉纹</el-radio>
            <el-radio label="山水纹">山水纹</el-radio>
            <el-radio label="花鸟纹">花鸟纹</el-radio>
            <el-radio label="福寿纹">福寿纹</el-radio>
            <el-radio label="龙凤纹">龙凤纹</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="备注说明">
          <el-input
            type="textarea"
            :rows="4"
            placeholder="请输入其他定制要求或备注"
            v-model="orderForm.remarks">
          </el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitOrder" :loading="submitting">提交订单</el-button>
          <el-button @click="resetForm">重置</el-button>
          <el-button type="success" @click="goToAdmin">管理员入口</el-button>
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
        material: '',
        sideLength: 100,
        height: 40,
        layers: '',
        pattern: '',
        remarks: ''
      },
      rules: {
        customerName: [
          { required: true, message: '请输入客户姓名', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
        ],
        material: [
          { required: true, message: '请选择胎体材质', trigger: 'change' }
        ],
        sideLength: [
          { required: true, message: '请输入墨盒边长', trigger: 'change' },
          { type: 'number', min: 50, max: 300, message: '墨盒边长需在 50-300mm 之间', trigger: 'change' }
        ],
        height: [
          { required: true, message: '请输入盒高', trigger: 'change' },
          { type: 'number', min: 20, max: 100, message: '盒高需在 20-100mm 之间', trigger: 'change' }
        ],
        layers: [
          { required: true, message: '请选择雕漆层数', trigger: 'change' }
        ],
        pattern: [
          { required: true, message: '请选择纹饰图案', trigger: 'change' }
        ]
      }
    }
  },
  methods: {
    submitOrder() {
      this.$refs.orderForm.validate((valid) => {
        if (valid) {
          this.submitting = true
          setTimeout(() => {
            const orders = JSON.parse(localStorage.getItem('lacquerOrders') || '[]')
            const newOrder = {
              id: Date.now(),
              orderNo: 'ORD' + Date.now(),
              ...this.orderForm,
              status: 0,
              statusText: '制胎',
              createTime: new Date().toLocaleString(),
              operationHistory: [
                {
                  status: 0,
                  statusText: '制胎',
                  operator: '系统',
                  operateTime: new Date().toLocaleString(),
                  remark: '订单创建'
                }
              ]
            }
            orders.unshift(newOrder)
            localStorage.setItem('lacquerOrders', JSON.stringify(orders))
            
            window.dispatchEvent(new StorageEvent('storage', {
              key: 'lacquerOrders',
              newValue: JSON.stringify(orders)
            }))
            
            this.submitting = false
            this.$message.success('订单提交成功！订单号：' + newOrder.orderNo)
            this.resetForm()
          }, 1000)
        } else {
          return false
        }
      })
    },
    resetForm() {
      this.$refs.orderForm.resetFields()
    },
    goToAdmin() {
      this.$router.push('/admin')
    }
  }
}
</script>

<style scoped>
.order-form-container {
  padding: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}
.order-card {
  max-width: 800px;
  margin: 0 auto;
  border-radius: 8px;
}
.card-header {
  font-size: 20px;
  font-weight: bold;
  color: #303133;
  text-align: center;
}
.el-radio {
  margin-right: 20px;
  margin-bottom: 10px;
}
</style>
