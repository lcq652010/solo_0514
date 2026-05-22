<template>
  <div class="page-container">
    <h1 class="page-title">在线预约</h1>
    
    <div class="card-wrapper">
      <el-form 
      ref="reserveForm"
        :model="form"
        :rules="rules"
        label-width="120px"
        class="reserve-form"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="车主姓名" prop="ownerName">
              <el-input v-model="form.ownerName" placeholder="请输入车主姓名"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="form.phone" placeholder="请输入联系电话" maxlength="11"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="车牌号码" prop="carNumber">
              <el-input v-model="form.carNumber" placeholder="如：京A88888"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="车辆品牌" prop="carBrand">
              <el-select v-model="form.carBrand" placeholder="请选择车辆品牌" style="width: 100%;">
                <el-option label="奥迪" value="奥迪"></el-option>
                <el-option label="宝马" value="宝马"></el-option>
                <el-option label="奔驰" value="奔驰"></el-option>
                <el-option label="丰田" value="丰田"></el-option>
                <el-option label="本田" value="本田"></el-option>
                <el-option label="大众" value="大众"></el-option>
                <el-option label="别克" value="别克"></el-option>
                <el-option label="其他" value="其他"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="保养套餐" prop="packageId">
              <el-select v-model="form.packageId" placeholder="请选择保养套餐" style="width: 100%;" @change="onPackageChange">
                <el-option 
                  v-for="pkg in packages" 
                  :key="pkg.id" 
                  :label="pkg.name" 
                  :value="pkg.id"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="预约日期" prop="reserveDate">
              <el-date-picker
                v-model="form.reserveDate"
                type="date"
                placeholder="选择预约日期"
                style="width: 100%;"
                :picker-options="pickerOptions"
              ></el-date-picker>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="维修工位" prop="stationId">
              <el-select v-model="form.stationId" placeholder="请选择工位" style="width: 100%;" @change="onStationChange">
                <el-option 
                  v-for="station in stations" 
                  :key="station.id" 
                  :label="station.name" 
                  :value="station.id"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="预约时段" prop="reserveTime">
              <el-select v-model="form.reserveTime" placeholder="请选择时段" style="width: 100%;">
                <el-option 
                  v-for="slot in timeSlots" 
                  :key="slot.value" 
                  :label="slot.label" 
                  :value="slot.value"
                  :disabled="slot.disabled"
                ></el-option>
              </el-select>
              <div v-if="conflictTip" class="conflict-tip">
                <i class="el-icon-warning"></i> {{ conflictTip }}
              </div>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="服务顾问" prop="consultant">
              <el-select v-model="form.consultant" placeholder="选择服务顾问" style="width: 100%;">
                <el-option label="张经理" value="张经理"></el-option>
                <el-option label="李主管" value="李主管"></el-option>
                <el-option label="王技师" value="王技师"></el-option>
                <el-option label="随机分配" value="随机分配"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="备注信息" prop="remark">
          <el-input
            type="textarea"
            :rows="4"
            v-model="form.remark"
            placeholder="请描述车辆具体情况或特殊需求（选填）"
          ></el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" size="large" @click="submitForm" class="submit-btn">
            提交预约
          </el-button>
          <el-button size="large" @click="resetForm">重置表单</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Reserve',
  data() {
    const validatePhone = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入联系电话'))
      } else if (!/^1[3-9]\d{9}$/.test(value)) {
        callback(new Error('请输入正确的手机号格式'))
      } else {
        callback()
      }
    }
    
    const validateCarNumber = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入车牌号码'))
      } else if (!/^[\u4e00-\u9fa5]{1}[A-Z]{1}[A-Z_0-9]{5}$/.test(value)) {
        callback(new Error('请输入正确的车牌号格式'))
      } else {
        callback()
      }
    }
    
    return {
      form: {
        ownerName: '',
        phone: '',
        carNumber: '',
        carBrand: '',
        packageId: '',
        stationId: '',
        reserveDate: '',
        reserveTime: '',
        consultant: '',
        remark: ''
      },
      rules: {
        ownerName: [
          { required: true, message: '请输入车主姓名', trigger: 'blur' },
          { min: 2, max: 10, message: '长度在 2 到 10 个字符', trigger: 'blur' }
        ],
        phone: [
          { validator: validatePhone, trigger: 'blur' }
        ],
        carNumber: [
          { validator: validateCarNumber, trigger: 'blur' }
        ],
        carBrand: [
          { required: true, message: '请选择车辆品牌', trigger: 'change' }
        ],
        packageId: [
          { required: true, message: '请选择保养套餐', trigger: 'change' }
        ],
        stationId: [
          { required: true, message: '请选择维修工位', trigger: 'change' }
        ],
        reserveDate: [
          { required: true, message: '请选择预约日期', trigger: 'change' }
        ],
        reserveTime: [
          { required: true, message: '请选择预约时段', trigger: 'change' }
        ]
      },
      packages: [
        { id: 1, name: '基础保养套餐 - ¥299' },
        { id: 2, name: '标准保养套餐 - ¥599' },
        { id: 3, name: '尊享保养套餐 - ¥1299' },
        { id: 4, name: '刹车系统养护 - ¥399' },
        { id: 5, name: '空调系统养护 - ¥299' },
        { id: 6, name: '漆面养护套餐 - ¥699' }
      ],
      stations: [
        { id: 1, name: '1号工位 - 机修' },
        { id: 2, name: '2号工位 - 机修' },
        { id: 3, name: '3号工位 - 美容' },
        { id: 4, name: '4号工位 - 美容' },
        { id: 5, name: '5号工位 - 快修' }
      ],
      timeSlots: [
        { label: '09:00-10:00', value: '09:00-10:00', disabled: false },
        { label: '10:00-11:00', value: '10:00-11:00', disabled: false },
        { label: '11:00-12:00', value: '11:00-12:00', disabled: false },
        { label: '14:00-15:00', value: '14:00-15:00', disabled: false },
        { label: '15:00-16:00', value: '15:00-16:00', disabled: false },
        { label: '16:00-17:00', value: '16:00-17:00', disabled: false }
      ],
      conflictTip: '',
      pickerOptions: {
        disabledDate(time) {
          return time.getTime() < Date.now() - 8.64e7
        },
        onClick: () => {
          this.checkTimeConflict()
        }
      }
    }
  },
  watch: {
    'form.stationId': function() {
      this.checkTimeConflict()
    },
    'form.reserveDate': function() {
      this.checkTimeConflict()
    }
  },
  mounted() {
    if (this.$route.query.packageId) {
      this.form.packageId = parseInt(this.$route.query.packageId)
    }
  },
  methods: {
    onPackageChange() {
    },
    onStationChange() {
      this.form.reserveTime = ''
      this.checkTimeConflict()
    },
    checkTimeConflict() {
      if (!this.form.stationId || !this.form.reserveDate) {
        this.timeSlots.forEach(slot => slot.disabled = false)
        this.conflictTip = ''
        return
      }
      
      const records = JSON.parse(localStorage.getItem('reserveRecords') || '[]')
      const selectedDate = new Date(this.form.reserveDate).toDateString()
      
      const conflictRecords = records.filter(r => {
        if (r.status === 4) return false
        const recordDate = new Date(r.reserveDate).toDateString()
        return r.stationId === this.form.stationId && recordDate === selectedDate
      })
      
      const conflictTimes = conflictRecords.map(r => r.reserveTime)
      
      this.timeSlots.forEach(slot => {
        slot.disabled = conflictTimes.includes(slot.value)
      })
      
      if (conflictTimes.length > 0) {
        const station = this.stations.find(s => s.id === this.form.stationId)
        this.conflictTip = `${station?.name || ''}已有 ${conflictTimes.length} 个时段被预约`
      } else {
        this.conflictTip = ''
      }
    },
    submitForm() {
      this.$refs.reserveForm.validate((valid) => {
        if (valid) {
          const reserveData = {
            id: Date.now(),
            ...this.form,
            status: 0,
            createTime: new Date().toLocaleString()
          }
          
          let records = JSON.parse(localStorage.getItem('reserveRecords') || '[]')
          records.unshift(reserveData)
          localStorage.setItem('reserveRecords', JSON.stringify(records))
          
          this.$message({
            type: 'success',
            message: '预约提交成功！'
          })
          
          setTimeout(() => {
            this.$router.push('/records')
          }, 1000)
        } else {
          this.$message.error('请完善必填信息')
          return false
        }
      })
    },
    resetForm() {
      this.$refs.reserveForm.resetFields()
    }
  }
}
</script>

<style scoped>
.reserve-form {
  max-width: 900px;
  margin: 0 auto;
}

.submit-btn {
  width: 200px;
  height: 44px;
}

.conflict-tip {
  margin-top: 8px;
  font-size: 12px;
  color: #e6a23c;
}

.conflict-tip i {
  margin-right: 4px;
}
</style>
