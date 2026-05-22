import sqlite3
import datetime
from flask import Flask, request, jsonify, g
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE = 'device_management.db'

DEVICE_STATUSES = ['正常', '故障', '维修中', '已修复']
WORK_ORDER_STATUSES = ['待处理', '处理中', '已完成']
HALL_AREAS = ['一楼大厅', '二楼大厅', '三楼大厅', 'VIP服务区', '24小时自助区']

FAULT_TYPES = {
    'hardware': '硬件故障',
    'software': '软件故障',
    'network': '网络故障',
    'printer': '打印故障',
    'touchscreen': '触摸屏故障',
    'power': '电源故障',
    'other': '其他故障'
}

URGENCY_LEVELS = {
    'high': {'name': '高', 'color': '#ff4d4f', 'description': '影响政务大厅正常服务，需立即处理'},
    'medium': {'name': '中', 'color': '#faad14', 'description': '影响部分业务，需4小时内处理'},
    'low': {'name': '低', 'color': '#52c41a', 'description': '不影响主要业务，可安排时间处理'}
}

COMMUNICATION_MODES = ['以太网', 'WiFi', '4G', '5G', '专网']

def success_response(data=None, message='操作成功', code=200):
    return jsonify({
        'code': code,
        'success': True,
        'message': message,
        'data': data,
        'timestamp': datetime.datetime.now().isoformat()
    })

def error_response(message='操作失败', code=400, errors=None):
    return jsonify({
        'code': code,
        'success': False,
        'message': message,
        'errors': errors,
        'timestamp': datetime.datetime.now().isoformat()
    })

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

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('DROP TABLE IF EXISTS maintenance_logs')
        cursor.execute('DROP TABLE IF EXISTS maintenance_records')
        cursor.execute('DROP TABLE IF EXISTS work_orders')
        cursor.execute('DROP TABLE IF EXISTS devices')
        
        cursor.execute('''
            CREATE TABLE devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_code TEXT UNIQUE NOT NULL,
                device_name TEXT NOT NULL,
                device_model TEXT,
                location TEXT NOT NULL,
                hall_area TEXT NOT NULL,
                communication_mode TEXT,
                status TEXT NOT NULL DEFAULT '正常',
                install_date TEXT,
                commission_date TEXT,
                last_maintenance_date TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE work_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_no TEXT UNIQUE NOT NULL,
                device_id INTEGER NOT NULL,
                device_code TEXT NOT NULL,
                device_name TEXT NOT NULL,
                hall_area TEXT NOT NULL,
                fault_type TEXT NOT NULL,
                fault_category TEXT NOT NULL,
                urgency_level TEXT NOT NULL DEFAULT 'medium',
                urgency_color TEXT NOT NULL DEFAULT '#faad14',
                fault_description TEXT,
                reporter TEXT,
                reporter_phone TEXT,
                status TEXT NOT NULL DEFAULT '待处理',
                handler TEXT,
                handle_description TEXT,
                created_at TEXT NOT NULL,
                handled_at TEXT,
                completed_at TEXT,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE maintenance_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER NOT NULL,
                work_order_id INTEGER,
                order_no TEXT,
                maintenance_type TEXT NOT NULL,
                description TEXT,
                parts_used TEXT,
                operator TEXT NOT NULL,
                duration_minutes INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                FOREIGN KEY (device_id) REFERENCES devices (id),
                FOREIGN KEY (work_order_id) REFERENCES work_orders (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE maintenance_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                work_order_id INTEGER NOT NULL,
                log_type TEXT NOT NULL,
                content TEXT NOT NULL,
                operator TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (work_order_id) REFERENCES work_orders (id)
            )
        ''')
        
        db.commit()

def generate_order_no():
    now = datetime.datetime.now()
    date_str = now.strftime('%Y%m%d')
    prefix = f'WO{date_str}'
    
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT order_no FROM work_orders WHERE order_no LIKE ? ORDER BY order_no DESC LIMIT 1', (f'{prefix}%',))
        result = cursor.fetchone()
        
        if result:
            last_no = result['order_no']
            seq = int(last_no[-4:]) + 1
        else:
            seq = 1
        
        return f'{prefix}{seq:04d}'

