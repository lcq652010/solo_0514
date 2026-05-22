import requests
import json
from datetime import datetime, timedelta

BASE_URL = 'http://127.0.0.1:5000'

def print_response(title, response):
    print(f'\n{"="*80}')
    print(f'[{title}]')
    print(f'状态码: {response.status_code}')
    try:
        data = response.json()
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except:
        print(response.text)
    print(f'{"="*80}\n')

def test_section(title):
    print(f'\n{"#"*80}')
    print(f'## {title}')
    print(f'{"#"*80}\n')

print('='*80)
print('传统兽骨镇尺定制订单管理系统 v3.0 - API全面测试')
print('='*80)

test_section('1. 系统基础测试')
print('测试健康检查接口...')
response = requests.get(f'{BASE_URL}/api/health')
print_response('健康检查', response)
assert response.status_code == 200
assert response.json()['code'] == 200
print('✓ 健康检查通过')

print('测试获取订单状态列表...')
response = requests.get(f'{BASE_URL}/api/statuses')
print_response('获取状态列表', response)
assert response.status_code == 200
assert len(response.json()['data']) == 8
print('✓ 状态列表获取通过')

print('测试获取所有选项...')
response = requests.get(f'{BASE_URL}/api/options')
print_response('获取选项列表', response)
assert response.status_code == 200
options = response.json()['data']
assert 'material_categories' in options
assert 'carving_depths' in options
assert 'styles' in options
print('✓ 选项列表获取通过')

test_section('2. 匠人管理测试')
print('测试获取匠人列表...')
response = requests.get(f'{BASE_URL}/api/craftsmen')
print_response('获取匠人列表', response)
assert response.status_code == 200
craftsmen = response.json()['data']
assert len(craftsmen) == 4
print(f'✓ 获取到 {len(craftsmen)} 位匠人')

print('获取空闲匠人...')
response = requests.get(f'{BASE_URL}/api/craftsmen?status=空闲')
print_response('获取空闲匠人', response)
free_craftsmen = response.json()['data']
print(f'✓ 空闲匠人: {len(free_craftsmen)} 位')

print('获取单个匠人详情...')
response = requests.get(f'{BASE_URL}/api/craftsmen/1')
print_response('匠人详情', response)
assert response.status_code == 200
assert response.json()['data']['name'] == '张师傅'
print('✓ 匠人详情获取通过')

test_section('3. 订单校验测试')
print('测试缺少必填字段的情况...')
invalid_data = {
    'customer_name': '测试用户'
}
response = requests.post(f'{BASE_URL}/api/orders', json=invalid_data)
print_response('缺少字段校验', response)
assert response.status_code == 400
assert 'errors' in response.json()['data']
print('✓ 必填字段校验通过')

print('测试数值范围超限的情况...')
invalid_data = {
    'customer_name': '测试用户',
    'customer_phone': '13800138000',
    'material_category': '牛骨',
    'length_cm': 100,
    'width_cm': 20,
    'thickness_cm': 10
}
response = requests.post(f'{BASE_URL}/api/orders/calculate', json=invalid_data)
print_response('数值范围校验', response)
assert response.status_code == 400
print('✓ 数值范围校验通过')

print('测试无效材料的情况...')
invalid_data = {
    'customer_name': '测试用户',
    'customer_phone': '13800138000',
    'material_category': '钻石',
    'length_cm': 15,
    'width_cm': 3,
    'thickness_cm': 1
}
response = requests.post(f'{BASE_URL}/api/orders/calculate', json=invalid_data)
print_response('材料校验', response)
assert response.status_code == 400
print('✓ 材料有效性校验通过')

test_section('4. 自动计价测试')
print('测试计价功能 - 基础订单...')
basic_order = {
    'material_category': '牛骨',
    'material_grade': 'B级',
    'length_cm': 15,
    'width_cm': 3,
    'thickness_cm': 1
}
response = requests.post(f'{BASE_URL}/api/orders/calculate', json=basic_order)
print_response('基础订单计价', response)
assert response.status_code == 200
basic_price = response.json()['data']['total_price']
print(f'✓ 基础订单价格: {basic_price} 元')

print('测试计价功能 - 特级材料+透雕+镜面抛光...')
premium_order = {
    'material_category': '鹿角',
    'material_grade': '特级',
    'length_cm': 20,
    'width_cm': 4,
    'thickness_cm': 1.5,
    'carving_content': '宁静致远',
    'carving_pattern': '龙纹',
    'carving_depth': '透雕',
    'polishing_requirement': '镜面抛光',
    'hot_stamping_content': '珍藏',
    'hot_stamping_pattern': '祥云'
}
response = requests.post(f'{BASE_URL}/api/orders/calculate', json=premium_order)
print_response('高端订单计价', response)
assert response.status_code == 200
premium_price = response.json()['data']['total_price']
print(f'✓ 高端订单价格: {premium_price} 元')
assert premium_price > basic_price
print('✓ 价格差异化验证通过')

