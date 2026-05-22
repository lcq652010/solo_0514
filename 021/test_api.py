import requests
import json
import time

BASE_URL = 'http://localhost:5000/api'

def print_response(title, response):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    data = response.json()
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return data

def test_get_constants():
    print("\n" + "="*60)
    print("  1. 获取系统常量")
    print("="*60)
    
    response = requests.get(f'{BASE_URL}/constants')
    return print_response("系统常量", response)

def test_device_management():
    print("\n" + "="*60)
    print("  2. 设备管理测试")
    print("="*60)
    
    devices = []
    
    device_data1 = {
        'device_code': 'BDC-001',
        'device_name': '不动产自助打证终端A',
        'device_model': 'HP-ZT2024',
        'location': '1号窗口旁',
        'hall_area': '一楼大厅',
        'communication_mode': '专网',
        'install_date': '2024-01-15',
        'commission_date': '2024-02-01'
    }
    response = requests.post(f'{BASE_URL}/devices', json=device_data1)
    print_response("创建设备1", response)
    devices.append(response.json()['data'])
    
    device_data2 = {
        'device_code': 'BDC-002',
        'device_name': '不动产自助打证终端B',
        'device_model': 'HP-ZT2024-Pro',
        'location': '2号窗口旁',
        'hall_area': 'VIP服务区',
        'communication_mode': '以太网',
        'install_date': '2024-02-20',
        'commission_date': '2024-03-10'
    }
    response = requests.post(f'{BASE_URL}/devices', json=device_data2)
    print_response("创建设备2", response)
    devices.append(response.json()['data'])
    
    device_data3 = {
        'device_code': 'BDC-003',
        'device_name': '不动产自助打证终端C',
        'device_model': 'HP-ZT2024-Pro',
        'location': '入口处',
        'hall_area': '24小时自助区',
        'communication_mode': '5G',
        'install_date': '2024-03-01',
        'commission_date': '2024-03-15'
    }
    response = requests.post(f'{BASE_URL}/devices', json=device_data3)
    print_response("创建设备3", response)
    devices.append(response.json()['data'])
    
    response = requests.get(f'{BASE_URL}/devices')
    data = print_response("获取所有设备", response)
    
    response = requests.get(f'{BASE_URL}/devices', params={'hall_area': '一楼大厅'})
    print_response("按区域筛选 - 一楼大厅", response)
    
    response = requests.get(f'{BASE_URL}/devices', params={'status': '正常'})
    print_response("按状态筛选 - 正常", response)
    
    response = requests.get(f'{BASE_URL}/devices/1')
    print_response("获取设备1详情(含工单记录)", response)
    
    response = requests.put(f'{BASE_URL}/devices/1', json={
        'device_model': 'HP-ZT2024-ProMax',
        'location': 'VIP专属位置'
    })
    print_response("更新设备信息", response)
    
    return data['data']['list']

def test_work_order_with_priority(devices):
    print("\n" + "="*60)
    print("  3. 故障工单测试（含优先级和区域）")
    print("="*60)
    
    orders = []
    
    work_order_data1 = {
        'device_id': devices[0]['id'],
        'fault_type': 'printer',
        'urgency_level': 'high',
        'fault_description': '打印机完全不工作，证书无法打印，严重影响窗口业务',
        'reporter': '张三',
        'reporter_phone': '13800138000'
    }
    response = requests.post(f'{BASE_URL}/work-orders', json=work_order_data1)
    data = print_response("上报高优先级打印故障", response)
    orders.append(data['data'])
    
    work_order_data2 = {
        'device_id': devices[1]['id'],
        'fault_type': 'network',
        'urgency_level': 'medium',
        'fault_description': '网络连接不稳定，偶尔断开，影响业务办理速度',
        'reporter': '李四',
        'reporter_phone': '13900139000'
    }
    response = requests.post(f'{BASE_URL}/work-orders', json=work_order_data2)
    data = print_response("上报中优先级网络故障", response)
    orders.append(data['data'])
    
    work_order_data3 = {
        'device_id': devices[2]['id'],
        'fault_type': 'touchscreen',
        'urgency_level': 'low',
        'fault_description': '触摸屏边缘部分不灵敏，不影响主要功能使用',
        'reporter': '王五',
        'reporter_phone': '13700137000'
    }
    response = requests.post(f'{BASE_URL}/work-orders', json=work_order_data3)
    data = print_response("上报低优先级触摸屏故障", response)
    orders.append(data['data'])
    
    response = requests.get(f'{BASE_URL}/work-orders')
    data = print_response("获取所有工单（按优先级排序，高优在前）", response)
    
    response = requests.get(f'{BASE_URL}/work-orders', params={'urgency_level': 'high'})
    print_response("按紧急级别筛选 - 高优先级", response)
    
    response = requests.get(f'{BASE_URL}/work-orders', params={'hall_area': '一楼大厅'})
    print_response("按区域筛选 - 一楼大厅", response)
    
    response = requests.get(f'{BASE_URL}/work-orders', params={'status': '待处理'})
    print_response("按状态筛选 - 待处理", response)
    
    return orders

