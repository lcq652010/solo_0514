<template>
  <div class="device-management">
    <div class="header">
      <h1 class="title">税务大厅自助发票代开终端运维管理系统</h1>
    </div>

    <div class="content">
      <div class="search-bar">
        <el-input
          v-model="searchForm.deviceCode"
          placeholder="请输入设备编号"
          clearable
          class="search-input"
          style="width: 200px"
          @keyup.enter.native="handleSearch"
        ></el-input>
        <el-input
          v-model="searchForm.hallName"
          placeholder="请输入办税服务厅名称"
          clearable
          class="search-input"
          style="width: 200px"
          @keyup.enter.native="handleSearch"
        ></el-input>
        <el-select
          v-model="searchForm.status"
          placeholder="设备状态"
          clearable
          style="width: 140px"
          @change="handleSearch"
        >
          <el-option label="正常" value="正常"></el-option>
          <el-option label="故障" value="故障"></el-option>
          <el-option label="离线" value="离线"></el-option>
          <el-option label="维护中" value="维护中"></el-option>
        </el-select>
        <el-button type="primary" @click="handleSearch" style="margin-left: 15px">
          <i class="el-icon-search"></i> 搜索
        </el-button>
        <el-button @click="handleReset" style="margin-left: 10px">
          <i class="el-icon-refresh"></i> 重置
        </el-button>
        <el-button type="danger" @click="openFaultDialog" style="margin-left: auto">
          <i class="el-icon-warning"></i> 故障上报
        </el-button>
      </div>

      <div class="table-container">
        <el-table
          :data="tableData"
          border
          stripe
          :row-class-name="tableRowClassName"
          style="width: 100%"
        >
          <el-table-column
            prop="deviceCode"
            label="设备编号"
            min-width="130"
            align="center"
          ></el-table-column>
          <el-table-column
            prop="hallName"
            label="办税服务厅"
            min-width="180"
            align="center"
          ></el-table-column>
          <el-table-column
            prop="location"
            label="安装位置"
            min-width="150"
            align="center"
          ></el-table-column>
          <el-table-column
            label="模块运行状态"
            min-width="240"
            align="left"
          >
            <template slot-scope="scope">
              <div class="module-status">
                <div class="module-item">
                  <span :class="['module-dot', getModuleStatusClass(scope.row.modules.idCard)]"></span>
                  <span>身份证读卡：{{ scope.row.modules.idCard }}</span>
                </div>
                <div class="module-item">
                  <span :class="['module-dot', getModuleStatusClass(scope.row.modules.invoicePrint)]"></span>
                  <span>发票打印：{{ scope.row.modules.invoicePrint }}</span>
                </div>
                <div class="module-item">
                  <span :class="['module-dot', getModuleStatusClass(scope.row.modules.taxDiskComm)]"></span>
                  <span>金税盘通信：{{ scope.row.modules.taxDiskComm }}</span>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column
            prop="status"
            label="设备状态"
            min-width="100"
            align="center"
          >
            <template slot-scope="scope">
              <el-tag :type="getStatusType(scope.row.status)" size="medium">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column
            label="操作"
            min-width="150"
            align="center"
          >
            <template slot-scope="scope">
              <el-button
                type="text"
                size="small"
                @click="handleReportFault(scope.row)"
              >
                故障上报
              </el-button>
              <el-button
                type="text"
                size="small"
                @click="handleToggleStatus(scope.row)"
              >
                切换状态
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div class="pagination-container">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page.sync="pagination.currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pagination.pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
        ></el-pagination>
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
        <el-form-item label="工单编号">
          <el-input v-model="faultForm.orderNo" disabled></el-input>
        </el-form-item>
        <el-form-item label="选择设备" prop="deviceId">
          <el-select
            v-model="faultForm.deviceId"
            placeholder="请选择设备"
            style="width: 100%"
            filterable
            clearable
          >
            <el-option
              v-for="device in deviceList"
              :key="device.id"
              :label="device.deviceCode + ' - ' + device.hallName"
              :value="device.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="设备编号">
          <el-input v-model="faultForm.deviceCode" disabled></el-input>
        </el-form-item>
        <el-form-item label="办税服务厅">
          <el-input v-model="faultForm.hallName" disabled></el-input>
        </el-form-item>
        <el-form-item label="安装位置">
          <el-input v-model="faultForm.location" disabled></el-input>
        </el-form-item>
        <el-form-item label="故障描述" prop="faultDescription">
          <el-input
            v-model="faultForm.faultDescription"
            type="textarea"
            :rows="4"
            placeholder="请详细描述故障情况"
            maxlength="500"
            show-word-limit
          ></el-input>
        </el-form-item>
        <el-form-item label="上报人">
          <el-input v-model="faultForm.reporter" placeholder="请输入上报人姓名"></el-input>
        </el-form-item>
        <el-form-item label="联系电话">
          <el-input v-model="faultForm.contactPhone" placeholder="请输入联系电话"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="faultDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitFaultForm">确 定</el-button>
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
        hallName: '',
        status: ''
      },
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      filteredDeviceList: [],
      allDeviceList: [],
      tableData: [],
      deviceList: [],
      faultDialogVisible: false,
      faultForm: {
        orderNo: '',
        deviceId: '',
        deviceCode: '',
        hallName: '',
        location: '',
        faultDescription: '',
        reporter: '',
        contactPhone: ''
      },
      faultRules: {
        deviceId: [
          { required: true, message: '请选择上报设备', trigger: 'change' }
        ],
        faultDescription: [
          { required: true, message: '请输入故障描述', trigger: 'blur' },
          { min: 10, message: '故障描述至少10个字符', trigger: 'blur' }
        ]
      },
      loading: false,
      statusList: ['正常', '故障', '离线', '维护中']
    }
  },
  created() {
    this.initDeviceData()
  },
  watch: {
    'pagination.currentPage': function(newVal) {
      this.loadTableData()
    }
  },
  methods: {
    initDeviceData() {
      this.allDeviceList = [
        { id: 1, deviceCode: 'FP-2024-001', hallName: '北京市朝阳区第一税务所', location: '一楼大厅东侧', status: '正常', modules: { idCard: '正常', invoicePrint: '正常', taxDiskComm: '正常' } },
        { id: 2, deviceCode: 'FP-2024-002', hallName: '北京市朝阳区第一税务所', location: '一楼大厅西侧', status: '故障', modules: { idCard: '故障', invoicePrint: '正常', taxDiskComm: '异常' } },
        { id: 3, deviceCode: 'FP-2024-003', hallName: '北京市朝阳区第二税务所', location: '二楼服务窗口旁', status: '离线', modules: { idCard: '离线', invoicePrint: '离线', taxDiskComm: '离线' } },
        { id: 4, deviceCode: 'FP-2024-004', hallName: '北京市海淀区第一税务所', location: '大堂入口左侧', status: '正常', modules: { idCard: '正常', invoicePrint: '正常', taxDiskComm: '正常' } },
        { id: 5, deviceCode: 'FP-2024-005', hallName: '北京市海淀区第一税务所', location: '大堂入口右侧', status: '维护中', modules: { idCard: '维护中', invoicePrint: '维护中', taxDiskComm: '维护中' } },
        { id: 6, deviceCode: 'FP-2024-006', hallName: '北京市海淀区第二税务所', location: '三楼自助区', status: '正常', modules: { idCard: '正常', invoicePrint: '正常', taxDiskComm: '正常' } },
        { id: 7, deviceCode: 'FP-2024-007', hallName: '北京市西城区税务所', location: '一楼大厅', status: '故障', modules: { idCard: '正常', invoicePrint: '故障', taxDiskComm: '异常' } },
        { id: 8, deviceCode: 'FP-2024-008', hallName: '北京市东城区税务所', location: '二楼201室门口', status: '正常', modules: { idCard: '正常', invoicePrint: '正常', taxDiskComm: '正常' } },
        { id: 9, deviceCode: 'FP-2024-009', hallName: '北京市丰台区税务所', location: '一楼服务大厅', status: '离线', modules: { idCard: '离线', invoicePrint: '离线', taxDiskComm: '离线' } },
        { id: 10, deviceCode: 'FP-2024-010', hallName: '北京市通州区税务所', location: '行政服务中心A区', status: '正常', modules: { idCard: '正常', invoicePrint: '正常', taxDiskComm: '正常' } },
        { id: 11, deviceCode: 'FP-2024-011', hallName: '北京市顺义区税务所', location: '一楼东侧', status: '正常', modules: { idCard: '正常', invoicePrint: '正常', taxDiskComm: '正常' } },
        { id: 12, deviceCode: 'FP-2024-012', hallName: '北京市昌平区税务所', location: '二楼自助服务区', status: '维护中', modules: { idCard: '维护中', invoicePrint: '维护中', taxDiskComm: '维护中' } },
        { id: 13, deviceCode: 'FP-2024-013', hallName: '北京市大兴区税务所', location: '大厅西北角', status: '正常', modules: { idCard: '正常', invoicePrint: '正常', taxDiskComm: '正常' } },
        { id: 14, deviceCode: 'FP-2024-014', hallName: '北京市房山区税务所', location: '一楼南侧', status: '故障', modules: { idCard: '异常', invoicePrint: '故障', taxDiskComm: '正常' } },
        { id: 15, deviceCode: 'FP-2024-015', hallName: '北京市石景山区税务所', location: '二楼西侧', status: '正常', modules: { idCard: '正常', invoicePrint: '正常', taxDiskComm: '正常' } },
        { id: 16, deviceCode: 'FP-2024-016', hallName: '上海市浦东新区税务所', location: '一楼办税大厅', status: '离线', modules: { idCard: '离线', invoicePrint: '离线', taxDiskComm: '离线' } },
        { id: 17, deviceCode: 'FP-2024-017', hallName: '上海市黄浦区税务所', location: '二楼自助区', status: '正常', modules: { idCard: '正常', invoicePrint: '正常', taxDiskComm: '正常' } },
        { id: 18, deviceCode: 'FP-2024-018', hallName: '广州市天河区税务所', location: '政务中心B区', status: '故障', modules: { idCard: '故障', invoicePrint: '故障', taxDiskComm: '异常' } },
        { id: 19, deviceCode: 'FP-2024-019', hallName: '深圳市南山区税务所', location: '科技园区服务点', status: '正常', modules: { idCard: '正常', invoicePrint: '正常', taxDiskComm: '正常' } },
        { id: 20, deviceCode: 'FP-2024-020', hallName: '杭州市西湖区税务所', location: '行政大厅东侧', status: '离线', modules: { idCard: '离线', invoicePrint: '离线', taxDiskComm: '离线' } }
      ]
      this.deviceList = this.allDeviceList
      this.filteredDeviceList = [...this.allDeviceList]
      this.pagination.total = this.allDeviceList.length
      this.loadTableData()
    },
    getStatusType(status) {
      const statusMap = {
        '正常': 'success',
        '故障': 'danger',
        '离线': 'warning',
        '维护中': 'info'
      }
      return statusMap[status] || ''
    },
    getModuleStatusClass(status) {
      if (status === '正常') return 'normal'
      if (status === '故障' || status === '异常') return 'error'
      return 'warning'
    },
    tableRowClassName({ row, rowIndex }) {
      if (row.status === '故障') {
        return 'fault-row'
      } else if (row.status === '离线') {
        return 'offline-row'
      }
      return ''
    },
    handleSearch() {
      this.loading = true
      
      setTimeout(() => {
        let filteredData = [...this.allDeviceList]
        
        if (this.searchForm.deviceCode && this.searchForm.deviceCode.trim()) {
          const keyword = this.searchForm.deviceCode.trim().toLowerCase()
          filteredData = filteredData.filter(item => 
            item.deviceCode.toLowerCase().includes(keyword)
          )
        }
        
        if (this.searchForm.hallName && this.searchForm.hallName.trim()) {
          const keyword = this.searchForm.hallName.trim()
          filteredData = filteredData.filter(item => 
            item.hallName.includes(keyword)
          )
        }

        if (this.searchForm.status) {
          filteredData = filteredData.filter(item => 
            item.status === this.searchForm.status
          )
        }
        
        this.filteredDeviceList = filteredData
        this.pagination.total = filteredData.length
        this.pagination.currentPage = 1
        
        this.loadTableData()
        this.loading = false
      }, 200)
    },
    handleReset() {
      this.searchForm = {
        deviceCode: '',
        hallName: '',
        status: ''
      }
      this.pagination.currentPage = 1
      this.handleSearch()
    },
    loadTableData() {
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      this.tableData = this.filteredDeviceList.slice(start, end)
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.pagination.currentPage = 1
      this.loadTableData()
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
    },
    openFaultDialog() {
      this.generateOrderNo()
      this.faultDialogVisible = true
    },
    handleReportFault(row) {
      this.generateOrderNo()
      this.faultForm.deviceId = row.id
      this.faultForm.deviceCode = row.deviceCode
      this.faultForm.hallName = row.hallName
      this.faultForm.location = row.location
      this.faultDialogVisible = true
    },
    handleToggleStatus(row) {
      const currentIndex = this.statusList.indexOf(row.status)
      const nextIndex = (currentIndex + 1) % this.statusList.length
      const nextStatus = this.statusList[nextIndex]
      
      this.$set(row, 'status', nextStatus)
      
      if (nextStatus === '正常') {
        this.$set(row.modules, 'idCard', '正常')
        this.$set(row.modules, 'invoicePrint', '正常')
        this.$set(row.modules, 'taxDiskComm', '正常')
      } else if (nextStatus === '故障') {
        this.$set(row.modules, 'idCard', '故障')
        this.$set(row.modules, 'invoicePrint', '异常')
        this.$set(row.modules, 'taxDiskComm', '正常')
      } else if (nextStatus === '离线') {
        this.$set(row.modules, 'idCard', '离线')
        this.$set(row.modules, 'invoicePrint', '离线')
        this.$set(row.modules, 'taxDiskComm', '离线')
      } else if (nextStatus === '维护中') {
        this.$set(row.modules, 'idCard', '维护中')
        this.$set(row.modules, 'invoicePrint', '维护中')
        this.$set(row.modules, 'taxDiskComm', '维护中')
      }
      
      this.$message({
        type: 'success',
        message: `${row.deviceCode} 状态已切换为：${nextStatus}`
      })
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
      this.faultForm.orderNo = `GD${year}${month}${day}${hours}${minutes}${seconds}${random}`
    },
    resetFaultForm() {
      this.faultForm = {
        orderNo: '',
        deviceId: '',
        deviceCode: '',
        hallName: '',
        location: '',
        faultDescription: '',
        reporter: '',
        contactPhone: ''
      }
      this.$refs.faultForm && this.$refs.faultForm.resetFields()
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
        } else {
          this.$message({
            type: 'error',
            message: '请完善必填信息后再提交'
          })
        }
      })
    }
  },
  watch: {
    'faultForm.deviceId'(newVal) {
      if (newVal) {
        const device = this.allDeviceList.find(item => item.id === newVal)
        if (device) {
          this.faultForm.deviceCode = device.deviceCode
          this.faultForm.hallName = device.hallName
          this.faultForm.location = device.location
        }
      } else {
        this.faultForm.deviceCode = ''
        this.faultForm.hallName = ''
        this.faultForm.location = ''
      }
    }
  }
}
</script>

