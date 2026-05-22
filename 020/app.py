from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import datetime
import os
import math

app = Flask(__name__)
CORS(app)

DATABASE = 'orders.db'

ORDER_STATUSES = [
    '待接单',
    '选竹',
    '锯坯',
    '粗雕',
    '精雕',
    '打磨',
    '上漆',
    '完工'
]

BAMBOO_TYPES = {
    '毛竹': {'price': 80, 'difficulty': 1},
    '刚竹': {'price': 100, 'difficulty': 1.2},
    '紫竹': {'price': 150, 'difficulty': 1.5},
    '斑竹': {'price': 180, 'difficulty': 1.6},
    '湘妃竹': {'price': 220, 'difficulty': 1.8},
    '罗汉竹': {'price': 250, 'difficulty': 2},
    '方竹': {'price': 280, 'difficulty': 2.2},
    '金丝竹': {'price': 320, 'difficulty': 2.5}
}

CARVING_PATTERNS = {
    '梅兰竹菊': {'price': 200, 'difficulty': 2, 'days': 3},
    '山水风景': {'price': 350, 'difficulty': 3, 'days': 5},
    '花鸟虫鱼': {'price': 280, 'difficulty': 2.5, 'days': 4},
    '龙凤呈祥': {'price': 500, 'difficulty': 4, 'days': 7},
    '福寿图案': {'price': 250, 'difficulty': 2, 'days': 3},
    '云纹': {'price': 150, 'difficulty': 1.5, 'days': 2},
    '回纹': {'price': 180, 'difficulty': 1.5, 'days': 2},
    '人物故事': {'price': 450, 'difficulty': 4, 'days': 6},
    '书法文字': {'price': 200, 'difficulty': 2, 'days': 3},
    '定制图案': {'price': 400, 'difficulty': 3.5, 'days': 5}
}

PLACEMENT_CURVES = [
    '平直(0°)',
    '微弧(5°-10°)',
    '中弧(10°-20°)',
    '大弧(20°-30°)',
    '定制弧度'
]

CRAFTSMEN = [
    {'id': 1, 'name': '张师傅', 'skill_level': '高级', 'specialty': '精雕', 'daily_output': 2},
    {'id': 2, 'name': '李师傅', 'skill_level': '中级', 'specialty': '打磨', 'daily_output': 3},
    {'id': 3, 'name': '王师傅', 'skill_level': '高级', 'specialty': '上漆', 'daily_output': 4},
    {'id': 4, 'name': '赵师傅', 'skill_level': '中级', 'specialty': '粗雕', 'daily_output': 3},
    {'id': 5, 'name': '陈师傅', 'skill_level': '特级', 'specialty': '全工序', 'daily_output': 1}
]

def success_response(data=None, message='操作成功'):
    return jsonify({
        'code': 200,
        'message': message,
        'data': data,
        'success': True
    })

def error_response(message='操作失败', code=400, data=None):
    return jsonify({
        'code': code,
        'message': message,
        'data': data,
        'success': False
    }), code

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def migrate_db():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA table_info(orders)")
    columns = [col[1] for col in cursor.fetchall()]
    
    new_columns = [
        'bamboo_type', 'carving_pattern', 'placement_curve',
        'length_cm', 'width_cm', 'thickness_cm',
        'craftsman_id', 'craftsman_name', 'estimated_days',
        'delivery_date', 'unit_price', 'total_price',
        'carving_difficulty'
    ]
    
    for col in new_columns:
        if col not in columns:
            try:
                cursor.execute(f'ALTER TABLE orders ADD COLUMN {col} TEXT')
            except:
                pass
    
    conn.commit()
    conn.close()

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
            design_requirements TEXT NOT NULL,
            bamboo_type TEXT NOT NULL,
            carving_pattern TEXT NOT NULL,
            placement_curve TEXT,
            length_cm REAL NOT NULL,
            width_cm REAL NOT NULL,
            thickness_cm REAL NOT NULL,
            size_spec TEXT,
            quantity INTEGER NOT NULL DEFAULT 1,
            budget REAL,
            unit_price REAL,
            total_price REAL,
            carving_difficulty REAL,
            craftsman_id INTEGER,
            craftsman_name TEXT,
            estimated_days INTEGER,
            delivery_date TEXT,
            status TEXT NOT NULL DEFAULT '待接单',
            remark TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    migrate_db()

