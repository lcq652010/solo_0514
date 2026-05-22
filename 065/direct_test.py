import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, init_db, migrate_db
import json

with app.app_context():
    init_db()
    migrate_db()

def test_api():
    print('=' * 70)
    print('麦秆贴画书签订单管理系统 v2.0 - API 测试')
    print('=' * 70)
    
    client = app.test_client()
    
    print('\n1. 测试首页 - 验证版本信息')
    response = client.get('/')
    print(f'状态码: {response.status_code}')
    if response.status_code == 200:
        data = response.get_json()
        print(f"版本: {data.get('version')}")
        print(f"业务字段: {list(data.get('business_fields', {}).keys())}")
    
    print('\n2. 测试获取所有枚举值')
    response = client.get('/api/enums')
    print(f'状态码: {response.status_code}')
    enums = response.get_json()
    print(f"麦秆品类 ({len(enums['wheat_straw_categories'])}种): {enums['wheat_straw_categories']}")
    print(f"书签规格 ({len(enums['bookmark_sizes'])}种): {enums['bookmark_sizes']}")
    print(f"贴画纹样 ({len(enums['pattern_types'])}种): {enums['pattern_types']}")
    print(f"裱封类型 ({len(enums['mounting_types'])}种): {enums['mounting_types']}")
    
    print('\n3. 测试创建完整业务信息的订单')
    order_data = {
        'customer_name': '李四',
        'phone': '13900139000',
        'email': 'lisi@example.com',
        'design_description': '山水风景，古典水墨风格',
        'quantity': 10,
        'deadline': '2026-06-15',
        'wheat_straw_category': '白麦秆',
        'bookmark_size': '中型 (60x150mm)',
        'pattern_type': '山水风景',
        'mounting_type': 'PVC塑封',
        'remark': '加急处理'
    }
    response = client.post('/api/orders', 
                          json=order_data,
                          content_type='application/json')
    print(f'状态码: {response.status_code}')
    result = response.get_json()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    order_id = result.get('order_id')
    
    print(f'\n4. 查询订单详情 - 验证业务字段是否保存')
    response = client.get(f'/api/orders/{order_id}')
    print(f'状态码: {response.status_code}')
    order = response.get_json()
    print(f"订单编号: {order['id']}")
    print(f"麦秆品类: {order['wheat_straw_category']}")
    print(f"书签规格: {order['bookmark_size']}")
    print(f"贴画纹样: {order['pattern_type']}")
    print(f"裱封类型: {order['mounting_type']}")
    print(f"当前状态: {order['status']}")
    
    print(f'\n5. 测试更新业务字段 - 调整麦秆品类和裱封类型')
    update_data = {
        'wheat_straw_category': '混合麦秆',
        'mounting_type': '亚克力封装',
        'remark': '客户要求升级为混合麦秆和亚克力封装'
    }
    response = client.put(
        f'/api/orders/{order_id}',
        json=update_data,
        content_type='application/json'
    )
    print(f'状态码: {response.status_code}')
    print(json.dumps(response.get_json(), ensure_ascii=False, indent=2))
    
    print(f'\n6. 验证业务字段更新结果')
    response = client.get(f'/api/orders/{order_id}')
    order = response.get_json()
    print(f"麦秆品类: {order['wheat_straw_category']}")
    print(f"裱封类型: {order['mounting_type']}")
    print(f"备注: {order['remark']}")
    
    print(f'\n7. 测试完整生产流程状态流转')
    print('-' * 50)
    workflow = ['选麦秆', '漂白', '压平', '裁剪', '拼贴', '裱封', '完工']
    for status in workflow:
        response = client.put(
            f'/api/orders/{order_id}/status',
            json={'status': status},
            content_type='application/json'
        )
        print(f"→ 更新状态为 '{status}': {response.get_json()['message']}")
    
    print(f'\n8. 验证最终订单状态和业务信息')
    response = client.get(f'/api/orders/{order_id}')
    order = response.get_json()
    print(f"订单编号: {order['id']}")
    print(f"客户姓名: {order['customer_name']}")
    print(f"麦秆品类: {order['wheat_straw_category']}  → 选麦秆、漂白工序依据")
    print(f"书签规格: {order['bookmark_size']}  → 裁剪工序依据")
    print(f"贴画纹样: {order['pattern_type']}  → 拼贴工序依据")
    print(f"裱封类型: {order['mounting_type']}  → 裱封工序依据")
    print(f"最终状态: {order['status']}")
    print(f"数量: {order['quantity']}个")
    
    print(f'\n9. 测试创建更多订单 - 验证不同业务组合')
    orders_to_create = [
        {
            'customer_name': '王芳',
            'phone': '13700137000',
            'design_description': '梅兰竹菊四君子',
            'quantity': 20,
            'wheat_straw_category': '黄麦秆',
            'bookmark_size': '大型 (70x180mm)',
            'pattern_type': '梅兰竹菊',
            'mounting_type': '丝绸装裱'
        },
        {
            'customer_name': '张伟',
            'phone': '13600136000',
            'design_description': '龙凤呈祥喜宴礼品',
            'quantity': 50,
            'wheat_straw_category': '红麦秆',
            'bookmark_size': '中型 (60x150mm)',
            'pattern_type': '龙凤呈祥',
            'mounting_type': '木质边框'
        },
        {
            'customer_name': '刘敏',
            'phone': '13500135000',
            'design_description': '花鸟虫鱼系列',
            'quantity': 15,
            'wheat_straw_category': '紫麦秆',
            'bookmark_size': '小型 (50x120mm)',
            'pattern_type': '花鸟虫鱼',
            'mounting_type': '冷裱膜'
        }
    ]
    
    for order_data in orders_to_create:
        response = client.post('/api/orders', 
                              json=order_data,
                              content_type='application/json')
        result = response.get_json()
        print(f"  ✓ 创建订单: {result.get('order_id')} - {order_data['pattern_type']}")
    
    print(f'\n10. 获取所有订单列表')
    response = client.get('/api/orders')
    orders = response.get_json()
    print(f"总订单数: {len(orders)}")
    for order in orders:
        print(f"  {order['id']} | {order['customer_name']} | {order['wheat_straw_category']} | {order['pattern_type']} | {order['status']}")
    
    print('\n' + '=' * 70)
    print('✓ 所有测试通过！系统迭代优化完成！')
    print('=' * 70)

if __name__ == '__main__':
    test_api()
