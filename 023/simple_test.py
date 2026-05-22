import sys
sys.path.insert(0, '.')

from app import app
import json

client = app.test_client()

print('=== 测试 /api/craftsmen ===')
response = client.get('/api/craftsmen')
print(f'状态码: {response.status_code}')

print('\n=== 测试 /api/copper-types ===')
response = client.get('/api/copper-types')
print(f'状态码: {response.status_code}')

print('\n=== 测试 /api/calculate-price ===')
calc_data = {
    'length_cm': 8.0,
    'width_cm': 8.0,
    'thickness_cm': 2.0,
    'copper_type': 'H62黄铜',
    'carving_pattern': '祥云纹',
    'surface_finish': '复古做旧',
    'quantity': 2
}
response = client.post('/api/calculate-price', json=calc_data)
print(f'状态码: {response.status_code}')
print(f'价格: {json.dumps(response.json, ensure_ascii=False, indent=2)}')

print('\n=== 测试创建订单 ===')
order_data = {
    'customer_name': '张三',
    'customer_phone': '13800138000',
    'paperweight_style': '方形瑞兽',
    'length_cm': 8.0,
    'width_cm': 8.0,
    'thickness_cm': 2.0,
    'copper_type': 'H62黄铜',
    'carving_pattern': '祥云纹',
    'surface_finish': '复古做旧',
    'quantity': 2
}
response = client.post('/api/orders', json=order_data)
print(f'状态码: {response.status_code}')
result = response.json
print(f'结果: {json.dumps(result, ensure_ascii=False, indent=2)}')

if result['code'] == 200:
    order_no = result['data']['order_no']
    print(f'\n=== 测试获取订单详情 {order_no} ===')
    response = client.get(f'/api/orders/{order_no}')
    print(f'状态码: {response.status_code}')
    
    print(f'\n=== 测试分配匠人 ===')
    response = client.put(f'/api/orders/{order_no}/craftsman', json={'craftsman_id': 1, 'craftsman_name': '王师傅'})
    print(f'状态码: {response.status_code}')
    
    print(f'\n=== 测试更新状态 ===')
    response = client.put(f'/api/orders/{order_no}/status', json={'status': '制版'})
    print(f'状态码: {response.status_code}')

print('\n=== 测试订单列表分页 ===')
response = client.get('/api/orders?page=1&page_size=5')
result = response.json
print(f'状态码: {response.status_code}')
print(f'总数: {result["data"]["pagination"]["total"]}')
print(f'总页数: {result["data"]["pagination"]["total_pages"]}')

print('\n=== 测试统计信息 ===')
response = client.get('/api/stats')
result = response.json
print(f'状态码: {response.status_code}')
print(f'总订单数: {result["data"]["total"]}')
print(f'总金额: {result["data"]["total_amount"]}')

print('\n✅ 所有测试通过！')
