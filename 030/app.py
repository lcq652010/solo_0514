from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gas_meter_v3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

FAULT_CATEGORIES = {
    '燃气泄漏': '燃气安全类',
    '压力异常': '燃气安全类',
    '阀门故障': '燃气安全类',
    '数据异常': '计量通讯类',
    '通讯中断': '计量通讯类',
    '电池电量低': '设备状态类',
    '传感器故障': '设备状态类',
    '显示屏故障': '设备状态类',
    '其他': '其他类'
}

PRIORITY_LEVELS = ['紧急', '高', '中', '低']

PRIORITY_RULES = {
    '燃气安全类': '紧急',
    '计量通讯类': '高',
    '设备状态类': '中',
    '其他类': '低'
}

def success_response(data=None, msg='成功', code=200):
    return jsonify({
        'code': code,
        'msg': msg,
        'data': data if data is not None else {}
    }), code

def error_response(msg='失败', code=400, data=None):
    return jsonify({
        'code': code,
        'msg': msg,
        'data': data if data is not None else {}
    }), code

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_no = db.Column(db.String(50), unique=True, nullable=False)
    device_name = db.Column(db.String(100), nullable=False)
    device_model = db.Column(db.String(100), nullable=False)
    communication_protocol = db.Column(db.String(50), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    building = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    install_date = db.Column(db.Date, nullable=False)
    enable_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='正常')
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'device_no': self.device_no,
            'device_name': self.device_name,
            'device_model': self.device_model,
            'communication_protocol': self.communication_protocol,
            'region': self.region,
            'building': self.building,
            'location': self.location,
            'install_date': self.install_date.strftime('%Y-%m-%d'),
            'enable_date': self.enable_date.strftime('%Y-%m-%d'),
            'status': self.status,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
        }

class DataUploadRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    device = db.relationship('Device', backref=db.backref('upload_records', lazy=True))
    upload_time = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(20), nullable=False)
    data_type = db.Column(db.String(50), default='计量数据')
    error_msg = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'device_no': self.device.device_no if self.device else '',
            'upload_time': self.upload_time.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self.status,
            'data_type': self.data_type,
            'error_msg': self.error_msg
        }

class WorkOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(50), unique=True, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    device = db.relationship('Device', backref=db.backref('work_orders', lazy=True))
    fault_type = db.Column(db.String(100), nullable=False)
    fault_category = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    fault_description = db.Column(db.Text, nullable=False)
    reporter = db.Column(db.String(50), nullable=False)
    report_time = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(20), default='待处理')
    handler = db.Column(db.String(50))
    handle_time = db.Column(db.DateTime)
    handle_result = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'order_no': self.order_no,
            'device_id': self.device_id,
            'device_no': self.device.device_no if self.device else '',
            'device_name': self.device.device_name if self.device else '',
            'region': self.device.region if self.device else '',
            'building': self.device.building if self.device else '',
            'fault_type': self.fault_type,
            'fault_category': self.fault_category,
            'priority': self.priority,
            'fault_description': self.fault_description,
            'reporter': self.reporter,
            'report_time': self.report_time.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self.status,
            'handler': self.handler,
            'handle_time': self.handle_time.strftime('%Y-%m-%d %H:%M:%S') if self.handle_time else '',
            'handle_result': self.handle_result
        }

class MaintenanceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    device = db.relationship('Device', backref=db.backref('maintenance_records', lazy=True))
    work_order_id = db.Column(db.Integer, db.ForeignKey('work_order.id'))
    work_order = db.relationship('WorkOrder', backref=db.backref('maintenance_records', lazy=True))
    maintenance_type = db.Column(db.String(50), nullable=False)
    maintenance_content = db.Column(db.Text, nullable=False)
    maintainer = db.Column(db.String(50), nullable=False)
    maintenance_time = db.Column(db.DateTime, default=datetime.now)
    remark = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'device_no': self.device.device_no if self.device else '',
            'device_name': self.device.device_name if self.device else '',
            'work_order_no': self.work_order.order_no if self.work_order else '',
            'maintenance_type': self.maintenance_type,
            'maintenance_content': self.maintenance_content,
            'maintainer': self.maintainer,
            'maintenance_time': self.maintenance_time.strftime('%Y-%m-%d %H:%M:%S'),
            'remark': self.remark
        }

