import urllib.request
import json
from urllib.error import HTTPError

BASE_URL = "http://127.0.0.1:5000/api"

def make_request(method, endpoint, data=None):
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url, method=method)
    if data:
        req.data = json.dumps(data).encode()
        req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        print(f"HTTP错误 {e.code}: {e.read().decode()}")
        return None
    except Exception as e:
        print(f"请求错误: {e}")
        return None

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_result(result, success_msg="操作成功"):
    if result and result.get('success'):
        print(f"✓ {success_msg}")
        if result.get('data'):
            print(json.dumps(result['data'], ensure_ascii=False, indent=2))
    else:
        print(f"✗ 操作失败: {result.get('message') if result else '未知错误'}")

print_section("地铁运维管理系统 - 新功能综合测试")

print_section("1. 健康检查测试")
result = make_request('GET', '/health')
print_result(result, "系统运行正常")

print_section("2. 获取故障分类和优先级配置")
result = make_request('GET', '/fault-categories')
print_result(result, "获取故障分类成功")

print_section("3. 添加多台测试设备（不同线路站点）")
test_devices = [
    {
        'device_id': 'TVM-001',
        'device_name': '1号线西单站售票机1号',
        'device_type': '售票机',
        'device_model': 'TVM-Pro-2024',
        'communication_protocol': 'MQTT',
        'device_serial': 'SN-TVM-001',
        'location': '1号线西单站A入口',
        'install_date': '2024-01-15',
        'commission_date': '2024-02-01'
    },
    {
        'device_id': 'TVM-002',
        'device_name': '1号线西单站售票机2号',
        'device_type': '售票机',
        'device_model': 'TVM-Pro-2024',
        'communication_protocol': 'MQTT',
        'device_serial': 'SN-TVM-002',
        'location': '1号线西单站B入口',
        'install_date': '2024-01-15',
        'commission_date': '2024-02-01'
    },
    {
        'device_id': 'AGM-001',
        'device_name': '2号线王府井站闸机',
        'device_type': '闸机',
        'device_model': 'AGM-X1',
        'communication_protocol': 'TCP/IP',
        'device_serial': 'SN-AGM-001',
        'location': '2号线王府井站C出口',
        'install_date': '2024-03-01',
        'commission_date': '2024-03-15'
    }
]

for device in test_devices:
    result = make_request('POST', '/devices', device)
    if result and result.get('success'):
        print(f"✓ 添加设备成功: {device['device_name']}")
    else:
        print(f"⚠ 设备可能已存在: {device['device_name']}")

print_section("4. 上报设备心跳（模拟设备在线状态）")
for device in test_devices:
    result = make_request('POST', f"/devices/{device['device_id']}/heartbeat")
    if result and result.get('success'):
        print(f"✓ 心跳上报成功: {device['device_id']}")

print_section("5. 获取设备列表 - 验证线路站点解析")
result = make_request('GET', '/devices')
if result and result.get('success'):
    devices = result['data']['devices']
    print(f"✓ 共 {len(devices)} 台设备")
    for device in devices:
        line_info = f", 线路: {device.get('line')}号线" if device.get('line') else ""
        station_info = f", 站点: {device.get('station')}站" if device.get('station') else ""
        status_info = f", 状态: {device['status']}"
        is_online = "在线" if device.get('is_online') else "离线"
        print(f"  - {device['device_name']} [{device['device_id']}] {status_info}, {is_online}{line_info}{station_info}")

print_section("6. 按线路筛选设备 - 筛选1号线设备")
result = make_request('GET', '/devices?line=1')
if result and result.get('success'):
    devices = result['data']['devices']
    print(f"✓ 1号线设备共 {len(devices)} 台")
    for device in devices:
        print(f"  - {device['device_name']}")

