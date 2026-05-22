<script lang="ts">
import Vue from 'vue'
import SearchFilter from '@/components/SearchFilter.vue'
import DeviceList from '@/components/DeviceList.vue'
import FaultReportModal from '@/components/FaultReportModal.vue'
import Pagination from '@/components/Pagination.vue'
import { mockDevices, generateOrderNo } from '@/data/mockData'
import type { DeviceModule, WorkOrder } from '@/types'

export default Vue.extend({
  name: 'HomePage',
  components: {
    SearchFilter,
    DeviceList,
    FaultReportModal,
    Pagination,
  },
  data() {
    return {
      allDevices: [...mockDevices] as DeviceModule[],
      workOrders: [] as WorkOrder[],
      searchDeviceCode: '',
      searchHallName: '',
      searchStatus: '',
      currentPage: 1,
      pageSize: 10,
      modalVisible: false,
      selectedDevice: null as DeviceModule | null,
      showSuccessToast: false,
      successMessage: '',
      listLoading: false,
    }
  },
  computed: {
    filteredDevices(): DeviceModule[] {
      let result = [...this.allDevices]
      if (this.searchDeviceCode.trim()) {
        const keyword = this.searchDeviceCode.trim().toLowerCase()
        result = result.filter((d) => d.deviceCode.toLowerCase().includes(keyword))
      }
      if (this.searchHallName.trim()) {
        const keyword = this.searchHallName.trim()
        result = result.filter((d) => d.hallName.includes(keyword))
      }
      if (this.searchStatus) {
        result = result.filter((d) => d.status === this.searchStatus)
      }
      return result
    },
    paginatedDevices(): DeviceModule[] {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredDevices.slice(start, end)
    },
    total(): number {
      return this.filteredDevices.length
    },
    normalCount(): number {
      return this.allDevices.filter((d) => d.status === 'normal').length
    },
    warningCount(): number {
      return this.allDevices.filter((d) => d.status === 'warning').length
    },
    faultOfflineCount(): number {
      return this.allDevices.filter((d) => d.status === 'fault' || d.status === 'offline').length
    },
  },
  methods: {
    onSearch() {
      this.listLoading = true
      setTimeout(() => {
        this.currentPage = 1
        this.listLoading = false
      }, 300)
    },
    onReset() {
      this.listLoading = true
      setTimeout(() => {
        this.searchDeviceCode = ''
        this.searchHallName = ''
        this.searchStatus = ''
        this.currentPage = 1
        this.listLoading = false
      }, 300)
    },
    onOpenModal() {
      this.selectedDevice = null
      this.modalVisible = true
    },
    onReportDevice(device: DeviceModule) {
      this.selectedDevice = device
      this.modalVisible = true
    },
    onCloseModal() {
      this.modalVisible = false
      this.selectedDevice = null
    },
    onSubmitReport(data: { deviceId: string; deviceCode: string; description: string }) {
      const orderNo = generateOrderNo()
      const now = new Date().toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
      })

      const workOrder: WorkOrder = {
        id: `order-${Date.now()}`,
        orderNo,
        deviceId: data.deviceId,
        deviceCode: data.deviceCode,
        description: data.description,
        createTime: now,
        status: 'pending',
      }
      this.workOrders.unshift(workOrder)

      const deviceIndex = this.allDevices.findIndex((d) => d.id === data.deviceId)
      if (deviceIndex !== -1) {
        this.$set(this.allDevices, deviceIndex, {
          ...this.allDevices[deviceIndex],
          status: 'fault',
        })
      }

      this.successMessage = `工单提交成功！工单编号：${orderNo}`
      this.showSuccessToast = true
      setTimeout(() => {
        this.showSuccessToast = false
      }, 3000)

      this.onCloseModal()
    },
    onPageChange(page: number) {
      this.listLoading = true
      setTimeout(() => {
        this.currentPage = page
        this.listLoading = false
      }, 200)
    },
    updateDeviceCode(val: string) {
      this.searchDeviceCode = val
    },
    updateHallName(val: string) {
      this.searchHallName = val
    },
    updateStatus(val: string) {
      this.listLoading = true
      setTimeout(() => {
        this.searchStatus = val
        this.currentPage = 1
        this.listLoading = false
      }, 200)
    },
    updatePageSize(val: number) {
      this.listLoading = true
      setTimeout(() => {
        this.pageSize = val
        this.currentPage = 1
        this.listLoading = false
      }, 200)
    },
    highlightKeyword(text: string, keyword: string): string {
      if (!keyword.trim()) return text
      const regex = new RegExp(`(${keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi')
      return text.replace(regex, '<span class="bg-yellow-200 text-yellow-800 px-0.5 rounded">$1</span>')
    },
    getDeviceRowClass(status: string): string {
      if (status === 'fault') return 'bg-red-50 border-l-4 border-l-red-500'
      if (status === 'offline') return 'bg-gray-100 border-l-4 border-l-gray-400 opacity-70'
      if (status === 'warning') return 'bg-amber-50 border-l-4 border-l-amber-400'
      return ''
    },
    getSearchKeyword(): string {
      return this.searchDeviceCode || this.searchHallName
    },
  },
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-gradient-to-r from-slate-800 to-slate-900 text-white shadow-lg">
      <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
            </svg>
          </div>
          <div>
            <h1 class="text-xl font-bold">市民服务中心自助终端运维管理系统</h1>
            <p class="text-xs text-slate-400">Citizen Service Center Self-Service Terminal Operation System</p>
          </div>
        </div>
        <div class="flex items-center gap-4">
          <div class="text-sm text-slate-300">
            <span class="text-slate-400">当前用户：</span>
            <span class="text-white font-medium">运维管理员</span>
          </div>
          <div class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-sm font-medium">
            运
          </div>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 py-6">
      <div class="grid grid-cols-4 gap-4 mb-6">
        <div class="bg-white rounded-lg shadow-sm p-5 border border-gray-100">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-500">设备总数</p>
              <p class="text-2xl font-bold text-gray-900 mt-1">{{ allDevices.length }}</p>
            </div>
            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
              </svg>
            </div>
          </div>
        </div>
        <div class="bg-white rounded-lg shadow-sm p-5 border border-gray-100">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-500">正常运行</p>
              <p class="text-2xl font-bold text-green-600 mt-1">{{ normalCount }}</p>
            </div>
            <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </div>
        <div class="bg-white rounded-lg shadow-sm p-5 border border-gray-100">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-500">设备预警</p>
              <p class="text-2xl font-bold text-amber-600 mt-1">{{ warningCount }}</p>
            </div>
            <div class="w-12 h-12 bg-amber-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
          </div>
        </div>
        <div class="bg-white rounded-lg shadow-sm p-5 border border-gray-100">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-500">故障/离线</p>
              <p class="text-2xl font-bold text-red-600 mt-1">{{ faultOfflineCount }}</p>
            </div>
            <div class="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <SearchFilter
        :deviceCode="searchDeviceCode"
        :hallName="searchHallName"
        :status="searchStatus"
        @update:deviceCode="updateDeviceCode"
        @update:hallName="updateHallName"
        @update:status="updateStatus"
        @search="onSearch"
        @reset="onReset"
        @openModal="onOpenModal"
      />

      <DeviceList
        :devices="paginatedDevices"
        :loading="listLoading"
        :searchKeyword="searchDeviceCode || searchHallName"
        @report="onReportDevice"
      />

      <Pagination
        v-if="total > 0"
        :current="currentPage"
        :total="total"
        :pageSize="pageSize"
        @update:pageSize="updatePageSize"
        @change="onPageChange"
      />
    </main>

    <FaultReportModal
      :visible="modalVisible"
      :devices="allDevices"
      :selectedDevice="selectedDevice"
      @close="onCloseModal"
      @submit="onSubmitReport"
    />

    <transition name="toast">
      <div
        v-if="showSuccessToast"
        class="fixed top-24 left-1/2 transform -translate-x-1/2 z-50"
      >
        <div class="bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <span>{{ successMessage }}</span>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}
.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translate(-50%, -20px);
}
</style>
