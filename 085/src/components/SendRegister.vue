<template>
  <div class="page-card">
    <h2 class="page-title">
      <i class="el-icon-s-promotion"></i>
      寄件登记
    </h2>

    <el-form
      ref="sendForm"
      :model="formData"
      :rules="rules"
      label-width="120px"
      class="send-form"
    >
      <el-divider content-position="left">寄件人信息</el-divider>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="寄件人姓名" prop="senderName">
            <el-input
              v-model="formData.senderName"
              placeholder="请输入寄件人姓名"
              clearable
            ></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="寄件人电话" prop="senderPhone">
            <el-input
              v-model="formData.senderPhone"
              placeholder="请输入寄件人手机号"
              clearable
            ></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item label="寄件人地址" prop="senderAddress">
        <el-input
          v-model="formData.senderAddress"
          type="textarea"
          :rows="2"
          placeholder="请输入寄件人详细地址"
        ></el-input>
      </el-form-item>

      <el-divider content-position="left">收件人信息</el-divider>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="收件人姓名" prop="receiverName">
            <el-input
              v-model="formData.receiverName"
              placeholder="请输入收件人姓名"
              clearable
            ></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="收件人电话" prop="receiverPhone">
            <el-input
              v-model="formData.receiverPhone"
              placeholder="请输入收件人手机号"
              clearable
            ></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item label="收件人地址" prop="receiverAddress">
        <el-input
          v-model="formData.receiverAddress"
          type="textarea"
          :rows="2"
          placeholder="请输入收件人详细地址"
        ></el-input>
      </el-form-item>

      <el-divider content-position="left">包裹信息</el-divider>

      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="物品类型" prop="goodsType">
            <el-select
              v-model="formData.goodsType"
              placeholder="请选择物品类型"
              style="width: 100%"
              clearable
            >
              <el-option label="文件资料" value="文件资料"></el-option>
              <el-option label="数码产品" value="数码产品"></el-option>
              <el-option label="服装鞋帽" value="服装鞋帽"></el-option>
              <el-option label="食品生鲜" value="食品生鲜"></el-option>
              <el-option label="家居用品" value="家居用品"></el-option>
              <el-option label="其他" value="其他"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="物品重量(kg)" prop="weight">
            <el-input-number
              v-model="formData.weight"
              :min="0"
              :step="0.1"
              :precision="1"
              style="width: 100%"
            ></el-input-number>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="是否保价" prop="isInsured">
            <el-switch
              v-model="formData.isInsured"
              active-text="是"
              inactive-text="否"
            ></el-switch>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20" v-if="formData.isInsured">
        <el-col :span="12">
          <el-form-item label="保价金额(元)" prop="insuredAmount">
            <el-input-number
              v-model="formData.insuredAmount"
              :min="0"
              :step="100"
              style="width: 100%"
            ></el-input-number>
          </el-form-item>
        </el-col>
      </el-row>

      <el-divider content-position="left">服务选择</el-divider>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="快递公司" prop="company">
            <el-select
              v-model="formData.company"
              placeholder="请选择快递公司"
              style="width: 100%"
              clearable
            >
              <el-option label="顺丰速运" value="顺丰速运"></el-option>
              <el-option label="圆通速递" value="圆通速递"></el-option>
              <el-option label="中通快递" value="中通快递"></el-option>
              <el-option label="韵达快递" value="韵达快递"></el-option>
              <el-option label="极兔速递" value="极兔速递"></el-option>
              <el-option label="京东物流" value="京东物流"></el-option>
              <el-option label="邮政EMS" value="邮政EMS"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="服务类型" prop="serviceType">
            <el-select
              v-model="formData.serviceType"
              placeholder="请选择服务类型"
              style="width: 100%"
              clearable
            >
              <el-option label="标准快递" value="标准快递"></el-option>
              <el-option label="加急快递" value="加急快递"></el-option>
              <el-option label="次日达" value="次日达"></el-option>
              <el-option label="同城配送" value="同城配送"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="预计运费(元)">
            <el-input
              v-model="estimatedFee"
              disabled
              style="width: 100%"
            ></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="取件方式" prop="pickupMethod">
            <el-radio-group v-model="formData.pickupMethod">
              <el-radio label="上门取件"></el-radio>
              <el-radio label="自行送件"></el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item label="取件时间" prop="pickupTime">
        <el-date-picker
          v-model="formData.pickupTime"
          type="datetime"
          placeholder="选择取件时间"
          style="width: 300px"
          format="yyyy-MM-dd HH:mm:ss"
          value-format="yyyy-MM-dd HH:mm:ss"
        ></el-date-picker>
      </el-form-item>

      <el-form-item label="备注信息">
        <el-input
          v-model="formData.remark"
          type="textarea"
          :rows="2"
          placeholder="请输入备注信息（选填）"
        ></el-input>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="submitForm" :loading="loading" size="large">
          <i class="el-icon-check"></i>
          提交寄件申请
        </el-button>
        <el-button @click="resetForm" size="large">
          <i class="el-icon-refresh"></i>
          重置表单
        </el-button>
      </el-form-item>
    </el-form>

    <div v-if="recentList.length > 0" class="recent-section">
      <el-divider content-position="left">最近寄件记录</el-divider>
      <el-table :data="recentList" border stripe style="width: 100%">
        <el-table-column prop="sendNo" label="寄件单号" width="180"></el-table-column>
        <el-table-column prop="receiverName" label="收件人" width="100"></el-table-column>
        <el-table-column prop="company" label="快递公司" width="120"></el-table-column>
        <el-table-column prop="goodsType" label="物品类型" width="100"></el-table-column>
        <el-table-column prop="fee" label="运费(元)" width="100" align="center"></el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="small">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="登记时间" width="180"></el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import moment from 'moment';

