<template>
  <div class="device-list-container">
    <div class="header">
      <h1>电力自助缴费打票终端运维管理系统</h1>
    </div>

    <div class="content">
      <div class="search-bar">
        <el-input
          v-model="searchForm.deviceCode"
          placeholder="请输入设备编号"
          clearable
          class="search-input"
          @keyup.enter.native="handleSearch"
        >
          <i slot="prefix" class="el-input__icon el-icon-search"></i>
        </el-input>
        <el-input
          v-model="searchForm.hallName"
          placeholder="请输入营业厅名称"
          clearable
          class="search-input"
          @keyup.enter.native="handleSearch"
        >
          <i slot="prefix" class="el-input__icon el-icon-office-building"></i>
        </el-input>
        <el-select
          v-model="searchForm.status"
          placeholder="设备状态"
          clearable
          class="status-select"
          @change="handleSearch"
        >
          <el-option label="全部状态" value=""></el-option>
          <el-option label="正常运行" value="normal"></el-option>
          <el-option label="故障" value="fault"></el-option>
          <el-option label="离线" value="offline"></el-option>
          <el-option label="维护中" value="maintenance"></el-option>
        </el-select>
        <el-button type="primary" @click="handleSearch" class="search-btn">
          <i class="el-icon-search"></i> 搜索
        </el-button>
        <el-button @click="handleReset" class="reset-btn">
          <i class="el-icon-refresh"></i> 重置
        </el-button>
      </div>

      <div class="table-container">
        <el-table
          ref="table"
          :data="tableData"
          border
          style="width: 100%"
          class="device-table"
          :row-class-name="getTableRowClassName"
          @selection-change="handleSelectionChange"
        >
          <el-table-column
            type="selection"
            width="55"
            align="center"
          >
          </el-table-column>
          <el-table-column
            prop="deviceCode"
            label="设备编号"
            width="150"
            align="center"
          >
          </el-table-column>
          <el-table-column
            prop="hallName"
            label="供电营业厅"
            min-width="150"
            align="center"
          >
          </el-table-column>
          <el-table-column
            prop="installLocation"
            label="安装点位"
            min-width="200"
            align="center"
          >
          </el-table-column>
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
            label="读卡模块"
            width="110"
            align="center"
          >
            <template slot-scope="scope">
              <el-tag :type="getModuleStatusType(scope.row.cardReader)" size="small">
                {{ getModuleStatusText(scope.row.cardReader) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column
            label="票据打印"
            width="110"
            align="center"
          >
            <template slot-scope="scope">
              <el-tag :type="getModuleStatusType(scope.row.printer)" size="small">
                {{ getModuleStatusText(scope.row.printer) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column
            label="网络通信"
            width="110"
            align="center"
          >
            <template slot-scope="scope">
              <el-tag :type="getModuleStatusType(scope.row.network)" size="small">
                {{ getModuleStatusText(scope.row.network) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column
            label="操作"
            width="150"
            align="center"
          >
            <template slot-scope="scope">
              <el-button
                type="danger"
                size="small"
                @click="openFaultReport(scope.row)"
              >
                <i class="el-icon-warning"></i> 故障上报
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div class="pagination-container">
        <el-button
          type="primary"
          @click="batchFaultReport"
          :disabled="selectedDevices.length === 0"
          class="batch-btn"
        >
          <i class="el-icon-warning"></i> 批量故障上报
        </el-button>
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.pageNum"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pagination.pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
          class="pagination"
        >
        </el-pagination>
      </div>
    </div>

    <fault-report-dialog
      :visible.sync="faultDialogVisible"
      :selected-devices="selectedDevices"
      @submit="handleFaultSubmit"
      @close="faultDialogVisible = false"
    >
    </fault-report-dialog>
  </div>
</template>

<script>
import FaultReportDialog from '@/components/FaultReportDialog.vue'

export default {
  name: 'DeviceList',
  components: {
    FaultReportDialog
  },
  data() {
    return {
      searchForm: {
        deviceCode: '',
        hallName: '',
        keyword: '',
        status: ''
      },
      allDeviceData: [],
      filteredData: [],
      tableData: [],
      selectedDevices: [],
      pagination: {
        pageNum: 1,
        pageSize: 10,
        total: 0
      },
      faultDialogVisible: false
    }
  },
  created() {
    this.initDeviceData()
  },
  methods: {
    initDeviceData() {
      this.allDeviceData = this.generateMockData()
      this.filteredData = [...this.allDeviceData]
      this.updateTableData()
    },
    getTableRowClassName({ row }) {
      if (row.status === 'fault') {
        return 'row-fault'
      } else if (row.status === 'offline') {
        return 'row-offline'
      } else if (row.status === 'maintenance') {
        return 'row-maintenance'
      }
      return ''
    },
    generateMockData() {
      const halls = [
        '朝阳供电营业厅', '海淀供电营业厅', '东城供电营业厅',
        '西城供电营业厅', '丰台供电营业厅', '石景山供电营业厅',
        '通州供电营业厅', '顺义供电营业厅', '昌平供电营业厅',
        '大兴供电营业厅'
      ]
      const locations = [
        '一楼大厅入口处', '二楼服务区左侧', '营业厅正门右侧',
        '自助服务区A区', '自助服务区B区', '缴费窗口旁',
        '客户休息区旁', '营业厅后门入口', '停车场入口处',
        '营业厅中心区域'
      ]
      const statuses = ['normal', 'normal', 'normal', 'fault', 'offline', 'maintenance']
      const moduleStatuses = ['normal', 'normal', 'normal', 'normal', 'warning', 'error']

      const data = []
      for (let i = 1; i <= 86; i++) {
        data.push({
          id: i,
          deviceCode: `PWR-${String(i).padStart(5, '0')}`,
          hallName: halls[Math.floor(Math.random() * halls.length)],
          installLocation: locations[Math.floor(Math.random() * locations.length)],
          status: statuses[Math.floor(Math.random() * statuses.length)],
          cardReader: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)],
          printer: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)],
          network: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)]
        })
      }
      return data
    },
    getStatusClass(status) {
      const classMap = {
        normal: 'status-normal',
        fault: 'status-fault',
        offline: 'status-offline',
        maintenance: 'status-maintenance'
      }
      return classMap[status] || ''
    },
    getStatusText(status) {
      const textMap = {
        normal: '正常运行',
        fault: '故障',
        offline: '离线',
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
        warning: '异常',
        error: '故障'
      }
      return textMap[status] || '未知'
    },
    handleSearch() {
      this.filteredData = this.allDeviceData.filter(item => {
        const keyword = (this.searchForm.keyword || '').toLowerCase().trim()
        const deviceCode = (this.searchForm.deviceCode || '').toLowerCase().trim()
        const hallName = (this.searchForm.hallName || '').trim()
        const status = this.searchForm.status

        const matchKeyword = !keyword || 
          item.deviceCode.toLowerCase().includes(keyword) ||
          item.hallName.includes(keyword) ||
          item.installLocation.includes(keyword)

        const matchDeviceCode = !deviceCode || 
          item.deviceCode.toLowerCase().includes(deviceCode)

        const matchHallName = !hallName || 
          item.hallName.includes(hallName)

        const matchStatus = !status || item.status === status

        return matchKeyword && matchDeviceCode && matchHallName && matchStatus
      })

      this.pagination.total = this.filteredData.length
      this.pagination.pageNum = 1
      this.updateTableData()
    },
    handleReset() {
      this.searchForm = {
        deviceCode: '',
        hallName: '',
        keyword: '',
        status: ''
      }
      this.filteredData = [...this.allDeviceData]
      this.pagination.pageNum = 1
      this.pagination.total = this.filteredData.length
      this.updateTableData()
    },
    updateTableData() {
      const start = (this.pagination.pageNum - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      this.tableData = this.filteredData.slice(start, end)
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.pagination.pageNum = 1
      this.updateTableData()
    },
    handleCurrentChange(val) {
      this.pagination.pageNum = val
      this.updateTableData()
    },
    handleSelectionChange(selection) {
      this.selectedDevices = selection
    },
    openFaultReport(row) {
      this.selectedDevices = [row]
      this.faultDialogVisible = true
    },
    batchFaultReport() {
      if (this.selectedDevices.length === 0) {
        this.$message.warning('请至少选择一台设备进行故障上报！')
        return
      }
      this.faultDialogVisible = true
    },
    handleFaultSubmit(data) {
      console.log('故障上报数据:', data)
      this.$message({
        type: 'success',
        message: `工单 ${data.workOrderNo} 提交成功！`
      })
      this.faultDialogVisible = false
      this.selectedDevices = []
      this.$refs.table && this.$refs.table.clearSelection()
    }
  }
}
</script>

<style scoped>
.device-list-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}
.header {
  text-align: center;
  padding: 20px 0;
}
.header h1 {
  color: #fff;
  font-size: 28px;
  font-weight: 600;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}
.content {
  background: #fff;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}
.search-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}
.search-input {
  width: 240px;
}
.status-select {
  width: 140px;
}
.search-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
}
.reset-btn {
  border-color: #dcdfe6;
}
.table-container {
  margin-bottom: 20px;
}
.device-table >>> .el-table__header th {
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
  font-weight: 600;
}
.device-table >>> .el-table__row:hover {
  background-color: #f0f9ff !important;
}
.device-table >>> .el-table__row.row-fault {
  background-color: #fef0f0 !important;
}
.device-table >>> .el-table__row.row-fault:hover {
  background-color: #fde2e2 !important;
}
.device-table >>> .el-table__row.row-offline {
  background-color: #f5f7fa !important;
}
.device-table >>> .el-table__row.row-offline:hover {
  background-color: #e4e7ed !important;
}
.device-table >>> .el-table__row.row-maintenance {
  background-color: #fdf6ec !important;
}
.device-table >>> .el-table__row.row-maintenance:hover {
  background-color: #faecd8 !important;
}
.pagination-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 10px;
}
.batch-btn {
  background: linear-gradient(135deg, #f56c6c 0%, #e64340 100%);
  border: none;
}
.pagination {
  text-align: right;
}
</style>
