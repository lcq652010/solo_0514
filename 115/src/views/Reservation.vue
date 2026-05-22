<template>
  <div class="reservation-page">
    <el-card>
      <div slot="header">
        <span>📝 在线预约座位</span>
      </div>

      <el-form
        :model="reservationForm"
        :rules="rules"
        ref="reservationForm"
        label-width="120px"
        class="reservation-form"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="选择楼层" prop="floor">
              <el-select v-model="reservationForm.floor" placeholder="请选择楼层" style="width: 100%;">
                <el-option label="一楼自习区" value="1"></el-option>
                <el-option label="二楼自习区" value="2"></el-option>
                <el-option label="三楼自习区" value="3"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="选择区域" prop="zone">
              <el-select v-model="reservationForm.zone" placeholder="请选择区域" style="width: 100%;">
                <el-option label="A区 - 靠窗区域" value="A"></el-option>
                <el-option label="B区 - 中央区域" value="B"></el-option>
                <el-option label="C区 - 安静区域" value="C"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="座位号" prop="seatNumber">
              <el-select v-model="reservationForm.seatNumber" placeholder="请选择座位号" style="width: 100%;">
                <el-option v-for="seat in availableSeats" :key="seat.id" :label="seat.number" :value="seat.id">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="预约日期" prop="date">
              <el-date-picker
                v-model="reservationForm.date"
                type="date"
                placeholder="选择日期"
                style="width: 100%;"
                :picker-options="pickerOptions"
              ></el-date-picker>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="开始时间" prop="startTime">
              <el-time-picker
                v-model="reservationForm.startTime"
                format="HH:mm"
                value-format="HH:mm"
                placeholder="选择开始时间"
                style="width: 100%;"
                :picker-options="{ start: '08:00', step: '00:30', end: '20:00' }"
              ></el-time-picker>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="结束时间" prop="endTime">
              <el-time-picker
                v-model="reservationForm.endTime"
                format="HH:mm"
                value-format="HH:mm"
                placeholder="选择结束时间"
                style="width: 100%;"
                :picker-options="{ start: '08:00', step: '00:30', end: '22:00' }"
              ></el-time-picker>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="预约用途" prop="purpose">
          <el-radio-group v-model="reservationForm.purpose">
            <el-radio label="自习">自习</el-radio>
            <el-radio label="阅读">阅读</el-radio>
            <el-radio label="小组讨论">小组讨论</el-radio>
            <el-radio label="其他">其他</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="reservationForm.phone" placeholder="请输入联系电话" maxlength="11"></el-input>
        </el-form-item>

        <el-form-item label="备注" prop="remark">
          <el-input
            type="textarea"
            v-model="reservationForm.remark"
            placeholder="请输入备注信息（选填）"
            :rows="3"
          ></el-input>
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
  name: 'Reservation',
  data() {
    const validatePhone = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入联系电话'));
      } else if (!/^1[3-9]\d{9}$/.test(value)) {
        callback(new Error('请输入正确的手机号格式'));
      } else {
        callback();
      }
    };

    const validateTime = (rule, value, callback) => {
      if (this.reservationForm.startTime && this.reservationForm.endTime) {
        if (this.reservationForm.startTime >= this.reservationForm.endTime) {
          callback(new Error('结束时间必须晚于开始时间'));
        } else {
          callback();
        }
      } else {
        callback();
      }
    };

    return {
      reservationForm: {
        floor: '',
        zone: '',
        seatNumber: '',
        date: '',
        startTime: '',
        endTime: '',
        purpose: '自习',
        phone: '',
        remark: ''
      },
      rules: {
        floor: [{ required: true, message: '请选择楼层', trigger: 'change' }],
        zone: [{ required: true, message: '请选择区域', trigger: 'change' }],
        seatNumber: [{ required: true, message: '请选择座位号', trigger: 'change' }],
        date: [{ required: true, message: '请选择预约日期', trigger: 'change' }],
        startTime: [{ required: true, message: '请选择开始时间', trigger: 'change' }],
        endTime: [
          { required: true, message: '请选择结束时间', trigger: 'change' },
          { validator: validateTime, trigger: 'change' }
        ],
        purpose: [{ required: true, message: '请选择预约用途', trigger: 'change' }],
        phone: [{ validator: validatePhone, trigger: 'blur' }]
      },
      pickerOptions: {
        disabledDate(time) {
          return time.getTime() < Date.now() - 8.64e7;
        }
      },
      availableSeats: []
    };
  },
  mounted() {
    if (this.$route.query.seatId) {
      const [zone, num] = this.$route.query.seatId.split('-');
      this.reservationForm.zone = zone;
    }
  },
  watch: {
    'reservationForm.zone': function(newVal) {
      this.generateSeats(newVal);
    }
  },
  methods: {
    generateSeats(zone) {
      this.availableSeats = [];
      const count = zone === 'B' ? 16 : 12;
      for (let i = 1; i <= count; i++) {
        this.availableSeats.push({
          id: `${zone}-${i}`,
          number: `${zone}${String(i).padStart(2, '0')}`
        });
      }
    },
    submitForm() {
      this.$refs.reservationForm.validate((valid) => {
        if (valid) {
          this.$confirm('确认提交预约信息吗？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            this.$message({
              type: 'success',
              message: '预约成功！请准时前往图书馆签到'
            });
            this.$router.push('/my-reservations');
          }).catch(() => {});
        } else {
          this.$message.error('请完善必填信息');
          return false;
        }
      });
    },
    resetForm() {
      this.$refs.reservationForm.resetFields();
    }
  }
};
</script>

<style scoped>
.reservation-page {
  padding: 0;
}

.reservation-form {
  max-width: 800px;
  margin: 0 auto;
}
</style>
