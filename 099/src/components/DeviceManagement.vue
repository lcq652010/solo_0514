<template>
  <div class="device-management">
    <div class="header">
      <h1>驾校自助体检拍照终端运维管理系统</h1>
    </div>
    
    <div class="content">
      <div class="search-bar">
        <el-input
          v-model="searchForm.deviceCode"
          placeholder="请输入设备编号"
          style="width: 200px; margin-right: 10px;"
          clearable
        ></el-input>
        <el-input
          v-model="searchForm.networkName"
          placeholder="请输入网点名称"
          style="width: 200px; margin-right: 10px;"
          clearable
        ></el-input>
        <el-button type="primary" @click="handleSearch">搜索</el-button>
        <el-button @click="handleReset">重置</el-button>
        <el-button type="success" @click="openReportDialog" style="margin-left: 20px;">故障上报</el-button>
      </div>

      <div class="table-container">
        <el-table :data="tableData" border style="width: 100%">
          <el-table-column prop="deviceCode" label="设备编号" width="150" align="center"></el-table-column>
          <el-table-column prop="networkName" label="服务网点" width="200" align="center"></el-table-column>
          <el-table-column prop="installLocation" label="安装位置" align="center"></el-table-column>
          <el-table-column prop="status" label="设备状态" width="120" align="center">
            <template slot-scope="scope">
              <span :class="getStatusClass(scope.row.status)">
                {{ getStatusText(scope.row.status) }}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150" align="center">
            <template slot-scope="scope">
              <el-button size="small" type="primary" @click="handleReport(scope.row)">上报故障</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div class="pagination">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.currentPage"
          :page-sizes="[5, 10, 20, 50]"
          :page-size="pagination.pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total">
        </el-pagination>
      </div>
    </div>

    <el-dialog
      title="故障上报"
      :visible.sync="reportDialogVisible"
      width="500px"
      @close="resetReportForm"
    >
      <el-form :model="reportForm" label-width="100px" ref="reportForm">
        <el-form-item label="工单编号">
          <el-input v-model="reportForm.orderNo" disabled></el-input>
        </el-form-item>
        <el-form-item label="选择设备" prop="deviceId">
          <el-select v-model="reportForm.deviceId" placeholder="请选择设备" style="width: 100%;">
            <el-option
              v-for="device in allDevices"
              :key="device.id"
              :label="`${device.deviceCode} - ${device.networkName}`"
              :value="device.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="故障描述" prop="faultDescription">
          <el-input
            type="textarea"
            v-model="reportForm.faultDescription"
            placeholder="请详细描述故障情况"
            :rows="4"
            maxlength="200"
            show-word-limit>
          </el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="reportDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitReport">确 定</el-button>
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
        networkName: ''
      },
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      allDevices: [],
      tableData: [],
      reportDialogVisible: false,
      reportForm: {
        orderNo: '',
        deviceId: '',
        faultDescription: ''
      },
      mockDevices: [
        { id: 1, deviceCode: 'TZJ-001', networkName: '朝阳驾校', installLocation: '一楼大厅', status: 'normal' },
        { id: 2, deviceCode: 'TZJ-002', networkName: '海淀驾校', installLocation: '二楼报名处', status: 'fault' },
        { id: 3, deviceCode: 'TZJ-003', networkName: '西城驾校', installLocation: '主楼一层', status: 'offline' },
        { id: 4, deviceCode: 'TZJ-004', networkName: '东城驾校', installLocation: '体检中心', status: 'maintaining' },
        { id: 5, deviceCode: 'TZJ-005', networkName: '丰台驾校', installLocation: '南门入口', status: 'normal' },
        { id: 6, deviceCode: 'TZJ-006', networkName: '石景山驾校', installLocation: '办公楼一层', status: 'normal' },
        { id: 7, deviceCode: 'TZJ-007', networkName: '通州驾校', installLocation: '服务大厅', status: 'fault' },
        { id: 8, deviceCode: 'TZJ-008', networkName: '昌平驾校', installLocation: '驾校入口', status: 'normal' },
        { id: 9, deviceCode: 'TZJ-009', networkName: '大兴驾校', installLocation: '综合楼一层', status: 'offline' },
        { id: 10, deviceCode: 'TZJ-010', networkName: '顺义驾校', installLocation: '报名大厅', status: 'maintaining' },
        { id: 11, deviceCode: 'TZJ-011', networkName: '房山驾校', installLocation: '主楼大厅', status: 'normal' },
        { id: 12, deviceCode: 'TZJ-012', networkName: '门头沟驾校', installLocation: '服务中心', status: 'normal' },
        { id: 13, deviceCode: 'TZJ-013', networkName: '怀柔驾校', installLocation: '体检区', status: 'fault' },
        { id: 14, deviceCode: 'TZJ-014', networkName: '平谷驾校', installLocation: '报名处', status: 'normal' },
        { id: 15, deviceCode: 'TZJ-015', networkName: '密云驾校', installLocation: '大厅左侧', status: 'offline' },
        { id: 16, deviceCode: 'TZJ-016', networkName: '延庆驾校', installLocation: '办公楼大厅', status: 'normal' },
        { id: 17, deviceCode: 'TZJ-017', networkName: '朝阳驾校二部', installLocation: '西区大厅', status: 'maintaining' },
        { id: 18, deviceCode: 'TZJ-018', networkName: '海淀驾校二部', installLocation: '东区一层', status: 'normal' },
        { id: 19, deviceCode: 'TZJ-019', networkName: '西城驾校二部', installLocation: '南区入口', status: 'normal' },
        { id: 20, deviceCode: 'TZJ-020', networkName: '东城驾校二部', installLocation: '北区服务台', status: 'fault' }
      ]
    }
  },
  created() {
    this.allDevices = [...this.mockDevices]
    this.loadData()
  },
  methods: {
    loadData() {
      let filteredData = [...this.mockDevices]
      
      if (this.searchForm.deviceCode) {
        filteredData = filteredData.filter(item => 
          item.deviceCode.toLowerCase().includes(this.searchForm.deviceCode.toLowerCase())
        )
      }
      
      if (this.searchForm.networkName) {
        filteredData = filteredData.filter(item => 
          item.networkName.toLowerCase().includes(this.searchForm.networkName.toLowerCase())
        )
      }
      
      this.pagination.total = filteredData.length
      
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      this.tableData = filteredData.slice(start, end)
    },
    handleSearch() {
      this.pagination.currentPage = 1
      this.loadData()
    },
    handleReset() {
      this.searchForm.deviceCode = ''
      this.searchForm.networkName = ''
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
    getStatusClass(status) {
      const statusMap = {
        'normal': 'status-normal',
        'fault': 'status-fault',
        'offline': 'status-offline',
        'maintaining': 'status-maintaining'
      }
      return statusMap[status] || ''
    },
    getStatusText(status) {
      const statusMap = {
        'normal': '正常',
        'fault': '故障',
        'offline': '离线',
        'maintaining': '维护中'
      }
      return statusMap[status] || status
    },
    generateOrderNo() {
      const date = new Date()
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      const hours = String(date.getHours()).padStart(2, '0')
      const minutes = String(date.getMinutes()).padStart(2, '0')
      const seconds = String(date.getSeconds()).padStart(2, '0')
      const random = String(Math.floor(Math.random() * 1000)).padStart(3, '0')
      return `GZ${year}${month}${day}${hours}${minutes}${seconds}${random}`
    },
    openReportDialog() {
      this.reportForm.orderNo = this.generateOrderNo()
      this.reportDialogVisible = true
    },
    handleReport(row) {
      this.reportForm.orderNo = this.generateOrderNo()
      this.reportForm.deviceId = row.id
      this.reportDialogVisible = true
    },
    resetReportForm() {
      this.reportForm = {
        orderNo: '',
        deviceId: '',
        faultDescription: ''
      }
    },
    submitReport() {
      if (!this.reportForm.deviceId) {
        this.$message.warning('请选择设备')
        return
      }
      if (!this.reportForm.faultDescription || this.reportForm.faultDescription.trim() === '') {
        this.$message.warning('请填写故障描述')
        return
      }
      
      this.$message.success(`工单 ${this.reportForm.orderNo} 提交成功！`)
      this.reportDialogVisible = false
      this.resetReportForm()
    }
  }
}
</script>

<style scoped>
.device-management {
  width: 100%;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.header {
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  padding: 20px 40px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.header h1 {
  color: #fff;
  font-size: 24px;
  font-weight: 500;
  margin: 0;
}

.content {
  padding: 20px 40px;
}

.search-bar {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.08);
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.table-container {
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.pagination {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.08);
  margin-top: 20px;
  text-align: right;
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

.status-maintaining {
  color: #e6a23c;
  font-weight: 500;
}
</style>