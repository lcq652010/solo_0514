from flask import Flask, request, jsonify, g
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATABASE = 'vehicle_admin.db'

DEVICE_STATUSES = ['正常', '故障', '维修中', '已修复']

DB_INITIALIZED = False

def ensure_db_initialized():
    global DB_INITIALIZED
    if not DB_INITIALIZED:
        init_db()
        DB_INITIALIZED = True

FAULT_TYPES = [
    '硬件故障',
    '软件故障',
    '网络故障',
    '摄像头故障',
    '打印机故障',
    '身份证阅读器故障',
    '触摸屏故障',
    '系统崩溃',
    '其他故障'
]

PRIORITY_LEVELS = ['紧急', '高', '一般', '低']

PRIORITY_DESCRIPTIONS = {
    '紧急': '影响核心业务，导致大厅业务停滞，需立即处理',
    '高': '影响重要业务，导致部分功能不可用，需优先处理',
    '一般': '影响较小，可按正常流程处理',
    '低': '轻微问题，不影响正常使用，可延后处理'
}

BRANCH_LIST = [
    '车管所一楼大厅',
    '车管所二楼办证区',
    '车管所三楼制证区',
    '车管所A网点',
    '车管所B网点',
    '车管所C网点'
]

ORDER_STATUS_LIST = ['待处理', '处理中', '已完成', '已取消']

