<template>
  <div class="page-container">
    <h2 class="page-title">
      <i class="el-icon-edit-outline"></i>
      在线挂号
    </h2>

    <el-steps :active="activeStep" align-center class="steps">
      <el-step title="选择挂号信息"></el-step>
      <el-step title="填写患者信息"></el-step>
      <el-step title="确认挂号成功"></el-step>
    </el-steps>

    <div v-show="activeStep === 0" class="step-content">
      <el-form :model="registerForm" :rules="step1Rules" ref="step1Form" label-width="100px" class="register-form">
        <el-form-item label="选择科室" prop="department">
          <el-select v-model="registerForm.department" placeholder="请选择科室" style="width: 300px;" @change="onDepartmentChange">
            <el-option v-for="dept in departments" :key="dept.id" :label="dept.name" :value="dept.name"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="选择医生" prop="doctor">
          <el-select v-model="registerForm.doctor" placeholder="请选择医生" style="width: 300px;" @change="onDoctorChange">
            <el-option v-for="doc in filteredDoctors" :key="doc.id" :label="doc.name + ' - ' + doc.title" :value="doc.name"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="选择日期" prop="date">
          <el-date-picker
            v-model="registerForm.date"
            type="date"
            placeholder="选择就诊日期"
            style="width: 300px;"
            value-format="yyyy-MM-dd"
            :picker-options="pickerOptions"
          ></el-date-picker>
        </el-form-item>

        <el-form-item label="选择时段" prop="time">
          <el-radio-group v-model="registerForm.time">
            <el-radio label="上午">上午 08:00-12:00</el-radio>
            <el-radio label="下午">下午 14:00-17:30</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item v-if="selectedSchedule">
          <el-alert
            :title="'挂号费：¥' + selectedSchedule.fee + '元，剩余号源：' + selectedSchedule.remaining + '个'"
            type="info"
            :closable="false"
            show-icon
          >
          </el-alert>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="nextStep">下一步</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div v-show="activeStep === 1" class="step-content">
      <el-form :model="registerForm" :rules="step2Rules" ref="step2Form" label-width="100px" class="register-form">
        <el-form-item label="患者姓名" prop="patientName">
          <el-input v-model="registerForm.patientName" placeholder="请输入患者姓名" style="width: 300px;"></el-input>
        </el-form-item>

        <el-form-item label="身份证号" prop="idCard">
          <el-input v-model="registerForm.idCard" placeholder="请输入身份证号" style="width: 300px;" maxlength="18"></el-input>
        </el-form-item>

        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="registerForm.phone" placeholder="请输入联系电话" style="width: 300px;" maxlength="11"></el-input>
        </el-form-item>

        <el-form-item label="性别" prop="gender">
          <el-radio-group v-model="registerForm.gender">
            <el-radio label="男">男</el-radio>
            <el-radio label="女">女</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="年龄" prop="age">
          <el-input-number v-model="registerForm.age" :min="0" :max="150" style="width: 300px;"></el-input-number>
        </el-form-item>

        <el-form-item label="症状描述">
          <el-input
            type="textarea"
            v-model="registerForm.symptoms"
            :rows="4"
            placeholder="请简要描述症状（选填）"
            style="width: 300px;"
          ></el-input>
        </el-form-item>

        <el-form-item>
          <el-button @click="prevStep">上一步</el-button>
          <el-button type="primary" @click="submitRegister">提交挂号</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div v-show="activeStep === 2" class="step-content success-content">
      <el-result icon="success" title="挂号成功" sub-title="请按时前往医院就诊">
        <template slot="extra">
          <el-card class="result-card">
            <div slot="header" class="card-header">
            <span>挂号详情</span>
          </div>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="就诊科室">{{ registerForm.department }}</el-descriptions-item>
            <el-descriptions-item label="就诊医生">{{ registerForm.doctor }}</el-descriptions-item>
            <el-descriptions-item label="就诊日期">{{ registerForm.date }}</el-descriptions-item>
            <el-descriptions-item label="就诊时段">{{ registerForm.time }}</el-descriptions-item>
            <el-descriptions-item label="患者姓名">{{ registerForm.patientName }}</el-descriptions-item>
            <el-descriptions-item label="挂号单号">{{ registerNo }}</el-descriptions-item>
          </el-descriptions>
        </el-card>
        <div style="margin-top: 20px;">
          <el-button type="primary" @click="goRecords">查看挂号记录</el-button>
          <el-button @click="resetForm">继续挂号</el-button>
        </div>
        </template>
      </el-result>
    </div>
  </div>
</template>

<script>
import { departments, doctors } from '@/mock/data';
import { store } from '@/store';

