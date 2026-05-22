from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

DATABASE = 'campus_card.db'


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT UNIQUE NOT NULL,
            device_name TEXT NOT NULL,
            device_model TEXT,
            communication_mode TEXT,
            campus TEXT,
            building TEXT,
            location TEXT NOT NULL,
            status TEXT DEFAULT '正常',
            enable_date TEXT,
            last_maintain_date TEXT,
            create_time TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fault_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_code TEXT UNIQUE NOT NULL,
            type_name TEXT NOT NULL,
            description TEXT,
            priority TEXT DEFAULT '普通',
            impact_level TEXT DEFAULT '低影响',
            create_time TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS work_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT UNIQUE NOT NULL,
            device_id TEXT NOT NULL,
            fault_type TEXT NOT NULL,
            fault_type_code TEXT,
            priority TEXT DEFAULT '普通',
            impact_level TEXT DEFAULT '低影响',
            fault_description TEXT,
            reporter TEXT,
            reporter_phone TEXT,
            status TEXT DEFAULT '待处理',
            report_time TEXT DEFAULT CURRENT_TIMESTAMP,
            handle_time TEXT,
            complete_time TEXT,
            handler TEXT,
            handle_note TEXT,
            FOREIGN KEY (device_id) REFERENCES devices (device_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS maintain_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            order_id TEXT,
            maintain_type TEXT NOT NULL,
            maintain_description TEXT,
            maintain_time TEXT DEFAULT CURRENT_TIMESTAMP,
            maintainer TEXT,
            FOREIGN KEY (device_id) REFERENCES devices (device_id)
        )
    ''')

    fault_types_data = [
        ('HW001', '硬件故障', '设备硬件损坏，如触摸屏、读卡器等', '高', '校园生活影响较大'),
        ('HW002', '电源故障', '设备供电异常', '中', '影响单台设备使用'),
        ('SW001', '软件崩溃', '系统软件异常退出', '高', '设备完全不可用'),
        ('SW002', '交易异常', '充值/消费交易失败', '紧急', '直接影响师生资金业务'),
        ('NET001', '网络断开', '设备无法连接服务器', '高', '无法进行联网交易'),
        ('NET002', '网络延迟', '网络响应缓慢', '中', '影响用户体验'),
        ('OTH001', '其他故障', '未分类的其他问题', '普通', '影响较小')
    ]

    for ft in fault_types_data:
        cursor.execute('''
            INSERT OR IGNORE INTO fault_types (type_code, type_name, description, priority, impact_level)
            VALUES (?, ?, ?, ?, ?)
        ''', ft)

    conn.commit()
    conn.close()


def generate_order_id():
    now = datetime.now()
    date_str = now.strftime('%Y%m%d')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT order_id FROM work_orders WHERE order_id LIKE ? ORDER BY order_id DESC LIMIT 1', (f'WO{date_str}%',))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        last_num = int(row['order_id'][-4:])
        new_num = last_num + 1
    else:
        new_num = 1
    
    return f'WO{date_str}{new_num:04d}'


@app.route('/api/devices', methods=['GET'])
def get_devices():
    campus = request.args.get('campus')
    building = request.args.get('building')
    status = request.args.get('status')
    
    conn = get_db()
    cursor = conn.cursor()
    
    query = 'SELECT * FROM devices WHERE 1=1'
    params = []
    
    if campus:
        query += ' AND campus = ?'
        params.append(campus)
    if building:
        query += ' AND building = ?'
        params.append(building)
    if status:
        query += ' AND status = ?'
        params.append(status)
    
    query += ' ORDER BY create_time DESC'
    cursor.execute(query, params)
    devices = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({
        'code': 200,
        'data': {
            'list': devices,
            'total': len(devices)
        },
        'msg': 'success'
    })


@app.route('/api/devices/<device_id>', methods=['GET'])
def get_device(device_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM devices WHERE device_id = ?', (device_id,))
    device = cursor.fetchone()
    conn.close()
    if device:
        return jsonify({'code': 200, 'data': dict(device), 'msg': 'success'})
    return jsonify({'code': 404, 'data': None, 'msg': '设备不存在'}), 404


@app.route('/api/devices', methods=['POST'])
def add_device():
    data = request.get_json()
    device_id = data.get('device_id')
    device_name = data.get('device_name')
    device_model = data.get('device_model', '')
    communication_mode = data.get('communication_mode', '')
    campus = data.get('campus', '')
    building = data.get('building', '')
    location = data.get('location')
    status = data.get('status', '正常')
    enable_date = data.get('enable_date')

    if not all([device_id, device_name, location]):
        return jsonify({'code': 400, 'msg': '设备编号、名称、位置不能为空'}), 400

    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO devices (device_id, device_name, device_model, communication_mode, campus, building, location, status, enable_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (device_id, device_name, device_model, communication_mode, campus, building, location, status, enable_date))
        conn.commit()
        return jsonify({'code': 200, 'data': None, 'msg': '设备添加成功'})
    except sqlite3.IntegrityError:
        return jsonify({'code': 400, 'data': None, 'msg': '设备编号已存在'}), 400
    finally:
        conn.close()


@app.route('/api/devices/<device_id>', methods=['PUT'])
def update_device(device_id):
    data = request.get_json()
    device_name = data.get('device_name')
    device_model = data.get('device_model')
    communication_mode = data.get('communication_mode')
    campus = data.get('campus')
    building = data.get('building')
    location = data.get('location')
    enable_date = data.get('enable_date')

    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM devices WHERE device_id = ?', (device_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'code': 404, 'data': None, 'msg': '设备不存在'}), 404

    update_fields = []
    update_values = []
    
    if device_name:
        update_fields.append('device_name = ?')
        update_values.append(device_name)
    if device_model:
        update_fields.append('device_model = ?')
        update_values.append(device_model)
    if communication_mode:
        update_fields.append('communication_mode = ?')
        update_values.append(communication_mode)
    if campus:
        update_fields.append('campus = ?')
        update_values.append(campus)
    if building:
        update_fields.append('building = ?')
        update_values.append(building)
    if location:
        update_fields.append('location = ?')
        update_values.append(location)
    if enable_date:
        update_fields.append('enable_date = ?')
        update_values.append(enable_date)
    
    if update_fields:
        update_values.append(device_id)
        cursor.execute(f'UPDATE devices SET {", ".join(update_fields)} WHERE device_id = ?', update_values)
        conn.commit()
    
    conn.close()
    return jsonify({'code': 200, 'data': None, 'msg': '设备信息更新成功'})


@app.route('/api/fault-types', methods=['GET'])
def get_fault_types():
    priority = request.args.get('priority')
    
    conn = get_db()
    cursor = conn.cursor()
    
    query = 'SELECT * FROM fault_types WHERE 1=1'
    params = []
    
    if priority:
        query += ' AND priority = ?'
        params.append(priority)
    
    query += ' ORDER BY priority DESC, type_code'
    cursor.execute(query, params)
    fault_types = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({
        'code': 200,
        'data': {
            'list': fault_types,
            'total': len(fault_types)
        },
        'msg': 'success'
    })


@app.route('/api/devices/<device_id>/status', methods=['PUT'])
def update_device_status(device_id):
    data = request.get_json()
    status = data.get('status')
    
    valid_status = ['正常', '故障', '维修中', '已修复']
    if status not in valid_status:
        return jsonify({'code': 400, 'data': None, 'msg': f'状态必须是: {", ".join(valid_status)}'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE devices SET status = ? WHERE device_id = ?', (status, device_id))
    conn.commit()
    conn.close()
    
    return jsonify({'code': 200, 'data': None, 'msg': '状态更新成功'})


@app.route('/api/devices/<device_id>', methods=['DELETE'])
def delete_device(device_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM devices WHERE device_id = ?', (device_id,))
    conn.commit()
    conn.close()
    return jsonify({'code': 200, 'data': None, 'msg': '设备删除成功'})


@app.route('/api/work-orders', methods=['POST'])
def create_work_order():
    data = request.get_json()
    device_id = data.get('device_id')
    fault_type = data.get('fault_type')
    fault_type_code = data.get('fault_type_code', '')
    priority = data.get('priority', '普通')
    impact_level = data.get('impact_level', '低影响')
    fault_description = data.get('fault_description', '')
    reporter = data.get('reporter', '')
    reporter_phone = data.get('reporter_phone', '')

    if not all([device_id, fault_type]):
        return jsonify({'code': 400, 'data': None, 'msg': '设备编号和故障类型不能为空'}), 400

    valid_priorities = ['普通', '中', '高', '紧急']
    if priority not in valid_priorities:
        return jsonify({'code': 400, 'data': None, 'msg': f'优先级必须为: {", ".join(valid_priorities)}'}), 400

    valid_impacts = ['低影响', '中影响', '高影响', '严重影响']
    if impact_level not in valid_impacts:
        return jsonify({'code': 400, 'data': None, 'msg': f'影响程度必须为: {", ".join(valid_impacts)}'}), 400

    order_id = generate_order_id()
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM devices WHERE device_id = ?', (device_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'code': 404, 'data': None, 'msg': '设备不存在'}), 404

    try:
        cursor.execute('''
            INSERT INTO work_orders (order_id, device_id, fault_type, fault_type_code, priority, impact_level, fault_description, reporter, reporter_phone)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (order_id, device_id, fault_type, fault_type_code, priority, impact_level, fault_description, reporter, reporter_phone))
        
        cursor.execute('UPDATE devices SET status = ? WHERE device_id = ?', ('故障', device_id))
        
        conn.commit()
        return jsonify({
            'code': 200,
            'data': {'order_id': order_id, 'priority': priority, 'impact_level': impact_level},
            'msg': '工单创建成功'
        })
    except Exception as e:
        conn.rollback()
        return jsonify({'code': 500, 'data': None, 'msg': str(e)}), 500
    finally:
        conn.close()


