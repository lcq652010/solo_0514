from datetime import datetime, date, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Device, ExceptionReport, WorkOrder, RecognitionRecord, DailyStats, MonthlyStats
from sqlalchemy import func, and_
import os

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'rfid_terminal.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

db.init_app(app)


def generate_work_order_no():
    today = date.today().strftime('%Y%m%d')
    prefix = f'WO{today}'
    last_order = WorkOrder.query.filter(WorkOrder.order_no.like(f'{prefix}%')).order_by(WorkOrder.order_no.desc()).first()
    if last_order:
        seq = int(last_order.order_no[-4:]) + 1
    else:
        seq = 1
    return f'{prefix}{seq:04d}'


@app.route('/')
def index():
    return jsonify({
        'message': '港口集装箱RFID识别终端运维管理系统',
        'version': '1.0.0',
        'status': 'running'
    })


@app.route('/api/devices', methods=['GET'])
def get_devices():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    keyword = request.args.get('keyword')
    work_zone = request.args.get('work_zone')
    wharf_code = request.args.get('wharf_code')
    
    query = Device.query
    if status:
        query = query.filter(Device.status == status)
    if work_zone:
        query = query.filter(Device.work_zone == work_zone)
    if wharf_code:
        query = query.filter(Device.wharf_code == wharf_code)
    if keyword:
        query = query.filter(
            (Device.device_code.like(f'%{keyword}%')) |
            (Device.device_name.like(f'%{keyword}%')) |
            (Device.sn_code.like(f'%{keyword}%'))
        )
    
    pagination = query.order_by(Device.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': {
            'items': [d.to_dict() for d in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }
    })


@app.route('/api/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    device = Device.query.get_or_404(device_id)
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': device.to_dict()
    })


@app.route('/api/devices', methods=['POST'])
def create_device():
    data = request.get_json()
    
    if Device.query.filter_by(device_code=data['device_code']).first():
        return jsonify({'code': 1, 'message': '设备编号已存在'}), 400
    
    device = Device(
        device_code=data['device_code'],
        device_name=data['device_name'],
        wharf_code=data.get('wharf_code'),
        crane_location=data.get('crane_location'),
        sn_code=data.get('sn_code'),
        work_zone=data.get('work_zone'),
        location=data.get('location'),
        install_date=datetime.strptime(data['install_date'], '%Y-%m-%d').date() if data.get('install_date') else None,
        status=data.get('status', 'normal'),
        signal_strength=data.get('signal_strength'),
        remarks=data.get('remarks')
    )
    
    db.session.add(device)
    db.session.commit()
    
    return jsonify({
        'code': 0,
        'message': '设备创建成功',
        'data': device.to_dict()
    }), 201


