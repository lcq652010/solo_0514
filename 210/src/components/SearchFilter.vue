<script lang="ts">
import Vue from 'vue'
import { statusConfigMap } from '@/data/mockData'

export default Vue.extend({
  name: 'SearchFilter',
  props: {
    deviceCode: {
      type: String,
      default: '',
    },
    hallName: {
      type: String,
      default: '',
    },
    status: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      statusOptions: [
        { value: '', label: '全部状态' },
        { value: 'normal', label: '正常' },
        { value: 'warning', label: '预警' },
        { value: 'fault', label: '故障' },
        { value: 'offline', label: '离线' },
      ],
    }
  },
  methods: {
    onDeviceCodeInput(e: Event) {
      const target = e.target as HTMLInputElement
      this.$emit('update:deviceCode', target.value)
    },
    onHallNameInput(e: Event) {
      const target = e.target as HTMLInputElement
      this.$emit('update:hallName', target.value)
    },
    onStatusChange(e: Event) {
      const target = e.target as HTMLSelectElement
      this.$emit('update:status', target.value)
    },
    onSearch() {
      this.$emit('search')
    },
    onReset() {
      this.$emit('update:deviceCode', '')
      this.$emit('update:hallName', '')
      this.$emit('update:status', '')
      this.$emit('reset')
    },
    onOpenModal() {
      this.$emit('openModal')
    },
    getStatusColor(status: string): string {
      if (!status) return ''
      const config = statusConfigMap[status as keyof typeof statusConfigMap]
      return config ? config.textColor : ''
    },
  },
})
</script>

<template>
  <div class="bg-white rounded-lg shadow-sm p-5 mb-5 border border-gray-100">
    <div class="flex flex-wrap items-center gap-4">
      <div class="flex items-center gap-2">
        <label class="text-sm text-gray-600 whitespace-nowrap">设备编号：</label>
        <input
          type="text"
          :value="deviceCode"
          @input="onDeviceCodeInput"
          placeholder="请输入设备编号"
          class="w-48 px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>
      <div class="flex items-center gap-2">
        <label class="text-sm text-gray-600 whitespace-nowrap">大厅名称：</label>
        <input
          type="text"
          :value="hallName"
          @input="onHallNameInput"
          placeholder="请输入大厅名称"
          class="w-48 px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>
      <div class="flex items-center gap-2">
        <label class="text-sm text-gray-600 whitespace-nowrap">运行状态：</label>
        <select
          :value="status"
          @change="onStatusChange"
          class="w-36 px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white cursor-pointer"
        >
          <option v-for="opt in statusOptions" :key="opt.value" :value="opt.value">
            {{ opt.label }}
          </option>
        </select>
      </div>
      <div class="flex items-center gap-2 ml-auto">
        <button
          type="button"
          @click="onSearch"
          class="px-4 py-2 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 transition-colors flex items-center gap-1"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          搜索
        </button>
        <button
          type="button"
          @click="onReset"
          class="px-4 py-2 bg-gray-100 text-gray-700 text-sm rounded-md hover:bg-gray-200 transition-colors"
        >
          重置
        </button>
        <button
          type="button"
          @click="onOpenModal"
          class="px-4 py-2 bg-red-500 text-white text-sm rounded-md hover:bg-red-600 transition-colors flex items-center gap-1"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          故障上报
        </button>
      </div>
    </div>
  </div>
</template>
