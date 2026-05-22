<template>
  <div class="page-card form-container">
    <el-steps :active="1" finish-status="success" style="margin-bottom: 40px">
      <el-step title="填写约课信息"></el-step>
      <el-step title="确认提交"></el-step>
      <el-step title="预约成功"></el-step>
    </el-steps>

    <el-form
      ref="bookingForm"
      :model="bookingForm"
      :rules="rules"
      label-width="120px"
      label-position="right"
    >
      <el-divider content-position="left">基本信息</el-divider>

      <el-form-item label="会员姓名" prop="memberName">
        <el-input v-model="bookingForm.memberName" placeholder="请输入您的姓名" style="width: 300px"></el-input>
      </el-form-item>

      <el-form-item label="联系电话" prop="phone">
        <el-input v-model="bookingForm.phone" placeholder="请输入联系电话" style="width: 300px"></el-input>
      </el-form-item>

      <el-divider content-position="left">课程选择</el-divider>

      <el-form-item label="选择教练" prop="trainerId">
        <el-select
          v-model="bookingForm.trainerId"
          placeholder="请选择教练"
          style="width: 300px"
          @change="handleTrainerChange"
        >
          <el-option
            v-for="trainer in availableTrainers"
            :key="trainer.id"
            :label="trainer.name"
            :value="trainer.id"
          >
            <span style="float: left">{{ trainer.name }}</span>
            <span style="float: right; color: #8492a6; font-size: 13px">
              {{ trainer.specialty }}
            </span>
          </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="课程类型" prop="courseType">
        <el-radio-group v-model="bookingForm.courseType">
          <el-radio label="1">一对一私教课</el-radio>
          <el-radio label="2">小班课 (2-4人)</el-radio>
          <el-radio label="3">特色课程</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item label="课程名称" prop="courseName" v-if="bookingForm.courseType === '3'">
        <el-select v-model="bookingForm.courseName" placeholder="请选择特色课程" style="width: 300px">
          <el-option label="瑜伽入门" value="瑜伽入门"></el-option>
          <el-option label="普拉提" value="普拉提"></el-option>
          <el-option label="拳击训练" value="拳击训练"></el-option>
          <el-option label="HIIT燃脂" value="HIIT燃脂"></el-option>
          <el-option label="康复训练" value="康复训练"></el-option>
        </el-select>
      </el-form-item>

      <el-divider content-position="left">时间选择</el-divider>

      <el-form-item label="上课日期" prop="date">
        <el-date-picker
          v-model="bookingForm.date"
          type="date"
          placeholder="选择上课日期"
          style="width: 300px"
          :picker-options="pickerOptions"
        ></el-date-picker>
      </el-form-item>

      <el-form-item label="上课时间" prop="time">
        <el-select v-model="bookingForm.time" placeholder="请选择时间段" style="width: 300px">
          <el-option label="09:00-10:00" value="09:00-10:00"></el-option>
          <el-option label="10:00-11:00" value="10:00-11:00"></el-option>
          <el-option label="11:00-12:00" value="11:00-12:00"></el-option>
          <el-option label="14:00-15:00" value="14:00-15:00"></el-option>
          <el-option label="15:00-16:00" value="15:00-16:00"></el-option>
          <el-option label="16:00-17:00" value="16:00-17:00"></el-option>
          <el-option label="17:00-18:00" value="17:00-18:00"></el-option>
          <el-option label="18:00-19:00" value="18:00-19:00"></el-option>
          <el-option label="19:00-20:00" value="19:00-20:00"></el-option>
          <el-option label="20:00-21:00" value="20:00-21:00"></el-option>
        </el-select>
      </el-form-item>

      <el-divider content-position="left">其他信息</el-divider>

      <el-form-item label="训练目标" prop="goal">
        <el-checkbox-group v-model="bookingForm.goal">
          <el-checkbox label="增肌"></el-checkbox>
          <el-checkbox label="减脂"></el-checkbox>
          <el-checkbox label="塑形"></el-checkbox>
          <el-checkbox label="康复"></el-checkbox>
          <el-checkbox label="体能提升"></el-checkbox>
        </el-checkbox-group>
      </el-form-item>

      <el-form-item label="备注说明" prop="remark">
        <el-input
          v-model="bookingForm.remark"
          type="textarea"
          :rows="4"
          placeholder="请输入备注信息（选填）"
          maxlength="200"
          show-word-limit
          style="width: 400px"
        ></el-input>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" size="large" @click="handleSubmit" :loading="submitLoading">
          <i class="el-icon-check"></i> 提交预约
        </el-button>
        <el-button size="large" @click="handleReset">
          <i class="el-icon-refresh-left"></i> 重置表单
        </el-button>
        <el-button size="large" @click="$router.push('/my-bookings')">
          <i class="el-icon-document"></i> 查看我的约课
        </el-button>
      </el-form-item>
    </el-form>

    <el-dialog
      title="预约成功"
      :visible.sync="successVisible"
      width="450px"
      :close-on-click-modal="false"
    >
      <div style="text-align: center; padding: 20px">
        <i class="el-icon-circle-check" style="font-size: 60px; color: #67c23a"></i>
        <h3 style="margin: 20px 0; color: #67c23a">预约成功！</h3>
        <el-descriptions :column="1" border size="small">
          <el-descriptions-item label="教练">{{ selectedTrainerName }}</el-descriptions-item>
          <el-descriptions-item label="日期">{{ bookingForm.date }}</el-descriptions-item>
          <el-descriptions-item label="时间">{{ bookingForm.time }}</el-descriptions-item>
        </el-descriptions>
        <p style="margin-top: 20px; color: #909399; font-size: 14px">
          教练会尽快与您联系确认课程详情，请保持手机畅通
        </p>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="goToMyBookings">查看我的约课</el-button>
        <el-button type="primary" @click="continueBooking">继续约课</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { mockTrainers, mockBookings } from '@/mock/data'

