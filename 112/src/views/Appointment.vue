<template>
  <div class="appointment">
    <el-card class="form-card">
      <div slot="header" class="card-header">
        <span>在线预约</span>
      </div>

      <el-form :model="form" :rules="rules" ref="form" label-width="120px" class="appointment-form">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="预约事项" prop="itemName">
              <el-select v-model="form.itemName" placeholder="请选择预约事项" style="width: 100%">
                <el-option label="居民身份证办理" value="居民身份证办理"></el-option>
                <el-option label="不动产权登记" value="不动产权登记"></el-option>
                <el-option label="社保卡申领" value="社保卡申领"></el-option>
                <el-option label="营业执照办理" value="营业执照办理"></el-option>
                <el-option label="公积金提取" value="公积金提取"></el-option>
                <el-option label="出入境证件办理" value="出入境证件办理"></el-option>
                <el-option label="医疗保险报销" value="医疗保险报销"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="预约日期" prop="date">
              <el-date-picker
                v-model="form.date"
                type="date"
                placeholder="选择预约日期"
                :picker-options="pickerOptions"
                style="width: 100%">
              </el-date-picker>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="预约时段" prop="timeSlot">
              <el-select v-model="form.timeSlot" placeholder="请选择预约时段" style="width: 100%" @change="checkConflict">
                <el-option 
                  v-for="slot in timeSlots" 
                  :key="slot.value" 
                  :label="slot.label" 
                  :value="slot.value"
                  :disabled="slot.disabled">
                  <span>{{ slot.label }}</span>
                  <span v-if="slot.disabled" style="color: #f56c6c; margin-left: 10px;">（已满）</span>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="办理窗口" prop="window">
              <el-select v-model="form.window" placeholder="请选择办理窗口" style="width: 100%" @change="checkConflict">
                <el-option label="1号窗口（综合业务）" value="1号窗口（综合业务）"></el-option>
                <el-option label="2号窗口（户政业务）" value="2号窗口（户政业务）"></el-option>
                <el-option label="3号窗口（社保业务）" value="3号窗口（社保业务）"></el-option>
                <el-option label="4号窗口（不动产）" value="4号窗口（不动产）"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-alert
          v-if="conflictMessage"
          :title="conflictMessage"
          type="warning"
          :closable="false"
          show-icon
          style="margin-bottom: 20px;">
        </el-alert>

        <el-divider content-position="left">申请人信息</el-divider>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="form.name" placeholder="请输入姓名" maxlength="20" show-word-limit></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-radio-group v-model="form.gender">
                <el-radio label="男">男</el-radio>
                <el-radio label="女">女</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="身份证号" prop="idCard">
              <el-input v-model="form.idCard" placeholder="请输入18位身份证号" maxlength="18"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="form.phone" placeholder="请输入11位手机号" maxlength="11"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="联系地址" prop="address">
              <el-input v-model="form.address" placeholder="请输入详细地址"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="备注说明" prop="remark">
              <el-input
                type="textarea"
                :rows="4"
                v-model="form.remark"
                placeholder="请输入需要说明的情况（选填）"
                maxlength="200"
                show-word-limit>
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item>
          <el-button type="primary" size="large" @click="handleSubmit" :loading="submitLoading">
            <i class="el-icon-check"></i> 提交预约
          </el-button>
          <el-button size="large" @click="handleReset">
            <i class="el-icon-refresh-left"></i> 重置表单
          </el-button>
          <el-button size="large" @click="$router.back()">
            <i class="el-icon-back"></i> 返回上页
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'Appointment',
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
        callback(new Error('请输入正确的11位手机号'))
      } else {
        callback()
      }
    }

    return {
      form: {
        itemName: '',
        date: '',
        timeSlot: '',
        window: '',
        name: '',
        gender: '男',
        idCard: '',
        phone: '',
        address: '',
        remark: ''
      },
      rules: {
        itemName: [
          { required: true, message: '请选择预约事项', trigger: 'change' }
        ],
        date: [
          { required: true, message: '请选择预约日期', trigger: 'change' }
        ],
        timeSlot: [
          { required: true, message: '请选择预约时段', trigger: 'change' }
        ],
        window: [
          { required: true, message: '请选择办理窗口', trigger: 'change' }
        ],
        name: [
          { required: true, message: '请输入姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        gender: [
          { required: true, message: '请选择性别', trigger: 'change' }
        ],
        idCard: [
          { required: true, validator: validateIdCard, trigger: 'blur' }
        ],
        phone: [
          { required: true, validator: validatePhone, trigger: 'blur' }
        ],
        address: [
          { required: true, message: '请输入联系地址', trigger: 'blur' }
        ]
      },
      pickerOptions: {
        disabledDate(time) {
          return time.getTime() < Date.now() - 8.64e7
        }
      },
      submitLoading: false,
      conflictMessage: '',
      bookedAppointments: [
        { date: new Date().toISOString().split('T')[0], timeSlot: '上午 09:00-10:00', window: '1号窗口（综合业务）' },
        { date: new Date().toISOString().split('T')[0], timeSlot: '上午 09:00-10:00', window: '1号窗口（综合业务）' },
        { date: new Date().toISOString().split('T')[0], timeSlot: '上午 09:00-10:00', window: '1号窗口（综合业务）' },
        { date: new Date().toISOString().split('T')[0], timeSlot: '上午 09:00-10:00', window: '1号窗口（综合业务）' },
        { date: new Date().toISOString().split('T')[0], timeSlot: '上午 09:00-10:00', window: '1号窗口（综合业务）' },
        { date: new Date().toISOString().split('T')[0], timeSlot: '下午 14:00-15:00', window: '2号窗口（户政业务）' },
        { date: new Date().toISOString().split('T')[0], timeSlot: '下午 14:00-15:00', window: '2号窗口（户政业务）' },
        { date: new Date().toISOString().split('T')[0], timeSlot: '下午 14:00-15:00', window: '2号窗口（户政业务）' }
      ],
      maxPerSlot: 5
    }
  },
  computed: {
    timeSlots() {
      const slots = [
        { label: '上午 09:00-10:00', value: '上午 09:00-10:00', disabled: false },
        { label: '上午 10:00-11:00', value: '上午 10:00-11:00', disabled: false },
        { label: '下午 14:00-15:00', value: '下午 14:00-15:00', disabled: false },
        { label: '下午 15:00-16:00', value: '下午 15:00-16:00', disabled: false }
      ]

      if (this.form.date && this.form.window) {
        const dateStr = this.formatDate(this.form.date)
        slots.forEach(slot => {
          const count = this.bookedAppointments.filter(
            a => a.date === dateStr && a.timeSlot === slot.value && a.window === this.form.window
          ).length
          slot.disabled = count >= this.maxPerSlot
        })
      }
      return slots
    }
  },
  watch: {
    'form.date'() {
      this.checkConflict()
    },
    'form.window'() {
      this.checkConflict()
    }
  },
  created() {
    if (this.$route.query.itemName) {
      this.form.itemName = this.$route.query.itemName
    }
  },
  methods: {
    formatDate(date) {
      if (!date) return ''
      const d = new Date(date)
      return d.toISOString().split('T')[0]
    },
    checkConflict() {
      if (!this.form.date || !this.form.window || !this.form.timeSlot) {
        this.conflictMessage = ''
        return
      }

      const dateStr = this.formatDate(this.form.date)
      const count = this.bookedAppointments.filter(
        a => a.date === dateStr && a.timeSlot === this.form.timeSlot && a.window === this.form.window
      ).length

      if (count >= this.maxPerSlot) {
        this.conflictMessage = `该时段（${this.form.timeSlot}）在 ${this.form.window} 的预约名额已满，请选择其他时段或窗口`
        this.form.timeSlot = ''
      } else if (count > 0) {
        this.conflictMessage = `该时段当前已有 ${count} 人预约，剩余可用名额：${this.maxPerSlot - count} 个`
      } else {
        this.conflictMessage = ''
      }
    },
    handleSubmit() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          const dateStr = this.formatDate(this.form.date)
          const count = this.bookedAppointments.filter(
            a => a.date === dateStr && a.timeSlot === this.form.timeSlot && a.window === this.form.window
          ).length
          
          if (count >= this.maxPerSlot) {
            this.$message.error('该时段预约名额已满，请重新选择')
            return
          }

          this.submitLoading = true
          setTimeout(() => {
            this.submitLoading = false
            this.bookedAppointments.push({
              date: dateStr,
              timeSlot: this.form.timeSlot,
              window: this.form.window
            })
            this.$message.success('预约提交成功！')
            this.$confirm('预约成功！是否查看办事记录？', '提示', {
              confirmButtonText: '查看',
              cancelButtonText: '继续预约',
              type: 'success'
            }).then(() => {
              this.$router.push('/records')
            }).catch(() => {})
          }, 1000)
        } else {
          this.$message.error('请检查表单填写是否正确')
          return false
        }
      })
    },
    handleReset() {
      this.$refs.form.resetFields()
      this.conflictMessage = ''
    }
  }
}
</script>

<style scoped>
.appointment {
  height: 100%;
}

.form-card {
  max-width: 1000px;
  margin: 0 auto;
}

.card-header {
  font-size: 18px;
  font-weight: 500;
  color: #303133;
}

.appointment-form {
  padding: 20px 0;
}
</style>
