import requests
import json

BASE_URL = 'http://localhost:5000/api'

def test_get_options():
    print("=== 测试获取所有选项 ===")
    response = requests.get(f'{BASE_URL}/options')
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        options = response.json()
        print(f"雕刻纹样选项: {options.get('carving_patterns', [])}")
        print(f"雕刻样式选项: {options.get('carving_styles', [])}")
        print(f"打孔位置选项: {options.get('hole_positions', [])}")
        print(f"抛光等级选项: {options.get('polishing_levels', [])}")
        print(f"材质类型选项: {options.get('material_types', [])}")

def test_create_detailed_order():
    print("\n=== 测试创建详细订单 ===")
    order_data = {
        "customer_name": "李四",
        "customer_phone": "13900139000",
        "customer_address": "上海市浦东新区某某路456号",
        "pendant_type": "佛牌",
        "material": "翡翠",
        "material_type": "冰种",
        "material_detail": "飘绿，水头足，无纹裂",
        "size": "5cm x 3.5cm",
        "pendant_length": 5.0,
        "pendant_width": 3.5,
        "pendant_thickness": 0.8,
        "pendant_weight": 28.5,
        "carving_pattern": "佛",
        "carving_style": "浮雕",
        "carving_depth": "中等深度",
        "carving_details": "弥勒佛笑口常开，大肚能容，底部雕刻祥云纹",
        "polishing_level": "高光",
        "polishing_details": "正面镜面抛光，背面亚光处理",
        "hole_position": "顶部正中",
        "hole_size": "2mm",
        "hole_count": 1,
        "design_description": "弥勒佛挂坠，寓意平安吉祥",
        "special_requirements": "配证书，配高档礼盒",
        "estimated_price": 2800.0
    }
    response = requests.post(f'{BASE_URL}/orders', json=order_data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    if response.status_code == 201:
        return response.json()['order_no']
    return None

def test_get_order_details(order_no):
    print(f"\n=== 测试获取订单详情 {order_no} ===")
    response = requests.get(f'{BASE_URL}/orders/{order_no}')
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        order = response.json()
        print("\n--- 材质信息 ---")
        print(f"材质: {order.get('material')}")
        print(f"材质类型: {order.get('material_type')}")
        print(f"材质详情: {order.get('material_detail')}")
        print("\n--- 尺寸信息 ---")
        print(f"长度: {order.get('pendant_length')} cm")
        print(f"宽度: {order.get('pendant_width')} cm")
        print(f"厚度: {order.get('pendant_thickness')} cm")
        print(f"重量: {order.get('pendant_weight')} g")
        print("\n--- 雕刻信息 ---")
        print(f"雕刻纹样: {order.get('carving_pattern')}")
        print(f"雕刻样式: {order.get('carving_style')}")
        print(f"雕刻深度: {order.get('carving_depth')}")
        print(f"雕刻详情: {order.get('carving_details')}")
        print("\n--- 抛光信息 ---")
        print(f"抛光等级: {order.get('polishing_level')}")
        print(f"抛光详情: {order.get('polishing_details')}")
        print("\n--- 打孔信息 ---")
        print(f"打孔位置: {order.get('hole_position')}")
        print(f"打孔尺寸: {order.get('hole_size')}")
        print(f"打孔数量: {order.get('hole_count')}")

def test_update_order_details(order_no):
    print(f"\n=== 测试更新订单详情 {order_no} ===")
    update_data = {
        "carving_depth": "加深雕刻",
        "polishing_level": "镜面抛光",
        "hole_count": 2,
        "estimated_price": 3200.0
    }
    response = requests.put(f'{BASE_URL}/orders/{order_no}', json=update_data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")

def test_update_carving_status(order_no):
    print(f"\n=== 测试更新雕刻状态 {order_no} ===")
    statuses = ['粗雕', '细雕', '抛光', '打孔', '完工']
    for status in statuses:
        response = requests.put(f'{BASE_URL}/orders/{order_no}/status', json={"status": status})
        print(f"更新为 '{status}': {response.status_code} - {response.json().get('message', '')}")

if __name__ == '__main__':
    try:
        test_get_options()
        order_no = test_create_detailed_order()
        if order_no:
            test_get_order_details(order_no)
            test_update_order_details(order_no)
            print("\n=== 更新后订单详情 ===")
            test_get_order_details(order_no)
            test_update_carving_status(order_no)
        print("\n=== 所有测试完成 ===")
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到服务器，请先运行 python app.py 启动服务")