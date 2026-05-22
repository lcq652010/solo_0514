<template>
  <div class="page-container">
    <div class="page-title">车主预约表单</div>
    
    <div class="form-container">
      <el-form
        ref="appointmentForm"
        :model="formData"
        :rules="formRules"
        label-width="120px"
        class="appointment-form"
      >
        <el-form-item label="选择套餐" prop="packageId">
          <el-select v-model="formData.packageId" placeholder="请选择保养套餐" style="width: 100%">
            <el-option
              v-for="pkg in packageList"
              :key="pkg.id"
              :label="pkg.name"
              :value="pkg.id"
            ></el-option>
          </el-select>
        </el-form-item>

        <el-divider content-position="left">车主信息</el-divider>

        <el-form-item label="车主姓名" prop="ownerName">
          <el-input v-model="formData.ownerName" placeholder="请输入车主姓名"></el-input>
        </el-form-item>

        <el-form-item label="联系电话" prop="phone">
          <el-input
            v-model="formData.phone"
            placeholder="请输入联系电话"
            maxlength="11"
            @input="validatePhoneRealTime"
            :status-icon="phoneStatus !== ''"
          >
            <template slot="append">
              <span v-if="phoneStatus === 'valid'" style="color: #67c23a;">
                <i class="el-icon-circle-check"></i> 格式正确
              </span>
              <span v-else-if="phoneStatus === 'invalid'" style="color: #f56c6c;">
                <i class="el-icon-circle-close"></i> 格式错误
              </span>
              <span v-else style="color: #909399;">
                <i class="el-icon-info"></i> 请输入11位手机号
              </span>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item label="车牌号" prop="plateNumber">
          <el-input v-model="formData.plateNumber" placeholder="请输入车牌号，如：京A88888"></el-input>
        </el-form-item>

        <el-form-item label="车辆品牌" prop="carBrand">
          <el-select v-model="formData.carBrand" placeholder="请选择车辆品牌" style="width: 100%">
            <el-option label="奥迪" value="奥迪"></el-option>
            <el-option label="宝马" value="宝马"></el-option>
            <el-option label="奔驰" value="奔驰"></el-option>
            <el-option label="大众" value="大众"></el-option>
            <el-option label="丰田" value="丰田"></el-option>
            <el-option label="本田" value="本田"></el-option>
            <el-option label="其他" value="其他"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="车辆型号" prop="carModel">
          <el-input v-model="formData.carModel" placeholder="请输入车辆型号"></el-input>
        </el-form-item>

        <el-divider content-position="left">预约信息</el-divider>

        <el-form-item label="预约日期" prop="appointmentDate">
          <el-date-picker
            v-model="formData.appointmentDate"
            type="date"
            placeholder="选择预约日期"
            style="width: 100%"
            :picker-options="pickerOptions"
          ></el-date-picker>
        </el-form-item>

        <el-form-item label="预约时段" prop="appointmentTime">
          <el-select v-model="formData.appointmentTime" placeholder="请选择预约时段" style="width: 100%">
            <el-option
              v-for="slot in timeSlots"
              :key="slot.value"
              :label="slot.label"
              :value="slot.value"
              :disabled="slot.disabled"
            >
              <span>{{ slot.label }}</span>
              <span v-if="slot.disabled" style="color: #f56c6c; margin-left: 10px; font-size: 12px;">(已被预约)</span>
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="选择技师" prop="technicianId">
          <el-select v-model="formData.technicianId" placeholder="请选择技师" style="width: 100%">
            <el-option
              v-for="tech in technicianList"
              :key="tech.id"
              :label="tech.name + ' - ' + tech.level"
              :value="tech.id"
            ></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="备注信息" prop="remark">
          <el-input
            v-model="formData.remark"
            type="textarea"
            :rows="4"
            placeholder="请输入备注信息（选填）"
          ></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="submitLoading">提交预约</el-button>
          <el-button @click="handleReset">重置表单</el-button>
          <el-button @click="$router.back()">返回</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Appointment',
  data() {
    const validatePhone = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入联系电话'))
      } else if (!/^1[3-9]\d{9}$/.test(value)) {
        callback(new Error('请输入正确的11位手机号码'))
      } else {
        callback()
      }
    }

    const validatePlateNumber = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入车牌号'))
      } else if (!/^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领][A-Z][A-Z0-9]{4,5}[A-Z0-9挂学警港澳]$/.test(value)) {
        callback(new Error('请输入正确的车牌号'))
      } else {
        callback()
      }
    }

    return {
      formData: {
        packageId: '',
        ownerName: '',
        phone: '',
        plateNumber: '',
        carBrand: '',
        carModel: '',
        appointmentDate: '',
        appointmentTime: '',
        technicianId: '',
        remark: ''
      },
      formRules: {
        packageId: [
          { required: true, message: '请选择保养套餐', trigger: 'change' }
        ],
        ownerName: [
          { required: true, message: '请输入车主姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        phone: [
          { validator: validatePhone, trigger: 'blur' }
        ],
        plateNumber: [
          { validator: validatePlateNumber, trigger: 'blur' }
        ],
        carBrand: [
          { required: true, message: '请选择车辆品牌', trigger: 'change' }
        ],
        carModel: [
          { required: true, message: '请输入车辆型号', trigger: 'blur' }
        ],
        appointmentDate: [
          { required: true, message: '请选择预约日期', trigger: 'change' }
        ],
        appointmentTime: [
          { required: true, message: '请选择预约时段', trigger: 'change' }
        ],
        technicianId: [
          { required: true, message: '请选择技师', trigger: 'change' }
        ]
      },
      packageList: [],
      technicianList: [],
      submitLoading: false,
      pickerOptions: {
        disabledDate(time) {
          return time.getTime() < Date.now() - 8.64e7
        }
      },
      existingAppointments: [],
      timeSlots: [
        { label: '09:00 - 10:00', value: '09:00 - 10:00', disabled: false },
        { label: '10:00 - 11:00', value: '10:00 - 11:00', disabled: false },
        { label: '11:00 - 12:00', value: '11:00 - 12:00', disabled: false },
        { label: '14:00 - 15:00', value: '14:00 - 15:00', disabled: false },
        { label: '15:00 - 16:00', value: '15:00 - 16:00', disabled: false },
        { label: '16:00 - 17:00', value: '16:00 - 17:00', disabled: false }
      ],
      phoneStatus: ''
    }
  },
  created() {
    this.loadPackageList()
    this.loadTechnicianList()
    this.loadExistingAppointments()
    
    if (this.$route.query.packageId) {
      this.formData.packageId = parseInt(this.$route.query.packageId)
    }
  },
  watch: {
    'formData.technicianId': function() {
      this.updateTimeSlotsAvailability()
    },
    'formData.appointmentDate': function() {
      this.updateTimeSlotsAvailability()
    }
  },
  methods: {
    validatePhoneRealTime() {
      if (!this.formData.phone) {
        this.phoneStatus = ''
        return
      }
      if (/^1[3-9]\d{9}$/.test(this.formData.phone)) {
        this.phoneStatus = 'valid'
      } else {
        this.phoneStatus = 'invalid'
      }
    },
    loadPackageList() {
      this.packageList = [
        { id: 1, name: '基础保养套餐 - ¥299' },
        { id: 2, name: '常规保养套餐 - ¥499' },
        { id: 3, name: '深度保养套餐A - ¥899' },
        { id: 4, name: '深度保养套餐B - ¥1299' },
        { id: 5, name: '豪华保养套餐 - ¥1999' },
        { id: 6, name: 'VIP尊享套餐 - ¥2999' }
      ]
    },
    loadTechnicianList() {
      this.technicianList = [
        { id: 1, name: '张师傅', level: '高级技师' },
        { id: 2, name: '李师傅', level: '高级技师' },
        { id: 3, name: '王师傅', level: '中级技师' },
        { id: 4, name: '赵师傅', level: '中级技师' },
        { id: 5, name: '刘师傅', level: '初级技师' }
      ]
    },
    loadExistingAppointments() {
      const today = new Date()
      const tomorrow = new Date(today)
      tomorrow.setDate(tomorrow.getDate() + 1)
      const dayAfter = new Date(today)
      dayAfter.setDate(dayAfter.getDate() + 2)
      
      const formatDate = (date) => {
        const year = date.getFullYear()
        const month = String(date.getMonth() + 1).padStart(2, '0')
        const day = String(date.getDate()).padStart(2, '0')
        return `${year}-${month}-${day}`
      }

      this.existingAppointments = [
        { technicianId: 1, date: formatDate(tomorrow), time: '09:00 - 10:00', customer: '陈先生' },
        { technicianId: 1, date: formatDate(tomorrow), time: '14:00 - 15:00', customer: '林女士' },
        { technicianId: 2, date: formatDate(tomorrow), time: '10:00 - 11:00', customer: '吴先生' },
        { technicianId: 2, date: formatDate(dayAfter), time: '09:00 - 10:00', customer: '郑女士' },
        { technicianId: 3, date: formatDate(tomorrow), time: '14:00 - 15:00', customer: '黄先生' },
        { technicianId: 3, date: formatDate(tomorrow), time: '15:00 - 16:00', customer: '张先生' },
        { technicianId: 4, date: formatDate(dayAfter), time: '10:00 - 11:00', customer: '王先生' },
        { technicianId: 5, date: formatDate(tomorrow), time: '09:00 - 10:00', customer: '赵先生' },
        { technicianId: 5, date: formatDate(dayAfter), time: '14:00 - 15:00', customer: '刘女士' }
      ]
    },
    updateTimeSlotsAvailability() {
      if (!this.formData.technicianId || !this.formData.appointmentDate) {
        this.timeSlots.forEach(slot => slot.disabled = false)
        return
      }

      const selectedDate = this.formatDate(this.formData.appointmentDate)
      
      this.timeSlots.forEach(slot => {
        const hasConflict = this.existingAppointments.some(apt => 
          apt.technicianId === this.formData.technicianId &&
          apt.date === selectedDate &&
          apt.time === slot.value
        )
        slot.disabled = hasConflict
      })

      if (this.formData.appointmentTime) {
        const currentSlot = this.timeSlots.find(slot => slot.value === this.formData.appointmentTime)
        if (currentSlot && currentSlot.disabled) {
          this.$message.warning('该时段已被预约，请选择其他时段')
          this.formData.appointmentTime = ''
        }
      }
    },
    formatDate(date) {
      if (!date) return ''
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    },
    checkTimeConflict() {
      if (!this.formData.technicianId || !this.formData.appointmentDate || !this.formData.appointmentTime) {
        return false
      }

      const selectedDate = this.formatDate(this.formData.appointmentDate)
      
      const hasConflict = this.existingAppointments.some(apt => 
        apt.technicianId === this.formData.technicianId &&
        apt.date === selectedDate &&
        apt.time === this.formData.appointmentTime
      )

      if (hasConflict) {
        const tech = this.technicianList.find(t => t.id === this.formData.technicianId)
        this.$message.error(`该时段已被预约，${tech ? tech.name : '技师'}在${this.formData.appointmentTime}已有安排`)
        return true
      }

      return false
    },
    handleSubmit() {
      this.$refs.appointmentForm.validate((valid) => {
        if (valid) {
          if (this.checkTimeConflict()) {
            return false
          }
          
          this.submitLoading = true
          setTimeout(() => {
            this.submitLoading = false
            
            const newRecord = {
              id: Date.now(),
              orderNo: 'YY' + Date.now().toString().slice(-10),
              customerName: this.formData.ownerName,
              phone: this.formData.phone,
              plateNumber: this.formData.plateNumber,
              carInfo: this.formData.carBrand + ' ' + this.formData.carModel,
              packageName: this.packageList.find(p => p.id === this.formData.packageId)?.name || '',
              technicianName: this.technicianList.find(t => t.id === this.formData.technicianId)?.name || '',
              appointmentDate: this.formatDate(this.formData.appointmentDate),
              appointmentTime: this.formData.appointmentTime,
              status: '待确认',
              createTime: new Date().toLocaleString('zh-CN', { hour12: false }).replace(/\//g, '-'),
              remark: this.formData.remark
            }
            
            let records = JSON.parse(localStorage.getItem('appointmentRecords') || '[]')
            records.unshift(newRecord)
            localStorage.setItem('appointmentRecords', JSON.stringify(records))
            localStorage.setItem('needRefreshRecords', 'true')
            
            this.$message.success('预约提交成功！')
            this.$router.push('/records')
          }, 1000)
        } else {
          this.$message.error('请检查表单填写是否正确')
          return false
        }
      })
    },
    handleReset() {
      this.$refs.appointmentForm.resetFields()
      this.timeSlots.forEach(slot => slot.disabled = false)
      this.phoneStatus = ''
    }
  }
}
</script>

<style scoped>
.appointment-form {
  padding: 20px 0;
}
</style>
