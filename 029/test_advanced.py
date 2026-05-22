import requests
import json

BASE_URL = 'http://localhost:5000/api'

def print_response(title, response):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(f"状态码: {response.status_code}")
    if response.headers.get('content-type', '').startswith('application/json'):
        data = response.json()
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return data
    else:
        print(response.text)
    return None

def test_unified_response_format():
    print("\n【测试1】统一接口返回格式")
    response = requests.get(f'{BASE_URL}/options')
    data = print_response("获取选项列表", response)
    if data and 'success' in data and 'code' in data and 'message' in data and 'data' in data:
        print("✓ 返回格式正确，包含 success, code, message, data")
    else:
        print("✗ 返回格式不正确")

def test_validation():
    print("\n【测试2】必填校验与数值规范")
    invalid_order = {
        "customer_name": "测试用户",
        "customer_phone": "123456",
        "pendant_type": "观音",
        "material": "翡翠",
        "design_description": "测试",
        "pendant_length": -5
    }
    response = requests.post(f'{BASE_URL}/orders', json=invalid_order)
    data = print_response("测试无效数据验证", response)
    if data and not data.get('success') and 'errors' in data:
        print("✓ 验证功能正常，正确返回错误信息")

def test_auto_price_calculation():
    print("\n【测试3】自动计价功能")
    price_data = {
        "material": "羊脂玉",
        "carving_style": "圆雕",
        "carving_difficulty": "大师级",
        "weight": 20
    }
    response = requests.post(f'{BASE_URL}/price/calculate', json=price_data)
    data = print_response("价格计算测试", response)
    if data and data.get('success'):
        price = data['data']['calculated_price']
        print(f"✓ 自动计算价格成功: {price} 元")
        print(f"  基准价格: {data['data']['price_detail']['base_price']}")
        print(f"  样式系数: {data['data']['price_detail']['style_multiplier']}")
        print(f"  难度系数: {data['data']['price_detail']['difficulty_multiplier']}")

def test_craftsman_management():
    print("\n【测试4】匠人管理功能")
    response = requests.get(f'{BASE_URL}/craftsmen')
    data = print_response("获取匠人列表", response)
    if data and data.get('success'):
        craftsmen = data['data']
        print(f"✓ 获取到 {len(craftsmen)} 个匠人")
        for cm in craftsmen:
            print(f"  - {cm['name']} ({cm['skill_level']}) 专长: {cm['specialty']}")
        return craftsmen
    return []

def test_order_with_advanced_features(craftsmen):
    print("\n【测试5】创建带高级功能的订单")
    order_data = {
        "customer_name": "王五",
        "customer_phone": "13900139999",
        "customer_address": "杭州市西湖区某某路888号",
        "pendant_type": "龙凤呈祥",
        "material": "和田玉",
        "material_type": "籽料",
        "material_detail": "一级白，无纹裂，油润度好",
        "pendant_length": 6.5,
        "pendant_width": 4.0,
        "pendant_thickness": 1.2,
        "pendant_weight": 35,
        "carving_pattern": "龙凤",
        "carving_style": "透雕",
        "carving_depth": "深雕",
        "carving_details": "正面龙凤呈祥，背面祥云如意，边缘滚边处理",
        "carving_difficulty": "复杂",
        "polishing_level": "高光",
        "polishing_details": "整体高光，细节处亚光处理",
        "hole_position": "顶部正中",
        "hole_size": "3mm",
        "hole_count": 1,
        "design_description": "传统龙凤挂坠，寓意吉祥如意",
        "special_requirements": "配高档红木盒子，出具鉴定证书",
        "estimated_price": 2800
    }
    response = requests.post(f'{BASE_URL}/orders', json=order_data)
    data = print_response("创建高级订单", response)
    if data and data.get('success'):
        order_no = data['data']['order_no']
        auto_price = data['data']['auto_calculated_price']
        print(f"✓ 订单创建成功，编号: {order_no}")
        print(f"✓ 自动计算价格: {auto_price} 元")
        return order_no
    return None

