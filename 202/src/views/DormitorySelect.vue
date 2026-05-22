<template>
  <div class="page-container">
    <div class="page-header">
      <div class="page-title">宿舍选择</div>
      <div class="page-subtitle">选择您所在的宿舍进行水电管理</div>
    </div>

    <el-card class="mb-20">
      <div slot="header">
        <span>快速选择</span>
      </div>
      <el-form :inline="true">
        <el-form-item label="楼栋">
          <el-select v-model="selectedBuilding" placeholder="请选择楼栋" @change="handleBuildingChange" style="width: 150px;">
            <el-option v-for="building in buildings" :key="building" :label="building" :value="building"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="房间">
          <el-select v-model="selectedRoom" placeholder="请选择房间" style="width: 150px;" @change="handleRoomChange">
            <el-option v-for="room in rooms" :key="room" :label="room" :value="room"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="confirmSelect" :disabled="!selectedBuilding || !selectedRoom">确认选择</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card>
      <div slot="header">
        <span>宿舍列表</span>
      </div>
      <el-row :gutter="20">
        <el-col :span="6" v-for="dorm in filteredDormitories" :key="dorm.id">
          <div class="dorm-card" @click="selectDormitory(dorm)" :class="{ active: isSelected(dorm) }">
            <div class="dorm-header">
              <span class="dorm-title">{{ dorm.building }} {{ dorm.room }}</span>
              <el-tag v-if="isSelected(dorm)" type="success" size="mini">已选择</el-tag>
            </div>
            <div class="dorm-info">
              <div class="info-item">
                <span class="label">住宿人数：</span>
                <span class="value">{{ dorm.currentResidents.length }}/{{ dorm.capacity }}</span>
              </div>
              <div class="info-item">
                <span class="label">成员：</span>
                <span class="value">{{ dorm.currentResidents.join('、') }}</span>
              </div>
            </div>
            <div class="dorm-balance" v-if="getDormBalance(dorm)">
              <span class="balance-item">
                <i class="el-icon-water-cup"></i>
                水费：<span :class="getBalanceClass(getDormBalance(dorm).water, 'water')">{{ getDormBalance(dorm).water.toFixed(2) }}元</span>
              </span>
              <span class="balance-item">
                <i class="el-icon-lightning"></i>
                电费：<span :class="getBalanceClass(getDormBalance(dorm).electricity, 'electricity')">{{ getDormBalance(dorm).electricity.toFixed(2) }}元</span>
              </span>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import { getDormitories, getBalance, setCurrentDormitory, getCurrentDormitory } from '@/utils/mockData'
import { EventBus } from '@/utils/eventBus'

export default {
  name: 'DormitorySelect',
  data() {
    return {
      dormitories: [],
      selectedBuilding: '',
      selectedRoom: '',
      currentDormitory: ''
    }
  },
  computed: {
    buildings() {
      const buildingSet = new Set(this.dormitories.map(d => d.building))
      return Array.from(buildingSet)
    },
    rooms() {
      if (!this.selectedBuilding) return []
      return this.dormitories
        .filter(d => d.building === this.selectedBuilding)
        .map(d => d.room)
    },
    filteredDormitories() {
      if (!this.selectedBuilding) return this.dormitories
      return this.dormitories.filter(d => d.building === this.selectedBuilding)
    }
  },
  created() {
    this.dormitories = getDormitories()
    this.currentDormitory = getCurrentDormitory()
    if (this.currentDormitory) {
      const [building, room] = this.currentDormitory.split('-')
      this.selectedBuilding = building
      this.selectedRoom = room
    }
    EventBus.$on('recharge-success', () => {
      this.dormitories = getDormitories()
    })
  },
  beforeDestroy() {
    EventBus.$off('recharge-success')
  },
  methods: {
    handleBuildingChange() {
      this.selectedRoom = ''
    },
    handleRoomChange() {
      if (this.selectedBuilding && this.selectedRoom) {
        this.confirmSelect()
      }
    },
    confirmSelect() {
      const dormKey = `${this.selectedBuilding}-${this.selectedRoom}`
      this.currentDormitory = dormKey
      setCurrentDormitory(dormKey)
      this.$message.success(`已选择 ${dormKey}`)
    },
    selectDormitory(dorm) {
      this.selectedBuilding = dorm.building
      this.selectedRoom = dorm.room
      this.confirmSelect()
    },
    isSelected(dorm) {
      return this.currentDormitory === `${dorm.building}-${dorm.room}`
    },
    getDormBalance(dorm) {
      return getBalance(`${dorm.building}-${dorm.room}`)
    },
    getBalanceClass(balance, type) {
      if (type === 'water' && balance < 30) return 'text-danger'
      if (type === 'electricity' && balance < 50) return 'text-danger'
      return 'text-success'
    }
  }
}
</script>

<style scoped>
.dorm-card {
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  padding: 15px;
  margin-bottom: 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.dorm-card:hover {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  border-color: #409EFF;
}

.dorm-card.active {
  border-color: #67C23A;
  background-color: #f0f9eb;
}

.dorm-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.dorm-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.dorm-info {
  margin-bottom: 10px;
}

.info-item {
  font-size: 13px;
  color: #606266;
  margin-bottom: 5px;
}

.info-item .label {
  color: #909399;
}

.dorm-balance {
  padding-top: 10px;
  border-top: 1px dashed #e4e7ed;
  display: flex;
  justify-content: space-between;
  font-size: 13px;
}

.balance-item {
  color: #606266;
}
</style>