def test_work_order_handling(orders):
    print("\n" + "="*60)
    print("  4. 工单处理测试（含维修日志）")
    print("="*60)
    
    order_id = orders[0]['id']
    
    response = requests.put(f'{BASE_URL}/work-orders/{order_id}/handle', json={
        'status': '处理中',
        'handler': '李工程师',
        'handle_description': '已到达现场，正在检查打印机硬件'
    })
    print_response("开始处理工单", response)
    
    response = requests.post(f'{BASE_URL}/work-orders/{order_id}/logs', json={
        'log_type': 'progress',
        'content': '已拆下打印机主板，发现电路板有烧毁痕迹，正在联系供应商申请配件',
        'operator': '李工程师'
    })
    print_response("添加维修进度日志", response)
    
    response = requests.post(f'{BASE_URL}/work-orders/{order_id}/logs', json={
        'log_type': 'progress',
        'content': '配件已送到，正在更换主板',
        'operator': '李工程师'
    })
    print_response("添加第二条维修日志", response)
    
    response = requests.put(f'{BASE_URL}/work-orders/{order_id}/handle', json={
        'status': '已完成',
        'handler': '李工程师',
        'handle_description': '已更换打印机主板，设备恢复正常使用，经测试打印功能正常'
    })
    print_response("完成工单处理", response)
    
    response = requests.get(f'{BASE_URL}/work-orders/{order_id}')
    print_response("查看工单详情（含设备信息和维修日志）", response)
    
    response = requests.get(f'{BASE_URL}/devices/1')
    print_response("查看设备1状态（应已更新为已修复）", response)

def test_device_work_order_link(devices):
    print("\n" + "="*60)
    print("  5. 设备工单联动测试")
    print("="*60)
    
    response = requests.get(f'{BASE_URL}/devices/{devices[0]["id"]}/work-orders')
    print_response("获取设备1的所有工单", response)
    
    response = requests.get(f'{BASE_URL}/devices/{devices[0]["id"]}/work-orders', params={'status': '已完成'})
    print_response("获取设备1的已完成工单", response)

def test_maintenance_records():
    print("\n" + "="*60)
    print("  6. 运维记录测试")
    print("="*60)
    
    record_data = {
        'device_id': 2,
        'maintenance_type': '日常巡检',
        'description': '清洁设备外观，检查系统运行状态，更新杀毒软件，检查网络连接',
        'parts_used': '无',
        'operator': '王技术员',
        'duration_minutes': 30
    }
    response = requests.post(f'{BASE_URL}/maintenance-records', json=record_data)
    print_response("创建日常巡检记录", response)
    
    response = requests.get(f'{BASE_URL}/maintenance-records')
    print_response("获取所有运维记录", response)

def test_dashboard_enhanced():
    print("\n" + "="*60)
    print("  7. 仪表盘统计测试（含完好率和区域统计）")
    print("="*60)
    
    response = requests.get(f'{BASE_URL}/dashboard')
    data = response.json()
    print(json.dumps(data, ensure_ascii=False, indent=2))
    
    print(f"\n{'='*60}")
    print("  数据解读")
    print(f"{'='*60}")
    print(f"  设备总数: {data['data']['devices']['total']}")
    print(f"  设备完好率: {data['data']['devices']['availability_rate']}%")
    print(f"  各状态分布: {data['data']['devices']['by_status']}")
    print(f"\n  工单总数: {data['data']['work_orders']['total']}")
    print(f"  高优先级工单: {data['data']['work_orders']['high_urgency']}")
    print(f"  今日新增: {data['data']['work_orders']['today_new']}")
    print(f"  今日完成: {data['data']['work_orders']['today_completed']}")
    print(f"\n  各区域统计:")
    for area, stats in data['data']['by_area'].items():
        print(f"    - {area}: 设备{stats['device_count']}台, 完好率{stats['availability_rate']}%, 待处理{stats['pending_orders']}单")

def test_pagination():
    print("\n" + "="*60)
    print("  8. 分页功能测试")
    print("="*60)
    
    response = requests.get(f'{BASE_URL}/work-orders', params={'page': 1, 'page_size': 2})
    data = print_response("工单列表分页-第1页", response)
    
    print(f"\n  分页信息:")
    print(f"    当前页: {data['data']['pagination']['page']}")
    print(f"    每页大小: {data['data']['pagination']['page_size']}")
    print(f"    总记录数: {data['data']['pagination']['total']}")
    print(f"    总页数: {data['data']['pagination']['total_pages']}")

if __name__ == '__main__':
    try:
        print("\n" + "="*60)
        print("  政务不动产自助打证终端运维管理系统")
        print("  完整版功能测试")
        print("="*60)
        
        test_get_constants()
        devices = test_device_management()
        orders = test_work_order_with_priority(devices)
        test_work_order_handling(orders)
        test_device_work_order_link(devices)
        test_maintenance_records()
        test_dashboard_enhanced()
        test_pagination()
        
        print("\n" + "="*60)
        print("  所有测试完成！")
        print("="*60)
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到服务器，请先运行 app.py 启动服务！")
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
