export type DeviceStatus = 'normal' | 'warning' | 'fault' | 'offline'

export type ModuleStatus = 'normal' | 'warning' | 'fault'

export interface DeviceModule {
  id: string
  deviceCode: string
  hallName: string
  areaName: string
  status: DeviceStatus
  lastOnline: string
  ipAddress: string
  identityVerify: ModuleStatus
  businessHandle: ModuleStatus
  voucherPrint: ModuleStatus
  network: ModuleStatus
}

export interface WorkOrder {
  id: string
  orderNo: string
  deviceId: string
  deviceCode: string
  description: string
  createTime: string
  status: 'pending' | 'processing' | 'resolved'
}

export interface SearchParams {
  deviceCode: string
  hallName: string
  status: string
}

export interface StatusConfig {
  label: string
  bgColor: string
  textColor: string
  dotColor: string
}

export interface ModuleStatusConfig {
  label: string
  icon: string
  normalColor: string
  warningColor: string
  faultColor: string
}
