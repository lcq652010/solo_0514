<template>
  <div class="page-container">
    <el-card>
      <div slot="header" class="clearfix">
        <span>车辆管理</span>
        <el-button style="float: right; padding: 3px 0" type="primary" size="small" @click="handleAdd">
          <i class="el-icon-plus"></i> 新增车辆
        </el-button>
      </div>

      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="车牌号">
          <el-input v-model="searchForm.plateNumber" placeholder="请输入车牌号" clearable></el-input>
        </el-form-item>
        <el-form-item label="车辆状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
            <el-option label="空闲" value="空闲"></el-option>
            <el-option label="在途" value="在途"></el-option>
            <el-option label="维修中" value="维修中"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="filteredVehicles" border style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
        <el-table-column prop="plateNumber" label="车牌号" width="120" align="center"></el-table-column>
        <el-table-column prop="type" label="车型" align="center"></el-table-column>
        <el-table-column prop="capacity" label="载重" width="100" align="center"></el-table-column>
        <el-table-column prop="driver" label="司机" width="100" align="center"></el-table-column>
        <el-table-column prop="phone" label="联系电话" width="130" align="center"></el-table-column>
        <el-table-column prop="currentLocation" label="当前位置" align="center"></el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="small">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button type="primary" size="mini" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="danger" size="mini" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="pagination.currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pagination.pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="pagination.total"
        style="margin-top: 20px; justify-content: flex-end;">
      </el-pagination>
    </el-card>

    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="600px">
      <el-form :model="vehicleForm" :rules="rules" ref="vehicleForm" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="车牌号" prop="plateNumber">
              <el-input v-model="vehicleForm.plateNumber" placeholder="请输入车牌号"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="车型" prop="type">
              <el-select v-model="vehicleForm.type" placeholder="请选择车型" style="width: 100%">
                <el-option label="4.2米厢式货车" value="4.2米厢式货车"></el-option>
                <el-option label="6.8米厢式货车" value="6.8米厢式货车"></el-option>
                <el-option label="9.6米厢式货车" value="9.6米厢式货车"></el-option>
                <el-option label="13米半挂车" value="13米半挂车"></el-option>
                <el-option label="4.2米冷藏车" value="4.2米冷藏车"></el-option>
                <el-option label="6.8米平板车" value="6.8米平板车"></el-option>
                <el-option label="9.6米平板车" value="9.6米平板车"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="载重" prop="capacity">
              <el-input v-model="vehicleForm.capacity" placeholder="例如：5吨"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="司机姓名" prop="driver">
              <el-input v-model="vehicleForm.driver" placeholder="请输入司机姓名"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="vehicleForm.phone" placeholder="请输入联系电话"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="车辆状态" prop="status">
              <el-select v-model="vehicleForm.status" placeholder="请选择状态" style="width: 100%">
                <el-option label="空闲" value="空闲"></el-option>
                <el-option label="在途" value="在途"></el-option>
                <el-option label="维修中" value="维修中"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="当前位置" prop="currentLocation">
              <el-input v-model="vehicleForm.currentLocation" placeholder="请输入当前位置"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitVehicleForm">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { vehicleApi } from '../api/mockData'

export default {
  name: 'VehicleList',
  data() {
    const validateCapacity = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入载重'))
      } else {
        const numValue = parseFloat(value)
        if (isNaN(numValue)) {
          callback(new Error('载重必须是数字'))
        } else if (numValue <= 0) {
          callback(new Error('载重必须大于0'))
        } else if (numValue > 100) {
          callback(new Error('载重不能超过100吨'))
        } else {
          callback()
        }
      }
    }
    return {
      loading: false,
      vehicles: [],
      searchForm: {
        plateNumber: '',
        status: ''
      },
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      dialogVisible: false,
      dialogTitle: '新增车辆',
      isEdit: false,
      vehicleForm: {
        id: null,
        plateNumber: '',
        type: '',
        capacity: '',
        driver: '',
        phone: '',
        status: '空闲',
        currentLocation: ''
      },
      rules: {
        plateNumber: [
          { required: true, message: '请输入车牌号', trigger: 'blur' }
        ],
        type: [
          { required: true, message: '请选择车型', trigger: 'change' }
        ],
        capacity: [
          { required: true, validator: validateCapacity, trigger: 'blur' }
        ],
        driver: [
          { required: true, message: '请输入司机姓名', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
        ],
        status: [
          { required: true, message: '请选择车辆状态', trigger: 'change' }
        ]
      }
    }
  },
  computed: {
    filteredVehicles() {
      let list = [...this.vehicles]
      if (this.searchForm.plateNumber) {
        list = list.filter(v => v.plateNumber.includes(this.searchForm.plateNumber))
      }
      if (this.searchForm.status) {
        list = list.filter(v => v.status === this.searchForm.status)
      }
      this.pagination.total = list.length
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      return list.slice(start, end)
    }
  },
  mounted() {
    this.loadVehicles()
  },
  methods: {
    async loadVehicles() {
      this.loading = true
      try {
        this.vehicles = await vehicleApi.getList()
      } catch (error) {
        this.$message.error('加载车辆数据失败')
      } finally {
        this.loading = false
      }
    },
    getStatusType(status) {
      const typeMap = {
        '空闲': 'success',
        '在途': 'primary',
        '维修中': 'warning'
      }
      return typeMap[status] || 'info'
    },
    handleSearch() {
      this.pagination.currentPage = 1
    },
    handleReset() {
      this.searchForm = {
        plateNumber: '',
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
      this.dialogTitle = '新增车辆'
      this.isEdit = false
      this.vehicleForm = {
        id: null,
        plateNumber: '',
        type: '',
        capacity: '',
        driver: '',
        phone: '',
        status: '空闲',
        currentLocation: ''
      }
      this.dialogVisible = true
      this.$nextTick(() => {
        this.$refs.vehicleForm.clearValidate()
      })
    },
    handleEdit(row) {
      this.dialogTitle = '编辑车辆'
      this.isEdit = true
      this.vehicleForm = { ...row }
      this.dialogVisible = true
      this.$nextTick(() => {
        this.$refs.vehicleForm.clearValidate()
      })
    },
    async submitVehicleForm() {
      this.$refs.vehicleForm.validate(async (valid) => {
        if (valid) {
          try {
            if (this.isEdit) {
              await vehicleApi.update(this.vehicleForm.id, this.vehicleForm)
              this.$message.success('更新成功')
            } else {
              await vehicleApi.add(this.vehicleForm)
              this.$message.success('添加成功')
            }
            this.dialogVisible = false
            this.loadVehicles()
          } catch (error) {
            this.$message.error('操作失败')
          }
        }
      })
    },
    handleDelete(row) {
      this.$confirm('确认删除该车辆信息?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await vehicleApi.delete(row.id)
          this.$message.success('删除成功')
          this.loadVehicles()
        } catch (error) {
          this.$message.error('删除失败')
        }
      }).catch(() => {})
    }
  }
}
</script>

<style scoped>
.search-form {
  margin-bottom: 20px;
}
</style>