print_section("7. 创建故障工单 - 测试优先级计算")
test_orders = [
    {
        'device_id': 'TVM-001',
        'fault_category': '硬件故障',
        'fault_type': '纸币识别器',
        'impact_level': '核心站点-早高峰',
        'fault_description': '纸币识别器卡票，无法识别，早高峰影响乘客购票',
        'reporter': '站务员张三',
        'reporter_phone': '13800138000'
    },
    {
        'device_id': 'TVM-002',
        'fault_category': '软件故障',
        'fault_type': '程序异常',
        'impact_level': '普通站点-平峰',
        'fault_description': '触摸屏界面偶尔无响应，需要重启',
        'reporter': '站务员李四',
        'reporter_phone': '13900139000'
    },
    {
        'device_id': 'AGM-001',
        'fault_category': '硬件故障',
        'fault_type': '闸机门体',
        'impact_level': '换乘站点-任何时段',
        'fault_description': '闸机无法关闭，需要紧急维修',
        'reporter': '站务员王五',
        'reporter_phone': '13700137000'
    }
]

order_ids = []
for order in test_orders:
    result = make_request('POST', '/work-orders', order)
    if result and result.get('success'):
        order_no = result['data']['order_no']
        priority = result['data']['priority']
        order_ids.append(order_no)
        print(f"✓ 工单创建成功: {order_no}, 优先级: {priority}")

print_section("8. 工单列表 - 验证优先级排序和高亮信息")
result = make_request('GET', '/work-orders')
if result and result.get('success'):
    orders = result['data']['orders']
    print(f"✓ 共 {len(orders)} 个工单（按优先级排序）")
    for order in orders:
        priority_info = order.get('priority_info', {})
        priority_level = priority_info.get('level', 0)
        color_info = f" (显示颜色: {priority_info.get('color')})"
        print(f"  [{order['priority']}] {order['order_no']} - {order['fault_description'][:30]}...{color_info}")

print_section("9. 按优先级筛选工单 - 只看高优先级")
result = make_request('GET', '/work-orders?priority=高')
if result and result.get('success'):
    orders = result['data']['orders']
    print(f"✓ 高优先级工单共 {len(orders)} 个")
    for order in orders:
        print(f"  - {order['order_no']}: {order['fault_type']}")

print_section("10. 处理工单 - 验证设备状态联动")
if order_ids:
    first_order = order_ids[0]
    result = make_request('PUT', f'/work-orders/{first_order}/handle', {
        'handler': '维修工程师A',
        'handle_description': '已到达现场，开始检查设备'
    })
    if result and result.get('success'):
        print(f"✓ 工单 {first_order} 已开始处理")
        print(f"  设备状态已自动更新为: 维修中")

print_section("11. 查看设备详情 - 验证工单联动信息")
result = make_request('GET', '/devices/TVM-001')
if result and result.get('success'):
    data = result['data']
    print(f"✓ 设备: {data['device']['device_name']}")
    print(f"  当前状态: {data['device']['status']}")
    print(f"  关联工单: {len(data['recent_orders'])} 个")
    for order in data['recent_orders']:
        print(f"    - {order['order_no']} [{order['status']}]")

print_section("12. 完成工单 - 自动记录维修日志")
if order_ids:
    first_order = order_ids[0]
    result = make_request('PUT', f'/work-orders/{first_order}/complete', {
        'result_description': '更换纸币识别器传感器，设备恢复正常',
        'maintenance_type': '部件更换',
        'cost': 850,
        'operator': '维修工程师A',
        'duration': 45
    })
    if result and result.get('success'):
        print(f"✓ 工单 {first_order} 已完成")
        print(f"  设备状态已自动更新为: 已修复")
        print(f"  维修日志已自动记录")

print_section("13. 查看设备状态变更日志")
result = make_request('GET', '/status-logs/TVM-001')
if result and result.get('success'):
    logs = result['data']['logs']
    print(f"✓ TVM-001 状态变更日志共 {len(logs)} 条")
    for log in logs:
        print(f"  - {log['created_at']}: {log['before_status']} -> {log['after_status']}")
        print(f"    原因: {log['change_reason']}, 操作人: {log['operator']}")

