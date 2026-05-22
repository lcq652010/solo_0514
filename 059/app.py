from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime, timedelta
import os
import re

app = Flask(__name__)
CORS(app)

DATABASE = 'orders.db'

ORDER_STATUSES = [
    '待接单',
    '制胎',
    '刮灰',
    '上漆',
    '莳绘',
    '打磨',
    '推光',
    '完工'
]

BODY_MATERIALS = {
    '樟木': 1.0,
    '楠木': 1.2,
    '榉木': 1.0,
    '黑檀木': 2.0,
    '紫檀木': 2.5,
    '花梨木': 1.8,
    '樱桃木': 1.1,
    '胡桃木': 1.3,
    '椴木': 0.9,
    '桦木': 0.95
}

SIZE_SPECS = [
    '8cm', '10cm', '12cm', '14cm', '16cm', '18cm', '20cm',
    '圆形-12cm', '圆形-15cm', '方形-10cm', '方形-12cm',
    '椭圆形-12x8cm', '椭圆形-15x10cm', '花瓣形-12cm', '荷叶形-15cm'
]

LACQUER_PROCESSES = {
    '单色大漆': 1.0,
    '推光漆': 1.2,
    '罩漆': 1.3,
    '描金': 1.5,
    '螺钿镶嵌': 2.0,
    '蛋壳镶嵌': 1.8,
    '变涂': 1.6,
    '犀皮漆': 2.2,
    '雕漆': 2.5,
    '堆漆': 1.7,
    '平漆': 1.0,
    '晕金': 1.4
}

DECORATIVE_PATTERNS = {
    '山水图案': 1.8,
    '花鸟图案': 1.5,
    '龙凤图案': 2.0,
    '云纹图案': 1.2,
    '回纹图案': 1.1,
    '梅兰竹菊': 1.6,
    '松鹤延年': 1.7,
    '富贵牡丹': 1.5,
    '荷花莲花': 1.4,
    '书法文字': 1.3,
    '几何纹样': 1.0,
    '缠枝花卉': 1.4,
    '祥云瑞气': 1.3,
    '简约素面': 1.0
}

BASE_PRICE = 200

def success_response(data=None, message='操作成功'):
    return jsonify({
        'code': 200,
        'success': True,
        'message': message,
        'data': data
    }), 200

def error_response(message='操作失败', code=400, data=None):
    return jsonify({
        'code': code,
        'success': False,
        'message': message,
        'data': data
    }), code

def validate_phone(phone):
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, phone))

def validate_quantity(quantity):
    return isinstance(quantity, int) and quantity > 0 and quantity <= 100

def calculate_price(body_material, lacquer_process, decorative_pattern, quantity):
    material_coeff = BODY_MATERIALS.get(body_material, 1.0)
    process_coeff = LACQUER_PROCESSES.get(lacquer_process, 1.0)
    pattern_coeff = DECORATIVE_PATTERNS.get(decorative_pattern, 1.0) if decorative_pattern else 1.0
    
    unit_price = BASE_PRICE * material_coeff * process_coeff * pattern_coeff
    total_price = round(unit_price * quantity, 2)
    
    return {
        'base_price': BASE_PRICE,
        'material_coeff': material_coeff,
        'process_coeff': process_coeff,
        'pattern_coeff': pattern_coeff,
        'unit_price': round(unit_price, 2),
        'quantity': quantity,
        'total_price': total_price
    }

