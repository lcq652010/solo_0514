<template>
  <div class="reservation">
    <div class="page-title">练车预约</div>
    <div class="card-wrapper">
      <el-form
        ref="reservationForm"
        :model="reservationForm"
        :rules="rules"
        label-width="100px"
        label-position="right"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="学员姓名" prop="studentName">
              <el-input v-model="reservationForm.studentName" placeholder="请输入学员姓名"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="reservationForm.phone" placeholder="请输入联系电话" maxlength="11"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="选择教练" prop="coach">
              <el-select v-model="reservationForm.coach" placeholder="请选择教练" style="width: 100%">
                <el-option label="张教练 (科目二)" value="张教练"></el-option>
                <el-option label="李教练 (科目三)" value="李教练"></el-option>
                <el-option label="王教练 (科目二)" value="王教练"></el-option>
                <el-option label="赵教练 (科目三)" value="赵教练"></el-option>
                <el-option label="周教练 (科目三)" value="周教练"></el-option>
                <el-option label="郑教练 (科目三)" value="郑教练"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="培训科目" prop="subject">
              <el-radio-group v-model="reservationForm.subject">
                <el-radio label="科目二">科目二</el-radio>
                <el-radio label="科目三">科目三</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="预约日期" prop="reserveDate">
              <el-date-picker
                v-model="reservationForm.reserveDate"
                type="date"
                placeholder="选择预约日期"
                style="width: 100%"
                :picker-options="pickerOptions"
              ></el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="预约时段" prop="timeSlot">
              <el-select v-model="reservationForm.timeSlot" placeholder="请选择时段" style="width: 100%">
                <el-option 
                  v-for="slot in timeSlots" 
                  :key="slot.value" 
                  :label="slot.label" 
                  :value="slot.value"
                  :disabled="slot.disabled"
                >
                  <span>{{ slot.label }}</span>
                  <span v-if="slot.disabled" style="color: #f56c6c; margin-left: 10px">（已预约）</span>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="备注" prop="remark">
          <el-input
            type="textarea"
            :rows="3"
            v-model="reservationForm.remark"
            placeholder="请输入特殊需求或备注（选填）"
          ></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm">提交预约</el-button>
          <el-button @click="resetForm">重置</el-button>
          <el-button type="info" @click="goToList">查看预约记录</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="card-wrapper" style="margin-top: 20px">
      <div class="tips-title">
        <i class="el-icon-info"></i>
        预约须知
      </div>
      <el-divider></el-divider>
      <div class="tips-content">
        <ul>
          <li>请提前至少1天进行预约，取消预约请提前2小时联系教练</li>
          <li>每人每天最多预约2小时，每周最多预约6小时</li>
          <li>预约成功后，请按时到达训练场，迟到超过15分钟预约自动取消</li>
          <li>累计3次爽约将暂停预约资格7天</li>
          <li>如遇恶劣天气等特殊情况，教练会提前通知调整预约</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Reservation',
  data() {
    const validatePhone = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入联系电话'));
      } else if (!/^1[3-9]\d{9}$/.test(value)) {
        callback(new Error('请输入正确的手机号码'));
      } else {
        callback();
      }
    };

    const validateTimeSlot = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请选择预约时段'));
      } else if (this.isConflict) {
        callback(new Error('该时段已被预约，请选择其他时段'));
      } else {
        callback();
      }
    };

    return {
      reservationForm: {
        studentName: '',
        phone: '',
        coach: '',
        subject: '',
        reserveDate: '',
        timeSlot: '',
        remark: ''
      },
      rules: {
        studentName: [
          { required: true, message: '请输入学员姓名', trigger: 'blur' }
        ],
        phone: [
          { validator: validatePhone, trigger: 'blur' }
        ],
        coach: [
          { required: true, message: '请选择教练', trigger: 'change' }
        ],
        subject: [
          { required: true, message: '请选择培训科目', trigger: 'change' }
        ],
        reserveDate: [
          { required: true, message: '请选择预约日期', trigger: 'change' }
        ],
        timeSlot: [
          { validator: validateTimeSlot, trigger: 'change' }
        ]
      },
      pickerOptions: {
        disabledDate(time) {
          const today = new Date();
          today.setHours(0, 0, 0, 0);
          return time.getTime() < today.getTime();
        }
      },
      existingReservations: [
        { coach: '张教练', date: '2026-05-18', timeSlot: '08:00-10:00', studentName: '张三' },
        { coach: '张教练', date: '2026-05-18', timeSlot: '14:00-16:00', studentName: '李四' },
        { coach: '李教练', date: '2026-05-18', timeSlot: '10:00-12:00', studentName: '王五' },
        { coach: '李教练', date: '2026-05-19', timeSlot: '08:00-10:00', studentName: '赵六' },
        { coach: '王教练', date: '2026-05-18', timeSlot: '16:00-18:00', studentName: '孙七' },
        { coach: '周教练', date: '2026-05-18', timeSlot: '08:00-10:00', studentName: '周八' },
        { coach: '郑教练', date: '2026-05-18', timeSlot: '10:00-12:00', studentName: '吴九' }
      ],
      baseTimeSlots: [
        { label: '上午 08:00-10:00', value: '08:00-10:00' },
        { label: '上午 10:00-12:00', value: '10:00-12:00' },
        { label: '下午 14:00-16:00', value: '14:00-16:00' },
        { label: '下午 16:00-18:00', value: '16:00-18:00' },
        { label: '晚间 18:00-20:00', value: '18:00-20:00' }
      ]
    };
  },
  computed: {
    timeSlots() {
      if (!this.reservationForm.coach || !this.reservationForm.reserveDate) {
        return this.baseTimeSlots.map(slot => ({ ...slot, disabled: false }));
      }
      const dateStr = typeof this.reservationForm.reserveDate === 'string' 
        ? this.reservationForm.reserveDate 
        : this.reservationForm.reserveDate.toISOString().split('T')[0];
      const bookedSlots = this.existingReservations.filter(
        r => r.coach === this.reservationForm.coach && r.date === dateStr
      ).map(r => r.timeSlot);
      return this.baseTimeSlots.map(slot => ({
        ...slot,
        disabled: bookedSlots.includes(slot.value)
      }));
    },
    isConflict() {
      if (!this.reservationForm.coach || !this.reservationForm.reserveDate || !this.reservationForm.timeSlot) {
        return false;
      }
      const dateStr = typeof this.reservationForm.reserveDate === 'string' 
        ? this.reservationForm.reserveDate 
        : this.reservationForm.reserveDate.toISOString().split('T')[0];
      return this.existingReservations.some(
        r => r.coach === this.reservationForm.coach && 
             r.date === dateStr && 
             r.timeSlot === this.reservationForm.timeSlot
      );
    }
  },
  watch: {
    'reservationForm.coach'(newVal, oldVal) {
      if (newVal && newVal !== oldVal && this.reservationForm.timeSlot) {
        this.$refs.reservationForm.validateField('timeSlot');
      }
    },
    'reservationForm.reserveDate'(newVal, oldVal) {
      if (newVal && newVal !== oldVal && this.reservationForm.timeSlot) {
        this.$refs.reservationForm.validateField('timeSlot');
      }
    }
  },
  mounted() {
    if (this.$route.query.coachName) {
      this.reservationForm.coach = this.$route.query.coachName;
    }
  },
  methods: {
    submitForm() {
      this.$refs.reservationForm.validate((valid) => {
        if (valid) {
          if (this.isConflict) {
            this.$message.error('该时段已被预约，请选择其他时段');
            return false;
          }
          this.$confirm('确认提交预约？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            const dateStr = typeof this.reservationForm.reserveDate === 'string'
              ? this.reservationForm.reserveDate
              : this.reservationForm.reserveDate.toISOString().split('T')[0];
            const newReservation = {
              id: Date.now(),
              studentName: this.reservationForm.studentName,
              phone: this.reservationForm.phone,
              coach: this.reservationForm.coach,
              subject: this.reservationForm.subject,
              reserveDate: dateStr,
              timeSlot: this.reservationForm.timeSlot,
              createTime: new Date().toLocaleString('zh-CN', { hour12: false }).replace(/\//g, '-'),
              status: '待确认'
            };
            this.existingReservations.push({
              coach: this.reservationForm.coach,
              date: dateStr,
              timeSlot: this.reservationForm.timeSlot,
              studentName: this.reservationForm.studentName
            });
            const reservations = JSON.parse(localStorage.getItem('reservations') || '[]');
            reservations.push(newReservation);
            localStorage.setItem('reservations', JSON.stringify(reservations));
            this.$message({
              type: 'success',
              message: '预约成功！正在跳转到预约记录...'
            });
            setTimeout(() => {
              this.$router.push('/reservation-list');
            }, 1000);
          }).catch(() => {});
        } else {
          this.$message.error('请检查表单填写是否正确');
          return false;
        }
      });
    },
    resetForm() {
      this.$refs.reservationForm.resetFields();
    },
    goToList() {
      this.$router.push('/reservation-list');
    }
  }
};
</script>

<style scoped>
.reservation {
  max-width: 800px;
}

.tips-title {
  font-size: 16px;
  font-weight: bold;
  color: #409eff;
  display: flex;
  align-items: center;
}

.tips-title i {
  margin-right: 8px;
}

.tips-content ul {
  padding-left: 20px;
  color: #606266;
  line-height: 2;
}

.tips-content li {
  margin-bottom: 8px;
}
</style>
