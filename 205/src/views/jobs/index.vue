<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">岗位列表</h2>
      <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新增岗位</el-button>
    </div>

    <div class="search-bar">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="岗位名称">
          <el-input v-model="searchForm.name" placeholder="请输入岗位名称" clearable></el-input>
        </el-form-item>
        <el-form-item label="所属部门">
          <el-select v-model="searchForm.department" placeholder="请选择部门" clearable style="width: 180px;">
            <el-option v-for="item in departmentOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="岗位类型">
          <el-select v-model="searchForm.type" placeholder="请选择类型" clearable style="width: 180px;">
            <el-option v-for="item in jobTypeOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable style="width: 180px;">
            <el-option label="招聘中" value="招聘中"></el-option>
            <el-option label="已暂停" value="已暂停"></el-option>
            <el-option label="已关闭" value="已关闭"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
          <el-button icon="el-icon-refresh" @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="table-container">
      <el-table :data="filteredList" border stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
        <el-table-column prop="name" label="岗位名称" min-width="150"></el-table-column>
        <el-table-column prop="department" label="所属部门" width="120" align="center"></el-table-column>
        <el-table-column prop="type" label="岗位类型" width="120" align="center"></el-table-column>
        <el-table-column prop="salary" label="薪资范围" width="120" align="center"></el-table-column>
        <el-table-column prop="location" label="工作地点" width="100" align="center"></el-table-column>
        <el-table-column prop="people" label="招聘人数" width="100" align="center"></el-table-column>
        <el-table-column prop="publishTime" label="发布时间" width="120" align="center"></el-table-column>
        <el-table-column label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === '招聘中' ? 'success' : scope.row.status === '已暂停' ? 'warning' : 'info'">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button size="mini" type="text" icon="el-icon-view" @click="handleView(scope.row)">查看</el-button>
            <el-button size="mini" type="text" icon="el-icon-edit" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="mini" type="text" icon="el-icon-delete" style="color: #F56C6C" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="filteredList.length">
      </el-pagination>
    </div>

    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="600px" @close="handleDialogClose">
      <el-form :model="jobForm" :rules="jobRules" ref="jobForm" label-width="100px">
        <el-form-item label="岗位名称" prop="name">
          <el-input v-model="jobForm.name" placeholder="请输入岗位名称"></el-input>
        </el-form-item>
        <el-form-item label="所属部门" prop="department">
          <el-select v-model="jobForm.department" placeholder="请选择部门" style="width: 100%;">
            <el-option v-for="item in departmentOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="岗位类型" prop="type">
          <el-select v-model="jobForm.type" placeholder="请选择类型" style="width: 100%;">
            <el-option v-for="item in jobTypeOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="薪资范围" prop="salary">
          <el-input v-model="jobForm.salary" placeholder="如：15k-25k"></el-input>
        </el-form-item>
        <el-form-item label="工作地点" prop="location">
          <el-input v-model="jobForm.location" placeholder="请输入工作地点"></el-input>
        </el-form-item>
        <el-form-item label="招聘人数" prop="people">
          <el-input-number v-model="jobForm.people" :min="1" :max="100"></el-input-number>
        </el-form-item>
        <el-form-item label="岗位状态" prop="status">
          <el-radio-group v-model="jobForm.status">
            <el-radio label="招聘中">招聘中</el-radio>
            <el-radio label="已暂停">已暂停</el-radio>
            <el-radio label="已关闭">已关闭</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="岗位职责" prop="description">
          <el-input type="textarea" v-model="jobForm.description" :rows="4" placeholder="请输入岗位职责"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </span>
    </el-dialog>

    <el-dialog title="岗位详情" :visible.sync="detailVisible" width="600px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="岗位名称">{{ jobDetail.name }}</el-descriptions-item>
        <el-descriptions-item label="所属部门">{{ jobDetail.department }}</el-descriptions-item>
        <el-descriptions-item label="岗位类型">{{ jobDetail.type }}</el-descriptions-item>
        <el-descriptions-item label="薪资范围">{{ jobDetail.salary }}</el-descriptions-item>
        <el-descriptions-item label="工作地点">{{ jobDetail.location }}</el-descriptions-item>
        <el-descriptions-item label="招聘人数">{{ jobDetail.people }}人</el-descriptions-item>
        <el-descriptions-item label="发布时间">{{ jobDetail.publishTime }}</el-descriptions-item>
        <el-descriptions-item label="岗位状态">
          <el-tag :type="jobDetail.status === '招聘中' ? 'success' : jobDetail.status === '已暂停' ? 'warning' : 'info'">
            {{ jobDetail.status }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="岗位职责" :span="2">
          {{ jobDetail.description }}
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script>
import { jobList, departmentOptions, jobTypeOptions } from '@/mock/data.js'

export default {
  name: 'Jobs',
  data() {
    return {
      list: [...jobList],
      searchForm: {
        name: '',
        department: '',
        type: '',
        status: ''
      },
      currentPage: 1,
      pageSize: 10,
      dialogVisible: false,
      dialogType: 'add',
      dialogTitle: '新增岗位',
      detailVisible: false,
      jobDetail: {},
      jobForm: {
        id: null,
        name: '',
        department: '',
        type: '',
        salary: '',
        location: '',
        people: 1,
        status: '招聘中',
        description: ''
      },
      jobRules: {
        name: [{ required: true, message: '请输入岗位名称', trigger: 'blur' }],
        department: [{ required: true, message: '请选择所属部门', trigger: 'change' }],
        type: [{ required: true, message: '请选择岗位类型', trigger: 'change' }],
        salary: [{ required: true, message: '请输入薪资范围', trigger: 'blur' }],
        location: [{ required: true, message: '请输入工作地点', trigger: 'blur' }],
        people: [{ required: true, message: '请输入招聘人数', trigger: 'change' }],
        status: [{ required: true, message: '请选择岗位状态', trigger: 'change' }],
        description: [{ required: true, message: '请输入岗位职责', trigger: 'blur' }]
      },
      departmentOptions,
      jobTypeOptions
    }
  },
  computed: {
    filteredList() {
      return this.list.filter(item => {
        const matchName = !this.searchForm.name || item.name.includes(this.searchForm.name)
        const matchDept = !this.searchForm.department || item.department === this.searchForm.department
        const matchType = !this.searchForm.type || item.type === this.searchForm.type
        const matchStatus = !this.searchForm.status || item.status === this.searchForm.status
        return matchName && matchDept && matchType && matchStatus
      })
    }
  },
  methods: {
    handleSearch() {
      this.currentPage = 1
    },
    handleReset() {
      this.searchForm = { name: '', department: '', type: '', status: '' }
      this.currentPage = 1
    },
    handleAdd() {
      this.dialogType = 'add'
      this.dialogTitle = '新增岗位'
      this.resetForm()
      this.dialogVisible = true
    },
    handleEdit(row) {
      this.dialogType = 'edit'
      this.dialogTitle = '编辑岗位'
      this.jobForm = { ...row }
      this.dialogVisible = true
    },
    handleView(row) {
      this.jobDetail = { ...row }
      this.detailVisible = true
    },
    handleDelete(row) {
      this.$confirm(`确定要删除岗位"${row.name}"吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.list.findIndex(item => item.id === row.id)
        if (index > -1) {
          this.list.splice(index, 1)
        }
        this.$message.success('删除成功')
      }).catch(() => {})
    },
    handleSubmit() {
      this.$refs.jobForm.validate((valid) => {
        if (valid) {
          if (this.dialogType === 'add') {
            const newId = Math.max(...this.list.map(item => item.id)) + 1
            const today = new Date().toISOString().split('T')[0]
            this.list.push({ ...this.jobForm, id: newId, publishTime: today })
            this.$message.success('新增成功')
          } else {
            const index = this.list.findIndex(item => item.id === this.jobForm.id)
            if (index > -1) {
              this.list.splice(index, 1, { ...this.jobForm })
            }
            this.$message.success('编辑成功')
          }
          this.dialogVisible = false
        }
      })
    },
    handleDialogClose() {
      this.resetForm()
    },
    resetForm() {
      this.jobForm = {
        id: null,
        name: '',
        department: '',
        type: '',
        salary: '',
        location: '',
        people: 1,
        status: '招聘中',
        description: ''
      }
      this.$nextTick(() => {
        if (this.$refs.jobForm) {
          this.$refs.jobForm.clearValidate()
        }
      })
    },
    handleSizeChange(val) {
      this.pageSize = val
    },
    handleCurrentChange(val) {
      this.currentPage = val
    }
  }
}
</script>

<style lang="scss" scoped>
.search-form {
  margin-bottom: 0;
}
</style>
