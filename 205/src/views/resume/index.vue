<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">简历投递</h2>
    </div>

    <div class="form-container">
      <h3 class="form-title">填写简历信息</h3>
      <el-form :model="resumeForm" :rules="resumeRules" ref="resumeForm" label-width="120px">
        <el-divider content-position="left">基本信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="resumeForm.name" placeholder="请输入姓名"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-radio-group v-model="resumeForm.gender">
                <el-radio label="男">男</el-radio>
                <el-radio label="女">女</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="手机号码" prop="phone">
              <el-input v-model="resumeForm.phone" placeholder="请输入手机号码"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="电子邮箱" prop="email">
              <el-input v-model="resumeForm.email" placeholder="请输入电子邮箱"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="出生日期" prop="birthday">
              <el-date-picker
                v-model="resumeForm.birthday"
                type="date"
                placeholder="选择出生日期"
                style="width: 100%;">
              </el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="工作年限" prop="experience">
              <el-select v-model="resumeForm.experience" placeholder="请选择工作年限" style="width: 100%;">
                <el-option label="应届毕业生" value="应届毕业生"></el-option>
                <el-option label="1-3年" value="1-3年"></el-option>
                <el-option label="3-5年" value="3-5年"></el-option>
                <el-option label="5-10年" value="5-10年"></el-option>
                <el-option label="10年以上" value="10年以上"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="居住地址" prop="address">
              <el-input v-model="resumeForm.address" placeholder="请输入居住地址"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">教育背景</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="最高学历" prop="education">
              <el-select v-model="resumeForm.education" placeholder="请选择最高学历" style="width: 100%;">
                <el-option label="大专" value="大专"></el-option>
                <el-option label="本科" value="本科"></el-option>
                <el-option label="硕士" value="硕士"></el-option>
                <el-option label="博士" value="博士"></el-option>
                <el-option label="其他" value="其他"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="毕业院校" prop="school">
              <el-input v-model="resumeForm.school" placeholder="请输入毕业院校"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="专业" prop="major">
              <el-input v-model="resumeForm.major" placeholder="请输入专业"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="毕业时间" prop="graduationTime">
              <el-date-picker
                v-model="resumeForm.graduationTime"
                type="month"
                placeholder="选择毕业时间"
                style="width: 100%;">
              </el-date-picker>
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">求职意向</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="应聘岗位" prop="jobId">
              <el-select v-model="resumeForm.jobId" placeholder="请选择应聘岗位" style="width: 100%;">
                <el-option
                  v-for="item in jobOptions"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="期望薪资" prop="expectedSalary">
              <el-input v-model="resumeForm.expectedSalary" placeholder="如：15k-20k"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="求职状态" prop="jobStatus">
              <el-select v-model="resumeForm.jobStatus" placeholder="请选择求职状态" style="width: 100%;">
                <el-option label="在职，考虑机会" value="在职，考虑机会"></el-option>
                <el-option label="在职，暂不考虑" value="在职，暂不考虑"></el-option>
                <el-option label="离职，随时到岗" value="离职，随时到岗"></el-option>
                <el-option label="应届生" value="应届生"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="到岗时间" prop="availableTime">
              <el-select v-model="resumeForm.availableTime" placeholder="请选择到岗时间" style="width: 100%;">
                <el-option label="随时到岗" value="随时到岗"></el-option>
                <el-option label="1周内" value="1周内"></el-option>
                <el-option label="2周内" value="2周内"></el-option>
                <el-option label="1个月内" value="1个月内"></el-option>
                <el-option label="1-3个月" value="1-3个月"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">技能特长</el-divider>
        <el-form-item label="专业技能" prop="skills">
          <el-input type="textarea" v-model="resumeForm.skills" :rows="4" placeholder="请描述您的专业技能和特长"></el-input>
        </el-form-item>

        <el-divider content-position="left">工作经历</el-divider>
        <el-form-item label="工作经历" prop="workExperience">
          <el-input type="textarea" v-model="resumeForm.workExperience" :rows="6" placeholder="请详细描述您的工作经历，包括公司名称、职位、工作时间、主要职责和业绩"></el-input>
        </el-form-item>

        <el-divider content-position="left">项目经历</el-divider>
        <el-form-item label="项目经历" prop="projectExperience">
          <el-input type="textarea" v-model="resumeForm.projectExperience" :rows="6" placeholder="请详细描述您参与的项目经历，包括项目名称、项目描述、担任角色、主要贡献等"></el-input>
        </el-form-item>

        <el-divider content-position="left">附件上传</el-divider>
        <el-form-item label="上传简历" prop="resumeFile">
          <el-upload
            ref="upload"
            action=""
            :auto-upload="false"
            :on-change="handleFileChange"
            :on-remove="handleFileRemove"
            :file-list="fileList"
            :limit="1"
            accept=".pdf,.doc,.docx">
            <el-button slot="trigger" size="small" type="primary">选择文件</el-button>
            <div slot="tip" class="el-upload__tip">只能上传 pdf/doc/docx 文件，且不超过 10MB</div>
          </el-upload>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" size="large" @click="handleSubmit">提交申请</el-button>
          <el-button size="large" @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { jobList } from '@/mock/data.js'
