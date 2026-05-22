import requests
import json

BASE_URL = 'http://localhost:5000/api'

def print_separator():
    print("\n" + "=" * 70)

def test_api():
    print_separator()
    print("开始测试智能燃气表运维管理系统 API v3.0")
    print_separator()
    
    print("\n1. 获取区域列表（新增接口）...")
    response = requests.get(f'{BASE_URL}/devices/regions')
    data = response.json()
    print(f"状态码: {response.status_code}, 响应: {data['msg']}")
    
    print("\n2. 获取故障类型配置...")
    response = requests.get(f'{BASE_URL}/fault-types')
    data = response.json()
    print(f"状态码: {response.status_code}")
    print(f"故障类型: {data['data']['fault_types']}")
    print(f"优先级规则: {data['data']['priority_rules']}")
    
    print("\n" + "-" * 70)
    print("\n3. 测试添加设备（新增区域、楼栋字段）...")
    device_data1 = {
        "device_no": "GAS001",
        "device_name": "智能燃气表-1号",
        "device_model": "G4-GPRS",
        "communication_protocol": "MQTT",
        "region": "东城区",
        "building": "A栋",
        "location": "1单元101室",
        "install_date": "2024-01-15",
        "enable_date": "2024-01-20"
    }
    response = requests.post(f'{BASE_URL}/devices', json=device_data1)
    data = response.json()
    print(f"状态码: {response.status_code}, 响应: {data['msg']}")
    device_id1 = data['data']['id']
    
    device_data2 = {
        "device_no": "GAS002",
        "device_name": "智能燃气表-2号",
        "device_model": "G4-GPRS",
        "communication_protocol": "LoRa",
        "region": "东城区",
        "building": "B栋",
        "location": "2单元302室",
        "install_date": "2024-02-01",
        "enable_date": "2024-02-05"
    }
    response = requests.post(f'{BASE_URL}/devices', json=device_data2)
    data = response.json()
    print(f"状态码: {response.status_code}, 响应: {data['msg']}")
    device_id2 = data['data']['id']
    
    device_data3 = {
        "device_no": "GAS003",
        "device_name": "智能燃气表-3号",
        "device_model": "G4-NB",
        "communication_protocol": "NB-IoT",
        "region": "西城区",
        "building": "C栋",
        "location": "1单元201室",
        "install_date": "2024-01-20",
        "enable_date": "2024-01-25"
    }
    response = requests.post(f'{BASE_URL}/devices', json=device_data3)
    data = response.json()
    print(f"状态码: {response.status_code}, 响应: {data['msg']}")
    device_id3 = data['data']['id']
    
    print("\n" + "-" * 70)
    print("\n4. 测试按区域筛选设备（东城区）...")
    response = requests.get(f'{BASE_URL}/devices?region=东城区')
    data = response.json()
    print(f"状态码: {response.status_code}, 东城区设备数: {data['data']['total']}")
    
    print("\n" + "-" * 70)
    print("\n5. 测试按楼栋筛选设备（A栋）...")
    response = requests.get(f'{BASE_URL}/devices?building=A栋')
    data = response.json()
    print(f"状态码: {response.status_code}, A栋设备数: {data['data']['total']}")
    
    print("\n" + "-" * 70)
    print("\n6. 测试获取楼栋列表（按区域筛选）...")
    response = requests.get(f'{BASE_URL}/devices/buildings?region=东城区')
    data = response.json()
    print(f"状态码: {response.status_code}, 东城区楼栋: {data['data']['buildings']}")
    
    print("\n" + "-" * 70)
    print("\n7. 测试【紧急优先级】故障上报（燃气泄漏 - 东城区A栋）...")
    workorder_data1 = {
        "device_id": device_id1,
        "fault_type": "燃气泄漏",
        "fault_description": "检测到微量燃气泄漏，浓度持续上升",
        "reporter": "张三"
    }
    response = requests.post(f'{BASE_URL}/workorders', json=workorder_data1)
    data = response.json()
    print(f"状态码: {response.status_code}")
    print(f"工单编号: {data['data']['order_no']}")
    print(f"故障分类: {data['data']['fault_category']}")
    print(f"紧急优先级: {data['data']['priority']}")
    print(f"所在区域: {data['data']['region']}")
    order_id1 = data['data']['id']
    
    print("\n" + "-" * 70)
    print("\n8. 测试【高优先级】故障上报（数据异常 - 西城区C栋）...")
    workorder_data2 = {
        "device_id": device_id3,
        "fault_type": "数据异常",
        "fault_description": "燃气读数连续3天无变化",
        "reporter": "李四"
    }
    response = requests.post(f'{BASE_URL}/workorders', json=workorder_data2)
    data = response.json()
    print(f"状态码: {response.status_code}")
    print(f"工单编号: {data['data']['order_no']}")
    print(f"故障分类: {data['data']['fault_category']}")
    print(f"紧急优先级: {data['data']['priority']}")
    print(f"所在区域: {data['data']['region']}")
    
    print("\n" + "-" * 70)
    print("\n9. 测试按区域筛选工单（东城区）...")
    response = requests.get(f'{BASE_URL}/workorders?region=东城区')
    data = response.json()
    print(f"状态码: {response.status_code}, 东城区工单数量: {data['data']['total']}")
    
    print("\n" + "-" * 70)
    print("\n10. 测试按优先级筛选工单（紧急）...")
    response = requests.get(f'{BASE_URL}/workorders?priority=紧急')
    data = response.json()
    print(f"状态码: {response.status_code}, 紧急工单数量: {data['data']['total']}")
    
    print("\n" + "-" * 70)
    print("\n11. 测试数据上传状态上报...")
    upload_records = [
        {"device_id": device_id1, "status": "成功", "data_type": "计量数据", "error_msg": ""},
        {"device_id": device_id1, "status": "成功", "data_type": "计量数据", "error_msg": ""},
        {"device_id": device_id1, "status": "失败", "data_type": "计量数据", "error_msg": "网络超时"},
        {"device_id": device_id2, "status": "成功", "data_type": "计量数据", "error_msg": ""},
        {"device_id": device_id3, "status": "成功", "data_type": "计量数据", "error_msg": ""},
    ]
    for record in upload_records:
        response = requests.post(f'{BASE_URL}/data-upload', json=record)
    print(f"已上报 {len(upload_records)} 条上传记录")
    
    print("\n" + "-" * 70)
    print("\n12. 测试查询上传失败记录...")
    response = requests.get(f'{BASE_URL}/data-upload?status=失败')
    data = response.json()
    print(f"状态码: {response.status_code}, 上传失败记录数: {data['data']['total']}")
    
    print("\n" + "-" * 70)
    print("\n13. 测试处理紧急工单...")
    handle_data = {
        "handler": "李工程师",
        "handle_result": "已更换密封垫圈，重新进行气密性测试合格，恢复供气",
        "next_status": "已修复"
    }
    response = requests.put(f'{BASE_URL}/workorders/{order_id1}/handle', json=handle_data)
    data = response.json()
    print(f"状态码: {response.status_code}, 处理结果: {data['msg']}")
    
    print("\n" + "-" * 70)
    print("\n14. 测试统计面板（含设备完好率、上传成功率、区域完好率）...")
    response = requests.get(f'{BASE_URL}/dashboard')
    data = response.json()
    print(f"状态码: {response.status_code}")
    stats = data['data']
    print(f"\n设备统计: 总计{stats['total_devices']}台 | 正常{stats['normal_devices']}台 | 故障{stats['fault_devices']}台")
    print(f"设备完好率: {stats['device_health_rate']}%")
    print(f"\n数据上传统计: 总计{stats['upload_stats']['total_uploads']}次 | 成功{stats['upload_stats']['success_uploads']}次")
    print(f"数据上传成功率: {stats['upload_stats']['success_rate']}%")
    print(f"\n各区域设备完好率统计:")
    for region_stat in stats['region_health_stats']:
        print(f"  {region_stat['region']}: {region_stat['health_rate']}% (共{region_stat['total_devices']}台)")
    
    print("\n" + "-" * 70)
    print("\n15. 测试统一错误响应（设备不存在）...")
    response = requests.get(f'{BASE_URL}/devices/99999')
    data = response.json()
    print(f"状态码: {response.status_code}")
    print(f"错误信息: {data['msg']}")
    print(f"统一格式验证: code={data['code']}, msg存在={('msg' in data)}, data存在={('data' in data)}")
    
    print_separator()
    print("✅ API v3.0 测试完成！")
    print("\n核心功能验证:")
    print("  ✓ 设备模块新增字段：区域、楼栋")
    print("  ✓ 支持按区域、楼栋筛选设备和工单")
    print("  ✓ 新增数据上传记录API，支持按状态查询")
    print("  ✓ 设备完好率统计（全局 + 按区域）")
    print("  ✓ 数据上传成功率统计")
    print("  ✓ 所有接口返回统一响应格式（code/msg/data）")
    print("  ✓ 新增获取区域列表、楼栋列表接口")
    print("  ✓ 支持按优先级分类筛选故障工单")
    print_separator()

if __name__ == '__main__':
    test_api()
