<template>
  <div class="appointment-form">
    <div class="page-title">宠物预约表单</div>
    <div class="card-wrapper">
      <el-form :model="formData" :rules="rules" ref="formData" label-width="120px" size="medium">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="宠物主人姓名" prop="ownerName">
              <el-input v-model="formData.ownerName" placeholder="请输入宠物主人姓名"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="formData.phone" placeholder="请输入联系电话"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="宠物名称" prop="petName">
              <el-input v-model="formData.petName" placeholder="请输入宠物名称"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="宠物类型" prop="petType">
              <el-select v-model="formData.petType" placeholder="请选择宠物类型" style="width: 100%;">
                <el-option label="小型犬" value="小型犬"></el-option>
                <el-option label="中型犬" value="中型犬"></el-option>
                <el-option label="大型犬" value="大型犬"></el-option>
                <el-option label="猫咪" value="猫咪"></el-option>
                <el-option label="其他" value="其他"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="宠物性别" prop="petGender">
              <el-radio-group v-model="formData.petGender">
                <el-radio label="公">公</el-radio>
                <el-radio label="母">母</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="宠物体重(kg)" prop="petWeight">
              <el-input-number v-model="formData.petWeight" :min="0" :step="0.5" style="width: 100%;"></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="美容师" prop="beautician">
              <el-select v-model="formData.beautician" placeholder="请选择美容师" style="width: 100%;" @change="onBeauticianChange">
                <el-option v-for="item in beauticianList" :key="item.id" :label="item.name" :value="item.id"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="预约日期" prop="appointmentDate">
              <el-date-picker
                v-model="formData.appointmentDate"
                type="date"
                placeholder="选择预约日期"
                style="width: 100%;"
                :picker-options="datePickerOptions"
                @change="onDateChange"
              ></el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="预约时段" prop="appointmentTime">
              <el-select v-model="formData.appointmentTime" placeholder="请选择预约时段" style="width: 100%;">
                <el-option 
                  v-for="item in timeSlots" 
                  :key="item.value" 
                  :label="item.label" 
                  :value="item.value"
                  :disabled="item.disabled"
                ></el-option>
              </el-select>
              <div v-if="conflictHint" style="color: #E6A23C; font-size: 12px; margin-top: 5px;">
                <i class="el-icon-warning"></i> {{ conflictHint }}
              </div>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="服务套餐" prop="servicePackage">
          <el-checkbox-group v-model="formData.servicePackage">
            <el-checkbox label="基础洗护套餐"></el-checkbox>
            <el-checkbox label="精致洗护套餐"></el-checkbox>
            <el-checkbox label="豪华美容套餐"></el-checkbox>
            <el-checkbox label="医疗洗护套餐"></el-checkbox>
            <el-checkbox label="猫咪专属套餐"></el-checkbox>
            <el-checkbox label="大型犬洗护"></el-checkbox>
          </el-checkbox-group>
        </el-form-item>

        <el-form-item label="特殊要求" prop="specialRequirements">
          <el-input
            type="textarea"
            v-model="formData.specialRequirements"
            placeholder="请输入特殊要求，如：宠物胆小、需要特定香波等"
            :rows="4"
          ></el-input>
        </el-form-item>

        <el-form-item label="是否会员" prop="isMember">
          <el-switch v-model="formData.isMember" active-text="是" inactive-text="否"></el-switch>
          <el-input
            v-if="formData.isMember"
            v-model="formData.memberCardNo"
            placeholder="请输入会员卡号"
            style="width: 200px; margin-left: 20px;"
          ></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit">提交预约</el-button>
          <el-button @click="handleReset">重置表单</el-button>
          <el-button type="success" @click="goToList">查看预约记录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AppointmentForm',
  data() {
    const validatePhone = (rule, value, callback) => {
      const phoneReg = /^1[3-9]\d{9}$/
      if (!value) {
        callback(new Error('请输入联系电话'))
      } else if (!phoneReg.test(value)) {
        callback(new Error('请输入正确的手机号码'))
      } else {
        callback()
      }
    }

    return {
      conflictHint: '',
      beauticianList: [
        { id: 1, name: '张美容师' },
        { id: 2, name: '李美容师' },
        { id: 3, name: '王美容师' },
        { id: 4, name: '赵美容师' }
      ],
      allTimeSlots: [
        { label: '09:00-10:00', value: '09:00-10:00' },
        { label: '10:00-11:00', value: '10:00-11:00' },
        { label: '11:00-12:00', value: '11:00-12:00' },
        { label: '14:00-15:00', value: '14:00-15:00' },
        { label: '15:00-16:00', value: '15:00-16:00' },
        { label: '16:00-17:00', value: '16:00-17:00' }
      ],
      datePickerOptions: {
        disabledDate(time) {
          return time.getTime() < Date.now() - 8.64e7
        }
      },
      formData: {
        ownerName: '',
        phone: '',
        petName: '',
        petType: '',
        petGender: '',
        petWeight: 0,
        beautician: '',
        appointmentDate: '',
        appointmentTime: '',
        servicePackage: [],
        specialRequirements: '',
        isMember: false,
        memberCardNo: ''
      },
      rules: {
        ownerName: [
          { required: true, message: '请输入宠物主人姓名', trigger: 'blur' }
        ],
        phone: [
          { required: true, validator: validatePhone, trigger: 'blur' }
        ],
        petName: [
          { required: true, message: '请输入宠物名称', trigger: 'blur' }
        ],
        petType: [
          { required: true, message: '请选择宠物类型', trigger: 'change' }
        ],
        petGender: [
          { required: true, message: '请选择宠物性别', trigger: 'change' }
        ],
        beautician: [
          { required: true, message: '请选择美容师', trigger: 'change' }
        ],
        appointmentDate: [
          { required: true, message: '请选择预约日期', trigger: 'change' }
        ],
        appointmentTime: [
          { required: true, message: '请选择预约时段', trigger: 'change' }
        ],
        servicePackage: [
          { type: 'array', required: true, message: '请选择服务套餐', trigger: 'change' }
        ]
      }
    }
  },
  computed: {
    timeSlots() {
      if (!this.formData.beautician || !this.formData.appointmentDate) {
        return this.allTimeSlots.map(slot => ({ ...slot, disabled: false }))
      }
      
      const appointments = JSON.parse(localStorage.getItem('appointments') || '[]')
      const dateStr = this.formatDate(this.formData.appointmentDate)
      
      const busySlots = appointments
        .filter(a => 
          a.beautician === this.formData.beautician && 
          a.appointmentDate === dateStr &&
          a.status !== '已取消'
        )
        .map(a => a.appointmentTime)
      
      return this.allTimeSlots.map(slot => ({
        ...slot,
        disabled: busySlots.includes(slot.value)
      }))
    }
  },
  methods: {
    formatDate(date) {
      if (!date) return ''
      const d = new Date(date)
      const year = d.getFullYear()
      const month = String(d.getMonth() + 1).padStart(2, '0')
      const day = String(d.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    },
    onBeauticianChange() {
      this.checkTimeSlotConflict()
      if (this.formData.appointmentTime) {
        const slot = this.timeSlots.find(s => s.value === this.formData.appointmentTime)
        if (slot && slot.disabled) {
          this.formData.appointmentTime = ''
        }
      }
    },
    onDateChange() {
      this.checkTimeSlotConflict()
      if (this.formData.appointmentTime) {
        const slot = this.timeSlots.find(s => s.value === this.formData.appointmentTime)
        if (slot && slot.disabled) {
          this.formData.appointmentTime = ''
        }
      }
    },
    checkTimeSlotConflict() {
      if (!this.formData.beautician || !this.formData.appointmentDate) {
        this.conflictHint = ''
        return
      }
      
      const appointments = JSON.parse(localStorage.getItem('appointments') || '[]')
      const dateStr = this.formatDate(this.formData.appointmentDate)
      const beauticianName = this.beauticianList.find(b => b.id === this.formData.beautician)?.name || ''
      
      const busySlots = appointments
        .filter(a => 
          a.beautician === this.formData.beautician && 
          a.appointmentDate === dateStr &&
          a.status !== '已取消'
        )
        .map(a => a.appointmentTime)
      
      if (busySlots.length > 0) {
        this.conflictHint = `${beauticianName}在${dateStr}已预约时段：${busySlots.join('、')}`
      } else {
        this.conflictHint = ''
      }
    },
    handleSubmit() {
      this.$refs.formData.validate((valid) => {
        if (valid) {
          const dateStr = this.formatDate(this.formData.appointmentDate)
          const appointment = {
            id: Date.now(),
            ...this.formData,
            appointmentDate: dateStr,
            beauticianName: this.beauticianList.find(b => b.id === this.formData.beautician)?.name || '',
            status: '待服务',
            createTime: new Date().toLocaleString()
          }
          let appointments = JSON.parse(localStorage.getItem('appointments') || '[]')
          appointments.unshift(appointment)
          localStorage.setItem('appointments', JSON.stringify(appointments))
          
          this.$message.success('预约成功！')
          this.$confirm('是否跳转至预约记录列表？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '继续预约',
            type: 'success'
          }).then(() => {
            this.$router.push('/appointments')
          }).catch(() => {
            this.handleReset()
          })
        }
      })
    },
    handleReset() {
      this.$refs.formData.resetFields()
      this.conflictHint = ''
    },
    goToList() {
      this.$router.push('/appointments')
    }
  }
}
</script>

<style scoped>
.el-checkbox {
  margin-right: 20px;
  margin-bottom: 10px;
}
</style>
