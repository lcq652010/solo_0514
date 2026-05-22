from datetime import datetime, date, timedelta
from io import StringIO
import csv
from flask import make_response
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from models import db, Device, FaultOrder, MaintenanceRecord

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)

FAULT_TYPES = ['打印卡纸', '无法读卡', '网络异常', '系统死机']

def generate_order_no():
    today = datetime.now().strftime('%Y%m%d')
    last_order = FaultOrder.query.filter(
        FaultOrder.order_no.like(f'GZ{today}%')
    ).order_by(FaultOrder.order_no.desc()).first()
    
    if last_order:
        last_num = int(last_order.order_no[-4:])
        new_num = str(last_num + 1).zfill(4)
    else:
        new_num = '0001'
    
    return f'GZ{today}{new_num}'

@app.route('/api/devices', methods=['POST'])
def add_device():
    data = request.get_json()
    
    if not all(key in data for key in ['device_code', 'device_name', 'hospital', 'floor', 'location', 'install_date', 'online_date']):
        return jsonify({'code': 400, 'message': '缺少必要参数'}), 400
    
    if Device.query.filter_by(device_code=data['device_code']).first():
        return jsonify({'code': 400, 'message': '设备编号已存在'}), 400
    
    if data.get('status') and data['status'] not in ['正常', '故障', '维修中', '离线']:
        return jsonify({'code': 400, 'message': '设备状态无效'}), 400
    
    device = Device(
        device_code=data['device_code'],
        device_name=data['device_name'],
        hospital=data['hospital'],
        floor=data['floor'],
        location=data['location'],
        install_date=datetime.strptime(data['install_date'], '%Y-%m-%d').date(),
        online_date=datetime.strptime(data['online_date'], '%Y-%m-%d').date(),
        status=data.get('status', '正常')
    )
    
    db.session.add(device)
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '设备添加成功', 'data': device.to_dict()})

@app.route('/api/devices', methods=['GET'])
def get_devices():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    hospital = request.args.get('hospital')
    floor = request.args.get('floor')
    keyword = request.args.get('keyword')
    
    query = Device.query
    
    if status:
        query = query.filter_by(status=status)
    if hospital:
        query = query.filter_by(hospital=hospital)
    if floor:
        query = query.filter_by(floor=floor)
    
    if keyword:
        query = query.filter(
            (Device.device_code.like(f'%{keyword}%')) |
            (Device.device_name.like(f'%{keyword}%')) |
            (Device.hospital.like(f'%{keyword}%')) |
            (Device.floor.like(f'%{keyword}%')) |
            (Device.location.like(f'%{keyword}%'))
        )
    
    pagination = query.order_by(Device.create_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': {
            'devices': [d.to_dict() for d in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }
    })

@app.route('/api/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    device = Device.query.get(device_id)
    if not device:
        return jsonify({'code': 404, 'message': '设备不存在'}), 404
    
    return jsonify({'code': 200, 'message': '获取成功', 'data': device.to_dict()})

@app.route('/api/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    device = Device.query.get(device_id)
    if not device:
        return jsonify({'code': 404, 'message': '设备不存在'}), 404
    
    data = request.get_json()
    
    if 'device_code' in data:
        existing = Device.query.filter_by(device_code=data['device_code']).first()
        if existing and existing.id != device_id:
            return jsonify({'code': 400, 'message': '设备编号已存在'}), 400
        device.device_code = data['device_code']
    
    if 'device_name' in data:
        device.device_name = data['device_name']
    if 'hospital' in data:
        device.hospital = data['hospital']
    if 'floor' in data:
        device.floor = data['floor']
    if 'location' in data:
        device.location = data['location']
    if 'install_date' in data:
        device.install_date = datetime.strptime(data['install_date'], '%Y-%m-%d').date()
    if 'online_date' in data:
        device.online_date = datetime.strptime(data['online_date'], '%Y-%m-%d').date()
    if 'status' in data:
        if data['status'] not in ['正常', '故障', '维修中', '离线']:
            return jsonify({'code': 400, 'message': '设备状态无效'}), 400
        device.status = data['status']
    
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '设备更新成功', 'data': device.to_dict()})

