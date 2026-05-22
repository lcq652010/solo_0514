<template>
  <div class="appointment">
    <el-card>
      <div slot="header" class="card-header">
        <span>在线预约</span>
      </div>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
        class="appointment-form"
      >
        <el-form-item label="选择套餐" prop="packageId">
          <el-select v-model="form.packageId" placeholder="请选择体检套餐" style="width: 100%">
            <el-option
              v-for="item in packageList"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            >
              <span>{{ item.name }}</span>
              <span style="float: right; color: #f56c6c; font-weight: bold">
                ¥{{ item.currentPrice }}
              </span>
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="预约日期" prop="appointmentDate">
          <el-date-picker
            v-model="form.appointmentDate"
            type="date"
            placeholder="选择预约日期"
            style="width: 100%"
            :picker-options="datePickerOptions"
          ></el-date-picker>
        </el-form-item>

        <el-form-item label="预约时段" prop="appointmentTime">
          <el-radio-group v-model="form.appointmentTime">
            <el-radio 
              v-for="slot in timeSlots" 
              :key="slot.value" 
              :label="slot.value" 
              :disabled="slot.full"
            >
              {{ slot.label }}
              <span v-if="slot.full" style="color: #f56c6c; margin-left: 8px;">(已满)</span>
              <span v-else style="color: #67c23a; margin-left: 8px;">(剩余{{ slot.remaining }}个名额)</span>
            </el-radio>
          </el-radio-group>
        </el-form-item>

        <el-divider content-position="left">预约人信息</el-divider>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="form.name" placeholder="请输入姓名"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-radio-group v-model="form.gender">
                <el-radio label="male">男</el-radio>
                <el-radio label="female">女</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="手机号码" prop="phone">
              <el-input v-model="form.phone" placeholder="请输入手机号码"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="身份证号" prop="idCard">
              <el-input v-model="form.idCard" placeholder="请输入身份证号"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="年龄" prop="age">
              <el-input-number
                v-model="form.age"
                :min="1"
                :max="120"
                style="width: 100%"
              ></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="婚姻状况" prop="maritalStatus">
              <el-select v-model="form.maritalStatus" placeholder="请选择" style="width: 100%">
                <el-option label="未婚" value="unmarried"></el-option>
                <el-option label="已婚" value="married"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="备注" prop="remark">
          <el-input
            v-model="form.remark"
            type="textarea"
            :rows="4"
            placeholder="请输入备注信息（选填）"
          ></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" size="large" @click="handleSubmit">
            提交预约
          </el-button>
          <el-button size="large" @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'Appointment',
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

    const validateIdCard = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入身份证号'))
      } else if (!/^\d{17}[\dXx]$/.test(value)) {
        callback(new Error('请输入正确的身份证号格式'))
      } else {
        callback()
      }
    }

    return {
      form: {
        packageId: null,
        appointmentDate: '',
        appointmentTime: 'morning',
        name: '',
        gender: 'male',
        phone: '',
        idCard: '',
        age: null,
        maritalStatus: '',
        remark: ''
      },
      rules: {
        packageId: [
          { required: true, message: '请选择体检套餐', trigger: 'change' }
        ],
        appointmentDate: [
          { required: true, message: '请选择预约日期', trigger: 'change' }
        ],
        appointmentTime: [
          { required: true, message: '请选择预约时段', trigger: 'change' }
        ],
        name: [
          { required: true, message: '请输入姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '姓名长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        gender: [
          { required: true, message: '请选择性别', trigger: 'change' }
        ],
        phone: [
          { validator: validatePhone, trigger: 'blur' }
        ],
        idCard: [
          { validator: validateIdCard, trigger: 'blur' }
        ],
        age: [
          { required: true, message: '请输入年龄', trigger: 'blur' },
          { type: 'number', min: 1, max: 120, message: '年龄必须在 1 到 120 之间', trigger: 'blur' }
        ],
        maritalStatus: [
          { required: true, message: '请选择婚姻状况', trigger: 'change' }
        ]
      },
      datePickerOptions: {
        disabledDate(time) {
          return time.getTime() < Date.now() - 8.64e7
        }
      },
      packageList: [
        { id: 1, name: '入职基础体检套餐', currentPrice: 199 },
        { id: 2, name: '青年常规体检套餐', currentPrice: 399 },
        { id: 3, name: '精英尊享体检套餐', currentPrice: 1599 },
        { id: 4, name: '女性专属体检套餐', currentPrice: 699 },
        { id: 5, name: '中年全面体检套餐', currentPrice: 999 },
        { id: 6, name: '老年关爱体检套餐', currentPrice: 1299 }
      ],
      timeSlots: [
        { value: 'morning', label: '上午 (8:00-12:00)', full: false, remaining: 20, max: 20 },
        { value: 'afternoon', label: '下午 (14:00-17:00)', full: false, remaining: 15, max: 15 }
      ],
      maxSlotsPerDay: {
        morning: 20,
        afternoon: 15
      },
      appointments: []
    }
  },
  mounted() {
    if (this.$route.query.packageId) {
      this.form.packageId = parseInt(this.$route.query.packageId)
    }
    this.initMockAppointments()
  },
  watch: {
    'form.appointmentDate'(newDate) {
      if (newDate) {
        this.updateTimeSlotStatus()
      }
    }
  },
  methods: {
    initMockAppointments() {
      const today = new Date()
      const tomorrow = new Date(today)
      tomorrow.setDate(tomorrow.getDate() + 1)
      const dayAfter = new Date(today)
      dayAfter.setDate(dayAfter.getDate() + 2)

      this.appointments = [
        { date: this.formatDate(tomorrow), time: 'morning', count: 20 },
        { date: this.formatDate(tomorrow), time: 'afternoon', count: 8 },
        { date: this.formatDate(dayAfter), time: 'morning', count: 5 },
        { date: this.formatDate(dayAfter), time: 'afternoon', count: 15 }
      ]
    },
    formatDate(date) {
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    },
    updateTimeSlotStatus() {
      const selectedDate = this.formatDate(new Date(this.form.appointmentDate))
      
      this.timeSlots.forEach(slot => {
        const appointment = this.appointments.find(
          a => a.date === selectedDate && a.time === slot.value
        )
        const bookedCount = appointment ? appointment.count : 0
        slot.remaining = slot.max - bookedCount
        slot.full = slot.remaining <= 0
      })

      if (this.timeSlots.find(s => s.value === this.form.appointmentTime)?.full) {
        const availableSlot = this.timeSlots.find(s => !s.full)
        this.form.appointmentTime = availableSlot ? availableSlot.value : ''
      }
    },
    handleSubmit() {
      this.$refs.formRef.validate((valid) => {
        if (valid) {
          const selectedDate = this.formatDate(new Date(this.form.appointmentDate))
          const selectedSlot = this.timeSlots.find(s => s.value === this.form.appointmentTime)
          
          if (selectedSlot && selectedSlot.full) {
            this.$message.error('所选时段已约满，请选择其他时段')
            return
          }

          const existingAppointment = this.appointments.find(
            a => a.date === selectedDate && a.time === this.form.appointmentTime
          )
          
          if (existingAppointment) {
            existingAppointment.count++
          } else {
            this.appointments.push({
              date: selectedDate,
              time: this.form.appointmentTime,
              count: 1
            })
          }

          this.updateTimeSlotStatus()
          this.$message.success('预约提交成功！')
          console.log('预约信息:', this.form)
          
          setTimeout(() => {
            this.$router.push({
              path: '/records',
              query: { refresh: 'true', t: Date.now() }
            })
          }, 1500)
        } else {
          this.$message.error('请检查表单填写是否正确')
          return false
        }
      })
    },
    handleReset() {
      this.$refs.formRef.resetFields()
    }
  }
}
</script>

<style scoped>
.appointment {
  padding: 0;
}

.card-header {
  font-size: 18px;
  font-weight: bold;
}

.appointment-form {
  max-width: 800px;
}
</style>