def calculate_price(bamboo_type, carving_pattern, quantity=1):
    bamboo_info = BAMBOO_TYPES.get(bamboo_type, {'price': 100, 'difficulty': 1})
    pattern_info = CARVING_PATTERNS.get(carving_pattern, {'price': 200, 'difficulty': 2, 'days': 3})
    
    bamboo_price = bamboo_info['price']
    pattern_price = pattern_info['price']
    difficulty = bamboo_info['difficulty'] * pattern_info['difficulty']
    
    base_price = bamboo_price + pattern_price
    unit_price = base_price * (1 + (difficulty - 1) * 0.3)
    total_price = unit_price * quantity
    
    estimated_days = math.ceil(pattern_info['days'] * quantity / 2)
    
    return {
        'unit_price': round(unit_price, 2),
        'total_price': round(total_price, 2),
        'carving_difficulty': round(difficulty, 2),
        'estimated_days': estimated_days
    }

def validate_order_data(data, is_create=True):
    errors = []
    
    required_fields = ['customer_name', 'customer_phone', 'design_requirements',
                       'bamboo_type', 'carving_pattern', 'length_cm', 'width_cm', 'thickness_cm']
    
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f'{field} 为必填项')
    
    if 'customer_phone' in data and data['customer_phone']:
        phone = str(data['customer_phone'])
        if not phone.isdigit() or len(phone) != 11:
            errors.append('手机号必须为11位数字')
    
    if 'bamboo_type' in data and data['bamboo_type']:
        if data['bamboo_type'] not in BAMBOO_TYPES:
            errors.append(f'竹材类型无效，可选值: {list(BAMBOO_TYPES.keys())}')
    
    if 'carving_pattern' in data and data['carving_pattern']:
        if data['carving_pattern'] not in CARVING_PATTERNS:
            errors.append(f'雕刻纹样无效，可选值: {list(CARVING_PATTERNS.keys())}')
    
    numeric_fields = ['length_cm', 'width_cm', 'thickness_cm', 'quantity']
    for field in numeric_fields:
        if field in data and data[field] is not None:
            try:
                val = float(data[field])
                if val <= 0:
                    errors.append(f'{field} 必须大于0')
                if field in ['length_cm', 'width_cm', 'thickness_cm'] and val > 100:
                    errors.append(f'{field} 不能超过100cm')
            except (ValueError, TypeError):
                errors.append(f'{field} 必须为有效数值')
    
    return errors

def generate_order_no():
    now = datetime.datetime.now()
    date_str = now.strftime('%Y%m%d')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT order_no FROM orders WHERE order_no LIKE ? ORDER BY order_no DESC LIMIT 1', (f'BD{date_str}%',))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        last_no = result['order_no']
        seq = int(last_no[-4:]) + 1
    else:
        seq = 1
    
    return f'BD{date_str}{seq:04d}'

@app.route('/api/options', methods=['GET'])
def get_options():
    return success_response({
        'bamboo_types': [{'name': k, 'price': v['price'], 'difficulty': v['difficulty']} for k, v in BAMBOO_TYPES.items()],
        'carving_patterns': [{'name': k, 'price': v['price'], 'difficulty': v['difficulty'], 'days': v['days']} for k, v in CARVING_PATTERNS.items()],
        'placement_curves': PLACEMENT_CURVES,
        'statuses': ORDER_STATUSES,
        'craftsmen': CRAFTSMEN
    }, '获取选项成功')

@app.route('/api/calculate', methods=['POST'])
def calculate_order_price():
    data = request.json
    
    bamboo_type = data.get('bamboo_type')
    carving_pattern = data.get('carving_pattern')
    quantity = data.get('quantity', 1)
    
    if not bamboo_type or bamboo_type not in BAMBOO_TYPES:
        return error_response('请选择有效的竹材类型')
    
    if not carving_pattern or carving_pattern not in CARVING_PATTERNS:
        return error_response('请选择有效的雕刻纹样')
    
    result = calculate_price(bamboo_type, carving_pattern, quantity)
    return success_response(result, '计价成功')

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json
    
    errors = validate_order_data(data)
    if errors:
        return error_response('数据验证失败', 400, {'errors': errors})
    
    bamboo_type = data['bamboo_type']
    carving_pattern = data['carving_pattern']
    quantity = int(data.get('quantity', 1))
    
    price_info = calculate_price(bamboo_type, carving_pattern, quantity)
    
    delivery_date = None
    if price_info['estimated_days']:
        delivery_date = (datetime.datetime.now() + datetime.timedelta(days=price_info['estimated_days'])).strftime('%Y-%m-%d')
    
    order_no = generate_order_no()
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO orders (
                order_no, customer_name, customer_phone, customer_address,
                design_requirements, bamboo_type, carving_pattern, placement_curve,
                length_cm, width_cm, thickness_cm, size_spec, quantity, budget,
                unit_price, total_price, carving_difficulty, estimated_days, delivery_date, remark
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_no,
            data['customer_name'],
            data['customer_phone'],
            data.get('customer_address', ''),
            data['design_requirements'],
            bamboo_type,
            carving_pattern,
            data.get('placement_curve', ''),
            float(data['length_cm']),
            float(data['width_cm']),
            float(data['thickness_cm']),
            data.get('size_spec', ''),
            quantity,
            data.get('budget', 0),
            price_info['unit_price'],
            price_info['total_price'],
            price_info['carving_difficulty'],
            price_info['estimated_days'],
            delivery_date,
            data.get('remark', '')
        ))
        conn.commit()
        
        order_id = cursor.lastrowid
        cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
        order = dict(cursor.fetchone())
        
        return success_response(order, '订单创建成功')
        
    except Exception as e:
        conn.rollback()
        return error_response(f'创建订单失败: {str(e)}', 500)
    finally:
        conn.close()