export default {
  name: 'BookingForm',
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
      availableTrainers: mockTrainers.filter(t => t.status !== 'offline'),
      bookedSlots: [...mockBookings],
      bookingForm: {
        memberName: '',
        phone: '',
        trainerId: '',
        courseType: '1',
        courseName: '',
        date: '',
        time: '',
        goal: [],
        remark: ''
      },
      rules: {
        memberName: [
          { required: true, message: '请输入您的姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '姓名长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        phone: [{ validator: validatePhone, trigger: 'blur' }],
        trainerId: [{ required: true, message: '请选择教练', trigger: 'change' }],
        date: [{ required: true, message: '请选择上课日期', trigger: 'change' }],
        time: [{ required: true, message: '请选择上课时间', trigger: 'change' }],
        goal: [{ type: 'array', required: true, message: '请至少选择一个训练目标', trigger: 'change' }]
      },
      pickerOptions: {
        disabledDate(time) {
          return time.getTime() < Date.now() - 8.64e7
        }
      },
      submitLoading: false,
      successVisible: false
    }
  },
  computed: {
    selectedTrainerName() {
      const trainer = this.availableTrainers.find(t => t.id === this.bookingForm.trainerId)
      return trainer ? trainer.name : ''
    }
  },
  mounted() {
    const { trainerId, trainerName } = this.$route.query
    if (trainerId) {
      this.bookingForm.trainerId = parseInt(trainerId)
    }
  },
  methods: {
    handleTrainerChange() {
      const trainer = this.availableTrainers.find(t => t.id === this.bookingForm.trainerId)
      if (trainer && this.bookingForm.courseType !== '3') {
        this.bookingForm.courseName = trainer.specialty.split('、')[0] + '训练课'
      }
    },
    checkTimeConflict() {
      const { trainerId, date, time } = this.bookingForm
      const trainerName = this.selectedTrainerName
      const formatDate = this.formatDate(date)
      
      const conflict = this.bookedSlots.find(
        slot => slot.trainerId === trainerId && 
                slot.date === formatDate && 
                slot.time === time &&
                slot.status !== 'cancelled'
      )
      
      if (conflict) {
        this.$message.error(`教练【${trainerName}】在 ${formatDate} ${time} 时段已有预约，请选择其他时段`)
        return true
      }
      return false
    },
    formatDate(date) {
      if (!date) return ''
      const d = new Date(date)
      const year = d.getFullYear()
      const month = String(d.getMonth() + 1).padStart(2, '0')
      const day = String(d.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    },
    handleSubmit() {
      this.$refs.bookingForm.validate(valid => {
        if (valid) {
          if (this.checkTimeConflict()) {
            return false
          }
          this.submitLoading = true
          setTimeout(() => {
            this.submitLoading = false
            const newBooking = {
              id: Date.now(),
              memberName: this.bookingForm.memberName,
              trainerId: this.bookingForm.trainerId,
              trainerName: this.selectedTrainerName,
              courseName: this.bookingForm.courseName,
              courseType: this.bookingForm.courseType,
              date: this.formatDate(this.bookingForm.date),
              time: this.bookingForm.time,
              status: 'pending',
              createTime: new Date().toLocaleString()
            }
            this.bookedSlots.push(newBooking)
            mockBookings.push(newBooking)
            this.successVisible = true
          }, 1000)
        } else {
          this.$message.error('请检查表单填写是否正确')
          return false
        }
      })
    },
    handleReset() {
      this.$refs.bookingForm.resetFields()
    },
    goToMyBookings() {
      this.successVisible = false
      this.$router.push({
        path: '/my-bookings',
        query: { refresh: 'true' }
      })
    },
    continueBooking() {
      this.successVisible = false
      this.handleReset()
    }
  }
}
</script>

<style scoped>
.el-divider {
  margin: 30px 0;
}
</style>
