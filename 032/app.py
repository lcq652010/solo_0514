from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import os
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'tin_tea_caddy_secret_key'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

ORDER_STATUSES = [
    '待接单',
    '熔锡',
    '制坯',
    '锻打',
    '雕花',
    '打磨',
    '抛光',
    '完工'
]

MOUTH_STYLES = ['直口', '翻口', '螺旋口', '宽口']

PATTERN_TYPES = ['传统龙纹', '祥云纹', '山水图', '梅兰竹菊', '花鸟图案', '几何纹样', '其他']

TIN_PURITIES = ['99.9%纯锡', '99%纯锡', '97%锡合金']

PRICING_CONFIG = {
    'base_price': 200,
    'tin_premium': {
        '99.9%纯锡': 1.5,
        '99%纯锡': 1.0,
        '97%锡合金': 0.8
    },
    'pattern_difficulty': {
        '传统龙纹': 2.0,
        '山水图': 1.8,
        '花鸟图案': 1.6,
        '梅兰竹菊': 1.4,
        '祥云纹': 1.2,
        '几何纹样': 1.0,
        '其他': 1.0
    },
    'size_multiplier': {
        'small': 1.0,
        'medium': 1.3,
        'large': 1.6
    }
}

WORK_DAYS_CONFIG = {
    'simple': 5,
    'medium': 7,
    'complex': 10
}

def success_response(data=None, message='操作成功', code=200):
    return jsonify({
        'code': code,
        'message': message,
        'data': data,
        'timestamp': datetime.utcnow().isoformat()
    }), code

def error_response(message='操作失败', code=400, errors=None):
    response = {
        'code': code,
        'message': message,
        'timestamp': datetime.utcnow().isoformat()
    }
    if errors:
        response['errors'] = errors
    return jsonify(response), code

def calculate_price(tin_purity, pattern, capacity, quantity=1):
    base = PRICING_CONFIG['base_price']
    tin_multiplier = PRICING_CONFIG['tin_premium'].get(tin_purity, 1.0)
    pattern_multiplier = PRICING_CONFIG['pattern_difficulty'].get(pattern, 1.0)
    
    cap_num = float(re.findall(r'\d+', str(capacity))[0]) if re.findall(r'\d+', str(capacity)) else 250
    if cap_num < 200:
        size_multiplier = PRICING_CONFIG['size_multiplier']['small']
    elif cap_num < 400:
        size_multiplier = PRICING_CONFIG['size_multiplier']['medium']
    else:
        size_multiplier = PRICING_CONFIG['size_multiplier']['large']
    
    total_price = base * tin_multiplier * pattern_multiplier * size_multiplier * quantity
    return round(total_price, 2)

def calculate_work_days(pattern):
    difficulty = PRICING_CONFIG['pattern_difficulty'].get(pattern, 1.0)
    if difficulty <= 1.0:
        return WORK_DAYS_CONFIG['simple']
    elif difficulty <= 1.4:
        return WORK_DAYS_CONFIG['medium']
    else:
        return WORK_DAYS_CONFIG['complex']

