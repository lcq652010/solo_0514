<template>
  <div class="page-container">
    <h2 class="page-title">活动列表</h2>
    
    <el-card class="search-card mb-20">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="活动名称">
          <el-input v-model="searchForm.keyword" placeholder="请输入活动名称" clearable></el-input>
        </el-form-item>
        <el-form-item label="活动状态">
          <el-select v-model="searchForm.status" placeholder="请选择" clearable>
            <el-option label="即将开始" value="upcoming"></el-option>
            <el-option label="进行中" value="ongoing"></el-option>
            <el-option label="已结束" value="ended"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-row :gutter="20">
      <el-col :span="8" v-for="activity in filteredActivities" :key="activity.id">
        <el-card class="activity-card card-shadow mb-20" :body-style="{ padding: '0' }">
          <img :src="activity.coverImage" class="activity-cover" alt="活动封面">
          <div class="activity-info">
            <h3 class="activity-title">{{ activity.title }}</h3>
            <p class="activity-desc">{{ activity.description }}</p>
            <div class="activity-meta">
              <span class="meta-item">
                <i class="el-icon-date"></i> {{ activity.date }} {{ activity.time }}
              </span>
              <span class="meta-item">
                <i class="el-icon-location-outline"></i> {{ activity.location }}
              </span>
              <span class="meta-item">
                <i class="el-icon-user"></i> {{ activity.currentParticipants }}/{{ activity.maxParticipants }}人
              </span>
            </div>
            <div class="activity-status">
              <el-tag :type="getStatusType(activity.status)">{{ getStatusText(activity.status) }}</el-tag>
            </div>
            <div class="activity-actions">
              <el-button size="small" type="primary" @click="goToDetail(activity.id)">查看详情</el-button>
              <el-button size="small" @click="goToRegister(activity.id)" :disabled="activity.currentParticipants >= activity.maxParticipants">
                {{ activity.currentParticipants >= activity.maxParticipants ? '已满员' : '立即报名' }}
              </el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-empty v-if="filteredActivities.length === 0" description="暂无活动数据"></el-empty>
  </div>
</template>

<script>
import { activities } from '../mock/data'

export default {
  name: 'ActivityList',
  data() {
    return {
      activities,
      searchForm: {
        keyword: '',
        status: ''
      }
    }
  },
  computed: {
    filteredActivities() {
      return this.activities.filter(item => {
        const keywordMatch = !this.searchForm.keyword || item.title.includes(this.searchForm.keyword)
        const statusMatch = !this.searchForm.status || item.status === this.searchForm.status
        return keywordMatch && statusMatch
      })
    }
  },
  methods: {
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
    goToDetail(id) {
      this.$router.push(`/activity/${id}`)
    },
    goToRegister(id) {
      this.$router.push(`/register/${id}`)
    },
    handleSearch() {
      this.$message.success('搜索完成')
    },
    handleReset() {
      this.searchForm.keyword = ''
      this.searchForm.status = ''
    }
  }
}
</script>

<style scoped>
.search-card {
  background: white;
}

.activity-card {
  transition: transform 0.3s;
}

.activity-card:hover {
  transform: translateY(-5px);
}

.activity-cover {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 4px 4px 0 0;
}

.activity-info {
  padding: 15px;
}

.activity-title {
  font-size: 16px;
  color: #303133;
  margin: 0 0 10px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.activity-desc {
  font-size: 13px;
  color: #606266;
  margin: 0 0 15px 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.5;
  height: 39px;
}

.activity-meta {
  margin-bottom: 15px;
}

.meta-item {
  display: block;
  font-size: 12px;
  color: #909399;
  margin-bottom: 8px;
}

.meta-item i {
  margin-right: 5px;
}

.activity-status {
  margin-bottom: 15px;
}

.activity-actions {
  display: flex;
  gap: 10px;
}
</style>
