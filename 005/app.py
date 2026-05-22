from flask import Flask, request, jsonify, g
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime, timedelta
import re

app = Flask(__name__)
CORS(app)

DATABASE = 'fan_orders.db'

ORDER_STATUSES = [
    '待接单',
    '选骨',
    '裱扇',
    '绘图',
    '题字',
    '上胶',
    '晾干',
    '成品完工'
]

PRICE_CONFIG = {
    'bone_materials': {
        '紫檀木': 200,
        '黄花梨': 250,
        '鸡翅木': 150,
        '红木': 180,
        '檀木': 160,
        '竹制': 50,
        '玉竹': 80,
        '湘妃竹': 120,
        '牛骨': 300,
        '象牙': 500
    },
    'painting_styles': {
        '工笔': 300,
        '写意': 200,
        '兼工带写': 250,
        '没骨': 280,
        '白描': 150,
        '泼墨': 220
    },
    'calligraphy_styles': {
        '楷书': 150,
        '行书': 120,
        '草书': 100,
        '隶书': 130,
        '篆书': 180,
        '瘦金体': 200
    },
    'paper_types': {
        '生宣': 50,
        '熟宣': 60,
        '半熟宣': 55,
        '夹江宣': 40,
        '皮纸': 70,
        '绢本': 100
    },
    'fan_sizes': {
        '5寸': 50,
        '6寸': 60,
        '7寸': 70,
        '8寸': 80,
        '9寸': 90,
        '10寸': 100,
        '12寸': 120,
        '14寸': 150
    },
    'difficulty_multiplier': {
        '简单': 1.0,
        '中等': 1.3,
        '复杂': 1.6,
        '大师级': 2.0
    }
}

FIELD_OPTIONS = {
    'fan_types': ['折扇', '团扇', '挂扇', '广告扇', '工艺扇'],
    'fan_shapes': ['圆形', '方形', '花瓣形', '芭蕉形', '海棠形'],
    'fan_sizes': ['5寸', '6寸', '7寸', '8寸', '9寸', '10寸', '12寸', '14寸'],
    'bone_materials': ['紫檀木', '黄花梨', '鸡翅木', '红木', '檀木', '竹制', '玉竹', '湘妃竹', '牛骨', '象牙'],
    'bone_colors': ['原木色', '深棕色', '黑色', '红色', '金色', '白色'],
    'bone_grades': ['普通', '精品', '珍藏级', '大师级'],
    'paper_types': ['生宣', '熟宣', '半熟宣', '夹江宣', '皮纸', '绢本'],
    'paper_origins': ['安徽泾县', '浙江绍兴', '四川夹江', '云南丽江', '福建'],
    'paper_grades': ['普通', '精品', '特净', '净皮', '棉料'],
    'paper_colors': ['白色', '仿古', '米色', '青色', '黄色', '红色'],
    'painting_styles': ['工笔', '写意', '兼工带写', '没骨', '白描', '泼墨'],
    'calligraphy_styles': ['楷书', '行书', '草书', '隶书', '篆书', '瘦金体'],
    'mounting_materials': ['绫绢', '锦缎', '丝绸', '棉布', '麻布'],
    'mounting_styles': ['卷轴', '镜片', '册页', '横幅', '竖幅', '斗方'],
    'glue_types': ['浆糊', '白乳胶', '淀粉胶', '糯米胶'],
    'drying_methods': ['自然阴干', '烘干', '风干', '恒温晾干'],
    'seal_options': ['不需要', '朱文', '白文', '朱白相间', '多枚印章'],
    'difficulty_levels': ['简单', '中等', '复杂', '大师级']
}

