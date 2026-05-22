<template>
  <div class="app-container">
    <div class="page-container">
      <div class="page-header">
        <h1 class="page-title">政务服务自助证照打印终端运维管理系统</h1>
        <el-button type="primary" @click="openReportDialog">
          <i class="el-icon-warning"></i> 故障上报
        </el-button>
      </div>

      <div class="search-bar">
        <el-form :inline="true" :model="searchForm" class="demo-form-inline">
          <el-form-item label="智能搜索">
            <el-input 
              v-model="searchForm.keyword" 
              placeholder="支持设备编号、大厅名称、位置搜索" 
              clearable
              style="width: 300px">
              <i slot="prefix" class="el-input__icon el-icon-search"></i>
            </el-input>
          </el-form-item>
          <el-form-item label="运行状态">
            <el-select v-model="searchForm.status" placeholder="全部状态" clearable style="width: 140px">
              <el-option label="全部状态" value=""></el-option>
              <el-option label="运行正常" value="normal"></el-option>
              <el-option label="运行警告" value="warning"></el-option>
              <el-option label="故障停机" value="error"></el-option>
              <el-option label="离线" value="offline"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="设备编号">
            <el-input v-model="searchForm.deviceCode" placeholder="设备编号" clearable style="width: 150px"></el-input>
          </el-form-item>
          <el-form-item label="大厅名称">
            <el-input v-model="searchForm.hallName" placeholder="大厅名称" clearable style="width: 150px"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
            <el-button icon="el-icon-refresh" @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <el-table :data="tableData" border stripe style="width: 100%" :row-class-name="getTableRowClassName">
        <el-table-column prop="deviceCode" label="设备编号" width="150" align="center"></el-table-column>
        <el-table-column prop="hallName" label="政务大厅" width="180" align="center"></el-table-column>
        <el-table-column prop="location" label="摆放位置" width="150" align="center"></el-table-column>
        <el-table-column label="身份核验" width="120" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusTagType(scope.row.identityVerify)" size="small">
              {{ getStatusText(scope.row.identityVerify) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="证照打印" width="120" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusTagType(scope.row.licensePrint)" size="small">
              {{ getStatusText(scope.row.licensePrint) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="数据加密" width="120" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusTagType(scope.row.dataEncrypt)" size="small">
              {{ getStatusText(scope.row.dataEncrypt) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="设备运行状态" width="130" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusTagType(scope.row.status)" size="medium">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="130" align="center">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="handleReport(scope.row)">故障上报</el-button>
            <el-dropdown @command="(cmd) => handleStatusChange(cmd, scope.row)" trigger="click">
              <span class="el-dropdown-link" style="color: #409EFF; cursor: pointer; font-size: 12px;">
                状态变更<i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="normal">运行正常</el-dropdown-item>
                <el-dropdown-item command="warning">运行警告</el-dropdown-item>
                <el-dropdown-item command="error">故障停机</el-dropdown-item>
                <el-dropdown-item command="offline">离线</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pagination.pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total">
        </el-pagination>
      </div>
    </div>

    <el-dialog title="故障上报" :visible.sync="dialogVisible" width="650px" :close-on-click-modal="false">
      <el-form :model="reportForm" :rules="reportRules" ref="reportForm" label-width="100px">
        <el-form-item label="工单编号">
          <el-input v-model="reportForm.orderNo" disabled>
            <template slot="append">
              <i class="el-icon-document" style="color: #409EFF"></i>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="选择设备" prop="deviceId">
          <el-select 
            v-model="reportForm.deviceId" 
            placeholder="请搜索选择设备" 
            style="width: 100%"
            filterable
            :filter-method="filterDevice"
            clearable>
            <el-option
              v-for="item in filteredDeviceList"
              :key="item.id"
              :label="`${item.deviceCode} - ${item.hallName} - ${item.location}`"
              :value="item.id">
              <span style="float: left">{{ item.deviceCode }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">
                <el-tag :type="getStatusTagType(item.status)" size="mini" style="margin-right: 5px">
                  {{ getStatusText(item.status) }}
                </el-tag>
                {{ item.hallName }}
              </span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="联系人" prop="contactPerson">
          <el-input v-model="reportForm.contactPerson" placeholder="请填写联系人姓名"></el-input>
        </el-form-item>
        <el-form-item label="联系电话" prop="contactPhone">
          <el-input v-model="reportForm.contactPhone" placeholder="请填写联系电话"></el-input>
        </el-form-item>
        <el-form-item label="故障描述" prop="faultDescription">
          <el-input
            type="textarea"
            v-model="reportForm.faultDescription"
            :rows="5"
            placeholder="请详细描述故障情况，以便运维人员快速定位问题">
          </el-input>
        </el-form-item>
        <el-form-item label="故障类型" prop="faultType">
          <el-select v-model="reportForm.faultType" placeholder="请选择故障类型" style="width: 100%">
            <el-option label="硬件故障" value="hardware"></el-option>
            <el-option label="软件故障" value="software"></el-option>
            <el-option label="网络故障" value="network"></el-option>
            <el-option label="纸张/耗材问题" value="supply"></el-option>
            <el-option label="其他问题" value="other"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="上报时间">
          <el-input v-model="reportForm.reportTime" disabled>
            <template slot="append">
              <i class="el-icon-time" style="color: #67C23A"></i>
            </template>
          </el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitReport" :loading="submitLoading">提交上报</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      searchForm: {
        keyword: '',
        deviceCode: '',
        hallName: '',
        statusFilter: ''
      },
      allDeviceData: [],
      filteredData: [],
      tableData: [],
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      dialogVisible: false,
      submitLoading: false,
      reportForm: {
        orderNo: '',
        deviceId: '',
        contactPerson: '',
        contactPhone: '',
        faultDescription: '',
        faultType: '',
        reportTime: ''
      },
      reportRules: {
        deviceId: [
          { required: true, message: '请选择故障设备', trigger: 'change' }
        ],
        contactPerson: [
          { required: true, message: '请填写联系人姓名', trigger: 'blur' }
        ],
        contactPhone: [
          { required: true, message: '请填写联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请填写正确的手机号码', trigger: 'blur' }
        ],
        faultDescription: [
          { required: true, message: '请详细描述故障情况', trigger: 'blur' },
          { min: 10, message: '故障描述至少10个字符，以便运维人员快速定位', trigger: 'blur' }
        ],
        faultType: [
          { required: true, message: '请选择故障类型', trigger: 'change' }
        ]
      },
      deviceList: [],
      filteredDeviceList: [],
      orderSequence: 1,
      searchTimer: null
    }
  },
  created() {
    this.initData()
  },
  methods: {
    initData() {
      this.allDeviceData = [
        { id: 1, deviceCode: 'ZZ-2024-001', hallName: '北京市政务服务中心', location: '一楼大厅东侧', status: 'normal', identityVerify: 'normal', licensePrint: 'normal', dataEncrypt: 'normal' },
        { id: 2, deviceCode: 'ZZ-2024-002', hallName: '北京市政务服务中心', location: '一楼大厅西侧', status: 'warning', identityVerify: 'normal', licensePrint: 'warning', dataEncrypt: 'normal' },
        { id: 3, deviceCode: 'ZZ-2024-003', hallName: '朝阳区政务服务中心', location: '二楼办事大厅', status: 'normal', identityVerify: 'normal', licensePrint: 'normal', dataEncrypt: 'normal' },
        { id: 4, deviceCode: 'ZZ-2024-004', hallName: '海淀区政务服务中心', location: '一楼入口处', status: 'error', identityVerify: 'error', licensePrint: 'error', dataEncrypt: 'warning' },
        { id: 5, deviceCode: 'ZZ-2024-005', hallName: '海淀区政务服务中心', location: '三楼301室旁', status: 'normal', identityVerify: 'normal', licensePrint: 'normal', dataEncrypt: 'normal' },
        { id: 6, deviceCode: 'ZZ-2024-006', hallName: '丰台区政务服务中心', location: '大厅服务台旁', status: 'offline', identityVerify: 'offline', licensePrint: 'offline', dataEncrypt: 'offline' },
        { id: 7, deviceCode: 'ZZ-2024-007', hallName: '东城区政务服务中心', location: '一楼自助服务区', status: 'normal', identityVerify: 'normal', licensePrint: 'normal', dataEncrypt: 'normal' },
        { id: 8, deviceCode: 'ZZ-2024-008', hallName: '西城区政务服务中心', location: '二楼自助服务区', status: 'warning', identityVerify: 'warning', licensePrint: 'normal', dataEncrypt: 'normal' },
        { id: 9, deviceCode: 'ZZ-2024-009', hallName: '通州区政务服务中心', location: '一楼大厅', status: 'normal', identityVerify: 'normal', licensePrint: 'normal', dataEncrypt: 'normal' },
        { id: 10, deviceCode: 'ZZ-2024-010', hallName: '顺义区政务服务中心', location: '办事大厅A区', status: 'normal', identityVerify: 'normal', licensePrint: 'normal', dataEncrypt: 'normal' },
        { id: 11, deviceCode: 'ZZ-2024-011', hallName: '大兴区政务服务中心', location: '一楼东侧', status: 'error', identityVerify: 'normal', licensePrint: 'error', dataEncrypt: 'error' },
        { id: 12, deviceCode: 'ZZ-2024-012', hallName: '昌平区政务服务中心', location: '二楼大厅', status: 'normal', identityVerify: 'normal', licensePrint: 'normal', dataEncrypt: 'normal' },
        { id: 13, deviceCode: 'ZZ-2024-013', hallName: '房山区政务服务中心', location: '一楼服务台', status: 'offline', identityVerify: 'offline', licensePrint: 'offline', dataEncrypt: 'offline' },
        { id: 14, deviceCode: 'ZZ-2024-014', hallName: '石景山区政务服务中心', location: '自助服务区', status: 'normal', identityVerify: 'normal', licensePrint: 'normal', dataEncrypt: 'normal' },
        { id: 15, deviceCode: 'ZZ-2024-015', hallName: '门头沟区政务服务中心', location: '一楼大厅', status: 'warning', identityVerify: 'normal', licensePrint: 'warning', dataEncrypt: 'warning' },
        { id: 16, deviceCode: 'ZZ-2024-016', hallName: '怀柔区政务服务中心', location: '大厅西区', status: 'error', identityVerify: 'error', licensePrint: 'error', dataEncrypt: 'normal' },
        { id: 17, deviceCode: 'ZZ-2024-017', hallName: '平谷区政务服务中心', location: '二楼东区', status: 'normal', identityVerify: 'normal', licensePrint: 'normal', dataEncrypt: 'normal' },
        { id: 18, deviceCode: 'ZZ-2024-018', hallName: '密云区政务服务中心', location: '一楼入口', status: 'offline', identityVerify: 'offline', licensePrint: 'offline', dataEncrypt: 'offline' },
        { id: 19, deviceCode: 'ZZ-2024-019', hallName: '延庆区政务服务中心', location: '办事大厅', status: 'warning', identityVerify: 'normal', licensePrint: 'warning', dataEncrypt: 'normal' },
        { id: 20, deviceCode: 'ZZ-2024-020', hallName: '经开区政务服务中心', location: '自助服务区A', status: 'normal', identityVerify: 'normal', licensePrint: 'normal', dataEncrypt: 'normal' },
        { id: 21, deviceCode: 'ZZ-2024-021', hallName: '东城区政务服务中心', location: '二楼大厅', status: 'normal', identityVerify: 'normal', licensePrint: 'normal', dataEncrypt: 'warning' },
        { id: 22, deviceCode: 'ZZ-2024-022', hallName: '西城区政务服务中心', location: '一楼自助区', status: 'error', identityVerify: 'error', licensePrint: 'error', dataEncrypt: 'error' },
        { id: 23, deviceCode: 'ZZ-2024-023', hallName: '朝阳区政务服务中心', location: '三楼西区', status: 'normal', identityVerify: 'normal', licensePrint: 'normal', dataEncrypt: 'normal' },
        { id: 24, deviceCode: 'ZZ-2024-024', hallName: '海淀区政务服务中心', location: '四楼东区', status: 'warning', identityVerify: 'normal', licensePrint: 'normal', dataEncrypt: 'warning' },
        { id: 25, deviceCode: 'ZZ-2024-025', hallName: '丰台区政务服务中心', location: '二楼自助区', status: 'offline', identityVerify: 'offline', licensePrint: 'offline', dataEncrypt: 'offline' }
      ]
      this.deviceList = [...this.allDeviceData]
      this.filteredDeviceList = [...this.allDeviceData]
      this.handleSearch()
    },
    getStatusTagType(status) {
      const typeMap = {
        'normal': 'success',
        'warning': 'warning',
        'error': 'danger',
        'offline': 'info'
      }
      return typeMap[status] || 'info'
    },
    getStatusText(status) {
      const textMap = {
        'normal': '运行正常',
        'warning': '运行警告',
        'error': '故障停机',
        'offline': '离线'
      }
      return textMap[status] || '未知'
    },
    getTableRowClassName({ row }) {
      if (row.status === 'error') {
        return 'error-row'
      } else if (row.status === 'offline') {
        return 'offline-row'
      } else if (row.status === 'warning') {
        return 'warning-row'
      }
      return ''
    },
    handleSearch() {
      clearTimeout(this.searchTimer)
      this.searchTimer = setTimeout(() => {
        let result = [...this.allDeviceData]
        const keyword = this.searchForm.keyword?.toLowerCase().trim()
        
        if (keyword) {
          result = result.filter(item => {
            const searchFields = [
              item.deviceCode.toLowerCase(),
              item.hallName.toLowerCase(),
              item.location.toLowerCase(),
              this.getStatusText(item.status).toLowerCase()
            ]
            return searchFields.some(field => field.includes(keyword))
          })
        }
        
        if (this.searchForm.deviceCode) {
          result = result.filter(item => 
            item.deviceCode.toLowerCase().includes(this.searchForm.deviceCode.toLowerCase())
          )
        }
        
        if (this.searchForm.hallName) {
          result = result.filter(item => 
            item.hallName.includes(this.searchForm.hallName)
          )
        }
        
        if (this.searchForm.statusFilter) {
          result = result.filter(item => item.status === this.searchForm.statusFilter)
        }
        
        this.filteredData = result
        this.pagination.total = result.length
        this.updateTableData()
      }, 300)
    },
    resetSearch() {
      this.searchForm = {
        keyword: '',
        deviceCode: '',
        hallName: '',
        statusFilter: ''
      }
      this.pagination.currentPage = 1
      this.handleSearch()
    },
    handleStatusChange(newStatus, row) {
      const deviceIndex = this.allDeviceData.findIndex(item => item.id === row.id)
      if (deviceIndex !== -1) {
        this.$set(this.allDeviceData, deviceIndex, {
          ...this.allDeviceData[deviceIndex],
          status: newStatus,
          identityVerify: newStatus,
          licensePrint: newStatus,
          dataEncrypt: newStatus
        })
        this.$message.success(`设备 ${row.deviceCode} 状态已变更为：${this.getStatusText(newStatus)}`)
        this.handleSearch()
      }
    },
    updateTableData() {
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      this.tableData = this.filteredData.slice(start, end)
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.pagination.currentPage = 1
      this.updateTableData()
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
      this.updateTableData()
    },
    generateOrderNo() {
      const now = new Date()
      const year = now.getFullYear()
      const month = String(now.getMonth() + 1).padStart(2, '0')
      const day = String(now.getDate()).padStart(2, '0')
      const hours = String(now.getHours()).padStart(2, '0')
      const minutes = String(now.getMinutes()).padStart(2, '0')
      const seconds = String(now.getSeconds()).padStart(2, '0')
      const sequence = String(this.orderSequence).padStart(4, '0')
      this.orderSequence++
      return `GZ${year}${month}${day}${hours}${minutes}${seconds}${sequence}`
    },
    filterDevice(query) {
      if (query) {
        const searchQuery = query.toLowerCase()
        this.filteredDeviceList = this.deviceList.filter(item => 
          item.deviceCode.toLowerCase().includes(searchQuery) ||
          item.hallName.toLowerCase().includes(searchQuery) ||
          item.location.toLowerCase().includes(searchQuery)
        )
      } else {
        this.filteredDeviceList = [...this.deviceList]
      }
    },
    openReportDialog() {
      this.filteredDeviceList = [...this.deviceList]
      this.reportForm = {
        orderNo: this.generateOrderNo(),
        deviceId: '',
        contactPerson: '',
        contactPhone: '',
        faultDescription: '',
        faultType: '',
        reportTime: this.formatDateTime(new Date())
      }
      this.dialogVisible = true
      this.$nextTick(() => {
        if (this.$refs.reportForm) {
          this.$refs.reportForm.clearValidate()
        }
      })
    },
    handleReport(row) {
      this.filteredDeviceList = [...this.deviceList]
      this.reportForm = {
        orderNo: this.generateOrderNo(),
        deviceId: row.id,
        contactPerson: '',
        contactPhone: '',
        faultDescription: '',
        faultType: '',
        reportTime: this.formatDateTime(new Date())
      }
      this.dialogVisible = true
      this.$nextTick(() => {
        if (this.$refs.reportForm) {
          this.$refs.reportForm.clearValidate()
        }
      })
    },
    formatDateTime(date) {
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      const hours = String(date.getHours()).padStart(2, '0')
      const minutes = String(date.getMinutes()).padStart(2, '0')
      const seconds = String(date.getSeconds()).padStart(2, '0')
      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
    },
    submitReport() {
      if (!this.reportForm.deviceId) {
        this.$message.warning('请先选择要上报故障的设备！')
        return
      }
      this.$refs.reportForm.validate((valid) => {
        if (valid) {
          this.submitLoading = true
          setTimeout(() => {
            this.submitLoading = false
            this.$message({
              type: 'success',
              message: '故障上报成功！工单号：' + this.reportForm.orderNo,
              duration: 3000
            })
            this.dialogVisible = false
          }, 1000)
        }
      })
    }
  },
  watch: {
    'searchForm.keyword': function() {
      this.pagination.currentPage = 1
      this.handleSearch()
    },
    'searchForm.statusFilter': function() {
      this.pagination.currentPage = 1
      this.handleSearch()
    }
  }
}
</script>

<style scoped>
.app-container {
  padding: 20px;
  min-height: 100vh;
  background-color: #f0f2f5;
}
</style>

<style>
.el-table .error-row {
  background-color: #fef0f0 !important;
  animation: errorPulse 2s ease-in-out infinite;
}

.el-table .error-row:hover > td {
  background-color: #fde2e2 !important;
}

.el-table .offline-row {
  background-color: #f4f4f5 !important;
}

.el-table .offline-row:hover > td {
  background-color: #e4e4e7 !important;
}

.el-table .warning-row {
  background-color: #fdf6ec !important;
}

.el-table .warning-row:hover > td {
  background-color: #faecd8 !important;
}

@keyframes errorPulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.8;
  }
}

.el-tag--success {
  background-color: #f0f9eb !important;
  border-color: #e1f3d8 !important;
  color: #67c23a !important;
}

.el-tag--warning {
  background-color: #fdf6ec !important;
  border-color: #faecd8 !important;
  color: #e6a23c !important;
}

.el-tag--danger {
  background-color: #fef0f0 !important;
  border-color: #fde2e2 !important;
  color: #f56c6c !important;
}

.el-tag--info {
  background-color: #f4f4f5 !important;
  border-color: #e9e9eb !important;
  color: #909399 !important;
}

.search-bar {
  background: #fff;
  padding: 15px 20px;
  border-radius: 4px;
  margin-bottom: 15px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.page-container {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style>
