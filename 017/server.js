const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const moment = require('moment');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(bodyParser.json());
app.use(express.static('public'));

let employees = [
  { id: 1, name: '张三', department: '技术部', position: '工程师' },
  { id: 2, name: '李四', department: '技术部', position: '工程师' },
  { id: 3, name: '王五', department: '市场部', position: '经理' },
  { id: 4, name: '赵六', department: '人事部', position: '专员' },
  { id: 5, name: '钱七', department: '财务部', position: '会计' }
];

let attendanceRecords = [
  { id: 1, employeeId: 1, employeeName: '张三', department: '技术部', date: '2026-05-15', checkIn: '09:00:00', checkOut: '18:00:00', status: '正常' },
  { id: 2, employeeId: 2, employeeName: '李四', department: '技术部', date: '2026-05-15', checkIn: '09:15:00', checkOut: '18:30:00', status: '迟到' },
  { id: 3, employeeId: 3, employeeName: '王五', department: '市场部', date: '2026-05-15', checkIn: '08:50:00', checkOut: '19:00:00', status: '正常' },
  { id: 4, employeeId: 1, employeeName: '张三', department: '技术部', date: '2026-05-14', checkIn: '09:05:00', checkOut: '18:10:00', status: '正常' },
  { id: 5, employeeId: 4, employeeName: '赵六', department: '人事部', date: '2026-05-15', checkIn: '09:30:00', checkOut: null, status: '早退' },
  { id: 6, employeeId: 5, employeeName: '钱七', department: '财务部', date: '2026-05-15', checkIn: '08:55:00', checkOut: '18:05:00', status: '正常' }
];

let nextAttendanceId = 7;

const woodTypes = [
  { id: 1, name: '红木', description: '高档家具用材，质地坚硬' },
  { id: 2, name: '花梨木', description: '纹理美观，香气宜人' },
  { id: 3, name: '橡木', description: '坚固耐用，纹理清晰' },
  { id: 4, name: '胡桃木', description: '色泽沉稳，质感细腻' },
  { id: 5, name: '樱桃木', description: '细腻光滑，色泽温暖' },
  { id: 6, name: '松木', description: '经济实用，纹理朴实' }
];

const grooveTypes = [
  { id: 1, name: '平槽', description: '平底直槽，用于平板拼接', depth: '6-12mm', width: '8-15mm' },
  { id: 2, name: '燕尾槽', description: '燕尾形，连接牢固，用于抽屉', angle: '15-20度', depth: '8-15mm' },
  { id: 3, name: 'U型槽', description: 'U形槽，用于装饰线条或滑轨', radius: '3-8mm', depth: '5-20mm' },
  { id: 4, name: 'V型槽', description: 'V形槽，用于拼板装饰', angle: '45-90度', depth: '3-10mm' },
  { id: 5, name: '圆弧形槽', description: '圆弧内胆槽，用于特殊造型', radius: '10-50mm' },
  { id: 6, name: '梯形槽', description: '梯形槽，用于高强度拼接', topWidth: '10-20mm', bottomWidth: '6-12mm' }
];

const carvingStyles = [
  { id: 1, name: '中式雕花', description: '传统纹样，如龙、凤、云纹', difficulty: '高', style: '浮雕、透雕' },
  { id: 2, name: '欧式雕花', description: '卷草纹、巴洛克风格', difficulty: '高', style: '浮雕、圆雕' },
  { id: 3, name: '简约线条', description: '现代简约风格，直线几何', difficulty: '低', style: '阴刻线' },
  { id: 4, name: '田园风格', description: '花卉、藤蔓自然纹样', difficulty: '中', style: '浅浮雕' },
  { id: 5, name: '中式回纹', description: '传统回字纹样，寓意吉祥', difficulty: '中', style: '阴刻、阳刻' },
  { id: 6, name: '素面无雕', description: '不雕花，保持原木质感', difficulty: '无', style: '抛光打磨' }
];

let orders = [
  {
    id: 1,
    orderNo: 'ORD202605001',
    customerName: '王先生',
    productName: '中式衣柜',
    woodType: '红木',
    dimensions: { length: 1800, width: 600, height: 2200, unit: 'mm' },
    grooveType: '燕尾槽',
    carvingStyle: '中式雕花',
    quantity: 2,
    orderDate: '2026-05-10',
    deliveryDate: '2026-06-20',
    status: '生产中',
    priority: '高',
    processRequirements: {
      grooving: '柜门采用燕尾槽拼接，背板U型槽',
      joining: '框架榫卯结构，面板平槽拼接',
      carving: '门板龙凤浮雕，顶线回纹装饰'
    },
    remarks: '客户要求使用传统榫卯工艺，雕花需手工雕刻'
  },
  {
    id: 2,
    orderNo: 'ORD202605002',
    customerName: '李女士',
    productName: '欧式餐桌',
    woodType: '橡木',
    dimensions: { length: 1600, width: 900, height: 750, unit: 'mm' },
    grooveType: '平槽',
    carvingStyle: '欧式雕花',
    quantity: 1,
    orderDate: '2026-05-12',
    deliveryDate: '2026-06-15',
    status: '待生产',
    priority: '中',
    processRequirements: {
      grooving: '桌面拼板采用平槽防变形',
      joining: '桌腿楔形榫，框架圆榫拼接',
      carving: '桌腿卷草纹浮雕，牙板装饰线'
    },
    remarks: '需要做防开裂处理'
  },
  {
    id: 3,
    orderNo: 'ORD202605003',
    customerName: '张总',
    productName: '现代简约书柜',
    woodType: '胡桃木',
    dimensions: { length: 2000, width: 350, height: 2000, unit: 'mm' },
    grooveType: 'U型槽',
    carvingStyle: '简约线条',
    quantity: 3,
    orderDate: '2026-05-08',
    deliveryDate: '2026-06-10',
    status: '已完成',
    priority: '低',
    processRequirements: {
      grooving: '层板U型槽安装，背板V型槽装饰',
      joining: '三合一连接件，隐形五金',
      carving: '门板阴刻直线装饰，极简风格'
    },
    remarks: '客户要求环保E0级板材'
  }
];

