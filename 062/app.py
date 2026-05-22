from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import re
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
CORS(app)

DATABASE = 'seal_orders.db'

ORDER_STATUSES = [
    '待接单',
    '选料',
    '切坯',
    '打磨',
    '篆刻',
    '抛光',
    '刻边款',
    '完工'
]

HORN_MATERIALS = [
    {'value': 'black_buffalo', 'label': '黑水牛角', 'description': '质地坚硬，色泽乌黑，密度高', 'price': 120},
    {'value': 'white_buffalo', 'label': '白水牛角', 'description': '质地细腻，色泽乳白，韧性好', 'price': 150},
    {'value': 'yellow_buffalo', 'label': '黄花牛角', 'description': '色泽金黄，纹理清晰，观赏性强', 'price': 180},
    {'value': 'yak', 'label': '牦牛角', 'description': '高原材质，质地致密，稀缺珍贵', 'price': 280},
    {'value': 'rhinoceros', 'label': '犀牛角(仿)', 'description': '仿真纹理，色泽接近，性价比高', 'price': 380}
]

SEAL_SPECIFICATIONS = [
    {'value': 'square_20', 'label': '正方形 2.0cm', 'size': '20x20mm', 'for_cutting': '20mm见方坯料', 'price_factor': 1.0},
    {'value': 'square_25', 'label': '正方形 2.5cm', 'size': '25x25mm', 'for_cutting': '25mm见方坯料', 'price_factor': 1.0},
    {'value': 'square_30', 'label': '正方形 3.0cm', 'size': '30x30mm', 'for_cutting': '30mm见方坯料', 'price_factor': 1.2},
    {'value': 'square_35', 'label': '正方形 3.5cm', 'size': '35x35mm', 'for_cutting': '35mm见方坯料', 'price_factor': 1.4},
    {'value': 'circle_20', 'label': '圆形 2.0cm', 'size': '直径20mm', 'for_cutting': '直径20mm圆形坯料', 'price_factor': 1.0},
    {'value': 'circle_25', 'label': '圆形 2.5cm', 'size': '直径25mm', 'for_cutting': '直径25mm圆形坯料', 'price_factor': 1.0},
    {'value': 'circle_30', 'label': '圆形 3.0cm', 'size': '直径30mm', 'for_cutting': '直径30mm圆形坯料', 'price_factor': 1.2},
    {'value': 'ellipse_30x20', 'label': '椭圆形 3.0x2.0cm', 'size': '30x20mm', 'for_cutting': '30x20mm椭圆坯料', 'price_factor': 1.1},
    {'value': 'rectangle_40x20', 'label': '长方形 4.0x2.0cm', 'size': '40x20mm', 'for_cutting': '40x20mm长方坯料', 'price_factor': 1.3}
]

SEAL_STYLES = [
    {'value': 'zhuanshu_xiaozhuan', 'label': '小篆', 'description': '线条圆润，结构对称，标准篆书', 'for_carving': '线条粗细均匀，转角圆润', 'difficulty': 1.0, 'days_needed': 2},
    {'value': 'zhuanshu_dazhuan', 'label': '大篆', 'description': '古朴厚重，线条粗犷，金文风格', 'for_carving': '线条变化丰富，苍劲有力', 'difficulty': 1.2, 'days_needed': 3},
    {'value': 'zhuanshu_miaozhuan', 'label': '缪篆', 'description': '平直方正，适于印面，汉印风格', 'for_carving': '方折为主，布白均匀', 'difficulty': 1.1, 'days_needed': 2},
    {'value': 'zhuanshu_bird', 'label': '鸟虫篆', 'description': '花鸟鱼虫，装饰性强，精美华丽', 'for_carving': '线条婉转流畅，图案化处理', 'difficulty': 1.5, 'days_needed': 4},
    {'value': 'li_shu', 'label': '隶书', 'description': '蚕头燕尾，古朴典雅，汉隶风格', 'for_carving': '波磔明显，结构扁方', 'difficulty': 1.1, 'days_needed': 2},
    {'value': 'kai_shu', 'label': '楷书', 'description': '端庄工整，易于辨识，实用性强', 'for_carving': '笔画清晰，结构方正', 'difficulty': 1.0, 'days_needed': 2},
    {'value': 'xing_shu', 'label': '行书', 'description': '流畅自然，灵动飘逸，艺术性强', 'for_carving': '连带自然，节奏明快', 'difficulty': 1.3, 'days_needed': 3}
]

