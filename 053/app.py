from flask import Flask, request, jsonify, g
from flask_cors import CORS
import sqlite3
import datetime
import os
import re

app = Flask(__name__)
CORS(app)

DATABASE = 'orders.db'

ORDER_STATUSES = [
    '待接单',
    '选料',
    '开坯',
    '挖膛',
    '雕花',
    '打磨',
    '上蜡',
    '完工'
]

PATTERN_STYLES = ['传统', '简约', '繁复', '现代', '复古']
PATTERN_TYPES = ['浮雕', '透雕', '阴刻', '圆雕']

WOOD_PRICE_MAP = {
    '紫檀木': 800,
    '黄花梨': 1200,
    '楠木': 300,
    '红木': 500,
    '鸡翅木': 200,
    '酸枝木': 600,
    '乌木': 400,
    '榉木': 150
}

CARVING_DIFFICULTY_MAP = {
    '简约': 1.0,
    '传统': 1.3,
    '繁复': 1.8,
    '现代': 1.2,
    '复古': 1.5
}

WORK_DAY_MAP = {
    '待接单': 0,
    '选料': 1,
    '开坯': 2,
    '挖膛': 3,
    '雕花': 5,
    '打磨': 2,
    '上蜡': 1,
    '完工': 0
}

def success_response(data=None, message='操作成功', code=200):
    response = {
        'success': True,
        'message': message,
        'code': code
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), code

def error_response(message='操作失败', code=400, errors=None):
    response = {
        'success': False,
        'message': message,
        'code': code
    }
    if errors is not None:
        response['errors'] = errors
    return jsonify(response), code

def validate_phone(phone):
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, phone))

def validate_positive_number(value, field_name):
    try:
        num = float(value)
        if num <= 0:
            return False, f'{field_name}必须大于0'
        if num > 100:
            return False, f'{field_name}不能超过100厘米'
        return True, None
    except (ValueError, TypeError):
        return False, f'{field_name}必须是有效的数字'

def validate_required(data, required_fields):
    errors = {}
    for field in required_fields:
        if field not in data or data[field] is None or str(data[field]).strip() == '':
            errors[field] = f'{field}为必填项'
    return errors

def validate_order_data(data, is_create=True):
    errors = {}
    
    required_fields = [
        'customer_name', 'customer_phone', 'wood_type', 'box_size', 'pattern',
        'outer_length', 'outer_width', 'outer_height',
        'inner_length', 'inner_width', 'inner_depth',
        'wall_thickness', 'lid_height'
    ] if is_create else []
    
    required_errors = validate_required(data, required_fields)
    errors.update(required_errors)
    
    if 'customer_phone' in data and data['customer_phone']:
        if not validate_phone(data['customer_phone']):
            errors['customer_phone'] = '请输入有效的手机号码'
    
    numeric_fields = [
        'outer_length', 'outer_width', 'outer_height',
        'inner_length', 'inner_width', 'inner_depth',
        'wall_thickness', 'lid_height'
    ]
    
    for field in numeric_fields:
        if field in data and data[field] is not None:
            is_valid, msg = validate_positive_number(data[field], field)
            if not is_valid:
                errors[field] = msg
    
    if 'pattern_style' in data and data['pattern_style']:
        if data['pattern_style'] not in PATTERN_STYLES:
            errors['pattern_style'] = f'图案风格必须是以下之一: {", ".join(PATTERN_STYLES)}'
    
    if 'pattern_type' in data and data['pattern_type']:
        if data['pattern_type'] not in PATTERN_TYPES:
            errors['pattern_type'] = f'图案类型必须是以下之一: {", ".join(PATTERN_TYPES)}'
    
    return errors

def calculate_price(wood_type, pattern_style, volume):
    wood_base_price = WOOD_PRICE_MAP.get(wood_type, 200)
    difficulty_multiplier = CARVING_DIFFICULTY_MAP.get(pattern_style, 1.0)
    base_price = wood_base_price * volume * difficulty_multiplier
    return round(base_price, 2)

def calculate_volume(outer_length, outer_width, outer_height):
    return outer_length * outer_width * outer_height / 1000