let nextOrderId = 4;

const departments = [
  { id: 1, name: '内科', description: '内科诊疗科室' },
  { id: 2, name: '外科', description: '外科手术科室' },
  { id: 3, name: '急诊科', description: '急诊急救科室' },
  { id: 4, name: '放射科', description: '影像检查科室' },
  { id: 5, name: '检验科', description: '医学检验科室' },
  { id: 6, name: '手术室', description: '手术操作科室' },
  { id: 7, name: 'ICU', description: '重症监护科室' },
  { id: 8, name: '妇产科', description: '妇产专科科室' }
];

const faultLevels = [
  { id: 1, name: '一级故障', description: '设备完全无法使用，影响重大', priority: '紧急', color: '#dc3545' },
  { id: 2, name: '二级故障', description: '设备部分功能失效，影响较大', priority: '高', color: '#fd7e14' },
  { id: 3, name: '三级故障', description: '设备功能轻微异常，不影响主要使用', priority: '中', color: '#ffc107' },
  { id: 4, name: '四级故障', description: '外观或辅助配件问题', priority: '低', color: '#28a745' }
];

const handleStatuses = [
  { id: 1, name: '待处理', description: '故障已上报，尚未开始处理', color: '#6c757d' },
  { id: 2, name: '处理中', description: '维修人员正在处理', color: '#007bff' },
  { id: 3, name: '待验收', description: '维修完成，等待使用部门验收', color: '#ffc107' },
  { id: 4, name: '已完成', description: '验收通过，故障处理完毕', color: '#28a745' },
  { id: 5, name: '已取消', description: '工单已取消', color: '#dc3545' }
];

const deviceTypes = [
  { id: 1, name: '监护仪', description: '生命体征监测设备' },
  { id: 2, name: '呼吸机', description: '呼吸支持设备' },
  { id: 3, name: '输液泵', description: '静脉输液设备' },
  { id: 4, name: '心电图机', description: '心电检查设备' },
  { id: 5, name: '超声仪', description: '超声诊断设备' },
  { id: 6, name: 'X光机', description: '放射影像设备' },
  { id: 7, name: '麻醉机', description: '手术麻醉设备' },
  { id: 8, name: '除颤仪', description: '心脏急救设备' }
];

let devices = [
  { id: 1, deviceCode: 'DEV-001', name: 'ICU监护仪01', type: '监护仪', department: 'ICU', status: '运行中', isPowerOn: true, lastMaintainDate: '2026-04-15', installDate: '2025-01-20', manufacturer: '迈瑞医疗' },
  { id: 2, deviceCode: 'DEV-002', name: 'ICU监护仪02', type: '监护仪', department: 'ICU', status: '运行中', isPowerOn: true, lastMaintainDate: '2026-04-20', installDate: '2025-01-20', manufacturer: '迈瑞医疗' },
  { id: 3, deviceCode: 'DEV-003', name: '外科呼吸机01', type: '呼吸机', department: '外科', status: '运行中', isPowerOn: true, lastMaintainDate: '2026-03-10', installDate: '2025-03-15', manufacturer: '飞利浦医疗' },
  { id: 4, deviceCode: 'DEV-004', name: '急诊科呼吸机01', type: '呼吸机', department: '急诊科', status: '故障', isPowerOn: false, lastMaintainDate: '2026-02-28', installDate: '2024-11-01', manufacturer: '飞利浦医疗' },
  { id: 5, deviceCode: 'DEV-005', name: '放射科X光机01', type: 'X光机', department: '放射科', status: '维护中', isPowerOn: false, lastMaintainDate: '2026-05-10', installDate: '2024-06-20', manufacturer: 'GE医疗' },
  { id: 6, deviceCode: 'DEV-006', name: '手术室麻醉机01', type: '麻醉机', department: '手术室', status: '运行中', isPowerOn: true, lastMaintainDate: '2026-04-01', installDate: '2025-02-10', manufacturer: '德尔格医疗' },
  { id: 7, deviceCode: 'DEV-007', name: '内科心电图机01', type: '心电图机', department: '内科', status: '运行中', isPowerOn: true, lastMaintainDate: '2026-03-25', installDate: '2025-05-12', manufacturer: '理邦仪器' },
  { id: 8, deviceCode: 'DEV-008', name: '急诊科除颤仪01', type: '除颤仪', department: '急诊科', status: '故障', isPowerOn: false, lastMaintainDate: '2026-01-15', installDate: '2024-08-30', manufacturer: '卓尔医疗' },
  { id: 9, deviceCode: 'DEV-009', name: 'ICU呼吸机01', type: '呼吸机', department: 'ICU', status: '运行中', isPowerOn: true, lastMaintainDate: '2026-04-30', installDate: '2025-04-18', manufacturer: '迈瑞医疗' },
  { id: 10, deviceCode: 'DEV-010', name: '妇产科超声仪01', type: '超声仪', department: '妇产科', status: '运行中', isPowerOn: true, lastMaintainDate: '2026-05-05', installDate: '2025-06-22', manufacturer: 'GE医疗' },
  { id: 11, deviceCode: 'DEV-011', name: '内科输液泵01', type: '输液泵', department: '内科', status: '闲置', isPowerOn: false, lastMaintainDate: '2026-04-12', installDate: '2025-07-01', manufacturer: '史密斯医疗' },
  { id: 12, deviceCode: 'DEV-012', name: '外科输液泵01', type: '输液泵', department: '外科', status: '运行中', isPowerOn: true, lastMaintainDate: '2026-05-02', installDate: '2025-07-01', manufacturer: '史密斯医疗' }
];

