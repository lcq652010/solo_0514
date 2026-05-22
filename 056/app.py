from flask import Flask, request, jsonify, g
import sqlite3
import os
from datetime import datetime, timedelta
import time

app = Flask(__name__)

DATABASE = 'orders.db'

ORDER_STATUSES = [
    '待接单',
    '选料',
    '切坯',
    '打磨',
    '雕刻',
    '烫花',
    '上油',
    '完工'
]

MATERIAL_PRICES = {
    '牛骨': 80,
    '骆驼骨': 120,
    '鹿角': 200,
    '象牙果': 60,
    '黄牛蹄': 100
}

GRADE_MULTIPLIERS = {
    'C级': 1.0,
    'B级': 1.2,
    'A级': 1.5,
    '特级': 2.0
}

CARVING_DIFFICULTY = {
    '浅雕(0.5mm)': 1.0,
    '中雕(1mm)': 1.3,
    '深雕(1.5mm)': 1.8,
    '透雕': 2.5
}

POLISHING_PRICES = {
    '自然纹理': 20,
    '磨砂': 30,
    '亚光': 40,
    '镜面抛光': 60
}

BASE_PRICE = 50
SIZE_PRICE_PER_CM3 = 2

def success_response(data=None, message='操作成功'):
    return jsonify({
        'code': 200,
        'message': message,
        'data': data,
        'timestamp': datetime.now().isoformat()
    }), 200

def error_response(message='操作失败', code=400, data=None):
    return jsonify({
        'code': code,
        'message': message,
        'data': data,
        'timestamp': datetime.now().isoformat()
    }), code

def validate_order_data(data):
    errors = []
    
    required_fields = ['customer_name', 'customer_phone', 'material_category', 'length_cm', 'width_cm', 'thickness_cm']
    for field in required_fields:
        if field not in data or not str(data[field]).strip():
            errors.append(f'缺少必填字段: {field}')
    
    if 'length_cm' in data:
        try:
            length = float(data['length_cm'])
            if length < 5 or length > 50:
                errors.append('长度必须在5-50cm之间')
        except (ValueError, TypeError):
            errors.append('长度必须是有效数字')
    
    if 'width_cm' in data:
        try:
            width = float(data['width_cm'])
            if width < 1 or width > 10:
                errors.append('宽度必须在1-10cm之间')
        except (ValueError, TypeError):
            errors.append('宽度必须是有效数字')
    
    if 'thickness_cm' in data:
        try:
            thickness = float(data['thickness_cm'])
            if thickness < 0.3 or thickness > 5:
                errors.append('厚度必须在0.3-5cm之间')
        except (ValueError, TypeError):
            errors.append('厚度必须是有效数字')
    
    if 'material_category' in data and data['material_category'] not in MATERIAL_PRICES:
        errors.append(f'无效的材料类别，有效选项: {list(MATERIAL_PRICES.keys())}')
    
    if 'material_grade' in data and data['material_grade'] and data['material_grade'] not in GRADE_MULTIPLIERS:
        errors.append(f'无效的材料等级，有效选项: {list(GRADE_MULTIPLIERS.keys())}')
    
    if 'carving_depth' in data and data['carving_depth'] and data['carving_depth'] not in CARVING_DIFFICULTY:
        errors.append(f'无效的雕刻深度，有效选项: {list(CARVING_DIFFICULTY.keys())}')
    
    return errors

def calculate_price(data):
    material_price = MATERIAL_PRICES.get(data.get('material_category', '牛骨'), 80)
    grade_multiplier = GRADE_MULTIPLIERS.get(data.get('material_grade', 'B级'), 1.2)
    carving_multiplier = CARVING_DIFFICULTY.get(data.get('carving_depth', '中雕(1mm)'), 1.3)
    polishing_price = POLISHING_PRICES.get(data.get('polishing_requirement', '亚光'), 40)
    
    length = float(data.get('length_cm', 15))
    width = float(data.get('width_cm', 3))
    thickness = float(data.get('thickness_cm', 1))
    volume = length * width * thickness
    size_price = volume * SIZE_PRICE_PER_CM3
    
    has_carving = 1 if data.get('carving_content') or data.get('carving_pattern') else 0
    has_hot_stamping = 1 if data.get('hot_stamping_content') or data.get('hot_stamping_pattern') else 0
    
    total_price = (BASE_PRICE + material_price * grade_multiplier + size_price + polishing_price) * carving_multiplier
    total_price = total_price * (1 + has_carving * 0.3 + has_hot_stamping * 0.15)
    
    return round(total_price, 2)