export default {
  name: 'SendRegister',
  data() {
    return {
      loading: false,
      formData: {
        senderName: '',
        senderPhone: '',
        senderAddress: '',
        receiverName: '',
        receiverPhone: '',
        receiverAddress: '',
        goodsType: '',
        weight: 0,
        isInsured: false,
        insuredAmount: 0,
        company: '',
        serviceType: '',
        pickupMethod: '上门取件',
        pickupTime: '',
        remark: ''
      },
      rules: {
        senderName: [
          { required: true, message: '请输入寄件人姓名', trigger: 'blur' }
        ],
        senderPhone: [
          { required: true, message: '请输入寄件人手机号', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
        ],
        senderAddress: [
          { required: true, message: '请输入寄件人地址', trigger: 'blur' }
        ],
        receiverName: [
          { required: true, message: '请输入收件人姓名', trigger: 'blur' }
        ],
        receiverPhone: [
          { required: true, message: '请输入收件人手机号', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
        ],
        receiverAddress: [
          { required: true, message: '请输入收件人地址', trigger: 'blur' }
        ],
        goodsType: [
          { required: true, message: '请选择物品类型', trigger: 'change' }
        ],
        weight: [
          { required: true, message: '请输入物品重量', trigger: 'change' },
          { type: 'number', min: 0.1, message: '重量必须大于0', trigger: 'change' }
        ],
        company: [
          { required: true, message: '请选择快递公司', trigger: 'change' }
        ],
        serviceType: [
          { required: true, message: '请选择服务类型', trigger: 'change' }
        ],
        pickupTime: [
          { required: true, message: '请选择取件时间', trigger: 'change' }
        ]
      },
      recentList: []
    };
  },
  computed: {
    estimatedFee() {
      let fee = 12;
      if (this.formData.weight > 1) {
        fee += (this.formData.weight - 1) * 5;
      }
      if (this.formData.serviceType === '加急快递') {
        fee *= 1.5;
      } else if (this.formData.serviceType === '次日达') {
        fee *= 2;
      }
      if (this.formData.isInsured && this.formData.insuredAmount > 0) {
        fee += this.formData.insuredAmount * 0.01;
      }
      return fee.toFixed(2);
    }
  },
  methods: {
    submitForm() {
      this.$refs.sendForm.validate((valid) => {
        if (valid) {
          this.loading = true;
          setTimeout(() => {
            const sendNo = this.generateSendNo();
            const newRecord = {
              ...this.formData,
              sendNo: sendNo,
              fee: this.estimatedFee,
              status: '待取件',
              createTime: moment().format('YYYY-MM-DD HH:mm:ss')
            };

            this.recentList.unshift(newRecord);
            if (this.recentList.length > 5) {
              this.recentList.pop();
            }

            this.saveToStorage(newRecord);
            this.loading = false;

            this.$message({
              type: 'success',
              message: `寄件登记成功！寄件单号：${sendNo}`
            });

            this.resetForm();
          }, 1000);
        } else {
          this.$message.error('请检查表单填写是否正确');
          return false;
        }
      });
    },
    resetForm() {
      this.$refs.sendForm.resetFields();
      this.formData.isInsured = false;
      this.formData.pickupMethod = '上门取件';
    },
    generateSendNo() {
      return 'SD' + moment().format('YYYYMMDDHHmmss') + Math.floor(Math.random() * 1000);
    },
    saveToStorage(record) {
      let list = JSON.parse(localStorage.getItem('sendList') || '[]');
      list.unshift({
        ...record,
        id: Date.now()
      });
      localStorage.setItem('sendList', JSON.stringify(list));
    },
    getStatusType(status) {
      const typeMap = {
        '待取件': 'warning',
        '已取件': 'primary',
        '运输中': 'info',
        '已签收': 'success',
        '已取消': 'danger'
      };
      return typeMap[status] || 'info';
    },
    loadRecentList() {
      const list = JSON.parse(localStorage.getItem('sendList') || '[]');
      this.recentList = list.slice(0, 5);
    }
  },
  mounted() {
    this.loadRecentList();
  }
};
</script>

<style scoped>
.send-form {
  max-width: 1000px;
}

.recent-section {
  margin-top: 30px;
}
</style>
