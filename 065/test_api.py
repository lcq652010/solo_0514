import requests
import json

BASE_URL = 'http://127.0.0.1:5000'

def test_api():
    print('=' * 50)
    print('麦秆贴画书签订单管理系统 API 测试')
    print('=' * 50)
    
    print('\n1. 测试首页')
    try:
        response = requests.get(f'{BASE_URL}/')
        print(f'状态码: {response.status_code}')
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    except Exception as e:
        print(f'错误: {e}')
        return
    
    print('\n2. 测试获取订单状态')
    try:
        response = requests.get(f'{BASE_URL}/api/statuses')
        print(f'状态码: {response.status_code}')
        print('订单状态列表:', response.json())
    except Exception as e:
        print(f'错误: {e}')
    
    print('\n3. 测试创建订单')
    order_data = {
        'customer_name': '张三',
        'phone': '13800138000',
        'email': 'zhangsan@example.com',
        'design_description': '梅兰竹菊图案，古典风格',
        'quantity': 5,
        'deadline': '2026-06-01',
        'remark': '希望颜色鲜艳一些'
    }
    try:
        response = requests.post(f'{BASE_URL}/api/orders', json=order_data)
        print(f'状态码: {response.status_code}')
        result = response.json()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        order_id = result.get('order_id')
    except Exception as e:
        print(f'错误: {e}')
        return
    
    print('\n4. 测试创建第二个订单')
    order_data2 = {
        'customer_name': '李四',
        'phone': '13900139000',
        'design_description': '山水风景图案',
        'quantity': 10
    }
    try:
        response = requests.post(f'{BASE_URL}/api/orders', json=order_data2)
        print(f'状态码: {response.status_code}')
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    except Exception as e:
        print(f'错误: {e}')
    
    print('\n5. 测试获取所有订单')
    try:
        response = requests.get(f'{BASE_URL}/api/orders')
        print(f'状态码: {response.status_code}')
        orders = response.json()
        print(f'订单数量: {len(orders)}')
        for order in orders:
            print(f"  - {order['id']}: {order['customer_name']} - {order['status']}")
    except Exception as e:
        print(f'错误: {e}')
    
    print(f'\n6. 测试获取单个订单 ({order_id})')
    try:
        response = requests.get(f'{BASE_URL}/api/orders/{order_id}')
        print(f'状态码: {response.status_code}')
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    except Exception as e:
        print(f'错误: {e}')
    
    print(f'\n7. 测试更新订单状态为"选麦秆" ({order_id})')
    try:
        response = requests.put(
            f'{BASE_URL}/api/orders/{order_id}/status',
            json={'status': '选麦秆'}
        )
        print(f'状态码: {response.status_code}')
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    except Exception as e:
        print(f'错误: {e}')
    
    print(f'\n8. 验证订单状态更新')
    try:
        response = requests.get(f'{BASE_URL}/api/orders/{order_id}')
        order = response.json()
        print(f"当前状态: {order['status']}")
        print(f"更新时间: {order['updated_at']}")
    except Exception as e:
        print(f'错误: {e}')
    
    print(f'\n9. 测试更新订单信息 ({order_id})')
    try:
        response = requests.put(
            f'{BASE_URL}/api/orders/{order_id}',
            json={'quantity': 8, 'remark': '修改为8个，加急处理'}
        )
        print(f'状态码: {response.status_code}')
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    except Exception as e:
        print(f'错误: {e}')
    
    print('\n' + '=' * 50)
    print('API 测试完成!')
    print('=' * 50)

if __name__ == '__main__':
    test_api()
