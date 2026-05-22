export const rooms = [
  {
    id: 1,
    name: '多功能会议厅',
    capacity: 50,
    location: 'A栋3楼',
    equipment: ['投影仪', '白板', '音响系统', '视频会议设备'],
    status: 'available'
  },
  {
    id: 2,
    name: '小型会议室A',
    capacity: 8,
    location: 'B栋2楼',
    equipment: ['投影仪', '白板'],
    status: 'occupied'
  },
  {
    id: 3,
    name: '小型会议室B',
    capacity: 6,
    location: 'B栋2楼',
    equipment: ['电视', '白板'],
    status: 'available'
  },
  {
    id: 4,
    name: '中型会议室',
    capacity: 20,
    location: 'A栋2楼',
    equipment: ['投影仪', '白板', '音响系统'],
    status: 'maintenance'
  },
  {
    id: 5,
    name: '培训室',
    capacity: 30,
    location: 'C栋1楼',
    equipment: ['投影仪', '白板', '音响系统', '录播设备'],
    status: 'available'
  },
  {
    id: 6,
    name: '高管会议室',
    capacity: 12,
    location: 'A栋10楼',
    equipment: ['投影仪', '白板', '视频会议设备', '茶水服务'],
    status: 'available'
  }
]

export const statusMap = {
  available: { label: '空闲', type: 'success' },
  occupied: { label: '使用中', type: 'danger' },
  maintenance: { label: '维护中', type: 'warning' }
}
