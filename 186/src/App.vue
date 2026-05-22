<template>
  <div class="app-container">
    <el-header class="header">
      <div class="header-content">
        <h1 class="title">税务自助完税证明打印终端运维管理系统</h1>
      </div>
    </el-header>
    <el-main class="main-content">
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm" class="search-form">
          <el-form-item label="设备编号">
            <el-input
              v-model="searchForm.deviceCode"
              placeholder="请输入设备编号"
              clearable
              style="width: 200px"
            ></el-input>
          </el-form-item>
          <el-form-item label="税务网点">
            <el-input
              v-model="searchForm.branchName"
              placeholder="请输入税务网点名称"
              clearable
              style="width: 200px"
            ></el-input>
          </el-form-item>
          <el-form-item label="运行状态">
            <el-select
              v-model="searchForm.status"
              placeholder="请选择运行状态"
              clearable
              style="width: 150px"
            >
              <el-option label="在线" value="online"></el-option>
              <el-option label="离线" value="offline"></el-option>
              <el-option label="故障" value="fault"></el-option>
              <el-option label="维护中" value="maintenance"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      <div class="table-container">
        <div class="table-header">
          <h3>设备列表</h3>
          <el-button type="primary" @click="openReportDialog">故障上报</el-button>
        </div>
        <el-table
          :data="tableData"
          border
          stripe
          style="width: 100%"
          @selection-change="handleSelectionChange"
          :row-class-name="getTableRowClassName"
        >
          <el-table-column type="selection" width="55"></el-table-column>
          <el-table-column prop="deviceCode" label="设备编号" width="150"></el-table-column>
          <el-table-column prop="branchName" label="税务服务厅" width="200"></el-table-column>
          <el-table-column prop="location" label="布设位置"></el-table-column>
          <el-table-column prop="status" label="运行状态" width="100">
            <template slot-scope="scope">
              <el-tag :type="getStatusType(scope.row.status)" size="small">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="身份核验" width="100">
            <template slot-scope="scope">
              <el-tag :type="getModuleStatusType(scope.row.identityVerify)" size="mini">
                {{ getModuleStatusText(scope.row.identityVerify) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="证明打印" width="100">
            <template slot-scope="scope">
              <el-tag :type="getModuleStatusType(scope.row.printModule)" size="mini">
                {{ getModuleStatusText(scope.row.printModule) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="税务联网核验" width="120">
            <template slot-scope="scope">
              <el-tag :type="getModuleStatusType(scope.row.networkVerify)" size="mini">
                {{ getModuleStatusText(scope.row.networkVerify) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150">
            <template slot-scope="scope">
              <el-button type="text" size="small" @click="handleReport(scope.row)">
                故障上报
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <div class="pagination">
          <el-pagination
            background
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="pagination.currentPage"
            :page-sizes="[10, 20, 50, 100]"
            :page-size="pagination.pageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="pagination.total"
          ></el-pagination>
        </div>
      </div>
    </el-main>

    <el-dialog
      title="故障上报"
      :visible.sync="reportDialogVisible"
      width="600px"
      @close="closeReportDialog"
    >
      <el-form :model="reportForm" :rules="reportRules" ref="reportForm" label-width="100px">
        <el-form-item label="工单编号">
          <el-input v-model="reportForm.workOrderNo" disabled></el-input>
        </el-form-item>
        <el-form-item label="设备编号" prop="deviceCode">
          <el-select v-model="reportForm.deviceCode" placeholder="请选择设备" style="width: 100%" filterable>
            <el-option
              v-for="device in allDevices"
              :key="device.deviceCode"
              :label="device.deviceCode"
              :value="device.deviceCode"
            >
              <span style="float: left">{{ device.deviceCode }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">
                {{ device.branchName }}
                <el-tag :type="getStatusType(device.status)" size="mini" style="margin-left: 8px">
                  {{ getStatusText(device.status) }}
                </el-tag>
              </span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="异常情况" prop="abnormalDesc">
          <el-input
            type="textarea"
            v-model="reportForm.abnormalDesc"
            placeholder="请详细描述异常情况"
            :rows="5"
            maxlength="500"
            show-word-limit
          ></el-input>
        </el-form-item>
        <el-form-item label="上报人">
          <el-input v-model="reportForm.reporter" placeholder="请输入上报人姓名"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="reportDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitReport">提交</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      searchForm: {
        deviceCode: '',
        branchName: '',
        status: ''
      },
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      allDevices: [],
      tableData: [],
      selectedDevices: [],
      reportDialogVisible: false,
      reportForm: {
        workOrderNo: '',
        deviceCode: '',
        abnormalDesc: '',
        reporter: ''
      },
      reportRules: {
        deviceCode: [
          { required: true, message: '请选择设备', trigger: 'change' }
        ],
        abnormalDesc: [
          { required: true, message: '请输入异常情况描述', trigger: 'blur' }
        ]
      },
      mockData: [
        { deviceCode: 'TAX-2024-001', branchName: '北京市税务局第一分局', location: '一楼大厅左侧', status: 'online', identityVerify: 'normal', printModule: 'normal', networkVerify: 'normal' },
        { deviceCode: 'TAX-2024-002', branchName: '北京市税务局第一分局', location: '一楼大厅右侧', status: 'online', identityVerify: 'normal', printModule: 'normal', networkVerify: 'normal' },
        { deviceCode: 'TAX-2024-003', branchName: '北京市税务局第二分局', location: '二楼办税服务区', status: 'offline', identityVerify: 'abnormal', printModule: 'abnormal', networkVerify: 'abnormal' },
        { deviceCode: 'TAX-2024-004', branchName: '北京市税务局第二分局', location: '二楼自助服务区', status: 'fault', identityVerify: 'abnormal', printModule: 'fault', networkVerify: 'abnormal' },
        { deviceCode: 'TAX-2024-005', branchName: '北京市税务局第三分局', location: '一楼入口处', status: 'online', identityVerify: 'normal', printModule: 'normal', networkVerify: 'normal' },
        { deviceCode: 'TAX-2024-006', branchName: '北京市税务局第三分局', location: '三楼办公区', status: 'maintenance', identityVerify: 'maintenance', printModule: 'maintenance', networkVerify: 'maintenance' },
        { deviceCode: 'TAX-2024-007', branchName: '上海市税务局第一分局', location: '一楼大厅A区', status: 'online', identityVerify: 'normal', printModule: 'normal', networkVerify: 'normal' },
        { deviceCode: 'TAX-2024-008', branchName: '上海市税务局第一分局', location: '一楼大厅B区', status: 'fault', identityVerify: 'fault', printModule: 'abnormal', networkVerify: 'abnormal' },
        { deviceCode: 'TAX-2024-009', branchName: '上海市税务局第二分局', location: '二楼办税厅', status: 'online', identityVerify: 'normal', printModule: 'normal', networkVerify: 'normal' },
        { deviceCode: 'TAX-2024-010', branchName: '上海市税务局第二分局', location: '三楼服务区', status: 'offline', identityVerify: 'abnormal', printModule: 'abnormal', networkVerify: 'abnormal' },
        { deviceCode: 'TAX-2024-011', branchName: '广州市税务局第一分局', location: '一楼入口左侧', status: 'online', identityVerify: 'normal', printModule: 'normal', networkVerify: 'normal' },
        { deviceCode: 'TAX-2024-012', branchName: '广州市税务局第一分局', location: '一楼入口右侧', status: 'online', identityVerify: 'normal', printModule: 'normal', networkVerify: 'normal' },
        { deviceCode: 'TAX-2024-013', branchName: '广州市税务局第二分局', location: '二楼自助区', status: 'maintenance', identityVerify: 'maintenance', printModule: 'maintenance', networkVerify: 'maintenance' },
        { deviceCode: 'TAX-2024-014', branchName: '深圳市税务局第一分局', location: '一楼大厅', status: 'fault', identityVerify: 'abnormal', printModule: 'fault', networkVerify: 'fault' },
        { deviceCode: 'TAX-2024-015', branchName: '深圳市税务局第一分局', location: '二楼办公区', status: 'online', identityVerify: 'normal', printModule: 'normal', networkVerify: 'normal' },
        { deviceCode: 'TAX-2024-016', branchName: '杭州市税务局第一分局', location: '一楼大厅A区', status: 'online', identityVerify: 'normal', printModule: 'warning', networkVerify: 'normal' },
        { deviceCode: 'TAX-2024-017', branchName: '杭州市税务局第一分局', location: '一楼大厅B区', status: 'offline', identityVerify: 'abnormal', printModule: 'abnormal', networkVerify: 'abnormal' },
        { deviceCode: 'TAX-2024-018', branchName: '杭州市税务局第二分局', location: '二楼办税厅', status: 'online', identityVerify: 'normal', printModule: 'normal', networkVerify: 'normal' },
        { deviceCode: 'TAX-2024-019', branchName: '成都市税务局第一分局', location: '一楼服务区', status: 'fault', identityVerify: 'fault', printModule: 'fault', networkVerify: 'abnormal' },
        { deviceCode: 'TAX-2024-020', branchName: '成都市税务局第一分局', location: '二楼办公区', status: 'online', identityVerify: 'normal', printModule: 'normal', networkVerify: 'normal' },
        { deviceCode: 'TAX-2024-021', branchName: '武汉市税务局第一分局', location: '一楼大厅', status: 'online', identityVerify: 'normal', printModule: 'warning', networkVerify: 'normal' },
        { deviceCode: 'TAX-2024-022', branchName: '武汉市税务局第一分局', location: '二楼自助区', status: 'maintenance', identityVerify: 'maintenance', printModule: 'maintenance', networkVerify: 'maintenance' },
        { deviceCode: 'TAX-2024-023', branchName: '南京市税务局第一分局', location: '一楼入口处', status: 'online', identityVerify: 'normal', printModule: 'normal', networkVerify: 'normal' },
        { deviceCode: 'TAX-2024-024', branchName: '南京市税务局第一分局', location: '二楼办税区', status: 'fault', identityVerify: 'abnormal', printModule: 'fault', networkVerify: 'abnormal' },
        { deviceCode: 'TAX-2024-025', branchName: '西安市税务局第一分局', location: '一楼大厅左侧', status: 'online', identityVerify: 'normal', printModule: 'normal', networkVerify: 'warning' }
      ]
    }
  },
  created() {
    this.initData()
  },
  methods: {
    initData() {
      this.allDevices = [...this.mockData]
      this.pagination.total = this.mockData.length
      this.loadTableData()
    },
    loadTableData() {
      let filteredData = [...this.allDevices]
      
      if (this.searchForm.deviceCode) {
        const keyword = this.searchForm.deviceCode.toLowerCase().trim()
        filteredData = filteredData.filter(item => {
          const deviceCode = item.deviceCode.toLowerCase()
          return deviceCode.includes(keyword) || 
                 deviceCode.split('-').some(part => part.includes(keyword))
        })
      }
      
      if (this.searchForm.branchName) {
        const keyword = this.searchForm.branchName.trim()
        filteredData = filteredData.filter(item => {
          const branchName = item.branchName
          return branchName.includes(keyword) ||
                 branchName.split(/[市区分局]/).some(part => part.includes(keyword))
        })
      }
      
      if (this.searchForm.status) {
        filteredData = filteredData.filter(item => item.status === this.searchForm.status)
      }
      
      this.pagination.total = filteredData.length
      
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      this.tableData = filteredData.slice(start, end)
    },
    getModuleStatusType(status) {
      const statusMap = {
        normal: 'success',
        warning: 'warning',
        abnormal: 'danger',
        fault: 'danger',
        maintenance: 'info'
      }
      return statusMap[status] || 'info'
    },
    getModuleStatusText(status) {
      const statusMap = {
        normal: '正常',
        warning: '警告',
        abnormal: '异常',
        fault: '故障',
        maintenance: '维护'
      }
      return statusMap[status] || '未知'
    },
    getTableRowClassName({ row }) {
      if (row.status === 'fault') {
        return 'fault-row'
      } else if (row.status === 'offline') {
        return 'offline-row'
      }
      return ''
    },
    handleSearch() {
      this.pagination.currentPage = 1
      this.loadTableData()
    },
    handleReset() {
      this.searchForm = {
        deviceCode: '',
        branchName: '',
        status: ''
      }
      this.pagination.currentPage = 1
      this.loadTableData()
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.loadTableData()
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
      this.loadTableData()
    },
    handleSelectionChange(val) {
      this.selectedDevices = val
    },
    getStatusType(status) {
      const statusMap = {
        online: 'success',
        offline: 'info',
        fault: 'danger',
        maintenance: 'warning'
      }
      return statusMap[status] || 'info'
    },
    getStatusText(status) {
      const statusMap = {
        online: '在线',
        offline: '离线',
        fault: '故障',
        maintenance: '维护中'
      }
      return statusMap[status] || '未知'
    },
    generateWorkOrderNo() {
      const date = new Date()
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      const random = Math.floor(Math.random() * 10000).toString().padStart(4, '0')
      return `WO${year}${month}${day}${random}`
    },
    openReportDialog() {
      this.reportForm = {
        workOrderNo: this.generateWorkOrderNo(),
        deviceCode: '',
        abnormalDesc: '',
        reporter: ''
      }
      
      if (this.selectedDevices.length === 1) {
        this.reportForm.deviceCode = this.selectedDevices[0].deviceCode
      }
      
      this.reportDialogVisible = true
    },
    handleReport(row) {
      this.reportForm = {
        workOrderNo: this.generateWorkOrderNo(),
        deviceCode: row.deviceCode,
        abnormalDesc: '',
        reporter: ''
      }
      this.reportDialogVisible = true
    },
    closeReportDialog() {
      this.$refs.reportForm.resetFields()
    },
    submitReport() {
      if (!this.reportForm.deviceCode) {
        this.$message({
          type: 'warning',
          message: '请先选择需要上报故障的设备！'
        })
        return
      }
      
      this.$refs.reportForm.validate((valid) => {
        if (valid) {
          this.$message({
            type: 'success',
            message: `故障上报成功！工单编号：${this.reportForm.workOrderNo}`
          })
          this.reportDialogVisible = false
        }
      })
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  height: 100%;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
}

.app-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
}

.header {
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  color: white;
  padding: 0 20px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.header-content {
  width: 100%;
}

.title {
  font-size: 24px;
  font-weight: 500;
  letter-spacing: 2px;
}

.main-content {
  flex: 1;
  padding: 20px;
  overflow: auto;
}

.search-bar {
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.search-form {
  margin-bottom: 0;
}

.table-container {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.table-header h3 {
  font-size: 18px;
  color: #303133;
  font-weight: 500;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.el-table {
  font-size: 14px;
}

.el-table .fault-row {
  background-color: #fef0f0 !important;
}

.el-table .fault-row:hover > td {
  background-color: #fde2e2 !important;
}

.el-table .offline-row {
  background-color: #f4f4f5 !important;
}

.el-table .offline-row:hover > td {
  background-color: #e9e9eb !important;
}

.el-table .cell {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.el-tag--success {
  background-color: #f0f9eb;
  border-color: #e1f3d8;
  color: #67c23a;
}

.el-tag--danger {
  background-color: #fef0f0;
  border-color: #fde2e2;
  color: #f56c6c;
}

.el-tag--warning {
  background-color: #fdf6ec;
  border-color: #faecd8;
  color: #e6a23c;
}

.el-tag--info {
  background-color: #f4f4f5;
  border-color: #e9e9eb;
  color: #909399;
}

.dialog-footer {
  text-align: right;
}
</style>
