import sqlite3
import datetime
import os
import re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE = 'orders.db'
DB_VERSION = 3

ORDER_STATUSES = [
    '待接单',
    '选皮',
    '蒸煮',
    '裁剪',
    '拼接',
    '雕花',
    '定型',
    '完工'
]

BARK_MATERIALS = {
    '白桦皮': {'price': 80, 'difficulty': 1},
    '黑桦皮': {'price': 120, 'difficulty': 2},
    '红桦皮': {'price': 150, 'difficulty': 2},
    '椴树皮': {'price': 100, 'difficulty': 1},
    '桑树皮': {'price': 180, 'difficulty': 3},
    '其他': {'price': 100, 'difficulty': 2}
}

SPLICING_TECHNIQUES = {
    '平接': {'price': 50, 'difficulty': 1, 'days': 1},
    '对接': {'price': 60, 'difficulty': 1, 'days': 1},
    '搭接': {'price': 80, 'difficulty': 2, 'days': 2},
    '榫接': {'price': 120, 'difficulty': 3, 'days': 3},
    '镶嵌接': {'price': 150, 'difficulty': 3, 'days': 3},
    '编织接': {'price': 180, 'difficulty': 4, 'days': 4},
    '其他': {'price': 100, 'difficulty': 2, 'days': 2}
}

CARVING_DEPTHS = {
    '浅雕(1-2mm)': {'price': 100, 'difficulty': 1, 'days': 1},
    '中雕(2-4mm)': {'price': 180, 'difficulty': 2, 'days': 2},
    '深雕(4-6mm)': {'price': 280, 'difficulty': 3, 'days': 3},
    '透雕': {'price': 380, 'difficulty': 4, 'days': 4}
}

PENHOLDER_STYLES = ['圆形', '方形', '椭圆形', '多边形', '异形']
PENHOLDER_SIZES = {
    '小号': {'size_range': '直径<6cm', 'price_factor': 0.8},
    '中号': {'size_range': '直径6-8cm', 'price_factor': 1.0},
    '大号': {'size_range': '直径8-10cm', 'price_factor': 1.2},
    '特大号': {'size_range': '直径>10cm', 'price_factor': 1.5}
}

CRAFTSPEOPLE = [
    {'id': 1, 'name': '张师傅', 'skill_level': '高级', 'daily_rate': 300},
    {'id': 2, 'name': '李师傅', 'skill_level': '中级', 'daily_rate': 220},
    {'id': 3, 'name': '王师傅', 'skill_level': '高级', 'daily_rate': 280},
    {'id': 4, 'name': '赵师傅', 'skill_level': '初级', 'daily_rate': 150}
]

BASE_PRICE = 200

def success_response(data=None, message='操作成功'):
    return jsonify({
        'code': 200,
        'success': True,
        'message': message,
        'data': data,
        'timestamp': datetime.datetime.now().isoformat()
    })

def error_response(message='操作失败', code=400, data=None):
    return jsonify({
        'code': code,
        'success': False,
        'message': message,
        'data': data,
        'timestamp': datetime.datetime.now().isoformat()
    }), code

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_db_version(cursor):
    try:
        cursor.execute('SELECT version FROM db_version WHERE id = 1')
        row = cursor.fetchone()
        return row['version'] if row else 1
    except:
        return 1

def set_db_version(cursor, version):
    cursor.execute('CREATE TABLE IF NOT EXISTS db_version (id INTEGER PRIMARY KEY, version INTEGER)')
    cursor.execute('INSERT OR REPLACE INTO db_version (id, version) VALUES (1, ?)', (version,))

