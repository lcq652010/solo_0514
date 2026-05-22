<template>
  <div class="page-container">
    <div class="header-section">
      <el-button type="text" icon="el-icon-arrow-left" @click="goBack">返回</el-button>
      <h2 class="page-title">维修进度</h2>
    </div>

    <el-card v-loading="loading" class="info-card">
      <div slot="header">
        <span>报修信息</span>
      </div>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="报修编号">{{ repairInfo.id }}</el-descriptions-item>
        <el-descriptions-item label="报修标题">{{ repairInfo.title }}</el-descriptions-item>
        <el-descriptions-item label="所属楼栋">{{ repairInfo.buildingName }}</el-descriptions-item>
        <el-descriptions-item label="报修类型">{{ repairInfo.typeName }}</el-descriptions-item>
        <el-descriptions-item label="紧急程度">
          <el-tag :type="getUrgencyTagType(repairInfo.urgency)" size="small">{{ repairInfo.urgencyName }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="维修地址" :span="2">{{ repairInfo.address }}</el-descriptions-item>
        <el-descriptions-item label="联系人">{{ repairInfo.contact }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ repairInfo.phone }}</el-descriptions-item>
        <el-descriptions-item label="问题描述" :span="2">{{ repairInfo.description }}</el-descriptions-item>
        <el-descriptions-item label="当前状态">
          <el-tag :color="getStatusColor(repairInfo.status)" size="small">{{ getStatusLabel(repairInfo.status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="维修人员" v-if="repairInfo.worker">{{ repairInfo.worker }} ({{ repairInfo.workerPhone }})</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-card class="timeline-card">
      <div slot="header">
        <span>进度时间轴</span>
      </div>
      <el-timeline>
        <el-timeline-item
          v-for="(activity, index) in activities"
          :key="index"
          :timestamp="activity.time"
          :type="activity.type"
          :color="activity.color"
          :size="activity.size"
          :icon="activity.icon"
        >
          <div class="timeline-content">
            <h4>{{ activity.title }}</h4>
            <p v-if="activity.description">{{ activity.description }}</p>
            <p v-if="activity.user" class="user-info">操作人：{{ activity.user }}</p>
          </div>
        </el-timeline-item>
      </el-timeline>
    </el-card>

    <el-card class="operation-card" v-if="repairInfo.status === '1'">
      <div slot="header">
        <span>操作</span>
      </div>
      <el-button type="primary" size="large" @click="startRepair">开始维修</el-button>
      <el-button type="success" size="large" @click="completeRepair">维修完成</el-button>
    </el-card>

    <el-card class="operation-card" v-if="repairInfo.status === '2'">
      <div slot="header">
        <span>操作</span>
      </div>
      <el-button type="success" size="large" @click="completeRepair">维修完成</el-button>
    </el-card>
  </div>
</template>

<script>
import { RepairStore } from '../store/repairStore'
import { EventBus, Events } from '../utils/eventBus'

export default {
  name: 'Progress',
  data() {
    return {
      loading: false,
      activities: []
    }
  },
  computed: {
    repairId() {
      return this.$route.params.id
    },
    repairInfo() {
      return RepairStore.getRepairById(this.repairId) || {}
    }
  },
  mounted() {
    this.loadRepairInfo()
    this.listenToStatusUpdates()
  },
  beforeDestroy() {
    EventBus.$off(Events.REPAIR_STATUS_UPDATED)
  },
  watch: {
    repairId() {
      this.loadRepairInfo()
    },
    'repairInfo.status'() {
      this.generateTimeline()
    }
  },
  methods: {
    listenToStatusUpdates() {
      EventBus.$on(Events.REPAIR_STATUS_UPDATED, (data) => {
        if (data.id === this.repairId) {
          this.$message.info(`状态已更新为：${RepairStore.getStatusLabel(data.status)}`)
        }
      })
    },
    loadRepairInfo() {
      this.loading = true
      setTimeout(() => {
        this.generateTimeline()
        this.loading = false
      }, 300)
    },
    generateTimeline() {
      if (!this.repairInfo) return
      
      this.activities = []
      
      this.activities.push({
        title: '提交报修申请',
        description: this.repairInfo.description,
        time: this.repairInfo.createTime,
        type: 'primary',
        color: '#409EFF',
        size: 'large',
        icon: 'el-icon-document',
        user: this.repairInfo.contact
      })

      if (this.repairInfo.dispatchTime) {
        this.activities.push({
          title: '已派单',
          description: `维修人员：${this.repairInfo.worker}（${this.repairInfo.workerPhone}）`,
          time: this.repairInfo.dispatchTime,
          type: 'warning',
          color: '#E6A23C',
          size: 'large',
          icon: 'el-icon-s-custom',
          user: '物业管理员'
        })
      }

      if (this.repairInfo.startTime) {
        this.activities.push({
          title: '维修人员开始工作',
          description: '维修人员已到达现场，开始维修工作',
          time: this.repairInfo.startTime,
          type: 'info',
          color: '#909399',
          size: 'large',
          icon: 'el-icon-s-tools',
          user: this.repairInfo.worker
        })
      }

      if (this.repairInfo.completeTime) {
        this.activities.push({
          title: '维修完成',
          description: '维修工作已完成，请业主验收确认',
          time: this.repairInfo.completeTime,
          type: 'success',
          color: '#67C23A',
          size: 'large',
          icon: 'el-icon-success',
          user: this.repairInfo.worker
        })
      }

      this.activities.reverse()
    },
    getStatusLabel(status) {
      return RepairStore.getStatusLabel(status)
    },
    getStatusColor(status) {
      return RepairStore.getStatusColor(status)
    },
    getUrgencyTagType(urgency) {
      const map = { '1': '', '2': 'warning', '3': 'danger' }
      return map[urgency] || ''
    },
    startRepair() {
      this.$confirm('确认开始维修吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        RepairStore.startRepair(this.repairId)
        this.$message.success('已开始维修！')
      }).catch(() => {})
    },
    completeRepair() {
      this.$confirm('确认维修完成吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'success'
      }).then(() => {
        RepairStore.completeRepair(this.repairId)
        this.$message.success('维修已完成！')
      }).catch(() => {})
    },
    goBack() {
      this.$router.back()
    }
  }
}
</script>

<style scoped>
.header-section {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.header-section .el-button {
  margin-right: 15px;
  font-size: 14px;
}

.header-section .page-title {
  margin: 0;
  padding: 0;
  border: none;
}

.info-card,
.timeline-card,
.operation-card {
  margin-bottom: 20px;
}

.timeline-content h4 {
  font-size: 14px;
  font-weight: 500;
  margin: 0 0 8px 0;
  color: #303133;
}

.timeline-content p {
  margin: 4px 0;
  font-size: 13px;
  color: #606266;
}

.timeline-content .user-info {
  color: #909399;
  font-size: 12px;
}

.operation-card .el-button {
  margin-right: 10px;
}
</style>
