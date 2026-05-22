from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime, timedelta
import uuid

app = Flask(__name__)
CORS(app)

DATABASE = 'orders.db'

STATUS_LIST = ['待接单', '选料', '切坯', '打磨', '篆刻', '抛光', '刻边款', '完工']

AGATE_TYPES = [
    '红玛瑙',
    '南红玛瑙',
    '战国红玛瑙',
    '水草玛瑙',
    '缠丝玛瑙',
    '缟玛瑙',
    '冰糖玛瑙',
    '海洋玉髓',
    '戈壁玛瑙',
    '其他'
]

SEAL_SPECIFICATIONS = [
    '1.0cm×1.0cm×5.0cm',
    '1.5cm×1.5cm×5.5cm',
    '2.0cm×2.0cm×6.0cm',
    '2.5cm×2.5cm×6.0cm',
    '3.0cm×3.0cm×6.5cm',
    '3.5cm×3.5cm×7.0cm',
    '4.0cm×4.0cm×7.0cm',
    '圆形直径2.0cm',
    '圆形直径2.5cm',
    '圆形直径3.0cm',
    '椭圆形3.0cm×2.0cm',
    '随形章',
    '定制尺寸'
]

CARVING_STYLES = [
    '汉印风格',
    '秦印风格',
    '古玺风格',
    '元朱文',
    '浙派',
    '皖派',
    '鸟虫篆',
    '肖形印',
    '细朱文',
    '满白文',
    '铁线篆',
    '现代风格',
    '定制风格'
]

EDGE_TREATMENTS = [
    '平直边',
    '圆弧边',
    '倒角边',
    '波浪边',
    '仿古边',
    '留边不打磨'
]

POLISHING_LEVELS = [
    '亚光',
    '柔光',
    '高光',
    '镜面抛光'
]

DIFFICULTY_LEVELS = ['简单', '一般', '中等', '困难', '极难']

AGATE_PRICE_MULTIPLIER = {
    '红玛瑙': 1.0,
    '南红玛瑙': 2.5,
    '战国红玛瑙': 3.0,
    '水草玛瑙': 1.5,
    '缠丝玛瑙': 1.8,
    '缟玛瑙': 1.6,
    '冰糖玛瑙': 2.0,
    '海洋玉髓': 2.2,
    '戈壁玛瑙': 1.3,
    '其他': 1.0
}

SPEC_PRICE_BASE = {
    '1.0cm×1.0cm×5.0cm': 80,
    '1.5cm×1.5cm×5.5cm': 120,
    '2.0cm×2.0cm×6.0cm': 180,
    '2.5cm×2.5cm×6.0cm': 250,
    '3.0cm×3.0cm×6.5cm': 350,
    '3.5cm×3.5cm×7.0cm': 480,
    '4.0cm×4.0cm×7.0cm': 650,
    '圆形直径2.0cm': 160,
    '圆形直径2.5cm': 220,
    '圆形直径3.0cm': 320,
    '椭圆形3.0cm×2.0cm': 200,
    '随形章': 280,
    '定制尺寸': 500
}

DIFFICULTY_MULTIPLIER = {
    '简单': 0.8,
    '一般': 1.0,
    '中等': 1.3,
    '困难': 1.8,
    '极难': 2.5
}

CARVING_STYLE_MULTIPLIER = {
    '汉印风格': 1.0,
    '秦印风格': 1.1,
    '古玺风格': 1.3,
    '元朱文': 1.4,
    '浙派': 1.2,
    '皖派': 1.25,
    '鸟虫篆': 1.8,
    '肖形印': 1.6,
    '细朱文': 1.5,
    '满白文': 1.3,
    '铁线篆': 1.7,
    '现代风格': 1.1,
    '定制风格': 2.0
}

CRAFTSMEN = [
    {'id': '1', 'name': '张师傅', 'skill_level': '高级', 'daily_capacity': 3, 'base_rate': 1.0},
    {'id': '2', 'name': '李师傅', 'skill_level': '中级', 'daily_capacity': 4, 'base_rate': 0.85},
    {'id': '3', 'name': '王师傅', 'skill_level': '高级', 'daily_capacity': 2, 'base_rate': 1.2},
    {'id': '4', 'name': '陈师傅', 'skill_level': '初级', 'daily_capacity': 5, 'base_rate': 0.7}
]

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_db_version():
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='db_version'")
        if cursor.fetchone():
            cursor.execute('SELECT version FROM db_version LIMIT 1')
            result = cursor.fetchone()
            conn.close()
            return result['version'] if result else 0
        else:
            conn.close()
            return 0
    except:
        conn.close()
        return 0

