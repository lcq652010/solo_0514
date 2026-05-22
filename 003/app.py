from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'baggage_management.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(app)


def success_response(data=None, message='操作成功', code=200):
    return jsonify({
        'code': code,
        'message': message,
        'data': data,
        'timestamp': datetime.now().isoformat()
    }), code


def error_response(message='操作失败', code=400):
    return jsonify({
        'code': code,
        'message': message,
        'data': None,
        'timestamp': datetime.now().isoformat()
    }), code


def paginate_query(query, page, per_page, item_converter):
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    items = [item_converter(item) for item in pagination.items]
    return {
        'list': items,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    }


class Device(db.Model):
    __tablename__ = 'devices'
    
    id = db.Column(db.Integer, primary_key=True)
    device_code = db.Column(db.String(50), unique=True, nullable=False)
    device_name = db.Column(db.String(100), nullable=False)
    device_model = db.Column(db.String(100))
    communication_mode = db.Column(db.String(50))
    terminal = db.Column(db.String(50))
    checkin_island = db.Column(db.String(50))
    location = db.Column(db.String(100), nullable=False)
    install_date = db.Column(db.Date, nullable=False)
    activation_date = db.Column(db.Date)
    status = db.Column(db.String(20), nullable=False, default='正常')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    maintenance_records = db.relationship('MaintenanceRecord', backref='device', lazy=True)
    work_orders = db.relationship('WorkOrder', backref='device', lazy=True)


class WorkOrder(db.Model):
    __tablename__ = 'work_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(50), unique=True, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    fault_type = db.Column(db.String(50), nullable=False, default='其他')
    fault_level = db.Column(db.String(20), nullable=False, default='一般')
    priority = db.Column(db.String(20), nullable=False, default='普通')
    fault_description = db.Column(db.Text, nullable=False)
    reporter = db.Column(db.String(50), nullable=False)
    report_time = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(20), nullable=False, default='待处理')
    handler = db.Column(db.String(50))
    handle_time = db.Column(db.DateTime)
    handle_result = db.Column(db.Text)
    repair_duration = db.Column(db.Integer)
    parts_used = db.Column(db.Text)


class MaintenanceRecord(db.Model):
    __tablename__ = 'maintenance_records'
    
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    record_type = db.Column(db.String(20), nullable=False)
    work_order_no = db.Column(db.String(50))
    fault_type = db.Column(db.String(50))
    fault_level = db.Column(db.String(20))
    description = db.Column(db.Text, nullable=False)
    operator = db.Column(db.String(50), nullable=False)
    operate_time = db.Column(db.DateTime, default=datetime.now)
    duration = db.Column(db.Integer)
    parts_used = db.Column(db.Text)
    remark = db.Column(db.Text)


def get_priority_weight(priority):
    weights = {'紧急': 1, '高': 2, '普通': 3, '低': 4}
    return weights.get(priority, 5)


def generate_order_no():
    today = datetime.now().strftime('%Y%m%d')
    last_order = WorkOrder.query.filter(WorkOrder.order_no.like(f'WO{today}%')).order_by(WorkOrder.order_no.desc()).first()
    if last_order:
        seq = int(last_order.order_no[-4:]) + 1
    else:
        seq = 1
    return f'WO{today}{seq:04d}'


def convert_device(device, include_orders=False):
    result = {
        'id': device.id,
        'device_code': device.device_code,
        'device_name': device.device_name,
        'device_model': device.device_model,
        'communication_mode': device.communication_mode,
        'terminal': device.terminal,
        'checkin_island': device.checkin_island,
        'location': device.location,
        'install_date': device.install_date.strftime('%Y-%m-%d') if device.install_date else None,
        'activation_date': device.activation_date.strftime('%Y-%m-%d') if device.activation_date else None,
        'status': device.status,
        'created_at': device.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': device.updated_at.strftime('%Y-%m-%d %H:%M:%S')
    }
    if include_orders:
        result['work_orders'] = [convert_work_order(order) for order in device.work_orders[:5]]
        result['maintenance_count'] = len(device.maintenance_records)
    return result


