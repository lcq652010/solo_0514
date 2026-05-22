from flask import Flask, request, jsonify, g
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.config['DATABASE'] = 'tax_invoice.db'

STATUS_OPTIONS = ['正常', '故障', '维修中', '已修复']
ORDER_STATUS_OPTIONS = ['待处理', '处理中', '已完成']

FAULT_TYPES = [
    '硬件故障',
    '软件故障',
    '网络故障',
    '打印机故障',
    '触摸屏故障',
    '读卡器故障',
    '电源故障',
    '其他故障'
]

PRIORITY_LEVELS = ['高', '中', '低']
COMMUNICATION_METHODS = ['有线网络', '无线网络', '4G', '5G', '其他']

def success_response(data=None, message='操作成功'):
    response = {
        'code': 200,
        'message': message,
        'success': True,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), 200

def error_response(message='操作失败', code=400):
    return jsonify({
        'code': code,
        'message': message,
        'success': False,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }), code

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
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
        
        cursor.execute("PRAGMA table_info(devices)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'device_model' not in columns:
            cursor.execute("ALTER TABLE devices ADD COLUMN device_model TEXT")
        if 'communication_method' not in columns:
            cursor.execute("ALTER TABLE devices ADD COLUMN communication_method TEXT")
        if 'commission_date' not in columns:
            cursor.execute("ALTER TABLE devices ADD COLUMN commission_date TEXT")
        
        cursor.execute("PRAGMA table_info(work_orders)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'priority' not in columns:
            cursor.execute("ALTER TABLE work_orders ADD COLUMN priority TEXT DEFAULT '中'")
        if 'business_impact' not in columns:
            cursor.execute("ALTER TABLE work_orders ADD COLUMN business_impact TEXT")
        
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
                communication_method TEXT,
                location TEXT NOT NULL,
                status TEXT DEFAULT '正常',
                install_date TEXT,
                commission_date TEXT,
                last_maintain_date TEXT,
                remark TEXT,
                create_time TEXT DEFAULT CURRENT_TIMESTAMP,
                update_time TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS work_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_no TEXT UNIQUE NOT NULL,
                device_id INTEGER NOT NULL,
                device_code TEXT NOT NULL,
                fault_type TEXT,
                fault_description TEXT NOT NULL,
                priority TEXT DEFAULT '中',
                business_impact TEXT,
                reporter TEXT,
                reporter_phone TEXT,
                status TEXT DEFAULT '待处理',
                handler TEXT,
                handle_result TEXT,
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
                order_no TEXT,
                maintain_type TEXT NOT NULL,
                maintain_content TEXT NOT NULL,
                maintainer TEXT,
                maintain_time TEXT,
                remark TEXT,
                create_time TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                real_name TEXT,
                phone TEXT,
                role TEXT DEFAULT '管理员',
                create_time TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute("SELECT COUNT(*) as count FROM admins WHERE username = 'admin'")
        if cursor.fetchone()['count'] == 0:
            cursor.execute(
                "INSERT INTO admins (username, password, real_name) VALUES (?, ?, ?)",
                ('admin', 'admin123', '系统管理员')
            )
        
        db.commit()
        migrate_db()

def generate_order_no():
    now = datetime.now()
    prefix = now.strftime('WO%Y%m%d')
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT order_no FROM work_orders WHERE order_no LIKE ? ORDER BY order_no DESC LIMIT 1",
            (prefix + '%',)
        )
        result = cursor.fetchone()
        if result:
            last_no = int(result['order_no'][-4:])
            new_no = last_no + 1
        else:
            new_no = 1
        return f"{prefix}{new_no:04d}"

@app.route('/api/devices', methods=['GET'])
def get_devices():
    db = get_db()
    cursor = db.cursor()
    
    status = request.args.get('status')
    device_code = request.args.get('device_code')
    device_model = request.args.get('device_model')
    communication_method = request.args.get('communication_method')
    location = request.args.get('location')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    
    sql = "SELECT * FROM devices WHERE 1=1"
    count_sql = "SELECT COUNT(*) as total FROM devices WHERE 1=1"
    params = []
    
    if status:
        sql += " AND status = ?"
        count_sql += " AND status = ?"
        params.append(status)
    if device_code:
        sql += " AND device_code LIKE ?"
        count_sql += " AND device_code LIKE ?"
        params.append(f"%{device_code}%")
    if device_model:
        sql += " AND device_model LIKE ?"
        count_sql += " AND device_model LIKE ?"
        params.append(f"%{device_model}%")
    if communication_method:
        sql += " AND communication_method = ?"
        count_sql += " AND communication_method = ?"
        params.append(communication_method)
    if location:
        sql += " AND location LIKE ?"
        count_sql += " AND location LIKE ?"
        params.append(f"%{location}%")
    
    cursor.execute(count_sql, params)
    total = cursor.fetchone()['total']
    
    sql += " ORDER BY create_time DESC LIMIT ? OFFSET ?"
    params.extend([page_size, (page - 1) * page_size])
    
    cursor.execute(sql, params)
    devices = cursor.fetchall()
    
    data = {
        'list': [dict(device) for device in devices],
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total': total,
            'total_pages': (total + page_size - 1) // page_size
        }
    }
    
    return success_response(data, '设备列表查询成功')