@app.route('/api/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    device = Device.query.get_or_404(device_id)
    data = request.get_json()
    
    if 'device_code' in data and data['device_code'] != device.device_code:
        if Device.query.filter_by(device_code=data['device_code']).first():
            return jsonify({'code': 1, 'message': '设备编号已存在'}), 400
        device.device_code = data['device_code']
    
    device.device_name = data.get('device_name', device.device_name)
    device.wharf_code = data.get('wharf_code', device.wharf_code)
    device.crane_location = data.get('crane_location', device.crane_location)
    device.sn_code = data.get('sn_code', device.sn_code)
    device.work_zone = data.get('work_zone', device.work_zone)
    device.location = data.get('location', device.location)
    if data.get('install_date'):
        device.install_date = datetime.strptime(data['install_date'], '%Y-%m-%d').date()
    device.status = data.get('status', device.status)
    device.signal_strength = data.get('signal_strength', device.signal_strength)
    device.remarks = data.get('remarks', device.remarks)
    
    db.session.commit()
    
    return jsonify({
        'code': 0,
        'message': '设备更新成功',
        'data': device.to_dict()
    })


@app.route('/api/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    device = Device.query.get_or_404(device_id)
    db.session.delete(device)
    db.session.commit()
    
    return jsonify({
        'code': 0,
        'message': '设备删除成功'
    })


@app.route('/api/devices/<int:device_id>/status', methods=['PUT'])
def update_device_status(device_id):
    device = Device.query.get_or_404(device_id)
    data = request.get_json()
    
    device.status = data['status']
    if data['status'] == 'normal':
        device.last_heartbeat = datetime.now()
    
    db.session.commit()
    
    return jsonify({
        'code': 0,
        'message': '状态更新成功',
        'data': device.to_dict()
    })


@app.route('/api/devices/<int:device_id>/heartbeat', methods=['POST'])
def device_heartbeat(device_id):
    device = Device.query.get_or_404(device_id)
    data = request.get_json()
    
    device.last_heartbeat = datetime.now()
    if data.get('signal_strength') is not None:
        device.signal_strength = data['signal_strength']
    
    db.session.commit()
    
    return jsonify({
        'code': 0,
        'message': '心跳上报成功'
    })


@app.route('/api/exceptions', methods=['GET'])
def get_exceptions():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    device_id = request.args.get('device_id', type=int)
    handled = request.args.get('handled')
    
    query = ExceptionReport.query
    if device_id:
        query = query.filter(ExceptionReport.device_id == device_id)
    if handled is not None:
        query = query.filter(ExceptionReport.handled == (handled == 'true'))
    
    pagination = query.order_by(ExceptionReport.start_time.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': {
            'items': [e.to_dict() for e in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }
    })


@app.route('/api/exceptions', methods=['POST'])
def create_exception():
    data = request.get_json()
    
    device = Device.query.get(data['device_id'])
    if not device:
        return jsonify({'code': 1, 'message': '设备不存在'}), 400
    
    start_time = datetime.now()
    if data.get('start_time'):
        start_time = datetime.fromisoformat(data['start_time'].replace('Z', '+00:00'))
    
    exception = ExceptionReport(
        device_id=data['device_id'],
        exception_type=data['exception_type'],
        start_time=start_time,
        description=data.get('description'),
        container_code=data.get('container_code'),
        rfid_data=data.get('rfid_data')
    )
    
    db.session.add(exception)
    
    if device.status == 'normal':
        if data['exception_type'] in ['read_failure', 'data_error']:
            device.status = 'fault'
        elif data['exception_type'] == 'signal_weak':
            device.status = 'signal_error'
    
    db.session.commit()
    
    return jsonify({
        'code': 0,
        'message': '异常上报成功',
        'data': exception.to_dict()
    }), 201


@app.route('/api/exceptions/<int:exception_id>/handle', methods=['PUT'])
def handle_exception(exception_id):
    exception = ExceptionReport.query.get_or_404(exception_id)
    data = request.get_json()
    
    exception.handled = True
    exception.handled_at = datetime.now()
    exception.handler = data.get('handler')
    
    db.session.commit()
    
    return jsonify({
        'code': 0,
        'message': '异常处理成功',
        'data': exception.to_dict()
    })


@app.route('/api/work-orders', methods=['GET'])
def get_work_orders():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    device_id = request.args.get('device_id', type=int)
    status = request.args.get('status')
    
    query = WorkOrder.query
    if device_id:
        query = query.filter(WorkOrder.device_id == device_id)
    if status:
        query = query.filter(WorkOrder.status == status)
    
    pagination = query.order_by(WorkOrder.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': {
            'items': [w.to_dict() for w in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }
    })


@app.route('/api/work-orders/<int:order_id>', methods=['GET'])
def get_work_order(order_id):
    order = WorkOrder.query.get_or_404(order_id)
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': order.to_dict()
    })


@app.route('/api/work-orders', methods=['POST'])
def create_work_order():
    data = request.get_json()
    
    device = Device.query.get(data['device_id'])
    if not device:
        return jsonify({'code': 1, 'message': '设备不存在'}), 400
    
    order_no = generate_work_order_no()
    
    work_order = WorkOrder(
        order_no=order_no,
        device_id=data['device_id'],
        exception_id=data.get('exception_id'),
        title=data['title'],
        description=data.get('description'),
        priority=data.get('priority', 'medium'),
        assign_to=data.get('assign_to'),
        created_by=data.get('created_by')
    )
    
    db.session.add(work_order)
    db.session.commit()
    
    return jsonify({
        'code': 0,
        'message': '工单创建成功',
        'data': work_order.to_dict()
    }), 201


