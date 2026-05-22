from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_db_connection, generate_order_no, init_db, HARBOR_AREAS, WORK_AREAS, FAULT_LEVELS
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

FAULT_TYPES = ['硬件故障', '软件故障', '网络故障', '电源故障', '传感器故障', '机械故障', '其他故障']
PRIORITY_LEVELS = ['紧急', '高', '一般', '低']
DEVICE_STATUS = ['正常', '故障', '维修中', '已修复']

if not os.path.exists('container_terminal.db'):
    init_db()

def success_response(data=None, message='操作成功', code=200):
    response = {
        'success': True,
        'code': code,
        'message': message,
        'timestamp': datetime.now().isoformat()
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), code

def error_response(message='操作失败', code=400, errors=None):
    response = {
        'success': False,
        'code': code,
        'message': message,
        'timestamp': datetime.now().isoformat()
    }
    if errors is not None:
        response['errors'] = errors
    return jsonify(response), code

def get_priority_weight(priority):
    weights = {'紧急': 4, '高': 3, '一般': 2, '低': 1}
    return weights.get(priority, 0)

def calculate_duration(start_time, end_time):
    try:
        start = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        return int((end - start).total_seconds() / 60)
    except:
        return None

@app.route('/api/enums', methods=['GET'])
def get_all_enums():
    return success_response({
        'fault_types': FAULT_TYPES,
        'priority_levels': PRIORITY_LEVELS,
        'device_status': DEVICE_STATUS,
        'harbor_areas': HARBOR_AREAS,
        'work_areas': WORK_AREAS,
        'fault_levels': FAULT_LEVELS
    }, '获取枚举值成功')

@app.route('/api/devices', methods=['GET'])
def get_devices():
    harbor_area = request.args.get('harbor_area')
    work_area = request.args.get('work_area')
    status = request.args.get('status')
    is_online = request.args.get('is_online')
    
    conn = get_db_connection()
    
    query = 'SELECT * FROM devices WHERE 1=1'
    params = []
    
    if harbor_area:
        query += ' AND harbor_area = ?'
        params.append(harbor_area)
    if work_area:
        query += ' AND work_area = ?'
        params.append(work_area)
    if status:
        query += ' AND status = ?'
        params.append(status)
    if is_online is not None:
        query += ' AND is_online = ?'
        params.append(1 if is_online == 'true' else 0)
    
    query += ' ORDER BY create_time DESC'
    
    devices = conn.execute(query, params).fetchall()
    conn.close()
    
    device_list = []
    for device in devices:
        device_dict = dict(device)
        device_dict['priority_weight'] = 0
        device_dict['has_pending_order'] = False
        device_list.append(device_dict)
    
    return success_response(device_list, '获取设备列表成功')

