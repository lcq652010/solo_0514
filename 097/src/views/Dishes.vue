<template>
  <div class="dishes-container">
    <el-card>
      <div slot="header" class="card-header">
        <span>菜品管理</span>
        <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新增菜品</el-button>
      </div>
      
      <el-table :data="dishes" border stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
        <el-table-column prop="name" label="菜品名称" align="center"></el-table-column>
        <el-table-column prop="categoryId" label="分类" width="120" align="center">
          <template slot-scope="scope">
            {{ getCategoryName(scope.row.categoryId) }}
          </template>
        </el-table-column>
        <el-table-column prop="price" label="售价" width="100" align="center">
          <template slot-scope="scope">
            ¥{{ scope.row.price }}
          </template>
        </el-table-column>
        <el-table-column prop="originalPrice" label="原价" width="100" align="center">
          <template slot-scope="scope">
            ¥{{ scope.row.originalPrice }}
          </template>
        </el-table-column>
        <el-table-column prop="stock" label="库存" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.stock <= 0 ? 'danger' : scope.row.stock <= 10 ? 'warning' : 'success'">
              {{ scope.row.stock }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === 1 ? 'success' : 'danger'">
              {{ scope.row.status === 1 ? '上架' : '下架' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="180" align="center"></el-table-column>
        <el-table-column label="操作" width="250" align="center">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" icon="el-icon-edit" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="mini" :type="scope.row.status === 1 ? 'warning' : 'success'" :icon="scope.row.status === 1 ? 'el-icon-bottom' : 'el-icon-top'" @click="toggleStatus(scope.row)">
              {{ scope.row.status === 1 ? '下架' : '上架' }}
            </el-button>
            <el-button size="mini" type="danger" icon="el-icon-delete" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="600px">
      <el-form :model="form" :rules="rules" ref="form" label-width="100px">
        <el-form-item label="菜品名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入菜品名称"></el-input>
        </el-form-item>
        <el-form-item label="菜品分类" prop="categoryId">
          <el-select v-model="form.categoryId" placeholder="请选择分类" style="width: 100%">
            <el-option v-for="item in categories" :key="item.id" :label="item.name" :value="item.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="售价" prop="price">
          <el-input-number v-model="form.price" :min="0" :precision="2" :step="1" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="原价" prop="originalPrice">
          <el-input-number v-model="form.originalPrice" :min="0" :precision="2" :step="1" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="库存数量" prop="stock">
          <el-input-number v-model="form.stock" :min="0" :max="9999" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="排序" prop="sort">
          <el-input-number v-model="form.sort" :min="1" :max="999"></el-input-number>
        </el-form-item>
        <el-form-item label="菜品描述" prop="description">
          <el-input type="textarea" v-model="form.description" :rows="3" placeholder="请输入菜品描述"></el-input>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio :label="1">上架</el-radio>
            <el-radio :label="0">下架</el-radio>
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
import { mockDishes, mockCategories } from '../data/mockData'

export default {
  name: 'Dishes',
  data() {
    return {
      dishes: [],
      categories: [],
      dialogVisible: false,
      dialogTitle: '新增菜品',
      isEdit: false,
      form: {
        id: null,
        name: '',
        categoryId: '',
        price: 0,
        originalPrice: 0,
        stock: 0,
        sort: 1,
        description: '',
        status: 1
      },
      rules: {
        name: [
          { required: true, message: '请输入菜品名称', trigger: 'blur' },
          { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
        ],
        categoryId: [
          { required: true, message: '请选择菜品分类', trigger: 'change' }
        ],
        price: [
          { required: true, message: '请输入售价', trigger: 'blur' }
        ],
        originalPrice: [
          { required: true, message: '请输入原价', trigger: 'blur' }
        ],
        stock: [
          { required: true, message: '请输入库存数量', trigger: 'blur' },
          { type: 'number', min: 0, message: '库存数量不能小于0', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.dishes = [...mockDishes]
    this.categories = [...mockCategories]
  },
  methods: {
    getCategoryName(categoryId) {
      const category = this.categories.find(item => item.id === categoryId)
      return category ? category.name : '未知'
    },
    handleAdd() {
      this.isEdit = false
      this.dialogTitle = '新增菜品'
      this.form = { id: null, name: '', categoryId: '', price: 0, originalPrice: 0, stock: 0, sort: this.dishes.length + 1, description: '', status: 1 }
      this.dialogVisible = true
      this.$nextTick(() => {
        this.$refs.form.resetFields()
      })
    },
    handleEdit(row) {
      this.isEdit = true
      this.dialogTitle = '编辑菜品'
      this.form = { ...row }
      this.dialogVisible = true
    },
    toggleStatus(row) {
      const status = row.status === 1 ? 0 : 1
      const msg = status === 1 ? '上架' : '下架'
      if (status === 1 && row.stock <= 0) {
        this.$message.error('库存为0时不能上架，请先补充库存！')
        return
      }
      this.$confirm(`确认${msg}该菜品吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        row.status = status
        this.$message.success(`${msg}成功`)
      }).catch(() => {})
    },
    handleDelete(row) {
      this.$confirm('确认删除该菜品吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.dishes.findIndex(item => item.id === row.id)
        if (index > -1) {
          this.dishes.splice(index, 1)
          this.$message.success('删除成功')
        }
      }).catch(() => {})
    },
    handleSubmit() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          if (this.form.status === 1 && this.form.stock <= 0) {
            this.$message.error('库存为0时不能上架，请先补充库存！')
            return
          }
          if (this.isEdit) {
            const index = this.dishes.findIndex(item => item.id === this.form.id)
            if (index > -1) {
              this.dishes[index] = { ...this.form }
              this.$message.success('编辑成功')
            }
          } else {
            const newId = Math.max(...this.dishes.map(item => item.id)) + 1
            this.dishes.push({
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

.dishes-container {
  padding: 0;
}
</style>