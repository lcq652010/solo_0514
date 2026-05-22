<template>
  <div class="work-order-list">
    <div class="page-header">
      <div class="page-title">工单管理</div>
      <div class="page-desc">查看和管理所有故障工单，追踪工单处理进度</div>
    </div>

    <div class="card-container">
      <div class="search-bar">
        <el-input
          v-model="searchForm.workOrderNo"
          placeholder="请输入工单编号"
          clearable
          style="width: 220px"
          prefix-icon="el-icon-document"
          @keyup.enter.native="handleSearch"
        />
        <el-input
          v-model="searchForm.deviceNo"
          placeholder="请输入设备编号"
          clearable
          style="width: 220px"
          prefix-icon="el-icon-monitor"
          @keyup.enter.native="handleSearch"
        />
        <el-select
          v-model="searchForm.status"
          placeholder="工单状态"
          clearable
          style="width: 160px"
        >
          <el-option label="待处理" value="pending" />
          <el-option label="处理中" value="processing" />
          <el-option label="已解决" value="resolved" />
          <el-option label="已关闭" value="closed" />
        </el-select>
        <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
        <el-button icon="el-icon-refresh" @click="handleReset">重置</el-button>
      </div>

      <div class="table-wrapper">
        <el-table
          :data="tableData"
          border
          stripe
          style="width: 100%"
          v-loading="loading"
        >
          <el-table-column
            prop="workOrderNo"
            label="工单编号"
            width="190"
            align="center"
          />
          <el-table-column
            prop="deviceNo"
            label="设备编号"
            width="120"
            align="center"
          />
          <el-table-column
            prop="organization"
            label="人才服务中心"
            min-width="180"
            show-overflow-tooltip
          />
          <el-table-column
            prop="problemDesc"
            label="问题描述"
            min-width="240"
            show-overflow-tooltip
          />
          <el-table-column
            prop="status"
            label="工单状态"
            width="110"
            align="center"
          >
            <template slot-scope="scope">
              <el-tag :type="getWorkOrderStatusType(scope.row.status)" effect="light">
                {{ getWorkOrderStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column
            prop="createTime"
            label="创建时间"
            width="170"
            align="center"
          >
            <template slot-scope="scope">
              {{ formatDate(scope.row.createTime) }}
            </template>
          </el-table-column>
          <el-table-column
            prop="updateTime"
            label="更新时间"
            width="170"
            align="center"
          >
            <template slot-scope="scope">
              {{ formatDate(scope.row.updateTime) }}
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div class="pagination-wrapper">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pagination.pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
          background
        />
      </div>
    </div>
  </div>
</template>

<script>
import workOrders from '@/mock/workOrder.js'
import {
  formatDate,
  getWorkOrderStatusText,
  getWorkOrderStatusType
} from '@/utils/index.js'

export default {
  name: 'WorkOrderList',
  data() {
    return {
      loading: false,
      searchForm: {
        workOrderNo: '',
        deviceNo: '',
        status: ''
      },
      allWorkOrders: [],
      filteredWorkOrders: [],
      tableData: [],
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      }
    }
  },
  created() {
    this.allWorkOrders = [...workOrders]
    this.filteredWorkOrders = [...this.allWorkOrders]
    this.pagination.total = this.filteredWorkOrders.length
    this.loadTableData()
  },
  methods: {
    formatDate,
    getWorkOrderStatusText,
    getWorkOrderStatusType,
    loadTableData() {
      const { currentPage, pageSize } = this.pagination
      const start = (currentPage - 1) * pageSize
      const end = start + pageSize
      this.tableData = this.filteredWorkOrders.slice(start, end)
    },
    handleSearch() {
      this.loading = true
      setTimeout(() => {
        const { workOrderNo, deviceNo, status } = this.searchForm
        this.filteredWorkOrders = this.allWorkOrders.filter(item => {
          const matchWorkOrderNo = !workOrderNo ||
            item.workOrderNo.toLowerCase().includes(workOrderNo.toLowerCase())
          const matchDeviceNo = !deviceNo ||
            item.deviceNo.toLowerCase().includes(deviceNo.toLowerCase())
          const matchStatus = !status || item.status === status
          return matchWorkOrderNo && matchDeviceNo && matchStatus
        })
        this.pagination.total = this.filteredWorkOrders.length
        this.pagination.currentPage = 1
        this.loadTableData()
        this.loading = false
      }, 300)
    },
    handleReset() {
      this.searchForm = {
        workOrderNo: '',
        deviceNo: '',
        status: ''
      }
      this.handleSearch()
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.pagination.currentPage = 1
      this.loadTableData()
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
      this.loadTableData()
    }
  }
}
</script>

<style lang="scss" scoped>
.work-order-list {
  ::v-deep .el-table th {
    background-color: #fafafa;
    color: #262626;
    font-weight: 600;
  }

  ::v-deep .el-table__row:hover > td {
    background-color: #f5faff;
  }

  ::v-deep .el-tag {
    border: none;
    padding: 0 10px;
  }
}
</style>
