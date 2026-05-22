<template>
  <div class="calling-page">
    <div class="calling-header">
      <div class="header-title">
        <h1>政务服务中心</h1>
        <p>请留意叫号信息，到相应窗口办理业务</p>
      </div>
      <div class="header-time">
        <div class="date">{{ currentDate }}</div>
        <div class="time">{{ currentTime }}</div>
      </div>
    </div>

    <div class="calling-main">
      <div class="current-calling" :class="{ highlight: isBlinking }">
        <div class="calling-icon">
          <i class="el-icon-microphone"></i>
        </div>
        <div class="calling-label">正在呼叫</div>
        <div class="calling-number" :class="{ blink: isBlinking }">{{ currentCalling.number }}</div>
        <div class="calling-window">{{ currentCalling.window }}</div>
        <div class="calling-tip">请 {{ currentCalling.number }} 号顾客到 {{ currentCalling.window }} 办理业务</div>
      </div>

      <div class="calling-actions">
        <el-button type="primary" size="large" @click="handleCallNext" :loading="callLoading">
          <i class="el-icon-microphone"></i> 呼叫下一位
        </el-button>
        <el-button type="success" size="large" @click="handleRecall">
          <i class="el-icon-refresh"></i> 重复呼叫
        </el-button>
        <el-button type="danger" size="large" @click="handlePass">
          <i class="el-icon-close"></i> 过号
        </el-button>
        <el-button type="warning" size="large" @click="handlePause">
          <i class="el-icon-video-pause"></i> 暂停叫号
        </el-button>
      </div>
    </div>

    <el-row :gutter="20" class="calling-info">
      <el-col :span="8">
        <el-card class="info-card">
          <div slot="header" class="card-header">
            <i class="el-icon-s-order"></i> 等待队列
          </div>
          <div class="waiting-list">
            <div 
              v-for="(item, index) in waitingList" 
              :key="index" 
              class="waiting-item"
              :class="{ 'next-item': index === 0 }">
              <span class="waiting-number">{{ item.number }}</span>
              <span class="waiting-type">{{ item.type }}</span>
              <el-tag v-if="index === 0" type="success" size="mini">下一位</el-tag>
            </div>
            <el-empty v-if="waitingList.length === 0" description="暂无等待人员" :image-size="80"></el-empty>
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card class="info-card">
          <div slot="header" class="card-header">
            <i class="el-icon-s-release"></i> 过号列表
          </div>
          <div class="passed-list">
            <div 
              v-for="(item, index) in passedList" 
              :key="index" 
              class="passed-item">
              <span class="passed-number">{{ item.number }}</span>
              <span class="passed-type">{{ item.type }}</span>
              <el-tag type="info" size="mini">已过号</el-tag>
            </div>
            <el-empty v-if="passedList.length === 0" description="暂无过号" :image-size="80"></el-empty>
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card class="info-card">
          <div slot="header" class="card-header">
            <i class="el-icon-time"></i> 今日统计
          </div>
          <div class="stats-grid">
            <div class="stat-box">
              <div class="stat-value">{{ todayStats.total }}</div>
              <div class="stat-name">总取号数</div>
            </div>
            <div class="stat-box">
              <div class="stat-value">{{ todayStats.served }}</div>
              <div class="stat-name">已办理</div>
            </div>
            <div class="stat-box">
              <div class="stat-value">{{ todayStats.waiting }}</div>
              <div class="stat-name">等待中</div>
            </div>
            <div class="stat-box">
              <div class="stat-value">{{ todayStats.passed }}</div>
              <div class="stat-name">过号数</div>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card class="info-card">
          <div slot="header" class="card-header">
            <i class="el-icon-set-up"></i> 窗口状态
          </div>
          <div class="window-status">
            <div v-for="window in windows" :key="window.id" class="window-item">
              <span class="window-name">{{ window.name }}</span>
              <el-tag :type="window.status === '正常' ? 'success' : 'info'" size="small">
                {{ window.status }}
              </el-tag>
              <span class="window-current" v-if="window.current">
                当前：{{ window.current }}
              </span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog
      title="人工呼叫"
      :visible.sync="manualDialogVisible"
      width="400px">
      <el-form :model="manualForm" label-width="80px">
        <el-form-item label="排队号">
          <el-input v-model="manualForm.number" placeholder="请输入排队号"></el-input>
        </el-form-item>
        <el-form-item label="窗口号">
          <el-select v-model="manualForm.window" placeholder="请选择窗口" style="width: 100%">
            <el-option label="1号窗口" value="1号窗口"></el-option>
            <el-option label="2号窗口" value="2号窗口"></el-option>
            <el-option label="3号窗口" value="3号窗口"></el-option>
            <el-option label="4号窗口" value="4号窗口"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="manualDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleManualCall">确认呼叫</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'Calling',
  data() {
    return {
      currentCalling: {
        number: 'A028',
        window: '1号窗口'
      },
      isBlinking: true,
      callLoading: false,
      manualDialogVisible: false,
      manualForm: {
        number: '',
        window: ''
      },
      waitingList: [
        { number: 'A029', type: '综合业务' },
        { number: 'A030', type: '综合业务' },
        { number: 'B015', type: '户政业务' },
        { number: 'C022', type: '社保业务' },
        { number: 'D008', type: '不动产' }
      ],
      todayStats: {
        total: 156,
        served: 128,
        waiting: 25,
        passed: 3
      },
      passedList: [],
      windows: [
        { id: 1, name: '1号窗口', status: '正常', current: 'A028' },
        { id: 2, name: '2号窗口', status: '正常', current: 'B014' },
        { id: 3, name: '3号窗口', status: '正常', current: 'C021' },
        { id: 4, name: '4号窗口', status: '暂停', current: '' }
      ],
      timer: null,
      refreshTimer: null
    }
  },
  computed: {
    currentDate() {
      const now = new Date()
      const weekDays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
      return `${now.getFullYear()}年${now.getMonth() + 1}月${now.getDate()}日 ${weekDays[now.getDay()]}`
    },
    currentTime() {
      const now = new Date()
      return `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`
    }
  },
  mounted() {
    this.timer = setInterval(() => {
      this.$forceUpdate()
    }, 1000)
    this.startAutoRefresh()
    this.subscribeNewTickets()
  },
  beforeDestroy() {
    if (this.timer) {
      clearInterval(this.timer)
    }
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer)
    }
  },
  methods: {
    startAutoRefresh() {
      this.refreshTimer = setInterval(() => {
        this.$bus.$emit('refreshQueue')
      }, 5000)
    },
    subscribeNewTickets() {
      this.$bus.$on('newTicket', (ticket) => {
        this.waitingList.push({
          number: ticket.number,
          type: ticket.businessType
        })
        this.todayStats.waiting++
        this.$message.info(`新号 ${ticket.number} 已加入队列`)
      })
    },
    handleCallNext() {
      this.callLoading = true
      setTimeout(() => {
        this.callLoading = false
        if (this.waitingList.length > 0) {
          const next = this.waitingList.shift()
          this.currentCalling = {
            number: next.number,
            window: '1号窗口'
          }
          this.todayStats.served++
          this.todayStats.waiting--
          this.isBlinking = true
          setTimeout(() => {
            this.isBlinking = false
          }, 3000)
          this.$message.success(`已呼叫 ${next.number}`)
        } else {
          this.$message.warning('暂无等待人员')
        }
      }, 1000)
    },
    handlePass() {
      this.$confirm(`确认 ${this.currentCalling.number} 号过号吗？过号后将移至过号列表`, '提示', {
        confirmButtonText: '确认过号',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const passedItem = {
          number: this.currentCalling.number,
          type: '综合业务',
          passTime: this.currentTime
        }
        this.passedList.unshift(passedItem)
        this.todayStats.passed++
        this.isBlinking = false
        this.$message.success(`${this.currentCalling.number} 号已过号`)
        
        if (this.waitingList.length > 0) {
          const next = this.waitingList.shift()
          this.currentCalling = {
            number: next.number,
            window: '1号窗口'
          }
          this.todayStats.waiting--
          this.isBlinking = true
          setTimeout(() => {
            this.isBlinking = false
          }, 3000)
        } else {
          this.currentCalling = {
            number: '-',
            window: '等待取号'
          }
        }
      }).catch(() => {})
    },
    handleRecall() {
      this.isBlinking = true
      this.$message.info(`重复呼叫 ${this.currentCalling.number}`)
      setTimeout(() => {
        this.isBlinking = false
      }, 3000)
    },
    handlePause() {
      this.$confirm('确认暂停叫号服务？', '提示', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message.success('叫号服务已暂停')
      }).catch(() => {})
    },
    handleManualCall() {
      if (!this.manualForm.number || !this.manualForm.window) {
        this.$message.warning('请填写完整信息')
        return
      }
      this.currentCalling = {
        number: this.manualForm.number,
        window: this.manualForm.window
      }
      this.isBlinking = true
      setTimeout(() => {
        this.isBlinking = false
      }, 3000)
      this.manualDialogVisible = false
      this.$message.success(`已呼叫 ${this.manualForm.number}`)
    }
  }
}
</script>

