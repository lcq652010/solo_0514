<template>
  <div class="page-container">
    <h1 class="page-title">施工进度</h1>
    
    <div class="card-wrapper" v-if="currentRecord">
      <div class="record-info">
        <div class="status-banner" :class="getStatusClass(currentRecord.status)">
          <i :class="getStatusIcon(currentRecord.status)"></i>
          <span>{{ getStatusText(currentRecord.status) }}</span>
        </div>
        <el-descriptions title="预约信息" :column="2" border>
          <el-descriptions-item label="预约编号">NO.{{ currentRecord.id }}</el-descriptions-item>
          <el-descriptions-item label="车主姓名">{{ currentRecord.ownerName }}</el-descriptions-item>
          <el-descriptions-item label="车牌号码">{{ currentRecord.carNumber }}</el-descriptions-item>
          <el-descriptions-item label="车辆品牌">{{ currentRecord.carBrand }}</el-descriptions-item>
          <el-descriptions-item label="保养套餐">{{ getPackageName(currentRecord.packageId) }}</el-descriptions-item>
          <el-descriptions-item label="维修工位">{{ getStationName(currentRecord.stationId) }}</el-descriptions-item>
          <el-descriptions-item label="服务顾问">{{ currentRecord.consultant }}</el-descriptions-item>
          <el-descriptions-item label="预约时间">{{ formatDate(currentRecord.reserveDate) }} {{ currentRecord.reserveTime }}</el-descriptions-item>
        </el-descriptions>
      </div>
      
      <div class="progress-section">
        <h3 class="section-title">
          <i class="el-icon-time"></i> 施工进度
        </h3>
        
        <el-steps :active="currentStep" finish-status="success" direction="vertical" class="steps-wrapper">
          <el-step title="预约确认">
            <template slot="description">
              <div class="step-content">
                <p>您的预约已成功确认</p>
                <span class="step-time">{{ currentRecord.status >= 1 ? getStepTime(0) : '--' }}</span>
              </div>
            </template>
          </el-step>
          
          <el-step title="车辆入场">
            <template slot="description">
              <div class="step-content">
                <p>车辆已进入施工车间</p>
                <span class="step-time">{{ currentRecord.status >= 2 ? getStepTime(1) : '--' }}</span>
              </div>
            </template>
          </el-step>
          
          <el-step title="保养施工中">
            <template slot="description">
              <div class="step-content">
                <p v-if="currentRecord.status >= 2">技师正在进行保养作业</p>
                <p v-else>等待施工...</p>
                <span class="step-time">{{ currentRecord.status >= 2 ? getStepTime(2) : '--' }}</span>
              </div>
            </template>
          </el-step>
          
          <el-step title="质量检测">
            <template slot="description">
              <div class="step-content">
                <p v-if="currentRecord.status >= 3">质量检测已通过</p>
                <p v-else>等待检测...</p>
                <span class="step-time">{{ currentRecord.status >= 3 ? getStepTime(3) : '--' }}</span>
              </div>
            </template>
          </el-step>
          
          <el-step title="完工交车">
            <template slot="description">
              <div class="step-content">
                <p v-if="currentRecord.status >= 3">车辆已完工，可前往取车</p>
                <p v-else>敬请期待...</p>
                <span class="step-time">{{ currentRecord.status >= 3 ? getStepTime(4) : '--' }}</span>
              </div>
            </template>
          </el-step>
        </el-steps>
      </div>
      
      <div class="progress-bar-section">
        <h3 class="section-title">
          <i class="el-icon-pie-chart"></i> 总体进度
        </h3>
        <el-progress 
          :percentage="progressPercentage" 
          :status="progressStatus"
          :stroke-width="20"
        ></el-progress>
        <div class="progress-text">
          完成度：{{ progressPercentage }}%
        </div>
      </div>
      
      <div class="actions-section">
        <div class="auto-refresh-tip">
          <i class="el-icon-refresh"></i> 实时同步中 | 最后更新：{{ lastUpdateTime }}
        </div>
        <el-button type="primary" @click="goBack">
          <i class="el-icon-arrow-left"></i> 返回列表
        </el-button>
        <el-button @click="simulateUpdate" v-if="currentRecord && currentRecord.status < 3">
          <i class="el-icon-setting"></i> 模拟状态更新
        </el-button>
        <el-button @click="contactService">
          <i class="el-icon-phone"></i> 联系客服
        </el-button>
      </div>
    </div>
    
    <div class="card-wrapper" v-else>
      <el-empty description="请从预约记录选择查看进度"></el-empty>
      <div style="text-align: center; margin-top: 20px;">
        <el-button type="primary" @click="$router.push('/records')">前往预约记录</el-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Progress',
  data() {
    return {
      records: [],
      currentRecord: null,
      pollingTimer: null,
      lastUpdateTime: '',
      packages: [
        { id: 1, name: '基础保养套餐' },
        { id: 2, name: '标准保养套餐' },
        { id: 3, name: '尊享保养套餐' },
        { id: 4, name: '刹车系统养护' },
        { id: 5, name: '空调系统养护' },
        { id: 6, name: '漆面养护套餐' }
      ],
      stations: [
        { id: 1, name: '1号工位 - 机修' },
        { id: 2, name: '2号工位 - 机修' },
        { id: 3, name: '3号工位 - 美容' },
        { id: 4, name: '4号工位 - 美容' },
        { id: 5, name: '5号工位 - 快修' }
      ]
    }
  },
  computed: {
    currentStep() {
      if (!this.currentRecord) return 0
      const status = this.currentRecord.status
      if (status === 0) return 0
      if (status === 1) return 1
      if (status === 2) return 3
      if (status >= 3) return 5
      return 0
    },
    progressPercentage() {
      if (!this.currentRecord) return 0
      const status = this.currentRecord.status
      if (status === 0) return 10
      if (status === 1) return 30
      if (status === 2) return 65
      if (status >= 3) return 100
      return 0
    },
    progressStatus() {
      if (this.progressPercentage >= 100) return 'success'
      return ''
    }
  },
  mounted() {
    this.loadRecords()
    this.startPolling()
  },
  beforeDestroy() {
    this.stopPolling()
  },
  methods: {
    loadRecords() {
      this.records = JSON.parse(localStorage.getItem('reserveRecords') || '[]')
      const recordId = this.$route.query.id
      if (recordId) {
        this.currentRecord = this.records.find(r => r.id == recordId) || this.records[0]
      } else if (this.records.length > 0) {
        this.currentRecord = this.records.find(r => r.status >= 1 && r.status <= 2) || this.records[0]
      }
      this.lastUpdateTime = new Date().toLocaleTimeString()
    },
    startPolling() {
      this.pollingTimer = setInterval(() => {
        this.loadRecords()
      }, 3000)
    },
    stopPolling() {
      if (this.pollingTimer) {
        clearInterval(this.pollingTimer)
        this.pollingTimer = null
      }
    },
    getPackageName(id) {
      const pkg = this.packages.find(p => p.id === id)
      return pkg ? pkg.name : '未知套餐'
    },
    getStationName(id) {
      const station = this.stations.find(s => s.id === id)
      return station ? station.name : '未分配'
    },
    getStatusText(status) {
      const statusMap = {
        0: '待确认',
        1: '待施工',
        2: '施工中',
        3: '已完工',
        4: '已取消'
      }
      return statusMap[status] || '未知'
    },
    getStatusClass(status) {
      const classMap = {
        0: 'status-warning',
        1: 'status-info',
        2: 'status-primary',
        3: 'status-success',
        4: 'status-danger'
      }
      return classMap[status] || 'status-info'
    },
    getStatusIcon(status) {
      const iconMap = {
        0: 'el-icon-time',
        1: 'el-icon-wait',
        2: 'el-icon-loading',
        3: 'el-icon-success',
        4: 'el-icon-error'
      }
      return iconMap[status] || 'el-icon-info'
    },
    formatDate(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
    },
    getStepTime(stepIndex) {
      const baseTime = new Date(this.currentRecord.createTime)
      baseTime.setMinutes(baseTime.getMinutes() + stepIndex * 30)
      return `${baseTime.getHours().toString().padStart(2, '0')}:${baseTime.getMinutes().toString().padStart(2, '0')}`
    },
    goBack() {
      this.$router.push('/records')
    },
    contactService() {
      this.$alert('客服热线：400-888-8888\n服务时间：9:00-18:00', '联系客服')
    },
    simulateUpdate() {
      if (this.currentRecord && this.currentRecord.status < 3) {
        const index = this.records.findIndex(r => r.id === this.currentRecord.id)
        if (index > -1) {
          this.records[index].status += 1
          localStorage.setItem('reserveRecords', JSON.stringify(this.records))
          this.loadRecords()
          this.$message.success('状态已更新！')
        }
      }
    }
  }
}
</script>