@app.route('/api/devices', methods=['POST'])
def add_device():
    data = request.json
    required_fields = ['device_code', 'device_name', 'location']
    
    for field in required_fields:
        if field not in data or not data[field]:
            return error_response(f'{field} 不能为空', 400)
    
    if 'communication_method' in data and data['communication_method'] not in COMMUNICATION_METHODS:
        return error_response(f'通信方式必须是: {", ".join(COMMUNICATION_METHODS)}', 400)
    
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute(
            "SELECT id FROM devices WHERE device_code = ?",
            (data['device_code'],)
        )
        if cursor.fetchone():
            return error_response('设备编号已存在', 400)
        
        cursor.execute('''
            INSERT INTO devices (
                device_code, device_name, device_model, communication_method,
                location, status, install_date, commission_date, remark
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['device_code'],
            data['device_name'],
            data.get('device_model'),
            data.get('communication_method'),
            data['location'],
            data.get('status', '正常'),
            data.get('install_date'),
            data.get('commission_date'),
            data.get('remark')
        ))
        db.commit()
        
        return success_response({'id': cursor.lastrowid}, '设备添加成功')
    except Exception as e:
        db.rollback()
        return error_response(str(e), 500)

@app.route('/api/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM devices WHERE id = ?", (device_id,))
    device = cursor.fetchone()
    
    if not device:
        return error_response('设备不存在', 404)
    
    return success_response(dict(device), '设备详情查询成功')

@app.route('/api/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    data = request.json
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT id FROM devices WHERE id = ?", (device_id,))
    if not cursor.fetchone():
        return error_response('设备不存在', 404)
    
    if 'communication_method' in data and data['communication_method'] not in COMMUNICATION_METHODS:
        return error_response(f'通信方式必须是: {", ".join(COMMUNICATION_METHODS)}', 400)
    
    if 'status' in data and data['status'] not in STATUS_OPTIONS:
        return error_response(f'状态值必须是: {", ".join(STATUS_OPTIONS)}', 400)
    
    update_fields = []
    params = []
    
    if 'device_name' in data:
        update_fields.append('device_name = ?')
        params.append(data['device_name'])
    if 'device_model' in data:
        update_fields.append('device_model = ?')
        params.append(data['device_model'])
    if 'communication_method' in data:
        update_fields.append('communication_method = ?')
        params.append(data['communication_method'])
    if 'location' in data:
        update_fields.append('location = ?')
        params.append(data['location'])
    if 'status' in data:
        update_fields.append('status = ?')
        params.append(data['status'])
    if 'install_date' in data:
        update_fields.append('install_date = ?')
        params.append(data['install_date'])
    if 'commission_date' in data:
        update_fields.append('commission_date = ?')
        params.append(data['commission_date'])
    if 'remark' in data:
        update_fields.append('remark = ?')
        params.append(data['remark'])
    
    update_fields.append('update_time = CURRENT_TIMESTAMP')
    params.append(device_id)
    
    sql = f"UPDATE devices SET {', '.join(update_fields)} WHERE id = ?"
    cursor.execute(sql, params)
    db.commit()
    
    return success_response(None, '设备更新成功')

@app.route('/api/devices/<int:device_id>/status', methods=['PUT'])
def update_device_status(device_id):
    data = request.json
    status = data.get('status')
    
    if not status or status not in STATUS_OPTIONS:
        return error_response(f'状态值必须是: {", ".join(STATUS_OPTIONS)}', 400)
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT id FROM devices WHERE id = ?", (device_id,))
    if not cursor.fetchone():
        return error_response('设备不存在', 404)
    
    cursor.execute(
        "UPDATE devices SET status = ?, update_time = CURRENT_TIMESTAMP WHERE id = ?",
        (status, device_id)
    )
    db.commit()
    
    return success_response(None, '状态更新成功')

@app.route('/api/devices/locations', methods=['GET'])
def get_locations():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT DISTINCT location FROM devices WHERE location IS NOT NULL AND location != ''")
    locations = cursor.fetchall()
    
    return success_response([loc['location'] for loc in locations], '区域列表查询成功')

@app.route('/api/work-orders', methods=['POST'])
def create_work_order():
    data = request.json
    required_fields = ['device_id', 'fault_description']
    
    for field in required_fields:
        if field not in data or not data[field]:
            return error_response(f'{field} 不能为空', 400)
    
    if 'fault_type' in data and data['fault_type'] not in FAULT_TYPES:
        return error_response(f'故障类型必须是: {", ".join(FAULT_TYPES)}', 400)
    
    if 'priority' in data and data['priority'] not in PRIORITY_LEVELS:
        return error_response(f'优先级必须是: {", ".join(PRIORITY_LEVELS)}', 400)
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT id, device_code FROM devices WHERE id = ?", (data['device_id'],))
    device = cursor.fetchone()
    if not device:
        return error_response('设备不存在', 404)
    
    order_no = generate_order_no()
    
    cursor.execute('''
        INSERT INTO work_orders (
            order_no, device_id, device_code, fault_type, fault_description,
            priority, business_impact, reporter, reporter_phone
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        order_no,
        data['device_id'],
        device['device_code'],
        data.get('fault_type'),
        data['fault_description'],
        data.get('priority', '中'),
        data.get('business_impact'),
        data.get('reporter'),
        data.get('reporter_phone')
    ))
    
    cursor.execute(
        "UPDATE devices SET status = '故障', update_time = CURRENT_TIMESTAMP WHERE id = ?",
        (data['device_id'],)
    )
    
    db.commit()
    
    return success_response({'order_no': order_no}, '工单创建成功')

