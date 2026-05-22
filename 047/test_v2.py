import requests
import json
from datetime import datetime, timedelta

BASE_URL = 'http://127.0.0.1:5000/api'

def test_calculate_price():
    print("=" * 50)
    print("测试 1: 自动计价功能")
    print("=" * 50)
    
    test_cases = [
        {'vessel_size': '口径10cm - 标准笔洗', 'clay_type': '白瓷泥', 'decoration_style': '素面无纹', 'quantity': 1},
        {'vessel_size': '口径15cm - 大号笔洗', 'clay_type': '汝瓷泥', 'decoration_style': '山水纹饰', 'quantity': 2},
        {'vessel_size': '口径12cm - 中号笔洗', 'clay_type': '紫砂泥', 'decoration_style': '龙凤纹饰', 'quantity': 3},
    ]
    
    for i, case in enumerate(test_cases, 1):
        response = requests.post(f'{BASE_URL}/orders/calculate-price', json=case)
        result = response.json()
        print(f"\n测试案例 {i}:")
        print(f"  规格: {case['vessel_size']}")
        print(f"  泥料: {case['clay_type']} (系数: {result['breakdown']['clay_factor']})")
        print(f"  纹饰: {case['decoration_style']} (系数: {result['breakdown']['decoration_factor']})")
        print(f"  数量: {case['quantity']}")
        print(f"  计算价格: ¥{result['calculated_price']}")
        print(f"  预计工期: {result['estimated_work_days']} 天")

def test_validation():
    print("\n" + "=" * 50)
    print("测试 2: 必填校验与数值规范")
    print("=" * 50)
    
    test_cases = [
        {'name': '缺少必填字段', 'data': {'customer_name': '测试用户'}, 'expected_code': 400},
        {'name': '手机号格式错误', 'data': {'customer_name': '测试', 'customer_phone': '12345', 'brush_washer_type': '圆形', 'vessel_size': '口径10cm - 标准笔洗', 'clay_type': '白瓷泥', 'glaze_type': '白瓷釉', 'decoration_style': '素面无纹'}, 'expected_code': 400},
        {'name': '数量超出范围', 'data': {'customer_name': '测试', 'customer_phone': '13800138000', 'brush_washer_type': '圆形', 'vessel_size': '口径10cm - 标准笔洗', 'clay_type': '白瓷泥', 'glaze_type': '白瓷釉', 'decoration_style': '素面无纹', 'quantity': 200}, 'expected_code': 400},
    ]
    
    for case in test_cases:
        response = requests.post(f'{BASE_URL}/orders', json=case['data'])
        print(f"\n{case['name']}:")
        print(f"  预期状态码: {case['expected_code']}")
        print(f"  实际状态码: {response.status_code}")
        if response.status_code == case['expected_code']:
            print(f"  ✓ 验证通过: {response.json().get('error')}")
        else:
            print(f"  ✗ 验证失败")

def test_create_order_with_craftsman():
    print("\n" + "=" * 50)
    print("测试 3: 创建订单（含匠人绑定）")
    print("=" * 50)
    
    data = {
        "customer_name": "王客户",
        "customer_phone": "13900139000",
        "customer_address": "杭州市西湖区",
        "brush_washer_type": "海棠形笔洗",
        "vessel_size": "口径12cm - 中号笔洗",
        "clay_type": "青瓷泥",
        "glaze_type": "青瓷釉",
        "decoration_style": "缠枝莲纹",
        "quantity": 2,
        "craftsman": "张师傅",
        "remark": "精品订单"
    }
    
    response = requests.post(f'{BASE_URL}/orders', json=data)
    print(f"状态码: {response.status_code}")
    if response.status_code == 201:
        order = response.json()
        print(f"\n订单创建成功:")
        print(f"  订单号: {order['order_no']}")
        print(f"  自动计价: ¥{order['estimated_price']}")
        print(f"  预计工期: {order['work_days']} 天")
        print(f"  交付日期: {order['delivery_date']}")
        print(f"  指定匠人: {order['craftsman']}")
        print(f"  泥料类型: {order['clay_type']}")
        print(f"  纹饰风格: {order['decoration_style']}")
        return order['order_no']
    else:
        print(f"错误: {response.json()}")
        return None

