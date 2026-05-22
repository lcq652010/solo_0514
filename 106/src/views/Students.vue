<template>
  <div class="page-container">
    <div class="card-wrapper">
      <div class="table-toolbar">
        <div class="search-form">
          <el-input v-model="searchForm.keyword" placeholder="搜索学员姓名/手机号" style="width: 200px" clearable></el-input>
          <el-select v-model="searchForm.className" placeholder="选择班级" style="width: 160px" clearable>
            <el-option v-for="item in classList" :key="item.id" :label="item.className" :value="item.className"></el-option>
          </el-select>
          <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
          <el-button icon="el-icon-refresh" @click="handleReset">重置</el-button>
        </div>
        <div>
          <el-button icon="el-icon-download" @click="handleExport">导出Excel</el-button>
          <el-button type="primary" icon="el-icon-plus" @click="handleAdd">添加学员</el-button>
        </div>
      </div>

      <el-table :data="filteredStudents" border stripe style="width: 100%" v-loading="loading">
        <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
        <el-table-column prop="studentNo" label="学号" width="100" align="center"></el-table-column>
        <el-table-column prop="name" label="姓名" width="100" align="center"></el-table-column>
        <el-table-column prop="gender" label="性别" width="80" align="center">
          <template slot-scope="scope">
            <i :class="scope.row.gender === '男' ? 'el-icon-male' : 'el-icon-female'" style="color: #409EFF"></i>
            {{ scope.row.gender }}
          </template>
        </el-table-column>
        <el-table-column prop="age" label="年龄" width="80" align="center"></el-table-column>
        <el-table-column prop="phone" label="手机号" width="130" align="center"></el-table-column>
        <el-table-column prop="className" label="所属班级" width="150" align="center">
          <template slot-scope="scope">
            <el-tag size="small">{{ scope.row.className }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="courseName" label="报名课程" min-width="150"></el-table-column>
        <el-table-column prop="enrollDate" label="报名日期" width="120" align="center"></el-table-column>
        <el-table-column prop="attendanceRate" label="出勤率" width="100" align="center">
          <template slot-scope="scope">
            <el-progress :percentage="scope.row.attendanceRate" :stroke-width="8" :show-text="false" style="width: 80px"></el-progress>
            <span style="margin-left: 5px; font-size: 12px">{{ scope.row.attendanceRate }}%</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === '在读' ? 'success' : scope.row.status === '休学' ? 'warning' : 'info'" size="small">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button type="text" size="small" icon="el-icon-view" @click="handleView(scope.row)">详情</el-button>
            <el-button type="text" size="small" icon="el-icon-edit" @click="handleEdit(scope.row)">编辑</el-button>
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

    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="650px" :close-on-click-modal="false">
      <el-form :model="studentForm" :rules="formRules" ref="studentFormRef" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="学号" prop="studentNo">
              <el-input v-model="studentForm.studentNo" placeholder="自动生成" :disabled="isEdit"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="studentForm.name" placeholder="请输入姓名"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-radio-group v-model="studentForm.gender">
                <el-radio label="男">男</el-radio>
                <el-radio label="女">女</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="年龄" prop="age">
              <el-input-number v-model="studentForm.age" :min="1" :max="100" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="手机号" prop="phone">
              <el-input v-model="studentForm.phone" placeholder="请输入手机号"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="studentForm.email" placeholder="请输入邮箱"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="所属班级" prop="className">
              <el-select v-model="studentForm.className" placeholder="请选择班级" style="width: 100%">
                <el-option v-for="item in classList" :key="item.id" :label="item.className" :value="item.className"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="学员状态" prop="status">
              <el-select v-model="studentForm.status" placeholder="请选择状态" style="width: 100%">
                <el-option label="在读" value="在读"></el-option>
                <el-option label="休学" value="休学"></el-option>
                <el-option label="毕业" value="毕业"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="家庭住址" prop="address">
          <el-input v-model="studentForm.address" placeholder="请输入家庭住址"></el-input>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input type="textarea" v-model="studentForm.remark" :rows="3" placeholder="请输入备注信息"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleSubmit">确 定</el-button>
      </div>
    </el-dialog>

    <el-dialog title="学员详情" :visible.sync="detailVisible" width="600px">
      <el-descriptions :column="2" border v-if="currentDetail">
        <el-descriptions-item label="学号">{{ currentDetail.studentNo }}</el-descriptions-item>
        <el-descriptions-item label="姓名">{{ currentDetail.name }}</el-descriptions-item>
        <el-descriptions-item label="性别">{{ currentDetail.gender }}</el-descriptions-item>
        <el-descriptions-item label="年龄">{{ currentDetail.age }}</el-descriptions-item>
        <el-descriptions-item label="手机号">{{ currentDetail.phone }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ currentDetail.email || '-' }}</el-descriptions-item>
        <el-descriptions-item label="所属班级">{{ currentDetail.className }}</el-descriptions-item>
        <el-descriptions-item label="报名课程">{{ currentDetail.courseName }}</el-descriptions-item>
        <el-descriptions-item label="报名日期">{{ currentDetail.enrollDate }}</el-descriptions-item>
        <el-descriptions-item label="学员状态">
          <el-tag :type="currentDetail.status === '在读' ? 'success' : currentDetail.status === '休学' ? 'warning' : 'info'">
            {{ currentDetail.status }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="出勤率">{{ currentDetail.attendanceRate }}%</el-descriptions-item>
        <el-descriptions-item label="家庭住址" :span="2">{{ currentDetail.address || '-' }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentDetail.remark || '暂无备注' }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'Students',
  data() {
    return {
      loading: false,
      searchForm: {
        keyword: '',
        className: ''
      },
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      dialogVisible: false,
      dialogTitle: '添加学员',
      detailVisible: false,
      isEdit: false,
      currentDetail: null,
      studentForm: {
        id: '',
        studentNo: '',
        name: '',
        gender: '男',
        age: 20,
        phone: '',
        email: '',
        className: '',
        courseName: '',
        address: '',
        status: '在读',
        remark: ''
      },
      formRules: {
        name: [
          { required: true, message: '请输入姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        gender: [
          { required: true, message: '请选择性别', trigger: 'change' }
        ],
        phone: [
          { required: true, message: '请输入手机号', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
        ],
        className: [
          { required: true, message: '请选择班级', trigger: 'change' }
        ],
        status: [
          { required: true, message: '请选择状态', trigger: 'change' }
        ]
      },
      classList: [
        { id: 1, className: 'Java全栈01班', courseName: 'Java全栈开发' },
        { id: 2, className: 'Java全栈02班', courseName: 'Java全栈开发' },
        { id: 3, className: 'Python01班', courseName: 'Python人工智能' },
        { id: 4, className: 'UI设计01班', courseName: 'UI/UX设计实战' },
        { id: 5, className: '商务英语01班', courseName: '商务英语进阶' },
        { id: 6, className: '前端开发01班', courseName: '前端开发工程师' }
      ],
      students: [
        { id: 1, studentNo: 'S20240001', name: '张三', gender: '男', age: 22, phone: '13800138001', email: 'zhangsan@example.com', className: 'Java全栈01班', courseName: 'Java全栈开发', enrollDate: '2024-01-10', address: '北京市朝阳区', attendanceRate: 95, status: '在读', remark: '学习认真' },
        { id: 2, studentNo: 'S20240002', name: '李四', gender: '女', age: 21, phone: '13800138002', email: 'lisi@example.com', className: 'Java全栈01班', courseName: 'Java全栈开发', enrollDate: '2024-01-12', address: '北京市海淀区', attendanceRate: 88, status: '在读', remark: '' },
        { id: 3, studentNo: 'S20240003', name: '王五', gender: '男', age: 23, phone: '13800138003', email: '', className: 'Python01班', courseName: 'Python人工智能', enrollDate: '2024-01-15', address: '上海市浦东新区', attendanceRate: 92, status: '在读', remark: '' },
        { id: 4, studentNo: 'S20240004', name: '赵六', gender: '女', age: 20, phone: '13800138004', email: 'zhaoliu@example.com', className: 'UI设计01班', courseName: 'UI/UX设计实战', enrollDate: '2024-01-18', address: '广州市天河区', attendanceRate: 100, status: '在读', remark: '表现优秀' },
        { id: 5, studentNo: 'S20240005', name: '孙七', gender: '男', age: 24, phone: '13800138005', email: '', className: '商务英语01班', courseName: '商务英语进阶', enrollDate: '2024-01-20', address: '深圳市南山区', attendanceRate: 75, status: '休学', remark: '' },
        { id: 6, studentNo: 'S20240006', name: '周八', gender: '女', age: 22, phone: '13800138006', email: 'zhouba@example.com', className: '前端开发01班', courseName: '前端开发工程师', enrollDate: '2024-02-01', address: '杭州市西湖区', attendanceRate: 98, status: '在读', remark: '' },
        { id: 7, studentNo: 'S20240007', name: '吴九', gender: '男', age: 21, phone: '13800138007', email: '', className: 'Java全栈02班', courseName: 'Java全栈开发', enrollDate: '2024-02-05', address: '成都市武侯区', attendanceRate: 85, status: '在读', remark: '' },
        { id: 8, studentNo: 'S20240008', name: '郑十', gender: '女', age: 23, phone: '13800138008', email: 'zhengshi@example.com', className: 'Python01班', courseName: 'Python人工智能', enrollDate: '2024-02-10', address: '武汉市洪山区', attendanceRate: 90, status: '在读', remark: '' }
      ]
    }
  },
  computed: {
    filteredStudents() {
      let result = [...this.students]
      
      if (this.searchForm.keyword) {
        const keyword = this.searchForm.keyword.toLowerCase()
        result = result.filter(item => 
          item.name.includes(keyword) || 
          item.phone.includes(keyword)
        )
      }
      
      if (this.searchForm.className) {
        result = result.filter(item => item.className === this.searchForm.className)
      }
      
      this.pagination.total = result.length
      
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      return result.slice(start, end)
    }
  },
  methods: {
    handleSearch() {
      this.pagination.currentPage = 1
    },
    handleReset() {
      this.searchForm = {
        keyword: '',
        className: ''
      }
      this.pagination.currentPage = 1
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
    },
    handleExport() {
      this.$message.success('导出成功')
    },
    handleAdd() {
      this.dialogTitle = '添加学员'
      this.isEdit = false
      this.resetForm()
      const now = new Date()
      const year = now.getFullYear()
      const num = String(this.students.length + 1).padStart(4, '0')
      this.studentForm.studentNo = `S${year}${num}`
      this.dialogVisible = true
    },
    handleEdit(row) {
      this.dialogTitle = '编辑学员'
      this.isEdit = true
      this.studentForm = { ...row }
      this.dialogVisible = true
    },
    handleView(row) {
      this.currentDetail = row
      this.detailVisible = true
    },
    handleDelete(row) {
      this.$confirm('确定要删除该学员吗？', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.students.findIndex(item => item.id === row.id)
        if (index > -1) {
          this.students.splice(index, 1)
          this.$message.success('删除成功')
        }
      }).catch(() => {})
    },
    handleSubmit() {
      this.$refs.studentFormRef.validate((valid) => {
        if (valid) {
          const classInfo = this.classList.find(item => item.className === this.studentForm.className)
          const now = new Date()
          const formatDate = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`
          
          if (this.isEdit) {
            const index = this.students.findIndex(item => item.id === this.studentForm.id)
            if (index > -1) {
              this.students[index] = {
                ...this.studentForm,
                courseName: classInfo ? classInfo.courseName : ''
              }
              this.$message.success('编辑成功')
            }
          } else {
            const newStudent = {
              ...this.studentForm,
              id: Date.now(),
              courseName: classInfo ? classInfo.courseName : '',
              enrollDate: formatDate,
              attendanceRate: 100
            }
            this.students.unshift(newStudent)
            this.$message.success('添加成功')
          }
          this.dialogVisible = false
        }
      })
    },
    resetForm() {
      this.studentForm = {
        id: '',
        studentNo: '',
        name: '',
        gender: '男',
        age: 20,
        phone: '',
        email: '',
        className: '',
        courseName: '',
        address: '',
        status: '在读',
        remark: ''
      }
      this.$nextTick(() => {
        this.$refs.studentFormRef.resetFields()
      })
    }
  },
  created() {
    this.pagination.total = this.students.length
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