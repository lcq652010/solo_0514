export const meetings = [
  {
    id: 1,
    title: 'Q2季度产品规划会议',
    roomId: 1,
    roomName: '多功能会议厅',
    date: '2026-05-20',
    startTime: '09:00',
    endTime: '11:00',
    organizer: '钱七',
    attendees: [1, 4, 5, 8, 12],
    attendeeNames: ['张三', '赵六', '钱七', '吴十', '陈十四'],
    description: '讨论Q2季度产品路线图和重点功能规划',
    minutes: '',
    status: 'upcoming'
  },
  {
    id: 2,
    title: '前端技术分享',
    roomId: 2,
    roomName: '小型会议室A',
    date: '2026-05-18',
    startTime: '14:00',
    endTime: '15:30',
    organizer: '李四',
    attendees: [1, 2, 3],
    attendeeNames: ['张三', '李四', '王五'],
    description: 'Vue3 Composition API 最佳实践分享',
    minutes: '1. Vue3 Composition API 基础语法介绍\n2. 响应式原理深入解析\n3. 实际项目中的应用案例\n4. 与 Options API 的对比分析\n5. 迁移注意事项和常见问题',
    status: 'completed'
  },
  {
    id: 3,
    title: 'UI设计评审',
    roomId: 3,
    roomName: '小型会议室B',
    date: '2026-05-19',
    startTime: '10:00',
    endTime: '11:30',
    organizer: '孙八',
    attendees: [4, 6, 7],
    attendeeNames: ['赵六', '孙八', '周九'],
    description: '新版本首页设计方案评审',
    minutes: '',
    status: 'upcoming'
  },
  {
    id: 4,
    title: '市场推广方案讨论',
    roomId: 5,
    roomName: '培训室',
    date: '2026-05-17',
    startTime: '14:00',
    endTime: '16:00',
    organizer: '吴十',
    attendees: [5, 8, 9, 12],
    attendeeNames: ['钱七', '吴十', '郑十一', '陈十四'],
    description: '讨论新产品上市推广方案',
    minutes: '1. 确定推广目标和KPI\n2. 线上推广渠道选择：抖音、小红书、微信公众号\n3. 线下活动规划：行业展会、用户沙龙\n4. 预算分配方案\n5. 时间节点和责任人确认',
    status: 'completed'
  },
  {
    id: 5,
    title: '新员工入职培训',
    roomId: 5,
    roomName: '培训室',
    date: '2026-05-25',
    startTime: '09:00',
    endTime: '17:00',
    organizer: '王十二',
    attendees: [10, 11],
    attendeeNames: ['王十二', '刘十三'],
    description: '5月新员工入职培训',
    minutes: '',
    status: 'upcoming'
  },
  {
    id: 6,
    title: '周例会',
    roomId: 2,
    roomName: '小型会议室A',
    date: '2026-05-16',
    startTime: '10:00',
    endTime: '10:30',
    organizer: '张三',
    attendees: [1, 2, 3],
    attendeeNames: ['张三', '李四', '王五'],
    description: '技术部周例会',
    minutes: '1. 上周工作完成情况汇报\n2. 本周工作计划安排\n3. 项目进度同步\n4. 问题讨论与解决方案',
    status: 'completed'
  }
]

export const meetingStatusMap = {
  upcoming: { label: '即将开始', type: 'primary' },
  completed: { label: '已结束', type: 'success' },
  cancelled: { label: '已取消', type: 'info' }
}
