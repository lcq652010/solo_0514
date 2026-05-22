from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank_atm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_code = db.Column(db.String(50), unique=True, nullable=False)
    device_name = db.Column(db.String(100), nullable=False)
    device_model = db.Column(db.String(100))
    system_version = db.Column(db.String(50))
    enable_date = db.Column(db.Date)
    area = db.Column(db.String(100))
    location = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='正常')
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class WorkOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(50), unique=True, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    fault_type = db.Column(db.String(50), nullable=False)
    fault_description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='一般')
    reporter = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='待处理')
    handle_user = db.Column(db.String(50))
    handle_result = db.Column(db.Text)
    complete_time = db.Column(db.DateTime)
    create_time = db.Column(db.DateTime, default=datetime.now)
    handle_time = db.Column(db.DateTime)
    device = db.relationship('Device', backref=db.backref('work_orders', lazy=True))


class MaintenanceLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_order_id = db.Column(db.Integer, db.ForeignKey('work_order.id'), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    log_type = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    operator = db.Column(db.String(50), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    work_order = db.relationship('WorkOrder', backref=db.backref('maintenance_logs', lazy=True))
    device = db.relationship('Device', backref=db.backref('maintenance_logs', lazy=True))


class MaintenanceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    work_order_id = db.Column(db.Integer, db.ForeignKey('work_order.id'))
    maintenance_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    operator = db.Column(db.String(50), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    device = db.relationship('Device', backref=db.backref('maintenance_records', lazy=True))


FAULT_TYPES = ['硬件故障', '软件故障', '网络故障', '电源故障', '打印机故障', '读卡器故障', '其他']
PRIORITY_LEVELS = ['低', '一般', '高', '紧急']
DEVICE_STATUSES = ['正常', '故障', '维修中', '已修复']
ORDER_STATUSES = ['待处理', '处理中', '已处理', '已完成']
AREA_LIST = ['天河区', '越秀区', '海珠区', '荔湾区', '白云区', '番禺区']

PRIORITY_WEIGHT = {'低': 0, '一般': 1, '高': 2, '紧急': 3}
PRIORITY_COLOR = {'低': '#52c41a', '一般': '#1890ff', '高': '#faad14', '紧急': '#f5222d'}


def generate_order_no():
    today = datetime.now().strftime('%Y%m%d')
    last_order = WorkOrder.query.filter(WorkOrder.order_no.like(f'WO{today}%')).order_by(WorkOrder.id.desc()).first()
    if last_order:
        seq = int(last_order.order_no[-4:]) + 1
    else:
        seq = 1
    return f'WO{today}{seq:04d}'


def parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        return None


def api_response(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            if isinstance(result, tuple):
                return result
            return jsonify({'code': 200, 'message': 'success', 'data': result}), 200
        except Exception as e:
            return jsonify({'code': 500, 'message': str(e), 'data': None}), 500
    return decorated


def success_response(data=None, message='操作成功'):
    return jsonify({'code': 200, 'message': message, 'data': data})


def error_response(message='操作失败', code=400):
    return jsonify({'code': code, 'message': message, 'data': None}), code


def sort_by_priority(orders):
    return sorted(orders, key=lambda x: PRIORITY_WEIGHT.get(x.priority, 0), reverse=True)


def device_to_dict(d):
    pending_count = WorkOrder.query.filter_by(device_id=d.id, status='待处理').count()
    processing_count = WorkOrder.query.filter_by(device_id=d.id, status='处理中').count()
    return {
        'id': d.id,
        'device_code': d.device_code,
        'device_name': d.device_name,
        'device_model': d.device_model,
        'system_version': d.system_version,
        'enable_date': d.enable_date.strftime('%Y-%m-%d') if d.enable_date else None,
        'area': d.area,
        'location': d.location,
        'status': d.status,
        'pending_order_count': pending_count,
        'processing_order_count': processing_count,
        'create_time': d.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        'update_time': d.update_time.strftime('%Y-%m-%d %H:%M:%S')
    }


def order_to_dict(o):
    return {
        'id': o.id,
        'order_no': o.order_no,
        'device_id': o.device_id,
        'device_code': o.device.device_code,
        'device_name': o.device.device_name,
        'area': o.device.area,
        'location': o.device.location,
        'fault_type': o.fault_type,
        'fault_description': o.fault_description,
        'priority': o.priority,
        'priority_color': PRIORITY_COLOR.get(o.priority, '#1890ff'),
        'reporter': o.reporter,
        'status': o.status,
        'handle_user': o.handle_user,
        'handle_result': o.handle_result,
        'create_time': o.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        'handle_time': o.handle_time.strftime('%Y-%m-%d %H:%M:%S') if o.handle_time else None,
        'complete_time': o.complete_time.strftime('%Y-%m-%d %H:%M:%S') if o.complete_time else None
    }


@app.route('/api/devices', methods=['POST'])
def add_device():
    data = request.get_json()
    if not data.get('device_code') or not data.get('device_name') or not data.get('location'):
        return error_response('设备编号、名称、位置不能为空')
    
    if Device.query.filter_by(device_code=data['device_code']).first():
        return error_response('设备编号已存在')
    
    enable_date = parse_date(data.get('enable_date'))
    
    device = Device(
        device_code=data['device_code'],
        device_name=data['device_name'],
        device_model=data.get('device_model'),
        system_version=data.get('system_version'),
        enable_date=enable_date,
        area=data.get('area'),
        location=data['location'],
        status=data.get('status', '正常')
    )
    db.session.add(device)
    db.session.commit()
    return success_response(device.id, '添加成功')


@app.route('/api/devices', methods=['GET'])
def get_devices():
    status = request.args.get('status')
    area = request.args.get('area')
    keyword = request.args.get('keyword', '')
    
    query = Device.query
    
    if status:
        query = query.filter_by(status=status)
    if area:
        query = query.filter_by(area=area)
    if keyword:
        query = query.filter(
            (Device.device_code.like(f'%{keyword}%')) |
            (Device.device_name.like(f'%{keyword}%')) |
            (Device.location.like(f'%{keyword}%'))
        )
    
    devices = query.order_by(Device.id.desc()).all()
    result = [device_to_dict(d) for d in devices]
    return success_response(result)


@app.route('/api/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    device = Device.query.get(device_id)
    if not device:
        return error_response('设备不存在', 404)
    
    orders = WorkOrder.query.filter_by(device_id=device_id).order_by(WorkOrder.id.desc()).limit(10).all()
    orders_data = [order_to_dict(o) for o in orders]
    
    logs = MaintenanceLog.query.filter_by(device_id=device_id).order_by(MaintenanceLog.id.desc()).limit(20).all()
    logs_data = [{
        'id': l.id,
        'log_type': l.log_type,
        'content': l.content,
        'operator': l.operator,
        'create_time': l.create_time.strftime('%Y-%m-%d %H:%M:%S')
    } for l in logs]
    
    result = device_to_dict(device)
    result['recent_orders'] = orders_data
    result['recent_logs'] = logs_data
    
    return success_response(result)


@app.route('/api/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    device = Device.query.get(device_id)
    if not device:
        return error_response('设备不存在', 404)
    
    data = request.get_json()
    if data.get('device_name'):
        device.device_name = data['device_name']
    if data.get('device_model'):
        device.device_model = data['device_model']
    if data.get('system_version'):
        device.system_version = data['system_version']
    if data.get('enable_date'):
        device.enable_date = parse_date(data.get('enable_date'))
    if data.get('area'):
        device.area = data['area']
    if data.get('location'):
        device.location = data['location']
    if data.get('status'):
        if data['status'] not in DEVICE_STATUSES:
            return error_response('无效的状态值')
        device.status = data['status']
    
    db.session.commit()
    return success_response(None, '更新成功')


@app.route('/api/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    device = Device.query.get(device_id)
    if not device:
        return error_response('设备不存在', 404)
    
    if WorkOrder.query.filter_by(device_id=device_id).count() > 0:
        return error_response('该设备存在关联工单，无法删除')
    
    db.session.delete(device)
    db.session.commit()
    return success_response(None, '删除成功')


@app.route('/api/workorders', methods=['POST'])
def create_workorder():
    data = request.get_json()
    if not data.get('device_id') or not data.get('fault_type') or not data.get('fault_description') or not data.get('reporter'):
        return error_response('设备ID、故障类型、故障描述、上报人不能为空')
    
    if data.get('fault_type') not in FAULT_TYPES:
        return error_response('无效的故障类型')
    
    if data.get('priority') and data.get('priority') not in PRIORITY_LEVELS:
        return error_response('无效的优先级')
    
    device = Device.query.get(data['device_id'])
    if not device:
        return error_response('设备不存在', 404)
    
    order_no = generate_order_no()
    work_order = WorkOrder(
        order_no=order_no,
        device_id=data['device_id'],
        fault_type=data['fault_type'],
        fault_description=data['fault_description'],
        priority=data.get('priority', '一般'),
        reporter=data['reporter'],
        status='待处理'
    )
    
    device.status = '故障'
    
    log = MaintenanceLog(
        work_order_id=work_order.id,
        device_id=data['device_id'],
        log_type='故障上报',
        content=f'上报故障：{data["fault_description"]}',
        operator=data['reporter']
    )
    
    db.session.add(work_order)
    db.session.add(log)
    db.session.commit()
    
    log.work_order_id = work_order.id
    db.session.commit()
    
    return success_response({'order_no': order_no}, '报修成功')


@app.route('/api/workorders', methods=['GET'])
def get_workorders():
    status = request.args.get('status')
    fault_type = request.args.get('fault_type')
    priority = request.args.get('priority')
    area = request.args.get('area')
    keyword = request.args.get('keyword', '')
    
    query = WorkOrder.query.join(Device)
    
    if status:
        query = query.filter(WorkOrder.status == status)
    if fault_type:
        query = query.filter(WorkOrder.fault_type == fault_type)
    if priority:
        query = query.filter(WorkOrder.priority == priority)
    if area:
        query = query.filter(Device.area == area)
    if keyword:
        query = query.filter(
            (WorkOrder.order_no.like(f'%{keyword}%')) |
            (Device.device_code.like(f'%{keyword}%')) |
            (Device.device_name.like(f'%{keyword}%'))
        )
    
    orders = query.order_by(WorkOrder.id.desc()).all()
    sorted_orders = sort_by_priority(orders)
    result = [order_to_dict(o) for o in sorted_orders]
    return success_response(result)


@app.route('/api/workorders/<int:order_id>', methods=['GET'])
def get_workorder(order_id):
    order = WorkOrder.query.get(order_id)
    if not order:
        return error_response('工单不存在', 404)
    
    logs = MaintenanceLog.query.filter_by(work_order_id=order_id).order_by(MaintenanceLog.id.desc()).all()
    logs_data = [{
        'id': l.id,
        'log_type': l.log_type,
        'content': l.content,
        'operator': l.operator,
        'create_time': l.create_time.strftime('%Y-%m-%d %H:%M:%S')
    } for l in logs]
    
    result = order_to_dict(order)
    result['maintenance_logs'] = logs_data
    return success_response(result)


@app.route('/api/workorders/<int:order_id>/start', methods=['PUT'])
def start_workorder(order_id):
    order = WorkOrder.query.get(order_id)
    if not order:
        return error_response('工单不存在', 404)
    
    if order.status != '待处理':
        return error_response('只有待处理工单可以开始处理')
    
    data = request.get_json()
    if not data.get('handle_user'):
        return error_response('处理人不能为空')
    
    order.handle_user = data['handle_user']
    order.status = '处理中'
    order.handle_time = datetime.now()
    
    order.device.status = '维修中'
    
    log = MaintenanceLog(
        work_order_id=order_id,
        device_id=order.device_id,
        log_type='开始处理',
        content=data.get('content', '开始处理故障'),
        operator=data['handle_user']
    )
    
    db.session.add(log)
    db.session.commit()
    return success_response(None, '开始处理')


@app.route('/api/workorders/<int:order_id>/handle', methods=['PUT'])
def handle_workorder(order_id):
    order = WorkOrder.query.get(order_id)
    if not order:
        return error_response('工单不存在', 404)
    
    data = request.get_json()
    if not data.get('handle_user') or not data.get('handle_result'):
        return error_response('处理人、处理结果不能为空')
    
    order.handle_user = data['handle_user']
    order.handle_result = data['handle_result']
    order.status = '已处理'
    order.handle_time = datetime.now()
    
    log = MaintenanceLog(
        work_order_id=order_id,
        device_id=order.device_id,
        log_type='处理记录',
        content=data['handle_result'],
        operator=data['handle_user']
    )
    
    db.session.add(log)
    db.session.commit()
    return success_response(None, '处理成功')


@app.route('/api/workorders/<int:order_id>/complete', methods=['PUT'])
def complete_workorder(order_id):
    order = WorkOrder.query.get(order_id)
    if not order:
        return error_response('工单不存在', 404)
    
    if order.status not in ['处理中', '已处理']:
        return error_response('只有处理中的工单可以完成')
    
    data = request.get_json()
    operator = data.get('operator', 'system') if data else 'system'
    
    order.status = '已完成'
    order.complete_time = datetime.now()
    order.device.status = '正常'
    
    log = MaintenanceLog(
        work_order_id=order_id,
        device_id=order.device_id,
        log_type='维修完成',
        content=data.get('content', '故障修复完成，设备恢复正常') if data else '故障修复完成，设备恢复正常',
        operator=operator
    )
    
    db.session.add(log)
    db.session.commit()
    return success_response(None, '维修完成')


@app.route('/api/maintenance', methods=['GET'])
def get_maintenance_records():
    device_id = request.args.get('device_id')
    query = MaintenanceRecord.query
    if device_id:
        query = query.filter_by(device_id=device_id)
    records = query.order_by(MaintenanceRecord.id.desc()).all()
    result = [{
        'id': r.id,
        'device_id': r.device_id,
        'device_code': r.device.device_code,
        'device_name': r.device.device_name,
        'area': r.device.area,
        'work_order_id': r.work_order_id,
        'maintenance_type': r.maintenance_type,
        'description': r.description,
        'operator': r.operator,
        'create_time': r.create_time.strftime('%Y-%m-%d %H:%M:%S')
    } for r in records]
    return success_response(result)


@app.route('/api/maintenance', methods=['POST'])
def add_maintenance_record():
    data = request.get_json()
    if not data.get('device_id') or not data.get('maintenance_type') or not data.get('description') or not data.get('operator'):
        return error_response('设备ID、维护类型、描述、操作人不能为空')
    
    device = Device.query.get(data['device_id'])
    if not device:
        return error_response('设备不存在', 404)
    
    record = MaintenanceRecord(
        device_id=data['device_id'],
        work_order_id=data.get('work_order_id'),
        maintenance_type=data['maintenance_type'],
        description=data['description'],
        operator=data['operator']
    )
    db.session.add(record)
    db.session.commit()
    return success_response(record.id, '添加成功')


@app.route('/api/maintenance/logs', methods=['GET'])
def get_maintenance_logs():
    device_id = request.args.get('device_id')
    work_order_id = request.args.get('work_order_id')
    
    query = MaintenanceLog.query
    if device_id:
        query = query.filter_by(device_id=device_id)
    if work_order_id:
        query = query.filter_by(work_order_id=work_order_id)
    
    logs = query.order_by(MaintenanceLog.id.desc()).all()
    result = [{
        'id': l.id,
        'work_order_id': l.work_order_id,
        'device_id': l.device_id,
        'device_code': l.device.device_code,
        'device_name': l.device.device_name,
        'log_type': l.log_type,
        'content': l.content,
        'operator': l.operator,
        'create_time': l.create_time.strftime('%Y-%m-%d %H:%M:%S')
    } for l in logs]
    return success_response(result)


@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    total_devices = Device.query.count()
    normal_devices = Device.query.filter_by(status='正常').count()
    fault_devices = Device.query.filter_by(status='故障').count()
    repairing_devices = Device.query.filter_by(status='维修中').count()
    repaired_devices = Device.query.filter_by(status='已修复').count()
    
    availability_rate = (normal_devices + repaired_devices) / total_devices * 100 if total_devices > 0 else 0
    
    total_orders = WorkOrder.query.count()
    pending_orders = WorkOrder.query.filter_by(status='待处理').count()
    processing_orders = WorkOrder.query.filter_by(status='处理中').count()
    completed_orders = WorkOrder.query.filter_by(status='已完成').count()
    
    urgent_orders = WorkOrder.query.filter_by(priority='紧急', status='待处理').count()
    high_orders = WorkOrder.query.filter_by(priority='高', status='待处理').count()
    
    fault_type_stats = []
    for ft in FAULT_TYPES:
        count = WorkOrder.query.filter_by(fault_type=ft).count()
        if count > 0:
            fault_type_stats.append({'type': ft, 'count': count})
    
    area_stats = []
    for area in AREA_LIST:
        device_count = Device.query.filter_by(area=area).count()
        fault_count = WorkOrder.query.join(Device).filter(Device.area == area, WorkOrder.status.in_(['待处理', '处理中'])).count()
        if device_count > 0:
            area_stats.append({
                'area': area,
                'device_count': device_count,
                'fault_count': fault_count
            })
    
    return success_response({
        'device_stats': {
            'total': total_devices,
            'normal': normal_devices,
            'fault': fault_devices,
            'repairing': repairing_devices,
            'repaired': repaired_devices,
            'availability_rate': round(availability_rate, 2)
        },
        'order_stats': {
            'total': total_orders,
            'pending': pending_orders,
            'processing': processing_orders,
            'completed': completed_orders,
            'urgent_pending': urgent_orders,
            'high_pending': high_orders
        },
        'fault_type_stats': fault_type_stats,
        'area_stats': area_stats
    })


@app.route('/api/statistics/availability', methods=['GET'])
def get_availability_stats():
    area = request.args.get('area')
    
    query = Device.query
    if area:
        query = query.filter_by(area=area)
    
    total_devices = query.count()
    normal_devices = query.filter(Device.status.in_(['正常', '已修复'])).count()
    fault_devices = query.filter(Device.status.in_(['故障', '维修中'])).count()
    
    availability_rate = normal_devices / total_devices * 100 if total_devices > 0 else 0
    
    area_detail = []
    for a in AREA_LIST:
        area_total = Device.query.filter_by(area=a).count()
        area_normal = Device.query.filter_by(area=a).filter(Device.status.in_(['正常', '已修复'])).count()
        if area_total > 0:
            area_detail.append({
                'area': a,
                'total': area_total,
                'normal': area_normal,
                'availability_rate': round(area_normal / area_total * 100, 2)
            })
    
    return success_response({
        'total_devices': total_devices,
        'normal_devices': normal_devices,
        'fault_devices': fault_devices,
        'availability_rate': round(availability_rate, 2),
        'area_detail': area_detail
    })


@app.route('/api/config', methods=['GET'])
def get_config():
    return success_response({
        'fault_types': FAULT_TYPES,
        'priority_levels': PRIORITY_LEVELS,
        'device_statuses': DEVICE_STATUSES,
        'order_statuses': ORDER_STATUSES,
        'area_list': AREA_LIST,
        'priority_color': PRIORITY_COLOR
    })


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