def calculate_delivery_date(start_date, total_days):
    return (start_date + datetime.timedelta(days=total_days)).strftime('%Y-%m-%d')

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
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS craftsmen (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                skill_level TEXT,
                specialty TEXT,
                status TEXT DEFAULT '空闲',
                created_at TEXT NOT NULL
            )
        ''')
        
        cursor.execute("PRAGMA table_info(orders)")
        columns = [col[1] for col in cursor.fetchall()]
        
        new_columns = [
            ('wood_origin', 'TEXT'),
            ('wood_grade', 'TEXT'),
            ('wood_density', 'TEXT'),
            ('outer_length', 'REAL NOT NULL DEFAULT 0'),
            ('outer_width', 'REAL NOT NULL DEFAULT 0'),
            ('outer_height', 'REAL NOT NULL DEFAULT 0'),
            ('inner_length', 'REAL NOT NULL DEFAULT 0'),
            ('inner_width', 'REAL NOT NULL DEFAULT 0'),
            ('inner_depth', 'REAL NOT NULL DEFAULT 0'),
            ('wall_thickness', 'REAL NOT NULL DEFAULT 0'),
            ('lid_height', 'REAL NOT NULL DEFAULT 0'),
            ('pattern_type', 'TEXT'),
            ('pattern_position', 'TEXT'),
            ('pattern_style', 'TEXT'),
            ('pattern_detail', 'TEXT'),
            ('price', 'REAL DEFAULT 0'),
            ('craftsman_id', 'INTEGER'),
            ('craftsman_name', 'TEXT'),
            ('estimated_days', 'INTEGER DEFAULT 0'),
            ('delivery_date', 'TEXT'),
            ('start_date', 'TEXT')
        ]
        
        for col_name, col_type in new_columns:
            if col_name not in columns:
                cursor.execute(f'ALTER TABLE orders ADD COLUMN {col_name} {col_type}')
        
        db.commit()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_no TEXT UNIQUE NOT NULL,
                customer_name TEXT NOT NULL,
                customer_phone TEXT NOT NULL,
                customer_address TEXT,
                wood_type TEXT NOT NULL,
                wood_origin TEXT,
                wood_grade TEXT,
                wood_density TEXT,
                box_size TEXT NOT NULL,
                outer_length REAL NOT NULL,
                outer_width REAL NOT NULL,
                outer_height REAL NOT NULL,
                inner_length REAL NOT NULL,
                inner_width REAL NOT NULL,
                inner_depth REAL NOT NULL,
                wall_thickness REAL NOT NULL,
                lid_height REAL NOT NULL,
                pattern TEXT NOT NULL,
                pattern_type TEXT,
                pattern_position TEXT,
                pattern_style TEXT,
                pattern_detail TEXT,
                description TEXT,
                price REAL DEFAULT 0,
                craftsman_id INTEGER,
                craftsman_name TEXT,
                estimated_days INTEGER DEFAULT 0,
                delivery_date TEXT,
                start_date TEXT,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS craftsmen (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                skill_level TEXT,
                specialty TEXT,
                status TEXT DEFAULT '空闲',
                created_at TEXT NOT NULL
            )
        ''')
        
        db.commit()
        migrate_db()

def generate_order_no():
    now = datetime.datetime.now()
    date_str = now.strftime('%Y%m%d')
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT order_no FROM orders WHERE order_no LIKE ? ORDER BY order_no DESC LIMIT 1', (f'{date_str}%',))
    last_order = cursor.fetchone()
    
    if last_order:
        last_no = int(last_order['order_no'][-4:])
        new_no = last_no + 1
    else:
        new_no = 1
    
    return f'{date_str}{new_no:04d}'

