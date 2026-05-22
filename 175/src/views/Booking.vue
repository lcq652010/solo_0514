<template>
  <div class="booking">
    <div class="page-header">
      <h1 class="page-title">预订登记</h1>
    </div>
    
    <el-card class="form-container">
      <el-form :model="bookingForm" :rules="rules" ref="bookingForm" label-width="100px">
        <el-divider content-position="left">客人信息</el-divider>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名" prop="guestName">
              <el-input v-model="bookingForm.guestName" placeholder="请输入客人姓名"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="手机号" prop="phone">
              <el-input v-model="bookingForm.phone" placeholder="请输入手机号"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="身份证号" prop="idCard">
          <el-input v-model="bookingForm.idCard" placeholder="请输入身份证号"></el-input>
        </el-form-item>
        
        <el-divider content-position="left">房间信息</el-divider>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="房型" prop="roomTypeId">
              <el-select v-model="bookingForm.roomTypeId" placeholder="请选择房型" style="width: 100%;" @change="onRoomTypeChange">
                <el-option
                  v-for="room in roomTypes"
                  :key="room.id"
                  :label="room.name"
                  :value="room.id"
                >
                  <span>{{ room.name }}</span>
                  <span style="float: right; color: #8492a6; font-size: 13px;">¥{{ room.price }}/晚</span>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="房间号" prop="roomNumber">
              <el-select v-model="bookingForm.roomNumber" placeholder="请选择房间" style="width: 100%;">
                <el-option
                  v-for="room in availableRooms"
                  :key="room.id"
                  :label="room.number"
                  :value="room.number"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="入住日期" prop="checkInDate">
              <el-date-picker
                v-model="bookingForm.checkInDate"
                type="date"
                placeholder="选择入住日期"
                style="width: 100%;"
                @change="calculateTotal"
              ></el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="退房日期" prop="checkOutDate">
              <el-date-picker
                v-model="bookingForm.checkOutDate"
                type="date"
                placeholder="选择退房日期"
                style="width: 100%;"
                @change="calculateTotal"
              ></el-date-picker>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="入住人数" prop="guests">
          <el-input-number v-model="bookingForm.guests" :min="1" :max="6"></el-input-number>
          <span style="margin-left: 10px;">人</span>
        </el-form-item>
        
        <el-divider content-position="left">费用信息</el-divider>
        
        <el-descriptions :column="2" border>
          <el-descriptions-item label="房费单价">
            <span v-if="selectedRoomType">¥{{ selectedRoomType.price }}</span>
            <span v-else>-</span>
          </el-descriptions-item>
          <el-descriptions-item label="入住天数">
            <span v-if="days > 0">{{ days }} 天</span>
            <span v-else>-</span>
          </el-descriptions-item>
          <el-descriptions-item label="房费小计">
            <span v-if="days > 0 && selectedRoomType">¥{{ roomSubtotal }}</span>
            <span v-else>-</span>
          </el-descriptions-item>
          <el-descriptions-item label="其他费用">¥0</el-descriptions-item>
        </el-descriptions>
        
        <div class="total-price">
          <span>总计：</span>
          <span class="price">¥{{ totalPrice }}</span>
        </div>
        
        <el-form-item>
          <el-button type="primary" @click="submitForm" size="large" :loading="loading">提交预订</el-button>
          <el-button @click="resetForm" size="large">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { roomTypes, rooms } from '../mock/data'

