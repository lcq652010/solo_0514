<template>
  <div class="classes">
    <div class="page-title">团课展示</div>
    <el-row :gutter="20">
      <el-col :span="8" v-for="cls in classList" :key="cls.id">
        <el-card class="class-card" shadow="hover">
          <img :src="cls.image" class="class-image" slot="cover">
          <div class="class-info">
            <h3>{{ cls.name }}</h3>
            <div class="class-meta">
              <span><i class="el-icon-user"></i> {{ cls.trainer }}</span>
              <span><i class="el-icon-time"></i> {{ cls.duration }}</span>
              <span><i class="el-icon-sunny"></i> {{ cls.difficulty }}</span>
            </div>
            <p class="class-desc">{{ cls.description }}</p>
            <div class="class-schedule">
              <div class="schedule-title">课程安排</div>
              <el-tag size="small" v-for="schedule in cls.schedules" :key="schedule" style="margin: 5px 5px 5px 0;">
                {{ schedule }}
              </el-tag>
            </div>
            <div class="class-actions">
              <span class="price">¥{{ cls.price }}/节</span>
              <el-button type="primary" size="small" @click="bookClass(cls)">立即预约</el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'Classes',
  data() {
    return {
      classList: [
        {
          id: 1,
          name: '动感单车',
          image: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
          trainer: '李教练',
          duration: '45分钟',
          difficulty: '中级',
          price: 88,
          description: '动感单车是一种高强度有氧训练，配合音乐节奏，燃脂效果显著。',
          schedules: ['周一 10:00', '周三 19:00', '周五 18:00', '周六 09:00']
        },
        {
          id: 2,
          name: '哈他瑜伽',
          image: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
          trainer: '王教练',
          duration: '60分钟',
          difficulty: '初级',
          price: 128,
          description: '哈他瑜伽通过体式练习，帮助放松身心，提升柔韧性。',
          schedules: ['周二 09:00', '周四 15:00', '周六 14:00', '周日 10:00']
        },
        {
          id: 3,
          name: '搏击操',
          image: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
          trainer: '陈教练',
          duration: '50分钟',
          difficulty: '高级',
          price: 98,
          description: '结合拳击与有氧运动，释放压力，塑造完美身材。',
          schedules: ['周一 19:00', '周三 10:00', '周五 19:00', '周日 15:00']
        },
        {
          id: 4,
          name: '普拉提',
          image: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
          trainer: '王教练',
          duration: '55分钟',
          difficulty: '中级',
          price: 138,
          description: '核心力量训练，改善体态，塑造修长身材。',
          schedules: ['周二 15:00', '周四 09:00', '周六 10:00']
        },
        {
          id: 5,
          name: 'HIIT燃脂',
          image: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
          trainer: '赵教练',
          duration: '30分钟',
          difficulty: '高级',
          price: 78,
          description: '高强度间歇训练，短时高效，持续燃脂。',
          schedules: ['周一 18:00', '周三 18:00', '周五 10:00', '周六 16:00']
        },
        {
          id: 6,
          name: '尊巴舞',
          image: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
          trainer: '李教练',
          duration: '50分钟',
          difficulty: '初级',
          price: 88,
          description: '热情洋溢的舞蹈健身，在欢乐中燃烧卡路里。',
          schedules: ['周二 19:00', '周四 19:00', '周六 19:00', '周日 16:00']
        }
      ]
    }
  },
  methods: {
    bookClass(cls) {
      this.$message.success(`您已预约${cls.name}课程，请留意上课时间！`)
    }
  }
}
</script>

<style scoped>
.classes {
  padding: 0;
}

.class-card {
  margin-bottom: 20px;
}

.class-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.class-info h3 {
  font-size: 18px;
  font-weight: 500;
  margin: 0 0 10px 0;
  color: #303133;
}

.class-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  font-size: 12px;
  color: #909399;
  margin-bottom: 10px;
}

.class-desc {
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
  margin-bottom: 15px;
}

.class-schedule {
  margin-bottom: 15px;
}

.schedule-title {
  font-size: 13px;
  color: #909399;
  margin-bottom: 8px;
}

.class-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid #ebeef5;
}

.price {
  font-size: 20px;
  font-weight: 500;
  color: #f56c6c;
}
</style>
