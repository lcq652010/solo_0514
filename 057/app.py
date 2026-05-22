from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///charging_station.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['UPLOAD_FOLDER'] = 'uploads/fault_images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
db = SQLAlchemy(app)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class ChargingPile(db.Model):
    __tablename__ = 'charging_pile'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_no = db.Column(db.String(50), unique=True, nullable=False, comment='设备编号')
    pile_no = db.Column(db.String(50), comment='桩体编号')
    name = db.Column(db.String(100), nullable=False, comment='充电桩名称')
    service_area = db.Column(db.String(100), comment='服务区名称')
    location = db.Column(db.String(200), nullable=False, comment='位置')
    power = db.Column(db.Float, nullable=False, comment='额定功率(kW)')
    output_power = db.Column(db.Float, comment='输出功率(kW)')
    gun_count = db.Column(db.Integer, comment='枪线数量')
    manufacturer = db.Column(db.String(100), comment='制造商')
    status = db.Column(db.String(20), nullable=False, default='空闲', comment='状态：空闲/充电中/故障/离线')
    create_time = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'device_no': self.device_no,
            'pile_no': self.pile_no,
            'name': self.name,
            'service_area': self.service_area,
            'location': self.location,
            'power': self.power,
            'output_power': self.output_power,
            'gun_count': self.gun_count,
            'manufacturer': self.manufacturer,
            'status': self.status,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
        }


class FaultRecord(db.Model):
    __tablename__ = 'fault_record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fault_no = db.Column(db.String(50), unique=True, nullable=False, comment='故障编号')
    device_no = db.Column(db.String(50), nullable=False, comment='设备编号')
    fault_type = db.Column(db.String(100), nullable=False, comment='故障类型')
    fault_phenomenon = db.Column(db.String(50), comment='故障现象：无法启动/中途断电/跳枪/不计费')
    fault_source = db.Column(db.String(50), comment='故障来源：用户上报/系统检测/巡检发现')
    fault_description = db.Column(db.Text, comment='故障描述')
    report_time = db.Column(db.DateTime, default=datetime.now, comment='上报时间')
    receive_time = db.Column(db.DateTime, comment='接收时间')
    handle_status = db.Column(db.String(20), default='待处理', comment='处理状态：待处理/处理中/已完成')
    handle_time = db.Column(db.DateTime, comment='处理完成时间')
    handle_duration = db.Column(db.Integer, comment='处理时长(分钟)')
    handle_result = db.Column(db.Text, comment='处理结果')

    def to_dict(self, include_images=False):
        data = {
            'id': self.id,
            'fault_no': self.fault_no,
            'device_no': self.device_no,
            'fault_type': self.fault_type,
            'fault_phenomenon': self.fault_phenomenon,
            'fault_source': self.fault_source,
            'fault_description': self.fault_description,
            'report_time': self.report_time.strftime('%Y-%m-%d %H:%M:%S'),
            'receive_time': self.receive_time.strftime('%Y-%m-%d %H:%M:%S') if self.receive_time else None,
            'handle_status': self.handle_status,
            'handle_time': self.handle_time.strftime('%Y-%m-%d %H:%M:%S') if self.handle_time else None,
            'handle_duration': self.handle_duration,
            'handle_result': self.handle_result
        }
        if include_images:
            images = FaultImage.query.filter_by(fault_no=self.fault_no).all()
            data['images'] = [img.to_dict() for img in images]
        return data


class FaultImage(db.Model):
    __tablename__ = 'fault_image'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fault_no = db.Column(db.String(50), nullable=False, comment='故障编号')
    image_name = db.Column(db.String(255), nullable=False, comment='图片名称')
    image_path = db.Column(db.String(255), nullable=False, comment='图片路径')
    upload_time = db.Column(db.DateTime, default=datetime.now, comment='上传时间')

    def to_dict(self):
        return {
            'id': self.id,
            'fault_no': self.fault_no,
            'image_name': self.image_name,
            'image_url': f'/api/fault-images/{self.id}/preview',
            'upload_time': self.upload_time.strftime('%Y-%m-%d %H:%M:%S')
        }


