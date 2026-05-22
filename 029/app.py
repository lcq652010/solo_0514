from flask import Flask, request, jsonify, g
import sqlite3
import re
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['DATABASE'] = 'jade_order_system.db'

ORDER_STATUSES = [
    '待接单', '选料', '切料', '粗雕', '细雕', '抛光', '打孔', '完工'
]

CARVING_PATTERNS = [
    '观音', '佛', '貔貅', '龙凤', '祥云', '山水', '花鸟', '人物', 
    '生肖', '八卦', '如意', '平安扣', '无事牌', '其他'
]

CARVING_STYLES = ['浮雕', '透雕', '圆雕', '阴刻', '阳刻', '线雕']

HOLE_POSITIONS = ['顶部正中', '顶部偏左', '顶部偏右', '底部正中', '侧面', '不打孔']

POLISHING_LEVELS = ['亚光', '半光', '高光', '镜面抛光']

MATERIAL_TYPES = [
    '和田玉', '翡翠', '独山玉', '岫玉', '蓝田玉', '绿松石', 
    '玛瑙', '碧玉', '白玉', '青玉', '墨玉', '羊脂玉', '其他'
]

CARVING_DIFFICULTY = {
    '简单': 1.0,
    '中等': 1.5,
    '复杂': 2.0,
    '大师级': 3.0
}

MATERIAL_PRICE_BASE = {
    '和田玉': 500,
    '翡翠': 800,
    '独山玉': 300,
    '岫玉': 150,
    '蓝田玉': 200,
    '绿松石': 400,
    '玛瑙': 100,
    '碧玉': 350,
    '白玉': 450,
    '青玉': 380,
    '墨玉': 420,
    '羊脂玉': 1200,
    '其他': 200
}

CARVING_STYLE_MULTIPLIER = {
    '浮雕': 1.0,
    '透雕': 1.8,
    '圆雕': 2.5,
    '阴刻': 0.8,
    '阳刻': 1.2,
    '线雕': 0.6
}

def success_response(data=None, message='操作成功', code=200):
    return jsonify({
        'success': True,
        'code': code,
        'message': message,
        'data': data
    }), code

def error_response(message='操作失败', code=400, errors=None):
    response = {
        'success': False,
        'code': code,
        'message': message
    }
    if errors:
        response['errors'] = errors
    return jsonify(response), code

def validate_phone(phone):
    if not phone:
        return False
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, phone))

def validate_positive_number(value, field_name):
    if value is not None:
        try:
            num = float(value)
            if num <= 0:
                return f'{field_name}必须大于0'
        except (ValueError, TypeError):
            return f'{field_name}必须是有效的数值'
    return None

def validate_order_data(data, is_create=True):
    errors = []
    
    required_fields = ['customer_name', 'customer_phone', 'pendant_type', 'material', 'design_description']
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f'缺少必填字段: {field}')
    
    if 'customer_phone' in data and data['customer_phone']:
        if not validate_phone(data['customer_phone']):
            errors.append('手机号格式不正确，应为11位有效手机号')
    
    num_fields = [
        ('pendant_length', '吊坠长度'),
        ('pendant_width', '吊坠宽度'),
        ('pendant_thickness', '吊坠厚度'),
        ('pendant_weight', '吊坠重量'),
        ('hole_count', '打孔数量')
    ]
    for field, name in num_fields:
        if field in data and data[field] is not None:
            error = validate_positive_number(data[field], name)
            if error:
                errors.append(error)
    
    if 'material' in data and data['material'] not in MATERIAL_TYPES:
        errors.append(f'无效的材质类型，可选值: {MATERIAL_TYPES}')
    
    if 'carving_pattern' in data and data['carving_pattern'] and data['carving_pattern'] not in CARVING_PATTERNS:
        errors.append(f'无效的雕刻纹样，可选值: {CARVING_PATTERNS}')
    
    if 'carving_style' in data and data['carving_style'] and data['carving_style'] not in CARVING_STYLES:
        errors.append(f'无效的雕刻样式，可选值: {CARVING_STYLES}')
    
    if 'polishing_level' in data and data['polishing_level'] and data['polishing_level'] not in POLISHING_LEVELS:
        errors.append(f'无效的抛光等级，可选值: {POLISHING_LEVELS}')
    
    if 'hole_position' in data and data['hole_position'] and data['hole_position'] not in HOLE_POSITIONS:
        errors.append(f'无效的打孔位置，可选值: {HOLE_POSITIONS}')
    
    return errors