def validate_order_data(data, is_create=True):
    errors = []
    
    if is_create:
        required_fields = ['customer_name', 'customer_phone', 'teacup_style', 
                           'body_material', 'size_spec', 'lacquer_process', 'lacquer_color']
        
        for field in required_fields:
            if field not in data or not str(data[field]).strip():
                errors.append(f'字段 {field} 为必填项')
    
    if 'customer_phone' in data and not validate_phone(data['customer_phone']):
        errors.append('手机号格式不正确，请输入11位有效手机号')
    
    if 'quantity' in data:
        if not validate_quantity(data['quantity']):
            errors.append('数量必须为1-100之间的整数')
    
    if 'body_material' in data and data['body_material'] not in BODY_MATERIALS:
        errors.append(f'无效的胎体材质，可选值: {list(BODY_MATERIALS.keys())}')
    
    if 'size_spec' in data and data['size_spec'] not in SIZE_SPECS:
        errors.append(f'无效的尺寸规格，可选值: {SIZE_SPECS}')
    
    if 'lacquer_process' in data and data['lacquer_process'] not in LACQUER_PROCESSES:
        errors.append(f'无效的漆面工艺，可选值: {list(LACQUER_PROCESSES.keys())}')
    
    if 'decorative_pattern' in data and data['decorative_pattern']:
        if data['decorative_pattern'] not in DECORATIVE_PATTERNS:
            errors.append(f'无效的纹样图案，可选值: {list(DECORATIVE_PATTERNS.keys())}')
    
    if 'delivery_date' in data and data['delivery_date']:
        try:
            datetime.fromisoformat(data['delivery_date'])
        except ValueError:
            errors.append('交付日期格式不正确，请使用 ISO 格式 (YYYY-MM-DD)')
    
    return errors

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_db_version(cursor):
    try:
        cursor.execute('PRAGMA user_version')
        return cursor.fetchone()[0]
    except:
        return 0

def set_db_version(cursor, version):
    cursor.execute(f'PRAGMA user_version = {version}')

def migrate_v2_to_v3(cursor):
    cursor.execute('''
        CREATE TABLE orders_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_no TEXT UNIQUE NOT NULL,
            customer_name TEXT NOT NULL,
            customer_phone TEXT NOT NULL,
            customer_address TEXT,
            teacup_style TEXT NOT NULL,
            body_material TEXT NOT NULL,
            size_spec TEXT NOT NULL,
            lacquer_process TEXT NOT NULL,
            decorative_pattern TEXT,
            lacquer_color TEXT NOT NULL,
            painting_details TEXT,
            polishing_requirements TEXT,
            special_requirements TEXT,
            quantity INTEGER NOT NULL DEFAULT 1,
            unit_price REAL NOT NULL DEFAULT 0,
            total_price REAL NOT NULL DEFAULT 0,
            delivery_date TIMESTAMP,
            status TEXT NOT NULL DEFAULT '待接单',
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP NOT NULL
        )
    ''')
    
    try:
        cursor.execute('''
            INSERT INTO orders_new (
                id, order_no, customer_name, customer_phone, customer_address,
                teacup_style, body_material, size_spec, lacquer_process,
                decorative_pattern, lacquer_color, painting_details,
                polishing_requirements, special_requirements, quantity,
                unit_price, total_price, status, created_at, updated_at
            )
            SELECT 
                id, order_no, customer_name, customer_phone, customer_address,
                teacup_style, body_material, size_spec, lacquer_process,
                decorative_pattern, lacquer_color, painting_details,
                polishing_requirements, special_requirements, quantity,
                200, 200 * quantity, status, created_at, updated_at
            FROM orders
        ''')
    except:
        pass
    
    cursor.execute('DROP TABLE IF EXISTS orders')
    cursor.execute('ALTER TABLE orders_new RENAME TO orders')

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    version = get_db_version(cursor)
    
    if version == 0:
        cursor.execute('''
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_no TEXT UNIQUE NOT NULL,
                customer_name TEXT NOT NULL,
                customer_phone TEXT NOT NULL,
                customer_address TEXT,
                teacup_style TEXT NOT NULL,
                body_material TEXT NOT NULL,
                size_spec TEXT NOT NULL,
                lacquer_process TEXT NOT NULL,
                decorative_pattern TEXT,
                lacquer_color TEXT NOT NULL,
                painting_details TEXT,
                polishing_requirements TEXT,
                special_requirements TEXT,
                quantity INTEGER NOT NULL DEFAULT 1,
                unit_price REAL NOT NULL DEFAULT 0,
                total_price REAL NOT NULL DEFAULT 0,
                delivery_date TIMESTAMP,
                status TEXT NOT NULL DEFAULT '待接单',
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL
            )
        ''')
        set_db_version(cursor, 3)
    elif version == 2:
        migrate_v2_to_v3(cursor)
        set_db_version(cursor, 3)
    
    conn.commit()
    conn.close()

