from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import datetime
import re

app = Flask(__name__)
CORS(app)

DATABASE = 'huimo_orders.db'

ORDER_STATUSES = [
    '待接单',
    '和料',
    '制墨',
    '压模',
    '描金',
    '阴干',
    '打磨',
    '完工'
]

MATERIAL_TYPES = [
    '松烟',
    '油烟',
    '漆烟',
    '松烟油烟混合',
    '朱砂墨',
    '药墨'
]

INK_STYLES = [
    '圆形墨',
    '方形墨',
    '长方形墨',
    '椭圆形墨',
    '不规则形',
    '仿古墨'
]

COMPLEXITY_LEVELS = ['简单', '普通', '复杂', '极复杂']

CRAFTSMEN = [
    {'id': 1, 'name': '张师傅', 'skill': '古法和料', 'daily_rate': 300},
    {'id': 2, 'name': '李师傅', 'skill': '精细压模', 'daily_rate': 350},
    {'id': 3, 'name': '王师傅', 'skill': '描金工艺', 'daily_rate': 400},
    {'id': 4, 'name': '赵师傅', 'skill': '全流程', 'daily_rate': 500}
]

MATERIAL_PRICES = {
    '松烟': 50,
    '油烟': 80,
    '漆烟': 120,
    '松烟油烟混合': 100,
    '朱砂墨': 200,
    '药墨': 150
}

COMPLEXITY_MULTIPLIERS = {
    '简单': 1.0,
    '普通': 1.2,
    '复杂': 1.5,
    '极复杂': 2.0
}

def success_response(data=None, message='操作成功'):
    return jsonify({
        'code': 200,
        'message': message,
        'data': data,
        'success': True
    }), 200

def error_response(message='操作失败', code=400):
    return jsonify({
        'code': code,
        'message': message,
        'data': None,
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
    
    new_columns = {
        'material_type': 'TEXT',
        'ink_style': 'TEXT',
        'spec_size': 'TEXT',
        'gilding_pattern': 'TEXT',
        'complexity': 'TEXT',
        'unit_price': 'REAL',
        'total_price': 'REAL',
        'craftsman_id': 'INTEGER',
        'craftsman_name': 'TEXT',
        'est_days': 'INTEGER',
        'delivery_date': 'TIMESTAMP'
    }
    
    for col_name, col_type in new_columns.items():
        if col_name not in columns:
            cursor.execute(f'ALTER TABLE orders ADD COLUMN {col_name} {col_type}')
    
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
            ink_type TEXT NOT NULL,
            material_type TEXT,
            weight TEXT,
            ink_style TEXT,
            spec_size TEXT,
            shape TEXT,
            pattern TEXT,
            gilding_pattern TEXT,
            complexity TEXT DEFAULT '普通',
            quantity INTEGER NOT NULL,
            unit_price REAL DEFAULT 0,
            total_price REAL DEFAULT 0,
            craftsman_id INTEGER,
            craftsman_name TEXT,
            est_days INTEGER DEFAULT 7,
            delivery_date TIMESTAMP,
            description TEXT,
            status TEXT NOT NULL DEFAULT '待接单',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    migrate_db()

def validate_phone(phone):
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, phone))

def validate_quantity(quantity):
    return isinstance(quantity, int) and quantity > 0

def validate_weight(weight):
    if not weight:
        return True
    pattern = r'^\d+(\.\d+)?(g|kg|两)?$'
    return bool(re.match(pattern, weight.lower()))

def calculate_price(material_type, quantity, complexity='普通', weight=None):
    base_price = MATERIAL_PRICES.get(material_type, 80)
    
    weight_factor = 1.0
    if weight:
        weight_match = re.search(r'(\d+(\.\d+)?)', weight)
        if weight_match:
            weight_value = float(weight_match.group(1))
            if 'kg' in weight.lower():
                weight_value *= 1000
            weight_factor = weight_value / 50.0
    
    complexity_multiplier = COMPLEXITY_MULTIPLIERS.get(complexity, 1.0)
    
    unit_price = base_price * weight_factor * complexity_multiplier
    total_price = unit_price * quantity
    
    return round(unit_price, 2), round(total_price, 2)

