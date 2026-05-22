from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inkstone.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
db = SQLAlchemy(app)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


STONE_DENSITY = {
    '端溪石': 2.75,
    '歙石': 2.8,
    '洮河石': 2.65,
    '澄泥砚': 2.4,
    '红丝石': 2.7,
    '松花石': 2.6,
    '其他': 2.7
}


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    orders = db.relationship('Order', backref='customer', lazy=True)


class Craftsman(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    skill_level = db.Column(db.String(50))
    status = db.Column(db.String(20), default='available')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    orders = db.relationship('Order', backref='craftsman', lazy=True)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    craftsman_id = db.Column(db.Integer, db.ForeignKey('craftsman.id'))
    inkstone_type = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(50))
    length = db.Column(db.Float)
    width = db.Column(db.Float)
    thickness = db.Column(db.Float)
    material = db.Column(db.String(100))
    stone_origin = db.Column(db.String(200))
    hardness = db.Column(db.String(50))
    stone_density = db.Column(db.Float)
    estimated_weight = db.Column(db.Float)
    actual_weight = db.Column(db.Float)
    estimated_volume = db.Column(db.Float)
    sketch_filename = db.Column(db.String(255))
    inscription_text = db.Column(db.String(200))
    design_description = db.Column(db.Text)
    status = db.Column(db.String(50), default='pending')
    status_history = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    process_records = db.relationship('ProcessRecord', backref='order', lazy=True)


class ProcessRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    process_name = db.Column(db.String(50), nullable=False)
    process_code = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    duration_hours = db.Column(db.Float)
    craftsman_id = db.Column(db.Integer, db.ForeignKey('craftsman.id'))
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


STATUS_FLOW = ['quarrying', 'cutting', 'carving_pool', 'engraving', 'polishing', 'waxing']
STATUS_NAMES = {
    'pending': '待分配',
    'quarrying': '采石',
    'cutting': '切坯',
    'carving_pool': '凿池',
    'engraving': '刻砚',
    'polishing': '细磨',
    'waxing': '封蜡',
    'completed': '已完成'
}


def generate_order_number():
    date_str = datetime.now().strftime('%Y%m%d')
    last_order = Order.query.order_by(Order.id.desc()).first()
    if last_order and last_order.order_number.startswith(date_str):
        sequence = int(last_order.order_number[-4:]) + 1
    else:
        sequence = 1
    return f"YAN{date_str}{sequence:04d}"


def calculate_weight_estimation(material, length, width, thickness):
    density = STONE_DENSITY.get(material, STONE_DENSITY['其他'])
    if length and width and thickness:
        volume = length * width * thickness / 1000
        weight = volume * density
        return round(volume, 4), round(weight, 2), density
    return None, None, density


def init_process_records(order_id):
    for i, process_code in enumerate(STATUS_FLOW):
        record = ProcessRecord(
            order_id=order_id,
            process_name=STATUS_NAMES[process_code],
            process_code=process_code,
            status='pending'
        )
        db.session.add(record)
    db.session.commit()


@app.route('/api/customers', methods=['POST'])
def create_customer():
    data = request.json
    customer = Customer(
        name=data['name'],
        phone=data['phone'],
        address=data.get('address', '')
    )
    db.session.add(customer)
    db.session.commit()
    return jsonify({
        'id': customer.id,
        'name': customer.name,
        'phone': customer.phone,
        'address': customer.address
    }), 201


@app.route('/api/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'phone': c.phone,
        'address': c.address
    } for c in customers])


@app.route('/api/craftsmen', methods=['POST'])
def create_craftsman():
    data = request.json
    craftsman = Craftsman(
        name=data['name'],
        phone=data['phone'],
        skill_level=data.get('skill_level', ''),
        status=data.get('status', 'available')
    )
    db.session.add(craftsman)
    db.session.commit()
    return jsonify({
        'id': craftsman.id,
        'name': craftsman.name,
        'phone': craftsman.phone,
        'skill_level': craftsman.skill_level,
        'status': craftsman.status
    }), 201


@app.route('/api/craftsmen', methods=['GET'])
def get_craftsmen():
    craftsmen = Craftsman.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'phone': c.phone,
        'skill_level': c.skill_level,
        'status': c.status
    } for c in craftsmen])