def set_db_version(version):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='db_version'")
    if not cursor.fetchone():
        cursor.execute('CREATE TABLE db_version (version INTEGER)')
        cursor.execute('INSERT INTO db_version VALUES (?)', (version,))
    else:
        cursor.execute('UPDATE db_version SET version = ?', (version,))
    conn.commit()
    conn.close()

def calculate_price(agate_type, seal_specification, carving_style, difficulty='一般'):
    base_price = SPEC_PRICE_BASE.get(seal_specification, 250)
    agate_multiplier = AGATE_PRICE_MULTIPLIER.get(agate_type, 1.0)
    style_multiplier = CARVING_STYLE_MULTIPLIER.get(carving_style, 1.0)
    difficulty_multiplier = DIFFICULTY_MULTIPLIER.get(difficulty, 1.0)
    
    total_price = base_price * agate_multiplier * style_multiplier * difficulty_multiplier
    return round(total_price, 2)

def estimate_delivery_date(carving_style, difficulty='一般'):
    style_multiplier = CARVING_STYLE_MULTIPLIER.get(carving_style, 1.0)
    difficulty_multiplier = DIFFICULTY_MULTIPLIER.get(difficulty, 1.0)
    
    base_days = 3
    estimated_days = int(base_days * style_multiplier * difficulty_multiplier)
    
    delivery_date = (datetime.now() + timedelta(days=estimated_days)).strftime('%Y-%m-%d')
    return delivery_date, estimated_days

def migrate_db():
    current_version = get_db_version()
    target_version = 3
    
    if current_version >= target_version:
        return
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'")
    has_orders_table = cursor.fetchone() is not None
    
    if has_orders_table:
        cursor.execute('''
            CREATE TABLE orders_new (
                id TEXT PRIMARY KEY,
                order_no TEXT UNIQUE NOT NULL,
                customer_name TEXT NOT NULL,
                customer_phone TEXT NOT NULL,
                agate_type TEXT NOT NULL DEFAULT '红玛瑙',
                seal_specification TEXT NOT NULL DEFAULT '2.5cm×2.5cm×6.0cm',
                inscription_content TEXT NOT NULL DEFAULT '',
                inscription_font TEXT NOT NULL DEFAULT '篆书',
                carving_style TEXT NOT NULL DEFAULT '汉印风格',
                carving_type TEXT NOT NULL DEFAULT '阳文',
                edge_treatment TEXT NOT NULL DEFAULT '平直边',
                polishing_level TEXT NOT NULL DEFAULT '高光',
                difficulty TEXT NOT NULL DEFAULT '一般',
                price REAL NOT NULL DEFAULT 0,
                craftsman_id TEXT,
                craftsman_name TEXT,
                estimated_days INTEGER,
                delivery_date TEXT,
                special_requirements TEXT,
                status TEXT NOT NULL DEFAULT '待接单',
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL
            )
        ''')
        try:
            cursor.execute('''
                INSERT INTO orders_new (id, order_no, customer_name, customer_phone, 
                                       agate_type, seal_specification, inscription_content,
                                       carving_style, special_requirements, status, created_at, updated_at)
                SELECT id, order_no, customer_name, customer_phone, 
                       agate_type, seal_specification, inscription_content,
                       carving_style, special_requirements, status, created_at, updated_at
                FROM orders
            ''')
        except:
            try:
                cursor.execute('''
                    INSERT INTO orders_new (id, order_no, customer_name, customer_phone, 
                                           inscription_content, special_requirements, status, created_at, updated_at)
                    SELECT id, order_no, customer_name, customer_phone, seal_content, 
                           special_requirements, status, created_at, updated_at
                    FROM orders
                ''')
            except:
                pass
        cursor.execute('DROP TABLE orders')
        cursor.execute('ALTER TABLE orders_new RENAME TO orders')
    else:
        cursor.execute('''
            CREATE TABLE orders (
                id TEXT PRIMARY KEY,
                order_no TEXT UNIQUE NOT NULL,
                customer_name TEXT NOT NULL,
                customer_phone TEXT NOT NULL,
                agate_type TEXT NOT NULL,
                seal_specification TEXT NOT NULL,
                inscription_content TEXT NOT NULL,
                inscription_font TEXT NOT NULL,
                carving_style TEXT NOT NULL,
                carving_type TEXT NOT NULL,
                edge_treatment TEXT NOT NULL,
                polishing_level TEXT NOT NULL,
                difficulty TEXT NOT NULL DEFAULT '一般',
                price REAL NOT NULL DEFAULT 0,
                craftsman_id TEXT,
                craftsman_name TEXT,
                estimated_days INTEGER,
                delivery_date TEXT,
                special_requirements TEXT,
                status TEXT NOT NULL DEFAULT '待接单',
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL
            )
        ''')
    
    conn.commit()
    conn.close()
    set_db_version(target_version)

