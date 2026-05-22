from flask import Blueprint, request, jsonify
from app import db
from models.fault import Fault
from models.device import Device
from datetime import datetime

fault_bp = Blueprint('fault', __name__)

@fault_bp.route('', methods=['GET'])
def get_faults():
    faults = Fault.query.order_by(Fault.created_at.desc()).all()
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': [fault.to_dict() for fault in faults]
    })

@fault_bp.route('', methods=['POST'])
def create_fault():
    data = request.get_json()
    if not data:
        return jsonify({'code': 400, 'message': '无数据提供'}), 400

    required_fields = ['device_id', 'fault_type', 'fault_desc']
    for field in required_fields:
        if field not in data:
            return jsonify({'code': 400, 'message': f'缺少必填字段: {field}'}), 400

    device = Device.query.get(data['device_id'])
    if not device:
        return jsonify({'code': 404, 'message': '设备不存在'}), 404

    fault = Fault(
        work_order_no=Fault.generate_work_order_no(),
        device_id=data['device_id'],
        fault_type=data['fault_type'],
        fault_desc=data['fault_desc'],
        reporter=data.get('reporter', '匿名'),
        status='pending'
    )

    device.status = 'fault'

    db.session.add(fault)
    db.session.commit()

    return jsonify({
        'code': 201,
        'message': '故障上报成功',
        'data': fault.to_dict()
    }), 201

@fault_bp.route('/<int:fault_id>', methods=['GET'])
def get_fault(fault_id):
    fault = Fault.query.get(fault_id)
    if not fault:
        return jsonify({'code': 404, 'message': '工单不存在'}), 404

    return jsonify({
        'code': 200,
        'message': 'success',
        'data': fault.to_dict()
    })

@fault_bp.route('/<int:fault_id>', methods=['DELETE'])
def delete_fault(fault_id):
    fault = Fault.query.get(fault_id)
    if not fault:
        return jsonify({'code': 404, 'message': '工单不存在'}), 404

    db.session.delete(fault)
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '工单删除成功'
    })

@fault_bp.route('/<int:fault_id>/handle', methods=['POST'])
def handle_fault(fault_id):
    fault = Fault.query.get(fault_id)
    if not fault:
        return jsonify({'code': 404, 'message': '工单不存在'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'code': 400, 'message': '无数据提供'}), 400

    action = data.get('action')
    if not action or action not in ['accept', 'complete']:
        return jsonify({'code': 400, 'message': '无效的操作类型，请使用 accept 或 complete'}), 400

    device = Device.query.get(fault.device_id)

    if action == 'accept':
        fault.status = 'processing'
        fault.handler = data.get('handler', '管理员')
        fault.handle_time = datetime.now()
        device.status = 'repairing'

        db.session.commit()

        return jsonify({
            'code': 200,
            'message': '工单已受理',
            'data': fault.to_dict()
        })

    elif action == 'complete':
        if fault.status != 'processing':
            return jsonify({'code': 400, 'message': '工单当前状态不能标记为完成'}), 400

        fault.status = 'completed'
        fault.handle_note = data.get('handle_note', '')
        device.status = 'fixed'

        db.session.commit()

        return jsonify({
            'code': 200,
            'message': '工单已完成，设备状态已更新为已修复',
            'data': fault.to_dict()
        })

    return jsonify({
        'code': 200,
        'message': '操作成功',
        'data': fault.to_dict()
    })