class AbnormalRecord(db.Model):
    __tablename__ = 'abnormal_record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_no = db.Column(db.String(50), nullable=False, comment='设备编号')
    abnormal_type = db.Column(db.String(100), nullable=False, comment='异常类型')
    abnormal_description = db.Column(db.Text, comment='异常描述')
    report_time = db.Column(db.DateTime, default=datetime.now, comment='上报时间')
    charge_duration = db.Column(db.Integer, comment='充电时长(分钟)')
    charge_voltage = db.Column(db.Float, comment='充电电压(V)')
    charge_current = db.Column(db.Float, comment='充电电流(A)')

    def to_dict(self):
        return {
            'id': self.id,
            'device_no': self.device_no,
            'abnormal_type': self.abnormal_type,
            'abnormal_description': self.abnormal_description,
            'report_time': self.report_time.strftime('%Y-%m-%d %H:%M:%S'),
            'charge_duration': self.charge_duration,
            'charge_voltage': self.charge_voltage,
            'charge_current': self.charge_current
        }


def generate_fault_no():
    date_str = datetime.now().strftime('%Y%m%d')
    last_fault = FaultRecord.query.filter(
        FaultRecord.fault_no.like(f'FAULT{date_str}%')
    ).order_by(FaultRecord.fault_no.desc()).first()
    
    if last_fault:
        seq = int(last_fault.fault_no[-4:]) + 1
    else:
        seq = 1
    return f'FAULT{date_str}{seq:04d}'


FAULT_PHENOMENON_OPTIONS = ['无法启动', '中途断电', '跳枪', '不计费']
FAULT_SOURCE_OPTIONS = ['用户上报', '系统检测', '巡检发现']


@app.route('/api/charging-piles', methods=['POST'])
def add_charging_pile():
    data = request.get_json()
    
    if not data.get('device_no') or not data.get('name') or not data.get('location') or not data.get('power'):
        return jsonify({'code': 400, 'msg': '缺少必要参数', 'data': None}), 400
    
    if ChargingPile.query.filter_by(device_no=data['device_no']).first():
        return jsonify({'code': 400, 'msg': '设备编号已存在', 'data': None}), 400
    
    pile = ChargingPile(
        device_no=data['device_no'],
        pile_no=data.get('pile_no'),
        name=data['name'],
        service_area=data.get('service_area'),
        location=data['location'],
        power=data['power'],
        output_power=data.get('output_power'),
        gun_count=data.get('gun_count'),
        manufacturer=data.get('manufacturer'),
        status=data.get('status', '空闲')
    )
    
    db.session.add(pile)
    db.session.commit()
    
    return jsonify({'code': 200, 'msg': '添加成功', 'data': pile.to_dict()})


@app.route('/api/charging-piles', methods=['GET'])
def get_charging_piles():
    service_area = request.args.get('service_area')
    query = ChargingPile.query
    
    if service_area:
        query = query.filter(ChargingPile.service_area.like(f'%{service_area}%'))
    
    piles = query.all()
    return jsonify({
        'code': 200,
        'msg': '查询成功',
        'data': [pile.to_dict() for pile in piles]
    })


@app.route('/api/charging-piles/<device_no>', methods=['GET'])
def get_charging_pile(device_no):
    pile = ChargingPile.query.filter_by(device_no=device_no).first()
    if not pile:
        return jsonify({'code': 404, 'msg': '设备不存在', 'data': None}), 404
    return jsonify({'code': 200, 'msg': '查询成功', 'data': pile.to_dict()})


@app.route('/api/charging-piles/<device_no>/status', methods=['PUT'])
def update_pile_status(device_no):
    data = request.get_json()
    status = data.get('status')
    
    if status not in ['空闲', '充电中', '故障', '离线']:
        return jsonify({'code': 400, 'msg': '无效的状态值', 'data': None}), 400
    
    pile = ChargingPile.query.filter_by(device_no=device_no).first()
    if not pile:
        return jsonify({'code': 404, 'msg': '设备不存在', 'data': None}), 404
    
    pile.status = status
    db.session.commit()
    
    return jsonify({'code': 200, 'msg': '状态更新成功', 'data': pile.to_dict()})