@app.route('/api/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    conn = get_db_connection()
    device = conn.execute('SELECT * FROM devices WHERE id = ?', (device_id,)).fetchone()
    
    if device is None:
        conn.close()
        return error_response('设备不存在', 404)
    
    device_dict = dict(device)
    
    pending_orders = conn.execute('''
        SELECT wo.* FROM work_orders wo 
        WHERE wo.device_id = ? AND wo.status = '待处理'
        ORDER BY CASE wo.priority WHEN '紧急' THEN 1 WHEN '高' THEN 2 WHEN '一般' THEN 3 ELSE 4 END
    ''', (device_id,)).fetchall()
    
    device_dict['pending_orders'] = [dict(o) for o in pending_orders]
    device_dict['has_pending_order'] = len(pending_orders) > 0
    
    records = conn.execute('''
        SELECT * FROM maintenance_records 
        WHERE device_id = ? ORDER BY handle_time DESC LIMIT 5
    ''', (device_id,)).fetchall()
    
    device_dict['recent_maintenance'] = [dict(r) for r in records]
    conn.close()
    
    return success_response(device_dict, '获取设备详情成功')

@app.route('/api/devices', methods=['POST'])
def add_device():
    data = request.get_json()
    required_fields = ['device_code', 'device_name', 'device_type', 'location', 'install_date']
    
    missing = [f for f in required_fields if f not in data]
    if missing:
        return error_response(f'缺少必填字段: {", ".join(missing)}', 400)

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO devices (device_code, device_name, device_type, device_model, 
                                protection_level, serial_number, commission_date,
                                harbor_area, work_area, location, install_date, status, is_online)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '正常', 1)
        ''', (data['device_code'], data['device_name'], data['device_type'],
              data.get('device_model'), data.get('protection_level'),
              data.get('serial_number'), data.get('commission_date'),
              data.get('harbor_area'), data.get('work_area'),
              data['location'], data['install_date']))
        conn.commit()
        device_id = cursor.lastrowid
        device = conn.execute('SELECT * FROM devices WHERE id = ?', (device_id,)).fetchone()
        conn.close()
        return success_response(dict(device), '设备添加成功', 201)
    except sqlite3.IntegrityError:
        conn.close()
        return error_response('设备编号已存在', 400)

@app.route('/api/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    data = request.get_json()
    conn = get_db_connection()
    device = conn.execute('SELECT * FROM devices WHERE id = ?', (device_id,)).fetchone()
    if device is None:
        conn.close()
        return error_response('设备不存在', 404)

    update_fields = []
    update_values = []
    allowed_fields = ['device_code', 'device_name', 'device_type', 'device_model', 
                      'protection_level', 'serial_number', 'commission_date',
                      'harbor_area', 'work_area', 'location', 'install_date', 
                      'status', 'is_online']
    
    for field in allowed_fields:
        if field in data:
            update_fields.append(f'{field} = ?')
            update_values.append(data[field])
    
    if update_fields:
        update_values.append(device_id)
        conn.execute(f'UPDATE devices SET {", ".join(update_fields)} WHERE id = ?', update_values)
        conn.commit()
    
    updated_device = conn.execute('SELECT * FROM devices WHERE id = ?', (device_id,)).fetchone()
    conn.close()
    return success_response(dict(updated_device), '设备更新成功')

@app.route('/api/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    conn = get_db_connection()
    device = conn.execute('SELECT * FROM devices WHERE id = ?', (device_id,)).fetchone()
    if device is None:
        conn.close()
        return error_response('设备不存在', 404)
    
    conn.execute('DELETE FROM devices WHERE id = ?', (device_id,))
    conn.commit()
    conn.close()
    return success_response(None, '设备删除成功')

@app.route('/api/devices/<int:device_id>/status', methods=['PUT'])
def update_device_status(device_id):
    data = request.get_json()
    if 'status' not in data:
        return error_response('缺少状态字段', 400)
    
    if data['status'] not in DEVICE_STATUS:
        return error_response(f'无效状态，有效值为: {DEVICE_STATUS}', 400)

    conn = get_db_connection()
    device = conn.execute('SELECT * FROM devices WHERE id = ?', (device_id,)).fetchone()
    if device is None:
        conn.close()
        return error_response('设备不存在', 404)

    conn.execute('UPDATE devices SET status = ? WHERE id = ?', (data['status'], device_id))
    conn.commit()
    updated_device = conn.execute('SELECT * FROM devices WHERE id = ?', (device_id,)).fetchone()
    conn.close()
    return success_response(dict(updated_device), '状态更新成功')

@app.route('/api/devices/<int:device_id>/heartbeat', methods=['PUT'])
def device_heartbeat(device_id):
    conn = get_db_connection()
    device = conn.execute('SELECT * FROM devices WHERE id = ?', (device_id,)).fetchone()
    if device is None:
        conn.close()
        return error_response('设备不存在', 404)
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn.execute('UPDATE devices SET is_online = 1, last_online_time = ? WHERE id = ?', (now, device_id))
    conn.commit()
    conn.close()
    return success_response({'device_id': device_id, 'last_online_time': now}, '心跳更新成功')

@app.route('/api/work-orders', methods=['GET'])
def get_work_orders():
    harbor_area = request.args.get('harbor_area')
    work_area = request.args.get('work_area')
    fault_type = request.args.get('fault_type')
    fault_level = request.args.get('fault_level')
    priority = request.args.get('priority')
    status = request.args.get('status')
    device_id = request.args.get('device_id')
    
    conn = get_db_connection()
    
    query = '''
        SELECT wo.*, d.device_name, d.device_code, d.harbor_area, d.work_area, d.location, d.status as device_status, d.is_online
        FROM work_orders wo
        JOIN devices d ON wo.device_id = d.id
        WHERE 1=1
    '''
    params = []
    
    if harbor_area:
        query += ' AND d.harbor_area = ?'
        params.append(harbor_area)
    if work_area:
        query += ' AND d.work_area = ?'
        params.append(work_area)
    if fault_type:
        query += ' AND wo.fault_type = ?'
        params.append(fault_type)
    if fault_level:
        query += ' AND wo.fault_level = ?'
        params.append(fault_level)
    if priority:
        query += ' AND wo.priority = ?'
        params.append(priority)
    if status:
        query += ' AND wo.status = ?'
        params.append(status)
    if device_id:
        query += ' AND wo.device_id = ?'
        params.append(device_id)
    
    query += '''
        ORDER BY CASE wo.priority 
            WHEN '紧急' THEN 1 
            WHEN '高' THEN 2 
            WHEN '一般' THEN 3 
            ELSE 4 
        END, wo.report_time DESC
    '''
    
    orders = conn.execute(query, params).fetchall()
    conn.close()
    
    order_list = []
    for order in orders:
        order_dict = dict(order)
        order_dict['priority_weight'] = get_priority_weight(order['priority'])
        order_dict['is_high_priority'] = order['priority'] in ['紧急', '高']
        order_list.append(order_dict)
    
    return success_response(order_list, '获取工单列表成功')

@app.route('/api/work-orders/<order_no>', methods=['GET'])
def get_work_order(order_no):
    conn = get_db_connection()
    order = conn.execute('''
        SELECT wo.*, d.device_name, d.device_code, d.harbor_area, d.work_area, d.location, d.status as device_status, d.is_online
        FROM work_orders wo
        JOIN devices d ON wo.device_id = d.id
        WHERE wo.order_no = ?
    ''', (order_no,)).fetchone()
    conn.close()
    
    if order is None:
        return error_response('工单不存在', 404)
    
    order_dict = dict(order)
    order_dict['priority_weight'] = get_priority_weight(order['priority'])
    order_dict['is_high_priority'] = order['priority'] in ['紧急', '高']
    
    return success_response(order_dict, '获取工单详情成功')

@app.route('/api/work-orders', methods=['POST'])
def create_work_order():
    data = request.get_json()
    required_fields = ['device_id', 'fault_type', 'fault_description', 'reporter']
    
    missing = [f for f in required_fields if f not in data]
    if missing:
        return error_response(f'缺少必填字段: {", ".join(missing)}', 400)

    if data['fault_type'] not in FAULT_TYPES:
        return error_response(f'无效故障类型，有效值为: {FAULT_TYPES}', 400)
    
    priority = data.get('priority', '一般')
    if priority not in PRIORITY_LEVELS:
        return error_response(f'无效优先级，有效值为: {PRIORITY_LEVELS}', 400)
    
    fault_level = data.get('fault_level', '一般')
    if fault_level not in FAULT_LEVELS:
        return error_response(f'无效故障等级，有效值为: {FAULT_LEVELS}', 400)

    conn = get_db_connection()
    device = conn.execute('SELECT * FROM devices WHERE id = ?', (data['device_id'],)).fetchone()
    if device is None:
        conn.close()
        return error_response('设备不存在', 404)

    order_no = generate_order_no()
    report_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    before_status = device['status']

    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO work_orders (order_no, device_id, fault_type, fault_level, priority, 
                                fault_description, reporter, report_time, status, before_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, '待处理', ?)
    ''', (order_no, data['device_id'], data['fault_type'], fault_level, priority,
          data['fault_description'], data['reporter'], report_time, before_status))
    conn.commit()

    conn.execute('UPDATE devices SET status = ? WHERE id = ?', ('故障', data['device_id']))
    conn.commit()

    order = conn.execute('''
        SELECT wo.*, d.device_name, d.device_code, d.harbor_area, d.work_area, d.location
        FROM work_orders wo
        JOIN devices d ON wo.device_id = d.id
        WHERE wo.order_no = ?
    ''', (order_no,)).fetchone()
    conn.close()

    return success_response(dict(order), '故障上报成功', 201)

