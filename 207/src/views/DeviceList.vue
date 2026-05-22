<template>
  <div class="device-management">
    <div class="header">
      <h1 class="title">教育缴费自助查询打印终端运维管理系统</h1>
    </div>

    <div class="content">
      <el-card class="search-card">
        <el-form :inline="true" :model="searchForm" class="search-form">
          <el-form-item label="设备编号">
            <el-input v-model="searchForm.deviceCode" placeholder="请输入设备编号" clearable></el-input>
          </el-form-item>
          <el-form-item label="网点名称">
            <el-input v-model="searchForm.schoolName" placeholder="请输入网点名称" clearable></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
            <el-button icon="el-icon-refresh" @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <el-card class="table-card">
        <div class="table-header">
          <el-button type="danger" icon="el-icon-warning" @click="openReportDialog">
            故障上报
          </el-button>
        </div>

        <el-table
          :data="tableData"
          border
          style="width: 100%"
          :row-class-name="tableRowClassName"
        >
          <el-table-column prop="deviceCode" label="设备编号" width="180" align="center"></el-table-column>
          <el-table-column prop="schoolName" label="学校网点" align="center"></el-table-column>
          <el-table-column prop="location" label="安装位置" align="center"></el-table-column>
          <el-table-column prop="status" label="设备运行状态" width="150" align="center">
            <template slot-scope="scope">
              <el-tag :type="getStatusType(scope.row.status)" effect="dark">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="lastOnlineTime" label="最后在线时间" width="180" align="center"></el-table-column>
          <el-table-column label="操作" width="120" align="center">
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
            :page-sizes="[10, 20, 50, 100]"
            :page-size="pagination.pageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="pagination.total">
          </el-pagination>
        </div>
      </el-card>
    </div>

    <el-dialog
      title="故障上报"
      :visible.sync="reportDialogVisible"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form :model="reportForm" :rules="reportRules" ref="reportForm" label-width="100px">
        <el-form-item label="工单编号" prop="orderNo">
          <el-input v-model="reportForm.orderNo" readonly></el-input>
        </el-form-item>
        <el-form-item label="选择设备" prop="deviceId">
          <el-select v-model="reportForm.deviceId" placeholder="请选择设备" filterable>
            <el-option
              v-for="device in deviceOptions"
              :key="device.id"
              :label="`${device.deviceCode} - ${device.schoolName}`"
              :value="device.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="设备信息" v-if="selectedDevice">
          <div class="device-info">
            <p><span>设备编号：</span>{{ selectedDevice.deviceCode }}</p>
            <p><span>学校网点：</span>{{ selectedDevice.schoolName }}</p>
            <p><span>安装位置：</span>{{ selectedDevice.location }}</p>
            <p><span>当前状态：</span>
              <el-tag :type="getStatusType(selectedDevice.status)" effect="dark" size="mini">
                {{ getStatusText(selectedDevice.status) }}
              </el-tag>
            </p>
          </div>
        </el-form-item>
        <el-form-item label="异常说明" prop="description">
          <el-input
            v-model="reportForm.description"
            type="textarea"
            :rows="4"
            placeholder="请详细描述设备故障情况"
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
      <span slot="footer" class="dialog-footer">
        <el-button @click="reportDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitReport">确 定</el-button>
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
        deviceCode: '',
        schoolName: ''
      },
      allDevices: [],
      filteredDevices: [],
      tableData: [],
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      reportDialogVisible: false,
      reportForm: {
        orderNo: '',
        deviceId: null,
        description: '',
        reporter: '',
        phone: ''
      },
      reportRules: {
        deviceId: [
          { required: true, message: '请选择设备', trigger: 'change' }
        ],
        description: [
          { required: true, message: '请填写异常说明', trigger: 'blur' },
          { min: 10, message: '异常说明至少10个字符', trigger: 'blur' }
        ],
        reporter: [
          { required: true, message: '请输入上报人姓名', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ]
      },
      deviceOptions: []
    }
  },
  computed: {
    selectedDevice() {
      if (!this.reportForm.deviceId) return null
      return this.allDevices.find(d => d.id === this.reportForm.deviceId)
    }
  },
  watch: {
    'reportForm.deviceId'(newVal) {
      if (newVal) {
        const device = this.allDevices.find(d => d.id === newVal)
        if (device && device.status === 'normal') {
          this.$message.warning('该设备当前运行正常，是否确认上报故障？')
        }
      }
    }
  },
  created() {
    this.initMockData()
  },
  methods: {
    initMockData() {
      const schools = [
        '北京市第一中学', '北京市第二中学', '北京市第三中学',
        '北京市海淀区实验小学', '北京市朝阳区第一小学', '北京市西城区育才学校',
        '上海市第一中学', '上海市浦东新区实验学校', '广州市天河中学',
        '深圳市南山外国语学校', '杭州市第一中学', '南京市金陵中学',
        '成都市第七中学', '武汉市第一中学', '西安市第一中学'
      ]
      const locations = [
        '教学楼一层大厅', '行政楼服务大厅', '图书馆入口',
        '食堂一层', '学生活动中心', '实验楼一层',
        '综合楼服务窗口', '宿舍楼大厅', '体育馆入口'
      ]
      const statuses = ['normal', 'warning', 'offline', 'fault']

      const devices = []
      for (let i = 1; i <= 85; i++) {
        const schoolIndex = Math.floor(Math.random() * schools.length)
        const locationIndex = Math.floor(Math.random() * locations.length)
        const statusIndex = Math.floor(Math.random() * statuses.length)
        
        devices.push({
          id: i,
          deviceCode: `EDU-${String(i).padStart(6, '0')}`,
          schoolName: schools[schoolIndex],
          location: locations[locationIndex],
          status: statuses[statusIndex],
          lastOnlineTime: this.generateRandomTime()
        })
      }

      this.allDevices = devices
      this.filteredDevices = [...devices]
      this.deviceOptions = devices.map(d => ({
        id: d.id,
        deviceCode: d.deviceCode,
        schoolName: d.schoolName
      }))
      this.handleSearch()
    },
    generateRandomTime() {
      const now = new Date()
      const randomDays = Math.floor(Math.random() * 7)
      const randomHours = Math.floor(Math.random() * 24)
      const randomMinutes = Math.floor(Math.random() * 60)
      
      now.setDate(now.getDate() - randomDays)
      now.setHours(now.getHours() - randomHours)
      now.setMinutes(now.getMinutes() - randomMinutes)
      
      const year = now.getFullYear()
      const month = String(now.getMonth() + 1).padStart(2, '0')
      const day = String(now.getDate()).padStart(2, '0')
      const hours = String(now.getHours()).padStart(2, '0')
      const minutes = String(now.getMinutes()).padStart(2, '0')
      const seconds = String(now.getSeconds()).padStart(2, '0')
      
      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
    },
    getStatusType(status) {
      const statusMap = {
        normal: 'success',
        warning: 'warning',
        offline: 'info',
        fault: 'danger'
      }
      return statusMap[status] || 'info'
    },
    getStatusText(status) {
      const statusMap = {
        normal: '运行正常',
        warning: '预警',
        offline: '离线',
        fault: '故障'
      }
      return statusMap[status] || '未知'
    },
    tableRowClassName({ row }) {
      const rowClassMap = {
        normal: 'row-normal',
        warning: 'row-warning',
        offline: 'row-offline',
        fault: 'row-fault'
      }
      return rowClassMap[row.status] || ''
    },
    handleSearch() {
      this.filteredDevices = this.allDevices.filter(device => {
        const matchDeviceCode = !this.searchForm.deviceCode || 
          device.deviceCode.toLowerCase().includes(this.searchForm.deviceCode.toLowerCase())
        const matchSchoolName = !this.searchForm.schoolName || 
          device.schoolName.includes(this.searchForm.schoolName)
        return matchDeviceCode && matchSchoolName
      })
      
      this.pagination.total = this.filteredDevices.length
      this.pagination.currentPage = 1
      this.updateTableData()
    },
    handleReset() {
      this.searchForm.deviceCode = ''
      this.searchForm.schoolName = ''
      this.handleSearch()
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.updateTableData()
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
      this.updateTableData()
    },
    updateTableData() {
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      this.tableData = this.filteredDevices.slice(start, end)
    },
    generateOrderNo() {
      const now = new Date()
      const year = now.getFullYear()
      const month = String(now.getMonth() + 1).padStart(2, '0')
      const day = String(now.getDate()).padStart(2, '0')
      const hours = String(now.getHours()).padStart(2, '0')
      const minutes = String(now.getMinutes()).padStart(2, '0')
      const seconds = String(now.getSeconds()).padStart(2, '0')
      const random = String(Math.floor(Math.random() * 10000)).padStart(4, '0')
      
      return `WO${year}${month}${day}${hours}${minutes}${seconds}${random}`
    },
    openReportDialog() {
      this.reportForm = {
        orderNo: this.generateOrderNo(),
        deviceId: null,
        description: '',
        reporter: '',
        phone: ''
      }
      this.reportDialogVisible = true
      this.$nextTick(() => {
        if (this.$refs.reportForm) {
          this.$refs.reportForm.clearValidate()
        }
      })
    },
    handleReport(row) {
      this.reportForm = {
        orderNo: this.generateOrderNo(),
        deviceId: row.id,
        description: '',
        reporter: '',
        phone: ''
      }
      this.reportDialogVisible = true
      this.$nextTick(() => {
        if (this.$refs.reportForm) {
          this.$refs.reportForm.clearValidate()
        }
      })
    },
    submitReport() {
      this.$refs.reportForm.validate((valid) => {
        if (valid) {
          this.$loading({
            lock: true,
            text: '正在提交...',
            spinner: 'el-icon-loading',
            background: 'rgba(0, 0, 0, 0.7)'
          })

          setTimeout(() => {
            this.$loading().close()
            this.$message.success(`故障上报成功！工单编号：${this.reportForm.orderNo}`)
            this.reportDialogVisible = false
          }, 1500)
        }
      })
    }
  }
}
</script>

