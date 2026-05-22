<template>
  <div class="page-container">
    <div class="page-header">
      <span class="page-title">用品分类管理</span>
    </div>
    
    <div class="search-bar">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="分类名称">
          <el-input v-model="searchForm.name" placeholder="请输入分类名称" clearable></el-input>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
            <el-option label="启用" :value="1"></el-option>
            <el-option label="禁用" :value="0"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <i class="el-icon-search"></i> 搜索
          </el-button>
          <el-button @click="handleReset">
            <i class="el-icon-refresh"></i> 重置
          </el-button>
          <el-button type="success" @click="handleAdd">
            <i class="el-icon-plus"></i> 新增分类
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="table-container">
      <el-table :data="tableData" border stripe>
        <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
        <el-table-column prop="name" label="分类名称" min-width="150"></el-table-column>
        <el-table-column prop="description" label="描述" min-width="200"></el-table-column>
        <el-table-column prop="sort" label="排序" width="100" align="center"></el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === 1 ? 'success' : 'danger'" size="small">
              {{ scope.row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="180" align="center"></el-table-column>
        <el-table-column label="操作" width="200" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="handleEdit(scope.row)">
              <i class="el-icon-edit"></i> 编辑
            </el-button>
            <el-button size="mini" type="danger" @click="handleDelete(scope.row)">
              <i class="el-icon-delete"></i> 删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination">
        <el-pagination
          :total="total"
          :page-size="pageSize"
          :current-page="currentPage"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        ></el-pagination>
      </div>
    </div>

    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="500px">
      <el-form :model="form" :rules="rules" ref="form" label-width="100px">
        <el-form-item label="分类名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入分类名称"></el-input>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input type="textarea" v-model="form.description" :rows="3" placeholder="请输入描述"></el-input>
        </el-form-item>
        <el-form-item label="排序" prop="sort">
          <el-input-number v-model="form.sort" :min="1" :max="999"></el-input-number>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio :label="1">启用</el-radio>
            <el-radio :label="0">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { categories } from '@/api/mockData'

export default {
  name: 'Categories',
  data() {
    return {
      searchForm: {
        name: '',
        status: null
      },
      tableData: [],
      total: 0,
      pageSize: 10,
      currentPage: 1,
      dialogVisible: false,
      dialogTitle: '新增分类',
      isEdit: false,
      form: {
        id: null,
        name: '',
        description: '',
        sort: 1,
        status: 1
      },
      rules: {
        name: [
          { required: true, message: '请输入分类名称', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        sort: [
          { required: true, message: '请输入排序', trigger: 'blur' }
        ]
      },
      dataList: []
    }
  },
  created() {
    this.dataList = [...categories]
    this.loadData()
  },
  methods: {
    loadData() {
      let filtered = [...this.dataList]
      
      if (this.searchForm.name) {
        filtered = filtered.filter(item => item.name.includes(this.searchForm.name))
      }
      
      if (this.searchForm.status !== null && this.searchForm.status !== '') {
        filtered = filtered.filter(item => item.status === this.searchForm.status)
      }
      
      this.total = filtered.length
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      this.tableData = filtered.slice(start, end)
    },
    handleSearch() {
      this.currentPage = 1
      this.loadData()
    },
    handleReset() {
      this.searchForm = {
        name: '',
        status: null
      }
      this.currentPage = 1
      this.loadData()
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.loadData()
    },
    handlePageChange(val) {
      this.currentPage = val
      this.loadData()
    },
    handleAdd() {
      this.isEdit = false
      this.dialogTitle = '新增分类'
      this.form = {
        id: null,
        name: '',
        description: '',
        sort: 1,
        status: 1
      }
      this.dialogVisible = true
      this.$nextTick(() => {
        this.$refs.form.clearValidate()
      })
    },
    handleEdit(row) {
      this.isEdit = true
      this.dialogTitle = '编辑分类'
      this.form = { ...row }
      this.dialogVisible = true
    },
    handleSubmit() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          if (this.isEdit) {
            const index = this.dataList.findIndex(item => item.id === this.form.id)
            if (index !== -1) {
              this.dataList[index] = { ...this.form }
            }
            this.$message.success('编辑成功')
          } else {
            const newId = Math.max(...this.dataList.map(item => item.id)) + 1
            const newItem = {
              ...this.form,
              id: newId,
              createTime: new Date().toISOString().split('T')[0]
            }
            this.dataList.push(newItem)
            this.$message.success('新增成功')
          }
          this.dialogVisible = false
          this.loadData()
        }
      })
    },
    handleDelete(row) {
      this.$confirm('确定要删除该分类吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.dataList.findIndex(item => item.id === row.id)
        if (index !== -1) {
          this.dataList.splice(index, 1)
          this.loadData()
          this.$message.success('删除成功')
        }
      }).catch(() => {})
    }
  }
}
</script>