<style scoped lang="scss">
.device-management {
  width: 100%;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;

  .header {
    background: #fff;
    border-radius: 8px;
    padding: 20px 30px;
    margin-bottom: 20px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);

    .title {
      font-size: 24px;
      font-weight: 600;
      color: #303133;
      text-align: center;
    }
  }

  .content {
    background: #fff;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  }

  .search-bar {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    padding: 20px 0;
    border-bottom: 1px solid #ebeef5;
  }

  .table-container {
    padding: 20px 0;
  }

  .pagination-container {
    display: flex;
    justify-content: flex-end;
    padding: 20px 0;
  }

  .module-status {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .module-item {
    display: flex;
    align-items: center;
    font-size: 12px;
  }

  .module-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 6px;
  }

  .module-dot.normal {
    background-color: #67c23a;
  }

  .module-dot.error {
    background-color: #f56c6c;
  }

  .module-dot.warning {
    background-color: #e6a23c;
  }
}
</style>

<style>
.el-table .fault-row {
  background-color: #fef0f0 !important;
}

.el-table .offline-row {
  background-color: #fdf6ec !important;
}

.el-table__body tr.fault-row:hover > td {
  background-color: #fde2e2 !important;
}

.el-table__body tr.offline-row:hover > td {
  background-color: #faecd8 !important;
}
</style>
