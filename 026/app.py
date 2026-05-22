from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

ORDER_STATUSES = [
    '待接单', '选线', '打稿', '牵经', '缂丝', '装框', '装柄', '完工'
]

FAN_STYLES = ['圆形团扇', '海棠形团扇', '方形团扇', '芭蕉形团扇', '异形团扇']

SILK_TYPES = ['桑蚕丝', '柞蚕丝', '天丝线', '彩色丝线', '金线']

FRAME_MATERIALS = ['紫竹', '湘妃竹', '梅鹿竹', '紫檀木', '红木', '鸡翅木']

PATTERN_COMPLEXITY = {
    'simple': {'name': '简单', 'base_price': 800, 'days': 7, 'color_min': 3, 'color_max': 8},
    'medium': {'name': '中等', 'base_price': 1500, 'days': 14, 'color_min': 8, 'color_max': 15},
    'complex': {'name': '复杂', 'base_price': 3000, 'days': 25, 'color_min': 15, 'color_max': 30},
    'master': {'name': '大师级', 'base_price': 8000, 'days': 45, 'color_min': 25, 'color_max': 50}
}

def success_response(data=None, message='操作成功', code=200):
    response = {
        'success': True,
        'code': code,
        'message': message,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), code

def error_response(message='操作失败', code=400, errors=None):
    response = {
        'success': False,
        'code': code,
        'message': message,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    if errors is not None:
        response['errors'] = errors
    return jsonify(response), code

class Craftsman(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    skill_level = db.Column(db.String(20))
    specialty = db.Column(db.String(200))
    status = db.Column(db.String(20), default='空闲')
    daily_output = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'skill_level': self.skill_level,
            'specialty': self.specialty,
            'status': self.status,
            'daily_output': self.daily_output,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(20), unique=True, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_address = db.Column(db.String(200))
    fan_style = db.Column(db.String(100), nullable=False)
    pattern_description = db.Column(db.Text, nullable=False)
    size = db.Column(db.String(50))
    material_requirement = db.Column(db.String(200))
    special_requirement = db.Column(db.Text)
    status = db.Column(db.String(20), default='待接单')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    remark = db.Column(db.Text)
    
    silk_thread_type = db.Column(db.String(200))
    pattern_design = db.Column(db.String(200))
    frame_material = db.Column(db.String(100))
    fan_size_width = db.Column(db.String(20))
    fan_size_height = db.Column(db.String(20))
    
    pattern_complexity = db.Column(db.String(20), default='medium')
    calculated_price = db.Column(db.Float)
    estimated_days = db.Column(db.Integer)
    estimated_delivery = db.Column(db.DateTime)
    
    assigned_craftsman_id = db.Column(db.Integer, db.ForeignKey('craftsman.id'))
    assigned_craftsman_name = db.Column(db.String(50))
    
    kesi_technique = db.Column(db.String(200))
    kesi_thread_count = db.Column(db.String(50))
    kesi_color_count = db.Column(db.Integer)
    kesi_completed_at = db.Column(db.DateTime)
    kesi_operator = db.Column(db.String(50))
    
    frame_type = db.Column(db.String(100))
    frame_size = db.Column(db.String(50))
    frame_material_detail = db.Column(db.String(200))
    frame_completed_at = db.Column(db.DateTime)
    frame_operator = db.Column(db.String(50))
    
    handle_material = db.Column(db.String(100))
    handle_style = db.Column(db.String(100))
    handle_length = db.Column(db.String(20))
    handle_completed_at = db.Column(db.DateTime)
    handle_operator = db.Column(db.String(50))

    def to_dict(self):
        return {
            'id': self.id,
            'order_no': self.order_no,
            'customer_name': self.customer_name,
            'customer_phone': self.customer_phone,
            'customer_address': self.customer_address,
            'fan_style': self.fan_style,
            'pattern_description': self.pattern_description,
            'size': self.size,
            'material_requirement': self.material_requirement,
            'special_requirement': self.special_requirement,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
            'remark': self.remark,
            'silk_thread_type': self.silk_thread_type,
            'pattern_design': self.pattern_design,
            'frame_material': self.frame_material,
            'fan_size_width': self.fan_size_width,
            'fan_size_height': self.fan_size_height,
            'pattern_complexity': self.pattern_complexity,
            'calculated_price': self.calculated_price,
            'estimated_days': self.estimated_days,
            'estimated_delivery': self.estimated_delivery.strftime('%Y-%m-%d') if self.estimated_delivery else None,
            'assigned_craftsman_id': self.assigned_craftsman_id,
            'assigned_craftsman_name': self.assigned_craftsman_name,
            'kesi_technique': self.kesi_technique,
            'kesi_thread_count': self.kesi_thread_count,
            'kesi_color_count': self.kesi_color_count,
            'kesi_completed_at': self.kesi_completed_at.strftime('%Y-%m-%d %H:%M:%S') if self.kesi_completed_at else None,
            'kesi_operator': self.kesi_operator,
            'frame_type': self.frame_type,
            'frame_size': self.frame_size,
            'frame_material_detail': self.frame_material_detail,
            'frame_completed_at': self.frame_completed_at.strftime('%Y-%m-%d %H:%M:%S') if self.frame_completed_at else None,
            'frame_operator': self.frame_operator,
            'handle_material': self.handle_material,
            'handle_style': self.handle_style,
            'handle_length': self.handle_length,
            'handle_completed_at': self.handle_completed_at.strftime('%Y-%m-%d %H:%M:%S') if self.handle_completed_at else None,
            'handle_operator': self.handle_operator
        }

def generate_order_no():
    today = datetime.now().strftime('%Y%m%d')
    last_order = Order.query.filter(Order.order_no.like(f'KS{today}%')).order_by(Order.id.desc()).first()
    if last_order:
        last_num = int(last_order.order_no[-4:])
        new_num = str(last_num + 1).zfill(4)
    else:
        new_num = '0001'
    return f'KS{today}{new_num}'

def validate_phone(phone):
    if not phone:
        return False
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, phone))

