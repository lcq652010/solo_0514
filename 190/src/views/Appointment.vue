<template>
  <div class="page-container">
    <div class="page-title">宠物就诊预约</div>
    
    <el-card class="box-card">
      <el-form :model="appointmentForm" :rules="rules" ref="appointmentForm" label-width="120px">
        <el-divider content-position="left">宠物信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="宠物名称" prop="petName">
              <el-input v-model="appointmentForm.petName"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="宠物类型" prop="petType">
              <el-select v-model="appointmentForm.petType" style="width: 100%">
                <el-option label="狗" value="狗"></el-option>
                <el-option label="猫" value="猫"></el-option>
                <el-option label="鸟" value="鸟"></el-option>
                <el-option label="其他" value="其他"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="品种" prop="breed">
              <el-input v-model="appointmentForm.breed"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="性别" prop="petGender">
              <el-radio-group v-model="appointmentForm.petGender">
                <el-radio label="公"></el-radio>
                <el-radio label="母"></el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="年龄(岁)" prop="age">
              <el-input-number v-model="appointmentForm.age" :min="0" :max="30"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="体重(kg)" prop="weight">
              <el-input-number v-model="appointmentForm.weight" :min="0" :max="100" :step="0.1"></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-divider content-position="left">主人信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="主人姓名" prop="ownerName">
              <el-input v-model="appointmentForm.ownerName"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="appointmentForm.phone"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="备用电话" prop="backupPhone">
              <el-input v-model="appointmentForm.backupPhone"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-divider content-position="left">预约信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="预约日期" prop="appointmentDate">
              <el-date-picker
                v-model="appointmentForm.appointmentDate"
                type="date"
                placeholder="选择日期"
                style="width: 100%">
              </el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="预约时段" prop="timeSlot">
              <el-select v-model="appointmentForm.timeSlot" style="width: 100%">
                <el-option 
                  v-for="slot in timeSlots" 
                  :key="slot.value" 
                  :label="slot.label" 
                  :value="slot.value"
                  :disabled="slot.disabled">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="就诊科室" prop="department">
              <el-select v-model="appointmentForm.department" style="width: 100%">
                <el-option label="内科" value="内科"></el-option>
                <el-option label="外科" value="外科"></el-option>
                <el-option label="皮肤科" value="皮肤科"></el-option>
                <el-option label="眼科" value="眼科"></el-option>
                <el-option label="牙科" value="牙科"></el-option>
                <el-option label="疫苗接种" value="疫苗接种"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="选择医师" prop="doctor">
              <el-select v-model="appointmentForm.doctor" style="width: 100%">
                <el-option label="张医生" value="张医生"></el-option>
                <el-option label="李医生" value="李医生"></el-option>
                <el-option label="王医生" value="王医生"></el-option>
                <el-option label="赵医生" value="赵医生"></el-option>
                <el-option label="刘医生" value="刘医生"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="16">
            <el-form-item label="症状描述" prop="symptoms">
              <el-input
                type="textarea"
                :rows="3"
                v-model="appointmentForm.symptoms"
                placeholder="请详细描述宠物的症状情况">
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row>
          <el-col :span="24" style="text-align: center;">
            <el-form-item>
              <el-button type="primary" size="large" @click="handleSubmit">提交预约</el-button>
              <el-button size="large" @click="handleReset">重置表单</el-button>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import dataStore from '@/store/dataStore.js'

