<template>
  <div class="device-list">
    <el-card>
      <div slot="header" class="card-header">
        <span>设备管理</span>
        <el-button type="primary" @click="openReportDialog">
          <i class="el-icon-warning"></i> 故障上报
        </el-button>
      </div>

      <div class="search-area">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="设备编号">
            <el-input
              v-model="searchForm.deviceCode"
              placeholder="请输入设备编号"
              clearable
              style="width: 200px"
              @input="handleSearch"
            ></el-input>
          </el-form-item>
          <el-form-item label="营业厅名称">
            <el-input
              v-model="searchForm.hallName"
              placeholder="请输入营业厅名称"
              clearable
              style="width: 200px"
              @input="handleSearch"
            ></el-input>
          </el-form-item>
          <el-form-item label="设备状态">
            <el-select
              v-model="searchForm.status"
              placeholder="全部状态"
              clearable
              style="width: 140px"
              @change="handleSearch"
            >
              <el-option label="正常" value="normal"></el-option>
              <el-option label="故障" value="fault"></el-option>
              <el-option label="离线" value="offline"></el-option>
              <el-option label="维护中" value="maintaining"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">
              <i class="el-icon-search"></i> 搜索
            </el-button>
            <el-button @click="handleReset">
              <i class="el-icon-refresh"></i> 重置
            </el-button>
          </el-form-item>
        </el-form>
      </div>

      <el-table
        :data="tableData"
        border
        style="width: 100%"
        v-loading="loading"
        :row-class-name="getRowClassName"
      >
        <el-table-column
          prop="deviceCode"
          label="设备编号"
          width="180"
          align="center"
        ></el-table-column>
        <el-table-column
          prop="hallName"
          label="所属营业厅"
          align="center"
        ></el-table-column>
        <el-table-column
          prop="location"
          label="摆放点位"
          align="center"
        ></el-table-column>
        <el-table-column
          prop="status"
          label="设备状态"
          width="120"
          align="center"
        >
          <template slot-scope="scope">
            <el-tag
              :type="getStatusType(scope.row.status)"
              :effect="'light'"
            >
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="读卡模块"
          width="120"
          align="center"
        >
          <template slot-scope="scope">
            <el-tag
              :type="scope.row.cardReader ? 'success' : 'danger'"
              size="mini"
              :effect="'light'"
            >
              {{ scope.row.cardReader ? '正常' : '异常' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="打印模块"
          width="120"
          align="center"
        >
          <template slot-scope="scope">
            <el-tag
              :type="scope.row.printer ? 'success' : 'danger'"
              size="mini"
              :effect="'light'"
            >
              {{ scope.row.printer ? '正常' : '异常' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="网络通信"
          width="120"
          align="center"
        >
          <template slot-scope="scope">
            <el-tag
              :type="scope.row.network ? 'success' : 'danger'"
              size="mini"
              :effect="'light'"
            >
              {{ scope.row.network ? '正常' : '异常' }}
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
              type="text"
              size="small"
              @click="openReportDialog(scope.row)"
            >
              故障上报
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-area">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.page"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pagination.size"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
        ></el-pagination>
      </div>
    </el-card>

    <el-dialog
      title="故障上报"
      :visible.sync="reportDialogVisible"
      width="500px"
      @close="resetReportForm"
    >
      <el-form
        :model="reportForm"
        :rules="reportRules"
        ref="reportFormRef"
        label-width="100px"
      >
        <el-form-item label="工单号" prop="orderNo">
          <el-input v-model="reportForm.orderNo" disabled></el-input>
        </el-form-item>
        <el-form-item label="选择设备" prop="deviceId">
          <el-select
            v-model="reportForm.deviceId"
            placeholder="请选择设备"
            style="width: 100%"
            filterable
          >
            <el-option
              v-for="device in deviceOptions"
              :key="device.id"
              :label="device.deviceCode + ' - ' + device.hallName"
              :value="device.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="故障详情" prop="faultDesc">
          <el-input
            v-model="reportForm.faultDesc"
            type="textarea"
            :rows="4"
            placeholder="请详细描述故障情况"
            maxlength="500"
            show-word-limit
          ></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="reportDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitReport">提交</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'DeviceList',
  data() {
    return {
      loading: false,
      searchForm: {
        deviceCode: '',
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
        orderNo: '',
        deviceId: '',
        faultDesc: ''
      },
      reportRules: {
        deviceId: [
          { required: true, message: '请选择设备', trigger: 'change' }
        ],
        faultDesc: [
          { required: true, message: '请填写故障详情', trigger: 'blur' },
          { min: 10, message: '故障详情至少10个字符', trigger: 'blur' }
        ]
      },
      deviceOptions: []
    }
  },
  created() {
    this.initMockData()
  },
  methods: {
    initMockData() {
      this.allDevices = [
        { id: 1, deviceCode: 'GAS-001', hallName: '朝阳路营业厅', location: '入口左侧', status: 'normal', cardReader: true, printer: true, network: true },
        { id: 2, deviceCode: 'GAS-002', hallName: '朝阳路营业厅', location: '服务台旁', status: 'fault', cardReader: false, printer: true, network: true },
        { id: 3, deviceCode: 'GAS-003', hallName: '人民路营业厅', location: '大厅中央', status: 'normal', cardReader: true, printer: true, network: true },
        { id: 4, deviceCode: 'GAS-004', hallName: '人民路营业厅', location: '休息区旁', status: 'offline', cardReader: true, printer: true, network: false },
        { id: 5, deviceCode: 'GAS-005', hallName: '建设路营业厅', location: '门口右侧', status: 'maintaining', cardReader: true, printer: false, network: true },
        { id: 6, deviceCode: 'GAS-006', hallName: '建设路营业厅', location: '缴费窗口旁', status: 'normal', cardReader: true, printer: true, network: true },
        { id: 7, deviceCode: 'GAS-007', hallName: '解放路营业厅', location: '大厅入口', status: 'normal', cardReader: true, printer: true, network: true },
        { id: 8, deviceCode: 'GAS-008', hallName: '解放路营业厅', location: '自助服务区', status: 'fault', cardReader: true, printer: false, network: true },
        { id: 9, deviceCode: 'GAS-009', hallName: '和平路营业厅', location: '一楼大厅', status: 'offline', cardReader: true, printer: true, network: false },
        { id: 10, deviceCode: 'GAS-010', hallName: '和平路营业厅', location: '二楼拐角', status: 'normal', cardReader: true, printer: true, network: true },
        { id: 11, deviceCode: 'GAS-011', hallName: '胜利路营业厅', location: '正门左侧', status: 'maintaining', cardReader: false, printer: false, network: true },
        { id: 12, deviceCode: 'GAS-012', hallName: '胜利路营业厅', location: '后门右侧', status: 'normal', cardReader: true, printer: true, network: true },
        { id: 13, deviceCode: 'GAS-013', hallName: '长江路营业厅', location: '服务大厅', status: 'normal', cardReader: true, printer: true, network: true },
        { id: 14, deviceCode: 'GAS-014', hallName: '长江路营业厅', location: 'VIP区旁', status: 'fault', cardReader: false, printer: true, network: true },
        { id: 15, deviceCode: 'GAS-015', hallName: '黄河路营业厅', location: '咨询台旁', status: 'normal', cardReader: true, printer: true, network: true },
        { id: 16, deviceCode: 'GAS-016', hallName: '黄河路营业厅', location: '等候区', status: 'offline', cardReader: true, printer: true, network: false }
      ]
      this.deviceOptions = [...this.allDevices]
      this.loadData()
    },
    loadData() {
      this.loading = true
      setTimeout(() => {
        let filteredData = [...this.allDevices]
        
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
        
        const start = (this.pagination.page - 1) * this.pagination.size
        const end = start + this.pagination.size
        this.tableData = filteredData.slice(start, end)
        
        this.loading = false
      }, 300)
    },
    handleSearch() {
      this.pagination.page = 1
      this.loadData()
    },
    handleReset() {
      this.searchForm = {
        deviceCode: '',
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
    getStatusType(status) {
      const statusMap = {
        normal: 'success',
        fault: 'danger',
        offline: 'info',
        maintaining: 'warning'
      }
      return statusMap[status] || 'info'
    },
    getStatusText(status) {
      const statusMap = {
        normal: '正常',
        fault: '故障',
        offline: '离线',
        maintaining: '维护中'
      }
      return statusMap[status] || '未知'
    },
    getRowClassName({ row }) {
      if (row.status === 'fault') {
        return 'fault-row'
      } else if (row.status === 'offline') {
        return 'offline-row'
      }
      return ''
    },
    generateOrderNo() {
      const date = new Date()
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      const random = Math.floor(Math.random() * 10000).toString().padStart(4, '0')
      return `WO${year}${month}${day}${random}`
    },
    openReportDialog(device = null) {
      this.reportForm.orderNo = this.generateOrderNo()
      if (device) {
        this.reportForm.deviceId = device.id
      }
      this.reportDialogVisible = true
    },
    resetReportForm() {
      this.reportForm = {
        orderNo: '',
        deviceId: '',
        faultDesc: ''
      }
      if (this.$refs.reportFormRef) {
        this.$refs.reportFormRef.resetFields()
      }
    },
    submitReport() {
      if (!this.reportForm.deviceId) {
        this.$message.warning('请选择要上报故障的设备！')
        return
      }
      this.$refs.reportFormRef.validate((valid) => {
        if (valid) {
          this.$message.success('故障上报成功！工单号：' + this.reportForm.orderNo)
          this.reportDialogVisible = false
        } else {
          this.$message.error('请完善表单信息后再提交！')
        }
      })
    }
  }
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
  font-weight: 500;
}

.search-area {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.pagination-area {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>

<style>
.el-table .fault-row {
  background-color: #fef0f0 !important;
}

.el-table .fault-row:hover > td {
  background-color: #fde2e2 !important;
}

.el-table .offline-row {
  background-color: #f4f4f5 !important;
}

.el-table .offline-row:hover > td {
  background-color: #e4e4e7 !important;
}
</style>
