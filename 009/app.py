from flask import Flask, request, g
from flask_cors import CORS
from models import get_db, init_db, generate_order_no, FAULT_CATEGORIES, PRIORITY_LEVELS, PRIORITY_COLORS, GASOLINE_TYPES, STATION_AREAS, MAINTENANCE_ACTIONS
from datetime import datetime
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from migrate_db import migrate

app = Flask(__name__)
CORS(app)

with app.app_context():
    migrate()
    init_db()

def success_response(data=None, message='success', code=200):
    return {
        'code': code,
        'message': message,
        'data': data,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def error_response(message='error', code=400, details=None):
    return {
        'code': code,
        'message': message,
        'details': details,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

@app.route('/api/devices', methods=['GET'])
def get_devices():
    conn = get_db()
    cursor = conn.cursor()
    
    status = request.args.get('status')
    station_area = request.args.get('station_area')
    gasoline_type = request.args.get('gasoline_type')
    
    query = 'SELECT * FROM devices WHERE 1=1'
    params = []
    
    if status:
        query += ' AND status = ?'
        params.append(status)
    
    if station_area:
        query += ' AND station_area = ?'
        params.append(station_area)
    
    if gasoline_type:
        query += ' AND gasoline_type = ?'
        params.append(gasoline_type)
    
    query += ' ORDER BY create_time DESC'
    
    cursor.execute(query, params)
    devices = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return success_response(devices)

@app.route('/api/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM devices WHERE id = ?', (device_id,))
    device = cursor.fetchone()
    
    if not device:
        conn.close()
        return error_response('设备不存在', 404), 404
    
    device_dict = dict(device)
    
    cursor.execute('''
        SELECT fr.* FROM fault_reports fr
        WHERE fr.device_id = ? ORDER BY fr.report_time DESC LIMIT 5
    ''', (device_id,))
    device_dict['recent_faults'] = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute('''
        SELECT mr.* FROM maintenance_records mr
        WHERE mr.device_id = ? ORDER BY mr.create_time DESC LIMIT 5
    ''', (device_id,))
    device_dict['recent_maintenance'] = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return success_response(device_dict)

@app.route('/api/devices', methods=['POST'])
def add_device():
    data = request.get_json()
    required_fields = ['device_no', 'device_name', 'device_type', 'location']
    for field in required_fields:
        if field not in data:
            return error_response(f'缺少必填字段: {field}', 400), 400
    
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO devices (device_no, device_name, device_type, device_model, control_version, 
                                station_area, gasoline_type, location, status, install_date, enable_date, description, update_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['device_no'],
            data['device_name'],
            data['device_type'],
            data.get('device_model'),
            data.get('control_version'),
            data.get('station_area'),
            data.get('gasoline_type'),
            data['location'],
            data.get('status', 'normal'),
            data.get('install_date'),
            data.get('enable_date'),
            data.get('description'),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        conn.commit()
        device_id = cursor.lastrowid
        conn.close()
        return success_response({'id': device_id}, '设备添加成功')
    except Exception as e:
        conn.close()
        return error_response(f'添加失败: {str(e)}', 500), 500

@app.route('/api/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM devices WHERE id = ?', (device_id,))
    if not cursor.fetchone():
        conn.close()
        return error_response('设备不存在', 404), 404
    
    update_fields = []
    update_values = []
    for field in ['device_no', 'device_name', 'device_type', 'device_model', 'control_version',
                  'station_area', 'gasoline_type', 'location', 'status', 'install_date', 'enable_date', 'description']:
        if field in data:
            update_fields.append(f'{field} = ?')
            update_values.append(data[field])
    
    update_fields.append('update_time = ?')
    update_values.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    update_values.append(device_id)
    
    cursor.execute(f'''
        UPDATE devices SET {', '.join(update_fields)} WHERE id = ?
    ''', update_values)
    conn.commit()
    conn.close()
    return success_response(None, '设备更新成功')

@app.route('/api/devices/<int:device_id>/status', methods=['PUT'])
def update_device_status(device_id):
    data = request.get_json()
    status = data.get('status')
    valid_statuses = ['normal', 'fault', 'maintaining', 'repaired']
    if status not in valid_statuses:
        return error_response(f'无效状态，有效状态: {valid_statuses}', 400), 400
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM devices WHERE id = ?', (device_id,))
    if not cursor.fetchone():
        conn.close()
        return error_response('设备不存在', 404), 404
    
    cursor.execute('''
        UPDATE devices SET status = ?, update_time = ? WHERE id = ?
    ''', (status, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), device_id))
    conn.commit()
    conn.close()
    return success_response(None, '状态更新成功')

@app.route('/api/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM devices WHERE id = ?', (device_id,))
    if not cursor.fetchone():
        conn.close()
        return error_response('设备不存在', 404), 404
    
    cursor.execute('DELETE FROM devices WHERE id = ?', (device_id,))
    conn.commit()
    conn.close()
    return success_response(None, '设备删除成功')

@app.route('/api/fault-reports', methods=['GET'])
def get_fault_reports():
    conn = get_db()
    cursor = conn.cursor()
    
    status = request.args.get('status')
    priority = request.args.get('priority')
    fault_category = request.args.get('fault_category')
    station_area = request.args.get('station_area')
    device_id = request.args.get('device_id')
    
    query = '''
        SELECT fr.*, d.device_name, d.device_no, d.station_area, d.location 
        FROM fault_reports fr 
        LEFT JOIN devices d ON fr.device_id = d.id 
        WHERE 1=1
    '''
    params = []
    
    if status:
        query += ' AND fr.status = ?'
        params.append(status)
    
    if priority:
        query += ' AND fr.priority = ?'
        params.append(priority)
    
    if fault_category:
        query += ' AND fr.fault_category = ?'
        params.append(fault_category)
    
    if station_area:
        query += ' AND d.station_area = ?'
        params.append(station_area)
    
    if device_id:
        query += ' AND fr.device_id = ?'
        params.append(device_id)
    
    query += '''
        ORDER BY CASE fr.priority 
            WHEN 'urgent' THEN 1 
            WHEN 'high' THEN 2 
            WHEN 'normal' THEN 3 
            ELSE 4 
        END, fr.report_time DESC
    '''
    
    cursor.execute(query, params)
    reports = [dict(row) for row in cursor.fetchall()]
    
    for report in reports:
        report['priority_color'] = PRIORITY_COLORS.get(report['priority'], '#6c757d')
    
    conn.close()
    return success_response(reports)

@app.route('/api/fault-reports/<int:report_id>', methods=['GET'])
def get_fault_report(report_id):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT fr.*, d.device_name, d.device_no, d.station_area, d.location 
        FROM fault_reports fr 
        LEFT JOIN devices d ON fr.device_id = d.id 
        WHERE fr.id = ?
    ''', (report_id,))
    report = cursor.fetchone()
    
    if not report:
        conn.close()
        return error_response('报修记录不存在', 404), 404
    
    report_dict = dict(report)
    report_dict['priority_color'] = PRIORITY_COLORS.get(report_dict['priority'], '#6c757d')
    
    cursor.execute('''
        SELECT mr.* FROM maintenance_records mr
        WHERE mr.fault_report_id = ? ORDER BY mr.create_time DESC
    ''', (report_id,))
    report_dict['maintenance_records'] = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return success_response(report_dict)

@app.route('/api/fault-reports', methods=['POST'])
def add_fault_report():
    data = request.get_json()
    required_fields = ['device_id', 'fault_type', 'fault_description', 'reporter']
    for field in required_fields:
        if field not in data:
            return error_response(f'缺少必填字段: {field}', 400), 400
    
    priority = data.get('priority', 'normal')
    if priority not in PRIORITY_LEVELS:
        return error_response(f'无效优先级，有效值: {PRIORITY_LEVELS}', 400), 400
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM devices WHERE id = ?', (data['device_id'],))
    if not cursor.fetchone():
        conn.close()
        return error_response('设备不存在', 404), 404
    
    order_no = generate_order_no('WO')
    try:
        cursor.execute('''
            INSERT INTO fault_reports (order_no, device_id, fault_type, fault_category, priority, fault_description, reporter, contact)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_no,
            data['device_id'],
            data['fault_type'],
            data.get('fault_category'),
            priority,
            data['fault_description'],
            data['reporter'],
            data.get('contact')
        ))
        conn.commit()
        
        cursor.execute('''
            UPDATE devices SET status = 'fault', update_time = ? WHERE id = ?
        ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), data['device_id']))
        conn.commit()
        
        report_id = cursor.lastrowid
        conn.close()
        return success_response({'id': report_id, 'order_no': order_no}, '故障上报成功')
    except Exception as e:
        conn.close()
        return error_response(f'上报失败: {str(e)}', 500), 500

@app.route('/api/fault-reports/<int:report_id>/process', methods=['PUT'])
def process_fault_report(report_id):
    data = request.get_json()
    action = data.get('action')
    valid_actions = ['processing', 'completed', 'cancelled']
    if action not in valid_actions:
        return error_response(f'无效操作，有效操作: {valid_actions}', 400), 400
    
    operator = data.get('operator', '系统')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM fault_reports WHERE id = ?', (report_id,))
    report = cursor.fetchone()
    if not report:
        conn.close()
        return error_response('报修记录不存在', 404), 404
    
    if action == 'processing':
        new_status = 'processing'
        device_status = 'maintaining'
        log_content = '开始处理故障报修'
    elif action == 'completed':
        new_status = 'completed'
        device_status = 'repaired'
        log_content = '故障报修处理完成'
    else:
        new_status = 'cancelled'
        device_status = 'normal'
        log_content = '故障报修已取消'
    
    cursor.execute('''
        UPDATE fault_reports SET status = ? WHERE id = ?
    ''', (new_status, report_id))
    
    cursor.execute('''
        UPDATE devices SET status = ?, update_time = ? WHERE id = ?
    ''', (device_status, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), report['device_id']))
    
    conn.commit()
    conn.close()
    return success_response(None, f'{log_content}')

@app.route('/api/maintenance-records', methods=['GET'])
def get_maintenance_records():
    conn = get_db()
    cursor = conn.cursor()
    
    device_id = request.args.get('device_id')
    fault_report_id = request.args.get('fault_report_id')
    
    query = '''
        SELECT mr.*, d.device_name, d.device_no, d.station_area, d.location 
        FROM maintenance_records mr 
        LEFT JOIN devices d ON mr.device_id = d.id 
        WHERE 1=1
    '''
    params = []
    
    if device_id:
        query += ' AND mr.device_id = ?'
        params.append(device_id)
    
    if fault_report_id:
        query += ' AND mr.fault_report_id = ?'
        params.append(fault_report_id)
    
    query += ' ORDER BY mr.create_time DESC'
    
    cursor.execute(query, params)
    records = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return success_response(records)

@app.route('/api/maintenance-records/<int:record_id>', methods=['GET'])
def get_maintenance_record(record_id):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT mr.*, d.device_name, d.device_no, d.station_area, d.location 
        FROM maintenance_records mr 
        LEFT JOIN devices d ON mr.device_id = d.id 
        WHERE mr.id = ?
    ''', (record_id,))
    record = cursor.fetchone()
    
    if not record:
        conn.close()
        return error_response('运维记录不存在', 404), 404
    
    record_dict = dict(record)
    
    cursor.execute('''
        SELECT ml.* FROM maintenance_logs ml
        WHERE ml.maintenance_id = ? ORDER BY ml.create_time ASC
    ''', (record_id,))
    record_dict['maintenance_logs'] = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return success_response(record_dict)

