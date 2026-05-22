<template>
  <div class="app-container">
    <div class="container">
      <div class="header">
        <h2>车管所自助临牌打印终端运维管理系统</h2>
      </div>

      <div class="search-bar">
        <el-row :gutter="16">
          <el-col :span="5">
            <el-input
              v-model="searchForm.deviceCode"
              placeholder="请输入设备编号"
              clearable
              @input="handleSearch"
              @keyup.enter.native="handleSearch"
            ></el-input>
          </el-col>
          <el-col :span="5">
            <el-input
              v-model="searchForm.branchName"
              placeholder="请输入网点名称"
              clearable
              @input="handleSearch"
              @keyup.enter.native="handleSearch"
            ></el-input>
          </el-col>
          <el-col :span="5">
            <el-select
              v-model="searchForm.status"
              placeholder="设备状态筛选"
              clearable
              @change="handleSearch"
              style="width: 100%"
            >
              <el-option label="在线" value="online"></el-option>
              <el-option label="离线" value="offline"></el-option>
              <el-option label="故障" value="fault"></el-option>
              <el-option label="异常" value="warning"></el-option>
            </el-select>
          </el-col>
          <el-col :span="9">
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="handleReset">重置</el-button>
            <el-button type="success" @click="openFaultDialog">故障上报</el-button>
          </el-col>
        </el-row>
      </div>

      <div class="table-container">
        <el-table
          :data="tableData"
          border
          stripe
          :row-class-name="getRowClassName"
          style="width: 100%"
        >
          <el-table-column
            prop="deviceCode"
            label="设备编号"
            width="180"
          ></el-table-column>
          <el-table-column
            prop="branchName"
            label="车管所网点"
            width="200"
          ></el-table-column>
          <el-table-column
            prop="installArea"
            label="安装区域"
            width="180"
          ></el-table-column>
          <el-table-column
            prop="status"
            label="设备状态"
            width="100"
          >
            <template slot-scope="scope">
              <span :class="getStatusClass(scope.row.status)">
                {{ getStatusText(scope.row.status) }}
              </span>
            </template>
          </el-table-column>
          <el-table-column
            prop="cardReaderStatus"
            label="读卡模块"
            width="100"
          >
            <template slot-scope="scope">
              <span :class="getModuleStatusClass(scope.row.cardReaderStatus)">
                {{ getModuleStatusText(scope.row.cardReaderStatus) }}
              </span>
            </template>
          </el-table-column>
          <el-table-column
            prop="printStatus"
            label="打印模块"
            width="100"
          >
            <template slot-scope="scope">
              <span :class="getModuleStatusClass(scope.row.printStatus)">
                {{ getModuleStatusText(scope.row.printStatus) }}
              </span>
            </template>
          </el-table-column>
          <el-table-column
            prop="networkStatus"
            label="网络模块"
            width="100"
          >
            <template slot-scope="scope">
              <span :class="getModuleStatusClass(scope.row.networkStatus)">
                {{ getModuleStatusText(scope.row.networkStatus) }}
              </span>
            </template>
          </el-table-column>
          <el-table-column
            prop="lastOnlineTime"
            label="最后在线时间"
            width="160"
          ></el-table-column>
          <el-table-column
            label="操作"
            width="150"
          >
            <template slot-scope="scope">
              <el-button
                type="text"
                size="small"
                @click="handleReportFault(scope.row)"
              >
                故障上报
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination-wrapper">
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
    </div>

    <el-dialog
      title="故障上报"
      :visible.sync="faultDialogVisible"
      width="600px"
      @close="resetFaultForm"
    >
      <el-form
        ref="faultForm"
        :model="faultForm"
        :rules="faultRules"
        label-width="100px"
      >
        <el-form-item label="工单编号" prop="orderNo">
          <el-input v-model="faultForm.orderNo" disabled></el-input>
        </el-form-item>
        <el-form-item label="选择设备" prop="deviceId">
          <el-select
            v-model="faultForm.deviceId"
            placeholder="请选择设备"
            style="width: 100%"
            filterable
          >
            <el-option
              v-for="item in deviceOptions"
              :key="item.id"
              :label="`${item.deviceCode} - ${item.branchName}`"
              :value="item.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="设备编号" prop="deviceCode">
          <el-input v-model="faultForm.deviceCode" disabled></el-input>
        </el-form-item>
        <el-form-item label="网点名称" prop="branchName">
          <el-input v-model="faultForm.branchName" disabled></el-input>
        </el-form-item>
        <el-form-item label="问题描述" prop="problemDescription">
          <el-input
            v-model="faultForm.problemDescription"
            type="textarea"
            :rows="4"
            placeholder="请详细描述故障问题"
            maxlength="500"
            show-word-limit
          ></el-input>
        </el-form-item>
        <el-form-item label="上报人" prop="reporter">
          <el-input v-model="faultForm.reporter" placeholder="请输入上报人姓名"></el-input>
        </el-form-item>
        <el-form-item label="联系电话" prop="contactPhone">
          <el-input v-model="faultForm.contactPhone" placeholder="请输入联系电话"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="faultDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitFaultForm">提 交</el-button>
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
      tableData: [],
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      allDevices: [],
      faultDialogVisible: false,
      faultForm: {
        orderNo: '',
        deviceId: '',
        deviceCode: '',
        branchName: '',
        problemDescription: '',
        reporter: '',
        contactPhone: ''
      },
      faultRules: {
        deviceId: [
          { required: true, message: '请选择设备', trigger: 'change' }
        ],
        problemDescription: [
          { required: true, message: '请填写问题描述', trigger: 'blur' },
          { min: 5, message: '问题描述至少5个字符', trigger: 'blur' }
        ],
        reporter: [
          { required: true, message: '请输入上报人姓名', trigger: 'blur' }
        ],
        contactPhone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
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
      const branchNames = [
        '北京市车管所朝阳分所',
        '北京市车管所海淀分所',
        '北京市车管所丰台分所',
        '北京市车管所东城分所',
        '北京市车管所西城分所',
        '上海市车管所浦东分所',
        '上海市车管所徐汇分所',
        '广州市车管所天河分所',
        '深圳市车管所福田分所',
        '杭州市车管所西湖分所'
      ]
      const areas = ['业务大厅', '办证中心', '服务窗口', '自助服务区', '24小时服务点']
      const statuses = ['online', 'offline', 'fault', 'warning']
      const moduleStatuses = ['normal', 'abnormal', 'offline']

      for (let i = 1; i <= 86; i++) {
        this.allDevices.push({
          id: i,
          deviceCode: `LP-${String(i).padStart(4, '0')}`,
          branchName: branchNames[Math.floor(Math.random() * branchNames.length)],
          installArea: areas[Math.floor(Math.random() * areas.length)],
          status: statuses[Math.floor(Math.random() * statuses.length)],
          cardReaderStatus: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)],
          printStatus: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)],
          networkStatus: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)],
          lastOnlineTime: this.generateRandomTime()
        })
      }

      this.deviceOptions = JSON.parse(JSON.stringify(this.allDevices))
      this.loadTableData()
    },
    generateRandomTime() {
      const now = new Date()
      const days = Math.floor(Math.random() * 7)
      const hours = Math.floor(Math.random() * 24)
      now.setDate(now.getDate() - days)
      now.setHours(now.getHours() - hours)
      return now.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      })
    },
    loadTableData() {
      let filteredData = [...this.allDevices]

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

      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      this.tableData = filteredData.slice(start, end)
    },
    handleSearch() {
      this.pagination.currentPage = 1
      this.loadTableData()
    },
    handleReset() {
      this.searchForm = {
        deviceCode: '',
        branchName: '',
        status: ''
      }
      this.pagination.currentPage = 1
      this.loadTableData()
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.loadTableData()
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
      this.loadTableData()
    },
    getStatusClass(status) {
      const classMap = {
        online: 'status-online',
        offline: 'status-offline',
        fault: 'status-fault',
        warning: 'status-warning'
      }
      return classMap[status] || ''
    },
    getStatusText(status) {
      const textMap = {
        online: '在线',
        offline: '离线',
        fault: '故障',
        warning: '异常'
      }
      return textMap[status] || '未知'
    },
    getModuleStatusClass(status) {
      const classMap = {
        normal: 'status-online',
        abnormal: 'status-warning',
        offline: 'status-offline'
      }
      return classMap[status] || ''
    },
    getModuleStatusText(status) {
      const textMap = {
        normal: '正常',
        abnormal: '异常',
        offline: '离线'
      }
      return textMap[status] || '未知'
    },
    getRowClassName({ row }) {
      if (row.status === 'fault') {
        return 'row-fault'
      } else if (row.status === 'warning') {
        return 'row-warning'
      } else if (row.status === 'offline') {
        return 'row-offline'
      }
      return ''
    },
    openFaultDialog() {
      this.generateOrderNo()
      this.faultDialogVisible = true
    },
    handleReportFault(row) {
      this.generateOrderNo()
      this.faultForm.deviceId = row.id
      this.faultForm.deviceCode = row.deviceCode
      this.faultForm.branchName = row.branchName
      this.faultDialogVisible = true
    },
    generateOrderNo() {
      const now = new Date()
      const dateStr = now.getFullYear().toString() +
        String(now.getMonth() + 1).padStart(2, '0') +
        String(now.getDate()).padStart(2, '0')
      const randomStr = String(Math.floor(Math.random() * 10000)).padStart(4, '0')
      this.faultForm.orderNo = `WO${dateStr}${randomStr}`
    },
    resetFaultForm() {
      this.$refs.faultForm.resetFields()
      this.faultForm = {
        orderNo: '',
        deviceId: '',
        deviceCode: '',
        branchName: '',
        problemDescription: '',
        reporter: '',
        contactPhone: ''
      }
    },
    submitFaultForm() {
      this.$refs.faultForm.validate((valid) => {
        if (valid) {
          this.$message({
            type: 'success',
            message: `工单 ${this.faultForm.orderNo} 提交成功！`
          })
          this.faultDialogVisible = false
          this.resetFaultForm()
        }
      })
    }
  },
  watch: {
    'faultForm.deviceId'(newVal) {
      if (newVal) {
        const device = this.allDevices.find(item => item.id === newVal)
        if (device) {
          this.faultForm.deviceCode = device.deviceCode
          this.faultForm.branchName = device.branchName
        }
      }
    }
  }
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.header h2 {
  color: #303133;
  font-size: 24px;
  font-weight: 500;
  margin: 0;
  padding: 10px 0;
}

.pagination-wrapper {
  margin-top: 20px;
  text-align: right;
}
</style>

<style>
.el-table .row-fault {
  background-color: #fef0f0 !important;
}

.el-table .row-fault:hover > td {
  background-color: #fde2e2 !important;
}

.el-table .row-warning {
  background-color: #fdf6ec !important;
}

.el-table .row-warning:hover > td {
  background-color: #faecd8 !important;
}

.el-table .row-offline {
  background-color: #f4f4f5 !important;
}

.el-table .row-offline:hover > td {
  background-color: #e9e9eb !important;
}
</style>
