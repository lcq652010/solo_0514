<template>
  <div class="device-list-container">
    <el-card shadow="hover">
      <div slot="header" class="card-header">
        <span>设备管理</span>
        <el-button type="primary" @click="openFaultReport">故障上报</el-button>
      </div>
      
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm" class="search-form">
          <el-form-item label="运行状态">
            <el-select v-model="searchForm.status" placeholder="全部状态" clearable style="width: 140px">
              <el-option label="全部状态" value=""></el-option>
              <el-option label="在线" value="online"></el-option>
              <el-option label="离线" value="offline"></el-option>
              <el-option label="故障" value="fault"></el-option>
              <el-option label="维护中" value="maintenance"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="关键词搜索">
            <el-input v-model="searchForm.keyword" placeholder="请输入设备编号/网点名称/安装位置" clearable style="width: 300px" @keyup.enter.native="handleSearch"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch" icon="el-icon-search">搜索</el-button>
            <el-button @click="handleReset" icon="el-icon-refresh">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <el-table 
        :data="tableData" 
        border 
        stripe 
        style="width: 100%" 
        v-loading="loading"
        :row-class-name="tableRowClassName">
        <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
        <el-table-column prop="deviceCode" label="设备编号" width="130" align="center"></el-table-column>
        <el-table-column prop="branchName" label="公积金服务网点" min-width="160" align="center"></el-table-column>
        <el-table-column prop="installLocation" label="安装位置" min-width="150" align="center"></el-table-column>
        <el-table-column prop="status" label="设备运行状态" width="120" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)" :effect="getStatusEffect(scope.row.status)" size="small">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="身份核验" width="120" align="center">
          <template slot-scope="scope">
            <el-tag :type="getModuleStatusType(scope.row.identityModule)" size="small">
              {{ getModuleStatusText(scope.row.identityModule) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="证明打印" width="120" align="center">
          <template slot-scope="scope">
            <el-tag :type="getModuleStatusType(scope.row.printModule)" size="small">
              {{ getModuleStatusText(scope.row.printModule) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="联网查询" width="120" align="center">
          <template slot-scope="scope">
            <el-tag :type="getModuleStatusType(scope.row.queryModule)" size="small">
              {{ getModuleStatusText(scope.row.queryModule) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" align="center">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="handleFaultReport(scope.row)">故障上报</el-button>
            <el-dropdown @command="(cmd) => handleStatusChange(scope.row, cmd)">
              <span class="el-dropdown-link">状态变更<i class="el-icon-arrow-down el-icon--right"></i></span>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="online">标记在线</el-dropdown-item>
                <el-dropdown-item command="offline">标记离线</el-dropdown-item>
                <el-dropdown-item command="maintenance">标记维护中</el-dropdown-item>
                <el-dropdown-item command="fault">标记故障</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
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
    
    <FaultReportDialog 
      ref="faultReportDialog" 
      :device-list="deviceList"
      @submit="handleSubmitFault"
    />
  </div>
</template>

<script>
import FaultReportDialog from './FaultReportDialog.vue'

export default {
  name: 'DeviceList',
  components: {
    FaultReportDialog
  },
  data() {
    return {
      loading: false,
      searchForm: {
        keyword: '',
        status: ''
      },
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      allDeviceData: [],
      tableData: []
    }
  },
  computed: {
    deviceList() {
      return this.allDeviceData.map(item => ({
        value: item.deviceCode,
        label: `${item.deviceCode} - ${item.branchName}`
      }))
    }
  },
  created() {
    this.initDeviceData()
  },
  methods: {
    initDeviceData() {
      this.allDeviceData = this.generateMockData()
      this.loadTableData()
    },
    generateMockData() {
      const branches = [
        '市公积金管理中心',
        '朝阳区公积金服务网点',
        '海淀区公积金服务网点',
        '西城区公积金服务网点',
        '东城区公积金服务网点',
        '丰台区公积金服务网点',
        '通州区公积金服务网点',
        '顺义区公积金服务网点',
        '昌平区公积金服务网点',
        '大兴区公积金服务网点'
      ]
      const locations = [
        '一楼服务大厅左侧',
        '一楼服务大厅右侧',
        '二楼办事大厅入口',
        '二楼办事大厅中间',
        '自助服务区A区',
        '自助服务区B区',
        '办事大厅进门左侧',
        '办事大厅进门右侧'
      ]
      const statuses = ['online', 'offline', 'fault', 'maintenance']
      const moduleStatuses = ['normal', 'warning', 'error', 'offline']
      
      const data = []
      for (let i = 1; i <= 68; i++) {
        data.push({
          id: i,
          deviceCode: `GJJ${String(i).padStart(6, '0')}`,
          branchName: branches[Math.floor(Math.random() * branches.length)],
          installLocation: locations[Math.floor(Math.random() * locations.length)],
          status: statuses[Math.floor(Math.random() * statuses.length)],
          identityModule: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)],
          printModule: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)],
          queryModule: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)],
          lastOnlineTime: this.generateRandomTime()
        })
      }
      return data
    },
    generateRandomTime() {
      const now = new Date()
      const past = new Date(now.getTime() - Math.random() * 7 * 24 * 60 * 60 * 1000)
      return past.toLocaleString('zh-CN')
    },
    loadTableData() {
      this.loading = true
      setTimeout(() => {
        let filteredData = [...this.allDeviceData]
        
        if (this.searchForm.status) {
          filteredData = filteredData.filter(item => item.status === this.searchForm.status)
        }
        
        if (this.searchForm.keyword) {
          const keyword = this.searchForm.keyword.toLowerCase().trim()
          filteredData = filteredData.filter(item => 
            item.deviceCode.toLowerCase().includes(keyword) ||
            item.branchName.toLowerCase().includes(keyword) ||
            item.installLocation.toLowerCase().includes(keyword)
          )
        }
        
        this.pagination.total = filteredData.length
        
        const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
        const end = start + this.pagination.pageSize
        this.tableData = filteredData.slice(start, end)
        
        this.loading = false
      }, 300)
    },
    tableRowClassName({ row }) {
      if (row.status === 'fault') {
        return 'fault-row'
      }
      if (row.status === 'offline') {
        return 'offline-row'
      }
      if (row.status === 'maintenance') {
        return 'maintenance-row'
      }
      return ''
    },
    getModuleStatusType(status) {
      const map = {
        normal: 'success',
        warning: 'warning',
        error: 'danger',
        offline: 'info'
      }
      return map[status] || 'info'
    },
    getModuleStatusText(status) {
      const map = {
        normal: '正常',
        warning: '异常',
        error: '故障',
        offline: '离线'
      }
      return map[status] || '未知'
    },
    handleStatusChange(row, newStatus) {
      this.$confirm(`确认将设备 ${row.deviceCode} 状态变更为「${this.getStatusText(newStatus)}」吗？`, '状态变更确认', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const device = this.allDeviceData.find(item => item.id === row.id)
        if (device) {
          device.status = newStatus
          this.loadTableData()
          this.$message.success(`设备 ${device.deviceCode} 状态已更新为「${this.getStatusText(newStatus)}」`)
        }
      }).catch(() => {
      })
    },
    handleSearch() {
      this.pagination.currentPage = 1
      this.loadTableData()
    },
    handleReset() {
      this.searchForm = {
        keyword: '',
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
    getStatusType(status) {
      const map = {
        online: 'success',
        offline: 'info',
        fault: 'danger',
        maintenance: 'warning'
      }
      return map[status] || 'info'
    },
    getStatusEffect(status) {
      return status === 'fault' ? 'dark' : 'light'
    },
    getStatusText(status) {
      const map = {
        online: '在线',
        offline: '离线',
        fault: '故障',
        maintenance: '维护中'
      }
      return map[status] || '未知'
    },
    openFaultReport() {
      this.$refs.faultReportDialog.open()
    },
    handleFaultReport(row) {
      this.$refs.faultReportDialog.open(row.deviceCode)
    },
    handleSubmitFault(data) {
      console.log('故障上报数据:', data)
      this.$message.success(`工单 ${data.orderNo} 提交成功！`)
    }
  }
}
</script>

<style scoped>
.device-list-container {
  width: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  font-weight: 500;
}

.search-bar {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f9fafc;
  border-radius: 4px;
}

.search-form {
  margin-bottom: 0;
}

.pagination-container {
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
  background-color: #e9e9eb !important;
}

.el-table .maintenance-row {
  background-color: #fdf6ec !important;
}

.el-table .maintenance-row:hover > td {
  background-color: #faecd8 !important;
}

.el-dropdown-link {
  cursor: pointer;
  color: #409EFF;
  font-size: 12px;
}

.el-dropdown-link:hover {
  color: #66b1ff;
}
</style>
