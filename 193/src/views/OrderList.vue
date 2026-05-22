<template>
  <div class="page-container">
    <el-card>
      <div slot="header" class="clearfix">
        <span>运单记录</span>
      </div>

      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="运单号">
          <el-input v-model="searchForm.orderNo" placeholder="请输入运单号" clearable style="width: 150px"></el-input>
        </el-form-item>
        <el-form-item label="运输状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable style="width: 120px">
            <el-option label="待调度" value="待调度"></el-option>
            <el-option label="已调度" value="已调度"></el-option>
            <el-option label="在途" value="在途"></el-option>
            <el-option label="已完成" value="已完成"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="运输线路">
          <el-select v-model="searchForm.routeId" placeholder="请选择线路" clearable style="width: 140px">
            <el-option v-for="route in routeList" :key="route.id" :label="route.name" :value="route.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="选择车辆">
          <el-select v-model="searchForm.vehicleId" placeholder="请选择车辆" clearable style="width: 140px">
            <el-option v-for="vehicle in vehicles" :key="vehicle.id" :label="vehicle.plateNumber" :value="vehicle.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="创建日期">
          <el-date-picker
            v-model="searchForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            style="width: 240px"
            value-format="yyyy-MM-dd">
          </el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <el-row :gutter="20" class="mb20">
        <el-col :span="6">
          <el-statistic title="总运单数" :value="statistics.total" value-style="color: #409EFF">
            <template slot="prefix">
              <i class="el-icon-document"></i>
            </template>
          </el-statistic>
        </el-col>
        <el-col :span="6">
          <el-statistic title="待调度" :value="statistics.pending" value-style="color: #E6A23C">
            <template slot="prefix">
              <i class="el-icon-time"></i>
            </template>
          </el-statistic>
        </el-col>
        <el-col :span="6">
          <el-statistic title="在途" :value="statistics.inTransit" value-style="color: #67C23A">
            <template slot="prefix">
              <i class="el-icon-location"></i>
            </template>
          </el-statistic>
        </el-col>
        <el-col :span="6">
          <el-statistic title="已完成" :value="statistics.completed" value-style="color: #909399">
            <template slot="prefix">
              <i class="el-icon-circle-check"></i>
            </template>
          </el-statistic>
        </el-col>
      </el-row>

      <el-table :data="paginatedOrders" border style="width: 100%" v-loading="loading">
        <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
        <el-table-column prop="orderNo" label="运单号" width="140" align="center"></el-table-column>
        <el-table-column prop="routeName" label="运输线路" width="120" align="center"></el-table-column>
        <el-table-column label="货物信息" align="center" width="150">
          <template slot-scope="scope">
            <div>{{ scope.row.goodsName }}</div>
            <div style="font-size: 12px; color: #909399">
              {{ scope.row.goodsWeight }}吨 / {{ scope.row.goodsVolume }}m³
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="freight" label="运费" width="100" align="center">
          <template slot-scope="scope">
            <span style="color: #F56C6C; font-weight: bold">¥{{ scope.row.freight || 0 }}</span>
          </template>
        </el-table-column>
        <el-table-column label="分配车辆" width="120" align="center">
          <template slot-scope="scope">
            <div v-if="scope.row.vehicleId">{{ getVehicleInfo(scope.row.vehicleId) }}</div>
            <div v-else style="color: #909399">-</div>
          </template>
        </el-table-column>
        <el-table-column prop="sender" label="发货方" align="center" show-overflow-tooltip></el-table-column>
        <el-table-column prop="receiver" label="收货方" align="center" show-overflow-tooltip></el-table-column>
        <el-table-column prop="requireTime" label="要求到达" width="110" align="center"></el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="160" align="center"></el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="small">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button type="primary" size="mini" @click="handleView(scope.row)">查看详情</el-button>
            <el-button type="success" size="mini" @click="handleComplete(scope.row)" v-if="scope.row.status === '在途'">完成运输</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="pagination.currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pagination.pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="pagination.total"
        style="margin-top: 20px; justify-content: flex-end;">
      </el-pagination>
    </el-card>

    <el-dialog title="运单详情" :visible.sync="detailDialogVisible" width="700px">
      <el-descriptions :column="2" border v-if="currentOrder">
        <el-descriptions-item label="运单号" :span="2">{{ currentOrder.orderNo }}</el-descriptions-item>
        <el-descriptions-item label="运输线路">{{ currentOrder.routeName || '-' }}</el-descriptions-item>
        <el-descriptions-item label="运费" contentStyle="color: #F56C6C; font-weight: bold">¥{{ currentOrder.freight || 0 }}</el-descriptions-item>
        <el-descriptions-item label="货物名称">{{ currentOrder.goodsName }}</el-descriptions-item>
        <el-descriptions-item label="货物信息">{{ currentOrder.goodsWeight }}吨 / {{ currentOrder.goodsVolume }}m³</el-descriptions-item>
        <el-descriptions-item label="发货单位" :span="2">{{ currentOrder.sender }}</el-descriptions-item>
        <el-descriptions-item label="发货电话">{{ currentOrder.senderPhone }}</el-descriptions-item>
        <el-descriptions-item label="发货地址" :span="2">{{ currentOrder.senderAddress }}</el-descriptions-item>
        <el-descriptions-item label="收货单位" :span="2">{{ currentOrder.receiver }}</el-descriptions-item>
        <el-descriptions-item label="收货电话">{{ currentOrder.receiverPhone }}</el-descriptions-item>
        <el-descriptions-item label="收货地址" :span="2">{{ currentOrder.receiverAddress }}</el-descriptions-item>
        <el-descriptions-item label="分配车辆">{{ getVehicleInfo(currentOrder.vehicleId) || '-' }}</el-descriptions-item>
        <el-descriptions-item label="要求到达时间">{{ currentOrder.requireTime }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ currentOrder.createTime }}</el-descriptions-item>
        <el-descriptions-item label="运单状态">
          <el-tag :type="getStatusType(currentOrder.status)" size="small">{{ currentOrder.status }}</el-tag>
        </el-descriptions-item>
      </el-descriptions>
      <div slot="footer" class="dialog-footer">
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { orderApi, vehicleApi, routeList } from '../api/mockData'

