export const mockStudents = [
  { id: 1, name: '张三', phone: '13800138001', className: 'Python入门班', remainHours: 28, totalHours: 50, status: '在读', enrollDate: '2024-01-15' },
  { id: 2, name: '李四', phone: '13800138002', className: 'Java进阶班', remainHours: 15, totalHours: 40, status: '在读', enrollDate: '2024-02-20' },
  { id: 3, name: '王五', phone: '13800138003', className: 'Web前端班', remainHours: 42, totalHours: 60, status: '在读', enrollDate: '2024-01-08' },
  { id: 4, name: '赵六', phone: '13800138004', className: 'Python入门班', remainHours: 0, totalHours: 30, status: '停课', enrollDate: '2023-11-10' },
  { id: 5, name: '孙七', phone: '13800138005', className: 'UI设计班', remainHours: 35, totalHours: 45, status: '在读', enrollDate: '2024-03-01' },
  { id: 6, name: '周八', phone: '13800138006', className: 'Java进阶班', remainHours: 8, totalHours: 40, status: '在读', enrollDate: '2024-02-15' },
  { id: 7, name: '吴九', phone: '13800138007', className: 'Web前端班', remainHours: 20, totalHours: 60, status: '在读', enrollDate: '2024-01-25' },
  { id: 8, name: '郑十', phone: '13800138008', className: 'Python入门班', remainHours: 12, totalHours: 50, status: '在读', enrollDate: '2024-02-05' }
];

export const mockAttendance = [
  { id: 1, studentId: 1, studentName: '张三', className: 'Python入门班', date: '2024-05-16', status: '正常', signInTime: '09:05', signOutTime: '11:30' },
  { id: 2, studentId: 2, studentName: '李四', className: 'Java进阶班', date: '2024-05-16', status: '正常', signInTime: '14:00', signOutTime: '16:45' },
  { id: 3, studentId: 3, studentName: '王五', className: 'Web前端班', date: '2024-05-16', status: '迟到', signInTime: '09:20', signOutTime: '11:30' },
  { id: 4, studentId: 5, studentName: '孙七', className: 'UI设计班', date: '2024-05-16', status: '正常', signInTime: '09:00', signOutTime: '11:25' },
  { id: 5, studentId: 1, studentName: '张三', className: 'Python入门班', date: '2024-05-15', status: '正常', signInTime: '09:02', signOutTime: '11:28' },
  { id: 6, studentId: 4, studentName: '赵六', className: 'Python入门班', date: '2024-05-15', status: '缺勤', signInTime: '-', signOutTime: '-' },
  { id: 7, studentId: 6, studentName: '周八', className: 'Java进阶班', date: '2024-05-15', status: '正常', signInTime: '14:05', signOutTime: '16:50' }
];

export const mockDeductions = [
  { id: 1, studentName: '张三', className: 'Python入门班', date: '2024-05-16', courseName: 'Python基础语法', hours: 2.5, remainHours: 28, operator: '王老师' },
  { id: 2, studentName: '李四', className: 'Java进阶班', date: '2024-05-16', courseName: 'Spring框架', hours: 3, remainHours: 15, operator: '李老师' },
  { id: 3, studentName: '王五', className: 'Web前端班', date: '2024-05-16', courseName: 'Vue.js实战', hours: 2.5, remainHours: 42, operator: '张老师' },
  { id: 4, studentName: '孙七', className: 'UI设计班', date: '2024-05-15', courseName: 'Photoshop基础', hours: 2, remainHours: 35, operator: '陈老师' },
  { id: 5, studentName: '张三', className: 'Python入门班', date: '2024-05-15', courseName: 'Python函数', hours: 2.5, remainHours: 30.5, operator: '王老师' },
  { id: 6, studentName: '周八', className: 'Java进阶班', date: '2024-05-15', courseName: 'MyBatis详解', hours: 3, remainHours: 11, operator: '李老师' },
  { id: 7, studentName: '吴九', className: 'Web前端班', date: '2024-05-14', courseName: 'CSS布局', hours: 2, remainHours: 22, operator: '张老师' }
];

export const mockSchedule = [
  { id: 1, className: 'Python入门班', weekDay: '周一', time: '09:00-11:30', courseName: 'Python基础语法', teacher: '王老师', classroom: 'A101' },
  { id: 2, className: 'Python入门班', weekDay: '周三', time: '09:00-11:30', courseName: 'Python函数与模块', teacher: '王老师', classroom: 'A101' },
  { id: 3, className: 'Python入门班', weekDay: '周五', time: '09:00-11:30', courseName: 'Python面向对象', teacher: '王老师', classroom: 'A101' },
  { id: 4, className: 'Java进阶班', weekDay: '周二', time: '14:00-17:00', courseName: 'Spring框架', teacher: '李老师', classroom: 'B202' },
  { id: 5, className: 'Java进阶班', weekDay: '周四', time: '14:00-17:00', courseName: 'MyBatis详解', teacher: '李老师', classroom: 'B202' },
  { id: 6, className: 'Java进阶班', weekDay: '周六', time: '09:00-12:00', courseName: '项目实战', teacher: '李老师', classroom: 'B202' },
  { id: 7, className: 'Web前端班', weekDay: '周一', time: '14:00-16:30', courseName: 'HTML/CSS基础', teacher: '张老师', classroom: 'C303' },
  { id: 8, className: 'Web前端班', weekDay: '周三', time: '14:00-16:30', courseName: 'JavaScript进阶', teacher: '张老师', classroom: 'C303' },
  { id: 9, className: 'Web前端班', weekDay: '周五', time: '14:00-16:30', courseName: 'Vue.js实战', teacher: '张老师', classroom: 'C303' },
  { id: 10, className: 'UI设计班', weekDay: '周二', time: '09:00-11:30', courseName: 'Photoshop基础', teacher: '陈老师', classroom: 'D404' },
  { id: 11, className: 'UI设计班', weekDay: '周四', time: '09:00-11:30', courseName: 'UI设计原理', teacher: '陈老师', classroom: 'D404' },
  { id: 12, className: 'UI设计班', weekDay: '周六', time: '14:00-17:00', courseName: '项目实战', teacher: '陈老师', classroom: 'D404' }
];

export const classOptions = ['Python入门班', 'Java进阶班', 'Web前端班', 'UI设计班'];
export const weekDays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'];
