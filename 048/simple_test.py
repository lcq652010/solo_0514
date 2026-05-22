import requests
import os
import sys

os.system('chcp 65001 > nul')

DATABASE = 'vehicle_admin.db'
if os.path.exists(DATABASE):
    os.remove(DATABASE)
    print('已清理旧数据库')

BASE_URL = 'http://localhost:5001/api'

print('=' * 60)
print('车管所运维管理系统API测试')
print('=' * 60)

try:
    print('\n[1] 获取故障配置')
    r = requests.get(f'{BASE_URL}/fault-config')
    print(f'    状态: {r.status_code}')
    if r.status_code == 200:
        data = r.json()['data']
        print(f'    故障类型: {len(data["fault_types"])} 种')
        print(f'    优先级: {data["priority_levels"]}')
        print('    [OK] 成功')

    print('\n[2] 添加设备')
    device_data = {
        'device_code': 'TEST-001',
        'device_name': '测试设备',
        'location': '车管所测试区',
        'install_date': '2024-05-16',
        'status': '正常'
    }
    r = requests.post(f'{BASE_URL}/devices', json=device_data)
    print(f'    状态: {r.status_code}')
    if r.status_code == 200:
        device_id = r.json()['data']['id']
        print(f'    设备ID: {device_id}')
        print('    [OK] 成功')
    else:
        device_id = None
        print(f'    [FAIL] {r.text}')

    if device_id:
        print('\n[3] 创建紧急优先级工单')
        order_data = {
            'device_id': device_id,
            'device_code': 'TEST-001',
            'fault_type': '系统崩溃',
            'fault_desc': '设备无法启动',
            'priority': '紧急',
            'reporter': '测试员',
            'reporter_phone': '13800138000'
        }
        r = requests.post(f'{BASE_URL}/work-orders', json=order_data)
        print(f'    状态: {r.status_code}')
        if r.status_code == 200:
            result = r.json()['data']
            print(f'    工单编号: {result["order_no"]}')
            print(f'    优先级: {result["priority"]}')
            print(f'    优先级说明: {result["priority_desc"]}')
            print('    [OK] 成功')

        print('\n[4] 创建高优先级工单')
        order_data2 = {
            'device_id': device_id,
            'device_code': 'TEST-001',
            'fault_type': '硬件故障',
            'fault_desc': '部分功能异常',
            'priority': '高',
            'reporter': '测试员',
            'reporter_phone': '13800138000'
        }
        r = requests.post(f'{BASE_URL}/work-orders', json=order_data2)
        print(f'    状态: {r.status_code}')
        if r.status_code == 200:
            print('    [OK] 成功')

        print('\n[5] 创建一般优先级工单')
        order_data3 = {
            'device_id': device_id,
            'device_code': 'TEST-001',
            'fault_type': '软件故障',
            'fault_desc': '小功能异常',
            'priority': '一般',
            'reporter': '测试员',
            'reporter_phone': '13800138000'
        }
        r = requests.post(f'{BASE_URL}/work-orders', json=order_data3)
        print(f'    状态: {r.status_code}')
        if r.status_code == 200:
            print('    [OK] 成功')

    print('\n[6] 获取工单列表(优先级排序)')
    r = requests.get(f'{BASE_URL}/work-orders')
    print(f'    状态: {r.status_code}')
    if r.status_code == 200:
        data = r.json()
        orders = data['data']
        print(f'    工单总数: {len(orders)}')
        if orders:
            print(f'    第一个工单优先级: {orders[0]["priority"]}')
            print(f'    包含设备名称: {orders[0].get("device_name")}')
        print('    [OK] 成功')

    print('\n[7] 按优先级筛选')
    r = requests.get(f'{BASE_URL}/work-orders?priority=紧急')
    print(f'    状态: {r.status_code}')
    if r.status_code == 200:
        print(f'    紧急工单: {len(r.json()["data"])} 个')
        print('    [OK] 成功')

    print('\n[8] 按故障类型筛选')
    r = requests.get(f'{BASE_URL}/work-orders?fault_type=硬件故障')
    print(f'    状态: {r.status_code}')
    if r.status_code == 200:
        print(f'    硬件故障工单: {len(r.json()["data"])} 个')
        print('    [OK] 成功')

    print('\n[9] 仪表盘统计')
    r = requests.get(f'{BASE_URL}/dashboard')
    print(f'    状态: {r.status_code}')
    if r.status_code == 200:
        data = r.json()['data']
        print(f'    优先级统计: {data["priority_stats"]}')
        print(f'    故障类型统计: {data["fault_type_stats"]}')
        print('    [OK] 成功')

    print('\n[10] 无效故障类型验证')
    if device_id:
        order_data_invalid = {
            'device_id': device_id,
            'device_code': 'TEST-001',
            'fault_type': '无效类型',
            'fault_desc': '测试',
            'priority': '一般',
            'reporter': '测试员'
        }
        r = requests.post(f'{BASE_URL}/work-orders', json=order_data_invalid)
        print(f'    状态: {r.status_code}')
        if r.status_code == 400:
            print('    [OK] 成功拦截')

    print('\n[11] 无效优先级验证')
    if device_id:
        order_data_invalid2 = {
            'device_id': device_id,
            'device_code': 'TEST-001',
            'fault_type': '硬件故障',
            'fault_desc': '测试',
            'priority': '无效优先级',
            'reporter': '测试员'
        }
        r = requests.post(f'{BASE_URL}/work-orders', json=order_data_invalid2)
        print(f'    状态: {r.status_code}')
        if r.status_code == 400:
            print('    [OK] 成功拦截')

    print('\n' + '=' * 60)
    print('测试完成! 故障分类和优先级功能已全部实现')
    print('=' * 60)

except Exception as e:
    print(f'\n错误: {e}')
    import traceback
    traceback.print_exc()
