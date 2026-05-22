export const courses = [
  {
    id: 1,
    name: 'Vue.js 从入门到精通',
    teacher: '张老师',
    category: '前端开发',
    duration: 48,
    students: 1256,
    price: 199,
    status: 'published',
    description: '全面系统学习 Vue.js 框架，掌握现代前端开发技能',
    createTime: '2024-01-15'
  },
  {
    id: 2,
    name: 'React 全家桶实战教程',
    teacher: '李老师',
    category: '前端开发',
    duration: 56,
    students: 987,
    price: 299,
    status: 'published',
    description: '深入学习 React 生态系统，打造企业级应用',
    createTime: '2024-02-20'
  },
  {
    id: 3,
    name: 'Node.js 后端开发实战',
    teacher: '王老师',
    category: '后端开发',
    duration: 40,
    students: 756,
    price: 249,
    status: 'published',
    description: '使用 Node.js 构建高性能后端服务',
    createTime: '2024-03-10'
  },
  {
    id: 4,
    name: 'Python 数据分析入门',
    teacher: '赵老师',
    category: '数据科学',
    duration: 36,
    students: 1523,
    price: 179,
    status: 'published',
    description: '从零开始学习 Python 数据分析技能',
    createTime: '2024-01-25'
  },
  {
    id: 5,
    name: 'Java 高级编程',
    teacher: '陈老师',
    category: '后端开发',
    duration: 64,
    students: 892,
    price: 399,
    status: 'draft',
    description: '深入理解 Java 高级特性与设计模式',
    createTime: '2024-04-05'
  },
  {
    id: 6,
    name: 'UI/UX 设计基础',
    teacher: '刘老师',
    category: '设计',
    duration: 32,
    students: 654,
    price: 159,
    status: 'published',
    description: '掌握用户界面与用户体验设计核心原理',
    createTime: '2024-02-28'
  }
]

export const myCourses = [
  {
    id: 1,
    name: 'Vue.js 从入门到精通',
    teacher: '张老师',
    progress: 75,
    totalChapters: 12,
    completedChapters: 9,
    enrollTime: '2024-03-01',
    lastLearnTime: '2024-05-10',
    status: 'learning'
  },
  {
    id: 4,
    name: 'Python 数据分析入门',
    teacher: '赵老师',
    progress: 30,
    totalChapters: 10,
    completedChapters: 3,
    enrollTime: '2024-04-15',
    lastLearnTime: '2024-05-08',
    status: 'learning'
  },
  {
    id: 2,
    name: 'React 全家桶实战教程',
    teacher: '李老师',
    progress: 100,
    totalChapters: 14,
    completedChapters: 14,
    enrollTime: '2024-02-10',
    lastLearnTime: '2024-04-20',
    status: 'completed'
  }
]

export const progressData = [
  {
    courseId: 1,
    courseName: 'Vue.js 从入门到精通',
    totalChapters: 12,
    completedChapters: 9,
    progress: 75,
    chapters: [
      { id: 1, name: 'Vue.js 简介与环境搭建', status: 'completed', duration: 45 },
      { id: 2, name: '模板语法与指令', status: 'completed', duration: 60 },
      { id: 3, name: '计算属性与侦听器', status: 'completed', duration: 55 },
      { id: 4, name: 'Class 与 Style 绑定', status: 'completed', duration: 40 },
      { id: 5, name: '条件渲染与列表渲染', status: 'completed', duration: 50 },
      { id: 6, name: '事件处理', status: 'completed', duration: 45 },
      { id: 7, name: '表单输入绑定', status: 'completed', duration: 55 },
      { id: 8, name: '组件基础', status: 'completed', duration: 70 },
      { id: 9, name: '组件通信', status: 'completed', duration: 80 },
      { id: 10, name: '插槽与自定义事件', status: 'in_progress', duration: 65 },
      { id: 11, name: 'Vue Router 使用', status: 'not_started', duration: 75 },
      { id: 12, name: 'Vuex 状态管理', status: 'not_started', duration: 90 }
    ],
    totalStudyTime: 720,
    lastStudyDate: '2024-05-10'
  },
  {
    courseId: 4,
    courseName: 'Python 数据分析入门',
    totalChapters: 10,
    completedChapters: 3,
    progress: 30,
    chapters: [
      { id: 1, name: 'Python 基础回顾', status: 'completed', duration: 60 },
      { id: 2, name: 'NumPy 数组操作', status: 'completed', duration: 75 },
      { id: 3, name: 'Pandas 数据处理', status: 'completed', duration: 90 },
      { id: 4, name: '数据可视化基础', status: 'in_progress', duration: 80 },
      { id: 5, name: 'Matplotlib 进阶', status: 'not_started', duration: 70 },
      { id: 6, name: 'Seaborn 统计图表', status: 'not_started', duration: 65 },
      { id: 7, name: '数据清洗实战', status: 'not_started', duration: 85 },
      { id: 8, name: '特征工程入门', status: 'not_started', duration: 75 },
      { id: 9, name: '机器学习基础', status: 'not_started', duration: 95 },
      { id: 10, name: '项目实战：电商数据分析', status: 'not_started', duration: 120 }
    ],
    totalStudyTime: 225,
    lastStudyDate: '2024-05-08'
  }
]

export const enrollmentRecords = [
  {
    id: 1,
    courseId: 1,
    name: '张三',
    phone: '13800138001',
    email: 'zhangsan@example.com',
    enrollTime: '2024-03-01 10:00:00'
  },
  {
    id: 2,
    courseId: 4,
    name: '李四',
    phone: '13800138002',
    email: 'lisi@example.com',
    enrollTime: '2024-04-15 14:30:00'
  },
  {
    id: 3,
    courseId: 2,
    name: '王五',
    phone: '13800138003',
    email: 'wangwu@example.com',
    enrollTime: '2024-02-10 09:15:00'
  }
]

export const homeworkList = [
  {
    id: 1,
    courseId: 1,
    courseName: 'Vue.js 从入门到精通',
    title: '第三章课后作业：计算属性实战',
    description: '使用计算属性实现一个购物车总价计算功能',
    deadline: '2024-05-20 23:59:59',
    status: 'not_submitted',
    score: null
  },
  {
    id: 2,
    courseId: 1,
    courseName: 'Vue.js 从入门到精通',
    title: '第五章课后作业：列表渲染练习',
    description: '实现一个待办事项列表，支持增删改查',
    deadline: '2024-05-25 23:59:59',
    status: 'not_submitted',
    score: null
  },
  {
    id: 3,
    courseId: 4,
    courseName: 'Python 数据分析入门',
    title: '第二章作业：NumPy 数组练习',
    description: '完成数组创建、索引、切片、运算等练习',
    deadline: '2024-05-18 23:59:59',
    status: 'submitted',
    submitTime: '2024-05-16 14:30:00',
    score: null
  },
  {
    id: 4,
    courseId: 2,
    courseName: 'React 全家桶实战教程',
    title: '期末大作业：React 项目实战',
    description: '使用 React + Redux 实现一个完整的博客系统',
    deadline: '2024-04-30 23:59:59',
    status: 'graded',
    submitTime: '2024-04-28 10:15:00',
    score: 92,
    comment: '完成度很高，代码规范，功能完整！'
  }
]