EDGE_STYLES = [
    {'value': 'none', 'label': '无边款', 'price_factor': 1.0},
    {'value': 'simple', 'label': '简约边款', 'price_factor': 1.1},
    {'value': 'full', 'label': '完整边款', 'price_factor': 1.2},
    {'value': 'poem', 'label': '诗文边款', 'price_factor': 1.3}
]

CRAFTSMEN = [
    {'id': 1, 'name': '张师傅', 'skill_level': '高级', 'specialty': ['zhuanshu_xiaozhuan', 'zhuanshu_dazhuan'], 'daily_capacity': 3},
    {'id': 2, 'name': '李师傅', 'skill_level': '特级', 'specialty': ['zhuanshu_bird', 'zhuanshu_miaozhuan'], 'daily_capacity': 2},
    {'id': 3, 'name': '王师傅', 'skill_level': '中级', 'specialty': ['li_shu', 'kai_shu', 'xing_shu'], 'daily_capacity': 4}
]

class ResponseCode:
    SUCCESS = 200
    CREATED = 201
    BAD_REQUEST = 400
    NOT_FOUND = 404
    INTERNAL_ERROR = 500
    VALIDATION_ERROR = 422

def api_response(code=ResponseCode.SUCCESS, message='success', data=None, **kwargs):
    response = {
        'code': code,
        'message': message,
        'timestamp': datetime.now().isoformat()
    }
    if data is not None:
        response['data'] = data
    response.update(kwargs)
    return jsonify(response), code

def validate_required(data, required_fields):
    missing = []
    for field in required_fields:
        if field not in data or data[field] is None or str(data[field]).strip() == '':
            missing.append(field)
    return missing

def validate_phone(phone):
    if not phone:
        return False
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, phone))

def validate_seal_text(text):
    if not text:
        return False
    return 1 <= len(text) <= 8

def get_material_price(material_value):
    for mat in HORN_MATERIALS:
        if mat['value'] == material_value:
            return mat['price']
    return 0

def get_spec_price_factor(spec_value):
    for spec in SEAL_SPECIFICATIONS:
        if spec['value'] == spec_value:
            return spec['price_factor']
    return 1.0

def get_style_difficulty(style_value):
    for style in SEAL_STYLES:
        if style['value'] == style_value:
            return style['difficulty'], style['days_needed']
    return 1.0, 2

def get_edge_price_factor(edge_value):
    for edge in EDGE_STYLES:
        if edge['value'] == edge_value:
            return edge['price_factor']
    return 1.0

def calculate_price(material, spec, style, edge):
    base_price = get_material_price(material)
    spec_factor = get_spec_price_factor(spec)
    style_difficulty, _ = get_style_difficulty(style)
    edge_factor = get_edge_price_factor(edge)
    
    total_price = base_price * spec_factor * style_difficulty * edge_factor
    return round(total_price, 2)

def calculate_delivery_date(style_value, status='待接单'):
    _, days_needed = get_style_difficulty(style_value)
    current_index = ORDER_STATUSES.index(status)
    remaining_statuses = len(ORDER_STATUSES) - current_index - 1
    total_days = days_needed + remaining_statuses
    delivery_date = datetime.now() + timedelta(days=total_days)
    return delivery_date.strftime('%Y-%m-%d')

