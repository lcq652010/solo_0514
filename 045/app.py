from flask import Flask, request, jsonify, g
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)

DATABASE = 'maintenance.db'

def success_response(data=None, message='操作成功'):
    response = {'code': 200, 'message': message}
    if data is not None:
        response['data'] = data
    return jsonify(response)

def error_response(message='操作失败', code=400):
    return jsonify({'code': code, 'message': message})

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

def migrate_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='devices'")
        if not cursor.fetchone():
            init_db()
            return
        
        cursor.execute("PRAGMA table_info(devices)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'device_model' not in columns:
            cursor.execute('ALTER TABLE devices ADD COLUMN device_model TEXT')
        if 'communication_mode' not in columns:
            cursor.execute('ALTER TABLE devices ADD COLUMN communication_mode TEXT')
        if 'operate_date' not in columns:
            cursor.execute('ALTER TABLE devices ADD COLUMN operate_date TEXT')
        if 'branch_area' not in columns:
            cursor.execute('ALTER TABLE devices ADD COLUMN branch_area TEXT')
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='work_orders'")
        if cursor.fetchone():
            cursor.execute("PRAGMA table_info(work_orders)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'fault_type' not in columns:
                cursor.execute('ALTER TABLE work_orders ADD COLUMN fault_type TEXT')
            if 'priority' not in columns:
                cursor.execute('ALTER TABLE work_orders ADD COLUMN priority TEXT DEFAULT "一般"')
        
        db.commit()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_code TEXT UNIQUE NOT NULL,
                device_name TEXT NOT NULL,
                device_model TEXT,
                communication_mode TEXT,
                branch_area TEXT,
                location TEXT NOT NULL,
                install_date TEXT NOT NULL,
                operate_date TEXT,
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
                fault_type TEXT NOT NULL,
                fault_description TEXT NOT NULL,
                priority TEXT NOT NULL DEFAULT '一般',
                reporter TEXT NOT NULL,
                reporter_phone TEXT,
                status TEXT NOT NULL DEFAULT '待处理',
                handle_user TEXT,
                handle_desc TEXT,
                create_time TEXT NOT NULL,
                handle_time TEXT,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS maintenance_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER NOT NULL,
                device_code TEXT NOT NULL,
                order_no TEXT,
                content TEXT NOT NULL,
                maintenance_user TEXT NOT NULL,
                before_status TEXT,
                after_status TEXT NOT NULL,
                create_time TEXT NOT NULL,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        ''')
        
        db.commit()

def generate_order_no():
    return 'WO' + datetime.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4().hex)[:4].upper()

FAULT_TYPES = ['硬件故障', '软件故障', '网络故障', '打印故障', '触摸屏故障', '其他']
PRIORITY_LEVELS = ['紧急', '高', '一般', '低']
BRANCH_AREAS = ['市区', '东区', '西区', '南区', '北区', '开发区', '县域']
DEVICE_STATUSES = ['正常', '故障', '维修中', '已修复']
ORDER_STATUSES = ['待处理', '处理中', '已完成']

@app.route('/api/devices', methods=['POST'])
def add_device():
    data = request.get_json()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO devices (device_code, device_name, device_model, communication_mode, 
                                branch_area, location, install_date, operate_date, status, create_time, update_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, '正常', ?, ?)
        ''', (
            data['device_code'],
            data['device_name'],
            data.get('device_model', ''),
            data.get('communication_mode', ''),
            data.get('branch_area', ''),
            data['location'],
            data['install_date'],
            data.get('operate_date', ''),
            now,
            now
        ))
        db.commit()
        
        return success_response({'id': cursor.lastrowid}, '设备录入成功')
    except sqlite3.IntegrityError:
        return error_response('设备编号已存在')

@app.route('/api/devices', methods=['GET'])
def get_devices():
    status = request.args.get('status')
    branch_area = request.args.get('branch_area')
    keyword = request.args.get('keyword', '')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    
    db = get_db()
    cursor = db.cursor()
    
    count_query = 'SELECT COUNT(*) as total FROM devices WHERE 1=1'
    query = 'SELECT * FROM devices WHERE 1=1'
    params = []
    
    if status:
        query += ' AND status = ?'
        count_query += ' AND status = ?'
        params.append(status)
    
    if branch_area:
        query += ' AND branch_area = ?'
        count_query += ' AND branch_area = ?'
        params.append(branch_area)
    
    if keyword:
        keyword_condition = ' AND (device_code LIKE ? OR device_name LIKE ? OR location LIKE ? OR device_model LIKE ?)'
        query += keyword_condition
        count_query += keyword_condition
        keyword_pattern = f'%{keyword}%'
        params.extend([keyword_pattern, keyword_pattern, keyword_pattern, keyword_pattern])
    
    cursor.execute(count_query, params)
    total = cursor.fetchone()['total']
    
    query += ' ORDER BY create_time DESC LIMIT ? OFFSET ?'
    params.extend([page_size, (page - 1) * page_size])
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    devices = []
    for row in rows:
        devices.append({
            'id': row['id'],
            'device_code': row['device_code'],
            'device_name': row['device_name'],
            'device_model': row['device_model'],
            'communication_mode': row['communication_mode'],
            'branch_area': row['branch_area'],
            'location': row['location'],
            'install_date': row['install_date'],
            'operate_date': row['operate_date'],
            'status': row['status'],
            'create_time': row['create_time'],
            'update_time': row['update_time']
        })
    
    return success_response({
        'list': devices,
        'total': total,
        'page': page,
        'page_size': page_size
    })

@app.route('/api/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM devices WHERE id = ?', (device_id,))
    row = cursor.fetchone()
    
    if not row:
        return error_response('设备不存在', 404)
    
    device = {
        'id': row['id'],
        'device_code': row['device_code'],
        'device_name': row['device_name'],
        'device_model': row['device_model'],
        'communication_mode': row['communication_mode'],
        'branch_area': row['branch_area'],
        'location': row['location'],
        'install_date': row['install_date'],
        'operate_date': row['operate_date'],
        'status': row['status'],
        'create_time': row['create_time'],
        'update_time': row['update_time']
    }
    
    return success_response(device)

@app.route('/api/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    data = request.get_json()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM devices WHERE id = ?', (device_id,))
    device = cursor.fetchone()
    
    if not device:
        return error_response('设备不存在', 404)
    
    try:
        cursor.execute('''
            UPDATE devices 
            SET device_code = ?, device_name = ?, device_model = ?, communication_mode = ?,
                branch_area = ?, location = ?, install_date = ?, operate_date = ?, update_time = ?
            WHERE id = ?
        ''', (
            data.get('device_code', device['device_code']),
            data.get('device_name', device['device_name']),
            data.get('device_model', device['device_model']),
            data.get('communication_mode', device['communication_mode']),
            data.get('branch_area', device['branch_area']),
            data.get('location', device['location']),
            data.get('install_date', device['install_date']),
            data.get('operate_date', device['operate_date']),
            now,
            device_id
        ))
        db.commit()
        
        return success_response(None, '设备更新成功')
    except sqlite3.IntegrityError:
        return error_response('设备编号已存在')

@app.route('/api/devices/<int:device_id>/status', methods=['PUT'])
def update_device_status(device_id):
    data = request.get_json()
    new_status = data.get('status')
    maintenance_user = data.get('maintenance_user', '管理员')
    content = data.get('content', '状态更新')
    
    if new_status not in DEVICE_STATUSES:
        return error_response(f'无效的状态值，可选值：{DEVICE_STATUSES}')
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM devices WHERE id = ?', (device_id,))
    device = cursor.fetchone()
    
    if not device:
        return error_response('设备不存在', 404)
    
    before_status = device['status']
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
        UPDATE devices SET status = ?, update_time = ? WHERE id = ?
    ''', (new_status, now, device_id))
    
    cursor.execute('''
        INSERT INTO maintenance_records (device_id, device_code, content, maintenance_user, before_status, after_status, create_time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (device_id, device['device_code'], content, maintenance_user, before_status, new_status, now))
    
    db.commit()
    
    return success_response(None, '状态更新成功')

@app.route('/api/work-orders', methods=['POST'])
def create_work_order():
    data = request.get_json()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    order_no = generate_order_no()
    
    fault_type = data.get('fault_type', '其他')
    if fault_type not in FAULT_TYPES:
        return error_response(f'无效的故障类型，可选值：{FAULT_TYPES}')
    
    priority = data.get('priority', '一般')
    if priority not in PRIORITY_LEVELS:
        return error_response(f'无效的优先级，可选值：{PRIORITY_LEVELS}')
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM devices WHERE id = ?', (data['device_id'],))
    device = cursor.fetchone()
    
    if not device:
        return error_response('设备不存在', 404)
    
    cursor.execute('''
        INSERT INTO work_orders (order_no, device_id, device_code, fault_type, fault_description, 
                                priority, reporter, reporter_phone, status, create_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, '待处理', ?)
    ''', (
        order_no,
        data['device_id'],
        device['device_code'],
        fault_type,
        data['fault_description'],
        priority,
        data.get('reporter', '匿名'),
        data.get('reporter_phone', ''),
        now
    ))
    
    cursor.execute('''
        UPDATE devices SET status = '故障', update_time = ? WHERE id = ?
    ''', (now, data['device_id']))
    
    db.commit()
    
    return success_response({'order_no': order_no, 'id': cursor.lastrowid}, '故障上报成功')

@app.route('/api/work-orders', methods=['GET'])
def get_work_orders():
    status = request.args.get('status')
    device_code = request.args.get('device_code', '')
    fault_type = request.args.get('fault_type')
    priority = request.args.get('priority')
    branch_area = request.args.get('branch_area')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    
    db = get_db()
    cursor = db.cursor()
    
    base_query = '''
        SELECT wo.*, d.branch_area 
        FROM work_orders wo 
        LEFT JOIN devices d ON wo.device_id = d.id 
        WHERE 1=1
    '''
    count_query = '''
        SELECT COUNT(*) as total 
        FROM work_orders wo 
        LEFT JOIN devices d ON wo.device_id = d.id 
        WHERE 1=1
    '''
    params = []
    
    if status:
        condition = ' AND wo.status = ?'
        base_query += condition
        count_query += condition
        params.append(status)
    
    if device_code:
        condition = ' AND wo.device_code LIKE ?'
        base_query += condition
        count_query += condition
        params.append(f'%{device_code}%')
    
    if fault_type:
        condition = ' AND wo.fault_type = ?'
        base_query += condition
        count_query += condition
        params.append(fault_type)
    
    if priority:
        condition = ' AND wo.priority = ?'
        base_query += condition
        count_query += condition
        params.append(priority)
    
    if branch_area:
        condition = ' AND d.branch_area = ?'
        base_query += condition
        count_query += condition
        params.append(branch_area)
    
    cursor.execute(count_query, params)
    total = cursor.fetchone()['total']
    
    base_query += ' ORDER BY CASE wo.priority WHEN "紧急" THEN 1 WHEN "高" THEN 2 WHEN "一般" THEN 3 ELSE 4 END, wo.create_time DESC LIMIT ? OFFSET ?'
    params.extend([page_size, (page - 1) * page_size])
    
    cursor.execute(base_query, params)
    rows = cursor.fetchall()
    
    orders = []
    for row in rows:
        orders.append({
            'id': row['id'],
            'order_no': row['order_no'],
            'device_id': row['device_id'],
            'device_code': row['device_code'],
            'fault_type': row['fault_type'],
            'fault_description': row['fault_description'],
            'priority': row['priority'],
            'reporter': row['reporter'],
            'reporter_phone': row['reporter_phone'],
            'status': row['status'],
            'handle_user': row['handle_user'],
            'handle_desc': row['handle_desc'],
            'create_time': row['create_time'],
            'handle_time': row['handle_time'],
            'branch_area': row['branch_area']
        })
    
    return success_response({
        'list': orders,
        'total': total,
        'page': page,
        'page_size': page_size
    })

@app.route('/api/work-orders/<int:order_id>/handle', methods=['PUT'])
def handle_work_order(order_id):
    data = request.get_json()
    handle_user = data.get('handle_user', '管理员')
    handle_desc = data.get('handle_desc', '')
    action = data.get('action', 'process')
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM work_orders WHERE id = ?', (order_id,))
    order = cursor.fetchone()
    
    if not order:
        return error_response('工单不存在', 404)
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if action == 'process':
        new_status = '处理中'
        device_status = '维修中'
    elif action == 'complete':
        new_status = '已完成'
        device_status = '已修复'
    else:
        return error_response('无效的操作，可选值：process/complete')
    
    cursor.execute('''
        UPDATE work_orders 
        SET status = ?, handle_user = ?, handle_desc = ?, handle_time = ?
        WHERE id = ?
    ''', (new_status, handle_user, handle_desc, now, order_id))
    
    cursor.execute('''
        UPDATE devices SET status = ?, update_time = ? WHERE id = ?
    ''', (device_status, now, order['device_id']))
    
    cursor.execute('SELECT device_code FROM devices WHERE id = ?', (order['device_id'],))
    device = cursor.fetchone()
    
    cursor.execute('''
        INSERT INTO maintenance_records (device_id, device_code, order_no, content, maintenance_user, before_status, after_status, create_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        order['device_id'],
        device['device_code'],
        order['order_no'],
        handle_desc or '工单处理',
        handle_user,
        order['status'],
        new_status,
        now
    ))
    
    db.commit()
    
    return success_response(None, '工单处理成功')

@app.route('/api/maintenance-records', methods=['GET'])
def get_maintenance_records():
    device_id = request.args.get('device_id')
    device_code = request.args.get('device_code', '')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    
    db = get_db()
    cursor = db.cursor()
    
    count_query = 'SELECT COUNT(*) as total FROM maintenance_records WHERE 1=1'
    query = 'SELECT * FROM maintenance_records WHERE 1=1'
    params = []
    
    if device_id:
        query += ' AND device_id = ?'
        count_query += ' AND device_id = ?'
        params.append(device_id)
    
    if device_code:
        query += ' AND device_code LIKE ?'
        count_query += ' AND device_code LIKE ?'
        params.append(f'%{device_code}%')
    
    if start_date:
        query += ' AND create_time >= ?'
        count_query += ' AND create_time >= ?'
        params.append(start_date)
    
    if end_date:
        query += ' AND create_time <= ?'
        count_query += ' AND create_time <= ?'
        params.append(end_date + ' 23:59:59')
    
    cursor.execute(count_query, params)
    total = cursor.fetchone()['total']
    
    query += ' ORDER BY create_time DESC LIMIT ? OFFSET ?'
    params.extend([page_size, (page - 1) * page_size])
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    records = []
    for row in rows:
        records.append({
            'id': row['id'],
            'device_id': row['device_id'],
            'device_code': row['device_code'],
            'order_no': row['order_no'],
            'content': row['content'],
            'maintenance_user': row['maintenance_user'],
            'before_status': row['before_status'],
            'after_status': row['after_status'],
            'create_time': row['create_time']
        })
    
    return success_response({
        'list': records,
        'total': total,
        'page': page,
        'page_size': page_size
    })

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT COUNT(*) as total FROM devices')
    total_devices = cursor.fetchone()['total']
    
    cursor.execute('SELECT COUNT(*) as count FROM devices WHERE status = "正常"')
    normal_devices = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM devices WHERE status = "故障"')
    fault_devices = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM devices WHERE status = "维修中"')
    repairing_devices = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM devices WHERE status = "已修复"')
    repaired_devices = cursor.fetchone()['count']
    
    availability_rate = (normal_devices + repaired_devices) / total_devices * 100 if total_devices > 0 else 0
    
    cursor.execute('SELECT COUNT(*) as total FROM work_orders')
    total_orders = cursor.fetchone()['total']
    
    cursor.execute('SELECT COUNT(*) as count FROM work_orders WHERE status = "待处理"')
    pending_orders = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM work_orders WHERE status = "处理中"')
    processing_orders = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM work_orders WHERE status = "已完成"')
    completed_orders = cursor.fetchone()['count']
    
    cursor.execute('SELECT fault_type, COUNT(*) as count FROM work_orders GROUP BY fault_type')
    fault_type_stats = cursor.fetchall()
    fault_type_distribution = {row['fault_type']: row['count'] for row in fault_type_stats}
    
    cursor.execute('SELECT priority, COUNT(*) as count FROM work_orders GROUP BY priority')
    priority_stats = cursor.fetchall()
    priority_distribution = {row['priority']: row['count'] for row in priority_stats}
    
    cursor.execute('''
        SELECT d.branch_area, 
               COUNT(*) as total,
               SUM(CASE WHEN d.status IN ('正常', '已修复') THEN 1 ELSE 0 END) as available
        FROM devices d 
        WHERE d.branch_area IS NOT NULL AND d.branch_area != ''
        GROUP BY d.branch_area
    ''')
    area_stats = cursor.fetchall()
    area_distribution = []
    for row in area_stats:
        area_distribution.append({
            'branch_area': row['branch_area'],
            'total': row['total'],
            'available': row['available'],
            'availability_rate': round(row['available'] / row['total'] * 100, 2) if row['total'] > 0 else 0
        })
    
    return success_response({
        'devices': {
            'total': total_devices,
            'normal': normal_devices,
            'fault': fault_devices,
            'repairing': repairing_devices,
            'repaired': repaired_devices,
            'availability_rate': round(availability_rate, 2)
        },
        'work_orders': {
            'total': total_orders,
            'pending': pending_orders,
            'processing': processing_orders,
            'completed': completed_orders,
            'fault_type_distribution': fault_type_distribution,
            'priority_distribution': priority_distribution
        },
        'area_distribution': area_distribution
    })

@app.route('/api/dictionary', methods=['GET'])
def get_dictionary():
    return success_response({
        'fault_types': FAULT_TYPES,
        'priority_levels': PRIORITY_LEVELS,
        'device_statuses': DEVICE_STATUSES,
        'order_statuses': ORDER_STATUSES,
        'branch_areas': BRANCH_AREAS,
        'communication_modes': ['有线网络', '无线网络', '4G', '5G', '其他']
    })

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    else:
        migrate_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