def calculate_price_and_days(color_count, complexity=None):
    if complexity and complexity in PATTERN_COMPLEXITY:
        config = PATTERN_COMPLEXITY[complexity]
        return config['base_price'], config['days']
    
    if color_count is None:
        color_count = 10
    
    for key in ['simple', 'medium', 'complex', 'master']:
        config = PATTERN_COMPLEXITY[key]
        if config['color_min'] <= color_count <= config['color_max']:
            return config['base_price'], config['days']
    
    return PATTERN_COMPLEXITY['medium']['base_price'], PATTERN_COMPLEXITY['medium']['days']

def validate_order_data(data):
    errors = []
    
    required_fields = ['customer_name', 'customer_phone', 'fan_style', 'pattern_description']
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f'缺少必填字段: {field}')
    
    if 'customer_phone' in data and data['customer_phone']:
        if not validate_phone(data['customer_phone']):
            errors.append('手机号格式不正确，请输入11位有效手机号')
    
    if 'fan_style' in data and data['fan_style']:
        if data['fan_style'] not in FAN_STYLES:
            errors.append(f'团扇风格不支持，可选风格: {FAN_STYLES}')
    
    if 'silk_thread_type' in data and data['silk_thread_type']:
        if data['silk_thread_type'] not in SILK_TYPES:
            errors.append(f'丝线品类不支持，可选品类: {SILK_TYPES}')
    
    if 'frame_material' in data and data['frame_material']:
        if data['frame_material'] not in FRAME_MATERIALS:
            errors.append(f'扇骨材质不支持，可选材质: {FRAME_MATERIALS}')
    
    if 'pattern_complexity' in data and data['pattern_complexity']:
        if data['pattern_complexity'] not in PATTERN_COMPLEXITY:
            errors.append(f'纹样复杂度不支持，可选类型: {list(PATTERN_COMPLEXITY.keys())}')
    
    return errors

@app.route('/api/craftsmen', methods=['POST'])
def create_craftsman():
    data = request.get_json()
    errors = []
    
    if not data.get('name'):
        errors.append('匠人姓名不能为空')
    
    if errors:
        return error_response('创建匠人失败', 400, errors)
    
    existing = Craftsman.query.filter_by(name=data['name']).first()
    if existing:
        return error_response('匠人已存在', 400)
    
    craftsman = Craftsman(
        name=data['name'],
        phone=data.get('phone', ''),
        skill_level=data.get('skill_level', '中级'),
        specialty=data.get('specialty', ''),
        status=data.get('status', '空闲'),
        daily_output=int(data.get('daily_output', 1))
    )
    
    db.session.add(craftsman)
    db.session.commit()
    
    return success_response(craftsman.to_dict(), '匠人创建成功', 201)