@app.route('/api/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    device = Device.query.get(device_id)
    if not device:
        return jsonify({'code': 404, 'message': '设备不存在'}), 404
    
    FaultOrder.query.filter_by(device_id=device_id).delete()
    MaintenanceRecord.query.filter_by(device_id=device_id).delete()
    
    db.session.delete(device)
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '设备删除成功'})

def check_repeat_fault(device_id, fault_type, report_time):
    seven_days_ago = report_time - timedelta(days=7)
    previous_faults = FaultOrder.query.filter(
        FaultOrder.device_id == device_id,
        FaultOrder.fault_type == fault_type,
        FaultOrder.report_time >= seven_days_ago,
        FaultOrder.report_time < report_time
    ).order_by(FaultOrder.report_time.desc()).all()
    
    if previous_faults:
        return True, len(previous_faults)
    return False, 0

@app.route('/api/fault-orders', methods=['POST'])
def report_fault():
    data = request.get_json()
    
    if not all(key in data for key in ['device_id', 'fault_type', 'fault_description', 'reporter']):
        return jsonify({'code': 400, 'message': '缺少必要参数'}), 400
    
    if data['fault_type'] not in FAULT_TYPES:
        return jsonify({'code': 400, 'message': f'故障类型无效，支持的类型：{", ".join(FAULT_TYPES)}'}), 400
    
    device = Device.query.get(data['device_id'])
    if not device:
        return jsonify({'code': 404, 'message': '设备不存在'}), 404
    
    order_no = generate_order_no()
    report_time = datetime.now()
    
    is_repeat, repeat_count = check_repeat_fault(data['device_id'], data['fault_type'], report_time)
    
    fault_order = FaultOrder(
        order_no=order_no,
        device_id=data['device_id'],
        fault_type=data['fault_type'],
        fault_description=data['fault_description'],
        reporter=data['reporter'],
        report_time=report_time,
        is_repeat_fault=is_repeat,
        repeat_count=repeat_count
    )
    
    device.status = '故障'
    
    db.session.add(fault_order)
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '故障上报成功', 'data': fault_order.to_dict()})

@app.route('/api/fault-orders', methods=['GET'])
def get_fault_orders():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    fault_type = request.args.get('fault_type')
    device_id = request.args.get('device_id', type=int)
    
    query = FaultOrder.query
    
    if status:
        query = query.filter_by(status=status)
    if fault_type:
        query = query.filter_by(fault_type=fault_type)
    if device_id:
        query = query.filter_by(device_id=device_id)
    
    pagination = query.order_by(FaultOrder.report_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': {
            'orders': [o.to_dict() for o in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }
    })

@app.route('/api/fault-orders/<string:order_no>/handle', methods=['PUT'])
def handle_fault_order(order_no):
    fault_order = FaultOrder.query.filter_by(order_no=order_no).first()
    if not fault_order:
        return jsonify({'code': 404, 'message': '工单不存在'}), 404
    
    data = request.get_json()
    
    if not all(key in data for key in ['handler', 'handle_result']):
        return jsonify({'code': 400, 'message': '缺少必要参数'}), 400
    
    fault_order.handler = data['handler']
    fault_order.handle_result = data['handle_result']
    fault_order.handle_time = datetime.now()
    fault_order.status = '已处理'
    
    device = Device.query.get(fault_order.device_id)
    if device:
        device.status = '正常'
        device.last_maintenance = datetime.now()
    
    maintenance = MaintenanceRecord(
        device_id=fault_order.device_id,
        order_no=order_no,
        maintenance_type='故障维修',
        maintenance_content=data['handle_result'],
        maintenance_person=data['handler'],
        cost=data.get('cost', 0.0)
    )
    
    db.session.add(maintenance)
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '工单处理成功', 'data': fault_order.to_dict()})