def migrate_v2_to_v3(cursor):
    cursor.execute('ALTER TABLE orders ADD COLUMN price REAL DEFAULT 0')
    cursor.execute('ALTER TABLE orders ADD COLUMN craftsman_id INTEGER DEFAULT 0')
    cursor.execute('ALTER TABLE orders ADD COLUMN craftsman_name TEXT DEFAULT ""')
    cursor.execute('ALTER TABLE orders ADD COLUMN work_days INTEGER DEFAULT 0')
    cursor.execute('ALTER TABLE orders ADD COLUMN delivery_date TIMESTAMP')
    cursor.execute('ALTER TABLE orders ADD COLUMN material_cost REAL DEFAULT 0')
    cursor.execute('ALTER TABLE orders ADD COLUMN process_cost REAL DEFAULT 0')
    cursor.execute('ALTER TABLE orders ADD COLUMN labor_cost REAL DEFAULT 0')

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_no TEXT UNIQUE NOT NULL,
            customer_name TEXT NOT NULL,
            customer_phone TEXT NOT NULL,
            customer_address TEXT,
            penholder_style TEXT,
            penholder_size TEXT,
            carving_pattern TEXT,
            special_requirements TEXT,
            bark_material TEXT DEFAULT '',
            size_height TEXT DEFAULT '',
            size_diameter TEXT DEFAULT '',
            size_thickness TEXT DEFAULT '',
            splicing_tech TEXT DEFAULT '',
            carving_position TEXT DEFAULT '',
            carving_depth TEXT DEFAULT '',
            carving_detail TEXT DEFAULT '',
            price REAL DEFAULT 0,
            craftsman_id INTEGER DEFAULT 0,
            craftsman_name TEXT DEFAULT '',
            work_days INTEGER DEFAULT 0,
            delivery_date TIMESTAMP,
            material_cost REAL DEFAULT 0,
            process_cost REAL DEFAULT 0,
            labor_cost REAL DEFAULT 0,
            status TEXT NOT NULL DEFAULT '待接单',
            create_time TIMESTAMP NOT NULL,
            update_time TIMESTAMP NOT NULL
        )
    ''')
    
    current_version = get_db_version(cursor)
    if current_version < DB_VERSION:
        print(f'正在升级数据库: v{current_version} -> v{DB_VERSION}')
        if current_version == 2:
            migrate_v2_to_v3(cursor)
        set_db_version(cursor, DB_VERSION)
        print('数据库升级完成！')
    
    conn.commit()
    conn.close()

def generate_order_no():
    now = datetime.datetime.now()
    date_str = now.strftime('%Y%m%d')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT order_no FROM orders WHERE order_no LIKE ? ORDER BY order_no DESC LIMIT 1', (f'{date_str}%',))
    row = cursor.fetchone()
    conn.close()
    if row:
        last_no = int(row['order_no'][-4:])
        new_no = last_no + 1
    else:
        new_no = 1
    return f'{date_str}{new_no:04d}'

def validate_phone(phone):
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, phone))

def validate_numeric_size(value):
    if not value:
        return True
    pattern = r'^\d+(\.\d+)?(cm|mm)?$'
    return bool(re.match(pattern, value.lower()))

def calculate_price(data):
    total = BASE_PRICE
    material_cost = 0
    process_cost = 0
    labor_cost = 0
    work_days = 1
    
    material = data.get('bark_material', '')
    if material in BARK_MATERIALS:
        material_cost = BARK_MATERIALS[material]['price']
        total += material_cost
    
    size = data.get('penholder_size', '')
    if size in PENHOLDER_SIZES:
        total *= PENHOLDER_SIZES[size]['price_factor']
    
    splicing = data.get('splicing_tech', '')
    if splicing in SPLICING_TECHNIQUES:
        splice_cost = SPLICING_TECHNIQUES[splicing]['price']
        process_cost += splice_cost
        total += splice_cost
        work_days += SPLICING_TECHNIQUES[splicing]['days']
    
    carving = data.get('carving_depth', '')
    if carving in CARVING_DEPTHS:
        carve_cost = CARVING_DEPTHS[carving]['price']
        process_cost += carve_cost
        total += carve_cost
        work_days += CARVING_DEPTHS[carving]['days']
    
    craftsman_id = data.get('craftsman_id', 0)
    if craftsman_id:
        craftsman = next((c for c in CRAFTSPEOPLE if c['id'] == craftsman_id), None)
        if craftsman:
            labor_cost = craftsman['daily_rate'] * work_days
            total += labor_cost
    
    return {
        'price': round(total, 2),
        'material_cost': round(material_cost, 2),
        'process_cost': round(process_cost, 2),
        'labor_cost': round(labor_cost, 2),
        'work_days': work_days
    }

def validate_order_data(data, is_create=True):
    errors = []
    
    required_fields = ['customer_name', 'customer_phone', 'penholder_style', 'penholder_size']
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f'缺少必填字段: {field}')
    
    if 'customer_phone' in data and data['customer_phone']:
        if not validate_phone(data['customer_phone']):
            errors.append('手机号格式不正确，请输入11位有效手机号')
    
    if 'penholder_style' in data and data['penholder_style']:
        if data['penholder_style'] not in PENHOLDER_STYLES:
            errors.append(f'笔筒样式不支持，可选值: {", ".join(PENHOLDER_STYLES)}')
    
    if 'penholder_size' in data and data['penholder_size']:
        if data['penholder_size'] not in PENHOLDER_SIZES:
            errors.append(f'笔筒尺寸不支持，可选值: {", ".join(PENHOLDER_SIZES.keys())}')
    
    if 'bark_material' in data and data['bark_material']:
        if data['bark_material'] not in BARK_MATERIALS:
            errors.append(f'树皮材质不支持，可选值: {", ".join(BARK_MATERIALS.keys())}')
    
    if 'splicing_tech' in data and data['splicing_tech']:
        if data['splicing_tech'] not in SPLICING_TECHNIQUES:
            errors.append(f'拼接工艺不支持，可选值: {", ".join(SPLICING_TECHNIQUES.keys())}')
    
    if 'carving_depth' in data and data['carving_depth']:
        if data['carving_depth'] not in CARVING_DEPTHS:
            errors.append(f'雕刻深度不支持，可选值: {", ".join(CARVING_DEPTHS.keys())}')
    
    size_fields = ['size_height', 'size_diameter', 'size_thickness']
    for field in size_fields:
        if field in data and data[field]:
            if not validate_numeric_size(data[field]):
                errors.append(f'{field} 格式不正确，请输入数值（如: 15cm 或 15）')
    
    if 'craftsman_id' in data and data['craftsman_id']:
        craftsman_ids = [c['id'] for c in CRAFTSPEOPLE]
        if data['craftsman_id'] not in craftsman_ids:
            errors.append(f'匠人ID不存在，可选值: {craftsman_ids}')
    
    if 'delivery_date' in data and data['delivery_date']:
        try:
            datetime.datetime.fromisoformat(data['delivery_date'].replace('Z', '+00:00'))
        except:
            errors.append('交付日期格式不正确，请使用 ISO 格式 (如: 2024-05-20)')
    
    return errors

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    if not data:
        return error_response('无效的请求数据', 400)
    
    errors = validate_order_data(data, is_create=True)
    if errors:
        return error_response('数据验证失败', 400, {'errors': errors})
    
    price_info = calculate_price(data)
    order_no = generate_order_no()
    now = datetime.datetime.now()
    
    delivery_date = None
    if 'delivery_date' in data and data['delivery_date']:
        try:
            delivery_date = datetime.datetime.fromisoformat(data['delivery_date'].replace('Z', '+00:00'))
        except:
            pass
    
    craftsman_name = ''
    craftsman_id = data.get('craftsman_id', 0)
    if craftsman_id:
        craftsman = next((c for c in CRAFTSPEOPLE if c['id'] == craftsman_id), None)
        if craftsman:
            craftsman_name = craftsman['name']
    
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO orders (
                order_no, customer_name, customer_phone, customer_address,
                penholder_style, penholder_size, carving_pattern, special_requirements,
                bark_material, size_height, size_diameter, size_thickness,
                splicing_tech, carving_position, carving_depth, carving_detail,
                price, material_cost, process_cost, labor_cost,
                craftsman_id, craftsman_name, work_days, delivery_date,
                status, create_time, update_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_no,
            data['customer_name'],
            data['customer_phone'],
            data.get('customer_address', ''),
            data.get('penholder_style', ''),
            data.get('penholder_size', ''),
            data.get('carving_pattern', ''),
            data.get('special_requirements', ''),
            data.get('bark_material', ''),
            data.get('size_height', ''),
            data.get('size_diameter', ''),
            data.get('size_thickness', ''),
            data.get('splicing_tech', ''),
            data.get('carving_position', ''),
            data.get('carving_depth', ''),
            data.get('carving_detail', ''),
            price_info['price'],
            price_info['material_cost'],
            price_info['process_cost'],
            price_info['labor_cost'],
            craftsman_id,
            craftsman_name,
            price_info['work_days'],
            delivery_date,
            '待接单',
            now,
            now
        ))
        conn.commit()
        order_id = cursor.lastrowid
        conn.close()
        return success_response({
            'order_id': order_id,
            'order_no': order_no,
            'price': price_info['price'],
            'work_days': price_info['work_days']
        }, '订单创建成功')
    except Exception as e:
        conn.close()
        return error_response(str(e), 500)

@app.route('/api/orders', methods=['GET'])
def get_orders():
    status = request.args.get('status')
    style = request.args.get('style')
    material = request.args.get('material')
    delivery_from = request.args.get('delivery_from')
    delivery_to = request.args.get('delivery_to')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    sort_by = request.args.get('sort_by', 'create_time')
    sort_order = request.args.get('sort_order', 'desc')
    
    conn = get_db()
    cursor = conn.cursor()
    
    where_clauses = []
    params = []
    
    if status and status in ORDER_STATUSES:
        where_clauses.append('status = ?')
        params.append(status)
    
    if style and style in PENHOLDER_STYLES:
        where_clauses.append('penholder_style = ?')
        params.append(style)
    
    if material and material in BARK_MATERIALS:
        where_clauses.append('bark_material = ?')
        params.append(material)
    
    if delivery_from:
        where_clauses.append('delivery_date >= ?')
        params.append(delivery_from)
    
    if delivery_to:
        where_clauses.append('delivery_date <= ?')
        params.append(delivery_to + ' 23:59:59')
    
    where_sql = ' AND '.join(where_clauses) if where_clauses else '1=1'
    
    valid_sort_fields = ['create_time', 'update_time', 'price', 'delivery_date', 'order_no']
    if sort_by not in valid_sort_fields:
        sort_by = 'create_time'
    if sort_order.lower() not in ['asc', 'desc']:
        sort_order = 'desc'
    
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
            'penholder_style': row['penholder_style'],
            'penholder_size': row['penholder_size'],
            'carving_pattern': row['carving_pattern'],
            'special_requirements': row['special_requirements'],
            'bark_material': row['bark_material'],
            'size_height': row['size_height'],
            'size_diameter': row['size_diameter'],
            'size_thickness': row['size_thickness'],
            'splicing_tech': row['splicing_tech'],
            'carving_position': row['carving_position'],
            'carving_depth': row['carving_depth'],
            'carving_detail': row['carving_detail'],
            'price': row['price'],
            'material_cost': row['material_cost'],
            'process_cost': row['process_cost'],
            'labor_cost': row['labor_cost'],
            'craftsman_id': row['craftsman_id'],
            'craftsman_name': row['craftsman_name'],
            'work_days': row['work_days'],
            'delivery_date': row['delivery_date'],
            'status': row['status'],
            'create_time': row['create_time'],
            'update_time': row['update_time']
        })
    
    return success_response({
        'list': orders,
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total': total,
            'total_pages': (total + page_size - 1) // page_size
        }
    })

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
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
        'penholder_style': row['penholder_style'],
        'penholder_size': row['penholder_size'],
        'carving_pattern': row['carving_pattern'],
        'special_requirements': row['special_requirements'],
        'bark_material': row['bark_material'],
        'size_height': row['size_height'],
        'size_diameter': row['size_diameter'],
        'size_thickness': row['size_thickness'],
        'splicing_tech': row['splicing_tech'],
        'carving_position': row['carving_position'],
        'carving_depth': row['carving_depth'],
        'carving_detail': row['carving_detail'],
        'price': row['price'],
        'material_cost': row['material_cost'],
        'process_cost': row['process_cost'],
        'labor_cost': row['labor_cost'],
        'craftsman_id': row['craftsman_id'],
        'craftsman_name': row['craftsman_name'],
        'work_days': row['work_days'],
        'delivery_date': row['delivery_date'],
        'status': row['status'],
        'create_time': row['create_time'],
        'update_time': row['update_time']
    }
    
    return success_response(order)

@app.route('/api/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()
    if not data:
        return error_response('无效的请求数据', 400)
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return error_response('订单不存在', 404)
    
    errors = validate_order_data(data, is_create=False)
    if errors:
        conn.close()
        return error_response('数据验证失败', 400, {'errors': errors})
    
    now = datetime.datetime.now()
    
    update_fields = []
    update_values = []
    
    field_mapping = {
        'customer_name': 'customer_name',
        'customer_phone': 'customer_phone',
        'customer_address': 'customer_address',
        'penholder_style': 'penholder_style',
        'penholder_size': 'penholder_size',
        'carving_pattern': 'carving_pattern',
        'special_requirements': 'special_requirements',
        'bark_material': 'bark_material',
        'size_height': 'size_height',
        'size_diameter': 'size_diameter',
        'size_thickness': 'size_thickness',
        'splicing_tech': 'splicing_tech',
        'carving_position': 'carving_position',
        'carving_depth': 'carving_depth',
        'carving_detail': 'carving_detail',
        'craftsman_id': 'craftsman_id',
        'delivery_date': 'delivery_date'
    }
    
    for json_field, db_field in field_mapping.items():
        if json_field in data:
            update_fields.append(f'{db_field} = ?')
            update_values.append(data[json_field])
    
    price_related_fields = ['bark_material', 'penholder_size', 'splicing_tech', 'carving_depth', 'craftsman_id']
    if any(f in data for f in price_related_fields):
        current_data = dict(row)
        current_data.update(data)
        price_info = calculate_price(current_data)
        update_fields.extend([
            'price = ?', 'material_cost = ?', 'process_cost = ?',
            'labor_cost = ?', 'work_days = ?'
        ])
        update_values.extend([
            price_info['price'], price_info['material_cost'],
            price_info['process_cost'], price_info['labor_cost'],
            price_info['work_days']
        ])
    
    if 'craftsman_id' in data:
        craftsman = next((c for c in CRAFTSPEOPLE if c['id'] == data['craftsman_id']), None)
        if craftsman:
            update_fields.append('craftsman_name = ?')
            update_values.append(craftsman['name'])
    
    if not update_fields:
        conn.close()
        return error_response('没有提供要更新的字段', 400)
    
    update_fields.append('update_time = ?')
    update_values.append(now)
    update_values.append(order_id)
    
    try:
        cursor.execute(f'''
            UPDATE orders SET {', '.join(update_fields)} WHERE id = ?
        ''', update_values)
        conn.commit()
        conn.close()
        return success_response(None, '订单更新成功')
    except Exception as e:
        conn.close()
        return error_response(str(e), 500)

@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    data = request.get_json()
    if not data or 'status' not in data:
        return error_response('缺少状态字段', 400)
    
    new_status = data['status']
    if new_status not in ORDER_STATUSES:
        return error_response('无效的订单状态', 400)
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return error_response('订单不存在', 404)
    
    now = datetime.datetime.now()
    try:
        cursor.execute('''
            UPDATE orders SET status = ?, update_time = ? WHERE id = ?
        ''', (new_status, now, order_id))
        conn.commit()
        conn.close()
        return success_response(None, '订单状态更新成功')
    except Exception as e:
        conn.close()
        return error_response(str(e), 500)

@app.route('/api/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return error_response('订单不存在', 404)
    
    try:
        cursor.execute('DELETE FROM orders WHERE id = ?', (order_id,))
        conn.commit()
        conn.close()
        return success_response(None, '订单删除成功')
    except Exception as e:
        conn.close()
        return error_response(str(e), 500)

@app.route('/api/orders/calculate', methods=['POST'])
def calculate_order_price():
    data = request.get_json()
    if not data:
        return error_response('无效的请求数据', 400)
    
    price_info = calculate_price(data)
    return success_response(price_info, '价格计算成功')

@app.route('/api/statuses', methods=['GET'])
def get_statuses():
    return success_response(ORDER_STATUSES)

@app.route('/api/materials', methods=['GET'])
def get_materials():
    result = [{'name': k, 'price': v['price'], 'difficulty': v['difficulty']} for k, v in BARK_MATERIALS.items()]
    return success_response(result)

@app.route('/api/splicing-techniques', methods=['GET'])
def get_splicing_techniques():
    result = [{'name': k, 'price': v['price'], 'difficulty': v['difficulty'], 'days': v['days']} for k, v in SPLICING_TECHNIQUES.items()]
    return success_response(result)

@app.route('/api/carving-depths', methods=['GET'])
def get_carving_depths():
    result = [{'name': k, 'price': v['price'], 'difficulty': v['difficulty'], 'days': v['days']} for k, v in CARVING_DEPTHS.items()]
    return success_response(result)

@app.route('/api/styles', methods=['GET'])
def get_styles():
    return success_response(PENHOLDER_STYLES)

@app.route('/api/sizes', methods=['GET'])
def get_sizes():
    result = [{'name': k, 'size_range': v['size_range'], 'price_factor': v['price_factor']} for k, v in PENHOLDER_SIZES.items()]
    return success_response(result)

@app.route('/api/craftspeople', methods=['GET'])
def get_craftspeople():
    return success_response(CRAFTSPEOPLE)

@app.route('/api/process-specs', methods=['GET'])
def get_process_specs():
    return success_response({
        'statuses': ORDER_STATUSES,
        'bark_materials': list(BARK_MATERIALS.keys()),
        'splicing_techniques': list(SPLICING_TECHNIQUES.keys()),
        'carving_depths': list(CARVING_DEPTHS.keys()),
        'penholder_styles': PENHOLDER_STYLES,
        'penholder_sizes': list(PENHOLDER_SIZES.keys()),
        'craftspeople': CRAFTSPEOPLE,
        'base_price': BASE_PRICE,
        'process_guide': {
            'cutting': ['size_height', 'size_diameter', 'size_thickness'],
            'splicing': ['splicing_tech', 'bark_material'],
            'carving': ['carving_pattern', 'carving_position', 'carving_depth', 'carving_detail']
        }
    })

if __name__ == '__main__':
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
        print('已重置数据库以应用 v3.0 新结构')
    init_db()
    print('桦树皮笔筒定制订单管理系统 v3.0 启动成功！')
    print('API 地址: http://127.0.0.1:5000')
    app.run(debug=True, host='0.0.0.0', port=5000)
