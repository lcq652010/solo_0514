from flask import Flask, request, jsonify, g
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

DATABASE = 'hospital_ultrasound.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def unified_response(success, message="", data=None, code=200):
    response = {
        "success": success,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }
    if data is not None:
        response["data"] = data
    return jsonify(response), code

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('DROP TABLE IF EXISTS maintenance_records')
        cursor.execute('DROP TABLE IF EXISTS work_orders')
        cursor.execute('DROP TABLE IF EXISTS devices')
        cursor.execute('DROP TABLE IF EXISTS device_operation_logs')
        
        cursor.execute('''
            CREATE TABLE devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_code TEXT UNIQUE NOT NULL,
                device_name TEXT NOT NULL,
                model TEXT,
                probe_count INTEGER DEFAULT 0,
                department TEXT,
                location TEXT,
                purchase_date TEXT,
                enable_date TEXT,
                status TEXT DEFAULT '正常',
                create_time TEXT DEFAULT CURRENT_TIMESTAMP,
                update_time TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE work_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_no TEXT UNIQUE NOT NULL,
                device_id INTEGER NOT NULL,
                device_code TEXT NOT NULL,
                department TEXT,
                fault_type TEXT NOT NULL,
                fault_description TEXT NOT NULL,
                priority TEXT DEFAULT '普通',
                reporter TEXT,
                report_time TEXT DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT '待处理',
                handler TEXT,
                handle_time TEXT,
                handle_result TEXT,
                fault_level TEXT DEFAULT '一般',
                repair_cost REAL DEFAULT 0,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE maintenance_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER NOT NULL,
                device_code TEXT NOT NULL,
                department TEXT,
                work_order_no TEXT,
                maintenance_type TEXT NOT NULL,
                description TEXT,
                operator TEXT,
                start_time TEXT,
                end_time TEXT,
                result TEXT,
                parts_used TEXT,
                cost REAL DEFAULT 0,
                create_time TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE device_operation_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER NOT NULL,
                device_code TEXT NOT NULL,
                operation_type TEXT NOT NULL,
                operator TEXT,
                remark TEXT,
                operation_time TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        ''')
        
        db.commit()

def generate_order_no():
    now = datetime.now()
    prefix = 'WO' + now.strftime('%Y%m%d')
    
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT order_no FROM work_orders WHERE order_no LIKE ? ORDER BY order_no DESC LIMIT 1', (prefix + '%',))
        last = cursor.fetchone()
        
        if last:
            last_num = int(last['order_no'][-4:])
            new_num = last_num + 1
        else:
            new_num = 1
        
        return f'{prefix}{new_num:04d}'

def get_departments():
    return [
        {'code': 'radiology', 'name': '放射科'},
        {'code': 'cardiology', 'name': '心内科'},
        {'code': 'emergency', 'name': '急诊科'},
        {'code': 'pediatrics', 'name': '儿科'},
        {'code': 'obstetrics', 'name': '妇产科'},
        {'code': 'surgery', 'name': '外科'},
        {'code': 'internal', 'name': '内科'},
        {'code': 'icu', 'name': 'ICU'}
    ]

@app.route('/api/devices', methods=['POST'])
def add_device():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO devices (device_code, device_name, model, probe_count, department, location, purchase_date, enable_date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['device_code'],
            data['device_name'],
            data.get('model', ''),
            data.get('probe_count', 0),
            data.get('department', ''),
            data.get('location', ''),
            data.get('purchase_date', ''),
            data.get('enable_date', ''),
            data.get('status', '正常')
        ))
        db.commit()
        
        cursor.execute('''
            INSERT INTO device_operation_logs (device_id, device_code, operation_type, operator, remark)
            VALUES (?, ?, '设备新增', ?, ?)
        ''', (cursor.lastrowid, data['device_code'], data.get('operator', '系统'), '新增设备'))
        db.commit()
        
        return unified_response(True, '设备添加成功', {'id': cursor.lastrowid})
    except sqlite3.IntegrityError:
        return unified_response(False, '设备编号已存在', None, 400)

