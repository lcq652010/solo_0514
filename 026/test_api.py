import requests
import json

BASE_URL = 'http://localhost:5000'

def test_health():
    print('1. 测试健康检查...')
    response = requests.get(f'{BASE_URL}/health')
    print(f'   状态码: {response.status_code}')
    print(f'   响应: {response.json()}')
    print()

def test_get_statuses():
    print('2. 获取订单状态列表...')
    response = requests.get(f'{BASE_URL}/api/statuses')
    print(f'   状态码: {response.status_code}')
    print(f'   订单状态: {response.json()}')
    print()

def test_create_order():
    print('3. 提交订单...')
    order_data = {
        'customer_name': '张三',
        'customer_phone': '13800138000',
        'customer_address': '北京市朝阳区',
        'fan_style': '圆形团扇',
        'pattern_description': '牡丹花纹，寓意富贵吉祥',
        'size': '直径30cm',
        'material_requirement': '真丝线，桑蚕丝面料',
        'special_requirement': '双面缂丝工艺',
        'remark': '客户希望两周内完成'
    }
    response = requests.post(f'{BASE_URL}/api/orders', json=order_data)
    print(f'   状态码: {response.status_code}')
    result = response.json()
    print(f'   响应: {json.dumps(result, ensure_ascii=False, indent=2)}')
    print()
    return result.get('order', {}).get('order_no')

def test_get_orders(order_no=None):
    print('4. 获取订单列表...')
    response = requests.get(f'{BASE_URL}/api/orders')
    print(f'   状态码: {response.status_code}')
    result = response.json()
    print(f'   订单总数: {result["total"]}')
    print(f'   订单列表: {json.dumps(result, ensure_ascii=False, indent=2)}')
    print()

def test_get_order_detail(order_no):
    print(f'5. 获取订单详情 {order_no}...')
    response = requests.get(f'{BASE_URL}/api/orders/{order_no}')
    print(f'   状态码: {response.status_code}')
    print(f'   订单详情: {json.dumps(response.json(), ensure_ascii=False, indent=2)}')
    print()

def test_update_order_status(order_no):
    print(f'6. 更新订单状态 {order_no}...')
    status_data = {
        'status': '选线',
        'remark': '已选定红色、粉色、绿色三种丝线'
    }
    response = requests.put(f'{BASE_URL}/api/orders/{order_no}/status', json=status_data)
    print(f'   状态码: {response.status_code}')
    print(f'   响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}')
    print()

def test_update_order_info(order_no):
    print(f'7. 更新订单信息 {order_no}...')
    update_data = {
        'customer_phone': '13900139000',
        'special_requirement': '加急订单，希望10天内完成'
    }
    response = requests.put(f'{BASE_URL}/api/orders/{order_no}', json=update_data)
    print(f'   状态码: {response.status_code}')
    print(f'   响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}')
    print()

if __name__ == '__main__':
    print('=' * 60)
    print('缂丝团扇订单管理系统 API 测试')
    print('=' * 60)
    print()
    
    try:
        test_health()
        test_get_statuses()
        order_no = test_create_order()
        if order_no:
            test_get_orders()
            test_get_order_detail(order_no)
            test_update_order_status(order_no)
            test_update_order_info(order_no)
            
            print('=' * 60)
            print('测试完成！')
            print(f'测试订单号: {order_no}')
            print('=' * 60)
    except requests.exceptions.ConnectionError:
        print('错误: 无法连接到服务器，请先运行 python app.py 启动服务！')
    except Exception as e:
        print(f'错误: {e}')
