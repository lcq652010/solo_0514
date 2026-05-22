from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import re
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

DATABASE = 'ceramic_orders.db'

ORDER_STATUSES = [
    '待接单',
    '揉泥',
    '拉坯',
    '利坯',
    '施釉',
    '绘画',
    '烧制',
    '完工'
]

CLAY_TYPES = [
    '紫砂泥',
    '青瓷泥',
    '白瓷泥',
    '黑瓷泥',
    '陶泥',
    '高岭土',
    '汝瓷泥',
    '钧瓷泥'
]

VESSEL_SIZES = [
    '口径8cm - 小笔洗',
    '口径10cm - 标准笔洗',
    '口径12cm - 中号笔洗',
    '口径15cm - 大号笔洗',
    '口径18cm - 特大笔洗',
    '定制尺寸'
]

GLAZE_TYPES = [
    '青花瓷釉',
    '青瓷釉',
    '白瓷釉',
    '黑釉',
    '酱釉',
    '钧釉',
    '汝釉',
    '哥釉',
    '定釉',
    '透明釉',
    '颜色釉'
]

DECORATION_STYLES = [
    '山水纹饰',
    '花鸟纹饰',
    '人物纹饰',
    '龙凤纹饰',
    '缠枝莲纹',
    '祥云纹饰',
    '回纹',
    '冰裂纹',
    '开片纹',
    '素面无纹',
    '定制纹饰'
]

CRAFTSMEN = [
    '张师傅',
    '李师傅',
    '王师傅',
    '陈师傅',
    '刘师傅',
    '赵师傅'
]

CLAY_PRICE_FACTORS = {
    '紫砂泥': 1.5,
    '青瓷泥': 1.2,
    '白瓷泥': 1.0,
    '黑瓷泥': 1.1,
    '陶泥': 0.8,
    '高岭土': 1.3,
    '汝瓷泥': 1.8,
    '钧瓷泥': 1.6
}

DECORATION_COMPLEXITY = {
    '素面无纹': {'factor': 1.0, 'days': 2},
    '回纹': {'factor': 1.1, 'days': 3},
    '冰裂纹': {'factor': 1.2, 'days': 3},
    '开片纹': {'factor': 1.2, 'days': 3},
    '祥云纹饰': {'factor': 1.3, 'days': 4},
    '缠枝莲纹': {'factor': 1.4, 'days': 5},
    '花鸟纹饰': {'factor': 1.5, 'days': 5},
    '山水纹饰': {'factor': 1.7, 'days': 6},
    '人物纹饰': {'factor': 1.8, 'days': 7},
    '龙凤纹饰': {'factor': 2.0, 'days': 8},
    '定制纹饰': {'factor': 2.5, 'days': 10}
}

SIZE_BASE_PRICES = {
    '口径8cm - 小笔洗': 180,
    '口径10cm - 标准笔洗': 280,
    '口径12cm - 中号笔洗': 380,
    '口径15cm - 大号笔洗': 580,
    '口径18cm - 特大笔洗': 880,
    '定制尺寸': 680
}

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def validate_phone(phone):
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, phone))

def validate_quantity(quantity):
    return isinstance(quantity, int) and quantity > 0 and quantity <= 100

def calculate_price(vessel_size, clay_type, decoration_style, quantity=1):
    base_price = SIZE_BASE_PRICES.get(vessel_size, 280)
    clay_factor = CLAY_PRICE_FACTORS.get(clay_type, 1.0)
    deco_factor = DECORATION_COMPLEXITY.get(decoration_style, {}).get('factor', 1.0)
    total_price = base_price * clay_factor * deco_factor * quantity
    return round(total_price, 2)

def calculate_work_days(decoration_style, quantity=1):
    base_days = DECORATION_COMPLEXITY.get(decoration_style, {}).get('days', 5)
    extra_days = (quantity - 1) * 1
    return base_days + extra_days

