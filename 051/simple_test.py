from app import app, init_db
import json

init_db()
client = app.test_client()

print('=' * 70)
print('系统功能优化测试 - 筛选功能 & 统一格式 & 完好率统计')
print('=' * 70)

print('\n' + '=' * 70)
print('1. 测试设备管理 - 校区/楼栋字段 & 筛选功能')
print('=' * 70)

devices_data = [
    {
        'device_id': 'DEV001',
        'device_name': '一号教学楼圈存机',
        'device_model': 'POS-2024-A1',
        'communication_mode': 'TCP/IP有线网络',
        'campus': '东校区',
        'building': '一号教学楼',
        'location': '一楼大厅',
        'status': '正常',
        'enable_date': '2024-01-15'
    },
    {
        'device_id': 'DEV002',
        'device_name': '二号教学楼圈存机',
        'device_model': 'POS-2024-B1',
        'communication_mode': 'WiFi无线网络',
        'campus': '东校区',
        'building': '二号教学楼',
        'location': '一楼大厅',
        'status': '正常',
        'enable_date': '2024-02-20'
    },
    {
        'device_id': 'DEV003',
        'device_name': '图书馆圈存机',
        'device_model': 'POS-2024-C1',
        'communication_mode': 'TCP/IP有线网络',
        'campus': '西校区',
        'building': '图书馆',
        'location': '一楼入口',
        'status': '正常',
        'enable_date': '2024-03-10'
    }
]

print('\n批量添加设备（含校区、楼栋字段）:')
for dev in devices_data:
    response = client.post('/api/devices', json=dev)
    print(f'  {dev["device_id"]}: {response.get_json()["msg"]}')

print('\n获取所有设备（统一返回格式）:')
response = client.get('/api/devices')
result = response.get_json()
print(f'  设备总数: {result["data"]["total"]}')
print(f'  返回格式包含 list 和 total 字段')

print('\n按校区筛选（东校区）:')
response = client.get('/api/devices?campus=东校区')
result = response.get_json()
print(f'  东校区设备数: {result["data"]["total"]}')
for dev in result['data']['list']:
    print(f'    - {dev["device_name"]} ({dev["building"]})')

print('\n按楼栋筛选（二号教学楼）:')
response = client.get('/api/devices?building=二号教学楼')
result = response.get_json()
print(f'  二号教学楼设备数: {result["data"]["total"]}')

print('\n组合筛选（东校区 + 正常状态）:')
response = client.get('/api/devices?campus=东校区&status=正常')
result = response.get_json()
print(f'  东校区正常设备数: {result["data"]["total"]}')

print('\n' + '=' * 70)
print('2. 测试工单管理 - 多条件筛选')
print('=' * 70)

orders_data = [
    {
        'device_id': 'DEV001',
        'fault_type': '交易异常',
        'fault_type_code': 'SW002',
        'priority': '紧急',
        'impact_level': '严重影响',
        'fault_description': '充值后余额未到账',
        'reporter': '张三',
        'reporter_phone': '13800138000'
    },
    {
        'device_id': 'DEV002',
        'fault_type': '网络延迟',
        'fault_type_code': 'NET002',
        'priority': '中',
        'impact_level': '中影响',
        'fault_description': '网络响应较慢',
        'reporter': '李四',
        'reporter_phone': '13900139000'
    },
    {
        'device_id': 'DEV003',
        'fault_type': '硬件故障',
        'fault_type_code': 'HW001',
        'priority': '高',
        'impact_level': '高影响',
        'fault_description': '触摸屏失灵',
        'reporter': '王五',
        'reporter_phone': '13700137000'
    }
]

print('\n创建多优先级工单:')
for order in orders_data:
    response = client.post('/api/work-orders', json=order)
    result = response.get_json()
    print(f'  {result["data"]["order_id"]} (优先级:{order["priority"]}): {result["msg"]}')