import { store } from '@/store/index.js'

export default {
  name: 'Resume',
  data() {
    return {
      resumeForm: {
        name: '',
        gender: '男',
        phone: '',
        email: '',
        birthday: '',
        experience: '',
        address: '',
        education: '',
        school: '',
        major: '',
        graduationTime: '',
        jobId: '',
        expectedSalary: '',
        jobStatus: '',
        availableTime: '',
        skills: '',
        workExperience: '',
        projectExperience: '',
        resumeFile: null
      },
      resumeRules: {
        name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
        gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
        phone: [
          { required: true, message: '请输入手机号码', trigger: 'blur' },
          { pattern: /^1[3456789]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入电子邮箱', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
        ],
        birthday: [{ required: true, message: '请选择出生日期', trigger: 'change' }],
        experience: [{ required: true, message: '请选择工作年限', trigger: 'change' }],
        address: [{ required: true, message: '请输入居住地址', trigger: 'blur' }],
        education: [{ required: true, message: '请选择最高学历', trigger: 'change' }],
        school: [{ required: true, message: '请输入毕业院校', trigger: 'blur' }],
        major: [{ required: true, message: '请输入专业', trigger: 'blur' }],
        graduationTime: [{ required: true, message: '请选择毕业时间', trigger: 'change' }],
        jobId: [{ required: true, message: '请选择应聘岗位', trigger: 'change' }],
        expectedSalary: [{ required: true, message: '请输入期望薪资', trigger: 'blur' }],
        jobStatus: [{ required: true, message: '请选择求职状态', trigger: 'change' }],
        availableTime: [{ required: true, message: '请选择到岗时间', trigger: 'change' }],
        skills: [{ required: true, message: '请输入专业技能', trigger: 'blur' }],
        workExperience: [{ required: true, message: '请输入工作经历', trigger: 'blur' }]
      },
      jobOptions: jobList.filter(item => item.status === '招聘中'),
      fileList: []
    }
  },
  computed: {
    applicationRecords() {
      return store.applications
    }
  },
  methods: {
    handleFileChange(file, fileList) {
      this.fileList = fileList
      this.resumeForm.resumeFile = file.raw
    },
    handleFileRemove(file, fileList) {
      this.fileList = fileList
      this.resumeForm.resumeFile = null
    },
    checkDuplicateApplication() {
      const selectedJob = this.jobOptions.find(item => item.id === this.resumeForm.jobId)
      if (!selectedJob) return false
      
      const isDuplicate = this.applicationRecords.some(item => {
        return item.name === this.resumeForm.name && 
               item.phone === this.resumeForm.phone &&
               item.jobName === selectedJob.name &&
               item.status !== '已拒绝'
      })
      return isDuplicate
    },
    handleSubmit() {
      this.$refs.resumeForm.validate((valid) => {
        if (valid) {
          if (!this.resumeForm.resumeFile) {
            this.$message.warning('请上传简历附件')
            return
          }
          
          if (this.checkDuplicateApplication()) {
            this.$message.error('您已投递过该岗位，请勿重复投递！')
            return
          }
          
          this.$confirm('确认提交简历申请吗？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'info'
          }).then(() => {
            const selectedJob = this.jobOptions.find(item => item.id === this.resumeForm.jobId)
            const newRecord = {
              id: Math.max(...this.applicationRecords.map(item => item.id), 0) + 1,
              name: this.resumeForm.name,
              phone: this.resumeForm.phone,
              email: this.resumeForm.email,
              jobName: selectedJob ? selectedJob.name : '',
              applyTime: new Date().toISOString().split('T')[0],
              status: '待审核',
              resume: this.resumeForm.resumeFile ? this.resumeForm.resumeFile.name : '简历.pdf'
            }
            store.addApplication(newRecord)
            this.$message.success('简历提交成功！我们会尽快与您联系。')
            this.handleReset()
          }).catch(() => {})
        }
      })
    },
    handleReset() {
      this.$refs.resumeForm.resetFields()
      this.fileList = []
      this.resumeForm.resumeFile = null
    }
  }
}
</script>

<style lang="scss" scoped>
.el-divider {
  margin: 20px 0;
}
</style>
