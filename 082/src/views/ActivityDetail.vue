<template>
  <div class="page-container">
    <el-button @click="goBack" class="back-btn">
      <i class="el-icon-arrow-left"></i> 返回列表
    </el-button>

    <el-card v-if="activity" class="detail-card card-shadow">
      <div class="detail-header">
        <img :src="activity.coverImage" class="detail-cover" alt="活动封面">
        <div class="detail-info">
          <h2 class="detail-title">{{ activity.title }}</h2>
          <div class="detail-meta">
            <el-tag :type="getStatusType(activity.status)" size="medium">
              {{ getStatusText(activity.status) }}
            </el-tag>
            <span class="meta-text">
              <i class="el-icon-date"></i> {{ activity.date }} {{ activity.time }}
            </span>
            <span class="meta-text">
              <i class="el-icon-location-outline"></i> {{ activity.location }}
            </span>
            <span class="meta-text">
              <i class="el-icon-s-custom"></i> {{ activity.organizer }}
            </span>
          </div>
          <div class="participant-info">
            <el-progress :percentage="participantPercentage" :status="progressStatus"></el-progress>
            <span class="participant-count">已报名 {{ activity.currentParticipants }}/{{ activity.maxParticipants }} 人</span>
          </div>
          <div class="detail-actions">
            <el-button type="primary" size="large" @click="goToRegister" :disabled="activity.currentParticipants >= activity.maxParticipants">
              {{ activity.currentParticipants >= activity.maxParticipants ? '名额已满' : '立即报名' }}
            </el-button>
            <el-button size="large" @click="goToCheckIn">签到入口</el-button>
          </div>
        </div>
      </div>

      <el-divider></el-divider>

      <div class="detail-content">
        <h3 class="content-title">活动详情</h3>
        <div class="content-text">
          <p v-for="(paragraph, index) in contentParagraphs" :key="index">{{ paragraph }}</p>
        </div>
      </div>
    </el-card>

    <el-empty v-else description="活动不存在"></el-empty>
  </div>
</template>

<script>
import { activities } from '../mock/data'

export default {
  name: 'ActivityDetail',
  data() {
    return {
      activity: null
    }
  },
  computed: {
    contentParagraphs() {
      if (!this.activity) return []
      return this.activity.content.split('\n').filter(p => p.trim())
    },
    participantPercentage() {
      if (!this.activity) return 0
      return Math.round((this.activity.currentParticipants / this.activity.maxParticipants) * 100)
    },
    progressStatus() {
      if (this.participantPercentage >= 100) return 'exception'
      if (this.participantPercentage >= 80) return 'warning'
      return undefined
    }
  },
  mounted() {
    this.loadActivity()
  },
  methods: {
    loadActivity() {
      const id = parseInt(this.$route.params.id)
      this.activity = activities.find(item => item.id === id)
    },
    getStatusType(status) {
      const map = {
        upcoming: 'success',
        ongoing: 'warning',
        ended: 'info'
      }
      return map[status] || 'info'
    },
    getStatusText(status) {
      const map = {
        upcoming: '即将开始',
        ongoing: '进行中',
        ended: '已结束'
      }
      return map[status] || status
    },
    goBack() {
      this.$router.push('/')
    },
    goToRegister() {
      this.$router.push(`/register/${this.activity.id}`)
    },
    goToCheckIn() {
      this.$router.push(`/checkin/${this.activity.id}`)
    }
  }
}
</script>

<style scoped>
.back-btn {
  margin-bottom: 20px;
}

.detail-card {
  background: white;
}

.detail-header {
  display: flex;
  gap: 30px;
}

.detail-cover {
  width: 400px;
  height: 250px;
  object-fit: cover;
  border-radius: 8px;
}

.detail-info {
  flex: 1;
}

.detail-title {
  font-size: 24px;
  color: #303133;
  margin: 0 0 20px 0;
}

.detail-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 25px;
  align-items: center;
}

.meta-text {
  font-size: 14px;
  color: #606266;
}

.meta-text i {
  margin-right: 5px;
}

.participant-info {
  margin-bottom: 25px;
}

.participant-count {
  display: block;
  text-align: right;
  font-size: 13px;
  color: #909399;
  margin-top: 8px;
}

.detail-actions {
  display: flex;
  gap: 15px;
}

.content-title {
  font-size: 18px;
  color: #303133;
  margin: 0 0 15px 0;
}

.content-text {
  line-height: 2;
  color: #606266;
}

.content-text p {
  margin-bottom: 10px;
}
</style>
