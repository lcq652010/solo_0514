from app import db
from datetime import datetime
import uuid

class Fault(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_order_no = db.Column(db.String(50), unique=True, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    fault_type = db.Column(db.String(50), nullable=False)
    fault_desc = db.Column(db.Text)
    report_time = db.Column(db.DateTime, default=datetime.now)
    reporter = db.Column(db.String(50))
    status = db.Column(db.String(20), default='pending')
    handle_time = db.Column(db.DateTime)
    handler = db.Column(db.String(50))
    handle_note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)

    device = db.relationship('Device', backref=db.backref('faults', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'work_order_no': self.work_order_no,
            'device_id': self.device_id,
            'device_code': self.device.device_code if self.device else None,
            'device_name': self.device.device_name if self.device else None,
            'fault_type': self.fault_type,
            'fault_desc': self.fault_desc,
            'report_time': self.report_time.strftime('%Y-%m-%d %H:%M:%S'),
            'reporter': self.reporter,
            'status': self.status,
            'status_text': self.get_status_text(),
            'handle_time': self.handle_time.strftime('%Y-%m-%d %H:%M:%S') if self.handle_time else None,
            'handler': self.handler,
            'handle_note': self.handle_note,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def get_status_text(self):
        status_map = {
            'pending': '待处理',
            'processing': '处理中',
            'completed': '已完成'
        }
        return status_map.get(self.status, '未知')

    @staticmethod
    def generate_work_order_no():
        now = datetime.now()
        prefix = 'WO'
        date_str = now.strftime('%Y%m%d')
        count = Fault.query.filter(Fault.work_order_no.like(f'{prefix}{date_str}%')).count()
        return f'{prefix}{date_str}{str(count + 1).zfill(4)}'