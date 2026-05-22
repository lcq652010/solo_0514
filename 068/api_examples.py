import requests
import json

BASE_URL = 'http://localhost:5000'

def print_response(title, response):
    print(f'\n=== {title} ===')
    print(f'Status Code: {response.status_code}')
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))

def main():
    print('椰壳雕手把件订单管理系统 v2.0 - API测试')
    
    print_response('获取系统信息', requests.get(f'{BASE_URL}/'))
    
    print_response('获取所有规格选项', requests.get(f'{BASE_URL}/api/specifications'))
    
    print_response('获取所有订单状态', requests.get(f'{BASE_URL}/api/statuses'))
    
    order_data = {
        'customer_name': '张三',
        'phone': '13800138000',
        'design_requirements': '雕刻龙凤图案，传统风格，线条流畅',
        'coconut_specification': '老椰壳(壁厚3-5mm)',
        'shape_type': '圆形',
        'outer_dimensions': '直径6cm，厚度1.5cm',
        'carving_pattern': '龙凤呈祥',
        'surface_treatment': '烫蜡工艺',
        'size': '6cm x 6cm x 1.5cm',
        'material_preference': '海南老椰壳',
        'blank_spec': '正圆形，壁厚均匀，无裂纹',
        'carving_depth': '浅浮雕(0.5-1mm)',
        'polishing_grade': '3000目精抛',
        'remark': '希望能够加急，作为礼品'
    }
    print_response('创建订单(含完整专业字段)', requests.post(f'{BASE_URL}/api/orders', json=order_data))
    
    order_data2 = {
        'customer_name': '李四',
        'phone': '13900139000',
        'design_requirements': '雕刻山水图案，简约风格',
        'coconut_specification': '中椰壳(直径7-9cm)',
        'shape_type': '随形',
        'outer_dimensions': '长8cm，宽5cm',
        'carving_pattern': '山水风景',
        'surface_treatment': '原色打磨',
        'material_preference': '天然椰壳',
        'blank_spec': '随形，自然边保留',
        'carving_depth': '深浮雕(1-2mm)',
        'polishing_grade': '2000目抛光'
    }
    print_response('创建第二个订单', requests.post(f'{BASE_URL}/api/orders', json=order_data2))
    
    print_response('获取订单列表', requests.get(f'{BASE_URL}/api/orders'))
    
    print_response('获取统计信息', requests.get(f'{BASE_URL}/api/stats'))
    
    orders_response = requests.get(f'{BASE_URL}/api/orders')
    if orders_response.status_code == 200:
        orders = orders_response.json()['orders']
        if orders:
            order_no = orders[0]['order_no']
            print_response(f'获取订单详情: {order_no}', requests.get(f'{BASE_URL}/api/orders/{order_no}'))
            
            update_data = {
                'status': '选椰壳',
                'operator': '王师傅',
                'remark': '已选定海南老椰壳，壁厚4mm'
            }
            print_response(f'更新订单状态到选椰壳: {order_no}', 
                          requests.put(f'{BASE_URL}/api/orders/{order_no}/status', json=update_data))
            
            update_data2 = {
                'status': '开坯',
                'operator': '王师傅',
                'remark': '开坯完成，正圆形，壁厚均匀'
            }
            print_response(f'更新订单状态到开坯: {order_no}', 
                          requests.put(f'{BASE_URL}/api/orders/{order_no}/status', json=update_data2))
            
            update_data3 = {
                'blank_spec': '正圆形，边缘整齐，壁厚一致',
                'carving_depth': '浅浮雕(0.8mm)',
                'remark': '客户要求调整雕刻深度'
            }
            print_response(f'更新订单专业参数: {order_no}',
                          requests.put(f'{BASE_URL}/api/orders/{order_no}', json=update_data3))
    
    print_response('获取更新后的统计信息', requests.get(f'{BASE_URL}/api/stats'))

if __name__ == '__main__':
    main()
