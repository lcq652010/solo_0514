<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">农产品列表</h2>
      <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新增农产品</el-button>
    </div>

    <div class="search-bar">
      <el-form :inline="true" :model="searchForm" size="small">
        <el-form-item label="名称">
          <el-input v-model="searchForm.name" placeholder="请输入农产品名称" clearable style="width: 180px"></el-input>
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="searchForm.category" placeholder="请选择分类" clearable style="width: 150px">
            <el-option
              v-for="item in productCategories"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
          <el-button icon="el-icon-refresh" @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="table-card">
      <el-table :data="tableData" border stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
        <el-table-column prop="name" label="农产品名称" min-width="120"></el-table-column>
        <el-table-column prop="category" label="分类" width="100" align="center"></el-table-column>
        <el-table-column prop="spec" label="规格" width="120"></el-table-column>
        <el-table-column prop="unit" label="单位" width="80" align="center"></el-table-column>
        <el-table-column prop="price" label="单价(元)" width="120" align="center">
          <template slot-scope="scope">
            {{ scope.row.price | formatCurrency }}
          </template>
        </el-table-column>
        <el-table-column prop="stock" label="库存数量" width="120" align="center"></el-table-column>
        <el-table-column prop="createTime" label="创建时间" min-width="160" align="center">
          <template slot-scope="scope">
            {{ scope.row.createTime | formatDate }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" icon="el-icon-edit" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="mini" type="danger" icon="el-icon-delete" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.page"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pagination.size"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total">
        </el-pagination>
      </div>
    </div>

    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      width="500px"
      :close-on-click-modal="false">
      <el-form :model="productForm" :rules="rules" ref="productForm" label-width="100px">
        <el-form-item label="农产品名称" prop="name">
          <el-input v-model="productForm.name" placeholder="请输入农产品名称"></el-input>
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select v-model="productForm.category" placeholder="请选择分类" style="width: 100%">
            <el-option
              v-for="item in productCategories"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="规格" prop="spec">
          <el-input v-model="productForm.spec" placeholder="请输入规格"></el-input>
        </el-form-item>
        <el-form-item label="单位" prop="unit">
          <el-input v-model="productForm.unit" placeholder="如：斤、袋、箱"></el-input>
        </el-form-item>
        <el-form-item label="单价(元)" prop="price">
          <el-input-number v-model="productForm.price" :min="0" :precision="2" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="库存数量" prop="stock">
          <el-input-number v-model="productForm.stock" :min="0" style="width: 100%"></el-input-number>
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
import { products, productCategories } from '../mock/data.js'

export default {
  name: 'Products',
  data() {
    return {
      productCategories,
      allData: [...products],
      tableData: [],
      searchForm: {
        name: '',
        category: ''
      },
      pagination: {
        page: 1,
        size: 10,
        total: 0
      },
      dialogVisible: false,
      dialogTitle: '新增农产品',
      isEdit: false,
      productForm: {
        id: null,
        name: '',
        category: '',
        spec: '',
        unit: '',
        price: 0,
        stock: 0
      },
      rules: {
        name: [{ required: true, message: '请输入农产品名称', trigger: 'blur' }],
        category: [{ required: true, message: '请选择分类', trigger: 'change' }],
        unit: [{ required: true, message: '请输入单位', trigger: 'blur' }],
        price: [{ required: true, message: '请输入单价', trigger: 'blur' }],
        stock: [{ required: true, message: '请输入库存数量', trigger: 'blur' }]
      }
    }
  },
  created() {
    this.loadData()
  },
  methods: {
    loadData() {
      let data = [...this.allData]
      
      if (this.searchForm.name) {
        data = data.filter(item => item.name.includes(this.searchForm.name))
      }
      if (this.searchForm.category) {
        data = data.filter(item => item.category === this.searchForm.category)
      }
      
      this.pagination.total = data.length
      const start = (this.pagination.page - 1) * this.pagination.size
      const end = start + this.pagination.size
      this.tableData = data.slice(start, end)
    },
    handleSearch() {
      this.pagination.page = 1
      this.loadData()
    },
    handleReset() {
      this.searchForm = { name: '', category: '' }
      this.pagination.page = 1
      this.loadData()
    },
    handleSizeChange(val) {
      this.pagination.size = val
      this.loadData()
    },
    handleCurrentChange(val) {
      this.pagination.page = val
      this.loadData()
    },
    handleAdd() {
      this.isEdit = false
      this.dialogTitle = '新增农产品'
      this.productForm = {
        id: null,
        name: '',
        category: '',
        spec: '',
        unit: '',
        price: 0,
        stock: 0
      }
      this.dialogVisible = true
      this.$nextTick(() => {
        this.$refs.productForm && this.$refs.productForm.clearValidate()
      })
    },
    handleEdit(row) {
      this.isEdit = true
      this.dialogTitle = '编辑农产品'
      this.productForm = { ...row }
      this.dialogVisible = true
    },
    handleDelete(row) {
      this.$confirm(`确定要删除"${row.name}"吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.allData.findIndex(item => item.id === row.id)
        if (index > -1) {
          this.allData.splice(index, 1)
          this.loadData()
          this.$message.success('删除成功')
        }
      }).catch(() => {})
    },
    handleSubmit() {
      this.$refs.productForm.validate((valid) => {
        if (valid) {
          if (this.isEdit) {
            const index = this.allData.findIndex(item => item.id === this.productForm.id)
            if (index > -1) {
              this.allData[index] = { ...this.productForm }
              this.$message.success('更新成功')
            }
          } else {
            const newId = Math.max(...this.allData.map(item => item.id)) + 1
            const newProduct = {
              ...this.productForm,
              id: newId,
              createTime: new Date().toLocaleString()
            }
            this.allData.unshift(newProduct)
            this.$message.success('新增成功')
          }
          this.dialogVisible = false
          this.loadData()
        }
      })
    }
  }
}
</script>