def test_filter_orders():
    print("\n" + "=" * 50)
    print("测试 4: 多维度筛选功能")
    print("=" * 50)
    
    filters = [
        {'name': '按纹饰风格筛选', 'params': {'decoration_style': '缠枝莲纹'}},
        {'name': '按泥料类型筛选', 'params': {'clay_type': '青瓷泥'}},
        {'name': '按匠人筛选', 'params': {'craftsman': '张师傅'}},
        {'name': '按状态筛选', 'params': {'status': '待接单'}},
        {'name': '按交付日期范围筛选', 'params': {'delivery_date_from': datetime.now().strftime('%Y-%m-%d'), 'delivery_date_to': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')}},
        {'name': '组合筛选', 'params': {'status': '待接单', 'clay_type': '青瓷泥', 'decoration_style': '缠枝莲纹'}},
    ]
    
    for f in filters:
        response = requests.get(f'{BASE_URL}/orders', params=f['params'])
        result = response.json()
        print(f"\n{f['name']}:")
        print(f"  筛选条件: {f['params']}")
        print(f"  匹配订单数: {result['pagination']['total']}")

def test_pagination_sorting():
    print("\n" + "=" * 50)
    print("测试 5: 分页与排序功能")
    print("=" * 50)
    
    test_cases = [
        {'name': '第1页，每页5条，按创建时间降序', 'params': {'page': 1, 'per_page': 5, 'sort_by': 'created_at', 'sort_order': 'DESC'}},
        {'name': '按价格升序排序', 'params': {'page': 1, 'per_page': 10, 'sort_by': 'estimated_price', 'sort_order': 'ASC'}},
        {'name': '按交付日期降序排序', 'params': {'page': 1, 'per_page': 10, 'sort_by': 'delivery_date', 'sort_order': 'DESC'}},
    ]
    
    for case in test_cases:
        response = requests.get(f'{BASE_URL}/orders', params=case['params'])
        result = response.json()
        print(f"\n{case['name']}:")
        print(f"  当前页: {result['pagination']['page']}")
        print(f"  每页条数: {result['pagination']['per_page']}")
        print(f"  总条数: {result['pagination']['total']}")
        print(f"  总页数: {result['pagination']['total_pages']}")
        print(f"  当前页订单数: {len(result['data'])}")
        if result['data']:
            print(f"  本页订单号: {[o['order_no'] for o in result['data'][:3]]}...")

def test_craftsman_list():
    print("\n" + "=" * 50)
    print("测试 6: 获取匠人列表")
    print("=" * 50)
    
    response = requests.get(f'{BASE_URL}/craftsmen')
    craftsmen = response.json()
    print(f"可用匠人列表: {craftsmen}")

def test_enhanced_stats():
    print("\n" + "=" * 50)
    print("测试 7: 增强统计功能")
    print("=" * 50)
    
    response = requests.get(f'{BASE_URL}/stats')
    stats = response.json()
    print(f"总订单数: {stats['total']}")
    print(f"待交付订单: {stats['pending_delivery']}")
    print(f"活跃匠人: {stats['active_craftsmen']}")
    print(f"总营收: ¥{stats['total_revenue']}")
    print("\n各状态订单数:")
    for status in ['待接单', '揉泥', '拉坯', '利坯', '施釉', '绘画', '烧制', '完工']:
        print(f"  {status}: {stats.get(status, 0)}")

if __name__ == '__main__':
    try:
        test_calculate_price()
        test_validation()
        order_no = test_create_order_with_craftsman()
        test_craftsman_list()
        test_filter_orders()
        test_pagination_sorting()
        test_enhanced_stats()
        
        print("\n" + "=" * 50)
        print("所有测试完成！")
        print("=" * 50)
    except Exception as e:
        print(f"\n测试出错: {e}")
        import traceback
        traceback.print_exc()
