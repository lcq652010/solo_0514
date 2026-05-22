<template>
  <div class="my-courses">
    <h1 class="page-title">我的课程</h1>
    <div class="page-card">
      <div class="filter-section">
        <el-form :inline="true" :model="filterForm" class="filter-form">
          <el-form-item label="课程分类">
            <el-select v-model="filterForm.category" placeholder="请选择分类" clearable>
              <el-option label="全部" value=""></el-option>
              <el-option label="前端开发" value="前端开发"></el-option>
              <el-option label="后端开发" value="后端开发"></el-option>
              <el-option label="数据科学" value="数据科学"></el-option>
              <el-option label="设计" value="设计"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="学习进度">
            <el-select v-model="filterForm.progress" placeholder="请选择进度" clearable>
              <el-option label="全部" value=""></el-option>
              <el-option label="0-30%" value="0-30"></el-option>
              <el-option label="30-60%" value="30-60"></el-option>
              <el-option label="60-100%" value="60-100"></el-option>
              <el-option label="已完成(100%)" value="100"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="学习状态">
            <el-select v-model="filterForm.status" placeholder="请选择状态" clearable>
              <el-option label="全部" value=""></el-option>
              <el-option label="学习中" value="learning"></el-option>
              <el-option label="已完成" value="completed"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleFilter">
              <i class="el-icon-search"></i> 筛选
            </el-button>
            <el-button @click="handleResetFilter">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <div class="filter-tags" v-if="hasActiveFilters">
        <span class="filter-label">当前筛选：</span>
        <el-tag v-if="filterForm.category" size="small" closable @close="filterForm.category = ''">
          分类：{{ filterForm.category }}
        </el-tag>
        <el-tag v-if="filterForm.progress" size="small" closable @close="filterForm.progress = ''">
          进度：{{ getProgressLabel(filterForm.progress) }}
        </el-tag>
        <el-tag v-if="filterForm.status" size="small" closable @close="filterForm.status = ''">
          状态：{{ filterForm.status === 'learning' ? '学习中' : '已完成' }}
        </el-tag>
        <el-button type="text" size="small" @click="handleResetFilter">清除全部</el-button>
      </div>

      <div v-if="filteredCourses.length === 0" class="empty-state">
        <i class="el-icon-notebook-2"></i>
        <p>暂无相关课程，快去报名吧！</p>
        <el-button type="primary" @click="$router.push('/courses')">去选课</el-button>
      </div>

      <el-row :gutter="20" v-else>
        <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="course in paginatedCourses" :key="course.id">
          <el-card class="course-card" shadow="hover">
            <div slot="header" class="card-header">
              <span>{{ course.name }}</span>
              <div class="header-tags">
                <el-tag
                  :type="course.progress === 100 ? 'success' : 'warning'"
                  size="small"
                >
                  {{ course.progress === 100 ? '已完成' : '学习中' }}
                </el-tag>
                <el-tag size="small" type="info">{{ course.category }}</el-tag>
              </div>
            </div>

            <div class="course-info">
              <p><i class="el-icon-user"></i> 讲师：{{ course.teacher }}</p>
              <p><i class="el-icon-date"></i> 报名时间：{{ course.enrollTime }}</p>
              <p><i class="el-icon-time"></i> 最近学习：{{ course.lastLearnTime }}</p>
            </div>

            <div class="progress-section">
              <div class="progress-label">
                <span>学习进度</span>
                <span 
                  class="progress-value"
                  :class="{
                    'progress-high': course.progress >= 80,
                    'progress-medium': course.progress >= 50 && course.progress < 80,
                    'progress-low': course.progress < 50
                  }"
                >
                  {{ course.progress }}%
                </span>
              </div>
              <div class="progress-bar-wrapper">
                <div class="progress-bar-container">
                  <div 
                    class="progress-bar-fill"
                    :class="{
                      'progress-high': course.progress >= 80,
                      'progress-medium': course.progress >= 50 && course.progress < 80,
                      'progress-low': course.progress < 50
                    }"
                    :style="{ width: course.progress + '%' }"
                  >
                    <div class="progress-bar-glow"></div>
                  </div>
                </div>
              </div>
              <div class="chapter-info">
                <span><i class="el-icon-collection"></i> 已完成 {{ course.completedChapters }} / {{ course.totalChapters }} 章</span>
                <span class="chapter-divider">|</span>
                <span><i class="el-icon-time"></i> 已学课时：{{ course.completedHours }} / {{ course.totalHours }} 分钟</span>
              </div>
            </div>

            <div class="card-actions">
              <el-button type="primary" style="flex: 1;" @click="handleContinue(course)">
                <i class="el-icon-video-play"></i>
                {{ course.progress === 100 ? '复习课程' : '继续学习' }}
              </el-button>
              <el-button style="flex: 1;" @click="handleHomework(course)">
                <i class="el-icon-document"></i>
                查看作业
              </el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <div class="pagination-container" v-if="filteredCourses.length > 0">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.currentPage"
          :page-sizes="[4, 8, 12, 20]"
          :page-size="pagination.pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
        ></el-pagination>
      </div>
    </div>
  </div>
</template>

<script>
import { myCourses, courses, progressData } from '@/mock/data'
import { EventBus } from '@/utils/eventBus'