@app.route('/api/calculate-weight', methods=['POST'])
def calculate_weight():
    data = request.json
    material = data.get('material', '其他')
    length = data.get('length')
    width = data.get('width')
    thickness = data.get('thickness')
    
    volume, weight, density = calculate_weight_estimation(material, length, width, thickness)
    
    return jsonify({
        'material': material,
        'stone_density': density,
        'length_cm': length,
        'width_cm': width,
        'thickness_cm': thickness,
        'estimated_volume_cm3': volume,
        'estimated_weight_g': weight,
        'estimated_weight_kg': round(weight / 1000, 3) if weight else None,
        'unit': '密度单位: g/cm³, 体积单位: cm³, 重量单位: g'
    })


@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json
    
    customer = Customer.query.get(data['customer_id'])
    if not customer:
        return jsonify({'error': '客户不存在'}), 404
    
    order_number = generate_order_number()
    
    material = data.get('material', '其他')
    length = data.get('length')
    width = data.get('width')
    thickness = data.get('thickness')
    
    volume, weight, density = calculate_weight_estimation(material, length, width, thickness)
    
    order = Order(
        order_number=order_number,
        customer_id=data['customer_id'],
        inkstone_type=data['inkstone_type'],
        size=data.get('size', ''),
        length=length,
        width=width,
        thickness=thickness,
        material=material,
        stone_origin=data.get('stone_origin', ''),
        hardness=data.get('hardness', ''),
        stone_density=density,
        estimated_volume=volume,
        estimated_weight=weight,
        inscription_text=data.get('inscription_text', ''),
        design_description=data.get('design_description', ''),
        status='pending',
        status_history='[]'
    )
    db.session.add(order)
    db.session.commit()
    
    init_process_records(order.id)
    
    return jsonify({
        'id': order.id,
        'order_number': order.order_number,
        'customer_id': order.customer_id,
        'inkstone_type': order.inkstone_type,
        'size': order.size,
        'length_cm': order.length,
        'width_cm': order.width,
        'thickness_cm': order.thickness,
        'material': order.material,
        'stone_origin': order.stone_origin,
        'hardness': order.hardness,
        'stone_density': order.stone_density,
        'estimated_volume_cm3': order.estimated_volume,
        'estimated_weight_g': order.estimated_weight,
        'estimated_weight_kg': round(order.estimated_weight / 1000, 3) if order.estimated_weight else None,
        'inscription_text': order.inscription_text,
        'status': STATUS_NAMES[order.status],
        'created_at': order.created_at.isoformat()
    }), 201


@app.route('/api/orders/<int:order_id>/assign', methods=['POST'])
def assign_craftsman(order_id):
    data = request.json
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({'error': '订单不存在'}), 404
    
    if order.status != 'pending':
        return jsonify({'error': '订单已分配，无法再次分配'}), 400
    
    craftsman = Craftsman.query.get(data['craftsman_id'])
    if not craftsman:
        return jsonify({'error': '匠人不存在'}), 404
    
    if craftsman.status != 'available':
        return jsonify({'error': '匠人当前不可用'}), 400
    
    order.craftsman_id = data['craftsman_id']
    order.status = 'quarrying'
    craftsman.status = 'busy'
    
    quarry_record = ProcessRecord.query.filter_by(
        order_id=order_id, process_code='quarrying'
    ).first()
    if quarry_record:
        quarry_record.craftsman_id = data['craftsman_id']
    
    db.session.commit()
    
    return jsonify({
        'id': order.id,
        'order_number': order.order_number,
        'craftsman_id': order.craftsman_id,
        'status': STATUS_NAMES[order.status],
        'message': '匠人分配成功，开始采石工序'
    })


