<template>
  <div class="seat-map-page">
    <el-card>
      <div slot="header" class="clearfix">
        <span>📊 座位分布图</span>
        <div style="float: right;">
          <el-select v-model="selectedFloor" placeholder="选择楼层" style="width: 150px; margin-right: 10px;">
            <el-option label="一楼自习区" value="1"></el-option>
            <el-option label="二楼自习区" value="2"></el-option>
            <el-option label="三楼自习区" value="3"></el-option>
          </el-select>
          <el-date-picker
            v-model="selectedDate"
            type="date"
            placeholder="选择日期"
            style="width: 150px;"
          ></el-date-picker>
        </div>
      </div>
      
      <div class="legend">
        <span class="legend-item"><span class="seat available"></span> 可预约</span>
        <span class="legend-item"><span class="seat occupied"></span> 已预约</span>
        <span class="legend-item"><span class="seat selected"></span> 已选中</span>
      </div>

      <div class="seat-container">
        <div class="zone">
          <h4>A区 - 靠窗区域</h4>
          <div class="seat-grid">
            <div
              v-for="seat in seatsA"
              :key="seat.id"
              :class="['seat', seat.status, { selected: selectedSeat?.id === seat.id }]"
              @click="selectSeat(seat)"
            >
              {{ seat.number }}
            </div>
          </div>
        </div>

        <div class="zone">
          <h4>B区 - 中央区域</h4>
          <div class="seat-grid">
            <div
              v-for="seat in seatsB"
              :key="seat.id"
              :class="['seat', seat.status, { selected: selectedSeat?.id === seat.id }]"
              @click="selectSeat(seat)"
            >
              {{ seat.number }}
            </div>
          </div>
        </div>

        <div class="zone">
          <h4>C区 - 安静区域</h4>
          <div class="seat-grid">
            <div
              v-for="seat in seatsC"
              :key="seat.id"
              :class="['seat', seat.status, { selected: selectedSeat?.id === seat.id }]"
              @click="selectSeat(seat)"
            >
              {{ seat.number }}
            </div>
          </div>
        </div>
      </div>

      <div v-if="selectedSeat" class="selected-info">
        <el-alert
          :title="`已选择座位: ${selectedSeat.number} (${selectedSeat.zone})`"
          type="info"
          :closable="false"
          show-icon
        >
          <template slot="default">
            <el-button type="primary" size="small" @click="goToReservation">立即预约</el-button>
          </template>
        </el-alert>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'SeatMap',
  data() {
    return {
      selectedFloor: '1',
      selectedDate: new Date(),
      selectedSeat: null,
      seatsA: [],
      seatsB: [],
      seatsC: []
    };
  },
  mounted() {
    this.generateSeats();
  },
  methods: {
    generateSeats() {
      this.seatsA = this.createSeats('A', 12);
      this.seatsB = this.createSeats('B', 16);
      this.seatsC = this.createSeats('C', 12);
    },
    createSeats(prefix, count) {
      const seats = [];
      for (let i = 1; i <= count; i++) {
        const random = Math.random();
        let status = 'available';
        if (random > 0.7) status = 'occupied';
        seats.push({
          id: `${prefix}-${i}`,
          number: `${prefix}${String(i).padStart(2, '0')}`,
          zone: `${prefix}区`,
          status: status
        });
      }
      return seats;
    },
    selectSeat(seat) {
      if (seat.status === 'occupied') {
        this.$message.warning('该座位已被预约，请选择其他座位');
        return;
      }
      this.selectedSeat = seat;
    },
    goToReservation() {
      this.$router.push({
        path: '/reservation',
        query: { seatId: this.selectedSeat.id }
      });
    }
  }
};
</script>

<style scoped>
.seat-map-page {
  padding: 0;
}

.legend {
  display: flex;
  gap: 30px;
  margin-bottom: 30px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 4px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.legend-item .seat {
  width: 24px;
  height: 24px;
  margin: 0;
}

.seat-container {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.zone h4 {
  margin-bottom: 15px;
  color: #606266;
  font-size: 16px;
}

.seat-grid {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 12px;
  max-width: 600px;
}

.seat {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s;
  border: 2px solid transparent;
}

.seat.available {
  background: #67c23a;
  color: white;
}

.seat.available:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(103, 194, 58, 0.4);
}

.seat.occupied {
  background: #909399;
  color: white;
  cursor: not-allowed;
}

.seat.selected {
  background: #409EFF;
  border-color: #303133;
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.4);
}

.selected-info {
  margin-top: 30px;
}

.selected-info .el-alert {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>
