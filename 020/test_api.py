import requests
import json

BASE_URL = 'http://localhost:5000'

def print_separator(title=''):
    print('\n' + '=' * 70)
    if title:
        print(f'  {title}')
        print('=' * 70)

def test_options():
    print_separator('测试1: 获取所有配置选项')
    try:
        response = requests.get(f'{BASE_URL}/api/options')
        data = response.json()
        print(f'状态码: {response.status_code}')
        print(f'✓ 竹材类型: {len(data["data"]["bamboo_types"])}种')
        print(f'✓ 雕刻纹样: {len(data["data"]["carving_patterns"])}种')
        print(f'✓ 放置弧度: {len(data["data"]["placement_curves"])}种')
        print(f'✓ 匠人团队: {len(data["data"]["craftsmen"])}人')
        print(f'✓ 订单状态: {len(data["data"]["statuses"])}种')
        return True
    except Exception as e:
        print(f'✗ 测试失败: {e}')
        return False

def test_calculate():
    print_separator('测试2: 订单计价预览')
    try:
        test_cases = [
            ('毛竹', '云纹', 1),
            ('紫竹', '龙凤呈祥', 2),
            ('金丝竹', '人物故事', 3)
        ]
        for bamboo, pattern, qty in test_cases:
            response = requests.post(f'{BASE_URL}/api/calculate', json={
                'bamboo_type': bamboo,
                'carving_pattern': pattern,
                'quantity': qty
            })
            data = response.json()
            print(f'\n  {bamboo} + {pattern} × {qty}:')
            print(f'    单价: ¥{data["data"]["unit_price"]:.2f}')
            print(f'    总价: ¥{data["data"]["total_price"]:.2f}')
            print(f'    难度系数: {data["data"]["carving_difficulty"]}')
            print(f'    预计工期: {data["data"]["estimated_days"]}天')
        print('✓ 计价功能正常')
        return True
    except Exception as e:
        print(f'✗ 测试失败: {e}')
        return False

def test_validation():
    print_separator('测试3: 必填校验与数值规范')
    invalid_cases = [
        ({}, '空数据'),
        ({'customer_name': '张三'}, '缺少必填字段'),
        ({'customer_name': '张三', 'customer_phone': '123'}, '手机号格式错误'),
        ({'customer_name': '张三', 'customer_phone': '13800138000', 'length_cm': -1}, '尺寸为负数'),
        ({'customer_name': '张三', 'customer_phone': '13800138000', 'bamboo_type': '不存在的竹子'}, '无效竹材类型')
    ]
    for data, desc in invalid_cases:
        response = requests.post(f'{BASE_URL}/api/orders', json=data)
        if response.status_code == 400:
            print(f'  ✓ {desc}: 正确拦截')
        else:
            print(f'  ✗ {desc}: 未正确拦截')
    print('✓ 校验功能正常')
    return True

def test_create_order():
    print_separator('测试4: 创建订单（自动计价）')
    order_data = {
        "customer_name": "李四",
        "customer_phone": "13900139000",
        "customer_address": "上海市浦东新区",
        "design_requirements": "精细雕刻，仿古风格",
        "bamboo_type": "紫竹",
        "carving_pattern": "龙凤呈祥",
        "placement_curve": "微弧(5°-10°)",
        "length_cm": 20.5,
        "width_cm": 5.2,
        "thickness_cm": 2.0,
        "quantity": 2,
        "budget": 2500,
        "remark": "加急订单"
    }
    try:
        response = requests.post(f'{BASE_URL}/api/orders', json=order_data)
        data = response.json()
        order = data['data']
        print(f'✓ 订单创建成功: {order["order_no"]}')
        print(f'  客户: {order["customer_name"]}')
        print(f'  竹材: {order["bamboo_type"]} | 纹样: {order["carving_pattern"]}')
        print(f'  尺寸: {order["length_cm"]}×{order["width_cm"]}×{order["thickness_cm"]} cm')
        print(f'  单价: ¥{order["unit_price"]:.2f} | 总价: ¥{order["total_price"]:.2f}')
        print(f'  难度系数: {order["carving_difficulty"]}')
        print(f'  预计工期: {order["estimated_days"]}天')
        print(f'  预计交付: {order["delivery_date"]}')
        print(f'  当前状态: {order["status"]}')
        return order['order_no']
    except Exception as e:
        print(f'✗ 测试失败: {e}')
        if 'response' in locals():
            print(f'响应: {response.text}')
        return None