def calculate_auto_price(material, carving_style, carving_difficulty, weight=10):
    base_price = MATERIAL_PRICE_BASE.get(material, 200)
    style_multiplier = CARVING_STYLE_MULTIPLIER.get(carving_style, 1.0)
    difficulty_multiplier = CARVING_DIFFICULTY.get(carving_difficulty, 1.0)
    
    total_price = base_price * style_multiplier * difficulty_multiplier * (weight / 10)
    return round(total_price, 2)

def calculate_deadline(carving_difficulty, start_date=None):
    if start_date is None:
        start_date = datetime.now()
    
    difficulty_days = {
        '简单': 3,
        '中等': 7,
        '复杂': 14,
        '大师级': 21
    }
    days = difficulty_days.get(carving_difficulty, 7)
    deadline = start_date + timedelta(days=days)
    return deadline.isoformat()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
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
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='craftsmen'")
        if not cursor.fetchone():
            cursor.execute('''
                CREATE TABLE craftsmen (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT,
                    skill_level TEXT NOT NULL,
                    specialty TEXT,
                    status TEXT DEFAULT '空闲',
                    daily_capacity INTEGER DEFAULT 1,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL
                )
            ''')
        
        cursor.execute("PRAGMA table_info(orders)")
        columns = [col[1] for col in cursor.fetchall()]
        
        new_columns = {
            'carving_difficulty': 'TEXT',
            'craftsman_id': 'INTEGER',
            'craftsman_name': 'TEXT',
            'start_date': 'TIMESTAMP',
            'deadline': 'TIMESTAMP',
            'actual_finish_date': 'TIMESTAMP',
            'auto_calculated_price': 'REAL',
            'price_calculated_at': 'TIMESTAMP'
        }
        
        for col_name, col_type in new_columns.items():
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
                customer_phone TEXT NOT NULL,
                customer_address TEXT,
                pendant_type TEXT NOT NULL,
                material TEXT NOT NULL,
                material_type TEXT,
                material_detail TEXT,
                size TEXT,
                pendant_length REAL,
                pendant_width REAL,
                pendant_thickness REAL,
                pendant_weight REAL,
                carving_pattern TEXT,
                carving_style TEXT,
                carving_depth TEXT,
                carving_details TEXT,
                carving_difficulty TEXT,
                polishing_level TEXT,
                polishing_details TEXT,
                hole_position TEXT,
                hole_size TEXT,
                hole_count INTEGER,
                design_description TEXT NOT NULL,
                special_requirements TEXT,
                status TEXT NOT NULL DEFAULT '待接单',
                craftsman_id INTEGER,
                craftsman_name TEXT,
                start_date TIMESTAMP,
                deadline TIMESTAMP,
                actual_finish_date TIMESTAMP,
                estimated_price REAL,
                auto_calculated_price REAL,
                price_calculated_at TIMESTAMP,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS craftsmen (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                skill_level TEXT NOT NULL,
                specialty TEXT,
                status TEXT DEFAULT '空闲',
                daily_capacity INTEGER DEFAULT 1,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL
            )
        ''')
        
        db.commit()
        migrate_db()
        
        cursor.execute("SELECT COUNT(*) as count FROM craftsmen")
        if cursor.fetchone()['count'] == 0:
            now = datetime.now().isoformat()
            default_craftsmen = [
                ('张师傅', '13800138001', '高级', '观音、佛类雕刻', '空闲', 2),
                ('李师傅', '13800138002', '大师', '复杂透雕、圆雕', '空闲', 1),
                ('王师傅', '13800138003', '中级', '花鸟、生肖', '空闲', 3),
                ('赵师傅', '13800138004', '高级', '山水、人物', '空闲', 2)
            ]
            for cm in default_craftsmen:
                cursor.execute('''
                    INSERT INTO craftsmen (name, phone, skill_level, specialty, status, daily_capacity, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (*cm, now, now))
            db.commit()