@app.route('/api/work-orders/<int:order_id>', methods=['PUT'])
def update_work_order(order_id):
    work_order = WorkOrder.query.get_or_404(order_id)
    data = request.get_json()
    
    work_order.title = data.get('title', work_order.title)
    work_order.description = data.get('description', work_order.description)
    work_order.priority = data.get('priority', work_order.priority)
    work_order.status = data.get('status', work_order.status)
    work_order.assign_to = data.get('assign_to', work_order.assign_to)
    
    if work_order.status == 'processing' and not work_order.started_at:
        work_order.started_at = datetime.now()
    elif work_order.status == 'completed' and not work_order.completed_at:
        work_order.completed_at = datetime.now()
    
    db.session.commit()
    
    return jsonify({
        'code': 0,
        'message': '工单更新成功',
        'data': work_order.to_dict()
    })


@app.route('/api/work-orders/<int:order_id>/status', methods=['PUT'])
def update_work_order_status(order_id):
    work_order = WorkOrder.query.get_or_404(order_id)
    data = request.get_json()
    
    work_order.status = data['status']
    
    if work_order.status == 'processing' and not work_order.started_at:
        work_order.started_at = datetime.now()
    elif work_order.status == 'completed' and not work_order.completed_at:
        work_order.completed_at = datetime.now()
    
    db.session.commit()
    
    return jsonify({
        'code': 0,
        'message': '状态更新成功',
        'data': work_order.to_dict()
    })


def update_daily_stats(device_id, stats_date=None):
    if stats_date is None:
        stats_date = date.today()
    
    start_datetime = datetime.combine(stats_date, datetime.min.time())
    end_datetime = datetime.combine(stats_date, datetime.max.time())
    
    total_recognitions = RecognitionRecord.query.filter(
        RecognitionRecord.device_id == device_id,
        RecognitionRecord.recognition_time >= start_datetime,
        RecognitionRecord.recognition_time <= end_datetime
    ).count()
    
    success_recognitions = RecognitionRecord.query.filter(
        RecognitionRecord.device_id == device_id,
        RecognitionRecord.recognition_time >= start_datetime,
        RecognitionRecord.recognition_time <= end_datetime,
        RecognitionRecord.success == True
    ).count()
    
    fail_recognitions = total_recognitions - success_recognitions
    success_rate = (success_recognitions / total_recognitions * 100) if total_recognitions > 0 else 100.0
    
    exceptions = ExceptionReport.query.filter(
        ExceptionReport.device_id == device_id,
        ExceptionReport.start_time >= start_datetime,
        ExceptionReport.start_time <= end_datetime
    ).all()
    
    exception_count = len(exceptions)
    total_exception_duration = sum(ex.duration or 0 for ex in exceptions if ex.duration)
    
    daily_stat = DailyStats.query.filter_by(device_id=device_id, stats_date=stats_date).first()
    if not daily_stat:
        daily_stat = DailyStats(device_id=device_id, stats_date=stats_date)
    
    daily_stat.total_recognitions = total_recognitions
    daily_stat.success_recognitions = success_recognitions
    daily_stat.fail_recognitions = fail_recognitions
    daily_stat.success_rate = success_rate
    daily_stat.exception_count = exception_count
    daily_stat.total_exception_duration = total_exception_duration
    
    db.session.add(daily_stat)
    db.session.commit()
    
    return daily_stat