def validate_order_data(data):
    errors = []
    
    if 'tin_purity' in data and data['tin_purity'] not in TIN_PURITIES:
        errors.append(f'锡料纯度无效，可选值: {TIN_PURITIES}')
    
    if 'mouth_style' in data and data['mouth_style'] not in MOUTH_STYLES:
        errors.append(f'罐口样式无效，可选值: {MOUTH_STYLES}')
    
    if 'carving_pattern' in data and data['carving_pattern'] not in PATTERN_TYPES:
        errors.append(f'雕刻花纹无效，可选值: {PATTERN_TYPES}')
    
    if 'quantity' in data:
        try:
            qty = int(data['quantity'])
            if qty < 1 or qty > 100:
                errors.append('数量必须在1-100之间')
        except:
            errors.append('数量必须是有效数字')
    
    for dim in ['body_height', 'body_diameter', 'body_thickness']:
        if dim in data and data[dim]:
            val = data[dim]
            if not re.match(r'^\d+(\.\d+)?\s*(cm|mm)$', str(val)):
                errors.append(f'{dim}格式无效，需包含数值和单位(如: 12cm, 2.5mm)')
    
    return errors

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='customer')
    phone = db.Column(db.String(20))
    skills = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'phone': self.phone,
            'skills': self.skills,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(20), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    customer = db.relationship('User', foreign_keys=[customer_id], backref=db.backref('customer_orders', lazy=True))
    craftsman_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    craftsman = db.relationship('User', foreign_keys=[craftsman_id], backref=db.backref('craftsman_orders', lazy=True))
    capacity = db.Column(db.String(50), nullable=False)
    tin_purity = db.Column(db.String(50), nullable=False)
    body_height = db.Column(db.String(20), nullable=False)
    body_diameter = db.Column(db.String(20), nullable=False)
    body_thickness = db.Column(db.String(20), nullable=False)
    mouth_style = db.Column(db.String(50), nullable=False)
    mouth_diameter = db.Column(db.String(20))
    carving_pattern = db.Column(db.String(100), nullable=False)
    carving_position = db.Column(db.String(100))
    engraving_text = db.Column(db.Text)
    design_desc = db.Column(db.Text, nullable=False)
    material = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Float, nullable=False, default=0)
    total_price = db.Column(db.Float, nullable=False, default=0)
    work_days = db.Column(db.Integer, default=7)
    estimated_delivery = db.Column(db.DateTime)
    actual_delivery = db.Column(db.DateTime)
    forging_notes = db.Column(db.Text)
    carving_notes = db.Column(db.Text)
    polishing_notes = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False, default='待接单')
    progress = db.Column(db.Float, nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'order_no': self.order_no,
            'customer_id': self.customer_id,
            'customer_username': self.customer.username if self.customer else None,
            'craftsman_id': self.craftsman_id,
            'craftsman_username': self.craftsman.username if self.craftsman else None,
            'capacity': self.capacity,
            'tin_purity': self.tin_purity,
            'body_size': {
                'height': self.body_height,
                'diameter': self.body_diameter,
                'thickness': self.body_thickness
            },
            'mouth_style': self.mouth_style,
            'mouth_diameter': self.mouth_diameter,
            'carving_pattern': self.carving_pattern,
            'carving_position': self.carving_position,
            'engraving_text': self.engraving_text,
            'design_desc': self.design_desc,
            'material': self.material,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'total_price': self.total_price,
            'work_days': self.work_days,
            'estimated_delivery': self.estimated_delivery.isoformat() if self.estimated_delivery else None,
            'actual_delivery': self.actual_delivery.isoformat() if self.actual_delivery else None,
            'forging_notes': self.forging_notes,
            'carving_notes': self.carving_notes,
            'polishing_notes': self.polishing_notes,
            'status': self.status,
            'progress': self.progress,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

def generate_order_no():
    today = datetime.now().strftime('%Y%m%d')
    count = Order.query.filter(Order.order_no.like(f'{today}%')).count()
    return f'{today}{str(count + 1).zfill(4)}'

def create_tables():
    with app.app_context():
        db.create_all()
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            hashed_pw = bcrypt.generate_password_hash('admin123').decode('utf-8')
            admin = User(username='admin', password=hashed_pw, role='admin')
            db.session.add(admin)
            db.session.commit()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return error_response('缺少必要参数: username, password', 400)
    
    if User.query.filter_by(username=data['username']).first():
        return error_response('用户名已存在', 400)
    
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(
        username=data['username'], 
        password=hashed_pw, 
        role=data.get('role', 'customer'),
        phone=data.get('phone'),
        skills=data.get('skills')
    )
    db.session.add(user)
    db.session.commit()
    
    return success_response({'user': user.to_dict()}, '注册成功', 201)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return error_response('缺少必要参数: username, password', 400)
    
    user = User.query.filter_by(username=data['username']).first()
    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return error_response('用户名或密码错误', 401)
    
    return success_response({'user': user.to_dict()}, '登录成功')

@app.route('/api/orders/calculate', methods=['POST'])
def calculate_order_price():
    data = request.get_json()
    required_fields = ['tin_purity', 'carving_pattern', 'capacity', 'quantity']
    
    for field in required_fields:
        if field not in data:
            return error_response(f'缺少必要参数: {field}', 400)
    
    validation_errors = validate_order_data(data)
    if validation_errors:
        return error_response('参数校验失败', 400, validation_errors)
    
    unit_price = calculate_price(data['tin_purity'], data['carving_pattern'], data['capacity'])
    total_price = unit_price * data.get('quantity', 1)
    work_days = calculate_work_days(data['carving_pattern'])
    
    return success_response({
        'unit_price': unit_price,
        'total_price': round(total_price, 2),
        'work_days': work_days,
        'estimated_delivery': (datetime.now() + timedelta(days=work_days)).isoformat()
    }, '价格计算成功')

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    required_fields = [
        'customer_id', 'capacity', 'tin_purity', 
        'body_height', 'body_diameter', 'body_thickness',
        'mouth_style', 'carving_pattern', 'design_desc', 'material'
    ]
    
    for field in required_fields:
        if field not in data:
            return error_response(f'缺少必要参数: {field}', 400)
    
    validation_errors = validate_order_data(data)
    if validation_errors:
        return error_response('参数校验失败', 400, validation_errors)
    
    customer = User.query.get(data['customer_id'])
    if not customer or customer.role != 'customer':
        return error_response('客户不存在', 404)
    
    quantity = data.get('quantity', 1)
    unit_price = calculate_price(data['tin_purity'], data['carving_pattern'], data['capacity'], 1)
    total_price = unit_price * quantity
    work_days = calculate_work_days(data['carving_pattern'])
    
    order_no = generate_order_no()
    order = Order(
        order_no=order_no,
        customer_id=data['customer_id'],
        capacity=data['capacity'],
        tin_purity=data['tin_purity'],
        body_height=data['body_height'],
        body_diameter=data['body_diameter'],
        body_thickness=data['body_thickness'],
        mouth_style=data['mouth_style'],
        mouth_diameter=data.get('mouth_diameter'),
        carving_pattern=data['carving_pattern'],
        carving_position=data.get('carving_position'),
        engraving_text=data.get('engraving_text'),
        design_desc=data['design_desc'],
        material=data['material'],
        quantity=quantity,
        unit_price=unit_price,
        total_price=total_price,
        work_days=work_days,
        estimated_delivery=datetime.now() + timedelta(days=work_days),
        status='待接单'
    )
    
    db.session.add(order)
    db.session.commit()
    
    return success_response({'order': order.to_dict()}, '订单提交成功', 201)

@app.route('/api/orders', methods=['GET'])
def get_orders():
    status = request.args.get('status')
    customer_id = request.args.get('customer_id')
    craftsman_id = request.args.get('craftsman_id')
    carving_pattern = request.args.get('carving_pattern')
    tin_purity = request.args.get('tin_purity')
    mouth_style = request.args.get('mouth_style')
    delivery_date_from = request.args.get('delivery_date_from')
    delivery_date_to = request.args.get('delivery_date_to')
    progress_min = request.args.get('progress_min')
    progress_max = request.args.get('progress_max')
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')
    
    query = Order.query
    
    if status:
        query = query.filter_by(status=status)
    if customer_id:
        query = query.filter_by(customer_id=customer_id)
    if craftsman_id:
        query = query.filter_by(craftsman_id=craftsman_id)
    if carving_pattern:
        query = query.filter_by(carving_pattern=carving_pattern)
    if tin_purity:
        query = query.filter_by(tin_purity=tin_purity)
    if mouth_style:
        query = query.filter_by(mouth_style=mouth_style)
    
    if progress_min:
        query = query.filter(Order.progress >= float(progress_min))
    if progress_max:
        query = query.filter(Order.progress <= float(progress_max))
    
    if delivery_date_from:
        query = query.filter(Order.estimated_delivery >= datetime.fromisoformat(delivery_date_from))
    if delivery_date_to:
        query = query.filter(Order.estimated_delivery <= datetime.fromisoformat(delivery_date_to))
    
    sort_column = getattr(Order, sort_by, Order.created_at)
    if sort_order == 'asc':
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return success_response({
        'orders': [order.to_dict() for order in pagination.items],
        'pagination': {
            'total': pagination.total,
            'pages': pagination.pages,
            'page': page,
            'per_page': per_page,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    }, '查询成功')

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return error_response('订单不存在', 404)
    return success_response({'order': order.to_dict()}, '查询成功')

@app.route('/api/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()
    order = Order.query.get(order_id)
    
    if not order:
        return error_response('订单不存在', 404)
    
    validation_errors = validate_order_data(data)
    if validation_errors:
        return error_response('参数校验失败', 400, validation_errors)
    
    if 'status' in data:
        if data['status'] not in ORDER_STATUSES:
            return error_response(f'无效状态，可选状态: {ORDER_STATUSES}', 400)
        order.status = data['status']
        order.progress = ORDER_STATUSES.index(data['status']) * 12.5
        if data['status'] == '完工':
            order.actual_delivery = datetime.utcnow()
    
    if 'capacity' in data:
        order.capacity = data['capacity']
    if 'tin_purity' in data:
        order.tin_purity = data['tin_purity']
    if 'body_height' in data:
        order.body_height = data['body_height']
    if 'body_diameter' in data:
        order.body_diameter = data['body_diameter']
    if 'body_thickness' in data:
        order.body_thickness = data['body_thickness']
    if 'mouth_style' in data:
        order.mouth_style = data['mouth_style']
    if 'mouth_diameter' in data:
        order.mouth_diameter = data['mouth_diameter']
    if 'carving_pattern' in data:
        order.carving_pattern = data['carving_pattern']
    if 'carving_position' in data:
        order.carving_position = data['carving_position']
    if 'engraving_text' in data:
        order.engraving_text = data['engraving_text']
    if 'design_desc' in data:
        order.design_desc = data['design_desc']
    if 'material' in data:
        order.material = data['material']
    if 'quantity' in data:
        order.quantity = data['quantity']
    
    if 'craftsman_id' in data:
        craftsman = User.query.get(data['craftsman_id'])
        if craftsman and craftsman.role in ['craftsman', 'admin']:
            order.craftsman_id = data['craftsman_id']
    
    if 'forging_notes' in data:
        order.forging_notes = data['forging_notes']
    if 'carving_notes' in data:
        order.carving_notes = data['carving_notes']
    if 'polishing_notes' in data:
        order.polishing_notes = data['polishing_notes']
    if 'estimated_delivery' in data:
        order.estimated_delivery = datetime.fromisoformat(data['estimated_delivery'])
    
    if 'tin_purity' in data or 'carving_pattern' in data or 'capacity' in data or 'quantity' in data:
        order.unit_price = calculate_price(order.tin_purity, order.carving_pattern, order.capacity)
        order.total_price = order.unit_price * order.quantity
        order.work_days = calculate_work_days(order.carving_pattern)
    
    order.updated_at = datetime.utcnow()
    db.session.commit()
    
    return success_response({'order': order.to_dict()}, '订单更新成功')

@app.route('/api/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return error_response('订单不存在', 404)
    
    db.session.delete(order)
    db.session.commit()
    
    return success_response(None, '订单删除成功')

@app.route('/api/statuses', methods=['GET'])
def get_statuses():
    return success_response({
        'statuses': ORDER_STATUSES,
        'mouth_styles': MOUTH_STYLES,
        'pattern_types': PATTERN_TYPES,
        'tin_purities': TIN_PURITIES,
        'pricing_config': PRICING_CONFIG
    }, '查询成功')

@app.route('/api/users', methods=['GET'])
def get_users():
    role = request.args.get('role')
    query = User.query
    
    if role:
        query = query.filter_by(role=role)
    
    users = query.all()
    return success_response({'users': [user.to_dict() for user in users]}, '查询成功')

@app.route('/api/craftsmen', methods=['GET'])
def get_craftsmen():
    craftsmen = User.query.filter(User.role.in_(['craftsman', 'admin']), User.is_active == True).all()
    return success_response({'craftsmen': [c.to_dict() for c in craftsmen]}, '查询成功')

if __name__ == '__main__':
    create_tables()
    app.run(debug=True, host='0.0.0.0', port=5000)