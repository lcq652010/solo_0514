<template>
  <div class="device-list">
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form" @submit.native.prevent>
        <el-form-item label="设备编号">
          <el-input
            v-model="searchForm.deviceCode"
            placeholder="请输入设备编号关键词"
            clearable
            style="width: 200px"
            @keyup.enter.native="handleSearch"
          ></el-input>
        </el-form-item>
        <el-form-item label="社区名称">
          <el-input
            v-model="searchForm.community"
            placeholder="请输入社区名称关键词"
            clearable
            style="width: 200px"
            @keyup.enter.native="handleSearch"
          ></el-input>
        </el-form-item>
        <el-form-item label="安放点位">
          <el-input
            v-model="searchForm.location"
            placeholder="请输入点位关键词"
            clearable
            style="width: 200px"
            @keyup.enter.native="handleSearch"
          ></el-input>
        </el-form-item>
        <el-form-item label="设备状态">
          <el-select
            v-model="searchForm.status"
            placeholder="全部状态"
            clearable
            style="width: 140px"
          >
            <el-option
              v-for="status in statusOptions"
              :key="status.value"
              :label="status.label"
              :value="status.value"
            >
              <span style="display: flex; align-items: center; gap: 6px;">
                <el-tag :type="status.type" size="mini" effect="light">{{ status.label }}</el-tag>
              </span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
          <el-button icon="el-icon-refresh" @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card">
      <div class="table-header">
        <div class="table-title">
          <i class="el-icon-s-platform"></i>
          <span>设备列表</span>
          <span class="count-badge">共 {{ total }} 台</span>
          <span v-if="isSearching" class="search-badge">
            筛选中
            <i class="el-icon-close" @click="handleReset"></i>
          </span>
        </div>
        <div class="table-actions">
          <el-button icon="el-icon-printer" @click="handlePrint">
            凭证打印
          </el-button>
          <el-button type="danger" icon="el-icon-warning" @click="openFaultReport">
            故障上报
          </el-button>
        </div>
      </div>

      <el-table
        :data="paginatedDevices"
        border
        stripe
        style="width: 100%"
        v-loading="loading"
        :row-class-name="tableRowClassName"
        highlight-current-row
        @row-click="handleRowClick"
        ref="deviceTable"
      >
        <el-table-column type="index" label="序号" width="60" align="center">
          <template slot-scope="scope">
            {{ (currentPage - 1) * pageSize + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column prop="deviceCode" label="设备编号" width="180" align="center">
          <template slot-scope="scope">
            <span class="device-code" :class="{ 'highlight': isMatchKeyword(scope.row.deviceCode) }">
              {{ scope.row.deviceCode }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="community" label="所属社区" min-width="160" align="center">
          <template slot-scope="scope">
            <span :class="{ 'highlight': isMatchKeyword(scope.row.community) }">
              {{ scope.row.community }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="location" label="安放点位" min-width="180" align="center">
          <template slot-scope="scope">
            <span :class="{ 'highlight': isMatchKeyword(scope.row.location) }">
              {{ scope.row.location }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="模块状态" min-width="240" align="center">
          <template slot-scope="scope">
            <div class="module-status">
              <el-tooltip content="信息查询模块" placement="top">
                <span :class="['module-item', scope.row.modules.infoQuery ? 'module-online' : 'module-offline']">
                  <i class="el-icon-search"></i>
                </span>
              </el-tooltip>
              <el-tooltip content="凭证打印模块" placement="top">
                <span :class="['module-item', scope.row.modules.printing ? 'module-online' : 'module-offline']">
                  <i class="el-icon-printer"></i>
                </span>
              </el-tooltip>
              <el-tooltip content="网络连接" placement="top">
                <span :class="['module-item', scope.row.modules.network ? 'module-online' : 'module-offline']">
                  <i class="el-icon-connection"></i>
                </span>
              </el-tooltip>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="statusText" label="运行状态" width="120" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)" effect="light" size="medium">
              <i :class="getStatusIcon(scope.row.status)"></i>
              {{ scope.row.statusText }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="lastOnline" label="最后在线时间" width="180" align="center"></el-table-column>
        <el-table-column prop="installDate" label="安装日期" width="140" align="center"></el-table-column>
        <el-table-column label="操作" width="180" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button type="text" size="small" icon="el-icon-view" @click="handleViewDetail(scope.row)">详情</el-button>
            <el-button
              type="text"
              size="small"
              icon="el-icon-warning"
              class="fault-btn"
              @click="openFaultReport(scope.row)"
            >
              报障
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrapper">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page.sync="currentPage"
          :page-sizes="[10, 20, 50]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          background
        >
        </el-pagination>
      </div>
    </el-card>

    <fault-report-modal
      :visible.sync="faultModalVisible"
      :selected-device="selectedDevice"
      :device-list="allDevices"
      @close="handleFaultClose"
      @submit="handleFaultSubmit"
    ></fault-report-modal>

    <el-dialog
      title="设备详情"
      :visible.sync="detailVisible"
      width="600px"
      v-if="currentDevice"
    >
      <el-descriptions :column="2" border>
        <el-descriptions-item label="设备编号">
          <span class="detail-code">{{ currentDevice.deviceCode }}</span>
        </el-descriptions-item>
        <el-descriptions-item label="所属社区">
          {{ currentDevice.community }}
        </el-descriptions-item>
        <el-descriptions-item label="安放点位">
          {{ currentDevice.location }}
        </el-descriptions-item>
        <el-descriptions-item label="运行状态">
          <el-tag :type="getStatusType(currentDevice.status)" size="small">
            {{ currentDevice.statusText }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="安装日期">
          {{ currentDevice.installDate }}
        </el-descriptions-item>
        <el-descriptions-item label="最后在线">
          {{ currentDevice.lastOnline }}
        </el-descriptions-item>
        <el-descriptions-item label="模块状态" :span="2">
          <div class="detail-modules">
            <div class="detail-module-item">
              <span :class="['module-icon', currentDevice.modules.infoQuery ? 'online' : 'offline']">
                <i class="el-icon-search"></i>
              </span>
              <span class="module-label">信息查询</span>
              <span class="module-status-text">
                {{ currentDevice.modules.infoQuery ? '正常' : '异常' }}
              </span>
            </div>
            <div class="detail-module-item">
              <span :class="['module-icon', currentDevice.modules.printing ? 'online' : 'offline']">
                <i class="el-icon-printer"></i>
              </span>
              <span class="module-label">凭证打印</span>
              <span class="module-status-text">
                {{ currentDevice.modules.printing ? '正常' : '异常' }}
              </span>
            </div>
            <div class="detail-module-item">
              <span :class="['module-icon', currentDevice.modules.network ? 'online' : 'offline']">
                <i class="el-icon-connection"></i>
              </span>
              <span class="module-label">网络连接</span>
              <span class="module-status-text">
                {{ currentDevice.modules.network ? '正常' : '异常' }}
              </span>
            </div>
          </div>
        </el-descriptions-item>
      </el-descriptions>
      <div slot="footer" class="dialog-footer">
        <el-button @click="detailVisible = false">关闭</el-button>
        <el-button type="primary" @click="openFaultReport(currentDevice)">故障上报</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { mockDevices, type Device, type WorkOrder } from '@/mock/data'
import { generateWorkOrderNo, formatDate } from '@/utils/workOrder'
import FaultReportModal from '@/components/FaultReportModal.vue'

export default Vue.extend({
  name: 'DeviceList',
  components: {
    FaultReportModal
  },
  data() {
    return {
      loading: false,
      allDevices: [] as Device[],
      searchForm: {
        deviceCode: '',
        community: '',
        location: '',
        status: ''
      },
      currentPage: 1,
      pageSize: 10,
      faultModalVisible: false,
      detailVisible: false,
      selectedDevice: null as Device | null,
      currentDevice: null as Device | null,
      workOrders: [] as WorkOrder[],
      statusOptions: [
        { value: 'running', label: '运行中', type: 'success' },
        { value: 'fault', label: '故障', type: 'danger' },
        { value: 'offline', label: '离线', type: 'info' },
        { value: 'maintenance', label: '维护中', type: 'warning' }
      ]
    }
  },
  computed: {
    isSearching(): boolean {
      return this.searchForm.deviceCode !== '' ||
             this.searchForm.community !== '' ||
             this.searchForm.location !== '' ||
             this.searchForm.status !== ''
    },
    filteredDevices(): Device[] {
      const keywordDevice = this.searchForm.deviceCode.trim().toLowerCase()
      const keywordCommunity = this.searchForm.community.trim()
      const keywordLocation = this.searchForm.location.trim()
      const statusFilter = this.searchForm.status

      return this.allDevices.filter(device => {
        const matchDeviceCode = !keywordDevice ||
          this.isFuzzyMatch(device.deviceCode.toLowerCase(), keywordDevice)
        const matchCommunity = !keywordCommunity ||
          this.isFuzzyMatch(device.community, keywordCommunity)
        const matchLocation = !keywordLocation ||
          this.isFuzzyMatch(device.location, keywordLocation)
        const matchStatus = !statusFilter || device.status === statusFilter
        return matchDeviceCode && matchCommunity && matchLocation && matchStatus
      })
    },
    paginatedDevices(): Device[] {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      const result = this.filteredDevices.slice(start, end)
      return result
    },
    total(): number {
      return this.filteredDevices.length
    }
  },
  watch: {
    'searchForm.deviceCode': function() {
      this.resetPage()
    },
    'searchForm.community': function() {
      this.resetPage()
    },
    'searchForm.location': function() {
      this.resetPage()
    },
    'searchForm.status': function() {
      this.resetPage()
    },
    filteredDevices: function() {
      this.$nextTick(() => {
        const table = this.$refs.deviceTable as any
        if (table) {
          table.doLayout()
        }
      })
    }
  },
  mounted() {
    this.loadData()
  },
  methods: {
    loadData() {
      this.loading = true
      setTimeout(() => {
        this.allDevices = mockDevices.map(device => ({
          ...device,
          modules: {
            infoQuery: device.status === 'running' ? Math.random() > 0.1 : false,
            printing: device.status === 'running' ? Math.random() > 0.15 : false,
            network: device.status === 'running'
          }
        }))
        this.loading = false
      }, 300)
    },
    resetPage() {
      this.currentPage = 1
    },
    isFuzzyMatch(source: string, keyword: string): boolean {
      if (!keyword) return true
      const chars = keyword.split('')
      let lastIndex = -1
      for (const char of chars) {
        const index = source.indexOf(char, lastIndex + 1)
        if (index === -1) {
          return false
        }
        lastIndex = index
      }
      return true
    },
    isMatchKeyword(text: string): boolean {
      const keywordDevice = this.searchForm.deviceCode.trim().toLowerCase()
      const keywordCommunity = this.searchForm.community.trim()
      const keywordLocation = this.searchForm.location.trim()
      
      const lowerText = text.toLowerCase()
      return lowerText.includes(keywordDevice) ||
             text.includes(keywordCommunity) ||
             text.includes(keywordLocation)
    },
    getStatusType(status: string): string {
      const typeMap: Record<string, string> = {
        running: 'success',
        fault: 'danger',
        offline: 'info',
        maintenance: 'warning'
      }
      return typeMap[status] || 'info'
    },
    getStatusIcon(status: string): string {
      const iconMap: Record<string, string> = {
        running: 'el-icon-circle-check',
        fault: 'el-icon-circle-close',
        offline: 'el-icon-time',
        maintenance: 'el-icon-setting'
      }
      return iconMap[status] || 'el-icon-question'
    },
    tableRowClassName({ row }: { row: Device }): string {
      if (row.status === 'fault') {
        return 'row-fault'
      } else if (row.status === 'offline') {
        return 'row-offline'
      } else if (row.status === 'maintenance') {
        return 'row-maintenance'
      }
      return ''
    },
    handleSearch() {
      this.resetPage()
    },
    handleReset() {
      this.searchForm.deviceCode = ''
      this.searchForm.community = ''
      this.searchForm.location = ''
      this.searchForm.status = ''
      this.resetPage()
    },
    handleSizeChange(val: number) {
      this.pageSize = val
      this.resetPage()
    },
    handleCurrentChange(val: number) {
      this.loading = true
      this.currentPage = val
      this.$nextTick(() => {
        setTimeout(() => {
          this.loading = false
        }, 150)
      })
    },
    handleRowClick(row: Device) {
      this.currentDevice = row
    },
    handleViewDetail(row: Device) {
      this.currentDevice = row
      this.detailVisible = true
    },
    handlePrint() {
      this.$message.info('凭证打印功能开发中...')
    },
    openFaultReport(device?: Device) {
      this.selectedDevice = device || null
      this.faultModalVisible = true
    },
    handleFaultClose() {
      this.faultModalVisible = false
      this.selectedDevice = null
    },
    handleFaultSubmit(deviceCode: string, faultDescription: string) {
      const device = this.allDevices.find(d => d.deviceCode === deviceCode)
      if (device) {
        const workOrder: WorkOrder = {
          id: this.workOrders.length + 1,
          workOrderNo: generateWorkOrderNo(),
          deviceCode: deviceCode,
          community: device.community,
          faultDescription: faultDescription,
          reportTime: formatDate(new Date()),
          status: 'pending',
          statusText: '待处理'
        }
        this.workOrders.push(workOrder)
        
        device.status = 'fault'
        device.statusText = '故障'
        device.modules = {
          infoQuery: false,
          printing: false,
          network: false
        }
        
        this.$message({
          message: `故障上报成功！工单号：${workOrder.workOrderNo}`,
          type: 'success',
          duration: 4000
        })

        this.$nextTick(() => {
          const table = this.$refs.deviceTable as any
          if (table) {
            table.doLayout()
          }
        })
      }
      this.faultModalVisible = false
      this.selectedDevice = null
    }
  }
})
</script>

<style scoped>
.device-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.search-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.search-form {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
}

.table-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.table-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.table-title i {
  font-size: 22px;
  color: #1890ff;
}

.table-actions {
  display: flex;
  gap: 10px;
}

.count-badge {
  font-size: 14px;
  font-weight: normal;
  color: #909399;
  background: #f0f2f5;
  padding: 4px 12px;
  border-radius: 12px;
}

.search-badge {
  font-size: 12px;
  font-weight: normal;
  color: #1890ff;
  background: #e6f7ff;
  border: 1px solid #91d5ff;
  padding: 2px 10px;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
}

.search-badge:hover {
  background: #bae7ff;
}

.highlight {
  background: linear-gradient(120deg, #fffbe6 0%, #fff1b8 100%);
  padding: 2px 6px;
  border-radius: 4px;
  color: #d46b08;
  font-weight: 500;
}

.device-code {
  font-family: 'Courier New', monospace;
  font-weight: 600;
  color: #1890ff;
}

.module-status {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
}

.module-item {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.module-item:hover {
  transform: scale(1.1);
}

.module-online {
  background: #f6ffed;
  color: #52c41a;
  border: 1px solid #b7eb8f;
}

.module-offline {
  background: #fff1f0;
  color: #ff4d4f;
  border: 1px solid #ffa39e;
}

.fault-btn {
  color: #ff4d4f !important;
}

.fault-btn:hover {
  color: #ff7875 !important;
}

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.detail-code {
  font-family: 'Courier New', monospace;
  font-weight: 600;
  color: #1890ff;
  font-size: 16px;
}

.detail-modules {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detail-module-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  background: #fafafa;
  border-radius: 6px;
}

.module-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.module-icon.online {
  background: #f6ffed;
  color: #52c41a;
}

.module-icon.offline {
  background: #fff1f0;
  color: #ff4d4f;
}

.module-label {
  min-width: 80px;
  color: #606266;
}

.module-status-text {
  font-weight: 500;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

::v-deep .el-table .cell {
  text-align: center;
}

::v-deep .el-table .row-fault {
  background: linear-gradient(90deg, #fff1f0 0%, #fff 100%) !important;
}

::v-deep .el-table .row-fault:hover > td {
  background: #fff1f0 !important;
}

::v-deep .el-table .row-offline {
  background: linear-gradient(90deg, #fafafa 0%, #fff 100%) !important;
}

::v-deep .el-table .row-offline:hover > td {
  background: #f5f5f5 !important;
}

::v-deep .el-table .row-maintenance {
  background: linear-gradient(90deg, #fff7e6 0%, #fff 100%) !important;
}

::v-deep .el-table .row-maintenance:hover > td {
  background: #fff7e6 !important;
}

::v-deep .el-table .current-row td {
  background: #e6f7ff !important;
}

::v-deep .el-tag {
  border-radius: 4px;
  font-weight: 500;
}

::v-deep .el-tag i {
  margin-right: 4px;
}

::v-deep .el-tag--success {
  background: #f6ffed;
  border-color: #b7eb8f;
  color: #52c41a;
}

::v-deep .el-tag--danger {
  background: #fff1f0;
  border-color: #ffa39e;
  color: #ff4d4f;
}

::v-deep .el-tag--warning {
  background: #fff7e6;
  border-color: #ffd591;
  color: #fa8c16;
}

::v-deep .el-tag--info {
  background: #f5f5f5;
  border-color: #d9d9d9;
  color: #8c8c8c;
}

::v-deep .el-descriptions__label {
  font-weight: 500;
  color: #606266;
}
</style>
