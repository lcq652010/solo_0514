export const materials = [
  {
    id: 1,
    name: '联想笔记本电脑',
    category: '电子设备',
    specification: 'ThinkPad X1 Carbon',
    unit: '台',
    quantity: 50,
    available: 32,
    location: 'A区3楼库房',
    status: 'normal',
    description: '高性能商务笔记本'
  },
  {
    id: 2,
    name: '罗技无线鼠标',
    category: '电子配件',
    specification: 'M185',
    unit: '个',
    quantity: 200,
    available: 156,
    location: 'B区1楼库房',
    status: 'normal',
    description: '2.4G无线办公鼠标'
  },
  {
    id: 3,
    name: '得力文件袋',
    category: '办公用品',
    specification: 'A4 按扣款',
    unit: '个',
    quantity: 500,
    available: 320,
    location: 'C区2楼库房',
    status: 'normal',
    description: '加厚防水文件袋'
  },
  {
    id: 4,
    name: '晨光签字笔',
    category: '办公用品',
    specification: '0.5mm 黑色',
    unit: '支',
    quantity: 1000,
    available: 789,
    location: 'C区2楼库房',
    status: 'normal',
    description: '中性笔 办公常用'
  },
  {
    id: 5,
    name: '惠普激光打印机',
    category: '办公设备',
    specification: 'LaserJet Pro M404dn',
    unit: '台',
    quantity: 20,
    available: 8,
    location: 'A区3楼库房',
    status: 'normal',
    description: '高速黑白激光打印机'
  },
  {
    id: 6,
    name: '移动硬盘',
    category: '电子设备',
    specification: '西部数据 2TB',
    unit: '个',
    quantity: 30,
    available: 12,
    location: 'A区3楼库房',
    status: 'normal',
    description: 'USB3.0 高速传输'
  },
  {
    id: 7,
    name: '会议投影仪',
    category: '办公设备',
    specification: '爱普生 CB-X49',
    unit: '台',
    quantity: 10,
    available: 3,
    location: 'B区1楼库房',
    status: 'low',
    description: '3600流明 高清商务投影仪'
  },
  {
    id: 8,
    name: '打印纸 A4',
    category: '办公用品',
    specification: '70g 500张/包',
    unit: '包',
    quantity: 1000,
    available: 0,
    location: 'C区2楼库房',
    status: 'empty',
    description: '高白度复印纸'
  }
]

function generateApplyRecords() {
  const records = []
  const applicants = ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十', '郑一', '王二']
  const departments = ['研发部', '市场部', '销售部', '人事部', '财务部', '行政部', '产品部', '运营部']
  const statuses = ['pending', 'approved', 'rejected', 'returned']
  const approvers = ['李经理', '王主管', '张总监', '刘主任']
  const purposes = ['项目开发使用', '展会活动使用', '日常办公使用', '客户演示使用', '培训使用', '会议使用', '临时项目使用']
  
  for (let i = 1; i <= 1000; i++) {
    const material = materials[Math.floor(Math.random() * materials.length)]
    const status = statuses[Math.floor(Math.random() * statuses.length)]
    const applyDate = new Date(2024, 0, Math.floor(Math.random() * 120) + 1)
    const expectReturnDate = new Date(applyDate.getTime() + Math.random() * 30 * 24 * 60 * 60 * 1000)
    const isApproved = status === 'approved' || status === 'returned'
    const isRejected = status === 'rejected'
    const isReturned = status === 'returned'
    
    records.push({
      id: i,
      materialId: material.id,
      materialName: material.name,
      specification: material.specification,
      applicant: applicants[Math.floor(Math.random() * applicants.length)],
      department: departments[Math.floor(Math.random() * departments.length)],
      applyQuantity: Math.floor(Math.random() * 10) + 1,
      applyDate: applyDate.toISOString().split('T')[0],
      expectReturnDate: expectReturnDate.toISOString().split('T')[0],
      purpose: purposes[Math.floor(Math.random() * purposes.length)],
      status: status,
      approver: isApproved || isRejected ? approvers[Math.floor(Math.random() * approvers.length)] : null,
      approveDate: isApproved || isRejected ? new Date(applyDate.getTime() + Math.random() * 3 * 24 * 60 * 60 * 1000).toISOString().split('T')[0] : null,
      actualReturnDate: isReturned ? new Date(expectReturnDate.getTime() - Math.random() * 5 * 24 * 60 * 60 * 1000).toISOString().split('T')[0] : null,
      rejectReason: isRejected ? '库存不足，请等待补货' : null
    })
  }
  return records
}

export const applyRecords = generateApplyRecords()

export const categoryOptions = [
  { value: '电子设备', label: '电子设备' },
  { value: '电子配件', label: '电子配件' },
  { value: '办公用品', label: '办公用品' },
  { value: '办公设备', label: '办公设备' }
]

export const statusOptions = [
  { value: 'pending', label: '待审批' },
  { value: 'approved', label: '已通过' },
  { value: 'rejected', label: '已拒绝' },
  { value: 'returned', label: '已归还' }
]
