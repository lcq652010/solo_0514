from flask import Flask, request, jsonify, g
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
DATABASE = 'metro_tvm.db'

FAULT_TYPES = ['卡票', '卡币', '不找零', '无法支付']

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
                device_id TEXT PRIMARY KEY,
                device_name TEXT NOT NULL,
                location TEXT NOT NULL,
                station TEXT NOT NULL,
                device_serial TEXT,
                production_date TEXT,
                status TEXT NOT NULL DEFAULT '正常',
                install_date TEXT,
                manufacturer TEXT,
                model TEXT,
                create_time TEXT NOT NULL,
                update_time TEXT NOT NULL,
                CHECK (status IN ('正常', '故障', '停用'))
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS work_orders (
                order_id TEXT PRIMARY KEY,
                device_id TEXT NOT NULL,
                fault_type TEXT NOT NULL,
                fault_description TEXT,
                reporter TEXT,
                contact TEXT,
                status TEXT NOT NULL DEFAULT '待处理',
                report_time TEXT NOT NULL,
                fault_hour INTEGER,
                period_type TEXT,
                handle_time TEXT,
                handle_result TEXT,
                FOREIGN KEY (device_id) REFERENCES devices (device_id),
                CHECK (status IN ('待处理', '处理中', '已完成')),
                CHECK (period_type IN ('高峰', '平峰'))
            )
        ''')
        
        db.commit()

def generate_order_id():
    now = datetime.now()
    date_str = now.strftime('%Y%m%d')
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT COUNT(*) FROM work_orders WHERE order_id LIKE ?', (f'WO{date_str}%',))
    count = cursor.fetchone()[0] + 1
    return f'WO{date_str}{count:04d}'

def get_period_type(hour):
    if 7 <= hour <= 9 or 17 <= hour <= 19:
        return '高峰'
    return '平峰'

@app.route('/api/devices', methods=['POST'])
def add_device():
    data = request.get_json()
    required_fields = ['device_id', 'device_name', 'location', 'station']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'缺少必填字段: {field}'}), 400
    
    now = datetime.now().isoformat()
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO devices (device_id, device_name, location, station, device_serial, 
                                production_date, status, install_date, manufacturer, model, 
                                create_time, update_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['device_id'],
            data['device_name'],
            data['location'],
            data['station'],
            data.get('device_serial'),
            data.get('production_date'),
            data.get('status', '正常'),
            data.get('install_date'),
            data.get('manufacturer'),
            data.get('model'),
            now,
            now
        ))
        db.commit()
        return jsonify({'message': '设备添加成功', 'device_id': data['device_id']}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': '设备ID已存在'}), 400

@app.route('/api/devices', methods=['GET'])
def get_devices():
    status = request.args.get('status')
    station = request.args.get('station')
    device_id = request.args.get('device_id')
    
    query = 'SELECT * FROM devices WHERE 1=1'
    params = []
    
    if status:
        query += ' AND status = ?'
        params.append(status)
    if station:
        query += ' AND station LIKE ?'
        params.append(f'%{station}%')
    if device_id:
        query += ' AND device_id LIKE ?'
        params.append(f'%{device_id}%')
    
    query += ' ORDER BY create_time DESC'
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    devices = []
    for row in rows:
        devices.append({
            'device_id': row['device_id'],
            'device_name': row['device_name'],
            'location': row['location'],
            'station': row['station'],
            'device_serial': row['device_serial'],
            'production_date': row['production_date'],
            'status': row['status'],
            'install_date': row['install_date'],
            'manufacturer': row['manufacturer'],
            'model': row['model'],
            'create_time': row['create_time'],
            'update_time': row['update_time']
        })
    
    return jsonify(devices)

@app.route('/api/devices/<device_id>', methods=['GET'])
def get_device(device_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM devices WHERE device_id = ?', (device_id,))
    row = cursor.fetchone()
    
    if not row:
        return jsonify({'error': '设备不存在'}), 404
    
    device = {
        'device_id': row['device_id'],
        'device_name': row['device_name'],
        'location': row['location'],
        'station': row['station'],
        'device_serial': row['device_serial'],
        'production_date': row['production_date'],
        'status': row['status'],
        'install_date': row['install_date'],
        'manufacturer': row['manufacturer'],
        'model': row['model'],
        'create_time': row['create_time'],
        'update_time': row['update_time']
    }
    
    return jsonify(device)

@app.route('/api/devices/<device_id>', methods=['PUT'])
def update_device(device_id):
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM devices WHERE device_id = ?', (device_id,))
    if not cursor.fetchone():
        return jsonify({'error': '设备不存在'}), 404
    
    update_fields = []
    params = []
    
    if 'device_name' in data:
        update_fields.append('device_name = ?')
        params.append(data['device_name'])
    if 'location' in data:
        update_fields.append('location = ?')
        params.append(data['location'])
    if 'station' in data:
        update_fields.append('station = ?')
        params.append(data['station'])
    if 'status' in data:
        if data['status'] not in ['正常', '故障', '停用']:
            return jsonify({'error': '状态值无效，必须是：正常、故障、停用'}), 400
        update_fields.append('status = ?')
        params.append(data['status'])
    if 'install_date' in data:
        update_fields.append('install_date = ?')
        params.append(data['install_date'])
    if 'manufacturer' in data:
        update_fields.append('manufacturer = ?')
        params.append(data['manufacturer'])
    if 'model' in data:
        update_fields.append('model = ?')
        params.append(data['model'])
    if 'device_serial' in data:
        update_fields.append('device_serial = ?')
        params.append(data['device_serial'])
    if 'production_date' in data:
        update_fields.append('production_date = ?')
        params.append(data['production_date'])
    
    if not update_fields:
        return jsonify({'error': '没有提供要更新的字段'}), 400
    
    update_fields.append('update_time = ?')
    params.append(datetime.now().isoformat())
    params.append(device_id)
    
    cursor.execute(f"UPDATE devices SET {', '.join(update_fields)} WHERE device_id = ?", params)
    db.commit()
    
    return jsonify({'message': '设备更新成功'})

@app.route('/api/workorders', methods=['POST'])
def create_work_order():
    data = request.get_json()
    required_fields = ['device_id', 'fault_type']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'缺少必填字段: {field}'}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM devices WHERE device_id = ?', (data['device_id'],))
    if not cursor.fetchone():
        return jsonify({'error': '设备不存在'}), 404
    
    if data['fault_type'] not in FAULT_TYPES:
        return jsonify({'error': f'故障类型无效，必须是：{", ".join(FAULT_TYPES)}'}), 400
    
    order_id = generate_order_id()
    now = datetime.now()
    fault_hour = now.hour
    period_type = get_period_type(fault_hour)
    report_time = now.isoformat()
    
    cursor.execute('''
        INSERT INTO work_orders (order_id, device_id, fault_type, fault_description, 
                                reporter, contact, status, report_time, fault_hour, period_type)
        VALUES (?, ?, ?, ?, ?, ?, '待处理', ?, ?, ?)
    ''', (
        order_id,
        data['device_id'],
        data['fault_type'],
        data.get('fault_description'),
        data.get('reporter'),
        data.get('contact'),
        report_time,
        fault_hour,
        period_type
    ))
    
    cursor.execute("UPDATE devices SET status = '故障', update_time = ? WHERE device_id = ?", 
                   (report_time, data['device_id']))
    
    db.commit()
    
    return jsonify({
        'message': '工单创建成功',
        'order_id': order_id
    }), 201

@app.route('/api/workorders', methods=['GET'])
def get_work_orders():
    status = request.args.get('status')
    device_id = request.args.get('device_id')
    station = request.args.get('station')
    
    if station:
        query = '''
            SELECT wo.* FROM work_orders wo 
            JOIN devices d ON wo.device_id = d.device_id 
            WHERE 1=1
        '''
        params = []
        
        if status:
            query += ' AND wo.status = ?'
            params.append(status)
        if device_id:
            query += ' AND wo.device_id = ?'
            params.append(device_id)
        if station:
            query += ' AND d.station LIKE ?'
            params.append(f'%{station}%')
        
        query += ' ORDER BY wo.report_time DESC'
    else:
        query = 'SELECT * FROM work_orders WHERE 1=1'
        params = []
        
        if status:
            query += ' AND status = ?'
            params.append(status)
        if device_id:
            query += ' AND device_id = ?'
            params.append(device_id)
        
        query += ' ORDER BY report_time DESC'
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    orders = []
    for row in rows:
        cursor.execute('SELECT station, location, device_name FROM devices WHERE device_id = ?', (row['device_id'],))
        device_info = cursor.fetchone()
        
        orders.append({
            'order_id': row['order_id'],
            'device_id': row['device_id'],
            'device_name': device_info['device_name'] if device_info else None,
            'station': device_info['station'] if device_info else None,
            'location': device_info['location'] if device_info else None,
            'fault_type': row['fault_type'],
            'fault_description': row['fault_description'],
            'reporter': row['reporter'],
            'contact': row['contact'],
            'status': row['status'],
            'report_time': row['report_time'],
            'fault_hour': row['fault_hour'],
            'period_type': row['period_type'],
            'handle_time': row['handle_time'],
            'handle_result': row['handle_result']
        })
    
    return jsonify(orders)

@app.route('/api/workorders/<order_id>', methods=['PUT'])
def handle_work_order(order_id):
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM work_orders WHERE order_id = ?', (order_id,))
    row = cursor.fetchone()
    if not row:
        return jsonify({'error': '工单不存在'}), 404
    
    if 'status' not in data:
        return jsonify({'error': '缺少必填字段: status'}), 400
    
    if data['status'] not in ['处理中', '已完成']:
        return jsonify({'error': '状态值无效，必须是：处理中、已完成'}), 400
    
    now = datetime.now().isoformat()
    
    cursor.execute('''
        UPDATE work_orders 
        SET status = ?, handle_time = ?, handle_result = ?
        WHERE order_id = ?
    ''', (
        data['status'],
        now,
        data.get('handle_result'),
        order_id
    ))
    
    if data['status'] == '已完成':
        cursor.execute("UPDATE devices SET status = '正常', update_time = ? WHERE device_id = ?", 
                       (now, row['device_id']))
    
    db.commit()
    
    return jsonify({'message': '工单处理成功'})

@app.route('/api/fault-types', methods=['GET'])
def get_fault_types():
    return jsonify(FAULT_TYPES)

@app.route('/api/dashboard/stats', methods=['GET'])
def get_stats():
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT COUNT(*) as total FROM devices')
    total_devices = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as count FROM devices WHERE status = '正常'")
    normal_devices = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM devices WHERE status = '故障'")
    fault_devices = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM devices WHERE status = '停用'")
    disabled_devices = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM work_orders WHERE status = '待处理'")
    pending_orders = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM work_orders WHERE status = '处理中'")
    processing_orders = cursor.fetchone()['count']
    
    return jsonify({
        'total_devices': total_devices,
        'normal_devices': normal_devices,
        'fault_devices': fault_devices,
        'disabled_devices': disabled_devices,
        'pending_orders': pending_orders,
        'processing_orders': processing_orders
    })

@app.route('/api/stats/fault-type-frequency', methods=['GET'])
def get_fault_type_frequency():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    db = get_db()
    cursor = db.cursor()
    
    query = '''
        SELECT fault_type, COUNT(*) as count 
        FROM work_orders 
        WHERE 1=1
    '''
    params = []
    
    if start_date:
        query += ' AND report_time >= ?'
        params.append(start_date)
    if end_date:
        query += ' AND report_time <= ?'
        params.append(end_date + 'T23:59:59')
    
    query += ' GROUP BY fault_type ORDER BY count DESC'
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    result = []
    for row in rows:
        result.append({
            'fault_type': row['fault_type'],
            'count': row['count']
        })
    
    return jsonify(result)

@app.route('/api/stats/period-type', methods=['GET'])
def get_period_type_stats():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    db = get_db()
    cursor = db.cursor()
    
    query = '''
        SELECT period_type, COUNT(*) as count 
        FROM work_orders 
        WHERE 1=1
    '''
    params = []
    
    if start_date:
        query += ' AND report_time >= ?'
        params.append(start_date)
    if end_date:
        query += ' AND report_time <= ?'
        params.append(end_date + 'T23:59:59')
    
    query += ' GROUP BY period_type'
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    result = {}
    for row in rows:
        result[row['period_type']] = row['count']
    
    cursor.execute('''
        SELECT fault_hour, COUNT(*) as count 
        FROM work_orders 
        WHERE 1=1
    ''' + (' AND report_time >= ?' if start_date else '') +
        (' AND report_time <= ?' if end_date else '') +
        ' GROUP BY fault_hour ORDER BY fault_hour',
        params
    )
    hour_rows = cursor.fetchall()
    
    hour_distribution = []
    for row in hour_rows:
        hour_distribution.append({
            'hour': row['fault_hour'],
            'count': row['count']
        })
    
    return jsonify({
        'period_stats': result,
        'hour_distribution': hour_distribution
    })

@app.route('/api/stats/device-monthly-rank', methods=['GET'])
def get_device_monthly_rank():
    year = request.args.get('year')
    month = request.args.get('month')
    top_n = request.args.get('top_n', 10, type=int)
    
    if not year or not month:
        now = datetime.now()
        year = now.year
        month = now.month
    
    month_str = f'{year}-{month:02d}'
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('''
        SELECT wo.device_id, d.device_name, d.station, COUNT(*) as fault_count
        FROM work_orders wo
        JOIN devices d ON wo.device_id = d.device_id
        WHERE SUBSTR(wo.report_time, 1, 7) = ?
        GROUP BY wo.device_id
        ORDER BY fault_count DESC
        LIMIT ?
    ''', (month_str, top_n))
    
    rows = cursor.fetchall()
    
    result = []
    rank = 1
    for row in rows:
        result.append({
            'rank': rank,
            'device_id': row['device_id'],
            'device_name': row['device_name'],
            'station': row['station'],
            'fault_count': row['fault_count']
        })
        rank += 1
    
    return jsonify({
        'year': int(year),
        'month': int(month),
        'ranking': result
    })

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