def assign_craftsman(style_value):
    for craftsman in CRAFTSMEN:
        if style_value in craftsman['specialty']:
            return craftsman['id'], craftsman['name']
    return CRAFTSMEN[0]['id'], CRAFTSMEN[0]['name']

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DROP TABLE IF EXISTS orders')
    
    cursor.execute('''
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_no TEXT UNIQUE NOT NULL,
            customer_name TEXT NOT NULL,
            customer_phone TEXT NOT NULL,
            seal_text TEXT NOT NULL,
            seal_spec TEXT NOT NULL,
            seal_size TEXT,
            seal_shape TEXT,
            horn_material TEXT NOT NULL,
            seal_style TEXT NOT NULL,
            edge_style TEXT,
            for_cutting TEXT,
            for_carving TEXT,
            for_polishing TEXT,
            special_requirements TEXT,
            price REAL NOT NULL,
            craftsman_id INTEGER,
            craftsman_name TEXT,
            estimated_days INTEGER,
            delivery_date TEXT,
            status TEXT NOT NULL DEFAULT '待接单',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print('数据库初始化完成')

def generate_order_no():
    date_str = datetime.now().strftime('%Y%m%d')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT order_no FROM orders WHERE order_no LIKE ? ORDER BY order_no DESC LIMIT 1', (f'{date_str}%',))
    last_order = cursor.fetchone()
    conn.close()
    
    if last_order:
        last_no = int(last_order['order_no'][-4:])
        new_no = last_no + 1
    else:
        new_no = 1
    
    return f'{date_str}{new_no:04d}'

def get_cutting_spec(seal_spec):
    for spec in SEAL_SPECIFICATIONS:
        if spec['value'] == seal_spec:
            return spec['for_cutting']
    return ''

def get_carving_spec(seal_style):
    for style in SEAL_STYLES:
        if style['value'] == seal_style:
            return style['for_carving']
    return ''

def get_polishing_spec(horn_material):
    for material in HORN_MATERIALS:
        if material['value'] == horn_material:
            if 'black' in horn_material:
                return '高光泽度抛光，突出乌黑质感'
            elif 'white' in horn_material:
                return '柔光抛光，保持温润质感'
            elif 'yellow' in horn_material:
                return '精细抛光，展现金黄纹理'
            else:
                return '标准精细抛光'
    return '标准精细抛光'

@app.route('/api/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        
        required_fields = ['customer_name', 'customer_phone', 'seal_text', 'seal_spec', 'horn_material', 'seal_style']
        missing_fields = validate_required(data, required_fields)
        if missing_fields:
            return api_response(
                code=ResponseCode.VALIDATION_ERROR,
                message='缺少必填字段',
                errors={'missing_fields': missing_fields}
            )
        
        if not validate_phone(data['customer_phone']):
            return api_response(
                code=ResponseCode.VALIDATION_ERROR,
                message='手机号码格式不正确',
                errors={'customer_phone': '请输入正确的11位手机号码'}
            )
        
        if not validate_seal_text(data['seal_text']):
            return api_response(
                code=ResponseCode.VALIDATION_ERROR,
                message='印文内容不合法',
                errors={'seal_text': '印文长度应在1-8个字符之间'}
            )
        
        valid_materials = [m['value'] for m in HORN_MATERIALS]
        if data['horn_material'] not in valid_materials:
            return api_response(
                code=ResponseCode.VALIDATION_ERROR,
                message='牛角材质不合法',
                errors={'horn_material': f'请选择有效材质: {", ".join(valid_materials)}'}
            )
        
        valid_specs = [s['value'] for s in SEAL_SPECIFICATIONS]
        if data['seal_spec'] not in valid_specs:
            return api_response(
                code=ResponseCode.VALIDATION_ERROR,
                message='印章规格不合法',
                errors={'seal_spec': f'请选择有效规格: {", ".join(valid_specs)}'}
            )
        
        valid_styles = [s['value'] for s in SEAL_STYLES]
        if data['seal_style'] not in valid_styles:
            return api_response(
                code=ResponseCode.VALIDATION_ERROR,
                message='篆刻风格不合法',
                errors={'seal_style': f'请选择有效风格: {", ".join(valid_styles)}'}
            )
        
        edge_style = data.get('edge_style', 'none')
        valid_edges = [e['value'] for e in EDGE_STYLES]
        if edge_style not in valid_edges:
            edge_style = 'none'
        
        order_no = generate_order_no()
        
        spec_info = next((s for s in SEAL_SPECIFICATIONS if s['value'] == data['seal_spec']), {})
        seal_size = spec_info.get('size', '')
        seal_shape = '正方形' if 'square' in data['seal_spec'] else '圆形' if 'circle' in data['seal_spec'] else '其他'
        
        for_cutting = get_cutting_spec(data['seal_spec'])
        for_carving = get_carving_spec(data['seal_style'])
        for_polishing = get_polishing_spec(data['horn_material'])
        
        price = calculate_price(
            data['horn_material'],
            data['seal_spec'],
            data['seal_style'],
            edge_style
        )
        
        craftsman_id, craftsman_name = assign_craftsman(data['seal_style'])
        _, estimated_days = get_style_difficulty(data['seal_style'])
        delivery_date = calculate_delivery_date(data['seal_style'])
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO orders (
                order_no, customer_name, customer_phone, seal_text,
                seal_spec, seal_size, seal_shape, horn_material, seal_style,
                edge_style, for_cutting, for_carving, for_polishing,
                special_requirements, price, craftsman_id, craftsman_name,
                estimated_days, delivery_date, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_no,
            data['customer_name'],
            data['customer_phone'],
            data['seal_text'],
            data['seal_spec'],
            seal_size,
            seal_shape,
            data['horn_material'],
            data['seal_style'],
            edge_style,
            for_cutting,
            for_carving,
            for_polishing,
            data.get('special_requirements', ''),
            price,
            craftsman_id,
            craftsman_name,
            estimated_days,
            delivery_date,
            '待接单'
        ))
        conn.commit()
        
        order_id = cursor.lastrowid
        cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
        order = cursor.fetchone()
        conn.close()
        
        return api_response(
            code=ResponseCode.CREATED,
            message='订单创建成功',
            data=dict(order)
        )
        
    except Exception as e:
        return api_response(
            code=ResponseCode.INTERNAL_ERROR,
            message='服务器内部错误',
            errors={'detail': str(e)}
        )

@app.route('/api/orders', methods=['GET'])
def get_orders():
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        
        status = request.args.get('status')
        material = request.args.get('material')
        style = request.args.get('style')
        keyword = request.args.get('keyword')
        delivery_from = request.args.get('delivery_from')
        delivery_to = request.args.get('delivery_to')
        
        valid_sort_fields = ['created_at', 'updated_at', 'price', 'delivery_date', 'order_no']
        if sort_by not in valid_sort_fields:
            sort_by = 'created_at'
        if sort_order not in ['asc', 'desc']:
            sort_order = 'desc'
        
        if page < 1:
            page = 1
        if page_size < 1 or page_size > 100:
            page_size = 10
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM orders WHERE 1=1'
        count_query = 'SELECT COUNT(*) as total FROM orders WHERE 1=1'
        params = []
        
        if status and status in ORDER_STATUSES:
            query += ' AND status = ?'
            count_query += ' AND status = ?'
            params.append(status)
        
        if material:
            query += ' AND horn_material = ?'
            count_query += ' AND horn_material = ?'
            params.append(material)
        
        if style:
            query += ' AND seal_style = ?'
            count_query += ' AND seal_style = ?'
            params.append(style)
        
        if delivery_from:
            query += ' AND delivery_date >= ?'
            count_query += ' AND delivery_date >= ?'
            params.append(delivery_from)
        
        if delivery_to:
            query += ' AND delivery_date <= ?'
            count_query += ' AND delivery_date <= ?'
            params.append(delivery_to)
        
        if keyword:
            keyword_pattern = f'%{keyword}%'
            query += ' AND (order_no LIKE ? OR customer_name LIKE ? OR customer_phone LIKE ? OR seal_text LIKE ?)'
            count_query += ' AND (order_no LIKE ? OR customer_name LIKE ? OR customer_phone LIKE ? OR seal_text LIKE ?)'
            params.extend([keyword_pattern, keyword_pattern, keyword_pattern, keyword_pattern])
        
        cursor.execute(count_query, params)
        total = cursor.fetchone()['total']
        
        query += f' ORDER BY {sort_by} {sort_order.upper()}'
        offset = (page - 1) * page_size
        query += f' LIMIT ? OFFSET ?'
        params.extend([page_size, offset])
        
        cursor.execute(query, params)
        orders = cursor.fetchall()
        conn.close()
        
        total_pages = (total + page_size - 1) // page_size
        
        return api_response(
            message='查询成功',
            data={
                'orders': [dict(order) for order in orders],
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total': total,
                    'total_pages': total_pages,
                    'has_next': page < total_pages,
                    'has_prev': page > 1
                }
            }
        )
        
    except Exception as e:
        return api_response(
            code=ResponseCode.INTERNAL_ERROR,
            message='服务器内部错误',
            errors={'detail': str(e)}
        )

@app.route('/api/orders/<order_no>', methods=['GET'])
def get_order(order_no):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        order = cursor.fetchone()
        conn.close()
        
        if order:
            return api_response(
                message='查询成功',
                data=dict(order)
            )
        else:
            return api_response(
                code=ResponseCode.NOT_FOUND,
                message='订单不存在'
            )
    except Exception as e:
        return api_response(
            code=ResponseCode.INTERNAL_ERROR,
            message='服务器内部错误',
            errors={'detail': str(e)}
        )

@app.route('/api/orders/<order_no>/status', methods=['PUT'])
def update_order_status(order_no):
    try:
        data = request.get_json()
        
        if 'status' not in data:
            return api_response(
                code=ResponseCode.VALIDATION_ERROR,
                message='缺少状态字段',
                errors={'missing_fields': ['status']}
            )
        
        if data['status'] not in ORDER_STATUSES:
            return api_response(
                code=ResponseCode.VALIDATION_ERROR,
                message='无效的订单状态',
                errors={'status': f'有效状态: {", ".join(ORDER_STATUSES)}'}
            )
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        order = cursor.fetchone()
        
        if not order:
            conn.close()
            return api_response(
                code=ResponseCode.NOT_FOUND,
                message='订单不存在'
            )
        
        new_delivery_date = calculate_delivery_date(order['seal_style'], data['status'])
        
        cursor.execute('''
            UPDATE orders 
            SET status = ?, delivery_date = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE order_no = ?
        ''', (data['status'], new_delivery_date, order_no))
        conn.commit()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        updated_order = cursor.fetchone()
        conn.close()
        
        return api_response(
            message='状态更新成功',
            data=dict(updated_order)
        )
        
    except Exception as e:
        return api_response(
            code=ResponseCode.INTERNAL_ERROR,
            message='服务器内部错误',
            errors={'detail': str(e)}
        )

@app.route('/api/orders/<order_no>', methods=['DELETE'])
def delete_order(order_no):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        order = cursor.fetchone()
        
        if not order:
            conn.close()
            return api_response(
                code=ResponseCode.NOT_FOUND,
                message='订单不存在'
            )
        
        cursor.execute('DELETE FROM orders WHERE order_no = ?', (order_no,))
        conn.commit()
        conn.close()
        
        return api_response(
            message='订单删除成功'
        )
    except Exception as e:
        return api_response(
            code=ResponseCode.INTERNAL_ERROR,
            message='服务器内部错误',
            errors={'detail': str(e)}
        )

@app.route('/api/orders/calculate', methods=['POST'])
def calculate_order():
    try:
        data = request.get_json()
        
        required_fields = ['seal_spec', 'horn_material', 'seal_style']
        missing_fields = validate_required(data, required_fields)
        if missing_fields:
            return api_response(
                code=ResponseCode.VALIDATION_ERROR,
                message='缺少必填字段',
                errors={'missing_fields': missing_fields}
            )
        
        edge_style = data.get('edge_style', 'none')
        
        price = calculate_price(
            data['horn_material'],
            data['seal_spec'],
            data['seal_style'],
            edge_style
        )
        
        delivery_date = calculate_delivery_date(data['seal_style'])
        craftsman_id, craftsman_name = assign_craftsman(data['seal_style'])
        
        return api_response(
            message='计价成功',
            data={
                'price': price,
                'delivery_date': delivery_date,
                'craftsman': {
                    'id': craftsman_id,
                    'name': craftsman_name
                },
                'cutting_spec': get_cutting_spec(data['seal_spec']),
                'carving_spec': get_carving_spec(data['seal_style']),
                'polishing_spec': get_polishing_spec(data['horn_material'])
            }
        )
        
    except Exception as e:
        return api_response(
            code=ResponseCode.INTERNAL_ERROR,
            message='服务器内部错误',
            errors={'detail': str(e)}
        )

@app.route('/api/statuses', methods=['GET'])
def get_statuses():
    return api_response(
        message='查询成功',
        data={'statuses': ORDER_STATUSES}
    )

@app.route('/api/horn-materials', methods=['GET'])
def get_horn_materials():
    return api_response(
        message='查询成功',
        data={'materials': HORN_MATERIALS}
    )

@app.route('/api/seal-specs', methods=['GET'])
def get_seal_specs():
    return api_response(
        message='查询成功',
        data={'specifications': SEAL_SPECIFICATIONS}
    )

@app.route('/api/seal-styles', methods=['GET'])
def get_seal_styles():
    return api_response(
        message='查询成功',
        data={'styles': SEAL_STYLES}
    )

@app.route('/api/edge-styles', methods=['GET'])
def get_edge_styles():
    return api_response(
        message='查询成功',
        data={'edge_styles': EDGE_STYLES}
    )

@app.route('/api/craftsmen', methods=['GET'])
def get_craftsmen():
    return api_response(
        message='查询成功',
        data={'craftsmen': CRAFTSMEN}
    )

if __name__ == '__main__':
    init_db()
    print('服务器启动在 http://localhost:5000')
    app.run(debug=True, host='0.0.0.0', port=5000)
