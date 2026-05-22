<template>
  <div class="device-management">
    <div class="page-header">
      <h2 class="page-title">设备管理</h2>
      <p class="page-desc">管理和监控图书馆自助电子借阅下载终端设备</p>
    </div>

    <SearchBar
      @search="handleSearch"
      @reset="handleReset"
    />

    <DeviceTable
      :data="filteredDevices"
      :loading="loading"
      @repair="handleRepair"
    />

    <RepairModal
      :visible.sync="repairModalVisible"
      :device="selectedDevice"
      :devices="devices"
      @submit="handleRepairSubmit"
    />
  </div>
</template>

<script>
import SearchBar from '@/components/SearchBar.vue'
import DeviceTable from '@/components/DeviceTable.vue'
import RepairModal from '@/components/RepairModal.vue'
import mockDevices from '@/mock/devices.js'

export default {
  name: 'DeviceManagement',
  components: {
    SearchBar,
    DeviceTable,
    RepairModal
  },
  data() {
    return {
      devices: [],
      filteredDevices: [],
      loading: false,
      repairModalVisible: false,
      selectedDevice: {},
      searchParams: {
        deviceCode: '',
        branchName: '',
        status: ''
      }
    }
  },
  created() {
    this.loadDevices()
  },
  methods: {
    loadDevices() {
      this.loading = true
      setTimeout(() => {
        this.devices = [...mockDevices]
        this.filteredDevices = [...mockDevices]
        this.loading = false
      }, 300)
    },
    handleSearch(params) {
      this.searchParams = { ...params }
      this.filterDevices()
    },
    handleReset() {
      this.searchParams = {
        deviceCode: '',
        branchName: '',
        status: ''
      }
      this.filteredDevices = [...this.devices]
    },
    filterDevices() {
      const { deviceCode, branchName, status } = this.searchParams
      const keywordDevice = deviceCode ? deviceCode.trim().toLowerCase() : ''
      const keywordBranch = branchName ? branchName.trim().toLowerCase() : ''
      
      this.filteredDevices = this.devices.filter(item => {
        const matchDeviceCode = !keywordDevice || 
          item.deviceCode.toLowerCase().includes(keywordDevice) ||
          item.deviceCode.toLowerCase().indexOf(keywordDevice) !== -1
        
        const matchBranchName = !keywordBranch || 
          item.branchName.toLowerCase().includes(keywordBranch) ||
          item.branchName.toLowerCase().indexOf(keywordBranch) !== -1 ||
          item.floor.toLowerCase().includes(keywordBranch)
        
        const matchStatus = !status || item.status === status
        
        return matchDeviceCode && matchBranchName && matchStatus
      })
    },
    handleRepair(device) {
      this.selectedDevice = { ...device }
      this.repairModalVisible = true
    },
    handleRepairSubmit(orderData) {
      const index = this.devices.findIndex(item => item.id === orderData.deviceId)
      if (index !== -1) {
        this.$set(this.devices[index], 'status', 'maintaining')
        this.$nextTick(() => {
          this.filterDevices()
        })
      }
      console.log('报修工单已提交:', orderData)
    }
  }
}
</script>

<style scoped lang="scss">
.device-management {
  padding: 24px;
  min-height: 100vh;
  background: #f0f2f5;

  .page-header {
    margin-bottom: 20px;

    .page-title {
      font-size: 24px;
      font-weight: 600;
      color: #303133;
      margin-bottom: 4px;
    }

    .page-desc {
      font-size: 14px;
      color: #909399;
    }
  }
}
</style>
