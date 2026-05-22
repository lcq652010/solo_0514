from app import db
from datetime import datetime

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_code = db.Column(db.String(50), unique=True, nullable=False)
    device_name = db.Column(db.String(100), nullable=False)
    install_location = db.Column(db.String(200))
    install_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='normal')
    last_maintenance_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'device_code': self.device_code,
            'device_name': self.device_name,
            'install_location': self.install_location,
            'install_date': self.install_date.strftime('%Y-%m-%d') if self.install_date else None,
            'status': self.status,
            'status_text': self.get_status_text(),
            'last_maintenance_date': self.last_maintenance_date.strftime('%Y-%m-%d') if self.last_maintenance_date else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def get_status_text(self):
        status_map = {
            'normal': '正常',
            'fault': '故障',
            'repairing': '维修中',
            'fixed': '已修复'
        }
        return status_map.get(self.status, '未知')