from flask import Flask, request, jsonify, g
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

DATABASE = 'stone_inkstone.db'

ORDER_STATUSES = [
    '待接单',
    '选石',
    '切坯',
    '雕刻',
    '打磨',
    '刻铭',
    '上蜡',
    '完工'
]

STONE_GRADE_PRICE_MULTIPLIER = {
    '特级': 2.0,
    '一级': 1.5,
    '二级': 1.2,
    '三级': 1.0
}

CARVING_DIFFICULTY_MULTIPLIER = {
    '简单': 1.0,
    '普通': 1.3,
    '复杂': 1.8,
    '极复杂': 2.5
}

BASE_PRICE = 500
SIZE_THRESHOLD = 300

def success_response(data=None, message='操作成功', code=200):
    return jsonify({
        'success': True,
        'code': code,
        'message': message,
        'data': data,
        'timestamp': datetime.now().isoformat()
    }), code

def error_response(message='操作失败', code=400, errors=None):
    response = {
        'success': False,
        'code': code,
        'message': message,
        'timestamp': datetime.now().isoformat()
    }
    if errors:
        response['errors'] = errors
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
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_no TEXT UNIQUE NOT NULL,
                customer_name TEXT NOT NULL,
                customer_phone TEXT NOT NULL,
                customer_address TEXT,
                inkstone_type TEXT NOT NULL,
                inkstone_style TEXT,
                material TEXT NOT NULL,
                stone_type TEXT,
                stone_grade TEXT,
                stone_origin TEXT,
                size_length REAL,
                size_width REAL,
                size_height REAL,
                size_note TEXT,
                pool_design TEXT,
                carving_pattern TEXT,
                carving_difficulty TEXT DEFAULT '普通',
                polishing_requirement TEXT,
                inscription TEXT,
                special_requirements TEXT,
                price REAL DEFAULT 0,
                craftsman_name TEXT,
                craftsman_phone TEXT,
                work_days INTEGER DEFAULT 15,
                delivery_date TIMESTAMP,
                status INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()

def generate_order_no():
    now = datetime.now()
    date_prefix = now.strftime('%Y%m%d')
    
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'SELECT order_no FROM orders WHERE order_no LIKE ? ORDER BY order_no DESC LIMIT 1',
            (f'SY{date_prefix}%',)
        )
        result = cursor.fetchone()
        
        if result:
            last_no = result[0]
            last_seq = int(last_no[-4:])
            new_seq = last_seq + 1
        else:
            new_seq = 1
        
        return f'SY{date_prefix}{new_seq:04d}'

def calculate_price(stone_grade, carving_difficulty, size_length, size_width, size_height):
    base_price = BASE_PRICE
    
    grade_multiplier = STONE_GRADE_PRICE_MULTIPLIER.get(stone_grade, 1.0)
    difficulty_multiplier = CARVING_DIFFICULTY_MULTIPLIER.get(carving_difficulty, 1.0)
    
    size_area = (size_length or 0) * (size_width or 0)
    size_multiplier = 1.0
    if size_area > SIZE_THRESHOLD:
        size_multiplier = 1.0 + (size_area - SIZE_THRESHOLD) / SIZE_THRESHOLD * 0.5
    
    final_price = base_price * grade_multiplier * difficulty_multiplier * size_multiplier
    return round(final_price, 2)

def validate_order_data(data, is_create=True):
    errors = []
    
    required_fields = ['customer_name', 'customer_phone', 'inkstone_type', 'material']
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f'{field} 为必填项')
    
    if 'customer_phone' in data and data['customer_phone']:
        phone = data['customer_phone']
        if not (len(phone) == 11 and phone.isdigit()):
            errors.append('手机号码格式不正确，应为11位数字')
    
    size_fields = ['size_length', 'size_width', 'size_height']
    for field in size_fields:
        if field in data and data[field] is not None:
            try:
                val = float(data[field])
                if val <= 0 or val > 100:
                    errors.append(f'{field} 应在 0-100 cm 范围内')
            except (ValueError, TypeError):
                errors.append(f'{field} 必须为有效数字')
    
    if 'stone_grade' in data and data['stone_grade']:
        if data['stone_grade'] not in STONE_GRADE_PRICE_MULTIPLIER:
            valid_grades = ', '.join(STONE_GRADE_PRICE_MULTIPLIER.keys())
            errors.append(f'石材品级无效，有效值为: {valid_grades}')
    
    if 'carving_difficulty' in data and data['carving_difficulty']:
        if data['carving_difficulty'] not in CARVING_DIFFICULTY_MULTIPLIER:
            valid_difficulties = ', '.join(CARVING_DIFFICULTY_MULTIPLIER.keys())
            errors.append(f'雕刻难度无效，有效值为: {valid_difficulties}')
    
    if 'work_days' in data and data['work_days'] is not None:
        try:
            days = int(data['work_days'])
            if days <= 0 or days > 180:
                errors.append('工期应在 1-180 天范围内')
        except (ValueError, TypeError):
            errors.append('工期必须为有效整数')
    
    return errors

