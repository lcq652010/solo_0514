from flask import Flask, request, jsonify, g
from flask_cors import CORS
import sqlite3
import re
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

DATABASE = 'bamboo_orders.db'

ORDER_STATUSES = [
    '待接单',
    '选竹',
    '破篾',
    '蒸煮',
    '编织',
    '定型',
    '打磨',
    '完工'
]

SPEC_DICT = {
    'bamboo_types': [
        '毛竹', '慈竹', '水竹', '楠竹', '桂竹', '苦竹', '斑竹', '紫竹'
    ],
    'strip_thickness': [
        '0.3mm（极细）', '0.5mm（细）', '0.8mm（中细）', '1.0mm（中）',
        '1.2mm（中粗）', '1.5mm（粗）', '2.0mm（特粗）'
    ],
    'weaving_patterns': [
        '人字纹', '回字纹', '菱形纹', '十字纹', '六角纹',
        '龟甲纹', '万字纹', '祥云纹', '梅花纹', '竹节纹'
    ],
    'size_specs': [
        '10cm × 6cm（小品）', '12cm × 7cm（小号）', '15cm × 8cm（中号）',
        '18cm × 9cm（大号）', '20cm × 10cm（特大）', '定制尺寸'
    ]
}

CRAFTSMEN = [
    {'id': 1, 'name': '张师傅', 'skill_level': '高级', 'daily_capacity': 5},
    {'id': 2, 'name': '李师傅', 'skill_level': '中级', 'daily_capacity': 8},
    {'id': 3, 'name': '王师傅', 'skill_level': '高级', 'daily_capacity': 6},
    {'id': 4, 'name': '陈师傅', 'skill_level': '初级', 'daily_capacity': 10}
]

PRICING_RULES = {
    'bamboo_base': {
        '毛竹': 20, '慈竹': 25, '水竹': 30, '楠竹': 35,
        '桂竹': 40, '苦竹': 45, '斑竹': 55, '紫竹': 65
    },
    'thickness_multiplier': {
        '0.3mm（极细）': 2.5, '0.5mm（细）': 2.0, '0.8mm（中细）': 1.5,
        '1.0mm（中）': 1.2, '1.2mm（中粗）': 1.0, '1.5mm（粗）': 0.9,
        '2.0mm（特粗）': 0.85
    },
    'pattern_complexity': {
        '人字纹': 1.0, '回字纹': 1.2, '菱形纹': 1.3, '十字纹': 1.1,
        '六角纹': 1.4, '龟甲纹': 1.6, '万字纹': 1.5, '祥云纹': 1.7,
        '梅花纹': 1.8, '竹节纹': 1.2
    },
    'size_base_price': {
        '10cm × 6cm（小品）': 30, '12cm × 7cm（小号）': 40,
        '15cm × 8cm（中号）': 50, '18cm × 9cm（大号）': 65,
        '20cm × 10cm（特大）': 80, '定制尺寸': 100
    }
}

WORK_DAYS_PER_STATUS = {
    '待接单': 0, '选竹': 1, '破篾': 2, '蒸煮': 1,
    '编织': 3, '定型': 2, '打磨': 1, '完工': 0
}

def success_response(data=None, message='操作成功', code=200):
    response = {
        'code': code,
        'success': True,
        'message': message,
        'timestamp': datetime.now().isoformat()
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), code

def error_response(message='操作失败', code=400, errors=None):
    response = {
        'code': code,
        'success': False,
        'message': message,
        'timestamp': datetime.now().isoformat()
    }
    if errors:
        response['errors'] = errors
    return jsonify(response), code

def validate_phone(phone):
    if not phone:
        return False, '手机号不能为空'
    if not re.match(r'^1[3-9]\d{9}$', phone):
        return False, '手机号格式不正确'
    return True, ''

def validate_quantity(quantity):
    if not quantity:
        return False, '数量不能为空'
    try:
        qty = int(quantity)
        if qty <= 0:
            return False, '数量必须大于0'
        if qty > 1000:
            return False, '数量不能超过1000'
    except (ValueError, TypeError):
        return False, '数量必须是有效数字'
    return True, ''

