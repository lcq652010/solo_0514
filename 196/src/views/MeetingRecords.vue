<template>
  <div class="meeting-records">
    <div class="page-header">
      <h2>会议记录</h2>
      <div class="header-actions">
        <el-button type="primary" icon="el-icon-plus" @click="goToBooking">
          新建会议
        </el-button>
      </div>
    </div>

    <div class="filter-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索会议主题或组织者"
        clearable
        style="width: 220px; margin-right: 12px;"
      >
        <i slot="prefix" class="el-input__icon el-icon-search"></i>
      </el-input>
      <el-select
        v-model="departmentFilter"
        placeholder="部门筛选"
        clearable
        style="width: 140px; margin-right: 12px;"
      >
        <el-option
          v-for="dept in departments"
          :key="dept"
          :label="dept"
          :value="dept"
        ></el-option>
      </el-select>
      <el-select
        v-model="roomFilter"
        placeholder="会议室筛选"
        clearable
        style="width: 160px; margin-right: 12px;"
      >
        <el-option
          v-for="room in roomList"
          :key="room.id"
          :label="room.name"
          :value="room.id"
        ></el-option>
      </el-select>
      <el-select
        v-model="statusFilter"
        placeholder="状态筛选"
        clearable
        style="width: 120px; margin-right: 12px;"
      >
        <el-option label="即将开始" value="upcoming"></el-option>
        <el-option label="已结束" value="completed"></el-option>
        <el-option label="已取消" value="cancelled"></el-option>
      </el-select>
      <el-date-picker
        v-model="dateRangeFilter"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        format="yyyy-MM-dd"
        value-format="yyyy-MM-dd"
        style="width: 260px;"
      ></el-date-picker>
    </div>

    <el-table
      :data="pagedMeetings"
      border
      stripe
      style="width: 100%;"
      v-loading="loading"
    >
      <el-table-column
        prop="title"
        label="会议主题"
        min-width="180"
      >
        <template slot-scope="scope">
          <span class="meeting-title">
            <i class="el-icon-document"></i>
            {{ scope.row.title }}
          </span>
        </template>
      </el-table-column>
      <el-table-column
        prop="roomName"
        label="会议室"
        width="130"
      ></el-table-column>
      <el-table-column
        label="会议时间"
        width="220"
      >
        <template slot-scope="scope">
          <div class="meeting-time">
            <div>{{ scope.row.date }}</div>
            <div class="time-range">{{ scope.row.startTime }} - {{ scope.row.endTime }}</div>
          </div>
        </template>
      </el-table-column>
      <el-table-column
        prop="organizer"
        label="组织者"
        width="100"
      ></el-table-column>
      <el-table-column
        label="参会人员"
        min-width="200"
      >
        <template slot-scope="scope">
          <div class="attendees">
            <el-tag
              v-for="(name, index) in scope.row.attendeeNames.slice(0, 3)"
              :key="index"
              size="mini"
              style="margin-right: 4px; margin-bottom: 4px;"
            >
              {{ name }}
            </el-tag>
            <span v-if="scope.row.attendeeNames.length > 3" class="more-attendees">
              +{{ scope.row.attendeeNames.length - 3 }}
            </span>
          </div>
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
            :type="meetingStatusMap[scope.row.status].type"
            size="small"
          >
            {{ meetingStatusMap[scope.row.status].label }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        width="180"
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
            v-if="scope.row.status === 'completed' && !scope.row.minutes"
            type="text"
            size="small"
            icon="el-icon-edit"
            @click="editMinutes(scope.row)"
          >
            录入纪要
          </el-button>
          <el-button
            v-if="scope.row.status === 'upcoming'"
            type="text"
            size="small"
            icon="el-icon-delete"
            @click="cancelMeeting(scope.row)"
          >
            取消
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination-wrapper">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[5, 10, 20, 50]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="filteredMeetings.length"
        background
      ></el-pagination>
    </div>

    <el-dialog
      title="会议详情"
      :visible.sync="detailVisible"
      width="600px"
    >
      <div v-if="currentMeeting" class="meeting-detail">
        <div class="detail-header">
          <h3>{{ currentMeeting.title }}</h3>
          <el-tag
            :type="meetingStatusMap[currentMeeting.status].type"
            size="small"
          >
            {{ meetingStatusMap[currentMeeting.status].label }}
          </el-tag>
        </div>
        <div class="detail-item">
          <span class="label">会议室：</span>
          <span class="value">{{ currentMeeting.roomName }}</span>
        </div>
        <div class="detail-item">
          <span class="label">时间：</span>
          <span class="value">{{ currentMeeting.date }} {{ currentMeeting.startTime }} - {{ currentMeeting.endTime }}</span>
        </div>
        <div class="detail-item">
          <span class="label">组织者：</span>
          <span class="value">{{ currentMeeting.organizer }}</span>
        </div>
        <div class="detail-item">
          <span class="label">参会人员：</span>
          <div class="value attendees-list">
            <el-tag
              v-for="(name, index) in currentMeeting.attendeeNames"
              :key="index"
              style="margin-right: 4px; margin-bottom: 4px;"
            >
              {{ name }}
            </el-tag>
          </div>
        </div>
        <div class="detail-item" v-if="currentMeeting.description">
          <span class="label">会议描述：</span>
          <span class="value">{{ currentMeeting.description }}</span>
        </div>
        <div class="detail-item" v-if="currentMeeting.minutes">
          <span class="label">会议纪要：</span>
          <div class="value minutes-content">
            {{ currentMeeting.minutes }}
          </div>
        </div>
      </div>
      <div slot="footer">
        <el-button @click="detailVisible = false">关闭</el-button>
      </div>
    </el-dialog>

    <el-dialog
      title="录入会议纪要"
      :visible.sync="minutesVisible"
      width="600px"
    >
      <el-form :model="minutesForm" label-width="80px">
        <el-form-item label="会议主题">
          <span>{{ currentMeeting ? currentMeeting.title : '' }}</span>
        </el-form-item>
        <el-form-item label="会议纪要" prop="minutes">
          <el-input
            v-model="minutesForm.minutes"
            type="textarea"
            :rows="8"
            placeholder="请输入会议纪要内容"
            maxlength="2000"
            show-word-limit
          ></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="minutesVisible = false">取消</el-button>
        <el-button type="primary" @click="saveMinutes" :loading="saving">保存</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { meetings, meetingStatusMap } from '@/mock/meetings'
import { rooms } from '@/mock/rooms'
import { employees, departments } from '@/mock/employees'

export default {
  name: 'MeetingRecords',
  data() {
    return {
      loading: false,
      saving: false,
      searchKeyword: '',
      departmentFilter: '',
      roomFilter: '',
      statusFilter: '',
      dateRangeFilter: [],
      currentPage: 1,
      pageSize: 5,
      meetings,
      meetingStatusMap,
      roomList: rooms,
      departments,
      employees,
      detailVisible: false,
      minutesVisible: false,
      currentMeeting: null,
      minutesForm: {
        minutes: ''
      }
    }
  },
  computed: {
    filteredMeetings() {
      return this.meetings.filter(meeting => {
        const matchKeyword = !this.searchKeyword ||
          meeting.title.includes(this.searchKeyword) ||
          meeting.organizer.includes(this.searchKeyword)
        const matchStatus = !this.statusFilter || meeting.status === this.statusFilter
        const matchRoom = !this.roomFilter || meeting.roomId === this.roomFilter
        
        let matchDept = true
        if (this.departmentFilter) {
          const deptEmployees = this.employees.filter(e => e.department === this.departmentFilter).map(e => e.name)
          matchDept = meeting.organizer === this.departmentFilter ||
            deptEmployees.some(name => meeting.attendeeNames.includes(name)) ||
            deptEmployees.includes(meeting.organizer)
        }

        let matchDate = true
        if (this.dateRangeFilter && this.dateRangeFilter.length === 2) {
          const [startDate, endDate] = this.dateRangeFilter
          matchDate = meeting.date >= startDate && meeting.date <= endDate
        }

        return matchKeyword && matchStatus && matchRoom && matchDept && matchDate
      })
    },
    pagedMeetings() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredMeetings.slice(start, end)
    }
  },
  watch: {
    filteredMeetings() {
      this.currentPage = 1
    }
  },
  methods: {
    goToBooking() {
      this.$router.push('/booking')
    },
    viewDetail(meeting) {
      this.currentMeeting = meeting
      this.detailVisible = true
    },
    editMinutes(meeting) {
      this.currentMeeting = meeting
      this.minutesForm.minutes = meeting.minutes || ''
      this.minutesVisible = true
    },
    saveMinutes() {
      if (!this.minutesForm.minutes.trim()) {
        this.$message.warning('请输入会议纪要内容')
        return
      }
      this.saving = true
      setTimeout(() => {
        this.currentMeeting.minutes = this.minutesForm.minutes
        this.saving = false
        this.minutesVisible = false
        this.$message.success('会议纪要保存成功')
      }, 800)
    },
    cancelMeeting(meeting) {
      this.$confirm('确定要取消此会议吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        meeting.status = 'cancelled'
        this.$message.success('会议已取消')
      }).catch(() => {})
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.currentPage = 1
    },
    handleCurrentChange(val) {
      this.currentPage = val
    }
  }
}
</script>

<style lang="scss" scoped>
.meeting-records {
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
    flex-wrap: wrap;
    gap: 10px;
  }

  .pagination-wrapper {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }

  .meeting-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 500;

    i {
      color: #409eff;
    }
  }

  .meeting-time {
    .time-range {
      color: #909399;
      font-size: 13px;
    }
  }

  .attendees {
    display: flex;
    flex-wrap: wrap;
    align-items: center;

    .more-attendees {
      color: #909399;
      font-size: 12px;
    }
  }

  .meeting-detail {
    .detail-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 20px;
      padding-bottom: 16px;
      border-bottom: 1px solid #ebeef5;

      h3 {
        margin: 0;
        color: #303133;
      }
    }

    .detail-item {
      display: flex;
      align-items: flex-start;
      margin-bottom: 16px;
      font-size: 14px;

      .label {
        width: 80px;
        color: #909399;
        flex-shrink: 0;
      }

      .value {
        color: #303133;
        flex: 1;

        &.attendees-list {
          display: flex;
          flex-wrap: wrap;
        }

        &.minutes-content {
          white-space: pre-wrap;
          line-height: 1.6;
          padding: 12px;
          background: #f5f7fa;
          border-radius: 4px;
        }
      }
    }
  }
}
</style>
