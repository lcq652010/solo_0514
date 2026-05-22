<template>
  <div class="learning-progress">
    <h1 class="page-title">学习进度</h1>
    
    <div v-if="progressList.length === 0" class="page-card">
      <div class="empty-state">
        <i class="el-icon-document"></i>
        <p>暂无学习记录，快去选择课程开始学习吧！</p>
        <el-button type="primary" @click="$router.push('/courses')">去选课</el-button>
      </div>
    </div>

    <div v-else>
      <div v-for="course in computedProgressList" :key="course.courseId" class="page-card progress-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
          <h3 style="font-size: 18px; color: #303133;">{{ course.courseName }}</h3>
          <div style="color: #909399; font-size: 14px;">
            已学课时：{{ formatStudyTime(course.completedHours) }} / {{ formatStudyTime(course.totalHours) }}
            &nbsp;&nbsp;|&nbsp;&nbsp;
            最近学习：{{ course.lastStudyDate }}
          </div>
        </div>

        <div class="progress-header">
          <span class="progress-title">学习进度</span>
          <span 
            class="progress-percent"
            :class="{
              'progress-high': course.progress >= 80,
              'progress-medium': course.progress >= 50 && course.progress < 80,
              'progress-low': course.progress < 50
            }"
          >
            {{ course.progress }}%
          </span>
        </div>
        <div class="custom-progress-bar">
          <div 
            class="progress-fill"
            :class="{
              'progress-high': course.progress >= 80,
              'progress-medium': course.progress >= 50 && course.progress < 80,
              'progress-low': course.progress < 50
            }"
            :style="{ width: course.progress + '%' }"
          >
            <div class="progress-shine"></div>
          </div>
        </div>

        <div class="progress-stats">
          <span class="stat-item">
            <i class="el-icon-collection"></i>
            已完成 {{ course.completedChapters }} / {{ course.totalChapters }} 个章节
          </span>
          <span class="stat-divider">|</span>
          <span class="stat-item">
            <i class="el-icon-time"></i>
            课时进度：{{ course.completedHours }} / {{ course.totalHours }} 分钟
          </span>
        </div>

        <el-table
          :data="course.chapters"
          border
          style="width: 100%"
          row-key="id"
        >
          <el-table-column prop="id" label="序号" width="80" align="center"></el-table-column>
          <el-table-column prop="name" label="章节名称" min-width="300"></el-table-column>
          <el-table-column prop="duration" label="时长" width="120" align="center">
            <template slot-scope="scope">
              {{ scope.row.duration }} 分钟
            </template>
          </el-table-column>
          <el-table-column prop="status" label="学习状态" width="120" align="center">
            <template slot-scope="scope">
              <el-tag v-if="scope.row.status === 'completed'" type="success" size="small">
                <i class="el-icon-check"></i> 已完成
              </el-tag>
              <el-tag v-else-if="scope.row.status === 'in_progress'" type="warning" size="small">
                <i class="el-icon-loading"></i> 学习中
              </el-tag>
              <el-tag v-else type="info" size="small">
                未开始
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" align="center">
            <template slot-scope="scope">
              <el-button
                size="mini"
                type="primary"
                @click="handleContinue(course, scope.row)"
              >
                {{ scope.row.status === 'completed' ? '复习' : '继续学习' }}
              </el-button>
              <el-button
                v-if="scope.row.status !== 'completed'"
                size="mini"
                type="success"
                @click="markChapterComplete(course, scope.row)"
              >
                标记完成
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script>
import { progressData } from '@/mock/data'
import { EventBus } from '@/utils/eventBus'

export default {
  name: 'LearningProgress',
  data() {
    return {
      progressList: progressData
    }
  },
  computed: {
    computedProgressList() {
      return this.progressList.map(course => {
        const totalHours = course.chapters.reduce((sum, ch) => sum + ch.duration, 0)
        const completedHours = course.chapters
          .filter(ch => ch.status === 'completed')
          .reduce((sum, ch) => sum + ch.duration, 0)
        const progress = Math.round((completedHours / totalHours) * 100)
        
        return {
          ...course,
          totalHours,
          completedHours,
          progress,
          completedChapters: course.chapters.filter(ch => ch.status === 'completed').length,
          totalChapters: course.chapters.length
        }
      })
    }
  },
  methods: {
    formatStudyTime(minutes) {
      const hours = Math.floor(minutes / 60)
      const mins = minutes % 60
      if (hours > 0) {
        return `${hours}小时${mins > 0 ? mins + '分钟' : ''}`
      }
      return `${mins}分钟`
    },
    handleContinue(course, chapter) {
      if (chapter.status !== 'completed') {
        chapter.status = 'in_progress'
      }
      this.$message({
        message: `正在进入「${course.courseName}」-「${chapter.name}」...`,
        type: 'info'
      })
      EventBus.$emit('progressUpdated')
    },
    updateChapterStatus(course, chapter, status) {
      chapter.status = status
      this.$message.success('学习状态已更新！')
      EventBus.$emit('progressUpdated')
    },
    markChapterComplete(course, chapter) {
      if (chapter.status !== 'completed') {
        chapter.status = 'completed'
        this.$message.success(`「${chapter.name}」已标记为完成！`)
        EventBus.$emit('progressUpdated')
      }
    }
  }
}
</script>

<style scoped>
.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.progress-title {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

.progress-percent {
  font-size: 24px;
  font-weight: bold;
}

.progress-percent.progress-high {
  color: #67C23A;
}

.progress-percent.progress-medium {
  color: #E6A23C;
}

.progress-percent.progress-low {
  color: #409EFF;
}

.custom-progress-bar {
  height: 20px;
  background: #E4E7ED;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 15px;
}

.progress-fill {
  height: 100%;
  border-radius: 10px;
  position: relative;
  transition: width 0.6s ease-out;
}

.progress-fill.progress-high {
  background: linear-gradient(90deg, #67C23A, #85CE61, #A0D98A);
}

.progress-fill.progress-medium {
  background: linear-gradient(90deg, #E6A23C, #F3D19E, #F8E3C6);
}

.progress-fill.progress-low {
  background: linear-gradient(90deg, #409EFF, #66B1FF, #99CCFF);
}

.progress-shine {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 60px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.5), transparent);
  animation: shine 2s infinite linear;
}

@keyframes shine {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.progress-stats {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  color: #606266;
  font-size: 14px;
  margin-bottom: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
}

.stat-item i {
  margin-right: 5px;
  color: #909399;
}

.stat-divider {
  color: #DCDFE6;
}
</style>