@app.route('/api/maintenance-records', methods=['POST'])
def add_maintenance_record():
    data = request.get_json()
    required_fields = ['device_id', 'maintenance_type', 'maintenance_content', 'maintenance_person']
    for field in required_fields:
        if field not in data:
            return error_response(f'缺少必填字段: {field}', 400), 400
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM devices WHERE id = ?', (data['device_id'],))
    if not cursor.fetchone():
        conn.close()
        return error_response('设备不存在', 404), 404
    
    fault_report_id = data.get('fault_report_id')
    if fault_report_id:
        cursor.execute('SELECT * FROM fault_reports WHERE id = ?', (fault_report_id,))
        if not cursor.fetchone():
            conn.close()
            return error_response('关联的故障报修不存在', 404), 404
    
    order_no = generate_order_no('MT')
    try:
        cursor.execute('''
            INSERT INTO maintenance_records 
            (order_no, device_id, fault_report_id, maintenance_type, maintenance_content, 
             maintenance_person, action_taken, parts_replaced, start_time, end_time, cost, remark)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_no,
            data['device_id'],
            fault_report_id,
            data['maintenance_type'],
            data['maintenance_content'],
            data['maintenance_person'],
            data.get('action_taken'),
            data.get('parts_replaced'),
            data.get('start_time'),
            data.get('end_time'),
            data.get('cost', 0),
            data.get('remark')
        ))
        conn.commit()
        record_id = cursor.lastrowid
        
        cursor.execute('''
            INSERT INTO maintenance_logs (maintenance_id, log_type, log_content, operator)
            VALUES (?, ?, ?, ?)
        ''', (record_id, 'create', '创建运维记录', data.get('maintenance_person', '系统')))
        conn.commit()
        
        conn.close()
        return success_response({'id': record_id, 'order_no': order_no}, '运维记录添加成功')
    except Exception as e:
        conn.close()
        return error_response(f'添加失败: {str(e)}', 500), 500

@app.route('/api/maintenance-logs', methods=['POST'])
def add_maintenance_log():
    data = request.get_json()
    required_fields = ['maintenance_id', 'log_type', 'log_content']
    for field in required_fields:
        if field not in data:
            return error_response(f'缺少必填字段: {field}', 400), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM maintenance_records WHERE id = ?', (data['maintenance_id'],))
    if not cursor.fetchone():
        conn.close()
        return error_response('运维记录不存在', 404), 404
    
    try:
        cursor.execute('''
            INSERT INTO maintenance_logs (maintenance_id, log_type, log_content, operator)
            VALUES (?, ?, ?, ?)
        ''', (
            data['maintenance_id'],
            data['log_type'],
            data['log_content'],
            data.get('operator', '系统')
        ))
        conn.commit()
        log_id = cursor.lastrowid
        conn.close()
        return success_response({'id': log_id}, '日志添加成功')
    except Exception as e:
        conn.close()
        return error_response(f'添加失败: {str(e)}', 500), 500

@app.route('/api/maintenance-logs/<int:maintenance_id>', methods=['GET'])
def get_maintenance_logs(maintenance_id):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM maintenance_logs WHERE maintenance_id = ? ORDER BY create_time ASC
    ''', (maintenance_id,))
    logs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return success_response(logs)

