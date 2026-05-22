<template>
  <div class="device-management">
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="设备编号">
          <el-input v-model="searchForm.deviceCode" placeholder="请输入设备编号" clearable></el-input>
        </el-form-item>
        <el-form-item label="所属院区">
          <el-select v-model="searchForm.hospitalArea" placeholder="请选择院区" clearable>
            <el-option label="全部院区" value=""></el-option>
            <el-option label="东院区" value="东院区"></el-option>
            <el-option label="西院区" value="西院区"></el-option>
            <el-option label="南院区" value="南院区"></el-option>
            <el-option label="北院区" value="北院区"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="运行状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
            <el-option label="全部状态" value=""></el-option>
            <el-option label="运行中" value="online"></el-option>
            <el-option label="异常" value="warning"></el-option>
            <el-option label="离线" value="offline"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card">
      <div class="card-header">
        <span class="card-title">设备列表</span>
        <el-button type="danger" @click="openReportDialog">故障提报</el-button>
      </div>
      
      <el-table 
        :data="tableData" 
        border 
        style="width: 100%"
        :row-class-name="getRowClassName"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column prop="deviceCode" label="设备编号" width="150" align="center"></el-table-column>
        <el-table-column prop="hospitalArea" label="院区" width="120" align="center"></el-table-column>
        <el-table-column prop="department" label="科室" width="150" align="center"></el-table-column>
        <el-table-column prop="location" label="摆放位置" align="center"></el-table-column>
        <el-table-column prop="status" label="整体状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="small">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="读卡模块" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.cardReader)" size="mini">
              {{ getStatusText(scope.row.cardReader) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="打印模块" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.printer)" size="mini">
              {{ getStatusText(scope.row.printer) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="加密模块" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.encrypt)" size="mini">
              {{ getStatusText(scope.row.encrypt) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" align="center">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="handleReport(scope.row)">故障提报</el-button>
            <el-button type="text" size="small">查看详情</el-button>
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
          :total="pagination.total"
        >
        </el-pagination>
      </div>
    </el-card>

    <el-dialog
      title="故障提报"
      :visible.sync="reportDialogVisible"
      width="600px"
      @close="closeReportDialog"
    >
      <el-form :model="reportForm" :rules="reportRules" ref="reportForm" label-width="100px">
        <el-form-item label="工单编号" prop="orderNo">
          <el-input v-model="reportForm.orderNo" disabled></el-input>
        </el-form-item>
        <el-form-item label="选择设备" prop="deviceId">
          <el-select v-model="reportForm.deviceId" placeholder="请选择设备" style="width: 100%" @change="onDeviceSelect" filterable>
            <el-option
              v-for="device in allDevices"
              :key="device.id"
              :label="`${device.deviceCode} - ${device.hospitalArea} ${device.department}`"
              :value="device.id"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="设备编号" prop="deviceCode">
          <el-input v-model="reportForm.deviceCode" disabled></el-input>
        </el-form-item>
        <el-form-item label="院区科室" prop="hospitalDept">
          <el-input v-model="reportForm.hospitalDept" disabled></el-input>
        </el-form-item>
        <el-form-item label="异常情况" prop="problemDesc">
          <el-input
            type="textarea"
            v-model="reportForm.problemDesc"
            :rows="4"
            placeholder="请详细描述设备异常情况"
          >
          </el-input>
        </el-form-item>
        <el-form-item label="联系人">
          <el-input v-model="reportForm.contactPerson" placeholder="请输入联系人姓名"></el-input>
        </el-form-item>
        <el-form-item label="联系电话">
          <el-input v-model="reportForm.contactPhone" placeholder="请输入联系电话"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="reportDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitReport">提 交</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'DeviceManagement',
  data() {
    return {
      searchForm: {
        deviceCode: '',
        hospitalArea: '',
        status: ''
      },
      reportDialogVisible: false,
      reportForm: {
        orderNo: '',
        deviceId: '',
        deviceCode: '',
        hospitalDept: '',
        problemDesc: '',
        contactPerson: '',
        contactPhone: ''
      },
      reportRules: {
        deviceId: [
          { required: true, message: '请选择设备', trigger: 'change' }
        ],
        problemDesc: [
          { required: true, message: '请填写异常情况', trigger: 'blur' },
          { min: 10, message: '异常情况描述不能少于10个字', trigger: 'blur' }
        ],
        contactPerson: [
          { required: true, message: '请填写联系人姓名', trigger: 'blur' }
        ],
        contactPhone: [
          { required: true, message: '请填写联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ]
      },
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      selectedDevices: [],
      mockDevices: [
        { id: 1, deviceCode: 'DY001', hospitalArea: '东院区', department: '门诊大厅', location: '一楼挂号处旁', status: 'online', cardReader: 'online', printer: 'online', encrypt: 'online' },
        { id: 2, deviceCode: 'DY002', hospitalArea: '东院区', department: '内科门诊', location: '二楼内科候诊区', status: 'online', cardReader: 'online', printer: 'warning', encrypt: 'online' },
        { id: 3, deviceCode: 'DY003', hospitalArea: '东院区', department: '外科门诊', location: '三楼外科候诊区', status: 'warning', cardReader: 'online', printer: 'offline', encrypt: 'online' },
        { id: 4, deviceCode: 'DY004', hospitalArea: '东院区', department: '妇产科门诊', location: '四楼妇产科门口', status: 'offline', cardReader: 'offline', printer: 'offline', encrypt: 'offline' },
        { id: 5, deviceCode: 'XY001', hospitalArea: '西院区', department: '门诊大厅', location: '一楼导医台旁', status: 'online', cardReader: 'online', printer: 'online', encrypt: 'warning' },
        { id: 6, deviceCode: 'XY002', hospitalArea: '西院区', department: '儿科门诊', location: '二楼儿科候诊区', status: 'online', cardReader: 'online', printer: 'online', encrypt: 'online' },
        { id: 7, deviceCode: 'XY003', hospitalArea: '西院区', department: '骨科门诊', location: '三楼骨科诊室旁', status: 'warning', cardReader: 'warning', printer: 'online', encrypt: 'online' },
        { id: 8, deviceCode: 'NY001', hospitalArea: '南院区', department: '急诊大厅', location: '急诊入口处', status: 'online', cardReader: 'online', printer: 'online', encrypt: 'online' },
        { id: 9, deviceCode: 'NY002', hospitalArea: '南院区', department: '放射科', location: '放射科登记处旁', status: 'offline', cardReader: 'offline', printer: 'offline', encrypt: 'offline' },
        { id: 10, deviceCode: 'BY001', hospitalArea: '北院区', department: '门诊大厅', location: '一楼自助服务区', status: 'online', cardReader: 'online', printer: 'warning', encrypt: 'online' },
        { id: 11, deviceCode: 'BY002', hospitalArea: '北院区', department: '心内科', location: '二楼心内科门口', status: 'online', cardReader: 'online', printer: 'online', encrypt: 'online' },
        { id: 12, deviceCode: 'BY003', hospitalArea: '北院区', department: '消化内科', location: '三楼消化科候诊区', status: 'warning', cardReader: 'online', printer: 'offline', encrypt: 'warning' }
      ]
    }
  },
  computed: {
    allDevices() {
      return this.mockDevices
    },
    filteredDevices() {
      let result = [...this.mockDevices]
      if (this.searchForm.deviceCode) {
        const keyword = this.searchForm.deviceCode.toLowerCase().trim()
        result = result.filter(item => 
          item.deviceCode.toLowerCase().includes(keyword) ||
          item.department.toLowerCase().includes(keyword) ||
          item.location.toLowerCase().includes(keyword)
        )
      }
      if (this.searchForm.hospitalArea) {
        result = result.filter(item => item.hospitalArea === this.searchForm.hospitalArea)
      }
      if (this.searchForm.status) {
        result = result.filter(item => item.status === this.searchForm.status)
      }
      return result
    },
    tableData() {
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      return this.filteredDevices.slice(start, end)
    }
  },
  watch: {
    filteredDevices(val) {
      this.pagination.total = val.length
    }
  },
  mounted() {
    this.pagination.total = this.mockDevices.length
  },
  methods: {
    getRowClassName({ row }) {
      if (row.status === 'warning') {
        return 'warning-row'
      } else if (row.status === 'offline') {
        return 'offline-row'
      }
      return ''
    },
    getStatusType(status) {
      const typeMap = {
        online: 'success',
        warning: 'warning',
        offline: 'danger'
      }
      return typeMap[status] || 'info'
    },
    getStatusText(status) {
      const textMap = {
        online: '运行中',
        warning: '异常',
        offline: '离线'
      }
      return textMap[status] || '未知'
    },
    handleSearch() {
      this.pagination.currentPage = 1
      this.pagination.total = this.filteredDevices.length
    },
    handleReset() {
      this.searchForm = {
        deviceCode: '',
        hospitalArea: '',
        status: ''
      }
      this.pagination.currentPage = 1
      this.pagination.total = this.mockDevices.length
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
    },
    handleSelectionChange(val) {
      this.selectedDevices = val
    },
    onDeviceSelect(deviceId) {
      const device = this.allDevices.find(d => d.id === deviceId)
      if (device) {
        this.reportForm.deviceCode = device.deviceCode
        this.reportForm.hospitalDept = `${device.hospitalArea} - ${device.department}`
      }
    },
    generateOrderNo() {
      const now = new Date()
      const year = now.getFullYear()
      const month = String(now.getMonth() + 1).padStart(2, '0')
      const day = String(now.getDate()).padStart(2, '0')
      const random = String(Math.floor(Math.random() * 10000)).padStart(4, '0')
      return `GD${year}${month}${day}${random}`
    },
    openReportDialog() {
      this.reportForm.orderNo = this.generateOrderNo()
      this.reportForm.deviceId = ''
      this.reportForm.deviceCode = ''
      this.reportForm.hospitalDept = ''
      this.reportForm.problemDesc = ''
      this.reportForm.contactPerson = ''
      this.reportForm.contactPhone = ''
      if (this.selectedDevices.length === 1) {
        const device = this.selectedDevices[0]
        this.reportForm.deviceId = device.id
        this.reportForm.deviceCode = device.deviceCode
        this.reportForm.hospitalDept = `${device.hospitalArea} - ${device.department}`
      }
      this.reportDialogVisible = true
    },
    handleReport(row) {
      this.reportForm.orderNo = this.generateOrderNo()
      this.reportForm.deviceId = row.id
      this.reportForm.deviceCode = row.deviceCode
      this.reportForm.hospitalDept = `${row.hospitalArea} - ${row.department}`
      this.reportForm.problemDesc = ''
      this.reportForm.contactPerson = ''
      this.reportForm.contactPhone = ''
      this.reportDialogVisible = true
    },
    closeReportDialog() {
      this.$refs.reportForm.resetFields()
    },
    submitReport() {
      if (!this.reportForm.deviceId) {
        this.$message.warning('请先选择需要提报故障的设备')
        return
      }
      this.$refs.reportForm.validate((valid) => {
        if (valid) {
          this.$message({
            type: 'success',
            message: `故障工单 ${this.reportForm.orderNo} 提交成功！我们会尽快处理。`
          })
          this.reportDialogVisible = false
        } else {
          this.$message.error('请完善表单信息后再提交')
        }
      })
    }
  }
}
</script>

<style scoped>
.device-management {
  height: 100%;
}

.search-card {
  margin-bottom: 20px;
}

.search-form {
  margin-bottom: 0;
}

.table-card {
  height: calc(100% - 100px);
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.card-title {
  font-size: 18px;
  font-weight: 500;
  color: #303133;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>

<style>
.el-table .warning-row {
  background-color: #fdf6ec !important;
}

.el-table .offline-row {
  background-color: #fef0f0 !important;
}

.el-table .warning-row:hover > td {
  background-color: #faecd8 !important;
}

.el-table .offline-row:hover > td {
  background-color: #fde2e2 !important;
}
</style>
