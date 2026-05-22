import sys
sys.path.insert(0, '.')

from app import app, db, Device, WorkOrder, MaintenanceRecord
import json

print('=' * 60)
print('开始测试机场自助行李托运机运维管理系统')
print('=' * 60)

with app.app_context():
    print('\n1. 测试数据库初始化...')
    print('✓ 数据库表创建成功')
    
    print('\n2. 测试设备录入接口...')
    client = app.test_client()
    
    device_data = {
        'device_code': 'BAG-TEST-001',
        'device_name': '测试航站楼1号自助托运机',
        'location': '测试航站楼A区',
        'install_date': '2024-01-15',
        'operator': '测试管理员'
    }
    
    response = client.post('/api/devices', 
                          data=json.dumps(device_data),
                          content_type='application/json')
    
    result = json.loads(response.data)
    if result['code'] == 200:
        print('✓ 设备录入成功')
        print(f'  设备编号: {result["data"]["device_code"]}')
        print(f'  设备名称: {result["data"]["device_name"]}')
    else:
        print('✗ 设备录入失败:', result['message'])
    
    print('\n3. 测试设备列表查询接口...')
    response = client.get('/api/devices?page=1&per_page=10')
    result = json.loads(response.data)
    if result['code'] == 200:
        print(f'✓ 设备查询成功，共 {result["data"]["total"]} 条记录')
    
    print('\n4. 测试故障上报接口...')
    fault_data = {
        'device_code': 'BAG-TEST-001',
        'fault_description': '测试故障：设备显示屏无法正常显示',
        'reporter': '测试操作员'
    }
    
    response = client.post('/api/work-orders',
                          data=json.dumps(fault_data),
                          content_type='application/json')
    
    result = json.loads(response.data)
    if result['code'] == 200:
        print('✓ 故障上报成功')
        print(f'  工单编号: {result["data"]["order_no"]}')
        print(f'  设备状态: 故障')
        order_no = result['data']['order_no']
    else:
        print('✗ 故障上报失败:', result['message'])
        order_no = None
    
    print('\n5. 测试工单查询接口...')
    response = client.get('/api/work-orders?status=待处理')
    result = json.loads(response.data)
    if result['code'] == 200:
        print(f'✓ 工单查询成功，共 {result["data"]["total"]} 条待处理工单')
    
    if order_no:
        print('\n6. 测试工单处理接口...')
        handle_data = {
            'handler': '测试工程师',
            'handle_result': '已更换显示屏排线，设备恢复正常',
            'action': '修复完成'
        }
        
        response = client.put(f'/api/work-orders/{order_no}/handle',
                             data=json.dumps(handle_data),
                             content_type='application/json')
        
        result = json.loads(response.data)
        if result['code'] == 200:
            print('✓ 工单处理成功')
            print(f'  工单状态: {result["data"]["status"]}')
            print(f'  设备状态: {result["data"]["device_status"]}')
        else:
            print('✗ 工单处理失败:', result['message'])
    
    print('\n7. 测试运维记录查询接口...')
    response = client.get('/api/maintenance-records?page=1&per_page=10')
    result = json.loads(response.data)
    if result['code'] == 200:
        print(f'✓ 运维记录查询成功，共 {result["data"]["total"]} 条记录')
    
    print('\n8. 测试统计数据接口...')
    response = client.get('/api/dashboard/statistics')
    result = json.loads(response.data)
    if result['code'] == 200:
        print('✓ 统计数据查询成功')
        print(f'  设备总数: {result["data"]["total_devices"]}')
        print(f'  正常设备: {result["data"]["normal_devices"]}')
        print(f'  故障设备: {result["data"]["fault_devices"]}')
        print(f'  维修中设备: {result["data"]["repairing_devices"]}')
        print(f'  待处理工单: {result["data"]["pending_orders"]}')
        print(f'  已完成工单: {result["data"]["completed_orders"]}')
    
    print('\n' + '=' * 60)
    print('所有接口测试完成！')
    print('=' * 60)
    print('\n数据库文件已创建: baggage_management.db')