def test_assign_craftsman(order_no, craftsmen):
    print("\n【测试6】绑定匠人到订单")
    if craftsmen:
        assign_data = {"craftsman_id": craftsmen[0]['id']}
        response = requests.put(f'{BASE_URL}/orders/{order_no}/assign', json=assign_data)
        data = print_response(f"分配匠人 {craftsmen[0]['name']}", response)
        if data and data.get('success'):
            print(f"✓ 匠人分配成功: {craftsmen[0]['name']}")

def test_order_filter_pagination():
    print("\n【测试7】筛选、分页、排序功能")
    params = {
        "material": "和田玉",
        "carving_style": "透雕",
        "carving_difficulty": "复杂",
        "page": 1,
        "page_size": 5,
        "sort_by": "created_at",
        "sort_order": "desc"
    }
    response = requests.get(f'{BASE_URL}/orders', params=params)
    data = print_response("带筛选分页的订单列表", response)
    if data and data.get('success'):
        pagination = data['data']['pagination']
        print(f"✓ 第 {pagination['page']} 页，共 {pagination['total']} 条记录，{pagination['total_pages']} 页")

def test_order_status_flow(order_no):
    print("\n【测试8】订单状态流转")
    statuses = ['选料', '切料', '粗雕', '细雕', '抛光', '打孔', '完工']
    for status in statuses:
        response = requests.put(f'{BASE_URL}/orders/{order_no}/status', json={"status": status})
        if response.status_code == 200:
            print(f"✓ 状态更新为: {status}")

def test_recalculate_price(order_no):
    print("\n【测试9】重新计算订单价格")
    response = requests.post(f'{BASE_URL}/orders/{order_no}/recalculate-price')
    data = print_response("重新计算价格", response)
    if data and data.get('success'):
        print(f"✓ 价格重新计算成功: {data['data']['auto_calculated_price']} 元")

def test_get_order_details(order_no):
    print("\n【测试10】获取订单完整详情")
    response = requests.get(f'{BASE_URL}/orders/{order_no}')
    data = print_response("订单完整详情", response)
    if data and data.get('success'):
        order = data['data']
        print("\n--- 订单摘要 ---")
        print(f"订单号: {order['order_no']}")
        print(f"客户: {order['customer_name']} ({order['customer_phone']})")
        print(f"材质: {order['material']} - {order['material_type']}")
        print(f"尺寸: {order['pendant_length']}x{order['pendant_width']}x{order['pendant_thickness']} cm")
        print(f"重量: {order['pendant_weight']} g")
        print(f"雕刻: {order['carving_pattern']} - {order['carving_style']} ({order['carving_difficulty']})")
        print(f"抛光: {order['polishing_level']}")
        print(f"打孔: {order['hole_position']} - {order['hole_count']} 个")
        print(f"匠人: {order.get('craftsman_name', '未分配')}")
        print(f"工期: 截止 {order['deadline']}")
        print(f"价格: 自动 {order['auto_calculated_price']} 元 / 预估 {order['estimated_price']} 元")
        print(f"状态: {order['status']}")

if __name__ == '__main__':
    print("="*60)
    print("  玉雕挂坠订单管理系统 - 高级功能测试")
    print("="*60)
    
    try:
        test_unified_response_format()
        test_validation()
        test_auto_price_calculation()
        craftsmen = test_craftsman_management()
        order_no = test_order_with_advanced_features(craftsmen)
        
        if order_no:
            test_assign_craftsman(order_no, craftsmen)
            test_order_status_flow(order_no)
            test_recalculate_price(order_no)
            test_get_order_details(order_no)
        
        test_order_filter_pagination()
        
        print("\n" + "="*60)
        print("  所有测试完成！")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到服务器，请先运行 python app.py 启动服务")
    except Exception as e:
        print(f"测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()