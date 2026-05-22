import sys
sys.path.insert(0, '.')

from app import app, db, Order, generate_order_no, ORDER_STATUSES
from datetime import datetime
import json

print('=' * 60)
print('缂丝团扇订单管理系统 - 功能测试')
print('=' * 60)
print()

with app.app_context():
    print('1. 测试订单状态列表...')
    print(f'   订单状态: {ORDER_STATUSES}')
    print(f'   共 {len(ORDER_STATUSES)} 个状态')
    print()
    
    print('2. 测试订单号生成...')
    order_no1 = generate_order_no()
    print(f'   生成订单号: {order_no1}')
    print()
    
    print('3. 测试创建订单...')
    order = Order(
        order_no=order_no1,
        customer_name='张三',
        customer_phone='13800138000',
        customer_address='北京市朝阳区',
        fan_style='圆形团扇',
        pattern_description='牡丹花纹',
        size='直径30cm',
        material_requirement='真丝线',
        special_requirement='双面缂丝',
        remark='测试订单'
    )
    db.session.add(order)
    db.session.commit()
    print(f'   订单创建成功，ID: {order.id}')
    print()
    
    print('4. 测试查询订单...')
    orders = Order.query.all()
    print(f'   订单总数: {len(orders)}')
    for o in orders:
        print(f'   - {o.order_no} - {o.customer_name} - {o.status}')
    print()
    
    print('5. 测试更新订单状态...')
    order.status = '选线'
    order.remark = '已选定丝线颜色'
    db.session.commit()
    updated_order = Order.query.filter_by(order_no=order_no1).first()
    print(f'   更新后状态: {updated_order.status}')
    print(f'   更新后备注: {updated_order.remark}')
    print()
    
    print('6. 测试订单号连续生成...')
    order_no2 = generate_order_no()
    print(f'   第二个订单号: {order_no2}')
    order2 = Order(
        order_no=order_no2,
        customer_name='李四',
        customer_phone='13900139000',
        fan_style='海棠形团扇',
        pattern_description='山水图案'
    )
    db.session.add(order2)
    db.session.commit()
    print(f'   第二单创建成功: {order_no2}')
    print()
    
    print('7. 测试订单转字典...')
    order_dict = order.to_dict()
    print(f'   订单字典: {json.dumps(order_dict, ensure_ascii=False, indent=2)}')
    print()
    
    print('=' * 60)
    print('所有功能测试通过！')
    print('=' * 60)
    print()
    print('系统运行说明:')
    print('1. 运行命令: python app.py')
    print('2. 访问地址: http://localhost:5000')
    print('3. API文档请查看 README.md')
    print()
    print('订单编号规则: KS + 日期(YYYYMMDD) + 4位序号')
    print(f'例如: {order_no1}')
    print()
    print('订单状态流程:')
    for i, status in enumerate(ORDER_STATUSES, 1):
        print(f'  {i}. {status}')
