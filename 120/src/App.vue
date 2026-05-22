<template>
  <div id="app">
    <div class="header">
      <h1>公积金中心自助查询打印终端运维管理系统</h1>
    </div>
    
    <div class="container">
      <div class="search-bar">
        <el-input
          v-model="searchForm.deviceCode"
          placeholder="请输入设备编号"
          style="width: 180px; margin-right: 10px;"
          clearable
          @input="handleSearch"
        ></el-input>
        <el-input
          v-model="searchForm.branchName"
          placeholder="请输入网点名称"
          style="width: 180px; margin-right: 10px;"
          clearable
          @input="handleSearch"
        ></el-input>
        <el-select
          v-model="searchForm.status"
          placeholder="设备状态"
          style="width: 120px; margin-right: 10px;"
          clearable
          @change="handleSearch"
        >
          <el-option label="全部" value=""></el-option>
          <el-option label="正常" value="normal"></el-option>
          <el-option label="故障" value="fault"></el-option>
          <el-option label="离线" value="offline"></el-option>
          <el-option label="维护中" value="maintenance"></el-option>
        </el-select>
        <el-button type="primary" @click="handleSearch">搜索</el-button>
        <el-button @click="handleReset">重置</el-button>
        <el-button type="success" @click="openReportDialog" style="margin-left: 20px;">故障上报</el-button>
      </div>

      <el-table :data="tableData" :row-class-name="getRowClassName" border style="width: 100%; margin-top: 20px;">
        <el-table-column prop="deviceCode" label="设备编号" width="120" align="center"></el-table-column>
        <el-table-column prop="branchName" label="公积金网点" width="180" align="center"></el-table-column>
        <el-table-column prop="installLocation" label="安装点位" width="150" align="center"></el-table-column>
        <el-table-column label="设备状态" width="100" align="center">
          <template slot-scope="scope">
            <span :class="getStatusClass(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="身份证读卡" width="110" align="center">
          <template slot-scope="scope">
            <span :class="scope.row.idCardReader ? 'status-normal' : 'status-fault'">
              {{ scope.row.idCardReader ? '正常' : '异常' }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="凭证打印" width="110" align="center">
          <template slot-scope="scope">
            <span :class="scope.row.receiptPrinter ? 'status-normal' : 'status-fault'">
              {{ scope.row.receiptPrinter ? '正常' : '异常' }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="网络通信" width="110" align="center">
          <template slot-scope="scope">
            <span :class="scope.row.network ? 'status-normal' : 'status-fault'">
              {{ scope.row.network ? '正常' : '异常' }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="130" align="center">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="handleReport(scope.row)">上报故障</el-button>
          </template>
        </el-table-column>
      </el-table>

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
      <el-form :model="reportForm" :rules="reportRules" ref="reportForm" label-width="100px">
        <el-form-item label="工单编号">
          <el-input v-model="reportForm.orderNo" disabled></el-input>
        </el-form-item>
        <el-form-item label="选择设备" prop="deviceId">
          <el-select v-model="reportForm.deviceId" placeholder="请选择设备" style="width: 100%;">
            <el-option
              v-for="device in allDevices"
              :key="device.id"
              :label="device.deviceCode + ' - ' + device.branchName"
              :value="device.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="故障描述" prop="faultDescription">
          <el-input
            type="textarea"
            v-model="reportForm.faultDescription"
            :rows="4"
            placeholder="请详细描述故障情况">
          </el-input>
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
        branchName: '',
        status: ''
      },
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      allDevices: [
        { id: 1, deviceCode: 'GJJ-001', branchName: '市公积金中心营业部', installLocation: '一楼大厅入口', status: 'normal', idCardReader: true, receiptPrinter: true, network: true },
        { id: 2, deviceCode: 'GJJ-002', branchName: '市公积金中心营业部', installLocation: '二楼业务区', status: 'fault', idCardReader: false, receiptPrinter: true, network: true },
        { id: 3, deviceCode: 'GJJ-003', branchName: '朝阳区公积金管理部', installLocation: '服务大厅左侧', status: 'normal', idCardReader: true, receiptPrinter: true, network: true },
        { id: 4, deviceCode: 'GJJ-004', branchName: '海淀区公积金管理部', installLocation: '自助服务区', status: 'offline', idCardReader: true, receiptPrinter: true, network: false },
        { id: 5, deviceCode: 'GJJ-005', branchName: '东城区公积金管理部', installLocation: '大厅咨询台旁', status: 'maintenance', idCardReader: true, receiptPrinter: false, network: true },
        { id: 6, deviceCode: 'GJJ-006', branchName: '西城区公积金管理部', installLocation: '一楼大堂', status: 'normal', idCardReader: true, receiptPrinter: true, network: true },
        { id: 7, deviceCode: 'GJJ-007', branchName: '丰台区公积金管理部', installLocation: '业务办理区', status: 'normal', idCardReader: true, receiptPrinter: true, network: true },
        { id: 8, deviceCode: 'GJJ-008', branchName: '通州区公积金管理部', installLocation: '服务中心入口', status: 'fault', idCardReader: true, receiptPrinter: false, network: true },
        { id: 9, deviceCode: 'GJJ-009', branchName: '顺义区公积金管理部', installLocation: '二楼自助区', status: 'normal', idCardReader: true, receiptPrinter: true, network: true },
        { id: 10, deviceCode: 'GJJ-010', branchName: '昌平区公积金管理部', installLocation: '大厅左侧', status: 'offline', idCardReader: true, receiptPrinter: true, network: false },
        { id: 11, deviceCode: 'GJJ-011', branchName: '大兴区公积金管理部', installLocation: '服务窗口旁', status: 'normal', idCardReader: true, receiptPrinter: true, network: true },
        { id: 12, deviceCode: 'GJJ-012', branchName: '房山区公积金管理部', installLocation: '一楼大厅', status: 'maintenance', idCardReader: false, receiptPrinter: true, network: true },
        { id: 13, deviceCode: 'GJJ-013', branchName: '石景山区公积金管理部', installLocation: '自助服务区', status: 'normal', idCardReader: true, receiptPrinter: true, network: true },
        { id: 14, deviceCode: 'GJJ-014', branchName: '门头沟区公积金管理部', installLocation: '业务大厅', status: 'normal', idCardReader: true, receiptPrinter: true, network: true },
        { id: 15, deviceCode: 'GJJ-015', branchName: '平谷区公积金管理部', installLocation: '一楼入口处', status: 'fault', idCardReader: false, receiptPrinter: false, network: true }
      ],
      reportDialogVisible: false,
      reportForm: {
        orderNo: '',
        deviceId: '',
        faultDescription: ''
      },
      reportRules: {
        deviceId: [
          { required: true, message: '请选择设备', trigger: 'change' }
        ],
        faultDescription: [
          { required: true, message: '请输入故障描述', trigger: 'blur' },
          { min: 5, message: '故障描述至少5个字符', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    filteredDevices() {
      let result = [...this.allDevices]
      
      if (this.searchForm.deviceCode) {
        result = result.filter(item => 
          item.deviceCode.toLowerCase().includes(this.searchForm.deviceCode.toLowerCase())
        )
      }
      
      if (this.searchForm.branchName) {
        result = result.filter(item => 
          item.branchName.includes(this.searchForm.branchName)
        )
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
  mounted() {
    this.pagination.total = this.allDevices.length
  },
  methods: {
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
        normal: '正常',
        fault: '故障',
        offline: '离线',
        maintenance: '维护中'
      }
      return textMap[status] || status
    },
    getRowClassName({ row }) {
      if (row.status === 'fault') {
        return 'row-fault'
      } else if (row.status === 'offline') {
        return 'row-offline'
      }
      return ''
    },
    handleSearch() {
      this.pagination.currentPage = 1
      this.pagination.total = this.filteredDevices.length
    },
    handleReset() {
      this.searchForm.deviceCode = ''
      this.searchForm.branchName = ''
      this.searchForm.status = ''
      this.pagination.currentPage = 1
      this.pagination.total = this.allDevices.length
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
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
      this.$refs.reportForm.resetFields()
      this.reportForm.orderNo = ''
      this.reportForm.deviceId = ''
      this.reportForm.faultDescription = ''
    },
    submitReport() {
      this.$refs.reportForm.validate((valid) => {
        if (valid) {
          const device = this.allDevices.find(d => d.id === this.reportForm.deviceId)
          this.$message.success(`故障上报成功！工单编号：${this.reportForm.orderNo}，设备：${device.deviceCode}`)
          this.reportDialogVisible = false
          this.resetReportForm()
        }
      })
    }
  },
  watch: {
    filteredDevices: {
      handler(val) {
        this.pagination.total = val.length
      },
      immediate: true
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

body {
  font-family: "Microsoft YaHei", sans-serif;
  background-color: #f5f7fa;
}

#app {
  min-height: 100vh;
}

.header {
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  color: white;
  padding: 20px 40px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.header h1 {
  font-size: 24px;
  font-weight: 500;
}

.container {
  padding: 30px;
  max-width: 1400px;
  margin: 0 auto;
}

.search-bar {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.pagination {
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

.status-maintenance {
  color: #e6a23c;
  font-weight: 500;
}
.row-fault {
  background-color: #fef0f0 !important;
}
.row-offline {
  background-color: #f5f7fa !important;
}
</style>
