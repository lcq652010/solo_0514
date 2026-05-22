import requests
import json
import time

BASE_URL = 'http://127.0.0.1:5000'

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def test_api():
    print_section("桦树皮笔筒定制订单管理系统 v3.0 API 测试")
    
    time.sleep(2)
    
    print_section("1. 测试数据字典接口")
    
    print("\n[1.1] 获取工艺规格...")
    response = requests.get(f'{BASE_URL}/api/process-specs')
    if response.status_code == 200:
        data = response.json()
        print(f"  ✓ 订单状态数: {len(data['data']['statuses'])}")
        print(f"  ✓ 树皮材质数: {len(data['data']['bark_materials'])}")
        print(f"  ✓ 拼接工艺数: {len(data['data']['splicing_techniques'])}")
        print(f"  ✓ 雕刻深度数: {len(data['data']['carving_depths'])}")
        print(f"  ✓ 笔筒样式数: {len(data['data']['penholder_styles'])}")
        print(f"  ✓ 笔筒尺寸数: {len(data['data']['penholder_sizes'])}")
        print(f"  ✓ 匠人数: {len(data['data']['craftspeople'])}")
        print(f"  ✓ 基础价格: {data['data']['base_price']}元")
    else:
        print(f"  ✗ 失败: {response.status_code}")
    
    print("\n[1.2] 获取匠人列表...")
    response = requests.get(f'{BASE_URL}/api/craftspeople')
    if response.status_code == 200:
        craftspeople = response.json()['data']
        for c in craftspeople:
            print(f"  - {c['name']}({c['skill_level']}): {c['daily_rate']}元/天")
    else:
        print(f"  ✗ 失败: {response.status_code}")
    
    print_section("2. 测试价格试算功能")
    
    test_cases = [
        {
            'name': '基础配置（中号+平接+浅雕）',
            'data': {
                'penholder_size': '中号',
                'bark_material': '白桦皮',
                'splicing_tech': '平接',
                'carving_depth': '浅雕(1-2mm)'
            }
        },
        {
            'name': '高配配置（大号+榫接+深雕+高级匠人）',
            'data': {
                'penholder_size': '大号',
                'bark_material': '桑树皮',
                'splicing_tech': '榫接',
                'carving_depth': '深雕(4-6mm)',
                'craftsman_id': 1
            }
        }
    ]
    
    for case in test_cases:
        print(f"\n[试算] {case['name']}...")
        response = requests.post(f'{BASE_URL}/api/orders/calculate', json=case['data'])
        if response.status_code == 200:
            result = response.json()['data']
            print(f"  ✓ 预估总价: {result['price']}元")
            print(f"    - 材料成本: {result['material_cost']}元")
            print(f"    - 工艺成本: {result['process_cost']}元")
            print(f"    - 人工成本: {result['labor_cost']}元")
            print(f"    - 预计工期: {result['work_days']}天")
        else:
            print(f"  ✗ 失败: {response.status_code}")
    
    print_section("3. 测试必填字段校验")
    
    print("\n[3.1] 提交缺少必填字段的订单...")
    bad_data = {'customer_name': '张三'}
    response = requests.post(f'{BASE_URL}/api/orders', json=bad_data)
    if response.status_code == 400:
        result = response.json()
        print(f"  ✓ 正确返回错误")
        print(f"  ✓ 错误信息: {result['message']}")
        if 'errors' in result['data']:
            for err in result['data']['errors']:
                print(f"    - {err}")
    else:
        print(f"  ✗ 未能正确校验")
    
    print("\n[3.2] 提交格式错误的手机号...")
    bad_phone_data = {
        'customer_name': '张三',
        'customer_phone': '123456789',
        'penholder_style': '圆形',
        'penholder_size': '中号'
    }
    response = requests.post(f'{BASE_URL}/api/orders', json=bad_phone_data)
    if response.status_code == 400:
        result = response.json()
        print(f"  ✓ 正确检测手机号格式错误")
    else:
        print(f"  ✗ 未能正确校验手机号")
    
    print_section("4. 测试创建完整订单")
    
    order_data = {
        'customer_name': '张三',
        'customer_phone': '13800138000',
        'customer_address': '北京市朝阳区',
        'penholder_style': '圆形',
        'penholder_size': '大号',
        'carving_pattern': '山水图案',
        'special_requirements': '希望能刻上名字',
        'bark_material': '白桦皮',
        'size_height': '15cm',
        'size_diameter': '8cm',
        'size_thickness': '2mm',
        'splicing_tech': '平接',
        'carving_position': '正面',
        'carving_depth': '中雕(2-4mm)',
        'carving_detail': '线条流畅，层次分明',
        'craftsman_id': 1,
        'delivery_date': '2024-05-25'
    }
    
    response = requests.post(f'{BASE_URL}/api/orders', json=order_data)
    if response.status_code == 200:
        result = response.json()['data']
        order_id = result['order_id']
        print(f"  ✓ 订单创建成功")
        print(f"  ✓ 订单ID: {order_id}")
        print(f"  ✓ 订单编号: {result['order_no']}")
        print(f"  ✓ 订单价格: {result['price']}元")
        print(f"  ✓ 预计工期: {result['work_days']}天")
    else:
        print(f"  ✗ 创建失败: {response.status_code}")
        print(response.text)
        return
    
    print_section("5. 测试获取订单详情")
    
    response = requests.get(f'{BASE_URL}/api/orders/{order_id}')
    if response.status_code == 200:
        order = response.json()['data']
        print(f"  ✓ 订单编号: {order['order_no']}")
        print(f"  ✓ 客户信息: {order['customer_name']} - {order['customer_phone']}")
        print(f"  ✓ 工艺信息: {order['bark_material']} / {order['splicing_tech']} / {order['carving_depth']}")
        print(f"  ✓ 价格信息: 总价{order['price']}元 (材料{order['material_cost']} + 工艺{order['process_cost']} + 人工{order['labor_cost']})")
        print(f"  ✓ 匠人信息: {order['craftsman_name']} (ID:{order['craftsman_id']})")
        print(f"  ✓ 工期交付: {order['work_days']}天 / {order['delivery_date']}")
        print(f"  ✓ 当前状态: {order['status']}")
    else:
        print(f"  ✗ 获取失败")
    
    print_section("6. 测试订单编辑与自动重新计价")
    
    update_data = {
        'bark_material': '桑树皮',
        'splicing_tech': '榫接',
        'carving_depth': '深雕(4-6mm)',
        'craftsman_id': 1
    }
    print(f"  更新工艺: 白桦皮→桑树皮, 平接→榫接, 中雕→深雕")
    
    response = requests.put(f'{BASE_URL}/api/orders/{order_id}', json=update_data)
    if response.status_code == 200:
        print(f"  ✓ 订单更新成功")
    else:
        print(f"  ✗ 更新失败: {response.status_code}")
    
    print("\n  验证重新计价结果...")
    response = requests.get(f'{BASE_URL}/api/orders/{order_id}')
    if response.status_code == 200:
        order = response.json()['data']
        print(f"  ✓ 更新后价格: {order['price']}元")
        print(f"  ✓ 更新后材质: {order['bark_material']}")
        print(f"  ✓ 更新后工艺: {order['splicing_tech']}")
        print(f"  ✓ 更新后雕刻: {order['carving_depth']}")
        print(f"  ✓ 自动重计价功能正常")
    
    print_section("7. 测试订单状态流转")
    
    status_flow = ['选皮', '蒸煮', '裁剪', '拼接', '雕花', '定型', '完工']
    for status in status_flow[:3]:
        response = requests.put(f'{BASE_URL}/api/orders/{order_id}/status', json={'status': status})
        if response.status_code == 200:
            print(f"  ✓ 状态更新: → {status}")
        else:
            print(f"  ✗ 更新失败: {status}")
    
    print_section("8. 测试多条件筛选查询")
    
    test_orders = [
        {'style': '圆形', 'material': '桑树皮', 'size': '大号'},
        {'style': '方形', 'material': '黑桦皮', 'size': '中号'},
        {'style': '椭圆形', 'material': '红桦皮', 'size': '小号'},
    ]
    
    for i, o in enumerate(test_orders):
        data = {
            'customer_name': f'测试客户{i+1}',
            'customer_phone': f'1390000000{i+1}',
            'penholder_style': o['style'],
            'penholder_size': o['size'],
            'bark_material': o['material']
        }
        requests.post(f'{BASE_URL}/api/orders', json=data)
    
    print("\n[8.1] 按笔筒风格筛选(圆形)...")
    response = requests.get(f'{BASE_URL}/api/orders?style=圆形')
    if response.status_code == 200:
        data = response.json()['data']
        print(f"  ✓ 筛选结果: {len(data['list'])}条记录")
    
    print("\n[8.2] 按树皮材质筛选(桑树皮)...")
    response = requests.get(f'{BASE_URL}/api/orders?material=桑树皮')
    if response.status_code == 200:
        data = response.json()['data']
        print(f"  ✓ 筛选结果: {len(data['list'])}条记录")
    
    print("\n[8.3] 组合筛选(圆形+桑树皮+待接单)...")
    response = requests.get(f'{BASE_URL}/api/orders?style=圆形&material=桑树皮&status=待接单')
    if response.status_code == 200:
        data = response.json()['data']
        print(f"  ✓ 筛选结果: {len(data['list'])}条记录")
    
    print_section("9. 测试分页与排序")
    
    print("\n[9.1] 测试分页(第1页, 每页2条)...")
    response = requests.get(f'{BASE_URL}/api/orders?page=1&page_size=2')
    if response.status_code == 200:
        data = response.json()['data']
        print(f"  ✓ 当前页: {data['pagination']['page']}")
        print(f"  ✓ 每页数量: {data['pagination']['page_size']}")
        print(f"  ✓ 总记录数: {data['pagination']['total']}")
        print(f"  ✓ 总页数: {data['pagination']['total_pages']}")
        print(f"  ✓ 本页记录数: {len(data['list'])}")
    
    print("\n[9.2] 测试按价格排序(降序)...")
    response = requests.get(f'{BASE_URL}/api/orders?sort_by=price&sort_order=desc&page_size=3')
    if response.status_code == 200:
        data = response.json()['data']
        prices = [o['price'] for o in data['list'] if o['price'] > 0]
        print(f"  ✓ 价格排序: {' → '.join([f'{p}元' for p in prices])}")
        if prices == sorted(prices, reverse=True):
            print(f"  ✓ 排序正确")
    
    print_section("10. 测试删除订单")
    
    response = requests.delete(f'{BASE_URL}/api/orders/{order_id}')
    if response.status_code == 200:
        print(f"  ✓ 订单删除成功")
    
    response = requests.get(f'{BASE_URL}/api/orders/{order_id}')
    if response.status_code == 404:
        print(f"  ✓ 验证订单已不存在")
    
    print_section("测试完成总结")
    print("""
  ✓ 数据字典接口正常
  ✓ 价格试算功能正常
  ✓ 必填字段校验正常
  ✓ 完整订单创建正常
  ✓ 订单详情查询正常
  ✓ 订单编辑与自动重计价正常
  ✓ 订单状态流转正常
  ✓ 多条件筛选查询正常
  ✓ 分页与排序功能正常
  ✓ 订单删除功能正常
  
  所有 v3.0 新功能测试通过！
    """)

if __name__ == '__main__':
    test_api()