<style scoped>
.record-info {
  margin-bottom: 30px;
}

.status-banner {
  padding: 15px 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 16px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 10px;
}

.status-warning {
  background: #fdf6ec;
  color: #e6a23c;
}

.status-info {
  background: #ecf5ff;
  color: #409eff;
}

.status-primary {
  background: #f0f9eb;
  color: #67c23a;
}

.status-success {
  background: #f0f9eb;
  color: #67c23a;
}

.status-danger {
  background: #fef0f0;
  color: #f56c6c;
}

.section-title {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
}

.section-title i {
  color: #409eff;
  margin-right: 8px;
}

.progress-section {
  margin-bottom: 40px;
}

.steps-wrapper {
  padding: 20px 40px;
}

.step-content {
  padding: 10px 0;
}

.step-content p {
  color: #606266;
  margin: 0 0 8px 0;
}

.step-time {
  font-size: 12px;
  color: #909399;
}

.progress-bar-section {
  margin-bottom: 30px;
  padding: 0 20px;
}

.progress-text {
  text-align: center;
  margin-top: 15px;
  font-size: 16px;
  color: #606266;
  font-weight: 500;
}

.actions-section {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}

.auto-refresh-tip {
  font-size: 12px;
  color: #909399;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
}

.auto-refresh-tip i {
  animation: spin 2s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.actions-section .el-button {
  margin: 0 10px;
  padding: 12px 30px;
}
</style>
