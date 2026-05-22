<template>
  <div class="room-status">
    <div class="page-header flex-between">
      <h1 class="page-title">房态管理</h1>
      <div>
        <el-tag type="success">空闲: {{ availableCount }} 间</el-tag>
        <el-tag type="danger" style="margin-left: 10px;">已入住: {{ occupiedCount }} 间</el-tag>
        <el-tag type="warning" style="margin-left: 10px;">清洁中: {{ cleaningCount }} 间</el-tag>
        <el-tag type="info" style="margin-left: 10px;">维护中: {{ maintenanceCount }} 间</el-tag>
      </div>
    </div>
    
    <el-card class="mb-20">
      <el-form :inline="true" :model="filterForm" class="demo-form-inline">
        <el-form-item label="楼层">
          <el-select v-model="filterForm.floor" placeholder="请选择楼层" clearable>
            <el-option label="1楼" :value="1"></el-option>
            <el-option label="2楼" :value="2"></el-option>
            <el-option label="3楼" :value="3"></el-option>
            <el-option label="4楼" :value="4"></el-option>
            <el-option label="5楼" :value="5"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="房态">
          <el-select v-model="filterForm.status" placeholder="请选择房态" clearable>
            <el-option label="空闲" value="available"></el-option>
            <el-option label="已入住" value="occupied"></el-option>
            <el-option label="清洁中" value="cleaning"></el-option>
            <el-option label="维护中" value="maintenance"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="房型">
          <el-select v-model="filterForm.type" placeholder="请选择房型" clearable>
            <el-option label="标准单人间" value="标准单人间"></el-option>
            <el-option label="标准双人间" value="标准双人间"></el-option>
            <el-option label="豪华大床房" value="豪华大床房"></el-option>
            <el-option label="家庭套房" value="家庭套房"></el-option>
            <el-option label="总统套房" value="总统套房"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="filter">筛选</el-button>
          <el-button @click="reset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-card>
      <div v-for="(floorRooms, floor) in groupedRooms" :key="floor" class="floor-section">
        <div class="floor-title">
          <h3>{{ floor }}楼</h3>
          <el-divider></el-divider>
        </div>
        <el-row :gutter="16">
          <el-col :xs="12" :sm="8" :md="6" :lg="4" v-for="room in floorRooms" :key="room.id">
            <div class="room-card" :class="'status-' + room.status" @click="showRoomDetail(room)">
              <div class="room-number">{{ room.number }}</div>
              <div class="room-type">{{ room.type }}</div>
              <div class="room-price">¥{{ room.price }}/晚</div>
              <div class="room-status-badge">
                <el-tag :type="statusMap[room.status].type" size="small">
                  {{ statusMap[room.status].label }}
                </el-tag>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-card>
    
    <el-dialog title="房间详情" :visible.sync="detailDialogVisible" width="500px">
      <el-descriptions v-if="currentRoom" :column="1" border>
        <el-descriptions-item label="房间号">{{ currentRoom.number }}</el-descriptions-item>
        <el-descriptions-item label="房型">{{ currentRoom.type }}</el-descriptions-item>
        <el-descriptions-item label="楼层">{{ currentRoom.floor }}楼</el-descriptions-item>
        <el-descriptions-item label="价格">¥{{ currentRoom.price }}/晚</el-descriptions-item>
        <el-descriptions-item label="当前状态">
          <el-tag :type="statusMap[currentRoom.status].type">
            {{ statusMap[currentRoom.status].label }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>
      
      <div class="status-actions mt-20">
        <el-button type="success" @click="changeStatus('available')" v-if="currentRoom && ['cleaning', 'maintenance'].includes(currentRoom.status)">
          <i class="el-icon-check"></i> 设为空闲
        </el-button>
        <el-button type="warning" @click="changeStatus('cleaning')" v-if="currentRoom && ['available', 'occupied'].includes(currentRoom.status)">
          <i class="el-icon-brush"></i> 清洁中
        </el-button>
        <el-button type="info" @click="changeStatus('maintenance')" v-if="currentRoom && currentRoom.status === 'available'">
          <i class="el-icon-tools"></i> 设为维护
        </el-button>
        <el-button type="danger" @click="changeStatus('occupied')" v-if="currentRoom && currentRoom.status === 'available'">
          <i class="el-icon-user"></i> 入住
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { rooms, statusMap } from '../mock/data'

export default {
  name: 'RoomStatus',
  data() {
    return {
      rooms: rooms,
      statusMap: statusMap,
      filterForm: {
        floor: '',
        status: '',
        type: ''
      },
      detailDialogVisible: false,
      currentRoom: null
    }
  },
  computed: {
    filteredRooms() {
      let result = [...this.rooms]
      
      if (this.filterForm.floor) {
        result = result.filter(room => room.floor === this.filterForm.floor)
      }
      
      if (this.filterForm.status) {
        result = result.filter(room => room.status === this.filterForm.status)
      }
      
      if (this.filterForm.type) {
        result = result.filter(room => room.type === this.filterForm.type)
      }
      
      return result
    },
    groupedRooms() {
      const groups = {}
      this.filteredRooms.forEach(room => {
        if (!groups[room.floor]) {
          groups[room.floor] = []
        }
        groups[room.floor].push(room)
      })
      
      Object.keys(groups).forEach(floor => {
        groups[floor].sort((a, b) => a.number.localeCompare(b.number))
      })
      
      return groups
    },
    availableCount() {
      return this.rooms.filter(room => room.status === 'available').length
    },
    occupiedCount() {
      return this.rooms.filter(room => room.status === 'occupied').length
    },
    cleaningCount() {
      return this.rooms.filter(room => room.status === 'cleaning').length
    },
    maintenanceCount() {
      return this.rooms.filter(room => room.status === 'maintenance').length
    }
  },
  methods: {
    filter() {
      
    },
    reset() {
      this.filterForm.floor = ''
      this.filterForm.status = ''
      this.filterForm.type = ''
    },
    showRoomDetail(room) {
      this.currentRoom = { ...room }
      this.detailDialogVisible = true
    },
    changeStatus(status) {
      const room = this.rooms.find(r => r.id === this.currentRoom.id)
      if (room) {
        room.status = status
        this.currentRoom.status = status
        this.$message.success(`房间状态已更新为：${this.statusMap[status].label}`)
      }
    }
  }
}
</script>

<style scoped>
.floor-section {
  margin-bottom: 30px;
}

.floor-title h3 {
  font-size: 18px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 10px;
}

.room-card {
  border: 2px solid #e4e7ed;
  border-radius: 8px;
  padding: 20px 15px;
  margin-bottom: 15px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  background-color: #fff;
}

.room-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.room-card.status-available {
  border-color: #67c23a;
  background: linear-gradient(135deg, #f0f9ff 0%, #e6ffed 100%);
}

.room-card.status-occupied {
  border-color: #f56c6c;
  background: linear-gradient(135deg, #fff5f5 0%, #ffe6e6 100%);
}

.room-card.status-cleaning {
  border-color: #e6a23c;
  background: linear-gradient(135deg, #fffbf5 0%, #fff7e6 100%);
}

.room-card.status-maintenance {
  border-color: #909399;
  background: linear-gradient(135deg, #f5f7fa 0%, #f0f2f5 100%);
}

.room-number {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 8px;
}

.room-type {
  font-size: 14px;
  color: #606266;
  margin-bottom: 5px;
}

.room-price {
  font-size: 16px;
  color: #f56c6c;
  font-weight: 500;
  margin-bottom: 10px;
}

.status-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}
</style>
