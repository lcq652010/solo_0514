<template>
  <div class="page-container">
    <div class="page-title">预约记录列表</div>
    
    <el-card class="box-card">
      <el-form :inline="true" :model="searchForm" class="demo-form-inline">
        <el-form-item label="预约编号">
          <el-input v-model="searchForm.appointmentNo" placeholder="请输入预约编号"></el-input>
        </el-form-item>
        <el-form-item label="宠物名称">
          <el-input v-model="searchForm.petName" placeholder="请输入宠物名称"></el-input>
        </el-form-item>
        <el-form-item label="宠物类型">
          <el-select v-model="searchForm.petType" placeholder="请选择宠物类型" clearable>
            <el-option label="狗" value="狗"></el-option>
            <el-option label="猫" value="猫"></el-option>
            <el-option label="鸟" value="鸟"></el-option>
            <el-option label="其他" value="其他"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="主人姓名">
          <el-input v-model="searchForm.ownerName" placeholder="请输入主人姓名"></el-input>
        </el-form-item>
        <el-form-item label="医师">
          <el-select v-model="searchForm.doctor" placeholder="请选择医师" clearable>
            <el-option label="张医生" value="张医生"></el-option>
            <el-option label="李医生" value="李医生"></el-option>
            <el-option label="王医生" value="王医生"></el-option>
            <el-option label="赵医生" value="赵医生"></el-option>
            <el-option label="刘医生" value="刘医生"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="就诊日期">
          <el-date-picker
            v-model="searchForm.appointmentDate"
            type="date"
            placeholder="选择就诊日期">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="就诊状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
            <el-option label="待就诊" value="待就诊"></el-option>
            <el-option label="已就诊" value="已就诊"></el-option>
            <el-option label="已取消" value="已取消"></el-option>
            <el-option label="已过期" value="已过期"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
      
      <el-table :data="paginatedData" border style="width: 100%" v-loading="loading">
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column prop="appointmentNo" label="预约编号" width="150"></el-table-column>
        <el-table-column prop="petName" label="宠物名称" width="100"></el-table-column>
        <el-table-column prop="petType" label="宠物类型" width="80"></el-table-column>
        <el-table-column prop="breed" label="品种" width="100"></el-table-column>
        <el-table-column prop="ownerName" label="主人姓名" width="100"></el-table-column>
        <el-table-column prop="phone" label="联系电话" width="120"></el-table-column>
        <el-table-column prop="appointmentDate" label="就诊日期" width="120"></el-table-column>
        <el-table-column prop="timeSlot" label="时段" width="120"></el-table-column>
        <el-table-column prop="department" label="科室" width="100"></el-table-column>
        <el-table-column prop="doctor" label="医师" width="100"></el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="handleView(scope.row)">查看</el-button>
            <el-button size="mini" type="success" @click="handleComplete(scope.row)" :disabled="scope.row.status !== '待就诊'">完成</el-button>
            <el-button size="mini" type="danger" @click="handleCancel(scope.row)" :disabled="scope.row.status !== '待就诊'">取消</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-container">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.currentPage"
          :page-sizes="[5, 10, 20, 50]"
          :page-size="pagination.pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total">
        </el-pagination>
      </div>
    </el-card>
    
    <el-dialog title="预约详情" :visible.sync="dialogVisible" width="700px">
      <el-descriptions :column="2" border v-if="currentRecord">
        <el-descriptions-item label="预约编号">{{ currentRecord.appointmentNo }}</el-descriptions-item>
        <el-descriptions-item label="预约状态">
          <el-tag :type="getStatusType(currentRecord.status)">
            {{ currentRecord.status }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="宠物名称">{{ currentRecord.petName }}</el-descriptions-item>
        <el-descriptions-item label="宠物类型">{{ currentRecord.petType }}</el-descriptions-item>
        <el-descriptions-item label="品种">{{ currentRecord.breed }}</el-descriptions-item>
        <el-descriptions-item label="性别">{{ currentRecord.petGender }}</el-descriptions-item>
        <el-descriptions-item label="年龄">{{ currentRecord.age }}岁</el-descriptions-item>
        <el-descriptions-item label="体重">{{ currentRecord.weight }}kg</el-descriptions-item>
        <el-descriptions-item label="主人姓名">{{ currentRecord.ownerName }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ currentRecord.phone }}</el-descriptions-item>
        <el-descriptions-item label="就诊日期">{{ currentRecord.appointmentDate }}</el-descriptions-item>
        <el-descriptions-item label="就诊时段">{{ currentRecord.timeSlot }}</el-descriptions-item>
        <el-descriptions-item label="就诊科室">{{ currentRecord.department }}</el-descriptions-item>
        <el-descriptions-item label="主治医师">{{ currentRecord.doctor }}</el-descriptions-item>
        <el-descriptions-item label="症状描述" :span="2">{{ currentRecord.symptoms }}</el-descriptions-item>
      </el-descriptions>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">关闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import dataStore from '@/store/dataStore.js'