def validate_order_data(data, is_update=False):
    errors = {}
    if not is_update:
        required_fields = ['customer_name', 'phone', 'style', 'size', 'quantity']
        for field in required_fields:
            if field not in data or not data[field]:
                errors[field] = f'{field}为必填项'
    if 'phone' in data:
        valid, msg = validate_phone(data.get('phone'))
        if not valid:
            errors['phone'] = msg
    if 'quantity' in data:
        valid, msg = validate_quantity(data.get('quantity'))
        if not valid:
            errors['quantity'] = msg
    if 'bamboo_type' in data and data['bamboo_type']:
        if data['bamboo_type'] not in SPEC_DICT['bamboo_types']:
            errors['bamboo_type'] = '无效的竹材种类'
    if 'strip_thickness' in data and data['strip_thickness']:
        if data['strip_thickness'] not in SPEC_DICT['strip_thickness']:
            errors['strip_thickness'] = '无效的篾丝粗细'
    if 'weaving_pattern' in data and data['weaving_pattern']:
        if data['weaving_pattern'] not in SPEC_DICT['weaving_patterns']:
            errors['weaving_pattern'] = '无效的编织纹样'
    if 'size_spec' in data and data['size_spec']:
        if data['size_spec'] not in SPEC_DICT['size_specs']:
            errors['size_spec'] = '无效的尺寸规格'
    return len(errors) == 0, errors

def calculate_price(data):
    bamboo_type = data.get('bamboo_type', '毛竹') or '毛竹'
    size_spec = data.get('size_spec', '15cm × 8cm（中号）') or '15cm × 8cm（中号）'
    strip_thickness = data.get('strip_thickness', '1.0mm（中）') or '1.0mm（中）'
    weaving_pattern = data.get('weaving_pattern', '人字纹') or '人字纹'
    quantity = data.get('quantity', 1) or 1
    try:
        quantity = int(quantity)
    except (ValueError, TypeError):
        quantity = 1
    bamboo_cost = PRICING_RULES['bamboo_base'].get(bamboo_type, 20)
    size_cost = PRICING_RULES['size_base_price'].get(size_spec, 50)
    thickness_mult = PRICING_RULES['thickness_multiplier'].get(strip_thickness, 1.0)
    pattern_mult = PRICING_RULES['pattern_complexity'].get(weaving_pattern, 1.0)
    unit_price = (bamboo_cost + size_cost) * thickness_mult * pattern_mult
    total_price = round(unit_price * quantity, 2)
    return {
        'unit_price': round(unit_price, 2),
        'total_price': total_price,
        'breakdown': {
            'bamboo_cost': bamboo_cost,
            'size_cost': size_cost,
            'thickness_multiplier': thickness_mult,
            'pattern_multiplier': pattern_mult,
            'quantity': quantity
        }
    }