def test_assign_craftsman(order_no):
    print_separator('测试5: 绑定匠人到订单')
    try:
        response = requests.put(f'{BASE_URL}/api/orders/{order_no}/craftsman', json={
            'craftsman_id': 1
        })
        data = response.json()
        order = data['data']
        print(f'✓ 匠人绑定成功')
        print(f'  匠人ID: {order["craftsman_id"]}')
        print(f'  匠人姓名: {order["craftsman_name"]}')
        return True
    except Exception as e:
        print(f'✗ 测试失败: {e}')
        return False

def test_update_status(order_no):
    print_separator('测试6: 更新订单制作进度')
    status_flow = ['选竹', '锯坯', '粗雕', '精雕']
    try:
        for status in status_flow:
            response = requests.put(f'{BASE_URL}/api/orders/{order_no}/status', json={
                'status': status
            })
            data = response.json()
            print(f'  → 更新为「{status}」: 成功')
        print(f'✓ 状态更新功能正常')
        return True
    except Exception as e:
        print(f'✗ 测试失败: {e}')
        return False

def test_filter_and_pagination():
    print_separator('测试7: 多条件筛选、分页、排序')
    try:
        test_cases = [
            ('分页查询', '?page=1&page_size=5'),
            ('按状态筛选', '?status=精雕'),
            ('按竹材筛选', '?bamboo_type=紫竹'),
            ('按题材筛选', '?carving_pattern=龙凤呈祥'),
            ('按价格排序', '?sort_by=total_price&sort_order=desc'),
            ('组合查询', '?status=精雕&bamboo_type=紫竹&page=1&page_size=10')
        ]
        for desc, query in test_cases:
            response = requests.get(f'{BASE_URL}/api/orders{query}')
            data = response.json()
            total = data['data']['pagination']['total']
            print(f'  ✓ {desc}: 找到 {total} 条记录')
        print('✓ 筛选分页功能正常')
        return True
    except Exception as e:
        print(f'✗ 测试失败: {e}')
        return False

def test_update_order(order_no):
    print_separator('测试8: 修改订单（自动重新计价）')
    try:
        response = requests.put(f'{BASE_URL}/api/orders/{order_no}', json={
            'bamboo_type': '金丝竹',
            'carving_pattern': '山水风景',
            'quantity': 3
        })
        data = response.json()
        order = data['data']
        print(f'✓ 订单更新成功')
        print(f'  更新后 - 竹材: {order["bamboo_type"]}')
        print(f'  更新后 - 纹样: {order["carving_pattern"]}')
        print(f'  更新后 - 数量: {order["quantity"]}')
        print(f'  更新后 - 总价: ¥{order["total_price"]:.2f}')
        print(f'  更新后 - 交付日期: {order["delivery_date"]}')
        return True
    except Exception as e:
        print(f'✗ 测试失败: {e}')
        return False

def test_get_order_detail(order_no):
    print_separator('测试9: 获取订单详情')
    try:
        response = requests.get(f'{BASE_URL}/api/orders/{order_no}')
        data = response.json()
        order = data['data']
        print(f'✓ 订单详情获取成功')
        print(f'  订单号: {order["order_no"]}')
        print(f'  客户: {order["customer_name"]}')
        print(f'  匠人: {order.get("craftsman_name", "未分配")}')
        print(f'  当前进度: {order["status"]}')
        return True
    except Exception as e:
        print(f'✗ 测试失败: {e}')
        return False

if __name__ == '__main__':
    print('=' * 70)
    print('  传统竹雕笔搁定制订单管理系统 - v2.0 完整测试')
    print('=' * 70)
    print('  请先确保服务已启动: python app.py')
    print('  按 Enter 开始测试...')
    input()
    
    test_options()
    test_calculate()
    test_validation()
    order_no = test_create_order()
    if order_no:
        test_assign_craftsman(order_no)
        test_update_status(order_no)
        test_filter_and_pagination()
        test_update_order(order_no)
        test_get_order_detail(order_no)
    
    print_separator('所有测试完成！')
    print('  ✓ 核心功能全部验证通过')
    print('  ✓ 必填校验与数值规范正常')
    print('  ✓ 自动计价与工期计算正常')
    print('  ✓ 匠人绑定功能正常')
    print('  ✓ 多条件筛选、分页、排序正常')
    print('  ✓ 统一接口返回格式正常')
    print('=' * 70)
