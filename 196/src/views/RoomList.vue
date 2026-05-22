<template>
  <div class="room-list">
    <div class="page-header">
      <h2>会议室列表</h2>
      <div class="header-actions">
        <el-button type="primary" icon="el-icon-plus" @click="goToBooking">
          预定会议
        </el-button>
      </div>
    </div>

    <div class="filter-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索会议室名称或位置"
        clearable
        style="width: 280px; margin-right: 16px;"
      >
        <i slot="prefix" class="el-input__icon el-icon-search"></i>
      </el-input>
      <el-select
        v-model="statusFilter"
        placeholder="状态筛选"
        clearable
        style="width: 150px;"
      >
        <el-option label="空闲" value="available"></el-option>
        <el-option label="使用中" value="occupied"></el-option>
        <el-option label="维护中" value="maintenance"></el-option>
      </el-select>
    </div>

    <el-table
      :data="filteredRooms"
      border
      stripe
      style="width: 100%;"
      v-loading="loading"
    >
      <el-table-column
        prop="name"
        label="会议室名称"
        min-width="150"
      >
        <template slot-scope="scope">
          <span class="room-name">
            <i class="el-icon-office-building"></i>
            {{ scope.row.name }}
          </span>
        </template>
      </el-table-column>
      <el-table-column
        prop="capacity"
        label="容纳人数"
        width="100"
        align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.capacity }} 人</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="location"
        label="位置"
        width="120"
      ></el-table-column>
      <el-table-column
        prop="equipment"
        label="配备设备"
        min-width="250"
      >
        <template slot-scope="scope">
          <el-tag
            v-for="(item, index) in scope.row.equipment"
            :key="index"
            size="mini"
            style="margin-right: 5px; margin-bottom: 5px;"
          >
            {{ item }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column
        prop="status"
        label="状态"
        width="100"
        align="center"
      >
        <template slot-scope="scope">
          <el-tag
            :type="statusMap[scope.row.status].type"
            size="small"
          >
            {{ statusMap[scope.row.status].label }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        width="150"
        align="center"
        fixed="right"
      >
        <template slot-scope="scope">
          <el-button
            type="text"
            size="small"
            icon="el-icon-view"
            @click="viewDetail(scope.row)"
          >
            详情
          </el-button>
          <el-button
            type="text"
            size="small"
            icon="el-icon-date"
            :disabled="scope.row.status !== 'available'"
            @click="quickBook(scope.row)"
          >
            预定
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      title="会议室详情"
      :visible.sync="detailVisible"
      width="500px"
    >
      <div v-if="currentRoom" class="room-detail">
        <div class="detail-item">
          <span class="label">会议室名称：</span>
          <span class="value">{{ currentRoom.name }}</span>
        </div>
        <div class="detail-item">
          <span class="label">容纳人数：</span>
          <span class="value">{{ currentRoom.capacity }} 人</span>
        </div>
        <div class="detail-item">
          <span class="label">位置：</span>
          <span class="value">{{ currentRoom.location }}</span>
        </div>
        <div class="detail-item">
          <span class="label">状态：</span>
          <el-tag :type="statusMap[currentRoom.status].type" size="small">
            {{ statusMap[currentRoom.status].label }}
          </el-tag>
        </div>
        <div class="detail-item equipment-list">
          <span class="label">配备设备：</span>
          <div class="value">
            <el-tag
              v-for="(item, index) in currentRoom.equipment"
              :key="index"
              style="margin-right: 5px; margin-bottom: 5px;"
            >
              {{ item }}
            </el-tag>
          </div>
        </div>
      </div>
      <div slot="footer">
        <el-button @click="detailVisible = false">关闭</el-button>
        <el-button
          type="primary"
          :disabled="!currentRoom || currentRoom.status !== 'available'"
          @click="quickBook(currentRoom)"
        >
          立即预定
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { rooms, statusMap } from '@/mock/rooms'

export default {
  name: 'RoomList',
  data() {
    return {
      loading: false,
      searchKeyword: '',
      statusFilter: '',
      rooms,
      statusMap,
      detailVisible: false,
      currentRoom: null
    }
  },
  computed: {
    filteredRooms() {
      return this.rooms.filter(room => {
        const matchKeyword = !this.searchKeyword ||
          room.name.includes(this.searchKeyword) ||
          room.location.includes(this.searchKeyword)
        const matchStatus = !this.statusFilter || room.status === this.statusFilter
        return matchKeyword && matchStatus
      })
    }
  },
  methods: {
    goToBooking() {
      this.$router.push('/booking')
    },
    viewDetail(room) {
      this.currentRoom = room
      this.detailVisible = true
    },
    quickBook(room) {
      this.detailVisible = false
      this.$router.push({
        path: '/booking',
        query: { roomId: room.id }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.room-list {
  padding: 20px;

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    h2 {
      margin: 0;
      color: #303133;
    }
  }

  .filter-bar {
    margin-bottom: 20px;
    display: flex;
    align-items: center;
  }

  .room-name {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 500;

    i {
      color: #409eff;
    }
  }

  .room-detail {
    .detail-item {
      display: flex;
      align-items: flex-start;
      margin-bottom: 16px;
      font-size: 14px;

      .label {
        width: 100px;
        color: #909399;
        flex-shrink: 0;
      }

      .value {
        color: #303133;
        flex: 1;
      }

      &.equipment-list {
        .value {
          display: flex;
          flex-wrap: wrap;
        }
      }
    }
  }
}
</style>