@app.route('/api/work-orders', methods=['GET'])
def get_work_orders():
    db = get_db()
    cursor = db.cursor()
    
    status = request.args.get('status')
    device_code = request.args.get('device_code')
    fault_type = request.args.get('fault_type')
    priority = request.args.get('priority')
    location = request.args.get('location')
    handler = request.args.get('handler')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    
    sql = "SELECT wo.*, d.location FROM work_orders wo LEFT JOIN devices d ON wo.device_id = d.id WHERE 1=1"
    count_sql = "SELECT COUNT(*) as total FROM work_orders wo LEFT JOIN devices d ON wo.device_id = d.id WHERE 1=1"
    params = []
    
    if status:
        sql += " AND wo.status = ?"
        count_sql += " AND wo.status = ?"
        params.append(status)
    if device_code:
        sql += " AND wo.device_code LIKE ?"
        count_sql += " AND wo.device_code LIKE ?"
        params.append(f"%{device_code}%")
    if fault_type:
        sql += " AND wo.fault_type = ?"
        count_sql += " AND wo.fault_type = ?"
        params.append(fault_type)
    if priority:
        sql += " AND wo.priority = ?"
        count_sql += " AND wo.priority = ?"
        params.append(priority)
    if location:
        sql += " AND d.location LIKE ?"
        count_sql += " AND d.location LIKE ?"
        params.append(f"%{location}%")
    if handler:
        sql += " AND wo.handler LIKE ?"
        count_sql += " AND wo.handler LIKE ?"
        params.append(f"%{handler}%")
    
    cursor.execute(count_sql, params)
    total = cursor.fetchone()['total']
    
    sql += " ORDER BY CASE wo.priority WHEN '高' THEN 1 WHEN '中' THEN 2 WHEN '低' THEN 3 ELSE 4 END, wo.create_time DESC LIMIT ? OFFSET ?"
    params.extend([page_size, (page - 1) * page_size])
    
    cursor.execute(sql, params)
    orders = cursor.fetchall()
    
    data = {
        'list': [dict(order) for order in orders],
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total': total,
            'total_pages': (total + page_size - 1) // page_size
        }
    }
    
    return success_response(data, '工单列表查询成功')

