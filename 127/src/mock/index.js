import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';

const mock = new MockAdapter(axios, { delayResponse: 500 });

const overtimeTypes = [
  { value: 'weekday', label: '工作日加班' },
  { value: 'weekend', label: '周末加班' },
  { value: 'holiday', label: '节假日加班' }
];

const statusMap = {
  pending: { label: '待审批', color: 'warning' },
  approved: { label: '已通过', color: 'success' },
  rejected: { label: '已驳回', color: 'danger' }
};

let records = [
  {
    id: 1,
    applicant: '张三',
    department: '技术部',
    type: 'weekday',
    startTime: '2024-05-15 18:00',
    endTime: '2024-05-15 21:00',
    duration: 3,
    reason: '项目上线调试',
    status: 'pending',
    createTime: '2024-05-15 09:00'
  },
  {
    id: 2,
    applicant: '张三',
    department: '技术部',
    type: 'weekend',
    startTime: '2024-05-18 09:00',
    endTime: '2024-05-18 18:00',
    duration: 8,
    reason: '需求开发',
    status: 'approved',
    createTime: '2024-05-17 15:00'
  },
  {
    id: 3,
    applicant: '李四',
    department: '技术部',
    type: 'weekday',
    startTime: '2024-05-16 18:30',
    endTime: '2024-05-16 22:00',
    duration: 3.5,
    reason: 'Bug修复',
    status: 'pending',
    createTime: '2024-05-16 10:00'
  },
  {
    id: 4,
    applicant: '王五',
    department: '产品部',
    type: 'holiday',
    startTime: '2024-05-01 09:00',
    endTime: '2024-05-01 18:00',
    duration: 8,
    reason: '版本迭代',
    status: 'rejected',
    createTime: '2024-04-30 14:00'
  }
];

mock.onPost('/api/overtime/apply').reply(config => {
  const data = JSON.parse(config.data);
  const newRecord = {
    id: records.length + 1,
    applicant: '张三',
    department: '技术部',
    ...data,
    status: 'pending',
    createTime: new Date().toLocaleString()
  };
  records.unshift(newRecord);
  return [200, { code: 200, message: '申请提交成功', data: newRecord }];
});

mock.onGet('/api/overtime/my-records').reply(config => {
  const { page = 1, pageSize = 10, status, startDate, endDate } = config.params || {};
  let filtered = records.filter(r => r.applicant === '张三');
  if (status) {
    filtered = filtered.filter(r => r.status === status);
  }
  if (startDate && endDate) {
    filtered = filtered.filter(r => {
      const recordDate = r.startTime.split(' ')[0];
      return recordDate >= startDate && recordDate <= endDate;
    });
  }
  const start = (page - 1) * pageSize;
  const end = start + parseInt(pageSize);
  const list = filtered.slice(start, end);
  return [200, { code: 200, data: { list, total: filtered.length } }];
});

mock.onGet('/api/overtime/approval-list').reply(config => {
  const { page = 1, pageSize = 10, status, department, startDate, endDate } = config.params || {};
  let filtered = [...records];
  if (department) {
    filtered = filtered.filter(r => r.department === department);
  }
  if (status) {
    filtered = filtered.filter(r => r.status === status);
  }
  if (startDate && endDate) {
    filtered = filtered.filter(r => {
      const recordDate = r.startTime.split(' ')[0];
      return recordDate >= startDate && recordDate <= endDate;
    });
  }
  const start = (page - 1) * pageSize;
  const end = start + parseInt(pageSize);
  const list = filtered.slice(start, end);
  return [200, { code: 200, data: { list, total: filtered.length } }];
});

mock.onPost('/api/overtime/approve').reply(config => {
  const data = JSON.parse(config.data);
  const record = records.find(r => r.id === data.id);
  if (record) {
    record.status = data.status;
    record.approvalRemark = data.approvalRemark;
    return [200, { code: 200, message: '审批成功' }];
  }
  return [400, { code: 400, message: '记录不存在' }];
});

mock.onGet('/api/overtime/statistics').reply(() => {
  const data = {
    monthly: {
      months: ['1月', '2月', '3月', '4月', '5月'],
      hours: [12, 18, 25, 32, 28]
    },
    byType: [
      { name: '工作日加班', value: 45 },
      { name: '周末加班', value: 32 },
      { name: '节假日加班', value: 18 }
    ],
    total: 95,
    average: 19
  };
  return [200, { code: 200, data }];
});

mock.onGet('/api/overtime/ledger').reply(config => {
  const { year = '2024', month } = config.params || {};
  const ledgerData = [];
  const daysInMonth = month ? new Date(year, month, 0).getDate() : 30;
  for (let i = 1; i <= daysInMonth; i++) {
    const date = `${year}-${String(month || 5).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
    if (Math.random() > 0.7) {
      const type = ['weekday', 'weekend', 'holiday'][Math.floor(Math.random() * 3)];
      const duration = Math.floor(Math.random() * 8) + 1;
      ledgerData.push({
        date,
        type,
        duration,
        status: ['pending', 'approved', 'rejected'][Math.floor(Math.random() * 3)],
        reason: '项目工作'
      });
    }
  }
  return [200, { code: 200, data: { list: ledgerData, total: ledgerData.length } }];
});

export default mock;
