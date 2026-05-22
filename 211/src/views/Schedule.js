window.Schedule = {
  template: `
    <div class="schedule-page">
      <h2 class="page-title">
        <i class="el-icon-date"></i>
        摄影师档期
      </h2>

      <el-row :gutter="24">
        <el-col :md="6">
          <el-card class="card-shadow photographer-list">
            <h3 class="list-title">摄影师</h3>
            <div
              v-for="p in photographers"
              :key="p.id"
              class="photographer-item"
              :class="{ active: selectedPhotographerId === p.id }"
              @click="selectPhotographer(p.id)">
              <img :src="p.avatar" class="avatar" />
              <div class="info">
                <div class="name">
                  {{ p.name }}
                  <el-tag size="mini" type="warning" v-if="p.level.includes('首席')">首席</el-tag>
                </div>
                <div class="level">{{ p.level }}</div>
                <el-rate :value="p.rating" disabled size="mini" />
              </div>
            </div>
          </el-card>
        </el-col>

        <el-col :md="18">
          <el-card class="card-shadow">
            <div class="calendar-header">
              <el-button-group>
                <el-button icon="el-icon-arrow-left" @click="prevWeek"></el-button>
                <el-button @click="goToday">今天</el-button>
                <el-button icon="el-icon-arrow-right" @click="nextWeek"></el-button>
              </el-button-group>
              <h3 class="date-range">{{ dateRangeText }}</h3>
              <el-button type="primary" icon="el-icon-plus" @click="addSchedule">
                添加档期
              </el-button>
            </div>

            <el-table
              :data="scheduleData"
              border
              class="schedule-table"
              style="width: 100%">
              <el-table-column
                prop="time"
                label="时段"
                width="120"
                fixed="left" />
              <el-table-column
                v-for="day in weekDays"
                :key="day.date"
                :label="day.label"
                :class-name="isToday(day.date) ? 'today-col' : ''">
                <template slot-scope="scope">
                  <div class="cell-content">
                    <div
                      v-for="slot in getSlots(day.date, scope.row.time)"
                      :key="slot.id"
                      class="schedule-slot"
                      :class="getStatusClass(slot.status)"
                      @click="slot.status === '可预约' ? bookSlot(slot) : viewSlot(slot)">
                      <div class="slot-time">{{ slot.time }}</div>
                      <div class="slot-status">{{ slot.status }}</div>
                      <div class="slot-order" v-if="slot.orderId">
                        订单号: {{ slot.orderId }}
                      </div>
                    </div>
                  </div>
                </template>
              </el-table-column>
            </el-table>

            <div class="legend">
              <span class="legend-item">
                <span class="dot available"></span> 可预约
              </span>
              <span class="legend-item">
                <span class="dot booked"></span> 已预订
              </span>
              <span class="legend-item">
                <span class="dot unavailable"></span> 不可用
              </span>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <el-dialog
        :visible.sync="bookingDialogVisible"
        title="预约档期"
        width="500px">
        <el-form :model="bookingForm" label-width="100px">
          <el-form-item label="摄影师">
            <el-input :value="currentPhotographer?.name" disabled />
          </el-form-item>
          <el-form-item label="日期">
            <el-input :value="bookingForm.date" disabled />
          </el-form-item>
          <el-form-item label="时段">
            <el-input :value="bookingForm.time" disabled />
          </el-form-item>
          <el-form-item label="客户姓名">
            <el-input v-model="bookingForm.customerName" placeholder="请输入客户姓名" />
          </el-form-item>
          <el-form-item label="联系电话">
            <el-input v-model="bookingForm.phone" placeholder="请输入联系电话" />
          </el-form-item>
          <el-form-item label="备注">
            <el-input
              v-model="bookingForm.remark"
              type="textarea"
              :rows="3"
              placeholder="请填写备注信息" />
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button @click="bookingDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmBooking">确认预约</el-button>
        </span>
      </el-dialog>
    </div>
  `,
  data() {
    return {
      selectedPhotographerId: 1,
      currentWeekStart: new Date(),
      scheduleData: [
        { time: '08:00-10:00' },
        { time: '10:00-12:00' },
        { time: '13:00-15:00' },
        { time: '15:00-17:00' },
        { time: '17:00-19:00' }
      ],
      bookingDialogVisible: false,
      bookingForm: {
        date: '',
        time: '',
        customerName: '',
        phone: '',
        remark: ''
      }
    };
  },
  computed: {
    photographers() {
      return this.$store.state.photographers;
    },
    currentPhotographer() {
      return this.photographers.find(p => p.id === this.selectedPhotographerId);
    },
    weekDays() {
      const days = [];
      const start = new Date(this.currentWeekStart);
      for (let i = 0; i < 7; i++) {
        const date = new Date(start);
        date.setDate(start.getDate() + i);
        const dateStr = moment(date).format('YYYY-MM-DD');
        const dayNames = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
        days.push({
          date: dateStr,
          label: moment(date).format('MM/DD') + ' ' + dayNames[date.getDay()]
        });
      }
      return days;
    },
    dateRangeText() {
      if (this.weekDays.length > 0) {
        return this.weekDays[0].date + ' 至 ' + this.weekDays[6].date;
      }
      return '';
    }
  },
  mounted() {
    const today = new Date();
    this.currentWeekStart = new Date(today.setDate(today.getDate() - today.getDay() + 1));
  },
  methods: {
    selectPhotographer(id) {
      this.selectedPhotographerId = id;
    },
    prevWeek() {
      const date = new Date(this.currentWeekStart);
      date.setDate(date.getDate() - 7);
      this.currentWeekStart = date;
    },
    nextWeek() {
      const date = new Date(this.currentWeekStart);
      date.setDate(date.getDate() + 7);
      this.currentWeekStart = date;
    },
    goToday() {
      const today = new Date();
      this.currentWeekStart = new Date(today.setDate(today.getDate() - today.getDay() + 1));
    },
    isToday(dateStr) {
      return dateStr === moment().format('YYYY-MM-DD');
    },
    getSlots(date, timeRange) {
      const slots = this.$store.state.schedule.filter(s => 
        s.photographerId === this.selectedPhotographerId && s.date === date
      );
      if (slots.length > 0) {
        return slots[0].timeSlots.filter(s => {
          const slotStart = s.time.split('-')[0];
          const rangeStart = timeRange.split('-')[0];
          return slotStart === rangeStart;
        }).map(s => ({ ...s, date: date }));
      }
      return [{
        id: date + '-' + timeRange,
        time: timeRange,
        status: '可预约',
        date: date
      }];
    },
    getStatusClass(status) {
      return {
        'available': status === '可预约',
        'booked': status === '已预订',
        'unavailable': status === '不可用'
      };
    },
    bookSlot(slot) {
      this.bookingForm = {
        date: slot.date,
        time: slot.time,
        customerName: '',
        phone: '',
        remark: ''
      };
      this.bookingDialogVisible = true;
    },
    viewSlot(slot) {
      if (slot.orderId) {
        this.$message.info('订单号: ' + slot.orderId);
      }
    },
    addSchedule() {
      this.$message.info('请在日历中选择可预约时段进行预约');
    },
    confirmBooking() {
      if (!this.bookingForm.customerName || !this.bookingForm.phone) {
        this.$message.warning('请填写客户姓名和联系电话');
        return;
      }
      this.$message.success('预约成功！');
      this.bookingDialogVisible = false;
    }
  }
};
