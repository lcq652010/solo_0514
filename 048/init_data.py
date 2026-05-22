import requests
import json

BASE_URL = 'http://localhost:5001/api'

def init_test_data():
    print('开始初始化测试数据...')
    
    response = requests.get(f'{BASE_URL}/config')
    if response.status_code == 200:
        config = response.json()['data']
        print('故障类型:', len(config['fault_types']), '种')
        print('优先级:', config['priority_levels'])
        print('网点列表:', config['branch_list'])
    else:
        print('获取配置失败')
    
    devices = [
        {
            'device_code': 'TZJ-001',
            'device_name': '自助体检一体机A1',
            'location': '车管所一楼大厅',
            'branch': '车管所一楼大厅',
            'install_date': '2024-01-15',
            'status': '正常',
            'remark': '主力设备 - 驾驶人体检'
        },
        {
            'device_code': 'TZJ-002',
            'device_name': '自助体检一体机A2',
            'location': '车管所二楼办证区',
            'branch': '车管所二楼办证区',
            'install_date': '2024-02-20',
            'status': '正常',
            'remark': '备用设备'
        },
        {
            'device_code': 'PZJ-001',
            'device_name': '自助拍照一体机B1',
            'location': '车管所一楼大厅',
            'branch': '车管所一楼大厅',
            'install_date': '2024-03-10',
            'status': '故障',
            'remark': '驾驶证拍照专用'
        },
        {
            'device_code': 'ZZJ-001',
            'device_name': '自助制证一体机C1',
            'location': '车管所一楼制证区',
            'branch': '车管所一楼大厅',
            'install_date': '2024-01-20',
            'status': '正常',
            'remark': '制证核心设备'
        },
        {
            'device_code': 'ZZJ-002',
            'device_name': '自助制证一体机C2',
            'location': '车管所A网点',
            'branch': '车管所A网点',
            'install_date': '2024-02-15',
            'status': '正常',
            'remark': 'A网点制证设备'
        },
        {
            'device_code': 'TZJ-003',
            'device_name': '自助体检一体机A3',
            'location': '车管所B网点',
            'branch': '车管所B网点',
            'install_date': '2024-03-01',
            'status': '正常',
            'remark': 'B网点体检设备'
        }
    ]
    
    device_ids = []
    for device in devices:
        try:
            response = requests.post(f'{BASE_URL}/devices', json=device)
            if response.status_code == 200:
                result = response.json()
                device_ids.append(result['data']['id'])
                print(f'设备 {device["device_code"]} ({device["branch"]}) 添加成功')
            else:
                print(f'设备 {device["device_code"]} 添加失败: {response.text}')
        except Exception as e:
            print(f'设备 {device["device_code"]} 添加异常: {e}')
    
    if device_ids:
        work_orders = [
            {
                'device_id': device_ids[2],
                'device_code': 'PZJ-001',
                'fault_type': '摄像头故障',
                'fault_desc': '摄像头无法启动，拍照功能异常，影响驾驶证拍照业务',
                'priority': '高',
                'reporter': '张三',
                'reporter_phone': '13800138000'
            },
            {
                'device_id': device_ids[3],
                'device_code': 'ZZJ-001',
                'fault_type': '打印机故障',
                'fault_desc': '制证打印机卡纸，无法正常输出驾驶证，大厅制证业务停滞',
                'priority': '紧急',
                'reporter': '李四',
                'reporter_phone': '13900139000'
            },
            {
                'device_id': device_ids[4],
                'device_code': 'ZZJ-002',
                'fault_type': '硬件故障',
                'fault_desc': '身份证阅读器无法读卡，A网点业务受影响',
                'priority': '高',
                'reporter': '王五',
                'reporter_phone': '13700137000'
            }
        ]
        
        for order in work_orders:
            try:
                response = requests.post(f'{BASE_URL}/work-orders', json=order)
                if response.status_code == 200:
                    data = response.json()['data']
                    print(f'工单创建成功: {data["order_no"]}, 优先级: {data["priority"]}')
                else:
                    print(f'工单创建失败: {response.text}')
            except Exception as e:
                print(f'工单创建异常: {e}')
        
        maintain_records = [
            {
                'device_id': device_ids[0],
                'device_code': 'TZJ-001',
                'maintain_type': '例行维护',
                'maintain_desc': '清洁设备、检查硬件连接、更新软件',
                'maintain_user': '系统管理员',
                'maintain_time': '2024-05-10',
                'remark': '设备运行正常'
            },
            {
                'device_id': device_ids[1],
                'device_code': 'TZJ-002',
                'maintain_type': '故障维修',
                'maintain_desc': '更换触摸屏模块',
                'maintain_user': '维修工程师',
                'maintain_time': '2024-05-12',
                'remark': '已修复'
            }
        ]
        
        for record in maintain_records:
            try:
                response = requests.post(f'{BASE_URL}/maintain-records', json=record)
                if response.status_code == 200:
                    print(f'运维记录添加成功: {record["maintain_type"]}')
                else:
                    print(f'运维记录添加失败: {response.text}')
            except Exception as e:
                print(f'运维记录添加异常: {e}')
    
    print('\n获取仪表盘统计数据...')
    response = requests.get(f'{BASE_URL}/dashboard')
    if response.status_code == 200:
        data = response.json()['data']
        print(f'设备总数: {data["total_devices"]}')
        print(f'设备完好率: {data["device_health_rate"]}%')
        print(f'待处理工单: {data["pending_orders"]}')
        print(f'处理中工单: {data["processing_orders"]}')
        print(f'已完成工单: {data["completed_orders"]}')
        print(f'优先级统计: {data["priority_stats"]}')
        print(f'各网点设备统计:')
        for branch, stats in data['branch_stats'].items():
            if stats['total'] > 0:
                print(f'  {branch}: {stats["total"]}台, 完好率: {stats["health_rate"]}%')
    
    print('\n测试数据初始化完成!')

if __name__ == '__main__':
    init_test_data()