print('\n按优先级筛选（紧急）:')
response = client.get('/api/work-orders?priority=紧急')
result = response.get_json()
print(f'  紧急工单数量: {result["data"]["total"]}')

print('\n按故障类型筛选（硬件故障）:')
response = client.get('/api/work-orders?fault_type_code=HW001')
result = response.get_json()
print(f'  硬件故障工单数量: {result["data"]["total"]}')

print('\n按状态筛选（待处理）:')
response = client.get('/api/work-orders?status=待处理')
result = response.get_json()
print(f'  待处理工单数量: {result["data"]["total"]}')

print('\n组合筛选（优先级高 + 待处理）:')
response = client.get('/api/work-orders?priority=高&status=待处理')
result = response.get_json()
print(f'  高优先级待处理工单数量: {result["data"]["total"]}')

print('\n处理一个工单演示流程:')
response = client.get('/api/work-orders?priority=紧急')
urgent_order = response.get_json()['data']['list'][0]
order_id = urgent_order['order_id']

response = client.put(f'/api/work-orders/{order_id}/handle', json={
    'handler': '王工程师',
    'handle_note': '已安排上门维修'
})
print(f'  开始处理工单 {order_id}: {response.get_json()["msg"]}')

response = client.put(f'/api/work-orders/{order_id}/complete', json={
    'handle_note': '修复交易接口，恢复正常'
})
print(f'  完成工单 {order_id}: {response.get_json()["msg"]}')

print('\n按处理状态筛选（已完成）:')
response = client.get('/api/work-orders?status=已完成')
result = response.get_json()
print(f'  已完成工单数量: {result["data"]["total"]}')

print('\n' + '=' * 70)
print('3. 测试统计功能 - 设备完好率 & 多维度统计')
print('=' * 70)

print('\n获取完整统计数据:')
response = client.get('/api/statistics')
stats = response.get_json()['data']

print(f'\n  【设备统计】')
print(f'    设备总数: {stats["devices"]["total"]}')
print(f'    正常设备: {stats["devices"]["normal"]}')
print(f'    故障设备: {stats["devices"]["fault"]}')
print(f'    维修中: {stats["devices"]["repairing"]}')
print(f'    已修复: {stats["devices"]["repaired"]}')
print(f'    设备完好率: {stats["devices"]["intact_rate"]}')

print(f'\n  【工单统计】')
print(f'    工单总数: {stats["work_orders"]["total"]}')
print(f'    待处理: {stats["work_orders"]["pending"]}')
print(f'    处理中: {stats["work_orders"]["handling"]}')
print(f'    已完成: {stats["work_orders"]["completed"]}')
print(f'    工单完成率: {stats["work_orders"]["completion_rate"]}')

print(f'\n  【优先级分布】')
for priority, count in stats['priority_distribution'].items():
    print(f'    {priority}: {count}')

print(f'\n  【校区分布】')
for item in stats['campus_distribution']:
    print(f'    {item["campus"]}: {item["count"]}台')

print(f'\n  【楼栋分布】')
for item in stats['building_distribution']:
    print(f'    {item["building"]}: {item["count"]}台')

print('\n按校区统计（东校区完好率）:')
response = client.get('/api/statistics?campus=东校区')
east_stats = response.get_json()['data']
print(f'  东校区设备完好率: {east_stats["devices"]["intact_rate"]}')

print('\n' + '=' * 70)
print('✅ 所有优化功能测试完成！')
print('=' * 70)
print('\n【本次优化总结】')
print('  ✓ 设备模块新增校区、楼栋字段')
print('  ✓ 支持按校区、楼栋、状态、优先级多条件筛选')
print('  ✓ 统一接口返回格式（code + data + msg，列表含list和total）')
print('  ✓ 新增设备完好率统计')
print('  ✓ 新增工单完成率统计')
print('  ✓ 支持按校区/楼栋维度统计')
print('  ✓ 故障类型优先级分布统计')