def order_to_dict(order):
    return {
        'id': order['id'],
        'order_no': order['order_no'],
        'customer_name': order['customer_name'],
        'customer_phone': order['customer_phone'],
        'customer_address': order['customer_address'],
        'wood_type': order['wood_type'],
        'wood_origin': order['wood_origin'],
        'wood_grade': order['wood_grade'],
        'wood_density': order['wood_density'],
        'box_size': order['box_size'],
        'outer_length': order['outer_length'],
        'outer_width': order['outer_width'],
        'outer_height': order['outer_height'],
        'inner_length': order['inner_length'],
        'inner_width': order['inner_width'],
        'inner_depth': order['inner_depth'],
        'wall_thickness': order['wall_thickness'],
        'lid_height': order['lid_height'],
        'pattern': order['pattern'],
        'pattern_type': order['pattern_type'],
        'pattern_position': order['pattern_position'],
        'pattern_style': order['pattern_style'],
        'pattern_detail': order['pattern_detail'],
        'description': order['description'],
        'price': order['price'],
        'craftsman_id': order['craftsman_id'],
        'craftsman_name': order['craftsman_name'],
        'estimated_days': order['estimated_days'],
        'delivery_date': order['delivery_date'],
        'start_date': order['start_date'],
        'status': order['status'],
        'created_at': order['created_at'],
        'updated_at': order['updated_at']
    }

def craftsman_to_dict(craftsman):
    return {
        'id': craftsman['id'],
        'name': craftsman['name'],
        'phone': craftsman['phone'],
        'skill_level': craftsman['skill_level'],
        'specialty': craftsman['specialty'],
        'status': craftsman['status'],
        'created_at': craftsman['created_at']
    }

@app.route('/api/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        
        errors = validate_order_data(data, is_create=True)
        if errors:
            return error_response('数据验证失败', 400, errors)
        
        db = get_db()
        order_no = generate_order_no()
        now = datetime.datetime.now()
        now_str = now.isoformat()
        
        volume = calculate_volume(
            float(data['outer_length']),
            float(data['outer_width']),
            float(data['outer_height'])
        )
        price = calculate_price(
            data['wood_type'],
            data.get('pattern_style', '传统'),
            volume
        )
        
        estimated_days = sum(WORK_DAY_MAP.values())
        delivery_date = calculate_delivery_date(now, estimated_days)
        
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO orders (
                order_no, customer_name, customer_phone, customer_address,
                wood_type, wood_origin, wood_grade, wood_density,
                box_size, outer_length, outer_width, outer_height,
                inner_length, inner_width, inner_depth, wall_thickness, lid_height,
                pattern, pattern_type, pattern_position, pattern_style, pattern_detail,
                description, price, estimated_days, delivery_date,
                status, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_no,
            data['customer_name'],
            data['customer_phone'],
            data.get('customer_address', ''),
            data['wood_type'],
            data.get('wood_origin', ''),
            data.get('wood_grade', ''),
            data.get('wood_density', ''),
            data['box_size'],
            float(data['outer_length']),
            float(data['outer_width']),
            float(data['outer_height']),
            float(data['inner_length']),
            float(data['inner_width']),
            float(data['inner_depth']),
            float(data['wall_thickness']),
            float(data['lid_height']),
            data['pattern'],
            data.get('pattern_type', ''),
            data.get('pattern_position', ''),
            data.get('pattern_style', '传统'),
            data.get('pattern_detail', ''),
            data.get('description', ''),
            price,
            estimated_days,
            delivery_date,
            ORDER_STATUSES[0],
            now_str,
            now_str
        ))
        db.commit()
        
        cursor.execute('SELECT * FROM orders WHERE id = ?', (cursor.lastrowid,))
        order = cursor.fetchone()
        
        return success_response({
            'order': order_to_dict(order)
        }, '订单创建成功', 201)
        
    except Exception as e:
        return error_response(str(e), 500)

