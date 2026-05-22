<template>
  <div id="app">
    <div class="header">
      <h1>景区自助购票取票终端运维管理系统</h1>
    </div>
    <div class="container">
      <el-card class="search-card">
        <el-form :inline="true" :model="searchForm" class="search-form">
          <el-form-item label="关键词搜索">
            <el-input v-model="searchForm.keyword" placeholder="输入设备编号/景区/安装区域" clearable style="width: 300px"></el-input>
          </el-form-item>
          <el-form-item label="设备编号">
            <el-input v-model="searchForm.deviceId" placeholder="请输入设备编号" clearable></el-input>
          </el-form-item>
          <el-form-item label="景区名称">
            <el-input v-model="searchForm.scenicName" placeholder="请输入景区名称" clearable></el-input>
          </el-form-item>
          <el-form-item label="设备状态">
            <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
              <el-option label="正常运行" value="normal"></el-option>
              <el-option label="预警" value="warning"></el-option>
              <el-option label="故障" value="fault"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch" icon="el-icon-search">查询</el-button>
            <el-button @click="handleReset" icon="el-icon-refresh">重置</el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <el-card class="table-card">
        <div class="table-header">
          <span class="title">设备列表</span>
          <el-button type="danger" @click="openReportDialog">故障上报</el-button>
        </div>
        <el-table :data="tableData" border stripe :row-class-name="getRowClassName" style="width: 100%">
          <el-table-column prop="deviceId" label="设备编号" width="130" align="center"></el-table-column>
          <el-table-column prop="scenicSpot" label="景区点位" align="center"></el-table-column>
          <el-table-column prop="installArea" label="安装区域" width="130" align="center"></el-table-column>
          <el-table-column prop="status" label="运行状态" width="100" align="center">
            <template slot-scope="scope">
              <el-tag :type="getStatusType(scope.row.status)" size="small">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="身份证读取" width="110" align="center">
            <template slot-scope="scope">
              <el-tag :type="getModuleStatusType(scope.row.idCardStatus)" size="mini">
                {{ getModuleStatusText(scope.row.idCardStatus) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="小票打印" width="110" align="center">
            <template slot-scope="scope">
              <el-tag :type="getModuleStatusType(scope.row.printStatus)" size="mini">
                {{ getModuleStatusText(scope.row.printStatus) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="支付对接" width="110" align="center">
            <template slot-scope="scope">
              <el-tag :type="getModuleStatusType(scope.row.payStatus)" size="mini">
                {{ getModuleStatusText(scope.row.payStatus) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="120" align="center">
            <template slot-scope="scope">
              <el-button type="text" size="small" @click="handleReport(scope.row)">故障上报</el-button>
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

    <el-dialog title="故障上报" :visible.sync="reportDialogVisible" width="600px">
      <el-form :model="reportForm" :rules="reportRules" ref="reportForm" label-width="100px">
        <el-form-item label="工单编号">
          <el-input v-model="reportForm.orderNo" disabled></el-input>
        </el-form-item>
        <el-form-item label="选择设备" prop="deviceId">
          <el-select v-model="reportForm.deviceId" placeholder="请选择设备" style="width: 100%" filterable>
            <el-option
              v-for="device in allDevices"
              :key="device.deviceId"
              :label="`${device.deviceId} - ${device.scenicSpot}`"
              :value="device.deviceId">
              <span style="float: left">{{ device.deviceId }} - {{ device.scenicSpot }}</span>
              <span style="float: right; margin-right: 20px">
                <el-tag :type="getStatusType(device.status)" size="mini">{{ getStatusText(device.status) }}</el-tag>
              </span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="设备信息" v-if="selectedDeviceInfo">
          <el-descriptions :column="2" border size="small">
            <el-descriptions-item label="设备编号">{{ selectedDeviceInfo.deviceId }}</el-descriptions-item>
            <el-descriptions-item label="当前状态">
              <el-tag :type="getStatusType(selectedDeviceInfo.status)">{{ getStatusText(selectedDeviceInfo.status) }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="景区点位" :span="2">{{ selectedDeviceInfo.scenicSpot }}</el-descriptions-item>
            <el-descriptions-item label="安装区域" :span="2">{{ selectedDeviceInfo.installArea }}</el-descriptions-item>
            <el-descriptions-item label="身份证读取">
              <el-tag :type="getModuleStatusType(selectedDeviceInfo.idCardStatus)" size="mini">{{ getModuleStatusText(selectedDeviceInfo.idCardStatus) }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="小票打印">
              <el-tag :type="getModuleStatusType(selectedDeviceInfo.printStatus)" size="mini">{{ getModuleStatusText(selectedDeviceInfo.printStatus) }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="支付对接">
              <el-tag :type="getModuleStatusType(selectedDeviceInfo.payStatus)" size="mini">{{ getModuleStatusText(selectedDeviceInfo.payStatus) }}</el-tag>
            </el-descriptions-item>
          </el-descriptions>
        </el-form-item>
        <el-form-item label="故障详情" prop="faultDetail">
          <el-input
            type="textarea"
            v-model="reportForm.faultDetail"
            :rows="5"
            placeholder="请详细描述故障现象、发生时间等信息（至少10个字符）">
          </el-input>
        </el-form-item>
        <el-form-item label="联系人" prop="contactPerson">
          <el-input v-model="reportForm.contactPerson" placeholder="请填写联系人姓名"></el-input>
        </el-form-item>
        <el-form-item label="联系电话" prop="contactPhone">
          <el-input v-model="reportForm.contactPhone" placeholder="请填写联系电话"></el-input>
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
        deviceId: '',
        scenicName: '',
        keyword: '',
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
        faultDetail: '',
        contactPerson: '',
        contactPhone: ''
      },
      reportRules: {
        deviceId: [
          { required: true, message: '请选择设备', trigger: 'change' }
        ],
        faultDetail: [
          { required: true, message: '请填写故障详情', trigger: 'blur' },
          { min: 10, message: '故障详情至少10个字符，请详细描述故障现象', trigger: 'blur' }
        ],
        contactPerson: [
          { required: true, message: '请填写联系人', trigger: 'blur' }
        ],
        contactPhone: [
          { required: true, message: '请填写联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.initData()
  },
  computed: {
    selectedDeviceInfo() {
      if (!this.reportForm.deviceId) return null
      return this.allDevices.find(d => d.deviceId === this.reportForm.deviceId)
    }
  },
  methods: {
    initData() {
      this.allDevices = [
        { deviceId: 'DEV001', scenicSpot: '黄山风景区南门', installArea: '入口大厅', status: 'normal', idCardStatus: 'normal', printStatus: 'normal', payStatus: 'normal' },
        { deviceId: 'DEV002', scenicSpot: '黄山风景区南门', installArea: '售票厅A区', status: 'normal', idCardStatus: 'normal', printStatus: 'warning', payStatus: 'normal' },
        { deviceId: 'DEV003', scenicSpot: '黄山风景区北门', installArea: '游客服务中心', status: 'fault', idCardStatus: 'fault', printStatus: 'normal', payStatus: 'warning' },
        { deviceId: 'DEV004', scenicSpot: '九华山风景区', installArea: '山门入口', status: 'normal', idCardStatus: 'normal', printStatus: 'normal', payStatus: 'normal' },
        { deviceId: 'DEV005', scenicSpot: '九华山风景区', installArea: '索道站', status: 'warning', idCardStatus: 'normal', printStatus: 'warning', payStatus: 'normal' },
        { deviceId: 'DEV006', scenicSpot: '西湖风景区', installArea: '断桥入口', status: 'normal', idCardStatus: 'normal', printStatus: 'normal', payStatus: 'normal' },
        { deviceId: 'DEV007', scenicSpot: '西湖风景区', installArea: '雷峰塔景区', status: 'fault', idCardStatus: 'normal', printStatus: 'fault', payStatus: 'fault' },
        { deviceId: 'DEV008', scenicSpot: '故宫博物院', installArea: '午门入口', status: 'normal', idCardStatus: 'normal', printStatus: 'normal', payStatus: 'normal' },
        { deviceId: 'DEV009', scenicSpot: '故宫博物院', installArea: '神武门出口', status: 'normal', idCardStatus: 'normal', printStatus: 'normal', payStatus: 'warning' },
        { deviceId: 'DEV010', scenicSpot: '八达岭长城', installArea: '北一楼入口', status: 'warning', idCardStatus: 'warning', printStatus: 'normal', payStatus: 'normal' },
        { deviceId: 'DEV011', scenicSpot: '八达岭长城', installArea: '南四楼入口', status: 'normal', idCardStatus: 'normal', printStatus: 'normal', payStatus: 'normal' },
        { deviceId: 'DEV012', scenicSpot: '张家界国家森林公园', installArea: '东门入口', status: 'normal', idCardStatus: 'normal', printStatus: 'warning', payStatus: 'normal' },
        { deviceId: 'DEV013', scenicSpot: '张家界国家森林公园', installArea: '西门入口', status: 'fault', idCardStatus: 'fault', printStatus: 'fault', payStatus: 'normal' },
        { deviceId: 'DEV014', scenicSpot: '九寨沟风景区', installArea: '沟口入口', status: 'normal', idCardStatus: 'normal', printStatus: 'normal', payStatus: 'normal' },
        { deviceId: 'DEV015', scenicSpot: '九寨沟风景区', installArea: '诺日朗中心', status: 'normal', idCardStatus: 'normal', printStatus: 'normal', payStatus: 'normal' },
        { deviceId: 'DEV016', scenicSpot: '三亚亚龙湾', installArea: '海滩入口', status: 'warning', idCardStatus: 'normal', printStatus: 'warning', payStatus: 'warning' },
        { deviceId: 'DEV017', scenicSpot: '三亚亚龙湾', installArea: '游客中心', status: 'normal', idCardStatus: 'normal', printStatus: 'normal', payStatus: 'normal' },
        { deviceId: 'DEV018', scenicSpot: '丽江古城', installArea: '大水车入口', status: 'normal', idCardStatus: 'normal', printStatus: 'normal', payStatus: 'normal' },
        { deviceId: 'DEV019', scenicSpot: '丽江古城', installArea: '四方街', status: 'fault', idCardStatus: 'normal', printStatus: 'fault', payStatus: 'normal' },
        { deviceId: 'DEV020', scenicSpot: '桂林漓江', installArea: '磨盘山码头', status: 'normal', idCardStatus: 'normal', printStatus: 'normal', payStatus: 'normal' }
      ]
      this.pagination.total = this.allDevices.length
      this.loadTableData()
    },
    getRowClassName({ row }) {
      if (row.status === 'fault') {
        return 'fault-row'
      } else if (row.status === 'warning') {
        return 'warning-row'
      }
      return ''
    },
    loadTableData() {
      let filteredData = [...this.allDevices]
      
      const keyword = this.searchForm.keyword || this.searchForm.deviceId || this.searchForm.scenicName
      if (keyword) {
        const lowerKeyword = keyword.toLowerCase()
        filteredData = filteredData.filter(item => 
          item.deviceId.toLowerCase().includes(lowerKeyword) ||
          item.scenicSpot.toLowerCase().includes(lowerKeyword) ||
          item.installArea.toLowerCase().includes(lowerKeyword)
        )
      }
      
      if (this.searchForm.status) {
        filteredData = filteredData.filter(item => item.status === this.searchForm.status)
      }
      
      this.pagination.total = filteredData.length
      
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      this.tableData = filteredData.slice(start, end)
    },
    getModuleStatusType(status) {
      return this.getStatusType(status)
    },
    getModuleStatusText(status) {
      return this.getStatusText(status)
    },
    handleSearch() {
      this.pagination.currentPage = 1
      this.loadTableData()
    },
    handleReset() {
      this.searchForm.keyword = ''
      this.searchForm.deviceId = ''
      this.searchForm.scenicName = ''
      this.searchForm.status = ''
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
    getStatusType(status) {
      const statusMap = {
        normal: 'success',
        warning: 'warning',
        fault: 'danger'
      }
      return statusMap[status] || 'info'
    },
    getStatusText(status) {
      const statusMap = {
        normal: '正常运行',
        warning: '预警',
        fault: '故障'
      }
      return statusMap[status] || '未知'
    },
    generateOrderNo() {
      const now = new Date()
      const year = now.getFullYear()
      const month = String(now.getMonth() + 1).padStart(2, '0')
      const day = String(now.getDate()).padStart(2, '0')
      const random = Math.floor(Math.random() * 10000).toString().padStart(4, '0')
      return `GD${year}${month}${day}${random}`
    },
    openReportDialog() {
      this.reportForm.orderNo = this.generateOrderNo()
      this.reportForm.deviceId = ''
      this.reportForm.faultDetail = ''
      this.reportForm.contactPerson = ''
      this.reportForm.contactPhone = ''
      this.reportDialogVisible = true
      this.$nextTick(() => {
        this.$refs.reportForm.clearValidate()
      })
    },
    handleReport(row) {
      this.reportForm.orderNo = this.generateOrderNo()
      this.reportForm.deviceId = row.deviceId
      this.reportForm.faultDetail = ''
      this.reportForm.contactPerson = ''
      this.reportForm.contactPhone = ''
      this.reportDialogVisible = true
      this.$nextTick(() => {
        this.$refs.reportForm.clearValidate()
      })
    },
    submitReport() {
      this.$refs.reportForm.validate((valid) => {
        if (valid) {
          this.$confirm('确认提交该故障工单吗？提交后将通知运维人员处理。', '提交确认', {
            confirmButtonText: '确定提交',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            this.$message({
              type: 'success',
              message: `工单 ${this.reportForm.orderNo} 提交成功！运维人员将尽快处理。`
            })
            this.reportDialogVisible = false
          }).catch(() => {
            this.$message({
              type: 'info',
              message: '已取消提交'
            })
          })
        } else {
          this.$message.error('请完善表单信息后再提交')
          return false
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
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", Arial, sans-serif;
  background-color: #f5f7fa;
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
  padding: 20px 40px;
}

.search-card {
  margin-bottom: 20px;
}

.search-form {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}

.table-card .table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.table-card .table-header .title {
  font-size: 18px;
  font-weight: 500;
  color: #303133;
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.dialog-footer {
  text-align: right;
}

.el-table .fault-row {
  background-color: #fef0f0 !important;
}

.el-table .fault-row:hover > td {
  background-color: #fde2e2 !important;
}

.el-table .warning-row {
  background-color: #fdf6ec !important;
}

.el-table .warning-row:hover > td {
  background-color: #faecd8 !important;
}
</style>
