export const departments = [
  { id: 1, name: '内科', description: '内科是医院的核心科室，主要诊治呼吸系统、消化系统、心血管系统等内科疾病。', doctorCount: 12, status: 1 },
  { id: 2, name: '外科', description: '外科主要开展普外科、骨科、神经外科等手术治疗，拥有先进的手术设备。', doctorCount: 10, status: 1 },
  { id: 3, name: '妇产科', description: '妇产科提供妇科疾病诊治、孕产妇保健、分娩服务等，设有VIP产房。', doctorCount: 8, status: 1 },
  { id: 4, name: '儿科', description: '儿科专注于儿童健康问题，包括新生儿护理、儿童预防接种等服务。', doctorCount: 6, status: 1 },
  { id: 5, name: '眼科', description: '眼科提供视力检查、白内障手术、青光眼治疗等眼科诊疗服务。', doctorCount: 5, status: 1 },
  { id: 6, name: '口腔科', description: '口腔科开展牙齿矫正、种植牙、口腔修复等口腔医疗服务。', doctorCount: 4, status: 1 },
  { id: 7, name: '皮肤科', description: '皮肤科诊治各类皮肤疾病，包括湿疹、银屑病、痤疮等。', doctorCount: 3, status: 1 },
  { id: 8, name: '中医科', description: '中医科提供中药调理、针灸、推拿等传统中医治疗服务。', doctorCount: 5, status: 0 }
];

export const doctors = [
  { id: 1, name: '张医生', departmentId: 1, department: '内科', title: '主任医师', specialty: '心血管疾病', experience: 20 },
  { id: 2, name: '李医生', departmentId: 1, department: '内科', title: '副主任医师', specialty: '呼吸系统', experience: 15 },
  { id: 3, name: '王医生', departmentId: 1, department: '内科', title: '主治医师', specialty: '消化系统', experience: 10 },
  { id: 4, name: '赵医生', departmentId: 2, department: '外科', title: '主任医师', specialty: '普外科', experience: 18 },
  { id: 5, name: '刘医生', departmentId: 2, department: '外科', title: '副主任医师', specialty: '骨科', experience: 12 },
  { id: 6, name: '陈医生', departmentId: 3, department: '妇产科', title: '主任医师', specialty: '妇产科', experience: 22 },
  { id: 7, name: '杨医生', departmentId: 4, department: '儿科', title: '副主任医师', specialty: '小儿内科', experience: 14 },
  { id: 8, name: '黄医生', departmentId: 5, department: '眼科', title: '主治医师', specialty: '白内障', experience: 8 }
];

export const schedules = [
  { id: 1, doctorId: 1, doctorName: '张医生', department: '内科', date: '2024-05-20', time: '上午', period: '08:00-12:00', total: 30, remaining: 15, fee: 50 },
  { id: 2, doctorId: 1, doctorName: '张医生', department: '内科', date: '2024-05-20', time: '下午', period: '14:00-17:30', total: 25, remaining: 20, fee: 50 },
  { id: 3, doctorId: 2, doctorName: '李医生', department: '内科', date: '2024-05-20', time: '上午', period: '08:00-12:00', total: 30, remaining: 8, fee: 45 },
  { id: 4, doctorId: 2, doctorName: '李医生', department: '内科', date: '2024-05-21', time: '上午', period: '08:00-12:00', total: 30, remaining: 25, fee: 45 },
  { id: 5, doctorId: 3, doctorName: '王医生', department: '内科', date: '2024-05-20', time: '下午', period: '14:00-17:30', total: 25, remaining: 22, fee: 35 },
  { id: 6, doctorId: 4, doctorName: '赵医生', department: '外科', date: '2024-05-20', time: '上午', period: '08:00-12:00', total: 20, remaining: 12, fee: 60 },
  { id: 7, doctorId: 4, doctorName: '赵医生', department: '外科', date: '2024-05-21', time: '下午', period: '14:00-17:30', total: 20, remaining: 18, fee: 60 },
  { id: 8, doctorId: 5, doctorName: '刘医生', department: '外科', date: '2024-05-20', time: '下午', period: '14:00-17:30', total: 20, remaining: 15, fee: 55 },
  { id: 9, doctorId: 6, doctorName: '陈医生', department: '妇产科', date: '2024-05-20', time: '上午', period: '08:00-12:00', total: 25, remaining: 10, fee: 50 },
  { id: 10, doctorId: 7, doctorName: '杨医生', department: '儿科', date: '2024-05-20', time: '上午', period: '08:00-12:00', total: 35, remaining: 5, fee: 40 },
  { id: 11, doctorId: 7, doctorName: '杨医生', department: '儿科', date: '2024-05-21', time: '下午', period: '14:00-17:30', total: 30, remaining: 28, fee: 40 },
  { id: 12, doctorId: 8, doctorName: '黄医生', department: '眼科', date: '2024-05-20', time: '上午', period: '08:00-12:00', total: 20, remaining: 16, fee: 45 },
  { id: 13, doctorId: 1, doctorName: '张医生', department: '内科', date: '2024-05-21', time: '上午', period: '08:00-12:00', total: 30, remaining: 0, fee: 50 }
];

export const registrations = [
  { id: 1, patientName: '张三', idCard: '110101199001011234', phone: '13800138001', department: '内科', doctor: '张医生', date: '2024-05-20', time: '上午', number: '001', status: 0, createTime: '2024-05-19 10:30:00' },
  { id: 2, patientName: '李四', idCard: '110101199102022345', phone: '13800138002', department: '外科', doctor: '赵医生', date: '2024-05-20', time: '上午', number: '005', status: 1, createTime: '2024-05-19 11:20:00' },
  { id: 3, patientName: '王五', idCard: '110101199203033456', phone: '13800138003', department: '儿科', doctor: '杨医生', date: '2024-05-20', time: '上午', number: '003', status: 0, createTime: '2024-05-19 14:15:00' },
  { id: 4, patientName: '赵六', idCard: '110101199304044567', phone: '13800138004', department: '妇产科', doctor: '陈医生', date: '2024-05-20', time: '上午', number: '002', status: 2, createTime: '2024-05-19 09:45:00' },
  { id: 5, patientName: '孙七', idCard: '110101199405055678', phone: '13800138005', department: '内科', doctor: '李医生', date: '2024-05-21', time: '上午', number: '008', status: 0, createTime: '2024-05-19 16:30:00' },
  { id: 6, patientName: '周八', idCard: '110101199506066789', phone: '13800138006', department: '眼科', doctor: '黄医生', date: '2024-05-20', time: '上午', number: '004', status: 1, createTime: '2024-05-19 08:20:00' },
  { id: 7, patientName: '测试患者', idCard: '110101199001019999', phone: '13900139001', department: '内科', doctor: '张医生', date: '2024-05-20', time: '下午', number: '010', status: 0, createTime: '2024-05-20 08:00:00' }
];

export const statusMap = {
  0: { label: '待就诊', type: 'warning' },
  1: { label: '已签到', type: 'success' },
  2: { label: '已完成', type: 'info' },
  3: { label: '已取消', type: 'danger' }
};
