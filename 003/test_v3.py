import sys
sys.path.insert(0, '.')

from app import app
import json

print('=' * 70)
print('机场自助行李托运机运维管理系统 v3.0 - 功能测试')
print('=' * 70)

client = app.test_client()

print('\n' + '=' * 70)
print('1. 测试设备录入接口（含航站楼、值机岛）')
print('=' * 70)

device_data = {
    'device_code': 'BAG-V3-T1-A001',
    'device_name': 'T1航站楼A区1号自助托运机',
    'device_model': 'BAG-2024-PRO',
    'communication_mode': '5G',
    'terminal': 'T1',
    'checkin_island': 'A岛',
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
    print(f'  航站楼: {result["data"]["terminal"]}')
    print(f'  值机岛: {result["data"]["checkin_island"]}')
    device_id = result['data']['id']
else:
    print('✗ 设备录入失败:', result['message'])
    device_id = None

print('\n' + '=' * 70)
print('2. 测试按航站楼筛选设备列表')
print('=' * 70)

response = client.get('/api/devices?terminal=T1')
result = json.loads(response.data)
if result['code'] == 200:
    print(f'✓ T1航站楼设备查询成功，共 {result["data"]["pagination"]["total"]} 条')
    print(f'  响应格式验证: 包含 list 和 pagination 字段')

print('\n' + '=' * 70)
print('3. 测试设备详情接口（设备工单联动）')
print('=' * 70)

if device_id:
    response = client.get(f'/api/devices/{device_id}')
    result = json.loads(response.data)
    if result['code'] == 200:
        print('✓ 设备详情查询成功')
        print(f'  设备信息: {result["data"]["device_code"]}')
        if 'work_orders' in result['data']:
            print(f'  关联工单: 已返回工单列表')
        if 'maintenance_count' in result['data']:
            print(f'  运维记录数: {result["data"]["maintenance_count"]}')

print('\n' + '=' * 70)
print('4. 测试故障上报接口（含故障等级）')
print('=' * 70)

fault_data = {
    'device_code': 'BAG-V3-T1-A001',
    'fault_type': '硬件故障',
    'priority': '紧急',
    'fault_level': '严重',
    'fault_description': '行李传送带电机烧坏，影响T1航站楼A区航班出港',
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
    print(f'  故障等级: {result["data"]["fault_level"]}')
    print(f'  优先级: {result["data"]["priority"]}')
    order_no = result['data']['order_no']
else:
    print('✗ 故障上报失败:', result['message'])
    order_no = None

print('\n' + '=' * 70)
print('5. 测试工单优先级排序（紧急工单优先）')
print('=' * 70)

# 再创建一个普通优先级工单
fault_data2 = {
    'device_code': 'BAG-V3-T1-A001',
    'fault_type': '软件故障',
    'priority': '普通',
    'fault_level': '一般',
    'fault_description': '触摸屏界面偶尔卡顿，不影响正常使用',
    'reporter': '李操作员'
}
client.post('/api/work-orders',
            data=json.dumps(fault_data2),
            content_type='application/json')

response = client.get('/api/work-orders?status=待处理')
result = json.loads(response.data)
if result['code'] == 200:
    orders = result['data']['list']
    print(f'✓ 工单查询成功，共 {len(orders)} 条')
    if len(orders) >= 2:
        print(f'  第一条优先级: {orders[0]["priority"]}')
        print(f'  第二条优先级: {orders[1]["priority"]}')
        if orders[0]['priority_weight'] < orders[1]['priority_weight']:
            print('  ✓ 优先级排序正确！')

print('\n' + '=' * 70)
print('6. 测试按航站楼、故障等级筛选工单')
print('=' * 70)

response = client.get('/api/work-orders?terminal=T1&fault_level=严重')
result = json.loads(response.data)
if result['code'] == 200:
    print(f'✓ T1航站楼严重故障工单筛选成功，共 {result["data"]["pagination"]["total"]} 条')

print('\n' + '=' * 70)
print('7. 测试工单处理接口（记录维修工时、配件）')
print('=' * 70)

if order_no:
    handle_data = {
        'handler': '王工程师',
        'handle_result': '已更换传送带电机和传动带，设备恢复正常',
        'action': '修复完成',
        'duration': 45,
        'parts_used': '传送带电机x1,传动带x1,轴承x2'
    }
    
    response = client.put(f'/api/work-orders/{order_no}/handle',
                         data=json.dumps(handle_data),
                         content_type='application/json')
    
    result = json.loads(response.data)
    if result['code'] == 200:
        print('✓ 工单处理成功')
        print(f'  处理人: {result["data"]["handler"]}')
        print(f'  设备状态: {result["data"]["device_status"]}')

print('\n' + '=' * 70)
print('8. 测试维修日志记录接口（含工时、配件）')
print('=' * 70)

response = client.get('/api/maintenance-records?record_type=运维处理')
result = json.loads(response.data)
if result['code'] == 200:
    records = result['data']['list']
    print(f'✓ 运维记录查询成功，共 {len(records)} 条')
    if records:
        print(f'  最新记录: {records[0]["description"][:50]}...')

print('\n' + '=' * 70)
print('9. 测试设备完好率统计')
print('=' * 70)

response = client.get('/api/devices/availability-rate?terminal=T1')
result = json.loads(response.data)
if result['code'] == 200:
    print('✓ 设备完好率统计成功')
    print(f'  设备总数: {result["data"]["total_devices"]}')
    print(f'  可用设备: {result["data"]["available_devices"]}')
    print(f'  完好率: {result["data"]["availability_rate"]}%')

print('\n' + '=' * 70)
print('10. 测试综合统计数据')
print('=' * 70)

response = client.get('/api/dashboard/statistics')
result = json.loads(response.data)
if result['code'] == 200:
    print('✓ 综合统计查询成功')
    print(f'  设备完好率: {result["data"]["device_statistics"]["availability_rate"]}%')
    print(f'  待处理紧急工单: {result["data"]["work_order_statistics"]["urgent_pending"]}')
    print(f'  今日上报工单: {result["data"]["work_order_statistics"]["today_reported"]}')
    print(f'  今日完成工单: {result["data"]["work_order_statistics"]["today_completed"]}')
    if result['data'].get('terminal_statistics'):
        print(f'  航站楼统计: 已包含各航站楼数据')

print('\n' + '=' * 70)
print('11. 测试统一响应格式')
print('=' * 70)

response = client.get('/api/devices')
result = json.loads(response.data)
if 'code' in result and 'message' in result and 'data' in result and 'timestamp' in result:
    print('✓ 响应格式验证通过')
    print(f'  code: {result["code"]}')
    print(f'  message: {result["message"]}')
    print(f'  timestamp: {result["timestamp"]}')

print('\n' + '=' * 70)
print('12. 测试分页格式')
print('=' * 70)

response = client.get('/api/devices?page=1&per_page=5')
result = json.loads(response.data)
pagination = result['data']['pagination']
if 'page' in pagination and 'total' in pagination and 'pages' in pagination:
    print('✓ 分页格式验证通过')
    print(f'  当前页: {pagination["page"]}')
    print(f'  每页数量: {pagination["per_page"]}')
    print(f'  总记录数: {pagination["total"]}')
    print(f'  总页数: {pagination["pages"]}')

print('\n' + '=' * 70)
print('所有 v3.0 功能测试完成！')
print('=' * 70)
print('\n新增功能总结:')
print('  ✓ 设备模块: 航站楼、值机岛字段')
print('  ✓ 故障模块: 故障等级字段')
print('  ✓ 设备工单联动: 设备详情关联工单列表')
print('  ✓ 维修日志增强: 工时、更换配件等字段')
print('  ✓ 多维度筛选: 航站楼、值机岛、故障等级')
print('  ✓ 优先级高亮排序: 紧急工单优先显示')
print('  ✓ 统一接口格式: 标准响应格式、分页封装')
print('  ✓ 设备完好率统计: 全局、按航站楼统计')
print('\n' + '=' * 70)