@app.route('/api/work-orders', methods=['GET'])
def get_work_orders():
    status = request.args.get('status')
    priority = request.args.get('priority')
    fault_type_code = request.args.get('fault_type_code')
    device_id = request.args.get('device_id')
    
    conn = get_db()
    cursor = conn.cursor()
    
    query = 'SELECT * FROM work_orders WHERE 1=1'
    params = []
    
    if status:
        query += ' AND status = ?'
        params.append(status)
    if priority:
        query += ' AND priority = ?'
        params.append(priority)
    if fault_type_code:
        query += ' AND fault_type_code = ?'
        params.append(fault_type_code)
    if device_id:
        query += ' AND device_id = ?'
        params.append(device_id)
    
    query += ' ORDER BY priority DESC, report_time DESC'
    cursor.execute(query, params)
    orders = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({
        'code': 200,
        'data': {
            'list': orders,
            'total': len(orders)
        },
        'msg': 'success'
    })


@app.route('/api/work-orders/<order_id>/handle', methods=['PUT'])
def handle_work_order(order_id):
    data = request.get_json()
    handler = data.get('handler', '')
    handle_note = data.get('handle_note', '')
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM work_orders WHERE order_id = ?', (order_id,))
    order = cursor.fetchone()
    
    if not order:
        conn.close()
        return jsonify({'code': 404, 'data': None, 'msg': '工单不存在'}), 404
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
        UPDATE work_orders 
        SET status = '处理中', handle_time = ?, handler = ?, handle_note = ?
        WHERE order_id = ?
    ''', (now, handler, handle_note, order_id))
    
    cursor.execute('UPDATE devices SET status = ? WHERE device_id = ?', ('维修中', order['device_id']))
    
    conn.commit()
    conn.close()
    
    return jsonify({'code': 200, 'data': None, 'msg': '工单已开始处理'})


@app.route('/api/work-orders/<order_id>/complete', methods=['PUT'])
def complete_work_order(order_id):
    data = request.get_json()
    handle_note = data.get('handle_note', '')
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM work_orders WHERE order_id = ?', (order_id,))
    order = cursor.fetchone()
    
    if not order:
        conn.close()
        return jsonify({'code': 404, 'data': None, 'msg': '工单不存在'}), 404
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
        UPDATE work_orders 
        SET status = '已完成', complete_time = ?, handle_note = COALESCE(?, handle_note)
        WHERE order_id = ?
    ''', (now, handle_note, order_id))
    
    cursor.execute('UPDATE devices SET status = ?, last_maintain_date = ? WHERE device_id = ?', ('已修复', now, order['device_id']))
    
    cursor.execute('''
        INSERT INTO maintain_records (device_id, order_id, maintain_type, maintain_description, maintain_time, maintainer)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (order['device_id'], order_id, '故障维修', handle_note or order['handle_note'] or '', now, order['handler'] or '管理员'))
    
    conn.commit()
    conn.close()
    
    return jsonify({'code': 200, 'data': None, 'msg': '工单已完成'})


@app.route('/api/maintain-records', methods=['GET'])
def get_maintain_records():
    device_id = request.args.get('device_id')
    maintain_type = request.args.get('maintain_type')
    
    conn = get_db()
    cursor = conn.cursor()
    
    query = 'SELECT * FROM maintain_records WHERE 1=1'
    params = []
    
    if device_id:
        query += ' AND device_id = ?'
        params.append(device_id)
    if maintain_type:
        query += ' AND maintain_type = ?'
        params.append(maintain_type)
    
    query += ' ORDER BY maintain_time DESC'
    cursor.execute(query, params)
    records = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({
        'code': 200,
        'data': {
            'list': records,
            'total': len(records)
        },
        'msg': 'success'
    })


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    campus = request.args.get('campus')
    building = request.args.get('building')
    
    conn = get_db()
    cursor = conn.cursor()
    
    where_clause = 'WHERE 1=1'
    params = []
    
    if campus:
        where_clause += ' AND campus = ?'
        params.append(campus)
    if building:
        where_clause += ' AND building = ?'
        params.append(building)
    
    cursor.execute(f'SELECT COUNT(*) as total FROM devices {where_clause}', params)
    total_devices = cursor.fetchone()['total']
    
    cursor.execute(f"SELECT COUNT(*) as count FROM devices {where_clause.replace('WHERE', 'AND')} AND status = '正常'", params)
    normal_devices = cursor.fetchone()['count']
    
    cursor.execute(f"SELECT COUNT(*) as count FROM devices {where_clause.replace('WHERE', 'AND')} AND status = '故障'", params)
    fault_devices = cursor.fetchone()['count']
    
    cursor.execute(f"SELECT COUNT(*) as count FROM devices {where_clause.replace('WHERE', 'AND')} AND status = '维修中'", params)
    repairing_devices = cursor.fetchone()['count']
    
    cursor.execute(f"SELECT COUNT(*) as count FROM devices {where_clause.replace('WHERE', 'AND')} AND status = '已修复'", params)
    repaired_devices = cursor.fetchone()['count']
    
    intact_rate = 0
    if total_devices > 0:
        intact_rate = round((normal_devices + repaired_devices) / total_devices * 100, 2)
    
    cursor.execute('SELECT COUNT(*) as total FROM work_orders')
    total_orders = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as count FROM work_orders WHERE status = '待处理'")
    pending_orders = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM work_orders WHERE status = '处理中'")
    handling_orders = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM work_orders WHERE status = '已完成'")
    completed_orders = cursor.fetchone()['count']
    
    cursor.execute("SELECT priority, COUNT(*) as count FROM work_orders GROUP BY priority")
    priority_stats = {row['priority']: row['count'] for row in cursor.fetchall()}
    
    cursor.execute("SELECT fault_type_code, fault_type, COUNT(*) as count FROM work_orders GROUP BY fault_type_code, fault_type")
    type_stats = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute('SELECT campus, COUNT(*) as count FROM devices WHERE campus IS NOT NULL AND campus != "" GROUP BY campus')
    campus_stats = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute('SELECT building, COUNT(*) as count FROM devices WHERE building IS NOT NULL AND building != "" GROUP BY building')
    building_stats = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({
        'code': 200,
        'data': {
            'devices': {
                'total': total_devices,
                'normal': normal_devices,
                'fault': fault_devices,
                'repairing': repairing_devices,
                'repaired': repaired_devices,
                'intact_rate': f'{intact_rate}%'
            },
            'work_orders': {
                'total': total_orders,
                'pending': pending_orders,
                'handling': handling_orders,
                'completed': completed_orders,
                'completion_rate': f'{round(completed_orders / total_orders * 100, 2) if total_orders > 0 else 0}%'
            },
            'priority_distribution': priority_stats,
            'type_distribution': type_stats,
            'campus_distribution': campus_stats,
            'building_distribution': building_stats
        },
        'msg': 'success'
    })


if __name__ == '__main__':
    init_db()
    print('数据库初始化完成')
    print('服务启动地址: http://127.0.0.1:5000')
    app.run(debug=False, host='0.0.0.0', port=5000)