@app.route('/api/work-orders/<string:order_no>', methods=['GET'])
def get_work_order(order_no):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT wo.*, d.location, d.device_name FROM work_orders wo LEFT JOIN devices d ON wo.device_id = d.id WHERE wo.order_no = ?", (order_no,))
    order = cursor.fetchone()
    
    if not order:
        return error_response('工单不存在', 404)
    
    return success_response(dict(order), '工单详情查询成功')

@app.route('/api/work-orders/<string:order_no>/handle', methods=['PUT'])
def handle_work_order(order_no):
    data = request.json
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT id, device_id FROM work_orders WHERE order_no = ?", (order_no,))
    order = cursor.fetchone()
    if not order:
        return error_response('工单不存在', 404)
    
    new_status = data.get('status', '处理中')
    handler = data.get('handler')
    handle_result = data.get('handle_result')
    
    if new_status not in ORDER_STATUS_OPTIONS:
        return error_response(f'工单状态必须是: {", ".join(ORDER_STATUS_OPTIONS)}', 400)
    
    cursor.execute('''
        UPDATE work_orders 
        SET status = ?, handler = ?, handle_result = ?, handle_time = CURRENT_TIMESTAMP
        WHERE order_no = ?
    ''', (new_status, handler, handle_result, order_no))
    
    if new_status == '处理中':
        cursor.execute(
            "UPDATE devices SET status = '维修中', update_time = CURRENT_TIMESTAMP WHERE id = ?",
            (order['device_id'],)
        )
    elif new_status == '已完成':
        cursor.execute(
            "UPDATE devices SET status = '已修复', update_time = CURRENT_TIMESTAMP WHERE id = ?",
            (order['device_id'],)
        )
        
        cursor.execute('''
            INSERT INTO maintain_records (device_id, device_code, order_no, maintain_type, maintain_content, maintainer)
            SELECT device_id, device_code, order_no, '故障维修', fault_description, ?
            FROM work_orders WHERE order_no = ?
        ''', (handler, order_no))
    
    db.commit()
    
    return success_response(None, '工单处理成功')

@app.route('/api/maintain-records', methods=['GET'])
def get_maintain_records():
    db = get_db()
    cursor = db.cursor()
    
    device_code = request.args.get('device_code')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    maintain_type = request.args.get('maintain_type')
    location = request.args.get('location')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    
    sql = "SELECT mr.*, d.location FROM maintain_records mr LEFT JOIN devices d ON mr.device_id = d.id WHERE 1=1"
    count_sql = "SELECT COUNT(*) as total FROM maintain_records mr LEFT JOIN devices d ON mr.device_id = d.id WHERE 1=1"
    params = []
    
    if device_code:
        sql += " AND mr.device_code LIKE ?"
        count_sql += " AND mr.device_code LIKE ?"
        params.append(f"%{device_code}%")
    if start_date:
        sql += " AND mr.maintain_time >= ?"
        count_sql += " AND mr.maintain_time >= ?"
        params.append(start_date)
    if end_date:
        sql += " AND mr.maintain_time <= ?"
        count_sql += " AND mr.maintain_time <= ?"
        params.append(end_date)
    if maintain_type:
        sql += " AND mr.maintain_type = ?"
        count_sql += " AND mr.maintain_type = ?"
        params.append(maintain_type)
    if location:
        sql += " AND d.location LIKE ?"
        count_sql += " AND d.location LIKE ?"
        params.append(f"%{location}%")
    
    cursor.execute(count_sql, params)
    total = cursor.fetchone()['total']
    
    sql += " ORDER BY mr.maintain_time DESC LIMIT ? OFFSET ?"
    params.extend([page_size, (page - 1) * page_size])
    
    cursor.execute(sql, params)
    records = cursor.fetchall()
    
    data = {
        'list': [dict(record) for record in records],
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total': total,
            'total_pages': (total + page_size - 1) // page_size
        }
    }
    
    return success_response(data, '运维记录查询成功')

@app.route('/api/maintain-records', methods=['POST'])
def add_maintain_record():
    data = request.json
    required_fields = ['device_id', 'maintain_type', 'maintain_content']
    
    for field in required_fields:
        if field not in data or not data[field]:
            return error_response(f'{field} 不能为空', 400)
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT id, device_code FROM devices WHERE id = ?", (data['device_id'],))
    device = cursor.fetchone()
    if not device:
        return error_response('设备不存在', 404)
    
    cursor.execute('''
        INSERT INTO maintain_records (device_id, device_code, maintain_type, maintain_content, maintainer, maintain_time, remark)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['device_id'],
        device['device_code'],
        data['maintain_type'],
        data['maintain_content'],
        data.get('maintainer'),
        data.get('maintain_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        data.get('remark')
    ))
    
    cursor.execute(
        "UPDATE devices SET last_maintain_date = CURRENT_TIMESTAMP, update_time = CURRENT_TIMESTAMP WHERE id = ?",
        (data['device_id'],)
    )
    
    db.commit()
    
    return success_response({'id': cursor.lastrowid}, '运维记录添加成功')

@app.route('/api/admins/login', methods=['POST'])
def admin_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return error_response('用户名和密码不能为空', 400)
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT id, username, real_name, phone, role FROM admins WHERE username = ? AND password = ?",
        (username, password)
    )
    admin = cursor.fetchone()
    
    if not admin:
        return error_response('用户名或密码错误', 401)
    
    return success_response(dict(admin), '登录成功')

@app.route('/api/dashboard/statistics', methods=['GET'])
def get_statistics():
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM devices")
    total_devices = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as count FROM devices WHERE status = '正常'")
    normal_devices = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM devices WHERE status = '故障'")
    fault_devices = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM devices WHERE status = '维修中'")
    repairing_devices = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM devices WHERE status = '已修复'")
    repaired_devices = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM work_orders WHERE status = '待处理'")
    pending_orders = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM work_orders WHERE status = '处理中'")
    processing_orders = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM work_orders WHERE status = '已完成'")
    completed_orders = cursor.fetchone()['count']
    
    cursor.execute("SELECT priority, COUNT(*) as count FROM work_orders GROUP BY priority")
    priority_stats = cursor.fetchall()
    
    cursor.execute("SELECT fault_type, COUNT(*) as count FROM work_orders GROUP BY fault_type")
    fault_type_stats = cursor.fetchall()
    
    cursor.execute("SELECT location, COUNT(*) as total, SUM(CASE WHEN status = '正常' THEN 1 ELSE 0 END) as normal FROM devices GROUP BY location")
    location_stats = cursor.fetchall()
    
    availability_rate = (normal_devices / total_devices * 100) if total_devices > 0 else 0
    
    data = {
        'device_stats': {
            'total': total_devices,
            'normal': normal_devices,
            'fault': fault_devices,
            'repairing': repairing_devices,
            'repaired': repaired_devices,
            'availability_rate': round(availability_rate, 2)
        },
        'order_stats': {
            'pending': pending_orders,
            'processing': processing_orders,
            'completed': completed_orders,
            'total': pending_orders + processing_orders + completed_orders,
            'completion_rate': round((completed_orders / (pending_orders + processing_orders + completed_orders) * 100) if (pending_orders + processing_orders + completed_orders) > 0 else 0, 2)
        },
        'priority_stats': [dict(p) for p in priority_stats],
        'fault_type_stats': [dict(f) for f in fault_type_stats],
        'location_stats': [
            {
                'location': loc['location'],
                'total': loc['total'],
                'normal': loc['normal'],
                'availability_rate': round((loc['normal'] / loc['total'] * 100) if loc['total'] > 0 else 0, 2)
            } for loc in location_stats
        ]
    }
    
    return success_response(data, '统计数据查询成功')

@app.route('/api/config/enums', methods=['GET'])
def get_enums():
    return success_response({
        'device_status_options': STATUS_OPTIONS,
        'order_status_options': ORDER_STATUS_OPTIONS,
        'fault_types': FAULT_TYPES,
        'priority_levels': PRIORITY_LEVELS,
        'communication_methods': COMMUNICATION_METHODS
    }, '枚举配置查询成功')

@app.errorhandler(404)
def not_found(error):
    return error_response('请求的资源不存在', 404)

@app.errorhandler(500)
def internal_error(error):
    return error_response('服务器内部错误', 500)

if __name__ == '__main__':
    init_db()
    print("数据库初始化完成！")
    print("默认管理员账号: admin / admin123")
    print("服务启动地址: http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
