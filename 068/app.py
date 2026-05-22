from flask import Flask, request, jsonify, g
import sqlite3
import os
from datetime import datetime
import random
import string

app = Flask(__name__)
app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), 'orders.db')

ORDER_STATUSES = [
    '待接单',
    '选椰壳',
    '开坯',
    '粗磨',
    '浮雕',
    '精修',
    '抛光',
    '完工'
]

COCONUT_SPECIFICATIONS = [
    '小椰壳(直径5-7cm)',
    '中椰壳(直径7-9cm)',
    '大椰壳(直径9-12cm)',
    '特大椰壳(直径12cm以上)',
    '老椰壳(壁厚3-5mm)',
    '嫩椰壳(壁厚1-2mm)',
    '天然原色',
    '碳化处理'
]

SHAPE_TYPES = [
    '圆形',
    '椭圆形',
    '方形',
    '长方形',
    '不规则形',
    '随形',
    '葫芦形',
    '平安扣形'
]

CARVING_PATTERNS = [
    '龙凤呈祥',
    '山水风景',
    '花鸟虫鱼',
    '人物肖像',
    '吉祥文字',
    '几何图案',
    '图腾纹样',
    '佛教题材',
    '道教题材',
    '生肖图案',
    '梅兰竹菊',
    '松鹤延年',
    '自定义图案'
]

SURFACE_TREATMENTS = [
    '原色打磨',
    '上清漆',
    '上木蜡油',
    '烫蜡工艺',
    '碳化处理',
    '做旧处理',
    '光面抛光',
    '磨砂质感',
    '纹理保留'
]


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


def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_no TEXT UNIQUE NOT NULL,
                customer_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                design_requirements TEXT NOT NULL,
                coconut_specification TEXT,
                shape_type TEXT,
                outer_dimensions TEXT,
                carving_pattern TEXT,
                surface_treatment TEXT,
                size TEXT,
                material_preference TEXT,
                blank_spec TEXT,
                carving_depth TEXT,
                polishing_grade TEXT,
                status TEXT NOT NULL DEFAULT '待接单',
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL,
                remark TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS status_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                operator TEXT,
                remark TEXT,
                created_at TIMESTAMP NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders (id)
            )
        ''')
        
        db.commit()


def generate_order_no():
    date_str = datetime.now().strftime('%Y%m%d')
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f'YKD{date_str}{random_str}'


def dict_from_row(row):
    if row is None:
        return None
    return {key: row[key] for key in row.keys()}


@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    required_fields = ['customer_name', 'phone', 'design_requirements']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'缺少必填字段: {field}'}), 400
    
    order_no = generate_order_no()
    now = datetime.now().isoformat()
    
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO orders (
                order_no, customer_name, phone, design_requirements,
                coconut_specification, shape_type, outer_dimensions,
                carving_pattern, surface_treatment, size, material_preference,
                blank_spec, carving_depth, polishing_grade,
                status, created_at, updated_at, remark
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_no,
            data['customer_name'],
            data['phone'],
            data['design_requirements'],
            data.get('coconut_specification', ''),
            data.get('shape_type', ''),
            data.get('outer_dimensions', ''),
            data.get('carving_pattern', ''),
            data.get('surface_treatment', ''),
            data.get('size', ''),
            data.get('material_preference', ''),
            data.get('blank_spec', ''),
            data.get('carving_depth', ''),
            data.get('polishing_grade', ''),
            '待接单',
            now,
            now,
            data.get('remark', '')
        ))
        
        order_id = cursor.lastrowid
        
        cursor.execute('''
            INSERT INTO status_logs (order_id, status, created_at)
            VALUES (?, ?, ?)
        ''', (order_id, '待接单', now))
        
        db.commit()
        
        cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
        order = dict_from_row(cursor.fetchone())
        
        return jsonify({
            'message': '订单创建成功',
            'order': order
        }), 201
        
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/orders', methods=['GET'])
def get_orders():
    status = request.args.get('status')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    
    offset = (page - 1) * per_page
    
    db = get_db()
    cursor = db.cursor()
    
    where_clause = ''
    params = []
    
    if status:
        if status not in ORDER_STATUSES:
            return jsonify({'error': '无效的订单状态'}), 400
        where_clause = 'WHERE status = ?'
        params.append(status)
    
    cursor.execute(f'''
        SELECT * FROM orders {where_clause}
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
    ''', params + [per_page, offset])
    
    orders = [dict_from_row(row) for row in cursor.fetchall()]
    
    cursor.execute(f'SELECT COUNT(*) as total FROM orders {where_clause}', params)
    total = cursor.fetchone()['total']
    
    return jsonify({
        'orders': orders,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': (total + per_page - 1) // per_page
        }
    })


@app.route('/api/orders/<order_no>', methods=['GET'])
def get_order(order_no):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
    order = dict_from_row(cursor.fetchone())
    
    if not order:
        return jsonify({'error': '订单不存在'}), 404
    
    cursor.execute('''
        SELECT * FROM status_logs
        WHERE order_id = ?
        ORDER BY created_at ASC
    ''', (order['id'],))
    
    status_logs = [dict_from_row(row) for row in cursor.fetchall()]
    
    return jsonify({
        'order': order,
        'status_logs': status_logs
    })


@app.route('/api/orders/<order_no>/status', methods=['PUT'])
def update_order_status(order_no):
    data = request.get_json()
    
    if not data or 'status' not in data:
        return jsonify({'error': '缺少status字段'}), 400
    
    new_status = data['status']
    if new_status not in ORDER_STATUSES:
        return jsonify({'error': '无效的订单状态'}), 400
    
    operator = data.get('operator', '管理员')
    remark = data.get('remark', '')
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
    order = dict_from_row(cursor.fetchone())
    
    if not order:
        return jsonify({'error': '订单不存在'}), 404
    
    if order['status'] == new_status:
        return jsonify({'message': '状态未变化', 'order': order}), 200
    
    now = datetime.now().isoformat()
    
    try:
        cursor.execute('''
            UPDATE orders
            SET status = ?, updated_at = ?
            WHERE order_no = ?
        ''', (new_status, now, order_no))
        
        cursor.execute('''
            INSERT INTO status_logs (order_id, status, operator, remark, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (order['id'], new_status, operator, remark, now))
        
        db.commit()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        updated_order = dict_from_row(cursor.fetchone())
        
        return jsonify({
            'message': '状态更新成功',
            'order': updated_order
        })
        
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/orders/<order_no>', methods=['PUT'])
def update_order(order_no):
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
    order = dict_from_row(cursor.fetchone())
    
    if not order:
        return jsonify({'error': '订单不存在'}), 404
    
    update_fields = []
    update_values = []
    
    allowed_fields = [
        'customer_name', 'phone', 'design_requirements',
        'coconut_specification', 'shape_type', 'outer_dimensions',
        'carving_pattern', 'surface_treatment', 'size', 'material_preference',
        'blank_spec', 'carving_depth', 'polishing_grade', 'remark'
    ]
    for field in allowed_fields:
        if field in data:
            update_fields.append(f'{field} = ?')
            update_values.append(data[field])
    
    if not update_fields:
        return jsonify({'error': '没有可更新的字段'}), 400
    
    now = datetime.now().isoformat()
    update_fields.append('updated_at = ?')
    update_values.append(now)
    update_values.append(order_no)
    
    try:
        cursor.execute(f'''
            UPDATE orders
            SET {', '.join(update_fields)}
            WHERE order_no = ?
        ''', update_values)
        
        db.commit()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        updated_order = dict_from_row(cursor.fetchone())
        
        return jsonify({
            'message': '订单更新成功',
            'order': updated_order
        })
        
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/orders/<order_no>', methods=['DELETE'])
def delete_order(order_no):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT id FROM orders WHERE order_no = ?', (order_no,))
    order = cursor.fetchone()
    
    if not order:
        return jsonify({'error': '订单不存在'}), 404
    
    try:
        cursor.execute('DELETE FROM status_logs WHERE order_id = ?', (order['id'],))
        cursor.execute('DELETE FROM orders WHERE order_no = ?', (order_no,))
        db.commit()
        
        return jsonify({'message': '订单删除成功'})
        
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/statuses', methods=['GET'])
def get_statuses():
    return jsonify({
        'statuses': ORDER_STATUSES
    })


