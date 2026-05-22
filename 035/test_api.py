import requests
import json

BASE_URL = 'http://127.0.0.1:5000/api'

def print_response(title, response):
    print(f'\n=== {title} ===')
    print(f'状态码: {response.status_code}')
    try:
        data = response.json()
        print(f'响应: {json.dumps(data, ensure_ascii=False, indent=2)}')
        return data
    except:
        print(f'响应: {response.text}')
        return None

def test_validation():
    print('【1】测试数据校验功能')
    print('1.1 测试空手机号校验:')
    r = requests.post(f'{BASE_URL}/orders', json={
        'customer_name': '测试用户',
        'phone': '',
        'style': '传统',
        'size': '15cm',
        'quantity': 5
    })
    print_response('空手机号校验', r)
    print('1.2 测试无效手机号格式:')
    r = requests.post(f'{BASE_URL}/orders', json={
        'customer_name': '测试用户',
        'phone': '123456',
        'style': '传统',
        'size': '15cm',
        'quantity': 5
    })
    print_response('无效手机号', r)
    print('1.3 测试数量范围校验:')
    r = requests.post(f'{BASE_URL}/orders', json={
        'customer_name': '测试用户',
        'phone': '13800138000',
        'style': '传统',
        'size': '15cm',
        'quantity': 0
    })
    print_response('数量为0', r)
    r = requests.post(f'{BASE_URL}/orders', json={
        'customer_name': '测试用户',
        'phone': '13800138000',
        'style': '传统',
        'size': '15cm',
        'quantity': 1001
    })
    print_response('数量超出范围', r)
    print('1.4 测试规格枚举值校验:')
    r = requests.post(f'{BASE_URL}/orders', json={
        'customer_name': '测试用户',
        'phone': '13800138000',
        'style': '传统',
        'size': '15cm',
        'quantity': 10,
        'bamboo_type': '不存在的竹子'
    })
    print_response('无效竹材种类', r)

def test_pricing():
    print('\n\n【2】测试自动计价功能')
    print('2.1 单独调用计价接口:')
    r = requests.post(f'{BASE_URL}/price/calculate', json={
        'bamboo_type': '紫竹',
        'size_spec': '20cm × 10cm（特大）',
        'strip_thickness': '0.3mm（极细）',
        'weaving_pattern': '梅花纹',
        'quantity': 10
    })
    print_response('价格计算', r)
    print('\n2.2 创建订单时自动计价:')
    r = requests.post(f'{BASE_URL}/orders', json={
        'customer_name': '王五',
        'phone': '13900139000',
        'email': 'wangwu@example.com',
        'address': '杭州市西湖区',
        'style': '传统中式',
        'size': '15cm × 8cm',
        'quantity': 5,
        'bamboo_type': '紫竹',
        'size_spec': '15cm × 8cm（中号）',
        'strip_thickness': '0.5mm（细）',
        'weaving_pattern': '人字纹'
    })
    result = print_response('创建订单(含计价)', r)
    if result and result.get('success'):
        order_no = result['data']['order_no']
        print(f'订单号: {order_no}')
        print(f'单价: {result["data"]["unit_price"]} 元')
        print(f'总价: {result["data"]["total_price"]} 元')
        return order_no
    return None

def test_craftsman_and_lead_time():
    print('\n\n【3】测试匠人绑定与工期计算')
    print('3.1 获取匠人列表:')
    r = requests.get(f'{BASE_URL}/craftsmen')
    print_response('匠人列表', r)
    print('\n3.2 创建订单并绑定匠人:')
    r = requests.post(f'{BASE_URL}/orders', json={
        'customer_name': '赵六',
        'phone': '13700137000',
        'style': '传统中式',
        'size': '18cm × 9cm',
        'quantity': 20,
        'bamboo_type': '毛竹',
        'size_spec': '18cm × 9cm（大号）',
        'strip_thickness': '1.0mm（中）',
        'weaving_pattern': '回字纹',
        'craftsman_id': 1
    })
    result = print_response('绑定匠人创建订单', r)
    if result and result.get('success'):
        order_no = result['data']['order_no']
        print(f'订单号: {order_no}')
        print(f'匠人: {result["data"]["craftsman_name"]}')
        print(f'预计交付日期: {result["data"]["estimated_delivery"]}')
        return order_no
    return None