@app.route('/api/orders', methods=['GET'])
def get_orders():
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        status = request.args.get('status')
        pattern_style = request.args.get('pattern_style')
        delivery_date_start = request.args.get('delivery_date_start')
        delivery_date_end = request.args.get('delivery_date_end')
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'DESC')
        
        valid_sort_fields = ['created_at', 'price', 'delivery_date', 'order_no']
        if sort_by not in valid_sort_fields:
            sort_by = 'created_at'
        if sort_order.upper() not in ['ASC', 'DESC']:
            sort_order = 'DESC'
        
        db = get_db()
        cursor = db.cursor()
        
        where_clauses = []
        params = []
        
        if status and status in ORDER_STATUSES:
            where_clauses.append('status = ?')
            params.append(status)
        
        if pattern_style and pattern_style in PATTERN_STYLES:
            where_clauses.append('pattern_style = ?')
            params.append(pattern_style)
        
        if delivery_date_start:
            where_clauses.append('delivery_date >= ?')
            params.append(delivery_date_start)
        
        if delivery_date_end:
            where_clauses.append('delivery_date <= ?')
            params.append(delivery_date_end)
        
        where_sql = ' AND '.join(where_clauses) if where_clauses else '1=1'
        
        count_sql = f'SELECT COUNT(*) as total FROM orders WHERE {where_sql}'
        cursor.execute(count_sql, params)
        total = cursor.fetchone()['total']
        
        offset = (page - 1) * page_size
        query_sql = f'''
            SELECT * FROM orders WHERE {where_sql}
            ORDER BY {sort_by} {sort_order}
            LIMIT ? OFFSET ?
        '''
        params.extend([page_size, offset])
        cursor.execute(query_sql, params)
        orders = cursor.fetchall()
        
        return success_response({
            'orders': [order_to_dict(order) for order in orders],
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total': total,
                'total_pages': (total + page_size - 1) // page_size
            }
        }, '获取订单列表成功')
        
    except Exception as e:
        return error_response(str(e), 500)

@app.route('/api/orders/<order_no>', methods=['GET'])
def get_order(order_no):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        order = cursor.fetchone()
        
        if not order:
            return error_response('订单不存在', 404)
        
        return success_response({
            'order': order_to_dict(order)
        }, '获取订单详情成功')
        
    except Exception as e:
        return error_response(str(e), 500)

@app.route('/api/orders/<order_no>', methods=['PUT'])
def update_order(order_no):
    try:
        data = request.get_json()
        
        errors = validate_order_data(data, is_create=False)
        if errors:
            return error_response('数据验证失败', 400, errors)
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        order = cursor.fetchone()
        
        if not order:
            return error_response('订单不存在', 404)
        
        update_fields = []
        update_values = []
        
        fields_map = {
            'customer_name': 'customer_name',
            'customer_phone': 'customer_phone',
            'customer_address': 'customer_address',
            'wood_type': 'wood_type',
            'wood_origin': 'wood_origin',
            'wood_grade': 'wood_grade',
            'wood_density': 'wood_density',
            'box_size': 'box_size',
            'outer_length': 'outer_length',
            'outer_width': 'outer_width',
            'outer_height': 'outer_height',
            'inner_length': 'inner_length',
            'inner_width': 'inner_width',
            'inner_depth': 'inner_depth',
            'wall_thickness': 'wall_thickness',
            'lid_height': 'lid_height',
            'pattern': 'pattern',
            'pattern_type': 'pattern_type',
            'pattern_position': 'pattern_position',
            'pattern_style': 'pattern_style',
            'pattern_detail': 'pattern_detail',
            'description': 'description'
        }
        
        for json_key, db_col in fields_map.items():
            if json_key in data:
                update_fields.append(f'{db_col} = ?')
                update_values.append(data[json_key])
        
        if any(f in ['wood_type', 'pattern_style', 'outer_length', 'outer_width', 'outer_height'] for f in data):
            wood_type = data.get('wood_type', order['wood_type'])
            pattern_style = data.get('pattern_style', order['pattern_style'])
            outer_length = float(data.get('outer_length', order['outer_length']))
            outer_width = float(data.get('outer_width', order['outer_width']))
            outer_height = float(data.get('outer_height', order['outer_height']))
            
            volume = calculate_volume(outer_length, outer_width, outer_height)
            new_price = calculate_price(wood_type, pattern_style, volume)
            
            update_fields.append('price = ?')
            update_values.append(new_price)
        
        if update_fields:
            now = datetime.datetime.now().isoformat()
            update_fields.append('updated_at = ?')
            update_values.append(now)
            update_values.append(order_no)
            
            cursor.execute(f'''
                UPDATE orders SET {', '.join(update_fields)} WHERE order_no = ?
            ''', update_values)
            db.commit()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        updated_order = cursor.fetchone()
        
        return success_response({
            'order': order_to_dict(updated_order)
        }, '订单更新成功')
        
    except Exception as e:
        return error_response(str(e), 500)

