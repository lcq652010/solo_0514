from flask import Flask, request, jsonify, g
from flask_cors import CORS
import sqlite3
import datetime
import os
import re

app = Flask(__name__)
CORS(app)

DATABASE = 'orders.db'

ORDER_STATUSES = ['待接单', '制版', '熔铜', '浇铸', '打磨', '錾刻', '做旧', '完工']

COPPER_TYPES = {
    'H62黄铜': {'price_per_cm3': 0.65, 'name': 'H62黄铜'},
    'H65黄铜': {'price_per_cm3': 0.70, 'name': 'H65黄铜'},
    'H68黄铜': {'price_per_cm3': 0.75, 'name': 'H68黄铜'},
    'T2紫铜': {'price_per_cm3': 0.85, 'name': 'T2紫铜'},
    'T3紫铜': {'price_per_cm3': 0.82, 'name': 'T3紫铜'},
    'QSn4-3青铜': {'price_per_cm3': 0.95, 'name': 'QSn4-3青铜'},
    'QSn6.5-0.1青铜': {'price_per_cm3': 0.98, 'name': 'QSn6.5-0.1青铜'},
    'B10白铜': {'price_per_cm3': 1.20, 'name': 'B10白铜'},
    'B30白铜': {'price_per_cm3': 1.50, 'name': 'B30白铜'}
}

CARVING_PATTERNS = {
    '无纹样': {'difficulty': 1.0, 'days': 0},
    '祥云纹': {'difficulty': 1.2, 'days': 1},
    '回纹': {'difficulty': 1.1, 'days': 1},
    '雷纹': {'difficulty': 1.3, 'days': 2},
    '饕餮纹': {'difficulty': 1.8, 'days': 3},
    '龙凤纹': {'difficulty': 2.0, 'days': 4},
    '山水纹': {'difficulty': 1.6, 'days': 3},
    '梅兰竹菊': {'difficulty': 1.5, 'days': 2},
    '花鸟纹': {'difficulty': 1.4, 'days': 2},
    '几何纹': {'difficulty': 1.1, 'days': 1},
    '自定义纹样': {'difficulty': 2.5, 'days': 5}
}

SURFACE_FINISHES = {
    '原色抛光': {'price_factor': 1.0, 'days': 1},
    '哑光拉丝': {'price_factor': 1.1, 'days': 1},
    '复古做旧': {'price_factor': 1.3, 'days': 2},
    '黑漆古': {'price_factor': 1.5, 'days': 3},
    '红漆古': {'price_factor': 1.5, 'days': 3},
    '热着色-褐色': {'price_factor': 1.4, 'days': 2},
    '热着色-蓝色': {'price_factor': 1.4, 'days': 2},
    '热着色-绿色': {'price_factor': 1.4, 'days': 2},
    '封釉保护': {'price_factor': 1.2, 'days': 1}
}

STYLES = ['方形瑞兽', '长条形素面', '圆形浮雕', '随形巧雕', '竹节造型', '其他']

CRAFTSMEN = [
    {'id': 1, 'name': '王师傅', 'skill_level': '高级', 'daily_rate': 500},
    {'id': 2, 'name': '李师傅', 'skill_level': '中级', 'daily_rate': 350},
    {'id': 3, 'name': '张师傅', 'skill_level': '高级', 'daily_rate': 480},
    {'id': 4, 'name': '陈师傅', 'skill_level': '初级', 'daily_rate': 250}
]

BASE_PROCESS_DAYS = {
    '待接单': 0,
    '制版': 1,
    '熔铜': 0.5,
    '浇铸': 1,
    '打磨': 1,
    '錾刻': 0,
    '做旧': 0,
    '完工': 0
}

def success_response(data, message='操作成功'):
    return jsonify({
        'code': 200,
        'message': message,
        'data': data,
        'timestamp': datetime.datetime.now().isoformat()
    }), 200

def error_response(message, code=400):
    return jsonify({
        'code': code,
        'message': message,
        'data': None,
        'timestamp': datetime.datetime.now().isoformat()
    }), code

