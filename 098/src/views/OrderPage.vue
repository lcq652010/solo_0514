<template>
  <div class="order-page">
    <el-card class="order-card" shadow="hover">
      <div slot="header" class="card-header">
        <span><i class="el-icon-edit"></i> 印章定制下单</span>
      </div>
      
      <el-form :model="orderForm" :rules="rules" ref="orderForm" label-width="120px" class="order-form">
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

        <el-form-item label="竹材种类" prop="bambooType">
          <el-select v-model="orderForm.bambooType" placeholder="请选择竹材种类" style="width: 100%;">
            <el-option label="毛竹" value="毛竹"></el-option>
            <el-option label="紫竹" value="紫竹"></el-option>
            <el-option label="湘妃竹" value="湘妃竹"></el-option>
            <el-option label="罗汉竹" value="罗汉竹"></el-option>
            <el-option label="玉竹" value="玉竹"></el-option>
            <el-option label="棕竹" value="棕竹"></el-option>
          </el-select>
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="印章直径(mm)" prop="diameter">
              <el-input-number v-model="orderForm.diameter" :min="10" :max="100" style="width: 100%;"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="印章高度(mm)" prop="height">
              <el-input-number v-model="orderForm.height" :min="20" :max="200" style="width: 100%;"></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="印文内容" prop="sealContent">
          <el-input
            v-model="orderForm.sealContent"
            type="textarea"
            :rows="3"
            placeholder="请输入印文内容（通常为2-4字）"
            maxlength="20"
            show-word-limit
          ></el-input>
        </el-form-item>

        <el-form-item label="图案选择" prop="pattern">
          <el-select v-model="orderForm.pattern" placeholder="请选择图案" style="width: 100%;">
            <el-option label="龙凤呈祥" value="龙凤呈祥"></el-option>
            <el-option label="祥云瑞气" value="祥云瑞气"></el-option>
            <el-option label="梅兰竹菊" value="梅兰竹菊"></el-option>
            <el-option label="山水意境" value="山水意境"></el-option>
            <el-option label="花鸟鱼虫" value="花鸟鱼虫"></el-option>
            <el-option label="素面无纹" value="素面无纹"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="字体选择" prop="fontType">
          <el-radio-group v-model="orderForm.fontType">
            <el-radio label="小篆">小篆</el-radio>
            <el-radio label="大篆">大篆</el-radio>
            <el-radio label="隶书">隶书</el-radio>
            <el-radio label="楷书">楷书</el-radio>
            <el-radio label="行书">行书</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="工艺选择" prop="craft">
          <el-select v-model="orderForm.craft" placeholder="请选择工艺" style="width: 100%;">
            <el-option label="手工雕刻" value="手工雕刻"></el-option>
            <el-option label="激光雕刻" value="激光雕刻"></el-option>
            <el-option label="浮雕工艺" value="浮雕工艺"></el-option>
            <el-option label="阴刻工艺" value="阴刻工艺"></el-option>
            <el-option label="阳刻工艺" value="阳刻工艺"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="备注说明">
          <el-input
            v-model="orderForm.remark"
            type="textarea"
            :rows="2"
            placeholder="如有特殊要求请在此说明"
          ></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitOrder" :loading="submitting">
            <i class="el-icon-check"></i> 提交订单
          </el-button>
          <el-button @click="resetForm">
            <i class="el-icon-refresh"></i> 重置表单
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-dialog title="订单提交成功" :visible.sync="dialogVisible" width="500px" @closed="handleDialogClosed">
      <div class="success-content">
        <i class="el-icon-success success-icon"></i>
        <p>您的订单已成功提交！</p>
        <p class="order-no">订单编号：{{ newOrderNo }}</p>
        <p>我们将尽快为您处理，请注意查收通知。</p>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="closeDialog">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'OrderPage',
  data() {
    return {
      orderForm: {
        customerName: '',
        phone: '',
        bambooType: '',
        diameter: 30,
        height: 60,
        sealContent: '',
        pattern: '',
        fontType: '小篆',
        craft: '',
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
        bambooType: [
          { required: true, message: '请选择竹材种类', trigger: 'change' }
        ],
        diameter: [
          { required: true, message: '请输入印章直径', trigger: 'change' },
          { type: 'number', min: 10, max: 100, message: '直径范围应在10-100mm之间', trigger: 'change' }
        ],
        height: [
          { required: true, message: '请输入印章高度', trigger: 'change' },
          { type: 'number', min: 20, max: 200, message: '高度范围应在20-200mm之间', trigger: 'change' }
        ],
        sealContent: [
          { required: true, message: '请输入印文内容', trigger: 'blur' }
        ],
        pattern: [
          { required: true, message: '请选择图案', trigger: 'change' }
        ],
        craft: [
          { required: true, message: '请选择工艺', trigger: 'change' }
        ]
      },
      submitting: false,
      dialogVisible: false,
      newOrderNo: ''
    }
  },
  methods: {
    submitOrder() {
      this.$refs.orderForm.validate((valid) => {
        if (valid) {
          this.submitting = true
          setTimeout(() => {
            this.submitting = false
            this.newOrderNo = 'SEAL' + Date.now().toString().slice(-8)
            this.dialogVisible = true
            
            const orders = JSON.parse(localStorage.getItem('sealOrders') || '[]')
            const now = this.formatDate(new Date())
            const newOrder = {
              id: Date.now(),
              orderNo: this.newOrderNo,
              ...this.orderForm,
              status: '选料',
              createTime: now,
              statusHistory: [
                { status: '选料', time: now }
              ]
            }
            orders.unshift(newOrder)
            localStorage.setItem('sealOrders', JSON.stringify(orders))
            window.dispatchEvent(new CustomEvent('orderUpdated'))
          }, 1000)
        }
      })
    },
    closeDialog() {
      this.dialogVisible = false
    },
    handleDialogClosed() {
      this.resetForm()
    },
    resetForm() {
      this.$refs.orderForm.resetFields()
      this.orderForm.fontType = '小篆'
      this.orderForm.diameter = 30
      this.orderForm.height = 60
    },
    formatDate(date) {
      const y = date.getFullYear()
      const m = String(date.getMonth() + 1).padStart(2, '0')
      const d = String(date.getDate()).padStart(2, '0')
      const h = String(date.getHours()).padStart(2, '0')
      const min = String(date.getMinutes()).padStart(2, '0')
      return `${y}-${m}-${d} ${h}:${min}`
    }
  }
}
</script>

<style scoped>
.order-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.order-card {
  border-radius: 8px;
}

.card-header {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
  display: flex;
  align-items: center;
}

.card-header i {
  margin-right: 8px;
  color: #409EFF;
}

.order-form {
  padding: 20px 0;
}

.success-content {
  text-align: center;
  padding: 20px 0;
}

.success-icon {
  font-size: 60px;
  color: #67C23A;
  margin-bottom: 20px;
}

.success-content p {
  font-size: 16px;
  color: #606266;
  margin-bottom: 10px;
}

.order-no {
  font-weight: bold;
  color: #409EFF;
  font-size: 18px;
}
</style>
