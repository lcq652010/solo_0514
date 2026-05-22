<template>
  <div class="order-form">
    <el-card class="form-card" shadow="hover">
      <div slot="header" class="card-header">
        <span>客户定制下单</span>
      </div>
      
      <el-form :model="orderForm" :rules="rules" ref="orderForm" label-width="120px">
        <el-divider content-position="left">基础信息</el-divider>
        
        <el-form-item label="客户姓名" prop="customerName">
          <el-input v-model="orderForm.customerName" placeholder="请输入姓名" style="width: 300px;"></el-input>
        </el-form-item>
        
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="orderForm.phone" placeholder="请输入联系电话" style="width: 300px;"></el-input>
        </el-form-item>
        
        <el-divider content-position="left">佛珠配置</el-divider>
        
        <el-form-item label="木料材质" prop="woodType">
          <el-select v-model="orderForm.woodType" placeholder="请选择木料" style="width: 300px;" @blur="validateField('woodType')">
            <el-option label="小叶紫檀" value="小叶紫檀"></el-option>
            <el-option label="海南黄花梨" value="海南黄花梨"></el-option>
            <el-option label="金丝楠木" value="金丝楠木"></el-option>
            <el-option label="老山檀香" value="老山檀香"></el-option>
            <el-option label="沉香木" value="沉香木"></el-option>
            <el-option label="酸枝木" value="酸枝木"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="珠子直径" prop="beadDiameter">
          <el-input-number 
            v-model="orderForm.beadDiameter" 
            :min="6" 
            :max="30" 
            :step="1" 
            style="width: 300px;" 
            @blur="validateField('beadDiameter')"
            @change="onDiameterChange"
          ></el-input-number>
          <span style="margin-left: 10px;">mm</span>
          <div class="diameter-hint" :class="diameterHintClass">
            <i :class="diameterIcon"></i>
            <span>{{ diameterHintText }}</span>
            <span class="range-tip">(生产推荐区间：10-20mm)</span>
          </div>
        </el-form-item>
        
        <el-form-item label="珠子颗数" prop="beadCount">
          <el-radio-group v-model="orderForm.beadCount" @change="validateField('beadCount')">
            <el-radio label="14">14颗</el-radio>
            <el-radio label="18">18颗</el-radio>
            <el-radio label="21">21颗</el-radio>
            <el-radio label="27">27颗</el-radio>
            <el-radio label="36">36颗</el-radio>
            <el-radio label="108">108颗</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="漆艺工艺" prop="lacquerTechnique">
          <el-select v-model="orderForm.lacquerTechnique" placeholder="请选择漆艺工艺" style="width: 300px;" @blur="validateField('lacquerTechnique')">
            <el-option label="大漆素髹" value="大漆素髹"></el-option>
            <el-option label="描金工艺" value="描金工艺"></el-option>
            <el-option label="螺钿镶嵌" value="螺钿镶嵌"></el-option>
            <el-option label="犀皮漆" value="犀皮漆"></el-option>
            <el-option label="雕漆工艺" value="雕漆工艺"></el-option>
            <el-option label="蛋壳镶嵌" value="蛋壳镶嵌"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="流苏款式" prop="tasselStyle">
          <el-select v-model="orderForm.tasselStyle" placeholder="请选择流苏款式" style="width: 300px;">
            <el-option label="传统中式流苏" value="传统中式流苏"></el-option>
            <el-option label="简洁款" value="简洁款"></el-option>
            <el-option label="莲花结流苏" value="莲花结流苏"></el-option>
            <el-option label="吉祥结流苏" value="吉祥结流苏"></el-option>
            <el-option label="不配流苏" value="不配流苏"></el-option>
          </el-select>
        </el-form-item>
        
        <el-divider content-position="left">备注信息</el-divider>
        
        <el-form-item label="特殊要求" prop="remark">
          <el-input type="textarea" v-model="orderForm.remark" :rows="4" placeholder="请输入其他特殊要求" style="width: 500px;"></el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" size="large" @click="submitOrder" :loading="submitting">提交订单</el-button>
          <el-button size="large" @click="resetForm">重置</el-button>
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
        woodType: '',
        beadDiameter: 15,
        beadCount: '18',
        lacquerTechnique: '',
        tasselStyle: '',
        remark: ''
      },
      diameterMin: 10,
      diameterMax: 20,
      rules: {
        customerName: [
          { required: true, message: '请输入客户姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ],
        woodType: [
          { required: true, message: '请选择木料材质', trigger: 'blur' }
        ],
        beadDiameter: [
          { required: true, message: '请输入珠子直径', trigger: 'blur' },
          { type: 'number', min: 6, max: 30, message: '直径范围应在 6-30mm 之间', trigger: 'blur' }
        ],
        beadCount: [
          { required: true, message: '请选择珠子颗数', trigger: 'change' }
        ],
        lacquerTechnique: [
          { required: true, message: '请选择漆艺工艺', trigger: 'blur' }
        ],
        tasselStyle: [
          { required: true, message: '请选择流苏款式', trigger: 'change' }
        ]
      }
    }
  },
  computed: {
    diameterHintClass() {
      if (this.orderForm.beadDiameter < this.diameterMin || this.orderForm.beadDiameter > this.diameterMax) {
        return 'warning'
      }
      return 'normal'
    },
    diameterIcon() {
      if (this.orderForm.beadDiameter < this.diameterMin || this.orderForm.beadDiameter > this.diameterMax) {
        return 'el-icon-warning'
      }
      return 'el-icon-success'
    },
    diameterHintText() {
      if (this.orderForm.beadDiameter < this.diameterMin) {
        return `直径偏小，生产难度较高`
      } else if (this.orderForm.beadDiameter > this.diameterMax) {
        return `直径偏大，材料成本较高`
      }
      return `直径在推荐生产范围内`
    }
  },
  methods: {
    onDiameterChange() {
    },
    validateField(field) {
      this.$refs.orderForm.validateField(field)
    },
    submitOrder() {
      this.$refs.orderForm.validate((valid) => {
        if (valid) {
          this.submitting = true
          setTimeout(() => {
            const orders = JSON.parse(localStorage.getItem('beadsOrders') || '[]')
            const newOrder = {
              id: Date.now(),
              ...this.orderForm,
              status: 0,
              createTime: new Date().toLocaleString(),
              processTimes: []
            }
            orders.unshift(newOrder)
            localStorage.setItem('beadsOrders', JSON.stringify(orders))
            
            window.dispatchEvent(new CustomEvent('orderUpdated'))
            
            this.$message({
              type: 'success',
              message: '订单提交成功！'
            })
            this.resetForm()
            this.submitting = false
          }, 1000)
        } else {
          this.$message.error('请完善表单信息')
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
.order-form {
  max-width: 800px;
  margin: 0 auto;
}

.form-card {
  border-radius: 8px;
}

.card-header {
  font-size: 20px;
  font-weight: 600;
  color: #8B4513;
}

.el-divider__text {
  background-color: #f5f7fa;
  color: #8B4513;
  font-weight: 600;
  padding: 0 15px;
}

.diameter-hint {
  display: flex;
  align-items: center;
  margin-top: 8px;
  font-size: 13px;
}

.diameter-hint i {
  margin-right: 5px;
}

.diameter-hint.normal {
  color: #67C23A;
}

.diameter-hint.warning {
  color: #E6A23C;
}

.range-tip {
  color: #909399;
  margin-left: 10px;
  font-size: 12px;
}
</style>
