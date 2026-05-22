from flask import Flask, request, jsonify, g
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATABASE = 'pos_maintenance.db'

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
                location TEXT NOT NULL,
                status TEXT DEFAULT '正常',
                install_date TEXT,
                last_maintenance_date TEXT,
                remark TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS work_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_no TEXT UNIQUE NOT NULL,
                device_id INTEGER NOT NULL,
                fault_description TEXT NOT NULL,
                reporter TEXT,
                reporter_phone TEXT,
                status TEXT DEFAULT '待处理',
                handle_user TEXT,
                handle_content TEXT,
                handle_time TEXT,
                report_time TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS maintenance_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER NOT NULL,
                work_order_id INTEGER,
                maintenance_type TEXT NOT NULL,
                content TEXT NOT NULL,
                operator TEXT NOT NULL,
                maintenance_time TEXT DEFAULT CURRENT_TIMESTAMP,
                remark TEXT,
                FOREIGN KEY (device_id) REFERENCES devices (id),
                FOREIGN KEY (work_order_id) REFERENCES work_orders (id)
            )
        ''')
        
        db.commit()

def generate_order_no():
    now = datetime.now()
    prefix = now.strftime('WO%Y%m%d')
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT order_no FROM work_orders WHERE order_no LIKE ? ORDER BY order_no DESC LIMIT 1', (prefix + '%',))
        result = cursor.fetchone()
        if result:
            last_no = result['order_no']
            seq = int(last_no[-4:]) + 1
        else:
            seq = 1
        return f'{prefix}{seq:04d}'

@app.route('/api/devices', methods=['POST'])
def add_device():
    data = request.json
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO devices (device_code, device_name, location, install_date, remark)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data['device_code'],
            data['device_name'],
            data['location'],
            data.get('install_date', ''),
            data.get('remark', '')
        ))
        db.commit()
        return jsonify({'code': 200, 'message': '设备添加成功', 'id': cursor.lastrowid})
    except sqlite3.IntegrityError:
        return jsonify({'code': 400, 'message': '设备编号已存在'}), 400
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/devices', methods=['GET'])
def get_devices():
    status = request.args.get('status')
    keyword = request.args.get('keyword')
    
    query = 'SELECT * FROM devices WHERE 1=1'
    params = []
    
    if status:
        query += ' AND status = ?'
        params.append(status)
    if keyword:
        query += ' AND (device_code LIKE ? OR device_name LIKE ? OR location LIKE ?)'
        params.extend([f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'])
    
    query += ' ORDER BY created_at DESC'
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query, params)
    devices = [dict(row) for row in cursor.fetchall()]
    return jsonify({'code': 200, 'data': devices})

@app.route('/api/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM devices WHERE id = ?', (device_id,))
    device = cursor.fetchone()
    if device:
        return jsonify({'code': 200, 'data': dict(device)})
    return jsonify({'code': 404, 'message': '设备不存在'}), 404

@app.route('/api/devices/<int:device_id>/status', methods=['PUT'])
def update_device_status(device_id):
    data = request.json
    new_status = data.get('status')
    
    if new_status not in ['正常', '故障', '维修中', '已修复']:
        return jsonify({'code': 400, 'message': '无效的状态值'}), 400
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM devices WHERE id = ?', (device_id,))
    if not cursor.fetchone():
        return jsonify({'code': 404, 'message': '设备不存在'}), 404
    
    cursor.execute('''
        UPDATE devices SET status = ?, last_maintenance_date = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (new_status, device_id))
    db.commit()
    return jsonify({'code': 200, 'message': '状态更新成功'})

@app.route('/api/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM devices WHERE id = ?', (device_id,))
    if not cursor.fetchone():
        return jsonify({'code': 404, 'message': '设备不存在'}), 404
    
    cursor.execute('DELETE FROM devices WHERE id = ?', (device_id,))
    db.commit()
    return jsonify({'code': 200, 'message': '设备删除成功'})