@app.route('/api/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        
        errors = validate_order_data(data)
        if errors:
            return error_response('数据验证失败', 400, errors)
        
        order_no = generate_order_no()
        
        stone_grade = data.get('stone_grade', '三级')
        carving_difficulty = data.get('carving_difficulty', '普通')
        size_length = data.get('size_length')
        size_width = data.get('size_width')
        size_height = data.get('size_height')
        
        price = calculate_price(stone_grade, carving_difficulty, size_length, size_width, size_height)
        
        work_days = data.get('work_days', 15)
        delivery_date = (datetime.now() + timedelta(days=int(work_days))).strftime('%Y-%m-%d %H:%M:%S')
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO orders (
                order_no, customer_name, customer_phone, customer_address,
                inkstone_type, inkstone_style, material, stone_type, stone_grade, stone_origin,
                size_length, size_width, size_height, size_note,
                pool_design, carving_pattern, carving_difficulty, polishing_requirement,
                inscription, special_requirements,
                price, craftsman_name, craftsman_phone, work_days, delivery_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_no,
            data['customer_name'],
            data['customer_phone'],
            data.get('customer_address', ''),
            data['inkstone_type'],
            data.get('inkstone_style', ''),
            data['material'],
            data.get('stone_type', ''),
            stone_grade,
            data.get('stone_origin', ''),
            size_length,
            size_width,
            size_height,
            data.get('size_note', ''),
            data.get('pool_design', ''),
            data.get('carving_pattern', ''),
            carving_difficulty,
            data.get('polishing_requirement', ''),
            data.get('inscription', ''),
            data.get('special_requirements', ''),
            price,
            data.get('craftsman_name', ''),
            data.get('craftsman_phone', ''),
            work_days,
            delivery_date
        ))
        db.commit()
        
        order_id = cursor.lastrowid
        cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
        order = cursor.fetchone()
        
        return success_response({
            'id': order['id'],
            'order_no': order['order_no'],
            'customer_name': order['customer_name'],
            'customer_phone': order['customer_phone'],
            'inkstone_type': order['inkstone_type'],
            'inkstone_style': order['inkstone_style'],
            'material': order['material'],
            'stone_type': order['stone_type'],
            'stone_grade': order['stone_grade'],
            'stone_origin': order['stone_origin'],
            'size_length': order['size_length'],
            'size_width': order['size_width'],
            'size_height': order['size_height'],
            'carving_difficulty': order['carving_difficulty'],
            'price': order['price'],
            'work_days': order['work_days'],
            'delivery_date': order['delivery_date'],
            'status': ORDER_STATUSES[order['status']],
            'status_code': order['status'],
            'created_at': order['created_at']
        }, '订单创建成功', 201)
        
    except Exception as e:
        return error_response(f'创建订单失败: {str(e)}', 500)