let faultRecords = [
  { id: 1, faultCode: 'FLT-202605001', deviceId: 4, deviceName: '急诊科呼吸机01', department: '急诊科', faultLevel: '一级故障', faultDesc: '设备无法开机，显示屏无显示', reporter: '李护士', reportTime: '2026-05-15 08:30:00', handleStatus: '处理中', handler: '王工程师', handleDesc: '正在检查电源模块', estimatedFixTime: '2026-05-16' },
  { id: 2, faultCode: 'FLT-202605002', deviceId: 8, deviceName: '急诊科除颤仪01', department: '急诊科', faultLevel: '二级故障', faultDesc: '除颤能量输出不稳定，误差超过10%', reporter: '张医生', reportTime: '2026-05-14 14:20:00', handleStatus: '待验收', handler: '王工程师', handleDesc: '已更换高压电容，正在测试验证', estimatedFixTime: '2026-05-15' },
  { id: 3, faultCode: 'FLT-202605003', deviceId: 5, deviceName: '放射科X光机01', department: '放射科', faultLevel: '三级故障', faultDesc: '球管散热风扇异响，不影响正常使用', reporter: '陈技师', reportTime: '2026-05-10 09:15:00', handleStatus: '已完成', handler: '刘工程师', handleDesc: '已更换散热风扇，运行正常', estimatedFixTime: '2026-05-12' },
  { id: 4, faultCode: 'FLT-202605004', deviceId: 1, deviceName: 'ICU监护仪01', department: 'ICU', faultLevel: '四级故障', faultDesc: '外壳塑料卡扣断裂，设备固定不稳', reporter: '王护士', reportTime: '2026-05-12 16:45:00', handleStatus: '已完成', handler: '王工程师', handleDesc: '已更换新的外壳卡扣', estimatedFixTime: '2026-05-13' },
  { id: 5, faultCode: 'FLT-202605005', deviceId: 10, deviceName: '妇产科超声仪01', department: '妇产科', faultLevel: '二级故障', faultDesc: '超声探头图像出现噪点，图像质量下降', reporter: '赵医生', reportTime: '2026-05-15 10:00:00', handleStatus: '待处理', handler: null, handleDesc: null, estimatedFixTime: null }
];

let nextDeviceId = 13;
let nextFaultId = 6;

const validateDeviceData = (data) => {
  const errors = [];
  
  if (!data.name) {
    errors.push('设备名称不能为空');
  }
  
  if (!data.type) {
    errors.push('设备类型不能为空');
  }
  
  if (!data.department) {
    errors.push('所属科室不能为空');
  }
  
  return errors;
};

const validateFaultData = (data) => {
  const errors = [];
  
  if (!data.deviceId) {
    errors.push('设备ID不能为空');
  }
  
  if (!data.faultLevel) {
    errors.push('故障等级不能为空');
  }
  
  if (!data.faultDesc) {
    errors.push('故障描述不能为空');
  }
  
  if (!data.reporter) {
    errors.push('上报人不能为空');
  }
  
  return errors;
};