def update_monthly_stats(device_id, year=None, month=None):
    if year is None:
        year = date.today().year
    if month is None:
        month = date.today().month
    
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = date(year, month + 1, 1) - timedelta(days=1)
    
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())
    
    total_recognitions = RecognitionRecord.query.filter(
        RecognitionRecord.device_id == device_id,
        RecognitionRecord.recognition_time >= start_datetime,
        RecognitionRecord.recognition_time <= end_datetime
    ).count()
    
    success_recognitions = RecognitionRecord.query.filter(
        RecognitionRecord.device_id == device_id,
        RecognitionRecord.recognition_time >= start_datetime,
        RecognitionRecord.recognition_time <= end_datetime,
        RecognitionRecord.success == True
    ).count()
    
    fail_recognitions = total_recognitions - success_recognitions
    success_rate = (success_recognitions / total_recognitions * 100) if total_recognitions > 0 else 100.0
    
    exceptions = ExceptionReport.query.filter(
        ExceptionReport.device_id == device_id,
        ExceptionReport.start_time >= start_datetime,
        ExceptionReport.start_time <= end_datetime
    ).all()
    
    exception_count = len(exceptions)
    total_exception_duration = sum(ex.duration or 0 for ex in exceptions if ex.duration)
    
    monthly_stat = MonthlyStats.query.filter_by(device_id=device_id, stats_year=year, stats_month=month).first()
    if not monthly_stat:
        monthly_stat = MonthlyStats(device_id=device_id, stats_year=year, stats_month=month)
    
    monthly_stat.total_recognitions = total_recognitions
    monthly_stat.success_recognitions = success_recognitions
    monthly_stat.fail_recognitions = fail_recognitions
    monthly_stat.success_rate = success_rate
    monthly_stat.exception_count = exception_count
    monthly_stat.total_exception_duration = total_exception_duration
    
    db.session.add(monthly_stat)
    db.session.commit()
    
    return monthly_stat


@app.route('/api/dashboard/statistics', methods=['GET'])
def get_statistics():
    total_devices = Device.query.count()
    normal_devices = Device.query.filter_by(status='normal').count()
    fault_devices = Device.query.filter_by(status='fault').count()
    offline_devices = Device.query.filter_by(status='offline').count()
    signal_error_devices = Device.query.filter_by(status='signal_error').count()
    
    total_exceptions = ExceptionReport.query.count()
    unhandled_exceptions = ExceptionReport.query.filter_by(handled=False).count()
    
    total_work_orders = WorkOrder.query.count()
    pending_work_orders = WorkOrder.query.filter_by(status='pending').count()
    processing_work_orders = WorkOrder.query.filter_by(status='processing').count()
    
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': {
            'devices': {
                'total': total_devices,
                'normal': normal_devices,
                'fault': fault_devices,
                'offline': offline_devices,
                'signal_error': signal_error_devices
            },
            'exceptions': {
                'total': total_exceptions,
                'unhandled': unhandled_exceptions
            },
            'work_orders': {
                'total': total_work_orders,
                'pending': pending_work_orders,
                'processing': processing_work_orders
            }
        }
    })


@app.route('/api/recognition/record', methods=['POST'])
def create_recognition_record():
    data = request.get_json()
    
    device = Device.query.get(data['device_id'])
    if not device:
        return jsonify({'code': 1, 'message': '设备不存在'}), 400
    
    record = RecognitionRecord(
        device_id=data['device_id'],
        container_code=data.get('container_code'),
        success=data.get('success', True),
        fail_reason=data.get('fail_reason')
    )
    
    db.session.add(record)
    db.session.commit()
    
    today = date.today()
    update_daily_stats(data['device_id'], today)
    update_monthly_stats(data['device_id'], today.year, today.month)
    
    return jsonify({
        'code': 0,
        'message': '识别记录上报成功',
        'data': record.to_dict()
    }), 201


@app.route('/api/recognition/records', methods=['GET'])
def get_recognition_records():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    device_id = request.args.get('device_id', type=int)
    success = request.args.get('success')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = RecognitionRecord.query
    
    if device_id:
        query = query.filter(RecognitionRecord.device_id == device_id)
    if success is not None:
        query = query.filter(RecognitionRecord.success == (success == 'true'))
    if start_date:
        query = query.filter(RecognitionRecord.recognition_time >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(RecognitionRecord.recognition_time <= datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1))
    
    pagination = query.order_by(RecognitionRecord.recognition_time.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': {
            'items': [r.to_dict() for r in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }
    })


@app.route('/api/exceptions/<int:exception_id>/end', methods=['PUT'])
def end_exception(exception_id):
    exception = ExceptionReport.query.get_or_404(exception_id)
    data = request.get_json()
    
    exception.end_time = datetime.now()
    exception.calculate_duration()
    exception.handled = True
    exception.handled_at = exception.end_time
    exception.handler = data.get('handler')
    
    db.session.commit()
    
    today = date.today()
    update_daily_stats(exception.device_id, today)
    update_monthly_stats(exception.device_id, today.year, today.month)
    
    return jsonify({
        'code': 0,
        'message': '异常已结束',
        'data': exception.to_dict()
    })


