<template>
  <div class="enroll-form">
    <h1 class="page-title">学员报名</h1>
    <div class="page-card">
      <div class="form-container">
        <el-form
          ref="enrollForm"
          :model="form"
          :rules="rules"
          label-width="100px"
          label-position="right"
        >
          <el-form-item label="报名课程" prop="courseId">
            <el-select v-model="form.courseId" placeholder="请选择课程" style="width: 100%">
              <el-option
                v-for="course in courseList"
                :key="course.id"
                :label="course.name"
                :value="course.id"
              ></el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="学员姓名" prop="name">
            <el-input v-model="form.name" placeholder="请输入姓名" maxlength="20" show-word-limit></el-input>
          </el-form-item>

          <el-form-item label="手机号码" prop="phone">
            <el-input v-model="form.phone" placeholder="请输入手机号码" maxlength="11"></el-input>
          </el-form-item>

          <el-form-item label="邮箱地址" prop="email">
            <el-input v-model="form.email" placeholder="请输入邮箱地址"></el-input>
          </el-form-item>

          <el-form-item label="性别" prop="gender">
            <el-radio-group v-model="form.gender">
              <el-radio label="male">男</el-radio>
              <el-radio label="female">女</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item label="出生日期" prop="birthday">
            <el-date-picker
              v-model="form.birthday"
              type="date"
              placeholder="选择日期"
              style="width: 100%"
              value-format="yyyy-MM-dd"
            ></el-date-picker>
          </el-form-item>

          <el-form-item label="学历" prop="education">
            <el-select v-model="form.education" placeholder="请选择学历" style="width: 100%">
              <el-option label="高中及以下" value="high_school"></el-option>
              <el-option label="大专" value="college"></el-option>
              <el-option label="本科" value="bachelor"></el-option>
              <el-option label="硕士" value="master"></el-option>
              <el-option label="博士及以上" value="doctor"></el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="工作经验" prop="experience">
            <el-select v-model="form.experience" placeholder="请选择工作经验" style="width: 100%">
              <el-option label="无经验" value="none"></el-option>
              <el-option label="1年以内" value="1year"></el-option>
              <el-option label="1-3年" value="1-3years"></el-option>
              <el-option label="3-5年" value="3-5years"></el-option>
              <el-option label="5年以上" value="5years+"></el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="学习目标" prop="goal">
            <el-checkbox-group v-model="form.goal">
              <el-checkbox label="skill">技能提升</el-checkbox>
              <el-checkbox label="job">求职就业</el-checkbox>
              <el-checkbox label="interest">兴趣爱好</el-checkbox>
              <el-checkbox label="certificate">考取证书</el-checkbox>
            </el-checkbox-group>
          </el-form-item>

          <el-form-item label="备注信息" prop="remark">
            <el-input
              v-model="form.remark"
              type="textarea"
              :rows="4"
              placeholder="请输入备注信息（选填）"
              maxlength="200"
              show-word-limit
            ></el-input>
          </el-form-item>

          <el-form-item label="是否同意协议" prop="agreement">
            <el-checkbox v-model="form.agreement">
              我已阅读并同意<a href="#" style="color: #409EFF;">《学员报名协议》</a>和<a href="#" style="color: #409EFF;">《隐私政策》</a>
            </el-checkbox>
          </el-form-item>

          <el-form-item class="form-footer">
            <el-button type="primary" size="large" @click="handleSubmit" :loading="submitting">
              <i class="el-icon-check"></i> 提交报名
            </el-button>
            <el-button size="large" @click="handleReset">重置表单</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
import { courses, enrollmentRecords } from '@/mock/data'

export default {
  name: 'EnrollForm',
  data() {
    const validatePhone = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入手机号码'))
      } else if (!/^1[3-9]\d{9}$/.test(value)) {
        callback(new Error('请输入正确的手机号码格式'))
      } else {
        callback()
      }
    }

    const validateEmail = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入邮箱地址'))
      } else if (!/^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/.test(value)) {
        callback(new Error('请输入正确的邮箱格式'))
      } else {
        callback()
      }
    }

    const validateAgreement = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请阅读并同意相关协议'))
      } else {
        callback()
      }
    }

    return {
      courseList: courses.filter(c => c.status === 'published'),
      enrollmentRecords: enrollmentRecords,
      form: {
        courseId: '',
        name: '',
        phone: '',
        email: '',
        gender: '',
        birthday: '',
        education: '',
        experience: '',
        goal: [],
        remark: '',
        agreement: false
      },
      rules: {
        courseId: [
          { required: true, message: '请选择报名课程', trigger: 'change' }
        ],
        name: [
          { required: true, message: '请输入学员姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '姓名长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        phone: [
          { validator: validatePhone, trigger: 'blur' }
        ],
        email: [
          { validator: validateEmail, trigger: 'blur' }
        ],
        gender: [
          { required: true, message: '请选择性别', trigger: 'change' }
        ],
        birthday: [
          { required: true, message: '请选择出生日期', trigger: 'change' }
        ],
        education: [
          { required: true, message: '请选择学历', trigger: 'change' }
        ],
        experience: [
          { required: true, message: '请选择工作经验', trigger: 'change' }
        ],
        agreement: [
          { validator: validateAgreement, trigger: 'change' }
        ]
      },
      submitting: false
    }
  },
  mounted() {
    if (this.$route.query.courseId) {
      this.form.courseId = parseInt(this.$route.query.courseId)
    }
  },
  methods: {
    checkDuplicateEnrollment() {
      const { courseId, phone, email } = this.form
      const duplicate = this.enrollmentRecords.find(record => 
        record.courseId === courseId && 
        (record.phone === phone || record.email === email)
      )
      return duplicate
    },
    handleSubmit() {
      this.$refs.enrollForm.validate((valid) => {
        if (valid) {
          const duplicate = this.checkDuplicateEnrollment()
          if (duplicate) {
            const course = this.courseList.find(c => c.id === duplicate.courseId)
            this.$message.error(`您已报名「${course.name}」课程，请勿重复报名！报名时间：${duplicate.enrollTime}`)
            return false
          }
          
          this.submitting = true
          setTimeout(() => {
            const newRecord = {
              id: this.enrollmentRecords.length + 1,
              courseId: this.form.courseId,
              name: this.form.name,
              phone: this.form.phone,
              email: this.form.email,
              enrollTime: new Date().toLocaleString()
            }
            this.enrollmentRecords.push(newRecord)
            
            this.submitting = false
            this.$message.success('报名提交成功！我们会尽快与您联系。')
            this.$router.push('/my-courses')
          }, 1000)
        } else {
          this.$message.error('请检查表单填写是否正确')
          return false
        }
      })
    },
    handleReset() {
      this.$refs.enrollForm.resetFields()
    }
  }
}
</script>
