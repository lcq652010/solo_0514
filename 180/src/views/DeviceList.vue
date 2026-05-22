<template>
  <div class="device-management">
    <div class="header">
      <h1>社保自助终端运维管理系统</h1>
    </div>
    
    <div class="content">
      <div class="search-bar">
        <el-input 
          v-model="searchForm.deviceCode" 
          placeholder="设备编号" 
          style="width: 200px; margin-right: 16px;"
          clearable
          @input="handleSearch"
        ></el-input>
        <el-input 
          v-model="searchForm.branchName" 
          placeholder="网点名称" 
          style="width: 200px; margin-right: 16px;"
          clearable
          @input="handleSearch"
        ></el-input>
        <el-select 
          v-model="searchForm.status" 
          placeholder="设备状态" 
          style="width: 150px; margin-right: 16px;"
          clearable
          @change="handleSearch"
        >
          <el-option label="全部状态" value=""></el-option>
          <el-option label="运行中" value="online"></el-option>
          <el-option label="故障" value="fault"></el-option>
          <el-option label="离线" value="offline"></el-option>
        </el-select>
        <el-button type="primary" @click="handleSearch">搜索</el-button>
        <el-button @click="handleReset">重置</el-button>
        <el-button type="success" @click="openReportDialog" style="margin-left: 16px;">故障上报</el-button>
      </div>

      <el-table 
        :data="tableData" 
        style="width: 100%; margin-top: 20px;"
        border
        :row-class-name="tableRowClassName"
      >
        <el-table-column prop="deviceCode" label="设备编号" width="180" align="center"></el-table-column>
        <el-table-column prop="branchName" label="社保办事网点" align="center"></el-table-column>
        <el-table-column prop="location" label="摆放位置" align="center"></el-table-column>
        <el-table-column prop="status" label="设备运行状态" width="120" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="medium">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="idReaderStatus" label="身份读取" width="110" align="center">
          <template slot-scope="scope">
            <el-tag :type="getModuleStatusType(scope.row.idReaderStatus)" size="small">
              {{ getModuleStatusText(scope.row.idReaderStatus) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="printerStatus" label="证明打印" width="110" align="center">
          <template slot-scope="scope">
            <el-tag :type="getModuleStatusType(scope.row.printerStatus)" size="small">
              {{ getModuleStatusText(scope.row.printerStatus) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="networkStatus" label="联网核验" width="110" align="center">
          <template slot-scope="scope">
            <el-tag :type="getModuleStatusType(scope.row.networkStatus)" size="small">
              {{ getModuleStatusText(scope.row.networkStatus) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" align="center">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="reportDevice(scope.row)">上报故障</el-button>
            <el-dropdown @command="(command) => changeDeviceStatus(scope.row, command)" trigger="click">
              <el-button type="text" size="small">状态变更<i class="el-icon-arrow-down el-icon--right"></i></el-button>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="online">设为运行中</el-dropdown-item>
                <el-dropdown-item command="fault">设为故障</el-dropdown-item>
                <el-dropdown-item command="offline">设为离线</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="pagination.currentPage"
        :page-sizes="[5, 10, 20, 50]"
        :page-size="pagination.pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="pagination.total"
        style="margin-top: 20px; justify-content: flex-end;"
      ></el-pagination>
    </div>

    <el-dialog
      title="故障上报"
      :visible.sync="reportDialogVisible"
      width="500px"
      :before-close="handleCloseDialog"
    >
      <el-form :model="reportForm" :rules="reportRules" ref="reportFormRef" label-width="100px">
        <el-form-item label="工单编号">
          <el-input v-model="reportForm.orderNo" disabled></el-input>
        </el-form-item>
        <el-form-item label="选择设备" prop="deviceId">
          <el-select v-model="reportForm.deviceId" placeholder="请选择设备" style="width: 100%;">
            <el-option
              v-for="device in allDevices"
              :key="device.id"
              :label="`${device.deviceCode} - ${device.branchName}`"
              :value="device.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="故障说明" prop="faultDescription">
          <el-input
            type="textarea"
            v-model="reportForm.faultDescription"
            :rows="4"
            placeholder="请详细描述故障情况"
            maxlength="500"
            show-word-limit
          ></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleCloseDialog">取 消</el-button>
        <el-button type="primary" @click="submitReport">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'DeviceList',
  data() {
    return {
      searchForm: {
        deviceCode: '',
        branchName: '',
        status: ''
      },
      allDevices: [],
      tableData: [],
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      reportDialogVisible: false,
      reportForm: {
        orderNo: '',
        deviceId: '',
        faultDescription: ''
      },
      reportRules: {
        deviceId: [
          { required: true, message: '请选择故障设备', trigger: 'change' },
          { type: 'number', message: '请选择有效的设备', trigger: 'change' }
        ],
        faultDescription: [
          { required: true, message: '请详细描述故障情况', trigger: 'blur' },
          { min: 10, message: '故障说明至少10个字符，请详细描述', trigger: 'blur' },
          { max: 500, message: '故障说明不能超过500个字符', trigger: 'blur' }
        ]
      },
      mockData: [
        { id: 1, deviceCode: 'SB-2024-001', branchName: '市社保局服务大厅', location: '一楼入口处', status: 'online', idReaderStatus: 'normal', printerStatus: 'normal', networkStatus: 'normal' },
        { id: 2, deviceCode: 'SB-2024-002', branchName: '市社保局服务大厅', location: '二楼办事区', status: 'online', idReaderStatus: 'normal', printerStatus: 'warning', networkStatus: 'normal' },
        { id: 3, deviceCode: 'SB-2024-003', branchName: '东城区社保所', location: '办事大厅', status: 'fault', idReaderStatus: 'error', printerStatus: 'error', networkStatus: 'error' },
        { id: 4, deviceCode: 'SB-2024-004', branchName: '西城区社保所', location: '一楼大厅', status: 'online', idReaderStatus: 'normal', printerStatus: 'normal', networkStatus: 'warning' },
        { id: 5, deviceCode: 'SB-2024-005', branchName: '南城区社保所', location: '办事窗口旁', status: 'offline', idReaderStatus: 'offline', printerStatus: 'offline', networkStatus: 'offline' },
        { id: 6, deviceCode: 'SB-2024-006', branchName: '北城区社保所', location: '二楼201室门口', status: 'online', idReaderStatus: 'normal', printerStatus: 'normal', networkStatus: 'normal' },
        { id: 7, deviceCode: 'SB-2024-007', branchName: '开发区社保中心', location: '大厅左侧', status: 'online', idReaderStatus: 'warning', printerStatus: 'normal', networkStatus: 'normal' },
        { id: 8, deviceCode: 'SB-2024-008', branchName: '高新区社保分中心', location: '服务台旁', status: 'fault', idReaderStatus: 'error', printerStatus: 'normal', networkStatus: 'error' },
        { id: 9, deviceCode: 'SB-2024-009', branchName: '滨海新区社保中心', location: 'A区办事大厅', status: 'online', idReaderStatus: 'normal', printerStatus: 'normal', networkStatus: 'normal' },
        { id: 10, deviceCode: 'SB-2024-010', branchName: '滨海新区社保中心', location: 'B区办事大厅', status: 'online', idReaderStatus: 'normal', printerStatus: 'warning', networkStatus: 'normal' },
        { id: 11, deviceCode: 'SB-2024-011', branchName: '江北区社保所', location: '一楼大厅', status: 'offline', idReaderStatus: 'offline', printerStatus: 'offline', networkStatus: 'offline' },
        { id: 12, deviceCode: 'SB-2024-012', branchName: '江南区社保所', location: '二楼服务中心', status: 'online', idReaderStatus: 'normal', printerStatus: 'normal', networkStatus: 'normal' },
        { id: 13, deviceCode: 'SB-2024-013', branchName: '站前区社保中心', location: '办事大厅', status: 'online', idReaderStatus: 'normal', printerStatus: 'normal', networkStatus: 'warning' },
        { id: 14, deviceCode: 'SB-2024-014', branchName: '站后区社保中心', location: 'A栋1楼', status: 'fault', idReaderStatus: 'error', printerStatus: 'error', networkStatus: 'error' },
        { id: 15, deviceCode: 'SB-2024-015', branchName: '中心区社保所', location: '政务中心', status: 'online', idReaderStatus: 'normal', printerStatus: 'normal', networkStatus: 'normal' }
      ]
    }
  },
  computed: {
    filteredData() {
      let data = [...this.mockData]
      if (this.searchForm.deviceCode) {
        data = data.filter(item => 
          item.deviceCode.toLowerCase().includes(this.searchForm.deviceCode.toLowerCase())
        )
      }
      if (this.searchForm.branchName) {
        data = data.filter(item => 
          item.branchName.toLowerCase().includes(this.searchForm.branchName.toLowerCase())
        )
      }
      if (this.searchForm.status) {
        data = data.filter(item => item.status === this.searchForm.status)
      }
      return data
    }
  },
  created() {
    this.allDevices = this.mockData
    this.loadData()
  },
  methods: {
    loadData() {
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      this.tableData = this.filteredData.slice(start, end)
      this.pagination.total = this.filteredData.length
    },
    handleSearch() {
      this.pagination.currentPage = 1
      this.loadData()
    },
    handleReset() {
      this.searchForm.deviceCode = ''
      this.searchForm.branchName = ''
      this.searchForm.status = ''
      this.pagination.currentPage = 1
      this.loadData()
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.loadData()
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
      this.loadData()
    },
    getStatusType(status) {
      const statusMap = {
        online: 'success',
        fault: 'danger',
        offline: 'info'
      }
      return statusMap[status] || 'info'
    },
    getStatusText(status) {
      const statusMap = {
        online: '运行中',
        fault: '故障',
        offline: '离线'
      }
      return statusMap[status] || '未知'
    },
    getModuleStatusType(status) {
      const statusMap = {
        normal: 'success',
        warning: 'warning',
        error: 'danger',
        offline: 'info'
      }
      return statusMap[status] || 'info'
    },
    getModuleStatusText(status) {
      const statusMap = {
        normal: '正常',
        warning: '异常',
        error: '故障',
        offline: '离线'
      }
      return statusMap[status] || '未知'
    },
    changeDeviceStatus(row, newStatus) {
      const device = this.mockData.find(d => d.id === row.id)
      if (device) {
        device.status = newStatus
        if (newStatus === 'online') {
          device.idReaderStatus = 'normal'
          device.printerStatus = 'normal'
          device.networkStatus = 'normal'
        } else if (newStatus === 'offline') {
          device.idReaderStatus = 'offline'
          device.printerStatus = 'offline'
          device.networkStatus = 'offline'
        } else if (newStatus === 'fault') {
          device.idReaderStatus = 'error'
          device.printerStatus = 'error'
          device.networkStatus = 'error'
        }
        this.loadData()
        this.$message.success(`设备 ${device.deviceCode} 状态已更新为 ${this.getStatusText(newStatus)}`)
      }
    },
    generateOrderNo() {
      const now = new Date()
      const year = now.getFullYear()
      const month = String(now.getMonth() + 1).padStart(2, '0')
      const day = String(now.getDate()).padStart(2, '0')
      const hours = String(now.getHours()).padStart(2, '0')
      const minutes = String(now.getMinutes()).padStart(2, '0')
      const seconds = String(now.getSeconds()).padStart(2, '0')
      const random = String(Math.floor(Math.random() * 10000)).padStart(4, '0')
      return `GZ${year}${month}${day}${hours}${minutes}${seconds}${random}`
    },
    openReportDialog() {
      this.reportForm.orderNo = this.generateOrderNo()
      this.reportForm.deviceId = ''
      this.reportForm.faultDescription = ''
      this.reportDialogVisible = true
      if (this.$refs.reportFormRef) {
        this.$refs.reportFormRef.resetFields()
      }
    },
    reportDevice(row) {
      this.reportForm.orderNo = this.generateOrderNo()
      this.reportForm.deviceId = row.id
      this.reportForm.faultDescription = ''
      this.reportDialogVisible = true
    },
    handleCloseDialog() {
      this.reportDialogVisible = false
    },
    submitReport() {
      if (!this.reportForm.deviceId) {
        this.$message.warning('请先选择要上报故障的设备')
        return
      }
      this.$refs.reportFormRef.validate((valid) => {
        if (valid) {
          const device = this.allDevices.find(d => d.id === this.reportForm.deviceId)
          if (!device) {
            this.$message.error('选择的设备不存在，请重新选择')
            return
          }
          this.$message.success(`故障上报成功！工单编号：${this.reportForm.orderNo}，设备：${device.deviceCode}`)
          this.reportDialogVisible = false
        } else {
          this.$message.error('请完善表单信息后再提交')
          return false
        }
      })
    },
    tableRowClassName({ row }) {
      if (row.status === 'fault') {
        return 'fault-row'
      } else if (row.status === 'offline') {
        return 'offline-row'
      }
      return ''
    }
  }
}
</script>

<style scoped>
.device-management {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 24px 32px;
  border-radius: 8px;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.header h1 {
  font-size: 28px;
  font-weight: 600;
  margin: 0;
}

.content {
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.search-bar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}

.el-pagination {
  display: flex;
}
</style>

<style>
.fault-row {
  background-color: #fff0f0 !important;
}

.fault-row:hover > td {
  background-color: #ffe6e6 !important;
}

.offline-row {
  background-color: #f5f7fa !important;
}

.offline-row:hover > td {
  background-color: #ebeef5 !important;
}

.el-table .fault-row td {
  border-bottom-color: #ffcccc;
}

.el-table .offline-row td {
  border-bottom-color: #dcdfe6;
}
</style>
