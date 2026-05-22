<template>
  <div class="device-container">
    <div class="header">
      <h1>不动产登记自助查询证明终端运维管理系统</h1>
    </div>
    
    <div class="content">
      <div class="search-bar">
        <el-input
          v-model="searchForm.keyword"
          placeholder="输入设备编号/大厅名称/布设点位搜索"
          clearable
          style="width: 350px; margin-right: 15px;"
          @keyup.enter.native="handleSearch"
        ></el-input>
        <el-select v-model="searchForm.status" placeholder="设备状态" clearable style="width: 150px; margin-right: 15px;">
          <el-option label="全部" value=""></el-option>
          <el-option label="正常运行" value="normal"></el-option>
          <el-option label="运行告警" value="warning"></el-option>
          <el-option label="故障停机" value="fault"></el-option>
          <el-option label="离线" value="offline"></el-option>
        </el-select>
        <el-button type="primary" @click="handleSearch" icon="el-icon-search">搜索</el-button>
        <el-button @click="handleReset" icon="el-icon-refresh">重置</el-button>
        <el-button type="success" @click="openReportDialog" style="margin-left: auto;" icon="el-icon-edit">故障上报</el-button>
      </div>

      <div class="table-wrapper">
        <el-table :data="tableData" border stripe style="width: 100%" :row-class-name="tableRowClassName">
          <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
          <el-table-column prop="deviceCode" label="设备编号" width="130" align="center"></el-table-column>
          <el-table-column prop="hallName" label="不动产服务大厅" width="160" align="center"></el-table-column>
          <el-table-column prop="location" label="布设点位" width="140" align="center"></el-table-column>
          <el-table-column label="设备运行状态" width="120" align="center">
            <template slot-scope="scope">
              <span :class="getStatusClass(scope.row.status)">
                {{ getStatusText(scope.row.status) }}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="身份核验" width="100" align="center">
            <template slot-scope="scope">
              <span :class="getModuleStatusClass(scope.row.modules.verify)">
                <i :class="getModuleIcon(scope.row.modules.verify)"></i>
                {{ getModuleStatusText(scope.row.modules.verify) }}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="证明打印" width="100" align="center">
            <template slot-scope="scope">
              <span :class="getModuleStatusClass(scope.row.modules.print)">
                <i :class="getModuleIcon(scope.row.modules.print)"></i>
                {{ getModuleStatusText(scope.row.modules.print) }}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="数据联网" width="100" align="center">
            <template slot-scope="scope">
              <span :class="getModuleStatusClass(scope.row.modules.network)">
                <i :class="getModuleIcon(scope.row.modules.network)"></i>
                {{ getModuleStatusText(scope.row.modules.network) }}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="180" align="center">
            <template slot-scope="scope">
              <el-button size="small" type="primary" @click="handleReport(scope.row)">上报故障</el-button>
              <el-button size="small" type="warning" @click="toggleDeviceStatus(scope.row)">切换状态</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div class="pagination-wrapper">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.page"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pagination.size"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
          background
        ></el-pagination>
      </div>
    </div>

    <el-dialog
      title="故障上报"
      :visible.sync="reportDialogVisible"
      width="600px"
      @close="resetReportForm"
    >
      <el-form :model="reportForm" :rules="reportRules" ref="reportForm" label-width="100px">
        <el-form-item label="工单编号">
          <el-input v-model="reportForm.orderNo" disabled></el-input>
        </el-form-item>
        <el-form-item label="选择设备" prop="deviceId">
          <el-select 
            v-model="reportForm.deviceId" 
            placeholder="请搜索选择设备" 
            style="width: 100%"
            filterable
            :filter-method="deviceFilterMethod"
            no-data-text="未找到匹配设备"
          >
            <el-option
              v-for="item in filteredDeviceOptions"
              :key="item.id"
              :label="item.deviceCode + ' - ' + item.hallName + ' - ' + item.location"
              :value="item.id"
            >
              <span>{{ item.deviceCode }}</span>
              <span style="color: #8492a6; font-size: 13px; margin-left: 10px;">{{ item.hallName }}</span>
              <span :class="getStatusClass(item.status)" style="margin-left: 10px; float: right;">
                {{ getStatusText(item.status) }}
              </span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="上报人" prop="reporter">
          <el-input v-model="reportForm.reporter" placeholder="请输入上报人姓名"></el-input>
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="reportForm.phone" placeholder="请输入联系电话"></el-input>
        </el-form-item>
        <el-form-item label="故障描述" prop="description">
          <el-input
            type="textarea"
            v-model="reportForm.description"
            placeholder="请详细描述故障情况（如：屏幕黑屏、无法打印、卡纸等）"
            :rows="4"
            maxlength="500"
            show-word-limit
          ></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="reportDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitReport" :loading="submitLoading">提交上报</el-button>
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
        keyword: '',
        status: ''
      },
      pagination: {
        page: 1,
        size: 10,
        total: 0
      },
      allDeviceList: [],
      tableData: [],
      reportDialogVisible: false,
      submitLoading: false,
      deviceSearchKeyword: '',
      reportForm: {
        orderNo: '',
        deviceId: '',
        reporter: '',
        phone: '',
        description: ''
      },
      reportRules: {
        deviceId: [
          { required: true, message: '请选择故障设备', trigger: 'change' }
        ],
        reporter: [
          { required: true, message: '请输入上报人姓名', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ],
        description: [
          { required: true, message: '请填写故障描述', trigger: 'blur' },
          { min: 5, message: '故障描述至少5个字符', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    filteredDeviceOptions() {
      if (!this.deviceSearchKeyword) {
        return this.allDeviceList
      }
      const keyword = this.deviceSearchKeyword.toLowerCase()
      return this.allDeviceList.filter(item => 
        item.deviceCode.toLowerCase().includes(keyword) ||
        item.hallName.includes(keyword) ||
        item.location.includes(keyword)
      )
    }
  },
  created() {
    this.initDeviceData()
    this.loadData()
  },
  methods: {
    initDeviceData() {
      this.allDeviceList = [
        { id: 1, deviceCode: 'BDC-001', hallName: '市政务服务中心', location: '一楼大厅东侧', status: 'normal', modules: { verify: 'normal', print: 'normal', network: 'normal' } },
        { id: 2, deviceCode: 'BDC-002', hallName: '市政务服务中心', location: '二楼办事区', status: 'normal', modules: { verify: 'normal', print: 'warning', network: 'normal' } },
        { id: 3, deviceCode: 'BDC-003', hallName: '区政务服务中心', location: '南门入口处', status: 'warning', modules: { verify: 'warning', print: 'normal', network: 'normal' } },
        { id: 4, deviceCode: 'BDC-004', hallName: '区政务服务中心', location: '不动产窗口旁', status: 'fault', modules: { verify: 'fault', print: 'fault', network: 'normal' } },
        { id: 5, deviceCode: 'BDC-005', hallName: '开发区政务中心', location: '一楼自助服务区', status: 'normal', modules: { verify: 'normal', print: 'normal', network: 'normal' } },
        { id: 6, deviceCode: 'BDC-006', hallName: '开发区政务中心', location: '二楼大厅', status: 'normal', modules: { verify: 'normal', print: 'normal', network: 'warning' } },
        { id: 7, deviceCode: 'BDC-007', hallName: '高新区政务中心', location: '北门入口', status: 'warning', modules: { verify: 'normal', print: 'warning', network: 'normal' } },
        { id: 8, deviceCode: 'BDC-008', hallName: '高新区政务中心', location: '办事大厅A区', status: 'normal', modules: { verify: 'normal', print: 'normal', network: 'normal' } },
        { id: 9, deviceCode: 'BDC-009', hallName: '西湖区便民中心', location: '一楼大厅', status: 'fault', modules: { verify: 'fault', print: 'fault', network: 'fault' } },
        { id: 10, deviceCode: 'BDC-010', hallName: '西湖区便民中心', location: '二楼201室旁', status: 'offline', modules: { verify: 'offline', print: 'offline', network: 'offline' } },
        { id: 11, deviceCode: 'BDC-011', hallName: '东湖区政务中心', location: '自助服务区1号', status: 'normal', modules: { verify: 'normal', print: 'normal', network: 'normal' } },
        { id: 12, deviceCode: 'BDC-012', hallName: '东湖区政务中心', location: '自助服务区2号', status: 'warning', modules: { verify: 'normal', print: 'warning', network: 'normal' } },
        { id: 13, deviceCode: 'BDC-013', hallName: '南城区政务中心', location: '大门左侧', status: 'offline', modules: { verify: 'offline', print: 'offline', network: 'offline' } },
        { id: 14, deviceCode: 'BDC-014', hallName: '南城区政务中心', location: '不动产专区', status: 'normal', modules: { verify: 'normal', print: 'normal', network: 'normal' } },
        { id: 15, deviceCode: 'BDC-015', hallName: '北城区便民中心', location: '服务大厅', status: 'fault', modules: { verify: 'normal', print: 'fault', network: 'normal' } },
        { id: 16, deviceCode: 'BDC-016', hallName: '北城区便民中心', location: '咨询台旁', status: 'normal', modules: { verify: 'normal', print: 'normal', network: 'normal' } },
        { id: 17, deviceCode: 'BDC-017', hallName: '江东区服务中心', location: '一楼入口处', status: 'offline', modules: { verify: 'offline', print: 'offline', network: 'offline' } },
        { id: 18, deviceCode: 'BDC-018', hallName: '江东区服务中心', location: '二楼办事大厅', status: 'normal', modules: { verify: 'normal', print: 'warning', network: 'normal' } },
        { id: 19, deviceCode: 'BDC-019', hallName: '河西区政务中心', location: '南门自助区', status: 'fault', modules: { verify: 'fault', print: 'fault', network: 'warning' } },
        { id: 20, deviceCode: 'BDC-020', hallName: '河西区政务中心', location: '北门咨询台', status: 'warning', modules: { verify: 'normal', print: 'normal', network: 'fault' } }
      ]
    },
    tableRowClassName({ row }) {
      if (row.status === 'fault') {
        return 'row-fault'
      } else if (row.status === 'offline') {
        return 'row-offline'
      } else if (row.status === 'warning') {
        return 'row-warning'
      }
      return ''
    },
    loadData() {
      let filteredData = [...this.allDeviceList]
      
      if (this.searchForm.keyword) {
        const keyword = this.searchForm.keyword.toLowerCase()
        filteredData = filteredData.filter(item => 
          item.deviceCode.toLowerCase().includes(keyword) ||
          item.hallName.includes(keyword) ||
          item.location.includes(keyword)
        )
      }
      
      if (this.searchForm.status) {
        filteredData = filteredData.filter(item => 
          item.status === this.searchForm.status
        )
      }
      
      this.pagination.total = filteredData.length
      
      const start = (this.pagination.page - 1) * this.pagination.size
      const end = start + this.pagination.size
      this.tableData = filteredData.slice(start, end)
    },
    handleSearch() {
      this.pagination.page = 1
      this.loadData()
    },
    handleReset() {
      this.searchForm = {
        keyword: '',
        status: ''
      }
      this.pagination.page = 1
      this.loadData()
    },
    handleSizeChange(size) {
      this.pagination.size = size
      this.loadData()
    },
    handleCurrentChange(page) {
      this.pagination.page = page
      this.loadData()
    },
    getStatusClass(status) {
      const classMap = {
        normal: 'status-normal',
        warning: 'status-warning',
        fault: 'status-fault',
        offline: 'status-offline'
      }
      return classMap[status] || ''
    },
    getStatusText(status) {
      const textMap = {
        normal: '正常运行',
        warning: '运行告警',
        fault: '故障停机',
        offline: '离线'
      }
      return textMap[status] || '未知'
    },
    getModuleStatusClass(status) {
      const classMap = {
        normal: 'module-status-normal',
        warning: 'module-status-warning',
        fault: 'module-status-fault',
        offline: 'module-status-offline'
      }
      return classMap[status] || ''
    },
    getModuleStatusText(status) {
      const textMap = {
        normal: '正常',
        warning: '告警',
        fault: '故障',
        offline: '离线'
      }
      return textMap[status] || '未知'
    },
    getModuleIcon(status) {
      const iconMap = {
        normal: 'el-icon-check',
        warning: 'el-icon-warning',
        fault: 'el-icon-close',
        offline: 'el-icon-remove-outline'
      }
      return iconMap[status] || ''
    },
    toggleDeviceStatus(row) {
      const statusList = ['normal', 'warning', 'fault', 'offline']
      const currentIndex = statusList.indexOf(row.status)
      const nextIndex = (currentIndex + 1) % statusList.length
      row.status = statusList[nextIndex]
      
      if (row.status === 'offline') {
        row.modules.verify = 'offline'
        row.modules.print = 'offline'
        row.modules.network = 'offline'
      } else if (row.status === 'fault') {
        row.modules.verify = 'fault'
        row.modules.print = 'fault'
        row.modules.network = Math.random() > 0.5 ? 'fault' : 'warning'
      } else {
        row.modules.verify = Math.random() > 0.3 ? 'normal' : 'warning'
        row.modules.print = Math.random() > 0.3 ? 'normal' : 'warning'
        row.modules.network = Math.random() > 0.3 ? 'normal' : 'warning'
      }
      
      this.$message.info(`${row.deviceCode} 状态已切换为 ${this.getStatusText(row.status)}`)
    },
    deviceFilterMethod(keyword) {
      this.deviceSearchKeyword = keyword
    },
    openReportDialog() {
      this.generateOrderNo()
      this.deviceSearchKeyword = ''
      this.reportDialogVisible = true
    },
    handleReport(row) {
      this.generateOrderNo()
      this.reportForm.deviceId = row.id
      this.deviceSearchKeyword = ''
      this.reportDialogVisible = true
    },
    generateOrderNo() {
      const now = new Date()
      const year = now.getFullYear()
      const month = String(now.getMonth() + 1).padStart(2, '0')
      const day = String(now.getDate()).padStart(2, '0')
      const random = Math.floor(Math.random() * 10000).toString().padStart(4, '0')
      this.reportForm.orderNo = `GZ${year}${month}${day}${random}`
    },
    resetReportForm() {
      this.$refs.reportForm && this.$refs.reportForm.resetFields()
      this.deviceSearchKeyword = ''
      this.reportForm = {
        orderNo: '',
        deviceId: '',
        reporter: '',
        phone: '',
        description: ''
      }
    },
    submitReport() {
      if (!this.reportForm.deviceId) {
        this.$message.warning('请先选择要上报故障的设备！')
        return
      }
      
      this.$refs.reportForm.validate((valid) => {
        if (valid) {
          const selectedDevice = this.allDeviceList.find(d => d.id === this.reportForm.deviceId)
          if (!selectedDevice) {
            this.$message.error('未找到所选设备信息，请重新选择！')
            return
          }
          
          this.submitLoading = true
          setTimeout(() => {
            this.submitLoading = false
            this.$message({
              type: 'success',
              message: `设备 ${selectedDevice.deviceCode} 故障上报成功！工单号：${this.reportForm.orderNo}`,
              duration: 3000
            })
            this.reportDialogVisible = false
          }, 1000)
        }
      })
    }
  }
}
</script>

<style scoped>
.device-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.header {
  text-align: center;
  padding: 20px 0;
  margin-bottom: 20px;
}

.header h1 {
  color: #fff;
  font-size: 28px;
  font-weight: 500;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.content {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.search-bar {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
  flex-wrap: wrap;
  gap: 10px;
}

.table-wrapper {
  margin-bottom: 20px;
}

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  padding-top: 10px;
}

.status-normal {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  background-color: #f0f9eb;
  color: #67c23a;
  font-size: 12px;
}

.status-warning {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  background-color: #fdf6ec;
  color: #e6a23c;
  font-size: 12px;
}

.status-fault {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  background-color: #fef0f0;
  color: #f56c6c;
  font-size: 12px;
}

.status-offline {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  background-color: #f4f4f5;
  color: #909399;
  font-size: 12px;
}

.module-status-normal {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  background-color: #f0f9eb;
  color: #67c23a;
  font-size: 11px;
}

.module-status-normal i {
  margin-right: 2px;
}

.module-status-warning {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  background-color: #fdf6ec;
  color: #e6a23c;
  font-size: 11px;
}

.module-status-warning i {
  margin-right: 2px;
}

.module-status-fault {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  background-color: #fef0f0;
  color: #f56c6c;
  font-size: 11px;
}

.module-status-fault i {
  margin-right: 2px;
}

.module-status-offline {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  background-color: #f4f4f5;
  color: #909399;
  font-size: 11px;
}

.module-status-offline i {
  margin-right: 2px;
}
</style>

<style>
.el-table .row-fault {
  background-color: #fef0f0 !important;
}

.el-table .row-fault:hover > td {
  background-color: #fde2e2 !important;
}

.el-table .row-offline {
  background-color: #f4f4f5 !important;
}

.el-table .row-offline:hover > td {
  background-color: #e9e9eb !important;
}

.el-table .row-warning {
  background-color: #fdf6ec !important;
}

.el-table .row-warning:hover > td {
  background-color: #faecd8 !important;
}
</style>
