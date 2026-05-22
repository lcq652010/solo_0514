export const deviceList = [
  { id: 1, deviceCode: 'CUS-2024-001', portHall: '深圳皇岗口岸', location: '入境大厅一楼A区', status: 'normal', statusText: '正常', idCardReader: 'normal', customsDeclarationPrint: 'normal', encryptionNetwork: 'normal' },
  { id: 2, deviceCode: 'CUS-2024-002', portHall: '深圳皇岗口岸', location: '入境大厅一楼B区', status: 'fault', statusText: '故障', idCardReader: 'fault', customsDeclarationPrint: 'normal', encryptionNetwork: 'normal' },
  { id: 3, deviceCode: 'CUS-2024-003', portHall: '深圳罗湖口岸', location: '出境大厅二楼', status: 'normal', statusText: '正常', idCardReader: 'normal', customsDeclarationPrint: 'normal', encryptionNetwork: 'normal' },
  { id: 4, deviceCode: 'CUS-2024-004', portHall: '深圳罗湖口岸', location: '入境大厅一楼', status: 'offline', statusText: '离线', idCardReader: 'offline', customsDeclarationPrint: 'offline', encryptionNetwork: 'offline' },
  { id: 5, deviceCode: 'CUS-2024-005', portHall: '广州白云机场口岸', location: 'T1航站楼国际到达区', status: 'maintenance', statusText: '维护中', idCardReader: 'maintenance', customsDeclarationPrint: 'normal', encryptionNetwork: 'normal' },
  { id: 6, deviceCode: 'CUS-2024-006', portHall: '广州白云机场口岸', location: 'T2航站楼国际出发区', status: 'normal', statusText: '正常', idCardReader: 'normal', customsDeclarationPrint: 'normal', encryptionNetwork: 'normal' },
  { id: 7, deviceCode: 'CUS-2024-007', portHall: '珠海拱北口岸', location: '入境大厅', status: 'normal', statusText: '正常', idCardReader: 'normal', customsDeclarationPrint: 'normal', encryptionNetwork: 'fault' },
  { id: 8, deviceCode: 'CUS-2024-008', portHall: '珠海拱北口岸', location: '出境大厅', status: 'fault', statusText: '故障', idCardReader: 'normal', customsDeclarationPrint: 'fault', encryptionNetwork: 'normal' },
  { id: 9, deviceCode: 'CUS-2024-009', portHall: '上海浦东机场口岸', location: 'T1航站楼', status: 'normal', statusText: '正常', idCardReader: 'normal', customsDeclarationPrint: 'normal', encryptionNetwork: 'normal' },
  { id: 10, deviceCode: 'CUS-2024-010', portHall: '上海浦东机场口岸', location: 'T2航站楼', status: 'offline', statusText: '离线', idCardReader: 'offline', customsDeclarationPrint: 'offline', encryptionNetwork: 'offline' },
  { id: 11, deviceCode: 'CUS-2024-011', portHall: '北京首都机场口岸', location: 'T3航站楼E区', status: 'normal', statusText: '正常', idCardReader: 'normal', customsDeclarationPrint: 'normal', encryptionNetwork: 'normal' },
  { id: 12, deviceCode: 'CUS-2024-012', portHall: '北京首都机场口岸', location: 'T2航站楼', status: 'maintenance', statusText: '维护中', idCardReader: 'normal', customsDeclarationPrint: 'maintenance', encryptionNetwork: 'normal' },
  { id: 13, deviceCode: 'CUS-2024-013', portHall: '厦门高崎机场口岸', location: '国际到达厅', status: 'normal', statusText: '正常', idCardReader: 'normal', customsDeclarationPrint: 'normal', encryptionNetwork: 'normal' },
  { id: 14, deviceCode: 'CUS-2024-014', portHall: '天津滨海机场口岸', location: '国际出发厅', status: 'normal', statusText: '正常', idCardReader: 'normal', customsDeclarationPrint: 'normal', encryptionNetwork: 'normal' },
  { id: 15, deviceCode: 'CUS-2024-015', portHall: '重庆江北机场口岸', location: 'T3A航站楼', status: 'fault', statusText: '故障', idCardReader: 'normal', customsDeclarationPrint: 'normal', encryptionNetwork: 'fault' }
]

export const portList = [
  '深圳皇岗口岸',
  '深圳罗湖口岸',
  '广州白云机场口岸',
  '珠海拱北口岸',
  '上海浦东机场口岸',
  '北京首都机场口岸',
  '厦门高崎机场口岸',
  '天津滨海机场口岸',
  '重庆江北机场口岸'
]

export const statusMap = {
  normal: { text: '正常', color: '#67C23A' },
  fault: { text: '故障', color: '#F56C6C' },
  offline: { text: '离线', color: '#909399' },
  maintenance: { text: '维护中', color: '#E6A23C' }
}