@app.route('/api/abnormal', methods=['POST'])
def report_abnormal():
    data = request.get_json()
    
    if not data.get('device_no') or not data.get('abnormal_type'):
        return jsonify({'code': 400, 'msg': '缺少必要参数', 'data': None}), 400
    
    abnormal = AbnormalRecord(
        device_no=data['device_no'],
        abnormal_type=data['abnormal_type'],
        abnormal_description=data.get('abnormal_description', ''),
        charge_duration=data.get('charge_duration'),
        charge_voltage=data.get('charge_voltage'),
        charge_current=data.get('charge_current')
    )
    
    db.session.add(abnormal)
    db.session.commit()
    
    return jsonify({'code': 200, 'msg': '异常上报成功', 'data': abnormal.to_dict()})


@app.route('/api/abnormal', methods=['GET'])
def get_abnormal_records():
    device_no = request.args.get('device_no')
    query = AbnormalRecord.query
    
    if device_no:
        query = query.filter_by(device_no=device_no)
    
    records = query.order_by(AbnormalRecord.report_time.desc()).all()
    
    return jsonify({
        'code': 200,
        'msg': '查询成功',
        'data': [record.to_dict() for record in records]
    })


@app.route('/api/faults', methods=['POST'])
def add_fault_record():
    data = request.get_json()
    
    if not data.get('device_no') or not data.get('fault_type'):
        return jsonify({'code': 400, 'msg': '缺少必要参数', 'data': None}), 400
    
    fault_phenomenon = data.get('fault_phenomenon')
    if fault_phenomenon and fault_phenomenon not in FAULT_PHENOMENON_OPTIONS:
        return jsonify({
            'code': 400, 
            'msg': f'无效的故障现象，可选值: {", ".join(FAULT_PHENOMENON_OPTIONS)}', 
            'data': None
        }), 400
    
    fault_source = data.get('fault_source')
    if fault_source and fault_source not in FAULT_SOURCE_OPTIONS:
        return jsonify({
            'code': 400, 
            'msg': f'无效的故障来源，可选值: {", ".join(FAULT_SOURCE_OPTIONS)}', 
            'data': None
        }), 400
    
    fault_no = generate_fault_no()
    
    fault = FaultRecord(
        fault_no=fault_no,
        device_no=data['device_no'],
        fault_type=data['fault_type'],
        fault_phenomenon=fault_phenomenon,
        fault_source=fault_source,
        fault_description=data.get('fault_description', ''),
        receive_time=datetime.now()
    )
    
    pile = ChargingPile.query.filter_by(device_no=data['device_no']).first()
    if pile:
        pile.status = '故障'
    
    db.session.add(fault)
    db.session.commit()
    
    return jsonify({'code': 200, 'msg': '故障记录添加成功', 'data': fault.to_dict()})


@app.route('/api/faults', methods=['GET'])
def get_fault_records():
    device_no = request.args.get('device_no')
    handle_status = request.args.get('handle_status')
    fault_source = request.args.get('fault_source')
    min_duration = request.args.get('min_duration', type=int)
    max_duration = request.args.get('max_duration', type=int)
    
    query = FaultRecord.query
    
    if device_no:
        query = query.filter_by(device_no=device_no)
    
    if handle_status:
        query = query.filter_by(handle_status=handle_status)
    
    if fault_source:
        query = query.filter_by(fault_source=fault_source)
    
    if min_duration is not None:
        query = query.filter(FaultRecord.handle_duration >= min_duration)
    
    if max_duration is not None:
        query = query.filter(FaultRecord.handle_duration <= max_duration)
    
    records = query.order_by(FaultRecord.report_time.desc()).all()
    
    return jsonify({
        'code': 200,
        'msg': '查询成功',
        'data': [record.to_dict() for record in records]
    })