def test_filter_and_pagination(order_no1, order_no2):
    print('\n\n【4】测试筛选与分页排序')
    print('4.1 创建更多测试订单:')
    for i in range(15):
        requests.post(f'{BASE_URL}/orders', json={
            'customer_name': f'测试用户{i+1}',
            'phone': f'138{i:08d}',
            'style': '传统',
            'size': '15cm',
            'quantity': i + 1,
            'bamboo_type': '毛竹',
            'weaving_pattern': '人字纹' if i < 8 else '回字纹',
            'craftsman_id': 2
        })
    print('已创建15个测试订单')
    print('\n4.2 按编织纹样筛选:')
    r = requests.get(f'{BASE_URL}/orders', params={
        'weaving_pattern': '回字纹'
    })
    print_response('按纹样筛选', r)
    print('\n4.3 按状态筛选:')
    r = requests.get(f'{BASE_URL}/orders', params={'status': '待接单'})
    print_response('按状态筛选', r)
    print('\n4.4 测试分页功能 (第1页，每页5条):')
    r = requests.get(f'{BASE_URL}/orders', params={'page': 1, 'page_size': 5})
    result = print_response('分页查询', r)
    if result and result.get('success'):
        pagination = result['data']['pagination']
        print(f'当前第 {pagination["page"]} 页，共 {pagination["total_pages"]} 页')
        print(f'总记录数: {pagination["total"]}')
    print('\n4.5 按价格降序排序:')
    r = requests.get(f'{BASE_URL}/orders', params={
        'sort_by': 'total_price',
        'sort_order': 'desc',
        'page_size': 5
    })
    print_response('按价格排序', r)
    print('\n4.6 更新订单状态用于测试:')
    r = requests.put(f'{BASE_URL}/orders/{order_no1}/status', json={'status': '完工'})
    print_response('更新订单状态', r)

def test_unified_response():
    print('\n\n【5】测试统一响应格式')
    print('5.1 成功响应格式:')
    r = requests.get(f'{BASE_URL}/statuses')
    result = print_response('成功响应', r)
    if result:
        print(f'响应包含字段: {list(result.keys())}')
        print(f'code: {result.get("code")}')
        print(f'success: {result.get("success")}')
        print(f'message: {result.get("message")}')
        print(f'timestamp: {result.get("timestamp")}')
    print('\n5.2 错误响应格式:')
    r = requests.get(f'{BASE_URL}/orders/9999999999')
    result = print_response('错误响应', r)
    if result:
        print(f'code: {result.get("code")}')
        print(f'success: {result.get("success")}')
        print(f'message: {result.get("message")}')

def test_enhanced_stats():
    print('\n\n【6】测试增强统计功能')
    r = requests.get(f'{BASE_URL}/stats')
    result = print_response('统计信息', r)
    if result and result.get('success'):
        data = result['data']
        print(f'总订单数: {data["total_orders"]}')
        print(f'总营收: {data["total_revenue"]} 元')
        print(f'按纹样统计: {data["by_pattern"]}')
        print(f'即将交付（未来7天）: {len(data["upcoming_deliveries"])} 个日期')

def main():
    print('=' * 60)
    print('传统竹编茶则定制订单管理系统 v2.0 全面功能测试')
    print('=' * 60)
    test_validation()
    order_no1 = test_pricing()
    order_no2 = test_craftsman_and_lead_time()
    test_filter_and_pagination(order_no1, order_no2)
    test_unified_response()
    test_enhanced_stats()
    print('\n\n' + '=' * 60)
    print('所有功能测试完成！')
    print('=' * 60)

if __name__ == '__main__':
    main()
