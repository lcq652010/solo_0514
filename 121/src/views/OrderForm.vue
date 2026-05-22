<template>
  <div class="page-card">
    <div class="page-title">包裹下单</div>
    <el-form :model="orderForm" :rules="rules" ref="orderForm" label-width="100px">
      <el-divider content-position="left">寄件人信息</el-divider>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="寄件人姓名" prop="senderName">
            <el-input v-model="orderForm.senderName" placeholder="请输入寄件人姓名"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="联系电话" prop="senderPhone">
            <el-input v-model="orderForm.senderPhone" placeholder="请输入联系电话"></el-input>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="16">
          <el-form-item label="寄件地址" prop="senderAddress">
            <el-input type="textarea" v-model="orderForm.senderAddress" :rows="2" placeholder="请输入详细地址"></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-divider content-position="left">收件人信息</el-divider>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="收件人姓名" prop="receiverName">
            <el-input v-model="orderForm.receiverName" placeholder="请输入收件人姓名"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="联系电话" prop="receiverPhone">
            <el-input v-model="orderForm.receiverPhone" placeholder="请输入联系电话"></el-input>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="16">
          <el-form-item label="收件地址" prop="receiverAddress">
            <el-input type="textarea" v-model="orderForm.receiverAddress" :rows="2" placeholder="请输入详细地址" @blur="checkDeliveryArea"></el-input>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20" v-if="deliveryWarning.show">
        <el-col :span="16">
          <el-alert
            :title="deliveryWarning.message"
            :type="deliveryWarning.type"
            show-icon
            :closable="false">
          </el-alert>
        </el-col>
      </el-row>

      <el-divider content-position="left">包裹信息</el-divider>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="包裹名称" prop="packageName">
            <el-input v-model="orderForm.packageName" placeholder="请输入包裹名称"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="包裹重量(kg)" prop="weight">
            <el-input-number v-model="orderForm.weight" :min="0.1" :step="0.1" :precision="1"></el-input-number>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="16">
          <el-form-item label="备注">
            <el-input type="textarea" v-model="orderForm.remark" :rows="3" placeholder="选填，请输入备注信息"></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item>
        <el-button type="primary" @click="submitForm">提交订单</el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'OrderForm',
  data() {
    const validatePhone = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入联系电话'));
      } else if (!/^1[3-9]\d{9}$/.test(value)) {
        callback(new Error('请输入正确的手机号格式'));
      } else {
        callback();
      }
    };

    return {
      deliveryWarning: {
        show: false,
        message: '',
        type: 'warning'
      },
      deliveryCities: ['北京', '上海', '广州', '深圳', '杭州', '南京', '成都', '武汉', '西安', '重庆', '苏州', '天津', '长沙', '郑州', '青岛', '大连', '厦门', '宁波', '无锡', '济南'],
      isOutOfRange: false,
      orderForm: {
        senderName: '',
        senderPhone: '',
        senderAddress: '',
        receiverName: '',
        receiverPhone: '',
        receiverAddress: '',
        packageName: '',
        weight: 1.0,
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
          { required: true, message: '请输入寄件地址', trigger: 'blur' },
          { min: 5, message: '地址长度不能少于5个字符', trigger: 'blur' }
        ],
        receiverName: [
          { required: true, message: '请输入收件人姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        receiverPhone: [
          { required: true, validator: validatePhone, trigger: 'blur' }
        ],
        receiverAddress: [
          { required: true, message: '请输入收件地址', trigger: 'blur' },
          { min: 5, message: '地址长度不能少于5个字符', trigger: 'blur' }
        ],
        packageName: [
          { required: true, message: '请输入包裹名称', trigger: 'blur' }
        ],
        weight: [
          { required: true, message: '请输入包裹重量', trigger: 'blur' }
        ]
      }
    };
  },
  methods: {
    checkDeliveryArea() {
      if (!this.orderForm.receiverAddress || this.orderForm.receiverAddress.length < 5) {
        this.deliveryWarning.show = false;
        this.isOutOfRange = false;
        return;
      }

      const address = this.orderForm.receiverAddress;
      let inRange = false;
      let matchedCity = '';

      for (const city of this.deliveryCities) {
        if (address.includes(city)) {
          inRange = true;
          matchedCity = city;
          break;
        }
      }

      if (inRange) {
        this.deliveryWarning = {
          show: true,
          message: '收件地址在【' + matchedCity + '】配送范围内，可正常下单',
          type: 'success'
        };
        this.isOutOfRange = false;
      } else {
        this.deliveryWarning = {
          show: true,
          message: '温馨提示：收件地址暂不在配送范围内，暂时无法下单配送。目前支持配送城市：' + this.deliveryCities.join('、'),
          type: 'error'
        };
        this.isOutOfRange = true;
      }
    },
    submitForm() {
      this.checkDeliveryArea();
      
      this.$refs.orderForm.validate(valid => {
        if (valid) {
          if (this.isOutOfRange) {
            this.$message.error('收件地址超出配送范围，无法下单！');
            return false;
          }
          this.$message.success('订单提交成功！订单号：WL' + Date.now());
          this.resetForm();
        } else {
          this.$message.error('请检查表单填写是否正确');
          return false;
        }
      });
    },
    resetForm() {
      this.$refs.orderForm.resetFields();
      this.deliveryWarning.show = false;
      this.isOutOfRange = false;
    }
  }
};
</script>

<style scoped>
.el-divider {
  margin: 20px 0;
}
</style>
