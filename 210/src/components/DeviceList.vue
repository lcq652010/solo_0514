<script lang="ts">
import Vue from 'vue'
import type { DeviceModule, ModuleStatus } from '@/types'
import { statusConfigMap, moduleStatusConfigMap, getModuleStatusColor } from '@/data/mockData'

export default Vue.extend({
  name: 'DeviceList',
  props: {
    devices: {
      type: Array as () => DeviceModule[],
      default: () => [],
    },
    loading: {
      type: Boolean,
      default: false,
    },
    searchKeyword: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      moduleKeys: ['identityVerify', 'businessHandle', 'voucherPrint', 'network'] as const,
    }
  },
  methods: {
    getStatusConfig(status: string) {
      return statusConfigMap[status as keyof typeof statusConfigMap] || statusConfigMap.offline
    },
    getModuleConfig(moduleKey: string) {
      return moduleStatusConfigMap[moduleKey]
    },
    getModuleColor(moduleKey: string, status: ModuleStatus): string {
      return getModuleStatusColor(moduleKey, status)
    },
    getModuleStatusClass(status: ModuleStatus): string {
      if (status === 'fault') return 'animate-pulse'
      if (status === 'warning') return 'animate-pulse opacity-75'
      return ''
    },
    onReport(device: DeviceModule) {
      this.$emit('report', device)
    },
    getRowClass(status: string): string {
      if (status === 'fault') return 'bg-red-50 border-l-4 border-l-red-500 fault-row'
      if (status === 'offline') return 'bg-gray-100 border-l-4 border-l-gray-400 opacity-75'
      if (status === 'warning') return 'bg-amber-50 border-l-4 border-l-amber-400 warning-row'
      return ''
    },
    highlight(text: string, keyword: string): string {
      if (!keyword.trim()) return text
      const escaped = keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
      const regex = new RegExp(`(${escaped})`, 'gi')
      return text.replace(regex, '<mark class="bg-yellow-200 text-yellow-800 px-0.5 rounded font-medium">$1</mark>')
    },
    getModuleTooltip(moduleKey: string, status: ModuleStatus): string {
      const config = moduleStatusConfigMap[moduleKey]
      const statusLabel = status === 'normal' ? '正常' : status === 'warning' ? '预警' : '故障'
      return `${config.label}: ${statusLabel}`
    },
  },
})
</script>

