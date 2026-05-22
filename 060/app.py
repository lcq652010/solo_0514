from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os
from collections import defaultdict

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mine_base_station.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(app)

class BaseStation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station_code = db.Column(db.String(20), unique=True, nullable=False)
    station_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    install_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='正常')
    last_online_time = db.Column(db.DateTime)
    signal_strength = db.Column(db.Integer)
    transmit_power = db.Column(db.Float)
    antenna_gain = db.Column(db.Float)
    power_supply = db.Column(db.String(50))
    tunnel_type = db.Column(db.String(50))
    working_face = db.Column(db.String(100))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'station_code': self.station_code,
            'station_name': self.station_name,
            'location': self.location,
            'install_date': self.install_date.strftime('%Y-%m-%d') if self.install_date else None,
            'status': self.status,
            'last_online_time': self.last_online_time.strftime('%Y-%m-%d %H:%M:%S') if self.last_online_time else None,
            'signal_strength': self.signal_strength,
            'transmit_power': self.transmit_power,
            'antenna_gain': self.antenna_gain,
            'power_supply': self.power_supply,
            'tunnel_type': self.tunnel_type,
            'working_face': self.working_face,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None,
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S') if self.update_time else None
        }

class PositionException(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station_code = db.Column(db.String(20), nullable=False)
    exception_type = db.Column(db.String(50), nullable=False)
    exception_desc = db.Column(db.Text)
    happen_time = db.Column(db.DateTime, nullable=False)
    handle_status = db.Column(db.String(20), default='待处理')
    handle_time = db.Column(db.DateTime)
    handle_user = db.Column(db.String(50))
    handle_remark = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'station_code': self.station_code,
            'exception_type': self.exception_type,
            'exception_desc': self.exception_desc,
            'happen_time': self.happen_time.strftime('%Y-%m-%d %H:%M:%S') if self.happen_time else None,
            'handle_status': self.handle_status,
            'handle_time': self.handle_time.strftime('%Y-%m-%d %H:%M:%S') if self.handle_time else None,
            'handle_user': self.handle_user,
            'handle_remark': self.handle_remark,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None
        }

class SignalHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station_code = db.Column(db.String(20), nullable=False)
    signal_strength = db.Column(db.Integer, nullable=False)
    record_time = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'station_code': self.station_code,
            'signal_strength': self.signal_strength,
            'record_time': self.record_time.strftime('%Y-%m-%d %H:%M:%S') if self.record_time else None
        }

class SafetyControl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    control_area = db.Column(db.String(100), nullable=False)
    control_type = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    create_time = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'control_area': self.control_area,
            'control_type': self.control_type,
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S') if self.start_time else None,
            'end_time': self.end_time.strftime('%Y-%m-%d %H:%M:%S') if self.end_time else None,
            'description': self.description,
            'is_active': self.is_active,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None
        }

class DeviceWarning(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station_code = db.Column(db.String(20), nullable=False)
    warning_type = db.Column(db.String(50), nullable=False)
    warning_level = db.Column(db.String(20), nullable=False)
    warning_desc = db.Column(db.Text)
    predicted_failure_days = db.Column(db.Integer)
    handle_status = db.Column(db.String(20), default='待处理')
    handle_time = db.Column(db.DateTime)
    handle_user = db.Column(db.String(50))
    create_time = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'station_code': self.station_code,
            'warning_type': self.warning_type,
            'warning_level': self.warning_level,
            'warning_desc': self.warning_desc,
            'predicted_failure_days': self.predicted_failure_days,
            'handle_status': self.handle_status,
            'handle_time': self.handle_time.strftime('%Y-%m-%d %H:%M:%S') if self.handle_time else None,
            'handle_user': self.handle_user,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None
        }

def generate_station_code():
    last_station = BaseStation.query.order_by(BaseStation.id.desc()).first()
    if last_station:
        last_num = int(last_station.station_code.replace('BS', ''))
        new_num = last_num + 1
    else:
        new_num = 1
    return f'BS{new_num:06d}'

