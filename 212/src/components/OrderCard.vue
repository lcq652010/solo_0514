<template>
  <div class="order-card">
    <div class="order-header">
      <div class="order-id">
        <i class="el-icon-document"></i>
        <span>订单号：{{ order.id }}</span>
      </div>
      <el-tag :type="statusTagType" size="small">
        {{ statusText }}
      </el-tag>
    </div>

    <div class="order-info">
      <div class="info-row">
        <span class="label">藤条材质：</span>
        <span class="value">{{ order.material }}</span>
      </div>
      <div class="info-row">
        <span class="label">尺寸规格：</span>
        <span class="value">高度 {{ order.height }}cm / 口径 {{ order.diameter }}cm</span>
      </div>
      <div class="info-row">
        <span class="label">编织款式：</span>
        <span class="value">{{ order.style }}</span>
      </div>
      <div class="info-row">
        <span class="label">提手配置：</span>
        <span class="value">{{ order.handle }}</span>
      </div>
      <div class="info-row">
        <span class="label">联系方式：</span>
        <span class="value">{{ order.contact }}</span>
      </div>
      <div class="info-row">
        <span class="label">下单时间：</span>
        <span class="value">{{ formatDate(order.createdAt) }}</span>
      </div>
    </div>

    <div class="progress-section">
      <div class="progress-header">
        <span>生产进度</span>
        <span class="progress-percent">{{ progressPercent }}%</span>
      </div>
      <el-progress
        :percentage="progressPercent"
        :status="order.status === 'completed' ? 'success' : ''"
        :stroke-width="8"
      ></el-progress>
    </div>

    <div class="order-actions" v-if="showActions">
      <el-button
        type="primary"
        size="small"
        :disabled="order.currentProcess >= 7"
        @click="handleAdvance"
      >
        <i class="el-icon-arrow-right"></i>
        {{ order.currentProcess >= 7 ? '已完工' : `推进到「${nextProcessName}」` }}
      </el-button>
      <el-button size="small" @click="handleViewDetail">
        查看详情
      </el-button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OrderCard',
  props: {
    order: {
      type: Object,
      required: true
    },
    showActions: {
      type: Boolean,
      default: true
    }
  },
  computed: {
    statusTagType() {
      const map = {
        pending: 'warning',
        processing: 'primary',
        completed: 'success'
      }
      return map[this.order.status] || 'info'
    },
    statusText() {
      const map = {
        pending: '待生产',
        processing: '生产中',
        completed: '已完工'
      }
      return map[this.order.status] || '未知'
    },
    progressPercent() {
      return Math.round((this.order.currentProcess / 7) * 100)
    },
    nextProcessName() {
      const processes = this.$store.state.processes
      const nextIndex = this.order.currentProcess + 1
      if (nextIndex < processes.length) {
        return processes[nextIndex].name
      }
      return '完工'
    }
  },
  methods: {
    formatDate(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
    },
    handleAdvance() {
      this.$emit('advance', this.order.id)
    },
    handleViewDetail() {
      this.$emit('view-detail', this.order)
    }
  }
}
</script>

<style lang="scss" scoped>
.order-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 2px 12px rgba(139, 69, 19, 0.1);
  border: 1px solid #EFEBE9;
  transition: all 0.3s;

  &:hover {
    box-shadow: 0 4px 20px rgba(139, 69, 19, 0.15);
    transform: translateY(-2px);
  }
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px dashed #D7CCC8;

  .order-id {
    display: flex;
    align-items: center;
    font-size: 15px;
    font-weight: 600;
    color: #5D4037;

    i {
      margin-right: 8px;
      color: #8B4513;
    }
  }
}

.order-info {
  .info-row {
    display: flex;
    margin-bottom: 8px;
    font-size: 14px;

    .label {
      color: #8D6E63;
      min-width: 90px;
    }

    .value {
      color: #3E2723;
      font-weight: 500;
    }
  }
}

.progress-section {
  margin: 16px 0;
  padding: 12px;
  background: #FDF5E6;
  border-radius: 8px;

  .progress-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
    font-size: 14px;
    color: #5D4037;
    font-weight: 500;

    .progress-percent {
      color: #8B4513;
    }
  }
}

.order-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 12px;
  border-top: 1px solid #EFEBE9;
}
</style>
