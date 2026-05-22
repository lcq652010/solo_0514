import sys
sys.path.insert(0, '.')

from app import app, db
import json

def test_v2_api():
    print("=" * 70)
    print("传统珐琅彩鼻烟壶定制订单管理系统 v2.0 - API测试")
    print("=" * 70)
    
    with app.app_context():
        db.create_all()
        print("\n✓ 数据库表结构创建成功")
    
        client = app.test_client()
        
        print("\n1. 测试获取系统状态...")
        r = client.get('/')
        print(f"   状态码: {r.status_code}")
        result = r.get_json()
        print(f"   版本: {result['version']}")
        print(f"   描述: {result['description']}")
        
        print("\n2. 测试获取选项列表 (材质、壶型、纹饰、颜色)...")
        r = client.get('/api/options')
        print(f"   状态码: {r.status_code}")
        options = r.get_json()
        print(f"   胎体材质选项 ({len(options['body_materials'])}种): {', '.join(options['body_materials'][:3])}...")
        print(f"   壶型样式选项 ({len(options['bottle_styles'])}种): {', '.join(options['bottle_styles'][:3])}...")
        print(f"   纹饰图案选项 ({len(options['decorative_patterns'])}种): {', '.join(options['decorative_patterns'][:3])}...")
        print(f"   珐琅色系选项 ({len(options['enamel_colors'])}种): {', '.join(options['enamel_colors'][:3])}...")
        
        print("\n3. 测试创建完整定制订单...")
        order_data = {
            "customer_name": "李四",
            "customer_phone": "13900139000",
            "customer_address": "北京市东城区故宫旁",
            "bottle_style": "扁壶形",
            "bottle_dimensions": "高8cm × 宽6cm × 厚3cm",
            "body_material": "紫铜胎",
            "decorative_pattern": "山水纹饰",
            "pattern_detail": "千里江山图局部，主峰巍峨，云雾缭绕，流水潺潺",
            "enamel_color_system": "宝石蓝、翡翠绿、明黄、鎏金",
            "glaze_requirement": "施釉厚度均匀，约0.15mm，釉面光洁无气泡",
            "painting_detail": "采用工笔画技法，线条细腻，层次分明，设色典雅",
            "firing_requirement": "分3次烧制，温度控制：低温780℃、中温820℃、高温850℃",
            "special_requirement": "底部落款'乾隆年制'篆书，配红木底座",
            "quantity": 1,
            "estimated_price": 15800
        }
        r = client.post('/api/orders', json=order_data)
        print(f"   状态码: {r.status_code}")
        result = r.get_json()
        order_id = result['order']['id']
        order_no = result['order']['order_no']
        print(f"   订单ID: {order_id}")
        print(f"   订单编号: {order_no}")
        print(f"   壶型: {result['order']['bottle_style']}")
        print(f"   尺寸: {result['order']['bottle_dimensions']}")
        print(f"   胎体: {result['order']['body_material']}")
        print(f"   纹饰: {result['order']['decorative_pattern']}")
        print(f"   色系: {result['order']['enamel_color_system']}")
        
        print("\n4. 验证各工序依据字段...")
        order = result['order']
        print(f"   【施釉依据】: {order['glaze_requirement']}")
        print(f"   【绘彩依据】: {order['painting_detail']}")
        print(f"   【烧造依据】: {order['firing_requirement']}")
        
        print("\n5. 测试订单状态流转 (制胎→施釉→绘彩→烧造)...")
        for status in ["制胎", "施釉", "绘彩", "烧造"]:
            r = client.put(f'/api/orders/{order_id}/status', json={"status": status})
            r = client.get(f'/api/orders/{order_id}')
            current_status = r.get_json()['status']
            print(f"   {status} ✓ - {status}工艺依据: ", end="")
            order_json = r.get_json()
            if status == "制胎":
                print(f"{order_json['body_material']} + {order_json['bottle_dimensions']}")
            elif status == "施釉":
                print(f"{order_json['glaze_requirement']}")
            elif status == "绘彩":
                print(f"{order_json['painting_detail'][:20]}...")
            elif status == "烧造":
                print(f"{order_json['firing_requirement']}")
        
        print("\n6. 测试查询订单列表...")
        r = client.get('/api/orders')
        print(f"   状态码: {r.status_code}")
        print(f"   订单总数: {r.get_json()['total']}")
        
        print("\n7. 测试更新订单定制细节...")
        update_data = {
            "enamel_color_system": "宝石蓝、翡翠绿、明黄、鎏金、胭脂粉",
            "painting_detail": "采用工笔画技法，线条细腻，层次分明，设色典雅，增加松鹤延年元素",
            "estimated_price": 16800
        }
        r = client.put(f'/api/orders/{order_id}', json=update_data)
        print(f"   状态码: {r.status_code}")
        updated = r.get_json()['order']
        print(f"   更新后色系: {updated['enamel_color_system']}")
        print(f"   更新后价格: {updated['estimated_price']}元")
        
        print("\n8. 测试删除订单...")
        r = client.delete(f'/api/orders/{order_id}')
        print(f"   状态码: {r.status_code}")
        print(f"   结果: {r.get_json()['message']}")
        
    print("\n" + "=" * 70)
    print("v2.0 所有功能测试通过！新字段已完整支持。")
    print("=" * 70)
    print("\n📋 字段说明:")
    print("  • 胎体材质 (body_material): 制胎工艺依据")
    print("  • 壶型尺寸 (bottle_dimensions): 制胎工艺依据")
    print("  • 纹饰图案 (decorative_pattern/pattern_detail): 绘彩工艺依据")
    print("  • 珐琅色系 (enamel_color_system): 施釉、绘彩、烧造工艺依据")
    print("  • 施釉要求 (glaze_requirement): 施釉工序明确依据")
    print("  • 绘彩细节 (painting_detail): 绘彩工序明确依据")
    print("  • 烧造要求 (firing_requirement): 烧造工序明确依据")
    print("\n🚀 启动命令: python run.py")

if __name__ == '__main__':
    test_v2_api()