def success_response(data=None, message='操作成功', code=200):
    response = {
        'code': code,
        'message': message,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    if data is not None:
        response['data'] = data
    return jsonify(response)

def error_response(message='操作失败', code=400):
    return jsonify({
        'code': code,
        'message': message,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }), code

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

@app.before_request
def before_request():
    ensure_db_initialized()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_code TEXT UNIQUE NOT NULL,
                device_name TEXT NOT NULL,
                location TEXT NOT NULL,
                branch TEXT NOT NULL DEFAULT '车管所一楼大厅',
                status TEXT DEFAULT '正常',
                install_date TEXT NOT NULL,
                last_maintain_date TEXT,
                remark TEXT,
                create_time TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        try:
            cursor.execute("PRAGMA table_info(devices)")
            columns = [col[1] for col in cursor.fetchall()]
            if 'branch' not in columns:
                cursor.execute('ALTER TABLE devices ADD COLUMN branch TEXT DEFAULT "车管所一楼大厅"')
                print('数据库迁移成功：已添加 branch 字段')
        except Exception as e:
            print(f'数据库迁移检查跳过: {e}')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS work_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_no TEXT UNIQUE NOT NULL,
                device_id INTEGER NOT NULL,
                device_code TEXT NOT NULL,
                fault_type TEXT NOT NULL,
                fault_desc TEXT NOT NULL,
                priority TEXT DEFAULT '一般',
                reporter TEXT NOT NULL,
                reporter_phone TEXT,
                status TEXT DEFAULT '待处理',
                handle_user TEXT,
                handle_desc TEXT,
                handle_time TEXT,
                create_time TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS maintain_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER NOT NULL,
                device_code TEXT NOT NULL,
                maintain_type TEXT NOT NULL,
                maintain_desc TEXT NOT NULL,
                maintain_user TEXT NOT NULL,
                maintain_time TEXT NOT NULL,
                remark TEXT,
                create_time TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        ''')
        
        try:
            cursor.execute("PRAGMA table_info(work_orders)")
            columns = [col[1] for col in cursor.fetchall()]
            if 'priority' not in columns:
                cursor.execute('ALTER TABLE work_orders ADD COLUMN priority TEXT DEFAULT "一般"')
                print('数据库迁移成功：已添加 priority 字段')
        except Exception as e:
            print(f'数据库迁移检查跳过: {e}')
        
        db.commit()
        print('数据库初始化完成')

def generate_order_no():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        date_prefix = datetime.now().strftime('%Y%m%d')
        cursor.execute('SELECT order_no FROM work_orders WHERE order_no LIKE ? ORDER BY order_no DESC LIMIT 1', (f'{date_prefix}%',))
        result = cursor.fetchone()
        if result:
            last_no = result['order_no']
            seq = int(last_no[-4:]) + 1
        else:
            seq = 1
        return f'{date_prefix}{seq:04d}'

@app.route('/api/devices', methods=['GET'])
def get_devices():
    db = get_db()
    cursor = db.cursor()
    
    status = request.args.get('status')
    branch = request.args.get('branch')
    keyword = request.args.get('keyword')
    
    query = 'SELECT * FROM devices WHERE 1=1'
    params = []
    
    if status:
        query += ' AND status = ?'
        params.append(status)
    
    if branch:
        query += ' AND branch = ?'
        params.append(branch)
    
    if keyword:
        query += ' AND (device_code LIKE ? OR device_name LIKE ?)'
        params.extend([f'%{keyword}%', f'%{keyword}%'])
    
    query += ' ORDER BY create_time DESC'
    cursor.execute(query, params)
    devices = [dict(row) for row in cursor.fetchall()]
    
    return success_response(devices, '获取设备列表成功')

@app.route('/api/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM devices WHERE id = ?', (device_id,))
    device = cursor.fetchone()
    if device:
        return success_response(dict(device), '获取设备信息成功')
    return error_response('设备不存在', 404)

@app.route('/api/devices', methods=['POST'])
def add_device():
    data = request.get_json()
    required_fields = ['device_code', 'device_name', 'location', 'branch', 'install_date']
    for field in required_fields:
        if field not in data or not data[field]:
            return error_response(f'{field} 不能为空')
    
    if 'branch' in data and data['branch'] not in BRANCH_LIST:
        return error_response('网点不在可选范围内')
    
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO devices (device_code, device_name, location, branch, status, install_date, remark)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['device_code'],
            data['device_name'],
            data['location'],
            data['branch'],
            data.get('status', '正常'),
            data['install_date'],
            data.get('remark', '')
        ))
        db.commit()
        return success_response({'id': cursor.lastrowid}, '设备添加成功')
    except sqlite3.IntegrityError:
        return error_response('设备编号已存在')

@app.route('/api/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM devices WHERE id = ?', (device_id,))
    if not cursor.fetchone():
        return error_response('设备不存在', 404)
    
    if 'branch' in data and data['branch'] not in BRANCH_LIST:
        return error_response('网点不在可选范围内')
    
    update_fields = []
    update_values = []
    
    for field in ['device_name', 'location', 'branch', 'status', 'install_date', 'last_maintain_date', 'remark']:
        if field in data:
            update_fields.append(f'{field} = ?')
            update_values.append(data[field])
    
    if not update_fields:
        return error_response('没有更新字段')
    
    update_values.append(device_id)
    
    cursor.execute(f'''
        UPDATE devices SET {', '.join(update_fields)} WHERE id = ?
    ''', update_values)
    db.commit()
    
    return success_response(None, '设备更新成功')

@app.route('/api/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM devices WHERE id = ?', (device_id,))
    if not cursor.fetchone():
        return error_response('设备不存在', 404)
    
    cursor.execute('DELETE FROM devices WHERE id = ?', (device_id,))
    db.commit()
    
    return success_response(None, '设备删除成功')

@app.route('/api/devices/<int:device_id>/status', methods=['PUT'])
def update_device_status(device_id):
    data = request.get_json()
    status = data.get('status')
    
    if status not in DEVICE_STATUSES:
        return error_response(f'状态必须是: {", ".join(DEVICE_STATUSES)}')
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM devices WHERE id = ?', (device_id,))
    if not cursor.fetchone():
        return error_response('设备不存在', 404)
    
    cursor.execute('UPDATE devices SET status = ? WHERE id = ?', (status, device_id))
    db.commit()
    
    return success_response(None, '设备状态更新成功')

@app.route('/api/work-orders', methods=['GET'])
def get_work_orders():
    db = get_db()
    cursor = db.cursor()
    
    status = request.args.get('status')
    fault_type = request.args.get('fault_type')
    priority = request.args.get('priority')
    device_id = request.args.get('device_id')
    branch = request.args.get('branch')
    keyword = request.args.get('keyword')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    
    base_query = '''
        SELECT wo.*, d.device_name, d.location, d.branch 
        FROM work_orders wo 
        LEFT JOIN devices d ON wo.device_id = d.id
    '''
    conditions = []
    params = []
    
    if status:
        conditions.append('wo.status = ?')
        params.append(status)
    
    if fault_type:
        conditions.append('wo.fault_type = ?')
        params.append(fault_type)
    
    if priority:
        conditions.append('wo.priority = ?')
        params.append(priority)
    
    if device_id:
        conditions.append('wo.device_id = ?')
        params.append(device_id)
    
    if branch:
        conditions.append('d.branch = ?')
        params.append(branch)
    
    if keyword:
        conditions.append('(wo.order_no LIKE ? OR d.device_name LIKE ? OR wo.fault_desc LIKE ?)')
        params.extend([f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'])
    
    where_clause = ' WHERE ' + ' AND '.join(conditions) if conditions else ''
    
    order_by = '''
        ORDER BY CASE wo.priority 
            WHEN '紧急' THEN 1 
            WHEN '高' THEN 2 
            WHEN '一般' THEN 3 
            ELSE 4 
        END, wo.create_time DESC
    '''
    
    count_query = f'''
        SELECT COUNT(*) as total 
        FROM work_orders wo 
        LEFT JOIN devices d ON wo.device_id = d.id
        {where_clause}
    '''
    cursor.execute(count_query, params)
    total = cursor.fetchone()['total']
    
    limit_offset = ' LIMIT ? OFFSET ?'
    params.extend([page_size, (page - 1) * page_size])
    
    full_query = base_query + where_clause + order_by + limit_offset
    cursor.execute(full_query, params)
    orders = [dict(row) for row in cursor.fetchall()]
    
    for order in orders:
        order['priority_desc'] = PRIORITY_DESCRIPTIONS.get(order['priority'], '')
    
    result = {
        'list': orders,
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': (total + page_size - 1) // page_size
    }
    
    return success_response(result, '获取工单列表成功')

@app.route('/api/work-orders/<int:order_id>', methods=['GET'])
def get_work_order(order_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT wo.*, d.device_name, d.location, d.branch
        FROM work_orders wo 
        LEFT JOIN devices d ON wo.device_id = d.id 
        WHERE wo.id = ?
    ''', (order_id,))
    order = cursor.fetchone()
    if order:
        order_dict = dict(order)
        order_dict['priority_desc'] = PRIORITY_DESCRIPTIONS.get(order_dict['priority'], '')
        return success_response(order_dict, '获取工单详情成功')
    return error_response('工单不存在', 404)

