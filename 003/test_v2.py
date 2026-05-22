import sys
sys.path.insert(0, '.')

from app import app
import json

print('=' * 70)
print('机场自助行李托运机运维管理系统 v2.0 - 功能测试')
print('=' * 70)

client = app.test_client()

print('\n' + '=' * 70)
print('1. 测试设备录入接口（含新字段）')
print('=' * 70)

device_data = {
    'device_code': 'BAG-V2-001',
    'device_name': 'T1航站楼A区自助托运机',
    'device_model': 'BAG-2024-PRO',
    'communication_mode': '5G',
    'location': 'T1航站楼A区1号机位',
    'install_date': '2024-01-15',
    'activation_date': '2024-02-01',
    'operator': '系统管理员'
}

response = client.post('/api/devices', 
                      data=json.dumps(device_data),
                      content_type='application/json')

result = json.loads(response.data)
if result['code'] == 200:
    print('✓ 设备录入成功')
    print(f'  设备编号: {result["data"]["device_code"]}')
    print(f'  设备型号: {result["data"]["device_model"]}')
    print(f'  通信方式: {result["data"]["communication_mode"]}')
    print(f'  启用日期: {result["data"]["activation_date"]}')
else:
    print('✗ 设备录入失败:', result['message'])

print('\n' + '=' * 70)
print('2. 测试设备列表查询接口')
print('=' * 70)

response = client.get('/api/devices?page=1&per_page=5')
result = json.loads(response.data)
if result['code'] == 200:
    print(f'✓ 设备查询成功，共 {result["data"]["total"]} 条记录')
    for device in result['data']['devices']:
        print(f'  - {device["device_code"]} | {device["device_name"]} | {device["status"]}')
        print(f'    型号: {device["device_model"]}, 通信: {device["communication_mode"]}')

print('\n' + '=' * 70)
print('3. 测试故障上报接口（含故障类型和紧急优先级）')
print('=' * 70)

fault_data = {
    'device_code': 'BAG-V2-001',
    'fault_type': '硬件故障',
    'priority': '紧急',
    'fault_description': '行李传送带电机烧坏，影响航班出港行李托运',
    'reporter': '张操作员'
}

response = client.post('/api/work-orders',
                      data=json.dumps(fault_data),
                      content_type='application/json')

result = json.loads(response.data)
if result['code'] == 200:
    print('✓ 故障上报成功')
    print(f'  工单编号: {result["data"]["order_no"]}')
    print(f'  故障类型: {result["data"]["fault_type"]}')
    print(f'  优先级: {result["data"]["priority"]}')
    print(f'  故障描述: {result["data"]["fault_description"]}')
else:
    print('✗ 故障上报失败:', result['message'])

print('\n' + '=' * 70)
print('4. 测试多优先级工单排序（紧急工单优先）')
print('=' * 70)

fault_data2 = {
    'device_code': 'BAG-V2-001',
    'fault_type': '软件故障',
    'priority': '普通',
    'fault_description': '触摸屏界面偶尔卡顿，不影响正常使用',
    'reporter': '李操作员'
}

client.post('/api/work-orders',
            data=json.dumps(fault_data2),
            content_type='application/json')

response = client.get('/api/work-orders?status=待处理')
result = json.loads(response.data)
if result['code'] == 200:
    print(f'✓ 工单查询成功，共 {result["data"]["total"]} 条待处理工单')
    for order in result['data']['work_orders']:
        print(f'  [{order["priority"]}] {order["order_no"]} - {order["fault_type"]}: {order["fault_description"][:30]}...')

print('\n' + '=' * 70)
print('5. 测试按故障类型筛选工单')
print('=' * 70)

response = client.get('/api/work-orders?fault_type=硬件故障')
result = json.loads(response.data)
if result['code'] == 200:
    print(f'✓ 硬件故障工单查询成功，共 {result["data"]["total"]} 条记录')

print('\n' + '=' * 70)
print('6. 测试按优先级筛选工单')
print('=' * 70)

response = client.get('/api/work-orders?priority=紧急')
result = json.loads(response.data)
if result['code'] == 200:
    print(f'✓ 紧急工单查询成功，共 {result["data"]["total"]} 条记录')

print('\n' + '=' * 70)
print('7. 测试统计数据接口（含新字段统计）')
print('=' * 70)

response = client.get('/api/dashboard/statistics')
result = json.loads(response.data)
if result['code'] == 200:
    print('✓ 统计数据查询成功')
    print(f'  设备总数: {result["data"]["total_devices"]}')
    print(f'  待处理紧急工单: {result["data"]["urgent_pending_orders"]}')
    print(f'  待处理高优先级工单: {result["data"]["high_priority_pending_orders"]}')
    print(f'  故障类型统计:')
    for ftype, count in result['data']['fault_type_statistics'].items():
        print(f'    - {ftype}: {count} 条')

print('\n' + '=' * 70)
print('所有功能测试完成！')
print('=' * 70)