@app.route('/api/specifications', methods=['GET'])
def get_specifications():
    return jsonify({
        'coconut_specifications': COCONUT_SPECIFICATIONS,
        'shape_types': SHAPE_TYPES,
        'carving_patterns': CARVING_PATTERNS,
        'surface_treatments': SURFACE_TREATMENTS,
        'order_statuses': ORDER_STATUSES
    })


@app.route('/api/stats', methods=['GET'])
def get_stats():
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('''
        SELECT status, COUNT(*) as count
        FROM orders
        GROUP BY status
    ''')
    
    stats = {row['status']: row['count'] for row in cursor.fetchall()}
    
    for status in ORDER_STATUSES:
        if status not in stats:
            stats[status] = 0
    
    cursor.execute('SELECT COUNT(*) as total FROM orders')
    total = cursor.fetchone()['total']
    
    return jsonify({
        'total': total,
        'by_status': stats
    })


@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': '传统椰壳雕手把件定制订单管理系统',
        'version': '2.0.0',
        'endpoints': {
            'POST /api/orders': '创建订单',
            'GET /api/orders': '获取订单列表',
            'GET /api/orders/<order_no>': '获取订单详情',
            'PUT /api/orders/<order_no>': '更新订单信息',
            'PUT /api/orders/<order_no>/status': '更新订单状态',
            'DELETE /api/orders/<order_no>': '删除订单',
            'GET /api/statuses': '获取所有订单状态',
            'GET /api/specifications': '获取所有规格选项',
            'GET /api/stats': '获取统计信息'
        }
    })


if __name__ == '__main__':
    init_db()
    print('数据库初始化完成')
    app.run(debug=True, host='0.0.0.0', port=5000)