const calculateDeviceStatistics = () => {
  const totalDevices = devices.length;
  const poweredOnDevices = devices.filter(d => d.isPowerOn).length;
  const runningDevices = devices.filter(d => d.status === '运行中').length;
  const faultDevices = devices.filter(d => d.status === '故障').length;
  const maintainingDevices = devices.filter(d => d.status === '维护中').length;
  
  const powerOnRate = totalDevices > 0 ? ((poweredOnDevices / totalDevices) * 100).toFixed(2) : 0;
  const goodConditionRate = totalDevices > 0 ? (((runningDevices + maintainingDevices) / totalDevices) * 100).toFixed(2) : 0;
  
  const departmentStats = departments.map(dept => {
    const deptDevices = devices.filter(d => d.department === dept.name);
    const deptTotal = deptDevices.length;
    const deptPoweredOn = deptDevices.filter(d => d.isPowerOn).length;
    const deptRunning = deptDevices.filter(d => d.status === '运行中').length;
    
    return {
      department: dept.name,
      total: deptTotal,
      poweredOn: deptPoweredOn,
      running: deptRunning,
      powerOnRate: deptTotal > 0 ? ((deptPoweredOn / deptTotal) * 100).toFixed(2) : 0,
      goodConditionRate: deptTotal > 0 ? ((deptRunning / deptTotal) * 100).toFixed(2) : 0
    };
  });
  
  const faultStats = {
    total: faultRecords.length,
    pending: faultRecords.filter(f => f.handleStatus === '待处理').length,
    processing: faultRecords.filter(f => f.handleStatus === '处理中').length,
    verifying: faultRecords.filter(f => f.handleStatus === '待验收').length,
    completed: faultRecords.filter(f => f.handleStatus === '已完成').length,
    level1: faultRecords.filter(f => f.faultLevel === '一级故障').length,
    level2: faultRecords.filter(f => f.faultLevel === '二级故障').length,
    level3: faultRecords.filter(f => f.faultLevel === '三级故障').length,
    level4: faultRecords.filter(f => f.faultLevel === '四级故障').length
  };
  
  return {
    summary: {
      totalDevices,
      poweredOnDevices,
      runningDevices,
      faultDevices,
      maintainingDevices,
      powerOnRate,
      goodConditionRate
    },
    departmentStats,
    faultStats
  };
};

const validateOrderData = (data) => {
  const errors = [];
  
  if (!data.customerName) {
    errors.push('客户姓名不能为空');
  }
  
  if (!data.productName) {
    errors.push('产品名称不能为空');
  }
  
  if (!data.woodType) {
    errors.push('木料品种不能为空');
  }
  
  if (!data.dimensions || !data.dimensions.length || !data.dimensions.width || !data.dimensions.height) {
    errors.push('外形尺寸（长、宽、高）不能为空');
  }
  
  if (data.dimensions && (data.dimensions.length <= 0 || data.dimensions.width <= 0 || data.dimensions.height <= 0)) {
    errors.push('尺寸数值必须大于0');
  }
  
  if (!data.grooveType) {
    errors.push('内胆槽型不能为空');
  }
  
  if (!data.carvingStyle) {
    errors.push('雕花风格不能为空');
  }
  
  if (!data.quantity || data.quantity <= 0) {
    errors.push('数量必须大于0');
  }
  
  return errors;
};

const generateProcessInstructions = (order) => {
  const grooveInfo = grooveTypes.find(g => g.name === order.grooveType);
  const carvingInfo = carvingStyles.find(c => c.name === order.carvingStyle);
  const woodInfo = woodTypes.find(w => w.name === order.woodType);
  
  return {
    grooving: {
      grooveType: order.grooveType,
      specifications: grooveInfo || {},
      instructions: [
        `槽型选择: ${order.grooveType}`,
        grooveInfo ? `技术参数: ${grooveInfo.description}` : '',
        `适用部位: ${order.productName}各拼接部位`,
        `注意事项: 根据${order.woodType}硬度调整刀具转速`
      ].filter(Boolean)
    },
    joining: {
      woodType: order.woodType,
      woodProperties: woodInfo || {},
      dimensions: order.dimensions,
      instructions: [
        `木料选择: ${order.woodType}`,
        woodInfo ? `材料特性: ${woodInfo.description}` : '',
        `产品尺寸: 长${order.dimensions.length}×宽${order.dimensions.width}×高${order.dimensions.height}${order.dimensions.unit || 'mm'}`,
        '拼接方式: 根据结构选择榫卯或五金连接'
      ]
    },
    carving: {
      style: order.carvingStyle,
      styleInfo: carvingInfo || {},
      instructions: [
        `雕花风格: ${order.carvingStyle}`,
        carvingInfo ? `工艺类型: ${carvingInfo.style}` : '',
        carvingInfo ? `难度等级: ${carvingInfo.difficulty}` : '',
        `注意事项: 雕花前确认纹样图纸，客户确认后施工`
      ]
    }
  };
};

const validateAttendanceData = (data) => {
  const errors = [];
  
  if (!data.employeeId) {
    errors.push('员工ID不能为空');
  }
  
  if (!data.date) {
    errors.push('考勤日期不能为空');
  } else if (!moment(data.date, 'YYYY-MM-DD', true).isValid()) {
    errors.push('日期格式不正确，请使用YYYY-MM-DD格式');
  }
  
  if (data.checkIn && !moment(data.checkIn, 'HH:mm:ss', true).isValid()) {
    errors.push('上班时间格式不正确，请使用HH:mm:ss格式');
  }
  
  if (data.checkOut && !moment(data.checkOut, 'HH:mm:ss', true).isValid()) {
    errors.push('下班时间格式不正确，请使用HH:mm:ss格式');
  }
  
  return errors;
};