def calculate_price(length_cm, width_cm, thickness_cm, copper_type, carving_pattern, surface_finish, quantity):
    volume = length_cm * width_cm * thickness_cm
    copper_price = volume * COPPER_TYPES[copper_type]['price_per_cm3']
    carving_factor = CARVING_PATTERNS[carving_pattern]['difficulty'] if carving_pattern in CARVING_PATTERNS else 1.0
    surface_factor = SURFACE_FINISHES[surface_finish]['price_factor']
    unit_price = copper_price * carving_factor * surface_factor
    total_price = unit_price * quantity
    return {
        'unit_price': round(unit_price, 2),
        'total_price': round(total_price, 2),
        'copper_cost': round(copper_price * quantity, 2),
        'carving_cost': round(copper_price * (carving_factor - 1) * quantity, 2),
        'surface_cost': round(copper_price * (surface_factor - 1) * quantity, 2)
    }

def calculate_estimated_days(carving_pattern, surface_finish):
    base_days = sum(BASE_PROCESS_DAYS.values())
    carving_days = CARVING_PATTERNS[carving_pattern]['days'] if carving_pattern in CARVING_PATTERNS else 0
    surface_days = SURFACE_FINISHES[surface_finish]['days']
    total_days = base_days + carving_days + surface_days
    return total_days

