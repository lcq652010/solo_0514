from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///brush_orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

ORDER_STATUSES = ['待接单', '选料', '理毛', '修毫', '装杆', '整笔', '完工']

HAIR_TYPE_PRICES = {
    '狼毫': 50,
    '羊毫': 30,
    '兼毫': 40,
    '紫毫': 80,
    '鸡毫': 25,
    '鼠毫': 60,
    '鹿毫': 45
}

HANDLE_MATERIAL_PRICES = {
    '竹制': 20,
    '红木': 80,
    '紫檀': 150,
    '牛角': 100,
    '象牙': 200,
    '檀木': 120,
    '鸡翅木': 60
}

DIFFICULTY_MULTIPLIERS = {
    '简单': 1.0,
    '普通': 1.2,
    '中等': 1.5,
    '复杂': 2.0,
    '极难': 2.5
}

CRAFTSMEN = [
    {'id': 1, 'name': '张师傅', 'skill': '理毛/修毫', 'capacity': 5},
    {'id': 2, 'name': '李师傅', 'skill': '装杆/整笔', 'capacity': 8},
    {'id': 3, 'name': '王师傅', 'skill': '选料/制笔', 'capacity': 6},
    {'id': 4, 'name': '赵师傅', 'skill': '全工序', 'capacity': 4}
]

def success_response(data=None, message='操作成功', code=200):
    return jsonify({
        'success': True,
        'code': code,
        'message': message,
        'data': data,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }), code

def error_response(message='操作失败', code=400, errors=None):
    return jsonify({
        'success': False,
        'code': code,
        'message': message,
        'errors': errors,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }), code

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(20), unique=True, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_address = db.Column(db.String(200))
    brush_type = db.Column(db.String(100), nullable=False)
    brush_size = db.Column(db.String(50))
    hair_type = db.Column(db.String(100), nullable=False)
    tip_length = db.Column(db.String(50))
    handle_material = db.Column(db.String(100), nullable=False)
    handle_size = db.Column(db.String(50))
    grooming_spec = db.Column(db.Text)
    trimming_spec = db.Column(db.Text)
    mounting_spec = db.Column(db.Text)
    quantity = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String(20), default='普通')
    unit_price = db.Column(db.Float, default=0.0)
    total_price = db.Column(db.Float, default=0.0)
    craftsman_id = db.Column(db.Integer)
    craftsman_name = db.Column(db.String(100))
    work_days = db.Column(db.Integer, default=7)
    delivery_date = db.Column(db.DateTime)
    requirements = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False, default='待接单')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'order_no': self.order_no,
            'customer_name': self.customer_name,
            'customer_phone': self.customer_phone,
            'customer_address': self.customer_address,
            'brush_type': self.brush_type,
            'brush_size': self.brush_size,
            'hair_type': self.hair_type,
            'tip_length': self.tip_length,
            'handle_material': self.handle_material,
            'handle_size': self.handle_size,
            'grooming_spec': self.grooming_spec,
            'trimming_spec': self.trimming_spec,
            'mounting_spec': self.mounting_spec,
            'quantity': self.quantity,
            'difficulty': self.difficulty,
            'unit_price': self.unit_price,
            'total_price': self.total_price,
            'craftsman_id': self.craftsman_id,
            'craftsman_name': self.craftsman_name,
            'work_days': self.work_days,
            'delivery_date': self.delivery_date.strftime('%Y-%m-%d') if self.delivery_date else None,
            'requirements': self.requirements,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

def validate_phone(phone):
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, phone))

def calculate_price(hair_type, handle_material, difficulty, quantity):
    hair_price = HAIR_TYPE_PRICES.get(hair_type, 40)
    handle_price = HANDLE_MATERIAL_PRICES.get(handle_material, 30)
    multiplier = DIFFICULTY_MULTIPLIERS.get(difficulty, 1.2)
    base_price = (hair_price + handle_price) * multiplier
    unit_price = round(base_price, 2)
    total_price = round(unit_price * quantity, 2)
    return unit_price, total_price

def calculate_work_days(difficulty, quantity):
    base_days = 5
    if difficulty == '简单':
        base_days = 3
    elif difficulty == '中等':
        base_days = 7
    elif difficulty == '复杂':
        base_days = 10
    elif difficulty == '极难':
        base_days = 15
    extra_days = (quantity - 1) // 5
    return base_days + extra_days

