<template>
  <div class="app-container">
    <div class="header">
      <h1>海关自助申报打印终端运维管理系统</h1>
      <div class="stats">
        <el-tag type="success">正常：{{ normalCount }}</el-tag>
        <el-tag type="danger">故障：{{ faultCount }}</el-tag>
        <el-tag type="info">离线：{{ offlineCount }}</el-tag>
        <el-tag type="warning">维护中：{{ maintenanceCount }}</el-tag>
      </div>
    </div>

    <div class="content">
      <div class="search-bar">
        <el-input
          v-model="searchForm.deviceCode"
          placeholder="设备编号"
          style="width: 200px"
          clearable
          @input="handleSearch"
        ></el-input>
        <el-input
          v-model="searchForm.portHall"
          placeholder="口岸名称"
          style="width: 200px; margin-left: 15px"
          clearable
          @input="handleSearch"
        ></el-input>
        <el-select
          v-model="searchForm.status"
          placeholder="设备状态"
          style="width: 150px; margin-left: 15px"
          clearable
          @change="handleSearch"
        >
          <el-option label="全部" value=""></el-option>
          <el-option label="正常" value="normal"></el-option>
          <el-option label="故障" value="fault"></el-option>
          <el-option label="离线" value="offline"></el-option>
          <el-option label="维护中" value="maintenance"></el-option>
        </el-select>
        <el-button type="primary" @click="handleSearch" style="margin-left: 15px">
          <i class="el-icon-search"></i>搜索
        </el-button>
        <el-button @click="handleReset" style="margin-left: 10px">
          <i class="el-icon-refresh"></i>重置
        </el-button>
        <el-button type="danger" @click="openReportDialog" style="margin-left: 20px">
          <i class="el-icon-warning"></i>故障上报
        </el-button>
      </div>

      <el-table
        :data="tableData"
        border
        style="width: 100%; margin-top: 20px"
        v-loading="loading"
        :row-class-name="tableRowClassName"
      >
        <el-table-column type="index" label="序号" width="80" align="center"></el-table-column>
        <el-table-column prop="deviceCode" label="设备编号" min-width="150" align="center"></el-table-column>
        <el-table-column prop="portHall" label="所属口岸大厅" min-width="180" align="center"></el-table-column>
        <el-table-column prop="location" label="布设位置" min-width="200" align="center"></el-table-column>
        <el-table-column prop="statusText" label="设备状态" width="120" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusTagType(scope.row.status)" size="small">
              {{ scope.row.statusText }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="身份证读卡" width="130" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusTagType(scope.row.idCardReader)" size="mini">
              {{ getModuleStatusText(scope.row.idCardReader) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="报关单打印" width="130" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusTagType(scope.row.customsDeclarationPrint)" size="mini">
              {{ getModuleStatusText(scope.row.customsDeclarationPrint) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="加密联网" width="130" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusTagType(scope.row.encryptionNetwork)" size="mini">
              {{ getModuleStatusText(scope.row.encryptionNetwork) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" align="center">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="handleReport(scope.row)">
              故障上报
            </el-button>
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
        ></el-pagination>
      </div>
    </div>

    <el-dialog
      title="故障上报"
      :visible.sync="reportDialogVisible"
      width="500px"
      @close="resetReportForm"
    >
      <el-form :model="reportForm" :rules="reportRules" ref="reportFormRef" label-width="100px">
        <el-form-item label="工单编号">
          <el-input v-model="reportForm.workOrderNo" disabled></el-input>
        </el-form-item>
        <el-form-item label="选择设备" prop="deviceId">
          <el-select v-model="reportForm.deviceId" placeholder="请选择设备" style="width: 100%">
            <el-option
              v-for="item in allDeviceList"
              :key="item.id"
              :label="item.deviceCode + ' - ' + item.portHall"
              :value="item.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="故障描述" prop="faultDescription">
          <el-input
            type="textarea"
            v-model="reportForm.faultDescription"
            placeholder="请详细描述故障情况"
            :rows="4"
            maxlength="200"
            show-word-limit
          ></el-input>
        </el-form-item>
        <el-form-item label="上报时间">
          <el-input v-model="reportForm.reportTime" disabled></el-input>
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
import { deviceList, statusMap } from './mock/data'

export default {
  name: 'App',
  data() {
    return {
      loading: false,
      allDeviceList: [],
      filteredData: [],
      tableData: [],
      statusMap: statusMap,
      searchForm: {
        deviceCode: '',
        portHall: '',
        status: ''
      },
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      reportDialogVisible: false,
      reportForm: {
        workOrderNo: '',
        deviceId: '',
        faultDescription: '',
        reportTime: ''
      },
      reportRules: {
        deviceId: [
          { required: true, message: '请选择设备', trigger: 'change' }
        ],
        faultDescription: [
          { required: true, message: '请填写故障描述', trigger: 'blur' },
          { min: 5, message: '故障描述至少5个字符', trigger: 'blur' }
        ]
      },
      workOrderCounter: 1
    }
  },
  computed: {
    normalCount() {
      return this.allDeviceList.filter(item => item.status === 'normal').length
    },
    faultCount() {
      return this.allDeviceList.filter(item => item.status === 'fault').length
    },
    offlineCount() {
      return this.allDeviceList.filter(item => item.status === 'offline').length
    },
    maintenanceCount() {
      return this.allDeviceList.filter(item => item.status === 'maintenance').length
    }
  },
  created() {
    this.initData()
  },
  methods: {
    initData() {
      this.loading = true
      setTimeout(() => {
        this.allDeviceList = deviceList
        this.handleSearch()
        this.loading = false
      }, 500)
    },
    tableRowClassName({ row, rowIndex }) {
      if (row.status === 'fault') {
        return 'fault-row'
      } else if (row.status === 'offline') {
        return 'offline-row'
      }
      return ''
    },
    getStatusTagType(status) {
      const typeMap = {
        normal: 'success',
        fault: 'danger',
        offline: 'info',
        maintenance: 'warning'
      }
      return typeMap[status] || 'info'
    },
    getModuleStatusText(status) {
      const textMap = {
        normal: '正常',
        fault: '故障',
        offline: '离线',
        maintenance: '维护中'
      }
      return textMap[status] || '未知'
    },
    handleSearch() {
      this.loading = true
      setTimeout(() => {
        let filteredData = [...this.allDeviceList]
        
        if (this.searchForm.deviceCode) {
          filteredData = filteredData.filter(item => 
            item.deviceCode.toLowerCase().includes(this.searchForm.deviceCode.toLowerCase())
          )
        }
        
        if (this.searchForm.portHall) {
          filteredData = filteredData.filter(item => 
            item.portHall.includes(this.searchForm.portHall)
          )
        }
        
        if (this.searchForm.status) {
          filteredData = filteredData.filter(item => 
            item.status === this.searchForm.status
          )
        }
        
        this.filteredData = filteredData
        this.pagination.total = filteredData.length
        this.updateTableData()
        this.loading = false
      }, 100)
    },
    handleReset() {
      this.searchForm.deviceCode = ''
      this.searchForm.portHall = ''
      this.searchForm.status = ''
      this.pagination.currentPage = 1
      this.handleSearch()
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
      this.loading = true
      setTimeout(() => {
        this.pagination.currentPage = val
        this.updateTableData()
        this.loading = false
      }, 100)
    },
    openReportDialog() {
      this.reportDialogVisible = true
      this.generateWorkOrderNo()
      this.reportForm.reportTime = this.getCurrentTime()
    },
    handleReport(row) {
      this.reportDialogVisible = true
      this.generateWorkOrderNo()
      this.reportForm.deviceId = row.id
      this.reportForm.reportTime = this.getCurrentTime()
    },
    generateWorkOrderNo() {
      const date = new Date()
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      const counter = String(this.workOrderCounter).padStart(4, '0')
      this.reportForm.workOrderNo = `WO${year}${month}${day}${counter}`
      this.workOrderCounter++
    },
    getCurrentTime() {
      const date = new Date()
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      const hour = String(date.getHours()).padStart(2, '0')
      const minute = String(date.getMinutes()).padStart(2, '0')
      const second = String(date.getSeconds()).padStart(2, '0')
      return `${year}-${month}-${day} ${hour}:${minute}:${second}`
    },
    resetReportForm() {
      this.$refs.reportFormRef.resetFields()
      this.reportForm.workOrderNo = ''
      this.reportForm.faultDescription = ''
      this.reportForm.reportTime = ''
    },
    submitReport() {
      if (!this.reportForm.deviceId) {
        this.$message.error('请选择设备！')
        return
      }
      this.$refs.reportFormRef.validate((valid) => {
        if (valid) {
          const device = this.allDeviceList.find(item => item.id === this.reportForm.deviceId)
          this.$message.success(`工单 ${this.reportForm.workOrderNo} 提交成功！设备：${device.deviceCode}`)
          this.reportDialogVisible = false
        } else {
          this.$message.error('请完善表单信息！')
        }
      })
    }
  }
}
</script>

<style>
.app-container {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 20px;
}

.el-table .fault-row {
  background-color: #fef0f0 !important;
}

.el-table .fault-row:hover > td {
  background-color: #fde2e2 !important;
}

.el-table .offline-row {
  background-color: #f5f7fa !important;
}

.el-table .offline-row:hover > td {
  background-color: #e4e7ed !important;
}

.header {
  background: linear-gradient(135deg, #409EFF 0%, #66b1ff 100%);
  color: white;
  padding: 25px 30px;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.header h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 500;
}

.stats {
  display: flex;
  gap: 10px;
}

.stats .el-tag {
  font-size: 14px;
  padding: 8px 15px;
}

.content {
  background-color: white;
  border-radius: 8px;
  padding: 25px;
  margin-top: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.search-bar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>