@app.route('/api/constants', methods=['GET'])
def get_constants():
    return success_response({
        'fault_categories': FAULT_CATEGORIES,
        'priority_levels': PRIORITY_LEVELS,
        'priority_colors': PRIORITY_COLORS,
        'gasoline_types': GASOLINE_TYPES,
        'station_areas': STATION_AREAS,
        'maintenance_actions': MAINTENANCE_ACTIONS,
        'device_statuses': ['normal', 'fault', 'maintaining', 'repaired'],
        'fault_statuses': ['pending', 'processing', 'completed', 'cancelled']
    })

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) as total FROM devices')
    total_devices = cursor.fetchone()['total']
    
    cursor.execute('SELECT COUNT(*) as count FROM devices WHERE status = "normal"')
    normal_devices = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM devices WHERE status = "fault"')
    fault_devices = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM devices WHERE status = "maintaining"')
    maintaining_devices = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM devices WHERE status = "repaired"')
    repaired_devices = cursor.fetchone()['count']
    
    device_rate = (normal_devices + repaired_devices) / total_devices * 100 if total_devices > 0 else 0
    
    cursor.execute('SELECT COUNT(*) as count FROM fault_reports WHERE status = "pending"')
    pending_reports = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM fault_reports WHERE priority = "urgent" AND status != "completed" AND status != "cancelled"')
    urgent_pending = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM maintenance_records')
    total_maintenance = cursor.fetchone()['count']
    
    cursor.execute('SELECT station_area, COUNT(*) as count FROM devices GROUP BY station_area')
    area_distribution = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute('SELECT gasoline_type, COUNT(*) as count FROM devices GROUP BY gasoline_type')
    gasoline_distribution = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute('SELECT status, COUNT(*) as count FROM fault_reports GROUP BY status')
    fault_status_distribution = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return success_response({
        'total_devices': total_devices,
        'normal_devices': normal_devices,
        'fault_devices': fault_devices,
        'maintaining_devices': maintaining_devices,
        'repaired_devices': repaired_devices,
        'device_intact_rate': round(device_rate, 2),
        'pending_reports': pending_reports,
        'urgent_pending': urgent_pending,
        'total_maintenance': total_maintenance,
        'area_distribution': area_distribution,
        'gasoline_distribution': gasoline_distribution,
        'fault_status_distribution': fault_status_distribution
    })

