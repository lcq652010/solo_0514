export const examTypeList = [
  { value: 'computer', label: '计算机类' },
  { value: 'english', label: '英语类' },
  { value: 'teacher', label: '教师类' }
]

export const subjectList = [
  {
    id: 1,
    name: '计算机等级考试-二级C语言',
    code: 'NCRE-2C',
    examType: 'computer',
    examDate: '2024-06-15',
    examTime: '09:00-11:00',
    fee: 80,
    quota: 500,
    enrolled: 320,
    status: 1,
    description: '全国计算机等级考试二级C语言程序设计',
    requirements: {
      minAge: 16,
      maxAge: 60,
      minEducation: '高中及以下',
      prerequisite: []
    }
  },
  {
    id: 2,
    name: '计算机等级考试-二级Java',
    code: 'NCRE-2J',
    examType: 'computer',
    examDate: '2024-06-15',
    examTime: '14:00-16:00',
    fee: 80,
    quota: 500,
    enrolled: 280,
    status: 1,
    description: '全国计算机等级考试二级Java语言程序设计',
    requirements: {
      minAge: 16,
      maxAge: 60,
      minEducation: '高中及以下',
      prerequisite: []
    }
  },
  {
    id: 3,
    name: '计算机等级考试-二级Python',
    code: 'NCRE-2P',
    examType: 'computer',
    examDate: '2024-06-16',
    examTime: '09:00-11:00',
    fee: 80,
    quota: 500,
    enrolled: 410,
    status: 1,
    description: '全国计算机等级考试二级Python语言程序设计',
    requirements: {
      minAge: 16,
      maxAge: 60,
      minEducation: '高中及以下',
      prerequisite: []
    }
  },
  {
    id: 4,
    name: '英语四级考试',
    code: 'CET-4',
    examType: 'english',
    examDate: '2024-06-22',
    examTime: '09:00-11:20',
    fee: 30,
    quota: 2000,
    enrolled: 1850,
    status: 1,
    description: '全国大学英语四级考试',
    requirements: {
      minAge: 18,
      maxAge: null,
      minEducation: '大专',
      prerequisite: []
    }
  },
  {
    id: 5,
    name: '英语六级考试',
    code: 'CET-6',
    examType: 'english',
    examDate: '2024-06-22',
    examTime: '15:00-17:25',
    fee: 30,
    quota: 1500,
    enrolled: 1200,
    status: 1,
    description: '全国大学英语六级考试',
    requirements: {
      minAge: 18,
      maxAge: null,
      minEducation: '大专',
      prerequisite: ['英语四级考试']
    }
  },
  {
    id: 6,
    name: '教师资格证-小学教育',
    code: 'TEC-PRIM',
    examType: 'teacher',
    examDate: '2024-07-01',
    examTime: '09:00-11:00',
    fee: 60,
    quota: 800,
    enrolled: 650,
    status: 0,
    description: '中小学教师资格考试-小学教育知识与能力',
    requirements: {
      minAge: 20,
      maxAge: null,
      minEducation: '大专',
      prerequisite: []
    }
  }
]

export const educationLevel = {
  '高中及以下': 1,
  '大专': 2,
  '本科': 3,
  '硕士': 4,
  '博士': 5
}

export const ticketList = []

export const applicationRecords = [
  {
    id: 1,
    applicantName: '张三',
    idCard: '110101199901011234',
    phone: '13800138001',
    email: 'zhangsan@example.com',
    subjectId: 1,
    subjectName: '计算机等级考试-二级C语言',
    subjectCode: 'NCRE-2C',
    examDate: '2024-06-15',
    examTime: '09:00-11:00',
    applyTime: '2024-05-10 10:30:00',
    status: 2,
    reviewTime: '2024-05-11 14:00:00',
    reviewer: '管理员A'
  },
  {
    id: 2,
    applicantName: '李四',
    idCard: '110101199902022345',
    phone: '13800138002',
    email: 'lisi@example.com',
    subjectId: 4,
    subjectName: '英语四级考试',
    subjectCode: 'CET-4',
    examDate: '2024-06-22',
    examTime: '09:00-11:20',
    applyTime: '2024-05-12 09:15:00',
    status: 1,
    reviewTime: '',
    reviewer: ''
  },
  {
    id: 3,
    applicantName: '王五',
    idCard: '110101199903033456',
    phone: '13800138003',
    email: 'wangwu@example.com',
    subjectId: 2,
    subjectName: '计算机等级考试-二级Java',
    subjectCode: 'NCRE-2J',
    examDate: '2024-06-15',
    examTime: '14:00-16:00',
    applyTime: '2024-05-13 16:45:00',
    status: 3,
    reviewTime: '2024-05-14 10:00:00',
    reviewer: '管理员B',
    rejectReason: '身份证信息不清晰'
  }
]

export const statusMap = {
  0: '未开始',
  1: '报名中',
  2: '已结束'
}

export const applyStatusMap = {
  1: '待审核',
  2: '审核通过',
  3: '审核不通过'
}

export const applyStatusTagType = {
  1: 'warning',
  2: 'success',
  3: 'danger'
}