def generate_order_no():
    today = datetime.now().strftime('%Y%m%d')
    last_order = WorkOrder.query.filter(WorkOrder.order_no.like(f'WO{today}%')).order_by(WorkOrder.order_no.desc()).first()
    if last_order:
        seq = int(last_order.order_no[-4:]) + 1
    else:
        seq = 1
    return f'WO{today}{seq:04d}'

def get_fault_category_and_priority(fault_type):
    category = FAULT_CATEGORIES.get(fault_type, '其他类')
    priority = PRIORITY_RULES.get(category, '低')
    return category, priority

@app.route('/api/devices', methods=['POST'])
def add_device():
    data = request.json
    required_fields = ['device_no', 'device_name', 'device_model', 
                       'communication_protocol', 'region', 'building', 
                       'location', 'install_date', 'enable_date']
    if not all(key in data for key in required_fields):
        return error_response('参数不全，缺少必填字段', 400)
    
    if Device.query.filter_by(device_no=data['device_no']).first():
        return error_response('设备编号已存在', 400)
    
    device = Device(
        device_no=data['device_no'],
        device_name=data['device_name'],
        device_model=data['device_model'],
        communication_protocol=data['communication_protocol'],
        region=data['region'],
        building=data['building'],
        location=data['location'],
        install_date=datetime.strptime(data['install_date'], '%Y-%m-%d').date(),
        enable_date=datetime.strptime(data['enable_date'], '%Y-%m-%d').date()
    )
    db.session.add(device)
    db.session.commit()
    return success_response(device.to_dict(), '添加成功')

@app.route('/api/devices', methods=['GET'])
def get_devices():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    status = request.args.get('status')
    device_model = request.args.get('device_model')
    protocol = request.args.get('communication_protocol')
    region = request.args.get('region')
    building = request.args.get('building')
    keyword = request.args.get('keyword', '')
    
    query = Device.query
    if status:
        query = query.filter_by(status=status)
    if device_model:
        query = query.filter_by(device_model=device_model)
    if protocol:
        query = query.filter_by(communication_protocol=protocol)
    if region:
        query = query.filter_by(region=region)
    if building:
        query = query.filter_by(building=building)
    if keyword:
        query = query.filter(
            (Device.device_no.like(f'%{keyword}%')) |
            (Device.device_name.like(f'%{keyword}%')) |
            (Device.location.like(f'%{keyword}%')) |
            (Device.region.like(f'%{keyword}%')) |
            (Device.building.like(f'%{keyword}%'))
        )
    
    pagination = query.order_by(Device.create_time.desc()).paginate(page=page, per_page=page_size, error_out=False)
    return success_response({
        'list': [d.to_dict() for d in pagination.items],
        'total': pagination.total,
        'page': page,
        'page_size': page_size
    })