def generate_order_no():
    date_str = datetime.now().strftime('%Y%m%d')
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT order_no FROM orders WHERE order_no LIKE ? ORDER BY order_no DESC LIMIT 1', (f'{date_str}%',))
        result = cursor.fetchone()
        if result:
            last_no = result[0]
            sequence = int(last_no[-4:]) + 1
        else:
            sequence = 1
        return f'{date_str}{sequence:04d}'

def order_to_dict(row):
    return {
        'id': row['id'],
        'order_no': row['order_no'],
        'customer_name': row['customer_name'],
        'customer_phone': row['customer_phone'],
        'customer_address': row['customer_address'],
        'pendant_type': row['pendant_type'],
        'material': row['material'],
        'material_type': row['material_type'],
        'material_detail': row['material_detail'],
        'size': row['size'],
        'pendant_length': row['pendant_length'],
        'pendant_width': row['pendant_width'],
        'pendant_thickness': row['pendant_thickness'],
        'pendant_weight': row['pendant_weight'],
        'carving_pattern': row['carving_pattern'],
        'carving_style': row['carving_style'],
        'carving_depth': row['carving_depth'],
        'carving_details': row['carving_details'],
        'carving_difficulty': row['carving_difficulty'],
        'polishing_level': row['polishing_level'],
        'polishing_details': row['polishing_details'],
        'hole_position': row['hole_position'],
        'hole_size': row['hole_size'],
        'hole_count': row['hole_count'],
        'design_description': row['design_description'],
        'special_requirements': row['special_requirements'],
        'status': row['status'],
        'craftsman_id': row['craftsman_id'],
        'craftsman_name': row['craftsman_name'],
        'start_date': row['start_date'],
        'deadline': row['deadline'],
        'actual_finish_date': row['actual_finish_date'],
        'estimated_price': row['estimated_price'],
        'auto_calculated_price': row['auto_calculated_price'],
        'price_calculated_at': row['price_calculated_at'],
        'created_at': row['created_at'],
        'updated_at': row['updated_at']
    }

@app.route('/api/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        if not data:
            return error_response('请求数据不能为空', 400)
        
        errors = validate_order_data(data, is_create=True)
        if errors:
            return error_response('数据验证失败', 400, errors)
        
        order_no = generate_order_no()
        now = datetime.now().isoformat()
        
        weight = data.get('pendant_weight', 10) or 10
        carving_difficulty = data.get('carving_difficulty', '中等') or '中等'
        carving_style = data.get('carving_style', '浮雕') or '浮雕'
        
        auto_price = calculate_auto_price(
            data['material'],
            carving_style,
            carving_difficulty,
            weight
        )
        
        deadline = calculate_deadline(carving_difficulty)
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO orders (
                order_no, customer_name, customer_phone, customer_address,
                pendant_type, material, material_type, material_detail,
                size, pendant_length, pendant_width, pendant_thickness, pendant_weight,
                carving_pattern, carving_style, carving_depth, carving_details, carving_difficulty,
                polishing_level, polishing_details,
                hole_position, hole_size, hole_count,
                design_description, special_requirements, status,
                auto_calculated_price, price_calculated_at, deadline,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_no,
            data['customer_name'],
            data['customer_phone'],
            data.get('customer_address', ''),
            data['pendant_type'],
            data['material'],
            data.get('material_type', ''),
            data.get('material_detail', ''),
            data.get('size', ''),
            data.get('pendant_length'),
            data.get('pendant_width'),
            data.get('pendant_thickness'),
            data.get('pendant_weight'),
            data.get('carving_pattern', ''),
            data.get('carving_style', ''),
            data.get('carving_depth', ''),
            data.get('carving_details', ''),
            carving_difficulty,
            data.get('polishing_level', ''),
            data.get('polishing_details', ''),
            data.get('hole_position', ''),
            data.get('hole_size', ''),
            data.get('hole_count'),
            data['design_description'],
            data.get('special_requirements', ''),
            '待接单',
            auto_price,
            now,
            deadline,
            now,
            now
        ))
        db.commit()
        
        return success_response({'order_no': order_no, 'auto_calculated_price': auto_price, 'deadline': deadline}, '订单创建成功', 201)
    except Exception as e:
        return error_response(f'创建订单失败: {str(e)}', 500)