def generate_order_no():
    date_prefix = datetime.now().strftime('%Y%m%d')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT order_no FROM orders WHERE order_no LIKE ? ORDER BY order_no DESC LIMIT 1', (f'{date_prefix}%',))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        last_no = int(result['order_no'][-4:])
        new_no = last_no + 1
    else:
        new_no = 1
    
    return f'{date_prefix}{new_no:04d}'

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    
    errors = validate_order_data(data, is_create=True)
    if errors:
        return error_response('数据验证失败', 400, {'errors': errors})
    
    order_no = generate_order_no()
    now = datetime.now().isoformat()
    
    quantity = data.get('quantity', 1)
    price_info = calculate_price(
        data['body_material'],
        data['lacquer_process'],
        data.get('decorative_pattern', ''),
        quantity
    )
    
    conn = get_db()
    cursor = conn.cursor()
    
    status = data.get('status', '待接单')
    if status not in ORDER_STATUSES:
        status = '待接单'
    
    try:
        cursor.execute('''
            INSERT INTO orders (
                order_no, customer_name, customer_phone, customer_address,
                teacup_style, body_material, size_spec, lacquer_process,
                decorative_pattern, lacquer_color, painting_details,
                polishing_requirements, special_requirements, quantity,
                unit_price, total_price, delivery_date, status, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_no,
            data['customer_name'],
            data['customer_phone'],
            data.get('customer_address', ''),
            data['teacup_style'],
            data['body_material'],
            data['size_spec'],
            data['lacquer_process'],
            data.get('decorative_pattern', ''),
            data['lacquer_color'],
            data.get('painting_details', ''),
            data.get('polishing_requirements', ''),
            data.get('special_requirements', ''),
            quantity,
            price_info['unit_price'],
            price_info['total_price'],
            data.get('delivery_date'),
            status,
            now,
            now
        ))
        conn.commit()
        order_id = cursor.lastrowid
        conn.close()
        
        return success_response({
            'id': order_id,
            'order_no': order_no,
            'price_info': price_info
        }, '订单创建成功')
    except Exception as e:
        conn.close()
        return error_response(f'创建订单失败: {str(e)}', 500)

@app.route('/api/orders/calculate-price', methods=['POST'])
def calculate_order_price():
    data = request.get_json()
    
    required_fields = ['body_material', 'lacquer_process', 'quantity']
    for field in required_fields:
        if field not in data:
            return error_response(f'缺少必填字段: {field}', 400)
    
    price_info = calculate_price(
        data['body_material'],
        data['lacquer_process'],
        data.get('decorative_pattern', ''),
        data['quantity']
    )
    
    return success_response(price_info, '价格计算成功')

@app.route('/api/orders', methods=['GET'])
def get_orders():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    status = request.args.get('status')
    keyword = request.args.get('keyword', '')
    delivery_date_from = request.args.get('delivery_date_from')
    delivery_date_to = request.args.get('delivery_date_to')
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')
    
    if page < 1:
        page = 1
    if page_size < 1 or page_size > 100:
        page_size = 10
    
    valid_sort_fields = ['created_at', 'updated_at', 'delivery_date', 'total_price', 'order_no']
    if sort_by not in valid_sort_fields:
        sort_by = 'created_at'
    if sort_order not in ['asc', 'desc']:
        sort_order = 'desc'
    
    conn = get_db()
    cursor = conn.cursor()
    
    where_clauses = []
    params = []
    
    if status and status in ORDER_STATUSES:
        where_clauses.append('status = ?')
        params.append(status)
    
    if keyword:
        where_clauses.append('(customer_name LIKE ? OR customer_phone LIKE ? OR order_no LIKE ?)')
        keyword_param = f'%{keyword}%'
        params.extend([keyword_param, keyword_param, keyword_param])
    
    if delivery_date_from:
        where_clauses.append('delivery_date >= ?')
        params.append(delivery_date_from)
    
    if delivery_date_to:
        where_clauses.append('delivery_date <= ?')
        params.append(delivery_date_to)
    
    where_sql = ' AND '.join(where_clauses) if where_clauses else '1=1'
    
    count_sql = f'SELECT COUNT(*) as total FROM orders WHERE {where_sql}'
    cursor.execute(count_sql, params)
    total = cursor.fetchone()['total']
    
    offset = (page - 1) * page_size
    order_sql = f'{sort_by} {sort_order.upper()}'
    query_sql = f'''
        SELECT * FROM orders WHERE {where_sql}
        ORDER BY {order_sql}
        LIMIT ? OFFSET ?
    '''
    params.extend([page_size, offset])
    cursor.execute(query_sql, params)
    
    rows = cursor.fetchall()
    conn.close()
    
    orders = []
    for row in rows:
        orders.append({
            'id': row['id'],
            'order_no': row['order_no'],
            'customer_name': row['customer_name'],
            'customer_phone': row['customer_phone'],
            'customer_address': row['customer_address'],
            'teacup_style': row['teacup_style'],
            'body_material': row['body_material'],
            'size_spec': row['size_spec'],
            'lacquer_process': row['lacquer_process'],
            'decorative_pattern': row['decorative_pattern'],
            'lacquer_color': row['lacquer_color'],
            'painting_details': row['painting_details'],
            'polishing_requirements': row['polishing_requirements'],
            'special_requirements': row['special_requirements'],
            'quantity': row['quantity'],
            'unit_price': row['unit_price'],
            'total_price': row['total_price'],
            'delivery_date': row['delivery_date'],
            'status': row['status'],
            'created_at': row['created_at'],
            'updated_at': row['updated_at']
        })
    
    pagination = {
        'page': page,
        'page_size': page_size,
        'total': total,
        'total_pages': (total + page_size - 1) // page_size,
        'has_next': page * page_size < total,
        'has_prev': page > 1
    }
    
    return success_response({
        'list': orders,
        'pagination': pagination
    }, '获取订单列表成功')

@app.route('/api/orders/<order_no>', methods=['GET'])
def get_order(order_no):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return error_response('订单不存在', 404)
    
    order = {
        'id': row['id'],
        'order_no': row['order_no'],
        'customer_name': row['customer_name'],
        'customer_phone': row['customer_phone'],
        'customer_address': row['customer_address'],
        'teacup_style': row['teacup_style'],
        'body_material': row['body_material'],
        'size_spec': row['size_spec'],
        'lacquer_process': row['lacquer_process'],
        'decorative_pattern': row['decorative_pattern'],
        'lacquer_color': row['lacquer_color'],
        'painting_details': row['painting_details'],
        'polishing_requirements': row['polishing_requirements'],
        'special_requirements': row['special_requirements'],
        'quantity': row['quantity'],
        'unit_price': row['unit_price'],
        'total_price': row['total_price'],
        'delivery_date': row['delivery_date'],
        'status': row['status'],
        'created_at': row['created_at'],
        'updated_at': row['updated_at']
    }
    
    return success_response(order, '获取订单详情成功')

@app.route('/api/orders/<order_no>', methods=['PUT'])
def update_order(order_no):
    data = request.get_json()
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return error_response('订单不存在', 404)
    
    errors = validate_order_data(data, is_create=False)
    if errors:
        conn.close()
        return error_response('数据验证失败', 400, {'errors': errors})
    
    now = datetime.now().isoformat()
    
    update_fields = []
    update_values = []
    
    fields = [
        'customer_name', 'customer_phone', 'customer_address',
        'teacup_style', 'body_material', 'size_spec', 'lacquer_process',
        'decorative_pattern', 'lacquer_color', 'painting_details',
        'polishing_requirements', 'special_requirements', 'quantity',
        'delivery_date'
    ]
    
    for field in fields:
        if field in data:
            update_fields.append(f'{field} = ?')
            update_values.append(data[field])
    
    if 'body_material' in data or 'lacquer_process' in data or 'decorative_pattern' in data or 'quantity' in data:
        body_material = data.get('body_material', row['body_material'])
        lacquer_process = data.get('lacquer_process', row['lacquer_process'])
        decorative_pattern = data.get('decorative_pattern', row['decorative_pattern'])
        quantity = data.get('quantity', row['quantity'])
        
        price_info = calculate_price(body_material, lacquer_process, decorative_pattern, quantity)
        update_fields.append('unit_price = ?')
        update_fields.append('total_price = ?')
        update_values.append(price_info['unit_price'])
        update_values.append(price_info['total_price'])
    
    if not update_fields:
        conn.close()
        return error_response('没有提供要更新的字段', 400)
    
    update_fields.append('updated_at = ?')
    update_values.append(now)
    update_values.append(order_no)
    
    try:
        cursor.execute(f'''
            UPDATE orders SET {', '.join(update_fields)} WHERE order_no = ?
        ''', update_values)
        conn.commit()
        conn.close()
        
        return success_response(None, '订单更新成功')
    except Exception as e:
        conn.close()
        return error_response(f'更新订单失败: {str(e)}', 500)

@app.route('/api/orders/<order_no>/status', methods=['PUT'])
def update_order_status(order_no):
    data = request.get_json()
    new_status = data.get('status')
    
    if not new_status:
        return error_response('缺少状态字段', 400)
    
    if new_status not in ORDER_STATUSES:
        return error_response('无效的订单状态', 400)
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
    if not cursor.fetchone():
        conn.close()
        return error_response('订单不存在', 404)
    
    now = datetime.now().isoformat()
    
    try:
        cursor.execute('''
            UPDATE orders SET status = ?, updated_at = ? WHERE order_no = ?
        ''', (new_status, now, order_no))
        conn.commit()
        conn.close()
        
        return success_response({'status': new_status}, '订单状态更新成功')
    except Exception as e:
        conn.close()
        return error_response(f'更新状态失败: {str(e)}', 500)

@app.route('/api/orders/<order_no>', methods=['DELETE'])
def delete_order(order_no):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
    if not cursor.fetchone():
        conn.close()
        return error_response('订单不存在', 404)
    
    try:
        cursor.execute('DELETE FROM orders WHERE order_no = ?', (order_no,))
        conn.commit()
        conn.close()
        
        return success_response(None, '订单删除成功')
    except Exception as e:
        conn.close()
        return error_response(f'删除订单失败: {str(e)}', 500)

@app.route('/api/statuses', methods=['GET'])
def get_statuses():
    return success_response(ORDER_STATUSES, '获取状态列表成功')

@app.route('/api/body-materials', methods=['GET'])
def get_body_materials():
    return success_response([
        {'name': name, 'coefficient': coeff}
        for name, coeff in BODY_MATERIALS.items()
    ], '获取胎体材质列表成功')

@app.route('/api/size-specs', methods=['GET'])
def get_size_specs():
    return success_response(SIZE_SPECS, '获取尺寸规格列表成功')

@app.route('/api/lacquer-processes', methods=['GET'])
def get_lacquer_processes():
    return success_response([
        {'name': name, 'coefficient': coeff}
        for name, coeff in LACQUER_PROCESSES.items()
    ], '获取漆面工艺列表成功')

@app.route('/api/decorative-patterns', methods=['GET'])
def get_decorative_patterns():
    return success_response([
        {'name': name, 'coefficient': coeff}
        for name, coeff in DECORATIVE_PATTERNS.items()
    ], '获取纹样图案列表成功')

@app.route('/api/options', methods=['GET'])
def get_all_options():
    return success_response({
        'statuses': ORDER_STATUSES,
        'body_materials': [{'name': name, 'coefficient': coeff} for name, coeff in BODY_MATERIALS.items()],
        'size_specs': SIZE_SPECS,
        'lacquer_processes': [{'name': name, 'coefficient': coeff} for name, coeff in LACQUER_PROCESSES.items()],
        'decorative_patterns': [{'name': name, 'coefficient': coeff} for name, coeff in DECORATIVE_PATTERNS.items()],
        'base_price': BASE_PRICE
    }, '获取所有选项成功')

@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db()
    cursor = conn.cursor()
    
    stats = {}
    for status in ORDER_STATUSES:
        cursor.execute('SELECT COUNT(*) as count, SUM(total_price) as amount FROM orders WHERE status = ?', (status,))
        result = cursor.fetchone()
        stats[status] = {
            'count': result['count'],
            'amount': round(result['amount'] or 0, 2)
        }
    
    cursor.execute('SELECT COUNT(*) as total, SUM(total_price) as total_amount FROM orders')
    total = cursor.fetchone()
    stats['total'] = {
        'count': total['total'],
        'amount': round(total['total_amount'] or 0, 2)
    }
    
    conn.close()
    
    return success_response(stats, '获取统计数据成功')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
