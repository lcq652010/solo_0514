from flask import Flask, request, jsonify, g
import sqlite3
import os
from datetime import datetime, timedelta
import uuid
import re

app = Flask(__name__)

DATABASE = 'metro_oms.db'

DEVICE_STATUS_MAP = {
    '正常': {'code': 1, 'label': '正常', 'color': 'success'},
    '故障': {'code': 2, 'label': '故障', 'color': 'danger'},
    '维修中': {'code': 3, 'label': '维修中', 'color': 'warning'},
    '已修复': {'code': 4, 'label': '已修复', 'color': 'info'}
}

PRIORITY_MAP = {
    '高': {'code': 1, 'label': '紧急', 'color': 'red', 'level': 3},
    '中': {'code': 2, 'label': '一般', 'color': 'orange', 'level': 2},
    '低': {'code': 3, 'label': '低', 'color': 'green', 'level': 1}
}

ORDER_STATUS_MAP = {
    '待处理': {'code': 1, 'label': '待处理', 'color': 'warning'},
    '处理中': {'code': 2, 'label': '处理中', 'color': 'primary'},
    '已完成': {'code': 3, 'label': '已完成', 'color': 'success'},
    '已关闭': {'code': 4, 'label': '已关闭', 'color': 'default'}
}

FAULT_CATEGORIES = {
    '硬件故障': ['纸币识别器', '硬币识别器', '打印机', '读卡器', '触摸屏', '电源模块', '工控机', '闸机门体', '票卡回收模块'],
    '软件故障': ['系统崩溃', '程序异常', '通信中断', '数据同步失败', '界面显示异常'],
    '网络故障': ['网络断开', '延迟过高', '丢包严重', 'DNS解析失败'],
    '电源故障': ['断电', '电压不稳', 'UPS异常', '电源模块故障'],
    '票卡故障': ['票卡卡住', '票卡读写失败', '票卡回收异常', '票卡发放异常'],
    '其他故障': ['未知故障', '环境因素', '人为损坏']
}

IMPACT_LEVELS = [
    '核心站点-早高峰',
    '核心站点-晚高峰', 
    '核心站点-平峰',
    '换乘站点-任何时段',
    '普通站点-早高峰',
    '普通站点-晚高峰',
    '普通站点-平峰',
    '全线影响'
]

def success_response(data=None, message='操作成功'):
    return jsonify({
        'code': 200,
        'success': True,
        'message': message,
        'data': data,
        'timestamp': datetime.now().isoformat()
    })

def error_response(message='操作失败', code=400, data=None):
    return jsonify({
        'code': code,
        'success': False,
        'message': message,
        'data': data,
        'timestamp': datetime.now().isoformat()
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

def parse_location(location):
    line_match = re.search(r'(\d+)号线', location)
    station_match = re.search(r'号线(.+?)站', location) or re.search(r'(.+?)站', location)
    
    line = line_match.group(1) if line_match else None
    station = station_match.group(1) if station_match else None
    
    return line, station

def calculate_priority(fault_category, impact_level=''):
    if impact_level and impact_level in IMPACT_LEVELS:
        if impact_level in ['核心站点-早高峰', '核心站点-晚高峰', '换乘站点-任何时段', '全线影响']:
            return '高'
        elif impact_level in ['核心站点-平峰', '普通站点-早高峰', '普通站点-晚高峰']:
            return '中'
        else:
            return '低'
    
    high_priority_categories = ['硬件故障', '电源故障', '票卡故障']
    if fault_category in high_priority_categories:
        return '高'
    return '中'

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id VARCHAR(50) UNIQUE NOT NULL,
                device_name VARCHAR(100) NOT NULL,
                device_type VARCHAR(50) NOT NULL,
                device_model VARCHAR(100),
                communication_protocol VARCHAR(50),
                device_serial VARCHAR(100),
                location VARCHAR(200) NOT NULL,
                line VARCHAR(20),
                station VARCHAR(50),
                status VARCHAR(20) NOT NULL DEFAULT '正常',
                online_status INTEGER DEFAULT 1,
                last_heartbeat TIMESTAMP,
                install_date DATE,
                commission_date DATE,
                last_maintenance_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS work_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_no VARCHAR(50) UNIQUE NOT NULL,
                device_id VARCHAR(50) NOT NULL,
                fault_category VARCHAR(50),
                fault_type VARCHAR(100),
                priority VARCHAR(20) DEFAULT '中',
                impact_level VARCHAR(50),
                fault_description TEXT,
                reporter VARCHAR(50),
                reporter_phone VARCHAR(20),
                status VARCHAR(20) NOT NULL DEFAULT '待处理',
                handler VARCHAR(50),
                handle_description TEXT,
                report_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                handle_time TIMESTAMP,
                complete_time TIMESTAMP,
                FOREIGN KEY (device_id) REFERENCES devices (device_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS maintenance_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id VARCHAR(50) NOT NULL,
                order_no VARCHAR(50),
                maintenance_type VARCHAR(50) NOT NULL,
                action_type VARCHAR(50),
                description TEXT,
                before_status VARCHAR(20),
                after_status VARCHAR(20),
                operator VARCHAR(50),
                result VARCHAR(20),
                cost DECIMAL(10,2),
                duration INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS device_status_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id VARCHAR(50) NOT NULL,
                before_status VARCHAR(20),
                after_status VARCHAR(20),
                change_reason TEXT,
                operator VARCHAR(50),
                order_no VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL,
                real_name VARCHAR(50),
                phone VARCHAR(20),
                role VARCHAR(20) DEFAULT 'admin',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute("SELECT * FROM admins WHERE username = ?", ('admin',))
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO admins (username, password, real_name, role) VALUES (?, ?, ?, ?)",
                ('admin', 'admin123', '系统管理员', 'super')
            )
        
        db.commit()

def generate_order_no():
    return f"WO{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:4].upper()}"

def log_device_status_change(device_id, before_status, after_status, change_reason, operator='system', order_no=None):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        '''INSERT INTO device_status_logs 
           (device_id, before_status, after_status, change_reason, operator, order_no)
           VALUES (?, ?, ?, ?, ?, ?)''',
        (device_id, before_status, after_status, change_reason, operator, order_no)
    )
    db.commit()

def update_device_status_with_log(device_id, new_status, change_reason, operator='system', order_no=None):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT status FROM devices WHERE device_id = ?", (device_id,))
    device = cursor.fetchone()
    if not device:
        return False
    
    old_status = device['status']
    if old_status == new_status:
        return True
    
    cursor.execute(
        "UPDATE devices SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE device_id = ?",
        (new_status, device_id)
    )
    
    log_device_status_change(device_id, old_status, new_status, change_reason, operator, order_no)
    db.commit()
    return True

@app.route('/api/health', methods=['GET'])
def health_check():
    return success_response({'status': 'ok'}, '系统运行正常')

@app.route('/api/fault-categories', methods=['GET'])
def get_fault_categories():
    return success_response({
        'categories': list(FAULT_CATEGORIES.keys()),
        'fault_types': FAULT_CATEGORIES,
        'impact_levels': IMPACT_LEVELS,
        'priorities': PRIORITY_MAP,
        'device_statuses': DEVICE_STATUS_MAP,
        'order_statuses': ORDER_STATUS_MAP
    })

@app.route('/api/devices', methods=['POST'])
def add_device():
    data = request.get_json()
    required_fields = ['device_id', 'device_name', 'device_type', 'location']
    
    for field in required_fields:
        if field not in data:
            return error_response(f'缺少必填字段: {field}', 400)
    
    db = get_db()
    cursor = db.cursor()
    
    line, station = parse_location(data['location'])
    
    try:
        cursor.execute(
            '''INSERT INTO devices 
               (device_id, device_name, device_type, device_model, communication_protocol, 
                device_serial, location, line, station, status, install_date, commission_date)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (
                data['device_id'],
                data['device_name'],
                data['device_type'],
                data.get('device_model', ''),
                data.get('communication_protocol', ''),
                data.get('device_serial', ''),
                data['location'],
                line,
                station,
                data.get('status', '正常'),
                data.get('install_date'),
                data.get('commission_date')
            )
        )
        db.commit()
        return success_response({'device_id': data['device_id']}, '设备添加成功')
    except sqlite3.IntegrityError:
        return error_response('设备编号已存在', 400)
    except Exception as e:
        return error_response(str(e), 500)

@app.route('/api/devices', methods=['GET'])
def get_devices():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    status = request.args.get('status')
    device_type = request.args.get('device_type')
    line = request.args.get('line')
    station = request.args.get('station')
    keyword = request.args.get('keyword', '')
    
    offset = (page - 1) * page_size
    
    db = get_db()
    cursor = db.cursor()
    
    query = "SELECT * FROM devices WHERE 1=1"
    params = []
    
    if status:
        query += " AND status = ?"
        params.append(status)
    if device_type:
        query += " AND device_type = ?"
        params.append(device_type)
    if line:
        query += " AND line = ?"
        params.append(line)
    if station:
        query += " AND station = ?"
        params.append(station)
    if keyword:
        query += " AND (device_id LIKE ? OR device_name LIKE ? OR location LIKE ?)"
        params.extend([f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'])
    
    count_query = query.replace('SELECT *', 'SELECT COUNT(*) as total')
    cursor.execute(count_query, params)
    total = cursor.fetchone()['total']
    
    query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([page_size, offset])
    
    cursor.execute(query, params)
    devices = []
    for row in cursor.fetchall():
        device = dict(row)
        status_info = DEVICE_STATUS_MAP.get(device['status'], {})
        device['status_info'] = status_info
        if device['last_heartbeat']:
            last_heartbeat = datetime.fromisoformat(device['last_heartbeat']) if isinstance(device['last_heartbeat'], str) else device['last_heartbeat']
            device['is_online'] = (datetime.now() - last_heartbeat).total_seconds() < 300
        else:
            device['is_online'] = device.get('online_status', 1) == 1
        devices.append(device)
    
    return success_response({
        'devices': devices,
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': (total + page_size - 1) // page_size
    })

@app.route('/api/devices/<device_id>', methods=['GET'])
def get_device(device_id):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM devices WHERE device_id = ?", (device_id,))
    device = cursor.fetchone()
    
    if not device:
        return error_response('设备不存在', 404)
    
    device_dict = dict(device)
    status_info = DEVICE_STATUS_MAP.get(device_dict['status'], {})
    device_dict['status_info'] = status_info
    
    cursor.execute("SELECT * FROM work_orders WHERE device_id = ? ORDER BY report_time DESC LIMIT 10", (device_id,))
    orders = [dict(row) for row in cursor.fetchall()]
    for order in orders:
        priority_info = PRIORITY_MAP.get(order['priority'], {})
        order['priority_info'] = priority_info
        order_status_info = ORDER_STATUS_MAP.get(order['status'], {})
        order['status_info'] = order_status_info
    
    cursor.execute("SELECT * FROM maintenance_records WHERE device_id = ? ORDER BY created_at DESC LIMIT 10", (device_id,))
    records = [dict(row) for row in cursor.fetchall()]
    
    return success_response({
        'device': device_dict,
        'recent_orders': orders,
        'recent_maintenance': records
    })

@app.route('/api/devices/<device_id>', methods=['PUT'])
def update_device(device_id):
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM devices WHERE device_id = ?", (device_id,))
    if not cursor.fetchone():
        return error_response('设备不存在', 404)
    
    update_fields = []
    update_values = []
    
    if 'device_name' in data:
        update_fields.append('device_name = ?')
        update_values.append(data['device_name'])
    if 'device_type' in data:
        update_fields.append('device_type = ?')
        update_values.append(data['device_type'])
    if 'device_model' in data:
        update_fields.append('device_model = ?')
        update_values.append(data['device_model'])
    if 'communication_protocol' in data:
        update_fields.append('communication_protocol = ?')
        update_values.append(data['communication_protocol'])
    if 'device_serial' in data:
        update_fields.append('device_serial = ?')
        update_values.append(data['device_serial'])
    if 'location' in data:
        update_fields.append('location = ?')
        update_values.append(data['location'])
        line, station = parse_location(data['location'])
        update_fields.append('line = ?')
        update_values.append(line)
        update_fields.append('station = ?')
        update_values.append(station)
    if 'status' in data:
        if data['status'] not in DEVICE_STATUS_MAP:
            return error_response('无效的设备状态', 400)
        update_fields.append('status = ?')
        update_values.append(data['status'])
    if 'install_date' in data:
        update_fields.append('install_date = ?')
        update_values.append(data['install_date'])
    if 'commission_date' in data:
        update_fields.append('commission_date = ?')
        update_values.append(data['commission_date'])
    
    if not update_fields:
        return error_response('没有提供更新字段', 400)
    
    update_fields.append('updated_at = CURRENT_TIMESTAMP')
    update_values.append(device_id)
    
    query = f"UPDATE devices SET {', '.join(update_fields)} WHERE device_id = ?"
    cursor.execute(query, update_values)
    db.commit()
    
    return success_response(None, '设备更新成功')

@app.route('/api/devices/<device_id>/status', methods=['PUT'])
def update_device_status(device_id):
    data = request.get_json()
    status = data.get('status')
    reason = data.get('reason', '手动更新状态')
    operator = data.get('operator', 'system')
    
    if status not in DEVICE_STATUS_MAP:
        return error_response('无效的设备状态', 400)
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM devices WHERE device_id = ?", (device_id,))
    if not cursor.fetchone():
        return error_response('设备不存在', 404)
    
    update_device_status_with_log(device_id, status, reason, operator)
    
    return success_response({'device_id': device_id, 'status': status}, '设备状态更新成功')

@app.route('/api/devices/<device_id>/heartbeat', methods=['POST'])
def device_heartbeat(device_id):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM devices WHERE device_id = ?", (device_id,))
    if not cursor.fetchone():
        return error_response('设备不存在', 404)
    
    cursor.execute(
        "UPDATE devices SET last_heartbeat = CURRENT_TIMESTAMP, online_status = 1, updated_at = CURRENT_TIMESTAMP WHERE device_id = ?",
        (device_id,)
    )
    db.commit()
    
    return success_response({'device_id': device_id}, '心跳更新成功')

@app.route('/api/devices/<device_id>', methods=['DELETE'])
def delete_device(device_id):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM devices WHERE device_id = ?", (device_id,))
    if not cursor.fetchone():
        return error_response('设备不存在', 404)
    
    cursor.execute("DELETE FROM devices WHERE device_id = ?", (device_id,))
    db.commit()
    
    return success_response(None, '设备删除成功')

@app.route('/api/work-orders', methods=['POST'])
def create_work_order():
    data = request.get_json()
    required_fields = ['device_id', 'fault_description']
    
    for field in required_fields:
        if field not in data:
            return error_response(f'缺少必填字段: {field}', 400)
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM devices WHERE device_id = ?", (data['device_id'],))
    device = cursor.fetchone()
    if not device:
        return error_response('设备不存在', 404)
    
    fault_category = data.get('fault_category', '')
    impact_level = data.get('impact_level', '')
    priority = data.get('priority') or calculate_priority(fault_category, impact_level)
    
    if priority not in PRIORITY_MAP:
        return error_response('无效的优先级', 400)
    
    order_no = generate_order_no()
    
    try:
        cursor.execute(
            '''INSERT INTO work_orders 
               (order_no, device_id, fault_category, fault_type, priority, impact_level, 
                fault_description, reporter, reporter_phone, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (
                order_no,
                data['device_id'],
                fault_category,
                data.get('fault_type', ''),
                priority,
                impact_level,
                data['fault_description'],
                data.get('reporter', ''),
                data.get('reporter_phone', ''),
                '待处理'
            )
        )
        
        update_device_status_with_log(
            data['device_id'], 
            '故障', 
            f'上报故障工单: {order_no}',
            data.get('reporter', 'system'),
            order_no
        )
        
        db.commit()
        return success_response({
            'order_no': order_no,
            'priority': priority,
            'priority_info': PRIORITY_MAP.get(priority, {})
        }, '工单创建成功')
    except Exception as e:
        return error_response(str(e), 500)

@app.route('/api/work-orders', methods=['GET'])
def get_work_orders():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    status = request.args.get('status')
    device_id = request.args.get('device_id')
    priority = request.args.get('priority')
    fault_category = request.args.get('fault_category')
    line = request.args.get('line')
    station = request.args.get('station')
    keyword = request.args.get('keyword', '')
    
    offset = (page - 1) * page_size
    
    db = get_db()
    cursor = db.cursor()
    
    base_query = """
        SELECT wo.*, d.device_name, d.device_type, d.location, d.line, d.station
        FROM work_orders wo
        LEFT JOIN devices d ON wo.device_id = d.device_id
        WHERE 1=1
    """
    params = []
    
    if status:
        base_query += " AND wo.status = ?"
        params.append(status)
    if device_id:
        base_query += " AND wo.device_id = ?"
        params.append(device_id)
    if priority:
        base_query += " AND wo.priority = ?"
        params.append(priority)
    if fault_category:
        base_query += " AND wo.fault_category = ?"
        params.append(fault_category)
    if line:
        base_query += " AND d.line = ?"
        params.append(line)
    if station:
        base_query += " AND d.station = ?"
        params.append(station)
    if keyword:
        base_query += " AND (wo.order_no LIKE ? OR wo.fault_description LIKE ? OR d.device_name LIKE ?)"
        params.extend([f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'])
    
    count_query = base_query.replace('SELECT wo.*, d.device_name, d.device_type, d.location, d.line, d.station', 'SELECT COUNT(*) as total')
    cursor.execute(count_query, params)
    total = cursor.fetchone()['total']
    
    base_query += """
        ORDER BY 
            CASE wo.priority 
                WHEN '高' THEN 1 
                WHEN '中' THEN 2 
                ELSE 3 
            END,
            CASE wo.status
                WHEN '待处理' THEN 1
                WHEN '处理中' THEN 2
                WHEN '已完成' THEN 3
                ELSE 4
            END,
            wo.report_time DESC
        LIMIT ? OFFSET ?
    """
    params.extend([page_size, offset])
    
    cursor.execute(base_query, params)
    orders = []
    for row in cursor.fetchall():
        order = dict(row)
        priority_info = PRIORITY_MAP.get(order['priority'], {})
        order['priority_info'] = priority_info
        order_status_info = ORDER_STATUS_MAP.get(order['status'], {})
        order['status_info'] = order_status_info
        orders.append(order)
    
    return success_response({
        'orders': orders,
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': (total + page_size - 1) // page_size
    })

@app.route('/api/work-orders/<order_no>', methods=['GET'])
def get_work_order(order_no):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("""
        SELECT wo.*, d.device_name, d.device_type, d.location, d.line, d.station, d.status as device_status
        FROM work_orders wo
        LEFT JOIN devices d ON wo.device_id = d.device_id
        WHERE wo.order_no = ?
    """, (order_no,))
    order = cursor.fetchone()
    
    if not order:
        return error_response('工单不存在', 404)
    
    order_dict = dict(order)
    priority_info = PRIORITY_MAP.get(order_dict['priority'], {})
    order_dict['priority_info'] = priority_info
    order_status_info = ORDER_STATUS_MAP.get(order_dict['status'], {})
    order_dict['status_info'] = order_status_info
    
    cursor.execute("SELECT * FROM maintenance_records WHERE order_no = ? ORDER BY created_at DESC", (order_no,))
    records = [dict(row) for row in cursor.fetchall()]
    
    return success_response({
        'order': order_dict,
        'maintenance_records': records
    })

@app.route('/api/work-orders/<order_no>/handle', methods=['PUT'])
def handle_work_order(order_no):
    data = request.get_json()
    handler = data.get('handler', '')
    handle_description = data.get('handle_description', '')
    
    if not handler:
        return error_response('处理人不能为空', 400)
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM work_orders WHERE order_no = ?", (order_no,))
    order = cursor.fetchone()
    
    if not order:
        return error_response('工单不存在', 404)
    
    if order['status'] != '待处理':
        return error_response('工单状态不允许处理', 400)
    
    cursor.execute(
        '''UPDATE work_orders 
           SET status = '处理中', handler = ?, handle_description = ?, handle_time = CURRENT_TIMESTAMP
           WHERE order_no = ?''',
        (handler, handle_description, order_no)
    )
    
    update_device_status_with_log(
        order['device_id'],
        '维修中',
        f'开始处理工单: {order_no}',
        handler,
        order_no
    )
    
    db.commit()
    
    return success_response({
        'order_no': order_no,
        'status': '处理中',
        'status_info': ORDER_STATUS_MAP.get('处理中', {})
    }, '工单处理中')

@app.route('/api/work-orders/<order_no>/complete', methods=['PUT'])
def complete_work_order(order_no):
    data = request.get_json()
    result_description = data.get('result_description', '')
    maintenance_type = data.get('maintenance_type', '维修')
    cost = data.get('cost', 0)
    operator = data.get('operator', '')
    duration = data.get('duration', 0)
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM work_orders WHERE order_no = ?", (order_no,))
    order = cursor.fetchone()
    
    if not order:
        return error_response('工单不存在', 404)
    
    if order['status'] != '处理中':
        return error_response('工单状态不允许完成', 400)
    
    cursor.execute("SELECT status FROM devices WHERE device_id = ?", (order['device_id'],))
    device = cursor.fetchone()
    before_status = device['status'] if device else None
    
    cursor.execute(
        '''UPDATE work_orders 
           SET status = '已完成', handle_description = COALESCE(handle_description, '') || ?, complete_time = CURRENT_TIMESTAMP
           WHERE order_no = ?''',
        (f' 处理结果：{result_description}', order_no)
    )
    
    update_device_status_with_log(
        order['device_id'],
        '已修复',
        f'完成工单: {order_no}',
        operator or order['handler'],
        order_no
    )
    
    cursor.execute(
        '''INSERT INTO maintenance_records 
           (device_id, order_no, maintenance_type, action_type, description, before_status, after_status, operator, result, cost, duration)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (
            order['device_id'],
            order_no,
            maintenance_type,
            '故障修复',
            result_description,
            before_status,
            '已修复',
            operator or order['handler'],
            '成功',
            cost,
            duration
        )
    )
    
    db.commit()
    
    return success_response({
        'order_no': order_no,
        'status': '已完成',
        'status_info': ORDER_STATUS_MAP.get('已完成', {})
    }, '工单已完成')

@app.route('/api/work-orders/<order_no>/close', methods=['PUT'])
def close_work_order(order_no):
    data = request.get_json()
    operator = data.get('operator', 'system')
    close_reason = data.get('close_reason', '')
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM work_orders WHERE order_no = ?", (order_no,))
    order = cursor.fetchone()
    
    if not order:
        return error_response('工单不存在', 404)
    
    cursor.execute(
        "UPDATE work_orders SET status = '已关闭', complete_time = CURRENT_TIMESTAMP WHERE order_no = ?",
        (order_no,)
    )
    
    db.commit()
    
    return success_response({
        'order_no': order_no,
        'status': '已关闭'
    }, '工单已关闭')

@app.route('/api/maintenance-records', methods=['GET'])
def get_maintenance_records():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    device_id = request.args.get('device_id')
    order_no = request.args.get('order_no')
    maintenance_type = request.args.get('maintenance_type')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    offset = (page - 1) * page_size
    
    db = get_db()
    cursor = db.cursor()
    
    query = "SELECT * FROM maintenance_records WHERE 1=1"
    params = []
    
    if device_id:
        query += " AND device_id = ?"
        params.append(device_id)
    if order_no:
        query += " AND order_no = ?"
        params.append(order_no)
    if maintenance_type:
        query += " AND maintenance_type = ?"
        params.append(maintenance_type)
    if start_date:
        query += " AND DATE(created_at) >= ?"
        params.append(start_date)
    if end_date:
        query += " AND DATE(created_at) <= ?"
        params.append(end_date)
    
    count_query = query.replace('SELECT *', 'SELECT COUNT(*) as total')
    cursor.execute(count_query, params)
    total = cursor.fetchone()['total']
    
    query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([page_size, offset])
    
    cursor.execute(query, params)
    records = [dict(row) for row in cursor.fetchall()]
    
    return success_response({
        'records': records,
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': (total + page_size - 1) // page_size
    })

@app.route('/api/maintenance-records/<int:record_id>', methods=['GET'])
def get_maintenance_record(record_id):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM maintenance_records WHERE id = ?", (record_id,))
    record = cursor.fetchone()
    
    if not record:
        return error_response('记录不存在', 404)
    
    return success_response(dict(record))

@app.route('/api/maintenance-records', methods=['POST'])
def create_maintenance_record():
    data = request.get_json()
    required_fields = ['device_id', 'maintenance_type', 'description', 'operator']
    
    for field in required_fields:
        if field not in data:
            return error_response(f'缺少必填字段: {field}', 400)
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT status FROM devices WHERE device_id = ?", (data['device_id'],))
    device = cursor.fetchone()
    if not device:
        return error_response('设备不存在', 404)
    
    try:
        cursor.execute(
            '''INSERT INTO maintenance_records 
               (device_id, order_no, maintenance_type, action_type, description, operator, result, cost, duration)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (
                data['device_id'],
                data.get('order_no'),
                data['maintenance_type'],
                data.get('action_type', '常规维护'),
                data['description'],
                data['operator'],
                data.get('result', '成功'),
                data.get('cost', 0),
                data.get('duration', 0)
            )
        )
        
        if data.get('update_device_status'):
            cursor.execute(
                "UPDATE devices SET last_maintenance_date = CURRENT_DATE, updated_at = CURRENT_TIMESTAMP WHERE device_id = ?",
                (data['device_id'],)
            )
        
        db.commit()
        return success_response({'id': cursor.lastrowid}, '维护记录创建成功')
    except Exception as e:
        return error_response(str(e), 500)

@app.route('/api/dashboard/statistics', methods=['GET'])
def get_statistics():
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM devices")
    total_devices = cursor.fetchone()['total']
    
    status_stats = {}
    for status in DEVICE_STATUS_MAP.keys():
        cursor.execute("SELECT COUNT(*) as count FROM devices WHERE status = ?", (status,))
        status_stats[status] = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM devices WHERE online_status = 1 OR last_heartbeat >= datetime('now', '-5 minutes')")
    online_devices = cursor.fetchone()['count']
    
    online_rate = (online_devices / total_devices * 100) if total_devices > 0 else 0
    
    cursor.execute("SELECT COUNT(*) as total FROM work_orders")
    total_orders = cursor.fetchone()['total']
    
    order_status_stats = {}
    for status in ORDER_STATUS_MAP.keys():
        cursor.execute("SELECT COUNT(*) as count FROM work_orders WHERE status = ?", (status,))
        order_status_stats[status] = cursor.fetchone()['count']
    
    priority_stats = {'高': 0, '中': 0, '低': 0}
    for priority in PRIORITY_MAP.keys():
        cursor.execute("SELECT COUNT(*) as count FROM work_orders WHERE priority = ? AND status != '已完成'", (priority,))
        priority_stats[priority] = cursor.fetchone()['count']
    
    cursor.execute("SELECT fault_category, COUNT(*) as count FROM work_orders GROUP BY fault_category")
    category_stats = {row['fault_category'] or '未分类': row['count'] for row in cursor.fetchall()}
    
    cursor.execute("SELECT line, COUNT(*) as count FROM devices WHERE line IS NOT NULL GROUP BY line")
    line_device_stats = {row['line']: row['count'] for row in cursor.fetchall()}
    
    today = datetime.now().date()
    thirty_days_ago = today - timedelta(days=30)
    
    cursor.execute("""
        SELECT COUNT(*) as count FROM work_orders 
        WHERE DATE(report_time) >= ?
    """, (thirty_days_ago.isoformat(),))
    recent_orders = cursor.fetchone()['count']
    
    cursor.execute("""
        SELECT COUNT(*) as count FROM maintenance_records 
        WHERE DATE(created_at) >= ?
    """, (thirty_days_ago.isoformat(),))
    recent_maintenance = cursor.fetchone()['count']
    
    return success_response({
        'devices': {
            'total': total_devices,
            'online': online_devices,
            'online_rate': round(online_rate, 2),
            'status_distribution': status_stats,
            'by_line': line_device_stats
        },
        'orders': {
            'total': total_orders,
            'status_distribution': order_status_stats,
            'pending_priority': priority_stats,
            'by_category': category_stats,
            'recent_30days': recent_orders
        },
        'maintenance': {
            'recent_30days': recent_maintenance
        }
    })

@app.route('/api/dashboard/online-rate', methods=['GET'])
def get_online_rate_detail():
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT DISTINCT line FROM devices WHERE line IS NOT NULL ORDER BY line")
    lines = [row['line'] for row in cursor.fetchall()]
    
    line_stats = []
    for line in lines:
        cursor.execute("SELECT COUNT(*) as total FROM devices WHERE line = ?", (line,))
        total = cursor.fetchone()['total']
        
        cursor.execute("""
            SELECT COUNT(*) as online FROM devices 
            WHERE line = ? AND (online_status = 1 OR last_heartbeat >= datetime('now', '-5 minutes'))
        """, (line,))
        online = cursor.fetchone()['online']
        
        rate = (online / total * 100) if total > 0 else 0
        
        cursor.execute("SELECT COUNT(*) as fault FROM devices WHERE line = ? AND status = '故障'", (line,))
        fault = cursor.fetchone()['fault']
        
        line_stats.append({
            'line': f'{line}号线',
            'total': total,
            'online': online,
            'online_rate': round(rate, 2),
            'fault': fault
        })
    
    cursor.execute("SELECT DISTINCT station FROM devices WHERE station IS NOT NULL ORDER BY station")
    stations = [row['station'] for row in cursor.fetchall()]
    
    station_stats = []
    for station in stations[:20]:
        cursor.execute("SELECT COUNT(*) as total FROM devices WHERE station = ?", (station,))
        total = cursor.fetchone()['total']
        
        cursor.execute("""
            SELECT COUNT(*) as online FROM devices 
            WHERE station = ? AND (online_status = 1 OR last_heartbeat >= datetime('now', '-5 minutes'))
        """, (station,))
        online = cursor.fetchone()['online']
        
        rate = (online / total * 100) if total > 0 else 0
        
        station_stats.append({
            'station': f'{station}站',
            'total': total,
            'online': online,
            'online_rate': round(rate, 2)
        })
    
    return success_response({
        'by_line': line_stats,
        'by_station': station_stats
    })

@app.route('/api/status-logs/<device_id>', methods=['GET'])
def get_device_status_logs(device_id):
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    offset = (page - 1) * page_size
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM device_status_logs WHERE device_id = ?", (device_id,))
    total = cursor.fetchone()['total']
    
    cursor.execute("""
        SELECT * FROM device_status_logs 
        WHERE device_id = ? 
        ORDER BY created_at DESC 
        LIMIT ? OFFSET ?
    """, (device_id, page_size, offset))
    logs = [dict(row) for row in cursor.fetchall()]
    
    return success_response({
        'logs': logs,
        'total': total,
        'page': page,
        'page_size': page_size
    })

@app.route('/api/admins/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return error_response('用户名和密码不能为空', 400)
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM admins WHERE username = ? AND password = ?", (username, password))
    admin = cursor.fetchone()
    
    if not admin:
        return error_response('用户名或密码错误', 401)
    
    return success_response({
        'id': admin['id'],
        'username': admin['username'],
        'real_name': admin['real_name'],
        'role': admin['role']
    }, '登录成功')

@app.errorhandler(404)
def not_found(error):
    return error_response('接口不存在', 404)

@app.errorhandler(500)
def internal_error(error):
    return error_response('服务器内部错误', 500)

if __name__ == '__main__':
    init_db()
    print("="*60)
    print("地铁自动售票检票一体机运维管理系统")
    print("="*60)
    print("数据库初始化完成！")
    print("默认管理员账号: admin / admin123")
    print()
    print("API接口清单:")
    print("-"*60)
    print("[健康检查]")
    print("  GET  /api/health - 健康检查")
    print()
    print("[设备管理]")
    print("  POST /api/devices - 添加设备")
    print("  GET  /api/devices - 获取设备列表（支持线路/站点筛选）")
    print("  GET  /api/devices/<device_id> - 获取设备详情（含工单联动）")
    print("  PUT  /api/devices/<device_id> - 更新设备信息")
    print("  PUT  /api/devices/<device_id>/status - 更新设备状态（带日志）")
    print("  POST /api/devices/<device_id>/heartbeat - 设备心跳上报")
    print("  DELETE /api/devices/<device_id> - 删除设备")
    print()
    print("[工单管理]")
    print("  POST /api/work-orders - 创建工单（自动更新设备状态）")
    print("  GET  /api/work-orders - 获取工单列表（优先级排序、多维度筛选）")
    print("  GET  /api/work-orders/<order_no> - 获取工单详情")
    print("  PUT  /api/work-orders/<order_no>/handle - 处理工单（设备联动）")
    print("  PUT  /api/work-orders/<order_no>/complete - 完成工单（记录日志）")
    print("  PUT  /api/work-orders/<order_no>/close - 关闭工单")
    print()
    print("[维修日志]")
    print("  POST /api/maintenance-records - 创建维护记录")
    print("  GET  /api/maintenance-records - 获取维护记录列表")
    print("  GET  /api/maintenance-records/<id> - 获取维护记录详情")
    print("  GET  /api/status-logs/<device_id> - 获取设备状态变更日志")
    print()
    print("[统计面板]")
    print("  GET  /api/dashboard/statistics - 获取综合统计数据（含在线率）")
    print("  GET  /api/dashboard/online-rate - 按线路/站点统计在线率")
    print("  GET  /api/fault-categories - 获取故障分类和状态配置")
    print()
    print("[管理员]")
    print("  POST /api/admins/login - 管理员登录")
    print("="*60)
    app.run(host='0.0.0.0', port=5000, debug=True)
