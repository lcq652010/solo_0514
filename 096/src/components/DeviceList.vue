<template>
  <div class="device-list">
    <el-card>
      <div slot="header" class="card-header">
        <span>设备管理</span>
        <el-button type="primary" @click="handleReport">故障上报</el-button>
      </div>
      
      <div class="search-bar">
        <el-input 
          v-model="searchForm.deviceNo" 
          placeholder="请输入设备编号" 
          style="width: 200px; margin-right: 10px;"
          clearable
        ></el-input>
        <el-input 
          v-model="searchForm.hallName" 
          placeholder="请输入政务大厅名称" 
          style="width: 200px; margin-right: 10px;"
          clearable
        ></el-input>
        <el-select 
          v-model="searchForm.status" 
          placeholder="设备状态筛选" 
          style="width: 150px; margin-right: 10px;"
          clearable
        >
          <el-option label="全部" value=""></el-option>
          <el-option label="正常" value="正常"></el-option>
          <el-option label="故障" value="故障"></el-option>
          <el-option label="离线" value="离线"></el-option>
          <el-option label="维护中" value="维护中"></el-option>
        </el-select>
        <el-button type="primary" @click="handleSearch">搜索</el-button>
        <el-button @click="handleReset">重置</el-button>
      </div>

      <el-table :data="tableData" border style="width: 100%; margin-top: 20px;" :row-class-name="tableRowClassName">
        <el-table-column prop="deviceNo" label="设备编号" width="130"></el-table-column>
        <el-table-column prop="hallName" label="所属政务大厅" min-width="180"></el-table-column>
        <el-table-column prop="window" label="摆放窗口" width="130"></el-table-column>
        <el-table-column prop="status" label="设备状态" width="100">
          <template slot-scope="scope">
            <span :class="getStatusClass(scope.row.status)">
              {{ scope.row.status }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="idCardReader" label="身份证阅读器" width="120">
          <template slot-scope="scope">
            <span :class="getStatusClass(scope.row.idCardReader)">
              {{ scope.row.idCardReader }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="printer" label="打印机" width="100">
          <template slot-scope="scope">
            <span :class="getStatusClass(scope.row.printer)">
              {{ scope.row.printer }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="encryptModule" label="加密模块" width="100">
          <template slot-scope="scope">
            <span :class="getStatusClass(scope.row.encryptModule)">
              {{ scope.row.encryptModule }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="handleReportSingle(scope.row)">故障上报</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.currentPage"
          :page-sizes="[5, 10, 15, 20]"
          :page-size="pagination.pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total">
        </el-pagination>
      </div>
    </el-card>
  </div>
</template>

<script>
import { deviceList } from '../mock/data.js'

export default {
  name: 'DeviceList',
  data() {
    return {
      searchForm: {
        deviceNo: '',
        hallName: '',
        status: ''
      },
      allDevices: [],
      filteredDevices: [],
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      }
    }
  },
  computed: {
    tableData() {
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      return this.filteredDevices.slice(start, end)
    }
  },
  created() {
    this.allDevices = [...deviceList]
    this.filteredDevices = [...deviceList]
    this.pagination.total = this.filteredDevices.length
  },
  methods: {
    tableRowClassName({ row }) {
      if (row.status === '故障') {
        return 'row-fault'
      } else if (row.status === '离线') {
        return 'row-offline'
      }
      return ''
    },
    getStatusClass(status) {
      const classMap = {
        '正常': 'status-normal',
        '故障': 'status-fault',
        '离线': 'status-offline',
        '维护中': 'status-maintenance'
      }
      return classMap[status] || ''
    },
    handleSearch() {
      this.filteredDevices = this.allDevices.filter(device => {
        const matchDeviceNo = !this.searchForm.deviceNo || 
          device.deviceNo.toLowerCase().includes(this.searchForm.deviceNo.toLowerCase())
        const matchHallName = !this.searchForm.hallName || 
          device.hallName.toLowerCase().includes(this.searchForm.hallName.toLowerCase())
        const matchStatus = !this.searchForm.status || device.status === this.searchForm.status
        return matchDeviceNo && matchHallName && matchStatus
      })
      this.pagination.total = this.filteredDevices.length
      this.pagination.currentPage = 1
    },
    handleReset() {
      this.searchForm = {
        deviceNo: '',
        hallName: '',
        status: ''
      }
      this.filteredDevices = [...this.allDevices]
      this.pagination.total = this.filteredDevices.length
      this.pagination.currentPage = 1
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
    },
    handleReport() {
      this.$emit('open-report')
    },
    handleReportSingle(row) {
      this.$emit('open-report', row)
    }
  }
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-bar {
  display: flex;
  align-items: center;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.status-normal {
  color: #67c23a;
  font-weight: bold;
}

.status-fault {
  color: #f56c6c;
  font-weight: bold;
}

.status-offline {
  color: #909399;
  font-weight: bold;
}

.status-maintenance {
  color: #e6a23c;
  font-weight: bold;
}
</style>

<style>
.el-table .row-fault {
  background-color: #fef0f0 !important;
}

.el-table .row-offline {
  background-color: #f5f7fa !important;
}
</style>
