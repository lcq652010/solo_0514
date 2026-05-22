<template>
  <div class="my-bookings">
    <div class="page-title">我的预约</div>
    <el-card>
      <div class="filter-bar">
        <el-form :inline="true" :model="filterForm">
          <el-form-item label="教练">
            <el-select v-model="filterForm.trainerId" placeholder="全部教练" clearable>
              <el-option v-for="trainer in trainers" :key="trainer.id" :label="trainer.name" :value="trainer.id"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="课程类型">
            <el-select v-model="filterForm.courseType" placeholder="全部类型" clearable>
              <el-option label="私教课" value="private"></el-option>
              <el-option label="团课" value="group"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="预约状态">
            <el-select v-model="filterForm.status" placeholder="全部状态" clearable>
              <el-option label="已确认" value="已确认"></el-option>
              <el-option label="已完成" value="已完成"></el-option>
              <el-option label="已取消" value="已取消"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="resetFilter">重置筛选</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <el-table :data="paginatedList" border style="width: 100%">
        <el-table-column prop="id" label="预约编号" width="120" align="center"></el-table-column>
        <el-table-column prop="trainerName" label="教练" width="120" align="center"></el-table-column>
        <el-table-column prop="memberName" label="会员姓名" width="120" align="center"></el-table-column>
        <el-table-column prop="date" label="预约日期" width="150" align="center">
          <template slot-scope="scope">
            {{ formatDate(scope.row.date) }}
          </template>
        </el-table-column>
        <el-table-column prop="timeSlot" label="时段" width="150" align="center"></el-table-column>
        <el-table-column prop="hours" label="课时" width="100" align="center">
          <template slot-scope="scope">{{ scope.row.hours }}课时</template>
        </el-table-column>
        <el-table-column prop="courseType" label="课程类型" width="120" align="center">
          <template slot-scope="scope">
            <el-tag size="small">{{ scope.row.courseType === 'group' ? '团课' : '私教课' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="120" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="180" align="center"></el-table-column>
        <el-table-column label="操作" width="180" align="center">
          <template slot-scope="scope">
            <el-button v-if="scope.row.status === '已确认'" type="danger" size="small" @click="cancelBooking(scope.row)">取消</el-button>
            <el-button v-if="scope.row.status === '已确认'" type="success" size="small" @click="completeBooking(scope.row)">完成</el-button>
            <el-button type="info" size="small" @click="viewDetail(scope.row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <el-empty v-if="filteredList.length === 0" description="暂无预约记录" style="margin-top: 20px;"></el-empty>
      
      <el-pagination
        v-if="filteredList.length > 0"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[5, 10, 20]"
        :page-size="pageSize"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        style="margin-top: 20px; justify-content: flex-end; display: flex;">
      </el-pagination>
    </el-card>

    <el-dialog title="预约详情" :visible.sync="detailVisible" width="500px">
      <div v-if="currentBooking">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="预约编号">{{ currentBooking.id }}</el-descriptions-item>
          <el-descriptions-item label="教练">{{ currentBooking.trainerName }}</el-descriptions-item>
          <el-descriptions-item label="会员姓名">{{ currentBooking.memberName }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ currentBooking.phone }}</el-descriptions-item>
          <el-descriptions-item label="预约日期">{{ formatDate(currentBooking.date) }}</el-descriptions-item>
          <el-descriptions-item label="预约时段">{{ currentBooking.timeSlot }}</el-descriptions-item>
          <el-descriptions-item label="课时数量">{{ currentBooking.hours }}课时</el-descriptions-item>
          <el-descriptions-item label="预约状态">
            <el-tag :type="getStatusType(currentBooking.status)">{{ currentBooking.status }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item v-if="currentBooking.remark" label="备注">{{ currentBooking.remark }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ currentBooking.createTime }}</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'MyBookings',
  data() {
    return {
      bookingList: [],
      detailVisible: false,
      currentBooking: null,
      filterForm: {
        trainerId: '',
        courseType: '',
        status: ''
      },
      currentPage: 1,
      pageSize: 10,
      trainers: [
        { id: 1, name: '张教练' },
        { id: 2, name: '李教练' },
        { id: 3, name: '王教练' },
        { id: 4, name: '陈教练' },
        { id: 5, name: '刘教练' },
        { id: 6, name: '赵教练' },
        { id: 7, name: '孙教练' },
        { id: 8, name: '周教练' }
      ]
    }
  },
  computed: {
    filteredList() {
      let list = [...this.bookingList]
      
      if (this.filterForm.trainerId) {
        list = list.filter(item => item.trainerId === this.filterForm.trainerId)
      }
      if (this.filterForm.courseType) {
        list = list.filter(item => item.courseType === this.filterForm.courseType)
      }
      if (this.filterForm.status) {
        list = list.filter(item => item.status === this.filterForm.status)
      }
      
      return list
    },
    paginatedList() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredList.slice(start, end)
    },
    total() {
      return this.filteredList.length
    }
  },
  created() {
    this.loadBookings()
  },
  methods: {
    loadBookings() {
      const bookings = JSON.parse(localStorage.getItem('bookings') || '[]')
      if (bookings.length === 0) {
        this.bookingList = [
          {
            id: 1715000000001,
            trainerId: 1,
            trainerName: '张教练',
            memberName: '测试会员',
            phone: '13800138000',
            date: new Date(),
            timeSlot: '10:00-11:00',
            hours: 2,
            courseType: 'private',
            remark: '希望安排在靠窗位置',
            status: '已确认',
            createTime: new Date().toLocaleString()
          }
        ]
      } else {
        this.bookingList = bookings.map(b => ({
          ...b,
          courseType: b.courseType || 'private'
        }))
      }
    },
    formatDate(date) {
      if (!date) return ''
      const d = new Date(date)
      return d.toLocaleDateString('zh-CN')
    },
    getStatusType(status) {
      const map = {
        '待确认': 'warning',
        '已确认': 'primary',
        '已完成': 'success',
        '已取消': 'info'
      }
      return map[status] || ''
    },
    cancelBooking(row) {
      this.$confirm('确定取消该预约吗？取消后将回退已扣除的课时。', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        if (row.status === '已确认') {
          const members = JSON.parse(localStorage.getItem('members') || '[]')
          const memberIndex = members.findIndex(m => m.phone === row.phone)
          if (memberIndex !== -1) {
            const member = members[memberIndex]
            member.usedHours -= row.hours
            member.remainingHours += row.hours
            if (!member.records) member.records = []
            member.records.unshift({
              time: new Date().toLocaleString(),
              type: '充值',
              hours: row.hours,
              remark: `取消预约回退 - ${row.trainerName}`
            })
            localStorage.setItem('members', JSON.stringify(members))
          }
        }
        row.status = '已取消'
        this.saveBookings()
        this.$message.success('预约已取消，课时已回退')
      })
    },
    completeBooking(row) {
      this.$confirm('确定标记该预约为已完成吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'success'
      }).then(() => {
        row.status = '已完成'
        this.saveBookings()
        this.$message.success('预约已完成')
      })
    },
    viewDetail(row) {
      this.currentBooking = row
      this.detailVisible = true
    },
    saveBookings() {
      localStorage.setItem('bookings', JSON.stringify(this.bookingList))
    },
    resetFilter() {
      this.filterForm = {
        trainerId: '',
        courseType: '',
        status: ''
      }
      this.currentPage = 1
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

<style scoped>
.my-bookings {
  padding: 0;
}

.filter-bar {
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
  margin-bottom: 20px;
}

.filter-bar .el-form {
  margin-bottom: 0;
}
</style>
