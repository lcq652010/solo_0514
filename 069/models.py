from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum

db = SQLAlchemy()

DEVICE_STATUS = ('normal', 'fault', 'offline', 'signal_error')
WORK_ORDER_STATUS = ('pending', 'processing', 'completed', 'closed')
EXCEPTION_TYPES = ('miss_read', 'wrong_read', 'comm_interrupt', 'power_failure')


class Device(db.Model):
    __tablename__ = 'devices'
    
    id = db.Column(db.Integer, primary_key=True)
    device_code = db.Column(db.String(50), unique=True, nullable=False)
    device_name = db.Column(db.String(100), nullable=False)
    wharf_code = db.Column(db.String(50))
    crane_location = db.Column(db.String(100))
    sn_code = db.Column(db.String(100))
    work_zone = db.Column(db.String(100))
    location = db.Column(db.String(200))
    install_date = db.Column(db.Date)
    status = db.Column(db.Enum(*DEVICE_STATUS, name='device_status'), default='normal')
    last_heartbeat = db.Column(db.DateTime)
    signal_strength = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    remarks = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'device_code': self.device_code,
            'device_name': self.device_name,
            'wharf_code': self.wharf_code,
            'crane_location': self.crane_location,
            'sn_code': self.sn_code,
            'work_zone': self.work_zone,
            'location': self.location,
            'install_date': self.install_date.strftime('%Y-%m-%d') if self.install_date else None,
            'status': self.status,
            'status_text': self.get_status_text(),
            'last_heartbeat': self.last_heartbeat.strftime('%Y-%m-%d %H:%M:%S') if self.last_heartbeat else None,
            'signal_strength': self.signal_strength,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'remarks': self.remarks
        }
    
    def get_status_text(self):
        status_map = {
            'normal': '正常',
            'fault': '故障',
            'offline': '离线',
            'signal_error': '信号异常'
        }
        return status_map.get(self.status, '未知')


class ExceptionReport(db.Model):
    __tablename__ = 'exception_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    exception_type = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.now)
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    description = db.Column(db.Text)
    container_code = db.Column(db.String(50))
    rfid_data = db.Column(db.Text)
    handled = db.Column(db.Boolean, default=False)
    handled_at = db.Column(db.DateTime)
    handler = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    device = db.relationship('Device', backref=db.backref('exceptions', lazy=True))
    
    def calculate_duration(self):
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            self.duration = int(delta.total_seconds())
        return self.duration
    
    def to_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'device_code': self.device.device_code if self.device else None,
            'device_name': self.device.device_name if self.device else None,
            'exception_type': self.exception_type,
            'exception_type_text': self.get_exception_type_text(),
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S') if self.start_time else None,
            'end_time': self.end_time.strftime('%Y-%m-%d %H:%M:%S') if self.end_time else None,
            'duration': self.duration,
            'duration_text': self.format_duration(),
            'description': self.description,
            'container_code': self.container_code,
            'rfid_data': self.rfid_data,
            'handled': self.handled,
            'handled_at': self.handled_at.strftime('%Y-%m-%d %H:%M:%S') if self.handled_at else None,
            'handler': self.handler,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def format_duration(self):
        if self.duration is None:
            return None
        hours = self.duration // 3600
        minutes = (self.duration % 3600) // 60
        seconds = self.duration % 60
        if hours > 0:
            return f'{hours}小时{minutes}分{seconds}秒'
        elif minutes > 0:
            return f'{minutes}分{seconds}秒'
        else:
            return f'{seconds}秒'
    
    def get_exception_type_text(self):
        type_map = {
            'miss_read': '漏读',
            'wrong_read': '误读',
            'comm_interrupt': '通信中断',
            'power_failure': '供电异常'
        }
        return type_map.get(self.exception_type, self.exception_type)


