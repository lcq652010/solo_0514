<template>
  <div class="categories-container">
    <el-card>
      <div slot="header" class="card-header">
        <span>菜品分类管理</span>
        <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新增分类</el-button>
      </div>
      
      <el-table :data="categories" border stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
        <el-table-column prop="name" label="分类名称" align="center"></el-table-column>
        <el-table-column prop="sort" label="排序" width="100" align="center"></el-table-column>
        <el-table-column prop="status" label="状态" width="120" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === 1 ? 'success' : 'danger'">
              {{ scope.row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="180" align="center"></el-table-column>
        <el-table-column label="操作" width="200" align="center">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" icon="el-icon-edit" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="mini" type="danger" icon="el-icon-delete" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="500px">
      <el-form :model="form" :rules="rules" ref="form" label-width="100px">
        <el-form-item label="分类名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入分类名称"></el-input>
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
import { mockCategories } from '../data/mockData'

export default {
  name: 'Categories',
  data() {
    return {
      categories: [],
      dialogVisible: false,
      dialogTitle: '新增分类',
      isEdit: false,
      form: {
        id: null,
        name: '',
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
      }
    }
  },
  created() {
    this.categories = [...mockCategories]
  },
  methods: {
    handleAdd() {
      this.isEdit = false
      this.dialogTitle = '新增分类'
      this.form = { id: null, name: '', sort: this.categories.length + 1, status: 1 }
      this.dialogVisible = true
      this.$nextTick(() => {
        this.$refs.form.resetFields()
      })
    },
    handleEdit(row) {
      this.isEdit = true
      this.dialogTitle = '编辑分类'
      this.form = { ...row }
      this.dialogVisible = true
    },
    handleDelete(row) {
      this.$confirm('确认删除该分类吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.categories.findIndex(item => item.id === row.id)
        if (index > -1) {
          this.categories.splice(index, 1)
          this.$message.success('删除成功')
        }
      }).catch(() => {})
    },
    handleSubmit() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          if (this.isEdit) {
            const index = this.categories.findIndex(item => item.id === this.form.id)
            if (index > -1) {
              this.categories[index] = { ...this.form }
              this.$message.success('编辑成功')
            }
          } else {
            const newId = Math.max(...this.categories.map(item => item.id)) + 1
            this.categories.push({
              ...this.form,
              id: newId,
              createTime: new Date().toLocaleString()
            })
            this.$message.success('新增成功')
          }
          this.dialogVisible = false
        }
      })
    }
  }
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.categories-container {
  padding: 0;
}
</style>