@app.route('/api/constants', methods=['GET'])
def get_constants():
    return success_response({
        'device_statuses': DEVICE_STATUSES,
        'work_order_statuses': WORK_ORDER_STATUSES,
        'fault_types': FAULT_TYPES,
        'urgency_levels': URGENCY_LEVELS,
        'communication_modes': COMMUNICATION_MODES,
        'hall_areas': HALL_AREAS
    })

@app.route('/api/hall-areas', methods=['GET'])
def get_hall_areas():
    return success_response(HALL_AREAS)

@app.route('/api/devices', methods=['POST'])
def create_device():
    data = request.json
    now = datetime.datetime.now().isoformat()
    
    required_fields = ['device_code', 'device_name', 'location', 'hall_area']
    for field in required_fields:
        if field not in data:
            return error_response(f'缺少必填字段: {field}', 400)
    
    if 'communication_mode' in data and data['communication_mode'] not in COMMUNICATION_MODES:
        return error_response(f'无效通信方式，有效值为: {COMMUNICATION_MODES}', 400)
    
    if 'hall_area' in data and data['hall_area'] not in HALL_AREAS:
        return error_response(f'无效大厅区域，有效值为: {HALL_AREAS}', 400)
    
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO devices (
                device_code, device_name, device_model, location, hall_area,
                communication_mode, status, install_date, commission_date,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['device_code'],
            data['device_name'],
            data.get('device_model', ''),
            data['location'],
            data['hall_area'],
            data.get('communication_mode', ''),
            data.get('status', '正常'),
            data.get('install_date', ''),
            data.get('commission_date', ''),
            now,
            now
        ))
        db.commit()
        
        return success_response({'id': cursor.lastrowid}, '设备录入成功', 201)
    except sqlite3.IntegrityError:
        return error_response('设备编号已存在', 400)