<style scoped>
.calling-page {
  height: 100%;
  overflow-y: auto;
}

.calling-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  padding: 30px 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 8px;
  margin-bottom: 20px;
}

.header-title h1 {
  font-size: 32px;
  margin-bottom: 10px;
}

.header-title p {
  font-size: 16px;
  opacity: 0.9;
}

.header-time {
  text-align: right;
}

.header-time .date {
  font-size: 16px;
  opacity: 0.9;
}

.header-time .time {
  font-size: 48px;
  font-weight: bold;
  font-family: 'Courier New', monospace;
}

.calling-main {
  display: flex;
  gap: 30px;
  margin-bottom: 20px;
}

.current-calling {
  flex: 1;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  border-radius: 20px;
  padding: 50px 40px;
  text-align: center;
  color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  box-shadow: 0 8px 30px rgba(240, 147, 251, 0.3);
}

.current-calling.highlight {
  animation: highlightPulse 1.5s infinite ease-in-out;
  transform: scale(1.02);
}

@keyframes highlightPulse {
  0%, 100% {
    box-shadow: 0 8px 30px rgba(240, 147, 251, 0.3), 0 0 0 0 rgba(245, 87, 108, 0.7);
  }
  50% {
    box-shadow: 0 8px 30px rgba(240, 147, 251, 0.3), 0 0 0 20px rgba(245, 87, 108, 0);
  }
}

