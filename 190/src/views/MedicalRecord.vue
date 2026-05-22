<template>
  <div class="page-container">
    <div class="page-title">病历录入</div>
    
    <el-card class="box-card">
      <el-form :model="recordForm" :rules="rules" ref="recordForm" label-width="120px">
        <el-divider content-position="left">基本信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="病历编号" prop="recordNo">
              <el-input v-model="recordForm.recordNo" disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="就诊日期" prop="visitDate">
              <el-date-picker
                v-model="recordForm.visitDate"
                type="datetime"
                placeholder="选择日期时间"
                style="width: 100%">
              </el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="就诊类型" prop="visitType">
              <el-select v-model="recordForm.visitType" style="width: 100%">
                <el-option label="初诊" value="初诊"></el-option>
                <el-option label="复诊" value="复诊"></el-option>
                <el-option label="急诊" value="急诊"></el-option>
                <el-option label="体检" value="体检"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="宠物名称" prop="petName">
              <el-input v-model="recordForm.petName"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="宠物品种" prop="breed">
              <el-input v-model="recordForm.breed"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="主人姓名" prop="ownerName">
              <el-input v-model="recordForm.ownerName"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="主治医师" prop="doctor">
              <el-select v-model="recordForm.doctor" style="width: 100%">
                <el-option label="张医生" value="张医生"></el-option>
                <el-option label="李医生" value="李医生"></el-option>
                <el-option label="王医生" value="王医生"></el-option>
                <el-option label="赵医生" value="赵医生"></el-option>
                <el-option label="刘医生" value="刘医生"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="科室" prop="department">
              <el-select v-model="recordForm.department" style="width: 100%">
                <el-option label="内科" value="内科"></el-option>
                <el-option label="外科" value="外科"></el-option>
                <el-option label="皮肤科" value="皮肤科"></el-option>
                <el-option label="眼科" value="眼科"></el-option>
                <el-option label="牙科" value="牙科"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="体温(℃)" prop="temperature">
              <el-input-number v-model="recordForm.temperature" :min="35" :max="45" :step="0.1"></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-divider content-position="left">诊断信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="主诉" prop="chiefComplaint">
              <el-input
                type="textarea"
                :rows="3"
                v-model="recordForm.chiefComplaint"
                placeholder="宠物主人描述的主要症状">
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="现病史" prop="presentIllness">
              <el-input
                type="textarea"
                :rows="3"
                v-model="recordForm.presentIllness"
                placeholder="当前疾病的详细情况">
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="既往病史" prop="pastHistory">
              <el-input
                type="textarea"
                :rows="3"
                v-model="recordForm.pastHistory"
                placeholder="过去的疾病史、手术史、过敏史等">
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="临床检查" prop="clinicalExamination">
              <el-input
                type="textarea"
                :rows="3"
                v-model="recordForm.clinicalExamination"
                placeholder="体格检查、实验室检查结果">
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="诊断结果" prop="diagnosis">
              <el-input
                type="textarea"
                :rows="3"
                v-model="recordForm.diagnosis"
                placeholder="最终诊断结论">
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="治疗方案" prop="treatmentPlan">
              <el-input
                type="textarea"
                :rows="3"
                v-model="recordForm.treatmentPlan"
                placeholder="具体治疗措施、用药方案">
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-divider content-position="left">医嘱信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="医嘱" prop="medicalAdvice">
              <el-input
                type="textarea"
                :rows="3"
                v-model="recordForm.medicalAdvice"
                placeholder="用药指导、护理建议、复查时间">
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="备注" prop="remarks">
              <el-input
                type="textarea"
                :rows="3"
                v-model="recordForm.remarks"
                placeholder="其他需要说明的信息">
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="下次复诊" prop="nextVisitDate">
              <el-date-picker
                v-model="recordForm.nextVisitDate"
                type="date"
                placeholder="选择复诊日期"
                style="width: 100%">
              </el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="费用(元)" prop="totalCost">
              <el-input-number v-model="recordForm.totalCost" :min="0" :max="99999" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="病历状态" prop="status">
              <el-radio-group v-model="recordForm.status">
                <el-radio label="待完成"></el-radio>
                <el-radio label="已完成"></el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row>
          <el-col :span="24" style="text-align: center;">
            <el-form-item>
              <el-button type="primary" size="large" @click="handleSubmit">保存病历</el-button>
              <el-button type="success" size="large" @click="handleSubmitAndPrint">保存并打印</el-button>
              <el-button size="large" @click="handleReset">重置</el-button>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'MedicalRecord',
  data() {
    return {
      recordForm: {
        recordNo: 'MR' + Date.now(),
        visitDate: '',
        visitType: '',
        petName: '',
        breed: '',
        ownerName: '',
        doctor: '',
        department: '',
        temperature: 38.5,
        chiefComplaint: '',
        presentIllness: '',
        pastHistory: '',
        clinicalExamination: '',
        diagnosis: '',
        treatmentPlan: '',
        medicalAdvice: '',
        remarks: '',
        nextVisitDate: '',
        totalCost: 0,
        status: '待完成'
      },
      rules: {
        visitDate: [
          { required: true, message: '请选择就诊日期', trigger: 'change' }
        ],
        visitType: [
          { required: true, message: '请选择就诊类型', trigger: 'change' }
        ],
        petName: [
          { required: true, message: '请输入宠物名称', trigger: 'blur' }
        ],
        ownerName: [
          { required: true, message: '请输入主人姓名', trigger: 'blur' }
        ],
        doctor: [
          { required: true, message: '请选择主治医师', trigger: 'change' }
        ],
        department: [
          { required: true, message: '请选择科室', trigger: 'change' }
        ],
        chiefComplaint: [
          { required: true, message: '请输入主诉', trigger: 'blur' }
        ],
        diagnosis: [
          { required: true, message: '请输入诊断结果', trigger: 'blur' }
        ],
        treatmentPlan: [
          { required: true, message: '请输入治疗方案', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    handleSubmit() {
      this.$refs.recordForm.validate((valid) => {
        if (valid) {
          this.$message.success('病历保存成功！')
        }
      })
    },
    handleSubmitAndPrint() {
      this.$refs.recordForm.validate((valid) => {
        if (valid) {
          this.$message.success('病历保存成功，即将打印...')
        }
      })
    },
    handleReset() {
      this.$refs.recordForm.resetFields()
      this.recordForm.recordNo = 'MR' + Date.now()
    }
  }
}
</script>

<style scoped>
</style>