def calculate_lead_time(data):
    base_days = 3
    
    if data.get('material_grade') == '特级':
        base_days += 2
    
    carving_depth = data.get('carving_depth', '中雕(1mm)')
    if carving_depth == '深雕(1.5mm)':
        base_days += 2
    elif carving_depth == '透雕':
        base_days += 4
    
    if data.get('polishing_requirement') == '镜面抛光':
        base_days += 1
    
    if data.get('carving_pattern') in ['龙纹', '凤纹', '山水纹']:
        base_days += 2
    
    return base_days

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
            CREATE TABLE IF NOT EXISTS craftsmen (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                specialty TEXT,
                skill_level TEXT DEFAULT '中级',
                daily_capacity INTEGER DEFAULT 2,
                status TEXT DEFAULT '空闲',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_no TEXT UNIQUE NOT NULL,
                customer_name TEXT NOT NULL,
                customer_phone TEXT NOT NULL,
                customer_address TEXT,
                material_category TEXT NOT NULL,
                material_origin TEXT,
                material_grade TEXT,
                length_cm DECIMAL(5,2) NOT NULL,
                width_cm DECIMAL(5,2) NOT NULL,
                thickness_cm DECIMAL(5,2) NOT NULL,
                carving_content TEXT,
                carving_pattern TEXT,
                carving_font TEXT,
                carving_depth TEXT,
                hot_stamping_content TEXT,
                hot_stamping_pattern TEXT,
                hot_stamping_position TEXT,
                polishing_requirement TEXT,
                special_requirements TEXT,
                style TEXT,
                total_price DECIMAL(10,2) NOT NULL,
                lead_days INTEGER NOT NULL,
                delivery_date TIMESTAMP,
                craftsman_id INTEGER,
                craftsman_name TEXT,
                status TEXT NOT NULL DEFAULT '待接单',
                progress_note TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (craftsman_id) REFERENCES craftsmen(id)
            )
        ''')
        
        cursor.execute('SELECT COUNT(*) as count FROM craftsmen')
        if cursor.fetchone()['count'] == 0:
            craftsmen_data = [
                ('张师傅', '13800138001', '雕刻', '高级', 2, '空闲'),
                ('李师傅', '13800138002', '打磨', '中级', 3, '空闲'),
                ('王师傅', '13800138003', '烫花', '高级', 2, '忙碌'),
                ('陈师傅', '13800138004', '全工艺', '特级', 1, '空闲')
            ]
            cursor.executemany('''
                INSERT INTO craftsmen (name, phone, specialty, skill_level, daily_capacity, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', craftsmen_data)
        
        db.commit()

def generate_order_no():
    timestamp = datetime.now().strftime('%Y%m%d%H%M')
    time_ms = int(time.time() * 1000) % 10000
    return f'ZC{timestamp}{time_ms:04d}'

def get_material_options():
    return {
        'material_categories': list(MATERIAL_PRICES.keys()),
        'material_origins': ['内蒙古', '新疆', '西藏', '进口', '本地'],
        'material_grades': list(GRADE_MULTIPLIERS.keys()),
        'carving_patterns': ['祥云纹', '回纹', '水波纹', '龙纹', '凤纹', '花鸟纹', '山水纹', '自定义'],
        'carving_fonts': ['楷书', '行书', '草书', '隶书', '篆书', '魏碑'],
        'carving_depths': list(CARVING_DIFFICULTY.keys()),
        'hot_stamping_patterns': ['祥云', '如意', '莲花', '蝙蝠', '寿字', '福字', '自定义'],
        'hot_stamping_positions': ['正面居中', '正面左侧', '正面右侧', '两端', '全周'],
        'polishing_requirements': list(POLISHING_PRICES.keys()),
        'styles': ['古典', '现代', '简约', '奢华', '中式', '欧式']
    }

@app.route('/api/options', methods=['GET'])
def get_options():
    return success_response(data=get_material_options(), message='获取选项成功')

@app.route('/api/craftsmen', methods=['GET'])
def get_craftsmen():
    status = request.args.get('status')
    specialty = request.args.get('specialty')
    
    cursor = get_db().cursor()
    query = 'SELECT * FROM craftsmen WHERE 1=1'
    params = []
    
    if status:
        query += ' AND status = ?'
        params.append(status)
    if specialty:
        query += ' AND specialty = ?'
        params.append(specialty)
    
    query += ' ORDER BY skill_level DESC, created_at DESC'
    cursor.execute(query, params)
    craftsmen = [dict(row) for row in cursor.fetchall()]
    
    return success_response(data=craftsmen, message='获取匠人列表成功')

@app.route('/api/craftsmen/<int:craftsman_id>', methods=['GET'])
def get_craftsman(craftsman_id):
    cursor = get_db().cursor()
    cursor.execute('SELECT * FROM craftsmen WHERE id = ?', (craftsman_id,))
    craftsman = cursor.fetchone()
    
    if craftsman is None:
        return error_response(message='匠人不存在', code=404)
    
    return success_response(data=dict(craftsman), message='获取匠人信息成功')

@app.route('/api/orders/calculate', methods=['POST'])
def calculate_order():
    data = request.get_json()
    
    errors = validate_order_data(data)
    if errors:
        return error_response(message='参数校验失败', data={'errors': errors})
    
    price = calculate_price(data)
    lead_days = calculate_lead_time(data)
    delivery_date = (datetime.now() + timedelta(days=lead_days)).strftime('%Y-%m-%d')
    
    return success_response(data={
        'total_price': price,
        'lead_days': lead_days,
        'delivery_date': delivery_date
    }, message='计价成功')

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    
    errors = validate_order_data(data)
    if errors:
        return error_response(message='订单数据校验失败', data={'errors': errors})
    
    order_no = generate_order_no()
    total_price = calculate_price(data)
    lead_days = calculate_lead_time(data)
    delivery_date = (datetime.now() + timedelta(days=lead_days)).strftime('%Y-%m-%d')
    
    craftsman_id = data.get('craftsman_id')
    craftsman_name = None
    if craftsman_id:
        cursor = get_db().cursor()
        cursor.execute('SELECT name FROM craftsmen WHERE id = ?', (craftsman_id,))
        craftsman = cursor.fetchone()
        if craftsman:
            craftsman_name = craftsman['name']
    
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO orders (
                order_no, customer_name, customer_phone, customer_address,
                material_category, material_origin, material_grade,
                length_cm, width_cm, thickness_cm,
                carving_content, carving_pattern, carving_font, carving_depth,
                hot_stamping_content, hot_stamping_pattern, hot_stamping_position,
                polishing_requirement, special_requirements, style,
                total_price, lead_days, delivery_date,
                craftsman_id, craftsman_name, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_no,
            data['customer_name'],
            data['customer_phone'],
            data.get('customer_address', ''),
            data['material_category'],
            data.get('material_origin', ''),
            data.get('material_grade', 'B级'),
            data['length_cm'],
            data['width_cm'],
            data['thickness_cm'],
            data.get('carving_content', ''),
            data.get('carving_pattern', ''),
            data.get('carving_font', ''),
            data.get('carving_depth', '中雕(1mm)'),
            data.get('hot_stamping_content', ''),
            data.get('hot_stamping_pattern', ''),
            data.get('hot_stamping_position', ''),
            data.get('polishing_requirement', '亚光'),
            data.get('special_requirements', ''),
            data.get('style', '古典'),
            total_price,
            lead_days,
            delivery_date,
            craftsman_id,
            craftsman_name,
            '待接单'
        ))
        db.commit()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        order = cursor.fetchone()
        
        return success_response(data=dict(order), message='订单创建成功')
        
    except Exception as e:
        db.rollback()
        return error_response(message=f'订单创建失败: {str(e)}', code=500)

