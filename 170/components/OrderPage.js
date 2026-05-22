Vue.component('OrderPage', {
  template: `
    <div class="order-page">
      <el-card class="order-card">
        <div slot="header" class="card-header">
          <span>麦秆画定制 - 客户下单</span>
        </div>
        
        <el-form :model="orderForm" :rules="rules" ref="orderForm" label-width="120px">
          <el-form-item label="客户姓名" prop="customerName">
            <el-input v-model="orderForm.customerName" placeholder="请输入您的姓名"></el-input>
          </el-form-item>
          
          <el-form-item label="联系电话" prop="phone">
            <el-input v-model="orderForm.phone" placeholder="请输入联系电话"></el-input>
          </el-form-item>
          
          <el-form-item label="麦秆选材等级" prop="materialLevel">
            <el-select v-model="orderForm.materialLevel" placeholder="请选择麦秆等级" style="width: 100%">
              <el-option label="A级（精选优质麦秆）" value="A"></el-option>
              <el-option label="B级（标准麦秆）" value="B"></el-option>
              <el-option label="C级（普通麦秆）" value="C"></el-option>
            </el-select>
          </el-form-item>
          
          <el-form-item label="画面尺寸">
            <el-col :span="11">
              <el-form-item prop="width">
                <el-input v-model.number="orderForm.width" placeholder="宽度（cm）" @input="updateSizeTip"></el-input>
              </el-form-item>
            </el-col>
            <el-col class="line" :span="2" style="text-align: center">×</el-col>
            <el-col :span="11">
              <el-form-item prop="height">
                <el-input v-model.number="orderForm.height" placeholder="高度（cm）" @input="updateSizeTip"></el-input>
              </el-form-item>
            </el-col>
            <div class="size-tip" :class="sizeTipType">
              <i :class="sizeTipIcon"></i>
              <span>{{ sizeTipText }}</span>
            </div>
          </el-form-item>
          
          <el-form-item label="题材风格" prop="style">
            <el-radio-group v-model="orderForm.style">
              <el-radio label="山水画">山水画</el-radio>
              <el-radio label="花鸟图">花鸟图</el-radio>
              <el-radio label="人物肖像">人物肖像</el-radio>
              <el-radio label="民俗风情">民俗风情</el-radio>
              <el-radio label="其他">其他</el-radio>
            </el-radio-group>
          </el-form-item>
          
          <el-form-item label="裱框类型" prop="frameType">
            <el-select v-model="orderForm.frameType" placeholder="请选择裱框类型" style="width: 100%">
              <el-option label="实木框（胡桃木）" value="walnut"></el-option>
              <el-option label="实木框（橡木）" value="oak"></el-option>
              <el-option label="铝合金框" value="aluminum"></el-option>
              <el-option label="无框" value="none"></el-option>
            </el-select>
          </el-form-item>
          
          <el-form-item label="加签名款">
            <el-switch v-model="orderForm.withSignature" active-text="是" inactive-text="否"></el-switch>
          </el-form-item>
          
          <el-form-item label="备注说明">
            <el-input type="textarea" v-model="orderForm.remarks" :rows="4" placeholder="请输入其他定制要求..."></el-input>
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="submitForm" size="large" style="width: 100%">提交订单</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  `,
  data() {
    const validateMaterial = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请选择麦秆等级'))
      } else if (!['A', 'B', 'C'].includes(value)) {
        callback(new Error('麦秆等级必须为A、B或C'))
      } else {
        callback()
      }
    }
    
    const validateSize = (min, max) => (rule, value, callback) => {
      if (value === '' || value === undefined || value === null) {
        callback(new Error('请输入尺寸'))
      } else if (isNaN(value)) {
        callback(new Error('请输入有效数字'))
      } else if (value < min) {
        callback(new Error(`尺寸不能小于${min}cm`))
      } else if (value > max) {
        callback(new Error(`尺寸不能大于${max}cm`))
      } else {
        callback()
      }
    }
    
    const validateStyle = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请选择题材风格'))
      } else if (!['山水画', '花鸟图', '人物肖像', '民俗风情', '其他'].includes(value)) {
        callback(new Error('请选择有效的题材风格'))
      } else {
        callback()
      }
    }
    
    const validateFrame = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请选择裱框类型'))
      } else if (!['walnut', 'oak', 'aluminum', 'none'].includes(value)) {
        callback(new Error('请选择有效的裱框类型'))
      } else {
        callback()
      }
    }
    
    return {
      orderForm: {
        customerName: '',
        phone: '',
        materialLevel: '',
        width: '',
        height: '',
        style: '',
        frameType: '',
        withSignature: false,
        remarks: ''
      },
      sizeTipText: '工艺推荐尺寸：宽度 30-100cm，高度 30-80cm',
      sizeTipType: 'tip-info',
      sizeTipIcon: 'el-icon-info',
      rules: {
        customerName: [
          { required: true, message: '请输入客户姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '姓名长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
        ],
        materialLevel: [
          { validator: validateMaterial, trigger: 'change' }
        ],
        width: [
          { validator: validateSize(10, 200), trigger: 'blur' }
        ],
        height: [
          { validator: validateSize(10, 200), trigger: 'blur' }
        ],
        style: [
          { validator: validateStyle, trigger: 'change' }
        ],
        frameType: [
          { validator: validateFrame, trigger: 'change' }
        ]
      }
    }
  },
  methods: {
    updateSizeTip() {
      const width = this.orderForm.width
      const height = this.orderForm.height
      
      if (!width && !height) {
        this.sizeTipText = '工艺推荐尺寸：宽度 30-100cm，高度 30-80cm'
        this.sizeTipType = 'tip-info'
        this.sizeTipIcon = 'el-icon-info'
        return
      }
      
      const widthValid = width >= 30 && width <= 100
      const heightValid = height >= 30 && height <= 80
      
      if (width && height) {
        const area = width * height
        if (widthValid && heightValid) {
          this.sizeTipText = `尺寸符合工艺标准！面积 ${area} cm²，标准制作周期 7-10 天`
          this.sizeTipType = 'tip-success'
          this.sizeTipIcon = 'el-icon-success'
        } else {
          const issues = []
          if (!widthValid) issues.push('宽度超出推荐范围')
          if (!heightValid) issues.push('高度超出推荐范围')
          this.sizeTipText = `注意：${issues.join('，')}，可能增加制作成本和周期（当前面积 ${area} cm²）`
          this.sizeTipType = 'tip-warning'
          this.sizeTipIcon = 'el-icon-warning'
        }
      } else if (width) {
        if (widthValid) {
          this.sizeTipText = '当前宽度在推荐范围内，请继续输入高度'
          this.sizeTipType = 'tip-info'
          this.sizeTipIcon = 'el-icon-info'
        } else {
          this.sizeTipText = '当前宽度超出推荐范围（30-100cm），建议调整'
          this.sizeTipType = 'tip-warning'
          this.sizeTipIcon = 'el-icon-warning'
        }
      } else if (height) {
        if (heightValid) {
          this.sizeTipText = '当前高度在推荐范围内，请继续输入宽度'
          this.sizeTipType = 'tip-info'
          this.sizeTipIcon = 'el-icon-info'
        } else {
          this.sizeTipText = '当前高度超出推荐范围（30-80cm），建议调整'
          this.sizeTipType = 'tip-warning'
          this.sizeTipIcon = 'el-icon-warning'
        }
      }
    },
    submitForm() {
      this.$refs.orderForm.validate((valid) => {
        if (valid) {
          const orderData = {
            ...this.orderForm,
            id: Date.now(),
            status: 0,
            isNew: true,
            createTime: new Date().toLocaleString(),
            statusHistory: [
              { status: 0, time: new Date().toLocaleString(), remark: '订单创建', operator: '系统' }
            ]
          }
          this.$emit('submit-order', orderData)
          this.$message.success('订单提交成功！')
          this.resetForm()
        } else {
          this.$message.error('请完善订单信息')
          return false
        }
      })
    },
    resetForm() {
      this.$refs.orderForm.resetFields()
      this.updateSizeTip()
    }
  },
  mounted() {
    this.updateSizeTip()
  }
})
