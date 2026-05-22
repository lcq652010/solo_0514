export const deviceList = [
  { id: 1, deviceNo: 'ZX-2024-001', hallName: '北京市政务服务中心', window: 'A区1号窗口', status: '正常', idCardReader: '正常', printer: '正常', encryptModule: '正常' },
  { id: 2, deviceNo: 'ZX-2024-002', hallName: '北京市政务服务中心', window: 'A区2号窗口', status: '故障', idCardReader: '故障', printer: '正常', encryptModule: '正常' },
  { id: 3, deviceNo: 'ZX-2024-003', hallName: '北京市政务服务中心', window: 'B区1号窗口', status: '离线', idCardReader: '离线', printer: '离线', encryptModule: '离线' },
  { id: 4, deviceNo: 'ZX-2024-004', hallName: '上海市政务服务中心', window: '1号窗口', status: '正常', idCardReader: '正常', printer: '正常', encryptModule: '正常' },
  { id: 5, deviceNo: 'ZX-2024-005', hallName: '上海市政务服务中心', window: '2号窗口', status: '维护中', idCardReader: '正常', printer: '维护中', encryptModule: '正常' },
  { id: 6, deviceNo: 'ZX-2024-006', hallName: '广州市政务服务中心', window: '一楼大厅1号', status: '正常', idCardReader: '正常', printer: '正常', encryptModule: '正常' },
  { id: 7, deviceNo: 'ZX-2024-007', hallName: '广州市政务服务中心', window: '一楼大厅2号', status: '正常', idCardReader: '正常', printer: '故障', encryptModule: '正常' },
  { id: 8, deviceNo: 'ZX-2024-008', hallName: '深圳市政务服务中心', window: 'A厅1号', status: '故障', idCardReader: '正常', printer: '故障', encryptModule: '故障' },
  { id: 9, deviceNo: 'ZX-2024-009', hallName: '深圳市政务服务中心', window: 'A厅2号', status: '正常', idCardReader: '正常', printer: '正常', encryptModule: '正常' },
  { id: 10, deviceNo: 'ZX-2024-010', hallName: '杭州市政务服务中心', window: '主厅1号', status: '离线', idCardReader: '离线', printer: '离线', encryptModule: '离线' },
  { id: 11, deviceNo: 'ZX-2024-011', hallName: '杭州市政务服务中心', window: '主厅2号', status: '正常', idCardReader: '正常', printer: '正常', encryptModule: '正常' },
  { id: 12, deviceNo: 'ZX-2024-012', hallName: '成都市政务服务中心', window: '1楼窗口1', status: '维护中', idCardReader: '维护中', printer: '正常', encryptModule: '维护中' },
  { id: 13, deviceNo: 'ZX-2024-013', hallName: '成都市政务服务中心', window: '1楼窗口2', status: '正常', idCardReader: '正常', printer: '正常', encryptModule: '正常' },
  { id: 14, deviceNo: 'ZX-2024-014', hallName: '武汉市政务服务中心', window: '大厅1号', status: '正常', idCardReader: '正常', printer: '正常', encryptModule: '故障' },
  { id: 15, deviceNo: 'ZX-2024-015', hallName: '武汉市政务服务中心', window: '大厅2号', status: '故障', idCardReader: '故障', printer: '故障', encryptModule: '正常' }
]

export const workOrders = []

export function generateOrderNo() {
  const date = new Date()
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const random = String(Math.floor(Math.random() * 10000)).padStart(4, '0')
  return `GD${year}${month}${day}${random}`
}
