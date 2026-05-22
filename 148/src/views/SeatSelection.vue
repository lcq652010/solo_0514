<template>
  <div class="seat-selection">
    <el-button icon="el-icon-arrow-left" @click="goBack" class="back-btn">
      返回场次选择
    </el-button>
    
    <el-card v-if="movie && schedule" class="movie-info-card card-shadow mb-20">
      <div class="movie-info">
        <img :src="movie.poster" :alt="movie.title" class="movie-poster" />
        <div class="info-content">
          <h2>{{ movie.title }}</h2>
          <p>{{ cinema.name }}</p>
          <p>{{ schedule.hall }} | {{ schedule.date }} {{ schedule.time }} | {{ schedule.language }} {{ schedule.dimension }}</p>
        </div>
      </div>
    </el-card>
    
    <el-card class="card-shadow">
      <div class="seat-container">
        <div class="screen">银幕</div>
        
        <div class="seat-legend">
          <div class="legend-item">
            <div class="seat-demo available"></div>
            <span>可选</span>
          </div>
          <div class="legend-item">
            <div class="seat-demo selected"></div>
            <span>已选</span>
          </div>
          <div class="legend-item">
            <div class="seat-demo locked"></div>
            <span>锁定中</span>
          </div>
          <div class="legend-item">
            <div class="seat-demo occupied"></div>
            <span>已售</span>
          </div>
        </div>
        
        <div class="seats-wrapper">
          <div class="row-numbers">
            <div v-for="row in 10" :key="row" class="row-number">{{ row }}</div>
          </div>
          <div class="seats-grid">
            <div v-for="(row, rowIndex) in seats" :key="rowIndex" class="seat-row">
              <div 
                v-for="seat in row" 
                :key="seat.id" 
                class="seat"
                :class="getSeatClass(seat)"
                @click="toggleSeat(seat)"
              >
                {{ seat.col }}
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="selection-summary">
        <div class="selected-seats">
          <strong>已选座位：</strong>
          <span v-if="selectedSeats.length === 0">请选择座位</span>
          <span v-else class="seat-tags">
            <el-tag 
              v-for="seat in selectedSeats" 
              :key="seat.id" 
              closable
              @close="toggleSeat(seat)"
              type="primary"
              size="small"
            >
              {{ seat.row }}排{{ seat.col }}座
            </el-tag>
          </span>
        </div>
        <div v-if="selectedSeats.length > 0" class="lock-timer">
          <i class="el-icon-time"></i>
          <span>座位锁定中，请在</span>
          <span class="time">{{ lockTimeDisplay }}</span>
          <span>内完成支付</span>
        </div>
        <div class="total-price">
          <span>合计：</span>
          <span class="price-symbol">¥</span>
          <span class="price">{{ totalPrice }}</span>
          <span class="count">({{ selectedSeats.length }}张)</span>
        </div>
        <el-button 
          type="primary" 
          size="large" 
          class="confirm-btn"
          :disabled="selectedSeats.length === 0 || isProcessing"
          :loading="isProcessing"
          @click="showOrderDialog = true"
        >
          确认选座
        </el-button>
      </div>
    </el-card>
    
    <el-dialog
      title="确认订单"
      :visible.sync="showOrderDialog"
      width="500px"
      @close="resetForm"
    >
      <el-form :model="orderForm" :rules="rules" ref="orderForm" label-width="80px">
        <el-form-item label="电影">
          <span>{{ movie?.title }}</span>
        </el-form-item>
        <el-form-item label="场次">
          <span>{{ schedule?.date }} {{ schedule?.time }}</span>
        </el-form-item>
        <el-form-item label="座位">
          <span>{{ selectedSeatsLabels }}</span>
        </el-form-item>
        <el-form-item label="总价">
          <span class="price">¥{{ totalPrice }}</span>
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="orderForm.phone" placeholder="请输入手机号" maxlength="11"></el-input>
        </el-form-item>
        <el-form-item label="验证码" prop="code">
          <el-input v-model="orderForm.code" placeholder="请输入验证码" style="width: 200px; margin-right: 10px;"></el-input>
          <el-button :disabled="countdown > 0" @click="sendCode">
            {{ countdown > 0 ? `${countdown}秒后重发` : '获取验证码' }}
          </el-button>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showOrderDialog = false">取消</el-button>
        <el-button type="primary" @click="submitOrder">支付 ¥{{ totalPrice }}</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { movies, cinemas, schedules, generateSeats } from '@/data/mock.js'