@app.route('/api/stations', methods=['POST'])
def add_station():
    data = request.get_json()
    
    if not data or 'station_name' not in data or 'location' not in data:
        return jsonify({'code': 400, 'message': '参数不完整', 'data': None}), 400
    
    station_code = generate_station_code()
    
    install_date_str = data.get('install_date')
    if install_date_str:
        install_date = datetime.strptime(install_date_str, '%Y-%m-%d')
    else:
        install_date = datetime.now()
    
    new_station = BaseStation(
        station_code=station_code,
        station_name=data['station_name'],
        location=data['location'],
        install_date=install_date,
        status=data.get('status', '正常'),
        signal_strength=data.get('signal_strength', 100),
        transmit_power=data.get('transmit_power'),
        antenna_gain=data.get('antenna_gain'),
        power_supply=data.get('power_supply'),
        tunnel_type=data.get('tunnel_type'),
        working_face=data.get('working_face')
    )
    
    try:
        db.session.add(new_station)
        db.session.commit()
        return jsonify({'code': 200, 'message': '添加成功', 'data': new_station.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'添加失败: {str(e)}', 'data': None}), 500

@app.route('/api/stations', methods=['GET'])
def get_stations():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    working_face = request.args.get('working_face')
    
    query = BaseStation.query
    
    if status:
        query = query.filter_by(status=status)
    if working_face:
        query = query.filter_by(working_face=working_face)
    
    pagination = query.order_by(BaseStation.create_time.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'code': 200,
        'message': '查询成功',
        'data': {
            'list': [station.to_dict() for station in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }
    }), 200

@app.route('/api/stations/<station_code>', methods=['GET'])
def get_station(station_code):
    station = BaseStation.query.filter_by(station_code=station_code).first()
    if not station:
        return jsonify({'code': 404, 'message': '基站不存在', 'data': None}), 404
    return jsonify({'code': 200, 'message': '查询成功', 'data': station.to_dict()}), 200

@app.route('/api/stations/<station_code>', methods=['PUT'])
def update_station(station_code):
    station = BaseStation.query.filter_by(station_code=station_code).first()
    if not station:
        return jsonify({'code': 404, 'message': '基站不存在', 'data': None}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'code': 400, 'message': '参数不完整', 'data': None}), 400
    
    if 'status' in data:
        valid_statuses = ['正常', '故障', '离线', '信号弱']
        if data['status'] not in valid_statuses:
            return jsonify({'code': 400, 'message': f'状态值无效，必须是: {", ".join(valid_statuses)}', 'data': None}), 400
        station.status = data['status']
        if data['status'] == '正常':
            station.last_online_time = datetime.now()
    
    if 'signal_strength' in data:
        station.signal_strength = data['signal_strength']
    if 'transmit_power' in data:
        station.transmit_power = data['transmit_power']
    if 'antenna_gain' in data:
        station.antenna_gain = data['antenna_gain']
    if 'power_supply' in data:
        station.power_supply = data['power_supply']
    if 'tunnel_type' in data:
        station.tunnel_type = data['tunnel_type']
    if 'working_face' in data:
        station.working_face = data['working_face']
    
    try:
        db.session.commit()
        return jsonify({'code': 200, 'message': '更新成功', 'data': station.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'更新失败: {str(e)}', 'data': None}), 500

@app.route('/api/stations/<station_code>/heartbeat', methods=['POST'])
def station_heartbeat(station_code):
    station = BaseStation.query.filter_by(station_code=station_code).first()
    if not station:
        return jsonify({'code': 404, 'message': '基站不存在', 'data': None}), 404
    
    data = request.get_json() or {}
    
    station.last_online_time = datetime.now()
    station.status = '正常'
    
    if 'signal_strength' in data:
        station.signal_strength = data['signal_strength']
        
        signal_history = SignalHistory(
            station_code=station_code,
            signal_strength=data['signal_strength'],
            record_time=datetime.now()
        )
        db.session.add(signal_history)
    
    try:
        db.session.commit()
        return jsonify({'code': 200, 'message': '心跳上报成功', 'data': station.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'心跳上报失败: {str(e)}', 'data': None}), 500