@app.route('/api/faults/<fault_no>', methods=['GET'])
def get_fault_detail(fault_no):
    fault = FaultRecord.query.filter_by(fault_no=fault_no).first()
    if not fault:
        return jsonify({'code': 404, 'msg': '故障记录不存在', 'data': None}), 404
    
    return jsonify({'code': 200, 'msg': '查询成功', 'data': fault.to_dict(include_images=True)})


@app.route('/api/faults/<fault_no>/receive', methods=['PUT'])
def receive_fault(fault_no):
    fault = FaultRecord.query.filter_by(fault_no=fault_no).first()
    if not fault:
        return jsonify({'code': 404, 'msg': '故障记录不存在', 'data': None}), 404
    
    if fault.handle_status != '待处理':
        return jsonify({'code': 400, 'msg': '该工单状态不是待处理', 'data': None}), 400
    
    fault.handle_status = '处理中'
    fault.receive_time = datetime.now()
    
    db.session.commit()
    
    return jsonify({'code': 200, 'msg': '工单接收成功', 'data': fault.to_dict()})


@app.route('/api/faults/<fault_no>/handle', methods=['PUT'])
def handle_fault(fault_no):
    data = request.get_json()
    handle_result = data.get('handle_result', '')
    
    fault = FaultRecord.query.filter_by(fault_no=fault_no).first()
    if not fault:
        return jsonify({'code': 404, 'msg': '故障记录不存在', 'data': None}), 404
    
    fault.handle_status = '已完成'
    fault.handle_time = datetime.now()
    fault.handle_result = handle_result
    
    if fault.receive_time:
        duration = (fault.handle_time - fault.receive_time).total_seconds() / 60
        fault.handle_duration = round(duration, 2)
    
    pile = ChargingPile.query.filter_by(device_no=fault.device_no).first()
    if pile:
        pile.status = '空闲'
    
    db.session.commit()
    
    return jsonify({'code': 200, 'msg': '故障处理完成', 'data': fault.to_dict()})


