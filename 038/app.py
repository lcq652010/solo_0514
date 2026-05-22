from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

ORDER_STATUSES = ['待接单', '选料', '开料', '雕刻', '打磨', '烫金', '上油', '完工']

WOOD_VARIETIES = ['紫檀木', '黄杨木', '黑檀木', '黄花梨', '鸡翅木', '酸枝木', '楠木', '桃木', '沉香木', '其他']
CARVING_PATTERNS = ['龙凤呈祥', '梅兰竹菊', '山水风景', '花鸟虫鱼', '人物肖像', '文字篆刻', '吉祥纹饰', '几何图案', '自定义']
SURFACE_TECHNIQUES = ['磨砂处理', '精细抛光', '天然上蜡', '烫金装饰', '描银处理', '彩绘装饰', '复古做旧', '保持原木']
CRAFTSMEN = ['张师傅', '李师傅', '王师傅', '赵师傅', '陈师傅']
DIFFICULTY_LEVELS = ['简单', '中等', '复杂', '大师级']

WOOD_PRICES = {
    '紫檀木': 180,
    '黄杨木': 120,
    '黑檀木': 150,
    '黄花梨': 280,
    '鸡翅木': 100,
    '酸枝木': 160,
    '楠木': 130,
    '桃木': 80,
    '沉香木': 380,
    '其他': 100
}

DIFFICULTY_MULTIPLIER = {
    '简单': 1.0,
    '中等': 1.3,
    '复杂': 1.8,
    '大师级': 2.5
}

PATTERN_DIFFICULTY = {
    '龙凤呈祥': '复杂',
    '梅兰竹菊': '中等',
    '山水风景': '复杂',
    '花鸟虫鱼': '中等',
    '人物肖像': '大师级',
    '文字篆刻': '简单',
    '吉祥纹饰': '中等',
    '几何图案': '简单',
    '自定义': '复杂'
}

WORK_DAYS = {
    '简单': 3,
    '中等': 5,
    '复杂': 8,
    '大师级': 15
}

def success_response(data=None, message='操作成功', code=200):
    response = {
        'success': True,
        'message': message,
        'code': code,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), code

def error_response(message='操作失败', code=400, errors=None):
    response = {
        'success': False,
        'message': message,
        'code': code,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    if errors is not None:
        response['errors'] = errors
    return jsonify(response), code

def validate_phone(phone):
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, phone))

def validate_quantity(quantity):
    return isinstance(quantity, int) and 1 <= quantity <= 100

def calculate_price(wood_variety, carving_pattern, quantity):
    base_price = WOOD_PRICES.get(wood_variety, 100)
    difficulty = PATTERN_DIFFICULTY.get(carving_pattern, '中等')
    multiplier = DIFFICULTY_MULTIPLIER.get(difficulty, 1.3)
    unit_price = round(base_price * multiplier, 2)
    total_price = round(unit_price * quantity, 2)
    return {
        'unit_price': unit_price,
        'total_price': total_price,
        'difficulty': difficulty
    }

def calculate_delivery_date(difficulty, start_date=None):
    if start_date is None:
        start_date = datetime.now()
    work_days = WORK_DAYS.get(difficulty, 5)
    delivery_date = start_date + timedelta(days=work_days)
    return delivery_date

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(20), unique=True, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    material = db.Column(db.String(50), nullable=False)
    wood_variety = db.Column(db.String(50), nullable=False)
    size_spec = db.Column(db.String(100), nullable=False)
    carving_pattern = db.Column(db.String(50), nullable=False)
    surface_technique = db.Column(db.String(50), nullable=False)
    design_requirement = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    craftsman = db.Column(db.String(50))
    work_days = db.Column(db.Integer)
    estimated_delivery = db.Column(db.DateTime)
    status = db.Column(db.String(20), nullable=False, default='待接单')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'order_no': self.order_no,
            'customer_name': self.customer_name,
            'customer_phone': self.customer_phone,
            'material': self.material,
            'wood_variety': self.wood_variety,
            'size_spec': self.size_spec,
            'carving_pattern': self.carving_pattern,
            'surface_technique': self.surface_technique,
            'design_requirement': self.design_requirement,
            'quantity': self.quantity,
            'difficulty': self.difficulty,
            'unit_price': self.unit_price,
            'total_price': self.total_price,
            'craftsman': self.craftsman,
            'work_days': self.work_days,
            'estimated_delivery': self.estimated_delivery.strftime('%Y-%m-%d') if self.estimated_delivery else None,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