@app.route('/api/orders', methods=['GET'])
def get_orders():
    try:
        status_filter = request.args.get('status', type=int)
        inkstone_style = request.args.get('inkstone_style', '')
        delivery_date_from = request.args.get('delivery_date_from', '')
        delivery_date_to = request.args.get('delivery_date_to', '')
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        
        valid_sort_fields = ['created_at', 'delivery_date', 'price', 'status']
        if sort_by not in valid_sort_fields:
            sort_by = 'created_at'
        if sort_order not in ['asc', 'desc']:
            sort_order = 'desc'
        
        offset = (page - 1) * per_page
        
        db = get_db()
        cursor = db.cursor()
        
        query = 'SELECT * FROM orders WHERE 1=1'
        params = []
        
        if status_filter is not None and 0 <= status_filter < len(ORDER_STATUSES):
            query += ' AND status = ?'
            params.append(status_filter)
        
        if inkstone_style:
            query += ' AND inkstone_style LIKE ?'
            params.append(f'%{inkstone_style}%')
        
        if delivery_date_from:
            query += ' AND DATE(delivery_date) >= DATE(?)'
            params.append(delivery_date_from)
        
        if delivery_date_to:
            query += ' AND DATE(delivery_date) <= DATE(?)'
            params.append(delivery_date_to)
        
        query += f' ORDER BY {sort_by} {sort_order.upper()} LIMIT ? OFFSET ?'
        params.extend([per_page, offset])
        
        cursor.execute(query, params)
        orders = cursor.fetchall()
        
        count_query = 'SELECT COUNT(*) as total FROM orders WHERE 1=1'
        count_params = []
        
        if status_filter is not None and 0 <= status_filter < len(ORDER_STATUSES):
            count_query += ' AND status = ?'
            count_params.append(status_filter)
        
        if inkstone_style:
            count_query += ' AND inkstone_style LIKE ?'
            count_params.append(f'%{inkstone_style}%')
        
        if delivery_date_from:
            count_query += ' AND DATE(delivery_date) >= DATE(?)'
            count_params.append(delivery_date_from)
        
        if delivery_date_to:
            count_query += ' AND DATE(delivery_date) <= DATE(?)'
            count_params.append(delivery_date_to)
        
        cursor.execute(count_query, count_params)
        total = cursor.fetchone()['total']
        
        result = []
        for order in orders:
            result.append({
                'id': order['id'],
                'order_no': order['order_no'],
                'customer_name': order['customer_name'],
                'customer_phone': order['customer_phone'],
                'customer_address': order['customer_address'],
                'inkstone_type': order['inkstone_type'],
                'inkstone_style': order['inkstone_style'],
                'material': order['material'],
                'stone_type': order['stone_type'],
                'stone_grade': order['stone_grade'],
                'stone_origin': order['stone_origin'],
                'size_length': order['size_length'],
                'size_width': order['size_width'],
                'size_height': order['size_height'],
                'size_note': order['size_note'],
                'pool_design': order['pool_design'],
                'carving_pattern': order['carving_pattern'],
                'carving_difficulty': order['carving_difficulty'],
                'polishing_requirement': order['polishing_requirement'],
                'inscription': order['inscription'],
                'special_requirements': order['special_requirements'],
                'price': order['price'],
                'craftsman_name': order['craftsman_name'],
                'craftsman_phone': order['craftsman_phone'],
                'work_days': order['work_days'],
                'delivery_date': order['delivery_date'],
                'status': ORDER_STATUSES[order['status']],
                'status_code': order['status'],
                'created_at': order['created_at'],
                'updated_at': order['updated_at']
            })
        
        return success_response({
            'orders': result,
            'pagination': {
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': (total + per_page - 1) // per_page,
                'sort_by': sort_by,
                'sort_order': sort_order
            }
        }, '查询成功')
        
    except Exception as e:
        return error_response(f'查询订单失败: {str(e)}', 500)

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
            'id': order['id'],
            'order_no': order['order_no'],
            'customer_name': order['customer_name'],
            'customer_phone': order['customer_phone'],
            'customer_address': order['customer_address'],
            'inkstone_type': order['inkstone_type'],
            'inkstone_style': order['inkstone_style'],
            'material': order['material'],
            'stone_type': order['stone_type'],
            'stone_grade': order['stone_grade'],
            'stone_origin': order['stone_origin'],
            'size_length': order['size_length'],
            'size_width': order['size_width'],
            'size_height': order['size_height'],
            'size_note': order['size_note'],
            'pool_design': order['pool_design'],
            'carving_pattern': order['carving_pattern'],
            'carving_difficulty': order['carving_difficulty'],
            'polishing_requirement': order['polishing_requirement'],
            'inscription': order['inscription'],
            'special_requirements': order['special_requirements'],
            'price': order['price'],
            'craftsman_name': order['craftsman_name'],
            'craftsman_phone': order['craftsman_phone'],
            'work_days': order['work_days'],
            'delivery_date': order['delivery_date'],
            'status': ORDER_STATUSES[order['status']],
            'status_code': order['status'],
            'created_at': order['created_at'],
            'updated_at': order['updated_at']
        }, '查询成功')
        
    except Exception as e:
        return error_response(f'查询订单失败: {str(e)}', 500)

@app.route('/api/orders/<order_no>/status', methods=['PUT'])
def update_order_status(order_no):
    try:
        data = request.get_json()
        status_code = data.get('status')
        
        if status_code is None or not isinstance(status_code, int):
            return error_response('请提供有效的状态码', 400)
        
        if status_code < 0 or status_code >= len(ORDER_STATUSES):
            return error_response(f'状态码必须在 0 到 {len(ORDER_STATUSES) - 1} 之间', 400)
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        order = cursor.fetchone()
        
        if not order:
            return error_response('订单不存在', 404)
        
        cursor.execute('''
            UPDATE orders SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE order_no = ?
        ''', (status_code, order_no))
        db.commit()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        updated_order = cursor.fetchone()
        
        return success_response({
            'order_no': updated_order['order_no'],
            'status': ORDER_STATUSES[updated_order['status']],
            'status_code': updated_order['status'],
            'updated_at': updated_order['updated_at']
        }, '状态更新成功')
        
    except Exception as e:
        return error_response(f'更新状态失败: {str(e)}', 500)

