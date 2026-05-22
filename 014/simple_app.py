from flask import Flask, request, jsonify, g
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)

DATABASE = 'orders.db'

ORDER_STATUSES = [
    '待接单',
    '选料',
    '打浆',
    '抄纸',
    '压榨',
    '烘干',
    '检选',
    '成品完工'
]

PAPER_TYPES = ['棉料', '皮料', '竹料', '混合料']
PAPER_SIZES = ['四尺', '六尺', '八尺', '丈二', '定制']


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


def generate_order_no():
    now = datetime.now()
    date_prefix = now.strftime('%Y%m%d')
    random_num = random.randint(1000, 9999)
    order_no = f'XZ{date_prefix}{random_num}'
    return order_no


@app.route('/api/orders/statuses', methods=['GET'])
def get_statuses():
    return jsonify({
        'success': True,
        'data': ORDER_STATUSES
    })


@app.route('/api/orders/types', methods=['GET'])
def get_paper_types():
    return jsonify({
        'success': True,
        'data': PAPER_TYPES
    })


@app.route('/api/orders/sizes', methods=['GET'])
def get_paper_sizes():
    return jsonify({
        'success': True,
        'data': PAPER_SIZES
    })


@app.route('/api/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        
        required_fields = ['customer_name', 'phone', 'paper_type', 'paper_size', 'quantity']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'缺少必填字段: {field}'}), 400
        
        order_no = generate_order_no()
        now = datetime.now().isoformat()
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            INSERT INTO orders (
                order_no, customer_name, phone, address, paper_type,
                paper_size, quantity, thickness, special_requirements,
                status, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_no,
            data['customer_name'],
            data['phone'],
            data.get('address', ''),
            data['paper_type'],
            data['paper_size'],
            data['quantity'],
            data.get('thickness', ''),
            data.get('special_requirements', ''),
            '待接单',
            now,
            now
        ))
        
        order_id = cursor.lastrowid
        
        cursor.execute('''
            INSERT INTO order_progress (order_id, status, description, operator, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (order_id, '待接单', '客户提交订单，等待接单', '系统', now))
        
        db.commit()
        
        return jsonify({
            'success': True,
            'order_id': order_id,
            'order_no': order_no,
            'message': '订单提交成功'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/orders', methods=['GET'])
def get_orders():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status', '')
        
        db = get_db()
        cursor = db.cursor()
        
        query = 'SELECT * FROM orders'
        params = []
        
        if status:
            query += ' WHERE status = ?'
            params.append(status)
        
        query += ' ORDER BY created_at DESC LIMIT ? OFFSET ?'
        params.extend([per_page, (page - 1) * per_page])
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        orders = []
        for row in rows:
            order = dict(row)
            orders.append(order)
        
        count_query = 'SELECT COUNT(*) as total FROM orders'
        count_params = []
        if status:
            count_query += ' WHERE status = ?'
            count_params.append(status)
        
        cursor.execute(count_query, count_params)
        total = cursor.fetchone()['total']
        
        return jsonify({
            'success': True,
            'data': orders,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': (total + per_page - 1) // per_page
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/orders/<order_no>', methods=['GET'])
def get_order(order_no):
    try:
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        row = cursor.fetchone()
        
        if not row:
            return jsonify({'error': '订单不存在'}), 404
        
        order = dict(row)
        
        cursor.execute('''
            SELECT * FROM order_progress 
            WHERE order_id = ? 
            ORDER BY created_at ASC
        ''', (row['id'],))
        progress_rows = cursor.fetchall()
        
        progress = [dict(p) for p in progress_rows]
        order['progress'] = progress
        
        return jsonify({
            'success': True,
            'data': order
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/orders/<order_no>/status', methods=['PUT'])
def update_order_status(order_no):
    try:
        data = request.get_json()
        new_status = data.get('status')
        description = data.get('description', '')
        operator = data.get('operator', '管理员')
        
        if not new_status:
            return jsonify({'error': '缺少状态参数'}), 400
        
        if new_status not in ORDER_STATUSES:
            return jsonify({'error': '无效的订单状态'}), 400
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('SELECT id, status FROM orders WHERE order_no = ?', (order_no,))
        row = cursor.fetchone()
        
        if not row:
            return jsonify({'error': '订单不存在'}), 404
        
        current_status = row['status']
        order_id = row['id']
        
        if ORDER_STATUSES.index(new_status) < ORDER_STATUSES.index(current_status):
            return jsonify({'error': '不能将订单状态回退到之前的阶段'}), 400
        
        now = datetime.now().isoformat()
        
        cursor.execute('''
            UPDATE orders 
            SET status = ?, updated_at = ?, remark = COALESCE(?, remark)
            WHERE order_no = ?
        ''', (new_status, now, data.get('remark'), order_no))
        
        cursor.execute('''
            INSERT INTO order_progress (order_id, status, description, operator, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (order_id, new_status, description or f'状态变更为: {new_status}', operator, now))
        
        db.commit()
        
        return jsonify({
            'success': True,
            'message': '订单状态更新成功'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    try:
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('SELECT COUNT(*) as total FROM orders')
        total_orders = cursor.fetchone()['total']
        
        status_counts = {}
        for status in ORDER_STATUSES:
            cursor.execute('SELECT COUNT(*) as count FROM orders WHERE status = ?', (status,))
            status_counts[status] = cursor.fetchone()['count']
        
        return jsonify({
            'success': True,
            'data': {
                'total_orders': total_orders,
                'status_counts': status_counts
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print('正在启动宣纸定制订单管理系统...')
    print(f'数据库路径: {os.path.abspath(DATABASE)}')
    app.run(debug=True, use_reloader=False, host='127.0.0.1', port=5000)