export default {
  name: 'Appointment',
  data() {
    const validatePhone = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入联系电话'))
      } else if (!/^1[3-9]\d{9}$/.test(value)) {
        callback(new Error('请输入正确的手机号码'))
      } else {
        callback()
      }
    }
    
    return {
      appointmentForm: {
        petName: '',
        petType: '',
        breed: '',
        petGender: '公',
        age: 1,
        weight: 5,
        ownerName: '',
        phone: '',
        backupPhone: '',
        appointmentDate: '',
        timeSlot: '',
        department: '',
        doctor: '',
        symptoms: ''
      },
      rules: {
        petName: [
          { required: true, message: '请输入宠物名称', trigger: 'blur' }
        ],
        petType: [
          { required: true, message: '请选择宠物类型', trigger: 'change' }
        ],
        breed: [
          { required: true, message: '请输入宠物品种', trigger: 'blur' }
        ],
        ownerName: [
          { required: true, message: '请输入主人姓名', trigger: 'blur' }
        ],
        phone: [
          { required: true, validator: validatePhone, trigger: 'blur' }
        ],
        appointmentDate: [
          { required: true, message: '请选择预约日期', trigger: 'change' }
        ],
        timeSlot: [
          { required: true, message: '请选择预约时段', trigger: 'change' }
        ],
        department: [
          { required: true, message: '请选择就诊科室', trigger: 'change' }
        ],
        doctor: [
          { required: true, message: '请选择医师', trigger: 'change' }
        ],
        symptoms: [
          { required: true, message: '请描述症状', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    timeSlots() {
      const allSlots = [
        { label: '08:00-09:00', value: '08:00-09:00' },
        { label: '09:00-10:00', value: '09:00-10:00' },
        { label: '10:00-11:00', value: '10:00-11:00' },
        { label: '11:00-12:00', value: '11:00-12:00' },
        { label: '14:00-15:00', value: '14:00-15:00' },
        { label: '15:00-16:00', value: '15:00-16:00' },
        { label: '16:00-17:00', value: '16:00-17:00' },
        { label: '17:00-18:00', value: '17:00-18:00' }
      ]
      
      if (this.appointmentForm.doctor && this.appointmentForm.appointmentDate) {
        const formattedDate = this.formatDate(this.appointmentForm.appointmentDate)
        const bookedSlots = dataStore.getBookedSlots(this.appointmentForm.doctor, formattedDate)
        
        return allSlots.map(slot => ({
          ...slot,
          disabled: bookedSlots.includes(slot.value)
        }))
      }
      
      return allSlots
    }
  },
  watch: {
    'appointmentForm.doctor': function() {
      this.appointmentForm.timeSlot = ''
    },
    'appointmentForm.appointmentDate': function() {
      this.appointmentForm.timeSlot = ''
    }
  },
  methods: {
    formatDate(date) {
      if (!date) return ''
      if (typeof date === 'string') return date
      const d = new Date(date)
      const year = d.getFullYear()
      const month = String(d.getMonth() + 1).padStart(2, '0')
      const day = String(d.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    },
    checkDuplicatePet() {
      const { petName, ownerName, phone } = this.appointmentForm
      const petRecords = dataStore.getPets()
      return petRecords.some(pet => 
        pet.petName === petName && 
        pet.ownerName === ownerName && 
        pet.phone === phone
      )
    },
    handleSubmit() {
      this.$refs.appointmentForm.validate((valid) => {
        if (valid) {
          if (this.checkDuplicatePet()) {
            this.$confirm('该宠物档案已存在，是否继续预约？', '提示', {
              confirmButtonText: '继续预约',
              cancelButtonText: '取消',
              type: 'warning'
            }).then(() => {
              this.submitAppointment()
            }).catch(() => {})
          } else {
            this.submitAppointment()
          }
        }
      })
    },
    submitAppointment() {
      const formattedDate = this.formatDate(this.appointmentForm.appointmentDate)
      const appointmentNo = 'AP' + Date.now()
      
      const newAppointment = {
        appointmentNo: appointmentNo,
        ...this.appointmentForm,
        appointmentDate: formattedDate,
        status: '待就诊'
      }
      
      dataStore.addAppointment(newAppointment)
      
      if (!this.checkDuplicatePet()) {
        dataStore.addPet({
          petName: this.appointmentForm.petName,
          petType: this.appointmentForm.petType,
          breed: this.appointmentForm.breed,
          ownerName: this.appointmentForm.ownerName,
          phone: this.appointmentForm.phone
        })
      }
      
      this.$alert(`预约成功！预约号：${appointmentNo}`, '提示', {
        confirmButtonText: '确定',
        callback: action => {
          this.handleReset()
        }
      })
    },
    handleReset() {
      this.$refs.appointmentForm.resetFields()
    }
  }
}
</script>

<style scoped>
</style>
