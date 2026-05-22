<template>
  <div class="page-card">
    <h2 class="page-title">
      <i class="el-icon-download"></i>
      快递入库登记
    </h2>
    
    <el-form
      ref="inboundForm"
      :model="formData"
      :rules="rules"
      label-width="120px"
      class="inbound-form"
    >
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="快递单号" prop="expressNo">
            <el-input
              v-model="formData.expressNo"
              placeholder="请输入快递单号"
              clearable
            ></el-input>
          </el-form-item>
        </el-col>
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
              <el-option label="其他" value="其他"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

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

      <el-form-item label="收件地址" prop="receiverAddress">
        <el-input
          v-model="formData.receiverAddress"
          type="textarea"
          :rows="2"
          placeholder="请输入收件地址"
        ></el-input>
      </el-form-item>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="快递重量(kg)" prop="weight">
            <el-input-number
              v-model="formData.weight"
              :min="0"
              :step="0.1"
              :precision="1"
              style="width: 100%"
              placeholder="请输入重量"
            ></el-input-number>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="快递类型" prop="type">
            <el-select
              v-model="formData.type"
              placeholder="请选择快递类型"
              style="width: 100%"
              clearable
            >
              <el-option label="普通快递" value="普通快递"></el-option>
              <el-option label="生鲜冷链" value="生鲜冷链"></el-option>
              <el-option label="贵重物品" value="贵重物品"></el-option>
              <el-option label="大件物品" value="大件物品"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item label="备注信息">
        <el-input
          v-model="formData.remark"
          type="textarea"
          :rows="2"
          placeholder="请输入备注信息（选填）"
        ></el-input>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="submitForm" :loading="loading">
          <i class="el-icon-check"></i>
          确认入库
        </el-button>
        <el-button @click="resetForm">
          <i class="el-icon-refresh"></i>
          重置表单
        </el-button>
      </el-form-item>
    </el-form>

    <div v-if="recentList.length > 0" class="recent-section">
      <h3 class="section-title">最近入库记录</h3>
      <el-table :data="recentList" border stripe style="width: 100%">
        <el-table-column prop="expressNo" label="快递单号" width="180"></el-table-column>
        <el-table-column prop="company" label="快递公司" width="120"></el-table-column>
        <el-table-column prop="receiverName" label="收件人" width="100"></el-table-column>
        <el-table-column prop="pickupCode" label="取件码" width="100" align="center">
          <template slot-scope="scope">
            <el-tag type="success" size="medium">{{ scope.row.pickupCode }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="inboundTime" label="入库时间" width="180"></el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === '待取件' ? 'warning' : 'success'" size="small">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'InboundForm',
  data() {
    return {
      loading: false,
      formData: {
        expressNo: '',
        company: '',
        receiverName: '',
        receiverPhone: '',
        receiverAddress: '',
        weight: 0,
        type: '',
        remark: ''
      },
      rules: {
        expressNo: [
          { required: true, message: '请输入快递单号', trigger: 'blur' },
          { min: 5, max: 30, message: '长度在 5 到 30 个字符', trigger: 'blur' }
        ],
        company: [
          { required: true, message: '请选择快递公司', trigger: 'change' }
        ],
        receiverName: [
          { required: true, message: '请输入收件人姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        receiverPhone: [
          { required: true, message: '请输入收件人手机号', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
        ],
        receiverAddress: [
          { required: true, message: '请输入收件地址', trigger: 'blur' }
        ],
        weight: [
          { required: true, message: '请输入快递重量', trigger: 'change' },
          { type: 'number', min: 0.1, message: '重量必须大于0', trigger: 'change' }
        ],
        type: [
          { required: true, message: '请选择快递类型', trigger: 'change' }
        ]
      },
      recentList: []
    };
  },
  methods: {
    submitForm() {
      this.$refs.inboundForm.validate((valid) => {
        if (valid) {
          this.loading = true;
          setTimeout(() => {
            const pickupCode = this.generatePickupCode();
            const newRecord = {
              ...this.formData,
              pickupCode: pickupCode,
              inboundTime: this.$moment().format('YYYY-MM-DD HH:mm:ss'),
              status: '待取件'
            };
            
            this.recentList.unshift(newRecord);
            if (this.recentList.length > 5) {
              this.recentList.pop();
            }
            
            this.saveToStorage(newRecord);
            this.loading = false;
            
            this.$message({
              type: 'success',
              message: `入库成功！取件码：${pickupCode}`
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
      this.$refs.inboundForm.resetFields();
    },
    generatePickupCode() {
      const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
      const list = JSON.parse(localStorage.getItem('expressList') || '[]');
      const existingCodes = new Set(list.map(item => item.pickupCode));
      let maxAttempts = 100;
      
      while (maxAttempts > 0) {
        let code = '';
        for (let i = 0; i < 6; i++) {
          code += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        if (!existingCodes.has(code)) {
          return code;
        }
        maxAttempts--;
      }
      
      const timestamp = Date.now().toString(36).toUpperCase();
      return timestamp.slice(-6);
    },
    saveToStorage(record) {
      let list = JSON.parse(localStorage.getItem('expressList') || '[]');
      list.unshift({
        ...record,
        id: Date.now(),
        createTime: new Date().toISOString()
      });
      localStorage.setItem('expressList', JSON.stringify(list));
    }
  },
  created() {
    this.$moment = require('moment');
  }
};
</script>

<style scoped>
.inbound-form {
  max-width: 900px;
}

.recent-section {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #e4e7ed;
}

.section-title {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 16px;
}
</style>
