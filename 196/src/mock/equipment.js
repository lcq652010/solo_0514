export const equipment = [
  {
    id: 1,
    name: '便携式投影仪',
    model: 'Epson CB-X06',
    status: 'available',
    borrower: '',
    borrowDate: '',
    expectedReturn: ''
  },
  {
    id: 2,
    name: '无线麦克风',
    model: 'Sennheiser XSW 1-835',
    status: 'borrowed',
    borrower: '李四',
    borrowDate: '2026-05-17',
    expectedReturn: '2026-05-20'
  },
  {
    id: 3,
    name: '笔记本电脑',
    model: 'MacBook Pro 16',
    status: 'available',
    borrower: '',
    borrowDate: '',
    expectedReturn: ''
  },
  {
    id: 4,
    name: '移动白板',
    model: 'Plus N-20J',
    status: 'available',
    borrower: '',
    borrowDate: '',
    expectedReturn: ''
  },
  {
    id: 5,
    name: '高清摄像头',
    model: 'Logitech C930e',
    status: 'maintenance',
    borrower: '',
    borrowDate: '',
    expectedReturn: ''
  },
  {
    id: 6,
    name: '便携式音响',
    model: 'Bose SoundLink Revolve+',
    status: 'available',
    borrower: '',
    borrowDate: '',
    expectedReturn: ''
  },
  {
    id: 7,
    name: '激光翻页笔',
    model: 'Logitech R800',
    status: 'borrowed',
    borrower: '赵六',
    borrowDate: '2026-05-18',
    expectedReturn: '2026-05-19'
  },
  {
    id: 8,
    name: '视频会议终端',
    model: 'Poly Studio X30',
    status: 'available',
    borrower: '',
    borrowDate: '',
    expectedReturn: ''
  }
]

export const equipmentStatusMap = {
  available: { label: '可借用', type: 'success' },
  borrowed: { label: '已借出', type: 'warning' },
  maintenance: { label: '维护中', type: 'info' }
}

export const borrowRecords = [
  {
    id: 1,
    equipmentName: '无线麦克风',
    model: 'Sennheiser XSW 1-835',
    borrower: '李四',
    borrowDate: '2026-05-17',
    expectedReturn: '2026-05-20',
    actualReturn: '',
    status: 'borrowing'
  },
  {
    id: 2,
    equipmentName: '激光翻页笔',
    model: 'Logitech R800',
    borrower: '赵六',
    borrowDate: '2026-05-18',
    expectedReturn: '2026-05-19',
    actualReturn: '',
    status: 'borrowing'
  },
  {
    id: 3,
    equipmentName: '便携式投影仪',
    model: 'Epson CB-X06',
    borrower: '张三',
    borrowDate: '2026-05-10',
    expectedReturn: '2026-05-12',
    actualReturn: '2026-05-12',
    status: 'returned'
  },
  {
    id: 4,
    equipmentName: '笔记本电脑',
    model: 'MacBook Pro 16',
    borrower: '王五',
    borrowDate: '2026-05-08',
    expectedReturn: '2026-05-10',
    actualReturn: '2026-05-10',
    status: 'returned'
  }
]