@app.route('/api/fault-images', methods=['POST'])
def upload_fault_image():
    if 'image' not in request.files:
        return jsonify({'code': 400, 'msg': '没有上传图片', 'data': None}), 400
    
    file = request.files['image']
    fault_no = request.form.get('fault_no')
    
    if not fault_no:
        return jsonify({'code': 400, 'msg': '缺少故障编号', 'data': None}), 400
    
    if not FaultRecord.query.filter_by(fault_no=fault_no).first():
        return jsonify({'code': 404, 'msg': '故障记录不存在', 'data': None}), 404
    
    if file.filename == '':
        return jsonify({'code': 400, 'msg': '未选择文件', 'data': None}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{fault_no}_{timestamp}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        fault_image = FaultImage(
            fault_no=fault_no,
            image_name=file.filename,
            image_path=file_path
        )
        db.session.add(fault_image)
        db.session.commit()
        
        return jsonify({'code': 200, 'msg': '图片上传成功', 'data': fault_image.to_dict()})
    
    return jsonify({'code': 400, 'msg': '不支持的文件格式', 'data': None}), 400


@app.route('/api/fault-images/<int:image_id>/preview', methods=['GET'])
def preview_fault_image(image_id):
    fault_image = FaultImage.query.get(image_id)
    if not fault_image:
        return jsonify({'code': 404, 'msg': '图片不存在', 'data': None}), 404
    
    return send_from_directory(
        os.path.dirname(fault_image.image_path),
        os.path.basename(fault_image.image_path)
    )


@app.route('/api/fault-images/<fault_no>', methods=['GET'])
def get_fault_images(fault_no):
    images = FaultImage.query.filter_by(fault_no=fault_no).order_by(FaultImage.upload_time.desc()).all()
    return jsonify({
        'code': 200,
        'msg': '查询成功',
        'data': [img.to_dict() for img in images]
    })


@app.route('/api/fault-statistics', methods=['GET'])
def get_fault_statistics():
    fault_source = request.args.get('fault_source')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = FaultRecord.query
    
    if fault_source:
        query = query.filter_by(fault_source=fault_source)
    
    if start_date:
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(FaultRecord.report_time >= start_dt)
        except:
            pass
    
    if end_date:
        try:
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            end_dt = end_dt.replace(hour=23, minute=59, second=59)
            query = query.filter(FaultRecord.report_time <= end_dt)
        except:
            pass
    
    records = query.all()
    
    total_count = len(records)
    completed_count = len([r for r in records if r.handle_status == '已完成'])
    pending_count = len([r for r in records if r.handle_status == '待处理'])
    processing_count = len([r for r in records if r.handle_status == '处理中'])
    
    durations = [r.handle_duration for r in records if r.handle_duration is not None]
    avg_duration = round(sum(durations) / len(durations), 2) if durations else 0
    max_duration = max(durations) if durations else 0
    min_duration = min(durations) if durations else 0
    
    source_stats = {}
    for source in FAULT_SOURCE_OPTIONS:
        source_records = [r for r in records if r.fault_source == source]
        source_stats[source] = len(source_records)
    
    duration_ranges = {
        '0-30分钟': len([d for d in durations if d <= 30]),
        '30-60分钟': len([d for d in durations if 30 < d <= 60]),
        '1-2小时': len([d for d in durations if 60 < d <= 120]),
        '2小时以上': len([d for d in durations if d > 120])
    }
    
    return jsonify({
        'code': 200,
        'msg': '统计成功',
        'data': {
            'total_count': total_count,
            'completed_count': completed_count,
            'pending_count': pending_count,
            'processing_count': processing_count,
            'avg_duration': avg_duration,
            'max_duration': max_duration,
            'min_duration': min_duration,
            'source_stats': source_stats,
            'duration_ranges': duration_ranges
        }
    })


@app.route('/api/fault-phenomenon-options', methods=['GET'])
def get_fault_phenomenon_options():
    return jsonify({
        'code': 200,
        'msg': '查询成功',
        'data': FAULT_PHENOMENON_OPTIONS
    })


@app.route('/api/fault-source-options', methods=['GET'])
def get_fault_source_options():
    return jsonify({
        'code': 200,
        'msg': '查询成功',
        'data': FAULT_SOURCE_OPTIONS
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'code': 200, 'msg': '系统运行正常', 'data': {'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print('数据库初始化完成')
    
    print('=' * 60)
    print('高速服务区充电桩运维管理系统后端')
    print('API文档:')
    print('  POST /api/charging-piles - 添加充电桩')
    print('  GET /api/charging-piles - 查询所有充电桩(支持service_area筛选)')
    print('  GET /api/charging-piles/<device_no> - 查询单个充电桩')
    print('  PUT /api/charging-piles/<device_no>/status - 更新充电桩状态')
    print('  POST /api/abnormal - 上报充电异常')
    print('  GET /api/abnormal - 查询异常记录')
    print('  POST /api/faults - 添加故障记录(支持fault_phenomenon, fault_source)')
    print('  GET /api/faults - 查询故障记录(支持device_no, handle_status, fault_source,时长筛选)')
    print('  GET /api/faults/<fault_no> - 查询故障详情(含图片)')
    print('  PUT /api/faults/<fault_no>/receive - 接收工单(开始计时)')
    print('  PUT /api/faults/<fault_no>/handle - 处理故障(完工计时)')
    print('  POST /api/fault-images - 上传故障图片')
    print('  GET /api/fault-images/<fault_no> - 查询故障图片列表')
    print('  GET /api/fault-images/<image_id>/preview - 预览故障图片')
    print('  GET /api/fault-statistics - 故障统计(支持来源和时间筛选)')
    print('  GET /api/fault-phenomenon-options - 获取故障现象选项')
    print('  GET /api/fault-source-options - 获取故障来源选项')
    print('  GET /api/health - 健康检查')
    print('=' * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