@app.route('/api/orders/<order_no>/craftsman', methods=['PUT'])
def update_craftsman(order_no):
    try:
        data = request.get_json()
        
        craftsman_name = data.get('craftsman_name', '')
        craftsman_phone = data.get('craftsman_phone', '')
        work_days = data.get('work_days')
        
        errors = []
        if craftsman_phone and not (len(craftsman_phone) == 11 and craftsman_phone.isdigit()):
            errors.append('匠人手机号码格式不正确')
        if work_days is not None:
            try:
                days = int(work_days)
                if days <= 0 or days > 180:
                    errors.append('工期应在 1-180 天范围内')
            except (ValueError, TypeError):
                errors.append('工期必须为有效整数')
        
        if errors:
            return error_response('数据验证失败', 400, errors)
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        order = cursor.fetchone()
        
        if not order:
            return error_response('订单不存在', 404)
        
        updates = []
        params = []
        
        if craftsman_name is not None:
            updates.append('craftsman_name = ?')
            params.append(craftsman_name)
        if craftsman_phone is not None:
            updates.append('craftsman_phone = ?')
            params.append(craftsman_phone)
        if work_days is not None:
            updates.append('work_days = ?')
            params.append(int(work_days))
            new_delivery = (datetime.now() + timedelta(days=int(work_days))).strftime('%Y-%m-%d %H:%M:%S')
            updates.append('delivery_date = ?')
            params.append(new_delivery)
        
        updates.append('updated_at = CURRENT_TIMESTAMP')
        
        params.append(order_no)
        
        cursor.execute(f'''
            UPDATE orders SET {', '.join(updates)} WHERE order_no = ?
        ''', params)
        db.commit()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        updated_order = cursor.fetchone()
        
        return success_response({
            'order_no': updated_order['order_no'],
            'craftsman_name': updated_order['craftsman_name'],
            'craftsman_phone': updated_order['craftsman_phone'],
            'work_days': updated_order['work_days'],
            'delivery_date': updated_order['delivery_date'],
            'updated_at': updated_order['updated_at']
        }, '匠人信息更新成功')
        
    except Exception as e:
        return error_response(f'更新匠人信息失败: {str(e)}', 500)

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
        
        return success_response({'order_no': order_no}, '订单删除成功')
        
    except Exception as e:
        return error_response(f'删除订单失败: {str(e)}', 500)

@app.route('/api/statuses', methods=['GET'])
def get_statuses():
    return success_response({
        'statuses': [
            {'code': i, 'name': status}
            for i, status in enumerate(ORDER_STATUSES)
        ]
    }, '查询成功')

@app.route('/api/config/prices', methods=['GET'])
def get_price_config():
    return success_response({
        'base_price': BASE_PRICE,
        'size_threshold': SIZE_THRESHOLD,
        'stone_grade_multipliers': STONE_GRADE_PRICE_MULTIPLIER,
        'carving_difficulty_multipliers': CARVING_DIFFICULTY_MULTIPLIER
    }, '查询成功')

@app.route('/api/calculate-price', methods=['POST'])
def calculate_price_api():
    try:
        data = request.get_json()
        
        stone_grade = data.get('stone_grade', '三级')
        carving_difficulty = data.get('carving_difficulty', '普通')
        size_length = data.get('size_length', 0)
        size_width = data.get('size_width', 0)
        size_height = data.get('size_height', 0)
        
        price = calculate_price(stone_grade, carving_difficulty, size_length, size_width, size_height)
        
        return success_response({
            'base_price': BASE_PRICE,
            'stone_grade': stone_grade,
            'stone_grade_multiplier': STONE_GRADE_PRICE_MULTIPLIER.get(stone_grade, 1.0),
            'carving_difficulty': carving_difficulty,
            'carving_difficulty_multiplier': CARVING_DIFFICULTY_MULTIPLIER.get(carving_difficulty, 1.0),
            'size_length': size_length,
            'size_width': size_width,
            'size_height': size_height,
            'final_price': price
        }, '价格计算成功')
        
    except Exception as e:
        return error_response(f'计算价格失败: {str(e)}', 500)

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
        print('数据库初始化完成')
    app.run(debug=True, host='0.0.0.0', port=5000)