@app.route('/api/work-orders/<order_no>/handle', methods=['PUT'])
def handle_work_order(order_no):
    data = request.get_json()
    required_fields = ['handler', 'handle_result', 'device_status']
    
    missing = [f for f in required_fields if f not in data]
    if missing:
        return error_response(f'缺少必填字段: {", ".join(missing)}', 400)

    if data['device_status'] not in DEVICE_STATUS:
        return error_response(f'无效设备状态，有效值为: {DEVICE_STATUS}', 400)

    conn = get_db_connection()
    order = conn.execute('SELECT * FROM work_orders WHERE order_no = ?', (order_no,)).fetchone()
    if order is None:
        conn.close()
        return error_response('工单不存在', 404)
    
    if order['status'] == '已处理':
        conn.close()
        return error_response('工单已处理，无需重复操作', 400)

    handle_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    handle_duration = calculate_duration(order['report_time'], handle_time)

    conn.execute('''
        UPDATE work_orders 
        SET status = '已处理', handler = ?, handle_time = ?, handle_duration = ?, 
            handle_result = ?, after_status = ?
        WHERE order_no = ?
    ''', (data['handler'], handle_time, handle_duration, data['handle_result'], 
          data['device_status'], order_no))
    conn.commit()

    conn.execute('UPDATE devices SET status = ? WHERE id = ?', 
                 (data['device_status'], order['device_id']))
    conn.commit()

    device = conn.execute('SELECT * FROM devices WHERE id = ?', (order['device_id'],)).fetchone()

    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO maintenance_records 
        (order_no, device_id, device_name, device_code, harbor_area, work_area, 
         fault_type, fault_level, priority, fault_description, reporter, report_time, 
         handler, handle_time, handle_duration, handle_result, before_status, after_status,
         cost, remark)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (order_no, order['device_id'], device['device_name'], device['device_code'],
          device['harbor_area'], device['work_area'], order['fault_type'], order['fault_level'],
          order['priority'], order['fault_description'], order['reporter'], order['report_time'],
          data['handler'], handle_time, handle_duration, data['handle_result'],
          order['before_status'], data['device_status'],
          data.get('cost', 0), data.get('remark', '')))
    conn.commit()

    updated_order = conn.execute('''
        SELECT wo.*, d.device_name, d.device_code, d.harbor_area, d.work_area, d.location
        FROM work_orders wo
        JOIN devices d ON wo.device_id = d.id
        WHERE wo.order_no = ?
    ''', (order_no,)).fetchone()
    conn.close()

    return success_response(dict(updated_order), '工单处理成功')

