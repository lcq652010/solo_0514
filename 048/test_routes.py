import sys
sys.path.insert(0, '.')

from app import app

with app.test_client() as client:
    print('测试 /api/dashboard 路由...')
    response = client.get('/api/dashboard')
    print(f'状态码: {response.status_code}')
    print(f'响应数据: {response.get_json()}')
    
    print('\n测试 /api/devices 路由...')
    response = client.get('/api/devices')
    print(f'状态码: {response.status_code}')
    print(f'响应数据: {response.get_json()}')
    
    print('\n测试添加设备...')
    device_data = {
        'device_code': 'TEST-001',
        'device_name': '测试设备',
        'location': '测试位置',
        'install_date': '2024-05-16'
    }
    response = client.post('/api/devices', json=device_data)
    print(f'状态码: {response.status_code}')
    print(f'响应数据: {response.get_json()}')

print('\n所有测试完成!')