export default {
  name: 'AppointmentList',
  data() {
    return {
      loading: false,
      searchForm: {
        appointmentNo: '',
        petName: '',
        petType: '',
        ownerName: '',
        doctor: '',
        appointmentDate: '',
        status: ''
      },
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      dialogVisible: false,
      currentRecord: null
    }
  },
  computed: {
    filteredData() {
      let data = dataStore.getAppointments()
      
      if (this.searchForm.appointmentNo) {
        data = data.filter(item => 
          item.appointmentNo.toLowerCase().includes(this.searchForm.appointmentNo.toLowerCase())
        )
      }
      
      if (this.searchForm.petName) {
        data = data.filter(item => 
          item.petName.includes(this.searchForm.petName)
        )
      }
      
      if (this.searchForm.petType) {
        data = data.filter(item => 
          item.petType === this.searchForm.petType
        )
      }
      
      if (this.searchForm.ownerName) {
        data = data.filter(item => 
          item.ownerName.includes(this.searchForm.ownerName)
        )
      }
      
      if (this.searchForm.doctor) {
        data = data.filter(item => 
          item.doctor === this.searchForm.doctor
        )
      }
      
      if (this.searchForm.appointmentDate) {
        const formattedDate = this.formatDate(this.searchForm.appointmentDate)
        data = data.filter(item => 
          item.appointmentDate === formattedDate
        )
      }
      
      if (this.searchForm.status) {
        data = data.filter(item => 
          item.status === this.searchForm.status
        )
      }
      
      return data
    },
    paginatedData() {
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      return this.filteredData.slice(start, end)
    }
  },
  mounted() {
    this.refreshData()
    dataStore.subscribe(() => {
      this.refreshData()
    })
  },
  methods: {
    refreshData() {
      this.pagination.total = this.filteredData.length
      if (this.pagination.currentPage > Math.ceil(this.pagination.total / this.pagination.pageSize)) {
        this.pagination.currentPage = 1
      }
    },
    formatDate(date) {
      if (!date) return ''
      if (typeof date === 'string') return date
      const d = new Date(date)
      const year = d.getFullYear()
      const month = String(d.getMonth() + 1).padStart(2, '0')
      const day = String(d.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    },
    getStatusType(status) {
      const typeMap = {
        '待就诊': 'warning',
        '已就诊': 'success',
        '已取消': 'info',
        '已过期': 'danger'
      }
      return typeMap[status] || ''
    },
    handleSearch() {
      this.loading = true
      setTimeout(() => {
        this.loading = false
        this.pagination.currentPage = 1
        this.refreshData()
        this.$message.success('查询完成')
      }, 300)
    },
    handleReset() {
      this.searchForm = {
        appointmentNo: '',
        petName: '',
        petType: '',
        ownerName: '',
        doctor: '',
        appointmentDate: '',
        status: ''
      }
      this.pagination.currentPage = 1
      this.refreshData()
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.pagination.currentPage = 1
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
    },
    handleView(row) {
      this.currentRecord = row
      this.dialogVisible = true
    },
    handleComplete(row) {
      this.$confirm('确认标记该预约为已就诊吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        dataStore.updateAppointmentStatus(row.appointmentNo, '已就诊')
        this.$message.success('操作成功')
      }).catch(() => {})
    },
    handleCancel(row) {
      this.$confirm('确定要取消该预约吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        dataStore.updateAppointmentStatus(row.appointmentNo, '已取消')
        this.$message.success('取消成功')
      }).catch(() => {})
    }
  }
}
</script>

<style scoped>
.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style>
