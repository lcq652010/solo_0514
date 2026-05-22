<template>
  <div class="page-container">
    <h2 class="page-title">我的报名记录</h2>

    <el-card class="filter-card mb-20">
      <el-form :inline="true" :model="filterForm" label-width="90px">
        <el-form-item label="活动类型">
          <el-select v-model="filterForm.activityType" placeholder="全部" clearable>
            <el-option label="文艺活动" value="文艺活动"></el-option>
            <el-option label="学术讲座" value="学术讲座"></el-option>
            <el-option label="体育活动" value="体育活动"></el-option>
            <el-option label="文化展览" value="文化展览"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="活动状态">
          <el-select v-model="filterForm.status" placeholder="全部" clearable>
            <el-option label="即将开始" value="upcoming"></el-option>
            <el-option label="进行中" value="ongoing"></el-option>
            <el-option label="已结束" value="ended"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="签到状态">
          <el-select v-model="filterForm.checkinStatus" placeholder="全部" clearable>
            <el-option label="已签到" value="checked"></el-option>
            <el-option label="未签到" value="unchecked"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="报名时间">
          <el-date-picker
            v-model="filterForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="yyyy-MM-dd"
            clearable
          ></el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleFilter">筛选</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card card-shadow">
      <el-table :data="paginatedData" style="width: 100%" border v-loading="loading">
        <el-table-column type="index" label="序号" width="80" align="center" :index="indexMethod"></el-table-column>
        <el-table-column prop="activityTitle" label="活动名称" min-width="200" show-overflow-tooltip></el-table-column>
        <el-table-column label="活动类型" width="100" align="center">
          <template slot-scope="scope">
            <el-tag type="info" size="small">
              {{ getActivityType(scope.row.activityId) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="报名人" width="100" align="center"></el-table-column>
        <el-table-column prop="phone" label="联系电话" width="130" align="center"></el-table-column>
        <el-table-column prop="registerTime" label="报名时间" width="180" align="center"></el-table-column>
        <el-table-column label="活动状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getActivityStatusType(scope.row.activityId)" size="small">
              {{ getActivityStatusText(scope.row.activityId) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="报名状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getRegisterStatusType(scope.row.status)" size="small">
              {{ getRegisterStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="签到状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.checkedIn ? 'success' : 'warning'" size="small">
              {{ scope.row.checkedIn ? '已签到' : '未签到' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="goToDetail(scope.row.activityId)">
              查看详情
            </el-button>
            <el-button
              size="mini"
              type="success"
              @click="goToCheckIn(scope.row.activityId)"
              :disabled="scope.row.checkedIn || scope.row.status === 'cancelled'"
            >
              {{ scope.row.checkedIn ? '已签到' : scope.row.status === 'cancelled' ? '已取消' : '去签到' }}
            </el-button>
            <el-button
              size="mini"
              type="danger"
              @click="handleCancel(scope.row)"
              :disabled="scope.row.checkedIn || scope.row.status === 'cancelled'"
            >
              {{ scope.row.status === 'cancelled' ? '已取消' : '取消报名' }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-empty v-if="filteredRegistrations.length === 0" description="暂无报名记录" :image-size="100">
        <el-button type="primary" @click="goToActivityList">去报名</el-button>
      </el-empty>

      <div class="pagination-wrap" v-if="filteredRegistrations.length > 0">
        <el-pagination
          background
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.currentPage"
          :page-sizes="[5, 10, 20, 50]"
          :page-size="pagination.pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="filteredRegistrations.length"
        ></el-pagination>
      </div>
    </el-card>
  </div>
</template>

<script>
import { activities, myRegistrations } from '../mock/data'

export default {
  name: 'MyRegistrations',
  data() {
    return {
      registrations: myRegistrations,
      loading: false,
      filterForm: {
        activityType: '',
        status: '',
        checkinStatus: '',
        dateRange: []
      },
      pagination: {
        currentPage: 1,
        pageSize: 10
      }
    }
  },
  computed: {
    filteredRegistrations() {
      return this.registrations.filter(item => {
        const activity = activities.find(a => a.id === item.activityId)
        
        const typeMatch = !this.filterForm.activityType || 
          (activity && activity.type === this.filterForm.activityType)
        
        const activityStatus = activity ? activity.status : 'ended'
        const statusMatch = !this.filterForm.status || activityStatus === this.filterForm.status
        
        const checkinMatch = !this.filterForm.checkinStatus ||
          (this.filterForm.checkinStatus === 'checked' ? item.checkedIn : !item.checkedIn)
        
        let dateMatch = true
        if (this.filterForm.dateRange && this.filterForm.dateRange.length === 2) {
          const startDate = this.filterForm.dateRange[0]
          const endDate = this.filterForm.dateRange[1]
          const registerDate = item.registerTime.split(' ')[0]
          dateMatch = registerDate >= startDate && registerDate <= endDate
        }
        
        return typeMatch && statusMatch && checkinMatch && dateMatch
      })
    },
    paginatedData() {
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      return this.filteredRegistrations.slice(start, end)
    }
  },
  methods: {
    indexMethod(index) {
      return (this.pagination.currentPage - 1) * this.pagination.pageSize + index + 1
    },
    getActivityType(activityId) {
      const activity = activities.find(a => a.id === activityId)
      return activity ? activity.type : '-'
    },
    getActivityStatus(activityId) {
      const activity = activities.find(a => a.id === activityId)
      return activity ? activity.status : 'ended'
    },
    getActivityStatusType(activityId) {
      const status = this.getActivityStatus(activityId)
      const map = {
        upcoming: 'primary',
        ongoing: 'warning',
        ended: 'info'
      }
      return map[status] || 'info'
    },
    getActivityStatusText(activityId) {
      const status = this.getActivityStatus(activityId)
      const map = {
        upcoming: '即将开始',
        ongoing: '进行中',
        ended: '已结束'
      }
      return map[status] || status
    },
    getRegisterStatusType(status) {
      const map = {
        registered: 'success',
        cancelled: 'info'
      }
      return map[status] || 'info'
    },
    getRegisterStatusText(status) {
      const map = {
        registered: '已报名',
        cancelled: '已取消'
      }
      return map[status] || status
    },
    goToDetail(activityId) {
      this.$router.push(`/activity/${activityId}`)
    },
    goToCheckIn(activityId) {
      this.$router.push(`/checkin/${activityId}`)
    },
    goToActivityList() {
      this.$router.push('/')
    },
    handleFilter() {
      this.pagination.currentPage = 1
      this.$message.success('筛选完成')
    },
    handleReset() {
      this.filterForm.activityType = ''
      this.filterForm.status = ''
      this.filterForm.checkinStatus = ''
      this.filterForm.dateRange = []
      this.pagination.currentPage = 1
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.pagination.currentPage = 1
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
    },
    handleCancel(row) {
      this.$confirm('确认取消该活动的报名吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.registrations.findIndex(r => r.id === row.id)
        if (index > -1) {
          this.registrations[index].status = 'cancelled'
        }
        this.$message.success('取消报名成功')
      }).catch(() => {
      })
    }
  }
}
</script>

<style scoped>
.filter-card {
  background: white;
}

.table-card {
  background: white;
}

.pagination-wrap {
  padding: 20px 0 0;
  text-align: right;
}
</style>
