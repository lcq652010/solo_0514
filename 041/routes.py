from flask import request, jsonify
from app import app, db
from models import Order, ORDER_STATUS, BODY_MATERIALS, BOTTLE_STYLES
from models import DECORATIVE_PATTERNS, ENAMEL_COLORS, COMPLEXITY_LEVELS, CRAFTSMEN
from models import generate_order_no, calculate_price, calculate_days, estimate_delivery_date, get_craftsman_by_id, validate_order_data
from datetime import datetime


@app.route('/')
def index():
    return jsonify({
        'message': '传统珐琅彩鼻烟壶定制订单管理系统',
        'version': '3.0.0',
        'status': 'running',
        'description': '支持自动计价、匠人工期绑定、多条件筛选排序'
    })


@app.route('/api/options', methods=['GET'])
def get_options():
    return jsonify({
        'order_status': ORDER_STATUS,
        'body_materials': BODY_MATERIALS,
        'bottle_styles': BOTTLE_STYLES,
        'decorative_patterns': DECORATIVE_PATTERNS,
        'enamel_colors': ENAMEL_COLORS,
        'complexity_levels': COMPLEXITY_LEVELS,
        'craftsmen': CRAFTSMEN
    })


@app.route('/api/calculate-price', methods=['POST'])
def api_calculate_price():
    data = request.get_json()
    body_material = data.get('body_material', '紫铜胎')
    complexity = data.get('complexity', '中等')
    enamel_color_system = data.get('enamel_color_system', '宝石蓝')
    quantity = data.get('quantity', 1)
    craftsman_id = data.get('craftsman_id')
    
    craftsman_factor = 1.0
    if craftsman_id:
        craftsman = get_craftsman_by_id(int(craftsman_id))
        if craftsman:
            craftsman_factor = craftsman['price_factor']
    
    price_detail = calculate_price(body_material, complexity, enamel_color_system, quantity, craftsman_factor)
    estimated_days = calculate_days(complexity)
    delivery_date = estimate_delivery_date(complexity=complexity)
    
    return jsonify({
        'price_detail': price_detail,
        'estimated_days': estimated_days,
        'estimated_delivery': delivery_date.strftime('%Y-%m-%d')
    })


@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    
    errors = validate_order_data(data)
    if errors:
        return jsonify({'errors': errors}), 400
    
    order_no = generate_order_no()
    
    complexity = data.get('complexity', '中等')
    quantity = data.get('quantity', 1)
    craftsman_id = data.get('craftsman_id')
    
    craftsman_factor = 1.0
    craftsman_name = None
    if craftsman_id:
        craftsman = get_craftsman_by_id(int(craftsman_id))
        if craftsman:
            craftsman_factor = craftsman['price_factor']
            craftsman_name = craftsman['name']
    
    price_detail = calculate_price(
        data['body_material'],
        complexity,
        data['enamel_color_system'],
        quantity,
        craftsman_factor
    )
    
    estimated_days = calculate_days(complexity)
    estimated_delivery = estimate_delivery_date(complexity=complexity)
    
    order = Order(
        order_no=order_no,
        customer_name=data['customer_name'],
        customer_phone=data['customer_phone'],
        customer_address=data.get('customer_address', ''),
        bottle_style=data.get('bottle_style', ''),
        bottle_dimensions=data.get('bottle_dimensions', ''),
        body_material=data['body_material'],
        decorative_pattern=data['decorative_pattern'],
        pattern_detail=data.get('pattern_detail', ''),
        enamel_color_system=data['enamel_color_system'],
        complexity=complexity,
        glaze_requirement=data.get('glaze_requirement', ''),
        painting_detail=data.get('painting_detail', ''),
        firing_requirement=data.get('firing_requirement', ''),
        craftsman_id=craftsman_id,
        craftsman_name=craftsman_name,
        estimated_days=estimated_days,
        estimated_delivery=estimated_delivery,
        special_requirement=data.get('special_requirement', ''),
        quantity=quantity,
        base_price=price_detail['base_price'],
        material_price=price_detail['material_price'],
        complexity_price=price_detail['complexity_price'],
        color_price=price_detail['color_price'],
        craftsman_price=price_detail['craftsman_price'],
        estimated_price=price_detail['estimated_price'],
        remarks=data.get('remarks', '')
    )
    
    db.session.add(order)
    db.session.commit()
    
    return jsonify({
        'message': '订单创建成功',
        'order': order.to_dict()
    }), 201


