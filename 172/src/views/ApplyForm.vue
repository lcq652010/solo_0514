<template>
  <div class="page-container">
    <div class="page-title">考试报名申请</div>
    
    <div class="form-wrapper">
      <el-form
        ref="applyForm"
        :model="applyForm"
        :rules="rules"
        label-width="120px"
        size="medium"
      >
        <el-card class="mb-20">
          <div slot="header" class="clearfix">
            <span>选择考试科目</span>
          </div>
          <el-form-item label="考试科目" prop="subjectId">
            <el-select
              v-model="applyForm.subjectId"
              placeholder="请选择考试科目"
              style="width: 100%;"
              @change="handleSubjectChange"
            >
              <el-option
                v-for="item in availableSubjects"
                :key="item.id"
                :label="item.name"
                :value="item.id"
                :disabled="isSubjectDisabled(item)"
              >
                <span style="float: left;">{{ item.name }}</span>
                <span style="float: right; color: #8492a6; font-size: 13px;">
                  {{ item.code }} - ¥{{ item.fee }}
                </span>
              </el-option>
            </el-select>
          </el-form-item>
          
          <div v-if="selectedSubject" style="background: #f5f7fa; padding: 15px; border-radius: 4px;">
            <p><strong>科目代码：</strong>{{ selectedSubject.code }}</p>
            <p><strong>考试时间：</strong>{{ selectedSubject.examDate }} {{ selectedSubject.examTime }}</p>
            <p><strong>报名费用：</strong>¥{{ selectedSubject.fee }}</p>
            <p><strong>科目说明：</strong>{{ selectedSubject.description }}</p>
            <div style="margin-top: 10px; padding-top: 10px; border-top: 1px dashed #dcdfe6;">
              <p style="font-weight: 500; margin-bottom: 8px;">报考要求：</p>
              <p v-if="selectedSubject.requirements.minAge">
                <i class="el-icon-info" style="color: #409EFF;"></i>
                最低年龄：{{ selectedSubject.requirements.minAge }}周岁
                <span v-if="selectedSubject.requirements.maxAge">，最高年龄：{{ selectedSubject.requirements.maxAge }}周岁</span>
              </p>
              <p v-if="selectedSubject.requirements.minEducation">
                <i class="el-icon-info" style="color: #409EFF;"></i>
                最低学历：{{ selectedSubject.requirements.minEducation }}
              </p>
              <p v-if="selectedSubject.requirements.prerequisite && selectedSubject.requirements.prerequisite.length > 0">
                <i class="el-icon-info" style="color: #409EFF;"></i>
                前置条件：需通过 {{ selectedSubject.requirements.prerequisite.join('、') }}
              </p>
            </div>
          </div>

          <el-alert
            v-if="qualificationCheckResult.show"
            :title="qualificationCheckResult.message"
            :type="qualificationCheckResult.passed ? 'success' : 'error'"
            :closable="false"
            style="margin-top: 15px;"
            show-icon
          >
          </el-alert>
        </el-card>

        <el-card class="mb-20">
          <div slot="header" class="clearfix">
            <span>个人信息</span>
          </div>
          
          <el-form-item label="姓名" prop="applicantName">
            <el-input v-model="applyForm.applicantName" placeholder="请输入真实姓名" maxlength="20"></el-input>
          </el-form-item>

          <el-form-item label="身份证号" prop="idCard">
            <el-input v-model="applyForm.idCard" placeholder="请输入18位身份证号" maxlength="18" @blur="checkDuplicateRegistration"></el-input>
          </el-form-item>

          <el-form-item label="手机号码" prop="phone">
            <el-input v-model="applyForm.phone" placeholder="请输入11位手机号码" maxlength="11"></el-input>
          </el-form-item>

          <el-form-item label="电子邮箱" prop="email">
            <el-input v-model="applyForm.email" placeholder="请输入常用邮箱地址" maxlength="50"></el-input>
          </el-form-item>

          <el-form-item label="性别" prop="gender">
            <el-radio-group v-model="applyForm.gender">
              <el-radio label="男">男</el-radio>
              <el-radio label="女">女</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item label="出生日期" prop="birthday">
            <el-date-picker
              v-model="applyForm.birthday"
              type="date"
              placeholder="选择出生日期"
              style="width: 100%;"
              value-format="yyyy-MM-dd"
              @change="handleBirthdayChange"
            ></el-date-picker>
          </el-form-item>

          <el-form-item label="年龄" prop="age">
            <el-input v-model="age" disabled placeholder="自动计算年龄"></el-input>
          </el-form-item>

          <el-form-item label="学历" prop="education">
            <el-select v-model="applyForm.education" placeholder="请选择学历" style="width: 100%;" @change="handleEducationChange">
              <el-option label="高中及以下" value="高中及以下"></el-option>
              <el-option label="大专" value="大专"></el-option>
              <el-option label="本科" value="本科"></el-option>
              <el-option label="硕士" value="硕士"></el-option>
              <el-option label="博士" value="博士"></el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="联系地址" prop="address">
            <el-input
              v-model="applyForm.address"
              type="textarea"
              :rows="3"
              placeholder="请输入详细联系地址"
              maxlength="200"
            ></el-input>
          </el-form-item>
        </el-card>

        <el-card class="mb-20">
          <div slot="header" class="clearfix">
            <span>上传证件</span>
          </div>
          
          <el-form-item label="身份证照片" prop="idCardPhoto">
            <el-upload
              class="upload-demo"
              action="#"
              :auto-upload="false"
              :on-change="handleIdCardUpload"
              :file-list="idCardFileList"
              limit="1"
              accept="image/*"
            >
              <el-button size="small" type="primary">点击上传</el-button>
              <div slot="tip" class="el-upload__tip">支持 jpg/png 文件，大小不超过 5MB</div>
            </el-upload>
          </el-form-item>

          <el-form-item label="证件照" prop="photo">
            <el-upload
              class="upload-demo"
              action="#"
              :auto-upload="false"
              :on-change="handlePhotoUpload"
              :file-list="photoFileList"
              limit="1"
              accept="image/*"
            >
              <el-button size="small" type="primary">点击上传</el-button>
              <div slot="tip" class="el-upload__tip">一寸免冠证件照，白底，大小不超过 2MB</div>
            </el-upload>
          </el-form-item>
        </el-card>

        <el-form-item>
          <el-checkbox v-model="agreeProtocol">我已阅读并同意《考试报名须知》和《考生诚信承诺书》</el-checkbox>
        </el-form-item>

        <el-form-item class="text-center">
          <el-button type="primary" size="large" @click="submitForm" :loading="submitting" :disabled="!qualificationCheckResult.passed">
            提交报名
          </el-button>
          <el-button size="large" @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { subjectList, applicationRecords, educationLevel } from '@/mock/data.js'

