import { registrations, schedules } from '@/mock/data';

// 简单的数据共享存储
export const store = {
  registrations: [...registrations],
  schedules: [...schedules],
  
  // 添加挂号记录
  addRegistration(record) {
    this.registrations.push(record);
  },
  
  // 更新号源
  updateScheduleRemaining(doctorName, date, time, delta) {
    const schedule = this.schedules.find(s => 
      s.doctorName === doctorName && s.date === date && s.time === time
    );
    if (schedule) {
      schedule.remaining += delta;
    }
  },
  
  // 获取最新挂号记录
  getRegistrations() {
    return this.registrations;
  },
  
  // 获取最新排班
  getSchedules() {
    return this.schedules;
  },
  
  // 订阅者列表
  subscribers: [],
  
  // 订阅数据变化
  subscribe(callback) {
    this.subscribers.push(callback);
    return () => {
      const index = this.subscribers.indexOf(callback);
      if (index > -1) {
        this.subscribers.splice(index, 1);
      }
    };
  },
  
  // 通知所有订阅者
  notify() {
    this.subscribers.forEach(callback => callback());
  }
};