@app.route('/api/orders', methods=['GET'])
def get_orders():
    try:
        db = get_db()
        cursor = db.cursor()
        
        status = request.args.get('status')
        carving_style = request.args.get('carving_style')
        carving_pattern = request.args.get('carving_pattern')
        material = request.args.get('material')
        deadline_start = request.args.get('deadline_start')
        deadline_end = request.args.get('deadline_end')
        
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        
        valid_sort_fields = ['created_at', 'updated_at', 'deadline', 'status', 'order_no']
        if sort_by not in valid_sort_fields:
            sort_by = 'created_at'
        if sort_order not in ['asc', 'desc']:
            sort_order = 'desc'
        
        query = 'SELECT * FROM orders WHERE 1=1'
        params = []
        
        if status:
            query += ' AND status = ?'
            params.append(status)
        
        if carving_style:
            query += ' AND carving_style = ?'
            params.append(carving_style)
        
        if carving_pattern:
            query += ' AND carving_pattern = ?'
            params.append(carving_pattern)
        
        if material:
            query += ' AND material = ?'
            params.append(material)
        
        if deadline_start:
            query += ' AND deadline >= ?'
            params.append(deadline_start)
        
        if deadline_end:
            query += ' AND deadline <= ?'
            params.append(deadline_end)
        
        count_query = query.replace('SELECT *', 'SELECT COUNT(*)')
        cursor.execute(count_query, params)
        total = cursor.fetchone()[0]
        
        query += f' ORDER BY {sort_by} {sort_order.upper()}'
        
        if page > 0 and page_size > 0:
            offset = (page - 1) * page_size
            query += ' LIMIT ? OFFSET ?'
            params.extend([page_size, offset])
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        orders = [order_to_dict(row) for row in rows]
        
        data = {
            'list': orders,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total': total,
                'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 0
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
        row = cursor.fetchone()
        if not row:
            return error_response('订单不存在', 404)
        return success_response(order_to_dict(row), '获取订单详情成功')
    except Exception as e:
        return error_response(f'获取订单详情失败: {str(e)}', 500)

@app.route('/api/orders/<order_no>/status', methods=['PUT'])
def update_order_status(order_no):
    try:
        data = request.get_json()
        if 'status' not in data:
            return error_response('缺少状态字段', 400)
        if data['status'] not in ORDER_STATUSES:
            return error_response(f'无效的状态，可选值: {ORDER_STATUSES}', 400)
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        if not cursor.fetchone():
            return error_response('订单不存在', 404)
        
        now = datetime.now().isoformat()
        update_fields = ['status = ?', 'updated_at = ?']
        update_values = [data['status'], now]
        
        if data['status'] == '完工':
            update_fields.append('actual_finish_date = ?')
            update_values.append(now)
        elif data['status'] == '粗雕':
            update_fields.append('start_date = ?')
            update_values.append(now)
        
        update_values.append(order_no)
        cursor.execute(f'''
            UPDATE orders SET {', '.join(update_fields)} WHERE order_no = ?
        ''', update_values)
        db.commit()
        
        return success_response(None, '订单状态更新成功')
    except Exception as e:
        return error_response(f'更新订单状态失败: {str(e)}', 500)

@app.route('/api/orders/<order_no>', methods=['PUT'])
def update_order(order_no):
    try:
        data = request.get_json()
        if not data:
            return error_response('请求数据不能为空', 400)
        
        errors = validate_order_data(data, is_create=False)
        if errors:
            return error_response('数据验证失败', 400, errors)
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        existing = cursor.fetchone()
        if not existing:
            return error_response('订单不存在', 404)
        
        update_fields = []
        update_values = []
        
        allowed_fields = [
            'customer_name', 'customer_phone', 'customer_address',
            'pendant_type', 'material', 'material_type', 'material_detail',
            'size', 'pendant_length', 'pendant_width', 'pendant_thickness', 'pendant_weight',
            'carving_pattern', 'carving_style', 'carving_depth', 'carving_details', 'carving_difficulty',
            'polishing_level', 'polishing_details',
            'hole_position', 'hole_size', 'hole_count',
            'design_description', 'special_requirements', 'estimated_price'
        ]
        
        for field in allowed_fields:
            if field in data:
                update_fields.append(f'{field} = ?')
                update_values.append(data[field])
        
        if not update_fields:
            return error_response('没有提供可更新的字段', 400)
        
        if 'material' in data or 'carving_style' in data or 'carving_difficulty' in data or 'pendant_weight' in data:
            material = data.get('material') or existing['material']
            carving_style = data.get('carving_style') or existing['carving_style'] or '浮雕'
            carving_difficulty = data.get('carving_difficulty') or existing['carving_difficulty'] or '中等'
            weight = data.get('pendant_weight') or existing['pendant_weight'] or 10
            
            auto_price = calculate_auto_price(material, carving_style, carving_difficulty, weight)
            update_fields.extend(['auto_calculated_price = ?', 'price_calculated_at = ?'])
            update_values.extend([auto_price, datetime.now().isoformat()])
            
            if 'carving_difficulty' in data:
                deadline = calculate_deadline(carving_difficulty)
                update_fields.append('deadline = ?')
                update_values.append(deadline)
        
        update_values.append(datetime.now().isoformat())
        update_values.append(order_no)
        
        cursor.execute(f'''
            UPDATE orders SET {', '.join(update_fields)}, updated_at = ? WHERE order_no = ?
        ''', update_values)
        db.commit()
        
        return success_response(None, '订单更新成功')
    except Exception as e:
        return error_response(f'更新订单失败: {str(e)}', 500)

@app.route('/api/orders/<order_no>/assign', methods=['PUT'])
def assign_craftsman(order_no):
    try:
        data = request.get_json()
        if 'craftsman_id' not in data:
            return error_response('缺少匠人ID字段', 400)
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('SELECT * FROM craftsmen WHERE id = ?', (data['craftsman_id'],))
        craftsman = cursor.fetchone()
        if not craftsman:
            return error_response('匠人不存在', 404)
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        if not cursor.fetchone():
            return error_response('订单不存在', 404)
        
        now = datetime.now().isoformat()
        cursor.execute('''
            UPDATE orders SET craftsman_id = ?, craftsman_name = ?, updated_at = ? WHERE order_no = ?
        ''', (data['craftsman_id'], craftsman['name'], now, order_no))
        db.commit()
        
        return success_response({'craftsman_name': craftsman['name']}, '匠人分配成功')
    except Exception as e:
        return error_response(f'分配匠人失败: {str(e)}', 500)

@app.route('/api/orders/<order_no>', methods=['DELETE'])
def delete_order(order_no):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        if not cursor.fetchone():
            return error_response('订单不存在', 404)
        cursor.execute('DELETE FROM orders WHERE order_no = ?', (order_no,))
        db.commit()
        return success_response(None, '订单删除成功')
    except Exception as e:
        return error_response(f'删除订单失败: {str(e)}', 500)

@app.route('/api/orders/<order_no>/recalculate-price', methods=['POST'])
def recalculate_price(order_no):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        row = cursor.fetchone()
        if not row:
            return error_response('订单不存在', 404)
        
        material = row['material'] or '其他'
        carving_style = row['carving_style'] or '浮雕'
        carving_difficulty = row['carving_difficulty'] or '中等'
        weight = row['pendant_weight'] or 10
        
        auto_price = calculate_auto_price(material, carving_style, carving_difficulty, weight)
        now = datetime.now().isoformat()
        
        cursor.execute('''
            UPDATE orders SET auto_calculated_price = ?, price_calculated_at = ?, updated_at = ? WHERE order_no = ?
        ''', (auto_price, now, now, order_no))
        db.commit()
        
        return success_response({'auto_calculated_price': auto_price}, '价格重新计算成功')
    except Exception as e:
        return error_response(f'重新计算价格失败: {str(e)}', 500)

@app.route('/api/craftsmen', methods=['GET'])
def get_craftsmen():
    try:
        status = request.args.get('status')
        skill_level = request.args.get('skill_level')
        
        db = get_db()
        cursor = db.cursor()
        query = 'SELECT * FROM craftsmen WHERE 1=1'
        params = []
        
        if status:
            query += ' AND status = ?'
            params.append(status)
        if skill_level:
            query += ' AND skill_level = ?'
            params.append(skill_level)
        
        query += ' ORDER BY created_at DESC'
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        craftsmen = []
        for row in rows:
            craftsmen.append({
                'id': row['id'],
                'name': row['name'],
                'phone': row['phone'],
                'skill_level': row['skill_level'],
                'specialty': row['specialty'],
                'status': row['status'],
                'daily_capacity': row['daily_capacity'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            })
        
        return success_response(craftsmen, '获取匠人列表成功')
    except Exception as e:
        return error_response(f'获取匠人列表失败: {str(e)}', 500)

@app.route('/api/craftsmen', methods=['POST'])
def create_craftsman():
    try:
        data = request.get_json()
        required_fields = ['name', 'skill_level']
        for field in required_fields:
            if field not in data or not data[field]:
                return error_response(f'缺少必填字段: {field}', 400)
        
        now = datetime.now().isoformat()
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO craftsmen (name, phone, skill_level, specialty, status, daily_capacity, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data.get('phone', ''),
            data['skill_level'],
            data.get('specialty', ''),
            data.get('status', '空闲'),
            data.get('daily_capacity', 1),
            now,
            now
        ))
        db.commit()
        
        return success_response({'id': cursor.lastrowid}, '匠人创建成功', 201)
    except Exception as e:
        return error_response(f'创建匠人失败: {str(e)}', 500)

@app.route('/api/statuses', methods=['GET'])
def get_statuses():
    return success_response(ORDER_STATUSES, '获取状态列表成功')

@app.route('/api/options', methods=['GET'])
def get_options():
    return success_response({
        'order_statuses': ORDER_STATUSES,
        'carving_patterns': CARVING_PATTERNS,
        'carving_styles': CARVING_STYLES,
        'hole_positions': HOLE_POSITIONS,
        'polishing_levels': POLISHING_LEVELS,
        'material_types': MATERIAL_TYPES,
        'carving_difficulty': list(CARVING_DIFFICULTY.keys()),
        'skill_levels': ['初级', '中级', '高级', '大师']
    }, '获取选项列表成功')

@app.route('/api/price/calculate', methods=['POST'])
def calculate_price():
    try:
        data = request.get_json()
        required_fields = ['material', 'carving_style', 'carving_difficulty']
        for field in required_fields:
            if field not in data or not data[field]:
                return error_response(f'缺少必填字段: {field}', 400)
        
        weight = data.get('weight', 10) or 10
        price = calculate_auto_price(
            data['material'],
            data['carving_style'],
            data['carving_difficulty'],
            weight
        )
        
        deadline = calculate_deadline(data['carving_difficulty'])
        
        return success_response({
            'calculated_price': price,
            'estimated_deadline': deadline,
            'price_detail': {
                'base_price': MATERIAL_PRICE_BASE.get(data['material'], 200),
                'style_multiplier': CARVING_STYLE_MULTIPLIER.get(data['carving_style'], 1.0),
                'difficulty_multiplier': CARVING_DIFFICULTY.get(data['carving_difficulty'], 1.0),
                'weight': weight
            }
        }, '价格计算成功')
    except Exception as e:
        return error_response(f'价格计算失败: {str(e)}', 500)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)