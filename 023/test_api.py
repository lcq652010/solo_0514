import requests
import json

BASE_URL = 'http://localhost:5000/api'

def test_craftsmen():
    print('=== 测试获取匠人列表 ===')
    response = requests.get(f'{BASE_URL}/craftsmen')
    data = response.json()
    print(f'状态码: {response.status_code}')
    print(f'返回: {json.dumps(data, ensure_ascii=False, indent=2)}')

def test_copper_types():
    print('\n=== 测试获取铜材类型列表 ===')
    response = requests.get(f'{BASE_URL}/copper-types')
    data = response.json()
    print(f'状态码: {response.status_code}')
    print(f'数量: {len(data["data"])}')

def test_carving_patterns():
    print('\n=== 测试获取錾刻纹样列表 ===')
    response = requests.get(f'{BASE_URL}/carving-patterns')
    data = response.json()
    print(f'状态码: {response.status_code}')
    print(f'数量: {len(data["data"])}')

def test_surface_finishes():
    print('\n=== 测试获取表面工艺列表 ===')
    response = requests.get(f'{BASE_URL}/surface-finishes')
    data = response.json()
    print(f'状态码: {response.status_code}')
    print(f'数量: {len(data["data"])}')

def test_calculate_price():
    print('\n=== 测试自动计价功能 ===')
    calc_data = {
        'length_cm': 8.0,
        'width_cm': 8.0,
        'thickness_cm': 2.0,
        'copper_type': 'H62黄铜',
        'carving_pattern': '祥云纹',
        'surface_finish': '复古做旧',
        'quantity': 2
    }
    response = requests.post(f'{BASE_URL}/calculate-price', json=calc_data)
    data = response.json()
    print(f'状态码: {response.status_code}')
    print(f'价格明细: {json.dumps(data["data"], ensure_ascii=False, indent=2)}')

def test_validation():
    print('\n=== 测试必填校验功能 ===')
    invalid_data = {
        'customer_name': '',
        'customer_phone': '123456789',
        'paperweight_style': '方形瑞兽',
        'length_cm': 8.0,
        'width_cm': 8.0,
        'thickness_cm': 2.0,
        'quantity': 2
    }
    response = requests.post(f'{BASE_URL}/orders', json=invalid_data)
    data = response.json()
    print(f'状态码: {response.status_code}')
    print(f'错误信息: {data["message"]}')

def test_create_order():
    print('\n=== 测试创建订单（包含自动计价）===')
    order_data = {
        'customer_name': '张三',
        'customer_phone': '13800138000',
        'customer_address': '北京市朝阳区xxx街道xxx号',
        'paperweight_style': '方形瑞兽',
        'length_cm': 8.0,
        'width_cm': 8.0,
        'thickness_cm': 2.0,
        'inscription': '宁静致远',
        'copper_type': 'H62黄铜',
        'carving_pattern': '祥云纹',
        'surface_finish': '复古做旧',
        'quantity': 2,
        'requirements': '边角圆润，表面哑光处理'
    }
    response = requests.post(f'{BASE_URL}/orders', json=order_data)
    data = response.json()
    print(f'状态码: {response.status_code}')
    print(f'返回: {json.dumps(data, ensure_ascii=False, indent=2)}')
    return data['data']['order_no'] if data['code'] == 200 else None

def test_get_order(order_no):
    print(f'\n=== 测试获取订单详情 {order_no} ===')
    response = requests.get(f'{BASE_URL}/orders/{order_no}')
    data = response.json()
    print(f'状态码: {response.status_code}')
    order = data['data']
    print(f'订单号: {order["order_no"]}')
    print(f'总价: {order["total_price"]} 元')
    print(f'预计工期: {order["estimated_days"]} 天')
    print(f'交付日期: {order["delivery_date"]}')

