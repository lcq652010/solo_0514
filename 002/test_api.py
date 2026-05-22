import requests
import json

BASE_URL = 'http://localhost:5000/api'

def print_response(title, response):
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"状态码: {response.status_code}")
    try:
        data = response.json()
        print(f"成功: {data.get('success')}")
        print(f"消息: {data.get('message')}")
        if 'data' in data:
            print(f"数据:\n{json.dumps(data['data'], ensure_ascii=False, indent=2)}")
    except:
        print(response.text)

def test_all_apis():
    print("开始测试API接口...")
    print("请确保服务已启动 (python app.py)")
    input("按回车继续...")

    print_response("1. 获取所有枚举值", 
        requests.get(f'{BASE_URL}/enums'))

    print_response("2. 获取仪表板统计", 
        requests.get(f'{BASE_URL}/dashboard/stats'))

    print_response("3. 获取设备完好率统计", 
        requests.get(f'{BASE_URL}/dashboard/availability'))

    print_response("4. 添加设备1（港区A，集装箱堆场）", 
        requests.post(f'{BASE_URL}/devices', json={
            'device_code': 'CT-A001',
            'device_name': '集装箱识别终端-A1',
            'device_type': '光学识别',
            'device_model': 'OCR-2024-Pro',
            'protection_level': 'IP67',
            'serial_number': 'SN20240515A001',
            'commission_date': '2024-03-01',
            'harbor_area': '港区A',
            'work_area': '集装箱堆场',
            'location': '1号码头入口',
            'install_date': '2024-01-15'
        }))

    print_response("5. 添加设备2（港区B，码头作业区）", 
        requests.post(f'{BASE_URL}/devices', json={
            'device_code': 'CT-B001',
            'device_name': '集装箱识别终端-B1',
            'device_type': 'RFID识别',
            'device_model': 'RFID-X600',
            'protection_level': 'IP65',
            'serial_number': 'SN20240515B001',
            'commission_date': '2024-04-01',
            'harbor_area': '港区B',
            'work_area': '码头作业区',
            'location': '2号码头出口',
            'install_date': '2024-02-20'
        }))

    print_response("6. 获取所有设备", 
        requests.get(f'{BASE_URL}/devices'))

    print_response("7. 按港区筛选设备（港区A）", 
        requests.get(f'{BASE_URL}/devices', params={'harbor_area': '港区A'}))

    print_response("8. 获取设备1详情（包含待处理工单和最近维修记录）", 
        requests.get(f'{BASE_URL}/devices/1'))

    print_response("9. 故障上报 - 紧急硬件故障（港区A）", 
        requests.post(f'{BASE_URL}/work-orders', json={
            'device_id': 1,
            'fault_type': '硬件故障',
            'fault_level': '严重',
            'priority': '紧急',
            'fault_description': '摄像头损坏，完全无法识别箱号，影响船舶作业',
            'reporter': '张三'
        }))

    print_response("10. 故障上报 - 一般软件故障（港区B）", 
        requests.post(f'{BASE_URL}/work-orders', json={
            'device_id': 2,
            'fault_type': '软件故障',
            'fault_level': '一般',
            'priority': '一般',
            'fault_description': '识别算法偶尔出现误判',
            'reporter': '李四'
        }))

    print_response("11. 获取所有工单（按优先级排序，紧急工单在前）", 
        requests.get(f'{BASE_URL}/work-orders'))

    print_response("12. 按港区筛选工单（港区A）", 
        requests.get(f'{BASE_URL}/work-orders', params={'harbor_area': '港区A'}))

    print_response("13. 按优先级筛选工单（紧急）", 
        requests.get(f'{BASE_URL}/work-orders', params={'priority': '紧急'}))

    print_response("14. 按故障等级筛选工单（严重）", 
        requests.get(f'{BASE_URL}/work-orders', params={'fault_level': '严重'}))

    print_response("15. 处理工单1", 
        requests.put(f'{BASE_URL}/work-orders/WO202605150001/handle', json={
            'handler': '李工',
            'handle_result': '更换摄像头模组，设备恢复正常',
            'device_status': '正常',
            'cost': 2500.0,
            'remark': '紧急维修，保障港口作业正常进行'
        }))

    print_response("16. 更新设备1心跳", 
        requests.put(f'{BASE_URL}/devices/1/heartbeat'))

    print_response("17. 获取所有维修记录", 
        requests.get(f'{BASE_URL}/maintenance-records'))

    print_response("18. 按港区筛选维修记录（港区A）", 
        requests.get(f'{BASE_URL}/maintenance-records', params={'harbor_area': '港区A'}))

    print_response("19. 再次获取仪表板统计（验证数据变化）", 
        requests.get(f'{BASE_URL}/dashboard/stats'))

    print_response("20. 获取30天趋势数据", 
        requests.get(f'{BASE_URL}/dashboard/trend'))

    print("\n" + "="*60)
    print("API测试完成！")
    print("="*60)

if __name__ == '__main__':
    test_all_apis()