def convert_work_order(order):
    return {
        'id': order.id,
        'order_no': order.order_no,
        'device_code': order.device.device_code,
        'device_name': order.device.device_name,
        'terminal': order.device.terminal,
        'checkin_island': order.device.checkin_island,
        'location': order.device.location,
        'fault_type': order.fault_type,
        'fault_level': order.fault_level,
        'priority': order.priority,
        'priority_weight': get_priority_weight(order.priority),
        'fault_description': order.fault_description,
        'reporter': order.reporter,
        'report_time': order.report_time.strftime('%Y-%m-%d %H:%M:%S'),
        'status': order.status,
        'handler': order.handler,
        'handle_time': order.handle_time.strftime('%Y-%m-%d %H:%M:%S') if order.handle_time else None,
        'handle_result': order.handle_result,
        'repair_duration': order.repair_duration,
        'parts_used': order.parts_used
    }


def convert_maintenance_record(record):
    return {
        'id': record.id,
        'device_code': record.device.device_code,
        'device_name': record.device.device_name,
        'terminal': record.device.terminal,
        'checkin_island': record.device.checkin_island,
        'record_type': record.record_type,
        'work_order_no': record.work_order_no,
        'fault_type': record.fault_type,
        'fault_level': record.fault_level,
        'description': record.description,
        'operator': record.operator,
        'operate_time': record.operate_time.strftime('%Y-%m-%d %H:%M:%S'),
        'duration': record.duration,
        'parts_used': record.parts_used,
        'remark': record.remark
    }


@app.route('/api/devices', methods=['POST'])
def add_device():
    data = request.json
    required_fields = ['device_code', 'device_name', 'location', 'install_date']
    for field in required_fields:
        if field not in data:
            return error_response(f'缺少必填字段: {field}')
    
    if Device.query.filter_by(device_code=data['device_code']).first():
        return error_response('设备编号已存在')
    
    device = Device(
        device_code=data['device_code'],
        device_name=data['device_name'],
        device_model=data.get('device_model'),
        communication_mode=data.get('communication_mode'),
        terminal=data.get('terminal'),
        checkin_island=data.get('checkin_island'),
        location=data['location'],
        install_date=datetime.strptime(data['install_date'], '%Y-%m-%d').date(),
        activation_date=datetime.strptime(data['activation_date'], '%Y-%m-%d').date() if data.get('activation_date') else None,
        status=data.get('status', '正常')
    )
    db.session.add(device)
    db.session.commit()
    
    record = MaintenanceRecord(
        device_id=device.id,
        record_type='设备录入',
        description=f'设备 {device.device_name} 录入系统',
        operator=data.get('operator', '系统管理员')
    )
    db.session.add(record)
    db.session.commit()
    
    return success_response(convert_device(device), '设备录入成功')


@app.route('/api/devices', methods=['GET'])
def get_devices():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    device_model = request.args.get('device_model')
    communication_mode = request.args.get('communication_mode')
    terminal = request.args.get('terminal')
    checkin_island = request.args.get('checkin_island')
    
    query = Device.query
    if status:
        query = query.filter_by(status=status)
    if device_model:
        query = query.filter(Device.device_model.like(f'%{device_model}%'))
    if communication_mode:
        query = query.filter_by(communication_mode=communication_mode)
    if terminal:
        query = query.filter_by(terminal=terminal)
    if checkin_island:
        query = query.filter_by(checkin_island=checkin_island)
    
    query = query.order_by(Device.created_at.desc())
    result = paginate_query(query, page, per_page, convert_device)
    
    return success_response(result, '查询成功')


