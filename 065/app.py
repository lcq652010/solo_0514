from flask import Flask, request, jsonify, g
from flask_cors import CORS
import sqlite3
import datetime
import os

app = Flask(__name__)
CORS(app)

DATABASE = 'orders.db'

ORDER_STATUSES = [
    '待接单',
    '选麦秆',
    '漂白',
    '压平',
    '裁剪',
    '拼贴',
    '裱封',
    '完工'
]

WHEAT_STRAW_CATEGORIES = [
    '白麦秆',
    '红麦秆',
    '黑麦秆',
    '紫麦秆',
    '黄麦秆',
    '混合麦秆'
]

BOOKMARK_SIZES = [
    '小型 (50x120mm)',
    '中型 (60x150mm)',
    '大型 (70x180mm)',
    '特大型 (80x200mm)',
    '异形定制'
]

PATTERN_TYPES = [
    '梅兰竹菊',
    '山水风景',
    '花鸟虫鱼',
    '龙凤呈祥',
    '吉祥文字',
    '几何图案',
    '人物肖像',
    '动物卡通',
    '客户定制'
]

MOUNTING_TYPES = [
    'PVC塑封',
    '冷裱膜',
    '热裱膜',
    '亚克力封装',
    '丝绸装裱',
    '木质边框',
    '金属边框'
]

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

