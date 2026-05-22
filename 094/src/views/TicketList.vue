<template>
  <div class="page-container">
    <h2 class="page-title">
      <i class="el-icon-tickets"></i>
      门票类型
    </h2>
    
    <el-row :gutter="20">
      <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="ticket in ticketList" :key="ticket.id">
        <el-card class="ticket-card" shadow="hover">
          <img :src="ticket.image" class="ticket-image" :alt="ticket.name">
          <div class="ticket-tags">
            <el-tag v-for="tag in ticket.tags" :key="tag" size="mini" type="danger">{{ tag }}</el-tag>
          </div>
          <div class="ticket-info">
            <h3 class="ticket-name">{{ ticket.name }}</h3>
            <p class="ticket-desc">{{ ticket.description }}</p>
            <div class="ticket-price">
              <span class="current-price">¥{{ ticket.price }}</span>
              <span class="original-price">¥{{ ticket.originalPrice }}</span>
            </div>
            <div class="ticket-meta">
              <span class="stock">库存: {{ ticket.stock }}张</span>
              <span class="valid">有效期: {{ ticket.validDays }}天</span>
            </div>
            <el-button 
              type="primary" 
              class="book-btn" 
              @click="goToBooking(ticket.id)"
              :disabled="ticket.stock === 0"
            >
              {{ ticket.stock === 0 ? '已售罄' : '立即预订' }}
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ticketTypes } from '@/data/mockData'

export default {
  name: 'TicketList',
  data() {
    return {
      ticketList: ticketTypes
    }
  },
  methods: {
    goToBooking(ticketId) {
      this.$router.push(`/booking/${ticketId}`)
    }
  }
}
</script>

<style scoped>
.ticket-card {
  margin-bottom: 20px;
  overflow: hidden;
  transition: transform 0.3s;
}

.ticket-card:hover {
  transform: translateY(-5px);
}

.ticket-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 4px;
}

.ticket-tags {
  margin-top: 10px;
}

.ticket-tags .el-tag {
  margin-right: 5px;
}

.ticket-info {
  padding-top: 15px;
}

.ticket-name {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 8px;
}

.ticket-desc {
  font-size: 14px;
  color: #606266;
  margin-bottom: 12px;
  line-height: 1.5;
}

.ticket-price {
  margin-bottom: 10px;
}

.current-price {
  font-size: 24px;
  font-weight: bold;
  color: #f56c6c;
}

.original-price {
  font-size: 14px;
  color: #909399;
  text-decoration: line-through;
  margin-left: 8px;
}

.ticket-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #909399;
  margin-bottom: 15px;
}

.book-btn {
  width: 100%;
}
</style>