@app.route('/api/maintenance-records', methods=['GET'])
def get_maintenance_records():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    device_id = request.args.get('device_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = MaintenanceRecord.query
    
    if device_id:
        query = query.filter_by(device_id=device_id)
    if start_date:
        query = query.filter(MaintenanceRecord.maintenance_time >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(MaintenanceRecord.maintenance_time <= datetime.strptime(end_date, '%Y-%m-%d 23:59:59'))
    
    pagination = query.order_by(MaintenanceRecord.maintenance_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': {
            'records': [r.to_dict() for r in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }
    })

@app.route('/api/maintenance-records', methods=['POST'])
def add_maintenance_record():
    data = request.get_json()
    
    if not all(key in data for key in ['device_id', 'maintenance_type', 'maintenance_content', 'maintenance_person']):
        return jsonify({'code': 400, 'message': '缺少必要参数'}), 400
    
    device = Device.query.get(data['device_id'])
    if not device:
        return jsonify({'code': 404, 'message': '设备不存在'}), 404
    
    maintenance = MaintenanceRecord(
        device_id=data['device_id'],
        maintenance_type=data['maintenance_type'],
        maintenance_content=data['maintenance_content'],
        maintenance_person=data['maintenance_person'],
        cost=data.get('cost', 0.0),
        remarks=data.get('remarks', '')
    )
    
    device.last_maintenance = datetime.now()
    
    db.session.add(maintenance)
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '运维记录添加成功', 'data': maintenance.to_dict()})

@app.route('/api/fault-types', methods=['GET'])
def get_fault_types():
    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': FAULT_TYPES
    })

@app.route('/api/devices/hospitals', methods=['GET'])
def get_hospitals():
    hospitals = db.session.query(Device.hospital).distinct().all()
    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': [h[0] for h in hospitals]
    })

@app.route('/api/devices/floors', methods=['GET'])
def get_floors():
    hospital = request.args.get('hospital')
    query = db.session.query(Device.floor).distinct()
    if hospital:
        query = query.filter_by(hospital=hospital)
    floors = query.all()
    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': [f[0] for f in floors]
    })

@app.route('/api/dashboard/statistics', methods=['GET'])
def get_statistics():
    total_devices = Device.query.count()
    normal_devices = Device.query.filter_by(status='正常').count()
    fault_devices = Device.query.filter_by(status='故障').count()
    repairing_devices = Device.query.filter_by(status='维修中').count()
    offline_devices = Device.query.filter_by(status='离线').count()
    
    pending_orders = FaultOrder.query.filter_by(status='待处理').count()
    total_orders = FaultOrder.query.count()
    
    total_maintenance = MaintenanceRecord.query.count()
    
    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': {
            'total_devices': total_devices,
            'normal_devices': normal_devices,
            'fault_devices': fault_devices,
            'repairing_devices': repairing_devices,
            'offline_devices': offline_devices,
            'pending_orders': pending_orders,
            'total_orders': total_orders,
            'total_maintenance': total_maintenance
        }
    })

@app.route('/api/fault-orders/type-ranking', methods=['GET'])
def get_fault_type_ranking():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = db.session.query(
        FaultOrder.fault_type,
        db.func.count(FaultOrder.id).label('count')
    )
    
    if start_date:
        query = query.filter(FaultOrder.report_time >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(FaultOrder.report_time <= datetime.strptime(end_date + ' 23:59:59', '%Y-%m-%d %H:%M:%S'))
    
    fault_counts = query.group_by(FaultOrder.fault_type).order_by(db.desc('count')).all()
    
    ranking = []
    total_count = sum(fc[1] for fc in fault_counts)
    
    for idx, (fault_type, count) in enumerate(fault_counts, 1):
        percentage = round((count / total_count * 100), 2) if total_count > 0 else 0
        ranking.append({
            'rank': idx,
            'fault_type': fault_type,
            'count': count,
            'percentage': percentage
        })
    
    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': {
            'ranking': ranking,
            'total': total_count
        }
    })

@app.route('/api/fault-orders/repeat-list', methods=['GET'])
def get_repeat_fault_list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    device_id = request.args.get('device_id', type=int)
    
    query = FaultOrder.query.filter_by(is_repeat_fault=True)
    
    if device_id:
        query = query.filter_by(device_id=device_id)
    
    pagination = query.order_by(FaultOrder.report_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': {
            'orders': [o.to_dict() for o in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }
    })

