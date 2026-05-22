<template>
  <div id="app">
    <div class="container">
      <header class="header">
        <h1>影院自助终端运维管理系统</h1>
      </header>

      <div class="search-bar">
        <el-input
          v-model="searchForm.keyword"
          placeholder="请输入关键字（设备编号/影院名称/摆放区域）"
          style="width: 280px; margin-right: 10px;"
          clearable
          @keyup.enter.native="handleSearch"
        ></el-input>
        <el-select
          v-model="searchForm.status"
          placeholder="设备状态"
          style="width: 140px; margin-right: 10px;"
          clearable
        >
          <el-option label="全部状态" value=""></el-option>
          <el-option label="运行中" value="online"></el-option>
          <el-option label="离线" value="offline"></el-option>
          <el-option label="故障" value="fault"></el-option>
          <el-option label="维护中" value="maintenance"></el-option>
        </el-select>
        <el-button type="primary" @click="handleSearch" icon="el-icon-search">搜索</el-button>
        <el-button @click="handleReset" icon="el-icon-refresh">重置</el-button>
        <el-button type="success" @click="openReportDialog" style="margin-left: 20px;" icon="el-icon-edit">
          故障上报
        </el-button>
      </div>

      <div class="table-container">
        <el-table 
          :data="tableData" 
          border 
          style="width: 100%"
          :row-class-name="getRowClassName"
        >
          <el-table-column prop="deviceNo" label="设备编号" width="130" align="center"></el-table-column>
          <el-table-column prop="cinemaName" label="影院门店" width="160" align="center"></el-table-column>
          <el-table-column prop="location" label="摆放区域" width="130" align="center"></el-table-column>
          <el-table-column prop="status" label="设备状态" width="100" align="center">
            <template slot-scope="scope">
              <el-tag :type="getStatusType(scope.row.status)" :effect="getStatusEffect(scope.row.status)" size="small">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="idCardStatus" label="身份读取" width="100" align="center">
            <template slot-scope="scope">
              <el-tag :type="getModuleStatusType(scope.row.idCardStatus)" size="mini">
                {{ getModuleStatusText(scope.row.idCardStatus) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="printStatus" label="票据打印" width="100" align="center">
            <template slot-scope="scope">
              <el-tag :type="getModuleStatusType(scope.row.printStatus)" size="mini">
                {{ getModuleStatusText(scope.row.printStatus) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="payStatus" label="支付交互" width="100" align="center">
            <template slot-scope="scope">
              <el-tag :type="getModuleStatusType(scope.row.payStatus)" size="mini">
                {{ getModuleStatusText(scope.row.payStatus) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="130" align="center">
            <template slot-scope="scope">
              <el-button size="small" type="primary" @click="handleReport(scope.row)">
                上报故障
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div class="pagination-container">
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
      @close="resetReportForm"
    >
      <el-form :model="reportForm" :rules="reportRules" ref="reportForm" label-width="100px">
        <el-form-item label="工单编号" prop="orderNo">
          <el-input v-model="reportForm.orderNo" disabled></el-input>
        </el-form-item>
        <el-form-item label="选择设备" prop="deviceId">
          <el-select 
            v-model="reportForm.deviceId" 
            placeholder="请选择设备" 
            style="width: 100%;"
            filterable
            clearable
          >
            <el-option
              v-for="device in allDevices"
              :key="device.id"
              :label="`${device.deviceNo} - ${device.cinemaName} (${device.location})`"
              :value="device.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="故障类型" prop="faultType">
          <el-select v-model="reportForm.faultType" placeholder="请选择故障类型" style="width: 100%;">
            <el-option label="硬件故障" value="hardware"></el-option>
            <el-option label="软件故障" value="software"></el-option>
            <el-option label="网络故障" value="network"></el-option>
            <el-option label="打印故障" value="printer"></el-option>
            <el-option label="其他故障" value="other"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="故障描述" prop="description">
          <el-input
            type="textarea"
            v-model="reportForm.description"
            :rows="4"
            placeholder="请详细描述故障情况（至少10个字符）"
            maxlength="500"
            show-word-limit
          ></el-input>
        </el-form-item>
        <el-form-item label="上报人" prop="reporter">
          <el-input v-model="reportForm.reporter" placeholder="请输入上报人姓名"></el-input>
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="reportForm.phone" placeholder="请输入联系电话"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="reportDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitReport">确 定</el-button>
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
        status: ''
      },
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      allDevices: [],
      filteredDevices: [],
      tableData: [],
      reportDialogVisible: false,
      reportForm: {
        orderNo: '',
        deviceId: '',
        faultType: '',
        description: '',
        reporter: '',
        phone: ''
      },
      reportRules: {
        deviceId: [
          { required: true, message: '请选择设备', trigger: 'change' }
        ],
        faultType: [
          { required: true, message: '请选择故障类型', trigger: 'change' }
        ],
        description: [
          { required: true, message: '请填写故障描述', trigger: 'blur' },
          { min: 10, message: '故障描述至少10个字符', trigger: 'blur' }
        ],
        reporter: [
          { required: true, message: '请输入上报人姓名', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.initData()
  },
  methods: {
    initData() {
      const cinemas = ['万达影城', 'CGV影城', '金逸影城', '中影国际影城', '博纳国际影城']
      const locations = ['一楼大厅', '二楼入口', '三楼等候区', '负一层取票区', 'VIP厅入口']
      const statuses = ['online', 'offline', 'fault', 'maintenance']
      const moduleStatuses = ['normal', 'warning', 'error']
      
      this.allDevices = []
      for (let i = 1; i <= 86; i++) {
        this.allDevices.push({
          id: i,
          deviceNo: `DEV${String(i).padStart(4, '0')}`,
          cinemaName: cinemas[Math.floor(Math.random() * cinemas.length)],
          location: locations[Math.floor(Math.random() * locations.length)],
          status: statuses[Math.floor(Math.random() * statuses.length)],
          idCardStatus: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)],
          printStatus: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)],
          payStatus: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)]
        })
      }
      
      this.filteredDevices = [...this.allDevices]
      this.pagination.total = this.allDevices.length
      this.loadPageData()
    },
    getStatusType(status) {
      const typeMap = {
        online: 'success',
        offline: 'info',
        fault: 'danger',
        maintenance: 'warning'
      }
      return typeMap[status] || 'info'
    },
    getStatusEffect(status) {
      return status === 'online' ? 'light' : 'dark'
    },
    getStatusText(status) {
      const textMap = {
        online: '运行中',
        offline: '离线',
        fault: '故障',
        maintenance: '维护中'
      }
      return textMap[status] || '未知'
    },
    getModuleStatusType(status) {
      const typeMap = {
        normal: 'success',
        warning: 'warning',
        error: 'danger'
      }
      return typeMap[status] || 'info'
    },
    getModuleStatusText(status) {
      const textMap = {
        normal: '正常',
        warning: '警告',
        error: '异常'
      }
      return textMap[status] || '未知'
    },
    getRowClassName({ row }) {
      if (row.status === 'fault') {
        return 'row-fault'
      } else if (row.status === 'offline') {
        return 'row-offline'
      } else if (row.status === 'maintenance') {
        return 'row-maintenance'
      }
      return ''
    },
    handleSearch() {
      this.filteredDevices = [...this.allDevices]
      
      if (this.searchForm.keyword.trim()) {
        const keyword = this.searchForm.keyword.toLowerCase().trim()
        this.filteredDevices = this.filteredDevices.filter(item => 
          item.deviceNo.toLowerCase().includes(keyword) ||
          item.cinemaName.includes(keyword) ||
          item.location.includes(keyword) ||
          this.getStatusText(item.status).includes(keyword)
        )
      }
      
      if (this.searchForm.status) {
        this.filteredDevices = this.filteredDevices.filter(item => 
          item.status === this.searchForm.status
        )
      }
      
      this.pagination.total = this.filteredDevices.length
      this.pagination.currentPage = 1
      this.loadPageData()
    },
    handleReset() {
      this.searchForm = {
        keyword: '',
        status: ''
      }
      this.handleSearch()
    },
    loadPageData() {
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      this.tableData = this.filteredDevices.slice(start, end)
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.pagination.currentPage = 1
      this.loadPageData()
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
      this.loadPageData()
    },
    openReportDialog() {
      this.generateOrderNo()
      this.reportDialogVisible = true
    },
    handleReport(row) {
      this.generateOrderNo()
      this.reportForm.deviceId = row.id
      this.reportDialogVisible = true
    },
    generateOrderNo() {
      const date = new Date()
      const dateStr = date.getFullYear().toString() + 
        String(date.getMonth() + 1).padStart(2, '0') +
        String(date.getDate()).padStart(2, '0')
      const random = Math.floor(Math.random() * 10000).toString().padStart(4, '0')
      this.reportForm.orderNo = `WO${dateStr}${random}`
    },
    resetReportForm() {
      this.reportForm = {
        orderNo: '',
        deviceId: '',
        faultType: '',
        description: '',
        reporter: '',
        phone: ''
      }
      this.$refs.reportForm && this.$refs.reportForm.clearValidate()
    },
    submitReport() {
      if (!this.reportForm.deviceId) {
        this.$message.warning('请选择需要上报故障的设备！')
        return
      }
      
      this.$refs.reportForm.validate((valid) => {
        if (valid) {
          const device = this.allDevices.find(d => d.id === this.reportForm.deviceId)
          if (device) {
            device.status = 'fault'
            this.handleSearch()
          }
          this.$message.success('故障上报成功！工单编号：' + this.reportForm.orderNo)
          this.reportDialogVisible = false
        }
      })
    }
  }
}
</script>

<style>
#app {
  font-family: 'Microsoft YaHei', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  text-align: center;
  padding: 20px 0;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  color: white;
}

.header h1 {
  margin: 0;
  font-size: 28px;
  font-weight: 500;
}

.search-bar {
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.table-container {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 20px;
}

.pagination-container {
  background: white;
  padding: 20px;
  border-radius: 8px;
  text-align: right;
}

.dialog-footer {
  text-align: center;
}

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
  background-color: #e4e4e7 !important;
}

.el-table .row-maintenance {
  background-color: #fdf6ec !important;
}

.el-table .row-maintenance:hover > td {
  background-color: #faecd8 !important;
}
</style>
