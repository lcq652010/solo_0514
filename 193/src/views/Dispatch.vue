<template>
  <div class="page-container">
    <el-row :gutter="20">
      <el-col :span="14">
        <el-card>
          <div slot="header" class="clearfix">
            <span>待调度运单</span>
            <el-tag type="danger" style="float: right">{{ pendingOrders.length }} 单</el-tag>
          </div>
          <el-table :data="pendingOrders" border style="width: 100%" height="500" @row-click="handleOrderSelect" highlight-current-row>
            <el-table-column type="radio" width="50"></el-table-column>
            <el-table-column prop="orderNo" label="运单号" width="140" align="center"></el-table-column>
            <el-table-column label="货物信息" align="center">
              <template slot-scope="scope">
                <div>{{ scope.row.goodsName }}</div>
                <div style="font-size: 12px; color: #909399">
                  {{ scope.row.goodsWeight }}吨 / {{ scope.row.goodsVolume }}m³
                </div>
              </template>
            </el-table-column>
            <el-table-column label="收发货信息" align="center">
              <template slot-scope="scope">
                <div>发: {{ scope.row.sender }}</div>
                <div style="font-size: 12px; color: #909399">收: {{ scope.row.receiver }}</div>
              </template>
            </el-table-column>
            <el-table-column label="运输时段" align="center" width="180">
              <template slot-scope="scope">
                <div>{{ scope.row.transportStartTime || '待设置' }}</div>
                <div style="font-size: 12px; color: #909399">至 {{ scope.row.transportEndTime || scope.row.requireTime }}</div>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>

      <el-col :span="10">
        <el-card>
          <div slot="header" class="clearfix">
            <span>车辆列表</span>
            <el-tag type="success" style="float: right; margin-right: 5px">{{ availableVehicles.length }} 空闲</el-tag>
            <el-tag type="warning" style="float: right">{{ busyVehicles.length }} 占用</el-tag>
          </div>
          <el-table :data="vehicles" border style="width: 100%" height="500" @row-click="handleVehicleSelect" highlight-current-row>
            <el-table-column type="radio" width="50">
              <template slot-scope="scope">
                <el-radio
                  v-model="selectedVehicleId"
                  :label="scope.row.id"
                  :disabled="scope.row.status !== '空闲'">
                </el-radio>
              </template>
            </el-table-column>
            <el-table-column prop="plateNumber" label="车牌号" width="100" align="center"></el-table-column>
            <el-table-column prop="type" label="车型" width="100" align="center"></el-table-column>
            <el-table-column prop="status" label="状态" width="80" align="center">
              <template slot-scope="scope">
                <el-tag :type="scope.row.status === '空闲' ? 'success' : 'warning'" size="small">
                  {{ scope.row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="占用时段" align="center">
              <template slot-scope="scope">
                <div v-if="scope.row.status !== '空闲'" style="font-size: 12px">
                  <div>{{ getVehicleOccupiedTime(scope.row.id).start }}</div>
                  <div style="color: #E6A23C">至 {{ getVehicleOccupiedTime(scope.row.id).end }}</div>
                </div>
                <span v-else style="color: #67C23A; font-size: 12px">全天可用</span>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <el-card style="margin-top: 20px">
      <div slot="header" class="clearfix">
        <span>调度操作</span>
      </div>
      <el-form :inline="true" :model="dispatchForm" label-width="100px">
        <el-form-item label="选中运单">
          <el-input v-model="selectedOrderInfo" readonly style="width: 300px"></el-input>
        </el-form-item>
        <el-form-item label="分配车辆">
          <el-input v-model="selectedVehicleInfo" readonly style="width: 300px"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" size="large" @click="handleDispatch" :disabled="!canDispatch">
            <i class="el-icon-check"></i> 确认调度
          </el-button>
          <el-button size="large" @click="handleClear">
            <i class="el-icon-refresh"></i> 重置选择
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card style="margin-top: 20px">
      <div slot="header" class="clearfix">
        <span>已调度运单</span>
      </div>
      <el-table :data="dispatchedOrders" border style="width: 100%">
        <el-table-column prop="orderNo" label="运单号" width="140" align="center"></el-table-column>
        <el-table-column prop="goodsName" label="货物名称" align="center"></el-table-column>
        <el-table-column label="分配车辆" align="center">
          <template slot-scope="scope">
            <div>{{ getVehicleInfo(scope.row.vehicleId).plateNumber }}</div>
            <div style="font-size: 12px; color: #909399">{{ getVehicleInfo(scope.row.vehicleId).driver }}</div>
          </template>
        </el-table-column>
        <el-table-column prop="sender" label="发货方" align="center"></el-table-column>
        <el-table-column prop="receiver" label="收货方" align="center"></el-table-column>
        <el-table-column prop="requireTime" label="要求到达" width="110" align="center"></el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag type="primary" size="small">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" align="center">
          <template slot-scope="scope">
            <el-button type="warning" size="mini" @click="handleStartTransport(scope.row)" v-if="scope.row.status === '已调度'">
              开始运输
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { orderApi, vehicleApi, mockVehicles } from '../api/mockData'

export default {
  name: 'Dispatch',
  data() {
    return {
      orders: [],
      vehicles: [],
      selectedOrder: null,
      selectedVehicle: null,
      selectedVehicleId: null,
      dispatchForm: {
        orderId: null,
        vehicleId: null
      },
      conflictCheckResult: null
    }
  },
  computed: {
    pendingOrders() {
      return this.orders.filter(o => o.status === '待调度')
    },
    dispatchedOrders() {
      return this.orders.filter(o => o.status === '已调度' || o.status === '在途')
    },
    availableVehicles() {
      return this.vehicles.filter(v => v.status === '空闲')
    },
    busyVehicles() {
      return this.vehicles.filter(v => v.status !== '空闲')
    },
    selectedOrderInfo() {
      return this.selectedOrder ? `${this.selectedOrder.orderNo} - ${this.selectedOrder.goodsName}` : '请在上方表格选择运单'
    },
    selectedVehicleInfo() {
      return this.selectedVehicle ? `${this.selectedVehicle.plateNumber} - ${this.selectedVehicle.driver}` : '请在上方表格选择车辆'
    },
    canDispatch() {
      return this.selectedOrder && this.selectedVehicle && this.selectedVehicle.status === '空闲' && !this.conflictCheckResult
    }
  },
  mounted() {
    this.loadData()
  },
  methods: {
    async loadData() {
      this.orders = await orderApi.getList()
      const vehiclesData = await vehicleApi.getList()
      const dispatchedVehicleIds = [...new Set(this.orders.filter(o => o.vehicleId).map(o => o.vehicleId))]
      this.vehicles = vehiclesData.map(v => {
        if (dispatchedVehicleIds.includes(v.id) && v.status === '空闲') {
          return { ...v, status: '已分配' }
        }
        return v
      })
    },
    handleOrderSelect(row) {
      this.selectedOrder = row
      this.dispatchForm.orderId = row.id
      this.checkTimeConflict()
    },
    handleVehicleSelect(row) {
      if (row.status !== '空闲') {
        this.$message.warning(`${row.plateNumber} 车辆当前已被占用，无法选择`)
        return
      }
      this.selectedVehicle = row
      this.selectedVehicleId = row.id
      this.dispatchForm.vehicleId = row.id
      this.checkTimeConflict()
    },
    checkTimeConflict() {
      if (!this.selectedOrder || !this.selectedVehicle) {
        this.conflictCheckResult = null
        return
      }
      
      const vehicleBusyOrders = this.orders.filter(o => 
        o.vehicleId === this.selectedVehicle.id && 
        (o.status === '已调度' || o.status === '在途')
      )
      
      if (vehicleBusyOrders.length > 0) {
        this.conflictCheckResult = {
          hasConflict: true,
          message: `车辆 ${this.selectedVehicle.plateNumber} 当前正在执行运单 ${vehicleBusyOrders[0].orderNo}`,
          conflictOrder: vehicleBusyOrders[0]
        }
        this.$message.error(this.conflictCheckResult.message)
      } else {
        this.conflictCheckResult = null
      }
    },
    getVehicleOccupiedTime(vehicleId) {
      const busyOrder = this.orders.find(o => 
        o.vehicleId === vehicleId && 
        (o.status === '已调度' || o.status === '在途')
      )
      if (busyOrder) {
        return {
          start: busyOrder.createTime ? busyOrder.createTime.split(' ')[0] : busyOrder.requireTime,
          end: busyOrder.requireTime
        }
      }
      return { start: '-', end: '-' }
    },
    async handleDispatch() {
      if (!this.selectedOrder) {
        this.$message.warning('请先选择运单')
        return
      }
      if (!this.selectedVehicle) {
        this.$message.warning('请先选择车辆')
        return
      }
      if (this.selectedVehicle.status !== '空闲') {
        this.$message.warning('该车辆已被占用，请选择其他车辆')
        return
      }
      
      this.checkTimeConflict()
      if (this.conflictCheckResult) {
        this.$message.error(this.conflictCheckResult.message)
        return
      }
      
      this.$confirm(`确认将运单 ${this.selectedOrder.orderNo} 分配给 ${this.selectedVehicle.plateNumber} 车辆?`, '调度确认', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await orderApi.dispatch(this.selectedOrder.id, this.selectedVehicle.id)
          const vehicleIndex = this.vehicles.findIndex(v => v.id === this.selectedVehicle.id)
          if (vehicleIndex > -1) {
            this.vehicles[vehicleIndex].status = '在途'
          }
          this.$message.success('调度成功！')
          this.handleClear()
          this.loadData()
        } catch (error) {
          this.$message.error('调度失败，请重试')
        }
      }).catch(() => {})
    },
    handleClear() {
      this.selectedOrder = null
      this.selectedVehicle = null
      this.selectedVehicleId = null
      this.conflictCheckResult = null
      this.dispatchForm = {
        orderId: null,
        vehicleId: null
      }
    },
    getVehicleInfo(vehicleId) {
      const vehicle = mockVehicles.find(v => v.id === vehicleId)
      return vehicle || { plateNumber: '-', driver: '-' }
    },
    async handleStartTransport(row) {
      this.$confirm('确认开始运输?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        await orderApi.updateStatus(row.id, '在途')
        this.$message.success('运输已开始！')
        this.loadData()
      }).catch(() => {})
    }
  }
}
</script>

<style scoped>
</style>
