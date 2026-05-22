import requests
import json

BASE_URL = 'http://localhost:5000/api'

def print_response(title, response):
    print(f'\n=== {title} ===')
    print(f'Status Code: {response.status_code}')
    print(f'Success: {response.json().get("success", "N/A")}')
    print(f'Message: {response.json().get("message", "N/A")}')
    try:
        data = response.json().get('data', {})
        if data:
            print('Data:')
            print(json.dumps(data, ensure_ascii=False, indent=2))
    except:
        print(response.text)

def test_all_apis():
    print('开始测试影院运维管理系统 API...')
    
    print('\n' + '='*60)
    print('0. 获取系统常量配置')
    print('='*60)
    
    response = requests.get(f'{BASE_URL}/config/constants')
    print_response('获取系统常量配置', response)
    
    print('\n' + '='*60)
    print('1. 测试设备管理接口（含区域字段）')
    print('='*60)
    
    device_data = {
        'device_code': 'DEV001',
        'device_name': '一号厅自助取票机',
        'device_model': 'TICKET-V2024',
        'device_type': 'ticket_machine',
        'communication_type': 'ethernet',
        'area': 'hall_1',
        'location': '一号厅入口',
        'commission_date': '2024-01-15',
        'status': 'normal'
    }
    response = requests.post(f'{BASE_URL}/devices', json=device_data)
    print_response('添加设备1（一号厅区域）', response)
    device1_id = response.json()['data']['device']['id'] if response.status_code == 201 else None
    
    device_data2 = {
        'device_code': 'DEV002',
        'device_name': '二号厅自助检票机',
        'device_model': 'CHECKIN-X100',
        'device_type': 'checkin_machine',
        'communication_type': 'wifi',
        'area': 'hall_2',
        'location': '二号厅入口',
        'commission_date': '2024-03-20',
        'status': 'normal'
    }
    response = requests.post(f'{BASE_URL}/devices', json=device_data2)
    print_response('添加设备2（二号厅区域）', response)
    device2_id = response.json()['data']['device']['id'] if response.status_code == 201 else None
    
    response = requests.get(f'{BASE_URL}/devices')
    print_response('获取所有设备', response)
    
    response = requests.get(f'{BASE_URL}/devices?area=hall_1')
    print_response('按区域筛选设备（一号厅）', response)
    
    if device1_id:
        response = requests.get(f'{BASE_URL}/devices/{device1_id}')
        print_response('获取单个设备详情', response)
        
        update_data = {
            'location': '一号厅入口左侧',
            'device_model': 'TICKET-V2024-PRO',
            'area': 'lobby'
        }
        response = requests.put(f'{BASE_URL}/devices/{device1_id}', json=update_data)
        print_response('更新设备信息（修改区域）', response)
    
    print('\n' + '='*60)
    print('2. 测试工单（故障上报）接口 - 含故障分类、优先级、区域筛选')
    print('='*60)
    
    if device1_id:
        workorder_data = {
            'device_id': device1_id,
            'fault_category': 'hardware',
            'fault_type': '打印机故障',
            'fault_description': '自助取票机打印机卡纸，无法打印票据',
            'priority': 'high',
            'impact_description': '影响高峰时段观众取票，预计影响300人次/小时',
            'reporter': '张三'
        }
        response = requests.post(f'{BASE_URL}/workorders', json=workorder_data)
        print_response('创建高优先级硬件故障工单', response)
        order1_id = response.json()['data']['work_order']['id'] if response.status_code == 201 else None
        order1_no = response.json()['data']['work_order']['order_no'] if response.status_code == 201 else None
        print(f'工单自动编号: {order1_no}')
    
    if device2_id:
        workorder_data2 = {
            'device_id': device2_id,
            'fault_category': 'software',
            'fault_type': '二维码扫描故障',
            'fault_description': '检票机无法识别二维码，乘客无法入场',
            'priority': 'urgent',
            'impact_description': '电影即将开场，大量观众排队，严重影响观影体验和客流',
            'reporter': '李四'
        }
        response = requests.post(f'{BASE_URL}/workorders', json=workorder_data2)
        print_response('创建紧急软件故障工单', response)
        order2_id = response.json()['data']['work_order']['id'] if response.status_code == 201 else None
    
    response = requests.get(f'{BASE_URL}/workorders')
    print_response('获取所有工单（按优先级排序）', response)
    
    response = requests.get(f'{BASE_URL}/workorders?priority=urgent')
    print_response('按优先级筛选工单（紧急）', response)
    
    response = requests.get(f'{BASE_URL}/workorders?fault_category=hardware')
    print_response('按故障分类筛选工单（硬件）', response)
    
    response = requests.get(f'{BASE_URL}/workorders?area=hall_2')
    print_response('按区域筛选工单（二号厅）', response)
    
    response = requests.get(f'{BASE_URL}/workorders?status=pending&priority=high')
    print_response('多条件组合筛选（待处理+高优）', response)
    
    print('\n' + '='*60)
    print('3. 测试工单处理接口')
    print('='*60)
    
    if 'order1_id' in locals() and order1_id:
        handle_data = {
            'handler': '王工程师',
            'action': 'start_repair'
        }
        response = requests.put(f'{BASE_URL}/workorders/{order1_id}/handle', json=handle_data)
        print_response('开始维修工单', response)
        
        complete_data = {
            'handler': '王工程师',
            'action': 'complete',
            'handle_result': '已更换打印机滚轴，清理卡纸，设备恢复正常'
        }
        response = requests.put(f'{BASE_URL}/workorders/{order1_id}/handle', json=complete_data)
        print_response('完成工单维修', response)
    
    print('\n' + '='*60)
    print('4. 测试运维记录接口（含区域筛选）')
    print('='*60)
    
    response = requests.get(f'{BASE_URL}/maintenance')
    print_response('获取所有运维记录', response)
    
    response = requests.get(f'{BASE_URL}/maintenance?area=lobby')
    print_response('按区域筛选运维记录（大堂）', response)
    
    if device2_id:
        maintenance_data = {
            'device_id': device2_id,
            'maintenance_type': '定期保养',
            'description': '设备清洁、传感器校准',
            'operator': '赵师傅',
            'result': '成功',
            'remarks': '设备运行状态良好'
        }
        response = requests.post(f'{BASE_URL}/maintenance', json=maintenance_data)
        print_response('添加定期保养记录', response)
    
    print('\n' + '='*60)
    print('5. 测试设备完好率和仪表盘统计接口')
    print('='*60)
    
    response = requests.get(f'{BASE_URL}/dashboard/health-rate')
    print_response('获取全局设备完好率', response)
    
    response = requests.get(f'{BASE_URL}/dashboard/health-rate?area=hall_2')
    print_response('按区域获取设备完好率（二号厅）', response)
    
    response = requests.get(f'{BASE_URL}/dashboard/stats')
    print_response('获取仪表盘统计数据', response)
    
    response = requests.get(f'{BASE_URL}/dashboard/stats?area=hall_1')
    print_response('按区域获取仪表盘统计数据（一号厅）', response)
    
    print('\n' + '='*60)
    print('API 测试完成！')
    print('='*60)

if __name__ == '__main__':
    test_all_apis()
