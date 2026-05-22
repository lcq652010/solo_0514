from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///maintenance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_code = db.Column(db.String(50), unique=True, nullable=False)
    device_name = db.Column(db.String(100), nullable=False)
    device_model = db.Column(db.String(100))
    communication_mode = db.Column(db.String(50))
    location = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='正常')
    install_date = db.Column(db.DateTime, default=datetime.now)
    enable_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'device_code': self.device_code,
            'device_name': self.device_name,
            'device_model': self.device_model,
            'communication_mode': self.communication_mode,
            'location': self.location,
            'status': self.status,
            'install_date': self.install_date.strftime('%Y-%m-%d') if self.install_date else None,
            'enable_date': self.enable_date.strftime('%Y-%m-%d') if self.enable_date else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class WorkOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(50), unique=True, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    device = db.relationship('Device', backref=db.backref('work_orders', lazy=True))
    fault_type = db.Column(db.String(50), default='其他故障')
    priority = db.Column(db.String(20), default='中')
    fault_description = db.Column(db.Text, nullable=False)
    reporter = db.Column(db.String(50), nullable=False)
    reporter_phone = db.Column(db.String(20))
    status = db.Column(db.String(20), default='待处理')
    handle_user = db.Column(db.String(50))
    handle_content = db.Column(db.Text)
    report_time = db.Column(db.DateTime, default=datetime.now)
    handle_time = db.Column(db.DateTime)
    complete_time = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        device = Device.query.get(self.device_id)
        return {
            'id': self.id,
            'order_no': self.order_no,
            'device_id': self.device_id,
            'device_code': device.device_code if device else '',
            'device_name': device.device_name if device else '',
            'location': device.location if device else '',
            'fault_type': self.fault_type,
            'priority': self.priority,
            'fault_description': self.fault_description,
            'reporter': self.reporter,
            'reporter_phone': self.reporter_phone,
            'status': self.status,
            'handle_user': self.handle_user,
            'handle_content': self.handle_content,
            'report_time': self.report_time.strftime('%Y-%m-%d %H:%M:%S') if self.report_time else None,
            'handle_time': self.handle_time.strftime('%Y-%m-%d %H:%M:%S') if self.handle_time else None,
            'complete_time': self.complete_time.strftime('%Y-%m-%d %H:%M:%S') if self.complete_time else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class MaintenanceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    device = db.relationship('Device', backref=db.backref('maintenance_records', lazy=True))
    work_order_id = db.Column(db.Integer, db.ForeignKey('work_order.id'))
    work_order = db.relationship('WorkOrder', backref=db.backref('maintenance_records', lazy=True))
    maintenance_type = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    operator = db.Column(db.String(50), nullable=False)
    maintenance_time = db.Column(db.DateTime, default=datetime.now)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        device = Device.query.get(self.device_id)
        return {
            'id': self.id,
            'device_id': self.device_id,
            'device_code': device.device_code if device else '',
            'device_name': device.device_name if device else '',
            'location': device.location if device else '',
            'work_order_id': self.work_order_id,
            'maintenance_type': self.maintenance_type,
            'content': self.content,
            'operator': self.operator,
            'maintenance_time': self.maintenance_time.strftime('%Y-%m-%d %H:%M:%S') if self.maintenance_time else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

def generate_order_no():
    today = datetime.now().strftime('%Y%m%d')
    last_order = WorkOrder.query.filter(WorkOrder.order_no.like(f'WO{today}%')).order_by(WorkOrder.id.desc()).first()
    if last_order:
        seq = int(last_order.order_no[-4:]) + 1
    else:
        seq = 1
    return f'WO{today}{seq:04d}'

def success_response(data=None, message='success'):
    return jsonify({
        'code': 200,
        'message': message,
        'data': data,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

def error_response(message='error', code=400):
    return jsonify({
        'code': code,
        'message': message,
        'data': None,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }), code

@app.route('/api/devices', methods=['GET'])
def get_devices():
    location = request.args.get('location')
    status = request.args.get('status')
    
    query = Device.query
    if location:
        query = query.filter(Device.location.like(f'%{location}%'))
    if status:
        query = query.filter(Device.status == status)
    
    devices = query.all()
    return success_response([d.to_dict() for d in devices])

@app.route('/api/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    device = Device.query.get(device_id)
    if not device:
        return error_response('设备不存在', 404)
    return success_response(device.to_dict())

@app.route('/api/devices', methods=['POST'])
def create_device():
    data = request.get_json()
    if not data.get('device_code') or not data.get('device_name') or not data.get('location'):
        return error_response('设备编号、名称和位置不能为空')
    
    if Device.query.filter_by(device_code=data['device_code']).first():
        return error_response('设备编号已存在')
    
    device = Device(
        device_code=data['device_code'],
        device_name=data['device_name'],
        device_model=data.get('device_model'),
        communication_mode=data.get('communication_mode'),
        location=data['location'],
        status=data.get('status', '正常')
    )
    if data.get('install_date'):
        device.install_date = datetime.strptime(data['install_date'], '%Y-%m-%d')
    if data.get('enable_date'):
        device.enable_date = datetime.strptime(data['enable_date'], '%Y-%m-%d')
    
    db.session.add(device)
    db.session.commit()
    return success_response(device.to_dict(), '设备添加成功')

@app.route('/api/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    device = Device.query.get(device_id)
    if not device:
        return error_response('设备不存在', 404)
    
    data = request.get_json()
    if data.get('device_code'):
        existing = Device.query.filter_by(device_code=data['device_code']).first()
        if existing and existing.id != device_id:
            return error_response('设备编号已存在')
        device.device_code = data['device_code']
    
    if data.get('device_name'):
        device.device_name = data['device_name']
    if data.get('device_model') is not None:
        device.device_model = data['device_model']
    if data.get('communication_mode') is not None:
        device.communication_mode = data['communication_mode']
    if data.get('location'):
        device.location = data['location']
    if data.get('status'):
        if data['status'] not in ['正常', '故障', '维修中', '已修复']:
            return error_response('无效的设备状态')
        device.status = data['status']
    if data.get('install_date'):
        device.install_date = datetime.strptime(data['install_date'], '%Y-%m-%d')
    if data.get('enable_date'):
        device.enable_date = datetime.strptime(data['enable_date'], '%Y-%m-%d')
    
    db.session.commit()
    return success_response(device.to_dict(), '设备更新成功')

@app.route('/api/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    device = Device.query.get(device_id)
    if not device:
        return error_response('设备不存在', 404)
    
    db.session.delete(device)
    db.session.commit()
    return success_response(None, '设备删除成功')

@app.route('/api/devices/<int:device_id>/status', methods=['PUT'])
def update_device_status(device_id):
    device = Device.query.get(device_id)
    if not device:
        return error_response('设备不存在', 404)
    
    data = request.get_json()
    status = data.get('status')
    if status not in ['正常', '故障', '维修中', '已修复']:
        return error_response('无效的设备状态')
    
    device.status = status
    db.session.commit()
    return success_response(device.to_dict(), '设备状态更新成功')

@app.route('/api/workorders', methods=['GET'])
def get_workorders():
    status = request.args.get('status')
    priority = request.args.get('priority')
    fault_type = request.args.get('fault_type')
    device_id = request.args.get('device_id')
    
    query = WorkOrder.query
    if status:
        query = query.filter(WorkOrder.status == status)
    if priority:
        query = query.filter(WorkOrder.priority == priority)
    if fault_type:
        query = query.filter(WorkOrder.fault_type.like(f'%{fault_type}%'))
    if device_id:
        query = query.filter(WorkOrder.device_id == device_id)
    
    workorders = query.order_by(WorkOrder.created_at.desc()).all()
    return success_response([w.to_dict() for w in workorders])

@app.route('/api/workorders/<int:order_id>', methods=['GET'])
def get_workorder(order_id):
    workorder = WorkOrder.query.get(order_id)
    if not workorder:
        return error_response('工单不存在', 404)
    return success_response(workorder.to_dict())

@app.route('/api/workorders', methods=['POST'])
def create_workorder():
    data = request.get_json()
    if not data.get('device_id') or not data.get('fault_description') or not data.get('reporter'):
        return error_response('设备ID、故障描述和上报人不能为空')
    
    device = Device.query.get(data['device_id'])
    if not device:
        return error_response('设备不存在', 404)
    
    fault_type = data.get('fault_type', '其他故障')
    priority = data.get('priority', '中')
    if priority not in ['高', '中', '低']:
        return error_response('优先级只能是高、中、低')
    
    order_no = generate_order_no()
    workorder = WorkOrder(
        order_no=order_no,
        device_id=data['device_id'],
        fault_type=fault_type,
        priority=priority,
        fault_description=data['fault_description'],
        reporter=data['reporter'],
        reporter_phone=data.get('reporter_phone', '')
    )
    
    device.status = '故障'
    
    db.session.add(workorder)
    db.session.commit()
    return success_response(workorder.to_dict(), '故障上报成功')

@app.route('/api/workorders/<int:order_id>/handle', methods=['PUT'])
def handle_workorder(order_id):
    workorder = WorkOrder.query.get(order_id)
    if not workorder:
        return error_response('工单不存在', 404)
    
    data = request.get_json()
    handle_user = data.get('handle_user')
    if not handle_user:
        return error_response('处理人不能为空')
    
    workorder.status = '处理中'
    workorder.handle_user = handle_user
    workorder.handle_time = datetime.now()
    
    device = Device.query.get(workorder.device_id)
    if device:
        device.status = '维修中'
    
    db.session.commit()
    return success_response(workorder.to_dict(), '工单已受理')

@app.route('/api/workorders/<int:order_id>/complete', methods=['PUT'])
def complete_workorder(order_id):
    workorder = WorkOrder.query.get(order_id)
    if not workorder:
        return error_response('工单不存在', 404)
    
    data = request.get_json()
    handle_content = data.get('handle_content')
    if not handle_content:
        return error_response('处理内容不能为空')
    
    workorder.status = '已完成'
    workorder.handle_content = handle_content
    workorder.complete_time = datetime.now()
    
    device = Device.query.get(workorder.device_id)
    if device:
        device.status = '已修复'
    
    record = MaintenanceRecord(
        device_id=workorder.device_id,
        work_order_id=workorder.id,
        maintenance_type='故障维修',
        content=handle_content,
        operator=workorder.handle_user or '系统'
    )
    db.session.add(record)
    
    db.session.commit()
    return success_response(workorder.to_dict(), '工单已完成')

@app.route('/api/maintenance', methods=['GET'])
def get_maintenance_records():
    device_id = request.args.get('device_id')
    maintenance_type = request.args.get('type')
    
    query = MaintenanceRecord.query
    if device_id:
        query = query.filter(MaintenanceRecord.device_id == device_id)
    if maintenance_type:
        query = query.filter(MaintenanceRecord.maintenance_type.like(f'%{maintenance_type}%'))
    
    records = query.order_by(MaintenanceRecord.created_at.desc()).all()
    return success_response([r.to_dict() for r in records])

@app.route('/api/maintenance', methods=['POST'])
def create_maintenance_record():
    data = request.get_json()
    if not data.get('device_id') or not data.get('maintenance_type') or not data.get('content') or not data.get('operator'):
        return error_response('设备ID、维护类型、内容和操作人不能为空')
    
    device = Device.query.get(data['device_id'])
    if not device:
        return error_response('设备不存在', 404)
    
    record = MaintenanceRecord(
        device_id=data['device_id'],
        work_order_id=data.get('work_order_id'),
        maintenance_type=data['maintenance_type'],
        content=data['content'],
        operator=data['operator']
    )
    if data.get('maintenance_time'):
        record.maintenance_time = datetime.strptime(data['maintenance_time'], '%Y-%m-%d %H:%M:%S')
    
    db.session.add(record)
    db.session.commit()
    return success_response(record.to_dict(), '运维记录添加成功')

@app.route('/api/locations', methods=['GET'])
def get_locations():
    locations = db.session.query(Device.location).distinct().all()
    location_list = [loc[0] for loc in locations]
    return success_response(location_list)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    total_devices = Device.query.count()
    normal_devices = Device.query.filter_by(status='正常').count()
    fault_devices = Device.query.filter_by(status='故障').count()
    repairing_devices = Device.query.filter_by(status='维修中').count()
    repaired_devices = Device.query.filter_by(status='已修复').count()
    
    health_rate = round((normal_devices / total_devices * 100), 2) if total_devices > 0 else 0
    
    total_workorders = WorkOrder.query.count()
    pending_workorders = WorkOrder.query.filter_by(status='待处理').count()
    handling_workorders = WorkOrder.query.filter_by(status='处理中').count()
    completed_workorders = WorkOrder.query.filter_by(status='已完成').count()
    
    high_priority = WorkOrder.query.filter_by(priority='高').count()
    medium_priority = WorkOrder.query.filter_by(priority='中').count()
    low_priority = WorkOrder.query.filter_by(priority='低').count()
    
    total_records = MaintenanceRecord.query.count()
    
    locations = db.session.query(Device.location).distinct().all()
    location_list = [loc[0] for loc in locations]
    
    return success_response({
        'devices': {
            'total': total_devices,
            'normal': normal_devices,
            'fault': fault_devices,
            'repairing': repairing_devices,
            'repaired': repaired_devices,
            'health_rate': health_rate
        },
        'workorders': {
            'total': total_workorders,
            'pending': pending_workorders,
            'handling': handling_workorders,
            'completed': completed_workorders,
            'priority': {
                'high': high_priority,
                'medium': medium_priority,
                'low': low_priority
            }
        },
        'maintenance_records': total_records,
        'locations': location_list
    })

with app.app_context():
    db.create_all()
    if Device.query.count() == 0:
        sample_devices = [
            Device(device_code='DEV001', device_name='核酸采样终端-01', device_model='HC-2000Pro', communication_mode='以太网/WiFi', location='门诊大厅1号窗口', status='正常', enable_date=datetime(2024, 1, 15)),
            Device(device_code='DEV002', device_name='核酸采样终端-02', device_model='HC-2000Pro', communication_mode='以太网/WiFi', location='门诊大厅2号窗口', status='正常', enable_date=datetime(2024, 1, 15)),
            Device(device_code='DEV003', device_name='核酸采样终端-03', device_model='HC-2000Lite', communication_mode='4G/以太网', location='住院部一楼', status='故障', enable_date=datetime(2024, 2, 20)),
            Device(device_code='DEV004', device_name='核酸采样终端-04', device_model='HC-2000Pro', communication_mode='以太网/WiFi', location='急诊部入口', status='正常', enable_date=datetime(2024, 3, 10)),
            Device(device_code='DEV005', device_name='核酸采样终端-05', device_model='HC-2000Lite', communication_mode='4G/以太网', location='发热门诊', status='维修中', enable_date=datetime(2024, 4, 1)),
        ]
        db.session.add_all(sample_devices)
        db.session.commit()
    
    if WorkOrder.query.count() == 0:
        today_str = datetime.now().strftime('%Y%m%d')
        sample_workorders = [
            WorkOrder(order_no=f'WO{today_str}0001', device_id=3, fault_type='硬件故障', priority='高', fault_description='触摸屏无响应，无法进行采样登记', reporter='张护士'),
            WorkOrder(order_no=f'WO{today_str}0002', device_id=5, fault_type='软件故障', priority='中', fault_description='扫码识别速度慢，偶发崩溃', reporter='李护士', status='处理中', handle_user='王工', handle_time=datetime.now()),
            WorkOrder(order_no=f'WO{today_str}0003', device_id=2, fault_type='网络故障', priority='低', fault_description='网络连接偶尔中断', reporter='赵护士', status='已完成', handle_user='王工', handle_content='更换网线，重启路由器', handle_time=datetime.now(), complete_time=datetime.now()),
        ]
        for wo in sample_workorders:
            db.session.add(wo)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