export default {
  name: 'MyCourses',
  data() {
    return {
      myCourses: myCourses,
      allCourses: courses,
      progressData: progressData,
      filterForm: {
        category: '',
        progress: '',
        status: ''
      },
      pagination: {
        currentPage: 1,
        pageSize: 8,
        total: 0
      },
      lastUpdateTime: null
    }
  },
  computed: {
    hasActiveFilters() {
      return this.filterForm.category || this.filterForm.progress || this.filterForm.status
    },
    coursesWithProgress() {
      return this.myCourses.map(course => {
        const courseDetail = this.allCourses.find(c => c.id === course.id)
        const progress = this.progressData.find(p => p.courseId === course.id)
        
        if (progress) {
          const totalHours = progress.chapters.reduce((sum, ch) => sum + ch.duration, 0)
          const completedHours = progress.chapters
            .filter(ch => ch.status === 'completed')
            .reduce((sum, ch) => sum + ch.duration, 0)
          const calculatedProgress = Math.round((completedHours / totalHours) * 100)
          
          return {
            ...course,
            category: courseDetail?.category || '其他',
            progress: calculatedProgress,
            totalHours,
            completedHours,
            status: calculatedProgress === 100 ? 'completed' : 'learning'
          }
        }
        return {
          ...course,
          category: courseDetail?.category || '其他',
          totalHours: 0,
          completedHours: 0
        }
      })
    },
    filteredCourses() {
      let result = this.coursesWithProgress
      
      if (this.filterForm.category) {
        result = result.filter(c => c.category === this.filterForm.category)
      }
      
      if (this.filterForm.progress) {
        if (this.filterForm.progress === '0-30') {
          result = result.filter(c => c.progress >= 0 && c.progress < 30)
        } else if (this.filterForm.progress === '30-60') {
          result = result.filter(c => c.progress >= 30 && c.progress < 60)
        } else if (this.filterForm.progress === '60-100') {
          result = result.filter(c => c.progress >= 60 && c.progress < 100)
        } else if (this.filterForm.progress === '100') {
          result = result.filter(c => c.progress === 100)
        }
      }
      
      if (this.filterForm.status) {
        result = result.filter(c => c.status === this.filterForm.status)
      }
      
      return result
    },
    paginatedCourses() {
      const { currentPage, pageSize } = this.pagination
      const start = (currentPage - 1) * pageSize
      const end = start + pageSize
      return this.filteredCourses.slice(start, end)
    }
  },
  watch: {
    filteredCourses: {
      handler(val) {
        this.pagination.total = val.length
      },
      immediate: true
    }
  },
  created() {
    EventBus.$on('progressUpdated', () => {
      this.lastUpdateTime = new Date().toLocaleString()
      this.$forceUpdate()
    })
  },
  beforeDestroy() {
    EventBus.$off('progressUpdated')
  },
  activated() {
    if (this.lastUpdateTime) {
      this.$message({
        message: '进度数据已自动刷新',
        type: 'info',
        duration: 1500
      })
    }
  },
  methods: {
    getProgressLabel(value) {
      const map = {
        '0-30': '0-30%',
        '30-60': '30-60%',
        '60-100': '60-100%',
        '100': '已完成(100%)'
      }
      return map[value] || value
    },
    handleFilter() {
      this.pagination.currentPage = 1
      this.$message.success('筛选条件已应用')
    },
    handleResetFilter() {
      this.filterForm = {
        category: '',
        progress: '',
        status: ''
      }
      this.pagination.currentPage = 1
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
    },
    handleContinue(course) {
      this.$message({
        message: `正在进入「${course.name}」...`,
        type: 'info'
      })
      this.$router.push('/progress')
    },
    handleHomework(course) {
      this.$message({
        message: `查看「${course.name}」的作业...`,
        type: 'info'
      })
      this.$router.push('/homework')
    }
  }
}
</script>

<style scoped>
.filter-section {
  background: #f5f7fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 15px;
}

.filter-form {
  margin: 0;
}

.filter-tags {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 20px;
  padding: 12px 15px;
  background: #ecf5ff;
  border-radius: 8px;
}

.filter-label {
  color: #409EFF;
  font-size: 14px;
  font-weight: 500;
}

.course-card {
  margin-bottom: 20px;
  transition: transform 0.3s, box-shadow 0.3s;
}

.course-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  color: #303133;
}

.header-tags {
  display: flex;
  gap: 5px;
}

.course-info {
  color: #606266;
  font-size: 14px;
  margin-bottom: 15px;
}

.course-info p {
  margin: 8px 0;
  display: flex;
  align-items: center;
}

.course-info i {
  margin-right: 8px;
  color: #909399;
}

.progress-section {
  background: #f5f7fa;
  padding: 15px;
  border-radius: 8px;
}

.progress-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  font-size: 14px;
  color: #606266;
  font-weight: 500;
}

.progress-value {
  font-weight: bold;
  font-size: 18px;
}

.progress-value.progress-high {
  color: #67C23A;
}

.progress-value.progress-medium {
  color: #E6A23C;
}

.progress-value.progress-low {
  color: #409EFF;
}

.progress-bar-wrapper {
  margin-bottom: 12px;
}

.progress-bar-container {
  height: 12px;
  background: #E4E7ED;
  border-radius: 6px;
  overflow: hidden;
  position: relative;
}

.progress-bar-fill {
  height: 100%;
  border-radius: 6px;
  position: relative;
  transition: width 0.5s ease-out;
}

.progress-bar-fill.progress-high {
  background: linear-gradient(90deg, #67C23A, #85CE61);
}

.progress-bar-fill.progress-medium {
  background: linear-gradient(90deg, #E6A23C, #F3D19E);
}

.progress-bar-fill.progress-low {
  background: linear-gradient(90deg, #409EFF, #66B1FF);
}

.progress-bar-glow {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 40px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4));
  animation: glow 2s infinite;
}

@keyframes glow {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 0.8; }
}

.chapter-info {
  margin-top: 10px;
  font-size: 12px;
  color: #909399;
  text-align: right;
  display: flex;
  justify-content: flex-end;
  flex-wrap: wrap;
  gap: 8px;
}

.chapter-info i {
  margin-right: 4px;
}

.chapter-divider {
  color: #DCDFE6;
}

.card-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style>
