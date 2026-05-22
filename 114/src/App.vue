<template>
  <div id="app">
    <div class="header">
      <h1>不动产登记中心自助查询打证终端运维管理系统</h1>
    </div>
    
    <div class="container">
      <div class="search-bar">
        <el-input
          v-model="searchForm.deviceCode"
          placeholder="请输入设备编号"
          clearable
          class="search-input"
        ></el-input>
        <el-input
          v-model="searchForm.hallName"
          placeholder="请输入大厅名称"
          clearable
          class="search-input"
        ></el-input>
        <el-select
          v-model="searchForm.status"
          placeholder="设备状态"
          clearable
          class="search-select"
        >
          <el-option label="正常" value="normal"></el-option>
          <el-option label="故障" value="fault"></el-option>
          <el-option label="离线" value="offline"></el-option>
          <el-option label="维护中" value="maintenance"></el-option>
        </el-select>
        <el-button type="primary" @click="handleSearch">搜索</el-button>
        <el-button @click="handleReset">重置</el-button>
        <el-button type="success" @click="openReportDialog">故障上报</el-button>
      </div>

      <el-table
        :data="tableData"
        border
        class="device-table"
        :row-class-name="getTableRowClassName"
      >
        <el-table-column
          prop="deviceCode"
          label="设备编号"
          width="150"
          align="center"
        ></el-table-column>
        <el-table-column
          prop="hallName"
          label="办事大厅"
          width="200"
          align="center"
        ></el-table-column>
        <el-table-column
          prop="location"
          label="摆放位置"
          align="center"
        ></el-table-column>
        <el-table-column
          prop="status"
          label="设备状态"
          width="120"
          align="center"
        >
          <template slot-scope="scope">
            <span :class="getStatusClass(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column
          prop="idCardStatus"
          label="身份证读卡"
          width="130"
          align="center"
        >
          <template slot-scope="scope">
            <span :class="getModuleStatusClass(scope.row.idCardStatus)">
              {{ getModuleStatusText(scope.row.idCardStatus) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column
          prop="printStatus"
          label="证书打印"
          width="130"
          align="center"
        >
          <template slot-scope="scope">
            <span :class="getModuleStatusClass(scope.row.printStatus)">
              {{ getModuleStatusText(scope.row.printStatus) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column
          prop="encryptStatus"
          label="数据加密"
          width="130"
          align="center"
        >
          <template slot-scope="scope">
            <span :class="getModuleStatusClass(scope.row.encryptStatus)">
              {{ getModuleStatusText(scope.row.encryptStatus) }}
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
              @click="quickReport(scope.row)"
              :disabled="scope.row.status === 'maintenance'"
            >
              故障上报
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
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

    <el-dialog
      title="故障上报"
      :visible.sync="reportDialogVisible"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form :model="reportForm" :rules="reportRules" ref="reportForm" label-width="100px">
        <el-form-item label="工单编号">
          <el-input v-model="reportForm.orderNo" disabled></el-input>
        </el-form-item>
        <el-form-item label="选择设备" prop="deviceId">
          <el-select v-model="reportForm.deviceId" placeholder="请选择设备" style="width: 100%">
            <el-option
              v-for="device in deviceList"
              :key="device.id"
              :label="device.deviceCode + ' - ' + device.hallName"
              :value="device.id"
              :disabled="device.status === 'maintenance'"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="故障描述" prop="description">
          <el-input
            type="textarea"
            v-model="reportForm.description"
            :rows="4"
            placeholder="请详细描述故障情况"
            maxlength="500"
            show-word-limit
          ></el-input>
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
  name: 'App',
  data() {
    return {
      searchForm: {
        deviceCode: '',
        hallName: '',
        status: ''
      },
      allDeviceData: [],
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
        description: ''
      },
      reportRules: {
        deviceId: [
          { required: true, message: '请选择设备', trigger: 'change' }
        ],
        description: [
          { required: true, message: '请填写故障描述', trigger: 'blur' },
          { min: 5, message: '故障描述不少于5个字', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    deviceList() {
      return this.allDeviceData.filter(d => d.status !== 'maintenance')
    }
  },
  created() {
    this.initMockData()
  },
  methods: {
    initMockData() {
      const halls = ['市政务服务中心大厅', '区政务服务中心大厅', '不动产登记中心大厅', '城东分中心大厅', '城西分中心大厅']
      const locations = ['一楼进门左侧', '一楼进门右侧', '二楼服务台旁', '三楼等候区', '负一楼大厅']
      const statuses = ['normal', 'normal', 'normal', 'fault', 'offline', 'maintenance']
      const moduleStatuses = ['running', 'running', 'running', 'warning', 'error']
      
      const data = []
      for (let i = 1; i <= 56; i++) {
        const hallIndex = Math.floor(Math.random() * halls.length)
        const locationIndex = Math.floor(Math.random() * locations.length)
        const statusIndex = Math.floor(Math.random() * statuses.length)
        
        data.push({
          id: i,
          deviceCode: `BDCZ-${String(i).padStart(4, '0')}`,
          hallName: halls[hallIndex],
          location: locations[locationIndex],
          status: statuses[statusIndex],
          idCardStatus: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)],
          printStatus: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)],
          encryptStatus: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)]
        })
      }
      this.allDeviceData = data
      this.handleSearch()
    },
    getStatusClass(status) {
      const classMap = {
        normal: 'status-normal',
        fault: 'status-fault',
        offline: 'status-offline',
        maintenance: 'status-maintenance'
      }
      return classMap[status] || 'status-normal'
    },
    getStatusText(status) {
      const textMap = {
        normal: '正常',
        fault: '故障',
        offline: '离线',
        maintenance: '维护中'
      }
      return textMap[status] || '未知'
    },
    getModuleStatusClass(status) {
      const classMap = {
        running: 'module-running',
        warning: 'module-warning',
        error: 'module-error'
      }
      return classMap[status] || 'module-running'
    },
    getModuleStatusText(status) {
      const textMap = {
        running: '运行中',
        warning: '警告',
        error: '异常'
      }
      return textMap[status] || '未知'
    },
    getTableRowClassName({ row }) {
      if (row.status === 'fault') {
        return 'row-fault'
      } else if (row.status === 'offline') {
        return 'row-offline'
      }
      return ''
    },
    handleSearch() {
      let filteredData = [...this.allDeviceData]
      
      if (this.searchForm.deviceCode) {
        filteredData = filteredData.filter(item => 
          item.deviceCode.toLowerCase().includes(this.searchForm.deviceCode.toLowerCase())
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
      this.pagination.currentPage = 1
      this.updateTableData(filteredData)
    },
    handleReset() {
      this.searchForm = {
        deviceCode: '',
        hallName: '',
        status: ''
      }
      this.handleSearch()
    },
    updateTableData(filteredData) {
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      this.tableData = filteredData.slice(start, end)
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.refreshTableData()
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
      this.refreshTableData()
    },
    refreshTableData() {
      let filteredData = [...this.allDeviceData]
      
      if (this.searchForm.deviceCode) {
        filteredData = filteredData.filter(item => 
          item.deviceCode.toLowerCase().includes(this.searchForm.deviceCode.toLowerCase())
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
      this.updateTableData(filteredData)
    },
    generateOrderNo() {
      const date = new Date()
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      const random = String(Math.floor(Math.random() * 10000)).padStart(4, '0')
      return `GZ${year}${month}${day}${random}`
    },
    openReportDialog() {
      this.reportForm = {
        orderNo: this.generateOrderNo(),
        deviceId: '',
        description: ''
      }
      this.$nextTick(() => {
        this.$refs.reportForm.clearValidate()
      })
      this.reportDialogVisible = true
    },
    quickReport(device) {
      this.reportForm = {
        orderNo: this.generateOrderNo(),
        deviceId: device.id,
        description: ''
      }
      this.$nextTick(() => {
        this.$refs.reportForm.clearValidate()
      })
      this.reportDialogVisible = true
    },
    submitReport() {
      this.$refs.reportForm.validate((valid) => {
        if (valid) {
          const device = this.allDeviceData.find(d => d.id === this.reportForm.deviceId)
          if (device) {
            device.status = 'fault'
            device.idCardStatus = 'error'
            device.printStatus = 'error'
            device.encryptStatus = 'error'
          }
          
          this.$message({
            type: 'success',
            message: `工单 ${this.reportForm.orderNo} 提交成功！`
          })
          
          this.reportDialogVisible = false
          this.refreshTableData()
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

#app {
  min-height: 100vh;
  background: #f0f2f5;
}

.header {
  background: linear-gradient(135deg, #1e3a8a, #3b82f6);
  color: white;
  padding: 20px 40px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.header h1 {
  font-size: 24px;
  font-weight: 500;
}

.container {
  padding: 20px 40px;
}

.search-bar {
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.search-input {
  width: 220px;
}

.search-select {
  width: 140px;
}

.device-table {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.status-normal {
  color: #67c23a;
  font-weight: 500;
}

.status-fault {
  color: #f56c6c;
  font-weight: 500;
}

.status-offline {
  color: #909399;
  font-weight: 500;
}

.status-maintenance {
  color: #e6a23c;
  font-weight: 500;
}

.module-running {
  color: #67c23a;
  font-weight: 500;
}

.module-warning {
  color: #e6a23c;
  font-weight: 500;
}

.module-error {
  color: #f56c6c;
  font-weight: 500;
}

.pagination {
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.el-table .row-fault {
  background-color: #fef0f0 !important;
}

.el-table .row-fault:hover > td {
  background-color: #fde2e2 !important;
}

.el-table .row-offline {
  background-color: #f5f7fa !important;
}

.el-table .row-offline:hover > td {
  background-color: #e4e7ed !important;
}
</style>