@app.route('/api/orders/<order_no>/status', methods=['PUT'])
def update_order_status(order_no):
    try:
        data = request.get_json()
        
        if 'status' not in data:
            return error_response('缺少 status 字段', 400)
        
        if data['status'] not in ORDER_STATUSES:
            return error_response('无效的订单状态', 400, {
                'valid_statuses': ORDER_STATUSES
            })
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        order = cursor.fetchone()
        
        if not order:
            return error_response('订单不存在', 404)
        
        now = datetime.datetime.now().isoformat()
        start_date = order['start_date']
        
        if data['status'] == '选料' and not start_date:
            start_date = datetime.datetime.now().strftime('%Y-%m-%d')
            cursor.execute('UPDATE orders SET start_date = ? WHERE order_no = ?', (start_date, order_no))
        
        cursor.execute('''
            UPDATE orders SET status = ?, updated_at = ? WHERE order_no = ?
        ''', (data['status'], now, order_no))
        db.commit()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        updated_order = cursor.fetchone()
        
        return success_response({
            'order': order_to_dict(updated_order)
        }, '订单状态更新成功')
        
    except Exception as e:
        return error_response(str(e), 500)

@app.route('/api/orders/<order_no>/assign', methods=['PUT'])
def assign_craftsman(order_no):
    try:
        data = request.get_json()
        
        if 'craftsman_id' not in data:
            return error_response('缺少 craftsman_id 字段', 400)
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('SELECT * FROM craftsmen WHERE id = ?', (data['craftsman_id'],))
        craftsman = cursor.fetchone()
        
        if not craftsman:
            return error_response('匠人不存在', 404)
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        order = cursor.fetchone()
        
        if not order:
            return error_response('订单不存在', 404)
        
        now = datetime.datetime.now().isoformat()
        cursor.execute('''
            UPDATE orders SET craftsman_id = ?, craftsman_name = ?, updated_at = ?
            WHERE order_no = ?
        ''', (data['craftsman_id'], craftsman['name'], now, order_no))
        db.commit()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        updated_order = cursor.fetchone()
        
        return success_response({
            'order': order_to_dict(updated_order)
        }, '匠人分配成功')
        
    except Exception as e:
        return error_response(str(e), 500)

@app.route('/api/orders/<order_no>', methods=['DELETE'])
def delete_order(order_no):
    try:
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        order = cursor.fetchone()
        
        if not order:
            return error_response('订单不存在', 404)
        
        cursor.execute('DELETE FROM orders WHERE order_no = ?', (order_no,))
        db.commit()
        
        return success_response(None, '订单删除成功')
        
    except Exception as e:
        return error_response(str(e), 500)

@app.route('/api/craftsmen', methods=['POST'])
def create_craftsman():
    try:
        data = request.get_json()
        
        if 'name' not in data or not data['name']:
            return error_response('匠人为必填项', 400)
        
        db = get_db()
        now = datetime.datetime.now().isoformat()
        
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO craftsmen (name, phone, skill_level, specialty, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data.get('phone', ''),
            data.get('skill_level', ''),
            data.get('specialty', ''),
            data.get('status', '空闲'),
            now
        ))
        db.commit()
        
        cursor.execute('SELECT * FROM craftsmen WHERE id = ?', (cursor.lastrowid,))
        craftsman = cursor.fetchone()
        
        return success_response({
            'craftsman': craftsman_to_dict(craftsman)
        }, '匠人创建成功', 201)
        
    except Exception as e:
        return error_response(str(e), 500)

@app.route('/api/craftsmen', methods=['GET'])
def get_craftsmen():
    try:
        status = request.args.get('status')
        db = get_db()
        cursor = db.cursor()
        
        if status:
            cursor.execute('SELECT * FROM craftsmen WHERE status = ? ORDER BY created_at DESC', (status,))
        else:
            cursor.execute('SELECT * FROM craftsmen ORDER BY created_at DESC')
        
        craftsmen = cursor.fetchall()
        
        return success_response({
            'craftsmen': [craftsman_to_dict(c) for c in craftsmen]
        }, '获取匠人列表成功')
        
    except Exception as e:
        return error_response(str(e), 500)

