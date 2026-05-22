<template>
  <div class="page-container">
    <el-button @click="goBack" class="back-btn">
      <i class="el-icon-arrow-left"></i> 返回
    </el-button>

    <el-card v-if="activity" class="register-card card-shadow">
      <div class="register-header">
        <h2 class="register-title">活动报名</h2>
        <div class="activity-info-bar">
          <span class="activity-name">{{ activity.title }}</span>
          <el-tag type="info">{{ activity.date }} {{ activity.time }}</el-tag>
          <el-tag type="warning">{{ activity.location }}</el-tag>
          <el-tag :type="isFull ? 'danger' : 'success'">
            {{ activity.currentParticipants }}/{{ activity.maxParticipants }}人
          </el-tag>
        </div>
        <el-alert
          v-if="isFull"
          title="活动已满员"
          type="error"
          :closable="false"
          style="margin-top: 15px;"
          show-icon>
        </el-alert>
      </div>

      <el-form
        ref="registerForm"
        :model="registerForm"
        :rules="rules"
        label-width="100px"
        class="register-form"
      >
        <el-form-item label="姓名" prop="name">
          <el-input v-model="registerForm.name" placeholder="请输入真实姓名" maxlength="20"></el-input>
        </el-form-item>

        <el-form-item label="手机号" prop="phone">
          <el-input v-model="registerForm.phone" placeholder="请输入手机号" maxlength="11"></el-input>
        </el-form-item>

        <el-form-item label="学号" prop="studentId">
          <el-input v-model="registerForm.studentId" placeholder="请输入学号" maxlength="15"></el-input>
        </el-form-item>

        <el-form-item label="学院" prop="college">
          <el-select v-model="registerForm.college" placeholder="请选择学院" style="width: 100%">
            <el-option label="计算机学院" value="计算机学院"></el-option>
            <el-option label="文学院" value="文学院"></el-option>
            <el-option label="理学院" value="理学院"></el-option>
            <el-option label="工学院" value="工学院"></el-option>
            <el-option label="商学院" value="商学院"></el-option>
            <el-option label="外语学院" value="外语学院"></el-option>
            <el-option label="艺术学院" value="艺术学院"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="年级" prop="grade">
          <el-radio-group v-model="registerForm.grade">
            <el-radio label="2021级"></el-radio>
            <el-radio label="2022级"></el-radio>
            <el-radio label="2023级"></el-radio>
            <el-radio label="2024级"></el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="性别" prop="gender">
          <el-radio-group v-model="registerForm.gender">
            <el-radio label="男"></el-radio>
            <el-radio label="女"></el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <el-input v-model="registerForm.email" placeholder="请输入邮箱地址" maxlength="50"></el-input>
        </el-form-item>

        <el-form-item label="备注" prop="remark">
          <el-input
            type="textarea"
            v-model="registerForm.remark"
            :rows="4"
            placeholder="如有特殊需求请在此说明（选填）"
            maxlength="200"
            show-word-limit
          ></el-input>
        </el-form-item>

        <el-form-item>
          <el-checkbox v-model="registerForm.agreed">
            我已阅读并同意<a href="#" class="agreement-link">《活动参与须知》</a>
          </el-checkbox>
        </el-form-item>

        <el-form-item class="form-actions">
          <el-button type="primary" size="large" @click="submitForm" :loading="submitting" :disabled="isFull">
            {{ isFull ? '活动已满员' : '确认报名' }}
          </el-button>
          <el-button size="large" @click="resetForm" :disabled="isFull">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-empty v-else description="活动不存在"></el-empty>
  </div>
</template>

<script>
import { activities } from '../mock/data'

export default {
  name: 'ActivityRegister',
  computed: {
    isFull() {
      if (!this.activity) return false
      return this.activity.currentParticipants >= this.activity.maxParticipants
    }
  },
  data() {
    const validatePhone = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入手机号'))
      } else if (!/^1[3-9]\d{9}$/.test(value)) {
        callback(new Error('请输入正确的手机号格式'))
      } else {
        callback()
      }
    }

    const validateEmail = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入邮箱地址'))
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
        callback(new Error('请输入正确的邮箱格式'))
      } else {
        callback()
      }
    }

    const validateAgreed = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请先阅读并同意活动参与须知'))
      } else {
        callback()
      }
    }

    return {
      activity: null,
      submitting: false,
      registerForm: {
        name: '',
        phone: '',
        studentId: '',
        college: '',
        grade: '',
        gender: '',
        email: '',
        remark: '',
        agreed: false
      },
      rules: {
        name: [
          { required: true, message: '请输入姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '姓名长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        phone: [
          { validator: validatePhone, trigger: 'blur' }
        ],
        studentId: [
          { required: true, message: '请输入学号', trigger: 'blur' },
          { pattern: /^\d+$/, message: '学号必须为数字', trigger: 'blur' }
        ],
        college: [
          { required: true, message: '请选择学院', trigger: 'change' }
        ],
        grade: [
          { required: true, message: '请选择年级', trigger: 'change' }
        ],
        gender: [
          { required: true, message: '请选择性别', trigger: 'change' }
        ],
        email: [
          { validator: validateEmail, trigger: 'blur' }
        ],
        agreed: [
          { validator: validateAgreed, trigger: 'change' }
        ]
      }
    }
  },
  mounted() {
    this.loadActivity()
  },
  methods: {
    loadActivity() {
      const id = parseInt(this.$route.params.id)
      this.activity = activities.find(item => item.id === id)
    },
    goBack() {
      this.$router.push(`/activity/${this.$route.params.id}`)
    },
    submitForm() {
      if (this.isFull) {
        this.$message.error('活动已满员')
        return false
      }
      this.$refs.registerForm.validate((valid) => {
        if (valid) {
          this.submitting = true
          setTimeout(() => {
            this.submitting = false
            this.$message.success('报名成功！')
            this.$router.push('/my-registrations')
          }, 1000)
        } else {
          this.$message.error('请完善表单信息')
          return false
        }
      })
    },
    resetForm() {
      this.$refs.registerForm.resetFields()
    }
  }
}
</script>

<style scoped>
.back-btn {
  margin-bottom: 20px;
}

.register-card {
  background: white;
  max-width: 700px;
  margin: 0 auto;
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.register-title {
  font-size: 22px;
  color: #303133;
  margin: 0 0 15px 0;
}

.activity-info-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  flex-wrap: wrap;
}

.activity-name {
  font-size: 14px;
  color: #606266;
  font-weight: 500;
}

.register-form {
  max-width: 500px;
  margin: 0 auto;
}

.agreement-link {
  color: #409eff;
  text-decoration: none;
}

.agreement-link:hover {
  text-decoration: underline;
}

.form-actions {
  text-align: center;
  padding-top: 20px;
}

.form-actions .el-button {
  width: 150px;
  margin: 0 10px;
}
</style>