@app.route('/api/exceptions', methods=['POST'])
def report_exception():
    data = request.get_json()
    
    if not data or 'station_code' not in data or 'exception_type' not in data:
        return jsonify({'code': 400, 'message': '参数不完整', 'data': None}), 400
    
    valid_exception_types = ['基站断电', '信号干扰', '通信中断']
    if data['exception_type'] not in valid_exception_types:
        return jsonify({'code': 400, 'message': f'异常类型无效，必须是: {", ".join(valid_exception_types)}', 'data': None}), 400
    
    station = BaseStation.query.filter_by(station_code=data['station_code']).first()
    if not station:
        return jsonify({'code': 404, 'message': '基站不存在', 'data': None}), 404
    
    happen_time_str = data.get('happen_time')
    if happen_time_str:
        happen_time = datetime.strptime(happen_time_str, '%Y-%m-%d %H:%M:%S')
    else:
        happen_time = datetime.now()
    
    exception = PositionException(
        station_code=data['station_code'],
        exception_type=data['exception_type'],
        exception_desc=data.get('exception_desc', ''),
        happen_time=happen_time
    )
    
    try:
        db.session.add(exception)
        db.session.commit()
        return jsonify({'code': 200, 'message': '异常上报成功', 'data': exception.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'异常上报失败: {str(e)}', 'data': None}), 500

@app.route('/api/exceptions', methods=['GET'])
def get_exceptions():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    station_code = request.args.get('station_code')
    handle_status = request.args.get('handle_status')
    
    query = PositionException.query
    
    if station_code:
        query = query.filter_by(station_code=station_code)
    if handle_status:
        query = query.filter_by(handle_status=handle_status)
    
    pagination = query.order_by(PositionException.create_time.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'code': 200,
        'message': '查询成功',
        'data': {
            'list': [exc.to_dict() for exc in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }
    }), 200

@app.route('/api/exceptions/<int:exception_id>/handle', methods=['PUT'])
def handle_exception(exception_id):
    exception = PositionException.query.get(exception_id)
    if not exception:
        return jsonify({'code': 404, 'message': '异常记录不存在', 'data': None}), 404
    
    data = request.get_json()
    if not data or 'handle_user' not in data:
        return jsonify({'code': 400, 'message': '参数不完整', 'data': None}), 400
    
    exception.handle_status = '已处理'
    exception.handle_time = datetime.now()
    exception.handle_user = data['handle_user']
    exception.handle_remark = data.get('handle_remark', '')
    
    try:
        db.session.commit()
        return jsonify({'code': 200, 'message': '处理成功', 'data': exception.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'处理失败: {str(e)}', 'data': None}), 500

@app.route('/api/stations/statistics', methods=['GET'])
def get_statistics():
    total = BaseStation.query.count()
    normal = BaseStation.query.filter_by(status='正常').count()
    fault = BaseStation.query.filter_by(status='故障').count()
    offline = BaseStation.query.filter_by(status='离线').count()
    weak_signal = BaseStation.query.filter_by(status='信号弱').count()
    
    pending_exceptions = PositionException.query.filter_by(handle_status='待处理').count()
    
    return jsonify({
        'code': 200,
        'message': '查询成功',
        'data': {
            'total_stations': total,
            'status_count': {
                '正常': normal,
                '故障': fault,
                '离线': offline,
                '信号弱': weak_signal
            },
            'pending_exceptions': pending_exceptions
        }
    }), 200

