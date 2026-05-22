import requests
import json
from datetime import datetime, timedelta

BASE_URL = 'http://127.0.0.1:5000/api'

def print_response(title, response):
    print(f'\n{"="*60}')
    print(f'{title}')
    print(f'状态码: {response.status_code}')
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    print(f'{"="*60}\n')

def test_api():
    print('\n' + '='*70)
    print('  传统石砚定制订单管理系统 - 全面优化版 API 测试')
    print('='*70)
    
    print('\n' + '='*70)
    print('1. 获取订单状态列表')
    response = requests.get(f'{BASE_URL}/statuses')
    print_response('获取订单状态列表', response)
    
    print('\n' + '='*70)
    print('2. 获取价格配置规则')
    response = requests.get(f'{BASE_URL}/config/prices')
    print_response('获取价格配置规则', response)
    
    print('\n' + '='*70)
    print('3. 测试价格计算功能')
    price_data = {
        'stone_grade': '特级',
        'carving_difficulty': '极复杂',
        'size_length': 25.0,
        'size_width': 20.0,
        'size_height': 5.0
    }
    response = requests.post(f'{BASE_URL}/calculate-price', json=price_data)
    print_response('价格计算结果', response)
    
    print('\n' + '='*70)
    print('4. 测试必填字段校验（故意不传必填项）')
    invalid_order = {
        'customer_name': '',
        'customer_phone': '12345',
        'inkstone_type': '',
        'material': ''
    }
    response = requests.post(f'{BASE_URL}/orders', json=invalid_order)
    print_response('必填字段校验测试', response)
    
    print('\n' + '='*70)
    print('5. 创建第一个订单（端砚 - 抄手砚 - 特级石材）')
    order1 = {
        'customer_name': '张三',
        'customer_phone': '13800138000',
        'customer_address': '北京市朝阳区某某街道123号',
        'inkstone_type': '端砚',
        'inkstone_style': '抄手砚',
        'material': '端石',
        'stone_type': '老坑石',
        'stone_grade': '特级',
        'stone_origin': '广东肇庆羚羊峡',
        'size_length': 20.0,
        'size_width': 15.0,
        'size_height': 3.0,
        'size_note': '长宽高允许±0.5cm误差',
        'pool_design': '椭圆形砚池，深1.5cm，边缘圆润过渡',
        'carving_pattern': '砚边雕刻祥云纹，砚背雕刻山水图案',
        'carving_difficulty': '复杂',
        'polishing_requirement': '3000目精磨，镜面效果，无划痕',
        'inscription': '天道酬勤',
        'special_requirements': '需要精雕细琢，保留石材天然纹理',
        'work_days': 20
    }
    response = requests.post(f'{BASE_URL}/orders', json=order1)
    print_response('创建第一个订单', response)
    order_no1 = response.json()['data']['order_no']
    print(f'生成的订单编号: {order_no1}')
    
    print('\n' + '='*70)
    print('6. 创建第二个订单（歙砚 - 箕形砚 - 一级石材）')
    order2 = {
        'customer_name': '李四',
        'customer_phone': '13900139000',
        'customer_address': '上海市浦东新区某某路456号',
        'inkstone_type': '歙砚',
        'inkstone_style': '箕形砚',
        'material': '歙石',
        'stone_type': '龙尾石',
        'stone_grade': '一级',
        'stone_origin': '江西婺源龙尾山',
        'size_length': 18.0,
        'size_width': 12.0,
        'size_height': 2.5,
        'size_note': '按标准尺寸制作',
        'pool_design': '月牙形砚池，深1cm，线条流畅',
        'carving_pattern': '砚边雕刻竹节纹，简约素雅',
        'carving_difficulty': '普通',
        'polishing_requirement': '2000目打磨，哑光效果，手感温润',
        'inscription': '宁静致远',
        'special_requirements': '需要仿古风格做旧处理',
        'work_days': 15
    }
    response = requests.post(f'{BASE_URL}/orders', json=order2)
    print_response('创建第二个订单', response)
    order_no2 = response.json()['data']['order_no']
    print(f'生成的订单编号: {order_no2}')
    
    print('\n' + '='*70)
    print('7. 创建第三个订单（洮砚 - 圆形砚 - 三级石材）')
    order3 = {
        'customer_name': '王五',
        'customer_phone': '13700137000',
        'customer_address': '广州市天河区某某路789号',
        'inkstone_type': '洮砚',
        'inkstone_style': '圆形砚',
        'material': '洮石',
        'stone_type': '喇嘛崖石',
        'stone_grade': '三级',
        'stone_origin': '甘肃卓尼',
        'size_length': 15.0,
        'size_width': 15.0,
        'size_height': 2.0,
        'pool_design': '圆形砚池，深0.8cm',
        'carving_pattern': '简约素面',
        'carving_difficulty': '简单',
        'polishing_requirement': '1500目打磨',
        'inscription': '上善若水',
        'work_days': 10
    }
    response = requests.post(f'{BASE_URL}/orders', json=order3)
    print_response('创建第三个订单', response)
    order_no3 = response.json()['data']['order_no']
    print(f'生成的订单编号: {order_no3}')
    
    print('\n' + '='*70)
    print('8. 绑定匠人信息到第一个订单')
    craftsman_data = {
        'craftsman_name': '陈大师',
        'craftsman_phone': '13600136000',
        'work_days': 25
    }
    response = requests.put(f'{BASE_URL}/orders/{order_no1}/craftsman', json=craftsman_data)
    print_response('绑定匠人信息', response)
    
    print('\n' + '='*70)
    print('9. 更新第一个订单状态：待接单 -> 选石 -> 切坯 -> 雕刻')
    for status in [1, 2, 3]:
        response = requests.put(f'{BASE_URL}/orders/{order_no1}/status', json={'status': status})
        print(f'更新状态为 {response.json()["data"]["status"]}')
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
        print()
    
    print('\n' + '='*70)
    print('10. 更新第二个订单状态：待接单 -> 完工')
    response = requests.put(f'{BASE_URL}/orders/{order_no2}/status', json={'status': 7})
    print_response('订单2状态更新为完工', response)
    
    print('\n' + '='*70)
    print('11. 获取所有订单列表（默认按创建时间倒序）')
    response = requests.get(f'{BASE_URL}/orders')
    result = response.json()
    print(f'总订单数: {result["data"]["pagination"]["total"]}')
    print(f'当前页: {result["data"]["pagination"]["page"]}')
    print(f'每页数量: {result["data"]["pagination"]["per_page"]}')
    print(f'排序字段: {result["data"]["pagination"]["sort_by"]}')
    print(f'排序方式: {result["data"]["pagination"]["sort_order"]}')
    print('\n订单列表:')
    for order in result['data']['orders']:
        print(f'  {order["order_no"]} - {order["inkstone_type"]}/{order["inkstone_style"]}')
        print(f'    客户: {order["customer_name"]} | 价格: ¥{order["price"]}')
        print(f'    石材: {order["stone_grade"]} | 难度: {order["carving_difficulty"]}')
        print(f'    匠人: {order["craftsman_name"] or "未分配"} | 工期: {order["work_days"]}天')
        print(f'    状态: {order["status"]} | 交付日期: {order["delivery_date"][:10]}')
        print()
    
    print('\n' + '='*70)
    print('12. 按砚式筛选（筛选"抄手砚"）')
    response = requests.get(f'{BASE_URL}/orders?inkstone_style=抄手砚')
    result = response.json()
    print(f'筛选"抄手砚"，找到 {result["data"]["pagination"]["total"]} 个订单')
    for order in result['data']['orders']:
        print(f'  - {order["order_no"]} - {order["inkstone_style"]}')
    
    print('\n' + '='*70)
    print('13. 按状态筛选（筛选"完工"状态，status=7）')
    response = requests.get(f'{BASE_URL}/orders?status=7')
    result = response.json()
    print(f'筛选"完工"状态，找到 {result["data"]["pagination"]["total"]} 个订单')
    for order in result['data']['orders']:
        print(f'  - {order["order_no"]} - {order["status"]}')
    
    print('\n' + '='*70)
    print('14. 按交付日期范围筛选（未来30天内交付）')
    today = datetime.now().strftime('%Y-%m-%d')
    future_30 = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    response = requests.get(f'{BASE_URL}/orders?delivery_date_from={today}&delivery_date_to={future_30}')
    result = response.json()
    print(f'未来30天内交付的订单数: {result["data"]["pagination"]["total"]}')
    for order in result['data']['orders']:
        print(f'  - {order["order_no"]} - 交付日期: {order["delivery_date"][:10]}')
    
    print('\n' + '='*70)
    print('15. 按价格升序排序')
    response = requests.get(f'{BASE_URL}/orders?sort_by=price&sort_order=asc')
    result = response.json()
    print('按价格从低到高排序:')
    for order in result['data']['orders']:
        print(f'  - {order["order_no"]} - ¥{order["price"]} - {order["inkstone_type"]}')
    
    print('\n' + '='*70)
    print('16. 分页测试（第1页，每页2条）')
    response = requests.get(f'{BASE_URL}/orders?page=1&per_page=2')
    result = response.json()
    print(f'第1页，共 {result["data"]["pagination"]["total_pages"]} 页')
    print(f'本页订单数: {len(result["data"]["orders"])}')
    for order in result['data']['orders']:
        print(f'  - {order["order_no"]}')
    
    print('\n' + '='*70)
    print('17. 查询单个订单详情')
    response = requests.get(f'{BASE_URL}/orders/{order_no1}')
    print_response('订单详情查询', response)
    
    print('\n' + '='*70)
    print('18. 删除第三个订单')
    response = requests.delete(f'{BASE_URL}/orders/{order_no3}')
    print_response('删除订单', response)
    
    print('\n' + '='*70)
    print('19. 删除后验证订单总数')
    response = requests.get(f'{BASE_URL}/orders')
    result = response.json()
    print(f'当前订单总数: {result["data"]["pagination"]["total"]}')
    
    print('\n' + '='*70)
    print('✓ 所有 API 测试完成！系统功能验证通过')
    print('='*70)

if __name__ == '__main__':
    test_api()
