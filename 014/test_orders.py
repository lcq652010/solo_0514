import requests
import json

BASE_URL = 'http://localhost:5000/api'

def test_create_order():
    print('=== 测试创建订单 ===')
    order_data = {
        'customer_name': '张三',
        'phone': '13800138000',
        'address': '北京市朝阳区某某街道123号',
        'paper_type': '皮料',
        'paper_size': '四尺',
        'quantity': 100,
        'thickness': '中等',
        'special_requirements': '需要水印，品质要求高'
    }
    
    response = requests.post(f'{BASE_URL}/orders', json=order_data)
    print(f'状态码: {response.status_code}')
    print(f'响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}')
    
    if response.status_code == 201:
        return response.json()['order_no']
    return None

def test_get_orders():
    print('\n=== 测试获取订单列表 ===')
    response = requests.get(f'{BASE_URL}/orders')
    print(f'状态码: {response.status_code}')
    print(f'响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}')

def test_get_order_detail(order_no):
    print(f'\n=== 测试获取订单详情: {order_no} ===')
    response = requests.get(f'{BASE_URL}/orders/{order_no}')
    print(f'状态码: {response.status_code}')
    print(f'响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}')

def test_update_order_status(order_no):
    print(f'\n=== 测试更新订单状态: {order_no} ===')
    status_data = {
        'status': '选料',
        'description': '已开始挑选优质原材料',
        'operator': '李师傅'
    }
    
    response = requests.put(f'{BASE_URL}/orders/{order_no}/status', json=status_data)
    print(f'状态码: {response.status_code}')
    print(f'响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}')

def test_get_statuses():
    print('\n=== 测试获取所有订单状态 ===')
    response = requests.get(f'{BASE_URL}/orders/statuses')
    print(f'状态码: {response.status_code}')
    print(f'响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}')

def test_get_paper_types():
    print('\n=== 测试获取宣纸类型 ===')
    response = requests.get(f'{BASE_URL}/orders/types')
    print(f'状态码: {response.status_code}')
    print(f'响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}')

def test_get_dashboard():
    print('\n=== 测试获取仪表板数据 ===')
    response = requests.get(f'{BASE_URL}/dashboard')
    print(f'状态码: {response.status_code}')
    print(f'响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}')

def create_sample_orders():
    print('\n=== 创建示例订单 ===')
    samples = [
        {
            'customer_name': '李四',
            'phone': '13900139000',
            'address': '上海市浦东新区某某路456号',
            'paper_type': '棉料',
            'paper_size': '六尺',
            'quantity': 50,
            'thickness': '稍厚',
            'special_requirements': '用于书法创作'
        },
        {
            'customer_name': '王五',
            'phone': '13700137000',
            'address': '广州市天河区某某街789号',
            'paper_type': '竹料',
            'paper_size': '八尺',
            'quantity': 200,
            'thickness': '薄',
            'special_requirements': '批量定制，用于画展'
        },
        {
            'customer_name': '赵六',
            'phone': '13600136000',
            'address': '杭州市西湖区某某路321号',
            'paper_type': '混合料',
            'paper_size': '丈二',
            'quantity': 30,
            'thickness': '厚',
            'special_requirements': '定制尺寸，用于大幅国画'
        }
    ]
    
    for sample in samples:
        response = requests.post(f'{BASE_URL}/orders', json=sample)
        if response.status_code == 201:
            print(f"创建订单成功: {response.json()['order_no']}")

if __name__ == '__main__':
    try:
        test_get_statuses()
        test_get_paper_types()
        
        order_no = test_create_order()
        
        if order_no:
            test_get_order_detail(order_no)
            test_update_order_status(order_no)
            test_get_order_detail(order_no)
        
        create_sample_orders()
        test_get_orders()
        test_get_dashboard()
        
        print('\n=== 所有测试完成 ===')
        
    except requests.exceptions.ConnectionError:
        print('错误: 无法连接到服务器，请先运行 python app.py 启动服务')
    except Exception as e:
        print(f'错误: {str(e)}')