@app.route('/api/config', methods=['GET'])
def get_config():
    return success_response({
        'fault_types': FAULT_TYPES,
        'priority_levels': PRIORITY_LEVELS,
        'priority_descriptions': PRIORITY_DESCRIPTIONS,
        'branch_list': BRANCH_LIST,
        'order_status_list': ORDER_STATUS_LIST,
        'device_statuses': DEVICE_STATUSES
    }, '获取配置成功')

@app.route('/api/work-orders', methods=['POST'])
def create_work_order():
    data = request.get_json()
    required_fields = ['device_id', 'device_code', 'fault_type', 'fault_desc', 'reporter']
    for field in required_fields:
        if field not in data or not data[field]:
            return error_response(f'{field} 不能为空')
    
    if data['fault_type'] not in FAULT_TYPES:
        return error_response(f'故障类型必须是: {", ".join(FAULT_TYPES)}')
    
    priority = data.get('priority', '一般')
    if priority not in PRIORITY_LEVELS:
        return error_response(f'优先级必须是: {", ".join(PRIORITY_LEVELS)}')
    
    order_no = generate_order_no()
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('''
        INSERT INTO work_orders (order_no, device_id, device_code, fault_type, fault_desc, priority, reporter, reporter_phone, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        order_no,
        data['device_id'],
        data['device_code'],
        data['fault_type'],
        data['fault_desc'],
        priority,
        data['reporter'],
        data.get('reporter_phone', ''),
        '待处理'
    ))
    db.commit()
    
    cursor.execute('UPDATE devices SET status = ? WHERE id = ?', ('故障', data['device_id']))
    db.commit()
    
    return success_response({
        'order_no': order_no, 
        'id': cursor.lastrowid,
        'priority': priority,
        'priority_desc': PRIORITY_DESCRIPTIONS[priority]
    }, '工单创建成功')

@app.route('/api/work-orders/<int:order_id>/handle', methods=['PUT'])
def handle_work_order(order_id):
    data = request.get_json()
    handle_user = data.get('handle_user')
    handle_desc = data.get('handle_desc')
    new_status = data.get('status', '处理中')
    
    if not handle_user:
        return error_response('处理人不能为空')
    
    if new_status not in ORDER_STATUS_LIST:
        return error_response(f'状态必须是: {", ".join(ORDER_STATUS_LIST)}')
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM work_orders WHERE id = ?', (order_id,))
    order = cursor.fetchone()
    if not order:
        return error_response('工单不存在', 404)
    
    handle_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        UPDATE work_orders 
        SET status = ?, handle_user = ?, handle_desc = ?, handle_time = ?
        WHERE id = ?
    ''', (new_status, handle_user, handle_desc, handle_time, order_id))
    db.commit()
    
    if new_status == '已完成':
        cursor.execute('UPDATE devices SET status = ? WHERE id = ?', ('已修复', order['device_id']))
        db.commit()
    elif new_status == '处理中':
        cursor.execute('UPDATE devices SET status = ? WHERE id = ?', ('维修中', order['device_id']))
        db.commit()
    
    return success_response(None, '工单处理成功')