export default {
  name: 'OrderList',
  data() {
    return {
      loading: false,
      orders: [],
      vehicles: [],
      routeList: routeList,
      searchForm: {
        orderNo: '',
        status: '',
        routeId: null,
        vehicleId: null,
        dateRange: [],
        sender: '',
        receiver: ''
      },
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      detailDialogVisible: false,
      currentOrder: null
    }
  },
  computed: {
    filteredOrders() {
      let list = [...this.orders]
      if (this.searchForm.orderNo) {
        list = list.filter(o => o.orderNo.includes(this.searchForm.orderNo))
      }
      if (this.searchForm.status) {
        list = list.filter(o => o.status === this.searchForm.status)
      }
      if (this.searchForm.routeId) {
        list = list.filter(o => o.routeId === this.searchForm.routeId)
      }
      if (this.searchForm.vehicleId) {
        list = list.filter(o => o.vehicleId === this.searchForm.vehicleId)
      }
      if (this.searchForm.dateRange && this.searchForm.dateRange.length === 2) {
        list = list.filter(o => {
          const orderDate = o.createTime ? o.createTime.split(' ')[0] : ''
          return orderDate >= this.searchForm.dateRange[0] && orderDate <= this.searchForm.dateRange[1]
        })
      }
      if (this.searchForm.sender) {
        list = list.filter(o => o.sender.includes(this.searchForm.sender))
      }
      if (this.searchForm.receiver) {
        list = list.filter(o => o.receiver.includes(this.searchForm.receiver))
      }
      return list
    },
    paginatedOrders() {
      const list = this.filteredOrders
      this.pagination.total = list.length
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      return list.slice(start, end)
    },
    statistics() {
      return {
        total: this.orders.length,
        pending: this.orders.filter(o => o.status === '待调度').length,
        inTransit: this.orders.filter(o => o.status === '在途' || o.status === '已调度').length,
        completed: this.orders.filter(o => o.status === '已完成').length
      }
    }
  },
  mounted() {
    this.loadOrders()
    this.loadVehicles()
  },
  methods: {
    async loadOrders() {
      this.loading = true
      try {
        this.orders = await orderApi.getList()
      } catch (error) {
        this.$message.error('加载运单数据失败')
      } finally {
        this.loading = false
      }
    },
    async loadVehicles() {
      this.vehicles = await vehicleApi.getList()
    },
    getStatusType(status) {
      const typeMap = {
        '待调度': 'warning',
        '已调度': 'primary',
        '在途': 'success',
        '已完成': 'info'
      }
      return typeMap[status] || 'info'
    },
    getVehicleInfo(vehicleId) {
      const vehicle = this.vehicles.find(v => v.id === vehicleId)
      return vehicle ? `${vehicle.plateNumber}(${vehicle.driver})` : '-'
    },
    handleSearch() {
      this.pagination.currentPage = 1
    },
    handleReset() {
      this.searchForm = {
        orderNo: '',
        status: '',
        routeId: null,
        vehicleId: null,
        dateRange: [],
        sender: '',
        receiver: ''
      }
      this.pagination.currentPage = 1
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
    },
    handleView(row) {
      this.currentOrder = row
      this.detailDialogVisible = true
    },
    handleComplete(row) {
      this.$confirm('确认完成该运单运输?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        await orderApi.updateStatus(row.id, '已完成')
        this.$message.success('运单已完成！')
        this.loadOrders()
      }).catch(() => {})
    }
  }
}
</script>

<style scoped>
.search-form {
  margin-bottom: 20px;
}
.mb20 {
  margin-bottom: 20px;
}
</style>
