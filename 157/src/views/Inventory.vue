<template>
  <div class="page-container">
    <div class="page-header">
      <span class="page-title">库存管理</span>
    </div>
    
    <div class="search-bar">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="用品名称">
          <el-input v-model="searchForm.name" placeholder="请输入用品名称" clearable></el-input>
        </el-form-item>
        <el-form-item label="用品分类">
          <el-select v-model="searchForm.categoryId" placeholder="请选择分类" clearable>
            <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="库存状态">
          <el-select v-model="searchForm.stockStatus" placeholder="请选择" clearable>
            <el-option label="库存充足" value="sufficient"></el-option>
            <el-option label="库存偏低" value="low"></el-option>
            <el-option label="库存不足" value="insufficient"></el-option>
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
            <i class="el-icon-plus"></i> 新增用品
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="table-container">
      <el-table :data="tableData" border stripe>
        <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
        <el-table-column prop="name" label="用品名称" min-width="150"></el-table-column>
        <el-table-column prop="categoryName" label="分类" width="120" align="center"></el-table-column>
        <el-table-column prop="spec" label="规格" width="120" align="center"></el-table-column>
        <el-table-column prop="unit" label="单位" width="80" align="center"></el-table-column>
        <el-table-column prop="stock" label="当前库存" width="100" align="center">
          <template slot-scope="scope">
            <span :style="{ color: getStockColor(scope.row.stock, scope.row.minStock) }">
              {{ scope.row.stock }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="minStock" label="最低库存" width="100" align="center"></el-table-column>
        <el-table-column prop="price" label="单价(元)" width="100" align="center"></el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === 1 ? 'success' : 'danger'" size="small">
              {{ scope.row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="handleEdit(scope.row)">
              <i class="el-icon-edit"></i> 编辑
            </el-button>
            <el-button size="mini" type="success" @click="handleStockIn(scope.row)">
              <i class="el-icon-download"></i> 入库
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

    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="600px">
      <el-form :model="form" :rules="rules" ref="form" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="用品名称" prop="name">
              <el-input v-model="form.name" placeholder="请输入用品名称"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="分类" prop="categoryId">
              <el-select v-model="form.categoryId" placeholder="请选择分类" style="width: 100%">
                <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="规格" prop="spec">
              <el-input v-model="form.spec" placeholder="请输入规格"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="单位" prop="unit">
              <el-input v-model="form.unit" placeholder="请输入单位"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="当前库存" prop="stock">
              <el-input-number v-model="form.stock" :min="0" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="最低库存" prop="minStock">
              <el-input-number v-model="form.minStock" :min="0" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="单价" prop="price">
              <el-input-number v-model="form.price" :min="0" :precision="2" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
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
import { supplies, categories } from '@/api/mockData'
import { EventBus } from '@/utils/eventBus'

export default {
  name: 'Inventory',
  data() {
    return {
      categories: categories,
      searchForm: {
        name: '',
        categoryId: null,
        stockStatus: ''
      },
      tableData: [],
      total: 0,
      pageSize: 10,
      currentPage: 1,
      dialogVisible: false,
      dialogTitle: '新增用品',
      isEdit: false,
      form: {
        id: null,
        name: '',
        categoryId: '',
        spec: '',
        unit: '',
        stock: 0,
        minStock: 10,
        price: 0,
        status: 1
      },
      rules: {
        name: [
          { required: true, message: '请输入用品名称', trigger: 'blur' },
          { min: 2, max: 30, message: '长度在 2 到 30 个字符', trigger: 'blur' }
        ],
        categoryId: [
          { required: true, message: '请选择分类', trigger: 'change' }
        ],
        unit: [
          { required: true, message: '请输入单位', trigger: 'blur' }
        ]
      },
      dataList: []
    }
  },
  created() {
    this.dataList = [...supplies]
    this.loadData()
  },
  mounted() {
    EventBus.$on('stock-updated', () => {
      this.dataList = [...supplies]
      this.loadData()
    })
  },
  beforeDestroy() {
    EventBus.$off('stock-updated')
  },
  methods: {
    getStockColor(stock, minStock) {
      if (stock < minStock * 0.5) return '#f56c6c'
      if (stock < minStock) return '#e6a23c'
      return '#67c23a'
    },
    loadData() {
      let filtered = [...this.dataList]
      
      if (this.searchForm.name) {
        filtered = filtered.filter(item => item.name.includes(this.searchForm.name))
      }
      
      if (this.searchForm.categoryId) {
        filtered = filtered.filter(item => item.categoryId === this.searchForm.categoryId)
      }
      
      if (this.searchForm.stockStatus) {
        filtered = filtered.filter(item => {
          if (this.searchForm.stockStatus === 'sufficient') {
            return item.stock >= item.minStock
          } else if (this.searchForm.stockStatus === 'low') {
            return item.stock < item.minStock && item.stock >= item.minStock * 0.5
          } else {
            return item.stock < item.minStock * 0.5
          }
        })
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
        categoryId: null,
        stockStatus: ''
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
      this.dialogTitle = '新增用品'
      this.form = {
        id: null,
        name: '',
        categoryId: '',
        spec: '',
        unit: '',
        stock: 0,
        minStock: 10,
        price: 0,
        status: 1
      }
      this.dialogVisible = true
      this.$nextTick(() => {
        this.$refs.form.clearValidate()
      })
    },
    handleEdit(row) {
      this.isEdit = true
      this.dialogTitle = '编辑用品'
      this.form = { ...row }
      this.dialogVisible = true
    },
    handleSubmit() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          const category = this.categories.find(c => c.id === this.form.categoryId)
          if (category) {
            this.form.categoryName = category.name
          }
          
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
              id: newId
            }
            this.dataList.push(newItem)
            this.$message.success('新增成功')
          }
          this.dialogVisible = false
          this.loadData()
        }
      })
    },
    handleStockIn(row) {
      this.$router.push({ path: '/stock-in', query: { supplyId: row.id } })
    },
    handleDelete(row) {
      this.$confirm('确定要删除该用品吗？', '提示', {
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
