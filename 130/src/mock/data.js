export const repairTypes = [
  { value: '1', label: '水电维修' },
  { value: '2', label: '管道疏通' },
  { value: '3', label: '电器维修' },
  { value: '4', label: '门窗维修' },
  { value: '5', label: '墙面地面' },
  { value: '6', label: '其他维修' }
]

export const urgencyLevels = [
  { value: '1', label: '一般' },
  { value: '2', label: '紧急' },
  { value: '3', label: '非常紧急' }
]

export const statusOptions = [
  { value: '0', label: '待派单', color: '#E6A23C' },
  { value: '1', label: '已派单', color: '#409EFF' },
  { value: '2', label: '维修中', color: '#909399' },
  { value: '3', label: '已完成', color: '#67C23A' },
  { value: '4', label: '已评价', color: '#67C23A' }
]

export const buildingOptions = [
  { value: '1', label: '1栋' },
  { value: '2', label: '2栋' },
  { value: '3', label: '3栋' },
  { value: '4', label: '4栋' },
  { value: '5', label: '5栋' },
  { value: '6', label: '6栋' },
  { value: '7', label: '7栋' },
  { value: '8', label: '8栋' }
]

export const repairList = [
  {
    id: '1',
    title: '客厅灯不亮',
    type: '1',
    typeName: '水电维修',
    description: '客厅主灯突然不亮了，检查开关没问题，可能是灯泡或线路问题。',
    building: '1',
    buildingName: '1栋',
    address: '1栋2单元301室',
    contact: '张三',
    phone: '13800138001',
    urgency: '2',
    urgencyName: '紧急',
    status: '0',
    createTime: '2024-01-15 10:30:00'
  },
  {
    id: '2',
    title: '厨房下水道堵塞',
    type: '2',
    typeName: '管道疏通',
    description: '厨房洗菜池下水很慢，可能有油污堵塞，需要疏通。',
    building: '2',
    buildingName: '2栋',
    address: '2栋1单元102室',
    contact: '李四',
    phone: '13800138002',
    urgency: '1',
    urgencyName: '一般',
    status: '1',
    worker: '王师傅',
    workerPhone: '13900139001',
    createTime: '2024-01-14 15:20:00',
    dispatchTime: '2024-01-14 16:00:00'
  },
  {
    id: '3',
    title: '空调不制冷',
    type: '3',
    typeName: '电器维修',
    description: '卧室空调开机后吹热风，不制冷，需要检查维修。',
    building: '3',
    buildingName: '3栋',
    address: '3栋3单元501室',
    contact: '王五',
    phone: '13800138003',
    urgency: '3',
    urgencyName: '非常紧急',
    status: '2',
    worker: '李师傅',
    workerPhone: '13900139002',
    createTime: '2024-01-13 09:00:00',
    dispatchTime: '2024-01-13 10:00:00',
    startTime: '2024-01-13 14:00:00'
  },
  {
    id: '4',
    title: '房门把手松动',
    type: '4',
    typeName: '门窗维修',
    description: '主卧房门把手松动，开关门不方便，需要紧固或更换。',
    building: '1',
    buildingName: '1栋',
    address: '1栋1单元201室',
    contact: '赵六',
    phone: '13800138004',
    urgency: '1',
    urgencyName: '一般',
    status: '3',
    worker: '张师傅',
    workerPhone: '13900139003',
    createTime: '2024-01-12 11:30:00',
    dispatchTime: '2024-01-12 14:00:00',
    startTime: '2024-01-12 15:00:00',
    completeTime: '2024-01-12 16:30:00'
  },
  {
    id: '5',
    title: '卫生间漏水',
    type: '5',
    typeName: '墙面地面',
    description: '卫生间地面防水层老化，漏水到楼下。',
    building: '4',
    buildingName: '4栋',
    address: '4栋2单元101室',
    contact: '钱七',
    phone: '13800138005',
    urgency: '2',
    urgencyName: '紧急',
    status: '0',
    createTime: '2024-01-16 09:00:00'
  },
  {
    id: '6',
    title: '电梯故障',
    type: '6',
    typeName: '其他维修',
    description: '2号电梯经常停运，按钮不灵敏，需要维修。',
    building: '2',
    buildingName: '2栋',
    address: '2栋电梯',
    contact: '物业',
    phone: '13800138006',
    urgency: '3',
    urgencyName: '非常紧急',
    status: '1',
    worker: '陈师傅',
    workerPhone: '13900139004',
    createTime: '2024-01-16 10:00:00',
    dispatchTime: '2024-01-16 10:30:00'
  },
  {
    id: '7',
    title: '门禁系统故障',
    type: '6',
    typeName: '其他维修',
    description: '单元门门禁无法刷卡开门，已影响业主正常出入。',
    building: '3',
    buildingName: '3栋',
    address: '3栋1单元门禁',
    contact: '孙八',
    phone: '13800138007',
    urgency: '2',
    urgencyName: '紧急',
    status: '2',
    worker: '陈师傅',
    workerPhone: '13900139004',
    createTime: '2024-01-17 08:30:00',
    dispatchTime: '2024-01-17 09:00:00',
    startTime: '2024-01-17 10:00:00'
  },
  {
    id: '8',
    title: '窗户玻璃破裂',
    type: '4',
    typeName: '门窗维修',
    description: '客厅落地窗玻璃被杂物击中破裂，存在安全隐患。',
    building: '5',
    buildingName: '5栋',
    address: '5栋3单元1202室',
    contact: '周九',
    phone: '13800138008',
    urgency: '1',
    urgencyName: '一般',
    status: '3',
    worker: '张师傅',
    workerPhone: '13900139003',
    createTime: '2024-01-18 14:00:00',
    dispatchTime: '2024-01-18 15:00:00',
    startTime: '2024-01-18 16:00:00',
    completeTime: '2024-01-18 18:00:00'
  }
]

export const workers = [
  { id: '1', name: '王师傅', phone: '13900139001', skill: '水电、管道' },
  { id: '2', name: '李师傅', phone: '13900139002', skill: '电器维修' },
  { id: '3', name: '张师傅', phone: '13900139003', skill: '门窗、墙面' },
  { id: '4', name: '陈师傅', phone: '13900139004', skill: '综合维修' }
]

export const progressSteps = [
  { status: 'submit', title: '提交报修', description: '业主提交报修申请' },
  { status: 'dispatch', title: '派单', description: '物业分配维修人员' },
  { status: 'processing', title: '维修中', description: '维修人员上门服务' },
  { status: 'complete', title: '完成', description: '维修完成待评价' },
  { status: 'evaluate', title: '已评价', description: '业主已评价' }
]