@app.route('/api/work-orders', methods=['POST'])
def create_work_order():
    data = request.json
    try:
        db = get_db()
        cursor = db.cursor()
        
        order_no = generate_order_no()
        
        cursor.execute('''
            INSERT INTO work_orders (order_no, device_id, fault_description, reporter, reporter_phone)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            order_no,
            data['device_id'],
            data['fault_description'],
            data.get('reporter', ''),
            data.get('reporter_phone', '')
        ))
        
        cursor.execute('''
            UPDATE devices SET status = '故障' WHERE id = ?
        ''', (data['device_id'],))
        
        db.commit()
        return jsonify({'code': 200, 'message': '工单创建成功', 'order_no': order_no})
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/work-orders', methods=['GET'])
def get_work_orders():
    status = request.args.get('status')
    device_id = request.args.get('device_id')
    
    query = '''
        SELECT wo.*, d.device_code, d.device_name, d.location 
        FROM work_orders wo 
        LEFT JOIN devices d ON wo.device_id = d.id 
        WHERE 1=1
    '''
    params = []
    
    if status:
        query += ' AND wo.status = ?'
        params.append(status)
    if device_id:
        query += ' AND wo.device_id = ?'
        params.append(device_id)
    
    query += ' ORDER BY wo.report_time DESC'
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query, params)
    orders = [dict(row) for row in cursor.fetchall()]
    return jsonify({'code': 200, 'data': orders})

@app.route('/api/work-orders/<order_no>/handle', methods=['PUT'])
def handle_work_order(order_no):
    data = request.json
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM work_orders WHERE order_no = ?', (order_no,))
    order = cursor.fetchone()
    if not order:
        return jsonify({'code': 404, 'message': '工单不存在'}), 404
    
    new_status = data.get('status', '处理中')
    
    if new_status not in ['待处理', '处理中', '已完成']:
        return jsonify({'code': 400, 'message': '无效的工单状态值'}), 400
    
    cursor.execute('''
        UPDATE work_orders 
        SET status = ?, handle_user = ?, handle_content = ?, handle_time = CURRENT_TIMESTAMP
        WHERE order_no = ?
    ''', (
        new_status,
        data.get('handle_user', ''),
        data.get('handle_content', ''),
        order_no
    ))
    
    if new_status == '已完成':
        cursor.execute('''
            UPDATE devices SET status = '已修复' WHERE id = ?
        ''', (order['device_id'],))
        
        cursor.execute('''
            INSERT INTO maintenance_records (device_id, work_order_id, maintenance_type, content, operator)
            VALUES (?, ?, '故障维修', ?, ?)
        ''', (
            order['device_id'],
            order['id'],
            data.get('handle_content', ''),
            data.get('handle_user', '')
        ))
    elif new_status == '处理中':
        cursor.execute('''
            UPDATE devices SET status = '维修中' WHERE id = ?
        ''', (order['device_id'],))
    
    db.commit()
    return jsonify({'code': 200, 'message': '工单处理成功'})

@app.route('/api/maintenance-records', methods=['GET'])
def get_maintenance_records():
    device_id = request.args.get('device_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = '''
        SELECT mr.*, d.device_code, d.device_name, wo.order_no 
        FROM maintenance_records mr 
        LEFT JOIN devices d ON mr.device_id = d.id 
        LEFT JOIN work_orders wo ON mr.work_order_id = wo.id 
        WHERE 1=1
    '''
    params = []
    
    if device_id:
        query += ' AND mr.device_id = ?'
        params.append(device_id)
    if start_date:
        query += ' AND mr.maintenance_time >= ?'
        params.append(start_date)
    if end_date:
        query += ' AND mr.maintenance_time <= ?'
        params.append(end_date)
    
    query += ' ORDER BY mr.maintenance_time DESC'
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query, params)
    records = [dict(row) for row in cursor.fetchall()]
    return jsonify({'code': 200, 'data': records})

@app.route('/api/maintenance-records', methods=['POST'])
def add_maintenance_record():
    data = request.json
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO maintenance_records (device_id, work_order_id, maintenance_type, content, operator, remark)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['device_id'],
            data.get('work_order_id'),
            data['maintenance_type'],
            data['content'],
            data['operator'],
            data.get('remark', '')
        ))
        
        cursor.execute('''
            UPDATE devices SET last_maintenance_date = CURRENT_TIMESTAMP WHERE id = ?
        ''', (data['device_id'],))
        
        db.commit()
        return jsonify({'code': 200, 'message': '运维记录添加成功', 'id': cursor.lastrowid})
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
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
    
    cursor.execute('SELECT COUNT(*) as pending FROM work_orders WHERE status = "待处理"')
    pending_orders = cursor.fetchone()['pending']
    
    return jsonify({
        'code': 200,
        'data': {
            'total_devices': total_devices,
            'normal_devices': normal_devices,
            'fault_devices': fault_devices,
            'repairing_devices': repairing_devices,
            'pending_orders': pending_orders
        }
    })

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)