@app.route('/api/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    device = Device.query.get(device_id)
    if not device:
        return error_response('设备不存在', 404)
    
    return success_response(convert_device(device, include_orders=True), '查询成功')


@app.route('/api/devices/<int:device_id>/status', methods=['PUT'])
def update_device_status(device_id):
    device = Device.query.get(device_id)
    if not device:
        return error_response('设备不存在', 404)
    
    data = request.json
    new_status = data.get('status')
    valid_statuses = ['正常', '故障', '维修中', '已修复']
    
    if new_status not in valid_statuses:
        return error_response(f'无效的状态值，必须是: {", ".join(valid_statuses)}')
    
    old_status = device.status
    device.status = new_status
    db.session.commit()
    
    record = MaintenanceRecord(
        device_id=device.id,
        record_type='状态变更',
        description=f'设备状态从 {old_status} 变更为 {new_status}',
        operator=data.get('operator', '系统管理员')
    )
    db.session.add(record)
    db.session.commit()
    
    return success_response({
        'device_code': device.device_code,
        'device_name': device.device_name,
        'old_status': old_status,
        'new_status': new_status
    }, '设备状态更新成功')


@app.route('/api/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    device = Device.query.get(device_id)
    if not device:
        return error_response('设备不存在', 404)
    
    data = request.json
    
    if data.get('device_code') and data['device_code'] != device.device_code:
        if Device.query.filter_by(device_code=data['device_code']).first():
            return error_response('设备编号已存在')
        device.device_code = data['device_code']
    
    if data.get('device_name'):
        device.device_name = data['device_name']
    if data.get('device_model'):
        device.device_model = data['device_model']
    if data.get('communication_mode'):
        device.communication_mode = data['communication_mode']
    if 'terminal' in data:
        device.terminal = data['terminal']
    if 'checkin_island' in data:
        device.checkin_island = data['checkin_island']
    if data.get('location'):
        device.location = data['location']
    if data.get('install_date'):
        device.install_date = datetime.strptime(data['install_date'], '%Y-%m-%d').date()
    if data.get('activation_date'):
        device.activation_date = datetime.strptime(data['activation_date'], '%Y-%m-%d').date()
    
    db.session.commit()
    
    return success_response(convert_device(device), '设备信息更新成功')


@app.route('/api/work-orders', methods=['POST'])
def report_fault():
    data = request.json
    required_fields = ['device_code', 'fault_description', 'reporter']
    for field in required_fields:
        if field not in data:
            return error_response(f'缺少必填字段: {field}')
    
    device = Device.query.filter_by(device_code=data['device_code']).first()
    if not device:
        return error_response('设备不存在', 404)
    
    valid_fault_types = ['硬件故障', '软件故障', '通信故障', '机械故障', '传感器故障', '电源故障', '其他']
    valid_priorities = ['紧急', '高', '普通', '低']
    valid_fault_levels = ['轻微', '一般', '严重', '致命']
    
    fault_type = data.get('fault_type', '其他')
    priority = data.get('priority', '普通')
    fault_level = data.get('fault_level', '一般')
    
    if fault_type not in valid_fault_types:
        return error_response(f'无效的故障类型，必须是: {", ".join(valid_fault_types)}')
    
    if priority not in valid_priorities:
        return error_response(f'无效的优先级，必须是: {", ".join(valid_priorities)}')
    
    if fault_level not in valid_fault_levels:
        return error_response(f'无效的故障等级，必须是: {", ".join(valid_fault_levels)}')
    
    order_no = generate_order_no()
    work_order = WorkOrder(
        order_no=order_no,
        device_id=device.id,
        fault_type=fault_type,
        fault_level=fault_level,
        priority=priority,
        fault_description=data['fault_description'],
        reporter=data['reporter']
    )
    db.session.add(work_order)
    
    device.status = '故障'
    db.session.commit()
    
    record = MaintenanceRecord(
        device_id=device.id,
        record_type='故障上报',
        work_order_no=order_no,
        fault_type=fault_type,
        fault_level=fault_level,
        description=f'[{priority}] {fault_type} ({fault_level}): {data["fault_description"]}',
        operator=data['reporter']
    )
    db.session.add(record)
    db.session.commit()
    
    return success_response(convert_work_order(work_order), '故障上报成功')


@app.route('/api/work-orders', methods=['GET'])
def get_work_orders():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    fault_type = request.args.get('fault_type')
    priority = request.args.get('priority')
    fault_level = request.args.get('fault_level')
    terminal = request.args.get('terminal')
    checkin_island = request.args.get('checkin_island')
    device_code = request.args.get('device_code')
    
    query = WorkOrder.query.join(Device)
    
    if status:
        query = query.filter(WorkOrder.status == status)
    if fault_type:
        query = query.filter(WorkOrder.fault_type == fault_type)
    if priority:
        query = query.filter(WorkOrder.priority == priority)
    if fault_level:
        query = query.filter(WorkOrder.fault_level == fault_level)
    if terminal:
        query = query.filter(Device.terminal == terminal)
    if checkin_island:
        query = query.filter(Device.checkin_island == checkin_island)
    if device_code:
        query = query.filter(Device.device_code.like(f'%{device_code}%'))
    
    query = query.order_by(
        db.case(
            (WorkOrder.priority == '紧急', 1),
            (WorkOrder.priority == '高', 2),
            (WorkOrder.priority == '普通', 3),
            (WorkOrder.priority == '低', 4),
            else_=5
        ),
        WorkOrder.report_time.desc()
    )
    
    result = paginate_query(query, page, per_page, convert_work_order)
    
    return success_response(result, '查询成功')


@app.route('/api/work-orders/<order_no>', methods=['GET'])
def get_work_order(order_no):
    work_order = WorkOrder.query.filter_by(order_no=order_no).first()
    if not work_order:
        return error_response('工单不存在', 404)
    
    return success_response(convert_work_order(work_order), '查询成功')


@app.route('/api/work-orders/<order_no>/handle', methods=['PUT'])
def handle_work_order(order_no):
    work_order = WorkOrder.query.filter_by(order_no=order_no).first()
    if not work_order:
        return error_response('工单不存在', 404)
    
    data = request.json
    handler = data.get('handler')
    handle_result = data.get('handle_result')
    action = data.get('action', '处理')
    duration = data.get('duration', 0)
    parts_used = data.get('parts_used')
    
    if not handler or not handle_result:
        return error_response('处理人和处理结果不能为空')
    
    work_order.handler = handler
    work_order.handle_time = datetime.now()
    work_order.handle_result = handle_result
    work_order.repair_duration = duration
    work_order.parts_used = parts_used
    
    if action == '开始维修':
        work_order.status = '处理中'
        work_order.device.status = '维修中'
    elif action == '修复完成':
        work_order.status = '已完成'
        work_order.device.status = '已修复'
    
    db.session.commit()
    
    record = MaintenanceRecord(
        device_id=work_order.device_id,
        record_type='运维处理',
        work_order_no=order_no,
        fault_type=work_order.fault_type,
        fault_level=work_order.fault_level,
        description=f'工单 {order_no} 处理: {handle_result}',
        operator=handler,
        duration=duration,
        parts_used=parts_used
    )
    db.session.add(record)
    db.session.commit()
    
    return success_response({
        'order_no': work_order.order_no,
        'status': work_order.status,
        'handler': work_order.handler,
        'handle_time': work_order.handle_time.strftime('%Y-%m-%d %H:%M:%S'),
        'device_status': work_order.device.status
    }, '工单处理成功')


@app.route('/api/maintenance-records', methods=['GET'])
def get_maintenance_records():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    device_code = request.args.get('device_code')
    record_type = request.args.get('record_type')
    fault_type = request.args.get('fault_type')
    fault_level = request.args.get('fault_level')
    terminal = request.args.get('terminal')
    checkin_island = request.args.get('checkin_island')
    
    query = MaintenanceRecord.query.join(Device)
    
    if device_code:
        query = query.filter(Device.device_code.like(f'%{device_code}%'))
    if record_type:
        query = query.filter(MaintenanceRecord.record_type == record_type)
    if fault_type:
        query = query.filter(MaintenanceRecord.fault_type == fault_type)
    if fault_level:
        query = query.filter(MaintenanceRecord.fault_level == fault_level)
    if terminal:
        query = query.filter(Device.terminal == terminal)
    if checkin_island:
        query = query.filter(Device.checkin_island == checkin_island)
    
    query = query.order_by(MaintenanceRecord.operate_time.desc())
    result = paginate_query(query, page, per_page, convert_maintenance_record)
    
    return success_response(result, '查询成功')


@app.route('/api/dashboard/statistics', methods=['GET'])
def get_statistics():
    total_devices = Device.query.count()
    normal_devices = Device.query.filter_by(status='正常').count()
    fault_devices = Device.query.filter_by(status='故障').count()
    repairing_devices = Device.query.filter_by(status='维修中').count()
    repaired_devices = Device.query.filter_by(status='已修复').count()
    
    availability_rate = round((normal_devices + repaired_devices) / total_devices * 100, 2) if total_devices > 0 else 0
    
    pending_orders = WorkOrder.query.filter_by(status='待处理').count()
    processing_orders = WorkOrder.query.filter_by(status='处理中').count()
    completed_orders = WorkOrder.query.filter_by(status='已完成').count()
    
    urgent_orders = WorkOrder.query.filter_by(priority='紧急', status='待处理').count()
    high_priority_orders = WorkOrder.query.filter_by(priority='高', status='待处理').count()
    
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
    today_orders = WorkOrder.query.filter(WorkOrder.report_time >= today_start, WorkOrder.report_time <= today_end).count()
    today_completed = WorkOrder.query.filter(WorkOrder.handle_time >= today_start, WorkOrder.handle_time <= today_end).count()
    
    total_maintenance = MaintenanceRecord.query.count()
    avg_repair_duration = db.session.query(db.func.avg(WorkOrder.repair_duration)).filter(WorkOrder.status == '已完成').scalar() or 0
    
    fault_type_stats = {
        '硬件故障': WorkOrder.query.filter_by(fault_type='硬件故障').count(),
        '软件故障': WorkOrder.query.filter_by(fault_type='软件故障').count(),
        '通信故障': WorkOrder.query.filter_by(fault_type='通信故障').count(),
        '机械故障': WorkOrder.query.filter_by(fault_type='机械故障').count(),
        '传感器故障': WorkOrder.query.filter_by(fault_type='传感器故障').count(),
        '电源故障': WorkOrder.query.filter_by(fault_type='电源故障').count(),
        '其他': WorkOrder.query.filter_by(fault_type='其他').count()
    }
    
    terminals = db.session.query(Device.terminal).filter(Device.terminal.isnot(None)).distinct().all()
    terminal_stats = {}
    for (terminal,) in terminals:
        term_devices = Device.query.filter_by(terminal=terminal).count()
        term_normal = Device.query.filter_by(terminal=terminal, status='正常').count()
        term_repaired = Device.query.filter_by(terminal=terminal, status='已修复').count()
        term_rate = round((term_normal + term_repaired) / term_devices * 100, 2) if term_devices > 0 else 0
        terminal_stats[terminal] = {
            'total': term_devices,
            'normal': term_normal,
            'availability_rate': term_rate
        }
    
    return success_response({
        'device_statistics': {
            'total': total_devices,
            'normal': normal_devices,
            'fault': fault_devices,
            'repairing': repairing_devices,
            'repaired': repaired_devices,
            'availability_rate': availability_rate
        },
        'work_order_statistics': {
            'pending': pending_orders,
            'processing': processing_orders,
            'completed': completed_orders,
            'urgent_pending': urgent_orders,
            'high_priority_pending': high_priority_orders,
            'today_reported': today_orders,
            'today_completed': today_completed
        },
        'maintenance_statistics': {
            'total_records': total_maintenance,
            'avg_repair_duration': round(avg_repair_duration, 2)
        },
        'fault_type_statistics': fault_type_stats,
        'terminal_statistics': terminal_stats
    }, '查询成功')


@app.route('/api/devices/availability-rate', methods=['GET'])
def get_availability_rate():
    terminal = request.args.get('terminal')
    checkin_island = request.args.get('checkin_island')
    
    query = Device.query
    if terminal:
        query = query.filter_by(terminal=terminal)
    if checkin_island:
        query = query.filter_by(checkin_island=checkin_island)
    
    total = query.count()
    normal = query.filter(Device.status.in_(['正常', '已修复'])).count()
    rate = round(normal / total * 100, 2) if total > 0 else 0
    
    return success_response({
        'total_devices': total,
        'available_devices': normal,
        'availability_rate': rate,
        'terminal': terminal,
        'checkin_island': checkin_island
    }, '查询成功')


@app.errorhandler(404)
def not_found(error):
    return error_response('接口不存在', 404)


@app.errorhandler(500)
def internal_error(error):
    return error_response('服务器内部错误', 500)


with app.app_context():
    db.create_all()
    print('数据库初始化完成！')

if __name__ == '__main__':
    print('=' * 70)
    print('机场自助行李托运机运维管理系统 v3.0 - 后端服务')
    print('=' * 70)
    print('新增功能:')
    print('  - 设备模块: 航站楼、值机岛字段')
    print('  - 故障模块: 故障等级字段')
    print('  - 设备工单联动: 设备详情关联工单列表')
    print('  - 维修日志增强: 工时、更换配件等字段')
    print('  - 多维度筛选: 航站楼、值机岛、故障等级')
    print('  - 统一接口格式: 标准响应格式、分页封装')
    print('  - 设备完好率统计: 全局、按航站楼统计')
    print('=' * 70)
    print('API 接口列表:')
    print('  POST /api/devices - 设备录入')
    print('  GET  /api/devices - 设备列表查询（支持多维度筛选）')
    print('  GET  /api/devices/<id> - 设备详情（含关联工单）')
    print('  PUT  /api/devices/<id> - 更新设备信息')
    print('  PUT  /api/devices/<id>/status - 更新设备状态')
    print('  POST /api/work-orders - 故障上报（含故障等级）')
    print('  GET  /api/work-orders - 工单列表查询（按优先级排序）')
    print('  GET  /api/work-orders/<order_no> - 工单详情')
    print('  PUT  /api/work-orders/<order_no>/handle - 处理工单')
    print('  GET  /api/maintenance-records - 运维记录查询')
    print('  GET  /api/dashboard/statistics - 综合统计数据')
    print('  GET  /api/devices/availability-rate - 设备完好率统计')
    print('=' * 70)
    app.run(debug=True, host='0.0.0.0', port=5000)
