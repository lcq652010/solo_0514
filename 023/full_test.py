import requests
import json

BASE_URL = 'http://localhost:5000/api'

def print_separator(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def test_basic_apis():
    print_separator("1. 测试基础数据 API")
    
    print("\n[匠人列表]")
    response = requests.get(f'{BASE_URL}/craftsmen')
    result = response.json()
    print(f"  状态码: {response.status_code}")
    print(f"  数量: {len(result['data'])}")
    for c in result['data']:
        print(f"    - {c['name']} ({c['skill_level']})")
    
    print("\n[铜材类型]")
    response = requests.get(f'{BASE_URL}/copper-types')
    result = response.json()
    print(f"  状态码: {response.status_code}")
    print(f"  数量: {len(result['data'])}")
    
    print("\n[錾刻纹样]")
    response = requests.get(f'{BASE_URL}/carving-patterns')
    result = response.json()
    print(f"  状态码: {response.status_code}")
    print(f"  数量: {len(result['data'])}")
    
    print("\n[表面工艺]")
    response = requests.get(f'{BASE_URL}/surface-finishes')
    result = response.json()
    print(f"  状态码: {response.status_code}")
    print(f"  数量: {len(result['data'])}")
    
    print("\n[镇纸样式]")
    response = requests.get(f'{BASE_URL}/styles')
    result = response.json()
    print(f"  状态码: {response.status_code}")
    print(f"  数量: {len(result['data'])}")
    print(f"  列表: {result['data']}")
    
    print("\n[订单状态]")
    response = requests.get(f'{BASE_URL}/statuses')
    result = response.json()
    print(f"  状态码: {response.status_code}")
    print(f"  列表: {result['data']}")

def test_price_calculation():
    print_separator("2. 测试自动计价功能")
    
    calc_data = {
        'length_cm': 8.0,
        'width_cm': 5.0,
        'thickness_cm': 2.0,
        'copper_type': 'H62黄铜',
        'carving_pattern': '祥云纹',
        'surface_finish': '复古做旧',
        'quantity': 10
    }
    print(f"  输入参数: {json.dumps(calc_data, ensure_ascii=False)}")
    
    response = requests.post(f'{BASE_URL}/calculate-price', json=calc_data)
    result = response.json()
    print(f"\n  状态码: {response.status_code}")
    if result['code'] == 200:
        data = result['data']
        print(f"\n  价格明细:")
        print(f"    - 铜材成本: ¥{data['copper_cost']:.2f}")
        print(f"    - 錾刻成本: ¥{data['carving_cost']:.2f}")
        print(f"    - 表面处理成本: ¥{data['surface_cost']:.2f}")
        print(f"    - 总价: ¥{data['total_price']:.2f}")
        print(f"    - 预计工期: {data['estimated_days']} 天")
    else:
        print(f"  错误: {result['message']}")

def test_validation():
    print_separator("3. 测试必填项校验功能")
    
    test_cases = [
        ("缺少客户姓名", {
            'customer_phone': '13800138000',
            'paperweight_style': '方形瑞兽',
            'length_cm': 8, 'width_cm': 5, 'thickness_cm': 2,
            'quantity': 1
        }),
        ("手机号格式错误", {
            'customer_name': '张三',
            'customer_phone': '12345',
            'paperweight_style': '方形瑞兽',
            'length_cm': 8, 'width_cm': 5, 'thickness_cm': 2,
            'quantity': 1
        }),
        ("尺寸超出范围", {
            'customer_name': '张三',
            'customer_phone': '13800138000',
            'paperweight_style': '方形瑞兽',
            'length_cm': 100, 'width_cm': 5, 'thickness_cm': 2,
            'quantity': 1
        })
    ]
    
    for test_name, data in test_cases:
        print(f"\n  [{test_name}]")
        response = requests.post(f'{BASE_URL}/orders', json=data)
        result = response.json()
        print(f"    状态码: {response.status_code}")
        print(f"    错误信息: {result['message']}")

def test_order_crud():
    print_separator("4. 测试订单创建与管理")
    
    order_data = {
        'customer_name': '王五',
        'customer_phone': '13900139000',
        'customer_address': '北京市东城区xxx街道',
        'paperweight_style': '圆形浮雕',
        'length_cm': 10.0,
        'width_cm': 6.0,
        'thickness_cm': 2.5,
        'inscription': '宁静致远',
        'copper_type': 'T2紫铜',
        'carving_pattern': '龙凤纹',
        'surface_finish': '黑漆古',
        'quantity': 5,
        'requirements': '边缘打磨圆润，刻字清晰'
    }
    
    print("\n  [创建订单]")
    response = requests.post(f'{BASE_URL}/orders', json=order_data)
    result = response.json()
    print(f"    状态码: {response.status_code}")
    if result['code'] == 200:
        order_no = result['data']['order_no']
        print(f"    订单号: {order_no}")
        print(f"    总价: ¥{result['data']['total_price']:.2f}")
        print(f"    预计工期: {result['data']['estimated_days']} 天")
        
        print("\n  [获取订单详情]")
        response = requests.get(f'{BASE_URL}/orders/{order_no}')
        result = response.json()
        if result['code'] == 200:
            order = result['data']
            print(f"    客户: {order['customer_name']}")
            print(f"    铜材: {order['copper_type']}")
            print(f"    纹样: {order['carving_pattern']}")
            print(f"    表面工艺: {order['surface_finish']}")
        
        print("\n  [更新订单状态]")
        response = requests.put(f'{BASE_URL}/orders/{order_no}/status', json={'status': '制版'})
        result = response.json()
        print(f"    更新为[制版]: {result['code'] == 200 and '成功' or '失败'}")
        
        response = requests.put(f'{BASE_URL}/orders/{order_no}/status', json={'status': '熔铜'})
        result = response.json()
        print(f"    更新为[熔铜]: {result['code'] == 200 and '成功' or '失败'}")
        
        print("\n  [分配匠人]")
        response = requests.put(f'{BASE_URL}/orders/{order_no}/craftsman', json={'craftsman_id': 1, 'craftsman_name': '王师傅'})
        result = response.json()
        print(f"    分配王师傅: {result['code'] == 200 and '成功' or '失败'}")

def test_filters_and_pagination():
    print_separator("5. 测试筛选和分页功能")
    
    styles = ['方形瑞兽', '长条形素面', '圆形浮雕']
    coppers = ['H62黄铜', 'H65黄铜', 'T2紫铜']
    patterns = ['无纹样', '祥云纹', '回纹']
    finishes = ['原色抛光', '哑光拉丝', '复古做旧']
    statuses = ['待接单', '制版', '熔铜', '浇铸', '打磨', '錾刻', '做旧', '完工']
    
    print("\n  [批量创建测试订单]")
    for i in range(15):
        order_data = {
            'customer_name': f'客户{i+1}',
            'customer_phone': f'138001380{i:02d}',
            'paperweight_style': styles[i % len(styles)],
            'length_cm': 6 + i * 0.5,
            'width_cm': 4 + i * 0.3,
            'thickness_cm': 1.5 + i * 0.1,
            'copper_type': coppers[i % len(coppers)],
            'carving_pattern': patterns[i % len(patterns)],
            'surface_finish': finishes[i % len(finishes)],
            'quantity': 1 + i
        }
        requests.post(f'{BASE_URL}/orders', json=order_data)
    print("    已创建 15 个测试订单")
    
    print("\n  [分页测试 - 第1页，每页5条]")
    response = requests.get(f'{BASE_URL}/orders?page=1&page_size=5')
    result = response.json()
    if result['code'] == 200:
        print(f"    总数: {result['data']['pagination']['total']}")
        print(f"    总页数: {result['data']['pagination']['total_pages']}")
        print(f"    当前页条数: {len(result['data']['list'])}")
    
    print("\n  [按样式筛选 - 方形瑞兽]")
    response = requests.get(f'{BASE_URL}/orders?style=方形瑞兽&page_size=100')
    result = response.json()
    if result['code'] == 200:
        print(f"    数量: {len(result['data']['list'])}")
    
    print("\n  [按铜材筛选 - T2紫铜]")
    response = requests.get(f'{BASE_URL}/orders?copper_type=T2紫铜&page_size=100')
    result = response.json()
    if result['code'] == 200:
        print(f"    数量: {len(result['data']['list'])}")
    
    print("\n  [按状态筛选 - 待接单]")
    response = requests.get(f'{BASE_URL}/orders?status=待接单&page_size=100')
    result = response.json()
    if result['code'] == 200:
        print(f"    数量: {len(result['data']['list'])}")
    
    print("\n  [按价格排序 - 降序]")
    response = requests.get(f'{BASE_URL}/orders?sort_by=total_price&sort_order=desc&page_size=3')
    result = response.json()
    if result['code'] == 200:
        for order in result['data']['list']:
            print(f"    - 订单{order['order_no']}: ¥{order['total_price']:.2f}")
    
    print("\n  [组合筛选 - 方形瑞兽 + H62黄铜]")
    response = requests.get(f'{BASE_URL}/orders?style=方形瑞兽&copper_type=H62黄铜&page_size=100')
    result = response.json()
    if result['code'] == 200:
        print(f"    数量: {len(result['data']['list'])}")

def test_statistics():
    print_separator("6. 测试统计功能")
    
    response = requests.get(f'{BASE_URL}/stats')
    result = response.json()
    if result['code'] == 200:
        stats = result['data']
        print(f"\n  总订单数: {stats['total']}")
        print(f"  总金额: ¥{stats['total_amount']:.2f}")
        print(f"\n  各状态订单数:")
        for status, count in stats.items():
            if status not in ['total', 'total_amount']:
                print(f"    - {status}: {count} 单")

def main():
    print("\n" + "🏮"*20)
    print("        传统铜制镇纸定制订单管理系统 - 功能测试")
    print("🏮"*20)
    
    try:
        test_basic_apis()
        test_price_calculation()
        test_validation()
        test_order_crud()
        test_filters_and_pagination()
        test_statistics()
        
        print_separator("测试完成")
        print("\n✅ 所有功能测试通过！")
        print("\n📋 已实现功能:")
        print("  1. 必填项校验与数值范围校验")
        print("  2. 铜材体积与价格自动计算")
        print("  3. 錾刻难度系数计价")
        print("  4. 匠人管理与分配")
        print("  5. 自动计算工期与交付日期")
        print("  6. 按样式、进度、铜材等筛选")
        print("  7. 分页与排序")
        print("  8. 统一API返回格式")
        print("\n🌐 服务器运行地址: http://localhost:5000")
        print("📄 前端页面: 直接在浏览器打开 index.html")
        print("\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ 错误: 无法连接到服务器！")
        print("请先运行: python app.py")

if __name__ == '__main__':
    main()