@app.route('/api/devices', methods=['GET'])
def get_devices():
    status = request.args.get('status')
    hall_area = request.args.get('hall_area')
    communication_mode = request.args.get('communication_mode')
    keyword = request.args.get('keyword')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    
    db = get_db()
    cursor = db.cursor()
    
    query = 'SELECT * FROM devices WHERE 1=1'
    count_query = 'SELECT COUNT(*) as total FROM devices WHERE 1=1'
    params = []
    
    if status:
        query += ' AND status = ?'
        count_query += ' AND status = ?'
        params.append(status)
    
    if hall_area:
        query += ' AND hall_area = ?'
        count_query += ' AND hall_area = ?'
        params.append(hall_area)
    
    if communication_mode:
        query += ' AND communication_mode = ?'
        count_query += ' AND communication_mode = ?'
        params.append(communication_mode)
    
    if keyword:
        query += ' AND (device_code LIKE ? OR device_name LIKE ? OR device_model LIKE ? OR location LIKE ?)'
        count_query += ' AND (device_code LIKE ? OR device_name LIKE ? OR device_model LIKE ? OR location LIKE ?)'
        params.extend([f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'])
    
    query += ' ORDER BY created_at DESC LIMIT ? OFFSET ?'
    params.extend([page_size, (page - 1) * page_size])
    
    cursor.execute(count_query, params[:-2] if len(params) >= 2 else params)
    total = cursor.fetchone()['total']
    
    cursor.execute(query, params)
    devices = cursor.fetchall()
    
    device_list = [dict(device) for device in devices]
    
    return success_response({
        'list': device_list,
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total': total,
            'total_pages': (total + page_size - 1) // page_size
        }
    })

@app.route('/api/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM devices WHERE id = ?', (device_id,))
    device = cursor.fetchone()
    
    if not device:
        return error_response('设备不存在', 404)
    
    device_dict = dict(device)
    
    cursor.execute('SELECT * FROM work_orders WHERE device_id = ? ORDER BY created_at DESC LIMIT 5', (device_id,))
    recent_orders = cursor.fetchall()
    device_dict['recent_orders'] = [dict(order) for order in recent_orders]
    
    cursor.execute('SELECT * FROM maintenance_records WHERE device_id = ? ORDER BY created_at DESC LIMIT 5', (device_id,))
    recent_maintenance = cursor.fetchall()
    device_dict['recent_maintenance'] = [dict(record) for record in recent_maintenance]
    
    return success_response(device_dict)

@app.route('/api/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    data = request.json
    now = datetime.datetime.now().isoformat()
    
    if 'communication_mode' in data and data['communication_mode'] not in COMMUNICATION_MODES:
        return error_response(f'无效通信方式，有效值为: {COMMUNICATION_MODES}', 400)
    
    if 'hall_area' in data and data['hall_area'] not in HALL_AREAS:
        return error_response(f'无效大厅区域，有效值为: {HALL_AREAS}', 400)
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM devices WHERE id = ?', (device_id,))
    if not cursor.fetchone():
        return error_response('设备不存在', 404)
    
    update_fields = []
    update_values = []
    
    for field in ['device_name', 'device_model', 'location', 'hall_area', 'communication_mode', 'status', 'install_date', 'commission_date']:
        if field in data:
            update_fields.append(f'{field} = ?')
            update_values.append(data[field])
    
    if not update_fields:
        return error_response('没有需要更新的字段', 400)
    
    update_fields.append('updated_at = ?')
    update_values.append(now)
    update_values.append(device_id)
    
    query = f"UPDATE devices SET {', '.join(update_fields)} WHERE id = ?"
    cursor.execute(query, update_values)
    db.commit()
    
    if 'hall_area' in data:
        cursor.execute('UPDATE work_orders SET hall_area = ? WHERE device_id = ?', (data['hall_area'], device_id))
        db.commit()
    
    return success_response(None, '设备信息更新成功')

@app.route('/api/devices/<int:device_id>/status', methods=['PUT'])
def update_device_status(device_id):
    data = request.json
    new_status = data.get('status')
    
    if new_status not in DEVICE_STATUSES:
        return error_response(f'无效状态，有效值为: {DEVICE_STATUSES}', 400)
    
    now = datetime.datetime.now().isoformat()
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM devices WHERE id = ?', (device_id,))
    device = cursor.fetchone()
    if not device:
        return error_response('设备不存在', 404)
    
    old_status = device['status']
    
    cursor.execute('''
        UPDATE devices SET status = ?, updated_at = ? WHERE id = ?
    ''', (new_status, now, device_id))
    db.commit()
    
    return success_response({
        'old_status': old_status,
        'new_status': new_status
    }, '设备状态更新成功')

@app.route('/api/devices/<int:device_id>/work-orders', methods=['GET'])
def get_device_work_orders(device_id):
    status = request.args.get('status')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    
    db = get_db()
    cursor = db.cursor()
    
    query = 'SELECT * FROM work_orders WHERE device_id = ?'
    count_query = 'SELECT COUNT(*) as total FROM work_orders WHERE device_id = ?'
    params = [device_id]
    
    if status:
        query += ' AND status = ?'
        count_query += ' AND status = ?'
        params.append(status)
    
    query += ' ORDER BY CASE urgency_level WHEN "high" THEN 1 WHEN "medium" THEN 2 ELSE 3 END, created_at DESC LIMIT ? OFFSET ?'
    params.extend([page_size, (page - 1) * page_size])
    
    cursor.execute(count_query, params[:-2] if len(params) >= 2 else params)
    total = cursor.fetchone()['total']
    
    cursor.execute(query, params)
    orders = cursor.fetchall()
    
    return success_response({
        'list': [dict(order) for order in orders],
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total': total,
            'total_pages': (total + page_size - 1) // page_size
        }
    })

@app.route('/api/work-orders', methods=['POST'])
def create_work_order():
    data = request.json
    now = datetime.datetime.now().isoformat()
    order_no = generate_order_no()
    
    required_fields = ['device_id', 'fault_type']
    for field in required_fields:
        if field not in data:
            return error_response(f'缺少必填字段: {field}', 400)
    
    if data['fault_type'] not in FAULT_TYPES:
        return error_response(f'无效故障类型，有效值为: {list(FAULT_TYPES.keys())}', 400)
    
    urgency = data.get('urgency_level', 'medium')
    if urgency not in URGENCY_LEVELS:
        return error_response(f'无效紧急级别，有效值为: {list(URGENCY_LEVELS.keys())}', 400)
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM devices WHERE id = ?', (data['device_id'],))
    device = cursor.fetchone()
    if not device:
        return error_response('设备不存在', 404)
    
    cursor.execute('''
        INSERT INTO work_orders (
            order_no, device_id, device_code, device_name, hall_area,
            fault_type, fault_category, urgency_level, urgency_color,
            fault_description, reporter, reporter_phone, status, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        order_no,
        data['device_id'],
        device['device_code'],
        device['device_name'],
        device['hall_area'],
        data['fault_type'],
        FAULT_TYPES[data['fault_type']],
        urgency,
        URGENCY_LEVELS[urgency]['color'],
        data.get('fault_description', ''),
        data.get('reporter', ''),
        data.get('reporter_phone', ''),
        '待处理',
        now
    ))
    order_id = cursor.lastrowid
    
    cursor.execute('''
        UPDATE devices SET status = '故障', updated_at = ? WHERE id = ?
    ''', (now, data['device_id']))
    
    cursor.execute('''
        INSERT INTO maintenance_logs (work_order_id, log_type, content, created_at)
        VALUES (?, ?, ?, ?)
    ''', (order_id, 'create', f'工单创建，故障类型: {FAULT_TYPES[data["fault_type"]]}', now))
    
    db.commit()
    
    return success_response({'order_no': order_no, 'id': order_id}, '故障上报成功', 201)

@app.route('/api/work-orders', methods=['GET'])
def get_work_orders():
    status = request.args.get('status')
    device_id = request.args.get('device_id')
    fault_type = request.args.get('fault_type')
    urgency_level = request.args.get('urgency_level')
    hall_area = request.args.get('hall_area')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    
    db = get_db()
    cursor = db.cursor()
    
    query = 'SELECT * FROM work_orders WHERE 1=1'
    count_query = 'SELECT COUNT(*) as total FROM work_orders WHERE 1=1'
    params = []
    
    if status:
        query += ' AND status = ?'
        count_query += ' AND status = ?'
        params.append(status)
    
    if device_id:
        query += ' AND device_id = ?'
        count_query += ' AND device_id = ?'
        params.append(device_id)
    
    if fault_type:
        query += ' AND fault_type = ?'
        count_query += ' AND fault_type = ?'
        params.append(fault_type)
    
    if urgency_level:
        query += ' AND urgency_level = ?'
        count_query += ' AND urgency_level = ?'
        params.append(urgency_level)
    
    if hall_area:
        query += ' AND hall_area = ?'
        count_query += ' AND hall_area = ?'
        params.append(hall_area)
    
    query += ' ORDER BY CASE urgency_level WHEN "high" THEN 1 WHEN "medium" THEN 2 ELSE 3 END, created_at DESC LIMIT ? OFFSET ?'
    params.extend([page_size, (page - 1) * page_size])
    
    cursor.execute(count_query, params[:-2] if len(params) >= 2 else params)
    total = cursor.fetchone()['total']
    
    cursor.execute(query, params)
    orders = cursor.fetchall()
    
    return success_response({
        'list': [dict(order) for order in orders],
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total': total,
            'total_pages': (total + page_size - 1) // page_size
        }
    })

@app.route('/api/work-orders/<int:order_id>', methods=['GET'])
def get_work_order(order_id):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM work_orders WHERE id = ?', (order_id,))
    work_order = cursor.fetchone()
    
    if not work_order:
        return error_response('工单不存在', 404)
    
    order_dict = dict(work_order)
    
    cursor.execute('SELECT * FROM devices WHERE id = ?', (order_dict['device_id'],))
    device = cursor.fetchone()
    if device:
        order_dict['device'] = dict(device)
    
    cursor.execute('SELECT * FROM maintenance_logs WHERE work_order_id = ? ORDER BY created_at ASC', (order_id,))
    logs = cursor.fetchall()
    order_dict['maintenance_logs'] = [dict(log) for log in logs]
    
    return success_response(order_dict)

@app.route('/api/work-orders/<int:order_id>/handle', methods=['PUT'])
def handle_work_order(order_id):
    data = request.json
    now = datetime.datetime.now().isoformat()
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM work_orders WHERE id = ?', (order_id,))
    work_order = cursor.fetchone()
    
    if not work_order:
        return error_response('工单不存在', 404)
    
    new_status = data.get('status', work_order['status'])
    
    if new_status not in WORK_ORDER_STATUSES:
        return error_response(f'无效状态，有效值为: {WORK_ORDER_STATUSES}', 400)
    
    handler = data.get('handler', work_order['handler'])
    handle_description = data.get('handle_description', work_order['handle_description'])
    
    update_fields = ['status = ?', 'handler = ?', 'handle_description = ?']
    update_values = [new_status, handler, handle_description]
    
    if new_status == '处理中' and work_order['status'] == '待处理':
        update_fields.append('handled_at = ?')
        update_values.append(now)
    
    if new_status == '已完成':
        update_fields.append('completed_at = ?')
        update_values.append(now)
    
    update_values.append(order_id)
    
    query = f"UPDATE work_orders SET {', '.join(update_fields)} WHERE id = ?"
    cursor.execute(query, update_values)
    
    if new_status == '处理中' and work_order['status'] != '处理中':
        cursor.execute('''
            UPDATE devices SET status = '维修中', updated_at = ? WHERE id = ?
        ''', (now, work_order['device_id']))
        
        cursor.execute('''
            INSERT INTO maintenance_logs (work_order_id, log_type, content, operator, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (order_id, 'start', f'开始处理: {handle_description}', handler, now))
    
    elif new_status == '已完成' and work_order['status'] != '已完成':
        cursor.execute('''
            UPDATE devices SET status = '已修复', updated_at = ? WHERE id = ?
        ''', (now, work_order['device_id']))
        
        cursor.execute('''
            INSERT INTO maintenance_records (
                device_id, work_order_id, order_no, maintenance_type, description, operator, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            work_order['device_id'],
            order_id,
            work_order['order_no'],
            '故障维修',
            handle_description,
            handler,
            now
        ))
        
        cursor.execute('''
            INSERT INTO maintenance_logs (work_order_id, log_type, content, operator, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (order_id, 'complete', f'工单完成: {handle_description}', handler, now))
    
    db.commit()
    
    return success_response({'new_status': new_status}, '工单处理成功')

@app.route('/api/work-orders/<int:order_id>/logs', methods=['POST'])
def add_maintenance_log(order_id):
    data = request.json
    now = datetime.datetime.now().isoformat()
    
    if 'content' not in data:
        return error_response('缺少日志内容', 400)
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM work_orders WHERE id = ?', (order_id,))
    if not cursor.fetchone():
        return error_response('工单不存在', 404)
    
    cursor.execute('''
        INSERT INTO maintenance_logs (work_order_id, log_type, content, operator, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        order_id,
        data.get('log_type', 'progress'),
        data['content'],
        data.get('operator', ''),
        now
    ))
    db.commit()
    
    return success_response({'id': cursor.lastrowid}, '维修日志添加成功', 201)

@app.route('/api/maintenance-records', methods=['GET'])
def get_maintenance_records():
    device_id = request.args.get('device_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    maintenance_type = request.args.get('maintenance_type')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    
    db = get_db()
    cursor = db.cursor()
    
    query = '''
        SELECT mr.*, d.device_code, d.device_name, d.hall_area, wo.order_no
        FROM maintenance_records mr
        LEFT JOIN devices d ON mr.device_id = d.id
        LEFT JOIN work_orders wo ON mr.work_order_id = wo.id
        WHERE 1=1
    '''
    count_query = 'SELECT COUNT(*) as total FROM maintenance_records WHERE 1=1'
    params = []
    
    if device_id:
        query += ' AND mr.device_id = ?'
        count_query += ' AND device_id = ?'
        params.append(device_id)
    
    if maintenance_type:
        query += ' AND mr.maintenance_type = ?'
        count_query += ' AND maintenance_type = ?'
        params.append(maintenance_type)
    
    if start_date:
        query += ' AND mr.created_at >= ?'
        count_query += ' AND created_at >= ?'
        params.append(start_date)
    
    if end_date:
        query += ' AND mr.created_at <= ?'
        count_query += ' AND created_at <= ?'
        params.append(end_date)
    
    query += ' ORDER BY mr.created_at DESC LIMIT ? OFFSET ?'
    params.extend([page_size, (page - 1) * page_size])
    
    cursor.execute(count_query, params[:-2] if len(params) >= 2 else params)
    total = cursor.fetchone()['total']
    
    cursor.execute(query, params)
    records = cursor.fetchall()
    
    return success_response({
        'list': [dict(record) for record in records],
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total': total,
            'total_pages': (total + page_size - 1) // page_size
        }
    })

@app.route('/api/maintenance-records', methods=['POST'])
def create_maintenance_record():
    data = request.json
    now = datetime.datetime.now().isoformat()
    
    required_fields = ['device_id', 'maintenance_type', 'operator']
    for field in required_fields:
        if field not in data:
            return error_response(f'缺少必填字段: {field}', 400)
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM devices WHERE id = ?', (data['device_id'],))
    if not cursor.fetchone():
        return error_response('设备不存在', 404)
    
    cursor.execute('''
        INSERT INTO maintenance_records (
            device_id, work_order_id, maintenance_type, description, parts_used, operator, duration_minutes, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['device_id'],
        data.get('work_order_id'),
        data['maintenance_type'],
        data.get('description', ''),
        data.get('parts_used', ''),
        data['operator'],
        data.get('duration_minutes', 0),
        now
    ))
    record_id = cursor.lastrowid
    
    cursor.execute('''
        UPDATE devices SET last_maintenance_date = ?, updated_at = ? WHERE id = ?
    ''', (now, now, data['device_id']))
    db.commit()
    
    return success_response({'id': record_id}, '运维记录创建成功', 201)

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT COUNT(*) as total FROM devices')
    total_devices = cursor.fetchone()['total']
    
    device_stats = {}
    for status in DEVICE_STATUSES:
        cursor.execute("SELECT COUNT(*) as count FROM devices WHERE status = ?", (status,))
        device_stats[status] = cursor.fetchone()['count']
    
    availability_rate = 0
    if total_devices > 0:
        normal_devices = device_stats.get('正常', 0) + device_stats.get('已修复', 0)
        availability_rate = round((normal_devices / total_devices) * 100, 2)
    
    cursor.execute("SELECT COUNT(*) as total FROM work_orders")
    total_orders = cursor.fetchone()['total']
    
    order_stats = {}
    for status in WORK_ORDER_STATUSES:
        cursor.execute("SELECT COUNT(*) as count FROM work_orders WHERE status = ?", (status,))
        order_stats[status] = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM work_orders WHERE urgency_level = 'high'")
    high_urgency_orders = cursor.fetchone()['count']
    
    fault_stats = {}
    for fault_type in FAULT_TYPES.keys():
        cursor.execute("SELECT COUNT(*) as count FROM work_orders WHERE fault_type = ?", (fault_type,))
        fault_stats[fault_type] = cursor.fetchone()['count']
    
    area_stats = {}
    for area in HALL_AREAS:
        cursor.execute("SELECT COUNT(*) as count FROM devices WHERE hall_area = ?", (area,))
        device_count = cursor.fetchone()['count']
        cursor.execute("SELECT COUNT(*) as count FROM devices WHERE hall_area = ? AND status IN ('正常', '已修复')", (area,))
        normal_count = cursor.fetchone()['count']
        area_availability = round((normal_count / device_count * 100), 2) if device_count > 0 else 0
        
        cursor.execute("SELECT COUNT(*) as count FROM work_orders WHERE hall_area = ? AND status = '待处理'", (area,))
        pending_orders = cursor.fetchone()['count']
        
        area_stats[area] = {
            'device_count': device_count,
            'normal_count': normal_count,
            'availability_rate': area_availability,
            'pending_orders': pending_orders
        }
    
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    cursor.execute("SELECT COUNT(*) as count FROM work_orders WHERE DATE(created_at) = ?", (today,))
    today_new_orders = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM work_orders WHERE DATE(completed_at) = ?", (today,))
    today_completed_orders = cursor.fetchone()['count']
    
    return success_response({
        'devices': {
            'total': total_devices,
            'by_status': device_stats,
            'availability_rate': availability_rate
        },
        'work_orders': {
            'total': total_orders,
            'by_status': order_stats,
            'high_urgency': high_urgency_orders,
            'by_fault_type': fault_stats,
            'today_new': today_new_orders,
            'today_completed': today_completed_orders
        },
        'by_area': area_stats
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
