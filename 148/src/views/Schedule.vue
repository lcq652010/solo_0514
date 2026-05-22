<template>
  <div class="schedule-page">
    <el-button icon="el-icon-arrow-left" @click="$router.push('/')" class="back-btn">
      返回电影列表
    </el-button>
    
    <div v-if="movie" class="movie-header card-shadow mb-20">
      <img :src="movie.poster" :alt="movie.title" class="movie-poster" />
      <div class="movie-info">
        <h1 class="page-title">{{ movie.title }}</h1>
        <p><strong>评分：</strong>{{ movie.rating }}</p>
        <p><strong>类型：</strong>{{ movie.type }}</p>
        <p><strong>片长：</strong>{{ movie.duration }}分钟</p>
      </div>
    </div>
    
    <el-card class="card-shadow mb-20">
      <h3>选择影院</h3>
      <el-radio-group v-model="selectedCinemaId" class="cinema-list">
        <el-radio-button 
          v-for="cinema in cinemas" 
          :key="cinema.id" 
          :label="cinema.id"
        >
          <div class="cinema-name">{{ cinema.name }}</div>
          <div class="cinema-address">{{ cinema.address }}</div>
          <div class="cinema-distance">{{ cinema.distance }}</div>
        </el-radio-button>
      </el-radio-group>
    </el-card>
    
    <el-card class="card-shadow mb-20">
      <h3>选择日期</h3>
      <el-radio-group v-model="selectedDate" class="date-list">
        <el-radio-button 
          v-for="date in dateList" 
          :key="date.value" 
          :label="date.value"
        >
          <div class="date-week">{{ date.week }}</div>
          <div class="date-day">{{ date.day }}</div>
        </el-radio-button>
      </el-radio-group>
    </el-card>
    
    <el-card class="card-shadow">
      <h3>选择场次</h3>
      <div v-if="filteredSchedules.length === 0" class="no-schedule">
        <el-empty description="暂无场次" />
      </div>
      <div v-else class="schedule-list">
        <div 
          v-for="schedule in filteredSchedules" 
          :key="schedule.id"
          class="schedule-item"
          @click="selectSchedule(schedule)"
        >
          <div class="schedule-time">
            <span class="start-time">{{ schedule.time }}</span>
            <span class="end-time">{{ schedule.endTime }}散场</span>
          </div>
          <div class="schedule-hall">{{ schedule.hall }}</div>
          <div class="schedule-info">
            <span class="tag">{{ schedule.language }}</span>
            <span class="tag">{{ schedule.dimension }}</span>
          </div>
          <div class="schedule-price">
            <span class="price-symbol">¥</span>
            <span class="price">{{ schedule.price }}</span>
          </div>
          <el-button type="primary" size="small" class="select-btn">选座</el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { movies, cinemas, schedules } from '@/data/mock.js'

export default {
  name: 'Schedule',
  data() {
    return {
      movie: null,
      cinemas,
      schedules,
      selectedCinemaId: 1,
      selectedDate: this.formatDate(new Date())
    }
  },
  computed: {
    dateList() {
      const dates = []
      for (let i = 0; i < 7; i++) {
        const date = new Date()
        date.setDate(date.getDate() + i)
        const weeks = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
        dates.push({
          value: this.formatDate(date),
          week: i === 0 ? '今天' : weeks[date.getDay()],
          day: `${date.getMonth() + 1}/${date.getDate()}`
        })
      }
      return dates
    },
    filteredSchedules() {
      return this.schedules.filter(s => 
        s.movieId === this.movie?.id &&
        s.cinemaId === this.selectedCinemaId &&
        s.date === this.selectedDate
      )
    }
  },
  mounted() {
    const movieId = parseInt(this.$route.params.movieId)
    this.movie = movies.find(m => m.id === movieId)
  },
  methods: {
    formatDate(date) {
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    },
    selectSchedule(schedule) {
      this.$router.push(`/seats/${schedule.id}`)
    }
  }
}
</script>

<style scoped>
.back-btn {
  margin-bottom: 20px;
}

.movie-header {
  display: flex;
  gap: 20px;
  padding: 20px;
}

.movie-poster {
  width: 120px;
  height: 170px;
  object-fit: cover;
  border-radius: 4px;
}

.movie-info {
  flex: 1;
}

.movie-info p {
  margin: 8px 0;
  color: #606266;
}

.cinema-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 15px;
}

.cinema-list .el-radio-button {
  margin-right: 0;
  margin-bottom: 10px;
}

.cinema-list .el-radio-button__inner {
  padding: 15px 20px;
  white-space: normal;
  text-align: left;
  width: 220px;
}

.cinema-name {
  font-weight: 600;
  color: #303133;
  margin-bottom: 5px;
}

.cinema-address {
  font-size: 12px;
  color: #909399;
  margin-bottom: 3px;
}

.cinema-distance {
  font-size: 12px;
  color: #409eff;
}

.date-list {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.date-list .el-radio-button__inner {
  padding: 12px 20px;
  text-align: center;
}

.date-week {
  font-weight: 600;
  margin-bottom: 3px;
}

.date-day {
  font-size: 12px;
  color: #909399;
}

.schedule-list {
  margin-top: 15px;
}

.schedule-item {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.3s;
}

.schedule-item:hover {
  border-color: #409eff;
  box-shadow: 0 2px 12px 0 rgba(64, 158, 255, 0.2);
}

.schedule-time {
  width: 150px;
}

.start-time {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.end-time {
  font-size: 12px;
  color: #909399;
  margin-left: 10px;
}

.schedule-hall {
  flex: 1;
  color: #606266;
}

.schedule-info {
  width: 120px;
}

.tag {
  display: inline-block;
  padding: 2px 8px;
  background: #ecf5ff;
  color: #409eff;
  border-radius: 4px;
  font-size: 12px;
  margin-right: 5px;
}

.schedule-price {
  width: 100px;
  text-align: right;
}

.price-symbol {
  font-size: 14px;
  color: #f56c6c;
}

.price {
  font-size: 24px;
  font-weight: 600;
  color: #f56c6c;
}

.select-btn {
  margin-left: 20px;
}

.no-schedule {
  padding: 50px 0;
}
</style>