const calculateAttendanceStatus = (checkIn, checkOut) => {
  const workStartTime = moment('09:00:00', 'HH:mm:ss');
  const workEndTime = moment('18:00:00', 'HH:mm:ss');
  
  let status = '正常';
  
  if (checkIn) {
    const checkInTime = moment(checkIn, 'HH:mm:ss');
    if (checkInTime.isAfter(workStartTime)) {
      status = '迟到';
    }
  }
  
  if (checkOut) {
    const checkOutTime = moment(checkOut, 'HH:mm:ss');
    if (checkOutTime.isBefore(workEndTime)) {
      status = status === '迟到' ? '迟到早退' : '早退';
    }
  }
  
  if (!checkOut) {
    status = '未打卡';
  }
  
  return status;
};

app.get('/api/employees', (req, res) => {
  res.json(employees);
});

app.get('/api/attendance', (req, res) => {
  try {
    const { employeeName, department, status, page = 1, pageSize = 10 } = req.query;
    
    let filteredRecords = [...attendanceRecords];
    
    if (employeeName) {
      filteredRecords = filteredRecords.filter(record => 
        record.employeeName.includes(employeeName)
      );
    }
    
    if (department) {
      filteredRecords = filteredRecords.filter(record => 
        record.department === department
      );
    }
    
    if (status) {
      filteredRecords = filteredRecords.filter(record => 
        record.status === status
      );
    }
    
    filteredRecords.sort((a, b) => {
      if (a.date !== b.date) {
        return new Date(b.date) - new Date(a.date);
      }
      return a.employeeId - b.employeeId;
    });
    
    const total = filteredRecords.length;
    const totalPages = Math.ceil(total / pageSize);
    const startIndex = (page - 1) * pageSize;
    const paginatedRecords = filteredRecords.slice(startIndex, startIndex + parseInt(pageSize));
    
    res.json({
      success: true,
      data: paginatedRecords,
      pagination: {
        page: parseInt(page),
        pageSize: parseInt(pageSize),
        total,
        totalPages
      }
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});

app.post('/api/attendance/checkin', (req, res) => {
  try {
    const { employeeId, checkInTime } = req.body;
    
    const validationErrors = validateAttendanceData({
      employeeId,
      date: moment().format('YYYY-MM-DD'),
      checkIn: checkInTime
    });
    
    if (validationErrors.length > 0) {
      return res.status(400).json({ 
        success: false, 
        message: '数据校验失败', 
        errors: validationErrors 
      });
    }
    
    const employee = employees.find(e => e.id === parseInt(employeeId));
    if (!employee) {
      return res.status(404).json({ success: false, message: '员工不存在' });
    }
    
    const today = moment().format('YYYY-MM-DD');
    const existingRecord = attendanceRecords.find(r => 
      r.employeeId === parseInt(employeeId) && r.date === today
    );
    
    if (existingRecord && existingRecord.checkIn) {
      return res.status(400).json({ 
        success: false, 
        message: '今日已打卡，请勿重复打卡' 
      });
    }
    
    const status = calculateAttendanceStatus(checkInTime, null);
    
    if (existingRecord) {
      existingRecord.checkIn = checkInTime;
      existingRecord.status = calculateAttendanceStatus(checkInTime, existingRecord.checkOut);
      res.json({ success: true, data: existingRecord, message: '上班打卡成功' });
    } else {
      const newRecord = {
        id: nextAttendanceId++,
        employeeId: parseInt(employeeId),
        employeeName: employee.name,
        department: employee.department,
        date: today,
        checkIn: checkInTime,
        checkOut: null,
        status
      };
      attendanceRecords.push(newRecord);
      res.json({ success: true, data: newRecord, message: '上班打卡成功' });
    }
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});

app.post('/api/attendance/checkout', (req, res) => {
  try {
    const { employeeId, checkOutTime } = req.body;
    
    const validationErrors = validateAttendanceData({
      employeeId,
      date: moment().format('YYYY-MM-DD'),
      checkOut: checkOutTime
    });
    
    if (validationErrors.length > 0) {
      return res.status(400).json({ 
        success: false, 
        message: '数据校验失败', 
        errors: validationErrors 
      });
    }
    
    const employee = employees.find(e => e.id === parseInt(employeeId));
    if (!employee) {
      return res.status(404).json({ success: false, message: '员工不存在' });
    }
    
    const today = moment().format('YYYY-MM-DD');
    const existingRecord = attendanceRecords.find(r => 
      r.employeeId === parseInt(employeeId) && r.date === today
    );
    
    if (!existingRecord) {
      return res.status(400).json({ 
        success: false, 
        message: '请先进行上班打卡' 
      });
    }
    
    if (existingRecord.checkOut) {
      return res.status(400).json({ 
        success: false, 
        message: '今日已下班打卡，请勿重复打卡' 
      });
    }
    
    existingRecord.checkOut = checkOutTime;
    existingRecord.status = calculateAttendanceStatus(existingRecord.checkIn, checkOutTime);
    
    res.json({ success: true, data: existingRecord, message: '下班打卡成功' });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});

app.get('/api/attendance/statistics', (req, res) => {
  const today = moment().format('YYYY-MM-DD');
  const todayRecords = attendanceRecords.filter(r => r.date === today);
  
  const statistics = {
    total: todayRecords.length,
    normal: todayRecords.filter(r => r.status === '正常').length,
    late: todayRecords.filter(r => r.status.includes('迟到')).length,
    earlyLeave: todayRecords.filter(r => r.status.includes('早退')).length,
    notCheckedOut: todayRecords.filter(r => !r.checkOut).length
  };
  
  res.json({ success: true, data: statistics });
});

app.get('/api/departments', (req, res) => {
  const departments = [...new Set(employees.map(e => e.department))];
  res.json({ success: true, data: departments });
});

app.get('/api/wood-types', (req, res) => {
  res.json({ success: true, data: woodTypes });
});

app.get('/api/groove-types', (req, res) => {
  res.json({ success: true, data: grooveTypes });
});

app.get('/api/carving-styles', (req, res) => {
  res.json({ success: true, data: carvingStyles });
});

app.get('/api/orders', (req, res) => {
  try {
    const { orderNo, customerName, woodType, status, page = 1, pageSize = 10 } = req.query;
    
    let filteredOrders = [...orders];
    
    if (orderNo) {
      filteredOrders = filteredOrders.filter(order => 
        order.orderNo.includes(orderNo)
      );
    }
    
    if (customerName) {
      filteredOrders = filteredOrders.filter(order => 
        order.customerName.includes(customerName)
      );
    }
    
    if (woodType) {
      filteredOrders = filteredOrders.filter(order => 
        order.woodType === woodType
      );
    }
    
    if (status) {
      filteredOrders = filteredOrders.filter(order => 
        order.status === status
      );
    }
    
    filteredOrders.sort((a, b) => {
      if (a.orderDate !== b.orderDate) {
        return new Date(b.orderDate) - new Date(a.orderDate);
      }
      return b.id - a.id;
    });
    
    const total = filteredOrders.length;
    const totalPages = Math.ceil(total / pageSize);
    const startIndex = (page - 1) * pageSize;
    const paginatedOrders = filteredOrders.slice(startIndex, startIndex + parseInt(pageSize));
    
    res.json({
      success: true,
      data: paginatedOrders,
      pagination: {
        page: parseInt(page),
        pageSize: parseInt(pageSize),
        total,
        totalPages
      }
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});

app.get('/api/orders/:id', (req, res) => {
  try {
    const order = orders.find(o => o.id === parseInt(req.params.id));
    
    if (!order) {
      return res.status(404).json({ success: false, message: '订单不存在' });
    }
    
    const processInstructions = generateProcessInstructions(order);
    
    res.json({
      success: true,
      data: {
        ...order,
        processInstructions
      }
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});

app.post('/api/orders', (req, res) => {
  try {
    const validationErrors = validateOrderData(req.body);
    
    if (validationErrors.length > 0) {
      return res.status(400).json({
        success: false,
        message: '数据校验失败',
        errors: validationErrors
      });
    }
    
    const orderNo = `ORD${moment().format('YYYYMM')}${String(nextOrderId).padStart(3, '0')}`;
    
    const newOrder = {
      id: nextOrderId++,
      orderNo,
      customerName: req.body.customerName,
      productName: req.body.productName,
      woodType: req.body.woodType,
      dimensions: {
        length: parseInt(req.body.dimensions.length),
        width: parseInt(req.body.dimensions.width),
        height: parseInt(req.body.dimensions.height),
        unit: req.body.dimensions.unit || 'mm'
      },
      grooveType: req.body.grooveType,
      carvingStyle: req.body.carvingStyle,
      quantity: parseInt(req.body.quantity),
      orderDate: moment().format('YYYY-MM-DD'),
      deliveryDate: req.body.deliveryDate,
      status: req.body.status || '待生产',
      priority: req.body.priority || '中',
      processRequirements: req.body.processRequirements || {
        grooving: '',
        joining: '',
        carving: ''
      },
      remarks: req.body.remarks || ''
    };
    
    orders.push(newOrder);
    
    res.json({
      success: true,
      data: newOrder,
      message: '订单创建成功'
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});

app.put('/api/orders/:id', (req, res) => {
  try {
    const orderIndex = orders.findIndex(o => o.id === parseInt(req.params.id));
    
    if (orderIndex === -1) {
      return res.status(404).json({ success: false, message: '订单不存在' });
    }
    
    const validationErrors = validateOrderData(req.body);
    
    if (validationErrors.length > 0) {
      return res.status(400).json({
        success: false,
        message: '数据校验失败',
        errors: validationErrors
      });
    }
    
    const updatedOrder = {
      ...orders[orderIndex],
      customerName: req.body.customerName,
      productName: req.body.productName,
      woodType: req.body.woodType,
      dimensions: {
        length: parseInt(req.body.dimensions.length),
        width: parseInt(req.body.dimensions.width),
        height: parseInt(req.body.dimensions.height),
        unit: req.body.dimensions.unit || 'mm'
      },
      grooveType: req.body.grooveType,
      carvingStyle: req.body.carvingStyle,
      quantity: parseInt(req.body.quantity),
      deliveryDate: req.body.deliveryDate,
      status: req.body.status,
      priority: req.body.priority,
      processRequirements: req.body.processRequirements,
      remarks: req.body.remarks
    };
    
    orders[orderIndex] = updatedOrder;
    
    res.json({
      success: true,
      data: updatedOrder,
      message: '订单更新成功'
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});

app.delete('/api/orders/:id', (req, res) => {
  try {
    const orderIndex = orders.findIndex(o => o.id === parseInt(req.params.id));
    
    if (orderIndex === -1) {
      return res.status(404).json({ success: false, message: '订单不存在' });
    }
    
    orders.splice(orderIndex, 1);
    
    res.json({
      success: true,
      message: '订单删除成功'
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});

app.get('/api/orders/:id/process-instructions', (req, res) => {
  try {
    const order = orders.find(o => o.id === parseInt(req.params.id));
    
    if (!order) {
      return res.status(404).json({ success: false, message: '订单不存在' });
    }
    
    const processInstructions = generateProcessInstructions(order);
    
    res.json({
      success: true,
      data: processInstructions
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});

app.get('/api/orders/statistics/summary', (req, res) => {
  const statistics = {
    total: orders.length,
    pending: orders.filter(o => o.status === '待生产').length,
    producing: orders.filter(o => o.status === '生产中').length,
    completed: orders.filter(o => o.status === '已完成').length,
    woodTypeDistribution: woodTypes.map(w => ({
      name: w.name,
      count: orders.filter(o => o.woodType === w.name).length
    }))
  };
  
  res.json({ success: true, data: statistics });
});

app.get('/api/departments/list', (req, res) => {
  res.json({ success: true, data: departments, message: '获取科室列表成功' });
});

app.get('/api/fault-levels', (req, res) => {
  res.json({ success: true, data: faultLevels, message: '获取故障等级列表成功' });
});

app.get('/api/handle-statuses', (req, res) => {
  res.json({ success: true, data: handleStatuses, message: '获取处理状态列表成功' });
});

app.get('/api/device-types', (req, res) => {
  res.json({ success: true, data: deviceTypes, message: '获取设备类型列表成功' });
});

app.get('/api/devices', (req, res) => {
  try {
    const { department, type, status, page = 1, pageSize = 10 } = req.query;
    
    let filteredDevices = [...devices];
    
    if (department) {
      filteredDevices = filteredDevices.filter(d => d.department === department);
    }
    
    if (type) {
      filteredDevices = filteredDevices.filter(d => d.type === type);
    }
    
    if (status) {
      filteredDevices = filteredDevices.filter(d => d.status === status);
    }
    
    filteredDevices.sort((a, b) => b.id - a.id);
    
    const total = filteredDevices.length;
    const totalPages = Math.ceil(total / pageSize);
    const startIndex = (page - 1) * pageSize;
    const paginatedDevices = filteredDevices.slice(startIndex, startIndex + parseInt(pageSize));
    
    res.json({
      success: true,
      data: paginatedDevices,
      pagination: {
        page: parseInt(page),
        pageSize: parseInt(pageSize),
        total,
        totalPages
      },
      message: '获取设备列表成功'
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});

app.get('/api/devices/:id', (req, res) => {
  try {
    const device = devices.find(d => d.id === parseInt(req.params.id));
    
    if (!device) {
      return res.status(404).json({ success: false, message: '设备不存在' });
    }
    
    const deviceFaults = faultRecords.filter(f => f.deviceId === device.id);
    
    res.json({
      success: true,
      data: {
        ...device,
        faultHistory: deviceFaults
      },
      message: '获取设备详情成功'
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});

app.post('/api/devices', (req, res) => {
  try {
    const validationErrors = validateDeviceData(req.body);
    
    if (validationErrors.length > 0) {
      return res.status(400).json({
        success: false,
        message: '数据校验失败',
        errors: validationErrors
      });
    }
    
    const deviceCode = `DEV-${String(nextDeviceId).padStart(3, '0')}`;
    
    const newDevice = {
      id: nextDeviceId++,
      deviceCode,
      name: req.body.name,
      type: req.body.type,
      department: req.body.department,
      status: req.body.status || '运行中',
      isPowerOn: req.body.isPowerOn !== undefined ? req.body.isPowerOn : true,
      lastMaintainDate: req.body.lastMaintainDate || moment().format('YYYY-MM-DD'),
      installDate: req.body.installDate || moment().format('YYYY-MM-DD'),
      manufacturer: req.body.manufacturer || ''
    };
    
    devices.push(newDevice);
    
    res.json({
      success: true,
      data: newDevice,
      message: '设备创建成功'
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});

app.put('/api/devices/:id', (req, res) => {
  try {
    const deviceIndex = devices.findIndex(d => d.id === parseInt(req.params.id));
    
    if (deviceIndex === -1) {
      return res.status(404).json({ success: false, message: '设备不存在' });
    }
    
    const validationErrors = validateDeviceData(req.body);
    
    if (validationErrors.length > 0) {
      return res.status(400).json({
        success: false,
        message: '数据校验失败',
        errors: validationErrors
      });
    }
    
    const updatedDevice = {
      ...devices[deviceIndex],
      name: req.body.name,
      type: req.body.type,
      department: req.body.department,
      status: req.body.status,
      isPowerOn: req.body.isPowerOn,
      lastMaintainDate: req.body.lastMaintainDate,
      manufacturer: req.body.manufacturer
    };
    
    devices[deviceIndex] = updatedDevice;
    
    res.json({
      success: true,
      data: updatedDevice,
      message: '设备更新成功'
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});

app.delete('/api/devices/:id', (req, res) => {
  try {
    const deviceIndex = devices.findIndex(d => d.id === parseInt(req.params.id));
    
    if (deviceIndex === -1) {
      return res.status(404).json({ success: false, message: '设备不存在' });
    }
    
    devices.splice(deviceIndex, 1);
    
    res.json({
      success: true,
      message: '设备删除成功'
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});

app.get('/api/fault-records', (req, res) => {
  try {
    const { department, faultLevel, handleStatus, page = 1, pageSize = 10 } = req.query;
    
    let filteredFaults = [...faultRecords];
    
    if (department) {
      filteredFaults = filteredFaults.filter(f => f.department === department);
    }
    
    if (faultLevel) {
      filteredFaults = filteredFaults.filter(f => f.faultLevel === faultLevel);
    }
    
    if (handleStatus) {
      filteredFaults = filteredFaults.filter(f => f.handleStatus === handleStatus);
    }
    
    filteredFaults.sort((a, b) => new Date(b.reportTime) - new Date(a.reportTime));
    
    const total = filteredFaults.length;
    const totalPages = Math.ceil(total / pageSize);
    const startIndex = (page - 1) * pageSize;
    const paginatedFaults = filteredFaults.slice(startIndex, startIndex + parseInt(pageSize));
    
    res.json({
      success: true,
      data: paginatedFaults,
      pagination: {
        page: parseInt(page),
        pageSize: parseInt(pageSize),
        total,
        totalPages
      },
      message: '获取故障记录列表成功'
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});

app.get('/api/fault-records/:id', (req, res) => {
  try {
    const fault = faultRecords.find(f => f.id === parseInt(req.params.id));
    
    if (!fault) {
      return res.status(404).json({ success: false, message: '故障记录不存在' });
    }
    
    const device = devices.find(d => d.id === fault.deviceId);
    
    res.json({
      success: true,
      data: {
        ...fault,
        deviceInfo: device
      },
      message: '获取故障详情成功'
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});

app.post('/api/fault-records', (req, res) => {
  try {
    const validationErrors = validateFaultData(req.body);
    
    if (validationErrors.length > 0) {
      return res.status(400).json({
        success: false,
        message: '数据校验失败',
        errors: validationErrors
      });
    }
    
    const device = devices.find(d => d.id === parseInt(req.body.deviceId));
    if (!device) {
      return res.status(404).json({ success: false, message: '关联设备不存在' });
    }
    
    const faultCode = `FLT-${moment().format('YYYYMM')}${String(nextFaultId).padStart(3, '0')}`;
    
    const newFault = {
      id: nextFaultId++,
      faultCode,
      deviceId: parseInt(req.body.deviceId),
      deviceName: device.name,
      department: device.department,
      faultLevel: req.body.faultLevel,
      faultDesc: req.body.faultDesc,
      reporter: req.body.reporter,
      reportTime: moment().format('YYYY-MM-DD HH:mm:ss'),
      handleStatus: '待处理',
      handler: null,
      handleDesc: null,
      estimatedFixTime: null
    };
    
    faultRecords.push(newFault);
    
    device.status = '故障';
    device.isPowerOn = false;
    
    res.json({
      success: true,
      data: newFault,
      message: '故障上报成功'
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});

app.put('/api/fault-records/:id', (req, res) => {
  try {
    const faultIndex = faultRecords.findIndex(f => f.id === parseInt(req.params.id));
    
    if (faultIndex === -1) {
      return res.status(404).json({ success: false, message: '故障记录不存在' });
    }
    
    const updatedFault = {
      ...faultRecords[faultIndex],
      faultLevel: req.body.faultLevel || faultRecords[faultIndex].faultLevel,
      faultDesc: req.body.faultDesc || faultRecords[faultIndex].faultDesc,
      handleStatus: req.body.handleStatus || faultRecords[faultIndex].handleStatus,
      handler: req.body.handler || faultRecords[faultIndex].handler,
      handleDesc: req.body.handleDesc || faultRecords[faultIndex].handleDesc,
      estimatedFixTime: req.body.estimatedFixTime || faultRecords[faultIndex].estimatedFixTime
    };
    
    faultRecords[faultIndex] = updatedFault;
    
    if (req.body.handleStatus === '已完成') {
      const device = devices.find(d => d.id === updatedFault.deviceId);
      if (device) {
        device.status = '运行中';
        device.isPowerOn = true;
      }
    }
    
    res.json({
      success: true,
      data: updatedFault,
      message: '故障记录更新成功'
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});

app.get('/api/devices/statistics/summary', (req, res) => {
  try {
    const statistics = calculateDeviceStatistics();
    
    res.json({
      success: true,
      data: statistics,
      message: '获取设备统计信息成功'
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`生产订单管理系统运行在 http://localhost:${PORT}`);
});
