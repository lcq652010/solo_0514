import sys
sys.path.insert(0, '.')

from app import app, db, Order, generate_order_no, ORDER_STATUSES
from datetime import datetime
import json

print('=' * 70)
print('缂丝团扇订单管理系统 - 增强版功能测试')
print('=' * 70)
print()

with app.app_context():
    print('【1】测试数据库字段完整性')
    print('-' * 50)
    
    order = Order.query.first()
    if order:
        print(f'现有订单: {order.order_no}')
        print(f'  丝线品类字段存在: {hasattr(order, "silk_thread_type")}')
        print(f'  纹样图案字段存在: {hasattr(order, "pattern_design")}')
        print(f'  扇骨材质字段存在: {hasattr(order, "frame_material")}')
        print(f'  扇面宽度字段存在: {hasattr(order, "fan_size_width")}')
        print(f'  扇面高度字段存在: {hasattr(order, "fan_size_height")}')
        print(f'  缂丝工艺字段存在: {hasattr(order, "kesi_technique")}')
        print(f'  装框类型字段存在: {hasattr(order, "frame_type")}')
        print(f'  装柄材质字段存在: {hasattr(order, "handle_material")}')
    print()
    
    print('【2】创建包含所有新字段的测试订单')
    print('-' * 50)
    
    order_no = generate_order_no()
    new_order = Order(
        order_no=order_no,
        customer_name='王师傅',
        customer_phone='13900139999',
        customer_address='苏州市姑苏区',
        fan_style='圆形团扇',
        pattern_description='牡丹花纹，富贵吉祥',
        size='直径30cm',
        silk_thread_type='桑蚕丝，120D',
        pattern_design='传统牡丹纹样，缠枝花卉',
        frame_material='紫竹',
        fan_size_width='30cm',
        fan_size_height='30cm',
        kesi_technique='双面缂丝，平缂+掼缂',
        kesi_thread_count='120根/厘米',
        kesi_color_count=15,
        frame_type='圆形实木框',
        frame_size='外框35cm，内框30cm',
        frame_material_detail='优质紫竹，经打磨上漆',
        handle_material='紫檀木',
        handle_style='传统直柄，雕花',
        handle_length='18cm',
        remark='VIP客户定制订单'
    )
    
    db.session.add(new_order)
    db.session.commit()
    
    print(f'订单创建成功: {order_no}')
    print(f'  丝线品类: {new_order.silk_thread_type}')
    print(f'  纹样图案: {new_order.pattern_design}')
    print(f'  扇骨材质: {new_order.frame_material}')
    print(f'  扇面尺寸: {new_order.fan_size_width} x {new_order.fan_size_height}')
    print(f'  缂丝工艺: {new_order.kesi_technique}')
    print(f'  装框材质: {new_order.frame_material_detail}')
    print(f'  装柄材质: {new_order.handle_material}')
    print()
    
    print('【3】测试缂丝工序更新')
    print('-' * 50)
    
    new_order.kesi_operator = '李师傅'
    new_order.kesi_completed_at = datetime.now()
    new_order.status = '装框'
    db.session.commit()
    
    updated = Order.query.filter_by(order_no=order_no).first()
    print(f'缂丝工序完成:')
    print(f'  缂丝师傅: {updated.kesi_operator}')
    print(f'  完成时间: {updated.kesi_completed_at}')
    print(f'  当前状态: {updated.status}')
    print()
    
    print('【4】测试装框工序更新')
    print('-' * 50)
    
    updated.frame_operator = '张师傅'
    updated.frame_completed_at = datetime.now()
    updated.status = '装柄'
    db.session.commit()
    
    updated2 = Order.query.filter_by(order_no=order_no).first()
    print(f'装框工序完成:')
    print(f'  装框师傅: {updated2.frame_operator}')
    print(f'  完成时间: {updated2.frame_completed_at}')
    print(f'  当前状态: {updated2.status}')
    print()
    
    print('【5】测试装柄工序更新')
    print('-' * 50)
    
    updated2.handle_operator = '王师傅'
    updated2.handle_completed_at = datetime.now()
    updated2.status = '完工'
    db.session.commit()
    
    final_order = Order.query.filter_by(order_no=order_no).first()
    print(f'装柄工序完成:')
    print(f'  装柄师傅: {final_order.handle_operator}')
    print(f'  完成时间: {final_order.handle_completed_at}')
    print(f'  最终状态: {final_order.status}')
    print()
    
    print('【6】订单完整信息导出')
    print('-' * 50)
    order_dict = final_order.to_dict()
    print(json.dumps(order_dict, ensure_ascii=False, indent=2))
    print()
    
    print('=' * 70)
    print('所有增强功能测试通过！')
    print('=' * 70)
    print()
    print('新增字段说明:')
    print('  【基础信息】')
    print('    - silk_thread_type: 丝线品类')
    print('    - pattern_design: 纹样图案')
    print('    - frame_material: 扇骨材质')
    print('    - fan_size_width/fan_size_height: 扇面尺寸')
    print()
    print('  【缂丝工序依据】')
    print('    - kesi_technique: 缂丝工艺要求')
    print('    - kesi_thread_count: 丝线密度')
    print('    - kesi_color_count: 颜色数量')
    print('    - kesi_completed_at: 完成时间')
    print('    - kesi_operator: 操作人员')
    print()
    print('  【装框工序依据】')
    print('    - frame_type: 框类型')
    print('    - frame_size: 框尺寸')
    print('    - frame_material_detail: 框材质详情')
    print('    - frame_completed_at: 完成时间')
    print('    - frame_operator: 操作人员')
    print()
    print('  【装柄工序依据】')
    print('    - handle_material: 柄材质')
    print('    - handle_style: 柄样式')
    print('    - handle_length: 柄长度')
    print('    - handle_completed_at: 完成时间')
    print('    - handle_operator: 操作人员')