@app.route('/api/orders', methods=['GET'])
def get_orders():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    status = request.args.get('status')
    style = request.args.get('style')
    delivery_date_from = request.args.get('delivery_date_from')
    delivery_date_to = request.args.get('delivery_date_to')
    material_category = request.args.get('material_category')
    craftsman_id = request.args.get('craftsman_id')
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')
    
    valid_sort_fields = ['created_at', 'updated_at', 'total_price', 'delivery_date', 'lead_days']
    if sort_by not in valid_sort_fields:
        sort_by = 'created_at'
    if sort_order not in ['asc', 'desc']:
        sort_order = 'desc'
    
    cursor = get_db().cursor()
    
    where_clauses = ['1=1']
    params = []
    
    if status:
        where_clauses.append('status = ?')
        params.append(status)
    if style:
        where_clauses.append('style = ?')
        params.append(style)
    if delivery_date_from:
        where_clauses.append('delivery_date >= ?')
        params.append(delivery_date_from)
    if delivery_date_to:
        where_clauses.append('delivery_date <= ?')
        params.append(delivery_date_to)
    if material_category:
        where_clauses.append('material_category = ?')
        params.append(material_category)
    if craftsman_id:
        where_clauses.append('craftsman_id = ?')
        params.append(craftsman_id)
    
    where_sql = ' AND '.join(where_clauses)
    
    count_sql = f'SELECT COUNT(*) as total FROM orders WHERE {where_sql}'
    cursor.execute(count_sql, params)
    total = cursor.fetchone()['total']
    
    offset = (page - 1) * page_size
    query_sql = f'''
        SELECT * FROM orders 
        WHERE {where_sql}
        ORDER BY {sort_by} {sort_order}
        LIMIT ? OFFSET ?
    '''
    params.extend([page_size, offset])
    cursor.execute(query_sql, params)
    orders = [dict(row) for row in cursor.fetchall()]
    
    total_pages = (total + page_size - 1) // page_size
    
    return success_response(data={
        'list': orders,
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total': total,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    }, message='获取订单列表成功')

@app.route('/api/orders/<order_no>', methods=['GET'])
def get_order(order_no):
    cursor = get_db().cursor()
    cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
    order = cursor.fetchone()
    
    if order is None:
        return error_response(message='订单不存在', code=404)
    
    return success_response(data=dict(order), message='获取订单详情成功')

@app.route('/api/admin/orders/<order_no>/status', methods=['PUT'])
def update_order_status(order_no):
    data = request.get_json()
    new_status = data.get('status')
    progress_note = data.get('progress_note', '')
    
    if new_status not in ORDER_STATUSES:
        return error_response(message=f'无效的订单状态，有效状态: {ORDER_STATUSES}')
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
    if cursor.fetchone() is None:
        return error_response(message='订单不存在', code=404)
    
    try:
        cursor.execute('''
            UPDATE orders 
            SET status = ?, progress_note = ?, updated_at = CURRENT_TIMESTAMP
            WHERE order_no = ?
        ''', (new_status, progress_note, order_no))
        db.commit()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        order = cursor.fetchone()
        
        return success_response(data=dict(order), message='订单状态更新成功')
        
    except Exception as e:
        db.rollback()
        return error_response(message=f'更新失败: {str(e)}', code=500)

@app.route('/api/admin/orders/<order_no>/craftsman', methods=['PUT'])
def assign_craftsman(order_no):
    data = request.get_json()
    craftsman_id = data.get('craftsman_id')
    
    if not craftsman_id:
        return error_response(message='请选择匠人')
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT name FROM craftsmen WHERE id = ?', (craftsman_id,))
    craftsman = cursor.fetchone()
    if craftsman is None:
        return error_response(message='匠人不存在', code=404)
    
    cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
    if cursor.fetchone() is None:
        return error_response(message='订单不存在', code=404)
    
    try:
        cursor.execute('''
            UPDATE orders 
            SET craftsman_id = ?, craftsman_name = ?, updated_at = CURRENT_TIMESTAMP
            WHERE order_no = ?
        ''', (craftsman_id, craftsman['name'], order_no))
        db.commit()
        
        cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
        order = cursor.fetchone()
        
        return success_response(data=dict(order), message='匠人分配成功')
        
    except Exception as e:
        db.rollback()
        return error_response(message=f'分配失败: {str(e)}', code=500)

@app.route('/api/admin/orders/<order_no>', methods=['DELETE'])
def delete_order(order_no):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM orders WHERE order_no = ?', (order_no,))
    if cursor.fetchone() is None:
        return error_response(message='订单不存在', code=404)
    
    try:
        cursor.execute('DELETE FROM orders WHERE order_no = ?', (order_no,))
        db.commit()
        
        return success_response(message='订单删除成功')
        
    except Exception as e:
        db.rollback()
        return error_response(message=f'删除失败: {str(e)}', code=500)

@app.route('/api/statuses', methods=['GET'])
def get_statuses():
    return success_response(data=ORDER_STATUSES, message='获取状态列表成功')

@app.route('/api/health', methods=['GET'])
def health_check():
    return success_response(data={
        'status': 'ok',
        'version': '3.0.0'
    }, message='系统运行正常')

if __name__ == '__main__':
    if os.path.exists('orders.db'):
        os.remove('orders.db')
    init_db()
    print('=' * 80)
    print('传统兽骨镇尺定制订单管理系统后端 v3.0')
    print('=' * 80)
    print('新功能:')
    print('  ✓ 必填字段校验与数值范围规范')
    print('  ✓ 按材料与工艺难度自动计价')
    print('  ✓ 匠人管理及订单绑定')
    print('  ✓ 自动计算工期与交付日期')
    print('  ✓ 多条件筛选(风格/进度/材料/匠人)')
    print('  ✓ 分页排序支持')
    print('  ✓ 统一接口返回格式')
    print('=' * 80)
    print('订单状态流程:')
    print(' -> '.join(ORDER_STATUSES))
    print('=' * 80)
    print('API接口列表:')
    print('GET    /api/health           - 健康检查')
    print('GET    /api/options          - 获取所有选项')
    print('GET    /api/statuses         - 获取订单状态')
    print('GET    /api/craftsmen        - 获取匠人列表')
    print('GET    /api/craftsmen/<id>   - 获取匠人详情')
    print('POST   /api/orders/calculate - 订单预计价')
    print('POST   /api/orders           - 创建订单')
    print('GET    /api/orders           - 查询订单(筛选/分页/排序)')
    print('GET    /api/orders/<no>      - 查询单个订单')
    print('PUT    /api/admin/orders/<no>/status    - 更新订单状态')
    print('PUT    /api/admin/orders/<no>/craftsman - 分配匠人')
    print('DELETE /api/admin/orders/<no>           - 删除订单')
    print('=' * 80)
    app.run(debug=True, host='0.0.0.0', port=5000)
