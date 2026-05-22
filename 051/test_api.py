import requests
import json

BASE_URL = 'http://127.0.0.1:5000/api'


def test_device_management():
    print('=' * 50)
    print('测试设备管理功能')
    print('=' * 50)

    device_data = {
        'device_id': 'DEV001',
        'device_name': '一号教学楼圈存机',
        'location': '一号教学楼大厅',
        'status': '正常',
        'install_date': '2024-01-15'
    }

    print('\n1. 添加设备:')
    response = requests.post(f'{BASE_URL}/devices', json=device_data)
    print(f'状态码: {response.status_code}')
    print(f'返回: {response.json()}')

    print('\n2. 获取所有设备:')
    response = requests.get(f'{BASE_URL}/devices')
    print(f'状态码: {response.status_code}')
    devices = response.json()
    print(f'设备数量: {len(devices["data"])}')

    print('\n3. 获取单个设备:')
    response = requests.get(f'{BASE_URL}/devices/DEV001')
    print(f'状态码: {response.status_code}')
    print(f'设备信息: {response.json()["data"]["device_name"]}')


def test_work_order():
    print('\n' + '=' * 50)
    print('测试工单管理功能')
    print('=' * 50)

    order_data = {
        'device_id': 'DEV001',
        'fault_type': '硬件故障',
        'fault_description': '触摸屏幕无响应',
        'reporter': '张三',
        'reporter_phone': '13800138000'
    }

    print('\n1. 故障上报（创建工单）:')
    response = requests.post(f'{BASE_URL}/work-orders', json=order_data)
    print(f'状态码: {response.status_code}')
    result = response.json()
    print(f'返回: {result}')
    order_id = result['data']['order_id']
    print(f'自动生成工单编号: {order_id}')

    print('\n2. 获取所有工单:')
    response = requests.get(f'{BASE_URL}/work-orders')
    print(f'状态码: {response.status_code}')
    orders = response.json()
    print(f'工单数量: {len(orders["data"])}')

    print('\n3. 开始处理工单:')
    handle_data = {
        'handler': '李工程师',
        'handle_note': '已安排人员上门维修'
    }
    response = requests.put(f'{BASE_URL}/work-orders/{order_id}/handle', json=handle_data)
    print(f'状态码: {response.status_code}')
    print(f'返回: {response.json()}')

    print('\n4. 完成工单:')
    complete_data = {
        'handle_note': '更换触摸屏模块，设备恢复正常'
    }
    response = requests.put(f'{BASE_URL}/work-orders/{order_id}/complete', json=complete_data)
    print(f'状态码: {response.status_code}')
    print(f'返回: {response.json()}')


def test_maintain_records():
    print('\n' + '=' * 50)
    print('测试运维记录功能')
    print('=' * 50)

    print('\n1. 获取所有运维记录:')
    response = requests.get(f'{BASE_URL}/maintain-records')
    print(f'状态码: {response.status_code}')
    records = response.json()
    print(f'记录数量: {len(records["data"])}')

    print('\n2. 按设备查询运维记录:')
    response = requests.get(f'{BASE_URL}/maintain-records?device_id=DEV001')
    print(f'状态码: {response.status_code}')
    records = response.json()
    print(f'DEV001的记录数量: {len(records["data"])}')


def test_statistics():
    print('\n' + '=' * 50)
    print('测试统计功能')
    print('=' * 50)

    print('\n获取统计数据:')
    response = requests.get(f'{BASE_URL}/statistics')
    print(f'状态码: {response.status_code}')
    stats = response.json()
    print(json.dumps(stats['data'], ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        test_device_management()
        test_work_order()
        test_maintain_records()
        test_statistics()
        print('\n' + '=' * 50)
        print('所有测试完成！')
        print('=' * 50)
    except Exception as e:
        print(f'测试失败: {e}')
        print('请先确保服务已启动: python app.py')
