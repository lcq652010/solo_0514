<template>
  <div id="app">
    <div class="header">
      <h1>景区自助门票售取票终端运维管理系统</h1>
    </div>
    <div class="container">
      <el-card class="search-card">
        <el-form :inline="true" :model="searchForm" class="search-form">
          <el-form-item label="设备编号">
            <el-input
              v-model="searchForm.deviceCode"
              placeholder="请输入设备编号"
              clearable
              @keyup.enter.native="handleSearch"
            ></el-input>
          </el-form-item>
          <el-form-item label="景区点位">
            <el-input
              v-model="searchForm.location"
              placeholder="请输入景区点位"
              clearable
              @keyup.enter.native="handleSearch"
            ></el-input>
          </el-form-item>
          <el-form-item label="设备状态">
            <el-select
              v-model="searchForm.status"
              placeholder="请选择设备状态"
              clearable
              style="width: 140px"
              @change="handleSearch"
            >
              <el-option label="全部" value=""></el-option>
              <el-option label="正常" value="正常"></el-option>
              <el-option label="故障" value="故障"></el-option>
              <el-option label="离线" value="离线"></el-option>
              <el-option label="维护中" value="维护中"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
          <el-form-item style="float: right">
            <el-button type="danger" @click="openFaultDialog">故障上报</el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <el-card class="table-card">
        <el-table :data="tableData" border stripe style="width: 100%" :row-class-name="tableRowClassName">
          <el-table-column prop="deviceCode" label="设备编号" width="120" align="center"></el-table-column>
          <el-table-column prop="location" label="景区点位" width="130" align="center"></el-table-column>
          <el-table-column prop="area" label="摆放区域" width="130" align="center"></el-table-column>
          <el-table-column prop="status" label="设备状态" width="100" align="center">
            <template slot-scope="scope">
              <el-tag :type="getStatusType(scope.row.status)" size="medium">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="qrModule" label="二维码模块" width="110" align="center">
            <template slot-scope="scope">
              <i
                :class="scope.row.qrModule ? 'el-icon-success status-icon success' : 'el-icon-error status-icon error'"
              ></i>
              <span>{{ scope.row.qrModule ? '正常' : '异常' }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="printer" label="打印机" width="110" align="center">
            <template slot-scope="scope">
              <i
                :class="scope.row.printer ? 'el-icon-success status-icon success' : 'el-icon-error status-icon error'"
              ></i>
              <span>{{ scope.row.printer ? '正常' : '异常' }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="idCardReader" label="身份证阅读器" width="130" align="center">
            <template slot-scope="scope">
              <i
                :class="scope.row.idCardReader ? 'el-icon-success status-icon success' : 'el-icon-error status-icon error'"
              ></i>
              <span>{{ scope.row.idCardReader ? '正常' : '异常' }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150" align="center">
            <template slot-scope="scope">
              <el-button size="small" type="text" @click="handleReport(scope.row)">故障上报</el-button>
              <el-button size="small" type="text">查看详情</el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination">
          <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="pagination.page"
            :page-sizes="[5, 10, 20, 50]"
            :page-size="pagination.size"
            layout="total, sizes, prev, pager, next, jumper"
            :total="pagination.total"
          ></el-pagination>
        </div>
      </el-card>
    </div>

    <el-dialog
      title="故障上报"
      :visible.sync="faultDialogVisible"
      width="500px"
      :before-close="handleDialogClose"
    >
      <el-form :model="faultForm" :rules="faultRules" ref="faultForm" label-width="100px">
        <el-form-item label="工单编号">
          <el-input v-model="faultForm.orderNo" disabled></el-input>
        </el-form-item>
        <el-form-item label="选择设备" prop="deviceId">
          <el-select v-model="faultForm.deviceId" placeholder="请选择设备" filterable style="width: 100%">
            <el-option
              v-for="item in deviceList"
              :key="item.id"
              :label="`${item.deviceCode} - ${item.location}`"
              :value="item.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="故障描述" prop="description">
          <el-input
            type="textarea"
            v-model="faultForm.description"
            placeholder="请详细描述故障情况"
            rows="4"
            maxlength="500"
            show-word-limit
          ></el-input>
        </el-form-item>
        <el-form-item label="上报时间">
          <el-input v-model="faultForm.reportTime" disabled></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="faultDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitFaultReport">确 定</el-button>
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
        location: '',
        status: ''
      },
      allDevices: [],
      tableData: [],
      pagination: {
        page: 1,
        size: 10,
        total: 0
      },
      faultDialogVisible: false,
      faultForm: {
        orderNo: '',
        deviceId: '',
        description: '',
        reportTime: ''
      },
      faultRules: {
        deviceId: [
          { required: true, message: '请选择设备', trigger: 'change' }
        ],
        description: [
          { required: true, message: '请输入故障描述', trigger: 'blur' },
          { min: 5, message: '故障描述至少5个字符', trigger: 'blur' }
        ]
      },
      deviceList: [],
      orderCounter: 1
    }
  },
  created() {
    this.initMockData()
  },
  methods: {
    initMockData() {
      const locations = ['黄山风景区', '泰山风景区', '华山风景区', '张家界风景区', '九寨沟风景区']
      const areas = ['东门入口', '西门入口', '南门入口', '北门入口', '游客中心', '山顶服务区']
      const statuses = ['正常', '故障', '离线', '维护中']
      const moduleStatuses = [true, true, true, true, false]
      
      this.allDevices = []
      for (let i = 1; i <= 35; i++) {
        this.allDevices.push({
          id: i,
          deviceCode: `DEV${String(i).padStart(4, '0')}`,
          location: locations[Math.floor(Math.random() * locations.length)],
          area: areas[Math.floor(Math.random() * areas.length)],
          status: statuses[Math.floor(Math.random() * statuses.length)],
          qrModule: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)],
          printer: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)],
          idCardReader: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)]
        })
      }
      
      this.deviceList = [...this.allDevices]
      this.handleSearch()
    },
    tableRowClassName({ row }) {
      if (row.status === '故障') {
        return 'fault-row'
      } else if (row.status === '离线') {
        return 'offline-row'
      }
      return ''
    },
    getStatusType(status) {
      const typeMap = {
        '正常': 'success',
        '故障': 'danger',
        '离线': 'info',
        '维护中': 'warning'
      }
      return typeMap[status] || 'info'
    },
    handleSearch() {
      let filtered = [...this.allDevices]
      
      if (this.searchForm.deviceCode) {
        filtered = filtered.filter(item => 
          item.deviceCode.toLowerCase().includes(this.searchForm.deviceCode.toLowerCase())
        )
      }
      
      if (this.searchForm.location) {
        filtered = filtered.filter(item => 
          item.location.includes(this.searchForm.location)
        )
      }
      
      if (this.searchForm.status) {
        filtered = filtered.filter(item => 
          item.status === this.searchForm.status
        )
      }
      
      this.pagination.total = filtered.length
      this.updateTableData(filtered)
    },
    handleReset() {
      this.searchForm = {
        deviceCode: '',
        location: '',
        status: ''
      }
      this.handleSearch()
    },
    updateTableData(filteredData) {
      const start = (this.pagination.page - 1) * this.pagination.size
      const end = start + this.pagination.size
      this.tableData = filteredData.slice(start, end)
    },
    handleSizeChange(val) {
      this.pagination.size = val
      this.pagination.page = 1
      this.handleSearch()
    },
    handleCurrentChange(val) {
      this.pagination.page = val
      this.handleSearch()
    },
    openFaultDialog() {
      this.generateOrderNo()
      this.faultForm.reportTime = this.getCurrentTime()
      this.faultDialogVisible = true
    },
    handleReport(row) {
      this.generateOrderNo()
      this.faultForm.deviceId = row.id
      this.faultForm.reportTime = this.getCurrentTime()
      this.faultDialogVisible = true
    },
    generateOrderNo() {
      const now = new Date()
      const dateStr = now.getFullYear().toString() + 
        String(now.getMonth() + 1).padStart(2, '0') + 
        String(now.getDate()).padStart(2, '0')
      const timeStr = String(now.getHours()).padStart(2, '0') + 
        String(now.getMinutes()).padStart(2, '0') + 
        String(now.getSeconds()).padStart(2, '0')
      this.faultForm.orderNo = `WO${dateStr}${timeStr}${String(this.orderCounter).padStart(3, '0')}`
      this.orderCounter++
    },
    getCurrentTime() {
      const now = new Date()
      return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')} ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`
    },
    handleDialogClose() {
      this.$refs.faultForm.resetFields()
      this.faultForm.orderNo = ''
      this.faultForm.description = ''
      this.faultDialogVisible = false
    },
    submitFaultReport() {
      this.$refs.faultForm.validate((valid) => {
        if (valid) {
          this.$message.success(`工单 ${this.faultForm.orderNo} 提交成功！`)
          this.handleDialogClose()
        }
      })
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
  background-color: #f0f2f5;
}

#app {
  min-height: 100vh;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px 40px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.header h1 {
  color: #fff;
  font-size: 24px;
  font-weight: 500;
}

.container {
  padding: 20px;
}

.search-card {
  margin-bottom: 20px;
}

.search-form {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
}

.table-card {
  min-height: 500px;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.el-tag--success {
  background-color: #f0f9eb;
  border-color: #e1f3d8;
  color: #67c23a;
}

.el-tag--danger {
  background-color: #fef0f0;
  border-color: #fde2e2;
  color: #f56c6c;
}

.el-tag--info {
  background-color: #f4f4f5;
  border-color: #e9e9eb;
  color: #909399;
}

.el-tag--warning {
  background-color: #fdf6ec;
  border-color: #faecd8;
  color: #e6a23c;
}

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
  background-color: #e9e9eb !important;
}

.status-icon {
  margin-right: 5px;
  font-size: 16px;
}

.status-icon.success {
  color: #67c23a;
}

.status-icon.error {
  color: #f56c6c;
}
</style>