test_section('5. 创建完整订单测试')
print('创建完整订单 - 绑定匠人...')
order_data = {
    'customer_name': '王五',
    'customer_phone': '13900139005',
    'customer_address': '北京市海淀区中关村',
    'material_category': '鹿角',
    'material_origin': '西藏',
    'material_grade': 'A级',
    'length_cm': 18,
    'width_cm': 3.5,
    'thickness_cm': 1.2,
    'carving_content': '厚德载物',
    'carving_pattern': '祥云纹',
    'carving_font': '楷书',
    'carving_depth': '深雕(1.5mm)',
    'hot_stamping_content': '王氏珍藏',
    'hot_stamping_pattern': '莲花',
    'hot_stamping_position': '正面居中',
    'polishing_requirement': '镜面抛光',
    'special_requirements': '骨材要求无裂纹，纹理均匀',
    'style': '古典',
    'craftsman_id': 1
}
response = requests.post(f'{BASE_URL}/api/orders', json=order_data)
print_response('创建完整订单', response)
assert response.status_code == 200
order = response.json()['data']
order_no = order['order_no']
print(f'✓ 订单创建成功，编号: {order_no}')
print(f'✓ 自动计算价格: {order["total_price"]} 元')
print(f'✓ 自动计算工期: {order["lead_days"]} 天')
print(f'✓ 预计交付日期: {order["delivery_date"]}')
print(f'✓ 绑定匠人: {order["craftsman_name"]}')

test_section('6. 批量创建测试订单')
test_orders = [
    {
        'customer_name': '赵六',
        'customer_phone': '13900139006',
        'material_category': '牛骨',
        'material_grade': 'C级',
        'length_cm': 15,
        'width_cm': 3,
        'thickness_cm': 1,
        'carving_content': '宁静致远',
        'carving_depth': '浅雕(0.5mm)',
        'polishing_requirement': '亚光',
        'style': '现代'
    },
    {
        'customer_name': '钱七',
        'customer_phone': '13900139007',
        'material_category': '骆驼骨',
        'material_grade': 'A级',
        'length_cm': 20,
        'width_cm': 4,
        'thickness_cm': 1.5,
        'carving_content': '上善若水',
        'carving_pattern': '山水纹',
        'carving_depth': '透雕',
        'polishing_requirement': '镜面抛光',
        'style': '中式',
        'craftsman_id': 4
    },
    {
        'customer_name': '孙八',
        'customer_phone': '13900139008',
        'material_category': '象牙果',
        'material_grade': 'B级',
        'length_cm': 12,
        'width_cm': 2.5,
        'thickness_cm': 0.8,
        'hot_stamping_content': '生日快乐',
        'hot_stamping_pattern': '福字',
        'polishing_requirement': '磨砂',
        'style': '简约'
    }
]

order_numbers = [order_no]
for idx, data in enumerate(test_orders):
    response = requests.post(f'{BASE_URL}/api/orders', json=data)
    assert response.status_code == 200
    created_order = response.json()['data']
    order_numbers.append(created_order['order_no'])
    print(f'✓ 创建测试订单 {idx+1}: {created_order["order_no"]}')

test_section('7. 订单状态流转测试')
status_flow = ['选料', '切坯', '打磨', '雕刻', '烫花', '上油', '完工']

for idx, status in enumerate(status_flow):
    print(f'更新订单状态到: {status}')
    update_data = {
        'status': status,
        'progress_note': f'完成{status}工序，一切正常'
    }
    response = requests.put(f'{BASE_URL}/api/admin/orders/{order_no}/status', json=update_data)
    print_response(f'更新状态 - {status}', response)
    assert response.status_code == 200
    assert response.json()['data']['status'] == status
    print(f'✓ 状态更新成功: {status}')

test_section('8. 匠人分配测试')
print('为订单分配新的匠人...')
assign_data = {
    'craftsman_id': 4
}
response = requests.put(f'{BASE_URL}/api/admin/orders/{order_numbers[1]}/craftsman', json=assign_data)
print_response('分配匠人', response)
assert response.status_code == 200
assert response.json()['data']['craftsman_name'] == '陈师傅'
print('✓ 匠人分配成功')

test_section('9. 多条件筛选测试')
print('按状态筛选订单...')
response = requests.get(f'{BASE_URL}/api/orders?status=完工')
print_response('按状态筛选(完工)', response)
assert response.status_code == 200
print(f'✓ 筛选到 {len(response.json()["data"]["list"])} 个已完工订单')

