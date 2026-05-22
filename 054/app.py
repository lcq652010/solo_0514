from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cinema_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

DEVICE_TYPE_CHOICES = ['ticket_machine', 'checkin_machine', 'vending_machine', 'advertising_display']
COMMUNICATION_TYPE_CHOICES = ['ethernet', 'wifi', '4g', '5g', 'bluetooth']
AREA_CHOICES = ['hall_1', 'hall_2', 'hall_3', 'hall_4', 'hall_5', 'lobby', 'entrance', 'other']

def success_response(data=None, message='操作成功', code=200):
    response = {
        'code': code,
        'message': message,
        'success': True,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), code

def error_response(message='操作失败', code=400, errors=None):
    response = {
        'code': code,
        'message': message,
        'success': False,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    if errors is not None:
        response['errors'] = errors
    return jsonify(response), code

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_code = db.Column(db.String(50), unique=True, nullable=False)
    device_name = db.Column(db.String(100), nullable=False)
    device_model = db.Column(db.String(100))
    device_type = db.Column(db.String(50), nullable=False)
    communication_type = db.Column(db.String(50))
    area = db.Column(db.String(50))
    location = db.Column(db.String(100), nullable=False)
    commission_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='normal')
    install_date = db.Column(db.DateTime, default=datetime.now)
    last_maintenance = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'device_code': self.device_code,
            'device_name': self.device_name,
            'device_model': self.device_model,
            'device_type': self.device_type,
            'communication_type': self.communication_type,
            'area': self.area,
            'location': self.location,
            'commission_date': self.commission_date.strftime('%Y-%m-%d') if self.commission_date else None,
            'status': self.status,
            'install_date': self.install_date.strftime('%Y-%m-%d %H:%M:%S') if self.install_date else None,
            'last_maintenance': self.last_maintenance.strftime('%Y-%m-%d %H:%M:%S') if self.last_maintenance else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

FAULT_CATEGORY_CHOICES = ['hardware', 'software', 'network', 'mechanical', 'power', 'other']
PRIORITY_CHOICES = ['low', 'medium', 'high', 'urgent']

class WorkOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(50), unique=True, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    device = db.relationship('Device', backref=db.backref('work_orders', lazy=True))
    fault_category = db.Column(db.String(50), nullable=False)
    fault_type = db.Column(db.String(100), nullable=False)
    fault_description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='medium')
    impact_description = db.Column(db.Text)
    reporter = db.Column(db.String(50), nullable=False)
    report_time = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(20), default='pending')
    handler = db.Column(db.String(50))
    handle_time = db.Column(db.DateTime)
    handle_result = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        device = Device.query.get(self.device_id)
        return {
            'id': self.id,
            'order_no': self.order_no,
            'device_id': self.device_id,
            'device_code': device.device_code if device else None,
            'device_name': device.device_name if device else None,
            'area': device.area if device else None,
            'location': device.location if device else None,
            'fault_category': self.fault_category,
            'fault_type': self.fault_type,
            'fault_description': self.fault_description,
            'priority': self.priority,
            'impact_description': self.impact_description,
            'reporter': self.reporter,
            'report_time': self.report_time.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self.status,
            'handler': self.handler,
            'handle_time': self.handle_time.strftime('%Y-%m-%d %H:%M:%S') if self.handle_time else None,
            'handle_result': self.handle_result,
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
    description = db.Column(db.Text, nullable=False)
    operator = db.Column(db.String(50), nullable=False)
    maintenance_time = db.Column(db.DateTime, default=datetime.now)
    result = db.Column(db.String(20), nullable=False)
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        device = Device.query.get(self.device_id)
        return {
            'id': self.id,
            'device_id': self.device_id,
            'device_code': device.device_code if device else None,
            'device_name': device.device_name if device else None,
            'area': device.area if device else None,
            'work_order_id': self.work_order_id,
            'maintenance_type': self.maintenance_type,
            'description': self.description,
            'operator': self.operator,
            'maintenance_time': self.maintenance_time.strftime('%Y-%m-%d %H:%M:%S'),
            'result': self.result,
            'remarks': self.remarks,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

def generate_order_no():
    today = datetime.now().strftime('%Y%m%d')
    prefix = f'WO{today}'
    last_order = WorkOrder.query.filter(WorkOrder.order_no.like(f'{prefix}%')).order_by(WorkOrder.order_no.desc()).first()
    if last_order:
        last_num = int(last_order.order_no[-4:])
        new_num = str(last_num + 1).zfill(4)
    else:
        new_num = '0001'
    return f'{prefix}{new_num}'

@app.route('/api/devices', methods=['POST'])
def add_device():
    data = request.get_json()
    if not data or 'device_code' not in data or 'device_name' not in data:
        return error_response('缺少必要参数：device_code, device_name')
    
    if Device.query.filter_by(device_code=data['device_code']).first():
        return error_response('设备编号已存在')
    
    commission_date = None
    if data.get('commission_date'):
        try:
            commission_date = datetime.strptime(data['commission_date'], '%Y-%m-%d')
        except:
            return error_response('投用日期格式错误，应为 YYYY-MM-DD')
    
    device = Device(
        device_code=data['device_code'],
        device_name=data['device_name'],
        device_model=data.get('device_model', ''),
        device_type=data.get('device_type', ''),
        communication_type=data.get('communication_type', ''),
        area=data.get('area', ''),
        location=data.get('location', ''),
        commission_date=commission_date,
        status=data.get('status', 'normal')
    )
    db.session.add(device)
    db.session.commit()
    return success_response({'device': device.to_dict()}, '设备添加成功', 201)

@app.route('/api/devices', methods=['GET'])
def get_devices():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    device_type = request.args.get('device_type')
    area = request.args.get('area')
    
    query = Device.query
    if status:
        query = query.filter_by(status=status)
    if device_type:
        query = query.filter_by(device_type=device_type)
    if area:
        query = query.filter_by(area=area)
    
    pagination = query.order_by(Device.created_at.desc()).paginate(page=page, per_page=per_page)
    devices = [d.to_dict() for d in pagination.items]
    
    return success_response({
        'list': devices,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }, '获取设备列表成功')

@app.route('/api/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    device = Device.query.get_or_404(device_id)
    return success_response({'device': device.to_dict()}, '获取设备详情成功')

@app.route('/api/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    device = Device.query.get_or_404(device_id)
    data = request.get_json()
    
    if 'device_name' in data:
        device.device_name = data['device_name']
    if 'device_model' in data:
        device.device_model = data['device_model']
    if 'device_type' in data:
        device.device_type = data['device_type']
    if 'communication_type' in data:
        device.communication_type = data['communication_type']
    if 'area' in data:
        device.area = data['area']
    if 'location' in data:
        device.location = data['location']
    if 'commission_date' in data:
        try:
            device.commission_date = datetime.strptime(data['commission_date'], '%Y-%m-%d')
        except:
            return error_response('投用日期格式错误，应为 YYYY-MM-DD')
    if 'status' in data:
        if data['status'] not in ['normal', 'fault', 'repairing', 'repaired']:
            return error_response('无效的状态值')
        device.status = data['status']
    
    db.session.commit()
    return success_response({'device': device.to_dict()}, '设备更新成功')

@app.route('/api/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    device = Device.query.get_or_404(device_id)
    db.session.delete(device)
    db.session.commit()
    return success_response(None, '设备删除成功')

@app.route('/api/workorders', methods=['POST'])
def create_workorder():
    data = request.get_json()
    if not data or 'device_id' not in data or 'fault_category' not in data or 'fault_type' not in data or 'fault_description' not in data or 'reporter' not in data:
        return error_response('缺少必要参数：device_id, fault_category, fault_type, fault_description, reporter')
    
    if data['fault_category'] not in FAULT_CATEGORY_CHOICES:
        return error_response(f'无效的故障分类，可选值: {FAULT_CATEGORY_CHOICES}')
    
    if data.get('priority') and data['priority'] not in PRIORITY_CHOICES:
        return error_response(f'无效的优先级，可选值: {PRIORITY_CHOICES}')
    
    device = Device.query.get(data['device_id'])
    if not device:
        return error_response('设备不存在', 404)
    
    order_no = generate_order_no()
    work_order = WorkOrder(
        order_no=order_no,
        device_id=data['device_id'],
        fault_category=data['fault_category'],
        fault_type=data['fault_type'],
        fault_description=data['fault_description'],
        priority=data.get('priority', 'medium'),
        impact_description=data.get('impact_description', ''),
        reporter=data['reporter'],
        status='pending'
    )
    
    device.status = 'fault'
    
    db.session.add(work_order)
    db.session.commit()
    return success_response({'work_order': work_order.to_dict()}, '工单创建成功', 201)

@app.route('/api/workorders', methods=['GET'])
def get_workorders():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    device_id = request.args.get('device_id', type=int)
    fault_category = request.args.get('fault_category')
    priority = request.args.get('priority')
    area = request.args.get('area')
    
    query = WorkOrder.query
    if status:
        query = query.filter_by(status=status)
    if device_id:
        query = query.filter_by(device_id=device_id)
    if fault_category:
        query = query.filter_by(fault_category=fault_category)
    if priority:
        query = query.filter_by(priority=priority)
    if area:
        query = query.join(Device).filter(Device.area == area)
    
    pagination = query.order_by(
        db.case(
            (WorkOrder.priority == 'urgent', 1),
            (WorkOrder.priority == 'high', 2),
            (WorkOrder.priority == 'medium', 3),
            (WorkOrder.priority == 'low', 4),
            else_=5
        ),
        WorkOrder.created_at.desc()
    ).paginate(page=page, per_page=per_page)
    work_orders = [w.to_dict() for w in pagination.items]
    
    return success_response({
        'list': work_orders,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }, '获取工单列表成功')

@app.route('/api/workorders/<int:order_id>', methods=['GET'])
def get_workorder(order_id):
    work_order = WorkOrder.query.get_or_404(order_id)
    return success_response({'work_order': work_order.to_dict()}, '获取工单详情成功')

@app.route('/api/workorders/<int:order_id>/handle', methods=['PUT'])
def handle_workorder(order_id):
    work_order = WorkOrder.query.get_or_404(order_id)
    data = request.get_json()
    
    if not data or 'handler' not in data or 'action' not in data:
        return error_response('缺少必要参数：handler, action')
    
    device = Device.query.get(work_order.device_id)
    
    if data['action'] == 'start_repair':
        work_order.status = 'processing'
        work_order.handler = data['handler']
        work_order.handle_time = datetime.now()
        device.status = 'repairing'
    
    elif data['action'] == 'complete':
        if 'handle_result' not in data:
            return error_response('请填写处理结果')
        work_order.status = 'completed'
        work_order.handle_result = data['handle_result']
        work_order.handle_time = datetime.now()
        device.status = 'repaired'
        
        record = MaintenanceRecord(
            device_id=work_order.device_id,
            work_order_id=work_order.id,
            maintenance_type='故障维修',
            description=work_order.fault_description,
            operator=data['handler'],
            result='成功',
            remarks=data['handle_result']
        )
        db.session.add(record)
    
    else:
        return error_response('无效的操作')
    
    db.session.commit()
    return success_response({'work_order': work_order.to_dict()}, '工单处理成功')

@app.route('/api/maintenance', methods=['GET'])
def get_maintenance_records():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    device_id = request.args.get('device_id', type=int)
    work_order_id = request.args.get('work_order_id', type=int)
    area = request.args.get('area')
    
    query = MaintenanceRecord.query
    if device_id:
        query = query.filter_by(device_id=device_id)
    if work_order_id:
        query = query.filter_by(work_order_id=work_order_id)
    if area:
        query = query.join(Device).filter(Device.area == area)
    
    pagination = query.order_by(MaintenanceRecord.created_at.desc()).paginate(page=page, per_page=per_page)
    records = [r.to_dict() for r in pagination.items]
    
    return success_response({
        'list': records,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }, '获取运维记录列表成功')

@app.route('/api/maintenance', methods=['POST'])
def add_maintenance_record():
    data = request.get_json()
    if not data or 'device_id' not in data or 'maintenance_type' not in data or 'description' not in data or 'operator' not in data or 'result' not in data:
        return error_response('缺少必要参数：device_id, maintenance_type, description, operator, result')
    
    device = Device.query.get(data['device_id'])
    if not device:
        return error_response('设备不存在', 404)
    
    record = MaintenanceRecord(
        device_id=data['device_id'],
        work_order_id=data.get('work_order_id'),
        maintenance_type=data['maintenance_type'],
        description=data['description'],
        operator=data['operator'],
        result=data['result'],
        remarks=data.get('remarks', '')
    )
    
    device.last_maintenance = datetime.now()
    
    db.session.add(record)
    db.session.commit()
    return success_response({'record': record.to_dict()}, '运维记录添加成功', 201)

@app.route('/api/config/constants', methods=['GET'])
def get_constants():
    return success_response({
        'device_type_choices': DEVICE_TYPE_CHOICES,
        'communication_type_choices': COMMUNICATION_TYPE_CHOICES,
        'fault_category_choices': FAULT_CATEGORY_CHOICES,
        'priority_choices': PRIORITY_CHOICES,
        'area_choices': AREA_CHOICES,
        'device_status_choices': ['normal', 'fault', 'repairing', 'repaired'],
        'work_order_status_choices': ['pending', 'processing', 'completed']
    }, '获取系统常量配置成功')

@app.route('/api/dashboard/health-rate', methods=['GET'])
def get_device_health_rate():
    area = request.args.get('area')
    
    query = Device.query
    if area:
        query = query.filter_by(area=area)
    
    total_devices = query.count()
    normal_devices = query.filter_by(status='normal').count()
    repaired_devices = query.filter_by(status='repaired').count()
    
    health_rate = 0
    if total_devices > 0:
        health_rate = round(((normal_devices + repaired_devices) / total_devices) * 100, 2)
    
    return success_response({
        'total_devices': total_devices,
        'normal_devices': normal_devices,
        'repaired_devices': repaired_devices,
        'health_rate': health_rate,
        'area': area
    }, '获取设备完好率成功')

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    area = request.args.get('area')
    
    device_query = Device.query
    order_query = WorkOrder.query
    
    if area:
        device_query = device_query.filter_by(area=area)
        order_query = order_query.join(Device).filter(Device.area == area)
    
    total_devices = device_query.count()
    normal_devices = device_query.filter_by(status='normal').count()
    fault_devices = device_query.filter_by(status='fault').count()
    repairing_devices = device_query.filter_by(status='repairing').count()
    pending_orders = order_query.filter(WorkOrder.status == 'pending').count()
    processing_orders = order_query.filter(WorkOrder.status == 'processing').count()
    total_orders = order_query.count()
    
    urgent_orders = order_query.filter(WorkOrder.priority == 'urgent', WorkOrder.status == 'pending').count()
    high_orders = order_query.filter(WorkOrder.priority == 'high', WorkOrder.status == 'pending').count()
    
    health_rate = 0
    if total_devices > 0:
        health_rate = round(((normal_devices + (device_query.filter_by(status='repaired').count())) / total_devices) * 100, 2)
    
    return success_response({
        'total_devices': total_devices,
        'normal_devices': normal_devices,
        'fault_devices': fault_devices,
        'repairing_devices': repairing_devices,
        'pending_orders': pending_orders,
        'processing_orders': processing_orders,
        'total_orders': total_orders,
        'urgent_pending_orders': urgent_orders,
        'high_pending_orders': high_orders,
        'health_rate': health_rate,
        'area': area
    }, '获取仪表盘统计数据成功')

@app.errorhandler(404)
def not_found(error):
    return error_response('资源不存在', 404)

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return error_response('服务器内部错误', 500)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
