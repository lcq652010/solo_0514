<template>
  <div class="booking-form">
    <div class="page-header">
      <h2>会议预定</h2>
    </div>

    <el-card class="form-card">
      <el-form
        ref="meetingForm"
        :model="form"
        :rules="rules"
        label-width="100px"
        label-position="right"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="会议主题" prop="title">
              <el-input
                v-model="form.title"
                placeholder="请输入会议主题"
                maxlength="50"
                show-word-limit
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="会议室" prop="roomId">
              <el-select
                v-model="form.roomId"
                placeholder="请选择会议室"
                style="width: 100%;"
                @change="handleRoomChange"
              >
                <el-option
                  v-for="room in availableRooms"
                  :key="room.id"
                  :label="`${room.name} (${room.capacity}人)`"
                  :value="room.id"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="会议日期" prop="date">
              <el-date-picker
                v-model="form.date"
                type="date"
                placeholder="选择日期"
                style="width: 100%;"
                :picker-options="pickerOptions"
                @change="onDateChange"
              ></el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="会议时间" required>
              <el-row :gutter="10">
                <el-col :span="11">
                  <el-form-item prop="startTime">
                    <el-time-picker
                      v-model="form.startTime"
                      :picker-options="startTimePickerOptions"
                      format="HH:mm"
                      value-format="HH:mm"
                      placeholder="开始时间"
                      style="width: 100%;"
                      @change="onStartTimeChange"
                    ></el-time-picker>
                  </el-form-item>
                </el-col>
                <el-col :span="2" class="time-separator">
                  <span>至</span>
                </el-col>
                <el-col :span="11">
                  <el-form-item prop="endTime">
                    <el-time-picker
                      v-model="form.endTime"
                      :picker-options="endTimePickerOptions"
                      format="HH:mm"
                      value-format="HH:mm"
                      placeholder="结束时间"
                      style="width: 100%;"
                      @change="checkConflict"
                    ></el-time-picker>
                  </el-form-item>
                </el-col>
              </el-row>
            </el-form-item>
          </el-col>
        </el-row>

        <el-alert
          v-if="conflictInfo.show"
          :title="conflictInfo.message"
          :type="conflictInfo.type"
          :closable="false"
          show-icon
          style="margin-bottom: 20px;"
        ></el-alert>

        <el-alert
          v-if="durationWarning.show"
          :title="durationWarning.message"
          :type="durationWarning.type"
          :closable="false"
          show-icon
          style="margin-bottom: 20px;"
        ></el-alert>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="组织者" prop="organizer">
              <el-select
                v-model="form.organizer"
                placeholder="请选择组织者"
                style="width: 100%;"
                filterable
              >
                <el-option
                  v-for="emp in employees"
                  :key="emp.id"
                  :label="emp.name"
                  :value="emp.name"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="参会人员" prop="attendees">
              <div class="attendee-select-wrapper">
                <div class="selected-attendees">
                  <el-tag
                    v-for="(name, index) in selectedAttendeeNames"
                    :key="index"
                    closable
                    @close="removeAttendee(index)"
                    style="margin-right: 5px; margin-bottom: 5px;"
                  >
                    {{ name }}
                  </el-tag>
                  <el-button
                    v-if="selectedAttendeeNames.length === 0"
                    type="text"
                    icon="el-icon-plus"
                    @click="openAttendeeSelect"
                  >
                    添加参会人员
                  </el-button>
                  <el-button
                    v-else
                    type="text"
                    icon="el-icon-plus"
                    size="small"
                    @click="openAttendeeSelect"
                    style="margin-left: 8px;"
                  >
                    添加
                  </el-button>
                </div>
              </div>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="会议描述">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="4"
            placeholder="请输入会议描述（可选）"
            maxlength="500"
            show-word-limit
          ></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm" :loading="submitting">
            提交预定
          </el-button>
          <el-button @click="resetForm">重置</el-button>
          <el-button @click="goBack">返回</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <AttendeeSelect
      ref="attendeeSelect"
      v-model="form.attendees"
      @change="handleAttendeeChange"
    ></AttendeeSelect>
  </div>
</template>

<script>
import { rooms } from '@/mock/rooms'
import { employees } from '@/mock/employees'
import { meetings } from '@/mock/meetings'
import AttendeeSelect from '@/components/AttendeeSelect.vue'