def migrate_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute("PRAGMA table_info(orders)")
        columns = [col[1] for col in cursor.fetchall()]
        
        new_columns = ['wheat_straw_category', 'bookmark_size', 'pattern_type', 'mounting_type']
        
        for col in new_columns:
            if col not in columns:
                cursor.execute(f'ALTER TABLE orders ADD COLUMN {col} TEXT')
                print(f'已添加字段: {col}')
        
        db.commit()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY,
                customer_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                design_description TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                deadline DATE,
                status TEXT NOT NULL,
                wheat_straw_category TEXT,
                bookmark_size TEXT,
                pattern_type TEXT,
                mounting_type TEXT,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL,
                remark TEXT
            )
        ''')
        db.commit()

def generate_order_id():
    now = datetime.datetime.now()
    date_prefix = now.strftime('%Y%m%d')
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id FROM orders WHERE id LIKE ? ORDER BY id DESC LIMIT 1', (f'{date_prefix}%',))
    last_order = cursor.fetchone()
    if last_order:
        last_num = int(last_order['id'][-4:])
        new_num = last_num + 1
    else:
        new_num = 1
    return f'{date_prefix}{new_num:04d}'

def validate_enum_field(value, valid_values, field_name):
    if value and value not in valid_values:
        return False, f'{field_name}无效，有效值为: {valid_values}'
    return True, ''

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    required_fields = ['customer_name', 'phone', 'design_description', 'quantity']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'缺少必填字段: {field}'}), 400
    
    valid, msg = validate_enum_field(data.get('wheat_straw_category'), WHEAT_STRAW_CATEGORIES, '麦秆品类')
    if not valid:
        return jsonify({'error': msg}), 400
    
    valid, msg = validate_enum_field(data.get('bookmark_size'), BOOKMARK_SIZES, '书签规格')
    if not valid:
        return jsonify({'error': msg}), 400
    
    valid, msg = validate_enum_field(data.get('pattern_type'), PATTERN_TYPES, '贴画纹样')
    if not valid:
        return jsonify({'error': msg}), 400
    
    valid, msg = validate_enum_field(data.get('mounting_type'), MOUNTING_TYPES, '裱封类型')
    if not valid:
        return jsonify({'error': msg}), 400
    
    db = get_db()
    order_id = generate_order_id()
    now = datetime.datetime.now().isoformat()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO orders (
            id, customer_name, phone, email, design_description,
            quantity, deadline, status, wheat_straw_category, bookmark_size,
            pattern_type, mounting_type, created_at, updated_at, remark
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        order_id,
        data['customer_name'],
        data['phone'],
        data.get('email', ''),
        data['design_description'],
        data['quantity'],
        data.get('deadline', ''),
        ORDER_STATUSES[0],
        data.get('wheat_straw_category', ''),
        data.get('bookmark_size', ''),
        data.get('pattern_type', ''),
        data.get('mounting_type', ''),
        now,
        now,
        data.get('remark', '')
    ))
    db.commit()
    return jsonify({'order_id': order_id, 'message': '订单创建成功'}), 201

@app.route('/api/orders', methods=['GET'])
def get_orders():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM orders ORDER BY created_at DESC')
    orders = cursor.fetchall()
    result = []
    for order in orders:
        result.append({
            'id': order['id'],
            'customer_name': order['customer_name'],
            'phone': order['phone'],
            'email': order['email'],
            'design_description': order['design_description'],
            'quantity': order['quantity'],
            'deadline': order['deadline'],
            'status': order['status'],
            'wheat_straw_category': order['wheat_straw_category'],
            'bookmark_size': order['bookmark_size'],
            'pattern_type': order['pattern_type'],
            'mounting_type': order['mounting_type'],
            'created_at': order['created_at'],
            'updated_at': order['updated_at'],
            'remark': order['remark']
        })
    return jsonify(result)

@app.route('/api/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
    order = cursor.fetchone()
    if not order:
        return jsonify({'error': '订单不存在'}), 404
    return jsonify({
        'id': order['id'],
        'customer_name': order['customer_name'],
        'phone': order['phone'],
        'email': order['email'],
        'design_description': order['design_description'],
        'quantity': order['quantity'],
        'deadline': order['deadline'],
        'status': order['status'],
        'wheat_straw_category': order['wheat_straw_category'],
        'bookmark_size': order['bookmark_size'],
        'pattern_type': order['pattern_type'],
        'mounting_type': order['mounting_type'],
        'created_at': order['created_at'],
        'updated_at': order['updated_at'],
        'remark': order['remark']
    })

@app.route('/api/orders/<order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    data = request.get_json()
    if 'status' not in data:
        return jsonify({'error': '缺少 status 字段'}), 400
    if data['status'] not in ORDER_STATUSES:
        return jsonify({'error': f'无效的状态值，有效状态为: {ORDER_STATUSES}'}), 400
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id FROM orders WHERE id = ?', (order_id,))
    if not cursor.fetchone():
        return jsonify({'error': '订单不存在'}), 404
    now = datetime.datetime.now().isoformat()
    cursor.execute('''
        UPDATE orders SET status = ?, updated_at = ? WHERE id = ?
    ''', (data['status'], now, order_id))
    db.commit()
    return jsonify({'message': '订单状态更新成功'})

@app.route('/api/orders/<order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id FROM orders WHERE id = ?', (order_id,))
    if not cursor.fetchone():
        return jsonify({'error': '订单不存在'}), 404
    
    valid, msg = validate_enum_field(data.get('wheat_straw_category'), WHEAT_STRAW_CATEGORIES, '麦秆品类')
    if not valid:
        return jsonify({'error': msg}), 400
    
    valid, msg = validate_enum_field(data.get('bookmark_size'), BOOKMARK_SIZES, '书签规格')
    if not valid:
        return jsonify({'error': msg}), 400
    
    valid, msg = validate_enum_field(data.get('pattern_type'), PATTERN_TYPES, '贴画纹样')
    if not valid:
        return jsonify({'error': msg}), 400
    
    valid, msg = validate_enum_field(data.get('mounting_type'), MOUNTING_TYPES, '裱封类型')
    if not valid:
        return jsonify({'error': msg}), 400
    
    update_fields = []
    update_values = []
    allowed_fields = [
        'customer_name', 'phone', 'email', 'design_description', 
        'quantity', 'deadline', 'remark',
        'wheat_straw_category', 'bookmark_size', 'pattern_type', 'mounting_type'
    ]
    for field in allowed_fields:
        if field in data:
            update_fields.append(f'{field} = ?')
            update_values.append(data[field])
    if not update_fields:
        return jsonify({'error': '没有提供要更新的字段'}), 400
    now = datetime.datetime.now().isoformat()
    update_fields.append('updated_at = ?')
    update_values.append(now)
    update_values.append(order_id)
    cursor.execute(f'''
        UPDATE orders SET {', '.join(update_fields)} WHERE id = ?
    ''', update_values)
    db.commit()
    return jsonify({'message': '订单更新成功'})

@app.route('/api/orders/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id FROM orders WHERE id = ?', (order_id,))
    if not cursor.fetchone():
        return jsonify({'error': '订单不存在'}), 404
    cursor.execute('DELETE FROM orders WHERE id = ?', (order_id,))
    db.commit()
    return jsonify({'message': '订单删除成功'})

@app.route('/api/statuses', methods=['GET'])
def get_statuses():
    return jsonify(ORDER_STATUSES)

@app.route('/api/enums', methods=['GET'])
def get_all_enums():
    return jsonify({
        'order_statuses': ORDER_STATUSES,
        'wheat_straw_categories': WHEAT_STRAW_CATEGORIES,
        'bookmark_sizes': BOOKMARK_SIZES,
        'pattern_types': PATTERN_TYPES,
        'mounting_types': MOUNTING_TYPES
    })

@app.route('/api/enums/wheat-straw-categories', methods=['GET'])
def get_wheat_straw_categories():
    return jsonify(WHEAT_STRAW_CATEGORIES)

@app.route('/api/enums/bookmark-sizes', methods=['GET'])
def get_bookmark_sizes():
    return jsonify(BOOKMARK_SIZES)

@app.route('/api/enums/pattern-types', methods=['GET'])
def get_pattern_types():
    return jsonify(PATTERN_TYPES)

@app.route('/api/enums/mounting-types', methods=['GET'])
def get_mounting_types():
    return jsonify(MOUNTING_TYPES)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': '麦秆贴画书签定制订单管理系统 API',
        'version': '2.0',
        'endpoints': {
            'POST /api/orders': '创建订单',
            'GET /api/orders': '获取所有订单',
            'GET /api/orders/<id>': '获取单个订单',
            'PUT /api/orders/<id>/status': '更新订单状态',
            'PUT /api/orders/<id>': '更新订单信息',
            'DELETE /api/orders/<id>': '删除订单',
            'GET /api/statuses': '获取所有订单状态',
            'GET /api/enums': '获取所有枚举值',
            'GET /api/enums/wheat-straw-categories': '获取麦秆品类',
            'GET /api/enums/bookmark-sizes': '获取书签规格',
            'GET /api/enums/pattern-types': '获取贴画纹样',
            'GET /api/enums/mounting-types': '获取裱封类型'
        },
        'business_fields': {
            'wheat_straw_category': '麦秆品类 - 选麦秆、漂白工序依据',
            'bookmark_size': '书签规格 - 裁剪工序依据',
            'pattern_type': '贴画纹样 - 拼贴工序依据',
            'mounting_type': '裱封类型 - 裱封工序依据'
        }
    })

if __name__ == '__main__':
    init_db()
    migrate_db()
    print('数据库初始化完成')
    print('=' * 60)
    print('订单状态:', ORDER_STATUSES)
    print('麦秆品类:', WHEAT_STRAW_CATEGORIES)
    print('书签规格:', BOOKMARK_SIZES)
    print('贴画纹样:', PATTERN_TYPES)
    print('裱封类型:', MOUNTING_TYPES)
    print('=' * 60)
    print('服务器运行在 http://127.0.0.1:5000')
    app.run(debug=True, host='0.0.0.0', port=5000)
