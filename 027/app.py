from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DATABASE = 'meter_management.db'

FAULT_CATEGORIES = {
    '硬件故障': ['通信模块损坏', '电源故障', '主板故障', '显示故障'],
    '通信异常': ['网络中断', '信号弱', '数据传输错误', '连接超时'],
    '数据异常': ['读数异常', '数据丢失', '采集频率异常', '数据溢出'],
    '电源问题': ['断电', '电压不稳', '电池耗尽', '供电异常'],
    '其他故障': ['未知错误', '环境因素', '人为损坏']
}

PRIORITY_LEVELS = ['紧急', '高', '中', '低']
COMMUNICATION_METHODS = ['GPRS', '4G', '5G', 'NB-IoT', 'LoRa', '以太网', 'RS485', '其他']
DEVICE_STATUSES = ['正常', '故障', '维修中', '已修复']

def api_response(code=200, data=None, message='success'):
    response = {
        'code': code,
        'message': message,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), code

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def migrate_db():
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("PRAGMA table_info(devices)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'device_model' not in columns:
            cursor.execute("ALTER TABLE devices ADD COLUMN device_model TEXT")
            print("已添加 device_model 字段")
        
        if 'communication_method' not in columns:
            cursor.execute("ALTER TABLE devices ADD COLUMN communication_method TEXT")
            print("已添加 communication_method 字段")
        
        if 'device_serial' not in columns:
            cursor.execute("ALTER TABLE devices ADD COLUMN device_serial TEXT")
            print("已添加 device_serial 字段")
        
        if 'commissioning_date' not in columns:
            cursor.execute("ALTER TABLE devices ADD COLUMN commissioning_date TEXT")
            print("已添加 commissioning_date 字段")
        
        if 'power_area' not in columns:
            cursor.execute("ALTER TABLE devices ADD COLUMN power_area TEXT")
            print("已添加 power_area 字段")
        
        if 'station_area' not in columns:
            cursor.execute("ALTER TABLE devices ADD COLUMN station_area TEXT")
            print("已添加 station_area 字段")
        
        cursor.execute("PRAGMA table_info(work_orders)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'priority' not in columns:
            cursor.execute("ALTER TABLE work_orders ADD COLUMN priority TEXT DEFAULT '中'")
            print("已添加 priority 字段")
        
        if 'fault_category' not in columns:
            cursor.execute("ALTER TABLE work_orders ADD COLUMN fault_category TEXT")
            print("已添加 fault_category 字段")
        
        if 'power_impact' not in columns:
            cursor.execute("ALTER TABLE work_orders ADD COLUMN power_impact TEXT")
            print("已添加 power_impact 字段")
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS collection_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER NOT NULL,
                device_code TEXT NOT NULL,
                collect_time TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT '成功',
                reading_value REAL,
                signal_strength INTEGER,
                create_time TEXT NOT NULL,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        ''')
        print("已创建 collection_records 表")
        
        conn.commit()
        print("数据库迁移完成")
    except Exception as e:
        print(f"数据库迁移出错: {e}")
    finally:
        conn.close()

def init_db():
    if not os.path.exists(DATABASE):
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_code TEXT UNIQUE NOT NULL,
                device_name TEXT NOT NULL,
                device_model TEXT,
                device_serial TEXT,
                location TEXT NOT NULL,
                power_area TEXT,
                station_area TEXT,
                communication_method TEXT,
                install_date TEXT NOT NULL,
                commissioning_date TEXT,
                status TEXT NOT NULL DEFAULT '正常',
                create_time TEXT NOT NULL,
                update_time TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS work_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_no TEXT UNIQUE NOT NULL,
                device_id INTEGER NOT NULL,
                device_code TEXT NOT NULL,
                fault_category TEXT NOT NULL,
                fault_type TEXT NOT NULL,
                fault_description TEXT NOT NULL,
                priority TEXT NOT NULL DEFAULT '中',
                power_impact TEXT,
                reporter TEXT NOT NULL,
                reporter_phone TEXT,
                status TEXT NOT NULL DEFAULT '待处理',
                handle_user TEXT,
                handle_time TEXT,
                handle_result TEXT,
                create_time TEXT NOT NULL,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS maintenance_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_no TEXT NOT NULL,
                device_id INTEGER NOT NULL,
                device_code TEXT NOT NULL,
                maintenance_user TEXT NOT NULL,
                maintenance_content TEXT NOT NULL,
                maintenance_time TEXT NOT NULL,
                before_status TEXT NOT NULL,
                after_status TEXT NOT NULL,
                remark TEXT,
                create_time TEXT NOT NULL,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS collection_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER NOT NULL,
                device_code TEXT NOT NULL,
                collect_time TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT '成功',
                reading_value REAL,
                signal_strength INTEGER,
                create_time TEXT NOT NULL,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("数据库初始化成功")
    else:
        migrate_db()

def generate_order_no():
    now = datetime.now()
    date_str = now.strftime("%Y%m%d")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM work_orders WHERE order_no LIKE ?", (f'WO{date_str}%',))
    count = cursor.fetchone()[0]
    conn.close()
    return f'WO{date_str}{count + 1:04d}'

@app.route('/api/constants', methods=['GET'])
def get_constants():
    return api_response(200, {
        'fault_categories': FAULT_CATEGORIES,
        'priority_levels': PRIORITY_LEVELS,
        'communication_methods': COMMUNICATION_METHODS,
        'device_statuses': DEVICE_STATUSES
    })

@app.route('/api/devices', methods=['GET'])
def get_devices():
    status = request.args.get('status')
    power_area = request.args.get('power_area')
    station_area = request.args.get('station_area')
    
    conn = get_db()
    cursor = conn.cursor()
    
    query = "SELECT * FROM devices WHERE 1=1"
    params = []
    
    if status:
        query += " AND status = ?"
        params.append(status)
    
    if power_area:
        query += " AND power_area LIKE ?"
        params.append(f'%{power_area}%')
    
    if station_area:
        query += " AND station_area LIKE ?"
        params.append(f'%{station_area}%')
    
    query += " ORDER BY create_time DESC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    devices = [dict(row) for row in rows]
    return api_response(200, {'list': devices, 'total': len(devices)})

@app.route('/api/devices/areas', methods=['GET'])
def get_device_areas():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT DISTINCT power_area FROM devices WHERE power_area IS NOT NULL AND power_area != ''")
    power_areas = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT DISTINCT station_area FROM devices WHERE station_area IS NOT NULL AND station_area != ''")
    station_areas = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return api_response(200, {'power_areas': power_areas, 'station_areas': station_areas})

@app.route('/api/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM devices WHERE id = ?", (device_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return api_response(200, dict(row))
    return api_response(404, None, '设备不存在'), 404

@app.route('/api/devices', methods=['POST'])
def add_device():
    data = request.get_json()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO devices (device_code, device_name, device_model, device_serial, location, 
                                power_area, station_area, communication_method, install_date, 
                                commissioning_date, status, create_time, update_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['device_code'],
            data['device_name'],
            data.get('device_model', ''),
            data.get('device_serial', ''),
            data['location'],
            data.get('power_area', ''),
            data.get('station_area', ''),
            data.get('communication_method', ''),
            data['install_date'],
            data.get('commissioning_date', ''),
            data.get('status', '正常'),
            now,
            now
        ))
        conn.commit()
        device_id = cursor.lastrowid
        conn.close()
        return api_response(200, {'id': device_id}, '设备添加成功')
    except sqlite3.IntegrityError:
        return api_response(400, None, '设备编号已存在'), 400

@app.route('/api/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    data = request.get_json()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE devices SET device_code=?, device_name=?, device_model=?, device_serial=?, 
                          location=?, power_area=?, station_area=?, communication_method=?, 
                          install_date=?, commissioning_date=?, status=?, update_time=?
        WHERE id=?
    ''', (
        data['device_code'],
        data['device_name'],
        data.get('device_model', ''),
        data.get('device_serial', ''),
        data['location'],
        data.get('power_area', ''),
        data.get('station_area', ''),
        data.get('communication_method', ''),
        data['install_date'],
        data.get('commissioning_date', ''),
        data.get('status', '正常'),
        now,
        device_id
    ))
    conn.commit()
    conn.close()
    return api_response(200, None, '设备更新成功')

@app.route('/api/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM devices WHERE id=?", (device_id,))
    conn.commit()
    conn.close()
    return api_response(200, None, '设备删除成功')

@app.route('/api/devices/status', methods=['PUT'])
def update_device_status():
    data = request.get_json()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if data['status'] not in DEVICE_STATUSES:
        return api_response(400, None, '无效的状态'), 400
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE devices SET status=?, update_time=? WHERE id=?
    ''', (data['status'], now, data['device_id']))
    conn.commit()
    conn.close()
    return api_response(200, None, '状态更新成功')

@app.route('/api/work-orders', methods=['GET'])
def get_work_orders():
    status = request.args.get('status')
    priority = request.args.get('priority')
    fault_category = request.args.get('fault_category')
    power_area = request.args.get('power_area')
    station_area = request.args.get('station_area')
    
    conn = get_db()
    cursor = conn.cursor()
    
    query = """
        SELECT w.*, d.power_area, d.station_area 
        FROM work_orders w 
        LEFT JOIN devices d ON w.device_id = d.id 
        WHERE 1=1
    """
    params = []
    
    if status:
        query += " AND w.status = ?"
        params.append(status)
    
    if priority:
        query += " AND w.priority = ?"
        params.append(priority)
    
    if fault_category:
        query += " AND w.fault_category = ?"
        params.append(fault_category)
    
    if power_area:
        query += " AND d.power_area LIKE ?"
        params.append(f'%{power_area}%')
    
    if station_area:
        query += " AND d.station_area LIKE ?"
        params.append(f'%{station_area}%')
    
    query += " ORDER BY CASE w.priority WHEN '紧急' THEN 1 WHEN '高' THEN 2 WHEN '中' THEN 3 ELSE 4 END, w.create_time DESC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    orders = [dict(row) for row in rows]
    return api_response(200, {'list': orders, 'total': len(orders)})

@app.route('/api/work-orders/<int:order_id>', methods=['GET'])
def get_work_order(order_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM work_orders WHERE id = ?", (order_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return api_response(200, dict(row))
    return api_response(404, None, '工单不存在'), 404

@app.route('/api/work-orders/report', methods=['POST'])
def report_fault():
    data = request.get_json()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    order_no = generate_order_no()
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, device_code, status FROM devices WHERE id = ?", (data['device_id'],))
    device = cursor.fetchone()
    
    if not device:
        conn.close()
        return api_response(404, None, '设备不存在'), 404
    
    if data.get('priority') not in PRIORITY_LEVELS:
        conn.close()
        return api_response(400, None, '无效的优先级'), 400
    
    cursor.execute('''
        UPDATE devices SET status='故障', update_time=? WHERE id=?
    ''', (now, data['device_id']))
    
    cursor.execute('''
        INSERT INTO work_orders (order_no, device_id, device_code, fault_category, fault_type, 
                                fault_description, priority, power_impact, reporter, reporter_phone, 
                                status, create_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        order_no,
        data['device_id'],
        device['device_code'],
        data['fault_category'],
        data['fault_type'],
        data['fault_description'],
        data.get('priority', '中'),
        data.get('power_impact', ''),
        data['reporter'],
        data.get('reporter_phone', ''),
        '待处理',
        now
    ))
    
    conn.commit()
    conn.close()
    return api_response(200, {'order_no': order_no}, '故障上报成功')

@app.route('/api/work-orders/<int:order_id>/handle', methods=['POST'])
def handle_work_order(order_id):
    data = request.get_json()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM work_orders WHERE id = ?", (order_id,))
    order = cursor.fetchone()
    
    if not order:
        conn.close()
        return api_response(404, None, '工单不存在'), 404
    
    cursor.execute('''
        UPDATE work_orders SET status='处理中', handle_user=?, handle_time=? WHERE id=?
    ''', (data['handle_user'], now, order_id))
    
    cursor.execute('''
        UPDATE devices SET status='维修中', update_time=? WHERE id=?
    ''', (now, order['device_id']))
    
    conn.commit()
    conn.close()
    return api_response(200, None, '工单处理成功')

@app.route('/api/work-orders/<int:order_id>/complete', methods=['POST'])
def complete_work_order(order_id):
    data = request.get_json()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM work_orders WHERE id = ?", (order_id,))
    order = cursor.fetchone()
    
    if not order:
        conn.close()
        return api_response(404, None, '工单不存在'), 404
    
    cursor.execute('''
        UPDATE work_orders SET status='已完成', handle_result=?, handle_time=? WHERE id=?
    ''', (data['handle_result'], now, order_id))
    
    cursor.execute('''
        UPDATE devices SET status='已修复', update_time=? WHERE id=?
    ''', (now, order['device_id']))
    
    cursor.execute('''
        INSERT INTO maintenance_records (order_no, device_id, device_code, maintenance_user, 
                                        maintenance_content, maintenance_time, before_status, 
                                        after_status, remark, create_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        order['order_no'],
        order['device_id'],
        order['device_code'],
        data.get('maintenance_user', data.get('handle_user', '管理员')),
        data['handle_result'],
        now,
        '维修中',
        '已修复',
        data.get('remark', ''),
        now
    ))
    
    conn.commit()
    conn.close()
    return api_response(200, None, '工单完成成功')

@app.route('/api/work-orders/stats', methods=['GET'])
def get_work_order_stats():
    power_area = request.args.get('power_area')
    station_area = request.args.get('station_area')
    
    conn = get_db()
    cursor = conn.cursor()
    
    stats = {}
    
    base_query = """
        SELECT w.* FROM work_orders w 
        LEFT JOIN devices d ON w.device_id = d.id 
        WHERE 1=1
    """
    params = []
    
    if power_area:
        base_query += " AND d.power_area LIKE ?"
        params.append(f'%{power_area}%')
    
    if station_area:
        base_query += " AND d.station_area LIKE ?"
        params.append(f'%{station_area}%')
    
    cursor.execute(base_query.replace('w.*', 'w.priority, COUNT(*) as count') + " GROUP BY w.priority", params)
    priority_stats = {row[0]: row[1] for row in cursor.fetchall()}
    stats['by_priority'] = priority_stats
    
    cursor.execute(base_query.replace('w.*', 'w.fault_category, COUNT(*) as count') + " GROUP BY w.fault_category", params)
    category_stats = {row[0]: row[1] for row in cursor.fetchall()}
    stats['by_category'] = category_stats
    
    cursor.execute(base_query.replace('w.*', 'w.status, COUNT(*) as count') + " GROUP BY w.status", params)
    status_stats = {row[0]: row[1] for row in cursor.fetchall()}
    stats['by_status'] = status_stats
    
    conn.close()
    
    return api_response(200, stats)

@app.route('/api/collection-records', methods=['GET'])
def get_collection_records():
    device_id = request.args.get('device_id')
    device_code = request.args.get('device_code')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    conn = get_db()
    cursor = conn.cursor()
    
    query = "SELECT * FROM collection_records WHERE 1=1"
    params = []
    
    if device_id:
        query += " AND device_id = ?"
        params.append(device_id)
    
    if device_code:
        query += " AND device_code = ?"
        params.append(device_code)
    
    if start_date:
        query += " AND collect_time >= ?"
        params.append(start_date)
    
    if end_date:
        query += " AND collect_time <= ?"
        params.append(end_date + ' 23:59:59')
    
    query += " ORDER BY collect_time DESC LIMIT 1000"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    records = [dict(row) for row in rows]
    return api_response(200, {'list': records, 'total': len(records)})

@app.route('/api/collection-records', methods=['POST'])
def add_collection_record():
    data = request.get_json()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, device_code FROM devices WHERE id = ?", (data['device_id'],))
    device = cursor.fetchone()
    
    if not device:
        conn.close()
        return api_response(404, None, '设备不存在'), 404
    
    cursor.execute('''
        INSERT INTO collection_records (device_id, device_code, collect_time, status, 
                                        reading_value, signal_strength, create_time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['device_id'],
        device['device_code'],
        data.get('collect_time', now),
        data.get('status', '成功'),
        data.get('reading_value', 0),
        data.get('signal_strength', 0),
        now
    ))
    
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    return api_response(200, {'id': record_id}, '采集记录添加成功')

@app.route('/api/maintenance-records', methods=['GET'])
def get_maintenance_records():
    device_code = request.args.get('device_code')
    power_area = request.args.get('power_area')
    station_area = request.args.get('station_area')
    
    conn = get_db()
    cursor = conn.cursor()
    
    query = """
        SELECT m.*, d.power_area, d.station_area 
        FROM maintenance_records m 
        LEFT JOIN devices d ON m.device_id = d.id 
        WHERE 1=1
    """
    params = []
    
    if device_code:
        query += " AND m.device_code = ?"
        params.append(device_code)
    
    if power_area:
        query += " AND d.power_area LIKE ?"
        params.append(f'%{power_area}%')
    
    if station_area:
        query += " AND d.station_area LIKE ?"
        params.append(f'%{station_area}%')
    
    query += " ORDER BY m.create_time DESC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    records = [dict(row) for row in rows]
    return api_response(200, {'list': records, 'total': len(records)})

@app.route('/api/maintenance-records/<int:record_id>', methods=['GET'])
def get_maintenance_record(record_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM maintenance_records WHERE id = ?", (record_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return api_response(200, dict(row))
    return api_response(404, None, '记录不存在'), 404

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    power_area = request.args.get('power_area')
    station_area = request.args.get('station_area')
    
    conn = get_db()
    cursor = conn.cursor()
    
    base_query = "SELECT * FROM devices WHERE 1=1"
    params = []
    
    if power_area:
        base_query += " AND power_area LIKE ?"
        params.append(f'%{power_area}%')
    
    if station_area:
        base_query += " AND station_area LIKE ?"
        params.append(f'%{station_area}%')
    
    cursor.execute(base_query.replace('*', 'COUNT(*)'))
    total_devices = cursor.fetchone()[0]
    
    cursor.execute(base_query.replace('*', 'COUNT(*)') + " AND status='正常'", params)
    normal_devices = cursor.fetchone()[0]
    
    cursor.execute(base_query.replace('*', 'COUNT(*)') + " AND status='故障'", params)
    fault_devices = cursor.fetchone()[0]
    
    cursor.execute(base_query.replace('*', 'COUNT(*)') + " AND status='维修中'", params)
    repairing_devices = cursor.fetchone()[0]
    
    device_health_rate = round((normal_devices / total_devices * 100), 2) if total_devices > 0 else 0
    
    work_order_query = """
        SELECT COUNT(*) FROM work_orders w 
        LEFT JOIN devices d ON w.device_id = d.id 
        WHERE 1=1
    """
    wo_params = params.copy()
    
    if power_area:
        work_order_query += " AND d.power_area LIKE ?"
    
    if station_area:
        work_order_query += " AND d.station_area LIKE ?"
    
    cursor.execute(work_order_query + " AND w.status='待处理'", wo_params)
    pending_orders = cursor.fetchone()[0]
    
    cursor.execute(work_order_query + " AND w.status='处理中'", wo_params)
    processing_orders = cursor.fetchone()[0]
    
    cursor.execute(work_order_query + " AND w.priority='紧急' AND w.status!='已完成'", wo_params)
    urgent_orders = cursor.fetchone()[0]
    
    collection_query = """
        SELECT COUNT(*) FROM collection_records c
        LEFT JOIN devices d ON c.device_id = d.id 
        WHERE 1=1
    """
    coll_params = params.copy()
    
    if power_area:
        collection_query += " AND d.power_area LIKE ?"
    
    if station_area:
        collection_query += " AND d.station_area LIKE ?"
    
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    cursor.execute(collection_query + " AND c.collect_time >= ?", coll_params + [seven_days_ago])
    total_collections = cursor.fetchone()[0]
    
    cursor.execute(collection_query + " AND c.collect_time >= ? AND c.status='成功'", coll_params + [seven_days_ago])
    success_collections = cursor.fetchone()[0]
    
    collection_success_rate = round((success_collections / total_collections * 100), 2) if total_collections > 0 else 0
    
    cursor.execute("SELECT COUNT(*) FROM maintenance_records")
    total_records = cursor.fetchone()[0]
    
    conn.close()
    
    return api_response(200, {
        'total_devices': total_devices,
        'normal_devices': normal_devices,
        'fault_devices': fault_devices,
        'repairing_devices': repairing_devices,
        'device_health_rate': device_health_rate,
        'pending_orders': pending_orders,
        'processing_orders': processing_orders,
        'urgent_orders': urgent_orders,
        'total_collections': total_collections,
        'success_collections': success_collections,
        'collection_success_rate': collection_success_rate,
        'total_records': total_records
    })

@app.route('/api/dashboard/trend', methods=['GET'])
def get_dashboard_trend():
    days = int(request.args.get('days', 7))
    conn = get_db()
    cursor = conn.cursor()
    
    collection_trend = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=days-1-i)).strftime('%Y-%m-%d')
        cursor.execute("""
            SELECT COUNT(*), SUM(CASE WHEN status='成功' THEN 1 ELSE 0 END)
            FROM collection_records 
            WHERE DATE(collect_time) = ?
        """, (date,))
        row = cursor.fetchone()
        total = row[0] or 0
        success = row[1] or 0
        rate = round((success / total * 100), 2) if total > 0 else 0
        collection_trend.append({
            'date': date,
            'total': total,
            'success': success,
            'rate': rate
        })
    
    fault_trend = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=days-1-i)).strftime('%Y-%m-%d')
        cursor.execute("""
            SELECT COUNT(*) FROM work_orders WHERE DATE(create_time) = ?
        """, (date,))
        count = cursor.fetchone()[0] or 0
        fault_trend.append({
            'date': date,
            'count': count
        })
    
    conn.close()
    
    return api_response(200, {
        'collection_trend': collection_trend,
        'fault_trend': fault_trend
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
