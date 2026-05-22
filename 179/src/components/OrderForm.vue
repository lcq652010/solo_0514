<template>
  <div class="order-form-container">
    <div class="page-header">
      <h2>玉雕平安扣定制</h2>
      <p>请选择您的定制参数</p>
    </div>

    <el-card class="form-card">
      <el-form :model="orderForm" :rules="rules" ref="orderForm" label-width="120px">
        <el-form-item label="玉料种类" prop="jadeType">
          <el-select v-model="orderForm.jadeType" placeholder="请选择玉料种类" style="width: 100%" @change="validateField('jadeType')">
            <el-option label="和田玉" value="和田玉"></el-option>
            <el-option label="翡翠" value="翡翠"></el-option>
            <el-option label="岫玉" value="岫玉"></el-option>
            <el-option label="蓝田玉" value="蓝田玉"></el-option>
            <el-option label="独山玉" value="独山玉"></el-option>
          </el-select>
          <div v-if="fieldErrors.jadeType" class="field-error">
            <i class="el-icon-error"></i> {{ fieldErrors.jadeType }}
          </div>
        </el-form-item>

        <el-form-item label="平安扣直径 (mm)" prop="diameter">
          <el-input-number v-model="orderForm.diameter" :min="20" :max="100" :step="1" style="width: 100%" @change="validateField('diameter')"></el-input-number>
          <div class="process-range">
            <i class="el-icon-info"></i>
            <span>工艺标准范围：<strong>30-60mm</strong>（推荐直径40mm）</span>
            <el-tag v-if="orderForm.diameter < 30" size="mini" type="warning">偏小</el-tag>
            <el-tag v-if="orderForm.diameter > 60" size="mini" type="warning">偏大</el-tag>
            <el-tag v-if="orderForm.diameter >= 30 && orderForm.diameter <= 60" size="mini" type="success">标准</el-tag>
          </div>
          <div v-if="fieldErrors.diameter" class="field-error">
            <i class="el-icon-error"></i> {{ fieldErrors.diameter }}
          </div>
        </el-form-item>

        <el-form-item label="厚度规格" prop="thickness">
          <el-radio-group v-model="orderForm.thickness" @change="validateField('thickness')">
            <el-radio label="薄款 (6-8mm)"></el-radio>
            <el-radio label="标准款 (8-10mm)"></el-radio>
            <el-radio label="厚款 (10-12mm)"></el-radio>
          </el-radio-group>
          <div class="process-range" style="margin-top: 8px">
            <i class="el-icon-info"></i>
            <span>工艺标准厚度：<strong>6-12mm</strong></span>
          </div>
          <div v-if="fieldErrors.thickness" class="field-error" style="margin-top: 5px">
            <i class="el-icon-error"></i> {{ fieldErrors.thickness }}
          </div>
        </el-form-item>

        <el-form-item label="雕刻纹路" prop="carvingPattern">
          <el-select v-model="orderForm.carvingPattern" placeholder="请选择雕刻纹路" style="width: 100%" @change="validateField('carvingPattern')">
            <el-option label="光面无纹" value="光面无纹"></el-option>
            <el-option label="祥云纹" value="祥云纹"></el-option>
            <el-option label="回纹" value="回纹"></el-option>
            <el-option label="莲花纹" value="莲花纹"></el-option>
            <el-option label="龙凤纹" value="龙凤纹"></el-option>
          </el-select>
          <div v-if="fieldErrors.carvingPattern" class="field-error">
            <i class="el-icon-error"></i> {{ fieldErrors.carvingPattern }}
          </div>
        </el-form-item>

        <el-form-item label="抛光等级" prop="polishLevel">
          <el-radio-group v-model="orderForm.polishLevel">
            <el-radio label="初级抛光"></el-radio>
            <el-radio label="中级抛光"></el-radio>
            <el-radio label="高级精抛"></el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="客户姓名" prop="customerName">
          <el-input v-model="orderForm.customerName" placeholder="请输入您的姓名"></el-input>
        </el-form-item>

        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="orderForm.phone" placeholder="请输入联系电话"></el-input>
        </el-form-item>

        <el-form-item label="备注信息">
          <el-input type="textarea" v-model="orderForm.remark" :rows="3" placeholder="其他特殊要求"></el-input>
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
      fieldErrors: {
        jadeType: '',
        diameter: '',
        thickness: '',
        carvingPattern: ''
      },
      orderForm: {
        jadeType: '',
        diameter: 50,
        thickness: '标准款 (8-10mm)',
        carvingPattern: '',
        polishLevel: '',
        customerName: '',
        phone: '',
        remark: ''
      },
      rules: {
        jadeType: [{ required: true, message: '请选择玉料种类', trigger: 'change' }],
        diameter: [
          { required: true, message: '请输入直径', trigger: 'blur' },
          { type: 'number', min: 20, max: 100, message: '直径必须在20-100mm之间', trigger: 'blur' }
        ],
        thickness: [{ required: true, message: '请选择厚度规格', trigger: 'change' }],
        carvingPattern: [{ required: true, message: '请选择雕刻纹路', trigger: 'change' }],
        polishLevel: [{ required: true, message: '请选择抛光等级', trigger: 'change' }],
        customerName: [{ required: true, message: '请输入客户姓名', trigger: 'blur' }],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    validateField(field) {
      this.fieldErrors[field] = ''
      switch(field) {
        case 'jadeType':
          if (!this.orderForm.jadeType) {
            this.fieldErrors.jadeType = '请选择玉料种类'
          }
          break
        case 'diameter':
          if (!this.orderForm.diameter) {
            this.fieldErrors.diameter = '请输入直径'
          } else if (this.orderForm.diameter < 20 || this.orderForm.diameter > 100) {
            this.fieldErrors.diameter = '直径必须在20-100mm之间'
          }
          break
        case 'thickness':
          if (!this.orderForm.thickness) {
            this.fieldErrors.thickness = '请选择厚度规格'
          }
          break
        case 'carvingPattern':
          if (!this.orderForm.carvingPattern) {
            this.fieldErrors.carvingPattern = '请选择雕刻纹路'
          }
          break
      }
    },
    submitOrder() {
      this.$refs.orderForm.validate((valid) => {
        if (valid) {
          this.submitting = true
          setTimeout(() => {
            const orders = JSON.parse(localStorage.getItem('jadeOrders') || '[]')
            const newOrder = {
              id: Date.now(),
              ...this.orderForm,
              status: 0,
              statusHistory: [
                { status: 0, time: new Date().toLocaleString(), remark: '订单创建' }
              ],
              createTime: new Date().toLocaleString()
            }
            orders.unshift(newOrder)
            localStorage.setItem('jadeOrders', JSON.stringify(orders))
            
            this.submitting = false
            this.$message.success('订单提交成功！')
            this.$router.push({ path: '/admin', query: { newOrderId: newOrder.id } })
          }, 1000)
        }
      })
    },
    resetForm() {
      this.$refs.orderForm.resetFields()
      this.fieldErrors = {
        jadeType: '',
        diameter: '',
        thickness: '',
        carvingPattern: ''
      }
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

.page-header {
  text-align: center;
  margin-bottom: 30px;
}

.page-header h2 {
  color: #409EFF;
  margin-bottom: 10px;
}

.page-header p {
  color: #606266;
}

.form-card {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.field-error {
  color: #f56c6c;
  font-size: 12px;
  margin-top: 4px;
  line-height: 1.5;
}

.process-range {
  font-size: 12px;
  color: #909399;
  margin-top: 6px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.process-range i {
  color: #409EFF;
}

.process-range strong {
  color: #606266;
  margin: 0 2px;
}

.process-range .el-tag {
  margin-left: 8px;
}
</style>
