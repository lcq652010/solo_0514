import requests
import os

if os.path.exists('vehicle_admin.db'):
    os.remove('vehicle_admin.db')
    print('已清理旧数据库')

BASE_URL = 'http://localhost:5001/api'

print('=' * 70)
print('车管所运维管理系统 V2 功能测试')
print('=' * 70)

try:
    print('\n【1】获取系统配置')
    r = requests.get(f'{BASE_URL}/config')
    if r.status_code == 200:
        data = r.json()['data']
        print(f'    故障类型: {len(data["fault_types"])} 种')
        print(f'    优先级: {data["priority_levels"]}')
        print(f'    网点数量: {len(data["branch_list"])} 个')
        print(f'    工单状态: {data["order_status_list"]}')
        print('    [OK] 成功')
    else:
        print(f'    [FAIL] {r.text}')

    print('\n【2】添加设备（含网点）')
    devices = [
        {
            'device_code': 'TEST-001',
            'device_name': '测试设备1号',
            'location': '一楼大厅',
            'branch': '车管所一楼大厅',
            'install_date': '2024-05-16',
            'status': '正常'
        },
        {
            'device_code': 'TEST-002',
            'device_name': '测试设备2号',
            'location': 'A网点',
            'branch': '车管所A网点',
            'install_date': '2024-05-16',
            'status': '正常'
        }
    ]
    device_ids = []
    for device in devices:
        r = requests.post(f'{BASE_URL}/devices', json=device)
        if r.status_code == 200:
            device_ids.append(r.json()['data']['id'])
            print(f'    {device["device_code"]} ({device["branch"]}) [OK]')
        else:
            print(f'    {device["device_code"]} [FAIL]')

    if device_ids:
        print('\n【3】创建不同优先级的工单')
        orders = [
            {
                'device_id': device_ids[0],
                'device_code': 'TEST-001',
                'fault_type': '系统崩溃',
                'fault_desc': '设备完全无法启动，核心业务停滞',
                'priority': '紧急',
                'reporter': '测试员',
                'reporter_phone': '13800138000'
            },
            {
                'device_id': device_ids[1],
                'device_code': 'TEST-002',
                'fault_type': '硬件故障',
                'fault_desc': '读卡器异常，影响A网点业务',
                'priority': '高',
                'reporter': '测试员',
                'reporter_phone': '13900139000'
            },
            {
                'device_id': device_ids[0],
                'device_code': 'TEST-001',
                'fault_type': '软件故障',
                'fault_desc': '字体显示问题，不影响使用',
                'priority': '一般',
                'reporter': '测试员',
                'reporter_phone': '13700137000'
            }
        ]
        for order in orders:
            r = requests.post(f'{BASE_URL}/work-orders', json=order)
            if r.status_code == 200:
                data = r.json()['data']
                print(f'    {data["order_no"]} [{order["priority"]}] [OK]')
            else:
                print(f'    [FAIL] {r.text}')

    print('\n【4】按网点筛选工单')
    r = requests.get(f'{BASE_URL}/work-orders?branch=车管所A网点')
    if r.status_code == 200:
        data = r.json()['data']
        print(f'    A网点工单数量: {data["total"]}')
        if data['list']:
            print(f'    工单设备: {data["list"][0]["device_name"]}')
        print('    [OK] 成功')
    else:
        print(f'    [FAIL] {r.text}')

    print('\n【5】按优先级筛选工单')
    r = requests.get(f'{BASE_URL}/work-orders?priority=紧急')
    if r.status_code == 200:
        data = r.json()['data']
        print(f'    紧急工单数量: {data["total"]}')
        if data['list']:
            print(f'    优先级说明: {data["list"][0]["priority_desc"]}')
        print('    [OK] 成功')
    else:
        print(f'    [FAIL] {r.text}')

    print('\n【6】按故障类型筛选工单')
    r = requests.get(f'{BASE_URL}/work-orders?fault_type=硬件故障')
    if r.status_code == 200:
        data = r.json()['data']
        print(f'    硬件故障工单数量: {data["total"]}')
        print('    [OK] 成功')
    else:
        print(f'    [FAIL] {r.text}')

    print('\n【7】工单优先级排序验证')
    r = requests.get(f'{BASE_URL}/work-orders')
    if r.status_code == 200:
        data = r.json()['data']
        if data['list']:
            priorities = [item['priority'] for item in data['list']]
            print(f'    排序后的优先级: {priorities}')
            print(f'    第一个优先级应为"紧急": {priorities[0] == "紧急"}')
        print('    [OK] 成功')
    else:
        print(f'    [FAIL] {r.text}')

    print('\n【8】仪表盘统计（含设备完好率）')
    r = requests.get(f'{BASE_URL}/dashboard')
    if r.status_code == 200:
        data = r.json()['data']
        print(f'    设备总数: {data["total_devices"]}')
        print(f'    设备完好率: {data["device_health_rate"]}%')
        print(f'    待处理工单: {data["pending_orders"]}')
        print(f'    处理中工单: {data["processing_orders"]}')
        print(f'    已完成工单: {data["completed_orders"]}')
        print(f'    优先级统计: {data["priority_stats"]}')
        print(f'    各网点设备统计:')
        for branch, stats in data['branch_stats'].items():
            if stats['total'] > 0:
                print(f'      {branch}: {stats["total"]}台, 完好率: {stats["health_rate"]}%')
        print('    [OK] 成功')
    else:
        print(f'    [FAIL] {r.text}')

    print('\n【9】处理工单（状态联动）')
    if device_ids:
        r = requests.get(f'{BASE_URL}/work-orders')
        if r.status_code == 200:
            orders = r.json()['data']['list']
            if orders:
                order_id = orders[0]['id']
                handle_data = {
                    'handle_user': '系统管理员',
                    'handle_desc': '已更换硬件模块',
                    'status': '处理中'
                }
                r = requests.put(f'{BASE_URL}/work-orders/{order_id}/handle', json=handle_data)
                if r.status_code == 200:
                    print('    工单处理成功 [OK]')
                    
                    r = requests.get(f'{BASE_URL}/devices/{orders[0]["device_id"]}')
                    if r.status_code == 200:
                        device_status = r.json()['data']['status']
                        print(f'    设备状态联动更新为: {device_status}')
                        print('    [OK] 状态联动成功')
                else:
                    print(f'    [FAIL] {r.text}')

    print('\n【10】按网点筛选设备')
    r = requests.get(f'{BASE_URL}/devices?branch=车管所A网点')
    if r.status_code == 200:
        data = r.json()['data']
        print(f'    A网点设备数量: {len(data)}')
        print('    [OK] 成功')
    else:
        print(f'    [FAIL] {r.text}')

    print('\n【11】统一响应格式验证')
    r = requests.get(f'{BASE_URL}/devices')
    if r.status_code == 200:
        data = r.json()
        has_code = 'code' in data
        has_message = 'message' in data
        has_timestamp = 'timestamp' in data
        print(f'    包含code: {has_code}')
        print(f'    包含message: {has_message}')
        print(f'    包含timestamp: {has_timestamp}')
        if all([has_code, has_message, has_timestamp]):
            print('    [OK] 响应格式统一')

    print('\n' + '=' * 70)
    print('所有 V2 新功能测试完成!')
    print('=' * 70)

except Exception as e:
    print(f'\n错误: {e}')
    import traceback
    traceback.print_exc()