.calling-icon {
  font-size: 48px;
  margin-bottom: 15px;
  animation: bounce 2s infinite ease-in-out;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.calling-label {
  font-size: 24px;
  opacity: 0.95;
  margin-bottom: 25px;
  font-weight: 500;
  letter-spacing: 4px;
}

.calling-number {
  font-size: 120px;
  font-weight: bold;
  letter-spacing: 30px;
  margin-bottom: 25px;
  text-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
  padding: 20px 0;
}

.calling-number.blink {
  animation: numberBlink 0.6s infinite alternate;
}

@keyframes numberBlink {
  from { 
    opacity: 1; 
    transform: scale(1);
    text-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
  }
  to { 
    opacity: 0.9; 
    transform: scale(1.08);
    text-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
  }
}

.calling-window {
  font-size: 36px;
  font-weight: 600;
  margin-bottom: 25px;
  background: rgba(255, 255, 255, 0.25);
  padding: 12px 40px;
  border-radius: 50px;
}

.calling-tip {
  font-size: 20px;
  opacity: 0.98;
  background: rgba(255, 255, 255, 0.2);
  padding: 18px 40px;
  border-radius: 40px;
  display: inline-block;
  font-weight: 500;
}

.calling-actions {
  display: flex;
  flex-direction: column;
  gap: 15px;
  justify-content: center;
}

.calling-actions .el-button {
  width: 180px;
  padding: 20px 0;
  font-size: 16px;
}

.card-header {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

.waiting-list {
  max-height: 300px;
  overflow-y: auto;
}

.waiting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 15px;
  border-bottom: 1px solid #f0f0f0;
  transition: all 0.3s ease;
}

.waiting-item.next-item {
  background: linear-gradient(90deg, #e6f7ff 0%, #fff 100%);
  border-left: 4px solid #409EFF;
  border-radius: 4px;
}

.waiting-item:last-child {
  border-bottom: none;
}

.waiting-number {
  font-size: 18px;
  font-weight: 600;
  color: #409EFF;
}

.waiting-type {
  color: #909399;
  font-size: 14px;
}

.passed-list {
  max-height: 300px;
  overflow-y: auto;
}

.passed-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 15px;
  border-bottom: 1px solid #f0f0f0;
  opacity: 0.6;
  filter: grayscale(50%);
  background: #f5f5f5;
}

.passed-number {
  font-size: 18px;
  font-weight: 600;
  color: #909399;
  text-decoration: line-through;
}

.passed-type {
  color: #909399;
  font-size: 14px;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.stat-box {
  background: #f5f7fa;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 5px;
}

.stat-name {
  font-size: 14px;
  color: #909399;
}

.window-item {
  display: flex;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
}

.window-item:last-child {
  border-bottom: none;
}

.window-name {
  width: 80px;
  font-weight: 500;
}

.window-current {
  margin-left: auto;
  color: #67c23a;
  font-size: 14px;
}
</style>