@app.route('/api/safety-control', methods=['POST'])
def add_safety_control():
    data = request.get_json()
    
    if not data or 'control_area' not in data or 'start_time' not in data or 'end_time' not in data:
        return jsonify({'code': 400, 'message': '参数不完整', 'data': None}), 400
    
    try:
        start_time = datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M:%S')
    except:
        return jsonify({'code': 400, 'message': '时间格式错误', 'data': None}), 400
    
    control = SafetyControl(
        control_area=data['control_area'],
        control_type=data.get('control_type', '安全管控'),
        start_time=start_time,
        end_time=end_time,
        description=data.get('description', '')
    )
    
    try:
        db.session.add(control)
        db.session.commit()
        return jsonify({'code': 200, 'message': '添加成功', 'data': control.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'添加失败: {str(e)}', 'data': None}), 500

@app.route('/api/safety-control', methods=['GET'])
def get_safety_controls():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    is_active = request.args.get('is_active')
    
    query = SafetyControl.query
    
    if is_active is not None:
        query = query.filter_by(is_active=is_active.lower() == 'true')
    
    pagination = query.order_by(SafetyControl.create_time.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'code': 200,
        'message': '查询成功',
        'data': {
            'list': [c.to_dict() for c in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }
    }), 200

def is_in_safety_control(station):
    now = datetime.now()
    controls = SafetyControl.query.filter(
        SafetyControl.is_active == True,
        SafetyControl.start_time <= now,
        SafetyControl.end_time >= now
    ).all()
    
    for control in controls:
        if control.control_area in station.location or control.control_area in (station.working_face or ''):
            return True, control
    return False, None

@app.route('/api/stations/<station_code>/signal-trend', methods=['GET'])
def get_signal_trend(station_code):
    station = BaseStation.query.filter_by(station_code=station_code).first()
    if not station:
        return jsonify({'code': 404, 'message': '基站不存在', 'data': None}), 404
    
    days = request.args.get('days', 7, type=int)
    start_time = datetime.now() - timedelta(days=days)
    
    histories = SignalHistory.query.filter(
        SignalHistory.station_code == station_code,
        SignalHistory.record_time >= start_time
    ).order_by(SignalHistory.record_time.asc()).all()
    
    if len(histories) < 2:
        return jsonify({
            'code': 200,
            'message': '数据不足',
            'data': {
                'station_code': station_code,
                'signal_list': [h.to_dict() for h in histories],
                'trend': 'stable',
                'attenuation_rate': 0,
                'warning': False
            }
        }), 200
    
    signal_values = [h.signal_strength for h in histories]
    first_signal = signal_values[0]
    last_signal = signal_values[-1]
    attenuation_rate = ((first_signal - last_signal) / first_signal * 100) if first_signal > 0 else 0
    
    if attenuation_rate > 30:
        trend = 'rapid_decline'
        warning = True
        warning_level = '高'
    elif attenuation_rate > 15:
        trend = 'slow_decline'
        warning = True
        warning_level = '中'
    elif attenuation_rate < -10:
        trend = 'rising'
        warning = False
    else:
        trend = 'stable'
        warning = False
    
    if warning:
        predicted_days = int((last_signal - 30) / (attenuation_rate / days)) if attenuation_rate > 0 else None
        existing_warning = DeviceWarning.query.filter_by(
            station_code=station_code,
            handle_status='待处理'
        ).first()
        
        if not existing_warning:
            warning_desc = f'信号强度在{days}天内衰减{attenuation_rate:.1f}%，当前信号{last_signal}'
            new_warning = DeviceWarning(
                station_code=station_code,
                warning_type='信号衰减预警',
                warning_level=warning_level,
                warning_desc=warning_desc,
                predicted_failure_days=predicted_days
            )
            db.session.add(new_warning)
            db.session.commit()
    
    return jsonify({
        'code': 200,
        'message': '查询成功',
        'data': {
            'station_code': station_code,
            'signal_list': [h.to_dict() for h in histories],
            'trend': trend,
            'attenuation_rate': round(attenuation_rate, 2),
            'warning': warning,
            'current_signal': last_signal,
            'predicted_failure_days': predicted_days if warning else None
        }
    }), 200

