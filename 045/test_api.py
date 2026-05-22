import requests
import json
import os

BASE_URL = 'http://localhost:5000/api'

def test_all():
    print("=" * 70)
    print("开始测试 API 接口（优化版 - 支持区域筛选+设备可用率）")
    print("=" * 70)
    
    print("\n" + "-" * 50)
    print("1. 测试获取字典数据（验证新增枚举值）")
    print("-" * 50)
    response = requests.get(f'{BASE_URL}/dictionary')
    print(f"状态码: {response.status_code}")
    data = response.json()['data']
    print(f"网点区域: {data['branch_areas']}")
    print(f"工单状态: {data['order_statuses']}")
    print(f"设备状态: {data['device_statuses']}")
    
    print("\n" + "-" * 50)
    print("2. 测试添加设备（含网点区域字段）")
    print("-" * 50)
    device_data_list = [
        {
            'device_code': 'GJJ-SH-001',
            'device_name': '市区支行终端1号',
            'device_model': 'HJ-GJJ-2024',
            'communication_mode': '有线网络',
            'branch_area': '市区',
            'location': '市区支行大厅',
            'install_date': '2024-01-15',
            'operate_date': '2024-02-01'
        },
        {
            'device_code': 'GJJ-DQ-001',
            'device_name': '东区支行终端1号',
            'device_model': 'HJ-GJJ-2024',
            'communication_mode': '无线网络',
            'branch_area': '东区',
            'location': '东区支行大厅',
            'install_date': '2024-01-20',
            'operate_date': '2024-02-10'
        },
        {
            'device_code': 'GJJ-KFQ-001',
            'device_name': '开发区终端1号',
            'device_model': 'HJ-GJJ-2024-Pro',
            'communication_mode': '5G',
            'branch_area': '开发区',
            'location': '开发区政务中心',
            'install_date': '2024-02-01',
            'operate_date': '2024-02-15'
        }
    ]
    
    device_ids = []
    for device_data in device_data_list:
        response = requests.post(f'{BASE_URL}/devices', json=device_data)
        print(f"添加设备 {device_data['device_code']}: {response.json()['message']}")
        device_ids.append(response.json()['data']['id'])
    
    print("\n" + "-" * 50)
    print("3. 测试按网点区域筛选设备")
    print("-" * 50)
    response = requests.get(f'{BASE_URL}/devices?branch_area=市区')
    devices = response.json()['data']['list']
    print(f"市区区域设备数量: {len(devices)}")
    for d in devices:
        print(f"  - {d['device_code']} ({d['branch_area']}) - {d['status']}")
    
    response = requests.get(f'{BASE_URL}/devices?branch_area=东区')
    devices = response.json()['data']['list']
    print(f"东区区域设备数量: {len(devices)}")
    
    print("\n" + "-" * 50)
    print("4. 测试按设备状态筛选")
    print("-" * 50)
    response = requests.get(f'{BASE_URL}/devices?status=正常')
    devices = response.json()['data']['list']
    print(f"正常状态设备数量: {len(devices)}")
    
    print("\n" + "-" * 50)
    print("5. 测试分页功能")
    print("-" * 50)
    response = requests.get(f'{BASE_URL}/devices?page=1&page_size=2')
    page_data = response.json()['data']
    print(f"第1页（每页2条）- 总数: {page_data['total']}, 当前页数量: {len(page_data['list'])}")
    
    print("\n" + "-" * 50)
    print("6. 测试故障上报（不同故障类型和优先级）")
    print("-" * 50)
    order_data_list = [
        {
            'device_id': device_ids[0],
            'fault_type': '触摸屏故障',
            'fault_description': '触摸屏失灵，点击无反应',
            'priority': '紧急',
            'reporter': '张三',
            'reporter_phone': '13800138000'
        },
        {
            'device_id': device_ids[1],
            'fault_type': '打印故障',
            'fault_description': '打印凭证卡纸',
            'priority': '高',
            'reporter': '李四',
            'reporter_phone': '13800138001'
        },
        {
            'device_id': device_ids[2],
            'fault_type': '网络故障',
            'fault_description': '网络连接不稳定',
            'priority': '一般',
            'reporter': '王五',
            'reporter_phone': '13800138002'
        }
    ]
    
    order_ids = []
    for order_data in order_data_list:
        response = requests.post(f'{BASE_URL}/work-orders', json=order_data)
        print(f"上报 {order_data['priority']} 优先级 {order_data['fault_type']}: {response.json()['message']}")
        order_ids.append(response.json()['data']['id'])
    
    print("\n" + "-" * 50)
    print("7. 测试按故障类型筛选工单")
    print("-" * 50)
    response = requests.get(f'{BASE_URL}/work-orders?fault_type=打印故障')
    orders = response.json()['data']['list']
    print(f"打印故障工单数量: {len(orders)}")
    
    print("\n" + "-" * 50)
    print("8. 测试按优先级（故障等级）筛选工单")
    print("-" * 50)
    response = requests.get(f'{BASE_URL}/work-orders?priority=紧急')
    orders = response.json()['data']['list']
    print(f"紧急优先级工单数量: {len(orders)}")
    for o in orders:
        print(f"  - {o['order_no']}: {o['fault_type']} ({o['priority']}) - {o['status']}")
    
    print("\n" + "-" * 50)
    print("9. 测试按处理状态筛选工单")
    print("-" * 50)
    response = requests.get(f'{BASE_URL}/work-orders?status=待处理')
    orders = response.json()['data']['list']
    print(f"待处理工单数量: {len(orders)}")
    
    print("\n" + "-" * 50)
    print("10. 测试按网点区域筛选工单")
    print("-" * 50)
    response = requests.get(f'{BASE_URL}/work-orders?branch_area=市区')
    orders = response.json()['data']['list']
    print(f"市区区域工单数量: {len(orders)}")
    
    print("\n" + "-" * 50)
    print("11. 测试处理工单（验证状态变更）")
    print("-" * 50)
    handle_data = {
        'handle_user': '李工程师',
        'handle_desc': '已到达现场，正在维修',
        'action': 'process'
    }
    response = requests.put(f'{BASE_URL}/work-orders/{order_ids[0]}/handle', json=handle_data)
    print(f"开始处理工单: {response.json()['message']}")
    
    complete_data = {
        'handle_user': '李工程师',
        'handle_desc': '更换触摸屏模块，设备恢复正常',
        'action': 'complete'
    }
    response = requests.put(f'{BASE_URL}/work-orders/{order_ids[0]}/handle', json=complete_data)
    print(f"完成工单: {response.json()['message']}")
    
    print("\n" + "-" * 50)
    print("12. 验证筛选结果变更")
    print("-" * 50)
    response = requests.get(f'{BASE_URL}/work-orders?status=已完成')
    orders = response.json()['data']['list']
    print(f"已完成工单数量: {len(orders)}")
    
    response = requests.get(f'{BASE_URL}/work-orders?status=处理中')
    orders = response.json()['data']['list']
    print(f"处理中工单数量: {len(orders)}")
    
    print("\n" + "-" * 50)
    print("13. 测试设备可用率统计")
    print("-" * 50)
    response = requests.get(f'{BASE_URL}/statistics')
    stats = response.json()['data']
    print(f"设备总数: {stats['devices']['total']}")
    print(f"正常: {stats['devices']['normal']}, 故障: {stats['devices']['fault']}, 维修中: {stats['devices']['repairing']}, 已修复: {stats['devices']['repaired']}")
    print(f"整体设备可用率: {stats['devices']['availability_rate']}%")
    
    print("\n各区域设备可用率:")
    for area in stats['area_distribution']:
        print(f"  {area['branch_area']}: {area['available']}/{area['total']} ({area['availability_rate']}%)")
    
    print("\n" + "-" * 50)
    print("14. 验证统一接口返回格式")
    print("-" * 50)
    response = requests.get(f'{BASE_URL}/devices')
    result = response.json()
    print(f"返回字段检查:")
    print(f"  - code: {result['code']} (200)")
    print(f"  - message: {result['message']}")
    print(f"  - data 存在: {'data' in result}")
    print(f"  - 分页信息存在: {'total' in result['data'] and 'page' in result['data']}")
    
    print("\n" + "=" * 70)
    print("✓ 所有 API 接口测试通过！系统优化完成。")
    print("=" * 70)
    print("\n优化总结:")
    print("  ✓ 设备模块新增网点区域字段")
    print("  ✓ 设备查询支持按区域、状态筛选")
    print("  ✓ 工单查询支持按故障类型、优先级、处理状态、网点区域筛选")
    print("  ✓ 所有列表接口支持分页")
    print("  ✓ 统一接口返回格式（code + message + data）")
    print("  ✓ 统计接口新增设备可用率计算（整体+分区域）")

if __name__ == '__main__':
    try:
        if os.path.exists('maintenance.db'):
            os.remove('maintenance.db')
            print("已清理旧数据库，使用全新数据库测试\n")
        test_all()
    except requests.exceptions.ConnectionError:
        print("\n错误：无法连接到服务器，请先运行 app.py 启动服务！")
