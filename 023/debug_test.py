import requests
import json

BASE_URL = 'http://localhost:5000/api'

print("测试创建订单...")
order_data = {
    'customer_name': '测试用户',
    'customer_phone': '13800138000',
    'paperweight_style': '方形瑞兽',
    'length_cm': 8.0,
    'width_cm': 5.0,
    'thickness_cm': 2.0,
    'copper_type': 'H62黄铜',
    'carving_pattern': '祥云纹',
    'surface_finish': '复古做旧',
    'quantity': 10
}

print(f"请求数据: {json.dumps(order_data, ensure_ascii=False, indent=2)}")
response = requests.post(f'{BASE_URL}/orders', json=order_data)
print(f"\n状态码: {response.status_code}")
print(f"响应内容: {response.text}")