import seatLockManager from '@/store/seatLock.js'
import orderStore from '@/store/orderStore.js'

export default {
  name: 'SeatSelection',
  data() {
    return {
      movie: null,
      cinema: null,
      schedule: null,
      seats: [],
      selectedSeats: [],
      showOrderDialog: false,
      orderForm: {
        phone: '',
        code: ''
      },
      countdown: 0,
      rules: {
        phone: [
          { required: true, message: '请输入手机号', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
        ],
        code: [
          { required: true, message: '请输入验证码', trigger: 'blur' },
          { len: 6, message: '验证码为6位', trigger: 'blur' }
        ]
      },
      refreshTimer: null,
      seatLockTimer: null,
      remainingLockTime: 0,
      isProcessing: false
    }
  },
  computed: {
    totalPrice() {
      return this.selectedSeats.length * (this.schedule?.price || 0)
    },
    selectedSeatsLabels() {
      return this.selectedSeats.map(s => `${s.row}排${s.col}座`).join('、')
    },
    scheduleId() {
      return this.schedule?.id || null
    },
    lockTimeDisplay() {
      const minutes = Math.floor(this.remainingLockTime / 60)
      const seconds = this.remainingLockTime % 60
      return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
    }
  },
  mounted() {
    const scheduleId = parseInt(this.$route.params.scheduleId)
    this.schedule = schedules.find(s => s.id === scheduleId)
    if (this.schedule) {
      this.movie = movies.find(m => m.id === this.schedule.movieId)
      this.cinema = cinemas.find(c => c.id === this.schedule.cinemaId)
      this.loadSeats()
      this.startSeatStatusRefresh()
    }
  },
  beforeDestroy() {
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer)
    }
    if (this.seatLockTimer) {
      clearInterval(this.seatLockTimer)
    }
    this.releaseSelectedSeats()
  },
  methods: {
    loadSeats() {
      this.seats = generateSeats(this.scheduleId)
      this.syncLockedSeats()
    },
    syncLockedSeats() {
      const lockedSeats = seatLockManager.getLockedSeats(this.scheduleId)
      const soldSeats = seatLockManager.getSoldSeats(this.scheduleId)
      this.seats.forEach(row => {
        row.forEach(seat => {
          if (seat.status === 'available' || seat.status === 'locked') {
            const isSold = soldSeats.some(
              ss => ss.row === seat.row && ss.col === seat.col
            )
            if (isSold) {
              seat.status = 'occupied'
              const idx = this.selectedSeats.findIndex(s => s.id === seat.id)
              if (idx > -1) {
                this.selectedSeats.splice(idx, 1)
              }
              return
            }
            
            const isLocked = lockedSeats.some(
              ls => ls.row === seat.row && ls.col === seat.col && ls.orderId !== 'temp'
            )
            if (isLocked && seat.status === 'available') {
              seat.status = 'locked'
            }
          }
        })
      })
    },
    startSeatStatusRefresh() {
      this.refreshTimer = setInterval(() => {
        this.syncLockedSeats()
      }, 5000)
    },
    getSeatClass(seat) {
      return {
        available: seat.status === 'available',
        selected: seat.status === 'selected',
        occupied: seat.status === 'occupied',
        locked: seat.status === 'locked'
      }
    },
    toggleSeat(seat) {
      if (seat.status === 'occupied') {
        this.$message.warning('该座位已售出，请选择其他座位')
        return
      }
      
      if (seat.status === 'locked') {
        this.$message.warning('该座位正在锁定中，请选择其他座位')
        return
      }
      
      if (seatLockManager.isSeatSold(this.scheduleId, seat.row, seat.col)) {
        seat.status = 'occupied'
        this.$message.warning('该座位已售出，请选择其他座位')
        return
      }
      
      if (seatLockManager.isSeatLocked(this.scheduleId, seat.row, seat.col)) {
        const lockInfo = seatLockManager.getLockInfo(this.scheduleId, seat.row, seat.col)
        if (lockInfo && lockInfo.orderId !== 'temp-' + this._uid) {
          seat.status = 'locked'
          this.$message.warning('该座位刚刚被其他用户锁定，请选择其他座位')
          return
        }
      }
      
      const index = this.selectedSeats.findIndex(s => s.id === seat.id)
      if (index > -1) {
        this.selectedSeats.splice(index, 1)
        seat.status = 'available'
        seatLockManager.unlockSeat(this.scheduleId, seat.row, seat.col)
        
        if (this.selectedSeats.length === 0) {
          this.stopLockTimer()
        }
      } else {
        if (this.selectedSeats.length >= 5) {
          this.$message.warning('最多选择5个座位')
          return
        }
        
        if (this.isProcessing) {
          return
        }
        
        this.isProcessing = true
        
        setTimeout(() => {
          if (seatLockManager.isSeatSold(this.scheduleId, seat.row, seat.col)) {
            seat.status = 'occupied'
            this.$message.warning('该座位已售出，请选择其他座位')
            this.isProcessing = false
            return
          }
          
          const lockInfo = seatLockManager.getLockInfo(this.scheduleId, seat.row, seat.col)
          if (lockInfo && lockInfo.orderId !== 'temp-' + this._uid) {
            seat.status = 'locked'
            this.$message.warning('该座位刚刚被其他用户锁定，请选择其他座位')
            this.isProcessing = false
            return
          }
          
          this.selectedSeats.push(seat)
          seat.status = 'selected'
          seatLockManager.lockSeat(this.scheduleId, seat.row, seat.col, 'temp-' + this._uid)
          
          if (this.selectedSeats.length === 1) {
            this.startLockTimer()
          }
          
          this.isProcessing = false
        }, 100)
      }
    },
    startLockTimer() {
      this.stopLockTimer()
      this.remainingLockTime = 15 * 60
      this.seatLockTimer = setInterval(() => {
        this.remainingLockTime--
        if (this.remainingLockTime <= 0) {
          this.stopLockTimer()
          this.releaseSelectedSeats()
          this.$message.warning('选座已超时，请重新选择座位')
        }
      }, 1000)
    },
    stopLockTimer() {
      if (this.seatLockTimer) {
        clearInterval(this.seatLockTimer)
        this.seatLockTimer = null
      }
      this.remainingLockTime = 0
    },
    releaseSelectedSeats() {
      this.selectedSeats.forEach(seat => {
        seatLockManager.unlockSeat(this.scheduleId, seat.row, seat.col)
        seat.status = 'available'
      })
      this.selectedSeats = []
      this.stopLockTimer()
    },
    goBack() {
      this.releaseSelectedSeats()
      if (this.movie) {
        this.$router.push(`/schedule/${this.movie.id}`)
      } else {
        this.$router.push('/')
      }
    },
    sendCode() {
      if (!this.orderForm.phone || !/^1[3-9]\d{9}$/.test(this.orderForm.phone)) {
        this.$message.error('请输入正确的手机号')
        return
      }
      this.countdown = 60
      this.$message.success('验证码已发送')
      const timer = setInterval(() => {
        this.countdown--
        if (this.countdown <= 0) {
          clearInterval(timer)
        }
      }, 1000)
    },
    submitOrder() {
      this.$refs.orderForm.validate(valid => {
        if (valid) {
          const conflictSeats = []
          this.selectedSeats.forEach(seat => {
            if (seatLockManager.isSeatSold(this.scheduleId, seat.row, seat.col)) {
              conflictSeats.push(`${seat.row}排${seat.col}座`)
              return
            }
            const lockInfo = seatLockManager.getLockInfo(this.scheduleId, seat.row, seat.col)
            if (lockInfo && lockInfo.orderId !== 'temp-' + this._uid) {
              conflictSeats.push(`${seat.row}排${seat.col}座`)
            }
          })
          
          if (conflictSeats.length > 0) {
            this.$message.error(`座位 ${conflictSeats.join('、')} 已被其他用户锁定，请重新选择`)
            this.syncLockedSeats()
            return
          }
          
          const orderId = 'ORD' + Date.now()
          seatLockManager.lockSeatsByOrder(
            this.scheduleId,
            this.selectedSeats,
            orderId
          )
          
          const now = new Date()
          const createTime = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')} ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`
          
          const newOrder = {
            id: orderId,
            movieTitle: this.movie.title,
            cinemaName: this.cinema.name,
            hall: this.schedule.hall,
            sessionTime: `${this.schedule.date} ${this.schedule.time}`,
            seats: this.selectedSeats.map(s => `${s.row}排${s.col}座`),
            quantity: this.selectedSeats.length,
            totalPrice: this.totalPrice,
            status: 'paid',
            createTime: createTime,
            phone: this.orderForm.phone
          }
          
          orderStore.addOrder(newOrder)
          
          this.selectedSeats.forEach(seat => {
            seat.status = 'occupied'
          })
          
          this.stopLockTimer()
          this.selectedSeats = []
          
          this.$message.success('购票成功！座位已锁定')
          this.showOrderDialog = false
          
          this.$router.push('/orders')
        }
      })
    },
    resetForm() {
      this.$refs.orderForm?.resetFields()
    }
  }
}
</script>