@app.route('/api/warnings', methods=['GET'])
def get_warnings():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    station_code = request.args.get('station_code')
    handle_status = request.args.get('handle_status')
    
    query = DeviceWarning.query
    
    if station_code:
        query = query.filter_by(station_code=station_code)
    if handle_status:
        query = query.filter_by(handle_status=handle_status)
    
    pagination = query.order_by(DeviceWarning.create_time.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'code': 200,
        'message': '查询成功',
        'data': {
            'list': [w.to_dict() for w in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }
    }), 200

@app.route('/api/warnings/<int:warning_id>/handle', methods=['PUT'])
def handle_warning(warning_id):
    warning = DeviceWarning.query.get(warning_id)
    if not warning:
        return jsonify({'code': 404, 'message': '预警记录不存在', 'data': None}), 404
    
    data = request.get_json()
    if not data or 'handle_user' not in data:
        return jsonify({'code': 400, 'message': '参数不完整', 'data': None}), 400
    
    warning.handle_status = '已处理'
    warning.handle_time = datetime.now()
    warning.handle_user = data['handle_user']
    
    try:
        db.session.commit()
        return jsonify({'code': 200, 'message': '处理成功', 'data': warning.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'处理失败: {str(e)}', 'data': None}), 500

@app.route('/api/reports/reliability', methods=['GET'])
def get_reliability_report():
    total_stations = BaseStation.query.count()
    if total_stations == 0:
        return jsonify({'code': 200, 'message': '无基站数据', 'data': None}), 200
    
    normal_count = BaseStation.query.filter_by(status='正常').count()
    fault_count = BaseStation.query.filter_by(status='故障').count()
    offline_count = BaseStation.query.filter_by(status='离线').count()
    weak_count = BaseStation.query.filter_by(status='信号弱').count()
    
    effective_offline = 0
    false_alarm_offline = 0
    offline_stations = BaseStation.query.filter_by(status='离线').all()
    
    for station in offline_stations:
        in_control, _ = is_in_safety_control(station)
        if in_control:
            false_alarm_offline += 1
        else:
            effective_offline += 1
    
    reliability_rate = ((normal_count + weak_count) / total_stations * 100) if total_stations > 0 else 0
    
    warning_count = DeviceWarning.query.filter_by(handle_status='待处理').count()
    exception_count = PositionException.query.filter_by(handle_status='待处理').count()
    
    report_time = datetime.now()
    
    return jsonify({
        'code': 200,
        'message': '查询成功',
        'data': {
            'report_time': report_time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_stations': total_stations,
            'status_distribution': {
                '正常': normal_count,
                '故障': fault_count,
                '离线': offline_count,
                '信号弱': weak_count
            },
            'offline_analysis': {
                'total_offline': offline_count,
                'effective_offline': effective_offline,
                'false_alarm_offline': false_alarm_offline,
                'false_alarm_rate': round((false_alarm_offline / offline_count * 100) if offline_count > 0 else 0, 2)
            },
            'network_reliability_rate': round(reliability_rate, 2),
            'pending_warnings': warning_count,
            'pending_exceptions': exception_count
        }
    }), 200