@app.route('/api/orders/<int:order_id>/process/<process_code>/start', methods=['POST'])
def start_process(order_id, process_code):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': '订单不存在'}), 404
    
    if process_code not in STATUS_FLOW:
        return jsonify({'error': '无效的工序代码'}), 400
    
    current_index = STATUS_FLOW.index(order.status) if order.status in STATUS_FLOW else -1
    target_index = STATUS_FLOW.index(process_code)
    
    if target_index > current_index + 1:
        return jsonify({'error': '请按顺序进行工序'}), 400
    
    process_record = ProcessRecord.query.filter_by(
        order_id=order_id, process_code=process_code
    ).first()
    
    if not process_record:
        return jsonify({'error': '工序记录不存在'}), 404
    
    if process_record.status == 'completed':
        return jsonify({'error': '该工序已完成'}), 400
    
    process_record.start_time = datetime.utcnow()
    process_record.status = 'in_progress'
    
    if order.status != process_code:
        order.status = process_code
    
    db.session.commit()
    
    return jsonify({
        'order_id': order.id,
        'order_number': order.order_number,
        'process_code': process_code,
        'process_name': STATUS_NAMES[process_code],
        'start_time': process_record.start_time.isoformat(),
        'status': '进行中',
        'message': f'{STATUS_NAMES[process_code]}工序已开始'
    })


@app.route('/api/orders/<int:order_id>/process/<process_code>/complete', methods=['POST'])
def complete_process(order_id, process_code):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': '订单不存在'}), 404
    
    if process_code not in STATUS_FLOW:
        return jsonify({'error': '无效的工序代码'}), 400
    
    process_record = ProcessRecord.query.filter_by(
        order_id=order_id, process_code=process_code
    ).first()
    
    if not process_record:
        return jsonify({'error': '工序记录不存在'}), 404
    
    if process_record.status == 'completed':
        return jsonify({'error': '该工序已完成'}), 400
    
    if process_record.status == 'pending':
        process_record.start_time = datetime.utcnow()
    
    process_record.end_time = datetime.utcnow()
    process_record.status = 'completed'
    
    if process_record.start_time:
        duration = process_record.end_time - process_record.start_time
        process_record.duration_hours = round(duration.total_seconds() / 3600, 2)
    
    data = request.json or {}
    if data.get('notes'):
        process_record.notes = data.get('notes')
    
    current_index = STATUS_FLOW.index(process_code)
    if current_index < len(STATUS_FLOW) - 1:
        order.status = STATUS_FLOW[current_index + 1]
    else:
        order.status = 'completed'
        if order.craftsman_id:
            craftsman = Craftsman.query.get(order.craftsman_id)
            if craftsman:
                craftsman.status = 'available'
    
    db.session.commit()
    
    return jsonify({
        'order_id': order.id,
        'order_number': order.order_number,
        'process_code': process_code,
        'process_name': STATUS_NAMES[process_code],
        'start_time': process_record.start_time.isoformat() if process_record.start_time else None,
        'end_time': process_record.end_time.isoformat() if process_record.end_time else None,
        'duration_hours': process_record.duration_hours,
        'status': '已完成',
        'next_status': STATUS_NAMES[order.status],
        'message': f'{STATUS_NAMES[process_code]}工序已完成，下一工序：{STATUS_NAMES[order.status]}'
    })


@app.route('/api/orders/<int:order_id>/next-status', methods=['POST'])
def next_status(order_id):
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({'error': '订单不存在'}), 404
    
    if order.status == 'pending':
        return jsonify({'error': '请先分配匠人'}), 400
    
    if order.status == 'completed':
        return jsonify({'error': '订单已完成'}), 400
    
    current_index = STATUS_FLOW.index(order.status)
    current_process = ProcessRecord.query.filter_by(
        order_id=order_id, process_code=order.status
    ).first()
    
    if current_process and current_process.status != 'completed':
        current_process.end_time = datetime.utcnow()
        current_process.status = 'completed'
        if current_process.start_time:
            duration = current_process.end_time - current_process.start_time
            current_process.duration_hours = round(duration.total_seconds() / 3600, 2)
    
    if current_index < len(STATUS_FLOW) - 1:
        order.status = STATUS_FLOW[current_index + 1]
        next_process = ProcessRecord.query.filter_by(
            order_id=order_id, process_code=order.status
        ).first()
        if next_process:
            next_process.start_time = datetime.utcnow()
            next_process.status = 'in_progress'
    else:
        order.status = 'completed'
        if order.craftsman_id:
            craftsman = Craftsman.query.get(order.craftsman_id)
            craftsman.status = 'available'
    
    db.session.commit()
    
    return jsonify({
        'id': order.id,
        'order_number': order.order_number,
        'status': STATUS_NAMES[order.status],
        'message': f'订单状态更新为：{STATUS_NAMES[order.status]}'
    })