def validate_order_data(data):
    required_fields = ['customer_name', 'customer_phone', 'paperweight_style', 
                       'length_cm', 'width_cm', 'thickness_cm', 'quantity']
    for field in required_fields:
        if field not in data:
            return False, f'缺少必填字段: {field}'
    if not data['customer_name'].strip():
        return False, '客户姓名不能为空'
    if not re.match(r'^1[3-9]\d{9}$', data['customer_phone']):
        return False, '请输入有效的手机号码'
    if data['paperweight_style'] not in STYLES:
        return False, f'镇纸样式不合法'
    try:
        length = float(data['length_cm'])
        width = float(data['width_cm'])
        thickness = float(data['thickness_cm'])
        if length <= 0 or length > 50:
            return False, '长度应在0-50cm之间'
        if width <= 0 or width > 50:
            return False, '宽度应在0-50cm之间'
        if thickness <= 0 or thickness > 10:
            return False, '厚度应在0-10cm之间'
    except ValueError:
        return False, '尺寸必须为数字'
    try:
        quantity = int(data['quantity'])
        if quantity <= 0 or quantity > 1000:
            return False, '数量应在1-1000之间'
    except ValueError:
        return False, '数量必须为整数'
    if 'copper_type' in data and data['copper_type'] not in COPPER_TYPES:
        return False, f'铜材类型不合法'
    if 'carving_pattern' in data and data['carving_pattern'] not in CARVING_PATTERNS:
        return False, f'錾刻纹样不合法'
    if 'surface_finish' in data and data['surface_finish'] not in SURFACE_FINISHES:
        return False, f'表面工艺不合法'
    return True, '校验通过'

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
                paperweight_style TEXT NOT NULL,
                length_cm REAL NOT NULL,
                width_cm REAL NOT NULL,
                thickness_cm REAL NOT NULL,
                inscription TEXT,
                copper_type TEXT NOT NULL,
                carving_pattern TEXT,
                surface_finish TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                total_price REAL NOT NULL,
                copper_cost REAL NOT NULL,
                carving_cost REAL NOT NULL,
                surface_cost REAL NOT NULL,
                craftsman_id INTEGER,
                craftsman_name TEXT,
                estimated_days INTEGER NOT NULL,
                delivery_date TIMESTAMP,
                requirements TEXT,
                status TEXT NOT NULL DEFAULT '待接单',
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL
            )
        ''')
        db.commit()

def generate_order_no():
    now = datetime.datetime.now()
    date_prefix = now.strftime('%Y%m%d')
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT order_no FROM orders WHERE order_no LIKE ? ORDER BY order_no DESC LIMIT 1', (f'{date_prefix}%',))
    last_order = cursor.fetchone()
    if last_order:
        last_no = int(last_order['order_no'][-4:])
        new_no = last_no + 1
    else:
        new_no = 1
    return f'{date_prefix}{new_no:04d}'

@app.route('/api/craftsmen', methods=['GET'])
def get_craftsmen():
    return success_response(CRAFTSMEN, '获取匠人列表成功')

@app.route('/api/copper-types', methods=['GET'])
def get_copper_types():
    result = [{'name': k, **v} for k, v in COPPER_TYPES.items()]
    return success_response(result, '获取铜材类型成功')

@app.route('/api/carving-patterns', methods=['GET'])
def get_carving_patterns():
    result = [{'name': k, **v} for k, v in CARVING_PATTERNS.items()]
    return success_response(result, '获取錾刻纹样成功')

@app.route('/api/surface-finishes', methods=['GET'])
def get_surface_finishes():
    result = [{'name': k, **v} for k, v in SURFACE_FINISHES.items()]
    return success_response(result, '获取表面工艺成功')

@app.route('/api/styles', methods=['GET'])
def get_styles():
    return success_response(STYLES, '获取镇纸样式成功')

@app.route('/api/statuses', methods=['GET'])
def get_statuses():
    return success_response(ORDER_STATUSES, '获取状态列表成功')

@app.route('/api/calculate-price', methods=['POST'])
def calculate_price_api():
    data = request.get_json()
    required = ['length_cm', 'width_cm', 'thickness_cm', 'copper_type', 'carving_pattern', 'surface_finish', 'quantity']
    for field in required:
        if field not in data:
            return error_response(f'缺少字段: {field}')
    if data['copper_type'] not in COPPER_TYPES:
        return error_response('铜材类型不合法')
    if data['carving_pattern'] not in CARVING_PATTERNS:
        return error_response('錾刻纹样不合法')
    if data['surface_finish'] not in SURFACE_FINISHES:
        return error_response('表面工艺不合法')
    try:
        price_info = calculate_price(
            float(data['length_cm']),
            float(data['width_cm']),
            float(data['thickness_cm']),
            data['copper_type'],
            data['carving_pattern'],
            data['surface_finish'],
            int(data['quantity'])
        )
        estimated_days = calculate_estimated_days(
            data['carving_pattern'],
            data['surface_finish']
        )
        return success_response({**price_info, 'estimated_days': estimated_days}, '计算成功')
    except Exception as e:
        return error_response(f'计算失败: {str(e)}')

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    valid, msg = validate_order_data(data)
    if not valid:
        return error_response(msg)
    db = get_db()
    cursor = db.cursor()
    order_no = generate_order_no()
    now = datetime.datetime.now().isoformat()
    copper_type = data.get('copper_type', 'H62黄铜')
    carving_pattern = data.get('carving_pattern', '无纹样')
    surface_finish = data.get('surface_finish', '原色抛光')
    price_info = calculate_price(
        float(data['length_cm']),
        float(data['width_cm']),
        float(data['thickness_cm']),
        copper_type,
        carving_pattern,
        surface_finish,
        int(data['quantity'])
    )
    estimated_days = calculate_estimated_days(carving_pattern, surface_finish)
    delivery_date = (datetime.datetime.now() + datetime.timedelta(days=estimated_days)).isoformat()
    try:
        cursor.execute('''
            INSERT INTO orders (
                order_no, customer_name, customer_phone, customer_address,
                paperweight_style, length_cm, width_cm, thickness_cm,
                inscription, copper_type, carving_pattern, surface_finish,
                quantity, unit_price, total_price, copper_cost,
                carving_cost, surface_cost,
                craftsman_id, craftsman_name,
                estimated_days, delivery_date,
                requirements, status, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_no,
            data['customer_name'],
            data['customer_phone'],
            data.get('customer_address', ''),
            data['paperweight_style'],
            float(data['length_cm']),
            float(data['width_cm']),
            float(data['thickness_cm']),
            data.get('inscription', ''),
            copper_type,
            carving_pattern,
            surface_finish,
            int(data['quantity']),
            price_info['unit_price'],
            price_info['total_price'],
            price_info['copper_cost'],
            price_info['carving_cost'],
            price_info['surface_cost'],
            data.get('craftsman_id'),
            data.get('craftsman_name'),
            estimated_days,
            delivery_date,
            data.get('requirements', ''),
            '待接单',
            now,
            now
        ))
        db.commit()
        return success_response({'order_no': order_no, 'total_price': price_info['total_price'], 'estimated_days': estimated_days, 'delivery_date': delivery_date}, '订单创建成功')
    except Exception as e:
        db.rollback()
        return error_response(f'创建失败: {str(e)}', 500)