@app.route('/api/reports/maintenance-priority', methods=['GET'])
def get_maintenance_priority():
    tunnel_type = request.args.get('tunnel_type')
    
    stations = BaseStation.query.all()
    if not stations:
        return jsonify({'code': 200, 'message': '无基站数据', 'data': None}), 200
    
    tunnel_groups = defaultdict(list)
    
    for station in stations:
        key = station.tunnel_type or '未分类'
        if tunnel_type and key != tunnel_type:
            continue
        
        priority_score = 0
        priority_reasons = []
        
        if station.status == '故障':
            priority_score += 100
            priority_reasons.append('设备故障')
        elif station.status == '离线':
            in_control, control = is_in_safety_control(station)
            if in_control:
                priority_score += 10
                priority_reasons.append('安全管控离线(误报)')
            else:
                priority_score += 80
                priority_reasons.append('设备离线')
        elif station.status == '信号弱':
            priority_score += 50
            priority_reasons.append('信号弱')
        
        warning = DeviceWarning.query.filter_by(
            station_code=station.station_code,
            handle_status='待处理'
        ).first()
        
        if warning:
            if warning.warning_level == '高':
                priority_score += 60
            elif warning.warning_level == '中':
                priority_score += 30
            priority_reasons.append(f'{warning.warning_level}级信号衰减预警')
        
        exception = PositionException.query.filter_by(
            station_code=station.station_code,
            handle_status='待处理'
        ).first()
        
        if exception:
            priority_score += 40
            priority_reasons.append(f'{exception.exception_type}异常待处理')
        
        if priority_score >= 100:
            priority_level = '紧急'
        elif priority_score >= 60:
            priority_level = '高'
        elif priority_score >= 30:
            priority_level = '中'
        elif priority_score > 0:
            priority_level = '低'
        else:
            priority_level = '正常'
        
        tunnel_groups[key].append({
            'station_code': station.station_code,
            'station_name': station.station_name,
            'location': station.location,
            'working_face': station.working_face,
            'status': station.status,
            'signal_strength': station.signal_strength,
            'priority_score': priority_score,
            'priority_level': priority_level,
            'priority_reasons': priority_reasons
        })
    
    result = []
    for tunnel, devices in tunnel_groups.items():
        sorted_devices = sorted(devices, key=lambda x: x['priority_score'], reverse=True)
        
        emergency_count = sum(1 for d in sorted_devices if d['priority_level'] == '紧急')
        high_count = sum(1 for d in sorted_devices if d['priority_level'] == '高')
        
        result.append({
            'tunnel_type': tunnel,
            'device_count': len(sorted_devices),
            'emergency_count': emergency_count,
            'high_count': high_count,
            'devices': sorted_devices
        })
    
    result = sorted(result, key=lambda x: x['emergency_count'] * 100 + x['high_count'], reverse=True)
    
    return jsonify({
        'code': 200,
        'message': '查询成功',
        'data': {
            'report_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'tunnel_list': result
        }
    }), 200

@app.route('/')
def index():
    return jsonify({
        'code': 200,
        'message': '矿山井下人员定位基站运维系统后端 API',
        'data': {
            'version': '2.0.0',
            'endpoints': {
                '基站管理': {
                    'POST /api/stations': '添加基站（支持发射功率、天线增益、供电方式、巷道类型、采掘工作面）',
                    'GET /api/stations': '获取基站列表（支持按状态、采掘工作面筛选）',
                    'GET /api/stations/<station_code>': '获取单个基站信息',
                    'PUT /api/stations/<station_code>': '更新基站信息',
                    'POST /api/stations/<station_code>/heartbeat': '基站心跳上报'
                },
                '异常管理': {
                    'POST /api/exceptions': '上报定位异常（类型：基站断电、信号干扰、通信中断）',
                    'GET /api/exceptions': '获取异常列表',
                    'PUT /api/exceptions/<exception_id>/handle': '处理异常'
                },
                '安全管控联动': {
                    'POST /api/safety-control': '添加安全管控记录',
                    'GET /api/safety-control': '获取安全管控列表'
                },
                '信号趋势分析与预警': {
                    'GET /api/stations/<station_code>/signal-trend': '获取基站信号衰减趋势分析',
                    'GET /api/warnings': '获取设备预警列表',
                    'PUT /api/warnings/<warning_id>/handle': '处理预警'
                },
                '报表与运维优先级': {
                    'GET /api/reports/reliability': '获取井下定位网络可靠性报表（含误报过滤）',
                    'GET /api/reports/maintenance-priority': '按巷道生成运维优先级清单'
                },
                '统计': {
                    'GET /api/stations/statistics': '获取统计信息'
                }
            }
        }
    }), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print('数据库初始化完成')
    app.run(debug=True, host='0.0.0.0', port=5000)