class WorkOrder(db.Model):
    __tablename__ = 'work_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(20), unique=True, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    exception_id = db.Column(db.Integer, db.ForeignKey('exception_reports.id'))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.Enum('low', 'medium', 'high', 'urgent', name='priority_level'), default='medium')
    status = db.Column(db.Enum(*WORK_ORDER_STATUS, name='work_order_status'), default='pending')
    assign_to = db.Column(db.String(50))
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    created_by = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    device = db.relationship('Device', backref=db.backref('work_orders', lazy=True))
    exception = db.relationship('ExceptionReport', backref=db.backref('work_order', uselist=False))
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_no': self.order_no,
            'device_id': self.device_id,
            'device_code': self.device.device_code if self.device else None,
            'device_name': self.device.device_name if self.device else None,
            'exception_id': self.exception_id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'priority_text': self.get_priority_text(),
            'status': self.status,
            'status_text': self.get_status_text(),
            'assign_to': self.assign_to,
            'started_at': self.started_at.strftime('%Y-%m-%d %H:%M:%S') if self.started_at else None,
            'completed_at': self.completed_at.strftime('%Y-%m-%d %H:%M:%S') if self.completed_at else None,
            'created_by': self.created_by,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def get_priority_text(self):
        priority_map = {
            'low': '低',
            'medium': '中',
            'high': '高',
            'urgent': '紧急'
        }
        return priority_map.get(self.priority, '未知')
    
    def get_status_text(self):
        status_map = {
            'pending': '待处理',
            'processing': '处理中',
            'completed': '已完成',
            'closed': '已关闭'
        }
        return status_map.get(self.status, '未知')


class RecognitionRecord(db.Model):
    __tablename__ = 'recognition_records'
    
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    container_code = db.Column(db.String(50))
    success = db.Column(db.Boolean, default=True)
    fail_reason = db.Column(db.String(100))
    recognition_time = db.Column(db.DateTime, default=datetime.now)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    device = db.relationship('Device', backref=db.backref('recognition_records', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'device_code': self.device.device_code if self.device else None,
            'device_name': self.device.device_name if self.device else None,
            'container_code': self.container_code,
            'success': self.success,
            'fail_reason': self.fail_reason,
            'recognition_time': self.recognition_time.strftime('%Y-%m-%d %H:%M:%S'),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class DailyStats(db.Model):
    __tablename__ = 'daily_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    stats_date = db.Column(db.Date, nullable=False)
    total_recognitions = db.Column(db.Integer, default=0)
    success_recognitions = db.Column(db.Integer, default=0)
    fail_recognitions = db.Column(db.Integer, default=0)
    success_rate = db.Column(db.Float, default=100.0)
    exception_count = db.Column(db.Integer, default=0)
    total_exception_duration = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    device = db.relationship('Device', backref=db.backref('daily_stats', lazy=True))
    
    __table_args__ = (db.UniqueConstraint('device_id', 'stats_date', name='_device_date_uc'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'device_code': self.device.device_code if self.device else None,
            'device_name': self.device.device_name if self.device else None,
            'wharf_code': self.device.wharf_code if self.device else None,
            'work_zone': self.device.work_zone if self.device else None,
            'stats_date': self.stats_date.strftime('%Y-%m-%d'),
            'total_recognitions': self.total_recognitions,
            'success_recognitions': self.success_recognitions,
            'fail_recognitions': self.fail_recognitions,
            'success_rate': round(self.success_rate, 2),
            'exception_count': self.exception_count,
            'total_exception_duration': self.total_exception_duration,
            'efficiency_score': self.calculate_efficiency_score()
        }
    
    def calculate_efficiency_score(self):
        rate_score = self.success_rate * 0.6
        availability_score = 100
        if self.total_exception_duration > 0:
            max_daily_seconds = 24 * 3600
            availability_score = max(0, 100 - (self.total_exception_duration / max_daily_seconds * 100))
            availability_score = availability_score * 0.4
        return round(rate_score + availability_score, 2)


class MonthlyStats(db.Model):
    __tablename__ = 'monthly_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    stats_year = db.Column(db.Integer, nullable=False)
    stats_month = db.Column(db.Integer, nullable=False)
    total_recognitions = db.Column(db.Integer, default=0)
    success_recognitions = db.Column(db.Integer, default=0)
    fail_recognitions = db.Column(db.Integer, default=0)
    success_rate = db.Column(db.Float, default=100.0)
    exception_count = db.Column(db.Integer, default=0)
    total_exception_duration = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    device = db.relationship('Device', backref=db.backref('monthly_stats', lazy=True))
    
    __table_args__ = (db.UniqueConstraint('device_id', 'stats_year', 'stats_month', name='_device_month_uc'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'device_code': self.device.device_code if self.device else None,
            'device_name': self.device.device_name if self.device else None,
            'wharf_code': self.device.wharf_code if self.device else None,
            'work_zone': self.device.work_zone if self.device else None,
            'stats_year': self.stats_year,
            'stats_month': self.stats_month,
            'stats_period': f'{self.stats_year}年{self.stats_month}月',
            'total_recognitions': self.total_recognitions,
            'success_recognitions': self.success_recognitions,
            'fail_recognitions': self.fail_recognitions,
            'success_rate': round(self.success_rate, 2),
            'exception_count': self.exception_count,
            'total_exception_duration': self.total_exception_duration
        }
