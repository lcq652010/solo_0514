<template>
  <div class="student-reg">
    <div class="page-title">学员报名</div>
    <div class="card-wrapper">
      <el-form
        ref="studentForm"
        :model="studentForm"
        :rules="rules"
        label-width="100px"
        label-position="right"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="studentForm.name" placeholder="请输入姓名"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-radio-group v-model="studentForm.gender">
                <el-radio label="男">男</el-radio>
                <el-radio label="女">女</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="身份证号" prop="idCard">
              <el-input 
                v-model="studentForm.idCard" 
                placeholder="请输入身份证号" 
                maxlength="18"
                @input="validateIdCardRealTime"
                clearable
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="手机号码" prop="phone">
              <el-input v-model="studentForm.phone" placeholder="请输入手机号码" maxlength="11"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="出生日期" prop="birthday">
              <el-date-picker
                v-model="studentForm.birthday"
                type="date"
                placeholder="选择出生日期"
                style="width: 100%"
              ></el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="报名班型" prop="classType">
              <el-select v-model="studentForm.classType" placeholder="请选择班型" style="width: 100%">
                <el-option label="C1 普通班" value="C1 普通班"></el-option>
                <el-option label="C1 VIP班" value="C1 VIP班"></el-option>
                <el-option label="C2 自动档班" value="C2 自动档班"></el-option>
                <el-option label="C2 VIP班" value="C2 VIP班"></el-option>
                <el-option label="快速取证班" value="快速取证班"></el-option>
                <el-option label="学生特惠班" value="学生特惠班"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="联系地址" prop="address">
              <el-input v-model="studentForm.address" placeholder="请输入联系地址"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="紧急联系人" prop="emergencyContact">
              <el-input v-model="studentForm.emergencyContact" placeholder="请输入紧急联系人"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="紧急联系电话" prop="emergencyPhone">
              <el-input v-model="studentForm.emergencyPhone" placeholder="请输入紧急联系电话" maxlength="11"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="文化程度" prop="education">
              <el-select v-model="studentForm.education" placeholder="请选择文化程度" style="width: 100%">
                <el-option label="初中及以下" value="初中及以下"></el-option>
                <el-option label="高中/中专" value="高中/中专"></el-option>
                <el-option label="大专" value="大专"></el-option>
                <el-option label="本科" value="本科"></el-option>
                <el-option label="硕士及以上" value="硕士及以上"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="备注" prop="remark">
          <el-input
            type="textarea"
            :rows="4"
            v-model="studentForm.remark"
            placeholder="请输入备注信息（选填）"
          ></el-input>
        </el-form-item>

        <el-form-item>
          <el-checkbox v-model="studentForm.agreement">
            我已阅读并同意《学员培训协议》
          </el-checkbox>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm">提交报名</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StudentReg',
  data() {
    const validatePhone = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入手机号码'));
      } else if (!/^1[3-9]\d{9}$/.test(value)) {
        callback(new Error('请输入正确的手机号码'));
      } else {
        callback();
      }
    };

    const validateIdCard = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入身份证号'));
        return;
      }
      const idCard = value.toUpperCase();
      if (!/^\d{17}[\dX]$/.test(idCard)) {
        callback(new Error('身份证号格式错误，应为18位数字或最后一位为X'));
        return;
      }
      const weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2];
      const checkCodes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2'];
      let sum = 0;
      for (let i = 0; i < 17; i++) {
        sum += parseInt(idCard[i]) * weights[i];
      }
      const checkCode = checkCodes[sum % 11];
      if (idCard[17] !== checkCode) {
        callback(new Error('身份证号校验位错误，请检查输入'));
        return;
      }
      callback();
    };

    const validateAgreement = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请阅读并同意学员培训协议'));
      } else {
        callback();
      }
    };

    return {
      studentForm: {
        name: '',
        gender: '',
        idCard: '',
        phone: '',
        birthday: '',
        classType: '',
        address: '',
        emergencyContact: '',
        emergencyPhone: '',
        education: '',
        remark: '',
        agreement: false
      },
      rules: {
        name: [
          { required: true, message: '请输入姓名', trigger: 'blur' },
          { min: 2, max: 10, message: '长度在 2 到 10 个字符', trigger: 'blur' }
        ],
        gender: [
          { required: true, message: '请选择性别', trigger: 'change' }
        ],
        idCard: [
          { validator: validateIdCard, trigger: 'change' }
        ],
        phone: [
          { validator: validatePhone, trigger: 'blur' }
        ],
        birthday: [
          { required: true, message: '请选择出生日期', trigger: 'change' }
        ],
        classType: [
          { required: true, message: '请选择报名班型', trigger: 'change' }
        ],
        address: [
          { required: true, message: '请输入联系地址', trigger: 'blur' }
        ],
        emergencyContact: [
          { required: true, message: '请输入紧急联系人', trigger: 'blur' }
        ],
        emergencyPhone: [
          { validator: validatePhone, trigger: 'blur' }
        ],
        education: [
          { required: true, message: '请选择文化程度', trigger: 'change' }
        ],
        agreement: [
          { validator: validateAgreement, trigger: 'change' }
        ]
      }
    };
  },
  mounted() {
    if (this.$route.query.className) {
      this.studentForm.classType = this.$route.query.className;
    }
  },
  methods: {
    validateIdCardRealTime() {
      if (this.studentForm.idCard && this.studentForm.idCard.length > 0) {
        this.$refs.studentForm.validateField('idCard');
      }
    },
    submitForm() {
      this.$refs.studentForm.validate((valid) => {
        if (valid) {
          this.$message({
            type: 'success',
            message: '报名成功！我们会尽快与您联系。'
          });
          console.log('报名信息:', this.studentForm);
        } else {
          this.$message.error('请检查表单填写是否正确');
          return false;
        }
      });
    },
    resetForm() {
      this.$refs.studentForm.resetFields();
    }
  }
};
</script>

<style scoped>
.student-reg {
  max-width: 900px;
}
</style>
