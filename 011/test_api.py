import requests
import json

BASE_URL = 'http://localhost:5000/api'

def print_response(result):
    print(f"Code: {result.get('code')}")
    print(f"Success: {result.get('success')}")
    print(f"Message: {result.get('message')}")
    if result.get('data'):
        print(f"Data: {json.dumps(result['data'], ensure_ascii=False, indent=2)[:500]}...")

def test_validation():
    print('\n=== 测试必填校验与数值规范 ===')
    
    print('测试1: 缺少必填字段')
    response = requests.post(f'{BASE_URL}/orders', json={
        'customer_name': '张三',
        'ink_type': '松烟墨',
        'quantity': 10
    })
    result = response.json()
    print(f"预期: 手机号必填，实际: {result['message']}")
    assert 'customer_phone' in result['message'], '手机号校验失败'
    
    print('测试2: 手机号格式错误')
    response = requests.post(f'{BASE_URL}/orders', json={
        'customer_name': '张三',
        'customer_phone': '123456',
        'ink_type': '松烟墨',
        'quantity': 10
    })
    result = response.json()
    print(f"预期: 手机号格式不正确，实际: {result['message']}")
    assert '手机号格式不正确' in result['message'], '手机号格式校验失败'
    
    print('测试3: 数量不是正整数')
    response = requests.post(f'{BASE_URL}/orders', json={
        'customer_name': '张三',
        'customer_phone': '13800138000',
        'ink_type': '松烟墨',
        'quantity': -5
    })
    result = response.json()
    print(f"预期: 数量必须是正整数，实际: {result['message']}")
    assert '数量必须是正整数' in result['message'], '数量校验失败'
    
    print('测试4: 墨料类型错误')
    response = requests.post(f'{BASE_URL}/orders', json={
        'customer_name': '张三',
        'customer_phone': '13800138000',
        'ink_type': '松烟墨',
        'quantity': 10,
        'material_type': '不存在的墨料'
    })
    result = response.json()
    print(f"预期: 墨料类型不正确，实际: {result['message']}")
    assert '墨料类型不正确' in result['message'], '墨料类型校验失败'
    
    print('✓ 必填校验与数值规范测试通过')

def test_auto_pricing():
    print('\n=== 测试自动计价功能 ===')
    
    order_data = {
        'customer_name': '张三',
        'customer_phone': '13800138000',
        'customer_address': '安徽省黄山市歙县',
        'ink_type': '松烟墨',
        'material_type': '漆烟',
        'weight': '100g',
        'ink_style': '长方形墨',
        'spec_size': '10cm x 3cm x 1.5cm',
        'shape': '长方形',
        'pattern': '龙纹',
        'gilding_pattern': '二龙戏珠，边缘云纹描金',
        'complexity': '复杂',
        'quantity': 20
    }
    
    response = requests.post(f'{BASE_URL}/orders', json=order_data)
    result = response.json()
    
    if result['success']:
        order = result['data']['order']
        unit_price = order['unit_price']
        total_price = order['total_price']
        print(f"墨料: {order['material_type']}, 重量: {order['weight']}, 复杂度: {order['complexity']}")
        print(f"数量: {order['quantity']}, 单价: {unit_price}元, 总价: {total_price}元")
        assert unit_price > 0, '单价应为正数'
        assert total_price == unit_price * order['quantity'], '总价计算错误'
        print('✓ 自动计价测试通过')
        return order['order_no']
    else:
        print(f"创建订单失败: {result['message']}")
        return None

def test_craftsman_assignment(order_no):
    print('\n=== 测试匠人绑定功能 ===')
    
    response = requests.get(f'{BASE_URL}/craftsmen')
    result = response.json()
    print(f"匠人列表: {[c['name'] for c in result['data']['craftsmen']]}")
    
    response = requests.put(f'{BASE_URL}/orders/{order_no}/craftsman', json={
        'craftsman_id': 3
    })
    result = response.json()
    
    if result['success']:
        order = result['data']['order']
        print(f"分配匠人: {order['craftsman_name']}")
        assert order['craftsman_id'] == 3, '匠人ID绑定错误'
        print('✓ 匠人绑定测试通过')
    else:
        print(f"匠人绑定失败: {result['message']}")

def test_delivery_date(order_no):
    print('\n=== 测试工期与交付日期 ===')
    
    response = requests.get(f'{BASE_URL}/orders/{order_no}')
    result = response.json()
    
    if result['success']:
        order = result['data']
        print(f"预估工期: {order['est_days']}天")
        print(f"交付日期: {order['delivery_date']}")
        assert order['est_days'] > 0, '预估工应为正数'
        assert order['delivery_date'], '交付日期不能为空'
        print('✓ 工期与交付日期测试通过')

