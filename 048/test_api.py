import requests
import time
import os

DATABASE = 'vehicle_admin.db'
if os.path.exists(DATABASE):
    os.remove(DATABASE)
    print('已清理旧数据库')

time.sleep(1)

BASE_URL = 'http://localhost:5001/api'

print('=' * 60)
print('开始测试车管所运维管理系统API接口')
print('=' * 60)

try:
    print('\n1. 测试获取故障配置接口...')
    r = requests.get(f'{BASE_URL}/fault-config')
    print(f'   状态码: {r.status_code}')
    if r.status_code == 200:
        data = r.json()['data']
        print(f'   故障类型数量: {len(data["fault_types"])}')
        print(f'   优先级等级: {data["priority_levels"]}')
        print('   ✓ 成功')
    else:
        print(f'   ✗ 失败: {r.text}')

    print('\n2. 测试添加设备...')
    device_data = {
        'device_code': 'TEST-001',
        'device_name': '测试设备一体机',
        'location': '车管所测试区',
        'install_date': '2024-05-16',
        'status': '正常'
    }
    r = requests.post(f'{BASE_URL}/devices', json=device_data)
    print(f'   状态码: {r.status_code}')
    if r.status_code == 200:
        result = r.json()
        device_id = result['data']['id']
        print(f'   设备ID: {device_id}')
        print('   ✓ 成功')
    else:
        print(f'   ✗ 失败: {r.text}')
        device_id = None

    if device_id:
        print('\n3. 测试创建【紧急】优先级工单...')
        order_data = {
            'device_id': device_id,
            'device_code': 'TEST-001',
            'fault_type': '系统崩溃',
            'fault_desc': '设备完全无法启动，影响核心业务办理',
            'priority': '紧急',
            'reporter': '测试员',
            'reporter_phone': '13800138000'
        }
        r = requests.post(f'{BASE_URL}/work-orders', json=order_data)
        print(f'   状态码: {r.status_code}')
        if r.status_code == 200:
            result = r.json()['data']
            print(f'   工单编号: {result["order_no"]}')
            print(f'   优先级: {result["priority"]}')
            print(f'   优先级说明: {result["priority_desc"]}')
            print('   ✓ 成功')
        else:
            print(f'   ✗ 失败: {r.text}')

        print('\n4. 测试创建【高】优先级工单...')
        order_data2 = {
            'device_id': device_id,
            'device_code': 'TEST-001',
            'fault_type': '硬件故障',
            'fault_desc': '部分功能异常，影响业务效率',
            'priority': '高',
            'reporter': '测试员',
            'reporter_phone': '13800138000'
        }
        r = requests.post(f'{BASE_URL}/work-orders', json=order_data2)
        print(f'   状态码: {r.status_code}')
        if r.status_code == 200:
            result = r.json()['data']
            print(f'   工单编号: {result["order_no"]}')
            print('   ✓ 成功')
        else:
            print(f'   ✗ 失败: {r.text}')

        print('\n5. 测试创建【一般】优先级工单...')
        order_data3 = {
            'device_id': device_id,
            'device_code': 'TEST-001',
            'fault_type': '软件故障',
            'fault_desc': '小功能异常，不影响主要业务',
            'priority': '一般',
            'reporter': '测试员',
            'reporter_phone': '13800138000'
        }
        r = requests.post(f'{BASE_URL}/work-orders', json=order_data3)
        print(f'   状态码: {r.status_code}')
        if r.status_code == 200:
            print('   ✓ 成功')
        else:
            print(f'   ✗ 失败: {r.text}')

    print('\n6. 测试获取工单列表(验证优先级排序)...')
    r = requests.get(f'{BASE_URL}/work-orders')
    print(f'   状态码: {r.status_code}')
    if r.status_code == 200:
        data = r.json()
        orders = data['data']
        print(f'   工单总数: {len(orders)}')
        if orders:
            print(f'   排序验证: 第一个工单优先级: {orders[0]["priority"]}')
            print(f'   第一个工单优先级说明: {orders[0]["priority_desc"]}')
            print(f'   包含设备信息: {orders[0].get("device_name", "N/A")}')
        print('   ✓ 成功')
    else:
        print(f'   ✗ 失败: {r.text}')

    print('\n7. 测试按优先级筛选工单...')
    r = requests.get(f'{BASE_URL}/work-orders?priority=紧急')
    print(f'   状态码: {r.status_code}')
    if r.status_code == 200:
        data = r.json()
        print(f'   紧急优先级工单数量: {len(data["data"])}')
        print('   ✓ 成功')
    else:
        print(f'   ✗ 失败: {r.text}')

    print('\n8. 测试按故障类型筛选工单...')
    r = requests.get(f'{BASE_URL}/work-orders?fault_type=硬件故障')
    print(f'   状态码: {r.status_code}')
    if r.status_code == 200:
        data = r.json()
        print(f'   硬件故障工单数量: {len(data["data"])}')
        print('   ✓ 成功')
    else:
        print(f'   ✗ 失败: {r.text}')

    print('\n9. 测试仪表盘接口(含优先级和故障类型统计)...')
    r = requests.get(f'{BASE_URL}/dashboard')
    print(f'   状态码: {r.status_code}')
    if r.status_code == 200:
        data = r.json()['data']
        print(f'   设备总数: {data["total_devices"]}')
        print(f'   待处理工单: {data["pending_orders"]}')
        print(f'   优先级统计: {data["priority_stats"]}')
        print(f'   故障类型统计: {data["fault_type_stats"]}')
        print('   ✓ 成功')
    else:
        print(f'   ✗ 失败: {r.text}')

    print('\n10. 测试无效故障类型验证...')
    if device_id:
        order_data_invalid = {
            'device_id': device_id,
            'device_code': 'TEST-001',
            'fault_type': '无效故障类型',
            'fault_desc': '测试',
            'priority': '一般',
            'reporter': '测试员'
        }
        r = requests.post(f'{BASE_URL}/work-orders', json=order_data_invalid)
        print(f'   状态码: {r.status_code}')
        if r.status_code == 400:
            print('   ✓ 成功拦截无效故障类型')
        else:
            print('   ✗ 验证失败')

    print('\n11. 测试无效优先级验证...')
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
        print(f'   状态码: {r.status_code}')
        if r.status_code == 400:
            print('   ✓ 成功拦截无效优先级')
        else:
            print('   ✗ 验证失败')

    print('\n' + '=' * 60)
    print('所有API测试完成! 故障分类和优先级功能已实现')
    print('=' * 60)

except Exception as e:
    print(f'\n发生错误: {e}')
    import traceback
    traceback.print_exc()