export default {
  name: 'Booking',
  data() {
    const validatePhone = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入手机号'))
      } else if (!/^1[3-9]\d{9}$/.test(value)) {
        callback(new Error('请输入正确的手机号'))
      } else {
        callback()
      }
    }
    
    const validateIdCard = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入身份证号'))
      } else if (!this.isValidIdCard(value)) {
        callback(new Error('请输入正确的身份证号'))
      } else {
        callback()
      }
    }
    
    return {
      roomTypes: roomTypes,
      rooms: rooms,
      bookingForm: {
        guestName: '',
        phone: '',
        idCard: '',
        roomTypeId: '',
        roomNumber: '',
        checkInDate: '',
        checkOutDate: '',
        guests: 1
      },
      rules: {
        guestName: [
          { required: true, message: '请输入客人姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        phone: [
          { validator: validatePhone, trigger: 'blur' }
        ],
        idCard: [
          { validator: validateIdCard, trigger: 'blur' }
        ],
        roomTypeId: [
          { required: true, message: '请选择房型', trigger: 'change' }
        ],
        roomNumber: [
          { required: true, message: '请选择房间', trigger: 'change' }
        ],
        checkInDate: [
          { required: true, message: '请选择入住日期', trigger: 'change' }
        ],
        checkOutDate: [
          { required: true, message: '请选择退房日期', trigger: 'change' }
        ]
      },
      loading: false
    }
  },
  computed: {
    selectedRoomType() {
      return this.roomTypes.find(room => room.id === this.bookingForm.roomTypeId)
    },
    availableRooms() {
      if (!this.selectedRoomType) return []
      return this.rooms.filter(room => 
        room.type === this.selectedRoomType.name && room.status === 'available'
      )
    },
    days() {
      if (!this.bookingForm.checkInDate || !this.bookingForm.checkOutDate) return 0
      const checkIn = new Date(this.bookingForm.checkInDate)
      const checkOut = new Date(this.bookingForm.checkOutDate)
      const diff = checkOut.getTime() - checkIn.getTime()
      return Math.max(0, Math.ceil(diff / (1000 * 3600 * 24)))
    },
    roomSubtotal() {
      if (!this.selectedRoomType) return 0
      return this.selectedRoomType.price * this.days
    },
    totalPrice() {
      return this.roomSubtotal
    }
  },
  mounted() {
    if (this.$route.query.roomTypeId) {
      this.bookingForm.roomTypeId = parseInt(this.$route.query.roomTypeId)
    }
  },
  methods: {
    isValidIdCard(idCard) {
      if (!/^\d{17}[\dXx]$/.test(idCard)) {
        return false
      }
      const weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
      const checkCodes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
      let sum = 0
      for (let i = 0; i < 17; i++) {
        sum += parseInt(idCard[i]) * weights[i]
      }
      const checkCode = checkCodes[sum % 11]
      return checkCode === idCard[17].toUpperCase()
    },
    checkRoomInventory() {
      if (!this.selectedRoomType || !this.bookingForm.checkInDate || !this.bookingForm.checkOutDate) {
        return { available: true, message: '' }
      }
      const availableCount = this.rooms.filter(room => 
        room.type === this.selectedRoomType.name && room.status === 'available'
      ).length
      if (availableCount <= 0) {
        return { 
          available: false, 
          message: `所选日期范围内"${this.selectedRoomType.name}"暂无空余房间，请选择其他房型或日期` 
        }
      }
      return { available: true, message: '', availableCount }
    },
    onRoomTypeChange() {
      this.bookingForm.roomNumber = ''
      this.calculateTotal()
    },
    calculateTotal() {
      const inventoryCheck = this.checkRoomInventory()
      if (!inventoryCheck.available) {
        this.$message.warning(inventoryCheck.message)
      }
    },
    formatDate(date) {
      if (!date) return ''
      const d = new Date(date)
      const year = d.getFullYear()
      const month = String(d.getMonth() + 1).padStart(2, '0')
      const day = String(d.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    },
    submitForm() {
      this.$refs.bookingForm.validate((valid) => {
        if (valid) {
          if (this.days <= 0) {
            this.$message.error('退房日期必须晚于入住日期')
            return
          }
          const inventoryCheck = this.checkRoomInventory()
          if (!inventoryCheck.available) {
            this.$message.error(inventoryCheck.message)
            return
          }
          this.loading = true
          setTimeout(() => {
            this.loading = false
            
            const room = this.rooms.find(r => r.number === this.bookingForm.roomNumber)
            if (room) {
              room.status = 'occupied'
            }
            
            const roomType = this.roomTypes.find(r => r.id === this.bookingForm.roomTypeId)
            if (roomType) {
              roomType.availableRooms = Math.max(0, roomType.availableRooms - 1)
            }
            
            this.$message.success('预订成功！')
            this.$router.push('/orders')
          }, 1000)
        } else {
          return false
        }
      })
    },
    resetForm() {
      this.$refs.bookingForm.resetFields()
    }
  }
}
</script>

<style scoped>
.total-price {
  text-align: right;
  padding: 20px;
  font-size: 18px;
}

.total-price .price {
  font-size: 28px;
  font-weight: bold;
  color: #f56c6c;
}

.el-descriptions {
  margin-bottom: 20px;
}
</style>
