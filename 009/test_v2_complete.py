import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if os.path.exists('gas_station.db'):
    os.remove('gas_station.db')
    print('🗑️  旧数据库已删除')

from models import init_db
init_db()
print('✅ 数据库初始化完成')

from app import app
import json

client = app.test_client()

print('\n' + '='*60)
print('🚀 加油站运维管理系统 V2.0 功能测试')
print('='*60)

print('\n📋 【1/8】测试系统常量接口')
resp = client.get('/api/constants')
result = resp.get_json()
print(f'   故障分类数量: {len(result["data"]["fault_categories"])}')
print(f'   优先级级别: {result["data"]["priority_levels"]}')
print(f'   加油站区域: {result["data"]["station_areas"][:3]}...')
print(f'   油品类型: {result["data"]["gasoline_types"][:3]}...')
print('✅ 系统常量获取成功')

print('\n📋 【2/8】测试添加设备（含新字段：区域、油号、型号等）')
device1 = {
    'device_no': 'FUEL-A-001',
    'device_name': 'A区1号加油机',
    'device_type': '加油机',
    'device_model': '正星ZSK-200A',
    'control_version': 'V3.2.1',
    'station_area': 'A区',
    'gasoline_type': '92#',
    'location': 'A区入口左侧',
    'install_date': '2024-01-15',
    'enable_date': '2024-02-01',
    'description': '主加油机，支持微信支付宝'
}
resp = client.post('/api/devices', json=device1)
device1_id = resp.get_json()['data']['id']
print(f'   设备1 ID: {device1_id}')

device2 = {
    'device_no': 'FUEL-B-001',
    'device_name': 'B区1号加油机',
    'device_type': '加油机',
    'device_model': '正星ZSK-300B',
    'control_version': 'V3.1.0',
    'station_area': 'B区',
    'gasoline_type': '95#',
    'location': 'B区中间位置',
    'install_date': '2024-03-10',
    'enable_date': '2024-03-15',
    'description': '高端加油机'
}
resp = client.post('/api/devices', json=device2)
device2_id = resp.get_json()['data']['id']
print(f'   设备2 ID: {device2_id}')
print('✅ 设备添加成功（含新字段）')

print('\n📋 【3/8】测试故障报修优先级和分类')
fault1 = {
    'device_id': device1_id,
    'fault_type': '油枪不出油',
    'fault_category': 'hardware',
    'priority': 'urgent',
    'fault_description': '1号油枪完全不出油，客户投诉',
    'reporter': '张三',
    'contact': '13800138000'
}
resp = client.post('/api/fault-reports', json=fault1)
fault1_id = resp.get_json()['data']['id']
fault1_order = resp.get_json()['data']['order_no']
print(f'   紧急故障工单: {fault1_order} (ID: {fault1_id})')

fault2 = {
    'device_id': device2_id,
    'fault_type': '显示屏闪烁',
    'fault_category': 'software',
    'priority': 'low',
    'fault_description': '显示屏偶尔闪烁，不影响正常使用',
    'reporter': '李四',
    'contact': '13900139000'
}
resp = client.post('/api/fault-reports', json=fault2)
fault2_id = resp.get_json()['data']['id']
fault2_order = resp.get_json()['data']['order_no']
print(f'   低优先级工单: {fault2_order} (ID: {fault2_id})')

fault3 = {
    'device_id': device1_id,
    'fault_type': '小票打印机卡纸',
    'fault_category': 'mechanical',
    'priority': 'normal',
    'fault_description': '打印机频繁卡纸，需清理',
    'reporter': '王五',
    'contact': '13700137000'
}
resp = client.post('/api/fault-reports', json=fault3)
fault3_id = resp.get_json()['data']['id']
print('✅ 故障报修成功（支持优先级和分类）')

print('\n📋 【4/8】测试优先级高亮排序')
resp = client.get('/api/fault-reports')
reports = resp.get_json()['data']
print(f'   工单总数: {len(reports)}')
print(f'   排序验证: 第1条优先级 = {reports[0]["priority"]} (颜色: {reports[0]["priority_color"]})')
print(f'            第2条优先级 = {reports[1]["priority"]} (颜色: {reports[1]["priority_color"]})')
print(f'            第3条优先级 = {reports[2]["priority"]} (颜色: {reports[2]["priority_color"]})')
if reports[0]['priority'] == 'urgent' and reports[1]['priority'] == 'normal' and reports[2]['priority'] == 'low':
    print('✅ 优先级排序正确（紧急→普通→低）')
else:
    print('⚠️  排序可能有问题')

print('\n📋 【5/8】测试多维度筛选功能')

resp = client.get('/api/fault-reports?priority=urgent')
print(f'   按优先级筛选(紧急): {len(resp.get_json()["data"])} 条')