def test_advanced_filter():
    print('\n=== 测试高级筛选与排序 ===')
    
    for i in range(3):
        orders = [
            {'customer_name': f'客户{i+1}', 'customer_phone': f'1380013800{i+1}', 
             'ink_type': '松烟墨', 'material_type': '油烟', 'ink_style': '圆形墨', 'quantity': 5,
             'complexity': '简单', 'delivery_date': '2025-06-15'},
            {'customer_name': f'客户{i+4}', 'customer_phone': f'1390013800{i+1}', 
             'ink_type': '油烟墨', 'material_type': '漆烟', 'ink_style': '长方形墨', 'quantity': 10,
             'complexity': '复杂', 'delivery_date': '2025-06-20'},
        ]
        for o in orders:
            requests.post(f'{BASE_URL}/orders', json=o)
    
    print('测试1: 按墨锭款式筛选')
    response = requests.get(f'{BASE_URL}/orders?ink_style=长方形墨')
    result = response.json()
    if result['success']:
        print(f"长方形墨订单数: {result['data']['pagination']['total']}")
    
    print('测试2: 按墨料类型筛选')
    response = requests.get(f'{BASE_URL}/orders?material_type=漆烟')
    result = response.json()
    if result['success']:
        print(f"漆烟墨订单数: {result['data']['pagination']['total']}")
    
    print('测试3: 按交付日期范围筛选')
    response = requests.get(f'{BASE_URL}/orders?delivery_date_from=2025-06-10&delivery_date_to=2025-06-18')
    result = response.json()
    if result['success']:
        print(f"日期范围内订单数: {result['data']['pagination']['total']}")
    
    print('测试4: 按价格排序')
    response = requests.get(f'{BASE_URL}/orders?sort_by=total_price&sort_order=DESC&per_page=3')
    result = response.json()
    if result['success']:
        orders = result['data']['orders']
        prices = [o['total_price'] for o in orders]
        print(f"价格排序(降序): {prices}")
        assert prices == sorted(prices, reverse=True), '排序结果错误'
    
    print('测试5: 分页功能')
    response = requests.get(f'{BASE_URL}/orders?page=1&per_page=2')
    result = response.json()
    if result['success']:
        print(f"第1页，每页2条，总页数: {result['data']['pagination']['total_pages']}")
    
    print('✓ 高级筛选与排序测试通过')

def test_unified_response_format():
    print('\n=== 测试统一响应格式 ===')
    
    endpoints = [
        ('GET', '/statuses', None),
        ('GET', '/material-types', None),
        ('GET', '/ink-styles', None),
        ('GET', '/complexity-levels', None),
        ('GET', '/craftsmen', None),
    ]
    
    for method, endpoint, data in endpoints:
        if method == 'GET':
            response = requests.get(f'{BASE_URL}{endpoint}')
        else:
            response = requests.post(f'{BASE_URL}{endpoint}', json=data)
        
        result = response.json()
        assert 'code' in result, f'{endpoint} 缺少 code 字段'
        assert 'success' in result, f'{endpoint} 缺少 success 字段'
        assert 'message' in result, f'{endpoint} 缺少 message 字段'
        assert 'data' in result, f'{endpoint} 缺少 data 字段'
        print(f"✓ {endpoint} 格式正确")
    
    print('✓ 统一响应格式测试通过')

def test_production_guide(order_no):
    print('\n=== 测试生产指导接口 ===')
    
    response = requests.get(f'{BASE_URL}/orders/{order_no}/production-guide')
    result = response.json()
    
    if result['success']:
        guide = result['data']
        print(f"订单: {guide['order_no']}, 状态: {guide['status']}")
        print(f"总价: {guide['total_price']}元")
        print(f"匠人: {guide.get('craftsman', '未分配')}")
        print(f"交付日期: {guide['delivery_date']}")
        print(f"工序数: {len(guide['steps'])}")
        for step, info in guide['steps'].items():
            print(f"  - {step}: {info['guide'][:50]}...")
        print('✓ 生产指导测试通过')

if __name__ == '__main__':
    print('=' * 70)
    print('徽墨定制订单管理系统 - 高级功能测试')
    print('=' * 70)
    
    try:
        test_unified_response_format()
        test_validation()
        order_no = test_auto_pricing()
        
        if order_no:
            test_craftsman_assignment(order_no)
            test_delivery_date(order_no)
            test_production_guide(order_no)
            test_advanced_filter()
        
        print('\n' + '=' * 70)
        print('✓ 所有测试完成！')
        print('=' * 70)
        
    except requests.exceptions.ConnectionError:
        print('\n错误: 无法连接到服务器，请先运行 app.py')
    except AssertionError as e:
        print(f'\n测试失败: {e}')
    except Exception as e:
        print(f'\n错误: {e}')
        import traceback
        traceback.print_exc()
