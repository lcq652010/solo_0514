from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os
import random

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'gas_monitoring.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_code = db.Column(db.String(50), unique=True, nullable=False)
    device_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    gas_type = db.Column(db.String(50), nullable=False)
    measure_range = db.Column(db.String(50))
    threshold = db.Column(db.Float, nullable=False)
    alarm_upper_limit = db.Column(db.Float)
    installation_point = db.Column(db.String(200))
    status = db.Column(db.String(20), default='正常')
    created_at = db.Column(db.DateTime, default=datetime.now)
    last_online = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'device_code': self.device_code,
            'device_name': self.device_name,
            'location': self.location,
            'gas_type': self.gas_type,
            'measure_range': self.measure_range,
            'threshold': self.threshold,
            'alarm_upper_limit': self.alarm_upper_limit,
            'installation_point': self.installation_point,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'last_online': self.last_online.strftime('%Y-%m-%d %H:%M:%S') if self.last_online else None
        }

class Alarm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_no = db.Column(db.String(30), unique=True, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    gas_value = db.Column(db.Float, nullable=False)
    alarm_time = db.Column(db.DateTime, default=datetime.now)
    confirm_status = db.Column(db.String(20), default='未确认')
    handle_result = db.Column(db.Text)
    handler = db.Column(db.String(50))
    handle_time = db.Column(db.DateTime)
    description = db.Column(db.Text)

    device = db.relationship('Device', backref=db.backref('alarms', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'ticket_no': self.ticket_no,
            'device_id': self.device_id,
            'device_code': self.device.device_code if self.device else None,
            'device_name': self.device.device_name if self.device else None,
            'gas_value': self.gas_value,
            'alarm_time': self.alarm_time.strftime('%Y-%m-%d %H:%M:%S'),
            'confirm_status': self.confirm_status,
            'handle_result': self.handle_result,
            'handler': self.handler,
            'handle_time': self.handle_time.strftime('%Y-%m-%d %H:%M:%S') if self.handle_time else None,
            'description': self.description
        }

class GasReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    gas_value = db.Column(db.Float, nullable=False)
    reading_time = db.Column(db.DateTime, default=datetime.now)

    device = db.relationship('Device', backref=db.backref('readings', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'device_code': self.device.device_code if self.device else None,
            'gas_value': self.gas_value,
            'reading_time': self.reading_time.strftime('%Y-%m-%d %H:%M:%S')
        }

def generate_ticket_no():
    today = datetime.now().strftime('%Y%m%d')
    last_alarm = Alarm.query.filter(Alarm.ticket_no.like(f'GD{today}%')).order_by(Alarm.id.desc()).first()
    if last_alarm:
        last_num = int(last_alarm.ticket_no[-4:])
        new_num = str(last_num + 1).zfill(4)
    else:
        new_num = '0001'
    return f'GD{today}{new_num}'

@app.route('/api/devices', methods=['POST'])
def add_device():
    data = request.get_json()
    required_fields = ['device_code', 'device_name', 'location', 'gas_type', 'threshold']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'缺少必填字段: {field}'}), 400
    
    if Device.query.filter_by(device_code=data['device_code']).first():
        return jsonify({'error': '设备编号已存在'}), 400
    
    device = Device(
        device_code=data['device_code'],
        device_name=data['device_name'],
        location=data['location'],
        gas_type=data['gas_type'],
        measure_range=data.get('measure_range'),
        threshold=data['threshold'],
        alarm_upper_limit=data.get('alarm_upper_limit'),
        installation_point=data.get('installation_point'),
        status=data.get('status', '正常')
    )
    db.session.add(device)
    db.session.commit()
    return jsonify({'message': '设备添加成功', 'device': device.to_dict()}), 201

@app.route('/api/devices', methods=['GET'])
def get_devices():
    status = request.args.get('status')
    gas_type = request.args.get('gas_type')
    
    query = Device.query
    if status:
        query = query.filter_by(status=status)
    if gas_type:
        query = query.filter_by(gas_type=gas_type)
    
    devices = query.all()
    return jsonify([device.to_dict() for device in devices])

@app.route('/api/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    device = Device.query.get_or_404(device_id)
    return jsonify(device.to_dict())

@app.route('/api/devices/code/<device_code>', methods=['GET'])
def get_device_by_code(device_code):
    device = Device.query.filter_by(device_code=device_code).first()
    if not device:
        return jsonify({'error': '设备不存在'}), 404
    return jsonify(device.to_dict())

@app.route('/api/devices/<int:device_id>/status', methods=['PUT'])
def update_device_status(device_id):
    device = Device.query.get_or_404(device_id)
    data = request.get_json()
    if 'status' not in data:
        return jsonify({'error': '缺少status字段'}), 400
    if data['status'] not in ['正常', '故障', '离线', '告警']:
        return jsonify({'error': '无效的状态值，必须是: 正常、故障、离线、告警'}), 400
    
    device.status = data['status']
    if data['status'] != '离线':
        device.last_online = datetime.now()
    db.session.commit()
    return jsonify({'message': '状态更新成功', 'device': device.to_dict()})

@app.route('/api/alarms', methods=['POST'])
def report_alarm():
    data = request.get_json()
    required_fields = ['device_code', 'gas_value']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'缺少必填字段: {field}'}), 400
    
    device = Device.query.filter_by(device_code=data['device_code']).first()
    if not device:
        return jsonify({'error': '设备不存在'}), 404
    
    ticket_no = generate_ticket_no()
    alarm = Alarm(
        ticket_no=ticket_no,
        device_id=device.id,
        gas_value=data['gas_value'],
        description=data.get('description', f'{device.gas_type}浓度超标: {data["gas_value"]}, 阈值: {device.threshold}')
    )
    
    device.status = '告警'
    device.last_online = datetime.now()
    
    db.session.add(alarm)
    db.session.commit()
    return jsonify({'message': '告警上报成功', 'alarm': alarm.to_dict()}), 201