def init_db():
    migrate_db()

def generate_order_no():
    today = datetime.now().strftime('%Y%m%d')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT order_no FROM orders WHERE order_no LIKE ? ORDER BY order_no DESC LIMIT 1', (f'{today}%',))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        last_no = int(result['order_no'][8:])
        new_no = last_no + 1
    else:
        new_no = 1
    
    return f'{today}{new_no:04d}'

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    
    required_fields = [
        'customer_name', 
        'customer_phone', 
        'agate_type', 
        'seal_specification',
        'inscription_content',
        'carving_style'
    ]
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'缺少必填字段: {field}'}), 400
    
    if data['agate_type'] not in AGATE_TYPES:
        return jsonify({'error': '无效的玛瑙种类'}), 400
    
    if data['seal_specification'] not in SEAL_SPECIFICATIONS:
        return jsonify({'error': '无效的印章规格'}), 400
    
    if data['carving_style'] not in CARVING_STYLES:
        return jsonify({'error': '无效的篆刻风格'}), 400
    
    difficulty = data.get('difficulty', '一般')
    if difficulty not in DIFFICULTY_LEVELS:
        return jsonify({'error': '无效的难度等级'}), 400
    
    price = calculate_price(
        data['agate_type'],
        data['seal_specification'],
        data['carving_style'],
        difficulty
    )
    
    delivery_date, estimated_days = estimate_delivery_date(
        data['carving_style'],
        difficulty
    )
    
    craftsman_id = data.get('craftsman_id')
    craftsman_name = None
    if craftsman_id:
        craftsman = next((c for c in CRAFTSMEN if c['id'] == craftsman_id), None)
        if craftsman:
            craftsman_name = craftsman['name']
        else:
            return jsonify({'error': '无效的匠人ID'}), 400
    
    order_id = str(uuid.uuid4())
    order_no = generate_order_no()
    now = datetime.now().isoformat()
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO orders (
                id, order_no, customer_name, customer_phone, agate_type, seal_specification,
                inscription_content, inscription_font, carving_style, carving_type,
                edge_treatment, polishing_level, difficulty, price,
                craftsman_id, craftsman_name, estimated_days, delivery_date,
                special_requirements, status, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_id,
            order_no,
            data['customer_name'],
            data['customer_phone'],
            data['agate_type'],
            data['seal_specification'],
            data['inscription_content'],
            data.get('inscription_font', '篆书'),
            data['carving_style'],
            data.get('carving_type', '阳文'),
            data.get('edge_treatment', '平直边'),
            data.get('polishing_level', '高光'),
            difficulty,
            price,
            craftsman_id,
            craftsman_name,
            estimated_days,
            delivery_date,
            data.get('special_requirements', ''),
            '待接单',
            now,
            now
        ))
        conn.commit()
    except sqlite3.Error as e:
        conn.close()
        return jsonify({'error': str(e)}), 500
    
    conn.close()
    
    return jsonify({
        'id': order_id,
        'order_no': order_no,
        'price': price,
        'delivery_date': delivery_date,
        'estimated_days': estimated_days,
        'message': '订单创建成功'
    }), 201

