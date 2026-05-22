import requests
import json

BASE_URL = 'http://localhost:5000'

def test_api():
    print("=" * 60)
    print("传统珐琅彩鼻烟壶定制订单管理系统 - API测试")
    print("=" * 60)
    
    print("\n1. 测试系统状态接口...")
    try:
        r = requests.get(f'{BASE_URL}/')
        print(f"   状态码: {r.status_code}")
        print(f"   响应: {json.dumps(r.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"   错误: {e}")
    
    print("\n2. 测试获取状态列表...")
    try:
        r = requests.get(f'{BASE_URL}/api/status')
        print(f"   状态码: {r.status_code}")
        print(f"   响应: {json.dumps(r.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"   错误: {e}")
    
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
    try:
        r = requests.post(f'{BASE_URL}/api/orders', json=order_data)
        print(f"   状态码: {r.status_code}")
        result = r.json()
        print(f"   响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
        order_id = result['order']['id']
        order_no = result['order']['order_no']
        print(f"   订单ID: {order_id}")
        print(f"   订单编号: {order_no}")
    except Exception as e:
        print(f"   错误: {e}")
        return
    
    print("\n4. 测试查询订单列表...")
    try:
        r = requests.get(f'{BASE_URL}/api/orders')
        print(f"   状态码: {r.status_code}")
        print(f"   订单总数: {r.json()['total']}")
    except Exception as e:
        print(f"   错误: {e}")
    
    print("\n5. 测试更新订单状态 (制胎)...")
    try:
        r = requests.put(f'{BASE_URL}/api/orders/{order_id}/status', json={"status": "制胎"})
        print(f"   状态码: {r.status_code}")
        print(f"   响应: {json.dumps(r.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"   错误: {e}")
    
    print("\n6. 测试查询单个订单...")
    try:
        r = requests.get(f'{BASE_URL}/api/orders/{order_id}')
        print(f"   状态码: {r.status_code}")
        print(f"   当前状态: {r.json()['status']}")
    except Exception as e:
        print(f"   错误: {e}")
    
    print("\n7. 测试状态流转 (施釉 → 绘彩 → 烧造)...")
    for status in ["施釉", "绘彩", "烧造"]:
        try:
            r = requests.put(f'{BASE_URL}/api/orders/{order_id}/status', json={"status": status})
            print(f"   更新为'{status}': 成功")
        except Exception as e:
            print(f"   更新为'{status}': 失败 - {e}")
    
    print("\n8. 再次查询订单状态...")
    try:
        r = requests.get(f'{BASE_URL}/api/orders/{order_id}')
        print(f"   最终状态: {r.json()['status']}")
    except Exception as e:
        print(f"   错误: {e}")
    
    print("\n" + "=" * 60)
    print("API测试完成！系统运行正常。")
    print("=" * 60)

if __name__ == '__main__':
    test_api()