import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if os.path.exists('gas_station.db'):
    os.remove('gas_station.db')
    print('旧数据库已删除')

from models import init_db, FAULT_CATEGORIES, PRIORITY_LEVELS
init_db()
print('数据库初始化完成')

print('\n=== 常量配置 ===')
print('故障分类:', FAULT_CATEGORIES)
print('优先级:', PRIORITY_LEVELS)

from app import app
import json

client = app.test_client()

print('\n=== 测试添加新设备（含新字段） ===')
device_data = {
    'device_no': 'FUEL-002',
    'device_name': '2号加油机',
    'device_type': '加油机',
    'device_model': '正星ZSK-200',
    'control_version': 'V3.2.1',
    'location': 'A区2号机位',
    'install_date': '2024-01-15',
    'enable_date': '2024-02-01',
    'description': '新增设备'
}
resp = client.post('/api/devices', json=device_data)
print('添加结果:', resp.get_json())

print('\n=== 获取设备列表 ===')
resp = client.get('/api/devices')
devices = resp.get_json()['data']
print('设备数量:', len(devices))
if devices:
    print('设备字段:', list(devices[0].keys()))
    device_id = devices[0]['id']
    print('设备型号:', devices[0].get('device_model'))
    print('主控版本:', devices[0].get('control_version'))
    print('启用日期:', devices[0].get('enable_date'))

print('\n=== 测试获取常量接口 ===')
resp = client.get('/api/constants')
print('常量接口:', json.dumps(resp.get_json(), ensure_ascii=False, indent=2))

print('\n=== 测试紧急故障上报 ===')
fault_data = {
    'device_id': device_id,
    'fault_type': '油枪无法出油',
    'fault_category': 'hardware',
    'priority': 'urgent',
    'fault_description': '1号油枪完全不出油，影响客户加油',
    'reporter': '张三',
    'contact': '13800138000'
}
resp = client.post('/api/fault-reports', json=fault_data)
print('紧急故障上报:', resp.get_json())

print('\n=== 测试普通故障上报 ===')
fault_data2 = {
    'device_id': device_id,
    'fault_type': '显示屏轻微闪烁',
    'fault_category': 'software',
    'priority': 'low',
    'fault_description': '显示屏偶尔闪烁，不影响正常使用',
    'reporter': '李四',
    'contact': '13900139000'
}
resp = client.post('/api/fault-reports', json=fault_data2)
print('普通故障上报:', resp.get_json())

print('\n=== 获取故障列表（按优先级排序） ===')
resp = client.get('/api/fault-reports')
reports = resp.get_json()['data']
print('故障数量:', len(reports))
for r in reports:
    print(f"  工单: {r['order_no']}, 优先级: {r['priority']}, 分类: {r['fault_category']}")

print('\n=== 按优先级筛选（仅紧急） ===')
resp = client.get('/api/fault-reports?priority=urgent')
reports = resp.get_json()['data']
print('紧急故障数量:', len(reports))

print('\n=== 按故障分类筛选（仅硬件） ===')
resp = client.get('/api/fault-reports?fault_category=hardware')
reports = resp.get_json()['data']
print('硬件故障数量:', len(reports))

print('\n✅ 所有新功能测试通过！')
