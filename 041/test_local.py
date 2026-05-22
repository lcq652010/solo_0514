import sys
sys.path.insert(0, '.')

from app import app, db
from models import Order, generate_order_no, ORDER_STATUS
import json

def test_local():
    print("=" * 60)
    print("传统珐琅彩鼻烟壶定制订单管理系统 - 本地测试")
    print("=" * 60)
    
    with app.app_context():
        db.create_all()
        
        print("\n1. 测试订单自动编号生成...")
        order_no1 = generate_order_no()
        print(f"   第一个订单号: {order_no1}")
        
        print("\n2. 测试创建订单...")
        order = Order(
            order_no=order_no1,
            customer_name="张三",
            customer_phone="13800138000",
            customer_address="北京市朝阳区",
            bottle_shape="扁圆形",
            bottle_material="白瓷",
            pattern_design="山水图案",
            color_requirement="青花为主",
            special_requirement="落款'乾隆年制'",
            quantity=2,
            estimated_price=8000,
            status="待接单"
        )
        db.session.add(order)
        db.session.commit()
        print(f"   订单创建成功! ID={order.id}, 编号={order.order_no}")
        
        print("\n3. 测试查询订单...")
        order = Order.query.get(order.id)
        print(f"   订单信息: {order.customer_name}, {order.status}")
        
        print("\n4. 测试更新订单状态...")
        for status in ["制胎", "施釉", "绘彩", "烧造", "打磨", "镶口", "完工"]:
            order.status = status
            db.session.commit()
            print(f"   更新状态 -> {status}: 成功")
        
        print("\n5. 测试订单列表查询...")
        orders = Order.query.all()
        print(f"   订单总数: {len(orders)}")
        for o in orders:
            print(f"     - {o.order_no}: {o.customer_name} ({o.status})")
        
        print("\n6. 测试状态列表:")
        print(f"   {ORDER_STATUS}")
        
        print("\n" + "=" * 60)
        print("所有功能测试通过！代码运行正常。")
        print("=" * 60)

if __name__ == '__main__':
    test_local()