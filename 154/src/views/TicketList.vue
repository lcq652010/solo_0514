<template>
  <div class="ticket-list-page">
    <div class="page-header">
      <h1 class="page-title">门票类型</h1>
      <p class="page-subtitle">选择适合您的门票类型，开启愉快的旅程</p>
    </div>
    
    <div class="ticket-grid">
      <el-card
        v-for="ticket in ticketTypes"
        :key="ticket.id"
        class="ticket-card"
        shadow="hover"
      >
        <div class="ticket-image">
          <img :src="ticket.image" :alt="ticket.name" />
          <div class="ticket-tags">
            <el-tag
              v-for="tag in ticket.tags"
              :key="tag"
              :type="getTagType(tag)"
              size="small"
            >
              {{ tag }}
            </el-tag>
          </div>
        </div>
        <div class="ticket-content">
          <h3 class="ticket-name">{{ ticket.name }}</h3>
          <p class="ticket-desc">{{ ticket.description }}</p>
          <div class="ticket-info">
            <span class="info-item">
              <i class="el-icon-time"></i>
              有效期：{{ ticket.validDays }}天
            </span>
            <span class="info-item">
              <i class="el-icon-warning"></i>
              限购：{{ ticket.maxPurchase }}张
            </span>
          </div>
          <div class="sales-info" v-if="getTicketRemaining(ticket.id) >= 0">
            <span class="remaining" :class="{ low: getTicketRemaining(ticket.id) < 10 }">
              <i class="el-icon-data-line"></i>
              今日剩余：{{ getTicketRemaining(ticket.id) }}张
            </span>
            <span class="sold">
              已售：{{ getTicketSold(ticket.id) }}张
            </span>
          </div>
          <div class="ticket-price">
            <span class="price">¥{{ ticket.price }}</span>
            <span class="original-price">¥{{ ticket.originalPrice }}</span>
            <span class="discount">
              省{{ ticket.originalPrice - ticket.price }}元
            </span>
          </div>
          <el-button
            type="primary"
            class="book-btn"
            :disabled="isTicketSoldOut(ticket.id)"
            @click="goToBooking(ticket.id)"
          >
            <i v-if="isTicketSoldOut(ticket.id)" class="el-icon-close"></i>
            {{ isTicketSoldOut(ticket.id) ? '今日已售罄' : '立即预订' }}
          </el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ticketTypes, getDailySales, formatDate } from '@/mock/data';

export default {
  name: 'TicketList',
  data() {
    return {
      ticketTypes,
      today: formatDate(new Date()),
      refreshTimer: null
    };
  },
  mounted() {
    this.startAutoRefresh();
  },
  beforeDestroy() {
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer);
    }
  },
  methods: {
    getTagType(tag) {
      const tagMap = {
        '热门': 'danger',
        '推荐': 'success',
        '优惠': 'warning',
        '超值': 'primary',
        '深度游': 'info',
        '售罄': 'info'
      };
      return tagMap[tag] || '';
    },
    getTicketSold(ticketId) {
      const ticket = this.ticketTypes.find(t => t.id === ticketId);
      if (!ticket) return 0;
      return getDailySales(ticket.name, this.today);
    },
    getTicketRemaining(ticketId) {
      const ticket = this.ticketTypes.find(t => t.id === ticketId);
      if (!ticket) return 0;
      const sold = getDailySales(ticket.name, this.today);
      return Math.max(0, ticket.dailyLimit - sold);
    },
    isTicketSoldOut(ticketId) {
      return this.getTicketRemaining(ticketId) <= 0;
    },
    goToBooking(ticketId) {
      if (this.isTicketSoldOut(ticketId)) {
        this.$message.warning('该门票今日已售罄，请选择其他日期或门票类型');
        return;
      }
      this.$router.push(`/booking/${ticketId}`);
    },
    startAutoRefresh() {
      this.refreshTimer = setInterval(() => {
        this.$forceUpdate();
      }, 5000);
    }
  }
};
</script>

<style scoped>
.ticket-list-page {
  padding: 0;
}

.ticket-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

.ticket-card {
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
}

.ticket-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.ticket-card /deep/ .el-card__body {
  padding: 0;
}

.ticket-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.ticket-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.ticket-card:hover .ticket-image img {
  transform: scale(1.05);
}

.ticket-tags {
  position: absolute;
  top: 12px;
  left: 12px;
  display: flex;
  gap: 6px;
}

.ticket-content {
  padding: 20px;
}

.ticket-name {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 10px 0;
}

.ticket-desc {
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
  margin-bottom: 15px;
  min-height: 44px;
}

.ticket-info {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
  font-size: 13px;
  color: #909399;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.info-item i {
  color: #409EFF;
}

.ticket-price {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin-bottom: 15px;
}

.price {
  font-size: 28px;
  font-weight: 700;
  color: #F56C6C;
}

.original-price {
  font-size: 14px;
  color: #C0C4CC;
  text-decoration: line-through;
}

.discount {
  font-size: 12px;
  color: #E6A23C;
  background: #FDF6EC;
  padding: 2px 8px;
  border-radius: 4px;
}

.sales-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  font-size: 12px;
  padding: 8px 12px;
  background: #F5F7FA;
  border-radius: 6px;
}

.remaining {
  color: #67C23A;
  display: flex;
  align-items: center;
  gap: 4px;
}

.remaining.low {
  color: #E6A23C;
  font-weight: 600;
}

.sold {
  color: #909399;
}

.book-btn {
  width: 100%;
  height: 44px;
  font-size: 16px;
  border-radius: 8px;
}

.book-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
