from app import db
from datetime import datetime

class MaintenanceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    fault_id = db.Column(db.Integer, db.ForeignKey('fault.id'))
    maintenance_type = db.Column(db.String(50), nullable=False)
    maintenance_date = db.Column(db.DateTime, default=datetime.now)
    operator = db.Column(db.String(50), nullable=False)
    maintenance_content = db.Column(db.Text)
    parts_replaced = db.Column(db.Text)
    cost = db.Column(db.Float)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)

    device = db.relationship('Device', backref=db.backref('maintenance_records', lazy=True))
    fault = db.relationship('Fault', backref=db.backref('maintenance_record', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'device_code': self.device.device_code if self.device else None,
            'device_name': self.device.device_name if self.device else None,
            'fault_id': self.fault_id,
            'work_order_no': self.fault.work_order_no if self.fault else None,
            'maintenance_type': self.maintenance_type,
            'maintenance_date': self.maintenance_date.strftime('%Y-%m-%d %H:%M:%S'),
            'operator': self.operator,
            'maintenance_content': self.maintenance_content,
            'parts_replaced': self.parts_replaced,
            'cost': self.cost,
            'notes': self.notes,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }