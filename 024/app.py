from flask import Flask, request, jsonify, g
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATABASE = 'traffic_management.db'

def success_response(data=None, message='操作成功', code=200):
    response = {
        'code': code,
        'message': message,
        'success': True,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), code

def error_response(message='操作失败', code=400, data=None):
    response = {
        'code': code,
        'message': message,
        'success': False,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), code

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
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_code TEXT UNIQUE NOT NULL,
                device_name TEXT NOT NULL,
                device_model TEXT,
                communication_protocol TEXT,
                service_hall TEXT,
                location TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT '正常',
                install_date TEXT NOT NULL,
                enable_date TEXT,
                last_maintain_date TEXT,
                create_time TEXT NOT NULL,
                update_time TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS work_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_no TEXT UNIQUE NOT NULL,
                device_id INTEGER NOT NULL,
                fault_type TEXT NOT NULL,
                fault_category TEXT NOT NULL DEFAULT '其他',
                fault_level TEXT NOT NULL DEFAULT '一般',
                priority TEXT NOT NULL DEFAULT '中',
                fault_description TEXT NOT NULL,
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
            CREATE TABLE IF NOT EXISTS maintain_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER NOT NULL,
                maintain_type TEXT NOT NULL,
                maintain_desc TEXT NOT NULL,
                maintain_user TEXT NOT NULL,
                maintain_time TEXT NOT NULL,
                create_time TEXT NOT NULL,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        ''')
        
        db.commit()

def generate_order_no():
    now = datetime.now()
    prefix = 'WO' + now.strftime('%Y%m%d')
    with app.app_context():
        cursor = get_db().cursor()
        cursor.execute('SELECT order_no FROM work_orders WHERE order_no LIKE ? ORDER BY order_no DESC LIMIT 1', (prefix + '%',))
        result = cursor.fetchone()
        if result:
            last_no = result['order_no']
            seq = int(last_no[-4:]) + 1
        else:
            seq = 1
        return prefix + str(seq).zfill(4)

@app.route('/api/service-halls', methods=['GET'])
def get_service_halls():
    halls = [
        {'code': 'A', 'name': 'A服务大厅'},
        {'code': 'B', 'name': 'B服务大厅'},
        {'code': 'C', 'name': 'C服务大厅'},
        {'code': 'D', 'name': 'D服务大厅'}
    ]
    return success_response(data=halls)

@app.route('/api/fault-levels', methods=['GET'])
def get_fault_levels():
    levels = [
        {'code': '紧急', 'name': '紧急', 'description': '系统完全瘫痪，所有业务无法办理'},
        {'code': '严重', 'name': '严重', 'description': '核心功能故障，主要业务受影响'},
        {'code': '一般', 'name': '一般', 'description': '部分功能故障，不影响主要业务'},
        {'code': '轻微', 'name': '轻微', 'description': '轻微问题，不影响业务运行'}
    ]
    return success_response(data=levels)

@app.route('/api/devices', methods=['GET'])
def get_devices():
    service_hall = request.args.get('service_hall')
    status = request.args.get('status')
    
    query = 'SELECT * FROM devices WHERE 1=1'
    params = []
    
    if service_hall:
        query += ' AND service_hall = ?'
        params.append(service_hall)
    if status:
        query += ' AND status = ?'
        params.append(status)
    
    query += ' ORDER BY create_time DESC'
    
    cursor = get_db().cursor()
    cursor.execute(query, params)
    devices = cursor.fetchall()
    
    result = [dict(row) for row in devices]
    return success_response(data=result)

@app.route('/api/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    cursor = get_db().cursor()
    cursor.execute('SELECT * FROM devices WHERE id = ?', (device_id,))
    device = cursor.fetchone()
    if device:
        return success_response(data=dict(device))
    return error_response(message='设备不存在', code=404)

@app.route('/api/devices', methods=['POST'])
def add_device():
    data = request.json
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute('''
            INSERT INTO devices (device_code, device_name, device_model, communication_protocol,
                                service_hall, location, status, install_date, enable_date, create_time, update_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['device_code'], data['device_name'], data.get('device_model', ''),
              data.get('communication_protocol', ''), data.get('service_hall', ''),
              data['location'], '正常', data.get('install_date', now.split()[0]),
              data.get('enable_date', ''), now, now))
        db.commit()
        return success_response(data={'id': cursor.lastrowid}, message='设备添加成功')
    except sqlite3.IntegrityError:
        return error_response(message='设备编号已存在', code=400)

@app.route('/api/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    data = request.json
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db = get_db()
    cursor = db.cursor()
    
    update_fields = []
    params = []
    
    if 'device_name' in data:
        update_fields.append('device_name = ?')
        params.append(data['device_name'])
    if 'device_model' in data:
        update_fields.append('device_model = ?')
        params.append(data['device_model'])
    if 'communication_protocol' in data:
        update_fields.append('communication_protocol = ?')
        params.append(data['communication_protocol'])
    if 'service_hall' in data:
        update_fields.append('service_hall = ?')
        params.append(data['service_hall'])
    if 'location' in data:
        update_fields.append('location = ?')
        params.append(data['location'])
    if 'status' in data:
        update_fields.append('status = ?')
        params.append(data['status'])
    if 'install_date' in data:
        update_fields.append('install_date = ?')
        params.append(data['install_date'])
    if 'enable_date' in data:
        update_fields.append('enable_date = ?')
        params.append(data['enable_date'])
    
    if not update_fields:
        return error_response(message='没有更新字段', code=400)
    
    update_fields.append('update_time = ?')
    params.append(now)
    params.append(device_id)
    
    cursor.execute(f'''
        UPDATE devices SET {', '.join(update_fields)} WHERE id = ?
    ''', params)
    db.commit()
    
    if cursor.rowcount:
        return success_response(message='设备更新成功')
    return error_response(message='设备不存在', code=404)

@app.route('/api/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM devices WHERE id = ?', (device_id,))
    db.commit()
    if cursor.rowcount:
        return success_response(message='设备删除成功')
    return error_response(message='设备不存在', code=404)

@app.route('/api/devices/<int:device_id>/status', methods=['PUT'])
def update_device_status(device_id):
    data = request.json
    status = data.get('status')
    if status not in ['正常', '故障', '维修中', '已修复']:
        return error_response(message='无效的状态值', code=400)
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        UPDATE devices SET status = ?, update_time = ? WHERE id = ?
    ''', (status, now, device_id))
    db.commit()
    
    if cursor.rowcount:
        return success_response(message='状态更新成功')
    return error_response(message='设备不存在', code=404)

@app.route('/api/work-orders', methods=['GET'])
def get_work_orders():
    status = request.args.get('status')
    device_id = request.args.get('device_id')
    fault_category = request.args.get('fault_category')
    fault_level = request.args.get('fault_level')
    priority = request.args.get('priority')
    service_hall = request.args.get('service_hall')
    handle_user = request.args.get('handle_user')
    
    query = '''
        SELECT wo.*, d.device_code, d.device_name, d.location, d.service_hall
        FROM work_orders wo
        JOIN devices d ON wo.device_id = d.id
        WHERE 1=1
    '''
    params = []
    
    if status:
        query += ' AND wo.status = ?'
        params.append(status)
    if device_id:
        query += ' AND wo.device_id = ?'
        params.append(device_id)
    if fault_category:
        query += ' AND wo.fault_category = ?'
        params.append(fault_category)
    if fault_level:
        query += ' AND wo.fault_level = ?'
        params.append(fault_level)
    if priority:
        query += ' AND wo.priority = ?'
        params.append(priority)
    if service_hall:
        query += ' AND d.service_hall = ?'
        params.append(service_hall)
    if handle_user:
        query += ' AND wo.handle_user = ?'
        params.append(handle_user)
    
    query += ' ORDER BY CASE wo.priority WHEN "高" THEN 1 WHEN "中" THEN 2 WHEN "低" THEN 3 END, wo.create_time DESC'
    
    cursor = get_db().cursor()
    cursor.execute(query, params)
    orders = cursor.fetchall()
    
    result = [dict(row) for row in orders]
    return success_response(data=result)

@app.route('/api/work-orders/<int:order_id>', methods=['GET'])
def get_work_order(order_id):
    cursor = get_db().cursor()
    cursor.execute('''
        SELECT wo.*, d.device_code, d.device_name, d.location, d.service_hall
        FROM work_orders wo
        JOIN devices d ON wo.device_id = d.id
        WHERE wo.id = ?
    ''', (order_id,))
    order = cursor.fetchone()
    if order:
        return success_response(data=dict(order))
    return error_response(message='工单不存在', code=404)

@app.route('/api/work-orders', methods=['POST'])
def create_work_order():
    data = request.json
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    order_no = generate_order_no()
    
    fault_categories = ['硬件故障', '软件故障', '网络故障', '系统故障', '支付故障', '打印故障', '其他']
    fault_category = data.get('fault_category', '其他')
    if fault_category not in fault_categories:
        fault_category = '其他'
    
    fault_levels = ['紧急', '严重', '一般', '轻微']
    fault_level = data.get('fault_level', '一般')
    if fault_level not in fault_levels:
        fault_level = '一般'
    
    priorities = ['高', '中', '低']
    priority = data.get('priority', '中')
    if priority not in priorities:
        priority = '中'
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('''
        INSERT INTO work_orders (order_no, device_id, fault_type, fault_category, fault_level, priority,
                                fault_description, reporter, reporter_phone, status, create_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, '待处理', ?)
    ''', (order_no, data['device_id'], data['fault_type'], fault_category, fault_level, priority,
          data['fault_description'], data['reporter'], data.get('reporter_phone', ''), now))
    db.commit()
    
    cursor.execute('''
        UPDATE devices SET status = '故障', update_time = ? WHERE id = ?
    ''', (now, data['device_id']))
    db.commit()
    
    return success_response(data={'id': cursor.lastrowid, 'order_no': order_no}, message='故障上报成功')

@app.route('/api/work-orders/<int:order_id>/handle', methods=['PUT'])
def handle_work_order(order_id):
    data = request.json
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT device_id FROM work_orders WHERE id = ?', (order_id,))
    order = cursor.fetchone()
    if not order:
        return error_response(message='工单不存在', code=404)
    
    device_id = order['device_id']
    new_status = data.get('status', '处理中')
    
    cursor.execute('''
        UPDATE work_orders
        SET status = ?, handle_user = ?, handle_desc = ?, handle_time = ?
        WHERE id = ?
    ''', (new_status, data.get('handle_user', ''), data.get('handle_desc', ''), now, order_id))
    
    device_status_map = {
        '处理中': '维修中',
        '已完成': '已修复'
    }
    if new_status in device_status_map:
        cursor.execute('''
            UPDATE devices SET status = ?, update_time = ? WHERE id = ?
        ''', (device_status_map[new_status], now, device_id))
    
    db.commit()
    return success_response(message='工单处理成功')

@app.route('/api/maintain-records', methods=['GET'])
def get_maintain_records():
    device_id = request.args.get('device_id')
    service_hall = request.args.get('service_hall')
    
    query = '''
        SELECT mr.*, d.device_code, d.device_name, d.location, d.service_hall
        FROM maintain_records mr
        JOIN devices d ON mr.device_id = d.id
        WHERE 1=1
    '''
    params = []
    
    if device_id:
        query += ' AND mr.device_id = ?'
        params.append(device_id)
    if service_hall:
        query += ' AND d.service_hall = ?'
        params.append(service_hall)
    
    query += ' ORDER BY mr.maintain_time DESC'
    
    cursor = get_db().cursor()
    cursor.execute(query, params)
    records = cursor.fetchall()
    
    result = [dict(row) for row in records]
    return success_response(data=result)

@app.route('/api/maintain-records', methods=['POST'])
def add_maintain_record():
    data = request.json
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO maintain_records (device_id, maintain_type, maintain_desc, maintain_user, maintain_time, create_time)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (data['device_id'], data['maintain_type'], data['maintain_desc'],
          data['maintain_user'], data.get('maintain_time', now), now))
    db.commit()
    
    cursor.execute('''
        UPDATE devices SET last_maintain_date = ?, update_time = ? WHERE id = ?
    ''', (data.get('maintain_time', now).split()[0], now, data['device_id']))
    db.commit()
    
    return success_response(data={'id': cursor.lastrowid}, message='运维记录添加成功')

@app.route('/api/fault-categories', methods=['GET'])
def get_fault_categories():
    categories = [
        {'code': '硬件故障', 'name': '硬件故障', 'description': '终端硬件设备故障，如触摸屏、读卡器、打印机等'},
        {'code': '软件故障', 'name': '软件故障', 'description': '应用程序、操作系统故障'},
        {'code': '网络故障', 'name': '网络故障', 'description': '网络连接、通信故障'},
        {'code': '系统故障', 'name': '系统故障', 'description': '核心业务系统故障'},
        {'code': '支付故障', 'name': '支付故障', 'description': '支付模块、银联/支付宝/微信支付故障'},
        {'code': '打印故障', 'name': '打印故障', 'description': '凭证打印、票据打印故障'},
        {'code': '其他', 'name': '其他', 'description': '其他类型故障'}
    ]
    return success_response(data=categories)

@app.route('/api/priorities', methods=['GET'])
def get_priorities():
    priorities = [
        {'code': '高', 'name': '高优先级', 'business_impact': '严重影响车管业务办理，导致终端完全不可用，影响缴费、上牌、违章处理等核心业务'},
        {'code': '中', 'name': '中优先级', 'business_impact': '部分功能受影响，终端部分业务可办理，非核心功能故障'},
        {'code': '低', 'name': '低优先级', 'business_impact': '轻微影响，不影响主要业务办理，仅影响辅助功能或界面显示'}
    ]
    return success_response(data=priorities)

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    cursor = get_db().cursor()
    
    cursor.execute('SELECT COUNT(*) as total FROM devices')
    total_devices = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as count FROM devices WHERE status = '正常'")
    normal_devices = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM devices WHERE status = '故障'")
    fault_devices = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM devices WHERE status = '维修中'")
    repairing_devices = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM devices WHERE status = '已修复'")
    repaired_devices = cursor.fetchone()['count']
    
    online_health_rate = 0
    if total_devices > 0:
        online_health_rate = round((normal_devices / total_devices) * 100, 2)
    
    cursor.execute("SELECT COUNT(*) as count FROM work_orders WHERE status = '待处理'")
    pending_orders = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM work_orders WHERE status = '处理中'")
    processing_orders = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM work_orders WHERE status = '已完成'")
    completed_orders = cursor.fetchone()['count']
    
    cursor.execute("SELECT priority, COUNT(*) as count FROM work_orders WHERE status != '已完成' GROUP BY priority")
    priority_stats = cursor.fetchall()
    priority_distribution = {row['priority']: row['count'] for row in priority_stats}
    
    cursor.execute("SELECT fault_category, COUNT(*) as count FROM work_orders WHERE status != '已完成' GROUP BY fault_category")
    category_stats = cursor.fetchall()
    category_distribution = {row['fault_category']: row['count'] for row in category_stats}
    
    cursor.execute("SELECT fault_level, COUNT(*) as count FROM work_orders WHERE status != '已完成' GROUP BY fault_level")
    level_stats = cursor.fetchall()
    level_distribution = {row['fault_level']: row['count'] for row in level_stats}
    
    cursor.execute('''
        SELECT d.service_hall, COUNT(*) as total,
               SUM(CASE WHEN d.status = '正常' THEN 1 ELSE 0 END) as normal_count
        FROM devices d
        GROUP BY d.service_hall
    ''')
    hall_stats = cursor.fetchall()
    hall_distribution = []
    for row in hall_stats:
        hall_rate = 0
        if row['total'] > 0:
            hall_rate = round((row['normal_count'] / row['total']) * 100, 2)
        hall_distribution.append({
            'service_hall': row['service_hall'] or '未分配',
            'total': row['total'],
            'normal_count': row['normal_count'],
            'health_rate': hall_rate
        })
    
    return success_response(data={
        'total_devices': total_devices,
        'normal_devices': normal_devices,
        'fault_devices': fault_devices,
        'repairing_devices': repairing_devices,
        'repaired_devices': repaired_devices,
        'online_health_rate': online_health_rate,
        'pending_orders': pending_orders,
        'processing_orders': processing_orders,
        'completed_orders': completed_orders,
        'priority_distribution': priority_distribution,
        'category_distribution': category_distribution,
        'level_distribution': level_distribution,
        'hall_distribution': hall_distribution
    })

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