@app.route('/api/devices/floor-availability/export', methods=['GET'])
def export_floor_availability():
    year = request.args.get('year', type=int, default=datetime.now().year)
    month = request.args.get('month', type=int, default=datetime.now().month)
    hospital = request.args.get('hospital')
    
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(seconds=1)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(seconds=1)
    
    days_in_month = (end_date - start_date).days + 1
    
    device_query = Device.query
    if hospital:
        device_query = device_query.filter_by(hospital=hospital)
    
    devices = device_query.all()
    
    floor_data = {}
    for device in devices:
        key = (device.hospital, device.floor)
        if key not in floor_data:
            floor_data[key] = {
                'hospital': device.hospital,
                'floor': device.floor,
                'total_devices': 0,
                'total_fault_duration': 0,
                'fault_count': 0
            }
        floor_data[key]['total_devices'] += 1
    
    fault_orders = FaultOrder.query.filter(
        FaultOrder.report_time >= start_date,
        FaultOrder.report_time <= end_date
    ).all()
    
    for fault in fault_orders:
        device = fault.device
        if device:
            key = (device.hospital, device.floor)
            if key in floor_data:
                floor_data[key]['fault_count'] += 1
                if fault.handle_time:
                    duration = (fault.handle_time - fault.report_time).total_seconds() / 3600
                    floor_data[key]['total_fault_duration'] += duration
    
    si = StringIO()
    cw = csv.writer(si)
    
    headers = ['院区', '楼层', '设备总数', '故障次数', '总故障时长(小时)', '平均故障时长(小时)', '月度可用性(%)']
    cw.writerow(headers)
    
    for key, data in floor_data.items():
        total_available_hours = data['total_devices'] * days_in_month * 24
        fault_hours = data['total_fault_duration']
        availability = round(((total_available_hours - fault_hours) / total_available_hours * 100), 2) if total_available_hours > 0 else 100
        avg_duration = round(data['total_fault_duration'] / data['fault_count'], 2) if data['fault_count'] > 0 else 0
        
        row = [
            data['hospital'],
            data['floor'],
            data['total_devices'],
            data['fault_count'],
            round(data['total_fault_duration'], 2),
            avg_duration,
            availability
        ]
        cw.writerow(row)
    
    output = make_response(si.getvalue())
    output.headers['Content-Disposition'] = f'attachment; filename=floor_availability_{year}{month:02d}.csv'
    output.headers['Content-type'] = 'text/csv; charset=utf-8'
    
    return output

@app.route('/api/devices/floor-availability', methods=['GET'])
def get_floor_availability():
    year = request.args.get('year', type=int, default=datetime.now().year)
    month = request.args.get('month', type=int, default=datetime.now().month)
    hospital = request.args.get('hospital')
    
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(seconds=1)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(seconds=1)
    
    days_in_month = (end_date - start_date).days + 1
    
    device_query = Device.query
    if hospital:
        device_query = device_query.filter_by(hospital=hospital)
    
    devices = device_query.all()
    
    floor_data = {}
    for device in devices:
        key = (device.hospital, device.floor)
        if key not in floor_data:
            floor_data[key] = {
                'hospital': device.hospital,
                'floor': device.floor,
                'total_devices': 0,
                'total_fault_duration': 0,
                'fault_count': 0
            }
        floor_data[key]['total_devices'] += 1
    
    fault_orders = FaultOrder.query.filter(
        FaultOrder.report_time >= start_date,
        FaultOrder.report_time <= end_date
    ).all()
    
    for fault in fault_orders:
        device = fault.device
        if device:
            key = (device.hospital, device.floor)
            if key in floor_data:
                floor_data[key]['fault_count'] += 1
                if fault.handle_time:
                    duration = (fault.handle_time - fault.report_time).total_seconds() / 3600
                    floor_data[key]['total_fault_duration'] += duration
    
    result = []
    for key, data in floor_data.items():
        total_available_hours = data['total_devices'] * days_in_month * 24
        fault_hours = data['total_fault_duration']
        availability = round(((total_available_hours - fault_hours) / total_available_hours * 100), 2) if total_available_hours > 0 else 100
        avg_duration = round(data['total_fault_duration'] / data['fault_count'], 2) if data['fault_count'] > 0 else 0
        
        result.append({
            'hospital': data['hospital'],
            'floor': data['floor'],
            'total_devices': data['total_devices'],
            'fault_count': data['fault_count'],
            'total_fault_duration': round(data['total_fault_duration'], 2),
            'avg_fault_duration': avg_duration,
            'availability': availability,
            'year': year,
            'month': month
        })
    
    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': result
    })

with app.app_context():
    db.create_all()
    print('数据库初始化完成')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