@app.route('/api/craftsmen', methods=['GET'])
def get_craftsmen():
    status = request.args.get('status')
    query = Craftsman.query
    
    if status:
        query = query.filter_by(status=status)
    
    craftsmen = query.all()
    return success_response([c.to_dict() for c in craftsmen], '查询成功', 200)

@app.route('/api/craftsmen/<int:id>', methods=['GET'])
def get_craftsman(id):
    craftsman = Craftsman.query.get(id)
    if not craftsman:
        return error_response('匠人不存在', 404)
    return success_response(craftsman.to_dict()), 200

@app.route('/api/craftsmen/<int:id>', methods=['PUT'])
def update_craftsman(id):
    craftsman = Craftsman.query.get(id)
    if not craftsman:
        return error_response('匠人不存在', 404)
    
    data = request.get_json()
    updatable_fields = ['name', 'phone', 'skill_level', 'specialty', 'status', 'daily_output']
    
    for field in updatable_fields:
        if field in data:
            setattr(craftsman, field, data[field])
    
    db.session.commit()
    return success_response(craftsman.to_dict(), '匠人信息更新成功'), 200

@app.route('/api/craftsmen/<int:id>', methods=['DELETE'])
def delete_craftsman(id):
    craftsman = Craftsman.query.get(id)
    if not craftsman:
        return error_response('匠人不存在', 404)
    
    db.session.delete(craftsman)
    db.session.commit()
    return success_response(None, '匠人删除成功'), 200

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    
    errors = validate_order_data(data)
    if errors:
        return error_response('订单验证失败', 400, errors)
    
    order_no = generate_order_no()
    
    complexity = data.get('pattern_complexity', 'medium')
    color_count = data.get('kesi_color_count', 10)
    price, days = calculate_price_and_days(color_count, complexity)
    
    order = Order(
        order_no=order_no,
        customer_name=data['customer_name'],
        customer_phone=data['customer_phone'],
        customer_address=data.get('customer_address', ''),
        fan_style=data['fan_style'],
        pattern_description=data['pattern_description'],
        size=data.get('size', ''),
        material_requirement=data.get('material_requirement', ''),
        special_requirement=data.get('special_requirement', ''),
        remark=data.get('remark', ''),
        silk_thread_type=data.get('silk_thread_type', ''),
        pattern_design=data.get('pattern_design', ''),
        frame_material=data.get('frame_material', ''),
        fan_size_width=data.get('fan_size_width', ''),
        fan_size_height=data.get('fan_size_height', ''),
        pattern_complexity=complexity,
        calculated_price=price,
        estimated_days=days,
        estimated_delivery=datetime.now() + timedelta(days=days),
        kesi_technique=data.get('kesi_technique', ''),
        kesi_thread_count=data.get('kesi_thread_count', ''),
        kesi_color_count=color_count if isinstance(color_count, int) else None,
        frame_type=data.get('frame_type', ''),
        frame_size=data.get('frame_size', ''),
        frame_material_detail=data.get('frame_material_detail', ''),
        handle_material=data.get('handle_material', ''),
        handle_style=data.get('handle_style', ''),
        handle_length=data.get('handle_length', '')
    )
    
    db.session.add(order)
    db.session.commit()
    
    return success_response(order.to_dict(), '订单创建成功', 201)