@app.route('/api/alarms', methods=['GET'])
def get_alarms():
    confirm_status = request.args.get('confirm_status')
    query = Alarm.query.order_by(Alarm.alarm_time.desc())
    
    if confirm_status:
        query = query.filter_by(confirm_status=confirm_status)
    
    alarms = query.all()
    return jsonify([alarm.to_dict() for alarm in alarms])

@app.route('/api/alarms/categorized', methods=['GET'])
def get_alarms_categorized():
    unconfirmed = Alarm.query.filter_by(confirm_status='未确认').order_by(Alarm.alarm_time.desc()).all()
    confirmed = Alarm.query.filter_by(confirm_status='已确认').order_by(Alarm.alarm_time.desc()).all()
    handled = Alarm.query.filter_by(confirm_status='已处置').order_by(Alarm.alarm_time.desc()).all()
    
    return jsonify({
        'unconfirmed': [alarm.to_dict() for alarm in unconfirmed],
        'confirmed': [alarm.to_dict() for alarm in confirmed],
        'handled': [alarm.to_dict() for alarm in handled]
    })

@app.route('/api/alarms/<int:alarm_id>/confirm', methods=['PUT'])
def confirm_alarm(alarm_id):
    alarm = Alarm.query.get_or_404(alarm_id)
    data = request.get_json()
    
    alarm.confirm_status = '已确认'
    alarm.handler = data.get('handler')
    alarm.handle_time = datetime.now()
    
    db.session.commit()
    return jsonify({'message': '告警确认成功', 'alarm': alarm.to_dict()})

@app.route('/api/alarms/<int:alarm_id>/handle', methods=['PUT'])
def handle_alarm(alarm_id):
    alarm = Alarm.query.get_or_404(alarm_id)
    data = request.get_json()
    
    alarm.confirm_status = '已处置'
    alarm.handle_result = data.get('handle_result')
    alarm.handler = data.get('handler')
    alarm.handle_time = datetime.now()
    
    db.session.commit()
    return jsonify({'message': '告警处置成功，已完成闭环', 'alarm': alarm.to_dict()})

