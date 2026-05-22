<template>
  <div class="order-form-container">
    <div class="page-header">
      <h1>传统景泰蓝手镯定制</h1>
      <p class="subtitle">匠心独运，传世精品</p>
    </div>

    <el-card class="form-card">
      <el-form :model="orderForm" :rules="rules" ref="orderForm" label-width="120px">
        <el-divider content-position="left">
          <span class="divider-title">基本信息</span>
        </el-divider>

        <el-form-item label="客户姓名" prop="customerName">
          <el-input v-model="orderForm.customerName" placeholder="请输入您的姓名" clearable></el-input>
        </el-form-item>

        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="orderForm.phone" placeholder="请输入联系电话" clearable></el-input>
        </el-form-item>

        <el-divider content-position="left">
          <span class="divider-title">胎体规格</span>
        </el-divider>

        <el-form-item label="胎体材质" prop="material">
          <el-select v-model="orderForm.material" placeholder="请选择胎体材质" style="width: 100%">
            <el-option label="紫铜" value="紫铜"></el-option>
            <el-option label="黄铜" value="黄铜"></el-option>
            <el-option label="纯银" value="纯银"></el-option>
            <el-option label="金胎" value="金胎"></el-option>
          </el-select>
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="手镯内径(mm)" prop="innerDiameter">
              <el-input-number v-model="orderForm.innerDiameter" :min="50" :max="70" :step="0.5" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="圈口粗细(mm)" prop="thickness">
              <el-input-number v-model="orderForm.thickness" :min="4" :max="15" :step="0.5" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">
          <span class="divider-title">珐琅工艺</span>
        </el-divider>

        <el-form-item label="珐琅釉色" prop="enamelColor">
          <el-checkbox-group v-model="orderForm.enamelColors">
            <el-checkbox label="宝石蓝">宝石蓝</el-checkbox>
            <el-checkbox label="翡翠绿">翡翠绿</el-checkbox>
            <el-checkbox label="珊瑚红">珊瑚红</el-checkbox>
            <el-checkbox label="明黄">明黄</el-checkbox>
            <el-checkbox label="紫罗兰">紫罗兰</el-checkbox>
            <el-checkbox label="胭脂粉">胭脂粉</el-checkbox>
            <el-checkbox label="月白">月白</el-checkbox>
            <el-checkbox label="墨黑">墨黑</el-checkbox>
          </el-checkbox-group>
        </el-form-item>

        <el-form-item label="掐丝纹样" prop="pattern">
          <el-radio-group v-model="orderForm.pattern">
            <el-radio label="祥云纹">祥云纹</el-radio>
            <el-radio label="缠枝莲">缠枝莲</el-radio>
            <el-radio label="龙凤纹">龙凤纹</el-radio>
            <el-radio label="牡丹纹">牡丹纹</el-radio>
            <el-radio label="山水纹">山水纹</el-radio>
            <el-radio label="百鸟朝凤">百鸟朝凤</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="备注说明">
          <el-input type="textarea" v-model="orderForm.remark" :rows="4" placeholder="请输入其他特殊要求..."></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" size="large" @click="submitOrder" :loading="submitting" class="submit-btn">
            提交定制订单
          </el-button>
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
        material: '',
        innerDiameter: 58,
        thickness: 8,
        enamelColors: [],
        pattern: '',
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
        material: [
          { required: true, message: '请选择胎体材质', trigger: 'change' }
        ],
        innerDiameter: [
          { required: true, message: '请输入手镯内径', trigger: 'blur' }
        ],
        thickness: [
          { required: true, message: '请输入圈口粗细', trigger: 'blur' }
        ],
        pattern: [
          { required: true, message: '请选择掐丝纹样', trigger: 'change' }
        ]
      }
    }
  },
  methods: {
    submitOrder() {
      this.$refs.orderForm.validate((valid) => {
        if (valid) {
          if (this.orderForm.enamelColors.length === 0) {
            this.$message.warning('请至少选择一种珐琅釉色');
            return;
          }
          this.submitting = true;
          setTimeout(() => {
            const order = {
              id: 'ORD' + Date.now(),
              ...this.orderForm,
              status: 0,
              statusText: '制胎',
              createTime: new Date().toLocaleString()
            };
            const orders = JSON.parse(localStorage.getItem('cloisonneOrders') || '[]');
            orders.unshift(order);
            localStorage.setItem('cloisonneOrders', JSON.stringify(orders));
            this.$message.success('订单提交成功！');
            this.submitting = false;
            this.resetForm();
          }, 1000);
        }
      });
    },
    resetForm() {
      this.$refs.orderForm.resetFields();
      this.orderForm.enamelColors = [];
    }
  }
}
</script>

<style scoped>
.order-form-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;
}

.page-header h1 {
  color: #8B4513;
  font-size: 32px;
  margin-bottom: 10px;
  font-weight: 600;
}

.subtitle {
  color: #666;
  font-size: 16px;
}

.form-card {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.divider-title {
  color: #8B4513;
  font-weight: 600;
  font-size: 16px;
}

.submit-btn {
  background: linear-gradient(135deg, #8B4513, #D2691E);
  border: none;
}
</style>