<style scoped>
.back-btn {
  margin-bottom: 20px;
}

.movie-info-card {
  padding: 20px;
}

.movie-info {
  display: flex;
  gap: 20px;
}

.movie-poster {
  width: 80px;
  height: 110px;
  object-fit: cover;
  border-radius: 4px;
}

.info-content h2 {
  margin: 0 0 10px 0;
  font-size: 20px;
}

.info-content p {
  margin: 5px 0;
  color: #606266;
}

.seat-container {
  text-align: center;
  padding: 20px 0;
}

.screen {
  width: 60%;
  height: 30px;
  line-height: 30px;
  background: linear-gradient(to bottom, #409eff, #66b1ff);
  color: white;
  border-radius: 0 0 50% 50%;
  margin: 0 auto 40px;
  font-weight: 600;
}

.seat-legend {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-bottom: 30px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.seat-demo {
  width: 28px;
  height: 28px;
  border-radius: 4px 4px 8px 8px;
}

.seat-demo.available {
  background: #f0f9eb;
  border: 1px solid #e1f3d8;
}

.seat-demo.selected {
  background: #409eff;
  border: 1px solid #409eff;
}

.seat-demo.occupied {
  background: #909399;
  border: 1px solid #909399;
}

.seat-demo.locked {
  background: #f56c6c;
  border: 1px solid #f56c6c;
  opacity: 0.7;
}

.seats-wrapper {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.row-numbers {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding-top: 0;
}

.row-number {
  width: 28px;
  height: 28px;
  line-height: 28px;
  text-align: center;
  font-size: 12px;
  color: #909399;
}

.seats-grid {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.seat-row {
  display: flex;
  gap: 6px;
  justify-content: center;
}

.seat {
  width: 28px;
  height: 28px;
  line-height: 28px;
  text-align: center;
  font-size: 12px;
  border-radius: 4px 4px 8px 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.seat.available {
  background: #f0f9eb;
  border: 1px solid #e1f3d8;
  color: #67c23a;
}

.seat.available:hover {
  background: #67c23a;
  color: white;
}

.seat.selected {
  background: #409eff;
  border: 1px solid #409eff;
  color: white;
}

.seat.occupied {
  background: #909399;
  border: 1px solid #909399;
  color: #c0c4cc;
  cursor: not-allowed;
  pointer-events: none;
}

.seat.locked {
  background: #f56c6c;
  border: 1px solid #f56c6c;
  color: white;
  cursor: not-allowed;
  opacity: 0.7;
  pointer-events: none;
}

.selection-summary {
  margin-top: 30px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}

.selected-seats {
  margin-bottom: 15px;
  line-height: 32px;
}

.seat-tags {
  margin-left: 10px;
}

.seat-tags .el-tag {
  margin-right: 8px;
  margin-bottom: 8px;
}

.lock-timer {
  padding: 10px 15px;
  background: #fff7e6;
  border: 1px solid #ffd591;
  border-radius: 4px;
  margin-bottom: 15px;
  color: #fa8c16;
  font-size: 14px;
}

.lock-timer .time {
  font-weight: 600;
  font-size: 16px;
  margin: 0 4px;
}

.total-price {
  margin-bottom: 20px;
}

.total-price .price-symbol {
  color: #f56c6c;
}

.total-price .price {
  font-size: 28px;
  font-weight: 600;
  color: #f56c6c;
}

.total-price .count {
  color: #909399;
  margin-left: 10px;
}

.confirm-btn {
  width: 100%;
}
</style>