@app.route('/')
def index():
    return success_response({
        'name': '加油站自助收银加油机运维管理系统 API',
        'version': '2.0',
        'endpoints': {
            '设备管理': {
                'GET /api/devices': '获取设备列表（支持status, station_area, gasoline_type筛选）',
                'GET /api/devices/<id>': '获取单个设备详情（含关联故障和运维记录）',
                'POST /api/devices': '添加设备',
                'PUT /api/devices/<id>': '更新设备',
                'PUT /api/devices/<id>/status': '更新设备状态',
                'DELETE /api/devices/<id>': '删除设备'
            },
            '故障报修': {
                'GET /api/fault-reports': '获取报修列表（支持多维度筛选，按优先级排序）',
                'GET /api/fault-reports/<id>': '获取单个报修详情（含关联运维记录）',
                'POST /api/fault-reports': '故障上报',
                'PUT /api/fault-reports/<id>/process': '处理报修'
            },
            '运维记录': {
                'GET /api/maintenance-records': '获取运维记录列表（支持设备、工单筛选）',
                'GET /api/maintenance-records/<id>': '获取单条运维记录（含日志）',
                'POST /api/maintenance-records': '添加运维记录（支持关联工单）'
            },
            '维修日志': {
                'GET /api/maintenance-logs/<maintenance_id>': '获取维修日志列表',
                'POST /api/maintenance-logs': '添加维修日志'
            },
            '系统常量': {
                'GET /api/constants': '获取所有系统常量配置'
            },
            '仪表盘': {
                'GET /api/dashboard/stats': '获取统计数据（含设备完好率）'
            }
        }
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
