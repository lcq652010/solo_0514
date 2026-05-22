import requests
import json

BASE_URL = 'http://127.0.0.1:5000/api'

def test_get_options():
    print("=== 测试获取所有标准选项 ===")
    response = requests.get(f'{BASE_URL}/options')
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"泥料类型: {result.get('clay_types', [])}")
    print(f"器型尺寸: {result.get('vessel_sizes', [])}")
    print(f"釉色种类: {result.get('glaze_types', [])}")
    print(f"纹饰风格: {result.get('decoration_styles', [])}")
    return result

def test_create_order_with_new_fields():
    print("\n=== 测试创建订单（含新字段） ===")
    data = {
        "customer_name": "李四",
        "customer_phone": "13900139000",
        "customer_address": "上海市浦东新区",
        "brush_washer_type": "海棠形笔洗",
        "size": "大号",
        "color": "青瓷",
        "design_requirements": "底部刻款",
        "quantity": 1,
        "estimated_price": 880.0,
        "remark": "加急订单",
        "clay_type": "青瓷泥",
        "vessel_size": "口径15cm - 大号笔洗",
        "glaze_type": "青瓷釉",
        "decoration_style": "缠枝莲纹"
    }
    response = requests.post(f'{BASE_URL}/orders', json=data)
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"订单号: {result.get('order_no')}")
    print(f"泥料类型: {result.get('clay_type')}")
    print(f"器型尺寸: {result.get('vessel_size')}")
    print(f"釉色种类: {result.get('glaze_type')}")
    print(f"纹饰风格: {result.get('decoration_style')}")
    return result.get('order_no')

def test_update_production_fields(order_no):
    print(f"\n=== 测试更新生产字段 {order_no} ===")
    data = {
        "clay_type": "汝瓷泥",
        "vessel_size": "口径12cm - 中号笔洗",
        "glaze_type": "汝釉",
        "decoration_style": "冰裂纹"
    }
    response = requests.put(f'{BASE_URL}/orders/{order_no}', json=data)
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"更新后泥料类型: {result.get('clay_type')}")
    print(f"更新后器型尺寸: {result.get('vessel_size')}")
    print(f"更新后釉色种类: {result.get('glaze_type')}")
    print(f"更新后纹饰风格: {result.get('decoration_style')}")

def test_get_order_detail(order_no):
    print(f"\n=== 测试获取订单详情（验证生产字段） ===")
    response = requests.get(f'{BASE_URL}/orders/{order_no}')
    print(f"状态码: {response.status_code}")
    result = response.json()
    print("\n=== 生产依据详情 ===")
    print(f"【揉泥依据】泥料类型: {result.get('clay_type')}")
    print(f"【拉坯依据】器型尺寸: {result.get('vessel_size')}")
    print(f"【施釉依据】釉色种类: {result.get('glaze_type')}")
    print(f"【绘画依据】纹饰风格: {result.get('decoration_style')}")

def test_get_orders():
    print("\n=== 测试获取所有订单 ===")
    response = requests.get(f'{BASE_URL}/orders')
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"订单总数: {len(result)}")

if __name__ == '__main__':
    try:
        test_get_options()
        order_no = test_create_order_with_new_fields()
        if order_no:
            test_update_production_fields(order_no)
            test_get_order_detail(order_no)
        test_get_orders()
        print("\n=== 所有测试完成！ ===")
    except Exception as e:
        print(f'测试出错: {e}')
        import traceback
        traceback.print_exc()