def generate_order_no():
    today = datetime.now().strftime('%Y%m%d')
    prefix = f'MB{today}'
    last_order = Order.query.filter(Order.order_no.like(f'{prefix}%')).order_by(Order.order_no.desc()).first()
    if last_order:
        last_num = int(last_order.order_no[-4:])
        new_num = str(last_num + 1).zfill(4)
    else:
        new_num = '0001'
    return f'{prefix}{new_num}'

def validate_order_data(data):
    errors = []
    if not data:
        errors.append('请求数据不能为空')
        return errors
    if 'customer_name' not in data or not data['customer_name'].strip():
        errors.append('客户姓名不能为空')
    if 'customer_phone' not in data or not data['customer_phone'].strip():
        errors.append('客户电话不能为空')
    elif not validate_phone(data['customer_phone']):
        errors.append('客户电话格式不正确')
    if 'brush_type' not in data or not data['brush_type'].strip():
        errors.append('毛笔款式不能为空')
    if 'hair_type' not in data or not data['hair_type'].strip():
        errors.append('毫毛类型不能为空')
    if 'handle_material' not in data or not data['handle_material'].strip():
        errors.append('笔杆材质不能为空')
    if 'quantity' not in data:
        errors.append('数量不能为空')
    elif not isinstance(data['quantity'], int) or data['quantity'] <= 0:
        errors.append('数量必须是正整数')
    elif data['quantity'] > 100:
        errors.append('单次订单数量不能超过100支')
    if 'difficulty' in data and data['difficulty'] not in DIFFICULTY_MULTIPLIERS:
        errors.append(f'难度等级必须是: {", ".join(DIFFICULTY_MULTIPLIERS.keys())}')
    return errors

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    errors = validate_order_data(data)
    if errors:
        return error_response('数据验证失败', 400, errors)
    order_no = generate_order_no()
    difficulty = data.get('difficulty', '普通')
    unit_price, total_price = calculate_price(
        data['hair_type'],
        data['handle_material'],
        difficulty,
        data['quantity']
    )
    work_days = calculate_work_days(difficulty, data['quantity'])
    delivery_date = datetime.now() + timedelta(days=work_days)
    new_order = Order(
        order_no=order_no,
        customer_name=data['customer_name'],
        customer_phone=data['customer_phone'],
        customer_address=data.get('customer_address', ''),
        brush_type=data['brush_type'],
        brush_size=data.get('brush_size', ''),
        hair_type=data['hair_type'],
        tip_length=data.get('tip_length', ''),
        handle_material=data['handle_material'],
        handle_size=data.get('handle_size', ''),
        grooming_spec=data.get('grooming_spec', ''),
        trimming_spec=data.get('trimming_spec', ''),
        mounting_spec=data.get('mounting_spec', ''),
        quantity=data['quantity'],
        difficulty=difficulty,
        unit_price=unit_price,
        total_price=total_price,
        work_days=work_days,
        delivery_date=delivery_date,
        requirements=data.get('requirements', ''),
        status='待接单'
    )
    db.session.add(new_order)
    db.session.commit()
    return success_response({'order': new_order.to_dict()}, '订单创建成功', 201)

@app.route('/api/orders', methods=['GET'])
def get_orders():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    brush_type = request.args.get('brush_type', '')
    status = request.args.get('status', '')
    delivery_date_start = request.args.get('delivery_date_start', '')
    delivery_date_end = request.args.get('delivery_date_end', '')
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')
    query = Order.query
    if brush_type:
        query = query.filter(Order.brush_type.like(f'%{brush_type}%'))
    if status and status in ORDER_STATUSES:
        query = query.filter(Order.status == status)
    if delivery_date_start:
        try:
            start_date = datetime.strptime(delivery_date_start, '%Y-%m-%d')
            query = query.filter(Order.delivery_date >= start_date)
        except ValueError:
            pass
    if delivery_date_end:
        try:
            end_date = datetime.strptime(delivery_date_end, '%Y-%m-%d')
            query = query.filter(Order.delivery_date <= end_date)
        except ValueError:
            pass
    sort_column = getattr(Order, sort_by, Order.created_at)
    if sort_order == 'asc':
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())
    if per_page > 100:
        per_page = 100
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

@app.route('/api/orders/<order_no>', methods=['GET'])
def get_order(order_no):
    order = Order.query.filter_by(order_no=order_no).first()
    if not order:
        return error_response('订单不存在', 404)
    return success_response({'order': order.to_dict()}, '获取订单详情成功')