CRAFTSMEN = [
    {'id': 1, 'name': '张师傅', 'specialty': '工笔,楷书', 'rating': 4.8, 'capacity': 3},
    {'id': 2, 'name': '李师傅', 'specialty': '写意,行书', 'rating': 4.9, 'capacity': 5},
    {'id': 3, 'name': '王师傅', 'specialty': '泼墨,草书', 'rating': 4.7, 'capacity': 4},
    {'id': 4, 'name': '陈大师', 'specialty': '工笔,隶书,篆书', 'rating': 5.0, 'capacity': 2},
    {'id': 5, 'name': '刘师傅', 'specialty': '兼工带写,瘦金体', 'rating': 4.6, 'capacity': 4}
]

WORK_DAYS = {
    '待接单': 0,
    '选骨': 1,
    '裱扇': 2,
    '绘图': 3,
    '题字': 2,
    '上胶': 1,
    '晾干': 2,
    '成品完工': 0
}

def success_response(data=None, message='操作成功'):
    return jsonify({
        'code': 200,
        'message': message,
        'data': data
    })

def error_response(message='操作失败', code=400):
    return jsonify({
        'code': code,
        'message': message,
        'data': None
    }), code

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
            ('bone_quantity', 'INTEGER'),
            ('bone_color', 'TEXT'),
            ('bone_grade', 'TEXT'),
            ('fan_shape', 'TEXT'),
            ('fan_folds', 'INTEGER'),
            ('painting_content', 'TEXT'),
            ('calligraphy_content', 'TEXT'),
            ('painting_style', 'TEXT'),
            ('calligraphy_style', 'TEXT'),
            ('calligraphy_text', 'TEXT'),
            ('seal_requirement', 'TEXT'),
            ('paper_origin', 'TEXT'),
            ('paper_grade', 'TEXT'),
            ('paper_color', 'TEXT'),
            ('mounting_material', 'TEXT'),
            ('mounting_style', 'TEXT'),
            ('glue_type', 'TEXT'),
            ('drying_method', 'TEXT'),
            ('difficulty_level', 'TEXT'),
            ('craftsman_id', 'INTEGER'),
            ('craftsman_name', 'TEXT'),
            ('estimated_days', 'INTEGER'),
            ('estimated_delivery', 'TIMESTAMP'),
            ('actual_delivery', 'TIMESTAMP')
        ]
        
        for col_name, col_type in new_columns:
            if col_name not in columns:
                try:
                    cursor.execute(f'ALTER TABLE orders ADD COLUMN {col_name} {col_type}')
                except sqlite3.OperationalError:
                    pass
        
        db.commit()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'")
        table_exists = cursor.fetchone() is not None
        
        if not table_exists:
            cursor.execute('''
                CREATE TABLE orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_no TEXT UNIQUE NOT NULL,
                    customer_name TEXT NOT NULL,
                    customer_phone TEXT NOT NULL,
                    customer_address TEXT,
                    fan_type TEXT NOT NULL,
                    fan_size TEXT NOT NULL,
                    fan_shape TEXT,
                    fan_folds INTEGER,
                    bone_material TEXT NOT NULL,
                    bone_quantity INTEGER,
                    bone_color TEXT,
                    bone_grade TEXT,
                    paper_type TEXT NOT NULL,
                    paper_origin TEXT,
                    paper_grade TEXT,
                    paper_color TEXT,
                    content_requirement TEXT NOT NULL,
                    painting_content TEXT,
                    calligraphy_content TEXT,
                    painting_style TEXT,
                    calligraphy_style TEXT,
                    calligraphy_text TEXT,
                    seal_requirement TEXT,
                    mounting_material TEXT,
                    mounting_style TEXT,
                    glue_type TEXT,
                    drying_method TEXT,
                    difficulty_level TEXT,
                    craftsman_id INTEGER,
                    craftsman_name TEXT,
                    estimated_days INTEGER,
                    estimated_delivery TIMESTAMP,
                    actual_delivery TIMESTAMP,
                    special_requirement TEXT,
                    status TEXT NOT NULL DEFAULT '待接单',
                    total_price REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
        else:
            migrate_db()
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_order_no ON orders(order_no)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_status ON orders(status)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_painting_style ON orders(painting_style)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_craftsman ON orders(craftsman_id)
        ''')
        db.commit()

