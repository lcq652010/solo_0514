<template>
  <div class="refund-page">
    <h1 class="page-title">退票改签</h1>
    
    <el-tabs v-model="activeTab" class="custom-tabs">
      <el-tab-pane label="申请退票" name="refund">
        <el-card class="card-shadow">
          <el-form :model="refundForm" :rules="refundRules" ref="refundForm" label-width="100px">
            <el-form-item label="订单号" prop="orderId">
              <el-input v-model="refundForm.orderId" placeholder="请输入订单号" clearable></el-input>
            </el-form-item>
            <el-form-item label="手机号" prop="phone">
              <el-input v-model="refundForm.phone" placeholder="请输入购票手机号" maxlength="11"></el-input>
            </el-form-item>
            <el-form-item label="退票原因" prop="reason">
              <el-select v-model="refundForm.reason" placeholder="请选择退票原因" style="width: 100%">
                <el-option label="时间冲突无法前往" value="time_conflict"></el-option>
                <el-option label="计划变更" value="plan_change"></el-option>
                <el-option label="不想看了" value="not_interested"></el-option>
                <el-option label="其他原因" value="other"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="详细说明" prop="description">
              <el-input 
                v-model="refundForm.description" 
                type="textarea" 
                :rows="4" 
                placeholder="请详细说明退票原因（选填）"
              ></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submitRefund" :loading="submitting">提交退票申请</el-button>
              <el-button @click="resetRefundForm">重置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
        
        <el-card class="card-shadow mt-20">
          <div slot="header">
            <span>退票记录</span>
          </div>
          <el-table :data="refundRecords" style="width: 100%">
            <el-table-column prop="orderId" label="订单号" width="200" show-overflow-tooltip></el-table-column>
            <el-table-column prop="movieTitle" label="电影名称" min-width="150" show-overflow-tooltip></el-table-column>
            <el-table-column prop="applyTime" label="申请时间" width="180"></el-table-column>
            <el-table-column prop="refundAmount" label="退款金额" width="120" align="center">
              <template slot-scope="scope">
                <span style="color: #f56c6c">¥{{ scope.row.refundAmount }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100" align="center">
              <template slot-scope="scope">
                <el-tag :type="scope.row.status === 'success' ? 'success' : 'warning'" size="small">
                  {{ scope.row.status === 'success' ? '退款成功' : '处理中' }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>
      
      <el-tab-pane label="申请改签" name="change">
        <el-card class="card-shadow">
          <el-form :model="changeForm" :rules="changeRules" ref="changeForm" label-width="100px">
            <el-form-item label="原订单号" prop="orderId">
              <el-input v-model="changeForm.orderId" placeholder="请输入原订单号" clearable></el-input>
            </el-form-item>
            <el-form-item label="手机号" prop="phone">
              <el-input v-model="changeForm.phone" placeholder="请输入购票手机号" maxlength="11"></el-input>
            </el-form-item>
            <el-form-item label="改签电影" prop="newMovieId">
              <el-select v-model="changeForm.newMovieId" placeholder="请选择改签电影" style="width: 100%" filterable>
                <el-option 
                  v-for="movie in movies" 
                  :key="movie.id" 
                  :label="movie.title" 
                  :value="movie.id"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="改签影院" prop="newCinemaId">
              <el-select v-model="changeForm.newCinemaId" placeholder="请选择改签影院" style="width: 100%">
                <el-option 
                  v-for="cinema in cinemas" 
                  :key="cinema.id" 
                  :label="cinema.name" 
                  :value="cinema.id"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="改签日期" prop="newDate">
              <el-date-picker
                v-model="changeForm.newDate"
                type="date"
                placeholder="选择日期"
                style="width: 100%"
                value-format="yyyy-MM-dd"
              ></el-date-picker>
            </el-form-item>
            <el-form-item label="改签场次" prop="newScheduleId">
              <el-select v-model="changeForm.newScheduleId" placeholder="请选择改签场次" style="width: 100%">
                <el-option 
                  v-for="schedule in filteredSchedules" 
                  :key="schedule.id" 
                  :label="`${schedule.time} - ${schedule.hall}`" 
                  :value="schedule.id"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="改签原因" prop="reason">
              <el-select v-model="changeForm.reason" placeholder="请选择改签原因" style="width: 100%">
                <el-option label="时间冲突" value="time_conflict"></el-option>
                <el-option label="想换其他场次" value="change_session"></el-option>
                <el-option label="其他原因" value="other"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item v-if="priceDiff > 0">
              <div class="price-diff">
                <span>需补差价：</span>
                <span class="price">¥{{ priceDiff }}</span>
              </div>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submitChange" :loading="changeSubmitting">
                {{ priceDiff > 0 ? '支付并改签' : '提交改签申请' }}
              </el-button>
              <el-button @click="resetChangeForm">重置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
        
        <el-card class="card-shadow mt-20">
          <div slot="header">
            <span>改签记录</span>
          </div>
          <el-table :data="changeRecords" style="width: 100%">
            <el-table-column prop="orderId" label="原订单号" width="180" show-overflow-tooltip></el-table-column>
            <el-table-column prop="movieTitle" label="电影名称" min-width="150" show-overflow-tooltip></el-table-column>
            <el-table-column prop="newSession" label="新场次" width="200" show-overflow-tooltip></el-table-column>
            <el-table-column prop="applyTime" label="申请时间" width="180"></el-table-column>
            <el-table-column prop="priceDiff" label="差价" width="100" align="center">
              <template slot-scope="scope">
                <span :style="{ color: scope.row.priceDiff > 0 ? '#f56c6c' : '#67c23a' }">
                  {{ scope.row.priceDiff > 0 ? '+' : '' }}{{ scope.row.priceDiff }}
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100" align="center">
              <template slot-scope="scope">
                <el-tag :type="scope.row.status === 'success' ? 'success' : 'warning'" size="small">
                  {{ scope.row.status === 'success' ? '改签成功' : '处理中' }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { movies, cinemas, schedules } from '@/data/mock.js'

export default {
  name: 'Refund',
  data() {
    return {
      activeTab: 'refund',
      movies,
      cinemas,
      schedules,
      submitting: false,
      changeSubmitting: false,
      refundForm: {
        orderId: '',
        phone: '',
        reason: '',
        description: ''
      },
      changeForm: {
        orderId: '',
        phone: '',
        newMovieId: '',
        newCinemaId: '',
        newDate: '',
        newScheduleId: '',
        reason: ''
      },
      refundRules: {
        orderId: [
          { required: true, message: '请输入订单号', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入手机号', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
        ],
        reason: [
          { required: true, message: '请选择退票原因', trigger: 'change' }
        ]
      },
      changeRules: {
        orderId: [
          { required: true, message: '请输入原订单号', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入手机号', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
        ],
        newMovieId: [
          { required: true, message: '请选择改签电影', trigger: 'change' }
        ],
        newCinemaId: [
          { required: true, message: '请选择改签影院', trigger: 'change' }
        ],
        newDate: [
          { required: true, message: '请选择改签日期', trigger: 'change' }
        ],
        newScheduleId: [
          { required: true, message: '请选择改签场次', trigger: 'change' }
        ],
        reason: [
          { required: true, message: '请选择改签原因', trigger: 'change' }
        ]
      },
      refundRecords: [
        {
          orderId: 'ORD202505100004',
          movieTitle: '我和我的父辈2',
          applyTime: '2025-05-10 09:30:25',
          refundAmount: 86,
          status: 'success'
        }
      ],
      changeRecords: [
        {
          orderId: 'ORD202505150003',
          movieTitle: '唐人街探案4',
          newSession: '2025-05-19 20:00 3号厅',
          applyTime: '2025-05-16 14:20:10',
          priceDiff: 20,
          status: 'success'
        }
      ]
    }
  },
  computed: {
    filteredSchedules() {
      if (!this.changeForm.newMovieId || !this.changeForm.newCinemaId || !this.changeForm.newDate) {
        return []
      }
      return this.schedules.filter(s => 
        s.movieId === this.changeForm.newMovieId &&
        s.cinemaId === this.changeForm.newCinemaId &&
        s.date === this.changeForm.newDate
      )
    },
    priceDiff() {
      if (!this.changeForm.newScheduleId) return 0
      const newSchedule = this.schedules.find(s => s.id === this.changeForm.newScheduleId)
      return newSchedule ? newSchedule.price - 49 : 0
    }
  },
  methods: {
    submitRefund() {
      this.$refs.refundForm.validate(valid => {
        if (valid) {
          this.submitting = true
          setTimeout(() => {
            this.submitting = false
            this.$message.success('退票申请提交成功！金额将在1-3个工作日内原路返回。')
            this.refundRecords.unshift({
              orderId: this.refundForm.orderId,
              movieTitle: '流浪地球3',
              applyTime: this.formatDateTime(new Date()),
              refundAmount: 98,
              status: 'processing'
            })
            this.resetRefundForm()
          }, 1500)
        }
      })
    },
    resetRefundForm() {
      this.$refs.refundForm.resetFields()
    },
    submitChange() {
      this.$refs.changeForm.validate(valid => {
        if (valid) {
          this.changeSubmitting = true
          setTimeout(() => {
            this.changeSubmitting = false
            this.$message.success('改签申请提交成功！')
            this.changeRecords.unshift({
              orderId: this.changeForm.orderId,
              movieTitle: this.movies.find(m => m.id === this.changeForm.newMovieId)?.title || '',
              newSession: `${this.changeForm.newDate} ${this.schedules.find(s => s.id === this.changeForm.newScheduleId)?.time || ''} ${this.schedules.find(s => s.id === this.changeForm.newScheduleId)?.hall || ''}`,
              applyTime: this.formatDateTime(new Date()),
              priceDiff: this.priceDiff,
              status: 'processing'
            })
            this.resetChangeForm()
          }, 1500)
        }
      })
    },
    resetChangeForm() {
      this.$refs.changeForm.resetFields()
    },
    formatDateTime(date) {
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      const hours = String(date.getHours()).padStart(2, '0')
      const minutes = String(date.getMinutes()).padStart(2, '0')
      const seconds = String(date.getSeconds()).padStart(2, '0')
      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
    }
  }
}
</script>

<style scoped>
.custom-tabs {
  margin-top: 20px;
}

.custom-tabs ::v-deep .el-tabs__header {
  margin-bottom: 20px;
}

.custom-tabs ::v-deep .el-tabs__item {
  font-size: 16px;
  padding: 0 30px;
}

.price-diff {
  font-size: 16px;
}

.price-diff .price {
  font-size: 24px;
  font-weight: 600;
  color: #f56c6c;
}
</style>