@app.route('/api/orders', methods=['GET'])
def get_orders():
    status = request.args.get('status')
    carving_style = request.args.get('carving_style')
    craftsman_id = request.args.get('craftsman_id')
    delivery_date_from = request.args.get('delivery_date_from')
    delivery_date_to = request.args.get('delivery_date_to')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')
    
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    offset = (page - 1) * per_page
    
    conn = get_db()
    cursor = conn.cursor()
    
    where_clauses = []
    params = []
    
    if status:
        if status not in STATUS_LIST:
            return jsonify({'error': '无效的状态'}), 400
        where_clauses.append('status = ?')
        params.append(status)
    
    if carving_style:
        if carving_style not in CARVING_STYLES:
            return jsonify({'error': '无效的篆刻风格'}), 400
        where_clauses.append('carving_style = ?')
        params.append(carving_style)
    
    if craftsman_id:
        where_clauses.append('craftsman_id = ?')
        params.append(craftsman_id)
    
    if delivery_date_from:
        where_clauses.append('delivery_date >= ?')
        params.append(delivery_date_from)
    
    if delivery_date_to:
        where_clauses.append('delivery_date <= ?')
        params.append(delivery_date_to)
    
    if min_price:
        where_clauses.append('price >= ?')
        params.append(float(min_price))
    
    if max_price:
        where_clauses.append('price <= ?')
        params.append(float(max_price))
    
    valid_sort_columns = ['created_at', 'updated_at', 'price', 'delivery_date', 'order_no']
    if sort_by not in valid_sort_columns:
        sort_by = 'created_at'
    
    if sort_order.lower() not in ['asc', 'desc']:
        sort_order = 'desc'
    
    where_sql = ' AND '.join(where_clauses) if where_clauses else '1=1'
    
    query_sql = f'''
        SELECT * FROM orders 
        WHERE {where_sql} 
        ORDER BY {sort_by} {sort_order} 
        LIMIT ? OFFSET ?
    '''
    count_sql = f'''
        SELECT COUNT(*) as total FROM orders WHERE {where_sql}
    '''
    
    cursor.execute(query_sql, params + [per_page, offset])
    orders = cursor.fetchall()
    
    cursor.execute(count_sql, params)
    total = cursor.fetchone()['total']
    conn.close()
    
    order_list = []
    for order in orders:
        order_list.append({
            'id': order['id'],
            'order_no': order['order_no'],
            'customer_name': order['customer_name'],
            'customer_phone': order['customer_phone'],
            'agate_type': order['agate_type'],
            'seal_specification': order['seal_specification'],
            'inscription_content': order['inscription_content'],
            'inscription_font': order['inscription_font'],
            'carving_style': order['carving_style'],
            'carving_type': order['carving_type'],
            'edge_treatment': order['edge_treatment'],
            'polishing_level': order['polishing_level'],
            'difficulty': order['difficulty'],
            'price': order['price'],
            'craftsman_id': order['craftsman_id'],
            'craftsman_name': order['craftsman_name'],
            'estimated_days': order['estimated_days'],
            'delivery_date': order['delivery_date'],
            'special_requirements': order['special_requirements'],
            'status': order['status'],
            'created_at': order['created_at'],
            'updated_at': order['updated_at']
        })
    
    return jsonify({
        'orders': order_list,
        'total': total,
        'page': page,
        'per_page': per_page,
        'sort_by': sort_by,
        'sort_order': sort_order
    })