def validate_order_data(data):
    required_fields = ['customer_name', 'customer_phone', 'fan_type', 'fan_size', 
                       'bone_material', 'paper_type', 'content_requirement']
    
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f'缺少必填字段: {field}'
    
    if len(data['customer_name']) < 2 or len(data['customer_name']) > 50:
        return False, '客户姓名长度应在2-50字符之间'
    
    if not re.match(r'^1[3-9]\d{9}$', data['customer_phone']):
        return False, '手机号码格式不正确'
    
    if data['fan_type'] not in FIELD_OPTIONS['fan_types']:
        return False, f'扇子类型必须是: {", ".join(FIELD_OPTIONS["fan_types"])}'
    
    if data['fan_size'] not in FIELD_OPTIONS['fan_sizes']:
        return False, f'扇子尺寸必须是: {", ".join(FIELD_OPTIONS["fan_sizes"])}'
    
    if data['bone_material'] not in FIELD_OPTIONS['bone_materials']:
        return False, f'扇骨材质必须是: {", ".join(FIELD_OPTIONS["bone_materials"])}'
    
    if data['paper_type'] not in FIELD_OPTIONS['paper_types']:
        return False, f'宣纸类型必须是: {", ".join(FIELD_OPTIONS["paper_types"])}'
    
    if 'bone_quantity' in data and data['bone_quantity'] is not None:
        if not isinstance(data['bone_quantity'], int) or data['bone_quantity'] < 1 or data['bone_quantity'] > 50:
            return False, '扇骨数量必须是1-50之间的整数'
    
    if 'fan_folds' in data and data['fan_folds'] is not None:
        if not isinstance(data['fan_folds'], int) or data['fan_folds'] < 1 or data['fan_folds'] > 30:
            return False, '扇面折数必须是1-30之间的整数'
    
    return True, '验证通过'

def calculate_price(data):
    total = 0
    
    total += PRICE_CONFIG['bone_materials'].get(data['bone_material'], 100)
    
    total += PRICE_CONFIG['paper_types'].get(data['paper_type'], 50)
    
    total += PRICE_CONFIG['fan_sizes'].get(data['fan_size'], 80)
    
    if 'painting_style' in data and data['painting_style']:
        total += PRICE_CONFIG['painting_styles'].get(data['painting_style'], 200)
    
    if 'calligraphy_style' in data and data['calligraphy_style']:
        total += PRICE_CONFIG['calligraphy_styles'].get(data['calligraphy_style'], 120)
    
    difficulty = data.get('difficulty_level', '中等')
    multiplier = PRICE_CONFIG['difficulty_multiplier'].get(difficulty, 1.3)
    
    return round(total * multiplier, 2)

def calculate_estimated_days(status):
    current_index = ORDER_STATUSES.index(status)
    remaining_days = sum(WORK_DAYS[s] for s in ORDER_STATUSES[current_index:])
    return remaining_days

def assign_craftsman(data):
    painting_style = data.get('painting_style', '')
    calligraphy_style = data.get('calligraphy_style', '')
    
    for craftsman in CRAFTSMEN:
        if painting_style and painting_style in craftsman['specialty']:
            return craftsman
        if calligraphy_style and calligraphy_style in craftsman['specialty']:
            return craftsman
    
    return CRAFTSMEN[1]

def generate_order_no():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        date_prefix = datetime.now().strftime('%Y%m%d')
        cursor.execute('SELECT order_no FROM orders WHERE order_no LIKE ? ORDER BY order_no DESC LIMIT 1', (f'{date_prefix}%',))
        result = cursor.fetchone()
        if result:
            last_no = result[0]
            match = re.search(r'(\d{4})$', last_no)
            if match:
                next_num = int(match.group(1)) + 1
            else:
                next_num = 1
        else:
            next_num = 1
        return f'{date_prefix}{next_num:04d}'

