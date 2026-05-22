import requests
import json

BASE_URL = 'http://localhost:5000/api'

def test_add_device():
    print('=== 测试添加设备 ===')
    data = {
        "device_code": "GAS-001",
        "device_name": "氨气监测终端-A区",
        "location": "化工园区A区1号厂房",
        "gas_type": "氨气",
        "measure_range": "0-100 ppm",
        "threshold": 25.0,
        "alarm_upper_limit": 50.0,
        "installation_point": "A区-1号反应釜旁",
        "status": "正常"
    }
    response = requests.post(f'{BASE_URL}/devices', json=data)
    print(f'状态码: {response.status_code}')
    print()

def test_report_alarms():
    print('=== 测试上报多条告警 ===')
    for i in range(3):
        data = {
            "device_code": "GAS-001",
            "gas_value": 28.5 + i * 2,
            "description": f"氨气浓度超标告警{i+1}"
        }
        response = requests.post(f'{BASE_URL}/alarms', json=data)
        print(f'告警{i+1}状态码: {response.status_code}')
    print()

def test_get_alarms_categorized():
    print('=== 测试获取分类告警列表 ===')
    response = requests.get(f'{BASE_URL}/alarms/categorized')
    data = response.json()
    print(f'状态码: {response.status_code}')
    print(f"未确认告警数: {len(data['unconfirmed'])}")
    print(f"已确认告警数: {len(data['confirmed'])}")
    print(f"已处置告警数: {len(data['handled'])}")
    print()

def test_confirm_alarm():
    print('=== 测试确认告警 ===')
    data = {
        "handler": "张三"
    }
    response = requests.put(f'{BASE_URL}/alarms/1/confirm', json=data)
    print(f'状态码: {response.status_code}')
    result = response.json()
    print(f"确认状态: {result['alarm']['confirm_status']}")
    print(f"处置人: {result['alarm']['handler']}")
    print()

def test_handle_alarm():
    print('=== 测试处置告警（闭环） ===')
    data = {
        "handler": "李四",
        "handle_result": "已关闭泄漏源，浓度恢复正常。现场通风处理完成。"
    }
    response = requests.put(f'{BASE_URL}/alarms/2/handle', json=data)
    print(f'状态码: {response.status_code}')
    result = response.json()
    print(f"确认状态: {result['alarm']['confirm_status']}")
    print(f"处置人: {result['alarm']['handler']}")
    print(f"处置结果: {result['alarm']['handle_result']}")
    print()

def test_get_daily_trend():
    print('=== 测试获取设备日趋势曲线 ===')
    response = requests.get(f'{BASE_URL}/devices/1/trend/daily')
    data = response.json()
    print(f'状态码: {response.status_code}')
    print(f"设备: {data['device_name']}")
    print(f"气体类型: {data['gas_type']}")
    print(f"时间范围: {data['time_range']}")
    print(f"数据点数量: {len(data['data'])}")
    if len(data['data']) > 0:
        print(f"最新浓度: {data['data'][-1]['gas_value']} ppm")
    print()

def test_get_weekly_trend():
    print('=== 测试获取设备周趋势曲线 ===')
    response = requests.get(f'{BASE_URL}/devices/1/trend/weekly')
    data = response.json()
    print(f'状态码: {response.status_code}')
    print(f"设备: {data['device_name']}")
    print(f"气体类型: {data['gas_type']}")
    print(f"时间范围: {data['time_range']}")
    print(f"数据点数量: {len(data['data'])}")
    print()

def test_get_dashboard():
    print('=== 测试获取仪表盘统计（含告警分类统计） ===')
    response = requests.get(f'{BASE_URL}/dashboard')
    data = response.json()
    print(f'状态码: {response.status_code}')
    print(f"设备总数: {data['total_devices']}")
    print(f"未确认告警: {data['unconfirmed_alarms']}")
    print(f"已确认告警: {data['confirmed_alarms']}")
    print(f"已处置告警: {data['handled_alarms']}")
    print()

def test_get_alarms_categorized_after_operations():
    print('=== 操作后再次获取分类告警列表 ===')
    response = requests.get(f'{BASE_URL}/alarms/categorized')
    data = response.json()
    print(f'状态码: {response.status_code}')
    print(f"未确认告警数: {len(data['unconfirmed'])}")
    print(f"已确认告警数: {len(data['confirmed'])}")
    print(f"已处置告警数: {len(data['handled'])}")
    print()

if __name__ == '__main__':
    try:
        test_add_device()
        test_report_alarms()
        test_get_alarms_categorized()
        test_confirm_alarm()
        test_handle_alarm()
        test_get_alarms_categorized_after_operations()
        test_get_daily_trend()
        test_get_weekly_trend()
        test_get_dashboard()
        print('所有测试完成！')
    except requests.exceptions.ConnectionError:
        print('连接失败，请先启动服务端：python app.py')
    except Exception as e:
        print(f'测试出错: {e}')
        import traceback
        traceback.print_exc()
