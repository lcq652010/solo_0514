<template>
  <div class="page-card">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px">
      <div>
        <el-button type="primary" icon="el-icon-date" @click="pickDate = true">
          选择日期
        </el-button>
        <span style="margin-left: 15px; font-size: 16px; font-weight: 500">
          {{ currentDate }}
        </span>
      </div>
      <div>
        <el-button-group>
          <el-button icon="el-icon-arrow-left" @click="prevDay">前一天</el-button>
          <el-button @click="today">今天</el-button>
          <el-button icon="el-icon-arrow-right" @click="nextDay">后一天</el-button>
        </el-button-group>
      </div>
    </div>

    <el-date-picker
      v-model="currentDateObj"
      ref="datePicker"
      type="date"
      style="display: none"
      @change="handleDateChange"
    ></el-date-picker>

    <el-row :gutter="20" style="margin-bottom: 25px">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-label">今日值班教练</div>
            <div class="stat-value">{{ todaySchedules.length }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-label">工作中</div>
            <div class="stat-value working">{{ workingCount }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-label">休息中</div>
            <div class="stat-value rest">{{ restCount }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-label">总排班数</div>
            <div class="stat-value">{{ totalScheduleCount }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-divider content-position="left">
      <span style="font-size: 16px; font-weight: 500">
        <i class="el-icon-date"></i> {{ currentDate }} 排班详情
      </span>
    </el-divider>

    <el-table :data="todaySchedules" border style="width: 100%" :row-class-name="tableRowClassName">
      <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
      <el-table-column label="教练信息" width="200">
        <template slot-scope="scope">
          <div style="display: flex; align-items: center">
            <el-avatar :size="45" :src="getTrainerAvatar(scope.row.trainerId)"></el-avatar>
            <div style="margin-left: 12px">
              <div style="font-weight: 500; color: #303133">{{ scope.row.trainerName }}</div>
              <div style="font-size: 12px; color: #909399">{{ getTrainerSpecialty(scope.row.trainerId) }}</div>
            </div>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="time" label="排班时段" width="180" align="center">
        <template slot-scope="scope">
          <el-tag type="primary" size="medium">{{ scope.row.time }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.status === 'working' ? 'success' : 'info'" size="small">
            {{ scope.row.status === 'working' ? '工作' : '休息' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="可约时段" min-width="300">
        <template slot-scope="scope">
          <div v-if="scope.row.status === 'working'" class="time-slots">
            <el-tag
              v-for="slot in getAvailableSlots(scope.row.time)"
              :key="slot"
              size="small"
              style="margin: 3px"
              :type="isSlotBooked(slot) ? 'info' : 'success'"
            >
              {{ slot }}
              <span v-if="isSlotBooked(slot)" style="color: #909399"> (已约)</span>
            </el-tag>
          </div>
          <span v-else style="color: #909399">休息时段，不可预约</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180" align="center" fixed="right">
        <template slot-scope="scope">
          <el-button
            type="primary"
            size="mini"
            icon="el-icon-plus"
            @click="handleAddSchedule(scope.row)"
          >
            排班
          </el-button>
          <el-button
            type="danger"
            size="mini"
            icon="el-icon-delete"
            @click="handleDeleteSchedule(scope.row)"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-empty
      v-if="todaySchedules.length === 0"
      description="当日暂无排班"
      style="margin: 50px 0"
    >
      <el-button type="primary" @click="showAddDialog">
        <i class="el-icon-plus"></i> 添加排班
      </el-button>
    </el-empty>

    <el-dialog title="添加排班" :visible.sync="addDialogVisible" width="500px">
      <el-form :model="scheduleForm" :rules="scheduleRules" ref="scheduleForm" label-width="100px">
        <el-form-item label="选择教练" prop="trainerId">
          <el-select v-model="scheduleForm.trainerId" placeholder="请选择教练" style="width: 100%">
            <el-option
              v-for="trainer in allTrainers"
              :key="trainer.id"
              :label="trainer.name"
              :value="trainer.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="排班日期" prop="date">
          <el-date-picker
            v-model="scheduleForm.date"
            type="date"
            placeholder="选择排班日期"
            style="width: 100%"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="开始时间" prop="startTime">
          <el-time-picker
            v-model="scheduleForm.startTime"
            format="HH:mm"
            value-format="HH:mm"
            placeholder="选择开始时间"
            style="width: 100%"
          ></el-time-picker>
        </el-form-item>
        <el-form-item label="结束时间" prop="endTime">
          <el-time-picker
            v-model="scheduleForm.endTime"
            format="HH:mm"
            value-format="HH:mm"
            placeholder="选择结束时间"
            style="width: 100%"
          ></el-time-picker>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="scheduleForm.status">
            <el-radio label="working">工作</el-radio>
            <el-radio label="rest">休息</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmitSchedule">确定</el-button>
      </span>
    </el-dialog>

    <div style="margin-top: 30px">
      <el-divider content-position="left">
        <span style="font-size: 16px; font-weight: 500">
          <i class="el-icon-calendar"></i> 周排班一览
        </span>
      </el-divider>
      <el-table :data="weekScheduleData" border style="width: 100%">
        <el-table-column prop="trainer" label="教练" width="120" align="center"></el-table-column>
        <el-table-column
          v-for="day in weekDays"
          :key="day.date"
          :label="day.label"
          :width="120"
          align="center"
        >
          <template slot-scope="scope">
            <div v-if="getScheduleStatus(scope.row.trainerId, day.date)">
              <el-tag
                size="mini"
                :type="getScheduleStatus(scope.row.trainerId, day.date) === 'working' ? 'success' : 'info'"
              >
                {{ getScheduleTime(scope.row.trainerId, day.date) }}
              </el-tag>
            </div>
            <span v-else style="color: #c0c4cc">休息</span>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import { mockTrainers, mockSchedule } from '@/mock/data'

export default {
  name: 'Schedule',
  data() {
    return {
      allTrainers: mockTrainers,
      scheduleData: { ...mockSchedule },
      currentDateObj: new Date(),
      pickDate: false,
      addDialogVisible: false,
      scheduleForm: {
        trainerId: '',
        date: '',
        startTime: '09:00',
        endTime: '18:00',
        status: 'working'
      },
      scheduleRules: {
        trainerId: [{ required: true, message: '请选择教练', trigger: 'change' }],
        date: [{ required: true, message: '请选择日期', trigger: 'change' }],
        startTime: [{ required: true, message: '请选择开始时间', trigger: 'change' }],
        endTime: [{ required: true, message: '请选择结束时间', trigger: 'change' }]
      },
      bookedSlots: ['10:00-11:00', '14:00-15:00']
    }
  },
  computed: {
    currentDate() {
      return this.formatDate(this.currentDateObj)
    },
    todaySchedules() {
      return this.scheduleData[this.currentDate] || []
    },
    workingCount() {
      return this.todaySchedules.filter(s => s.status === 'working').length
    },
    restCount() {
      return this.todaySchedules.filter(s => s.status === 'rest').length
    },
    totalScheduleCount() {
      let count = 0
      Object.values(this.scheduleData).forEach(dayList => {
        count += dayList.length
      })
      return count
    },
    weekDays() {
      const days = []
      const today = new Date(this.currentDateObj)
      const dayOfWeek = today.getDay()
      const monday = new Date(today)
      monday.setDate(today.getDate() - (dayOfWeek === 0 ? 6 : dayOfWeek - 1))

      const weekLabels = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']

      for (let i = 0; i < 7; i++) {
        const date = new Date(monday)
        date.setDate(monday.getDate() + i)
        days.push({
          date: this.formatDate(date),
          label: weekLabels[i],
          isToday: this.formatDate(date) === this.currentDate
        })
      }
      return days
    },
    weekScheduleData() {
      return this.allTrainers.map(trainer => ({
        trainerId: trainer.id,
        trainer: trainer.name
      }))
    }
  },
  methods: {
    formatDate(date) {
      const d = new Date(date)
      const year = d.getFullYear()
      const month = String(d.getMonth() + 1).padStart(2, '0')
      const day = String(d.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    },
    handleDateChange(val) {
      this.currentDateObj = val
    },
    prevDay() {
      const date = new Date(this.currentDateObj)
      date.setDate(date.getDate() - 1)
      this.currentDateObj = date
    },
    nextDay() {
      const date = new Date(this.currentDateObj)
      date.setDate(date.getDate() + 1)
      this.currentDateObj = date
    },
    today() {
      this.currentDateObj = new Date()
    },
    getTrainerAvatar(trainerId) {
      const trainer = this.allTrainers.find(t => t.id === trainerId)
      return trainer ? trainer.avatar : ''
    },
    getTrainerSpecialty(trainerId) {
      const trainer = this.allTrainers.find(t => t.id === trainerId)
      return trainer ? trainer.specialty.split('、')[0] : ''
    },
    getAvailableSlots(timeRange) {
      const slots = []
      const [start, end] = timeRange.split('-')
      const startHour = parseInt(start.split(':')[0])
      const endHour = parseInt(end.split(':')[0])

      for (let i = startHour; i < endHour; i++) {
        slots.push(`${String(i).padStart(2, '0')}:00-${String(i + 1).padStart(2, '0')}:00`)
      }
      return slots
    },
    isSlotBooked(slot) {
      return this.bookedSlots.includes(slot)
    },
    tableRowClassName({ row }) {
      return row.status === 'rest' ? 'rest-row' : ''
    },
    showAddDialog() {
      this.scheduleForm = {
        trainerId: '',
        date: this.currentDate,
        startTime: '09:00',
        endTime: '18:00',
        status: 'working'
      }
      this.addDialogVisible = true
    },
    handleAddSchedule(row) {
      this.scheduleForm = {
        trainerId: row.trainerId,
        date: this.currentDate,
        startTime: '09:00',
        endTime: '18:00',
        status: 'working'
      }
      this.addDialogVisible = true
    },
    handleDeleteSchedule(row) {
      this.$confirm('确定删除该排班吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const date = this.currentDate
        if (this.scheduleData[date]) {
          const index = this.scheduleData[date].findIndex(
            s => s.trainerId === row.trainerId && s.time === row.time
          )
          if (index > -1) {
            this.scheduleData[date].splice(index, 1)
            this.$message.success('删除成功')
          }
        }
      }).catch(() => {})
    },
    handleSubmitSchedule() {
      this.$refs.scheduleForm.validate(valid => {
        if (valid) {
          const date = this.formatDate(this.scheduleForm.date)
          const trainer = this.allTrainers.find(t => t.id === this.scheduleForm.trainerId)

          if (!this.scheduleData[date]) {
            this.$set(this.scheduleData, date, [])
          }

          this.scheduleData[date].push({
            trainerId: this.scheduleForm.trainerId,
            trainerName: trainer ? trainer.name : '',
            time: `${this.scheduleForm.startTime}-${this.scheduleForm.endTime}`,
            status: this.scheduleForm.status
          })

          this.addDialogVisible = false
          this.$message.success('排班添加成功')
        }
      })
    },
    getScheduleStatus(trainerId, date) {
      const daySchedule = this.scheduleData[date] || []
      const schedule = daySchedule.find(s => s.trainerId === trainerId)
      return schedule ? schedule.status : null
    },
    getScheduleTime(trainerId, date) {
      const daySchedule = this.scheduleData[date] || []
      const schedule = daySchedule.find(s => s.trainerId === trainerId)
      return schedule ? schedule.time : ''
    }
  }
}
</script>

<style scoped>
.rest-row {
  background-color: #f5f7fa !important;
}

.stat-item {
  text-align: center;
  padding: 10px 0;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #303133;

  &.working {
    color: #67c23a;
  }

  &.rest {
    color: #909399;
  }
}

.time-slots {
  display: flex;
  flex-wrap: wrap;
  padding: 5px 0;
}
</style>