@app.route('/api/devices', methods=['GET'])
def get_devices():
    db = get_db()
    cursor = db.cursor()
    
    status = request.args.get('status')
    department = request.args.get('department')
    device_code = request.args.get('device_code')
    
    query = 'SELECT * FROM devices WHERE 1=1'
    params = []
    
    if status:
        query += ' AND status = ?'
        params.append(status)
    if department:
        query += ' AND department = ?'
        params.append(department)
    if device_code:
        query += ' AND device_code LIKE ?'
        params.append(f'%{device_code}%')
    
    query += ' ORDER BY create_time DESC'
    
    cursor.execute(query, params)
    devices = [dict(row) for row in cursor.fetchall()]
    
    for device in devices:
        if device['status'] == '正常':
            device['status_color'] = 'success'
        elif device['status'] == '故障':
            device['status_color'] = 'danger'
        elif device['status'] == '维修中':
            device['status_color'] = 'warning'
        else:
            device['status_color'] = 'info'
    
    return unified_response(True, '获取设备列表成功', devices)

@app.route('/api/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM devices WHERE id = ?', (device_id,))
    device = cursor.fetchone()
    
    if device:
        device_dict = dict(device)
        if device_dict['status'] == '正常':
            device_dict['status_color'] = 'success'
        elif device_dict['status'] == '故障':
            device_dict['status_color'] = 'danger'
        elif device_dict['status'] == '维修中':
            device_dict['status_color'] = 'warning'
        else:
            device_dict['status_color'] = 'info'
        return unified_response(True, '获取设备信息成功', device_dict)
    else:
        return unified_response(False, '设备不存在', None, 404)

