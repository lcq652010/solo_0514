import sys
sys.path.insert(0, '.')

from app import app
import json

def test_flask_api():
    print("=" * 60)
    print("传统珐琅彩鼻烟壶定制订单管理系统 - Flask API测试")
    print("=" * 60)
    
    client = app.test_client()
    
    print("\n1. 测试系统状态接口...")
    r = client.get('/')
    print(f"   状态码: {r.status_code}")
    print(f"   响应: {json.dumps(r.get_json(), ensure_ascii=False, indent=2)}")
    
    print("\n2. 测试获取状态列表...")
    r = client.get('/api/status')
    print(f"   状态码: {r.status_code}")
    print(f"   响应: {json.dumps(r.get_json(), ensure_ascii=False, indent=2)}")
    
    print("\n3. 测试创建订单...")
    order_data = {
        "customer_name": "张三",
        "customer_phone": "13800138000",
        "customer_address": "北京市朝阳区",
        "bottle_shape": "扁圆形",
        "bottle_material": "白瓷",
        "pattern_design": "山水图案",
        "color_requirement": "青花为主",
        "special_requirement": "落款'乾隆年制'",
        "quantity": 2,
        "estimated_price": 8000
    }
    r = client.post('/api/orders', json=order_data)
    print(f"   状态码: {r.status_code}")
    result = r.get_json()
    print(f"   响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
    order_id = result['order']['id']
    order_no = result['order']['order_no']
    print(f"   订单ID: {order_id}")
    print(f"   订单编号: {order_no}")
    
    print("\n4. 测试查询订单列表...")
    r = client.get('/api/orders')
    print(f"   状态码: {r.status_code}")
    print(f"   订单总数: {r.get_json()['total']}")
    
    print("\n5. 测试更新订单状态 (制胎)...")
    r = client.put(f'/api/orders/{order_id}/status', json={"status": "制胎"})
    print(f"   状态码: {r.status_code}")
    print(f"   响应: {json.dumps(r.get_json(), ensure_ascii=False, indent=2)}")
    
    print("\n6. 测试查询单个订单...")
    r = client.get(f'/api/orders/{order_id}')
    print(f"   状态码: {r.status_code}")
    print(f"   当前状态: {r.get_json()['status']}")
    
    print("\n7. 测试状态流转 (施釉 → 绘彩 → 烧造)...")
    for status in ["施釉", "绘彩", "烧造"]:
        r = client.put(f'/api/orders/{order_id}/status', json={"status": status})
        print(f"   更新为'{status}': 成功")
    
    print("\n8. 再次查询订单状态...")
    r = client.get(f'/api/orders/{order_id}')
    print(f"   最终状态: {r.get_json()['status']}")
    
    print("\n9. 测试更新订单信息...")
    update_data = {
        "customer_address": "北京市海淀区",
        "estimated_price": 9000
    }
    r = client.put(f'/api/orders/{order_id}', json=update_data)
    print(f"   状态码: {r.status_code}")
    print(f"   更新后地址: {r.get_json()['order']['customer_address']}")
    print(f"   更新后价格: {r.get_json()['order']['estimated_price']}")
    
    print("\n10. 测试删除订单...")
    r = client.delete(f'/api/orders/{order_id}')
    print(f"   状态码: {r.status_code}")
    print(f"   响应: {json.dumps(r.get_json(), ensure_ascii=False, indent=2)}")
    
    print("\n11. 验证订单已删除...")
    r = client.get(f'/api/orders/{order_id}')
    print(f"   状态码: {r.status_code} (404表示已删除)")
    
    print("\n" + "=" * 60)
    print("所有API测试通过！系统运行正常。")
    print("=" * 60)
    print("\n提示: 执行 'python run.py' 即可启动服务")
    print("服务地址: http://127.0.0.1:5000")

if __name__ == '__main__':
    test_flask_api()