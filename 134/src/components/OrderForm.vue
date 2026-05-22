<template>
  <div class="order-form-container">
    <el-card class="form-card">
      <div slot="header" class="card-header">
        <h2>传统砚台定制</h2>
        <p>匠心工艺，专属定制</p>
      </div>

      <el-form :model="orderForm" :rules="rules" ref="orderForm" label-width="120px">
        <el-divider content-position="left">砚石材质</el-divider>
        <el-form-item label="砚石材质" prop="material">
          <el-select v-model="orderForm.material" placeholder="请选择砚石材质" style="width: 100%">
            <el-option
              v-for="item in materials"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>

        <el-divider content-position="left">砚台样式</el-divider>
        <el-form-item label="砚台样式" prop="style">
          <el-radio-group v-model="orderForm.style">
            <el-radio-button
              v-for="item in styles"
              :key="item.value"
              :label="item.value">
              {{ item.label }}
            </el-radio-button>
          </el-radio-group>
        </el-form-item>

        <el-divider content-position="left">尺寸规格</el-divider>
        <el-form-item label="长度 (cm)" prop="length">
          <el-input-number v-model="orderForm.length" :min="5" :max="50" :step="0.5" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="宽度 (cm)" prop="width">
          <el-input-number v-model="orderForm.width" :min="5" :max="40" :step="0.5" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="厚度 (cm)" prop="thickness">
          <el-input-number v-model="orderForm.thickness" :min="1" :max="10" :step="0.5" style="width: 100%"></el-input-number>
        </el-form-item>

        <el-divider content-position="left">雕刻题材</el-divider>
        <el-form-item label="雕刻题材" prop="carving">
          <el-select v-model="orderForm.carving" placeholder="请选择雕刻题材" style="width: 100%">
            <el-option
              v-for="item in carvings"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>

        <el-divider content-position="left">刻字服务</el-divider>
        <el-form-item label="是否刻字">
          <el-switch v-model="orderForm.needEngraving"></el-switch>
        </el-form-item>
        <el-form-item v-if="orderForm.needEngraving" label="刻字内容" prop="engravingText">
          <el-input
            v-model="orderForm.engravingText"
            type="textarea"
            :rows="3"
            placeholder="请输入刻字内容"
            maxlength="50"
            show-word-limit>
          </el-input>
        </el-form-item>

        <el-divider content-position="left">订单留言</el-divider>
        <el-form-item label="订单留言" prop="message">
          <el-input
            v-model="orderForm.message"
            type="textarea"
            :rows="4"
            placeholder="请输入其他定制要求或留言"
            maxlength="200"
            show-word-limit>
          </el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" size="large" @click="submitOrder" style="width: 100%">提交订单</el-button>
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
      orderForm: {
        material: '',
        style: '',
        length: 20,
        width: 15,
        thickness: 3,
        carving: '',
        needEngraving: false,
        engravingText: '',
        message: ''
      },
      materials: [
        { label: '端石 (广东肇庆)', value: 'duanshi' },
        { label: '歙石 (安徽歙县)', value: 'sheshi' },
        { label: '洮河石 (甘肃)', value: 'taohe' },
        { label: '澄泥 (山西绛州)', value: 'chengni' },
        { label: '红丝石 (山东)', value: 'hongsi' },
        { label: '松花石 (吉林)', value: 'songhua' }
      ],
      styles: [
        { label: '圆形', value: 'circle' },
        { label: '方形', value: 'square' },
        { label: '长方形', value: 'rectangle' },
        { label: '随形', value: 'freeform' },
        { label: '古琴式', value: 'guqin' },
        { label: '箕形', value: 'ji' }
      ],
      carvings: [
        { label: '山水风景', value: 'landscape' },
        { label: '花鸟虫鱼', value: 'flower' },
        { label: '龙凤呈祥', value: 'dragon' },
        { label: '松竹梅兰', value: 'bamboo' },
        { label: '人物典故', value: 'figure' },
        { label: '素面无雕', value: 'plain' }
      ],
      rules: {
        material: [
          { required: true, message: '请选择砚石材质', trigger: 'change' }
        ],
        style: [
          { required: true, message: '请选择砚台样式', trigger: 'change' }
        ],
        length: [
          { required: true, message: '请输入长度', trigger: 'blur' }
        ],
        width: [
          { required: true, message: '请输入宽度', trigger: 'blur' }
        ],
        thickness: [
          { required: true, message: '请输入厚度', trigger: 'blur' }
        ],
        carving: [
          { required: true, message: '请选择雕刻题材', trigger: 'change' }
        ],
        engravingText: [
          { required: true, message: '请输入刻字内容', trigger: 'blur' }
        ]
      }
    };
  },
  methods: {
    submitOrder() {
      this.$refs.orderForm.validate((valid) => {
        if (valid) {
          const order = {
            id: 'ORD' + Date.now(),
            ...this.orderForm,
            status: 0,
            createTime: new Date().toLocaleString()
          };
          
          const orders = JSON.parse(localStorage.getItem('inkstoneOrders') || '[]');
          orders.unshift(order);
          localStorage.setItem('inkstoneOrders', JSON.stringify(orders));
          
          this.$message.success('订单提交成功！');
          this.$refs.orderForm.resetFields();
          this.orderForm.needEngraving = false;
        } else {
          this.$message.error('请完善订单信息');
          return false;
        }
      });
    }
  }
};
</script>

<style scoped>
.order-form-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 0 20px;
}

.form-card {
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  text-align: center;
}

.card-header h2 {
  margin: 0 0 8px 0;
  color: #60463b;
}

.card-header p {
  margin: 0;
  color: #909399;
  font-size: 14px;
}
</style>
