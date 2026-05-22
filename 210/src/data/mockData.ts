import type { Device, DeviceModule, StatusConfig, DeviceStatus, ModuleStatus, ModuleStatusConfig } from '@/types'

export const statusConfigMap: Record<DeviceStatus, StatusConfig> = {
  normal: {
    label: '正常',
    bgColor: 'bg-green-100',
    textColor: 'text-green-700',
    dotColor: 'bg-green-500',
  },
  warning: {
    label: '预警',
    bgColor: 'bg-amber-100',
    textColor: 'text-amber-700',
    dotColor: 'bg-amber-500',
  },
  fault: {
    label: '故障',
    bgColor: 'bg-red-100',
    textColor: 'text-red-700',
    dotColor: 'bg-red-500',
  },
  offline: {
    label: '离线',
    bgColor: 'bg-gray-100',
    textColor: 'text-gray-600',
    dotColor: 'bg-gray-400',
  },
}

export const moduleStatusConfigMap: Record<string, ModuleStatusConfig> = {
  identityVerify: {
    label: '身份核验',
    icon: 'M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2M15 11h3m-3 4h2',
    normalColor: 'text-green-500',
    warningColor: 'text-amber-500',
    faultColor: 'text-red-500',
  },
  businessHandle: {
    label: '业务办理',
    icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
    normalColor: 'text-blue-500',
    warningColor: 'text-amber-500',
    faultColor: 'text-red-500',
  },
  voucherPrint: {
    label: '凭证打印',
    icon: 'M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z',
    normalColor: 'text-purple-500',
    warningColor: 'text-amber-500',
    faultColor: 'text-red-500',
  },
  network: {
    label: '网络通信',
    icon: 'M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0',
    normalColor: 'text-cyan-500',
    warningColor: 'text-amber-500',
    faultColor: 'text-red-500',
  },
}

const halls = [
  '市民服务中心A厅',
  '市民服务中心B厅',
  '市民服务中心C厅',
  '政务服务中心东厅',
  '政务服务中心西厅',
  '社保服务大厅',
  '不动产登记大厅',
  '出入境办理大厅',
]

const areas = [
  '自助服务区1号区',
  '自助服务区2号区',
  '自助服务区3号区',
  '大厅入口左侧',
  '大厅入口右侧',
  '2楼东区',
  '2楼西区',
  '3楼南侧',
]

const statuses: DeviceStatus[] = ['normal', 'normal', 'normal', 'normal', 'warning', 'fault', 'offline', 'normal']
const moduleStatuses: ModuleStatus[] = ['normal', 'normal', 'normal', 'normal', 'warning', 'fault']

function generateDeviceCode(index: number): string {
  const prefix = 'ZZ'
  const num = String(index).padStart(4, '0')
  return `${prefix}${num}`
}

function generateIp(index: number): string {
  const third = Math.floor(index / 256)
  const fourth = index % 256
  return `192.168.${third}.${fourth}`
}

function randomDate(): string {
  const now = new Date()
  const daysAgo = Math.floor(Math.random() * 7)
  const hoursAgo = Math.floor(Math.random() * 24)
  now.setDate(now.getDate() - daysAgo)
  now.setHours(now.getHours() - hoursAgo)
  return now.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function randomModuleStatus(deviceStatus: DeviceStatus, index: number): {
  identityVerify: ModuleStatus
  businessHandle: ModuleStatus
  voucherPrint: ModuleStatus
  network: ModuleStatus
} {
  if (deviceStatus === 'offline') {
    return {
      identityVerify: 'fault',
      businessHandle: 'fault',
      voucherPrint: 'fault',
      network: 'fault',
    }
  }
  if (deviceStatus === 'fault') {
    return {
      identityVerify: moduleStatuses[index % moduleStatuses.length],
      businessHandle: moduleStatuses[(index + 1) % moduleStatuses.length],
      voucherPrint: moduleStatuses[(index + 2) % moduleStatuses.length],
      network: moduleStatuses[(index + 3) % moduleStatuses.length],
    }
  }
  if (deviceStatus === 'warning') {
    return {
      identityVerify: moduleStatuses[index % 5] === 'fault' ? 'warning' : 'normal',
      businessHandle: moduleStatuses[(index + 1) % 5] === 'fault' ? 'warning' : 'normal',
      voucherPrint: moduleStatuses[(index + 2) % 5] === 'fault' ? 'warning' : 'normal',
      network: moduleStatuses[(index + 3) % 5] === 'fault' ? 'warning' : 'normal',
    }
  }
  return {
    identityVerify: moduleStatuses[index % 5] === 'fault' ? 'normal' : 'normal',
    businessHandle: moduleStatuses[(index + 1) % 5] === 'fault' ? 'normal' : 'normal',
    voucherPrint: moduleStatuses[(index + 2) % 5] === 'fault' ? 'normal' : 'normal',
    network: moduleStatuses[(index + 3) % 5] === 'fault' ? 'normal' : 'normal',
  }
}

export const mockDevices: DeviceModule[] = Array.from({ length: 48 }, (_, i) => {
  const status = statuses[i % statuses.length]
  const moduleStatus = randomModuleStatus(status, i)
  return {
    id: `device-${i + 1}`,
    deviceCode: generateDeviceCode(i + 1),
    hallName: halls[i % halls.length],
    areaName: areas[i % areas.length],
    status,
    lastOnline: randomDate(),
    ipAddress: generateIp(i + 1),
    ...moduleStatus,
  }
})

export function generateOrderNo(): string {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  const random = Math.floor(Math.random() * 10000).toString().padStart(4, '0')
  return `GD${year}${month}${day}${random}`
}

export function getModuleStatusColor(moduleKey: string, status: ModuleStatus): string {
  const config = moduleStatusConfigMap[moduleKey]
  if (!config) return 'text-gray-500'
  if (status === 'normal') return config.normalColor
  if (status === 'warning') return config.warningColor
  return config.faultColor
}