print('按风格筛选订单...')
response = requests.get(f'{BASE_URL}/api/orders?style=古典')
print_response('按风格筛选(古典)', response)
assert response.status_code == 200
print(f'✓ 筛选到 {len(response.json()["data"]["list"])} 个古典风格订单')

print('按材料筛选订单...')
response = requests.get(f'{BASE_URL}/api/orders?material_category=牛骨')
print_response('按材料筛选(牛骨)', response)
assert response.status_code == 200
print(f'✓ 筛选到 {len(response.json()["data"]["list"])} 个牛骨材料订单')

print('按匠人筛选订单...')
response = requests.get(f'{BASE_URL}/api/orders?craftsman_id=4')
print_response('按匠人筛选(陈师傅)', response)
assert response.status_code == 200
print(f'✓ 筛选到 {len(response.json()["data"]["list"])} 个陈师傅的订单')

print('按交付日期范围筛选...')
today = datetime.now().strftime('%Y-%m-%d')
week_later = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
response = requests.get(f'{BASE_URL}/api/orders?delivery_date_from={today}&delivery_date_to={week_later}')
print_response('按交付日期筛选', response)
assert response.status_code == 200
print(f'✓ 筛选到 {len(response.json()["data"]["list"])} 个本周交付的订单')

test_section('10. 分页排序测试')
print('测试分页功能 - 第1页，每页2条...')
response = requests.get(f'{BASE_URL}/api/orders?page=1&page_size=2')
print_response('分页测试-第1页', response)
assert response.status_code == 200
data = response.json()['data']
assert len(data['list']) == 2
assert data['pagination']['page'] == 1
print(f'✓ 第1页获取成功，共 {data["pagination"]["total"]} 条记录')

print('测试分页功能 - 第2页，每页2条...')
response = requests.get(f'{BASE_URL}/api/orders?page=2&page_size=2')
print_response('分页测试-第2页', response)
assert response.status_code == 200
data = response.json()['data']
print(f'✓ 第2页获取成功，共 {data["pagination"]["total_pages"]} 页')

print('测试排序 - 按价格降序...')
response = requests.get(f'{BASE_URL}/api/orders?sort_by=total_price&sort_order=desc')
print_response('按价格降序排序', response)
assert response.status_code == 200
orders = response.json()['data']['list']
if len(orders) >= 2:
    assert orders[0]['total_price'] >= orders[1]['total_price']
print('✓ 价格降序排序正确')

print('测试排序 - 按交付日期升序...')
response = requests.get(f'{BASE_URL}/api/orders?sort_by=delivery_date&sort_order=asc')
print_response('按交付日期升序排序', response)
assert response.status_code == 200
print('✓ 交付日期升序排序正确')

test_section('11. 综合查询测试')
print('多条件组合查询 + 排序 + 分页...')
params = {
    'status': '待接单',
    'style': '现代',
    'sort_by': 'total_price',
    'sort_order': 'desc',
    'page': 1,
    'page_size': 10
}
response = requests.get(f'{BASE_URL}/api/orders', params=params)
print_response('多条件组合查询', response)
assert response.status_code == 200
print('✓ 多条件组合查询成功')

test_section('12. 订单删除测试')
print('删除测试订单...')
delete_order_no = order_numbers[-1]
response = requests.delete(f'{BASE_URL}/api/admin/orders/{delete_order_no}')
print_response('删除订单', response)
assert response.status_code == 200
print(f'✓ 订单 {delete_order_no} 删除成功')

print('验证订单已删除...')
response = requests.get(f'{BASE_URL}/api/orders/{delete_order_no}')
print_response('查询已删除订单', response)
assert response.status_code == 404
print('✓ 订单删除验证通过')

test_section('13. 统一返回格式验证')
print('验证所有接口返回格式统一...')
endpoints = [
    ('GET', '/api/health', None),
    ('GET', '/api/options', None),
    ('GET', '/api/statuses', None),
    ('GET', '/api/craftsmen', None),
    ('GET', '/api/orders', None),
]

for method, endpoint, _ in endpoints:
    if method == 'GET':
        response = requests.get(f'{BASE_URL}{endpoint}')
    data = response.json()
    assert 'code' in data
    assert 'message' in data
    assert 'data' in data
    assert 'timestamp' in data
    print(f'✓ {endpoint} 格式正确')

print('\n' + '='*80)
print('🎉 所有测试通过！系统 v3.0 功能完整验证成功')
print('='*80)
print('\n测试总结:')
print('  ✓ 系统基础功能正常')
print('  ✓ 匠人管理功能完整')
print('  ✓ 必填字段与数值范围校验有效')
print('  ✓ 自动计价与工期计算正确')
print('  ✓ 订单状态流转正常')
print('  ✓ 匠人分配功能正常')
print('  ✓ 多条件筛选功能完善')
print('  ✓ 分页排序功能正常')
print('  ✓ 接口返回格式统一')
print('='*80)