export default {
  name: 'BookingForm',
  components: {
    AttendeeSelect
  },
  data() {
    const MIN_DURATION = 30
    const MAX_DURATION = 480

    const validateTime = (rule, value, callback) => {
      if (this.form.startTime && this.form.endTime) {
        if (this.form.startTime >= this.form.endTime) {
          callback(new Error('结束时间必须大于开始时间'))
          return
        }
        const duration = this.getDurationMinutes(this.form.startTime, this.form.endTime)
        if (duration < MIN_DURATION) {
          callback(new Error(`会议时长不能少于 ${MIN_DURATION} 分钟`))
          return
        }
        if (duration > MAX_DURATION) {
          callback(new Error(`会议时长不能超过 ${MAX_DURATION / 60} 小时`))
          return
        }
        callback()
      } else {
        callback()
      }
    }

    const validateAttendees = (rule, value, callback) => {
      if (value.length === 0) {
        callback(new Error('请至少选择一名参会人员'))
      } else {
        callback()
      }
    }

    return {
      submitting: false,
      rooms,
      employees,
      meetings,
      selectedAttendeeNames: [],
      conflictInfo: {
        show: false,
        message: '',
        type: 'error'
      },
      durationWarning: {
        show: false,
        message: '',
        type: 'warning'
      },
      minDuration: MIN_DURATION,
      maxDuration: MAX_DURATION,
      pickerOptions: {
        disabledDate(time) {
          return time.getTime() < Date.now() - 8.64e7
        }
      },
      form: {
        title: '',
        roomId: '',
        date: '',
        startTime: '',
        endTime: '',
        organizer: '',
        attendees: [],
        description: ''
      },
      rules: {
        title: [
          { required: true, message: '请输入会议主题', trigger: 'blur' },
          { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
        ],
        roomId: [
          { required: true, message: '请选择会议室', trigger: 'change' }
        ],
        date: [
          { required: true, message: '请选择会议日期', trigger: 'change' }
        ],
        startTime: [
          { required: true, message: '请选择开始时间', trigger: 'change' }
        ],
        endTime: [
          { required: true, message: '请选择结束时间', trigger: 'change' },
          { validator: validateTime, trigger: 'change' }
        ],
        organizer: [
          { required: true, message: '请选择组织者', trigger: 'change' }
        ],
        attendees: [
          { validator: validateAttendees, trigger: 'change' }
        ]
      }
    }
  },
  computed: {
    availableRooms() {
      return this.rooms.filter(room => room.status === 'available')
    },
    selectedDateStr() {
      if (!this.form.date) return ''
      return typeof this.form.date === 'string' ? this.form.date : this.form.date.toISOString().split('T')[0]
    },
    occupiedTimeRanges() {
      if (!this.form.roomId || !this.selectedDateStr) return []
      return this.meetings
        .filter(m => m.roomId === this.form.roomId && m.date === this.selectedDateStr && m.status !== 'cancelled')
        .map(m => ({ start: m.startTime, end: m.endTime }))
    },
    startTimePickerOptions() {
      const ranges = this.occupiedTimeRanges
      const self = this
      return {
        selectableRange: '08:00:00 - 20:00:00',
        disabledDate(time) {
          return false
        },
        disabledTime(date) {
          return self.getDisabledTimes(ranges, 'start')
        }
      }
    },
    endTimePickerOptions() {
      const ranges = this.occupiedTimeRanges
      const startTime = this.form.startTime
      const self = this
      return {
        selectableRange: startTime ? `${startTime}:00 - 20:30:00` : '08:30:00 - 20:30:00',
        disabledDate(time) {
          return false
        },
        disabledTime(date) {
          return self.getDisabledTimes(ranges, 'end')
        }
      }
    }
  },
  mounted() {
    const roomId = this.$route.query.roomId
    if (roomId) {
      this.form.roomId = parseInt(roomId)
    }
  },
  methods: {
    getDisabledTimes(ranges, type) {
      const hours = []
      const minutes = []
      const seconds = []

      ranges.forEach(range => {
        const [startH, startM] = range.start.split(':').map(Number)
        const [endH, endM] = range.end.split(':').map(Number)

        if (type === 'start') {
          for (let h = startH; h < endH; h++) {
            if (!hours.includes(h)) hours.push(h)
          }
          for (let m = 0; m < 60; m += 30) {
            if (startH === endH) {
              if (m >= startM && m < endM) {
                minutes.push(m)
                if (!hours.includes(startH)) hours.push(startH)
              }
            } else {
              if (m >= startM && !hours.includes(startH)) {
                minutes.push(m)
              }
              if (m < endM && !hours.includes(endH)) {
                minutes.push(m)
              }
            }
          }
        } else {
          for (let h = startH; h <= endH; h++) {
            if (h < endH || endM === 0) {
              if (!hours.includes(h)) hours.push(h)
            }
          }
        }
      })

      return { hours, minutes: [], seconds: [] }
    },
    getDurationMinutes(start, end) {
      const [startH, startM] = start.split(':').map(Number)
      const [endH, endM] = end.split(':').map(Number)
      return (endH * 60 + endM) - (startH * 60 + startM)
    },
    formatDuration(minutes) {
      const hours = Math.floor(minutes / 60)
      const mins = minutes % 60
      if (hours > 0 && mins > 0) {
        return `${hours}小时${mins}分钟`
      } else if (hours > 0) {
        return `${hours}小时`
      } else {
        return `${mins}分钟`
      }
    },
    isTimeOverlap(existingStart, existingEnd, newStart, newEnd) {
      const toMinutes = (time) => {
        const [h, m] = time.split(':').map(Number)
        return h * 60 + m
      }
      const es = toMinutes(existingStart)
      const ee = toMinutes(existingEnd)
      const ns = toMinutes(newStart)
      const ne = toMinutes(newEnd)
      return ns < ee && ne > es
    },
    onDateChange() {
      this.form.startTime = ''
      this.form.endTime = ''
      this.checkConflict()
    },
    onStartTimeChange() {
      this.form.endTime = ''
      this.checkConflict()
    },
    checkConflict() {
      this.conflictInfo.show = false
      this.durationWarning.show = false

      if (this.form.startTime && this.form.endTime) {
        const duration = this.getDurationMinutes(this.form.startTime, this.form.endTime)
        if (duration < this.minDuration) {
          this.durationWarning = {
            show: true,
            message: `会议时长为 ${this.formatDuration(duration)}，建议会议时长不少于 ${this.minDuration} 分钟`,
            type: 'warning'
          }
        } else if (duration > this.maxDuration) {
          this.durationWarning = {
            show: true,
            message: `会议时长为 ${this.formatDuration(duration)}，超过最大限制 ${this.maxDuration / 60} 小时`,
            type: 'error'
          }
        }
      }

      if (this.form.roomId && this.selectedDateStr && this.form.startTime && this.form.endTime) {
        const roomName = this.rooms.find(r => r.id === this.form.roomId)?.name
        
        const conflictingMeetings = this.meetings.filter(m => {
          if (m.roomId !== this.form.roomId) return false
          if (m.date !== this.selectedDateStr) return false
          if (m.status === 'cancelled') return false
          return this.isTimeOverlap(m.startTime, m.endTime, this.form.startTime, this.form.endTime)
        })

        if (conflictingMeetings.length > 0) {
          const conflictList = conflictingMeetings.map(m => 
            `「${m.title}」${m.startTime}-${m.endTime}`
          ).join('、')
          this.conflictInfo = {
            show: true,
            message: `会议室「${roomName}」在该时段已有预约：${conflictList}，请选择其他时段`,
            type: 'error'
          }
        }
      }
    },
    handleRoomChange() {
      this.form.startTime = ''
      this.form.endTime = ''
      this.checkConflict()
    },
    openAttendeeSelect() {
      this.$refs.attendeeSelect.open()
    },
    handleAttendeeChange(selected) {
      this.selectedAttendeeNames = selected.map(emp => emp.name)
    },
    removeAttendee(index) {
      this.form.attendees.splice(index, 1)
      this.selectedAttendeeNames.splice(index, 1)
    },
    submitForm() {
      this.$refs.meetingForm.validate((valid) => {
        if (valid) {
          if (this.conflictInfo.show) {
            this.$message.error('当前时段存在冲突，请重新选择时间')
            return false
          }
          const duration = this.getDurationMinutes(this.form.startTime, this.form.endTime)
          if (duration < this.minDuration || duration > this.maxDuration) {
            this.$message.error('会议时长不符合要求')
            return false
          }
          this.submitting = true
          setTimeout(() => {
            const newMeeting = {
              id: Date.now(),
              title: this.form.title,
              roomId: this.form.roomId,
              roomName: this.rooms.find(r => r.id === this.form.roomId)?.name,
              date: this.selectedDateStr,
              startTime: this.form.startTime,
              endTime: this.form.endTime,
              organizer: this.form.organizer,
              attendees: this.form.attendees,
              attendeeNames: this.selectedAttendeeNames,
              description: this.form.description,
              minutes: '',
              status: 'upcoming'
            }
            this.meetings.push(newMeeting)

            const room = this.rooms.find(r => r.id === this.form.roomId)
            if (room) {
              room.status = 'occupied'
            }

            this.submitting = false
            this.$message.success('会议预定成功！')
            this.$router.push('/records')
          }, 1000)
        } else {
          this.$message.error('请完善表单信息')
          return false
        }
      })
    },
    resetForm() {
      this.$refs.meetingForm.resetFields()
      this.selectedAttendeeNames = []
      this.conflictInfo.show = false
      this.durationWarning.show = false
    },
    goBack() {
      this.$router.back()
    }
  }
}
</script>

<style lang="scss" scoped>
.booking-form {
  padding: 20px;

  .page-header {
    margin-bottom: 20px;

    h2 {
      margin: 0;
      color: #303133;
    }
  }

  .form-card {
    max-width: 900px;
  }

  .time-separator {
    display: flex;
    align-items: center;
    justify-content: center;
    color: #909399;
    padding-top: 8px;
  }

  .attendee-select-wrapper {
    width: 100%;
    min-height: 40px;

    .selected-attendees {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      padding: 5px 10px;
      border: 1px solid #dcdfe6;
      border-radius: 4px;
      min-height: 40px;
      transition: all 0.3s;

      &:hover {
        border-color: #c0c4cc;
      }
    }
  }
}
</style>
