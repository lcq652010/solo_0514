<template>
  <div class="room-types">
    <div class="page-header flex-between">
      <h1 class="page-title">房型展示</h1>
      <el-button type="primary" @click="goToBooking">立即预订</el-button>
    </div>
    
    <el-row :gutter="20">
      <el-col :xs="24" :sm="12" :md="8" :lg="8" v-for="room in roomTypes" :key="room.id">
        <el-card class="room-card mb-20" shadow="hover">
          <img :src="room.image" class="room-image" alt="房间图片">
          <div class="room-info">
            <div class="room-header">
              <h3>{{ room.name }}</h3>
              <div class="price">
                <span class="current-price">¥{{ room.price }}</span>
                <span class="original-price">/晚</span>
                <span class="discount" v-if="room.originalPrice > room.price">
                  {{ Math.round((1 - room.price / room.originalPrice) * 100) }}% OFF
                </span>
              </div>
            </div>
            
            <div class="room-details">
              <el-row :gutter="10">
                <el-col :span="8">
                  <span class="detail-label">面积</span>
                  <span class="detail-value">{{ room.area }}㎡</span>
                </el-col>
                <el-col :span="8">
                  <span class="detail-label">床型</span>
                  <span class="detail-value">{{ room.bedType }}</span>
                </el-col>
                <el-col :span="8">
                  <span class="detail-label">可住</span>
                  <span class="detail-value">{{ room.capacity }}人</span>
                </el-col>
              </el-row>
            </div>
            
            <div class="room-facilities">
              <el-tag size="small" v-for="facility in room.facilities.slice(0, 5)" :key="facility">
                {{ facility }}
              </el-tag>
            </div>
            
            <p class="room-description">{{ room.description }}</p>
            
            <div class="room-footer flex-between">
              <div>
                <span class="available" :class="{ 'sold-out': room.availableRooms <= 0 }">
                  {{ room.availableRooms > 0 ? '剩余 ' + room.availableRooms + ' 间' : '已满房' }}
                </span>
              </div>
              <el-button 
                type="primary" 
                size="small" 
                @click="bookRoom(room)" 
                :disabled="room.availableRooms <= 0"
              >
                {{ room.availableRooms > 0 ? '预订' : '已满' }}
              </el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { roomTypes } from '../mock/data'

export default {
  name: 'RoomTypes',
  data() {
    return {
      roomTypes: roomTypes
    }
  },
  methods: {
    goToBooking() {
      this.$router.push('/booking')
    },
    bookRoom(room) {
      this.$router.push({
        path: '/booking',
        query: { roomTypeId: room.id }
      })
    }
  }
}
</script>

<style scoped>
.room-card {
  overflow: hidden;
}

.room-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 15px;
}

.room-header {
  margin-bottom: 15px;
}

.room-header h3 {
  font-size: 18px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 10px;
}

.price {
  display: flex;
  align-items: baseline;
}

.current-price {
  font-size: 24px;
  font-weight: bold;
  color: #f56c6c;
  margin-right: 5px;
}

.original-price {
  font-size: 14px;
  color: #909399;
  text-decoration: line-through;
}

.discount {
  background-color: #fef0f0;
  color: #f56c6c;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  margin-left: 10px;
}

.room-details {
  margin-bottom: 15px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.detail-label {
  display: block;
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}

.detail-value {
  display: block;
  font-size: 14px;
  color: #303133;
  font-weight: 500;
}

.room-facilities {
  margin-bottom: 15px;
  min-height: 32px;
}

.room-facilities .el-tag {
  margin-right: 5px;
  margin-bottom: 5px;
}

.room-description {
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
  margin-bottom: 15px;
}

.room-footer {
  padding-top: 15px;
  border-top: 1px solid #ebeef5;
}

.available {
  font-size: 14px;
  color: #67c23a;
}

.available.sold-out {
  color: #f56c6c;
  font-weight: bold;
}
</style>
