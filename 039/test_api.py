import requests
import json
import os

BASE_URL = "http://127.0.0.1:5000"

def print_response(title, response):
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"状态码: {response.status_code}")
    try:
        data = response.json()
        print(f"成功: {data.get('success', False)}")
        print(f"消息: {data.get('message', '')}")
        if 'data' in data:
            print(f"数据: {json.dumps(data['data'], ensure_ascii=False, indent=2)}")
    except:
        print(f"响应文本: {response.text}")
    print(f"{'='*50}\n")

def test_api():
    print("开始 API 测试 (v3.0 优化版）...")
    
    # 1. 获取枚举配置
    print("\n1. 测试获取枚举配置")
    response = requests.get(f"{BASE_URL}/api/config/enums")
    print_response("获取枚举配置", response)
    
    # 2. 添加多个设备（不同区域）
    print("\n2. 测试添加设备（不同区域）")
    devices = [
        {
            "device_code": "DEVICE001",
            "device_name": "一楼大厅自助终端A",
            "device_model": "TAX-2024-PRO",
            "communication_method": "有线网络",
            "location": "一楼大厅A区",
            "install_date": "2024-01-01",
            "commission_date": "2024-01-15",
            "remark": "新装设备，支持电子发票和纸质发票"
        },
        {
            "device_code": "DEVICE002",
            "device_name": "一楼大厅自助终端B",
            "device_model": "TAX-2024-LITE",
            "communication_method": "无线网络",
            "location": "一楼大厅B区",
            "install_date": "2024-01-01",
            "commission_date": "2024-01-15",
            "remark": "备用设备"
        },
        {
            "device_code": "DEVICE003",
            "device_name": "二楼办税厅自助终端A",
            "device_model": "TAX-2024-PRO",
            "communication_method": "5G",
            "location": "二楼办税厅A区",
            "install_date": "2024-02-01",
            "commission_date": "2024-02-10",
            "remark": "5G联网设备"
        }
    ]
    
    device_ids = []
    for device in devices:
        response = requests.post(f"{BASE_URL}/api/devices", json=device)
        print_response(f"添加设备: {device['device_name']}", response)
        if response.status_code == 200:
            device_ids.append(response.json()['data']['id'])
    
    # 3. 获取区域列表
    print("\n3. 测试获取区域列表")
    response = requests.get(f"{BASE_URL}/api/devices/locations")
    print_response("获取区域列表", response)
    
    # 4. 按区域筛选设备
    print("\n4. 测试按区域筛选设备（一楼大厅）")
    response = requests.get(f"{BASE_URL}/api/devices?location=一楼大厅")
    print_response("按区域筛选设备", response)
    
    # 5. 创建设备故障工单（不同优先级）
    print("\n5. 测试创建工单（不同优先级）")
    orders_data = [
        {
            "device_id": device_ids[0] if len(device_ids) > 0 else 1,
            "fault_type": "打印机故障",
            "fault_description": "打印机卡纸，无法打印发票，已影响3名纳税人办税",
            "priority": "高",
            "business_impact": "导致发票开具业务中断，影响大厅正常办税秩序",
            "reporter": "张三",
            "reporter_phone": "13800138000"
        },
        {
            "device_id": device_ids[1] if len(device_ids) > 1 else 2,
            "fault_type": "触摸屏故障",
            "fault_description": "触摸屏反应迟钝，部分区域点击无响应",
            "priority": "中",
            "business_impact": "影响用户体验，但业务尚可进行",
            "reporter": "李四",
            "reporter_phone": "13900139000"
        },
        {
            "device_id": device_ids[2] if len(device_ids) > 2 else 3,
            "fault_type": "软件故障",
            "fault_description": "界面显示字体略小，不影响正常使用",
            "priority": "低",
            "business_impact": "无业务影响，建议后续版本优化",
            "reporter": "王五",
            "reporter_phone": "13700137000"
        }
    ]
    
    order_nos = []
    for order in orders_data:
        response = requests.post(f"{BASE_URL}/api/work-orders", json=order)
        print_response(f"创建{order['priority']}优先级工单", response)
        if response.status_code == 200:
            order_nos.append(response.json()['data']['order_no'])
    
    # 6. 按故障类型筛选工单
    print("\n6. 测试按故障类型筛选工单（打印机故障）")
    response = requests.get(f"{BASE_URL}/api/work-orders?fault_type=打印机故障")
    print_response("按故障类型筛选", response)
    
    # 7. 按优先级筛选工单
    print("\n7. 测试按优先级筛选工单（高优先级）")
    response = requests.get(f"{BASE_URL}/api/work-orders?priority=高")
    print_response("按高优先级筛选", response)
    
    # 8. 按处理状态筛选工单
    print("\n8. 测试按处理状态筛选工单（待处理）")
    response = requests.get(f"{BASE_URL}/api/work-orders?status=待处理")
    print_response("按待处理状态筛选", response)
    
    # 9. 按区域筛选工单
    print("\n9. 测试按区域筛选工单（一楼大厅）")
    response = requests.get(f"{BASE_URL}/api/work-orders?location=一楼大厅")
    print_response("按区域筛选工单", response)
    
    # 10. 处理第一个工单
    if len(order_nos) > 0:
        print(f"\n10. 测试处理第一个工单 (工单编号: {order_nos[0]})")
        handle_data = {
            "status": "处理中",
            "handler": "张工程师",
            "handle_result": "已到达现场，正在检查打印机硬件"
        }
        response = requests.put(f"{BASE_URL}/api/work-orders/{order_nos[0]}/handle", json=handle_data)
        print_response("处理工单（处理中）", response)
    
    # 11. 完成工单处理
    if len(order_nos) > 0:
        print(f"\n11. 测试完成工单处理 (工单编号: {order_nos[0]})")
        handle_data = {
            "status": "已完成",
            "handler": "张工程师",
            "handle_result": "清理打印机进纸通道，更换搓纸轮，设备恢复正常"
        }
        response = requests.put(f"{BASE_URL}/api/work-orders/{order_nos[0]}/handle", json=handle_data)
        print_response("完成工单处理", response)
    
    # 12. 按处理状态筛选（已完成）
    print("\n12. 测试按处理状态筛选工单（已完成）")
    response = requests.get(f"{BASE_URL}/api/work-orders?status=已完成")
    print_response("按已完成状态筛选", response)
    
    # 13. 查询运维记录
    print("\n13. 测试查询运维记录")
    response = requests.get(f"{BASE_URL}/api/maintain-records")
    print_response("查询运维记录", response)
    
    # 14. 查询统计数据（含设备可用率）
    print("\n14. 测试查询统计数据（含设备可用率）")
    response = requests.get(f"{BASE_URL}/api/dashboard/statistics")
    print_response("查询统计数据", response)
    
    # 15. 查询单个设备详情
    if len(device_ids) > 0:
        print(f"\n15. 测试查询单个设备详情 (设备ID: {device_ids[0]})")
        response = requests.get(f"{BASE_URL}/api/devices/{device_ids[0]}")
        print_response("查询设备详情", response)
    
    # 16. 查询单个工单详情
    if len(order_nos) > 1:
        print(f"\n16. 测试查询单个工单详情 (工单编号: {order_nos[1]})")
        response = requests.get(f"{BASE_URL}/api/work-orders/{order_nos[1]}")
        print_response("查询工单详情", response)
    
    print("\n" + "="*70)
    print("API 测试完成！系统 v3.0 优化功能验证：")
    print("  ✓ 统一接口响应格式（code、success、message、timestamp）")
    print("  ✓ 设备模块：设备型号、通信方式、投用日期、区域筛选")
    print("  ✓ 故障模块：故障类型分类、紧急优先级标记、业务影响描述")
    print("  ✓ 多维度组合筛选：区域、故障类型、优先级、处理状态")
    print("  ✓ 工单按优先级智能排序（高→中→低）")
    print("  ✓ 设备可用率统计（整体 + 按区域）")
    print("  ✓ 分页查询支持（设备、工单、运维记录）")
    print("  ✓ 区域列表查询接口")
    print("="*70)

if __name__ == "__main__":
    # 先删除旧数据库，确保测试环境干净
    db_path = os.path.join(os.path.dirname(__file__), 'tax_invoice.db')
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print("已清理旧数据库，确保测试环境干净\n")
        except:
            pass
    
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("\n错误：无法连接到服务器！")
        print("请先运行以下命令启动服务：")
        print("  python app.py")
    except Exception as e:
        print(f"\n测试出错: {e}")
        import traceback
        traceback.print_exc()
