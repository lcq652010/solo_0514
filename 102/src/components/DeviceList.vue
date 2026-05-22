<template>
  <div class="device-list-container">
    <div class="header">
      <h1>车管所自助违章处理终端运维管理系统</h1>
      <el-button type="primary" @click="openFaultReport" icon="el-icon-warning">故障上报</el-button>
    </div>

    <div class="search-bar">
      <el-input 
        v-model="searchForm.deviceCode" 
        placeholder="请输入设备编号" 
        clearable 
        style="width: 220px; margin-right: 15px;"
        @keyup.enter.native="handleSearch"
      >
        <i slot="prefix" class="el-input__icon el-icon-search"></i>
      </el-input>
      <el-input 
        v-model="searchForm.branchName" 
        placeholder="请输入网点名称" 
        clearable 
        style="width: 220px; margin-right: 15px;"
        @keyup.enter.native="handleSearch"
      >
        <i slot="prefix" class="el-input__icon el-icon-office-building"></i>
      </el-input>
      <el-select 
        v-model="searchForm.status" 
        placeholder="设备状态" 
        clearable 
        style="width: 150px; margin-right: 15px;"
        @change="handleSearch"
      >
        <el-option label="正常" value="正常" />
        <el-option label="故障" value="故障" />
        <el-option label="离线" value="离线" />
        <el-option label="维护中" value="维护中" />
      </el-select>
      <el-button type="primary" @click="handleSearch" icon="el-icon-search">查询</el-button>
      <el-button @click="handleReset" style="margin-left: 10px;" icon="el-icon-refresh">重置</el-button>
    </div>

    <div class="table-container">
      <el-table 
        :data="tableData" 
        border 
        style="width: 100%"
        :header-cell-style="{ background: '#f5f7fa', color: '#606266', fontWeight: 'bold' }"
        :row-class-name="getRowClassName"
      >
        <el-table-column prop="deviceCode" label="设备编号" width="180" align="center" />
        <el-table-column prop="branchName" label="车管所网点" width="200" align="center" />
        <el-table-column prop="area" label="放置区域" align="center" />
        <el-table-column prop="status" label="设备状态" width="120" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="medium">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="cardReaderStatus" label="读卡模块" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getModuleStatusType(scope.row.cardReaderStatus)" size="small">
              {{ scope.row.cardReaderStatus }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="printerStatus" label="打印模块" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getModuleStatusType(scope.row.printerStatus)" size="small">
              {{ scope.row.printerStatus }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="networkStatus" label="网络模块" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getModuleStatusType(scope.row.networkStatus)" size="small">
              {{ scope.row.networkStatus }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" align="center">
          <template slot-scope="scope">
            <el-button 
              type="text" 
              size="small" 
              @click="handleQuickReport(scope.row)"
              :disabled="scope.row.status === '正常'"
            >
              故障上报
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
        :page-sizes="[5, 10, 20, 50]"
        :page-size="pagination.pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="pagination.total"
      >
      </el-pagination>
    </div>

    <FaultReportModal 
      ref="faultReportModal" 
      :device-list="deviceList"
      @submit="handleFaultSubmit"
    />
  </div>
</template>

<script>
import FaultReportModal from './FaultReportModal.vue'

export default {
  name: 'DeviceList',
  components: {
    FaultReportModal
  },
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
      allDeviceList: [],
      tableData: [],
      deviceList: []
    }
  },
  created() {
    this.mockData()
  },
  methods: {
    mockData() {
      const branchNames = [
        '北京市公安局交通管理局车管所',
        '上海市公安局交通警察总队车管所',
        '广州市公安局交通警察支队车管所',
        '深圳市公安局交通警察局车管所',
        '杭州市公安局交通警察支队车管所',
        '成都市公安局交通管理局车管所'
      ]
      const areas = ['业务大厅', '自助服务区', '24小时自助终端区', '门口服务区']
      const statuses = ['正常', '故障', '离线', '维护中']
      const moduleStatuses = ['正常', '异常']

      for (let i = 1; i <= 35; i++) {
        this.allDeviceList.push({
          id: i,
          deviceCode: `CZ-${String(i).padStart(4, '0')}`,
          branchName: branchNames[Math.floor(Math.random() * branchNames.length)],
          area: areas[Math.floor(Math.random() * areas.length)],
          status: statuses[Math.floor(Math.random() * statuses.length)],
          cardReaderStatus: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)],
          printerStatus: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)],
          networkStatus: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)]
        })
      }
      
      this.deviceList = this.allDeviceList
      this.handleSearch()
    },
    getRowClassName({ row }) {
      if (row.status === '故障') {
        return 'error-row'
      } else if (row.status === '离线') {
        return 'offline-row'
      }
      return ''
    },
    getStatusType(status) {
      const statusMap = {
        '正常': 'success',
        '故障': 'danger',
        '离线': 'info',
        '维护中': 'warning'
      }
      return statusMap[status] || 'info'
    },
    getModuleStatusType(status) {
      return status === '正常' ? 'success' : 'danger'
    },
    handleSearch() {
      let filteredData = [...this.allDeviceList]
      
      if (this.searchForm.deviceCode) {
        filteredData = filteredData.filter(item => 
          item.deviceCode.toLowerCase().includes(this.searchForm.deviceCode.toLowerCase())
        )
      }
      
      if (this.searchForm.branchName) {
        filteredData = filteredData.filter(item => 
          item.branchName.includes(this.searchForm.branchName)
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
    handleReset() {
      this.searchForm = {
        deviceCode: '',
        branchName: '',
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
      this.pagination.currentPage = 1
      this.handleSearch()
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
      this.handleSearch()
    },
    openFaultReport() {
      this.$refs.faultReportModal.open()
    },
    handleQuickReport(row) {
      this.$refs.faultReportModal.open(row)
    },
    handleFaultSubmit(data) {
      if (!data.deviceId) {
        this.$message.error('请选择故障设备')
        return
      }

      const workOrderNo = this.generateWorkOrderNo()
      
      const deviceIndex = this.allDeviceList.findIndex(d => d.id === data.deviceId)
      if (deviceIndex > -1) {
        this.$set(this.allDeviceList, deviceIndex, {
          ...this.allDeviceList[deviceIndex],
          status: '故障'
        })
      }
      
      this.handleSearch()
      
      this.$message({
        type: 'success',
        message: `工单 ${workOrderNo} 提交成功，已通知运维人员`
      })
    },
    generateWorkOrderNo() {
      const now = new Date()
      const year = now.getFullYear()
      const month = String(now.getMonth() + 1).padStart(2, '0')
      const day = String(now.getDate()).padStart(2, '0')
      const random = String(Math.floor(Math.random() * 10000)).padStart(4, '0')
      return `GD${year}${month}${day}${random}`
    }
  }
}
</script>

<style scoped>
.device-list-container {
  max-width: 1200px;
  margin: 0 auto;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 24px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid #e4e7ed;
}

.header h1 {
  font-size: 24px;
  color: #303133;
  font-weight: 600;
}

.search-bar {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.table-container {
  margin-bottom: 20px;
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  padding-top: 16px;
}

::v-deep .el-table .error-row {
  background-color: #fef0f0 !important;
}

::v-deep .el-table .offline-row {
  background-color: #f4f4f5 !important;
}

::v-deep .el-table .error-row:hover > td {
  background-color: #fde2e2 !important;
}

::v-deep .el-table .offline-row:hover > td {
  background-color: #e9e9eb !important;
}
</style>