def generate_order_no():
    today = datetime.now().strftime('%Y%m%d')
    last_order = Order.query.filter(Order.order_no.like(f'WD{today}%')).order_by(Order.id.desc()).first()
    if last_order:
        last_num = int(last_order.order_no[-4:])
        new_num = str(last_num + 1).zfill(4)
    else:
        new_num = '0001'
    return f'WD{today}{new_num}'

@app.route('/api/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        if not data:
            return error_response('请求数据不能为空', 400)
        
        required_fields = ['customer_name', 'customer_phone', 'material', 'wood_variety', 
                          'size_spec', 'carving_pattern', 'surface_technique', 
                          'design_requirement', 'quantity']
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return error_response('缺少必填字段', 400, {'missing_fields': missing_fields})
        
        validation_errors = {}
        
        if len(data['customer_name'].strip()) < 2 or len(data['customer_name']) > 50:
            validation_errors['customer_name'] = '客户姓名长度应在2-50个字符之间'
        
        if not validate_phone(data['customer_phone']):
            validation_errors['customer_phone'] = '请输入有效的手机号码'
        
        if data['wood_variety'] not in WOOD_VARIETIES:
            validation_errors['wood_variety'] = f'无效的木料品种，可选值: {WOOD_VARIETIES}'
        
        if data['carving_pattern'] not in CARVING_PATTERNS:
            validation_errors['carving_pattern'] = f'无效的雕刻纹样，可选值: {CARVING_PATTERNS}'
        
        if data['surface_technique'] not in SURFACE_TECHNIQUES:
            validation_errors['surface_technique'] = f'无效的表面工艺，可选值: {SURFACE_TECHNIQUES}'
        
        if not validate_quantity(data['quantity']):
            validation_errors['quantity'] = '数量必须是1-100之间的整数'
        
        if len(data['size_spec'].strip()) < 3:
            validation_errors['size_spec'] = '尺寸规格不能为空'
        
        if len(data['design_requirement'].strip()) < 5:
            validation_errors['design_requirement'] = '设计要求至少需要5个字符'
        
        if validation_errors:
            return error_response('数据验证失败', 400, validation_errors)
        
        price_info = calculate_price(data['wood_variety'], data['carving_pattern'], data['quantity'])
        difficulty = price_info['difficulty']
        estimated_delivery = calculate_delivery_date(difficulty)
        
        order_no = generate_order_no()
        new_order = Order(
            order_no=order_no,
            customer_name=data['customer_name'].strip(),
            customer_phone=data['customer_phone'],
            material=data['material'],
            wood_variety=data['wood_variety'],
            size_spec=data['size_spec'],
            carving_pattern=data['carving_pattern'],
            surface_technique=data['surface_technique'],
            design_requirement=data['design_requirement'].strip(),
            quantity=data['quantity'],
            difficulty=difficulty,
            unit_price=price_info['unit_price'],
            total_price=price_info['total_price'],
            work_days=WORK_DAYS.get(difficulty, 5),
            estimated_delivery=estimated_delivery
        )
        db.session.add(new_order)
        db.session.commit()
        
        return success_response({'order': new_order.to_dict()}, '订单创建成功', 201)
    except Exception as e:
        db.session.rollback()
        return error_response(f'创建订单失败: {str(e)}', 500)

@app.route('/api/orders', methods=['GET'])
def get_orders():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status')
        carving_pattern = request.args.get('carving_pattern')
        wood_variety = request.args.get('wood_variety')
        difficulty = request.args.get('difficulty')
        craftsman = request.args.get('craftsman')
        delivery_start = request.args.get('delivery_start')
        delivery_end = request.args.get('delivery_end')
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        
        query = Order.query
        
        if status and status in ORDER_STATUSES:
            query = query.filter_by(status=status)
        if carving_pattern and carving_pattern in CARVING_PATTERNS:
            query = query.filter_by(carving_pattern=carving_pattern)
        if wood_variety and wood_variety in WOOD_VARIETIES:
            query = query.filter_by(wood_variety=wood_variety)
        if difficulty and difficulty in DIFFICULTY_LEVELS:
            query = query.filter_by(difficulty=difficulty)
        if craftsman:
            query = query.filter(Order.craftsman.like(f'%{craftsman}%'))
        if delivery_start:
            try:
                start_date = datetime.strptime(delivery_start, '%Y-%m-%d')
                query = query.filter(Order.estimated_delivery >= start_date)
            except:
                pass
        if delivery_end:
            try:
                end_date = datetime.strptime(delivery_end, '%Y-%m-%d')
                query = query.filter(Order.estimated_delivery <= end_date)
            except:
                pass
        
        valid_sort_columns = ['created_at', 'updated_at', 'total_price', 'estimated_delivery', 'quantity']
        if sort_by in valid_sort_columns:
            sort_column = getattr(Order, sort_by)
            if sort_order == 'asc':
                query = query.order_by(sort_column.asc())
            else:
                query = query.order_by(sort_column.desc())
        
        per_page = min(max(1, per_page), 100)
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        orders = [order.to_dict() for order in pagination.items]
        
        data = {
            'orders': orders,
            'pagination': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }
        
        return success_response(data, '获取订单列表成功')
    except Exception as e:
        return error_response(f'获取订单列表失败: {str(e)}', 500)

@app.route('/api/orders/<order_no>', methods=['GET'])
def get_order(order_no):
    try:
        order = Order.query.filter_by(order_no=order_no).first()
        if not order:
            return error_response('订单不存在', 404)
        return success_response({'order': order.to_dict()}, '获取订单详情成功')
    except Exception as e:
        return error_response(f'获取订单详情失败: {str(e)}', 500)

@app.route('/api/orders/<order_no>/status', methods=['PUT'])
def update_order_status(order_no):
    try:
        order = Order.query.filter_by(order_no=order_no).first()
        if not order:
            return error_response('订单不存在', 404)
        
        data = request.get_json()
        if not data or 'status' not in data:
            return error_response('缺少status字段', 400)
        
        new_status = data['status']
        if new_status not in ORDER_STATUSES:
            return error_response('无效的订单状态', 400, {'valid_statuses': ORDER_STATUSES})
        
        order.status = new_status
        db.session.commit()
        return success_response({'order': order.to_dict()}, '订单状态更新成功')
    except Exception as e:
        db.session.rollback()
        return error_response(f'更新订单状态失败: {str(e)}', 500)

@app.route('/api/orders/<order_no>/assign', methods=['PUT'])
def assign_craftsman(order_no):
    try:
        order = Order.query.filter_by(order_no=order_no).first()
        if not order:
            return error_response('订单不存在', 404)
        
        data = request.get_json()
        if not data or 'craftsman' not in data:
            return error_response('缺少craftsman字段', 400)
        
        craftsman = data['craftsman']
        if craftsman not in CRAFTSMEN:
            return error_response('无效的匠人', 400, {'valid_craftsmen': CRAFTSMEN})
        
        order.craftsman = craftsman
        db.session.commit()
        return success_response({'order': order.to_dict()}, '匠人分配成功')
    except Exception as e:
        db.session.rollback()
        return error_response(f'分配匠人失败: {str(e)}', 500)

@app.route('/api/orders/<order_no>', methods=['PUT'])
def update_order(order_no):
    try:
        order = Order.query.filter_by(order_no=order_no).first()
        if not order:
            return error_response('订单不存在', 404)
        
        data = request.get_json()
        if not data:
            return error_response('请求数据不能为空', 400)
        
        validation_errors = {}
        
        if 'customer_name' in data:
            if len(data['customer_name'].strip()) < 2 or len(data['customer_name']) > 50:
                validation_errors['customer_name'] = '客户姓名长度应在2-50个字符之间'
            else:
                order.customer_name = data['customer_name'].strip()
        
        if 'customer_phone' in data:
            if not validate_phone(data['customer_phone']):
                validation_errors['customer_phone'] = '请输入有效的手机号码'
            else:
                order.customer_phone = data['customer_phone']
        
        if 'material' in data:
            order.material = data['material']
        
        if 'wood_variety' in data:
            if data['wood_variety'] not in WOOD_VARIETIES:
                validation_errors['wood_variety'] = f'无效的木料品种'
            else:
                order.wood_variety = data['wood_variety']
        
        if 'size_spec' in data:
            if len(data['size_spec'].strip()) < 3:
                validation_errors['size_spec'] = '尺寸规格不能为空'
            else:
                order.size_spec = data['size_spec']
        
        if 'carving_pattern' in data:
            if data['carving_pattern'] not in CARVING_PATTERNS:
                validation_errors['carving_pattern'] = f'无效的雕刻纹样'
            else:
                order.carving_pattern = data['carving_pattern']
        
        if 'surface_technique' in data:
            if data['surface_technique'] not in SURFACE_TECHNIQUES:
                validation_errors['surface_technique'] = f'无效的表面工艺'
            else:
                order.surface_technique = data['surface_technique']
        
        if 'design_requirement' in data:
            if len(data['design_requirement'].strip()) < 5:
                validation_errors['design_requirement'] = '设计要求至少需要5个字符'
            else:
                order.design_requirement = data['design_requirement'].strip()
        
        if 'quantity' in data:
            if not validate_quantity(data['quantity']):
                validation_errors['quantity'] = '数量必须是1-100之间的整数'
            else:
                order.quantity = data['quantity']
        
        if 'craftsman' in data:
            if data['craftsman'] not in CRAFTSMEN:
                validation_errors['craftsman'] = f'无效的匠人'
            else:
                order.craftsman = data['craftsman']
        
        if validation_errors:
            return error_response('数据验证失败', 400, validation_errors)
        
        if 'wood_variety' in data or 'carving_pattern' in data or 'quantity' in data:
            price_info = calculate_price(order.wood_variety, order.carving_pattern, order.quantity)
            order.difficulty = price_info['difficulty']
            order.unit_price = price_info['unit_price']
            order.total_price = price_info['total_price']
            order.work_days = WORK_DAYS.get(order.difficulty, 5)
            order.estimated_delivery = calculate_delivery_date(order.difficulty)
        
        db.session.commit()
        return success_response({'order': order.to_dict()}, '订单更新成功')
    except Exception as e:
        db.session.rollback()
        return error_response(f'更新订单失败: {str(e)}', 500)

@app.route('/api/orders/<order_no>', methods=['DELETE'])
def delete_order(order_no):
    try:
        order = Order.query.filter_by(order_no=order_no).first()
        if not order:
            return error_response('订单不存在', 404)
        
        db.session.delete(order)
        db.session.commit()
        return success_response(None, '订单删除成功')
    except Exception as e:
        db.session.rollback()
        return error_response(f'删除订单失败: {str(e)}', 500)

@app.route('/api/price/calculate', methods=['POST'])
def calculate_order_price():
    try:
        data = request.get_json()
        if not data:
            return error_response('请求数据不能为空', 400)
        
        required_fields = ['wood_variety', 'carving_pattern', 'quantity']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return error_response('缺少必填字段', 400, {'missing_fields': missing_fields})
        
        if data['wood_variety'] not in WOOD_VARIETIES:
            return error_response('无效的木料品种', 400)
        if data['carving_pattern'] not in CARVING_PATTERNS:
            return error_response('无效的雕刻纹样', 400)
        if not validate_quantity(data['quantity']):
            return error_response('数量必须是1-100之间的整数', 400)
        
        price_info = calculate_price(data['wood_variety'], data['carving_pattern'], data['quantity'])
        difficulty = price_info['difficulty']
        estimated_delivery = calculate_delivery_date(difficulty)
        
        result = {
            **price_info,
            'wood_price': WOOD_PRICES.get(data['wood_variety'], 100),
            'difficulty_multiplier': DIFFICULTY_MULTIPLIER.get(difficulty, 1.3),
            'work_days': WORK_DAYS.get(difficulty, 5),
            'estimated_delivery': estimated_delivery.strftime('%Y-%m-%d')
        }
        
        return success_response(result, '价格计算成功')
    except Exception as e:
        return error_response(f'价格计算失败: {str(e)}', 500)

@app.route('/api/options', methods=['GET'])
def get_all_options():
    try:
        data = {
            'statuses': ORDER_STATUSES,
            'wood_varieties': WOOD_VARIETIES,
            'carving_patterns': CARVING_PATTERNS,
            'surface_techniques': SURFACE_TECHNIQUES,
            'craftsmen': CRAFTSMEN,
            'difficulty_levels': DIFFICULTY_LEVELS,
            'wood_prices': WOOD_PRICES,
            'difficulty_multiplier': DIFFICULTY_MULTIPLIER,
            'pattern_difficulty': PATTERN_DIFFICULTY
        }
        return success_response(data, '获取配置选项成功')
    except Exception as e:
        return error_response(f'获取配置选项失败: {str(e)}', 500)

@app.route('/api/statuses', methods=['GET'])
def get_statuses():
    return success_response({'statuses': ORDER_STATUSES}, '获取订单状态成功')

@app.route('/api/wood-varieties', methods=['GET'])
def get_wood_varieties():
    return success_response({'wood_varieties': WOOD_VARIETIES, 'prices': WOOD_PRICES}, '获取木料品种成功')

@app.route('/api/carving-patterns', methods=['GET'])
def get_carving_patterns():
    return success_response({'carving_patterns': CARVING_PATTERNS, 'difficulty': PATTERN_DIFFICULTY}, '获取雕刻纹样成功')

@app.route('/api/surface-techniques', methods=['GET'])
def get_surface_techniques():
    return success_response({'surface_techniques': SURFACE_TECHNIQUES}, '获取表面工艺成功')

@app.route('/api/craftsmen', methods=['GET'])
def get_craftsmen():
    return success_response({'craftsmen': CRAFTSMEN}, '获取匠人列表成功')

@app.errorhandler(404)
def not_found(error):
    return error_response('请求的资源不存在', 404)

@app.errorhandler(500)
def internal_error(error):
    return error_response('服务器内部错误', 500)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