@app.route('/api/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    data = request.json
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('''
        UPDATE devices 
        SET device_name=?, model=?, probe_count=?, department=?, location=?, purchase_date=?, enable_date=?, status=?, update_time=CURRENT_TIMESTAMP
        WHERE id=?
    ''', (
        data['device_name'],
        data.get('model', ''),
        data.get('probe_count', 0),
        data.get('department', ''),
        data.get('location', ''),
        data.get('purchase_date', ''),
        data.get('enable_date', ''),
        data.get('status', '正常'),
        device_id
    ))
    db.commit()
    
    if cursor.rowcount > 0:
        cursor.execute('SELECT device_code FROM devices WHERE id = ?', (device_id,))
        device = cursor.fetchone()
        cursor.execute('''
            INSERT INTO device_operation_logs (device_id, device_code, operation_type, operator, remark)
            VALUES (?, ?, '设备更新', ?, ?)
        ''', (device_id, device['device_code'], data.get('operator', '系统'), '更新设备信息'))
        db.commit()
        return unified_response(True, '设备更新成功')
    else:
        return unified_response(False, '设备不存在', None, 404)

@app.route('/api/devices/<int:device_id>/status', methods=['PUT'])
def update_device_status(device_id):
    data = request.json
    status = data.get('status')
    
    if status not in ['正常', '故障', '维修中', '已修复']:
        return unified_response(False, '无效的状态', None, 400)
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        UPDATE devices SET status=?, update_time=CURRENT_TIMESTAMP WHERE id=?
    ''', (status, device_id))
    db.commit()
    
    if cursor.rowcount > 0:
        cursor.execute('SELECT device_code FROM devices WHERE id = ?', (device_id,))
        device = cursor.fetchone()
        cursor.execute('''
            INSERT INTO device_operation_logs (device_id, device_code, operation_type, operator, remark)
            VALUES (?, ?, '状态变更', ?, ?)
        ''', (device_id, device['device_code'], data.get('operator', '系统'), f'状态变更为：{status}'))
        db.commit()
        return unified_response(True, '状态更新成功')
    else:
        return unified_response(False, '设备不存在', None, 404)

@app.route('/api/departments', methods=['GET'])
def get_departments_list():
    return unified_response(True, '获取科室列表成功', get_departments())

@app.route('/api/fault-types', methods=['GET'])
def get_fault_types():
    fault_types = [
        {'code': 'hardware', 'name': '硬件故障', 'description': '设备硬件损坏或失灵'},
        {'code': 'software', 'name': '软件故障', 'description': '系统软件或应用程序故障'},
        {'code': 'probe', 'name': '探头故障', 'description': '超声探头损坏或异常'},
        {'code': 'display', 'name': '显示故障', 'description': '图像显示异常或黑屏'},
        {'code': 'power', 'name': '电源故障', 'description': '电源供应问题'},
        {'code': 'network', 'name': '网络故障', 'description': '网络连接或数据传输问题'},
        {'code': 'other', 'name': '其他故障', 'description': '未分类的其他故障'}
    ]
    return unified_response(True, '获取故障类型列表成功', fault_types)

@app.route('/api/fault-levels', methods=['GET'])
def get_fault_levels():
    fault_levels = [
        {'code': 'critical', 'name': '严重', 'description': '设备完全无法使用，严重影响临床工作'},
        {'code': 'major', 'name': '较大', 'description': '主要功能异常，影响正常使用'},
        {'code': 'general', 'name': '一般', 'description': '次要功能异常，部分功能可用'},
        {'code': 'minor', 'name': '轻微', 'description': '轻微问题，不影响主要功能'}
    ]
    return unified_response(True, '获取故障等级列表成功', fault_levels)

@app.route('/api/work-orders/report', methods=['POST'])
def report_fault():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT id, device_code, status, department FROM devices WHERE id = ?', (data['device_id'],))
    device = cursor.fetchone()
    
    if not device:
        return unified_response(False, '设备不存在', None, 404)
    
    order_no = generate_order_no()
    
    fault_type = data.get('fault_type', 'other')
    priority = data.get('priority', '普通')
    fault_level = data.get('fault_level', 'general')
    
    if priority not in ['紧急', '高', '普通', '低']:
        priority = '普通'
    
    cursor.execute('''
        INSERT INTO work_orders (order_no, device_id, device_code, department, fault_type, fault_description, priority, fault_level, reporter)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        order_no,
        data['device_id'],
        device['device_code'],
        device['department'],
        fault_type,
        data['fault_description'],
        priority,
        fault_level,
        data.get('reporter', '')
    ))
    
    cursor.execute('''
        UPDATE devices SET status='故障', update_time=CURRENT_TIMESTAMP WHERE id=?
    ''', (data['device_id'],))
    
    db.commit()
    return unified_response(True, '故障上报成功', {'order_no': order_no})

@app.route('/api/work-orders', methods=['GET'])
def get_work_orders():
    db = get_db()
    cursor = db.cursor()
    
    status = request.args.get('status')
    fault_type = request.args.get('fault_type')
    priority = request.args.get('priority')
    department = request.args.get('department')
    fault_level = request.args.get('fault_level')
    
    query = 'SELECT * FROM work_orders WHERE 1=1'
    params = []
    
    if status:
        query += ' AND status = ?'
        params.append(status)
    if fault_type:
        query += ' AND fault_type = ?'
        params.append(fault_type)
    if priority:
        query += ' AND priority = ?'
        params.append(priority)
    if department:
        query += ' AND department = ?'
        params.append(department)
    if fault_level:
        query += ' AND fault_level = ?'
        params.append(fault_level)
    
    query += ' ORDER BY CASE priority WHEN "紧急" THEN 1 WHEN "高" THEN 2 WHEN "普通" THEN 3 WHEN "低" THEN 4 END, report_time DESC'
    
    cursor.execute(query, params)
    orders = [dict(row) for row in cursor.fetchall()]
    
    priority_colors = {
        '紧急': 'danger',
        '高': 'warning',
        '普通': 'primary',
        '低': 'success'
    }
    
    for order in orders:
        order['priority_color'] = priority_colors.get(order['priority'], 'secondary')
        if order['status'] == '待处理':
            order['status_color'] = 'warning'
        elif order['status'] == '处理中':
            order['status_color'] = 'primary'
        elif order['status'] == '已完成':
            order['status_color'] = 'success'
    
    return unified_response(True, '获取工单列表成功', orders)

