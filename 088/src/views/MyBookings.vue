<template>
  <div class="page-card">
    <div class="search-bar">
      <el-date-picker
        v-model="dateRange"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        style="width: 350px"
      ></el-date-picker>
      <el-select v-model="filterCourseType" placeholder="课程类型" style="width: 140px" clearable>
        <el-option label="一对一私教课" value="1"></el-option>
        <el-option label="小班课 (2-4人)" value="2"></el-option>
        <el-option label="特色课程" value="3"></el-option>
      </el-select>
      <el-select v-model="filterStatus" placeholder="预约状态" style="width: 120px" clearable>
        <el-option label="待确认" value="pending"></el-option>
        <el-option label="已确认" value="confirmed"></el-option>
        <el-option label="已完成" value="completed"></el-option>
        <el-option label="已取消" value="cancelled"></el-option>
      </el-select>
      <el-button type="primary" @click="handleSearch">
        <i class="el-icon-search"></i> 搜索
      </el-button>
      <el-button @click="handleReset">
        <i class="el-icon-refresh"></i> 重置
      </el-button>
      <el-button type="success" @click="goToBooking" style="margin-left: auto">
        <i class="el-icon-plus"></i> 新增约课
      </el-button>
    </div>

    <el-row :gutter="20" style="margin-bottom: 20px">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon pending">
              <i class="el-icon-time"></i>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ pendingCount }}</div>
              <div class="stat-label">待确认</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon confirmed">
              <i class="el-icon-check"></i>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ confirmedCount }}</div>
              <div class="stat-label">已确认</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon completed">
              <i class="el-icon-finished"></i>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ completedCount }}</div>
              <div class="stat-label">已完成</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon total">
              <i class="el-icon-document"></i>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ bookings.length }}</div>
              <div class="stat-label">全部预约</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <div class="table-container">
      <el-table
        :data="filteredBookings"
        border
        style="width: 100%"
        :row-class-name="tableRowClassName"
      >
        <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
        <el-table-column prop="memberName" label="会员姓名" width="100" align="center"></el-table-column>
        <el-table-column prop="trainerName" label="教练" width="100" align="center"></el-table-column>
        <el-table-column prop="courseName" label="课程名称" min-width="150"></el-table-column>
        <el-table-column prop="courseType" label="课程类型" width="130" align="center">
          <template slot-scope="scope">
            <el-tag :type="getCourseTypeColor(scope.row.courseType)" size="small">
              {{ getCourseTypeText(scope.row.courseType) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="date" label="上课日期" width="120" align="center"></el-table-column>
        <el-table-column prop="time" label="上课时间" width="120" align="center"></el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="small" effect="dark">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="160" align="center"></el-table-column>
        <el-table-column label="操作" width="220" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button
              type="primary"
              size="mini"
              icon="el-icon-view"
              @click="handleView(scope.row)"
            >
              详情
            </el-button>
            <el-button
              v-if="scope.row.status === 'pending'"
              type="warning"
              size="mini"
              icon="el-icon-edit"
              @click="handleEdit(scope.row)"
            >
              修改
            </el-button>
            <el-button
              v-if="scope.row.status === 'pending' || scope.row.status === 'confirmed'"
              type="danger"
              size="mini"
              icon="el-icon-close"
              @click="handleCancel(scope.row)"
            >
              取消
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          :current-page="pagination.page"
          :page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[5, 10, 20, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        ></el-pagination>
      </div>
    </div>

    <el-dialog title="预约详情" :visible.sync="detailVisible" width="500px">
      <div v-if="currentBooking" style="padding: 10px 0">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="会员姓名">{{ currentBooking.memberName }}</el-descriptions-item>
          <el-descriptions-item label="教练">{{ currentBooking.trainerName }}</el-descriptions-item>
          <el-descriptions-item label="课程名称">{{ currentBooking.courseName }}</el-descriptions-item>
          <el-descriptions-item label="课程类型">
            <el-tag :type="getCourseTypeColor(currentBooking.courseType)" size="small">
              {{ getCourseTypeText(currentBooking.courseType) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="上课日期">{{ currentBooking.date }}</el-descriptions-item>
          <el-descriptions-item label="上课时间">{{ currentBooking.time }}</el-descriptions-item>
          <el-descriptions-item label="预约状态">
            <el-tag :type="getStatusType(currentBooking.status)" effect="dark">
              {{ getStatusText(currentBooking.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ currentBooking.createTime }}</el-descriptions-item>
        </el-descriptions>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="detailVisible = false">关闭</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { mockBookings } from '@/mock/data'

export default {
  name: 'MyBookings',
  data() {
    return {
      bookings: [...mockBookings],
      dateRange: '',
      filterCourseType: '',
      filterStatus: '',
      pagination: {
        page: 1,
        pageSize: 10,
        total: mockBookings.length
      },
      detailVisible: false,
      currentBooking: null
    }
  },
  computed: {
    pendingCount() {
      return this.bookings.filter(b => b.status === 'pending').length
    },
    confirmedCount() {
      return this.bookings.filter(b => b.status === 'confirmed').length
    },
    completedCount() {
      return this.bookings.filter(b => b.status === 'completed').length
    },
    filteredBookings() {
      let list = this.bookings
      
      if (this.filterCourseType) {
        list = list.filter(item => item.courseType === this.filterCourseType)
      }
      if (this.filterStatus) {
        list = list.filter(item => item.status === this.filterStatus)
      }
      if (this.dateRange && this.dateRange.length === 2) {
        const start = new Date(this.dateRange[0]).getTime()
        const end = new Date(this.dateRange[1]).getTime()
        list = list.filter(item => {
          const itemDate = new Date(item.date).getTime()
          return itemDate >= start && itemDate <= end
        })
      }
      
      this.pagination.total = list.length
      const startIndex = (this.pagination.page - 1) * this.pagination.pageSize
      const endIndex = startIndex + this.pagination.pageSize
      return list.slice(startIndex, endIndex)
    }
  },
  mounted() {
    if (this.$route.query.refresh === 'true') {
      this.refreshList()
    }
  },
  watch: {
    '$route'(to, from) {
      if (to.path === '/my-bookings' && to.query.refresh === 'true') {
        this.refreshList()
      }
    }
  },
  methods: {
    refreshList() {
      this.bookings = [...mockBookings]
      this.pagination.page = 1
    },
    getStatusType(status) {
      const map = {
        pending: 'warning',
        confirmed: 'primary',
        completed: 'success',
        cancelled: 'info'
      }
      return map[status] || 'info'
    },
    getStatusText(status) {
      const map = {
        pending: '待确认',
        confirmed: '已确认',
        completed: '已完成',
        cancelled: '已取消'
      }
      return map[status] || '未知'
    },
    getCourseTypeColor(type) {
      const map = {
        '1': 'primary',
        '2': 'success',
        '3': 'warning'
      }
      return map[type] || 'info'
    },
    getCourseTypeText(type) {
      const map = {
        '1': '一对一私教课',
        '2': '小班课 (2-4人)',
        '3': '特色课程'
      }
      return map[type] || '未知'
    },
    tableRowClassName({ row }) {
      if (row.status === 'cancelled') return 'cancelled-row'
      if (row.status === 'completed') return 'completed-row'
      return ''
    },
    handleSearch() {
      this.pagination.page = 1
    },
    handleReset() {
      this.dateRange = ''
      this.filterCourseType = ''
      this.filterStatus = ''
      this.pagination.page = 1
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.pagination.page = 1
    },
    handleCurrentChange(val) {
      this.pagination.page = val
    },
    handleView(row) {
      this.currentBooking = row
      this.detailVisible = true
    },
    handleEdit(row) {
      this.$message.info('修改预约功能开发中...')
    },
    handleCancel(row) {
      this.$confirm('确定要取消该预约吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.bookings.findIndex(b => b.id === row.id)
        if (index > -1) {
          this.bookings[index].status = 'cancelled'
          this.$message.success('预约已取消')
        }
      }).catch(() => {})
    },
    goToBooking() {
      this.$router.push('/booking')
    }
  }
}
</script>

<style scoped>
.cancelled-row {
  background-color: #f5f7fa !important;
  color: #909399;
}
.completed-row {
  background-color: #f0f9ff !important;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 10px 0;
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin-right: 15px;

  &.pending {
    background-color: #fdf6ec;
    color: #e6a23c;
  }
  &.confirmed {
    background-color: #ecf5ff;
    color: #409eff;
  }
  &.completed {
    background-color: #f0f9eb;
    color: #67c23a;
  }
  &.total {
    background-color: #f4f4f5;
    color: #909399;
  }
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  line-height: 1.2;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}
</style>