def row_to_dict(row):
    return {
        'id': row['id'],
        'order_no': row['order_no'],
        'customer_name': row['customer_name'],
        'customer_phone': row['customer_phone'],
        'customer_address': row['customer_address'],
        'fan_type': row['fan_type'],
        'fan_size': row['fan_size'],
        'fan_shape': row['fan_shape'],
        'fan_folds': row['fan_folds'],
        'bone_material': row['bone_material'],
        'bone_quantity': row['bone_quantity'],
        'bone_color': row['bone_color'],
        'bone_grade': row['bone_grade'],
        'paper_type': row['paper_type'],
        'paper_origin': row['paper_origin'],
        'paper_grade': row['paper_grade'],
        'paper_color': row['paper_color'],
        'content_requirement': row['content_requirement'],
        'painting_content': row['painting_content'],
        'calligraphy_content': row['calligraphy_content'],
        'painting_style': row['painting_style'],
        'calligraphy_style': row['calligraphy_style'],
        'calligraphy_text': row['calligraphy_text'],
        'seal_requirement': row['seal_requirement'],
        'mounting_material': row['mounting_material'],
        'mounting_style': row['mounting_style'],
        'glue_type': row['glue_type'],
        'drying_method': row['drying_method'],
        'difficulty_level': row['difficulty_level'],
        'craftsman_id': row['craftsman_id'],
        'craftsman_name': row['craftsman_name'],
        'estimated_days': row['estimated_days'],
        'estimated_delivery': row['estimated_delivery'],
        'actual_delivery': row['actual_delivery'],
        'special_requirement': row['special_requirement'],
        'status': row['status'],
        'total_price': row['total_price'],
        'created_at': row['created_at'],
        'updated_at': row['updated_at']
    }

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    
    valid, message = validate_order_data(data)
    if not valid:
        return error_response(message)
    
    order_no = generate_order_no()
    total_price = calculate_price(data)
    difficulty_level = data.get('difficulty_level', '中等')
    craftsman = assign_craftsman(data)
    estimated_days = calculate_estimated_days('待接单')
    estimated_delivery = (datetime.now() + timedelta(days=estimated_days)).strftime('%Y-%m-%d %H:%M:%S')
    
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute('''
            INSERT INTO orders (
                order_no, customer_name, customer_phone, customer_address,
                fan_type, fan_size, fan_shape, fan_folds,
                bone_material, bone_quantity, bone_color, bone_grade,
                paper_type, paper_origin, paper_grade, paper_color,
                content_requirement, painting_content, calligraphy_content,
                painting_style, calligraphy_style, calligraphy_text, seal_requirement,
                mounting_material, mounting_style, glue_type, drying_method,
                difficulty_level, craftsman_id, craftsman_name,
                estimated_days, estimated_delivery,
                special_requirement, status, total_price
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_no,
            data['customer_name'],
            data['customer_phone'],
            data.get('customer_address', ''),
            data['fan_type'],
            data['fan_size'],
            data.get('fan_shape', ''),
            data.get('fan_folds'),
            data['bone_material'],
            data.get('bone_quantity'),
            data.get('bone_color', ''),
            data.get('bone_grade', ''),
            data['paper_type'],
            data.get('paper_origin', ''),
            data.get('paper_grade', ''),
            data.get('paper_color', ''),
            data['content_requirement'],
            data.get('painting_content', ''),
            data.get('calligraphy_content', ''),
            data.get('painting_style', ''),
            data.get('calligraphy_style', ''),
            data.get('calligraphy_text', ''),
            data.get('seal_requirement', ''),
            data.get('mounting_material', ''),
            data.get('mounting_style', ''),
            data.get('glue_type', ''),
            data.get('drying_method', ''),
            difficulty_level,
            craftsman['id'],
            craftsman['name'],
            estimated_days,
            estimated_delivery,
            data.get('special_requirement', ''),
            '待接单',
            total_price
        ))
        db.commit()
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        order = cursor.fetchone()
        return success_response({
            'order': row_to_dict(order),
            'price_details': {
                'base_price': total_price / PRICE_CONFIG['difficulty_multiplier'].get(difficulty_level, 1.3),
                'difficulty_multiplier': PRICE_CONFIG['difficulty_multiplier'].get(difficulty_level, 1.3),
                'final_price': total_price
            }
        }, '订单创建成功')
    except Exception as e:
        db.rollback()
        return error_response(f'创建订单失败: {str(e)}', 500)

@app.route('/api/orders', methods=['GET'])
def get_orders():
    status = request.args.get('status')
    painting_style = request.args.get('painting_style')
    calligraphy_style = request.args.get('calligraphy_style')
    craftsman_id = request.args.get('craftsman_id')
    delivery_start = request.args.get('delivery_start')
    delivery_end = request.args.get('delivery_end')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')
    
    valid_sort_fields = ['created_at', 'updated_at', 'total_price', 'estimated_delivery']
    if sort_by not in valid_sort_fields:
        return error_response(f'排序字段必须是: {", ".join(valid_sort_fields)}')
    if sort_order not in ['asc', 'desc']:
        return error_response('排序方向必须是: asc 或 desc')
    
    offset = (page - 1) * per_page
    db = get_db()
    cursor = db.cursor()
    
    where_clauses = []
    params = []
    
    if status:
        if status not in ORDER_STATUSES:
            return error_response(f'无效的订单状态，必须是: {", ".join(ORDER_STATUSES)}')
        where_clauses.append('status = ?')
        params.append(status)
    
    if painting_style:
        if painting_style not in FIELD_OPTIONS['painting_styles']:
            return error_response(f'无效的绘画风格，必须是: {", ".join(FIELD_OPTIONS["painting_styles"])}')
        where_clauses.append('painting_style = ?')
        params.append(painting_style)
    
    if calligraphy_style:
        if calligraphy_style not in FIELD_OPTIONS['calligraphy_styles']:
            return error_response(f'无效的书法风格，必须是: {", ".join(FIELD_OPTIONS["calligraphy_styles"])}')
        where_clauses.append('calligraphy_style = ?')
        params.append(calligraphy_style)
    
    if craftsman_id:
        where_clauses.append('craftsman_id = ?')
        params.append(int(craftsman_id))
    
    if delivery_start:
        where_clauses.append('estimated_delivery >= ?')
        params.append(delivery_start)
    
    if delivery_end:
        where_clauses.append('estimated_delivery <= ?')
        params.append(delivery_end)
    
    where_sql = ' AND '.join(where_clauses) if where_clauses else '1=1'
    
    count_sql = f'SELECT COUNT(*) as total FROM orders WHERE {where_sql}'
    cursor.execute(count_sql, params)
    total = cursor.fetchone()['total']
    
    query_sql = f'''
        SELECT * FROM orders 
        WHERE {where_sql} 
        ORDER BY {sort_by} {sort_order.upper()} 
        LIMIT ? OFFSET ?
    '''
    params.extend([per_page, offset])
    cursor.execute(query_sql, params)
    orders = cursor.fetchall()
    
    return success_response({
        'orders': [row_to_dict(order) for order in orders],
        'pagination': {
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }
    })

@app.route('/api/orders/<order_no>', methods=['GET'])
def get_order(order_no):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
    order = cursor.fetchone()
    if not order:
        return error_response('订单不存在', 404)
    return success_response({'order': row_to_dict(order)})

@app.route('/api/orders/<order_no>/status', methods=['PUT'])
def update_order_status(order_no):
    data = request.get_json()
    if 'status' not in data:
        return error_response('缺少状态字段')
    
    new_status = data['status']
    if new_status not in ORDER_STATUSES:
        return error_response(f'无效的订单状态，必须是: {", ".join(ORDER_STATUSES)}')
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
    order = cursor.fetchone()
    if not order:
        return error_response('订单不存在', 404)
    
    estimated_days = calculate_estimated_days(new_status)
    estimated_delivery = (datetime.now() + timedelta(days=estimated_days)).strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        cursor.execute('''
            UPDATE orders SET status = ?, estimated_days = ?, estimated_delivery = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE order_no = ?
        ''', (new_status, estimated_days, estimated_delivery, order_no))
        db.commit()
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        updated_order = cursor.fetchone()
        return success_response({
            'order': row_to_dict(updated_order)
        }, '状态更新成功')
    except Exception as e:
        db.rollback()
        return error_response(f'更新失败: {str(e)}', 500)

@app.route('/api/orders/<order_no>', methods=['PUT'])
def update_order(order_no):
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
    order = cursor.fetchone()
    if not order:
        return error_response('订单不存在', 404)
    
    update_fields = []
    update_values = []
    allowed_fields = [
        'customer_name', 'customer_phone', 'customer_address',
        'fan_type', 'fan_size', 'fan_shape', 'fan_folds',
        'bone_material', 'bone_quantity', 'bone_color', 'bone_grade',
        'paper_type', 'paper_origin', 'paper_grade', 'paper_color',
        'content_requirement', 'painting_content', 'calligraphy_content',
        'painting_style', 'calligraphy_style', 'calligraphy_text', 'seal_requirement',
        'mounting_material', 'mounting_style', 'glue_type', 'drying_method',
        'difficulty_level', 'special_requirement'
    ]
    
    for field in allowed_fields:
        if field in data:
            update_fields.append(f'{field} = ?')
            update_values.append(data[field])
    
    if not update_fields:
        return error_response('没有提供需要更新的字段')
    
    if 'bone_material' in data or 'paper_type' in data or 'fan_size' in data or \
       'painting_style' in data or 'calligraphy_style' in data or 'difficulty_level' in data:
        current_data = dict(data)
        if 'bone_material' not in current_data:
            current_data['bone_material'] = order['bone_material']
        if 'paper_type' not in current_data:
            current_data['paper_type'] = order['paper_type']
        if 'fan_size' not in current_data:
            current_data['fan_size'] = order['fan_size']
        if 'painting_style' not in current_data:
            current_data['painting_style'] = order['painting_style']
        if 'calligraphy_style' not in current_data:
            current_data['calligraphy_style'] = order['calligraphy_style']
        if 'difficulty_level' not in current_data:
            current_data['difficulty_level'] = order['difficulty_level'] or '中等'
        
        new_price = calculate_price(current_data)
        update_fields.append('total_price = ?')
        update_values.append(new_price)
    
    if 'painting_style' in data or 'calligraphy_style' in data:
        current_data = dict(data)
        if 'painting_style' not in current_data:
            current_data['painting_style'] = order['painting_style']
        if 'calligraphy_style' not in current_data:
            current_data['calligraphy_style'] = order['calligraphy_style']
        
        craftsman = assign_craftsman(current_data)
        update_fields.append('craftsman_id = ?')
        update_values.append(craftsman['id'])
        update_fields.append('craftsman_name = ?')
        update_values.append(craftsman['name'])
    
    update_fields.append('updated_at = CURRENT_TIMESTAMP')
    update_values.append(order_no)
    
    try:
        cursor.execute(f'''
            UPDATE orders SET {', '.join(update_fields)} WHERE order_no = ?
        ''', update_values)
        db.commit()
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        updated_order = cursor.fetchone()
        return success_response({
            'order': row_to_dict(updated_order)
        }, '订单更新成功')
    except Exception as e:
        db.rollback()
        return error_response(f'更新失败: {str(e)}', 500)

@app.route('/api/orders/<order_no>', methods=['DELETE'])
def delete_order(order_no):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
    order = cursor.fetchone()
    if not order:
        return error_response('订单不存在', 404)
    try:
        cursor.execute('DELETE FROM orders WHERE order_no = ?', (order_no,))
        db.commit()
        return success_response(None, '订单删除成功')
    except Exception as e:
        db.rollback()
        return error_response(f'删除失败: {str(e)}', 500)

@app.route('/api/statuses', methods=['GET'])
def get_statuses():
    return success_response({
        'statuses': ORDER_STATUSES,
        'status_days': WORK_DAYS
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    db = get_db()
    cursor = db.cursor()
    stats = {}
    for status in ORDER_STATUSES:
        cursor.execute('SELECT COUNT(*) as count FROM orders WHERE status = ?', (status,))
        stats[status] = cursor.fetchone()['count']
    cursor.execute('SELECT COUNT(*) as total FROM orders')
    stats['total'] = cursor.fetchone()['total']
    
    cursor.execute('SELECT SUM(total_price) as revenue FROM orders')
    stats['total_revenue'] = cursor.fetchone()['revenue'] or 0
    
    return success_response({'stats': stats})

@app.route('/api/field-options', methods=['GET'])
def get_field_options():
    return success_response(FIELD_OPTIONS)

@app.route('/api/craftsmen', methods=['GET'])
def get_craftsmen():
    return success_response({
        'craftsmen': CRAFTSMEN,
        'total': len(CRAFTSMEN)
    })

@app.route('/api/price-calculate', methods=['POST'])
def price_calculate():
    data = request.get_json()
    price = calculate_price(data)
    difficulty = data.get('difficulty_level', '中等')
    base_price = price / PRICE_CONFIG['difficulty_multiplier'].get(difficulty, 1.3)
    
    return success_response({
        'base_price': round(base_price, 2),
        'difficulty_level': difficulty,
        'difficulty_multiplier': PRICE_CONFIG['difficulty_multiplier'].get(difficulty, 1.3),
        'final_price': price,
        'price_detail': {
            'bone_material': PRICE_CONFIG['bone_materials'].get(data.get('bone_material', '竹制'), 50),
            'paper_type': PRICE_CONFIG['paper_types'].get(data.get('paper_type', '生宣'), 50),
            'fan_size': PRICE_CONFIG['fan_sizes'].get(data.get('fan_size', '10寸'), 80),
            'painting_style': PRICE_CONFIG['painting_styles'].get(data.get('painting_style', ''), 0),
            'calligraphy_style': PRICE_CONFIG['calligraphy_styles'].get(data.get('calligraphy_style', ''), 0)
        }
    })

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
        print('数据库初始化完成')
    else:
        with app.app_context():
            init_db()
            migrate_db()
            print('数据库迁移完成')
    print('=' * 60)
    print('传统宣纸扇定制订单管理系统后端 v2.0 启动成功')
    print('=' * 60)
    print(f'订单状态: {", ".join(ORDER_STATUSES)}')
    print(f'匠人数量: {len(CRAFTSMEN)} 位')
    print(f'服务地址: http://localhost:5001')
    print('=' * 60)
    print('API 列表:')
    print('  POST   /api/orders          - 创建订单')
    print('  GET    /api/orders          - 获取订单列表(支持筛选、排序、分页)')
    print('  GET    /api/orders/<no>     - 获取订单详情')
    print('  PUT    /api/orders/<no>     - 更新订单(自动重算价格)')
    print('  PUT    /api/orders/<no>/status - 更新订单状态')
    print('  DELETE /api/orders/<no>     - 删除订单')
    print('  GET    /api/statuses        - 获取订单状态')
    print('  GET    /api/stats           - 获取订单统计')
    print('  GET    /api/field-options   - 获取字段选项')
    print('  GET    /api/craftsmen       - 获取匠人列表')
    print('  POST   /api/price-calculate - 价格试算')
    print('=' * 60)
    app.run(host='0.0.0.0', port=5001, debug=True)