@app.route('/api/gas-types', methods=['GET'])
def get_gas_types():
    gas_types = db.session.query(Device.gas_type).distinct().all()
    return jsonify([gt[0] for gt in gas_types])

@app.route('/api/devices/<int:device_id>/trend/daily', methods=['GET'])
def get_device_daily_trend(device_id):
    device = Device.query.get_or_404(device_id)
    end_time = datetime.now()
    start_time = end_time - timedelta(days=1)
    
    readings = GasReading.query.filter(
        GasReading.device_id == device_id,
        GasReading.reading_time >= start_time,
        GasReading.reading_time <= end_time
    ).order_by(GasReading.reading_time).all()
    
    if not readings:
        readings = generate_mock_readings(device_id, hours=24)
    
    return jsonify({
        'device_id': device_id,
        'device_code': device.device_code,
        'device_name': device.device_name,
        'gas_type': device.gas_type,
        'threshold': device.threshold,
        'time_range': f'{start_time.strftime("%Y-%m-%d %H:%M:%S")} - {end_time.strftime("%Y-%m-%d %H:%M:%S")}',
        'data': [r.to_dict() for r in readings]
    })

@app.route('/api/devices/<int:device_id>/trend/weekly', methods=['GET'])
def get_device_weekly_trend(device_id):
    device = Device.query.get_or_404(device_id)
    end_time = datetime.now()
    start_time = end_time - timedelta(days=7)
    
    readings = GasReading.query.filter(
        GasReading.device_id == device_id,
        GasReading.reading_time >= start_time,
        GasReading.reading_time <= end_time
    ).order_by(GasReading.reading_time).all()
    
    if not readings:
        readings = generate_mock_readings(device_id, days=7)
    
    return jsonify({
        'device_id': device_id,
        'device_code': device.device_code,
        'device_name': device.device_name,
        'gas_type': device.gas_type,
        'threshold': device.threshold,
        'time_range': f'{start_time.strftime("%Y-%m-%d %H:%M:%S")} - {end_time.strftime("%Y-%m-%d %H:%M:%S")}',
        'data': [r.to_dict() for r in readings]
    })

def generate_mock_readings(device_id, hours=None, days=None):
    device = Device.query.get(device_id)
    base_value = device.threshold * 0.6
    readings = []
    
    if hours:
        for i in range(hours):
            reading_time = datetime.now() - timedelta(hours=hours - i)
            gas_value = round(base_value + random.uniform(-base_value * 0.3, base_value * 0.6), 2)
            reading = GasReading(
                device_id=device_id,
                gas_value=gas_value,
                reading_time=reading_time
            )
            readings.append(reading)
    elif days:
        for i in range(days * 24):
            reading_time = datetime.now() - timedelta(hours=days * 24 - i)
            gas_value = round(base_value + random.uniform(-base_value * 0.3, base_value * 0.6), 2)
            reading = GasReading(
                device_id=device_id,
                gas_value=gas_value,
                reading_time=reading_time
            )
            readings.append(reading)
    
    db.session.add_all(readings)
    db.session.commit()
    return readings

@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    total_devices = Device.query.count()
    normal_devices = Device.query.filter_by(status='正常').count()
    fault_devices = Device.query.filter_by(status='故障').count()
    offline_devices = Device.query.filter_by(status='离线').count()
    alarm_devices = Device.query.filter_by(status='告警').count()
    unconfirmed_alarms = Alarm.query.filter_by(confirm_status='未确认').count()
    confirmed_alarms = Alarm.query.filter_by(confirm_status='已确认').count()
    handled_alarms = Alarm.query.filter_by(confirm_status='已处置').count()
    
    return jsonify({
        'total_devices': total_devices,
        'normal_devices': normal_devices,
        'fault_devices': fault_devices,
        'offline_devices': offline_devices,
        'alarm_devices': alarm_devices,
        'unconfirmed_alarms': unconfirmed_alarms,
        'confirmed_alarms': confirmed_alarms,
        'handled_alarms': handled_alarms
    })

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
