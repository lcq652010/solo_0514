export const jobList = [
  { id: 1, name: '高级前端工程师', department: '技术部', type: '技术开发', salary: '25k-35k', location: '北京', status: '招聘中', people: 3, publishTime: '2026-05-10', description: '负责公司核心产品的前端开发工作' },
  { id: 2, name: 'Java后端开发工程师', department: '技术部', type: '技术开发', salary: '20k-30k', location: '上海', status: '招聘中', people: 2, publishTime: '2026-05-08', description: '负责后端服务的设计与开发' },
  { id: 3, name: '产品经理', department: '产品部', type: '产品设计', salary: '20k-28k', location: '深圳', status: '招聘中', people: 1, publishTime: '2026-05-05', description: '负责产品规划与需求分析' },
  { id: 4, name: 'UI设计师', department: '设计部', type: '设计', salary: '15k-22k', location: '广州', status: '已暂停', people: 1, publishTime: '2026-05-03', description: '负责产品界面设计' },
  { id: 5, name: '数据分析师', department: '数据部', type: '数据分析', salary: '18k-25k', location: '北京', status: '招聘中', people: 2, publishTime: '2026-05-01', description: '负责业务数据分析与报告' },
  { id: 6, name: '测试工程师', department: '技术部', type: '技术开发', salary: '12k-18k', location: '杭州', status: '招聘中', people: 2, publishTime: '2026-04-28', description: '负责软件测试与质量保证' }
]

export const departmentOptions = [
  { value: '技术部', label: '技术部' },
  { value: '产品部', label: '产品部' },
  { value: '设计部', label: '设计部' },
  { value: '数据部', label: '数据部' },
  { value: '市场部', label: '市场部' },
  { value: '人事部', label: '人事部' }
]

export const jobTypeOptions = [
  { value: '技术开发', label: '技术开发' },
  { value: '产品设计', label: '产品设计' },
  { value: '设计', label: '设计' },
  { value: '数据分析', label: '数据分析' },
  { value: '市场运营', label: '市场运营' },
  { value: '人力资源', label: '人力资源' }
]

export const applicationList = [
  { id: 1, name: '张三', phone: '13800138001', email: 'zhangsan@example.com', jobName: '高级前端工程师', applyTime: '2026-05-15', status: '待面试', resume: '张三_前端.pdf' },
  { id: 2, name: '李四', phone: '13800138002', email: 'lisi@example.com', jobName: 'Java后端开发工程师', applyTime: '2026-05-14', status: '面试中', resume: '李四_后端.pdf' },
  { id: 3, name: '王五', phone: '13800138003', email: 'wangwu@example.com', jobName: '产品经理', applyTime: '2026-05-13', status: '已录用', resume: '王五_产品.pdf' },
  { id: 4, name: '赵六', phone: '13800138004', email: 'zhaoliu@example.com', jobName: 'UI设计师', applyTime: '2026-05-12', status: '待审核', resume: '赵六_设计.pdf' },
  { id: 5, name: '钱七', phone: '13800138005', email: 'qianqi@example.com', jobName: '数据分析师', applyTime: '2026-05-11', status: '已拒绝', resume: '钱七_数据.pdf' },
  { id: 6, name: '孙八', phone: '13800138006', email: 'sunba@example.com', jobName: '测试工程师', applyTime: '2026-05-10', status: '待面试', resume: '孙八_测试.pdf' },
  { id: 7, name: '周九', phone: '13800138007', email: 'zhoujiu@example.com', jobName: '高级前端工程师', applyTime: '2026-05-09', status: '面试中', resume: '周九_前端.pdf' },
  { id: 8, name: '吴十', phone: '13800138008', email: 'wushi@example.com', jobName: 'Java后端开发工程师', applyTime: '2026-05-08', status: '待录用', resume: '吴十_后端.pdf' }
]

export const interviewList = [
  { id: 1, candidateName: '张三', jobName: '高级前端工程师', interviewer: '李经理', type: '技术一面', time: '2026-05-18 10:00', location: '会议室A', status: '未开始', result: '' },
  { id: 2, candidateName: '李四', jobName: 'Java后端开发工程师', interviewer: '王总监', type: '技术二面', time: '2026-05-18 14:00', location: '会议室B', status: '未开始', result: '' },
  { id: 3, candidateName: '王五', jobName: '产品经理', interviewer: '赵副总', type: 'HR面试', time: '2026-05-17 15:30', location: '会议室C', status: '已完成', result: '通过' },
  { id: 4, candidateName: '周九', jobName: '高级前端工程师', interviewer: '李经理', type: '技术二面', time: '2026-05-17 09:00', location: '会议室A', status: '已完成', result: '待定' },
  { id: 5, candidateName: '吴十', jobName: 'Java后端开发工程师', interviewer: '王总监', type: 'HR面试', time: '2026-05-16 16:00', location: '会议室D', status: '已完成', result: '通过' }
]

export const interviewerOptions = [
  { value: '李经理', label: '李经理（技术部）' },
  { value: '王总监', label: '王总监（技术部）' },
  { value: '赵副总', label: '赵副总（产品部）' },
  { value: '张经理', label: '张经理（HR）' },
  { value: '刘主管', label: '刘主管（设计部）' }
]

export const interviewTypeOptions = [
  { value: '技术一面', label: '技术一面' },
  { value: '技术二面', label: '技术二面' },
  { value: '技术终面', label: '技术终面' },
  { value: 'HR面试', label: 'HR面试' },
  { value: '综合面试', label: '综合面试' }
]

export const offerList = [
  { id: 1, candidateName: '王五', jobName: '产品经理', salary: '25k', offerTime: '2026-05-17', entryTime: '2026-06-01', status: '待确认', remark: '薪资已谈妥，等待回复' },
  { id: 2, candidateName: '吴十', jobName: 'Java后端开发工程师', salary: '28k', offerTime: '2026-05-16', entryTime: '2026-06-15', status: '已接受', remark: '已确认入职时间' },
  { id: 3, candidateName: '陈明', jobName: '数据分析师', salary: '22k', offerTime: '2026-05-10', entryTime: '2026-05-30', status: '已入职', remark: '已完成入职手续' },
  { id: 4, candidateName: '刘芳', jobName: 'UI设计师', salary: '18k', offerTime: '2026-05-05', entryTime: '2026-05-20', status: '已拒绝', remark: '候选人选择其他公司' }
]

export const statusOptions = [
  { value: '待审核', label: '待审核' },
  { value: '待面试', label: '待面试' },
  { value: '面试中', label: '面试中' },
  { value: '待录用', label: '待录用' },
  { value: '已录用', label: '已录用' },
  { value: '已拒绝', label: '已拒绝' }
]