@app.route('/api/orders/<order_no>/status', methods=['PUT'])
def update_order_status(order_no):
    order = Order.query.filter_by(order_no=order_no).first()
    if not order:
        return error_response('订单不存在', 404)
    data = request.get_json()
    if not data or 'status' not in data:
        return error_response('缺少状态信息', 400)
    new_status = data['status']
    if new_status not in ORDER_STATUSES:
        return error_response(f'无效的订单状态，必须是: {", ".join(ORDER_STATUSES)}', 400)
    order.status = new_status
    db.session.commit()
    return success_response({'order': order.to_dict()}, '状态更新成功')

@app.route('/api/orders/<order_no>/craftsman', methods=['PUT'])
def assign_craftsman(order_no):
    order = Order.query.filter_by(order_no=order_no).first()
    if not order:
        return error_response('订单不存在', 404)
    data = request.get_json()
    if not data or 'craftsman_id' not in data:
        return error_response('缺少匠人ID', 400)
    craftsman_id = data['craftsman_id']
    craftsman = next((c for c in CRAFTSMEN if c['id'] == craftsman_id), None)
    if not craftsman:
        return error_response('匠人不存在', 400)
    order.craftsman_id = craftsman_id
    order.craftsman_name = craftsman['name']
    db.session.commit()
    return success_response({'order': order.to_dict()}, '匠人绑定成功')

@app.route('/api/orders/<order_no>', methods=['PUT'])
def update_order(order_no):
    order = Order.query.filter_by(order_no=order_no).first()
    if not order:
        return error_response('订单不存在', 404)
    data = request.get_json()
    if not data:
        return error_response('缺少更新信息', 400)
    if 'customer_name' in data:
        if not data['customer_name'].strip():
            return error_response('客户姓名不能为空', 400)
        order.customer_name = data['customer_name']
    if 'customer_phone' in data:
        if not validate_phone(data['customer_phone']):
            return error_response('客户电话格式不正确', 400)
        order.customer_phone = data['customer_phone']
    if 'customer_address' in data:
        order.customer_address = data['customer_address']
    if 'brush_type' in data:
        order.brush_type = data['brush_type']
    if 'brush_size' in data:
        order.brush_size = data['brush_size']
    if 'hair_type' in data:
        order.hair_type = data['hair_type']
    if 'tip_length' in data:
        order.tip_length = data['tip_length']
    if 'handle_material' in data:
        order.handle_material = data['handle_material']
    if 'handle_size' in data:
        order.handle_size = data['handle_size']
    if 'grooming_spec' in data:
        order.grooming_spec = data['grooming_spec']
    if 'trimming_spec' in data:
        order.trimming_spec = data['trimming_spec']
    if 'mounting_spec' in data:
        order.mounting_spec = data['mounting_spec']
    if 'quantity' in data:
        if not isinstance(data['quantity'], int) or data['quantity'] <= 0:
            return error_response('数量必须是正整数', 400)
        order.quantity = data['quantity']
    if 'difficulty' in data:
        if data['difficulty'] not in DIFFICULTY_MULTIPLIERS:
            return error_response(f'难度等级必须是: {", ".join(DIFFICULTY_MULTIPLIERS.keys())}', 400)
        order.difficulty = data['difficulty']
    if 'requirements' in data:
        order.requirements = data['requirements']
    if 'status' in data and data['status'] in ORDER_STATUSES:
        order.status = data['status']
    if any(k in data for k in ['hair_type', 'handle_material', 'difficulty', 'quantity']):
        order.unit_price, order.total_price = calculate_price(
            order.hair_type,
            order.handle_material,
            order.difficulty,
            order.quantity
        )
        order.work_days = calculate_work_days(order.difficulty, order.quantity)
        order.delivery_date = order.created_at + timedelta(days=order.work_days)
    db.session.commit()
    return success_response({'order': order.to_dict()}, '订单更新成功')

@app.route('/api/orders/<order_no>', methods=['DELETE'])
def delete_order(order_no):
    order = Order.query.filter_by(order_no=order_no).first()
    if not order:
        return error_response('订单不存在', 404)
    db.session.delete(order)
    db.session.commit()
    return success_response(None, '订单删除成功')

@app.route('/api/statuses', methods=['GET'])
def get_statuses():
    return success_response({'statuses': ORDER_STATUSES}, '获取状态列表成功')

@app.route('/api/craftsmen', methods=['GET'])
def get_craftsmen():
    return success_response({'craftsmen': CRAFTSMEN}, '获取匠人列表成功')

@app.route('/api/price-config', methods=['GET'])
def get_price_config():
    data = {
        'hair_type_prices': HAIR_TYPE_PRICES,
        'handle_material_prices': HANDLE_MATERIAL_PRICES,
        'difficulty_multipliers': DIFFICULTY_MULTIPLIERS
    }
    return success_response(data, '获取价格配置成功')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
