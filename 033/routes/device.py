from flask import Blueprint, request, jsonify
from app import db
from models.device import Device
from datetime import datetime

device_bp = Blueprint('device', __name__)

@device_bp.route('', methods=['GET'])
def get_devices():
    devices = Device.query.all()
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': [device.to_dict() for device in devices]
    })

@device_bp.route('', methods=['POST'])
def create_device():
    data = request.get_json()
    if not data:
        return jsonify({'code': 400, 'message': '无数据提供'}), 400

    required_fields = ['device_code', 'device_name']
    for field in required_fields:
        if field not in data:
            return jsonify({'code': 400, 'message': f'缺少必填字段: {field}'}), 400

    existing_device = Device.query.filter_by(device_code=data['device_code']).first()
    if existing_device:
        return jsonify({'code': 400, 'message': '设备编号已存在'}), 400

    device = Device(
        device_code=data['device_code'],
        device_name=data['device_name'],
        install_location=data.get('install_location'),
        status=data.get('status', 'normal')
    )

    if 'install_date' in data and data['install_date']:
        try:
            device.install_date = datetime.strptime(data['install_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'code': 400, 'message': '安装日期格式错误，请使用YYYY-MM-DD'}), 400

    db.session.add(device)
    db.session.commit()

    return jsonify({
        'code': 201,
        'message': '设备录入成功',
        'data': device.to_dict()
    }), 201

@device_bp.route('/<int:device_id>', methods=['GET'])
def get_device(device_id):
    device = Device.query.get(device_id)
    if not device:
        return jsonify({'code': 404, 'message': '设备不存在'}), 404

    return jsonify({
        'code': 200,
        'message': 'success',
        'data': device.to_dict()
    })

@device_bp.route('/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    device = Device.query.get(device_id)
    if not device:
        return jsonify({'code': 404, 'message': '设备不存在'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'code': 400, 'message': '无数据提供'}), 400

    if 'device_code' in data:
        existing_device = Device.query.filter(
            Device.device_code == data['device_code'],
            Device.id != device_id
        ).first()
        if existing_device:
            return jsonify({'code': 400, 'message': '设备编号已存在'}), 400
        device.device_code = data['device_code']

    if 'device_name' in data:
        device.device_name = data['device_name']

    if 'install_location' in data:
        device.install_location = data['install_location']

    if 'status' in data:
        valid_statuses = ['normal', 'fault', 'repairing', 'fixed']
        if data['status'] not in valid_statuses:
            return jsonify({'code': 400, 'message': '无效的设备状态'}), 400
        device.status = data['status']

    if 'install_date' in data:
        if data['install_date']:
            try:
                device.install_date = datetime.strptime(data['install_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'code': 400, 'message': '安装日期格式错误，请使用YYYY-MM-DD'}), 400
        else:
            device.install_date = None

    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '设备更新成功',
        'data': device.to_dict()
    })

@device_bp.route('/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    device = Device.query.get(device_id)
    if not device:
        return jsonify({'code': 404, 'message': '设备不存在'}), 404

    db.session.delete(device)
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '设备删除成功'
    })