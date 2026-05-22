<script lang="ts">
import Vue from 'vue'
import type { Device } from '@/types'
import { statusConfigMap } from '@/data/mockData'

function generateOrderNo(): string {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  const random = Math.floor(Math.random() * 10000).toString().padStart(4, '0')
  return `GD${year}${month}${day}${random}`
}

export default Vue.extend({
  name: 'FaultReportModal',
  props: {
    visible: {
      type: Boolean,
      default: false,
    },
    devices: {
      type: Array as () => Device[],
      default: () => [],
    },
    selectedDevice: {
      type: Object as () => Device | null,
      default: null,
    },
  },
  data() {
    return {
      localDeviceId: '',
      description: '',
      orderNo: '',
      deviceSearchKeyword: '',
      showDeviceDropdown: false,
      submitErrors: {
        device: '',
        description: '',
      } as { device: string; description: string },
    }
  },
  computed: {
    filteredDeviceOptions(): Device[] {
      if (!this.deviceSearchKeyword.trim()) return this.devices
      const keyword = this.deviceSearchKeyword.trim().toLowerCase()
      return this.devices.filter(
        (d) =>
          d.deviceCode.toLowerCase().includes(keyword) ||
          d.hallName.toLowerCase().includes(keyword) ||
          d.areaName.toLowerCase().includes(keyword)
      )
    },
    selectedDeviceInfo(): Device | null {
      if (!this.localDeviceId) return null
      return this.devices.find((d) => d.id === this.localDeviceId) || null
    },
    isFormValid(): boolean {
      return this.localDeviceId !== '' && this.description.trim().length >= 5
    },
  },
  watch: {
    visible: {
      handler(val: boolean) {
        if (val) {
          this.orderNo = generateOrderNo()
          if (this.selectedDevice) {
            this.localDeviceId = this.selectedDevice.id
            this.deviceSearchKeyword = this.selectedDevice.deviceCode
          } else {
            this.localDeviceId = ''
            this.deviceSearchKeyword = ''
          }
          this.description = ''
          this.submitErrors = { device: '', description: '' }
          this.showDeviceDropdown = false
        }
      },
      immediate: true,
    },
    selectedDevice: {
      handler(val: Device | null) {
        if (val && this.visible) {
          this.localDeviceId = val.id
          this.deviceSearchKeyword = val.deviceCode
        }
      },
    },
  },
  methods: {
    getStatusConfig(status: string) {
      return statusConfigMap[status as keyof typeof statusConfigMap] || statusConfigMap.offline
    },
    onClose() {
      this.$emit('close')
    },
    validateForm(): boolean {
      let valid = true
      this.submitErrors = { device: '', description: '' }

      if (!this.localDeviceId) {
        this.submitErrors.device = '请选择故障设备'
        valid = false
      }

      if (!this.description.trim()) {
        this.submitErrors.description = '请填写问题描述'
        valid = false
      } else if (this.description.trim().length < 5) {
        this.submitErrors.description = '问题描述至少需要5个字符'
        valid = false
      } else if (this.description.trim().length > 500) {
        this.submitErrors.description = '问题描述不能超过500个字符'
        valid = false
      }

      return valid
    },
    onSubmit() {
      if (!this.validateForm()) return

      const device = this.devices.find((d) => d.id === this.localDeviceId)
      if (!device) return

      this.$emit('submit', {
        deviceId: device.id,
        deviceCode: device.deviceCode,
        description: this.description.trim(),
      })
    },
    onMaskClick(e: MouseEvent) {
      if ((e.target as HTMLElement).classList.contains('modal-mask')) {
        this.onClose()
      }
    },
    onDeviceSelect(deviceId: string) {
      this.localDeviceId = deviceId
      const device = this.devices.find((d) => d.id === deviceId)
      if (device) {
        this.deviceSearchKeyword = device.deviceCode
      }
      this.showDeviceDropdown = false
      this.submitErrors.device = ''
    },
    onDeviceSearchInput(e: Event) {
      const target = e.target as HTMLInputElement
      this.deviceSearchKeyword = target.value
      this.showDeviceDropdown = true
      this.submitErrors.device = ''
    },
    onDescChange(e: Event) {
      const target = e.target as HTMLTextAreaElement
      this.description = target.value
      if (this.submitErrors.description && this.description.trim().length >= 5) {
        this.submitErrors.description = ''
      }
    },
    onFocusDeviceInput() {
      this.showDeviceDropdown = true
    },
    onBlurDeviceInput() {
      setTimeout(() => {
        this.showDeviceDropdown = false
      }, 200)
    },
    clearDeviceSelection() {
      this.localDeviceId = ''
      this.deviceSearchKeyword = ''
      this.showDeviceDropdown = true
    },
  },
})
</script>

