<template>
  <div class="booking">
    <div class="page-title">私教预约</div>
    <el-card>
      <el-form :model="form" :rules="rules" ref="form" label-width="120px" style="max-width: 600px; margin: 0 auto;">
        <el-form-item label="选择教练" prop="trainerId">
          <el-select v-model="form.trainerId" placeholder="请选择教练" style="width: 100%;">
            <el-option v-for="trainer in trainers" :key="trainer.id" :label="trainer.name" :value="trainer.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="会员姓名" prop="memberName">
          <el-input v-model="form.memberName" placeholder="请输入会员姓名"></el-input>
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入联系电话"></el-input>
        </el-form-item>
        <el-form-item label="预约日期" prop="date">
          <el-date-picker v-model="form.date" type="date" placeholder="选择日期" style="width: 100%;"></el-date-picker>
        </el-form-item>
        <el-form-item label="预约时段" prop="timeSlot">
          <el-select v-model="form.timeSlot" placeholder="请选择时段" style="width: 100%;">
            <el-option 
              v-for="slot in timeSlots" 
              :key="slot.value" 
              :label="slot.label" 
              :value="slot.value"
              :disabled="isTimeSlotDisabled(slot.value)">
              <span>{{ slot.label }}</span>
              <span v-if="isTimeSlotDisabled(slot.value)" style="color: #f56c6c; margin-left: 10px;">(已预约)</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="课时数量" prop="hours">
          <el-input-number v-model="form.hours" :min="1" :max="10"></el-input-number>
          <span style="margin-left: 10px; color: #909399;">课时</span>
        </el-form-item>
        <el-form-item label="备注">
          <el-input type="textarea" v-model="form.remark" :rows="3" placeholder="请输入备注信息"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm">提交预约</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'Booking',
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
      form: {
        trainerId: '',
        memberName: '',
        phone: '',
        date: '',
        timeSlot: '',
        hours: 1,
        courseType: 'private',
        remark: ''
      },
      rules: {
        trainerId: [{ required: true, message: '请选择教练', trigger: 'change' }],
        memberName: [{ required: true, message: '请输入会员姓名', trigger: 'blur' }],
        phone: [{ required: true, validator: validatePhone, trigger: 'blur' }],
        date: [{ required: true, message: '请选择预约日期', trigger: 'change' }],
        timeSlot: [{ required: true, message: '请选择预约时段', trigger: 'change' }]
      },
      trainers: [
        { id: 1, name: '张教练' },
        { id: 2, name: '李教练' },
        { id: 3, name: '王教练' },
        { id: 4, name: '陈教练' },
        { id: 5, name: '刘教练' },
        { id: 6, name: '赵教练' },
        { id: 7, name: '孙教练' },
        { id: 8, name: '周教练' }
      ],
      timeSlots: [
        { label: '09:00-10:00', value: '09:00-10:00' },
        { label: '10:00-11:00', value: '10:00-11:00' },
        { label: '14:00-15:00', value: '14:00-15:00' },
        { label: '15:00-16:00', value: '15:00-16:00' },
        { label: '16:00-17:00', value: '16:00-17:00' },
        { label: '19:00-20:00', value: '19:00-20:00' },
        { label: '20:00-21:00', value: '20:00-21:00' }
      ]
    }
  },
  mounted() {
    if (this.$route.query.trainerId) {
      this.form.trainerId = parseInt(this.$route.query.trainerId)
    }
  },
  methods: {
    formatDate(date) {
      if (!date) return ''
      return new Date(date).toLocaleDateString('zh-CN')
    },
    isTimeSlotDisabled(slotValue) {
      if (!this.form.trainerId || !this.form.date) {
        return false
      }
      const bookings = JSON.parse(localStorage.getItem('bookings') || '[]')
      const targetDate = this.formatDate(this.form.date)
      return bookings.some(booking => 
        booking.trainerId === this.form.trainerId && 
        this.formatDate(booking.date) === targetDate && 
        booking.timeSlot === slotValue &&
        booking.status !== '已取消'
      )
    },
    checkMemberHours() {
      const members = JSON.parse(localStorage.getItem('members') || '[]')
      const member = members.find(m => m.phone === this.form.phone)
      if (!member) {
        return { valid: true, message: '' }
      }
      if (member.remainingHours < this.form.hours) {
        return { 
          valid: false, 
          message: `会员剩余课时不足！当前剩余 ${member.remainingHours} 课时，需要 ${this.form.hours} 课时` 
        }
      }
      return { valid: true, message: '' }
    },
    checkTimeConflict() {
      if (this.isTimeSlotDisabled(this.form.timeSlot)) {
        const trainer = this.trainers.find(t => t.id === this.form.trainerId)
        return {
          valid: false,
          message: `${trainer?.name || '该教练'} 在 ${this.formatDate(this.form.date)} ${this.form.timeSlot} 时段已有预约，请选择其他时段`
        }
      }
      return { valid: true, message: '' }
    },
    submitForm() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          const timeConflictCheck = this.checkTimeConflict()
          if (!timeConflictCheck.valid) {
            this.$message.error(timeConflictCheck.message)
            return false
          }
          const hoursCheck = this.checkMemberHours()
          if (!hoursCheck.valid) {
            this.$message.error(hoursCheck.message)
            return false
          }
          
          const members = JSON.parse(localStorage.getItem('members') || '[]')
          const memberIndex = members.findIndex(m => m.phone === this.form.phone)
          if (memberIndex !== -1) {
            const member = members[memberIndex]
            member.usedHours += this.form.hours
            member.remainingHours -= this.form.hours
            if (!member.records) member.records = []
            member.records.unshift({
              time: new Date().toLocaleString(),
              type: '消课',
              hours: this.form.hours,
              remark: `预约消费 - ${this.trainers.find(t => t.id === this.form.trainerId)?.name}`
            })
            localStorage.setItem('members', JSON.stringify(members))
          }
          
          const bookings = JSON.parse(localStorage.getItem('bookings') || '[]')
          const newBooking = {
            id: Date.now(),
            ...this.form,
            trainerName: this.trainers.find(t => t.id === this.form.trainerId)?.name,
            status: '已确认',
            createTime: new Date().toLocaleString()
          }
          bookings.unshift(newBooking)
          localStorage.setItem('bookings', JSON.stringify(bookings))
          this.$message.success('预约提交成功，课时已扣除！')
          this.$router.push('/my-bookings')
        } else {
          this.$message.error('请完善表单信息')
          return false
        }
      })
    },
    resetForm() {
      this.$refs.form.resetFields()
    }
  }
}
</script>

<style scoped>
.booking {
  padding: 0;
}
</style>