def generate_order_no():
    now = datetime.now()
    date_str = now.strftime('%Y%m%d')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT order_no FROM orders WHERE order_no LIKE ? ORDER BY order_no DESC LIMIT 1', (f'{date_str}%',))
    result = cursor.fetchone()
    if result:
        last_no = result['order_no']
        sequence = int(last_no[-4:]) + 1
    else:
        sequence = 1
    conn.close()
    return f'{date_str}{sequence:04d}'

@app.route('/api/orders/calculate-price', methods=['POST'])
def calculate_order_price():
    data = request.get_json()
    vessel_size = data.get('vessel_size', '口径10cm - 标准笔洗')
    clay_type = data.get('clay_type', '白瓷泥')
    decoration_style = data.get('decoration_style', '素面无纹')
    quantity = data.get('quantity', 1)
    
    price = calculate_price(vessel_size, clay_type, decoration_style, quantity)
    work_days = calculate_work_days(decoration_style, quantity)
    
    return jsonify({
        'calculated_price': price,
        'estimated_work_days': work_days,
        'breakdown': {
            'base_price': SIZE_BASE_PRICES.get(vessel_size, 280),
            'clay_factor': CLAY_PRICE_FACTORS.get(clay_type, 1.0),
            'decoration_factor': DECORATION_COMPLEXITY.get(decoration_style, {}).get('factor', 1.0),
            'quantity': quantity
        }
    })

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    
    required_fields = ['customer_name', 'customer_phone', 'brush_washer_type', 'vessel_size', 'clay_type', 'glaze_type', 'decoration_style']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'缺少必填字段: {field}'}), 400
    
    if not validate_phone(data['customer_phone']):
        return jsonify({'error': '手机号码格式不正确'}), 400
    
    quantity = data.get('quantity', 1)
    if not validate_quantity(quantity):
        return jsonify({'error': '数量必须是1-100之间的整数'}), 400
    
    if data.get('clay_type') not in CLAY_TYPES:
        return jsonify({'error': '无效的泥料类型'}), 400
    
    if data.get('decoration_style') not in DECORATION_STYLES:
        return jsonify({'error': '无效的纹饰风格'}), 400
    
    order_no = generate_order_no()
    
    estimated_price = calculate_price(
        data['vessel_size'],
        data['clay_type'],
        data['decoration_style'],
        quantity
    )
    
    work_days = calculate_work_days(data['decoration_style'], quantity)
    
    delivery_date = data.get('delivery_date')
    if not delivery_date:
        delivery_date = (datetime.now() + timedelta(days=work_days + 3)).strftime('%Y-%m-%d')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO orders (
                order_no, customer_name, customer_phone, customer_address,
                brush_washer_type, size, color, design_requirements,
                quantity, estimated_price, status, remark,
                clay_type, vessel_size, glaze_type, decoration_style,
                craftsman, work_days, delivery_date,
                clay_price_factor, decoration_price_factor, base_price
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_no,
            data['customer_name'],
            data['customer_phone'],
            data.get('customer_address', ''),
            data['brush_washer_type'],
            data.get('size', data['vessel_size']),
            data.get('color', ''),
            data.get('design_requirements', ''),
            quantity,
            estimated_price,
            '待接单',
            data.get('remark', ''),
            data['clay_type'],
            data['vessel_size'],
            data['glaze_type'],
            data['decoration_style'],
            data.get('craftsman', ''),
            work_days,
            delivery_date,
            CLAY_PRICE_FACTORS.get(data['clay_type'], 1.0),
            DECORATION_COMPLEXITY.get(data['decoration_style'], {}).get('factor', 1.0),
            SIZE_BASE_PRICES.get(data['vessel_size'], 280)
        ))
        conn.commit()
        
        cursor.execute('SELECT * FROM orders WHERE id = ?', (cursor.lastrowid,))
        order = cursor.fetchone()
        conn.close()
        return jsonify(dict(order)), 201
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders', methods=['GET'])
def get_orders():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'DESC')
    
    status = request.args.get('status')
    decoration_style = request.args.get('decoration_style')
    clay_type = request.args.get('clay_type')
    craftsman = request.args.get('craftsman')
    delivery_date_from = request.args.get('delivery_date_from')
    delivery_date_to = request.args.get('delivery_date_to')
    keyword = request.args.get('keyword')
    
    valid_sort_columns = ['created_at', 'updated_at', 'delivery_date', 'estimated_price', 'quantity']
    if sort_by not in valid_sort_columns:
        sort_by = 'created_at'
    if sort_order not in ['ASC', 'DESC']:
        sort_order = 'DESC'
    
    query = 'SELECT * FROM orders WHERE 1=1'
    count_query = 'SELECT COUNT(*) as total FROM orders WHERE 1=1'
    params = []
    
    if status:
        query += ' AND status = ?'
        count_query += ' AND status = ?'
        params.append(status)
    
    if decoration_style:
        query += ' AND decoration_style = ?'
        count_query += ' AND decoration_style = ?'
        params.append(decoration_style)
    
    if clay_type:
        query += ' AND clay_type = ?'
        count_query += ' AND clay_type = ?'
        params.append(clay_type)
    
    if craftsman:
        query += ' AND craftsman = ?'
        count_query += ' AND craftsman = ?'
        params.append(craftsman)
    
    if delivery_date_from:
        query += ' AND delivery_date >= ?'
        count_query += ' AND delivery_date >= ?'
        params.append(delivery_date_from)
    
    if delivery_date_to:
        query += ' AND delivery_date <= ?'
        count_query += ' AND delivery_date <= ?'
        params.append(delivery_date_to)
    
    if keyword:
        keyword_pattern = f'%{keyword}%'
        query += ' AND (order_no LIKE ? OR customer_name LIKE ? OR customer_phone LIKE ?)'
        count_query += ' AND (order_no LIKE ? OR customer_name LIKE ? OR customer_phone LIKE ?)'
        params.extend([keyword_pattern, keyword_pattern, keyword_pattern])
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(count_query, params)
    total = cursor.fetchone()['total']
    
    query += f' ORDER BY {sort_by} {sort_order} LIMIT ? OFFSET ?'
    params.extend([per_page, (page - 1) * per_page])
    
    cursor.execute(query, params)
    orders = cursor.fetchall()
    conn.close()
    
    return jsonify({
        'data': [dict(order) for order in orders],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': (total + per_page - 1) // per_page
        }
    })