export default {
  name: 'RegistrationForm',
  data() {
    const validateIdCard = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入身份证号'));
      } else if (!/^\d{17}[\dXx]$/.test(value)) {
        callback(new Error('请输入正确的身份证号'));
      } else {
        callback();
      }
    };
    const validatePhone = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入联系电话'));
      } else if (!/^1[3-9]\d{9}$/.test(value)) {
        callback(new Error('请输入正确的手机号'));
      } else {
        callback();
      }
    };
    return {
      departments: departments.filter(d => d.status === 1),
      doctors: [...doctors],
      activeStep: 0,
      registerNo: '',
      registerForm: {
        department: '',
        doctor: '',
        date: '',
        time: '',
        patientName: '',
        idCard: '',
        phone: '',
        gender: '男',
        age: 30,
        symptoms: ''
      },
      step1Rules: {
        department: [{ required: true, message: '请选择科室', trigger: 'change' }],
        doctor: [{ required: true, message: '请选择医生', trigger: 'change' }],
        date: [{ required: true, message: '请选择就诊日期', trigger: 'change' }],
        time: [{ required: true, message: '请选择就诊时段', trigger: 'change' }]
      },
      step2Rules: {
        patientName: [{ required: true, message: '请输入患者姓名', trigger: 'blur' }],
        idCard: [{ required: true, validator: validateIdCard, trigger: 'blur' }],
        phone: [{ required: true, validator: validatePhone, trigger: 'blur' }],
        gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
        age: [{ required: true, message: '请输入年龄', trigger: 'blur' }]
      },
      pickerOptions: {
        disabledDate(time) {
          return time.getTime() < Date.now() - 8.64e7;
        }
      },
      refreshTimer: null
    };
  },
  computed: {
    scheduleList() {
      return store.getSchedules();
    },
    registrationList() {
      return store.getRegistrations();
    },
    filteredDoctors() {
      if (!this.registerForm.department) return [];
      return this.doctors.filter(doc => doc.department === this.registerForm.department);
    },
    selectedSchedule() {
      if (!this.registerForm.doctor || !this.registerForm.date || !this.registerForm.time) {
        return null;
      }
      return this.scheduleList.find(s => 
        s.doctorName === this.registerForm.doctor && 
        s.date === this.registerForm.date && 
        s.time === this.registerForm.time
      );
    }
  },
  mounted() {
    if (this.$route.query.department) {
      this.registerForm.department = this.$route.query.department;
    }
    if (this.$route.query.doctor) {
      this.registerForm.doctor = this.$route.query.doctor;
    }
    if (this.$route.query.date) {
      this.registerForm.date = this.$route.query.date;
    }
    if (this.$route.query.time) {
      this.registerForm.time = this.$route.query.time;
    }
    // 自动刷新号源状态
    this.startAutoRefresh();
  },
  beforeDestroy() {
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer);
    }
  },
  methods: {
    startAutoRefresh() {
      // 每30秒自动刷新一次号源状态
      this.refreshTimer = setInterval(() => {
        // 触发计算属性重新计算
        this.$forceUpdate();
      }, 30000);
    },
    onDepartmentChange() {
      this.registerForm.doctor = '';
    },
    onDoctorChange() {
    },
    nextStep() {
      this.$refs.step1Form.validate(valid => {
        if (valid) {
          if (!this.selectedSchedule) {
            this.$message.warning('该医生在所选日期时段没有排班，请重新选择');
            return;
          }
          if (this.selectedSchedule.remaining <= 0) {
            this.$message.warning('该时段号源已满，请选择其他时段');
            return;
          }
          this.activeStep = 1;
        }
      });
    },
    prevStep() {
      this.activeStep = 0;
    },
    submitRegister() {
      this.$refs.step2Form.validate(valid => {
        if (valid) {
          // 校验1：号源余量校验
          if (this.selectedSchedule && this.selectedSchedule.remaining <= 0) {
            this.$message.error('该时段号源已满，请选择其他时段或医生！');
            return;
          }
          
          // 校验2：患者当日同科室重复挂号校验（根据身份证号）
          const duplicateRecord = this.registrationList.find(record => 
            record.idCard === this.registerForm.idCard && 
            record.department === this.registerForm.department && 
            record.date === this.registerForm.date &&
            record.status !== 3 // 已取消的记录不算重复
          );
          
          if (duplicateRecord) {
            this.$message.error(`该患者当日已在${this.registerForm.department}挂过号，请勿重复挂号！`);
            return;
          }
          
          this.registerNo = 'GH' + Date.now().toString().slice(-8);
          const newRegistration = {
            id: this.registrationList.length + 1,
            patientName: this.registerForm.patientName,
            idCard: this.registerForm.idCard,
            phone: this.registerForm.phone,
            department: this.registerForm.department,
            doctor: this.registerForm.doctor,
            date: this.registerForm.date,
            time: this.registerForm.time,
            number: String(this.registrationList.length + 1).padStart(3, '0'),
            status: 0,
            createTime: new Date().toLocaleString()
          };
          
          // 使用store保存数据并通知所有页面更新
          store.addRegistration(newRegistration);
          store.updateScheduleRemaining(
            this.registerForm.doctor, 
            this.registerForm.date, 
            this.registerForm.time, 
            -1
          );
          store.notify();
          
          this.activeStep = 2;
          this.$message.success('挂号成功！');
        }
      });
    },
    goRecords() {
      this.$router.push('/records');
    },
    resetForm() {
      this.activeStep = 0;
      this.registerForm = {
        department: '',
        doctor: '',
        date: '',
        time: '',
        patientName: '',
        idCard: '',
        phone: '',
        gender: '男',
        age: 30,
        symptoms: ''
      };
      this.$refs.step1Form.resetFields();
      this.$refs.step2Form.resetFields();
    }
  }
};
</script>

<style scoped>
.steps {
  margin: 30px 0;
  padding: 0 100px;
}

.step-content {
  padding: 20px 50px;
}

.register-form {
  max-width: 600px;
  margin: 0 auto;
}

.success-content {
  text-align: center;
}

.result-card {
  max-width: 600px;
  margin: 0 auto;
  text-align: left;
}

.card-header {
  font-weight: 600;
  color: #303133;
}
</style>