def calculate_lead_time(craftsman_id, quantity):
    craftsman = next((c for c in CRAFTSMEN if c['id'] == craftsman_id), None)
    if not craftsman:
        return None
    total_work_days = sum(WORK_DAYS_PER_STATUS.values())
    daily_capacity = craftsman['daily_capacity']
    batches = (quantity + daily_capacity - 1) // daily_capacity
    total_days = total_work_days * batches
    estimated_delivery = datetime.now() + timedelta(days=total_days)
    return {
        'work_days': total_days,
        'estimated_delivery': estimated_delivery.strftime('%Y-%m-%d'),
        'craftsman': craftsman
    }

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
        new_columns = [
            ('bamboo_type', 'TEXT'),
            ('size_spec', 'TEXT'),
            ('strip_thickness', 'TEXT'),
            ('weaving_pattern', 'TEXT'),
            ('unit_price', 'REAL DEFAULT 0'),
            ('total_price', 'REAL DEFAULT 0'),
            ('craftsman_id', 'INTEGER'),
            ('craftsman_name', 'TEXT'),
            ('estimated_delivery', 'TEXT'),
            ('price_breakdown', 'TEXT')
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
                phone TEXT NOT NULL,
                email TEXT,
                address TEXT,
                style TEXT NOT NULL,
                size TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                bamboo_type TEXT,
                size_spec TEXT,
                strip_thickness TEXT,
                weaving_pattern TEXT,
                pattern_description TEXT,
                special_requirements TEXT,
                unit_price REAL DEFAULT 0,
                total_price REAL DEFAULT 0,
                price_breakdown TEXT,
                craftsman_id INTEGER,
                craftsman_name TEXT,
                estimated_delivery TEXT,
                status TEXT NOT NULL DEFAULT '待接单',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()
        migrate_db()

def generate_order_no():
    now = datetime.now()
    date_prefix = now.strftime('%Y%m%d')
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT order_no FROM orders WHERE order_no LIKE ? ORDER BY order_no DESC LIMIT 1', (f'{date_prefix}%',))
    last_order = cursor.fetchone()
    if last_order:
        last_num = int(last_order['order_no'][8:])
        new_num = last_num + 1
    else:
        new_num = 1
    return f'{date_prefix}{new_num:04d}'

@app.route('/')
def index():
    return success_response({
        'name': '传统竹编茶则定制订单管理系统',
        'version': '2.0',
        'status': '运行中'
    })

@app.route('/api/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json() or {}
        valid, errors = validate_order_data(data)
        if not valid:
            return error_response('数据验证失败', 400, errors)
        order_no = generate_order_no()
        pricing = calculate_price(data)
        craftsman_id = data.get('craftsman_id')
        lead_time = None
        craftsman_name = None
        estimated_delivery = None
        if craftsman_id:
            try:
                craftsman_id = int(craftsman_id)
                lead_time = calculate_lead_time(craftsman_id, int(data['quantity']))
                if lead_time:
                    craftsman_name = lead_time['craftsman']['name']
                    estimated_delivery = lead_time['estimated_delivery']
            except (ValueError, TypeError):
                pass
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO orders (
                order_no, customer_name, phone, email, address,
                style, size, quantity, bamboo_type, size_spec,
                strip_thickness, weaving_pattern, pattern_description,
                special_requirements, unit_price, total_price,
                price_breakdown, craftsman_id, craftsman_name, estimated_delivery
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_no,
            data['customer_name'],
            data['phone'],
            data.get('email', ''),
            data.get('address', ''),
            data['style'],
            data['size'],
            int(data['quantity']),
            data.get('bamboo_type', ''),
            data.get('size_spec', ''),
            data.get('strip_thickness', ''),
            data.get('weaving_pattern', ''),
            data.get('pattern_description', ''),
            data.get('special_requirements', ''),
            pricing['unit_price'],
            pricing['total_price'],
            str(pricing['breakdown']),
            craftsman_id,
            craftsman_name or '',
            estimated_delivery or ''
        ))
        db.commit()
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        order = cursor.fetchone()
        order_dict = dict(order)
        order_dict['pricing'] = pricing
        if lead_time:
            order_dict['lead_time'] = lead_time
        return success_response(order_dict, '订单创建成功', 201)
    except Exception as e:
        return error_response(f'创建订单失败: {str(e)}', 500)

@app.route('/api/orders', methods=['GET'])
def get_orders():
    try:
        page = max(1, int(request.args.get('page', 1)))
        page_size = min(100, max(1, int(request.args.get('page_size', 10))))
        offset = (page - 1) * page_size
        status = request.args.get('status')
        weaving_pattern = request.args.get('weaving_pattern')
        delivery_date = request.args.get('delivery_date')
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        allowed_sort_fields = ['created_at', 'updated_at', 'total_price', 'estimated_delivery', 'quantity']
        if sort_by not in allowed_sort_fields:
            sort_by = 'created_at'
        if sort_order not in ['asc', 'desc']:
            sort_order = 'desc'
        where_conditions = []
        params = []
        if status:
            where_conditions.append('status = ?')
            params.append(status)
        if weaving_pattern:
            where_conditions.append('weaving_pattern = ?')
            params.append(weaving_pattern)
        if delivery_date:
            where_conditions.append('DATE(estimated_delivery) = ?')
            params.append(delivery_date)
        where_clause = ' AND '.join(where_conditions) if where_conditions else '1=1'
        db = get_db()
        cursor = db.cursor()
        count_query = f'SELECT COUNT(*) as total FROM orders WHERE {where_clause}'
        cursor.execute(count_query, params)
        total = cursor.fetchone()['total']
        query = f'''
            SELECT * FROM orders WHERE {where_clause}
            ORDER BY {sort_by} {sort_order}
            LIMIT ? OFFSET ?
        '''
        params.extend([page_size, offset])
        cursor.execute(query, params)
        orders = cursor.fetchall()
        data = {
            'list': [dict(order) for order in orders],
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total': total,
                'total_pages': (total + page_size - 1) // page_size
            }
        }
        return success_response(data, '获取订单列表成功')
    except Exception as e:
        return error_response(f'获取订单列表失败: {str(e)}', 500)

@app.route('/api/orders/<order_no>', methods=['GET'])
def get_order(order_no):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        order = cursor.fetchone()
        if not order:
            return error_response('订单不存在', 404)
        return success_response(dict(order), '获取订单详情成功')
    except Exception as e:
        return error_response(f'获取订单详情失败: {str(e)}', 500)

@app.route('/api/orders/<order_no>/status', methods=['PUT'])
def update_order_status(order_no):
    try:
        data = request.get_json() or {}
        if 'status' not in data:
            return error_response('缺少 status 字段', 400)
        if data['status'] not in ORDER_STATUSES:
            return error_response('无效的订单状态', 400)
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        order = cursor.fetchone()
        if not order:
            return error_response('订单不存在', 404)
        cursor.execute('''
            UPDATE orders 
            SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE order_no = ?
        ''', (data['status'], order_no))
        db.commit()
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        updated_order = cursor.fetchone()
        return success_response(dict(updated_order), '状态更新成功')
    except Exception as e:
        return error_response(f'状态更新失败: {str(e)}', 500)