@app.route('/api/orders', methods=['GET'])
def get_orders():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status', '')
    bottle_style = request.args.get('bottle_style', '')
    decorative_pattern = request.args.get('decorative_pattern', '')
    body_material = request.args.get('body_material', '')
    complexity = request.args.get('complexity', '')
    craftsman_id = request.args.get('craftsman_id', '')
    delivery_start = request.args.get('delivery_start', '')
    delivery_end = request.args.get('delivery_end', '')
    keyword = request.args.get('keyword', '')
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')
    
    query = Order.query
    
    if status and status in ORDER_STATUS:
        query = query.filter_by(status=status)
    
    if bottle_style and bottle_style in BOTTLE_STYLES:
        query = query.filter_by(bottle_style=bottle_style)
    
    if decorative_pattern and decorative_pattern in DECORATIVE_PATTERNS:
        query = query.filter_by(decorative_pattern=decorative_pattern)
    
    if body_material and body_material in BODY_MATERIALS:
        query = query.filter_by(body_material=body_material)
    
    if complexity and complexity in COMPLEXITY_LEVELS:
        query = query.filter_by(complexity=complexity)
    
    if craftsman_id:
        query = query.filter_by(craftsman_id=int(craftsman_id))
    
    if delivery_start:
        try:
            start_date = datetime.strptime(delivery_start, '%Y-%m-%d')
            query = query.filter(Order.estimated_delivery >= start_date)
        except ValueError:
            pass
    
    if delivery_end:
        try:
            end_date = datetime.strptime(delivery_end, '%Y-%m-%d')
            query = query.filter(Order.estimated_delivery <= end_date)
        except ValueError:
            pass
    
    if keyword:
        query = query.filter(
            (Order.order_no.like(f'%{keyword}%')) |
            (Order.customer_name.like(f'%{keyword}%')) |
            (Order.customer_phone.like(f'%{keyword}%'))
        )
    
    sort_column = getattr(Order, sort_by, Order.created_at)
    if sort_order == 'desc':
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'orders': [order.to_dict() for order in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    })


@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': '订单不存在'}), 404
    return jsonify(order.to_dict())


@app.route('/api/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': '订单不存在'}), 404
    
    data = request.get_json()
    
    if 'customer_name' in data:
        order.customer_name = data['customer_name']
    if 'customer_phone' in data:
        order.customer_phone = data['customer_phone']
    if 'customer_address' in data:
        order.customer_address = data['customer_address']
    if 'bottle_style' in data:
        order.bottle_style = data['bottle_style']
    if 'bottle_dimensions' in data:
        order.bottle_dimensions = data['bottle_dimensions']
    if 'body_material' in data:
        order.body_material = data['body_material']
    if 'decorative_pattern' in data:
        order.decorative_pattern = data['decorative_pattern']
    if 'pattern_detail' in data:
        order.pattern_detail = data['pattern_detail']
    if 'enamel_color_system' in data:
        order.enamel_color_system = data['enamel_color_system']
    if 'complexity' in data:
        order.complexity = data['complexity']
    if 'glaze_requirement' in data:
        order.glaze_requirement = data['glaze_requirement']
    if 'painting_detail' in data:
        order.painting_detail = data['painting_detail']
    if 'firing_requirement' in data:
        order.firing_requirement = data['firing_requirement']
    
    if 'craftsman_id' in data:
        craftsman = get_craftsman_by_id(int(data['craftsman_id']))
        if craftsman:
            order.craftsman_id = data['craftsman_id']
            order.craftsman_name = craftsman['name']
    
    if 'actual_delivery' in data and data['actual_delivery']:
        try:
            order.actual_delivery = datetime.strptime(data['actual_delivery'], '%Y-%m-%d')
        except ValueError:
            pass
    
    if 'special_requirement' in data:
        order.special_requirement = data['special_requirement']
    if 'quantity' in data:
        order.quantity = data['quantity']
    if 'remarks' in data:
        order.remarks = data['remarks']
    
    db.session.commit()
    return jsonify({
        'message': '订单更新成功',
        'order': order.to_dict()
    })


@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': '订单不存在'}), 404
    
    data = request.get_json()
    if 'status' not in data:
        return jsonify({'error': '缺少状态字段'}), 400
    
    if data['status'] not in ORDER_STATUS:
        return jsonify({'error': f'无效的状态值，可选值: {", ".join(ORDER_STATUS)}'}), 400
    
    order.status = data['status']
    
    if data['status'] == '完工':
        order.actual_delivery = datetime.now()
    
    db.session.commit()
    return jsonify({
        'message': '订单状态更新成功',
        'order': order.to_dict()
    })


@app.route('/api/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': '订单不存在'}), 404
    
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': '订单删除成功'})


@app.route('/api/status', methods=['GET'])
def get_status_list():
    return jsonify({
        'status_list': ORDER_STATUS
    })