@app.route('/api/work-orders/<order_no>/handle', methods=['PUT'])
def handle_work_order(order_no):
    data = request.json
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM work_orders WHERE order_no = ?', (order_no,))
    order = cursor.fetchone()
    
    if not order:
        return unified_response(False, '工单不存在', None, 404)
    
    new_status = data.get('status', '处理中')
    handler = data.get('handler', '')
    handle_result = data.get('handle_result', '')
    repair_cost = data.get('repair_cost', 0)
    
    cursor.execute('''
        UPDATE work_orders 
        SET status=?, handler=?, handle_time=CURRENT_TIMESTAMP, handle_result=?, repair_cost=?
        WHERE order_no=?
    ''', (new_status, handler, handle_result, repair_cost, order_no))
    
    if new_status == '处理中':
        cursor.execute('''
            UPDATE devices SET status='维修中', update_time=CURRENT_TIMESTAMP WHERE id=?
        ''', (order['device_id'],))
    elif new_status == '已完成':
        cursor.execute('''
            UPDATE devices SET status='已修复', update_time=CURRENT_TIMESTAMP WHERE id=?
        ''', (order['device_id'],))
        
        cursor.execute('''
            INSERT INTO maintenance_records 
            (device_id, device_code, department, work_order_no, maintenance_type, description, operator, start_time, end_time, result, cost)
            VALUES (?, ?, ?, ?, '故障维修', ?, ?, ?, CURRENT_TIMESTAMP, ?, ?)
        ''', (
            order['device_id'],
            order['device_code'],
            order['department'],
            order_no,
            order['fault_description'],
            handler,
            order['report_time'],
            handle_result,
            repair_cost
        ))
    
    db.commit()
    return unified_response(True, '工单处理成功')

@app.route('/api/maintenance-records', methods=['GET'])
def get_maintenance_records():
    db = get_db()
    cursor = db.cursor()
    
    device_id = request.args.get('device_id')
    department = request.args.get('department')
    maintenance_type = request.args.get('maintenance_type')
    
    query = 'SELECT * FROM maintenance_records WHERE 1=1'
    params = []
    
    if device_id:
        query += ' AND device_id = ?'
        params.append(device_id)
    if department:
        query += ' AND department = ?'
        params.append(department)
    if maintenance_type:
        query += ' AND maintenance_type = ?'
        params.append(maintenance_type)
    
    query += ' ORDER BY create_time DESC'
    
    cursor.execute(query, params)
    records = [dict(row) for row in cursor.fetchall()]
    
    return unified_response(True, '获取运维记录成功', records)