@app.route('/api/orders/<order_no>', methods=['PUT'])
def update_order(order_no):
    try:
        data = request.get_json() or {}
        valid, errors = validate_order_data(data, is_update=True)
        if not valid:
            return error_response('数据验证失败', 400, errors)
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        order = cursor.fetchone()
        if not order:
            return error_response('订单不存在', 404)
        update_fields = []
        update_values = []
        allowed_fields = [
            'customer_name', 'phone', 'email', 'address',
            'style', 'size', 'quantity', 'bamboo_type',
            'size_spec', 'strip_thickness', 'weaving_pattern',
            'pattern_description', 'special_requirements', 'craftsman_id'
        ]
        for field in allowed_fields:
            if field in data:
                update_fields.append(f'{field} = ?')
                update_values.append(data[field])
        if any(f in ['bamboo_type', 'size_spec', 'strip_thickness', 'weaving_pattern', 'quantity'] for f in data):
            order_dict = dict(order)
            order_dict.update(data)
            pricing = calculate_price(order_dict)
            update_fields.append('unit_price = ?')
            update_fields.append('total_price = ?')
            update_fields.append('price_breakdown = ?')
            update_values.extend([pricing['unit_price'], pricing['total_price'], str(pricing['breakdown'])])
        if 'craftsman_id' in data and data['craftsman_id']:
            try:
                craftsman_id = int(data['craftsman_id'])
                qty = data.get('quantity') or order['quantity']
                lead_time = calculate_lead_time(craftsman_id, int(qty))
                if lead_time:
                    update_fields.append('craftsman_name = ?')
                    update_fields.append('estimated_delivery = ?')
                    update_values.extend([lead_time['craftsman']['name'], lead_time['estimated_delivery']])
            except (ValueError, TypeError):
                pass
        if not update_fields:
            return error_response('没有提供要更新的字段', 400)
        update_fields.append('updated_at = CURRENT_TIMESTAMP')
        update_values.append(order_no)
        cursor.execute(f'''
            UPDATE orders 
            SET {', '.join(update_fields)}
            WHERE order_no = ?
        ''', update_values)
        db.commit()
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        updated_order = cursor.fetchone()
        return success_response(dict(updated_order), '订单更新成功')
    except Exception as e:
        return error_response(f'订单更新失败: {str(e)}', 500)

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
        return error_response(f'订单删除失败: {str(e)}', 500)

@app.route('/api/statuses', methods=['GET'])
def get_statuses():
    return success_response(ORDER_STATUSES, '获取状态列表成功')

@app.route('/api/specs', methods=['GET'])
def get_specs():
    return success_response(SPEC_DICT, '获取规格字典成功')

@app.route('/api/craftsmen', methods=['GET'])
def get_craftsmen():
    return success_response(CRAFTSMEN, '获取匠人列表成功')

@app.route('/api/price/calculate', methods=['POST'])
def calculate_price_api():
    try:
        data = request.get_json() or {}
        pricing = calculate_price(data)
        return success_response(pricing, '价格计算成功')
    except Exception as e:
        return error_response(f'价格计算失败: {str(e)}', 500)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT status, COUNT(*) as count FROM orders GROUP BY status')
        status_stats = {row['status']: row['count'] for row in cursor.fetchall()}
        for status in ORDER_STATUSES:
            if status not in status_stats:
                status_stats[status] = 0
        cursor.execute('SELECT COUNT(*) as total, SUM(total_price) as revenue FROM orders')
        result = cursor.fetchone()
        total_orders = result['total'] or 0
        total_revenue = result['revenue'] or 0
        cursor.execute('SELECT weaving_pattern, COUNT(*) as count FROM orders WHERE weaving_pattern != "" GROUP BY weaving_pattern')
        pattern_stats = {row['weaving_pattern']: row['count'] for row in cursor.fetchall()}
        cursor.execute('''
            SELECT DATE(estimated_delivery) as delivery_date, COUNT(*) as count 
            FROM orders 
            WHERE estimated_delivery != '' AND status != '完工'
            GROUP BY DATE(estimated_delivery)
            ORDER BY delivery_date
            LIMIT 7
        ''')
        delivery_stats = [{'date': row['delivery_date'], 'count': row['count']} for row in cursor.fetchall()]
        return success_response({
            'total_orders': total_orders,
            'total_revenue': round(total_revenue, 2),
            'by_status': status_stats,
            'by_pattern': pattern_stats,
            'upcoming_deliveries': delivery_stats
        }, '获取统计信息成功')
    except Exception as e:
        return error_response(f'获取统计信息失败: {str(e)}', 500)

if __name__ == '__main__':
    init_db()
    app.run(debug=False, host='127.0.0.1', port=5000)
