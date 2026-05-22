<template>
  <div class="movie-list">
    <h1 class="page-title">正在热映</h1>
    
    <el-card class="search-card mb-20 card-shadow">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索电影名称"
        prefix-icon="el-icon-search"
        clearable
        style="width: 100%; max-width: 400px"
      >
      </el-input>
    </el-card>
    
    <div class="movies-grid">
      <el-card 
        v-for="movie in filteredMovies" 
        :key="movie.id"
        class="movie-card card-shadow"
        shadow="hover"
        @click.native="showMovieDetail(movie)"
      >
        <img :src="movie.poster" class="movie-poster" :alt="movie.title" />
        <div class="movie-info">
          <h3 class="movie-title">{{ movie.title }}</h3>
          <div class="movie-rating">
            <i class="el-icon-star-on"></i>
            <span>{{ movie.rating }}</span>
          </div>
          <p class="movie-type">{{ movie.type }}</p>
          <p class="movie-duration">{{ movie.duration }}分钟</p>
        </div>
        <el-button 
          type="primary" 
          class="buy-btn"
          @click.stop="goToSchedule(movie.id)"
        >
          购票
        </el-button>
      </el-card>
    </div>
    
    <el-dialog
      :title="selectedMovie?.title"
      :visible.sync="detailDialogVisible"
      width="700px"
    >
      <div v-if="selectedMovie" class="movie-detail">
        <div class="detail-left">
          <img :src="selectedMovie.poster" :alt="selectedMovie.title" />
        </div>
        <div class="detail-right">
          <p><strong>评分：</strong>{{ selectedMovie.rating }}</p>
          <p><strong>类型：</strong>{{ selectedMovie.type }}</p>
          <p><strong>导演：</strong>{{ selectedMovie.director }}</p>
          <p><strong>主演：</strong>{{ selectedMovie.actors }}</p>
          <p><strong>片长：</strong>{{ selectedMovie.duration }}分钟</p>
          <p><strong>上映日期：</strong>{{ selectedMovie.releaseDate }}</p>
          <p><strong>剧情简介：</strong></p>
          <p class="description">{{ selectedMovie.description }}</p>
        </div>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="detailDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="goToSchedule(selectedMovie.id)">立即购票</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { movies } from '@/data/mock.js'

export default {
  name: 'MovieList',
  data() {
    return {
      movies,
      searchKeyword: '',
      detailDialogVisible: false,
      selectedMovie: null
    }
  },
  computed: {
    filteredMovies() {
      if (!this.searchKeyword) return this.movies
      return this.movies.filter(movie => 
        movie.title.includes(this.searchKeyword)
      )
    }
  },
  methods: {
    showMovieDetail(movie) {
      this.selectedMovie = movie
      this.detailDialogVisible = true
    },
    goToSchedule(movieId) {
      this.detailDialogVisible = false
      this.$router.push(`/schedule/${movieId}`)
    }
  }
}
</script>

<style scoped>
.search-card {
  padding: 20px;
}

.movies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}

.movie-card {
  cursor: pointer;
  transition: transform 0.3s;
  overflow: hidden;
}

.movie-card:hover {
  transform: translateY(-5px);
}

.movie-poster {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border-radius: 4px;
}

.movie-info {
  padding: 15px 0;
}

.movie-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 10px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.movie-rating {
  color: #e6a23c;
  font-size: 14px;
  margin-bottom: 8px;
}

.movie-rating i {
  margin-right: 4px;
}

.movie-type,
.movie-duration {
  font-size: 13px;
  color: #909399;
  margin: 4px 0;
}

.buy-btn {
  width: 100%;
}

.movie-detail {
  display: flex;
  gap: 20px;
}

.detail-left img {
  width: 200px;
  height: 280px;
  object-fit: cover;
  border-radius: 4px;
}

.detail-right p {
  margin: 10px 0;
  line-height: 1.6;
  color: #606266;
}

.detail-right .description {
  text-indent: 2em;
}
</style>