@app.route('/api/orders', methods=['GET'])
def get_orders():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    status = request.args.get('status')
    style = request.args.get('style')
    copper_type = request.args.get('copper_type')
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')
    delivery_date_from = request.args.get('delivery_date_from')
    delivery_date_to = request.args.get('delivery_date_to')
    if page < 1:
        page = 1
    if page_size < 1 or page_size > 100:
        page_size = 10
    offset = (page - 1) * page_size
    db = get_db()
    cursor = db.cursor()
    where_clauses = []
    params = []
    if status:
        where_clauses.append('status = ?')
        params.append(status)
    if style:
        where_clauses.append('paperweight_style = ?')
        params.append(style)
    if copper_type:
        where_clauses.append('copper_type = ?')
        params.append(copper_type)
    if delivery_date_from:
        where_clauses.append('delivery_date >= ?')
        params.append(delivery_date_from)
    if delivery_date_to:
        where_clauses.append('delivery_date <= ?')
        params.append(delivery_date_to)
    where_sql = 'WHERE ' + ' AND '.join(where_clauses) if where_clauses else ''
    valid_sort_columns = ['created_at', 'updated_at', 'total_price', 'delivery_date', 'order_no']
    if sort_by not in valid_sort_columns:
        sort_by = 'created_at'
    if sort_order not in ['asc', 'desc']:
            sort_order = 'desc'
    count_sql = f'SELECT COUNT(*) as total FROM orders {where_sql}'
    cursor.execute(count_sql, params)
    total = cursor.fetchone()['total']
    query_sql = f'''
        SELECT * FROM orders {where_sql}
        ORDER BY {sort_by} {sort_order}
        LIMIT ? OFFSET ?
    '''
    params.extend([page_size, offset])
    cursor.execute(query_sql, params)
    orders = cursor.fetchall()
    result = [dict(order) for order in orders]
    pagination = {
        'page': page,
        'page_size': page_size,
        'total': total,
        'total_pages': (total + page_size - 1) // page_size
    }
    return success_response({'list': result, 'pagination': pagination}, '获取订单列表成功')

@app.route('/api/orders/<order_no>', methods=['GET'])
def get_order(order_no):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
    order = cursor.fetchone()
    if order is None:
        return error_response('订单不存在', 404)
    return success_response(dict(order), '获取订单详情成功')

@app.route('/api/orders/<order_no>/status', methods=['PUT'])
def update_order_status(order_no):
    data = request.get_json()
    if 'status' not in data:
        return error_response('缺少status字段')
    if data['status'] not in ORDER_STATUSES:
        return error_response(f'状态必须是以下之一: {ORDER_STATUSES}')
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
    if cursor.fetchone() is None:
        return error_response('订单不存在', 404)
    now = datetime.datetime.now().isoformat()
    try:
        cursor.execute('''
            UPDATE orders SET status = ?, updated_at = ? WHERE order_no = ?
        ''', (data['status'], now, order_no))
        db.commit()
        return success_response(None, '状态更新成功')
    except Exception as e:
        db.rollback()
        return error_response(f'更新失败: {str(e)}', 500)

@app.route('/api/orders/<order_no>/craftsman', methods=['PUT'])
def assign_craftsman(order_no):
    data = request.get_json()
    if 'craftsman_id' not in data or 'craftsman_name' not in data:
        return error_response('缺少craftsman_id或craftsman_name字段')
    craftsman_ids = [c['id'] for c in CRAFTSMEN]
    if int(data['craftsman_id']) not in craftsman_ids:
        return error_response('匠人不存在')
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
    if cursor.fetchone() is None:
        return error_response('订单不存在', 404)
    now = datetime.datetime.now().isoformat()
    try:
        cursor.execute('''
            UPDATE orders SET craftsman_id = ?, craftsman_name = ?, updated_at = ? WHERE order_no = ?
        ''', (data['craftsman_id'], data['craftsman_name'], now, order_no))
        db.commit()
        return success_response(None, '匠人分配成功')
    except Exception as e:
        db.rollback()
        return error_response(f'分配失败: {str(e)}', 500)

@app.route('/api/orders/<order_no>', methods=['DELETE'])
def delete_order(order_no):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
    if cursor.fetchone() is None:
        return error_response('订单不存在', 404)
    try:
        cursor.execute('DELETE FROM orders WHERE order_no = ?', (order_no,))
        db.commit()
        return success_response(None, '订单删除成功')
    except Exception as e:
        db.rollback()
        return error_response(f'删除失败: {str(e)}', 500)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    db = get_db()
    cursor = db.cursor()
    stats = {}
    for status in ORDER_STATUSES:
        cursor.execute('SELECT COUNT(*) as count FROM orders WHERE status = ?', (status,))
        result = cursor.fetchone()
        stats[status] = result['count']
    cursor.execute('SELECT COUNT(*) as total FROM orders')
    stats['total'] = cursor.fetchone()['total']
    cursor.execute('SELECT SUM(total_price) as total_amount FROM orders')
    result = cursor.fetchone()
    stats['total_amount'] = result['total_amount'] or 0
    return success_response(stats, '获取统计成功')

if __name__ == '__main__':
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)