@app.route('/api/orders', methods=['GET'])
def get_orders():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    status = request.args.get('status')
    keyword = request.args.get('keyword')
    bamboo_type = request.args.get('bamboo_type')
    carving_pattern = request.args.get('carving_pattern')
    delivery_date_start = request.args.get('delivery_date_start')
    delivery_date_end = request.args.get('delivery_date_end')
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')
    
    valid_sort_fields = ['created_at', 'updated_at', 'delivery_date', 'total_price', 'carving_difficulty']
    if sort_by not in valid_sort_fields:
        sort_by = 'created_at'
    if sort_order not in ['asc', 'desc']:
        sort_order = 'desc'
    
    conn = get_db()
    cursor = conn.cursor()
    
    where_clauses = ['1=1']
    params = []
    
    if status:
        where_clauses.append('status = ?')
        params.append(status)
    
    if bamboo_type:
        where_clauses.append('bamboo_type = ?')
        params.append(bamboo_type)
    
    if carving_pattern:
        where_clauses.append('carving_pattern = ?')
        params.append(carving_pattern)
    
    if delivery_date_start:
        where_clauses.append('delivery_date >= ?')
        params.append(delivery_date_start)
    
    if delivery_date_end:
        where_clauses.append('delivery_date <= ?')
        params.append(delivery_date_end)
    
    if keyword:
        where_clauses.append('(order_no LIKE ? OR customer_name LIKE ? OR customer_phone LIKE ?)')
        params.extend([f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'])
    
    where_sql = ' AND '.join(where_clauses)
    
    count_sql = f'SELECT COUNT(*) as total FROM orders WHERE {where_sql}'
    cursor.execute(count_sql, params)
    total = cursor.fetchone()['total']
    
    offset = (page - 1) * page_size
    query_sql = f'''
        SELECT * FROM orders WHERE {where_sql}
        ORDER BY {sort_by} {sort_order.upper()}
        LIMIT ? OFFSET ?
    '''
    params.extend([page_size, offset])
    
    cursor.execute(query_sql, params)
    orders = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    total_pages = math.ceil(total / page_size) if page_size > 0 else 0
    
    return success_response({
        'list': orders,
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total': total,
            'total_pages': total_pages
        }
    }, '获取订单列表成功')

@app.route('/api/orders/<order_no>', methods=['GET'])
def get_order(order_no):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
    order = cursor.fetchone()
    conn.close()
    
    if not order:
        return error_response('订单不存在', 404)
    
    return success_response(dict(order), '获取订单详情成功')

@app.route('/api/orders/<order_no>/status', methods=['PUT'])
def update_order_status(order_no):
    data = request.json
    new_status = data.get('status')
    
    if new_status not in ORDER_STATUSES:
        return error_response(f'无效的状态，可选值: {ORDER_STATUSES}')
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        if not cursor.fetchone():
            conn.close()
            return error_response('订单不存在', 404)
        
        cursor.execute('''
            UPDATE orders SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE order_no = ?
        ''', (new_status, order_no))
        conn.commit()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        order = dict(cursor.fetchone())
        
        return success_response(order, '状态更新成功')
        
    except Exception as e:
        conn.rollback()
        return error_response(f'更新失败: {str(e)}', 500)
    finally:
        conn.close()

@app.route('/api/orders/<order_no>/craftsman', methods=['PUT'])
def assign_craftsman(order_no):
    data = request.json
    craftsman_id = data.get('craftsman_id')
    
    craftsman = next((c for c in CRAFTSMEN if c['id'] == craftsman_id), None)
    if not craftsman:
        return error_response('无效的匠人ID')
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        if not cursor.fetchone():
            conn.close()
            return error_response('订单不存在', 404)
        
        cursor.execute('''
            UPDATE orders SET craftsman_id = ?, craftsman_name = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE order_no = ?
        ''', (craftsman_id, craftsman['name'], order_no))
        conn.commit()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        order = dict(cursor.fetchone())
        
        return success_response(order, '匠人分配成功')
        
    except Exception as e:
        conn.rollback()
        return error_response(f'分配失败: {str(e)}', 500)
    finally:
        conn.close()

@app.route('/api/orders/<order_no>', methods=['PUT'])
def update_order(order_no):
    data = request.json
    
    errors = validate_order_data(data, is_create=False)
    if errors:
        return error_response('数据验证失败', 400, {'errors': errors})
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        existing = cursor.fetchone()
        if not existing:
            conn.close()
            return error_response('订单不存在', 404)
        
        update_fields = []
        params = []
        
        allowed_fields = [
            'customer_name', 'customer_phone', 'customer_address',
            'design_requirements', 'bamboo_type', 'carving_pattern',
            'placement_curve', 'length_cm', 'width_cm', 'thickness_cm',
            'size_spec', 'quantity', 'budget', 'delivery_date', 'remark'
        ]
        
        for field in allowed_fields:
            if field in data:
                update_fields.append(f'{field} = ?')
                params.append(data[field])
        
        if 'bamboo_type' in data or 'carving_pattern' in data or 'quantity' in data:
            bamboo = data.get('bamboo_type', existing['bamboo_type'])
            pattern = data.get('carving_pattern', existing['carving_pattern'])
            qty = data.get('quantity', existing['quantity'])
            
            price_info = calculate_price(bamboo, pattern, qty)
            update_fields.extend(['unit_price = ?', 'total_price = ?', 'carving_difficulty = ?', 'estimated_days = ?'])
            params.extend([price_info['unit_price'], price_info['total_price'], price_info['carving_difficulty'], price_info['estimated_days']])
            
            delivery_date = (datetime.datetime.now() + datetime.timedelta(days=price_info['estimated_days'])).strftime('%Y-%m-%d')
            update_fields.append('delivery_date = ?')
            params.append(delivery_date)
        
        if not update_fields:
            return error_response('没有提供要更新的字段')
        
        update_fields.append('updated_at = CURRENT_TIMESTAMP')
        params.append(order_no)
        
        cursor.execute(f'''
            UPDATE orders SET {', '.join(update_fields)} WHERE order_no = ?
        ''', params)
        conn.commit()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        order = dict(cursor.fetchone())
        
        return success_response(order, '订单更新成功')
        
    except Exception as e:
        conn.rollback()
        return error_response(f'更新失败: {str(e)}', 500)
    finally:
        conn.close()

@app.route('/api/orders/<order_no>', methods=['DELETE'])
def delete_order(order_no):
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        if not cursor.fetchone():
            conn.close()
            return error_response('订单不存在', 404)
        
        cursor.execute('DELETE FROM orders WHERE order_no = ?', (order_no,))
        conn.commit()
        
        return success_response(None, '订单删除成功')
        
    except Exception as e:
        conn.rollback()
        return error_response(f'删除失败: {str(e)}', 500)
    finally:
        conn.close()

@app.route('/api/statuses', methods=['GET'])
def get_statuses():
    return success_response(ORDER_STATUSES, '获取状态列表成功')

if __name__ == '__main__':
    init_db()
    print('=' * 70)
    print('传统竹雕笔搁定制订单管理系统 - 后端服务 v2.0')
    print('=' * 70)
    print('✓ 数据库初始化完成')
    print('✓ 支持必填校验与数值规范')
    print('✓ 支持按竹材与雕刻难度自动计价')
    print('✓ 支持匠人绑定与工期估算')
    print('✓ 支持多条件筛选、分页、排序')
    print('✓ 统一接口返回格式')
    print(f'✓ 竹材类型 ({len(BAMBOO_TYPES)}种): {list(BAMBOO_TYPES.keys())}')
    print(f'✓ 雕刻纹样 ({len(CARVING_PATTERNS)}种): {list(CARVING_PATTERNS.keys())}')
    print(f'✓ 匠人团队 ({len(CRAFTSMEN)}人): {[c["name"] for c in CRAFTSMEN]}')
    print('=' * 70)
    print('服务启动地址: http://localhost:5000')
    print('接口文档: 查看 API文档.md')
    print('=' * 70)
    app.run(debug=True, host='0.0.0.0', port=5000)