@app.route('/api/maintenance-records', methods=['GET'])
def get_maintenance_records():
    harbor_area = request.args.get('harbor_area')
    work_area = request.args.get('work_area')
    fault_type = request.args.get('fault_type')
    fault_level = request.args.get('fault_level')
    device_id = request.args.get('device_id')
    
    conn = get_db_connection()
    
    query = 'SELECT * FROM maintenance_records WHERE 1=1'
    params = []
    
    if harbor_area:
        query += ' AND harbor_area = ?'
        params.append(harbor_area)
    if work_area:
        query += ' AND work_area = ?'
        params.append(work_area)
    if fault_type:
        query += ' AND fault_type = ?'
        params.append(fault_type)
    if fault_level:
        query += ' AND fault_level = ?'
        params.append(fault_level)
    if device_id:
        query += ' AND device_id = ?'
        params.append(device_id)
    
    query += ' ORDER BY handle_time DESC'
    
    records = conn.execute(query, params).fetchall()
    conn.close()
    
    return success_response([dict(r) for r in records], '获取维修记录成功')

@app.route('/api/maintenance-records/<int:record_id>', methods=['GET'])
def get_maintenance_record(record_id):
    conn = get_db_connection()
    record = conn.execute('SELECT * FROM maintenance_records WHERE id = ?', (record_id,)).fetchone()
    conn.close()
    if record is None:
        return error_response('记录不存在', 404)
    return success_response(dict(record), '获取维修记录详情成功')