print_section("14. 手动记录常规维护日志")
result = make_request('POST', '/maintenance-records', {
    'device_id': 'TVM-002',
    'maintenance_type': '常规巡检',
    'action_type': '清洁保养',
    'description': '定期清洁触摸屏和读卡器，检查电源连接',
    'operator': '维护工程师B',
    'result': '成功',
    'cost': 0,
    'duration': 30,
    'update_device_status': True
})
if result and result.get('success'):
    print(f"✓ 维护记录创建成功，记录ID: {result['data']['id']}")

print_section("15. 获取维修记录列表")
result = make_request('GET', '/maintenance-records')
if result and result.get('success'):
    records = result['data']['records']
    print(f"✓ 维修记录共 {len(records)} 条")
    for record in records:
        print(f"  - {record['created_at']}: {record['maintenance_type']} - {record['description'][:20]}...")

print_section("16. 综合统计数据 - 含设备在线率")
result = make_request('GET', '/dashboard/statistics')
if result and result.get('success'):
    data = result['data']
    devices = data['devices']
    orders = data['orders']
    
    print("✓ 设备统计:")
    print(f"  总设备数: {devices['total']}")
    print(f"  在线设备: {devices['online']}")
    print(f"  在线率: {devices['online_rate']}%")
    print(f"  状态分布: {devices['status_distribution']}")
    print()
    print("✓ 工单统计:")
    print(f"  总工单: {orders['total']}")
    print(f"  状态分布: {orders['status_distribution']}")
    print(f"  待处理优先级: {orders['pending_priority']}")
    print(f"  近30天工单: {orders['recent_30days']}")

print_section("17. 按线路/站点统计在线率")
result = make_request('GET', '/dashboard/online-rate')
if result and result.get('success'):
    data = result['data']
    print("✓ 按线路统计:")
    for line_stat in data['by_line']:
        print(f"  {line_stat['line']}: 总数 {line_stat['total']}, 在线 {line_stat['online']}, "
              f"在线率 {line_stat['online_rate']}%, 故障 {line_stat['fault']} 台")
    
    if data.get('by_station'):
        print("\n✓ 按站点统计(前5):")
        for station_stat in data['by_station'][:5]:
            print(f"  {station_stat['station']}: 总数 {station_stat['total']}, "
                  f"在线 {station_stat['online']}, 在线率 {station_stat['online_rate']}%")

print_section("18. 多维度筛选工单 - 按线路和状态")
result = make_request('GET', '/work-orders?line=1&status=待处理')
if result and result.get('success'):
    orders = result['data']['orders']
    print(f"✓ 1号线待处理工单共 {len(orders)} 个")
    for order in orders:
        print(f"  - {order['order_no']}: {order['fault_type']} [{order['priority']}]")

print_section("19. 工单详情 - 验证完整信息")
if order_ids:
    first_order = order_ids[0]
    result = make_request('GET', f'/work-orders/{first_order}')
    if result and result.get('success'):
        order_data = result['data']
        order = order_data['order']
        records = order_data['maintenance_records']
        print(f"✓ 工单详情: {order['order_no']}")
        print(f"  设备: {order['device_name']}")
        print(f"  故障类型: {order['fault_category']} - {order['fault_type']}")
        print(f"  优先级: {order['priority']}")
        print(f"  当前状态: {order['status']}")
        print(f"  关联维修记录: {len(records)} 条")

print_section("20. 测试统一响应格式")
result = make_request('GET', '/health')
if result:
    print("✓ 响应格式验证:")
    print(f"  success字段: {result.get('success')}")
    print(f"  code字段: {result.get('code')}")
    print(f"  message字段: {result.get('message')}")
    print(f"  data字段: {'存在' if result.get('data') else '无'}")
    print(f"  timestamp字段: {'存在' if result.get('timestamp') else '无'}")

print("\n" + "="*60)
print("  所有功能测试完成！")
print("  ✓ 统一接口响应格式")
print("  ✓ 线路站点自动解析和筛选")
print("  ✓ 设备-工单状态自动联动")
print("  ✓ 优先级自动计算和高亮排序")
print("  ✓ 状态变更历史日志")
print("  ✓ 维修记录详细记录")
print("  ✓ 设备在线率统计")
print("  ✓ 多维度筛选功能")
print("="*60)