@app.route('/api/maintain-records', methods=['GET'])
def get_maintain_records():
    db = get_db()
    cursor = db.cursor()
    device_id = request.args.get('device_id')
    branch = request.args.get('branch')
    keyword = request.args.get('keyword')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    
    base_query = '''
        SELECT mr.*, d.device_name, d.branch 
        FROM maintain_records mr 
        LEFT JOIN devices d ON mr.device_id = d.id
    '''
    conditions = []
    params = []
    
    if device_id:
        conditions.append('mr.device_id = ?')
        params.append(device_id)
    
    if branch:
        conditions.append('d.branch = ?')
        params.append(branch)
    
    if keyword:
        conditions.append('(d.device_name LIKE ? OR mr.maintain_desc LIKE ?)')
        params.extend([f'%{keyword}%', f'%{keyword}%'])
    
    where_clause = ' WHERE ' + ' AND '.join(conditions) if conditions else ''
    
    count_query = f'''
        SELECT COUNT(*) as total 
        FROM maintain_records mr 
        LEFT JOIN devices d ON mr.device_id = d.id
        {where_clause}
    '''
    cursor.execute(count_query, params)
    total = cursor.fetchone()['total']
    
    limit_offset = ' LIMIT ? OFFSET ?'
    params.extend([page_size, (page - 1) * page_size])
    
    full_query = base_query + where_clause + ' ORDER BY mr.maintain_time DESC' + limit_offset
    cursor.execute(full_query, params)
    records = [dict(row) for row in cursor.fetchall()]
    
    result = {
        'list': records,
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': (total + page_size - 1) // page_size
    }
    
    return success_response(result, '获取运维记录列表成功')

@app.route('/api/maintain-records', methods=['POST'])
def add_maintain_record():
    data = request.get_json()
    required_fields = ['device_id', 'device_code', 'maintain_type', 'maintain_desc', 'maintain_user', 'maintain_time']
    for field in required_fields:
        if field not in data or not data[field]:
            return error_response(f'{field} 不能为空')
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('''
        INSERT INTO maintain_records (device_id, device_code, maintain_type, maintain_desc, maintain_user, maintain_time, remark)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['device_id'],
        data['device_code'],
        data['maintain_type'],
        data['maintain_desc'],
        data['maintain_user'],
        data['maintain_time'],
        data.get('remark', '')
    ))
    db.commit()
    
    cursor.execute('UPDATE devices SET last_maintain_date = ? WHERE id = ?', (data['maintain_time'], data['device_id']))
    db.commit()
    
    return success_response({'id': cursor.lastrowid}, '运维记录添加成功')

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT COUNT(*) as total FROM devices')
    total_devices = cursor.fetchone()['total']
    
    cursor.execute('SELECT COUNT(*) as count FROM devices WHERE status IN ("正常", "已修复")')
    normal_devices = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM devices WHERE status = ?', ('故障',))
    fault_devices = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM devices WHERE status = ?', ('维修中',))
    repairing_devices = cursor.fetchone()['count']
    
    health_rate = round((normal_devices / total_devices * 100), 2) if total_devices > 0 else 100.0
    
    cursor.execute('SELECT COUNT(*) as pending FROM work_orders WHERE status = ?', ('待处理',))
    pending_orders = cursor.fetchone()['pending']
    
    cursor.execute('SELECT COUNT(*) as processing FROM work_orders WHERE status = ?', ('处理中',))
    processing_orders = cursor.fetchone()['processing']
    
    cursor.execute('SELECT COUNT(*) as completed FROM work_orders WHERE status = ?', ('已完成',))
    completed_orders = cursor.fetchone()['completed']
    
    cursor.execute('SELECT COUNT(*) as total FROM work_orders')
    total_orders = cursor.fetchone()['total']
    
    priority_stats = {}
    for priority in PRIORITY_LEVELS:
        cursor.execute('SELECT COUNT(*) as count FROM work_orders WHERE priority = ? AND status != ?', (priority, '已完成'))
        priority_stats[priority] = cursor.fetchone()['count']
    
    fault_type_stats = {}
    for fault_type in FAULT_TYPES:
        cursor.execute('SELECT COUNT(*) as count FROM work_orders WHERE fault_type = ? AND status != ?', (fault_type, '已完成'))
        fault_type_stats[fault_type] = cursor.fetchone()['count']
    
    branch_stats = {}
    for branch in BRANCH_LIST:
        cursor.execute('SELECT COUNT(*) as total FROM devices WHERE branch = ?', (branch,))
        total = cursor.fetchone()['total']
        cursor.execute('SELECT COUNT(*) as normal FROM devices WHERE branch = ? AND status IN ("正常", "已修复")', (branch,))
        normal = cursor.fetchone()['normal']
        branch_stats[branch] = {
            'total': total,
            'normal': normal,
            'health_rate': round((normal / total * 100), 2) if total > 0 else 100.0
        }
    
    return success_response({
        'total_devices': total_devices,
        'normal_devices': normal_devices,
        'fault_devices': fault_devices,
        'repairing_devices': repairing_devices,
        'device_health_rate': health_rate,
        'pending_orders': pending_orders,
        'processing_orders': processing_orders,
        'completed_orders': completed_orders,
        'total_orders': total_orders,
        'priority_stats': priority_stats,
        'fault_type_stats': fault_type_stats,
        'branch_stats': branch_stats
    }, '获取统计数据成功')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001, debug=False)