@app.route('/api/orders', methods=['GET'])
def get_orders():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    status = request.args.get('status')
    fan_style = request.args.get('fan_style')
    craftsman = request.args.get('craftsman')
    delivery_from = request.args.get('delivery_from')
    delivery_to = request.args.get('delivery_to')
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')
    
    query = Order.query
    
    if status and status in ORDER_STATUSES:
        query = query.filter_by(status=status)
    
    if fan_style:
        query = query.filter_by(fan_style=fan_style)
    
    if craftsman:
        query = query.filter(Order.assigned_craftsman_name.like(f'%{craftsman}%'))
    
    if delivery_from:
        try:
            from_date = datetime.strptime(delivery_from, '%Y-%m-%d')
            query = query.filter(Order.estimated_delivery >= from_date)
        except:
            pass
    
    if delivery_to:
        try:
            to_date = datetime.strptime(delivery_to, '%Y-%m-%d')
            query = query.filter(Order.estimated_delivery <= to_date)
        except:
            pass
    
    sort_column = getattr(Order, sort_by, Order.created_at)
    if sort_order == 'asc':
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    result = {
        'orders': [order.to_dict() for order in pagination.items],
        'pagination': {
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    }
    
    return success_response(result), 200

@app.route('/api/orders/<order_no>', methods=['GET'])
def get_order(order_no):
    order = Order.query.filter_by(order_no=order_no).first()
    if not order:
        return error_response('订单不存在', 404)
    return success_response(order.to_dict()), 200

@app.route('/api/orders/<order_no>/assign', methods=['PUT'])
def assign_craftsman(order_no):
    order = Order.query.filter_by(order_no=order_no).first()
    if not order:
        return error_response('订单不存在', 404)
    
    data = request.get_json()
    craftsman_id = data.get('craftsman_id')
    
    if not craftsman_id:
        return error_response('请指定匠人ID', 400)
    
    craftsman = Craftsman.query.get(craftsman_id)
    if not craftsman:
        return error_response('匠人不存在', 404)
    
    if craftsman.status != '空闲':
        return error_response('该匠人当前忙碌，请选择其他匠人', 400)
    
    order.assigned_craftsman_id = craftsman_id
    order.assigned_craftsman_name = craftsman.name
    craftsman.status = '忙碌'
    
    db.session.commit()
    
    return success_response(order.to_dict(), '匠人分配成功'), 200

@app.route('/api/orders/<order_no>/status', methods=['PUT'])
def update_order_status(order_no):
    order = Order.query.filter_by(order_no=order_no).first()
    if not order:
        return error_response('订单不存在', 404)
    
    data = request.get_json()
    new_status = data.get('status')
    
    if new_status not in ORDER_STATUSES:
        return error_response(f'无效的订单状态，有效状态为: {ORDER_STATUSES}', 400)
    
    order.status = new_status
    if 'remark' in data:
        order.remark = data['remark']
    
    db.session.commit()
    
    return success_response(order.to_dict(), '订单状态更新成功'), 200

@app.route('/api/orders/<order_no>', methods=['PUT'])
def update_order(order_no):
    order = Order.query.filter_by(order_no=order_no).first()
    if not order:
        return error_response('订单不存在', 404)
    
    data = request.get_json()
    
    updatable_fields = [
        'customer_name', 'customer_phone', 'customer_address',
        'fan_style', 'pattern_description', 'size',
        'material_requirement', 'special_requirement', 'remark',
        'silk_thread_type', 'pattern_design', 'frame_material',
        'fan_size_width', 'fan_size_height',
        'pattern_complexity',
        'kesi_technique', 'kesi_thread_count', 'kesi_color_count',
        'kesi_operator',
        'frame_type', 'frame_size', 'frame_material_detail',
        'frame_operator',
        'handle_material', 'handle_style', 'handle_length',
        'handle_operator'
    ]
    
    for field in updatable_fields:
        if field in data:
            setattr(order, field, data[field])
    
    if 'kesi_color_count' in data or 'pattern_complexity' in data:
        color_count = data.get('kesi_color_count', order.kesi_color_count)
        complexity = data.get('pattern_complexity', order.pattern_complexity)
        price, days = calculate_price_and_days(color_count, complexity)
        order.calculated_price = price
        order.estimated_days = days
        order.estimated_delivery = order.created_at + timedelta(days=days)
    
    db.session.commit()
    
    return success_response(order.to_dict(), '订单更新成功'), 200

@app.route('/api/orders/<order_no>/kesi', methods=['PUT'])
def update_kesi_detail(order_no):
    order = Order.query.filter_by(order_no=order_no).first()
    if not order:
        return error_response('订单不存在', 404)
    
    data = request.get_json()
    
    kesi_fields = [
        'kesi_technique', 'kesi_thread_count', 'kesi_color_count',
        'kesi_operator'
    ]
    
    for field in kesi_fields:
        if field in data:
            setattr(order, field, data[field])
    
    if data.get('completed', False):
        order.kesi_completed_at = datetime.now()
        order.status = '装框'
    
    db.session.commit()
    
    return success_response(order.to_dict(), '缂丝工序信息更新成功'), 200

@app.route('/api/orders/<order_no>/frame', methods=['PUT'])
def update_frame_detail(order_no):
    order = Order.query.filter_by(order_no=order_no).first()
    if not order:
        return error_response('订单不存在', 404)
    
    data = request.get_json()
    
    frame_fields = [
        'frame_type', 'frame_size', 'frame_material_detail',
        'frame_operator'
    ]
    
    for field in frame_fields:
        if field in data:
            setattr(order, field, data[field])
    
    if data.get('completed', False):
        order.frame_completed_at = datetime.now()
        order.status = '装柄'
    
    db.session.commit()
    
    return success_response(order.to_dict(), '装框工序信息更新成功'), 200

@app.route('/api/orders/<order_no>/handle', methods=['PUT'])
def update_handle_detail(order_no):
    order = Order.query.filter_by(order_no=order_no).first()
    if not order:
        return error_response('订单不存在', 404)
    
    data = request.get_json()
    
    handle_fields = [
        'handle_material', 'handle_style', 'handle_length',
        'handle_operator'
    ]
    
    for field in handle_fields:
        if field in data:
            setattr(order, field, data[field])
    
    if data.get('completed', False):
        order.handle_completed_at = datetime.now()
        order.status = '完工'
        
        if order.assigned_craftsman_id:
            craftsman = Craftsman.query.get(order.assigned_craftsman_id)
            if craftsman:
                craftsman.status = '空闲'
    
    db.session.commit()
    
    return success_response(order.to_dict(), '装柄工序信息更新成功'), 200

@app.route('/api/orders/<order_no>', methods=['DELETE'])
def delete_order(order_no):
    order = Order.query.filter_by(order_no=order_no).first()
    if not order:
        return error_response('订单不存在', 404)
    
    if order.assigned_craftsman_id:
        craftsman = Craftsman.query.get(order.assigned_craftsman_id)
        if craftsman:
            craftsman.status = '空闲'
    
    db.session.delete(order)
    db.session.commit()
    
    return success_response(None, '订单删除成功'), 200

@app.route('/api/statuses', methods=['GET'])
def get_statuses():
    data = {
        'order_statuses': ORDER_STATUSES,
        'fan_styles': FAN_STYLES,
        'silk_types': SILK_TYPES,
        'frame_materials': FRAME_MATERIALS,
        'pattern_complexity': {k: v['name'] for k, v in PATTERN_COMPLEXITY.items()}
    }
    return success_response(data), 200

@app.route('/api/price/calculate', methods=['POST'])
def calculate_order_price():
    data = request.get_json()
    
    complexity = data.get('pattern_complexity', 'medium')
    color_count = data.get('kesi_color_count', 10)
    
    price, days = calculate_price_and_days(color_count, complexity)
    
    result = {
        'pattern_complexity': complexity,
        'complexity_name': PATTERN_COMPLEXITY[complexity]['name'],
        'color_count': color_count,
        'calculated_price': price,
        'estimated_days': days,
        'estimated_delivery': (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
    }
    
    return success_response(result, '价格计算成功'), 200

@app.route('/health', methods=['GET'])
def health_check():
    return success_response({
        'service': '缂丝团扇订单管理系统',
        'version': '2.0.0',
        'features': [
            '统一接口返回格式',
            '必填字段校验',
            '规范选项验证',
            '纹样复杂度自动计价',
            '匠人绑定与工期管理',
            '多条件筛选查询',
            '分页排序功能'
        ]
    }, '系统运行正常'), 200

@app.errorhandler(404)
def not_found(error):
    return error_response('请求的资源不存在', 404)

@app.errorhandler(500)
def internal_error(error):
    return error_response('服务器内部错误', 500)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print('数据库初始化完成')
    app.run(debug=True, host='0.0.0.0', port=5000)