@app.route('/api/maintenance-records', methods=['POST'])
def add_maintenance_record():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT device_code, department FROM devices WHERE id = ?', (data['device_id'],))
    device = cursor.fetchone()
    
    if not device:
        return unified_response(False, '设备不存在', None, 404)
    
    cursor.execute('''
        INSERT INTO maintenance_records 
        (device_id, device_code, department, work_order_no, maintenance_type, description, operator, start_time, end_time, result, parts_used, cost)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['device_id'],
        device['device_code'],
        device['department'],
        data.get('work_order_no', ''),
        data['maintenance_type'],
        data.get('description', ''),
        data.get('operator', ''),
        data.get('start_time', ''),
        data.get('end_time', ''),
        data.get('result', ''),
        data.get('parts_used', ''),
        data.get('cost', 0)
    ))
    db.commit()
    
    return unified_response(True, '运维记录添加成功', {'id': cursor.lastrowid})

@app.route('/api/device-operation-logs', methods=['GET'])
def get_device_operation_logs():
    db = get_db()
    cursor = db.cursor()
    
    device_id = request.args.get('device_id')
    
    if device_id:
        cursor.execute('SELECT * FROM device_operation_logs WHERE device_id = ? ORDER BY operation_time DESC', (device_id,))
    else:
        cursor.execute('SELECT * FROM device_operation_logs ORDER BY operation_time DESC LIMIT 100')
    
    logs = [dict(row) for row in cursor.fetchall()]
    return unified_response(True, '获取设备操作日志成功', logs)

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT COUNT(*) as total FROM devices')
    total_devices = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as count FROM devices WHERE status='正常'")
    normal_devices = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM devices WHERE status='故障'")
    fault_devices = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM devices WHERE status='维修中'")
    repairing_devices = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM devices WHERE status='已修复'")
    repaired_devices = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM work_orders WHERE status='待处理'")
    pending_orders = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM work_orders WHERE priority='紧急' AND status!='已完成'")
    urgent_orders = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as total FROM maintenance_records')
    total_records = cursor.fetchone()['total']
    
    cursor.execute('''
        SELECT fault_type, COUNT(*) as count 
        FROM work_orders 
        GROUP BY fault_type 
        ORDER BY count DESC
    ''')
    fault_type_stats = [dict(row) for row in cursor.fetchall()]
    
    availability_rate = 0
    intact_rate = 0
    
    if total_devices > 0:
        availability_rate = round((normal_devices + repaired_devices) / total_devices * 100, 2)
        intact_rate = round((normal_devices + repaired_devices) / total_devices * 100, 2)
    
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    cursor.execute('''
        SELECT COUNT(*) as count 
        FROM maintenance_records 
        WHERE create_time >= ?
    ''', (thirty_days_ago,))
    monthly_maintenance = cursor.fetchone()['count']
    
    cursor.execute('SELECT SUM(cost) as total FROM maintenance_records')
    total_cost_result = cursor.fetchone()
    total_maintenance_cost = total_cost_result['total'] or 0
    
    return unified_response(True, '获取统计数据成功', {
        'total_devices': total_devices,
        'normal_devices': normal_devices,
        'fault_devices': fault_devices,
        'repairing_devices': repairing_devices,
        'repaired_devices': repaired_devices,
        'pending_orders': pending_orders,
        'urgent_orders': urgent_orders,
        'total_records': total_records,
        'fault_type_stats': fault_type_stats,
        'availability_rate': availability_rate,
        'intact_rate': intact_rate,
        'monthly_maintenance': monthly_maintenance,
        'total_maintenance_cost': total_maintenance_cost
    })

@app.route('/api/dashboard/department-stats', methods=['GET'])
def get_department_stats():
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('''
        SELECT 
            department,
            COUNT(*) as total_devices,
            SUM(CASE WHEN status IN ('正常', '已修复') THEN 1 ELSE 0 END) as available_devices
        FROM devices 
        WHERE department IS NOT NULL AND department != ''
        GROUP BY department
    ''')
    
    stats = []
    for row in cursor.fetchall():
        row_dict = dict(row)
        total = row_dict['total_devices']
        available = row_dict['available_devices']
        if total > 0:
            row_dict['availability_rate'] = round(available / total * 100, 2)
            row_dict['intact_rate'] = round(available / total * 100, 2)
        else:
            row_dict['availability_rate'] = 0
            row_dict['intact_rate'] = 0
        stats.append(row_dict)
    
    return unified_response(True, '获取科室统计成功', stats)

if __name__ == '__main__':
    init_db()
    print('数据库初始化完成！')
    print('服务器启动中... http://localhost:5000')
    app.run(debug=True, host='0.0.0.0', port=5000)