@app.route('/api/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
    order = cursor.fetchone()
    conn.close()
    
    if not order:
        return jsonify({'error': '订单不存在'}), 404
    
    return jsonify({
        'id': order['id'],
        'order_no': order['order_no'],
        'customer_name': order['customer_name'],
        'customer_phone': order['customer_phone'],
        'agate_type': order['agate_type'],
        'seal_specification': order['seal_specification'],
        'inscription_content': order['inscription_content'],
        'inscription_font': order['inscription_font'],
        'carving_style': order['carving_style'],
        'carving_type': order['carving_type'],
        'edge_treatment': order['edge_treatment'],
        'polishing_level': order['polishing_level'],
        'difficulty': order['difficulty'],
        'price': order['price'],
        'craftsman_id': order['craftsman_id'],
        'craftsman_name': order['craftsman_name'],
        'estimated_days': order['estimated_days'],
        'delivery_date': order['delivery_date'],
        'special_requirements': order['special_requirements'],
        'status': order['status'],
        'created_at': order['created_at'],
        'updated_at': order['updated_at']
    })

@app.route('/api/orders/<order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
    order = cursor.fetchone()
    
    if not order:
        conn.close()
        return jsonify({'error': '订单不存在'}), 404
    
    update_fields = []
    update_values = []
    
    if 'customer_name' in data:
        update_fields.append('customer_name = ?')
        update_values.append(data['customer_name'])
    
    if 'customer_phone' in data:
        update_fields.append('customer_phone = ?')
        update_values.append(data['customer_phone'])
    
    if 'agate_type' in data:
        if data['agate_type'] not in AGATE_TYPES:
            conn.close()
            return jsonify({'error': '无效的玛瑙种类'}), 400
        update_fields.append('agate_type = ?')
        update_values.append(data['agate_type'])
    
    if 'seal_specification' in data:
        if data['seal_specification'] not in SEAL_SPECIFICATIONS:
            conn.close()
            return jsonify({'error': '无效的印章规格'}), 400
        update_fields.append('seal_specification = ?')
        update_values.append(data['seal_specification'])
    
    if 'inscription_content' in data:
        update_fields.append('inscription_content = ?')
        update_values.append(data['inscription_content'])
    
    if 'inscription_font' in data:
        update_fields.append('inscription_font = ?')
        update_values.append(data['inscription_font'])
    
    if 'carving_style' in data:
        if data['carving_style'] not in CARVING_STYLES:
            conn.close()
            return jsonify({'error': '无效的篆刻风格'}), 400
        update_fields.append('carving_style = ?')
        update_values.append(data['carving_style'])
    
    if 'carving_type' in data:
        update_fields.append('carving_type = ?')
        update_values.append(data['carving_type'])
    
    if 'edge_treatment' in data:
        if data['edge_treatment'] not in EDGE_TREATMENTS:
            conn.close()
            return jsonify({'error': '无效的边款处理方式'}), 400
        update_fields.append('edge_treatment = ?')
        update_values.append(data['edge_treatment'])
    
    if 'polishing_level' in data:
        if data['polishing_level'] not in POLISHING_LEVELS:
            conn.close()
            return jsonify({'error': '无效的抛光等级'}), 400
        update_fields.append('polishing_level = ?')
        update_values.append(data['polishing_level'])
    
    if 'difficulty' in data:
        if data['difficulty'] not in DIFFICULTY_LEVELS:
            conn.close()
            return jsonify({'error': '无效的难度等级'}), 400
        update_fields.append('difficulty = ?')
        update_values.append(data['difficulty'])
    
    if 'craftsman_id' in data:
        craftsman = next((c for c in CRAFTSMEN if c['id'] == data['craftsman_id']), None)
        if not craftsman:
            conn.close()
            return jsonify({'error': '无效的匠人ID'}), 400
        update_fields.append('craftsman_id = ?')
        update_fields.append('craftsman_name = ?')
        update_values.append(data['craftsman_id'])
        update_values.append(craftsman['name'])
    
    if 'delivery_date' in data:
        update_fields.append('delivery_date = ?')
        update_values.append(data['delivery_date'])
    
    if 'special_requirements' in data:
        update_fields.append('special_requirements = ?')
        update_values.append(data['special_requirements'])
    
    if 'status' in data:
        if data['status'] not in STATUS_LIST:
            conn.close()
            return jsonify({'error': '无效的状态值'}), 400
        update_fields.append('status = ?')
        update_values.append(data['status'])
    
    if not update_fields:
        conn.close()
        return jsonify({'error': '没有提供更新字段'}), 400
    
    if any(f in update_fields for f in ['agate_type = ?', 'seal_specification = ?', 'carving_style = ?', 'difficulty = ?']):
        current_agate = order['agate_type']
        current_spec = order['seal_specification']
        current_style = order['carving_style']
        current_difficulty = order['difficulty']
        
        if 'agate_type = ?' in update_fields:
            current_agate = data['agate_type']
        if 'seal_specification = ?' in update_fields:
            current_spec = data['seal_specification']
        if 'carving_style = ?' in update_fields:
            current_style = data['carving_style']
        if 'difficulty = ?' in update_fields:
            current_difficulty = data['difficulty']
        
        new_price = calculate_price(current_agate, current_spec, current_style, current_difficulty)
        update_fields.append('price = ?')
        update_values.append(new_price)
    
    update_fields.append('updated_at = ?')
    update_values.append(datetime.now().isoformat())
    update_values.append(order_id)
    
    try:
        cursor.execute(f'''
            UPDATE orders SET {', '.join(update_fields)} WHERE id = ?
        ''', update_values)
        conn.commit()
    except sqlite3.Error as e:
        conn.close()
        return jsonify({'error': str(e)}), 500
    
    conn.close()
    
    return jsonify({'message': '订单更新成功'})

@app.route('/api/orders/<order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    data = request.get_json()
    
    if 'status' not in data:
        return jsonify({'error': '缺少状态字段'}), 400
    
    status = data['status']
    if status not in STATUS_LIST:
        return jsonify({'error': '无效的状态值'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
    order = cursor.fetchone()
    
    if not order:
        conn.close()
        return jsonify({'error': '订单不存在'}), 404
    
    try:
        cursor.execute('''
            UPDATE orders SET status = ?, updated_at = ? WHERE id = ?
        ''', (status, datetime.now().isoformat(), order_id))
        conn.commit()
    except sqlite3.Error as e:
        conn.close()
        return jsonify({'error': str(e)}), 500
    
    conn.close()
    
    return jsonify({'message': '状态更新成功', 'new_status': status})

@app.route('/api/orders/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
    order = cursor.fetchone()
    
    if not order:
        conn.close()
        return jsonify({'error': '订单不存在'}), 404
    
    try:
        cursor.execute('DELETE FROM orders WHERE id = ?', (order_id,))
        conn.commit()
    except sqlite3.Error as e:
        conn.close()
        return jsonify({'error': str(e)}), 500
    
    conn.close()
    
    return jsonify({'message': '订单删除成功'})

@app.route('/api/statuses', methods=['GET'])
def get_statuses():
    return jsonify({'statuses': STATUS_LIST})

@app.route('/api/agate-types', methods=['GET'])
def get_agate_types():
    return jsonify({'agate_types': AGATE_TYPES})

@app.route('/api/seal-specifications', methods=['GET'])
def get_seal_specifications():
    return jsonify({'seal_specifications': SEAL_SPECIFICATIONS})

@app.route('/api/carving-styles', methods=['GET'])
def get_carving_styles():
    return jsonify({'carving_styles': CARVING_STYLES})

@app.route('/api/edge-treatments', methods=['GET'])
def get_edge_treatments():
    return jsonify({'edge_treatments': EDGE_TREATMENTS})

@app.route('/api/polishing-levels', methods=['GET'])
def get_polishing_levels():
    return jsonify({'polishing_levels': POLISHING_LEVELS})

@app.route('/api/difficulty-levels', methods=['GET'])
def get_difficulty_levels():
    return jsonify({'difficulty_levels': DIFFICULTY_LEVELS})

@app.route('/api/craftsmen', methods=['GET'])
def get_craftsmen():
    return jsonify({'craftsmen': CRAFTSMEN})

@app.route('/api/calculate-price', methods=['POST'])
def api_calculate_price():
    data = request.get_json()
    
    required_fields = ['agate_type', 'seal_specification', 'carving_style']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'缺少必填字段: {field}'}), 400
    
    if data['agate_type'] not in AGATE_TYPES:
        return jsonify({'error': '无效的玛瑙种类'}), 400
    
    if data['seal_specification'] not in SEAL_SPECIFICATIONS:
        return jsonify({'error': '无效的印章规格'}), 400
    
    if data['carving_style'] not in CARVING_STYLES:
        return jsonify({'error': '无效的篆刻风格'}), 400
    
    difficulty = data.get('difficulty', '一般')
    if difficulty not in DIFFICULTY_LEVELS:
        return jsonify({'error': '无效的难度等级'}), 400
    
    price = calculate_price(
        data['agate_type'],
        data['seal_specification'],
        data['carving_style'],
        difficulty
    )
    
    delivery_date, estimated_days = estimate_delivery_date(
        data['carving_style'],
        difficulty
    )
    
    return jsonify({
        'price': price,
        'delivery_date': delivery_date,
        'estimated_days': estimated_days
    })

@app.route('/api/options', methods=['GET'])
def get_all_options():
    return jsonify({
        'statuses': STATUS_LIST,
        'agate_types': AGATE_TYPES,
        'seal_specifications': SEAL_SPECIFICATIONS,
        'carving_styles': CARVING_STYLES,
        'edge_treatments': EDGE_TREATMENTS,
        'polishing_levels': POLISHING_LEVELS,
        'difficulty_levels': DIFFICULTY_LEVELS,
        'craftsmen': CRAFTSMEN,
        'agate_price_multipliers': AGATE_PRICE_MULTIPLIER,
        'spec_price_base': SPEC_PRICE_BASE
    })

if __name__ == '__main__':
    init_db()
    print('数据库初始化/迁移完成')
    print('订单状态列表:', STATUS_LIST)
    print('玛瑙种类:', len(AGATE_TYPES), '种')
    print('印章规格:', len(SEAL_SPECIFICATIONS), '种')
    print('篆刻风格:', len(CARVING_STYLES), '种')
    print('边款处理:', len(EDGE_TREATMENTS), '种')
    print('抛光等级:', len(POLISHING_LEVELS), '种')
    print('难度等级:', len(DIFFICULTY_LEVELS), '级')
    print('匠人数量:', len(CRAFTSMEN), '人')
    app.run(debug=True, host='0.0.0.0', port=5000)