def calculate_delivery_date(est_days=7):
    now = datetime.datetime.now()
    delivery = now + datetime.timedelta(days=est_days)
    return delivery.strftime('%Y-%m-%d')

def estimate_work_days(complexity, quantity):
    base_days = {
        '简单': 3,
        '普通': 5,
        '复杂': 8,
        '极复杂': 12
    }.get(complexity, 5)
    
    quantity_factor = (quantity - 1) / 10.0
    return max(base_days + int(quantity_factor * 2), base_days)

def generate_order_no():
    now = datetime.datetime.now()
    date_prefix = now.strftime('%Y%m%d')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT order_no FROM orders WHERE order_no LIKE ? ORDER BY order_no DESC LIMIT 1', (f'{date_prefix}%',))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        last_no = result['order_no']
        sequence = int(last_no[-4:]) + 1
    else:
        sequence = 1
    
    return f'{date_prefix}{sequence:04d}'

@app.route('/api/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        if not data:
            return error_response('请求数据不能为空')
        
        required_fields = ['customer_name', 'customer_phone', 'ink_type', 'quantity']
        for field in required_fields:
            if field not in data or not data[field]:
                return error_response(f'缺少必填字段: {field}')
        
        if not validate_phone(data['customer_phone']):
            return error_response('手机号格式不正确')
        
        if not validate_quantity(data['quantity']):
            return error_response('数量必须是正整数')
        
        material_type = data.get('material_type', '')
        if material_type and material_type not in MATERIAL_TYPES:
            return error_response(f'墨料类型不正确，可选值: {",".join(MATERIAL_TYPES)}')
        
        ink_style = data.get('ink_style', '')
        if ink_style and ink_style not in INK_STYLES:
            return error_response(f'墨锭款式不正确，可选值: {",".join(INK_STYLES)}')
        
        complexity = data.get('complexity', '普通')
        if complexity not in COMPLEXITY_LEVELS:
            return error_response(f'工艺复杂度不正确，可选值: {",".join(COMPLEXITY_LEVELS)}')
        
        weight = data.get('weight', '')
        if weight and not validate_weight(weight):
            return error_response('重量格式不正确，例如: 50g, 100g, 1两')
        
        unit_price, total_price = calculate_price(
            material_type or '油烟', 
            data['quantity'], 
            complexity, 
            weight
        )
        
        est_days = data.get('est_days') or estimate_work_days(complexity, data['quantity'])
        delivery_date = data.get('delivery_date') or calculate_delivery_date(est_days)
        
        craftsman_id = data.get('craftsman_id')
        craftsman_name = None
        if craftsman_id:
            for c in CRAFTSMEN:
                if c['id'] == craftsman_id:
                    craftsman_name = c['name']
                    break
        
        order_no = generate_order_no()
        
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO orders (
                order_no, customer_name, customer_phone, customer_address,
                ink_type, material_type, weight, ink_style, spec_size,
                shape, pattern, gilding_pattern, complexity, quantity,
                unit_price, total_price, craftsman_id, craftsman_name,
                est_days, delivery_date, description, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_no,
            data['customer_name'],
            data['customer_phone'],
            data.get('customer_address', ''),
            data['ink_type'],
            material_type,
            weight,
            ink_style,
            data.get('spec_size', ''),
            data.get('shape', ''),
            data.get('pattern', ''),
            data.get('gilding_pattern', ''),
            complexity,
            data['quantity'],
            unit_price,
            total_price,
            craftsman_id,
            craftsman_name,
            est_days,
            delivery_date,
            data.get('description', ''),
            '待接单'
        ))
        conn.commit()
        order_id = cursor.lastrowid
        
        cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
        order = dict(cursor.fetchone())
        conn.close()
        
        return success_response({'order': order}, '订单创建成功')
        
    except Exception as e:
        return error_response(f'创建订单失败: {str(e)}', 500)