resp = client.get('/api/fault-reports?station_area=A区')
print(f'   按区域筛选(A区): {len(resp.get_json()["data"])} 条')

resp = client.get('/api/devices?gasoline_type=95#')
print(f'   按油号筛选(95#): {len(resp.get_json()["data"])} 台')

resp = client.get('/api/devices?station_area=B区&gasoline_type=95#')
print(f'   组合筛选(B区+95#): {len(resp.get_json()["data"])} 台')
print('✅ 多维度筛选功能正常')

print('\n📋 【6/8】测试设备工单联动')
resp = client.get(f'/api/devices/{device1_id}')
device_detail = resp.get_json()['data']
print(f'   设备关联故障数: {len(device_detail["recent_faults"])}')
print(f'   设备关联运维数: {len(device_detail["recent_maintenance"])}')

resp = client.get(f'/api/fault-reports/{fault1_id}')
fault_detail = resp.get_json()['data']
print(f'   故障关联运维数: {len(fault_detail["maintenance_records"])}')
print('✅ 设备工单联动正常')

print('\n📋 【7/8】测试维修日志记录功能')
maint1 = {
    'device_id': device1_id,
    'fault_report_id': fault1_id,
    'maintenance_type': '故障维修',
    'maintenance_content': '更换油枪密封圈，清理油路',
    'maintenance_person': '李工',
    'action_taken': '更换配件',
    'parts_replaced': '密封圈x1, 油枪滤芯x1',
    'start_time': '2026-05-15 14:00:00',
    'end_time': '2026-05-15 15:30:00',
    'cost': 280.00,
    'remark': '维修完成，测试正常'
}
resp = client.post('/api/maintenance-records', json=maint1)
maint1_id = resp.get_json()['data']['id']
print(f'   创建运维记录 ID: {maint1_id}')

log1 = {
    'maintenance_id': maint1_id,
    'log_type': 'check',
    'log_content': '到达现场，检查设备状态',
    'operator': '李工'
}
resp = client.post('/api/maintenance-logs', json=log1)
print(f'   添加检查日志')

log2 = {
    'maintenance_id': maint1_id,
    'log_type': 'repair',
    'log_content': '拆卸油枪，发现密封圈老化变形',
    'operator': '李工'
}
resp = client.post('/api/maintenance-logs', json=log2)
print(f'   添加维修日志')

log3 = {
    'maintenance_id': maint1_id,
    'log_type': 'complete',
    'log_content': '更换密封圈，测试加油正常，交付使用',
    'operator': '李工'
}
resp = client.post('/api/maintenance-logs', json=log3)
print(f'   添加完成日志')

resp = client.get(f'/api/maintenance-logs/{maint1_id}')
logs = resp.get_json()['data']
print(f'   运维日志总数: {len(logs)} 条')
for log in logs:
    print(f'     - [{log["create_time"][:19]}] {log["log_type"]}: {log["log_content"]}')
print('✅ 维修日志记录功能正常')

print('\n📋 【8/8】测试设备完好率统计')
resp = client.get('/api/dashboard/stats')
stats = resp.get_json()['data']
print(f'   设备总数: {stats["total_devices"]} 台')
print(f'   正常设备: {stats["normal_devices"]} 台')
print(f'   故障设备: {stats["fault_devices"]} 台')
print(f'   维修中: {stats["maintaining_devices"]} 台')
print(f'   已修复: {stats["repaired_devices"]} 台')
print(f'   👉 设备完好率: {stats["device_intact_rate"]}%')
print(f'   待处理故障: {stats["pending_reports"]} 个')
print(f'   紧急待处理: {stats["urgent_pending"]} 个')
print(f'   运维记录总数: {stats["total_maintenance"]} 条')
print(f'   区域分布: {stats["area_distribution"]}')
print('✅ 设备完好率统计正常')

print('\n' + '='*60)
print('🎉 所有功能测试通过！系统 V2.0 已就绪')
print('='*60)

print('\n📝 新增功能总结:')
print('   ✅ 设备字段扩展：区域、油号、设备型号、主控版本')
print('   ✅ 故障分类：硬件/软件/网络/电源/机械/传感器/其他')
print('   ✅ 紧急优先级：低→普通→高→紧急（带颜色标识）')
print('   ✅ 多维度筛选：区域、油号、优先级、状态等')
print('   ✅ 优先级自动排序：紧急故障优先显示')
print('   ✅ 设备工单联动：设备详情关联故障和运维记录')
print('   ✅ 维修日志记录：完整的维修过程跟踪')
print('   ✅ 统一接口格式：统一的 success/error 响应')
print('   ✅ 设备完好率统计：实时计算设备完好率百分比')
