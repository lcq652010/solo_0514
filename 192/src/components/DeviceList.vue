<template>
  <div class="device-list-container">
    <div class="header">
      <h1>出入境自助签注打印终端运维管理系统</h1>
    </div>

    <div class="search-bar">
      <el-input
        v-model="searchForm.deviceNo"
        placeholder="请输入设备编号"
        style="width: 200px; margin-right: 10px;"
        clearable
      ></el-input>
      <el-input
        v-model="searchForm.hallName"
        placeholder="请输入大厅名称"
        style="width: 200px; margin-right: 10px;"
        clearable
      ></el-input>
      <el-select
        v-model="searchForm.status"
        placeholder="请选择设备状态"
        style="width: 150px; margin-right: 10px;"
        clearable
      >
        <el-option label="正常运行" value="running"></el-option>
        <el-option label="运行警告" value="warning"></el-option>
        <el-option label="故障停机" value="error"></el-option>
        <el-option label="维护中" value="maintenance"></el-option>
        <el-option label="离线" value="offline"></el-option>
      </el-select>
      <el-button type="primary" @click="handleSearch">搜索</el-button>
      <el-button @click="handleReset">重置</el-button>
      <el-button type="success" @click="openReportDialog" style="margin-left: 20px;">故障上报</el-button>
    </div>

    <el-table
      :data="tableData"
      border
      style="width: 100%; margin-top: 20px;"
      :row-class-name="getRowClassName"
    >
      <el-table-column
        prop="deviceNo"
        label="设备编号"
        width="150"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="hallName"
        label="出入境大厅"
        width="200"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="location"
        label="摆放位置"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="idReaderStatus"
        label="身份读取"
        width="120"
        align="center"
      >
        <template slot-scope="scope">
          <span :class="getModuleStatusClass(scope.row.idReaderStatus)">
            {{ getModuleStatusText(scope.row.idReaderStatus) }}
          </span>
        </template>
      </el-table-column>
      <el-table-column
        prop="printStatus"
        label="签注打印"
        width="120"
        align="center"
      >
        <template slot-scope="scope">
          <span :class="getModuleStatusClass(scope.row.printStatus)">
            {{ getModuleStatusText(scope.row.printStatus) }}
          </span>
        </template>
      </el-table-column>
      <el-table-column
        prop="networkStatus"
        label="联网核验"
        width="120"
        align="center"
      >
        <template slot-scope="scope">
          <span :class="getModuleStatusClass(scope.row.networkStatus)">
            {{ getModuleStatusText(scope.row.networkStatus) }}
          </span>
        </template>
      </el-table-column>
      <el-table-column
        prop="status"
        label="设备运行状态"
        width="150"
        align="center"
      >
        <template slot-scope="scope">
          <span :class="getStatusClass(scope.row.status)">
            {{ getStatusText(scope.row.status) }}
          </span>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        width="150"
        align="center"
      >
        <template slot-scope="scope">
          <el-button
            type="text"
            size="small"
            @click="handleReport(scope.row)"
          >
            故障上报
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
        :total="pagination.total"
        background
      ></el-pagination>
    </div>

    <el-dialog
      title="故障上报"
      :visible.sync="reportDialogVisible"
      width="500px"
      @close="resetReportForm"
    >
      <el-form :model="reportForm" :rules="reportRules" label-width="100px" ref="reportForm">
        <el-form-item label="工单编号">
          <el-input v-model="reportForm.workOrderNo" disabled></el-input>
        </el-form-item>
        <el-form-item label="选择设备" prop="deviceId">
          <el-select v-model="reportForm.deviceId" placeholder="请选择设备" style="width: 100%;">
            <el-option
              v-for="device in allDevices"
              :key="device.id"
              :label="device.deviceNo + ' - ' + device.hallName"
              :value="device.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="故障描述" prop="faultDescription">
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
        <el-button @click="reportDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitReport">提交</el-button>
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
        deviceNo: '',
        hallName: '',
        status: ''
      },
      pagination: {
        page: 1,
        size: 10,
        total: 0
      },
      allDevices: [],
      tableData: [],
      reportDialogVisible: false,
      reportForm: {
        workOrderNo: '',
        deviceId: '',
        faultDescription: ''
      },
      reportRules: {
        deviceId: [
          { required: true, message: '请选择设备', trigger: 'change' }
        ],
        faultDescription: [
          { required: true, message: '请填写故障描述', trigger: 'blur' },
          { min: 5, message: '故障描述至少5个字符', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.initMockData()
    this.loadData()
  },
  methods: {
    initMockData() {
      const halls = ['北京市出入境大厅', '上海市出入境大厅', '广州市出入境大厅', '深圳市出入境大厅', '杭州市出入境大厅']
      const locations = ['一楼大厅入口', '二楼办证区', '三楼等候区', '四楼办事大厅', '地下一层']
      const statuses = ['running', 'warning', 'error', 'maintenance', 'offline']
      const moduleStatuses = ['normal', 'warning', 'fault']
      
      const devices = []
      for (let i = 1; i <= 86; i++) {
        devices.push({
          id: i,
          deviceNo: `EQ${String(i).padStart(4, '0')}`,
          hallName: halls[Math.floor(Math.random() * halls.length)],
          location: locations[Math.floor(Math.random() * locations.length)],
          status: statuses[Math.floor(Math.random() * statuses.length)],
          idReaderStatus: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)],
          printStatus: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)],
          networkStatus: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)]
        })
      }
      this.allDevices = devices
    },
    loadData() {
      let filteredData = [...this.allDevices]
      
      if (this.searchForm.deviceNo) {
        filteredData = filteredData.filter(item => 
          item.deviceNo.toLowerCase().includes(this.searchForm.deviceNo.toLowerCase())
        )
      }
      
      if (this.searchForm.hallName) {
        filteredData = filteredData.filter(item => 
          item.hallName.includes(this.searchForm.hallName)
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
        deviceNo: '',
        hallName: '',
        status: ''
      }
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
    getStatusClass(status) {
      const classMap = {
        running: 'status-running',
        warning: 'status-warning',
        error: 'status-error',
        maintenance: 'status-maintenance',
        offline: 'status-offline'
      }
      return classMap[status] || ''
    },
    getStatusText(status) {
      const textMap = {
        running: '正常运行',
        warning: '运行警告',
        error: '故障停机',
        maintenance: '维护中',
        offline: '离线'
      }
      return textMap[status] || '未知'
    },
    getRowClassName({ row }) {
      if (row.status === 'error' || row.status === 'offline') {
        return 'row-highlight'
      }
      return ''
    },
    getModuleStatusClass(status) {
      const classMap = {
        normal: 'status-running',
        warning: 'status-warning',
        fault: 'status-error'
      }
      return classMap[status] || ''
    },
    getModuleStatusText(status) {
      const textMap = {
        normal: '正常',
        warning: '警告',
        fault: '故障'
      }
      return textMap[status] || '未知'
    },
    generateWorkOrderNo() {
      const now = new Date()
      const year = now.getFullYear()
      const month = String(now.getMonth() + 1).padStart(2, '0')
      const day = String(now.getDate()).padStart(2, '0')
      const hours = String(now.getHours()).padStart(2, '0')
      const minutes = String(now.getMinutes()).padStart(2, '0')
      const seconds = String(now.getSeconds()).padStart(2, '0')
      const random = String(Math.floor(Math.random() * 1000)).padStart(3, '0')
      return `WO${year}${month}${day}${hours}${minutes}${seconds}${random}`
    },
    openReportDialog() {
      this.reportForm.workOrderNo = this.generateWorkOrderNo()
      this.reportDialogVisible = true
    },
    handleReport(row) {
      this.reportForm.workOrderNo = this.generateWorkOrderNo()
      this.reportForm.deviceId = row.id
      this.reportDialogVisible = true
    },
    resetReportForm() {
      this.reportForm = {
        workOrderNo: '',
        deviceId: '',
        faultDescription: ''
      }
      if (this.$refs.reportForm) {
        this.$refs.reportForm.resetFields()
      }
    },
    submitReport() {
      this.$refs.reportForm.validate((valid) => {
        if (valid) {
          this.$message.success(`故障工单 ${this.reportForm.workOrderNo} 提交成功！`)
          this.reportDialogVisible = false
        } else {
          this.$message.warning('请完善表单信息后再提交')
          return false
        }
      })
    }
  }
}
</script>

<style scoped>
.device-list-container {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h1 {
  color: #303133;
  font-size: 24px;
  font-weight: 500;
}

.search-bar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.status-running {
  color: #67C23A;
  font-weight: 500;
}

.status-warning {
  color: #E6A23C;
  font-weight: 500;
}

.status-error {
  color: #F56C6C;
  font-weight: 500;
}

.status-maintenance {
  color: #909399;
  font-weight: 500;
}

.status-offline {
  color: #000000;
  font-weight: 500;
}

::v-deep .el-table .row-highlight {
  background-color: #fef0f0 !important;
}
</style>