@app.route('/api/orders', methods=['GET'])
def get_orders():
    try:
        status = request.args.get('status')
        ink_style = request.args.get('ink_style')
        material_type = request.args.get('material_type')
        delivery_date_from = request.args.get('delivery_date_from')
        delivery_date_to = request.args.get('delivery_date_to')
        
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'DESC')
        
        if sort_by not in ['created_at', 'delivery_date', 'total_price', 'status', 'order_no']:
            sort_by = 'created_at'
        if sort_order.upper() not in ['ASC', 'DESC']:
            sort_order = 'DESC'
        
        offset = (page - 1) * per_page
        
        conn = get_db()
        cursor = conn.cursor()
        
        where_clauses = []
        params = []
        
        if status:
            where_clauses.append('status = ?')
            params.append(status)
        
        if ink_style:
            where_clauses.append('ink_style = ?')
            params.append(ink_style)
        
        if material_type:
            where_clauses.append('material_type = ?')
            params.append(material_type)
        
        if delivery_date_from:
            where_clauses.append('delivery_date >= ?')
            params.append(delivery_date_from)
        
        if delivery_date_to:
            where_clauses.append('delivery_date <= ?')
            params.append(delivery_date_to)
        
        where_sql = ' AND '.join(where_clauses) if where_clauses else '1=1'
        
        count_sql = f'SELECT COUNT(*) as count FROM orders WHERE {where_sql}'
        cursor.execute(count_sql, params)
        total = cursor.fetchone()['count']
        
        query_sql = f'''
            SELECT * FROM orders WHERE {where_sql} 
            ORDER BY {sort_by} {sort_order} 
            LIMIT ? OFFSET ?
        '''
        params.extend([per_page, offset])
        cursor.execute(query_sql, params)
        
        orders = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return success_response({
            'orders': orders,
            'pagination': {
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': (total + per_page - 1) // per_page
            }
        }, '获取订单列表成功')
        
    except Exception as e:
        return error_response(f'获取订单列表失败: {str(e)}', 500)

@app.route('/api/orders/<order_no>', methods=['GET'])
def get_order(order_no):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        order = cursor.fetchone()
        conn.close()
        
        if order:
            return success_response(dict(order), '获取订单详情成功')
        else:
            return error_response('订单不存在', 404)
            
    except Exception as e:
        return error_response(f'获取订单详情失败: {str(e)}', 500)

@app.route('/api/orders/<order_no>/status', methods=['PUT'])
def update_order_status(order_no):
    try:
        data = request.get_json()
        
        if 'status' not in data:
            return error_response('缺少状态字段')
        
        if data['status'] not in ORDER_STATUSES:
            return error_response(f'无效的订单状态，可选值: {",".join(ORDER_STATUSES)}')
        
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        order = cursor.fetchone()
        
        if not order:
            conn.close()
            return error_response('订单不存在', 404)
        
        cursor.execute('''
            UPDATE orders 
            SET status = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE order_no = ?
        ''', (data['status'], order_no))
        conn.commit()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        updated_order = dict(cursor.fetchone())
        conn.close()
        
        return success_response({'order': updated_order}, '状态更新成功')
        
    except Exception as e:
        return error_response(f'更新状态失败: {str(e)}', 500)

@app.route('/api/orders/<order_no>/craftsman', methods=['PUT'])
def assign_craftsman(order_no):
    try:
        data = request.get_json()
        
        if 'craftsman_id' not in data:
            return error_response('缺少匠人ID字段')
        
        craftsman_id = data['craftsman_id']
        craftsman = None
        for c in CRAFTSMEN:
            if c['id'] == craftsman_id:
                craftsman = c
                break
        
        if not craftsman:
            return error_response('无效的匠人ID')
        
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        order = cursor.fetchone()
        
        if not order:
            conn.close()
            return error_response('订单不存在', 404)
        
        cursor.execute('''
            UPDATE orders 
            SET craftsman_id = ?, craftsman_name = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE order_no = ?
        ''', (craftsman_id, craftsman['name'], order_no))
        conn.commit()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        updated_order = dict(cursor.fetchone())
        conn.close()
        
        return success_response({'order': updated_order}, '匠人分配成功')
        
    except Exception as e:
        return error_response(f'分配匠人失败: {str(e)}', 500)