@app.route('/api/orders/<order_no>', methods=['GET'])
def get_order(order_no):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
    order = cursor.fetchone()
    conn.close()
    
    if not order:
        return jsonify({'error': '订单不存在'}), 404
    
    return jsonify(dict(order))

@app.route('/api/orders/<order_no>/status', methods=['PUT'])
def update_order_status(order_no):
    data = request.get_json()
    new_status = data.get('status')
    
    if new_status not in ORDER_STATUSES:
        return jsonify({'error': '无效的订单状态'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': '订单不存在'}), 404
    
    try:
        cursor.execute('''
            UPDATE orders SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE order_no = ?
        ''', (new_status, order_no))
        conn.commit()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        order = cursor.fetchone()
        conn.close()
        return jsonify(dict(order))
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders/<order_no>', methods=['PUT'])
def update_order(order_no):
    data = request.get_json()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
    existing_order = cursor.fetchone()
    if not existing_order:
        conn.close()
        return jsonify({'error': '订单不存在'}), 404
    
    if 'customer_phone' in data and not validate_phone(data['customer_phone']):
        conn.close()
        return jsonify({'error': '手机号码格式不正确'}), 400
    
    if 'quantity' in data and not validate_quantity(data['quantity']):
        conn.close()
        return jsonify({'error': '数量必须是1-100之间的整数'}), 400
    
    if 'craftsman' in data and data['craftsman'] not in CRAFTSMEN + ['']:
        conn.close()
        return jsonify({'error': '无效的匠人名称'}), 400
    
    update_fields = []
    params = []
    
    allowed_fields = [
        'customer_name', 'customer_phone', 'customer_address',
        'brush_washer_type', 'size', 'color', 'design_requirements',
        'quantity', 'estimated_price', 'remark',
        'clay_type', 'vessel_size', 'glaze_type', 'decoration_style',
        'craftsman', 'work_days', 'delivery_date'
    ]
    
    for field in allowed_fields:
        if field in data:
            update_fields.append(f'{field} = ?')
            params.append(data[field])
    
    if not update_fields:
        conn.close()
        return jsonify({'error': '没有可更新的字段'}), 400
    
    update_fields.append('updated_at = CURRENT_TIMESTAMP')
    params.append(order_no)
    
    try:
        cursor.execute(f'''
            UPDATE orders SET {', '.join(update_fields)} WHERE order_no = ?
        ''', params)
        conn.commit()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        order = cursor.fetchone()
        conn.close()
        return jsonify(dict(order))
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders/<order_no>', methods=['DELETE'])
def delete_order(order_no):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': '订单不存在'}), 404
    
    try:
        cursor.execute('DELETE FROM orders WHERE order_no = ?', (order_no,))
        conn.commit()
        conn.close()
        return jsonify({'message': '订单删除成功'})
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/statuses', methods=['GET'])
def get_statuses():
    return jsonify(ORDER_STATUSES)

@app.route('/api/craftsmen', methods=['GET'])
def get_craftsmen():
    return jsonify(CRAFTSMEN)

@app.route('/api/options/clay-types', methods=['GET'])
def get_clay_types():
    return jsonify([{'name': t, 'price_factor': CLAY_PRICE_FACTORS.get(t, 1.0)} for t in CLAY_TYPES])

@app.route('/api/options/vessel-sizes', methods=['GET'])
def get_vessel_sizes():
    return jsonify([{'name': s, 'base_price': SIZE_BASE_PRICES.get(s, 280)} for s in VESSEL_SIZES])

@app.route('/api/options/glaze-types', methods=['GET'])
def get_glaze_types():
    return jsonify(GLAZE_TYPES)

@app.route('/api/options/decoration-styles', methods=['GET'])
def get_decoration_styles():
    return jsonify([{
        'name': s,
        'price_factor': DECORATION_COMPLEXITY.get(s, {}).get('factor', 1.0),
        'work_days': DECORATION_COMPLEXITY.get(s, {}).get('days', 5)
    } for s in DECORATION_STYLES])

@app.route('/api/options', methods=['GET'])
def get_all_options():
    return jsonify({
        'clay_types': CLAY_TYPES,
        'vessel_sizes': VESSEL_SIZES,
        'glaze_types': GLAZE_TYPES,
        'decoration_styles': DECORATION_STYLES,
        'order_statuses': ORDER_STATUSES,
        'craftsmen': CRAFTSMEN,
        'price_factors': {
            'clay': CLAY_PRICE_FACTORS,
            'decoration': {k: v['factor'] for k, v in DECORATION_COMPLEXITY.items()}
        }
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) as total FROM orders')
    total = cursor.fetchone()['total']
    
    stats = {'total': total}
    
    for status in ORDER_STATUSES:
        cursor.execute('SELECT COUNT(*) as count FROM orders WHERE status = ?', (status,))
        stats[status] = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM orders WHERE delivery_date >= DATE("now") AND status != "完工"')
    stats['pending_delivery'] = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(DISTINCT craftsman) as count FROM orders WHERE craftsman != ""')
    stats['active_craftsmen'] = cursor.fetchone()['count']
    
    cursor.execute('SELECT SUM(estimated_price) as total FROM orders')
    result = cursor.fetchone()
    stats['total_revenue'] = result['total'] if result['total'] else 0
    
    conn.close()
    return jsonify(stats)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
