from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Device(db.Model):
    __tablename__ = 'devices'
    
    id = db.Column(db.Integer, primary_key=True)
    device_code = db.Column(db.String(50), unique=True, nullable=False)
    device_name = db.Column(db.String(100), nullable=False)
    hospital = db.Column(db.String(100), nullable=False)
    floor = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    install_date = db.Column(db.Date, nullable=False)
    online_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='正常')
    last_maintenance = db.Column(db.DateTime)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'device_code': self.device_code,
            'device_name': self.device_name,
            'hospital': self.hospital,
            'floor': self.floor,
            'location': self.location,
            'install_date': self.install_date.strftime('%Y-%m-%d') if self.install_date else None,
            'online_date': self.online_date.strftime('%Y-%m-%d') if self.online_date else None,
            'status': self.status,
            'last_maintenance': self.last_maintenance.strftime('%Y-%m-%d %H:%M:%S') if self.last_maintenance else None,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
        }

class FaultOrder(db.Model):
    __tablename__ = 'fault_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(30), unique=True, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    fault_type = db.Column(db.String(50), nullable=False)
    fault_description = db.Column(db.Text, nullable=False)
    reporter = db.Column(db.String(50), nullable=False)
    report_time = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(20), nullable=False, default='待处理')
    handle_time = db.Column(db.DateTime)
    handler = db.Column(db.String(50))
    handle_result = db.Column(db.Text)
    is_repeat_fault = db.Column(db.Boolean, default=False)
    repeat_count = db.Column(db.Integer, default=0)
    
    device = db.relationship('Device', backref=db.backref('fault_orders', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_no': self.order_no,
            'device_id': self.device_id,
            'device_code': self.device.device_code if self.device else None,
            'device_name': self.device.device_name if self.device else None,
            'fault_type': self.fault_type,
            'fault_description': self.fault_description,
            'reporter': self.reporter,
            'report_time': self.report_time.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self.status,
            'handle_time': self.handle_time.strftime('%Y-%m-%d %H:%M:%S') if self.handle_time else None,
            'handler': self.handler,
            'handle_result': self.handle_result,
            'is_repeat_fault': self.is_repeat_fault,
            'repeat_count': self.repeat_count
        }

class MaintenanceRecord(db.Model):
    __tablename__ = 'maintenance_records'
    
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    order_no = db.Column(db.String(30))
    maintenance_type = db.Column(db.String(20), nullable=False)
    maintenance_content = db.Column(db.Text, nullable=False)
    maintenance_time = db.Column(db.DateTime, default=datetime.now)
    maintenance_person = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Float, default=0.0)
    remarks = db.Column(db.Text)
    
    device = db.relationship('Device', backref=db.backref('maintenance_records', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'device_code': self.device.device_code if self.device else None,
            'device_name': self.device.device_name if self.device else None,
            'order_no': self.order_no,
            'maintenance_type': self.maintenance_type,
            'maintenance_content': self.maintenance_content,
            'maintenance_time': self.maintenance_time.strftime('%Y-%m-%d %H:%M:%S'),
            'maintenance_person': self.maintenance_person,
            'cost': self.cost,
            'remarks': self.remarks
        }