def test_assign_craftsman(order_no):
    print(f'\n=== 测试分配匠人 {order_no} ===')
    assign_data = {
        'craftsman_id': 1,
        'craftsman_name': '王师傅'
    }
    response = requests.put(f'{BASE_URL}/orders/{order_no}/craftsman', json=assign_data)
    data = response.json()
    print(f'状态码: {response.status_code}')
    print(f'返回: {json.dumps(data, ensure_ascii=False, indent=2)}')

def test_update_status(order_no, status):
    print(f'\n=== 测试更新订单状态为: {status} ===')
    response = requests.put(f'{BASE_URL}/orders/{order_no}/status', json={'status': status})
    data = response.json()
    print(f'状态码: {response.status_code}')
    print(f'返回: {json.dumps(data, ensure_ascii=False, indent=2)}')

def test_get_orders_with_filters():
    print('\n=== 测试获取订单列表（带分页和筛选）===')
    params = {
        'page': 1,
        'page_size': 5,
        'status': '制版',
        'style': '方形瑞兽',
        'sort_by': 'created_at',
        'sort_order': 'desc'
    }
    response = requests.get(f'{BASE_URL}/orders', params=params)
    data = response.json()
    print(f'状态码: {response.status_code}')
    print(f'总数: {data["data"]["pagination"]["total"]}')
    print(f'当前页: {data["data"]["pagination"]["page"]}')
    print(f'订单数量: {len(data["data"]["list"])}')

def test_stats():
    print('\n=== 测试获取统计信息（包含总金额）===')
    response = requests.get(f'{BASE_URL}/stats')
    data = response.json()
    print(f'状态码: {response.status_code}')
    print(f'总订单数: {data["data"]["total"]}')
    print(f'总金额: {data["data"]["total_amount"]} 元')

def create_test_orders(count=5):
    print(f'\n=== 创建 {count} 个测试订单 ===')
    styles = ['方形瑞兽', '长条形素面', '圆形浮雕', '随形巧雕']
    coppers = ['H62黄铜', 'H65黄铜', 'T2紫铜', 'QSn4-3青铜']
    patterns = ['无纹样', '祥云纹', '回纹', '龙凤纹']
    finishes = ['原色抛光', '哑光拉丝', '复古做旧', '黑漆古']
    statuses = ['待接单', '制版', '熔铜', '浇铸', '打磨', '錾刻', '做旧', '完工']
    
    for i in range(count):
        order_data = {
            'customer_name': f'测试客户{i+1}',
            'customer_phone': f'1380000000{i}',
            'paperweight_style': styles[i % len(styles)],
            'length_cm': 6.0 + i,
            'width_cm': 4.0 + i * 0.5,
            'thickness_cm': 1.5 + i * 0.2,
            'copper_type': coppers[i % len(coppers)],
            'carving_pattern': patterns[i % len(patterns)],
            'surface_finish': finishes[i % len(finishes)],
            'quantity': 1 + i
        }
        response = requests.post(f'{BASE_URL}/orders', json=order_data)
        data = response.json()
        if data['code'] == 200:
            order_no = data['data']['order_no']
            test_update_status(order_no, statuses[i % len(statuses)])
            print(f'创建订单 {order_no} 成功，状态: {statuses[i % len(statuses)]}')

if __name__ == '__main__':
    try:
        test_craftsmen()
        test_copper_types()
        test_carving_patterns()
        test_surface_finishes()
        test_calculate_price()
        test_validation()
        
        order_no = test_create_order()
        if order_no:
            test_get_order(order_no)
            test_assign_craftsman(order_no)
            test_update_status(order_no, '制版')
            test_update_status(order_no, '熔铜')
            test_update_status(order_no, '浇铸')
            
            create_test_orders(5)
            
            test_get_orders_with_filters()
            test_stats()
            
        print('\n✅ 所有测试完成！')
    except requests.exceptions.ConnectionError:
        print('\n❌ 错误: 无法连接到服务器，请先启动 app.py')
        print('运行命令: python app.py')