@app.route('/api/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    result = []
    for order in orders:
        result.append({
            'id': order.id,
            'order_number': order.order_number,
            'customer_name': order.customer.name,
            'craftsman_name': order.craftsman.name if order.craftsman else None,
            'inkstone_type': order.inkstone_type,
            'estimated_weight_g': order.estimated_weight,
            'status': STATUS_NAMES[order.status],
            'created_at': order.created_at.isoformat(),
            'updated_at': order.updated_at.isoformat()
        })
    return jsonify(result)


@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': '订单不存在'}), 404
    
    sketch_url = f'/api/orders/{order_id}/sketch' if order.sketch_filename else None
    
    process_records = []
    for record in order.process_records:
        process_records.append({
            'process_code': record.process_code,
            'process_name': record.process_name,
            'status': record.status,
            'start_time': record.start_time.isoformat() if record.start_time else None,
            'end_time': record.end_time.isoformat() if record.end_time else None,
            'duration_hours': record.duration_hours,
            'notes': record.notes
        })
    
    return jsonify({
        'id': order.id,
        'order_number': order.order_number,
        'customer_id': order.customer_id,
        'customer_name': order.customer.name,
        'customer_phone': order.customer.phone,
        'craftsman_id': order.craftsman_id,
        'craftsman_name': order.craftsman.name if order.craftsman else None,
        'inkstone_type': order.inkstone_type,
        'size': order.size,
        'length_cm': order.length,
        'width_cm': order.width,
        'thickness_cm': order.thickness,
        'material': order.material,
        'stone_origin': order.stone_origin,
        'hardness': order.hardness,
        'stone_density': order.stone_density,
        'estimated_volume_cm3': order.estimated_volume,
        'estimated_weight_g': order.estimated_weight,
        'estimated_weight_kg': round(order.estimated_weight / 1000, 3) if order.estimated_weight else None,
        'actual_weight': order.actual_weight,
        'sketch_filename': order.sketch_filename,
        'sketch_url': sketch_url,
        'inscription_text': order.inscription_text,
        'design_description': order.design_description,
        'status': STATUS_NAMES[order.status],
        'process_records': process_records,
        'created_at': order.created_at.isoformat(),
        'updated_at': order.updated_at.isoformat()
    })


@app.route('/api/orders/<int:order_id>/work-report', methods=['GET'])
def get_work_report(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': '订单不存在'}), 404
    
    process_records = []
    total_duration = 0
    completed_count = 0
    
    for record in order.process_records:
        duration = record.duration_hours or 0
        total_duration += duration
        if record.status == 'completed':
            completed_count += 1
        
        process_records.append({
            'process_code': record.process_code,
            'process_name': record.process_name,
            'status': record.status,
            'status_text': '待开始' if record.status == 'pending' else ('进行中' if record.status == 'in_progress' else '已完成'),
            'start_time': record.start_time.isoformat() if record.start_time else None,
            'end_time': record.end_time.isoformat() if record.end_time else None,
            'duration_hours': duration,
            'duration_text': f'{duration} 小时' if duration else None,
            'notes': record.notes
        })
    
    return jsonify({
        'order_id': order.id,
        'order_number': order.order_number,
        'inkstone_type': order.inkstone_type,
        'craftsman_name': order.craftsman.name if order.craftsman else None,
        'status': STATUS_NAMES[order.status],
        'estimated_weight_g': order.estimated_weight,
        'estimated_weight_kg': round(order.estimated_weight / 1000, 3) if order.estimated_weight else None,
        'total_processes': len(STATUS_FLOW),
        'completed_processes': completed_count,
        'total_duration_hours': round(total_duration, 2),
        'total_duration_text': f'{round(total_duration, 2)} 小时',
        'process_records': process_records,
        'generated_at': datetime.utcnow().isoformat()
    })


@app.route('/api/work-reports', methods=['GET'])
def get_all_work_reports():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    craftsman_id = request.args.get('craftsman_id')
    
    query = Order.query
    if start_date:
        query = query.filter(Order.created_at >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(Order.created_at <= datetime.fromisoformat(end_date))
    
    orders = query.all()
    reports = []
    
    for order in orders:
        total_duration = 0
        completed_count = 0
        for record in order.process_records:
            if record.duration_hours:
                total_duration += record.duration_hours
            if record.status == 'completed':
                completed_count += 1
        
        reports.append({
            'order_id': order.id,
            'order_number': order.order_number,
            'inkstone_type': order.inkstone_type,
            'craftsman_name': order.craftsman.name if order.craftsman else None,
            'status': STATUS_NAMES[order.status],
            'estimated_weight_kg': round(order.estimated_weight / 1000, 3) if order.estimated_weight else None,
            'total_processes': len(STATUS_FLOW),
            'completed_processes': completed_count,
            'total_duration_hours': round(total_duration, 2),
            'created_at': order.created_at.isoformat()
        })
    
    return jsonify({
        'total_orders': len(reports),
        'reports': reports
    })


@app.route('/api/orders/<int:order_id>/status', methods=['GET'])
def get_order_status_flow(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': '订单不存在'}), 404
    
    current_status = order.status
    status_flow = []
    
    if current_status == 'pending':
        status_flow.append({'status': 'pending', 'name': '待分配', 'completed': True})
        for s in STATUS_FLOW:
            status_flow.append({'status': s, 'name': STATUS_NAMES[s], 'completed': False})
        status_flow.append({'status': 'completed', 'name': '已完成', 'completed': False})
    else:
        status_flow.append({'status': 'pending', 'name': '待分配', 'completed': True})
        
        if current_status == 'completed':
            for s in STATUS_FLOW:
                status_flow.append({'status': s, 'name': STATUS_NAMES[s], 'completed': True})
            status_flow.append({'status': 'completed', 'name': '已完成', 'completed': True})
        else:
            current_index = STATUS_FLOW.index(current_status)
            for i, s in enumerate(STATUS_FLOW):
                status_flow.append({
                    'status': s, 
                    'name': STATUS_NAMES[s], 
                    'completed': i <= current_index,
                    'current': i == current_index
                })
            status_flow.append({'status': 'completed', 'name': '已完成', 'completed': False})
    
    return jsonify({
        'order_number': order.order_number,
        'current_status': STATUS_NAMES[current_status],
        'status_flow': status_flow
    })


@app.route('/api/orders/<int:order_id>/upload-sketch', methods=['POST'])
def upload_sketch(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': '订单不存在'}), 404
    
    if 'sketch' not in request.files:
        return jsonify({'error': '未上传文件'}), 400
    
    file = request.files['sketch']
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400
    
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{order.order_number}_{uuid.uuid4().hex[:8]}.{ext}"
        filename = secure_filename(filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        order.sketch_filename = filename
        db.session.commit()
        
        return jsonify({
            'order_id': order.id,
            'order_number': order.order_number,
            'sketch_filename': filename,
            'sketch_url': f'/api/orders/{order_id}/sketch',
            'message': '设计草图上传成功'
        })
    
    return jsonify({'error': '不支持的文件格式，仅支持 png, jpg, jpeg, gif, bmp'}), 400


@app.route('/api/orders/<int:order_id>/sketch', methods=['GET'])
def get_sketch(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': '订单不存在'}), 404
    
    if not order.sketch_filename:
        return jsonify({'error': '该订单暂无设计草图'}), 404
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], order.sketch_filename)
    if not os.path.exists(file_path):
        return jsonify({'error': '文件不存在'}), 404
    
    return send_from_directory(app.config['UPLOAD_FOLDER'], order.sketch_filename)


@app.route('/api/orders/<int:order_id>/sketch', methods=['DELETE'])
def delete_sketch(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': '订单不存在'}), 404
    
    if not order.sketch_filename:
        return jsonify({'error': '该订单暂无设计草图'}), 404
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], order.sketch_filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    order.sketch_filename = None
    db.session.commit()
    
    return jsonify({
        'order_id': order.id,
        'order_number': order.order_number,
        'message': '设计草图删除成功'
    })


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