@app.route('/api/orders/<order_no>', methods=['DELETE'])
def delete_order(order_no):
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        order = cursor.fetchone()
        
        if not order:
            conn.close()
            return error_response('订单不存在', 404)
        
        cursor.execute('DELETE FROM orders WHERE order_no = ?', (order_no,))
        conn.commit()
        conn.close()
        
        return success_response(None, '订单删除成功')
        
    except Exception as e:
        return error_response(f'删除订单失败: {str(e)}', 500)

@app.route('/api/statuses', methods=['GET'])
def get_statuses():
    return success_response({'statuses': ORDER_STATUSES}, '获取状态列表成功')

@app.route('/api/material-types', methods=['GET'])
def get_material_types():
    types_with_prices = [
        {'name': t, 'base_price': MATERIAL_PRICES[t]} 
        for t in MATERIAL_TYPES
    ]
    return success_response({'material_types': types_with_prices}, '获取墨料类型成功')

@app.route('/api/ink-styles', methods=['GET'])
def get_ink_styles():
    return success_response({'ink_styles': INK_STYLES}, '获取墨锭款式成功')

@app.route('/api/complexity-levels', methods=['GET'])
def get_complexity_levels():
    levels_with_multipliers = [
        {'level': l, 'multiplier': COMPLEXITY_MULTIPLIERS[l]}
        for l in COMPLEXITY_LEVELS
    ]
    return success_response({'complexity_levels': levels_with_multipliers}, '获取工艺复杂度成功')

@app.route('/api/craftsmen', methods=['GET'])
def get_craftsmen():
    return success_response({'craftsmen': CRAFTSMEN}, '获取匠人列表成功')

@app.route('/api/orders/<order_no>/production-guide', methods=['GET'])
def get_production_guide(order_no):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        order = cursor.fetchone()
        conn.close()
        
        if not order:
            return error_response('订单不存在', 404)
        
        order = dict(order)
        
        guide = {
            'order_no': order['order_no'],
            'status': order['status'],
            'total_price': order.get('total_price', 0),
            'craftsman': order.get('craftsman_name'),
            'delivery_date': order.get('delivery_date'),
            'steps': {}
        }
        
        if order.get('material_type'):
            guide['steps']['和料'] = {
                'material_type': order.get('material_type', ''),
                'weight': order.get('weight', ''),
                'unit_price': order.get('unit_price', 0),
                'guide': f'根据墨料类型「{order.get("material_type", "未指定")}」进行和料工序，注意控制配比和搅拌时间，单价: {order.get("unit_price", 0)}元/锭'
            }
        
        if order.get('ink_style') or order.get('spec_size'):
            guide['steps']['压模'] = {
                'ink_style': order.get('ink_style', ''),
                'spec_size': order.get('spec_size', ''),
                'guide': f'墨锭款式「{order.get("ink_style", "未指定")}」，规格尺寸「{order.get("spec_size", "未指定")}」，选择对应模具进行压模'
            }
        
        if order.get('gilding_pattern'):
            guide['steps']['描金'] = {
                'gilding_pattern': order.get('gilding_pattern', ''),
                'pattern': order.get('pattern', ''),
                'complexity': order.get('complexity', ''),
                'guide': f'按照纹饰描金要求「{order.get("gilding_pattern", "未指定")}」进行描金工序，工艺复杂度「{order.get("complexity", "普通")}」，注意精细度控制'
            }
        
        return success_response(guide, '获取生产指导成功')
        
    except Exception as e:
        return error_response(f'获取生产指导失败: {str(e)}', 500)

if __name__ == '__main__':
    init_db()
    print('徽墨定制订单管理系统后端启动中...')
    print('数据库初始化完成')
    print('API 地址: http://localhost:5000')
    app.run(debug=True, host='0.0.0.0', port=5000)