@app.route('/api/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    device = Device.query.get(device_id)
    if not device:
        return error_response('设备不存在', 404)
    
    data = request.json
    if 'device_name' in data:
        device.device_name = data['device_name']
    if 'device_model' in data:
        device.device_model = data['device_model']
    if 'communication_protocol' in data:
        device.communication_protocol = data['communication_protocol']
    if 'region' in data:
        device.region = data['region']
    if 'building' in data:
        device.building = data['building']
    if 'location' in data:
        device.location = data['location']
    if 'install_date' in data:
        device.install_date = datetime.strptime(data['install_date'], '%Y-%m-%d').date()
    if 'enable_date' in data:
        device.enable_date = datetime.strptime(data['enable_date'], '%Y-%m-%d').date()
    if 'status' in data:
        if data['status'] not in ['正常', '故障', '维修中', '已修复']:
            return error_response('状态值无效', 400)
        device.status = data['status']
    
    db.session.commit()
    return success_response(device.to_dict(), '更新成功')

@app.route('/api/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    device = Device.query.get(device_id)
    if not device:
        return error_response('设备不存在', 404)
    
    db.session.delete(device)
    db.session.commit()
    return success_response(msg='删除成功')

@app.route('/api/devices/regions', methods=['GET'])
def get_regions():
    regions = db.session.query(Device.region).distinct().all()
    region_list = [r[0] for r in regions]
    return success_response({'regions': region_list})

@app.route('/api/devices/buildings', methods=['GET'])
def get_buildings():
    region = request.args.get('region')
    query = db.session.query(Device.building).distinct()
    if region:
        query = query.filter_by(region=region)
    buildings = query.all()
    building_list = [b[0] for b in buildings]
    return success_response({'buildings': building_list})

@app.route('/api/data-upload', methods=['POST'])
def report_upload():
    data = request.json
    if not all(key in data for key in ['device_id', 'status']):
        return error_response('参数不全', 400)
    
    device = Device.query.get(data['device_id'])
    if not device:
        return error_response('设备不存在', 404)
    
    record = DataUploadRecord(
        device_id=data['device_id'],
        status=data['status'],
        data_type=data.get('data_type', '计量数据'),
        error_msg=data.get('error_msg', '')
    )
    db.session.add(record)
    db.session.commit()
    return success_response(record.to_dict(), '上报成功')

@app.route('/api/data-upload', methods=['GET'])
def get_upload_records():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    device_id = request.args.get('device_id', type=int)
    status = request.args.get('status')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = DataUploadRecord.query
    if device_id:
        query = query.filter_by(device_id=device_id)
    if status:
        query = query.filter_by(status=status)
    if start_date:
        query = query.filter(DataUploadRecord.upload_time >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(DataUploadRecord.upload_time <= datetime.strptime(end_date, '%Y-%m-%d'))
    
    pagination = query.order_by(DataUploadRecord.upload_time.desc()).paginate(page=page, per_page=page_size, error_out=False)
    return success_response({
        'list': [r.to_dict() for r in pagination.items],
        'total': pagination.total,
        'page': page,
        'page_size': page_size
    })

@app.route('/api/workorders', methods=['POST'])
def create_workorder():
    data = request.json
    if not all(key in data for key in ['device_id', 'fault_type', 'fault_description', 'reporter']):
        return error_response('参数不全', 400)
    
    device = Device.query.get(data['device_id'])
    if not device:
        return error_response('设备不存在', 404)
    
    fault_category, priority = get_fault_category_and_priority(data['fault_type'])
    
    order_no = generate_order_no()
    work_order = WorkOrder(
        order_no=order_no,
        device_id=data['device_id'],
        fault_type=data['fault_type'],
        fault_category=fault_category,
        priority=priority,
        fault_description=data['fault_description'],
        reporter=data['reporter']
    )
    
    device.status = '故障'
    db.session.add(work_order)
    db.session.commit()
    return success_response(work_order.to_dict(), '上报成功')

@app.route('/api/workorders', methods=['GET'])
def get_workorders():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    status = request.args.get('status')
    device_id = request.args.get('device_id', type=int)
    fault_category = request.args.get('fault_category')
    priority = request.args.get('priority')
    region = request.args.get('region')
    building = request.args.get('building')
    
    query = WorkOrder.query.join(Device)
    if status:
        query = query.filter(WorkOrder.status == status)
    if device_id:
        query = query.filter(WorkOrder.device_id == device_id)
    if fault_category:
        query = query.filter(WorkOrder.fault_category == fault_category)
    if priority:
        query = query.filter(WorkOrder.priority == priority)
    if region:
        query = query.filter(Device.region == region)
    if building:
        query = query.filter(Device.building == building)
    
    pagination = query.order_by(
        db.case(
            (WorkOrder.priority == '紧急', 1),
            (WorkOrder.priority == '高', 2),
            (WorkOrder.priority == '中', 3),
            (WorkOrder.priority == '低', 4),
            else_=5
        ),
        WorkOrder.report_time.desc()
    ).paginate(page=page, per_page=page_size, error_out=False)
    
    return success_response({
        'list': [w.to_dict() for w in pagination.items],
        'total': pagination.total,
        'page': page,
        'page_size': page_size
    })

@app.route('/api/workorders/<int:order_id>/handle', methods=['PUT'])
def handle_workorder(order_id):
    work_order = WorkOrder.query.get(order_id)
    if not work_order:
        return error_response('工单不存在', 404)
    
    data = request.json
    if not all(key in data for key in ['handler', 'handle_result', 'next_status']):
        return error_response('参数不全', 400)
    
    if data['next_status'] not in ['维修中', '已修复']:
        return error_response('状态值无效', 400)
    
    work_order.handler = data['handler']
    work_order.handle_result = data['handle_result']
    work_order.handle_time = datetime.now()
    work_order.status = data['next_status']
    
    device = Device.query.get(work_order.device_id)
    if device:
        if data['next_status'] == '维修中':
            device.status = '维修中'
        elif data['next_status'] == '已修复':
            device.status = '已修复'
    
    db.session.commit()
    return success_response(work_order.to_dict(), '处理成功')

@app.route('/api/maintenance', methods=['POST'])
def add_maintenance():
    data = request.json
    if not all(key in data for key in ['device_id', 'maintenance_type', 'maintenance_content', 'maintainer']):
        return error_response('参数不全', 400)
    
    device = Device.query.get(data['device_id'])
    if not device:
        return error_response('设备不存在', 404)
    
    record = MaintenanceRecord(
        device_id=data['device_id'],
        work_order_id=data.get('work_order_id'),
        maintenance_type=data['maintenance_type'],
        maintenance_content=data['maintenance_content'],
        maintainer=data['maintainer'],
        remark=data.get('remark', '')
    )
    db.session.add(record)
    db.session.commit()
    return success_response(record.to_dict(), '添加成功')

@app.route('/api/maintenance', methods=['GET'])
def get_maintenance():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    device_id = request.args.get('device_id', type=int)
    work_order_id = request.args.get('work_order_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = MaintenanceRecord.query
    if device_id:
        query = query.filter_by(device_id=device_id)
    if work_order_id:
        query = query.filter_by(work_order_id=work_order_id)
    if start_date:
        query = query.filter(MaintenanceRecord.maintenance_time >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(MaintenanceRecord.maintenance_time <= datetime.strptime(end_date, '%Y-%m-%d'))
    
    pagination = query.order_by(MaintenanceRecord.maintenance_time.desc()).paginate(page=page, per_page=page_size, error_out=False)
    return success_response({
        'list': [m.to_dict() for m in pagination.items],
        'total': pagination.total,
        'page': page,
        'page_size': page_size
    })

@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    total_devices = Device.query.count()
    normal_devices = Device.query.filter_by(status='正常').count()
    fault_devices = Device.query.filter_by(status='故障').count()
    repairing_devices = Device.query.filter_by(status='维修中').count()
    repaired_devices = Device.query.filter_by(status='已修复').count()
    pending_orders = WorkOrder.query.filter_by(status='待处理').count()
    processing_orders = WorkOrder.query.filter_by(status='维修中').count()
    completed_orders = WorkOrder.query.filter_by(status='已修复').count()
    
    category_stats = db.session.query(
        WorkOrder.fault_category,
        db.func.count(WorkOrder.id)
    ).group_by(WorkOrder.fault_category).all()
    
    priority_stats = db.session.query(
        WorkOrder.priority,
        db.func.count(WorkOrder.id)
    ).filter_by(status='待处理').group_by(WorkOrder.priority).all()
    
    total_uploads = DataUploadRecord.query.count()
    success_uploads = DataUploadRecord.query.filter_by(status='成功').count()
    upload_success_rate = round((success_uploads / total_uploads * 100), 2) if total_uploads > 0 else 100.0
    
    health_rate = round((normal_devices / total_devices * 100), 2) if total_devices > 0 else 100.0
    
    region_stats = db.session.query(
        Device.region,
        db.func.count(Device.id),
        db.func.sum(db.case((Device.status == '正常', 1), else_=0))
    ).group_by(Device.region).all()
    
    region_health_stats = []
    for region, total, normal in region_stats:
        rate = round((normal / total * 100), 2) if total > 0 else 100.0
        region_health_stats.append({
            'region': region,
            'total_devices': total,
            'normal_devices': normal,
            'health_rate': rate
        })
    
    return success_response({
        'total_devices': total_devices,
        'normal_devices': normal_devices,
        'fault_devices': fault_devices,
        'repairing_devices': repairing_devices,
        'repaired_devices': repaired_devices,
        'device_health_rate': health_rate,
        'pending_orders': pending_orders,
        'processing_orders': processing_orders,
        'completed_orders': completed_orders,
        'category_stats': {cat: cnt for cat, cnt in category_stats},
        'priority_stats': {p: cnt for p, cnt in priority_stats},
        'upload_stats': {
            'total_uploads': total_uploads,
            'success_uploads': success_uploads,
            'success_rate': upload_success_rate
        },
        'region_health_stats': region_health_stats
    })

@app.route('/api/fault-types', methods=['GET'])
def get_fault_types():
    return success_response({
        'fault_types': list(FAULT_CATEGORIES.keys()),
        'fault_categories': list(set(FAULT_CATEGORIES.values())),
        'category_mapping': FAULT_CATEGORIES,
        'priority_rules': PRIORITY_RULES,
        'priority_levels': PRIORITY_LEVELS
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
