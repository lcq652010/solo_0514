from flask import Blueprint, request, jsonify
from app import db
from models.maintenance import MaintenanceRecord
from models.device import Device
from datetime import datetime

maintenance_bp = Blueprint('maintenance', __name__)

@maintenance_bp.route('', methods=['GET'])
def get_maintenance_records():
    device_id = request.args.get('device_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = MaintenanceRecord.query.order_by(MaintenanceRecord.maintenance_date.desc())

    if device_id:
        query = query.filter_by(device_id=device_id)

    if start_date:
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(MaintenanceRecord.maintenance_date >= start_dt)
        except ValueError:
            pass

    if end_date:
        try:
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            end_dt = end_dt.replace(hour=23, minute=59, second=59)
            query = query.filter(MaintenanceRecord.maintenance_date <= end_dt)
        except ValueError:
            pass

    records = query.all()

    return jsonify({
        'code': 200,
        'message': 'success',
        'data': [record.to_dict() for record in records]
    })

@maintenance_bp.route('', methods=['POST'])
def create_maintenance_record():
    data = request.get_json()
    if not data:
        return jsonify({'code': 400, 'message': '无数据提供'}), 400

    required_fields = ['device_id', 'maintenance_type', 'operator']
    for field in required_fields:
        if field not in data:
            return jsonify({'code': 400, 'message': f'缺少必填字段: {field}'}), 400

    device = Device.query.get(data['device_id'])
    if not device:
        return jsonify({'code': 404, 'message': '设备不存在'}), 404

    record = MaintenanceRecord(
        device_id=data['device_id'],
        fault_id=data.get('fault_id'),
        maintenance_type=data['maintenance_type'],
        operator=data['operator'],
        maintenance_content=data.get('maintenance_content', ''),
        parts_replaced=data.get('parts_replaced', ''),
        cost=data.get('cost', 0.0),
        notes=data.get('notes', '')
    )

    if 'maintenance_date' in data and data['maintenance_date']:
        try:
            record.maintenance_date = datetime.strptime(data['maintenance_date'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                record.maintenance_date = datetime.strptime(data['maintenance_date'], '%Y-%m-%d')
            except ValueError:
                return jsonify({'code': 400, 'message': '日期格式错误，请使用YYYY-MM-DD或YYYY-MM-DD HH:MM:SS'}), 400

    device.last_maintenance_date = record.maintenance_date.date()

    db.session.add(record)
    db.session.commit()

    return jsonify({
        'code': 201,
        'message': '运维记录添加成功',
        'data': record.to_dict()
    }), 201

@maintenance_bp.route('/<int:record_id>', methods=['GET'])
def get_maintenance_record(record_id):
    record = MaintenanceRecord.query.get(record_id)
    if not record:
        return jsonify({'code': 404, 'message': '运维记录不存在'}), 404

    return jsonify({
        'code': 200,
        'message': 'success',
        'data': record.to_dict()
    })

@maintenance_bp.route('/<int:record_id>', methods=['PUT'])
def update_maintenance_record(record_id):
    record = MaintenanceRecord.query.get(record_id)
    if not record:
        return jsonify({'code': 404, 'message': '运维记录不存在'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'code': 400, 'message': '无数据提供'}), 400

    if 'maintenance_type' in data:
        record.maintenance_type = data['maintenance_type']
    if 'operator' in data:
        record.operator = data['operator']
    if 'maintenance_content' in data:
        record.maintenance_content = data['maintenance_content']
    if 'parts_replaced' in data:
        record.parts_replaced = data['parts_replaced']
    if 'cost' in data:
        record.cost = data['cost']
    if 'notes' in data:
        record.notes = data['notes']

    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '运维记录更新成功',
        'data': record.to_dict()
    })

@maintenance_bp.route('/<int:record_id>', methods=['DELETE'])
def delete_maintenance_record(record_id):
    record = MaintenanceRecord.query.get(record_id)
    if not record:
        return jsonify({'code': 404, 'message': '运维记录不存在'}), 404

    db.session.delete(record)
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '运维记录删除成功'
    })