<style scoped>
.device-management {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px 40px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.title {
  color: #ffffff;
  font-size: 24px;
  font-weight: 600;
  margin: 0;
}

.content {
  padding: 20px 40px;
}

.search-card {
  margin-bottom: 20px;
  border-radius: 8px;
}

.search-form {
  margin: 0;
}

.table-card {
  border-radius: 8px;
}

.table-header {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.device-info {
  background-color: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
  width: 100%;
}

.device-info p {
  margin: 8px 0;
  font-size: 14px;
  color: #606266;
}

.device-info span {
  color: #909399;
}

::v-deep .el-table .row-normal {
  background-color: #f0f9ff;
}

::v-deep .el-table .row-warning {
  background-color: #fdf6ec;
}

::v-deep .el-table .row-offline {
  background-color: #f4f4f5;
}

::v-deep .el-table .row-fault {
  background-color: #fef0f0;
}

::v-deep .el-table .row-normal:hover > td {
  background-color: #e6f7ff !important;
}

::v-deep .el-table .row-warning:hover > td {
  background-color: #faecd8 !important;
}

::v-deep .el-table .row-offline:hover > td {
  background-color: #e9e9eb !important;
}

::v-deep .el-table .row-fault:hover > td {
  background-color: #fde2e2 !important;
}
</style>
