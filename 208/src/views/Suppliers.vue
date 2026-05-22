<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">供应商管理</h2>
      <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新增供应商</el-button>
    </div>

    <div class="search-bar">
      <el-form :inline="true" :model="searchForm" size="small">
        <el-form-item label="供应商名称">
          <el-input v-model="searchForm.name" placeholder="请输入供应商名称" clearable style="width: 200px"></el-input>
        </el-form-item>
        <el-form-item label="联系人">
          <el-input v-model="searchForm.contact" placeholder="请输入联系人" clearable style="width: 150px"></el-input>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable style="width: 120px">
            <el-option label="启用" :value="1"></el-option>
            <el-option label="禁用" :value="0"></el-option>
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
        <el-table-column prop="name" label="供应商名称" min-width="180"></el-table-column>
        <el-table-column prop="type" label="主营品类" width="100" align="center"></el-table-column>
        <el-table-column prop="contact" label="联系人" width="100" align="center"></el-table-column>
        <el-table-column prop="phone" label="联系电话" width="140" align="center"></el-table-column>
        <el-table-column prop="address" label="地址" min-width="200"></el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === 1 ? 'success' : 'danger'" size="small">
              {{ scope.row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" min-width="160" align="center">
          <template slot-scope="scope">
            {{ scope.row.createTime | formatDate }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" icon="el-icon-edit" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button 
              size="mini" 
              :type="scope.row.status === 1 ? 'warning' : 'success'" 
              :icon="scope.row.status === 1 ? 'el-icon-close' : 'el-icon-check'"
              @click="handleToggleStatus(scope.row)">
              {{ scope.row.status === 1 ? '禁用' : '启用' }}
            </el-button>
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
      width="550px"
      :close-on-click-modal="false">
      <el-form :model="supplierForm" :rules="rules" ref="supplierForm" label-width="100px">
        <el-form-item label="供应商名称" prop="name">
          <el-input v-model="supplierForm.name" placeholder="请输入供应商名称"></el-input>
        </el-form-item>
        <el-form-item label="主营品类" prop="type">
          <el-select v-model="supplierForm.type" placeholder="请选择主营品类" style="width: 100%">
            <el-option
              v-for="item in productCategories"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="联系人" prop="contact">
          <el-input v-model="supplierForm.contact" placeholder="请输入联系人姓名"></el-input>
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="supplierForm.phone" placeholder="请输入联系电话"></el-input>
        </el-form-item>
        <el-form-item label="地址" prop="address">
          <el-input v-model="supplierForm.address" type="textarea" :rows="2" placeholder="请输入详细地址"></el-input>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="supplierForm.status">
            <el-radio :label="1">启用</el-radio>
            <el-radio :label="0">禁用</el-radio>
          </el-radio-group>
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
import { suppliers, productCategories } from '../mock/data.js'

export default {
  name: 'Suppliers',
  data() {
    return {
      productCategories,
      allData: [...suppliers],
      tableData: [],
      searchForm: {
        name: '',
        contact: '',
        status: ''
      },
      pagination: {
        page: 1,
        size: 10,
        total: 0
      },
      dialogVisible: false,
      dialogTitle: '新增供应商',
      isEdit: false,
      supplierForm: {
        id: null,
        name: '',
        type: '',
        contact: '',
        phone: '',
        address: '',
        status: 1
      },
      rules: {
        name: [{ required: true, message: '请输入供应商名称', trigger: 'blur' }],
        type: [{ required: true, message: '请选择主营品类', trigger: 'change' }],
        contact: [{ required: true, message: '请输入联系人', trigger: 'blur' }],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3456789]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ],
        address: [{ required: true, message: '请输入地址', trigger: 'blur' }]
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
      if (this.searchForm.contact) {
        data = data.filter(item => item.contact.includes(this.searchForm.contact))
      }
      if (this.searchForm.status !== '') {
        data = data.filter(item => item.status === this.searchForm.status)
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
      this.searchForm = { name: '', contact: '', status: '' }
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
      this.dialogTitle = '新增供应商'
      this.supplierForm = {
        id: null,
        name: '',
        type: '',
        contact: '',
        phone: '',
        address: '',
        status: 1
      }
      this.dialogVisible = true
      this.$nextTick(() => {
        this.$refs.supplierForm && this.$refs.supplierForm.clearValidate()
      })
    },
    handleEdit(row) {
      this.isEdit = true
      this.dialogTitle = '编辑供应商'
      this.supplierForm = { ...row }
      this.dialogVisible = true
    },
    handleToggleStatus(row) {
      const newStatus = row.status === 1 ? 0 : 1
      this.$confirm(`确定要${newStatus === 1 ? '启用' : '禁用'}"${row.name}"吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.allData.findIndex(item => item.id === row.id)
        if (index > -1) {
          this.allData[index].status = newStatus
          this.loadData()
          this.$message.success(`${newStatus === 1 ? '启用' : '禁用'}成功`)
        }
      }).catch(() => {})
    },
    handleSubmit() {
      this.$refs.supplierForm.validate((valid) => {
        if (valid) {
          if (this.isEdit) {
            const index = this.allData.findIndex(item => item.id === this.supplierForm.id)
            if (index > -1) {
              this.allData[index] = { ...this.supplierForm }
              this.$message.success('更新成功')
            }
          } else {
            const newId = Math.max(...this.allData.map(item => item.id)) + 1
            const newSupplier = {
              ...this.supplierForm,
              id: newId,
              createTime: new Date().toLocaleString()
            }
            this.allData.unshift(newSupplier)
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
