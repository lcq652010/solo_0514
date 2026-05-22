import requests
import json

BASE_URL = 'http://localhost:5000'

print('=' * 50)
print('1. 添加设备')
data = {
    'device_code': 'POS002',
    'device_name': '自助收银机2号',
    'location': '二楼出口',
    'install_date': '2024-02-20'
}
r = requests.post(f'{BASE_URL}/api/devices', json=data)
print(f'状态码: {r.status_code}, 响应: {r.json()}')

print('\n' + '=' * 50)
print('2. 查询设备列表')
r = requests.get(f'{BASE_URL}/api/devices')
result = r.json()
print(f'状态码: {r.status_code}')
for device in result['data']:
    print(f"  {device['device_code']}: {device['device_name']} - 状态: {device['status']}")

print('\n' + '=' * 50)
print('3. 创建报修工单')
data = {
    'device_id': 2,
    'fault_description': '打印机卡纸',
    'reporter': '李四',
    'reporter_phone': '13900139000'
}
r = requests.post(f'{BASE_URL}/api/work-orders', json=data)
result = r.json()
print(f'状态码: {r.status_code}, 响应: {result}')
order_no = result['order_no']

print('\n' + '=' * 50)
print('4. 查询工单列表')
r = requests.get(f'{BASE_URL}/api/work-orders')
result = r.json()
print(f'状态码: {r.status_code}')
for order in result['data']:
    print(f"  {order['order_no']}: {order['fault_description']} - 状态: {order['status']}")

print('\n' + '=' * 50)
print(f'5. 处理工单: {order_no}')
data = {
    'status': '已完成',
    'handle_user': '王工',
    'handle_content': '清理打印机，更换硒鼓'
}
print(f'  请求数据: {data}')
r = requests.put(f'{BASE_URL}/api/work-orders/{order_no}/handle', json=data)
print(f'  状态码: {r.status_code}, 响应: {r.json()}')

print('\n' + '=' * 50)
print('6. 再次查询工单列表')
r = requests.get(f'{BASE_URL}/api/work-orders')
result = r.json()
print(f'状态码: {r.status_code}')
for order in result['data']:
    print(f"  {order['order_no']}: {order['fault_description']} - 状态: {order['status']} - 处理人: {order['handle_user']}")

print('\n' + '=' * 50)
print('7. 查询运维记录')
r = requests.get(f'{BASE_URL}/api/maintenance-records')
result = r.json()
print(f'状态码: {r.status_code}')
for record in result['data']:
    print(f"  {record['maintenance_type']}: {record['content']} - 操作人: {record['operator']}")

print('\n' + '=' * 50)
print('8. 更新设备状态为正常')
r = requests.put(f'{BASE_URL}/api/devices/2/status', json={'status': '正常'})
print(f'状态码: {r.status_code}, 响应: {r.json()}')

print('\n' + '=' * 50)
print('9. 查询统计数据')
r = requests.get(f'{BASE_URL}/api/dashboard/stats')
result = r.json()
print(f'状态码: {r.status_code}')
stats = result['data']
print(f"  设备总数: {stats['total_devices']}")
print(f"  正常设备: {stats['normal_devices']}")
print(f"  故障设备: {stats['fault_devices']}")
print(f"  维修中设备: {stats['repairing_devices']}")
print(f"  待处理工单: {stats['pending_orders']}")

print('\n' + '=' * 50)
print('所有测试完成！')