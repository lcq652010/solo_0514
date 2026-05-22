from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///water_meter.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_code = db.Column(db.String(50), unique=True, nullable=False)
    device_name = db.Column(db.String(100), nullable=False)
    device_model = db.Column(db.String(100))
    communication_mode = db.Column(db.String(50))
    area = db.Column(db.String(100))
    pipeline = db.Column(db.String(100))
    install_location = db.Column(db.String(200))
    install_date = db.Column(db.Date)
    commissioning_date = db.Column(db.Date)
    last_upload_time = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='normal')
    last_maintenance_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'device_code': self.device_code,
            'device_name': self.device_name,
            'device_model': self.device_model,
            'communication_mode': self.communication_mode,
            'area': self.area,
            'pipeline': self.pipeline,
            'install_location': self.install_location,
            'install_date': self.install_date.strftime('%Y-%m-%d') if self.install_date else None,
            'commissioning_date': self.commissioning_date.strftime('%Y-%m-%d') if self.commissioning_date else None,
            'last_upload_time': self.last_upload_time.strftime('%Y-%m-%d %H:%M:%S') if self.last_upload_time else None,
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


class Fault(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_order_no = db.Column(db.String(50), unique=True, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    fault_type = db.Column(db.String(50), nullable=False)
    fault_category = db.Column(db.String(50), default='device')
    priority = db.Column(db.String(20), default='medium')
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
            'area': self.device.area if self.device else None,
            'pipeline': self.device.pipeline if self.device else None,
            'fault_type': self.fault_type,
            'fault_category': self.fault_category,
            'fault_category_text': self.get_fault_category_text(),
            'priority': self.priority,
            'priority_text': self.get_priority_text(),
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

    def get_fault_category_text(self):
        category_map = {
            'device': '设备故障',
            'sensor': '传感器异常',
            'communication': '通信故障',
            'power': '电源故障',
            'software': '软件异常',
            'other': '其他故障'
        }
        return category_map.get(self.fault_category, '未知分类')

    def get_priority_text(self):
        priority_map = {
            'high': '紧急',
            'medium': '一般',
            'low': '低'
        }
        return priority_map.get(self.priority, '未知')

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
            'area': self.device.area if self.device else None,
            'pipeline': self.device.pipeline if self.device else None,
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


def api_response(code=200, message='success', data=None, **kwargs):
    response = {
        'code': code,
        'message': message,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    if data is not None:
        response['data'] = data
    response.update(kwargs)
    return jsonify(response), code


@app.route('/')
def index():
    return api_response(200, '智能水表远程采集终端运维管理系统 API', {
        'endpoints': {
            'devices': '/api/devices',
            'faults': '/api/faults',
            'maintenance': '/api/maintenance',
            'statistics': '/api/statistics'
        }
    })


@app.route('/api/devices', methods=['GET'])
def get_devices():
    area = request.args.get('area')
    pipeline = request.args.get('pipeline')
    status = request.args.get('status')
    communication_mode = request.args.get('communication_mode')

    query = Device.query

    if area:
        query = query.filter(Device.area.like(f'%{area}%'))
    if pipeline:
        query = query.filter(Device.pipeline.like(f'%{pipeline}%'))
    if status:
        query = query.filter_by(status=status)
    if communication_mode:
        query = query.filter_by(communication_mode=communication_mode)

    devices = query.all()
    return api_response(200, 'success', [device.to_dict() for device in devices], total=len(devices))


@app.route('/api/devices', methods=['POST'])
def create_device():
    data = request.get_json()
    if not data:
        return api_response(400, '无数据提供')

    required_fields = ['device_code', 'device_name']
    for field in required_fields:
        if field not in data:
            return api_response(400, f'缺少必填字段: {field}')

    existing_device = Device.query.filter_by(device_code=data['device_code']).first()
    if existing_device:
        return api_response(400, '设备编号已存在')

    device = Device(
        device_code=data['device_code'],
        device_name=data['device_name'],
        device_model=data.get('device_model'),
        communication_mode=data.get('communication_mode'),
        area=data.get('area'),
        pipeline=data.get('pipeline'),
        install_location=data.get('install_location'),
        status=data.get('status', 'normal')
    )

    if 'install_date' in data and data['install_date']:
        try:
            device.install_date = datetime.strptime(data['install_date'], '%Y-%m-%d').date()
        except ValueError:
            return api_response(400, '安装日期格式错误，请使用YYYY-MM-DD')

    if 'commissioning_date' in data and data['commissioning_date']:
        try:
            device.commissioning_date = datetime.strptime(data['commissioning_date'], '%Y-%m-%d').date()
        except ValueError:
            return api_response(400, '投用日期格式错误，请使用YYYY-MM-DD')

    db.session.add(device)
    db.session.commit()

    return api_response(201, '设备录入成功', device.to_dict())


@app.route('/api/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    device = Device.query.get(device_id)
    if not device:
        return api_response(404, '设备不存在')

    return api_response(200, 'success', device.to_dict())


@app.route('/api/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    device = Device.query.get(device_id)
    if not device:
        return api_response(404, '设备不存在')

    data = request.get_json()
    if not data:
        return api_response(400, '无数据提供')

    if 'device_code' in data:
        existing_device = Device.query.filter(
            Device.device_code == data['device_code'],
            Device.id != device_id
        ).first()
        if existing_device:
            return api_response(400, '设备编号已存在')
        device.device_code = data['device_code']

    if 'device_name' in data:
        device.device_name = data['device_name']
    if 'device_model' in data:
        device.device_model = data['device_model']
    if 'communication_mode' in data:
        device.communication_mode = data['communication_mode']
    if 'area' in data:
        device.area = data['area']
    if 'pipeline' in data:
        device.pipeline = data['pipeline']
    if 'install_location' in data:
        device.install_location = data['install_location']
    if 'status' in data:
        valid_statuses = ['normal', 'fault', 'repairing', 'fixed']
        if data['status'] not in valid_statuses:
            return api_response(400, '无效的设备状态')
        device.status = data['status']
    if 'install_date' in data:
        if data['install_date']:
            try:
                device.install_date = datetime.strptime(data['install_date'], '%Y-%m-%d').date()
            except ValueError:
                return api_response(400, '安装日期格式错误，请使用YYYY-MM-DD')
        else:
            device.install_date = None
    if 'commissioning_date' in data:
        if data['commissioning_date']:
            try:
                device.commissioning_date = datetime.strptime(data['commissioning_date'], '%Y-%m-%d').date()
            except ValueError:
                return api_response(400, '投用日期格式错误，请使用YYYY-MM-DD')
        else:
            device.commissioning_date = None

    db.session.commit()

    return api_response(200, '设备更新成功', device.to_dict())


@app.route('/api/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    device = Device.query.get(device_id)
    if not device:
        return api_response(404, '设备不存在')

    db.session.delete(device)
    db.session.commit()

    return api_response(200, '设备删除成功')


@app.route('/api/faults', methods=['GET'])
def get_faults():
    area = request.args.get('area')
    pipeline = request.args.get('pipeline')
    fault_category = request.args.get('category')
    priority = request.args.get('priority')
    status = request.args.get('status')

    query = Fault.query.join(Device)

    if area:
        query = query.filter(Device.area.like(f'%{area}%'))
    if pipeline:
        query = query.filter(Device.pipeline.like(f'%{pipeline}%'))
    if fault_category:
        query = query.filter(Fault.fault_category == fault_category)
    if priority:
        query = query.filter(Fault.priority == priority)
    if status:
        query = query.filter(Fault.status == status)

    faults = query.order_by(Fault.priority.desc(), Fault.created_at.desc()).all()
    return api_response(200, 'success', [fault.to_dict() for fault in faults], total=len(faults))


@app.route('/api/faults', methods=['POST'])
def create_fault():
    data = request.get_json()
    if not data:
        return api_response(400, '无数据提供')

    required_fields = ['device_id', 'fault_type', 'fault_desc']
    for field in required_fields:
        if field not in data:
            return api_response(400, f'缺少必填字段: {field}')

    device = Device.query.get(data['device_id'])
    if not device:
        return api_response(404, '设备不存在')

    valid_categories = ['device', 'sensor', 'communication', 'power', 'software', 'other']
    fault_category = data.get('fault_category', 'device')
    if fault_category not in valid_categories:
        return api_response(400, '无效的故障分类')

    valid_priorities = ['high', 'medium', 'low']
    priority = data.get('priority', 'medium')
    if priority not in valid_priorities:
        return api_response(400, '无效的优先级')

    fault = Fault(
        work_order_no=Fault.generate_work_order_no(),
        device_id=data['device_id'],
        fault_type=data['fault_type'],
        fault_category=fault_category,
        priority=priority,
        fault_desc=data['fault_desc'],
        reporter=data.get('reporter', '匿名'),
        status='pending'
    )

    device.status = 'fault'

    db.session.add(fault)
    db.session.commit()

    return api_response(201, '故障上报成功', fault.to_dict())


@app.route('/api/faults/<int:fault_id>', methods=['GET'])
def get_fault(fault_id):
    fault = Fault.query.get(fault_id)
    if not fault:
        return api_response(404, '工单不存在')

    return api_response(200, 'success', fault.to_dict())


@app.route('/api/faults/<int:fault_id>', methods=['DELETE'])
def delete_fault(fault_id):
    fault = Fault.query.get(fault_id)
    if not fault:
        return api_response(404, '工单不存在')

    db.session.delete(fault)
    db.session.commit()

    return api_response(200, '工单删除成功')


@app.route('/api/faults/<int:fault_id>/handle', methods=['POST'])
def handle_fault(fault_id):
    fault = Fault.query.get(fault_id)
    if not fault:
        return api_response(404, '工单不存在')

    data = request.get_json()
    if not data:
        return api_response(400, '无数据提供')

    action = data.get('action')
    if not action or action not in ['accept', 'complete']:
        return api_response(400, '无效的操作类型，请使用 accept 或 complete')

    device = Device.query.get(fault.device_id)

    if action == 'accept':
        fault.status = 'processing'
        fault.handler = data.get('handler', '管理员')
        fault.handle_time = datetime.now()
        device.status = 'repairing'

        db.session.commit()

        return api_response(200, '工单已受理', fault.to_dict())

    elif action == 'complete':
        if fault.status != 'processing':
            return api_response(400, '工单当前状态不能标记为完成')

        fault.status = 'completed'
        fault.handle_note = data.get('handle_note', '')
        device.status = 'fixed'

        db.session.commit()

        return api_response(200, '工单已完成，设备状态已更新为已修复', fault.to_dict())

    return api_response(200, '操作成功', fault.to_dict())


@app.route('/api/maintenance', methods=['GET'])
def get_maintenance_records():
    device_id = request.args.get('device_id', type=int)
    area = request.args.get('area')
    pipeline = request.args.get('pipeline')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = MaintenanceRecord.query.join(Device)

    if device_id:
        query = query.filter(MaintenanceRecord.device_id == device_id)
    if area:
        query = query.filter(Device.area.like(f'%{area}%'))
    if pipeline:
        query = query.filter(Device.pipeline.like(f'%{pipeline}%'))
    if start_date:
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(MaintenanceRecord.maintenance_date >= start_dt)
        except ValueError:
            pass
    if end_date:
        try:
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            end_dt = end_dt.replace(hour=23, minute=59, second=59)
            query = query.filter(MaintenanceRecord.maintenance_date <= end_dt)
        except ValueError:
            pass

    records = query.order_by(MaintenanceRecord.maintenance_date.desc()).all()
    return api_response(200, 'success', [record.to_dict() for record in records], total=len(records))


@app.route('/api/maintenance', methods=['POST'])
def create_maintenance_record():
    data = request.get_json()
    if not data:
        return api_response(400, '无数据提供')

    required_fields = ['device_id', 'maintenance_type', 'operator']
    for field in required_fields:
        if field not in data:
            return api_response(400, f'缺少必填字段: {field}')

    device = Device.query.get(data['device_id'])
    if not device:
        return api_response(404, '设备不存在')

    record = MaintenanceRecord(
        device_id=data['device_id'],
        fault_id=data.get('fault_id'),
        maintenance_type=data['maintenance_type'],
        operator=data['operator'],
        maintenance_content=data.get('maintenance_content', ''),
        parts_replaced=data.get('parts_replaced', ''),
        cost=data.get('cost', 0.0),
        notes=data.get('notes', '')
    )

    if 'maintenance_date' in data and data['maintenance_date']:
        try:
            record.maintenance_date = datetime.strptime(data['maintenance_date'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                record.maintenance_date = datetime.strptime(data['maintenance_date'], '%Y-%m-%d')
            except ValueError:
                return api_response(400, '日期格式错误，请使用YYYY-MM-DD或YYYY-MM-DD HH:MM:SS')

    device.last_maintenance_date = record.maintenance_date.date()

    db.session.add(record)
    db.session.commit()

    return api_response(201, '运维记录添加成功', record.to_dict())


@app.route('/api/maintenance/<int:record_id>', methods=['GET'])
def get_maintenance_record(record_id):
    record = MaintenanceRecord.query.get(record_id)
    if not record:
        return api_response(404, '运维记录不存在')

    return api_response(200, 'success', record.to_dict())


@app.route('/api/maintenance/<int:record_id>', methods=['PUT'])
def update_maintenance_record(record_id):
    record = MaintenanceRecord.query.get(record_id)
    if not record:
        return api_response(404, '运维记录不存在')

    data = request.get_json()
    if not data:
        return api_response(400, '无数据提供')

    if 'maintenance_type' in data:
        record.maintenance_type = data['maintenance_type']
    if 'operator' in data:
        record.operator = data['operator']
    if 'maintenance_content' in data:
        record.maintenance_content = data['maintenance_content']
    if 'parts_replaced' in data:
        record.parts_replaced = data['parts_replaced']
    if 'cost' in data:
        record.cost = data['cost']
    if 'notes' in data:
        record.notes = data['notes']

    db.session.commit()

    return api_response(200, '运维记录更新成功', record.to_dict())


@app.route('/api/maintenance/<int:record_id>', methods=['DELETE'])
def delete_maintenance_record(record_id):
    record = MaintenanceRecord.query.get(record_id)
    if not record:
        return api_response(404, '运维记录不存在')

    db.session.delete(record)
    db.session.commit()

    return api_response(200, '运维记录删除成功')


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    area = request.args.get('area')
    pipeline = request.args.get('pipeline')

    device_query = Device.query
    if area:
        device_query = device_query.filter(Device.area.like(f'%{area}%'))
    if pipeline:
        device_query = device_query.filter(Device.pipeline.like(f'%{pipeline}%'))

    total_devices = device_query.count()

    normal_devices = device_query.filter(Device.status == 'normal').count()
    fixed_devices = device_query.filter(Device.status == 'fixed').count()
    healthy_devices = normal_devices + fixed_devices
    device_health_rate = round((healthy_devices / total_devices * 100), 2) if total_devices > 0 else 0

    twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
    online_devices = device_query.filter(Device.last_upload_time >= twenty_four_hours_ago).count()
    upload_success_rate = round((online_devices / total_devices * 100), 2) if total_devices > 0 else 0

    fault_query = Fault.query.join(Device)
    if area:
        fault_query = fault_query.filter(Device.area.like(f'%{area}%'))
    if pipeline:
        fault_query = fault_query.filter(Device.pipeline.like(f'%{pipeline}%'))

    total_faults = fault_query.count()
    pending_faults = fault_query.filter(Fault.status == 'pending').count()
    processing_faults = fault_query.filter(Fault.status == 'processing').count()
    completed_faults = fault_query.filter(Fault.status == 'completed').count()
    high_priority_faults = fault_query.filter(Fault.priority == 'high').count()

    maintenance_query = MaintenanceRecord.query.join(Device)
    if area:
        maintenance_query = maintenance_query.filter(Device.area.like(f'%{area}%'))
    if pipeline:
        maintenance_query = maintenance_query.filter(Device.pipeline.like(f'%{pipeline}%'))

    total_maintenance = maintenance_query.count()

    areas = db.session.query(Device.area).filter(Device.area.isnot(None)).distinct().all()
    area_list = [a[0] for a in areas]

    pipelines = db.session.query(Device.pipeline).filter(Device.pipeline.isnot(None)).distinct().all()
    pipeline_list = [p[0] for p in pipelines]

    area_stats = []
    for a in area_list:
        area_device_count = Device.query.filter_by(area=a).count()
        area_healthy = Device.query.filter(Device.area == a, Device.status.in_(['normal', 'fixed'])).count()
        area_health_rate = round((area_healthy / area_device_count * 100), 2) if area_device_count > 0 else 0
        area_online = Device.query.filter(Device.area == a, Device.last_upload_time >= twenty_four_hours_ago).count()
        area_upload_rate = round((area_online / area_device_count * 100), 2) if area_device_count > 0 else 0
        area_faults = Fault.query.join(Device).filter(Device.area == a).count()
        area_stats.append({
            'area': a,
            'total_devices': area_device_count,
            'device_health_rate': area_health_rate,
            'upload_success_rate': area_upload_rate,
            'total_faults': area_faults
        })

    return api_response(200, '统计数据获取成功', {
        'overview': {
            'total_devices': total_devices,
            'healthy_devices': healthy_devices,
            'device_health_rate': device_health_rate,
            'online_devices': online_devices,
            'upload_success_rate': upload_success_rate,
            'total_faults': total_faults,
            'pending_faults': pending_faults,
            'processing_faults': processing_faults,
            'completed_faults': completed_faults,
            'high_priority_faults': high_priority_faults,
            'total_maintenance': total_maintenance
        },
        'device_status_distribution': {
            'normal': normal_devices,
            'fault': total_devices - healthy_devices,
            'repairing': device_query.filter(Device.status == 'repairing').count(),
            'fixed': fixed_devices
        },
        'areas': area_list,
        'pipelines': pipeline_list,
        'area_statistics': area_stats
    })


@app.route('/api/devices/<int:device_id>/upload', methods=['POST'])
def record_device_upload(device_id):
    device = Device.query.get(device_id)
    if not device:
        return api_response(404, '设备不存在')

    device.last_upload_time = datetime.now()
    db.session.commit()

    return api_response(200, '数据上传记录更新成功', device.to_dict())


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)