<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden relative">
    <div v-if="loading" class="absolute inset-0 bg-white bg-opacity-80 flex items-center justify-center z-10">
      <div class="flex items-center gap-3">
        <svg class="animate-spin h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span class="text-gray-600 text-sm">加载中...</span>
      </div>
    </div>

    <div class="overflow-x-auto">
      <table class="w-full">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              设备编号
            </th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              服务大厅
            </th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              布设区域
            </th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              运行状态
            </th>
            <th class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
              模块状态
            </th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              最后在线时间
            </th>
            <th class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
              操作
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr
            v-for="device in devices"
            :key="device.id"
            :class="[
              getRowClass(device.status),
              'hover:bg-blue-50 transition-all duration-200',
            ]"
          >
            <td class="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">
              <span v-html="highlight(device.deviceCode, searchKeyword)"></span>
              <div class="text-xs text-gray-400 font-mono">{{ device.ipAddress }}</div>
            </td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-600">
              <span v-html="highlight(device.hallName, searchKeyword)"></span>
            </td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-600">
              {{ device.areaName }}
            </td>
            <td class="px-4 py-3 whitespace-nowrap">
              <span
                :class="[
                  'inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium',
                  getStatusConfig(device.status).bgColor,
                  getStatusConfig(device.status).textColor,
                  device.status === 'fault' ? 'animate-pulse' : '',
                ]"
              >
                <span
                  :class="[
                    'w-2 h-2 rounded-full',
                    getStatusConfig(device.status).dotColor,
                    device.status === 'fault' ? 'animate-ping' : '',
                  ]"
                ></span>
                {{ getStatusConfig(device.status).label }}
              </span>
            </td>
            <td class="px-4 py-3 whitespace-nowrap">
              <div class="flex items-center justify-center gap-1">
                <div
                  v-for="moduleKey in moduleKeys"
                  :key="moduleKey"
                  :class="[
                    'w-9 h-9 rounded-md flex items-center justify-center cursor-help transition-all duration-200 hover:scale-110',
                    getModuleStatusClass(device[moduleKey]),
                  ]"
                  :title="getModuleTooltip(moduleKey, device[moduleKey])"
                  :style="{
                    backgroundColor: device[moduleKey] === 'fault'
                      ? 'rgba(239, 68, 68, 0.1)'
                      : device[moduleKey] === 'warning'
                        ? 'rgba(245, 158, 11, 0.1)'
                        : 'rgba(34, 197, 94, 0.08)',
                  }"
                >
                  <svg
                    :class="['w-4 h-4', getModuleColor(moduleKey, device[moduleKey])]"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      :d="getModuleConfig(moduleKey).icon"
                    />
                  </svg>
                </div>
              </div>
            </td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
              {{ device.lastOnline }}
            </td>
            <td class="px-4 py-3 whitespace-nowrap text-center">
              <button
                type="button"
                @click="onReport(device)"
                :class="[
                  'text-sm font-medium transition-colors',
                  device.status === 'fault'
                    ? 'text-red-600 hover:text-red-800 font-semibold'
                    : 'text-red-600 hover:text-red-800',
                ]"
              >
                {{ device.status === 'fault' ? '已上报' : '上报故障' }}
              </button>
            </td>
          </tr>
          <tr v-if="devices.length === 0 && !loading">
            <td colspan="7" class="px-4 py-12 text-center text-gray-400">
              <div class="flex flex-col items-center gap-2">
                <svg class="w-12 h-12 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>暂无设备数据</span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="px-4 py-3 bg-gray-50 border-t border-gray-100">
      <div class="flex items-center justify-center gap-6 text-xs text-gray-500">
        <div class="flex items-center gap-1.5">
          <div class="w-4 h-4 rounded bg-green-100 flex items-center justify-center">
            <svg class="w-2.5 h-2.5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0" />
            </svg>
          </div>
          <span>身份核验</span>
        </div>
        <div class="flex items-center gap-1.5">
          <div class="w-4 h-4 rounded bg-blue-100 flex items-center justify-center">
            <svg class="w-2.5 h-2.5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <span>业务办理</span>
        </div>
        <div class="flex items-center gap-1.5">
          <div class="w-4 h-4 rounded bg-purple-100 flex items-center justify-center">
            <svg class="w-2.5 h-2.5 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
            </svg>
          </div>
          <span>凭证打印</span>
        </div>
        <div class="flex items-center gap-1.5">
          <div class="w-4 h-4 rounded bg-cyan-100 flex items-center justify-center">
            <svg class="w-2.5 h-2.5 text-cyan-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0" />
            </svg>
          </div>
          <span>网络通信</span>
        </div>
        <div class="flex items-center gap-1.5 text-gray-400">
          <span class="text-gray-400">|</span>
          <div class="flex items-center gap-1">
            <span class="w-2 h-2 rounded-full bg-green-500"></span>
            <span>正常</span>
          </div>
          <div class="flex items-center gap-1">
            <span class="w-2 h-2 rounded-full bg-amber-500"></span>
            <span>预警</span>
          </div>
          <div class="flex items-center gap-1">
            <span class="w-2 h-2 rounded-full bg-red-500"></span>
            <span>故障</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fault-row {
  animation: faultBlink 2s ease-in-out infinite;
}

.warning-row {
  animation: warningPulse 1.5s ease-in-out infinite;
}

@keyframes faultBlink {
  0%, 100% {
    background-color: #fef2f2;
  }
  50% {
    background-color: #fee2e2;
  }
}

@keyframes warningPulse {
  0%, 100% {
    background-color: #fffbeb;
  }
  50% {
    background-color: #fef3c7;
  }
}
</style>
