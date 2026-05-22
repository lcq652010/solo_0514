<template>
  <div class="page-container">
    <div class="card-wrapper">
      <div class="attendance-header">
        <div class="class-selector">
          <el-form :inline="true" :model="filterForm">
            <el-form-item label="选择班级">
              <el-select v-model="filterForm.classId" placeholder="请选择班级" style="width: 200px" @change="onClassChange">
                <el-option v-for="item in classList" :key="item.id" :label="item.className" :value="item.id"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="上课日期">
              <el-date-picker
                v-model="filterForm.date"
                type="date"
                placeholder="选择日期"
                style="width: 200px"
                value-format="yyyy-MM-dd"
              ></el-date-picker>
            </el-form-item>
            <el-form-item label="考勤状态">
              <el-select v-model="filterForm.status" placeholder="全部状态" style="width: 150px" clearable>
                <el-option label="未打卡" value="pending"></el-option>
                <el-option label="出勤" value="present"></el-option>
                <el-option label="迟到" value="late"></el-option>
                <el-option label="缺勤" value="absent"></el-option>
                <el-option label="请假" value="leave"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" icon="el-icon-search" @click="loadAttendance">加载名单</el-button>
              <el-button icon="el-icon-refresh" @click="resetFilter">重置筛选</el-button>
            </el-form-item>
          </el-form>
        </div>
        
        <div class="attendance-stats" v-if="currentClass">
          <el-card shadow="never" class="stat-card">
            <div class="stat-item">
              <span class="stat-label">班级名称</span>
              <span class="stat-value">{{ currentClass.className }}</span>
            </div>
          </el-card>
          <el-card shadow="never" class="stat-card">
            <div class="stat-item">
              <span class="stat-label">课程名称</span>
              <span class="stat-value">{{ currentClass.courseName }}</span>
            </div>
          </el-card>
          <el-card shadow="never" class="stat-card">
            <div class="stat-item">
              <span class="stat-label">上课时间</span>
              <span class="stat-value">{{ currentClass.startTime }} - {{ currentClass.endTime }}</span>
            </div>
          </el-card>
          <el-card shadow="never" class="stat-card">
            <div class="stat-item">
              <span class="stat-label">当前时间</span>
              <span class="stat-value" style="color: #409EFF; font-weight: bold">{{ currentTime }}</span>
            </div>
          </el-card>
        </div>
      </div>

      <div class="attendance-summary mb-20" v-if="attendanceList.length > 0">
        <el-row :gutter="20">
          <el-col :span="4">
            <div class="summary-item total">
              <div class="summary-count">{{ totalCount }}</div>
              <div class="summary-label">总人数</div>
            </div>
          </el-col>
          <el-col :span="5">
            <div class="summary-item present">
              <div class="summary-count">{{ presentCount }}</div>
              <div class="summary-label">已出勤</div>
            </div>
          </el-col>
          <el-col :span="5">
            <div class="summary-item late">
              <div class="summary-count">{{ lateCount }}</div>
              <div class="summary-label">迟到</div>
            </div>
          </el-col>
          <el-col :span="5">
            <div class="summary-item absent">
              <div class="summary-count">{{ absentCount }}</div>
              <div class="summary-label">缺勤</div>
            </div>
          </el-col>
          <el-col :span="5">
            <div class="summary-item leave">
              <div class="summary-count">{{ leaveCount }}</div>
              <div class="summary-label">请假</div>
            </div>
          </el-col>
        </el-row>
      </div>

      <div class="table-toolbar mb-20" v-if="attendanceList.length > 0">
        <div class="toolbar-left">
          <span style="font-size: 16px; font-weight: bold">学员考勤打卡</span>
          <span style="margin-left: 15px; color: #606266">
            已选择: <el-tag type="primary" size="mini">{{ selectedRows.length }} / {{ paginatedList.length }}</el-tag> 人
          </span>
          <el-button-group style="margin-left: 15px">
            <el-button size="small" icon="el-icon-check" @click="handleSelectAll(true)">全选</el-button>
            <el-button size="small" icon="el-icon-close" @click="handleSelectAll(false)">反选</el-button>
          </el-button-group>
        </div>
        <div class="toolbar-right">
          <el-button-group>
            <el-button type="success" icon="el-icon-check" @click="batchMark('present')">批量出勤</el-button>
            <el-button type="warning" icon="el-icon-time" @click="batchMark('late')">批量迟到</el-button>
            <el-button type="danger" icon="el-icon-close" @click="batchMark('absent')">批量缺勤</el-button>
            <el-button type="info" icon="el-icon-document" @click="batchMark('leave')">批量请假</el-button>
          </el-button-group>
          <el-button type="primary" icon="el-icon-check" @click="submitAllAttendance">一键提交考勤</el-button>
        </div>
      </div>

      <el-table 
        ref="attendanceTable"
        :data="paginatedList" 
        border 
        stripe 
        style="width: 100%" 
        v-loading="loading"
        @selection-change="handleSelectionChange"
        v-if="attendanceList.length > 0"
      >
        <el-table-column type="selection" width="55" align="center"></el-table-column>
        <el-table-column type="index" label="序号" width="60" align="center" :index="indexMethod"></el-table-column>
        <el-table-column prop="studentNo" label="学号" width="100" align="center"></el-table-column>
        <el-table-column prop="studentName" label="姓名" width="100" align="center"></el-table-column>
        <el-table-column prop="checkInTime" label="打卡时间" width="150" align="center">
          <template slot-scope="scope">
            <span v-if="scope.row.checkInTime">{{ scope.row.checkInTime }}</span>
            <span v-else style="color: #909399">--</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="考勤状态" width="120" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="medium">
              <i :class="getStatusIcon(scope.row.status)" style="margin-right: 3px"></i>
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="打卡操作" width="250" align="center">
          <template slot-scope="scope">
            <el-button 
              type="success" 
              size="small" 
              icon="el-icon-check" 
              @click="markAttendance(scope.row, 'present')"
              :disabled="scope.row.status === 'present'"
            >
              出勤
            </el-button>
            <el-button 
              type="warning" 
              size="small" 
              icon="el-icon-time" 
              @click="markAttendance(scope.row, 'late')"
              :disabled="scope.row.status === 'late'"
            >
              迟到
            </el-button>
            <el-button 
              type="danger" 
              size="small" 
              icon="el-icon-close" 
              @click="markAttendance(scope.row, 'absent')"
              :disabled="scope.row.status === 'absent'"
            >
              缺勤
            </el-button>
            <el-button 
              type="info" 
              size="small" 
              icon="el-icon-document" 
              @click="markAttendance(scope.row, 'leave')"
              :disabled="scope.row.status === 'leave'"
            >
              请假
            </el-button>
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" min-width="150">
          <template slot-scope="scope">
            <el-input 
              v-model="scope.row.remark" 
              placeholder="添加备注" 
              size="small"
            ></el-input>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrapper mt-20 text-right" v-if="filteredList.length > 0">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.currentPage"
          :page-sizes="[5, 10, 20, 50]"
          :page-size="pagination.pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="filteredList.length"
        ></el-pagination>
      </div>

      <el-empty description="请先选择班级和日期加载考勤名单" v-if="!currentClass && attendanceList.length === 0"></el-empty>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Attendance',
  data() {
    return {
      loading: false,
      currentTime: '',
      timer: null,
      filterForm: {
        classId: '',
        date: '',
        status: ''
      },
      pagination: {
        currentPage: 1,
        pageSize: 10
      },
      selectedRows: [],
      currentClass: null,
      classList: [
        { id: 1, className: 'Java全栈01班', courseName: 'Java全栈开发', teacher: '张老师', classroom: 'A101', startTime: '09:00', endTime: '12:00' },
        { id: 2, className: 'Java全栈02班', courseName: 'Java全栈开发', teacher: '张老师', classroom: 'A102', startTime: '14:00', endTime: '17:00' },
        { id: 3, className: 'Python01班', courseName: 'Python人工智能', teacher: '李老师', classroom: 'A201', startTime: '09:00', endTime: '12:00' },
        { id: 4, className: 'UI设计01班', courseName: 'UI/UX设计实战', teacher: '王老师', classroom: 'B101', startTime: '10:00', endTime: '13:00' },
        { id: 5, className: '商务英语01班', courseName: '商务英语进阶', teacher: '刘老师', classroom: 'B102', startTime: '19:00', endTime: '21:00' },
        { id: 6, className: '前端开发01班', courseName: '前端开发工程师', teacher: '赵老师', classroom: '在线直播', startTime: '19:00', endTime: '21:30' }
      ],
      attendanceList: [],
      attendanceHistory: []
    }
  },
  computed: {
    filteredList() {
      let result = [...this.attendanceList]
      
      if (this.filterForm.status) {
        result = result.filter(item => item.status === this.filterForm.status)
      }
      
      return result
    },
    paginatedList() {
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      return this.filteredList.slice(start, end)
    },
    totalCount() {
      return this.attendanceList.length
    },
    presentCount() {
      return this.attendanceList.filter(item => item.status === 'present').length
    },
    lateCount() {
      return this.attendanceList.filter(item => item.status === 'late').length
    },
    absentCount() {
      return this.attendanceList.filter(item => item.status === 'absent').length
    },
    leaveCount() {
      return this.attendanceList.filter(item => item.status === 'leave').length
    }
  },
  methods: {
    indexMethod(index) {
      return (this.pagination.currentPage - 1) * this.pagination.pageSize + index + 1
    },
    updateTime() {
      const now = new Date()
      const pad = n => n < 10 ? '0' + n : n
      this.currentTime = `${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`
    },
    getStatusType(status) {
      const map = {
        'pending': '',
        'present': 'success',
        'late': 'warning',
        'absent': 'danger',
        'leave': 'info'
      }
      return map[status] || 'info'
    },
    getStatusIcon(status) {
      const map = {
        'pending': 'el-icon-question',
        'present': 'el-icon-check',
        'late': 'el-icon-time',
        'absent': 'el-icon-close',
        'leave': 'el-icon-document'
      }
      return map[status] || ''
    },
    getStatusText(status) {
      const map = {
        'pending': '未打卡',
        'present': '出勤',
        'late': '迟到',
        'absent': '缺勤',
        'leave': '请假'
      }
      return map[status] || '未知'
    },
    onClassChange(val) {
      this.currentClass = this.classList.find(item => item.id === val)
    },
    loadAttendance() {
      if (!this.filterForm.classId) {
        this.$message.warning('请先选择班级')
        return
      }
      if (!this.filterForm.date) {
        this.$message.warning('请选择上课日期')
        return
      }
      
      this.loading = true
      this.selectedRows = []
      this.pagination.currentPage = 1
      
      setTimeout(() => {
        const classStudents = this.getClassStudents(this.filterForm.classId)
        this.attendanceList = classStudents.map(student => ({
          ...student,
          checkInTime: '',
          status: 'pending',
          remark: ''
        }))
        this.loading = false
        this.$message.success('考勤名单加载成功')
        if (this.$refs.attendanceTable) {
          this.$refs.attendanceTable.clearSelection()
        }
      }, 500)
    },
    getClassStudents(classId) {
      const studentMap = {
        1: [
          { studentNo: 'S20240001', studentName: '张三' },
          { studentNo: 'S20240002', studentName: '李四' },
          { studentNo: 'S2024010', studentName: '王小明' },
          { studentNo: 'S2024011', studentName: '陈小红' },
          { studentNo: 'S2024012', studentName: '刘大伟' }
        ],
        2: [
          { studentNo: 'S20240007', studentName: '吴九' },
          { studentNo: 'S20240009', studentName: '钱十一' },
          { studentNo: 'S2024013', studentName: '赵强' },
          { studentNo: 'S2024014', studentName: '孙丽' }
        ],
        3: [
          { studentNo: 'S20240003', studentName: '王五' },
          { studentNo: 'S20240008', studentName: '郑十' },
          { studentNo: 'S2024015', studentName: '周杰' },
          { studentNo: 'S2024016', studentName: '吴芳' },
          { studentNo: 'S2024017', studentName: '郑军' }
        ],
        4: [
          { studentNo: 'S20240004', studentName: '赵六' },
          { studentNo: 'S2024018', studentName: '钱多多' }
        ],
        5: [
          { studentNo: 'S20240005', studentName: '孙七' },
          { studentNo: 'S2024019', studentName: '李娜' }
        ],
        6: [
          { studentNo: 'S20240006', studentName: '周八' },
          { studentNo: 'S2024020', studentName: '王飞' },
          { studentNo: 'S2024021', studentName: '刘洋' },
          { studentNo: 'S2024022', studentName: '陈静' }
        ]
      }
      return studentMap[classId] || []
    },
    handleSelectionChange(rows) {
      this.selectedRows = rows
    },
    handleSelectAll(selectAll) {
      if (this.$refs.attendanceTable) {
        if (selectAll) {
          this.filteredList.forEach(row => {
            this.$refs.attendanceTable.toggleRowSelection(row, true)
          })
        } else {
          this.$refs.attendanceTable.clearSelection()
        }
      }
    },
    markAttendance(row, status) {
      row.status = status
      if (status !== 'absent' && status !== 'leave') {
        const now = new Date()
        const pad = n => n < 10 ? '0' + n : n
        row.checkInTime = `${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`
      }
    },
    batchMark(status) {
      if (this.selectedRows.length === 0) {
        this.$message.warning('请先选择要标记的学员')
        return
      }
      const now = new Date()
      const pad = n => n < 10 ? '0' + n : n
      const timeStr = `${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`
      
      this.selectedRows.forEach(row => {
        row.status = status
        if (status !== 'absent' && status !== 'leave') {
          row.checkInTime = timeStr
        }
      })
      this.$message.success(`已批量标记${this.selectedRows.length}名学员为${this.getStatusText(status)}`)
    },
    submitAllAttendance() {
      const pendingCount = this.attendanceList.filter(item => item.status === 'pending').length
      
      if (pendingCount > 0) {
        this.$confirm(`还有 ${pendingCount} 名学员未打卡，确定全部提交吗？`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.doSubmitAttendance()
        }).catch(() => {})
      } else {
        this.doSubmitAttendance()
      }
    },
    doSubmitAttendance() {
      this.loading = true
      setTimeout(() => {
        this.loading = false
        const present = this.presentCount
        const late = this.lateCount
        const absent = this.absentCount
        const leave = this.leaveCount
        
        const historyRecord = {
          classId: this.filterForm.classId,
          className: this.currentClass?.className,
          date: this.filterForm.date,
          present,
          late,
          absent,
          leave,
          submitTime: new Date().toLocaleString()
        }
        this.attendanceHistory.push(historyRecord)
        
        this.$message({
          message: `考勤提交成功！出勤: ${present}人，迟到: ${late}人，缺勤: ${absent}人，请假: ${leave}人`,
          type: 'success',
          duration: 5000
        })
        
        if (this.$refs.attendanceTable) {
          this.$refs.attendanceTable.clearSelection()
        }
      }, 800)
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
    },
    resetFilter() {
      this.filterForm.status = ''
      this.pagination.currentPage = 1
    }
  },
  mounted() {
    this.updateTime()
    this.timer = setInterval(() => {
      this.updateTime()
    }, 1000)
    
    const now = new Date()
    const pad = n => n < 10 ? '0' + n : n
    this.filterForm.date = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`
  },
  beforeDestroy() {
    if (this.timer) {
      clearInterval(this.timer)
    }
  }
}
</script>

<style scoped lang="scss">
.attendance-header {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #EBEEF5;
}

.attendance-stats {
  margin-top: 15px;
  display: flex;
  gap: 15px;
  
  .stat-card {
    flex: 1;
    background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    
    .stat-item {
      text-align: center;
      
      .stat-label {
        display: block;
        font-size: 13px;
        color: #909399;
        margin-bottom: 5px;
      }
      
      .stat-value {
        display: block;
        font-size: 15px;
        font-weight: 600;
        color: #303133;
      }
    }
  }
}

.attendance-summary {
  .summary-item {
    text-align: center;
    padding: 20px;
    border-radius: 8px;
    color: #fff;
    
    &.total {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    &.present {
      background: linear-gradient(135deg, #67C23A 0%, #85CE61 100%);
    }
    
    &.late {
      background: linear-gradient(135deg, #E6A23C 0%, #EEBE77 100%);
    }
    
    &.absent {
      background: linear-gradient(135deg, #F56C6C 0%, #F78989 100%);
    }
    
    &.leave {
      background: linear-gradient(135deg, #909399 0%, #A6A9AD 100%);
    }
    
    .summary-count {
      font-size: 32px;
      font-weight: bold;
      margin-bottom: 5px;
    }
    
    .summary-label {
      font-size: 14px;
      opacity: 0.9;
    }
  }
}

.table-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  .toolbar-left {
    display: flex;
    align-items: center;
  }
  
  .toolbar-right {
    display: flex;
    align-items: center;
    gap: 10px;
  }
}

.pagination-wrapper {
  .el-pagination {
    display: inline-block;
  }
}
</style>