@app.route('/api/stats/daily', methods=['GET'])
def get_daily_stats():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 30, type=int)
    device_id = request.args.get('device_id', type=int)
    work_zone = request.args.get('work_zone')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = DailyStats.query
    
    if device_id:
        query = query.filter(DailyStats.device_id == device_id)
    if work_zone:
        query = query.join(Device).filter(Device.work_zone == work_zone)
    if start_date:
        query = query.filter(DailyStats.stats_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(DailyStats.stats_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    pagination = query.order_by(DailyStats.stats_date.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': {
            'items': [s.to_dict() for s in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }
    })


@app.route('/api/stats/monthly', methods=['GET'])
def get_monthly_stats():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    device_id = request.args.get('device_id', type=int)
    work_zone = request.args.get('work_zone')
    year = request.args.get('year', type=int)
    
    query = MonthlyStats.query
    
    if device_id:
        query = query.filter(MonthlyStats.device_id == device_id)
    if work_zone:
        query = query.join(Device).filter(Device.work_zone == work_zone)
    if year:
        query = query.filter(MonthlyStats.stats_year == year)
    
    pagination = query.order_by(MonthlyStats.stats_year.desc(), MonthlyStats.stats_month.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': {
            'items': [s.to_dict() for s in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }
    })


@app.route('/api/stats/maintenance-devices', methods=['GET'])
def get_maintenance_devices():
    days = request.args.get('days', 7, type=int)
    limit = request.args.get('limit', 10, type=int)
    work_zone = request.args.get('work_zone')
    min_success_rate = request.args.get('min_success_rate', 90, type=float)
    
    end_date = date.today()
    start_date = end_date - timedelta(days=days - 1)
    
    subquery = db.session.query(
        DailyStats.device_id,
        func.avg(DailyStats.success_rate).label('avg_success_rate'),
        func.sum(DailyStats.exception_count).label('total_exception_count'),
        func.sum(DailyStats.total_exception_duration).label('total_duration')
    ).filter(
        DailyStats.stats_date >= start_date,
        DailyStats.stats_date <= end_date
    ).group_by(DailyStats.device_id).subquery()
    
    query = db.session.query(
        Device,
        subquery.c.avg_success_rate,
        subquery.c.total_exception_count,
        subquery.c.total_duration
    ).outerjoin(
        subquery, Device.id == subquery.c.device_id
    )
    
    if work_zone:
        query = query.filter(Device.work_zone == work_zone)
    
    results = query.all()
    
    device_scores = []
    for device, avg_rate, exp_count, total_duration in results:
        avg_rate = avg_rate or 100.0
        exp_count = exp_count or 0
        total_duration = total_duration or 0
        
        rate_score = avg_rate * 0.5
        availability_score = max(0, 100 - (total_duration / (days * 24 * 3600) * 100)) * 0.3
        stability_score = max(0, 100 - exp_count * 5) * 0.2
        
        efficiency_score = round(rate_score + availability_score + stability_score, 2)
        
        if efficiency_score < min_success_rate:
            device_scores.append({
                **device.to_dict(),
                'avg_success_rate': round(avg_rate, 2),
                'total_exception_count': exp_count,
                'total_exception_duration': total_duration,
                'efficiency_score': efficiency_score,
                'maintenance_priority': '高' if efficiency_score < 70 else '中' if efficiency_score < 85 else '低'
            })
    
    device_scores.sort(key=lambda x: x['efficiency_score'])
    device_scores = device_scores[:limit]
    
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': {
            'period_days': days,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'devices': device_scores
        }
    })


@app.route('/api/stats/refresh', methods=['POST'])
def refresh_stats():
    data = request.get_json()
    days = data.get('days', 7)
    
    end_date = date.today()
    start_date = end_date - timedelta(days=days - 1)
    
    devices = Device.query.all()
    
    for device in devices:
        current_date = start_date
        while current_date <= end_date:
            update_daily_stats(device.id, current_date)
            update_monthly_stats(device.id, current_date.year, current_date.month)
            current_date += timedelta(days=1)
    
    return jsonify({
        'code': 0,
        'message': f'已刷新最近{days}天的统计数据'
    })


with app.app_context():
    db.create_all()
    print('数据库初始化完成')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
