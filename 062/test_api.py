import requests
import json

BASE_URL = 'http://localhost:5000/api'

def print_response(title, response):
    print(f'\n=== {title} ===')
    print(f'状态码: {response.status_code}')
    result = response.json()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result

def test_validation():
    print('\n=== 测试字段校验功能 ===')
    
    print('\n1. 测试缺少必填字段:')
    data = {
        'customer_name': '张三',
        'seal_text': '张三之印'
    }
    response = requests.post(f'{BASE_URL}/orders', json=data)
    print_response('缺少必填字段测试', response)
    
    print('\n2. 测试手机号码格式错误:')
    data = {
        'customer_name': '张三',
        'customer_phone': '12345',
        'seal_text': '张三之印',
        'seal_spec': 'square_25',
        'horn_material': 'black_buffalo',
        'seal_style': 'zhuanshu_xiaozhuan'
    }
    response = requests.post(f'{BASE_URL}/orders', json=data)
    print_response('手机号码格式测试', response)
    
    print('\n3. 测试印文内容过长:')
    data = {
        'customer_name': '张三',
        'customer_phone': '13800138000',
        'seal_text': '这是一个非常长的印文内容测试',
        'seal_spec': 'square_25',
        'horn_material': 'black_buffalo',
        'seal_style': 'zhuanshu_xiaozhuan'
    }
    response = requests.post(f'{BASE_URL}/orders', json=data)
    print_response('印文长度测试', response)

def test_calculate():
    print('\n=== 测试计价功能 ===')
    data = {
        'seal_spec': 'square_25',
        'horn_material': 'black_buffalo',
        'seal_style': 'zhuanshu_xiaozhuan',
        'edge_style': 'simple'
    }
    response = requests.post(f'{BASE_URL}/orders/calculate', json=data)
    print_response('计价测试', response)

def test_create_order():
    print('\n=== 测试创建订单（自动计价+匠人绑定） ===')
    data = {
        'customer_name': '张三',
        'customer_phone': '13800138000',
        'seal_text': '张三之印',
        'seal_spec': 'square_25',
        'horn_material': 'black_buffalo',
        'seal_style': 'zhuanshu_xiaozhuan',
        'edge_style': 'simple',
        'special_requirements': '印面要清晰，线条要均匀'
    }
    response = requests.post(f'{BASE_URL}/orders', json=data)
    result = print_response('创建订单测试', response)
    return result.get('data', {}).get('order_no')

def test_create_multiple_orders():
    print('\n=== 创建多个订单用于筛选测试 ===')
    orders = [
        {
            'customer_name': '李四',
            'customer_phone': '13900139000',
            'seal_text': '李四藏书',
            'seal_spec': 'circle_30',
            'horn_material': 'white_buffalo',
            'seal_style': 'zhuanshu_dazhuan',
            'edge_style': 'full'
        },
        {
            'customer_name': '王五',
            'customer_phone': '13700137000',
            'seal_text': '王五印信',
            'seal_spec': 'rectangle_40x20',
            'horn_material': 'yak',
            'seal_style': 'zhuanshu_bird',
            'edge_style': 'poem'
        },
        {
            'customer_name': '赵六',
            'customer_phone': '13600136000',
            'seal_text': '赵六书画',
            'seal_spec': 'ellipse_30x20',
            'horn_material': 'yellow_buffalo',
            'seal_style': 'li_shu',
            'edge_style': 'none'
        }
    ]
    
    order_nos = []
    for order in orders:
        response = requests.post(f'{BASE_URL}/orders', json=order)
        result = response.json()
        if result.get('data'):
            order_nos.append(result['data'].get('order_no'))
    
    print(f'成功创建 {len(order_nos)} 个订单')
    return order_nos

def test_pagination():
    print('\n=== 测试分页排序功能 ===')
    
    print('\n1. 默认分页（第1页，每页10条）:')
    response = requests.get(f'{BASE_URL}/orders')
    print_response('默认分页测试', response)
    
    print('\n2. 按价格升序排序:')
    response = requests.get(f'{BASE_URL}/orders?sort_by=price&sort_order=asc')
    print_response('价格升序测试', response)
    
    print('\n3. 按交付日期降序排序:')
    response = requests.get(f'{BASE_URL}/orders?sort_by=delivery_date&sort_order=desc')
    print_response('交付日期降序测试', response)

def test_filter():
    print('\n=== 测试高级筛选功能 ===')
    
    print('\n1. 按状态筛选（待接单）:')
    response = requests.get(f'{BASE_URL}/orders?status=待接单')
    print_response('按状态筛选', response)
    
    print('\n2. 按材质筛选（白水牛角）:')
    response = requests.get(f'{BASE_URL}/orders?material=white_buffalo')
    print_response('按材质筛选', response)
    
    print('\n3. 按风格筛选（隶书）:')
    response = requests.get(f'{BASE_URL}/orders?style=li_shu')
    print_response('按风格筛选', response)
    
    print('\n4. 关键词搜索（李四）:')
    response = requests.get(f'{BASE_URL}/orders?keyword=李四')
    print_response('关键词搜索', response)
    
    print('\n5. 组合筛选（待接单 + 牦牛角材质）:')
    response = requests.get(f'{BASE_URL}/orders?status=待接单&material=yak')
    print_response('组合筛选测试', response)

def test_status_update(order_no):
    print(f'\n=== 测试状态更新（自动更新交付日期） ===')
    
    print('\n1. 更新为选料状态:')
    data = {'status': '选料'}
    response = requests.put(f'{BASE_URL}/orders/{order_no}/status', json=data)
    print_response('更新为选料', response)
    
    print('\n2. 更新为切坯状态:')
    data = {'status': '切坯'}
    response = requests.put(f'{BASE_URL}/orders/{order_no}/status', json=data)
    print_response('更新为切坯', response)
    
    print('\n3. 查看订单详情，验证交付日期更新:')
    response = requests.get(f'{BASE_URL}/orders/{order_no}')
    print_response('订单详情', response)

def test_get_options():
    print('=== 获取所有选项数据 ===')
    
    endpoints = [
        ('状态列表', '/statuses'),
        ('材质列表', '/horn-materials'),
        ('规格列表', '/seal-specs'),
        ('风格列表', '/seal-styles'),
        ('边款列表', '/edge-styles'),
        ('匠人列表', '/craftsmen')
    ]
    
    for name, endpoint in endpoints:
        print(f'\n{name}:')
        response = requests.get(f'{BASE_URL}{endpoint}')
        print_response(name, response)

if __name__ == '__main__':
    try:
        print('=' * 60)
        print('传统牛角印章定制订单管理系统 - 功能测试')
        print('=' * 60)
        
        test_get_options()
        test_validation()
        test_calculate()
        order_no = test_create_order()
        test_create_multiple_orders()
        test_pagination()
        test_filter()
        
        if order_no:
            test_status_update(order_no)
        
        print('\n' + '=' * 60)
        print('所有测试完成！')
        print('=' * 60)
        
    except Exception as e:
        print(f'\n测试出错: {e}')
        import traceback
        traceback.print_exc()
        print('请确保服务器已启动！')