export default {
  name: 'ApplyForm',
  data() {
    const validateIdCard = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入身份证号'))
      } else if (!/^\d{17}[\dXx]$/.test(value)) {
        callback(new Error('请输入正确的18位身份证号'))
      } else {
        callback()
      }
    }

    const validatePhone = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入手机号码'))
      } else if (!/^1[3-9]\d{9}$/.test(value)) {
        callback(new Error('请输入正确的11位手机号码'))
      } else {
        callback()
      }
    }

    const validateEmail = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入电子邮箱'))
      } else if (!/^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/.test(value)) {
        callback(new Error('请输入正确的邮箱格式'))
      } else {
        callback()
      }
    }

    return {
      subjectList,
      applicationRecords,
      applyForm: {
        subjectId: '',
        applicantName: '',
        idCard: '',
        phone: '',
        email: '',
        gender: '',
        birthday: '',
        education: '',
        address: ''
      },
      rules: {
        subjectId: [
          { required: true, message: '请选择考试科目', trigger: 'change' }
        ],
        applicantName: [
          { required: true, message: '请输入姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '姓名长度在2到20个字符', trigger: 'blur' }
        ],
        idCard: [
          { validator: validateIdCard, trigger: 'blur' }
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
        address: [
          { required: true, message: '请输入联系地址', trigger: 'blur' }
        ]
      },
      agreeProtocol: false,
      submitting: false,
      idCardFileList: [],
      photoFileList: [],
      age: '',
      qualificationCheckResult: {
        show: false,
        passed: true,
        message: ''
      }
    }
  },
  computed: {
    availableSubjects() {
      return this.subjectList.filter(item => 
        item.status === 1 && item.enrolled < item.quota
      )
    },
    selectedSubject() {
      return this.subjectList.find(item => item.id === this.applyForm.subjectId)
    }
  },
  mounted() {
    const subjectId = this.$route.query.subjectId
    if (subjectId) {
      this.applyForm.subjectId = parseInt(subjectId)
    }
  },
  methods: {
    isSubjectDisabled(subject) {
      if (!this.applyForm.idCard) return false
      const existingRecord = this.applicationRecords.find(record =>
        record.idCard === this.applyForm.idCard &&
        record.subjectId === subject.id &&
        record.status !== 3
      )
      return !!existingRecord
    },

    calculateAge(birthday) {
      if (!birthday) return ''
      const birthDate = new Date(birthday)
      const today = new Date()
      let age = today.getFullYear() - birthDate.getFullYear()
      const monthDiff = today.getMonth() - birthDate.getMonth()
      if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        age--
      }
      return age
    },

    handleBirthdayChange() {
      this.age = this.calculateAge(this.applyForm.birthday)
      this.checkQualification()
    },

    handleEducationChange() {
      this.checkQualification()
    },

    handleSubjectChange() {
      this.checkQualification()
    },

    checkDuplicateRegistration() {
      if (!this.applyForm.idCard || !this.applyForm.subjectId) {
        return
      }
      
      const existingRecord = this.applicationRecords.find(record =>
        record.idCard === this.applyForm.idCard &&
        record.subjectId === this.applyForm.subjectId &&
        record.status !== 3
      )

      if (existingRecord) {
        const statusText = { 1: '待审核', 2: '审核通过' }[existingRecord.status]
        this.$message.warning(`您已报名该科目，当前状态：${statusText}，请勿重复报名`)
      }
      
      this.checkQualification()
    },

    checkQualification() {
      if (!this.selectedSubject || !this.applyForm.idCard) {
        this.qualificationCheckResult = { show: false, passed: false, message: '' }
        return
      }

      const requirements = this.selectedSubject.requirements
      const failedChecks = []

      const existingRecord = this.applicationRecords.find(record =>
        record.idCard === this.applyForm.idCard &&
        record.subjectId === this.applyForm.subjectId &&
        record.status !== 3
      )

      if (existingRecord) {
        const statusText = { 1: '待审核', 2: '审核通过' }[existingRecord.status]
        failedChecks.push(`您已报名该科目（状态：${statusText}），请勿重复报名`)
      }

      if (this.age) {
        if (requirements.minAge && this.age < requirements.minAge) {
          failedChecks.push(`年龄不足，最低要求 ${requirements.minAge} 周岁`)
        }
        if (requirements.maxAge && this.age > requirements.maxAge) {
          failedChecks.push(`年龄超出限制，最高要求 ${requirements.maxAge} 周岁`)
        }
      }

      if (this.applyForm.education) {
        const userLevel = educationLevel[this.applyForm.education]
        const requiredLevel = educationLevel[requirements.minEducation]
        if (userLevel < requiredLevel) {
          failedChecks.push(`学历不满足要求，最低要求 ${requirements.minEducation}`)
        }
      }

      if (requirements.prerequisite && requirements.prerequisite.length > 0) {
        const passedPrerequisites = requirements.prerequisite.filter(subjectName => {
          return this.applicationRecords.some(record =>
            record.idCard === this.applyForm.idCard &&
            record.subjectName === subjectName &&
            record.status === 2
          )
        })

        if (passedPrerequisites.length < requirements.prerequisite.length) {
          failedChecks.push(`需先通过前置科目：${requirements.prerequisite.join('、')}`)
        }
      }

      if (failedChecks.length > 0) {
        this.qualificationCheckResult = {
          show: true,
          passed: false,
          message: `报名资格校验不通过：${failedChecks.join('；')}`
        }
      } else {
        this.qualificationCheckResult = {
          show: true,
          passed: true,
          message: '恭喜，您满足该科目的所有报考条件！'
        }
      }
    },

    handleIdCardUpload(file) {
      this.idCardFileList = [file]
    },
    handlePhotoUpload(file) {
      this.photoFileList = [file]
    },

    submitForm() {
      this.$refs.applyForm.validate((valid) => {
        if (valid) {
          if (!this.qualificationCheckResult.passed) {
            this.$message.error('您不满足该科目的报考资格，无法提交报名')
            return
          }

          if (!this.agreeProtocol) {
            this.$message.warning('请阅读并同意相关协议')
            return
          }
          if (this.idCardFileList.length === 0) {
            this.$message.warning('请上传身份证照片')
            return
          }
          if (this.photoFileList.length === 0) {
            this.$message.warning('请上传证件照')
            return
          }
          
          this.submitting = true
          
          setTimeout(() => {
            this.submitting = false
            
            const newRecord = {
              id: this.applicationRecords.length + 1,
              applicantName: this.applyForm.applicantName,
              idCard: this.applyForm.idCard,
              phone: this.applyForm.phone,
              email: this.applyForm.email,
              subjectId: this.applyForm.subjectId,
              subjectName: this.selectedSubject.name,
              subjectCode: this.selectedSubject.code,
              examDate: this.selectedSubject.examDate,
              examTime: this.selectedSubject.examTime,
              applyTime: new Date().toLocaleString('zh-CN', { 
                year: 'numeric', month: '2-digit', day: '2-digit',
                hour: '2-digit', minute: '2-digit', second: '2-digit'
              }).replace(/\//g, '-'),
              status: 1,
              reviewTime: '',
              reviewer: ''
            }
            this.applicationRecords.push(newRecord)
            
            this.$message.success('报名申请提交成功！请等待审核')
            this.$router.push('/records')
          }, 1500)
        } else {
          this.$message.error('请检查表单信息是否填写正确')
          return false
        }
      })
    },
    resetForm() {
      this.$refs.applyForm.resetFields()
      this.agreeProtocol = false
      this.idCardFileList = []
      this.photoFileList = []
      this.age = ''
      this.qualificationCheckResult = { show: false, passed: false, message: '' }
    }
  }
}
</script>

<style scoped>
.upload-demo {
  width: 100%;
}
</style>
