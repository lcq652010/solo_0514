<template>
  <div class="page-container">
    <el-card class="card-box">
      <div slot="header" class="clearfix">
        <span>寄件下单</span>
      </div>
      <el-form :model="orderForm" :rules="rules" ref="orderForm" label-width="120px" class="demo-ruleForm">
        <el-divider content-position="left">寄件人信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="寄件人姓名" prop="senderName">
              <el-input v-model="orderForm.senderName" placeholder="请输入寄件人姓名"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="senderPhone">
              <el-input v-model="orderForm.senderPhone" placeholder="请输入联系电话"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="寄件地址" prop="senderAddress">
          <el-input type="textarea" v-model="orderForm.senderAddress" :rows="2" placeholder="请输入详细地址"></el-input>
        </el-form-item>
        
        <el-divider content-position="left">收件人信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="收件人姓名" prop="receiverName">
              <el-input v-model="orderForm.receiverName" placeholder="请输入收件人姓名"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="receiverPhone">
              <el-input v-model="orderForm.receiverPhone" placeholder="请输入联系电话"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="收件地址" prop="receiverAddress">
          <el-input type="textarea" v-model="orderForm.receiverAddress" :rows="2" placeholder="请输入详细地址"></el-input>
        </el-form-item>
        
        <el-divider content-position="left">包裹信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="物品类型" prop="goodsType">
              <el-select v-model="orderForm.goodsType" placeholder="请选择物品类型" style="width: 100%;">
                <el-option label="文件资料" value="文件资料"></el-option>
                <el-option label="电子产品" value="电子产品"></el-option>
                <el-option label="服装鞋帽" value="服装鞋帽"></el-option>
                <el-option label="食品生鲜" value="食品生鲜"></el-option>
                <el-option label="日常用品" value="日常用品"></el-option>
                <el-option label="其他" value="其他"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="重量(kg)" prop="weight">
              <el-input-number v-model="orderForm.weight" :min="0.1" :step="0.1" style="width: 100%;"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="快递类型" prop="expressType">
              <el-select v-model="orderForm.expressType" placeholder="请选择快递类型" style="width: 100%;">
                <el-option label="普通快递" value="普通快递"></el-option>
                <el-option label="加急快递" value="加急快递"></el-option>
                <el-option label="冷链运输" value="冷链运输"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="预估运费(元)" prop="freight">
              <el-input v-model="orderForm.freight" disabled placeholder="系统自动计算"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="付款方式" prop="payType">
              <el-radio-group v-model="orderForm.payType">
                <el-radio label="寄付">寄付</el-radio>
                <el-radio label="到付">到付</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="备注">
          <el-input type="textarea" v-model="orderForm.remark" :rows="3" placeholder="请输入备注信息（选填）"></el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="submitForm" size="large">提交订单</el-button>
          <el-button @click="resetForm" size="large">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'SendOrder',
  data() {
    const validatePhone = (rule, value, callback) => {
      const reg = /^1[3-9]\d{9}$/
      if (!value) {
        callback(new Error('请输入手机号码'))
      } else if (!reg.test(value)) {
        callback(new Error('请输入正确的手机号码格式'))
      } else {
        callback()
      }
    }
    return {
      orderForm: {
        senderName: '',
        senderPhone: '',
        senderAddress: '',
        receiverName: '',
        receiverPhone: '',
        receiverAddress: '',
        goodsType: '',
        weight: 1,
        expressType: '普通快递',
        freight: '',
        payType: '寄付',
        remark: ''
      },
      rules: {
        senderName: [
          { required: true, message: '请输入寄件人姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        senderPhone: [
          { required: true, validator: validatePhone, trigger: 'blur' }
        ],
        senderAddress: [
          { required: true, message: '请输入寄件地址', trigger: 'blur' }
        ],
        receiverName: [
          { required: true, message: '请输入收件人姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        receiverPhone: [
          { required: true, validator: validatePhone, trigger: 'blur' }
        ],
        receiverAddress: [
          { required: true, message: '请输入收件地址', trigger: 'blur' }
        ],
        goodsType: [
          { required: true, message: '请选择物品类型', trigger: 'change' }
        ],
        weight: [
          { required: true, message: '请输入重量', trigger: 'blur' }
        ],
        expressType: [
          { required: true, message: '请选择快递类型', trigger: 'change' }
        ]
      }
    }
  },
  watch: {
    'orderForm.weight': 'calculateFreight',
    'orderForm.expressType': 'calculateFreight'
  },
  methods: {
    calculateFreight() {
      let basePrice = 10
      if (this.orderForm.expressType === '加急快递') {
        basePrice = 15
      } else if (this.orderForm.expressType === '冷链运输') {
        basePrice = 20
      }
      const weight = this.orderForm.weight || 1
      this.orderForm.freight = (basePrice + (weight - 1) * 3).toFixed(2)
    },
    submitForm() {
      this.$refs.orderForm.validate((valid) => {
        if (valid) {
          this.$message.success('订单提交成功！')
          console.log('订单信息：', this.orderForm)
          this.resetForm()
        } else {
          this.$message.error('请检查表单信息是否填写正确')
          return false
        }
      })
    },
    resetForm() {
      this.$refs.orderForm.resetFields()
      this.orderForm.weight = 1
      this.orderForm.freight = ''
    }
  },
  mounted() {
    this.calculateFreight()
  }
}
</script>

<style scoped>
.el-card {
  max-width: 900px;
  margin: 0 auto;
}

.el-divider {
  margin: 20px 0;
}

.el-divider__text {
  font-weight: 500;
  color: #409EFF;
}
</style>
