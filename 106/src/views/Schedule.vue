<template>
  <div class="page-container">
    <div class="card-wrapper">
      <div class="table-toolbar">
        <div class="search-form">
          <el-select v-model="searchForm.courseId" placeholder="选择课程" style="width: 180px" clearable>
            <el-option v-for="item in courseList" :key="item.id" :label="item.courseName" :value="item.id"></el-option>
          </el-select>
          <el-date-picker
            v-model="searchForm.month"
            type="month"
            placeholder="选择月份"
            style="width: 180px"
            value-format="yyyy-MM"
          ></el-date-picker>
          <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
        </div>
        <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新增排课</el-button>
      </div>

      <el-table :data="filteredSchedules" border stripe style="width: 100%" v-loading="loading">
        <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
        <el-table-column prop="className" label="班级名称" width="150" align="center"></el-table-column>
        <el-table-column prop="courseName" label="课程名称" min-width="150"></el-table-column>
        <el-table-column prop="teacher" label="授课老师" width="120" align="center"></el-table-column>
        <el-table-column prop="classDate" label="上课日期" width="120" align="center"></el-table-column>
        <el-table-column prop="timeSlot" label="上课时段" width="150" align="center">
          <template slot-scope="scope">
            <el-tag type="primary" size="small">{{ scope.row.startTime }} - {{ scope.row.endTime }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="classroom" label="教室" width="100" align="center"></el-table-column>
        <el-table-column prop="studentCount" label="已报名/容量" width="120" align="center">
          <template slot-scope="scope">
            <span style="color: #409EFF">{{ scope.row.studentCount }}</span> / {{ scope.row.maxStudents }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="small">{{ getStatusText(scope.row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button type="text" size="small" icon="el-icon-edit" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="text" size="small" icon="el-icon-view" @click="handleView(scope.row)">详情</el-button>
            <el-button type="text" size="small" icon="el-icon-delete" style="color: #f56c6c" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrapper mt-20 text-right">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.currentPage"
          :page-sizes="[10, 20, 50]"
          :page-size="pagination.pageSize"
          layout="total, sizes, prev, pager, next"
          :total="pagination.total"
        ></el-pagination>
      </div>
    </div>

    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="700px" :close-on-click-modal="false">
      <div class="conflict-warning" v-if="conflictInfo.hasConflict" style="margin-bottom: 15px">
        <el-alert
          :title="'该教室在此时段已有课程：' + conflictInfo.className + ' (' + conflictInfo.timeSlot + ')'"
          type="warning"
          show-icon
          :closable="false"
        ></el-alert>
      </div>
      <el-form :model="scheduleForm" :rules="formRules" ref="scheduleFormRef" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="班级名称" prop="className">
              <el-input v-model="scheduleForm.className" placeholder="请输入班级名称"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="所属课程" prop="courseId">
              <el-select v-model="scheduleForm.courseId" placeholder="请选择课程" style="width: 100%" @change="onCourseChange">
                <el-option v-for="item in courseList" :key="item.id" :label="item.courseName" :value="item.id"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="授课老师" prop="teacher">
              <el-input v-model="scheduleForm.teacher" placeholder="请输入授课老师"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="上课教室" prop="classroom">
              <el-select v-model="scheduleForm.classroom" placeholder="请选择教室" style="width: 100%" @change="checkConflict">
                <el-option label="A101" value="A101"></el-option>
                <el-option label="A102" value="A102"></el-option>
                <el-option label="A201" value="A201"></el-option>
                <el-option label="B101" value="B101"></el-option>
                <el-option label="B102" value="B102"></el-option>
                <el-option label="在线直播" value="在线直播"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="上课日期" prop="classDate">
              <el-date-picker
                v-model="scheduleForm.classDate"
                type="date"
                placeholder="选择日期"
                style="width: 100%"
                value-format="yyyy-MM-dd"
                @change="checkConflict"
              ></el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="上课时段" required>
              <el-col :span="11">
                <el-time-picker
                  v-model="scheduleForm.startTime"
                  placeholder="开始时间"
                  format="HH:mm"
                  value-format="HH:mm"
                  style="width: 100%"
                  @change="checkConflict"
                  :disabled-hours="disabledHours"
                  :disabled-minutes="disabledMinutes"
                ></el-time-picker>
              </el-col>
              <el-col :span="2" class="text-center" style="line-height: 40px">至</el-col>
              <el-col :span="11">
                <el-time-picker
                  v-model="scheduleForm.endTime"
                  placeholder="结束时间"
                  format="HH:mm"
                  value-format="HH:mm"
                  style="width: 100%"
                  @change="checkConflict"
                  :disabled-hours="disabledHours"
                  :disabled-minutes="disabledMinutes"
                ></el-time-picker>
              </el-col>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="最大人数" prop="maxStudents">
              <el-input-number v-model="scheduleForm.maxStudents" :min="5" :max="100" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="班级状态" prop="status">
              <el-radio-group v-model="scheduleForm.status">
                <el-radio label="not_started">未开始</el-radio>
                <el-radio label="ongoing">进行中</el-radio>
                <el-radio label="completed">已结束</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="备注" prop="remark">
          <el-input type="textarea" v-model="scheduleForm.remark" :rows="3" placeholder="请输入备注信息"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleSubmit">确 定</el-button>
      </div>
    </el-dialog>

    <el-dialog title="班级详情" :visible.sync="detailVisible" width="600px">
      <el-descriptions :column="2" border v-if="currentDetail">
        <el-descriptions-item label="班级名称">{{ currentDetail.className }}</el-descriptions-item>
        <el-descriptions-item label="课程名称">{{ currentDetail.courseName }}</el-descriptions-item>
        <el-descriptions-item label="授课老师">{{ currentDetail.teacher }}</el-descriptions-item>
        <el-descriptions-item label="上课教室">{{ currentDetail.classroom }}</el-descriptions-item>
        <el-descriptions-item label="上课日期">{{ currentDetail.classDate }}</el-descriptions-item>
        <el-descriptions-item label="上课时段">{{ currentDetail.startTime }} - {{ currentDetail.endTime }}</el-descriptions-item>
        <el-descriptions-item label="报名人数">{{ currentDetail.studentCount }} / {{ currentDetail.maxStudents }}</el-descriptions-item>
        <el-descriptions-item label="班级状态">
          <el-tag :type="getStatusType(currentDetail.status)">{{ getStatusText(currentDetail.status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentDetail.remark || '暂无备注' }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'Schedule',
  data() {
    return {
      loading: false,
      searchForm: {
        courseId: '',
        month: ''
      },
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      dialogVisible: false,
      dialogTitle: '新增排课',
      detailVisible: false,
      isEdit: false,
      currentDetail: null,
      conflictInfo: {
        hasConflict: false,
        className: '',
        timeSlot: ''
      },
      scheduleForm: {
        id: '',
        className: '',
        courseId: '',
        courseName: '',
        teacher: '',
        classroom: '',
        classDate: '',
        startTime: '',
        endTime: '',
        maxStudents: 30,
        studentCount: 0,
        status: 'not_started',
        remark: ''
      },
      formRules: {
        className: [
          { required: true, message: '请输入班级名称', trigger: 'blur' },
          { min: 2, max: 30, message: '长度在 2 到 30 个字符', trigger: 'blur' }
        ],
        courseId: [
          { required: true, message: '请选择课程', trigger: 'change' }
        ],
        teacher: [
          { required: true, message: '请输入授课老师', trigger: 'blur' }
        ],
        classroom: [
          { required: true, message: '请选择教室', trigger: 'change' }
        ],
        classDate: [
          { required: true, message: '请选择上课日期', trigger: 'change' }
        ],
        maxStudents: [
          { required: true, message: '请输入最大人数', trigger: 'blur' }
        ]
      },
      courseList: [
        { id: 1, courseName: 'Java全栈开发', teacher: '张老师' },
        { id: 2, courseName: 'Python人工智能', teacher: '李老师' },
        { id: 3, courseName: 'UI/UX设计实战', teacher: '王老师' },
        { id: 4, courseName: '商务英语进阶', teacher: '刘老师' },
        { id: 6, courseName: '前端开发工程师', teacher: '赵老师' }
      ],
      schedules: [
        { id: 1, className: 'Java全栈01班', courseId: 1, courseName: 'Java全栈开发', teacher: '张老师', classroom: 'A101', classDate: '2024-03-18', startTime: '09:00', endTime: '12:00', maxStudents: 30, studentCount: 25, status: 'ongoing', remark: '周一、三、五上课' },
        { id: 2, className: 'Java全栈02班', courseId: 1, courseName: 'Java全栈开发', teacher: '张老师', classroom: 'A102', classDate: '2024-03-18', startTime: '14:00', endTime: '17:00', maxStudents: 30, studentCount: 28, status: 'ongoing', remark: '周二、四、六上课' },
        { id: 3, className: 'Python01班', courseId: 2, courseName: 'Python人工智能', teacher: '李老师', classroom: 'A201', classDate: '2024-03-19', startTime: '09:00', endTime: '12:00', maxStudents: 25, studentCount: 20, status: 'not_started', remark: '周一至周五上课' },
        { id: 4, className: 'UI设计01班', courseId: 3, courseName: 'UI/UX设计实战', teacher: '王老师', classroom: 'B101', classDate: '2024-03-20', startTime: '10:00', endTime: '13:00', maxStudents: 20, studentCount: 18, status: 'ongoing', remark: '周末班' },
        { id: 5, className: '商务英语01班', courseId: 4, courseName: '商务英语进阶', teacher: '刘老师', classroom: 'B102', classDate: '2024-03-15', startTime: '19:00', endTime: '21:00', maxStudents: 30, studentCount: 22, status: 'completed', remark: '晚班课程' },
        { id: 6, className: '前端开发01班', courseId: 6, courseName: '前端开发工程师', teacher: '赵老师', classroom: '在线直播', classDate: '2024-03-21', startTime: '19:00', endTime: '21:30', maxStudents: 50, studentCount: 45, status: 'not_started', remark: '线上直播课程' }
      ]
    }
  },
  computed: {
    filteredSchedules() {
      let result = [...this.schedules]
      
      if (this.searchForm.courseId) {
        result = result.filter(item => item.courseId === this.searchForm.courseId)
      }
      
      if (this.searchForm.month) {
        result = result.filter(item => item.classDate.startsWith(this.searchForm.month))
      }
      
      this.pagination.total = result.length
      
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      return result.slice(start, end)
    },
    disabledHours() {
      return []
    },
    disabledMinutes() {
      return []
    }
  },
  methods: {
    getStatusType(status) {
      const map = {
        'not_started': 'info',
        'ongoing': 'success',
        'completed': 'warning'
      }
      return map[status] || 'info'
    },
    getStatusText(status) {
      const map = {
        'not_started': '未开始',
        'ongoing': '进行中',
        'completed': '已结束'
      }
      return map[status] || '未知'
    },
    handleSearch() {
      this.pagination.currentPage = 1
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
    },
    handleAdd() {
      this.dialogTitle = '新增排课'
      this.isEdit = false
      this.resetForm()
      this.dialogVisible = true
    },
    handleEdit(row) {
      this.dialogTitle = '编辑排课'
      this.isEdit = true
      this.scheduleForm = { ...row }
      this.dialogVisible = true
    },
    handleView(row) {
      this.currentDetail = row
      this.detailVisible = true
    },
    handleDelete(row) {
      this.$confirm('确定要删除该排课吗？', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.schedules.findIndex(item => item.id === row.id)
        if (index > -1) {
          this.schedules.splice(index, 1)
          this.$message.success('删除成功')
        }
      }).catch(() => {})
    },
    onCourseChange(val) {
      const course = this.courseList.find(item => item.id === val)
      if (course) {
        this.scheduleForm.teacher = course.teacher
      }
    },
    checkConflict() {
      if (!this.scheduleForm.classroom || !this.scheduleForm.classDate || !this.scheduleForm.startTime || !this.scheduleForm.endTime) {
        this.conflictInfo.hasConflict = false
        return
      }

      const newStart = this.timeToMinutes(this.scheduleForm.startTime)
      const newEnd = this.timeToMinutes(this.scheduleForm.endTime)

      const conflict = this.schedules.find(item => {
        if (this.isEdit && item.id === this.scheduleForm.id) return false
        if (item.classroom !== this.scheduleForm.classroom) return false
        if (item.classDate !== this.scheduleForm.classDate) return false
        
        const existStart = this.timeToMinutes(item.startTime)
        const existEnd = this.timeToMinutes(item.endTime)
        
        return !(newEnd <= existStart || newStart >= existEnd)
      })

      if (conflict) {
        this.conflictInfo = {
          hasConflict: true,
          className: conflict.className,
          timeSlot: `${conflict.startTime} - ${conflict.endTime}`
        }
      } else {
        this.conflictInfo.hasConflict = false
      }
    },
    timeToMinutes(time) {
      const [hours, minutes] = time.split(':').map(Number)
      return hours * 60 + minutes
    },
    handleSubmit() {
      this.checkConflict()
      if (this.conflictInfo.hasConflict) {
        this.$message.error('教室时段冲突，无法保存排课！')
        return
      }
      
      this.$refs.scheduleFormRef.validate((valid) => {
        if (valid) {
          const course = this.courseList.find(item => item.id === this.scheduleForm.courseId)
          if (this.isEdit) {
            const index = this.schedules.findIndex(item => item.id === this.scheduleForm.id)
            if (index > -1) {
              this.schedules[index] = { 
                ...this.scheduleForm,
                courseName: course ? course.courseName : ''
              }
              this.$message.success('编辑成功')
            }
          } else {
            const newSchedule = {
              ...this.scheduleForm,
              id: Date.now(),
              courseName: course ? course.courseName : '',
              studentCount: 0
            }
            this.schedules.unshift(newSchedule)
            this.$message.success('新增成功')
          }
          this.dialogVisible = false
        }
      })
    },
    resetForm() {
      this.conflictInfo = {
        hasConflict: false,
        className: '',
        timeSlot: ''
      }
      this.scheduleForm = {
        id: '',
        className: '',
        courseId: '',
        courseName: '',
        teacher: '',
        classroom: '',
        classDate: '',
        startTime: '',
        endTime: '',
        maxStudents: 30,
        studentCount: 0,
        status: 'not_started',
        remark: ''
      }
      this.$nextTick(() => {
        this.$refs.scheduleFormRef.resetFields()
      })
    }
  },
  created() {
    this.pagination.total = this.schedules.length
  }
}
</script>

<style scoped lang="scss">
.pagination-wrapper {
  .el-pagination {
    display: inline-block;
  }
}
</style>