@app.route('/api/maintenance-records/device/<int:device_id>', methods=['GET'])
def get_device_maintenance_records(device_id):
    conn = get_db_connection()
    records = conn.execute('''
        SELECT * FROM maintenance_records 
        WHERE device_id = ? ORDER BY handle_time DESC
    ''', (device_id,)).fetchall()
    conn.close()
    return success_response([dict(r) for r in records], '获取设备维修记录成功')

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    conn = get_db_connection()
    
    total_devices = conn.execute('SELECT COUNT(*) as count FROM devices').fetchone()['count']
    online_devices = conn.execute('SELECT COUNT(*) as count FROM devices WHERE is_online = 1').fetchone()['count']
    normal_devices = conn.execute('SELECT COUNT(*) as count FROM devices WHERE status = "正常"').fetchone()['count']
    fault_devices = conn.execute('SELECT COUNT(*) as count FROM devices WHERE status = "故障"').fetchone()['count']
    repairing_devices = conn.execute('SELECT COUNT(*) as count FROM devices WHERE status = "维修中"').fetchone()['count']
    pending_orders = conn.execute('SELECT COUNT(*) as count FROM work_orders WHERE status = "待处理"').fetchone()['count']
    urgent_orders = conn.execute('SELECT COUNT(*) as count FROM work_orders WHERE status = "待处理" AND priority = "紧急"').fetchone()['count']
    total_records = conn.execute('SELECT COUNT(*) as count FROM maintenance_records').fetchone()['count']
    
    online_rate = round((online_devices / total_devices * 100), 2) if total_devices > 0 else 0
    health_rate = round((normal_devices / total_devices * 100), 2) if total_devices > 0 else 0
    
    harbor_stats = []
    for harbor in HARBOR_AREAS:
        count = conn.execute('SELECT COUNT(*) as count FROM devices WHERE harbor_area = ?', (harbor,)).fetchone()['count']
        if count > 0:
            normal = conn.execute('SELECT COUNT(*) as count FROM devices WHERE harbor_area = ? AND status = "正常"', (harbor,)).fetchone()['count']
            harbor_stats.append({
                'harbor_area': harbor,
                'total': count,
                'normal_count': normal,
                'health_rate': round((normal / count * 100), 2)
            })
    
    fault_type_stats = []
    for ftype in FAULT_TYPES:
        count = conn.execute('SELECT COUNT(*) as count FROM maintenance_records WHERE fault_type = ?', (ftype,)).fetchone()['count']
        if count > 0:
            fault_type_stats.append({'fault_type': ftype, 'count': count})
    
    conn.close()
    
    return success_response({
        'total_devices': total_devices,
        'online_devices': online_devices,
        'online_rate': online_rate,
        'normal_devices': normal_devices,
        'health_rate': health_rate,
        'fault_devices': fault_devices,
        'repairing_devices': repairing_devices,
        'pending_orders': pending_orders,
        'urgent_orders': urgent_orders,
        'total_maintenance_records': total_records,
        'harbor_stats': harbor_stats,
        'fault_type_stats': fault_type_stats
    }, '获取统计数据成功')

@app.route('/api/dashboard/availability', methods=['GET'])
def get_availability_stats():
    conn = get_db_connection()
    
    total_devices = conn.execute('SELECT COUNT(*) as count FROM devices').fetchone()['count']
    online_devices = conn.execute('SELECT COUNT(*) as count FROM devices WHERE is_online = 1').fetchone()['count']
    normal_devices = conn.execute('SELECT COUNT(*) as count FROM devices WHERE status = "正常"').fetchone()['count']
    
    online_rate = round((online_devices / total_devices * 100), 2) if total_devices > 0 else 0
    health_rate = round((normal_devices / total_devices * 100), 2) if total_devices > 0 else 0
    availability_rate = round(((online_devices + normal_devices) / (total_devices * 2) * 100), 2) if total_devices > 0 else 0
    
    area_stats = []
    for area in WORK_AREAS:
        total = conn.execute('SELECT COUNT(*) as count FROM devices WHERE work_area = ?', (area,)).fetchone()['count']
        if total > 0:
            online = conn.execute('SELECT COUNT(*) as count FROM devices WHERE work_area = ? AND is_online = 1', (area,)).fetchone()['count']
            normal = conn.execute('SELECT COUNT(*) as count FROM devices WHERE work_area = ? AND status = "正常"', (area,)).fetchone()['count']
            area_stats.append({
                'work_area': area,
                'total': total,
                'online': online,
                'online_rate': round((online / total * 100), 2),
                'normal': normal,
                'health_rate': round((normal / total * 100), 2)
            })
    
    conn.close()
    
    return success_response({
        'total_devices': total_devices,
        'online_devices': online_devices,
        'online_rate': online_rate,
        'normal_devices': normal_devices,
        'health_rate': health_rate,
        'availability_rate': availability_rate,
        'area_stats': area_stats
    }, '获取设备完好率统计成功')

@app.route('/api/dashboard/trend', methods=['GET'])
def get_trend_data():
    conn = get_db_connection()
    
    daily_orders = conn.execute('''
        SELECT DATE(report_time) as date, COUNT(*) as count 
        FROM work_orders 
        WHERE report_time >= DATE('now', '-30 days')
        GROUP BY DATE(report_time)
        ORDER BY date
    ''').fetchall()
    
    daily_records = conn.execute('''
        SELECT DATE(handle_time) as date, COUNT(*) as count 
        FROM maintenance_records 
        WHERE handle_time >= DATE('now', '-30 days')
        GROUP BY DATE(handle_time)
        ORDER BY date
    ''').fetchall()
    
    conn.close()
    
    return success_response({
        'daily_orders': [dict(d) for d in daily_orders],
        'daily_repairs': [dict(d) for d in daily_records]
    }, '获取趋势数据成功')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