<template>
  <transition name="modal">
    <div
      v-if="visible"
      class="modal-mask fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click="onMaskClick"
    >
      <div class="bg-white rounded-lg shadow-xl w-full max-w-2xl mx-4 overflow-hidden transform transition-all max-h-[90vh] flex flex-col">
        <div class="px-6 py-4 border-b border-gray-100 flex items-center justify-between bg-gradient-to-r from-red-500 to-orange-500 flex-shrink-0">
          <h3 class="text-lg font-semibold text-white flex items-center gap-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            故障上报
          </h3>
          <button
            type="button"
            @click="onClose"
            class="text-white hover:text-gray-200 transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div class="px-6 py-5 space-y-5 overflow-y-auto flex-1">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">
                工单编号
              </label>
              <div class="px-3 py-2 bg-blue-50 border border-blue-200 rounded-md text-sm text-blue-700 font-mono">
                {{ orderNo }}
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">
                上报时间
              </label>
              <div class="px-3 py-2 bg-gray-50 border border-gray-200 rounded-md text-sm text-gray-600">
                {{ new Date().toLocaleString('zh-CN') }}
              </div>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">
              选择设备 <span class="text-red-500">*</span>
            </label>
            <div class="relative">
              <div class="relative">
                <input
                  type="text"
                  :value="deviceSearchKeyword"
                  @input="onDeviceSearchInput"
                  @focus="onFocusDeviceInput"
                  @blur="onBlurDeviceInput"
                  placeholder="输入设备编号、大厅名称或区域搜索..."
                  :class="[
                    'w-full px-3 py-2 border rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent pr-10',
                    submitErrors.device ? 'border-red-500 bg-red-50' : 'border-gray-300',
                  ]"
                />
                <button
                  v-if="localDeviceId"
                  type="button"
                  @click="clearDeviceSelection"
                  class="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <div
                v-if="showDeviceDropdown && filteredDeviceOptions.length > 0"
                class="absolute z-20 w-full mt-1 bg-white border border-gray-200 rounded-md shadow-lg max-h-60 overflow-y-auto"
              >
                <div
                  v-for="device in filteredDeviceOptions"
                  :key="device.id"
                  @mousedown.prevent="onDeviceSelect(device.id)"
                  :class="[
                    'px-3 py-2 cursor-pointer hover:bg-blue-50 transition-colors border-b border-gray-100 last:border-b-0',
                    localDeviceId === device.id ? 'bg-blue-50' : '',
                  ]"
                >
                  <div class="flex items-center justify-between">
                    <div class="flex-1">
                      <div class="text-sm font-medium text-gray-900">{{ device.deviceCode }}</div>
                      <div class="text-xs text-gray-500">{{ device.hallName }} - {{ device.areaName }}</div>
                    </div>
                    <span
                      :class="[
                        'inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs',
                        getStatusConfig(device.status).bgColor,
                        getStatusConfig(device.status).textColor,
                      ]"
                    >
                      <span
                        :class="[
                          'w-1.5 h-1.5 rounded-full',
                          getStatusConfig(device.status).dotColor,
                        ]"
                      ></span>
                      {{ getStatusConfig(device.status).label }}
                    </span>
                  </div>
                </div>
              </div>

              <div
                v-if="showDeviceDropdown && deviceSearchKeyword && filteredDeviceOptions.length === 0"
                class="absolute z-20 w-full mt-1 bg-white border border-gray-200 rounded-md shadow-lg p-4 text-center text-gray-500 text-sm"
              >
                未找到匹配的设备
              </div>
            </div>
            <p v-if="submitErrors.device" class="mt-1 text-xs text-red-500">
              {{ submitErrors.device }}
            </p>

            <div v-if="selectedDeviceInfo" class="mt-3 p-3 bg-gray-50 rounded-md border border-gray-200">
              <div class="text-xs text-gray-500 mb-1">已选择设备信息：</div>
              <div class="grid grid-cols-2 gap-2 text-sm">
                <div><span class="text-gray-500">设备编号：</span><span class="font-medium">{{ selectedDeviceInfo.deviceCode }}</span></div>
                <div><span class="text-gray-500">IP地址：</span><span class="font-mono">{{ selectedDeviceInfo.ipAddress }}</span></div>
                <div class="col-span-2"><span class="text-gray-500">位置：</span>{{ selectedDeviceInfo.hallName }} - {{ selectedDeviceInfo.areaName }}</div>
              </div>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">
              问题描述 <span class="text-red-500">*</span>
            </label>
            <textarea
              :value="description"
              @input="onDescChange"
              rows="5"
              placeholder="请详细描述故障现象（如：设备无法开机、触摸屏无响应、打印故障等）..."
              :class="[
                'w-full px-3 py-2 border rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent resize-none',
                submitErrors.description ? 'border-red-500 bg-red-50' : 'border-gray-300',
              ]"
            ></textarea>
            <div class="flex justify-between items-center mt-1">
              <p v-if="submitErrors.description" class="text-xs text-red-500">
                {{ submitErrors.description }}
              </p>
              <p v-else class="text-xs text-gray-400">
                请详细描述故障现象，至少5个字符
              </p>
              <p :class="['text-xs', description.length > 500 ? 'text-red-500' : 'text-gray-400']">
                {{ description.length }}/500
              </p>
            </div>
          </div>

          <div class="bg-amber-50 border border-amber-200 rounded-md p-3">
            <div class="flex items-start gap-2">
              <svg class="w-5 h-5 text-amber-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div class="text-xs text-amber-700">
                <p class="font-medium mb-1">温馨提示：</p>
                <ul class="list-disc list-inside space-y-0.5">
                  <li>请准确描述故障现象，以便运维人员快速定位问题</li>
                  <li>工单提交后，设备状态将自动更新为"故障"</li>
                  <li>运维人员将在2小时内响应处理</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <div class="px-6 py-4 bg-gray-50 border-t border-gray-100 flex justify-between items-center flex-shrink-0">
          <div class="text-xs text-gray-500">
            <span class="text-red-500">*</span> 为必填项
          </div>
          <div class="flex gap-3">
            <button
              type="button"
              @click="onClose"
              class="px-4 py-2 bg-white border border-gray-300 text-gray-700 text-sm rounded-md hover:bg-gray-50 transition-colors"
            >
              取消
            </button>
            <button
              type="button"
              @click="onSubmit"
              :disabled="!isFormValid"
              :class="[
                'px-6 py-2 text-sm rounded-md transition-colors flex items-center gap-1',
                isFormValid
                  ? 'bg-red-500 text-white hover:bg-red-600 cursor-pointer'
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed',
              ]"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              提交工单
            </button>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: all 0.2s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
.modal-enter-from > div,
.modal-leave-to > div {
  transform: scale(0.95) translateY(20px);
}
</style>