@app.route('/api/craftsmen/<int:craftsman_id>', methods=['PUT'])
def update_craftsman(craftsman_id):
    try:
        data = request.get_json()
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('SELECT * FROM craftsmen WHERE id = ?', (craftsman_id,))
        craftsman = cursor.fetchone()
        
        if not craftsman:
            return error_response('匠人不存在', 404)
        
        update_fields = []
        update_values = []
        
        for field in ['name', 'phone', 'skill_level', 'specialty', 'status']:
            if field in data:
                update_fields.append(f'{field} = ?')
                update_values.append(data[field])
        
        if update_fields:
            update_values.append(craftsman_id)
            cursor.execute(f'''
                UPDATE craftsmen SET {', '.join(update_fields)} WHERE id = ?
            ''', update_values)
            db.commit()
        
        cursor.execute('SELECT * FROM craftsmen WHERE id = ?', (craftsman_id,))
        updated_craftsman = cursor.fetchone()
        
        return success_response({
            'craftsman': craftsman_to_dict(updated_craftsman)
        }, '匠人更新成功')
        
    except Exception as e:
        return error_response(str(e), 500)

@app.route('/api/craftsmen/<int:craftsman_id>', methods=['DELETE'])
def delete_craftsman(craftsman_id):
    try:
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('SELECT * FROM craftsmen WHERE id = ?', (craftsman_id,))
        craftsman = cursor.fetchone()
        
        if not craftsman:
            return error_response('匠人不存在', 404)
        
        cursor.execute('DELETE FROM craftsmen WHERE id = ?', (craftsman_id,))
        db.commit()
        
        return success_response(None, '匠人删除成功')
        
    except Exception as e:
        return error_response(str(e), 500)

@app.route('/api/statuses', methods=['GET'])
def get_statuses():
    return success_response({
        'order_statuses': ORDER_STATUSES,
        'pattern_styles': PATTERN_STYLES,
        'pattern_types': PATTERN_TYPES
    }, '获取状态列表成功')

@app.route('/api/price/calculate', methods=['POST'])
def calculate_order_price():
    try:
        data = request.get_json()
        
        required_fields = ['wood_type', 'outer_length', 'outer_width', 'outer_height']
        errors = validate_required(data, required_fields)
        if errors:
            return error_response('数据验证失败', 400, errors)
        
        volume = calculate_volume(
            float(data['outer_length']),
            float(data['outer_width']),
            float(data['outer_height'])
        )
        price = calculate_price(
            data['wood_type'],
            data.get('pattern_style', '传统'),
            volume
        )
        
        return success_response({
            'price': price,
            'volume': volume,
            'wood_base_price': WOOD_PRICE_MAP.get(data['wood_type'], 200),
            'difficulty_multiplier': CARVING_DIFFICULTY_MAP.get(data.get('pattern_style', '传统'), 1.0)
        }, '价格计算成功')
        
    except Exception as e:
        return error_response(str(e), 500)

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    try:
        db = get_db()
        cursor = db.cursor()
        
        stats = {}
        for status in ORDER_STATUSES:
            cursor.execute('SELECT COUNT(*) as count FROM orders WHERE status = ?', (status,))
            result = cursor.fetchone()
            stats[status] = result['count']
        
        cursor.execute('SELECT COUNT(*) as total FROM orders')
        total = cursor.fetchone()
        
        cursor.execute('SELECT COUNT(*) as count FROM craftsmen WHERE status = ?', ('空闲',))
        available_craftsmen = cursor.fetchone()
        
        cursor.execute('SELECT COUNT(*) as total FROM craftsmen')
        total_craftsmen = cursor.fetchone()
        
        cursor.execute('SELECT SUM(price) as total_price FROM orders')
        total_price_result = cursor.fetchone()
        
        return success_response({
            'orders': {
                'total': total['total'],
                'by_status': stats
            },
            'craftsmen': {
                'total': total_craftsmen['total'],
                'available': available_craftsmen['count']
            },
            'revenue': {
                'total': round(total_price_result['total_price'] or 0, 2)
            }
        }, '获取统计数据成功')
        
    except Exception as e:
        return error_response(str(e), 500)

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
        print('数据库初始化完成')
    else:
        with app.app_context():
            migrate_db()
            print('数据库迁移完成')
    app.run(debug=True, host='0.0.0.0', port=5000)
