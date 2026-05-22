<template>
  <div class="app-container">
    <div class="header">
      <h1>法院自助阅卷打印终端运维管理系统</h1>
    </div>
    
    <div class="content">
      <div class="search-bar">
        <el-input
          v-model="searchForm.deviceNo"
          placeholder="请输入设备编号"
          style="width: 200px; margin-right: 10px;"
          clearable
        ></el-input>
        <el-input
          v-model="searchForm.serviceCenter"
          placeholder="请输入诉讼服务中心名称"
          style="width: 250px; margin-right: 10px;"
          clearable
        ></el-input>
        <el-select
          v-model="searchForm.status"
          placeholder="请选择设备状态"
          style="width: 150px; margin-right: 10px;"
          clearable
        >
          <el-option label="正常" value="normal"></el-option>
          <el-option label="故障" value="fault"></el-option>
          <el-option label="离线" value="offline"></el-option>
          <el-option label="维护中" value="maintenance"></el-option>
        </el-select>
        <el-button type="primary" @click="handleSearch">搜索</el-button>
        <el-button @click="handleReset">重置</el-button>
        <el-button type="success" @click="openReportDialog" style="margin-left: 20px;">故障上报</el-button>
      </div>
      
      <el-table :data="tableData" border stripe style="width: 100%; margin-top: 20px;" :row-class-name="tableRowClassName">
        <el-table-column prop="deviceNo" label="设备编号" width="120"></el-table-column>
        <el-table-column prop="serviceCenter" label="诉讼服务中心" width="200"></el-table-column>
        <el-table-column prop="location" label="摆放位置" width="130"></el-table-column>
        <el-table-column prop="status" label="设备状态" width="100">
          <template slot-scope="scope">
            <span :class="getStatusClass(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="idCardStatus" label="身份证读卡" width="110">
          <template slot-scope="scope">
            <span :class="getModuleStatusClass(scope.row.idCardStatus)">
              {{ getModuleStatusText(scope.row.idCardStatus) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="printStatus" label="卷宗打印" width="110">
          <template slot-scope="scope">
            <span :class="getModuleStatusClass(scope.row.printStatus)">
              {{ getModuleStatusText(scope.row.printStatus) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="securityStatus" label="安全加密" width="110">
          <template slot-scope="scope">
            <span :class="getModuleStatusClass(scope.row.securityStatus)">
              {{ getModuleStatusText(scope.row.securityStatus) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template slot-scope="scope">
            <el-button size="mini" type="text" @click="handleReport(scope.row)">故障上报</el-button>
            <el-button size="mini" type="text" @click="handleView(scope.row)">查看详情</el-button>
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
              :label="`${device.deviceNo} - ${device.serviceCenter}`"
              :value="device.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="故障描述" prop="description">
          <el-input
            type="textarea"
            v-model="reportForm.description"
            placeholder="请详细描述故障情况"
            :rows="4"
            maxlength="500"
            show-word-limit
          ></el-input>
        </el-form-item>
        <el-form-item label="上报人">
          <el-input v-model="reportForm.reporter" placeholder="请输入上报人姓名"></el-input>
        </el-form-item>
        <el-form-item label="联系电话">
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
  name: 'App',
  data() {
    return {
      searchForm: {
        deviceNo: '',
        serviceCenter: '',
        status: ''
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
        description: '',
        reporter: '',
        phone: ''
      },
      reportRules: {
        deviceId: [
          { required: true, message: '请选择设备', trigger: 'change' }
        ],
        description: [
          { required: true, message: '请输入故障描述', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.initData()
  },
  methods: {
    initData() {
      const serviceCenters = [
        '北京市朝阳区人民法院诉讼服务中心',
        '北京市海淀区人民法院诉讼服务中心',
        '上海市浦东新区人民法院诉讼服务中心',
        '广州市天河区人民法院诉讼服务中心',
        '深圳市南山区人民法院诉讼服务中心'
      ]
      
      const locations = [
        '一楼大厅左侧',
        '二楼服务窗口旁',
        '三楼自助服务区',
        '立案大厅入口',
        '信访接待区'
      ]
      
      const statuses = ['normal', 'fault', 'offline', 'maintenance']
      const moduleStatuses = ['running', 'warning', 'stopped']
      
      this.allDevices = []
      for (let i = 1; i <= 56; i++) {
        this.allDevices.push({
          id: i,
          deviceNo: `YJ-${String(i).padStart(4, '0')}`,
          serviceCenter: serviceCenters[Math.floor(Math.random() * serviceCenters.length)],
          location: locations[Math.floor(Math.random() * locations.length)],
          status: statuses[Math.floor(Math.random() * statuses.length)],
          idCardStatus: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)],
          printStatus: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)],
          securityStatus: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)]
        })
      }
      
      this.pagination.total = this.allDevices.length
      this.loadTableData()
    },
    
    loadTableData() {
      let filteredData = [...this.allDevices]
      
      if (this.searchForm.deviceNo) {
        filteredData = filteredData.filter(item => 
          item.deviceNo.toLowerCase().includes(this.searchForm.deviceNo.toLowerCase())
        )
      }
      
      if (this.searchForm.serviceCenter) {
        filteredData = filteredData.filter(item => 
          item.serviceCenter.includes(this.searchForm.serviceCenter)
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
        deviceNo: '',
        serviceCenter: '',
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
      const map = {
        normal: 'status-normal',
        fault: 'status-fault',
        offline: 'status-offline',
        maintenance: 'status-maintenance'
      }
      return map[status] || ''
    },
    
    getStatusText(status) {
      const map = {
        normal: '正常',
        fault: '故障',
        offline: '离线',
        maintenance: '维护中'
      }
      return map[status] || status
    },
    
    getModuleStatusClass(status) {
      const map = {
        running: 'module-running',
        warning: 'module-warning',
        stopped: 'module-stopped'
      }
      return map[status] || ''
    },
    
    getModuleStatusText(status) {
      const map = {
        running: '运行中',
        warning: '警告',
        stopped: '停止'
      }
      return map[status] || status
    },
    
    generateOrderNo() {
      const date = new Date()
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      const random = Math.floor(Math.random() * 10000).toString().padStart(4, '0')
      return `GZ${year}${month}${day}${random}`
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
    
    handleView(row) {
      this.$message.info(`查看设备 ${row.deviceNo} 详情`)
    },
    
    resetReportForm() {
      this.$refs.reportForm.resetFields()
      this.reportForm = {
        orderNo: '',
        deviceId: '',
        description: '',
        reporter: '',
        phone: ''
      }
    },
    
    submitReport() {
      this.$refs.reportForm.validate((valid) => {
        if (valid) {
          const device = this.allDevices.find(d => d.id === this.reportForm.deviceId)
          this.$message.success(`工单 ${this.reportForm.orderNo} 提交成功！设备：${device.deviceNo}`)
          this.reportDialogVisible = false
        }
      })
    },
    
    tableRowClassName({ row }) {
      if (row.status === 'fault') {
        return 'row-fault'
      } else if (row.status === 'offline') {
        return 'row-offline'
      }
      return ''
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
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
  background-color: #f5f7fa;
}

.app-container {
  min-height: 100vh;
  padding: 20px;
}

.header {
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  color: white;
  padding: 20px 30px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px rgba(64, 158, 255, 0.3);
}

.header h1 {
  font-size: 24px;
  font-weight: 500;
}

.content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.search-bar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px 0;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
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

.module-stopped {
  color: #f56c6c;
  font-weight: 500;
}

.dialog-footer {
  text-align: right;
}

.el-table .row-fault {
  background-color: #fef0f0 !important;
}

.el-table .row-offline {
  background-color: #f4f4f5 !important;
}

.el-table--striped .el-table__body tr.row-fault td.el-table__cell {
  background-color: #fef0f0 !important;
}

.el-table--striped .el-table__body tr.row-offline td.el-table__cell {
  background-color: #f4f4f5 !important;
}
</style>
