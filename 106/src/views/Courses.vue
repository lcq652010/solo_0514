<template>
  <div class="page-container">
    <div class="card-wrapper">
      <div class="table-toolbar">
        <div class="search-form">
          <el-input 
            v-model="searchForm.keyword" 
            placeholder="搜索课程名称" 
            style="width: 200px" 
            clearable
          ></el-input>
          <el-select v-model="searchForm.status" placeholder="课程状态" style="width: 120px" clearable>
            <el-option label="启用" value="enabled"></el-option>
            <el-option label="停用" value="disabled"></el-option>
          </el-select>
          <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
          <el-button icon="el-icon-refresh" @click="handleReset">重置</el-button>
        </div>
        <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新增课程</el-button>
      </div>

      <el-table :data="filteredCourses" border stripe style="width: 100%" v-loading="loading">
        <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
        <el-table-column prop="courseCode" label="课程编号" width="120" align="center"></el-table-column>
        <el-table-column prop="courseName" label="课程名称" min-width="150"></el-table-column>
        <el-table-column prop="courseType" label="课程类型" width="120" align="center">
          <template slot-scope="scope">
            <el-tag :type="getCourseTypeTag(scope.row.courseType)" size="small">{{ scope.row.courseType }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="duration" label="课时(小时)" width="120" align="center"></el-table-column>
        <el-table-column prop="price" label="学费(元)" width="120" align="center"></el-table-column>
        <el-table-column prop="teacher" label="主讲老师" width="120" align="center"></el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === 'enabled' ? 'success' : 'info'" size="small">
              {{ scope.row.status === 'enabled' ? '启用' : '停用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="160" align="center"></el-table-column>
        <el-table-column label="操作" width="200" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button type="text" size="small" icon="el-icon-edit" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="text" size="small" :icon="scope.row.status === 'enabled' ? 'el-icon-video-pause' : 'el-icon-video-play'" @click="toggleStatus(scope.row)">
              {{ scope.row.status === 'enabled' ? '停用' : '启用' }}
            </el-button>
            <el-button type="text" size="small" icon="el-icon-delete" style="color: #f56c6c" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrapper mt-20 text-right">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pagination.pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
        ></el-pagination>
      </div>
    </div>

    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="600px" :close-on-click-modal="false">
      <el-form :model="courseForm" :rules="formRules" ref="courseFormRef" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="课程编号" prop="courseCode">
              <el-input v-model="courseForm.courseCode" placeholder="请输入课程编号" :disabled="isEdit"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="课程名称" prop="courseName">
              <el-input v-model="courseForm.courseName" placeholder="请输入课程名称"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="课程类型" prop="courseType">
              <el-select v-model="courseForm.courseType" placeholder="请选择课程类型" style="width: 100%">
                <el-option label="编程开发" value="编程开发"></el-option>
                <el-option label="设计创意" value="设计创意"></el-option>
                <el-option label="语言培训" value="语言培训"></el-option>
                <el-option label="职业技能" value="职业技能"></el-option>
                <el-option label="学历提升" value="学历提升"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="主讲老师" prop="teacher">
              <el-input v-model="courseForm.teacher" placeholder="请输入主讲老师"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="课时(小时)" prop="duration">
              <el-input-number v-model="courseForm.duration" :min="1" :max="1000" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="学费(元)" prop="price">
              <el-input-number v-model="courseForm.price" :min="0" :precision="2" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="课程简介" prop="description">
          <el-input type="textarea" v-model="courseForm.description" :rows="4" placeholder="请输入课程简介"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleSubmit">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'Courses',
  data() {
    return {
      loading: false,
      searchForm: {
        keyword: '',
        status: ''
      },
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      dialogVisible: false,
      dialogTitle: '新增课程',
      isEdit: false,
      courseForm: {
        id: '',
        courseCode: '',
        courseName: '',
        courseType: '',
        duration: 40,
        price: 0,
        teacher: '',
        description: '',
        status: 'enabled'
      },
      formRules: {
        courseCode: [
          { required: true, message: '请输入课程编号', trigger: 'blur' },
          { pattern: /^[A-Za-z0-9]+$/, message: '课程编号只能包含字母和数字', trigger: 'blur' }
        ],
        courseName: [
          { required: true, message: '请输入课程名称', trigger: 'blur' },
          { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
        ],
        courseType: [
          { required: true, message: '请选择课程类型', trigger: 'change' }
        ],
        teacher: [
          { required: true, message: '请输入主讲老师', trigger: 'blur' }
        ],
        duration: [
          { required: true, message: '请输入课时', trigger: 'blur' }
        ],
        price: [
          { required: true, message: '请输入学费', trigger: 'blur' }
        ]
      },
      courses: [
        { id: 1, courseCode: 'DEV001', courseName: 'Java全栈开发', courseType: '编程开发', duration: 120, price: 12800, teacher: '张老师', status: 'enabled', createTime: '2024-01-10 10:30:00', description: '从零基础到全栈工程师' },
        { id: 2, courseCode: 'DEV002', courseName: 'Python人工智能', courseType: '编程开发', duration: 80, price: 9800, teacher: '李老师', status: 'enabled', createTime: '2024-01-12 14:20:00', description: 'Python基础与AI应用' },
        { id: 3, courseCode: 'DES001', courseName: 'UI/UX设计实战', courseType: '设计创意', duration: 60, price: 6800, teacher: '王老师', status: 'enabled', createTime: '2024-01-15 09:00:00', description: '用户界面与体验设计' },
        { id: 4, courseCode: 'LAN001', courseName: '商务英语进阶', courseType: '语言培训', duration: 40, price: 3800, teacher: '刘老师', status: 'enabled', createTime: '2024-01-18 16:45:00', description: '职场英语沟通技巧' },
        { id: 5, courseCode: 'PRO001', courseName: '产品经理实战', courseType: '职业技能', duration: 50, price: 5800, teacher: '陈老师', status: 'disabled', createTime: '2024-02-01 11:30:00', description: '产品设计与项目管理' },
        { id: 6, courseCode: 'DEV003', courseName: '前端开发工程师', courseType: '编程开发', duration: 100, price: 10800, teacher: '赵老师', status: 'enabled', createTime: '2024-02-05 08:30:00', description: 'Vue、React前端技术栈' },
        { id: 7, courseCode: 'DES002', courseName: '平面设计基础', courseType: '设计创意', duration: 30, price: 2800, teacher: '孙老师', status: 'enabled', createTime: '2024-02-10 15:00:00', description: 'Photoshop、Illustrator' },
        { id: 8, courseCode: 'LAN002', courseName: '日语N2考级班', courseType: '语言培训', duration: 60, price: 4800, teacher: '周老师', status: 'enabled', createTime: '2024-02-15 10:00:00', description: '日语能力考N2备考' }
      ]
    }
  },
  computed: {
    filteredCourses() {
      let result = [...this.courses]
      
      if (this.searchForm.keyword) {
        result = result.filter(item => 
          item.courseName.includes(this.searchForm.keyword) || 
          item.courseCode.includes(this.searchForm.keyword)
        )
      }
      
      if (this.searchForm.status) {
        result = result.filter(item => item.status === this.searchForm.status)
      }
      
      this.pagination.total = result.length
      
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      return result.slice(start, end)
    }
  },
  methods: {
    getCourseTypeTag(type) {
      const typeMap = {
        '编程开发': 'danger',
        '设计创意': 'warning',
        '语言培训': 'success',
        '职业技能': 'primary',
        '学历提升': 'info'
      }
      return typeMap[type] || 'info'
    },
    handleSearch() {
      this.pagination.currentPage = 1
    },
    handleReset() {
      this.searchForm = {
        keyword: '',
        status: ''
      }
      this.pagination.currentPage = 1
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
    },
    handleAdd() {
      this.dialogTitle = '新增课程'
      this.isEdit = false
      this.resetForm()
      this.dialogVisible = true
    },
    handleEdit(row) {
      this.dialogTitle = '编辑课程'
      this.isEdit = true
      this.courseForm = { ...row }
      this.dialogVisible = true
    },
    toggleStatus(row) {
      const newStatus = row.status === 'enabled' ? 'disabled' : 'enabled'
      this.$confirm(`确定要${newStatus === 'enabled' ? '启用' : '停用'}该课程吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        row.status = newStatus
        this.$message({
          type: 'success',
          message: `${newStatus === 'enabled' ? '启用' : '停用'}成功`
        })
      }).catch(() => {})
    },
    handleDelete(row) {
      this.$confirm('确定要删除该课程吗？删除后无法恢复！', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'error'
      }).then(() => {
        const index = this.courses.findIndex(item => item.id === row.id)
        if (index > -1) {
          this.courses.splice(index, 1)
          this.$message.success('删除成功')
        }
      }).catch(() => {})
    },
    handleSubmit() {
      this.$refs.courseFormRef.validate((valid) => {
        if (valid) {
          if (this.isEdit) {
            const index = this.courses.findIndex(item => item.id === this.courseForm.id)
            if (index > -1) {
              this.courses[index] = { ...this.courseForm }
              this.$message.success('编辑成功')
            }
          } else {
            const now = new Date()
            const formatTime = (date) => {
              const pad = n => n < 10 ? '0' + n : n
              return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`
            }
            const newCourse = {
              ...this.courseForm,
              id: Date.now(),
              createTime: formatTime(now)
            }
            this.courses.unshift(newCourse)
            this.$message.success('新增成功')
          }
          this.dialogVisible = false
        }
      })
    },
    resetForm() {
      this.courseForm = {
        id: '',
        courseCode: '',
        courseName: '',
        courseType: '',
        duration: 40,
        price: 0,
        teacher: '',
        description: '',
        status: 'enabled'
      }
      this.$nextTick(() => {
        this.$refs.courseFormRef.resetFields()
      })
    }
  },
  created() {
    this.pagination.total = this.courses.length
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