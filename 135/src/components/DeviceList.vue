<template>
  <div class="device-list">
    <el-card>
      <div slot="header" class="card-header">
        <span>设备列表</span>
        <el-button type="primary" icon="el-icon-plus" @click="handleAddReport">
          故障上报
        </el-button>
      </div>

      <div class="search-bar">
        <el-input
          v-model="searchForm.deviceCode"
          placeholder="请输入设备编号"
          prefix-icon="el-icon-search"
          style="width: 250px; margin-right: 15px;"
          clearable
          @input="handleSearch"
        ></el-input>
        <el-input
          v-model="searchForm.servicePoint"
          placeholder="请输入服务点名称"
          prefix-icon="el-icon-search"
          style="width: 250px; margin-right: 15px;"
          clearable
          @input="handleSearch"
        ></el-input>
        <el-button type="primary" @click="handleSearch">搜索</el-button>
        <el-button @click="handleReset">重置</el-button>
      </div>

      <el-table
        :data="tableData"
        border
        style="width: 100%; margin-top: 20px;"
        v-loading="loading"
      >
        <el-table-column
          prop="deviceCode"
          label="设备编号"
          width="150"
          align="center"
        ></el-table-column>
        <el-table-column
          prop="servicePoint"
          label="政务服务点"
          min-width="200"
          align="center"
        ></el-table-column>
        <el-table-column
          prop="location"
          label="安放位置"
          min-width="250"
          align="center"
        ></el-table-column>
        <el-table-column
          prop="status"
          label="设备状态"
          width="120"
          align="center"
        >
          <template slot-scope="scope">
            <span :class="getStatusClass(scope.row.status)">
              {{ scope.row.status }}
            </span>
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
              @click="handleReportFault(scope.row)"
              :disabled="scope.row.status === '正常'"
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
    </el-card>
  </div>
</template>

<script>
import { mockDeviceList } from '../mockData'

export default {
  name: 'DeviceList',
  data() {
    return {
      loading: false,
      searchForm: {
        deviceCode: '',
        servicePoint: ''
      },
      allDeviceList: [],
      filteredList: [],
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
      return this.filteredList.slice(start, end)
    }
  },
  created() {
    this.fetchDeviceList()
  },
  methods: {
    fetchDeviceList() {
      this.loading = true
      setTimeout(() => {
        this.allDeviceList = mockDeviceList
        this.filteredList = [...this.allDeviceList]
        this.pagination.total = this.filteredList.length
        this.loading = false
      }, 500)
    },
    getStatusClass(status) {
      const statusMap = {
        '正常': 'status-normal',
        '故障': 'status-fault',
        '离线': 'status-offline',
        '维护中': 'status-maintenance'
      }
      return statusMap[status] || ''
    },
    handleSearch() {
      this.pagination.currentPage = 1
      this.filteredList = this.allDeviceList.filter(item => {
        const matchCode = !this.searchForm.deviceCode || 
          item.deviceCode.toLowerCase().includes(this.searchForm.deviceCode.toLowerCase())
        const matchPoint = !this.searchForm.servicePoint || 
          item.servicePoint.toLowerCase().includes(this.searchForm.servicePoint.toLowerCase())
        return matchCode && matchPoint
      })
      this.pagination.total = this.filteredList.length
    },
    handleReset() {
      this.searchForm = {
        deviceCode: '',
        servicePoint: ''
      }
      this.handleSearch()
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.pagination.currentPage = 1
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
    },
    handleReportFault(device) {
      this.$emit('report-fault', device)
    },
    handleAddReport() {
      this.$emit('report-fault', null)
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

.search-bar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
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

.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
