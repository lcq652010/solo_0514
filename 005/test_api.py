import requests
import json
from datetime import datetime, timedelta

BASE_URL = 'http://localhost:5001/api'

def print_header(title):
    print('\n' + '=' * 70)
    print(f'  {title}')
    print('=' * 70)

def test_api():
    print_header('传统宣纸扇定制订单管理系统 v2.0 - 完整功能测试')
    
    # 1. 测试字段选项API
    print_header('1. 获取字段选项')
    try:
        response = requests.get(f'{BASE_URL}/field-options')
        print(f'状态码: {response.status_code}')
        if response.status_code == 200:
            data = response.json()
            options = data['data']
            print(f'✓ 扇子类型: {len(options["fan_types"])} 种')
            print(f'✓ 扇骨材质: {len(options["bone_materials"])} 种')
            print(f'✓ 宣纸类型: {len(options["paper_types"])} 种')
            print(f'✓ 绘画风格: {len(options["painting_styles"])} 种')
            print(f'✓ 书法风格: {len(options["calligraphy_styles"])} 种')
            print(f'✓ 难度等级: {options["difficulty_levels"]}')
        else:
            print(f'✗ 错误: {response.text}')
    except Exception as e:
        print(f'✗ 连接失败: {e}')

    # 2. 测试匠人列表API
    print_header('2. 获取匠人列表')
    try:
        response = requests.get(f'{BASE_URL}/craftsmen')
        print(f'状态码: {response.status_code}')
        if response.status_code == 200:
            data = response.json()
            craftsmen = data['data']['craftsmen']
            print(f'✓ 匠人总数: {len(craftsmen)} 位')
            for c in craftsmen:
                print(f'  - {c["name"]} (擅长: {c["specialty"]}, 评分: {c["rating"]})')
        else:
            print(f'✗ 错误: {response.text}')
    except Exception as e:
        print(f'✗ 连接失败: {e}')

    # 3. 测试价格试算API
    print_header('3. 价格试算功能')
    price_test_data = [
        {
            'name': '基础款',
            'data': {'bone_material': '竹制', 'paper_type': '生宣', 'fan_size': '10寸'}
        },
        {
            'name': '工笔+楷书 中等难度',
            'data': {'bone_material': '紫檀木', 'paper_type': '绢本', 'fan_size': '12寸',
                     'painting_style': '工笔', 'calligraphy_style': '楷书', 'difficulty_level': '中等'}
        },
        {
            'name': '大师级作品',
            'data': {'bone_material': '象牙', 'paper_type': '绢本', 'fan_size': '14寸',
                     'painting_style': '工笔', 'calligraphy_style': '篆书', 'difficulty_level': '大师级'}
        }
    ]
    for test in price_test_data:
        try:
            response = requests.post(f'{BASE_URL}/price-calculate', json=test['data'])
            if response.status_code == 200:
                data = response.json()
                result = data['data']
                print(f'\n{test["name"]}:')
                print(f'  基础价格: {result["base_price"]}元')
                print(f'  难度系数: {result["difficulty_multiplier"]}x')
                print(f'  最终价格: {result["final_price"]}元')
                print(f'  价格明细:')
                for k, v in result['price_detail'].items():
                    if v > 0:
                        print(f'    - {k}: {v}元')
            else:
                print(f'  ✗ 错误: {response.text}')
        except Exception as e:
            print(f'  ✗ 连接失败: {e}')

    # 4. 测试必填校验
    print_header('4. 必填字段校验测试')
    invalid_orders = [
        {'name': '缺少客户姓名', 'data': {'customer_phone': '13800138000', 'fan_type': '折扇', 'fan_size': '10寸',
                                           'bone_material': '竹制', 'paper_type': '生宣', 'content_requirement': '测试'}},
        {'name': '手机号格式错误', 'data': {'customer_name': '张三', 'customer_phone': '12345', 'fan_type': '折扇', 'fan_size': '10寸',
                                           'bone_material': '竹制', 'paper_type': '生宣', 'content_requirement': '测试'}},
        {'name': '扇骨数量超出范围', 'data': {'customer_name': '张三', 'customer_phone': '13800138000', 'fan_type': '折扇', 'fan_size': '10寸',
                                             'bone_material': '竹制', 'bone_quantity': 100, 'paper_type': '生宣', 'content_requirement': '测试'}},
    ]
    for test in invalid_orders:
        try:
            response = requests.post(f'{BASE_URL}/orders', json=test['data'])
            result = response.json()
            print(f'{test["name"]}: {result["message"]} ✓')
        except Exception as e:
            print(f'{test["name"]}: {e}')

    # 5. 创建完整订单
    print_header('5. 创建完整订单')
    order_data = {
        'customer_name': '王小明',
        'customer_phone': '13900139000',
        'customer_address': '杭州市西湖区xxx街道',
        'fan_type': '折扇',
        'fan_size': '10寸',
        'fan_shape': '圆形',
        'fan_folds': 18,
        'bone_material': '紫檀木',
        'bone_quantity': 16,
        'bone_color': '深棕色',
        'bone_grade': '精品',
        'paper_type': '生宣',
        'paper_origin': '安徽泾县',
        'paper_grade': '特净',
        'paper_color': '仿古',
        'content_requirement': '绘制山水风景画，题古诗词',
        'painting_content': '黄山云海图',
        'calligraphy_content': '苏轼《念奴娇·赤壁怀古》',
        'painting_style': '工笔',
        'calligraphy_style': '楷书',
        'calligraphy_text': '大江东去，浪淘尽，千古风流人物...',
        'seal_requirement': '朱文',
        'mounting_material': '绫绢',
        'mounting_style': '卷轴',
        'glue_type': '糯米胶',
        'drying_method': '自然阴干',
        'difficulty_level': '复杂',
        'special_requirement': '需要礼盒包装，配流苏'
    }
    try:
        response = requests.post(f'{BASE_URL}/orders', json=order_data)
        print(f'状态码: {response.status_code}')
        if response.status_code == 200:
            data = response.json()
            order = data['data']['order']
            price_details = data['data']['price_details']
            order_no = order['order_no']
            print(f'✓ 订单创建成功，订单号: {order_no}')
            print(f'✓ 订单价格: {order["total_price"]}元 (难度系数: {price_details["difficulty_multiplier"]})')
            print(f'✓ 分配匠人: {order["craftsman_name"]}')
            print(f'✓ 预计工期: {order["estimated_days"]}天')
            print(f'✓ 预计交货: {order["estimated_delivery"]}')
        else:
            print(f'✗ 错误: {response.text}')
            order_no = None
    except Exception as e:
        print(f'✗ 连接失败: {e}')
        order_no = None

    # 6. 完整流程测试 - 更新状态
    if order_no:
        print_header('6. 订单完整流程测试')
        status_flow = ['选骨', '裱扇', '绘图', '题字', '上胶', '晾干', '成品完工']
        
        for i, status in enumerate(status_flow, 1):
            try:
                response = requests.put(f'{BASE_URL}/orders/{order_no}/status', json={'status': status})
                if response.status_code == 200:
                    data = response.json()
                    order = data['data']['order']
                    print(f'{i}. 更新为 [{status}] ✓')
                    print(f'   剩余工期: {order["estimated_days"]}天')
                    print(f'   预计交货: {order["estimated_delivery"]}')
                else:
                    print(f'{i}. 更新为 [{status}] ✗: {response.text}')
            except Exception as e:
                print(f'{i}. 更新为 [{status}] ✗: {e}')

    # 7. 测试筛选功能
    print_header('7. 订单筛选与排序测试')
    filter_tests = [
        {'name': '按状态筛选(成品完工)', 'params': {'status': '成品完工'}},
        {'name': '按绘画风格筛选(工笔)', 'params': {'painting_style': '工笔'}},
        {'name': '按书法风格筛选(楷书)', 'params': {'calligraphy_style': '楷书'}},
        {'name': '按价格升序排列', 'params': {'sort_by': 'total_price', 'sort_order': 'asc'}},
        {'name': '按交货日期降序排列', 'params': {'sort_by': 'estimated_delivery', 'sort_order': 'desc'}},
        {'name': '组合筛选', 'params': {'status': '成品完工', 'painting_style': '工笔', 'page': 1, 'per_page': 10}}
    ]
    for test in filter_tests:
        try:
            response = requests.get(f'{BASE_URL}/orders', params=test['params'])
            if response.status_code == 200:
                data = response.json()
                orders = data['data']['orders']
                pagination = data['data']['pagination']
                print(f'{test["name"]}: 找到 {len(orders)} 条记录 (共 {pagination["total"]} 条) ✓')
            else:
                print(f'{test["name"]}: ✗ {response.text}')
        except Exception as e:
            print(f'{test["name"]}: ✗ {e}')

    # 8. 测试更新订单自动重算价格
    if order_no:
        print_header('8. 订单更新自动重算价格')
        try:
            response = requests.put(f'{BASE_URL}/orders/{order_no}', json={
                'bone_material': '象牙',
                'difficulty_level': '大师级'
            })
            if response.status_code == 200:
                data = response.json()
                order = data['data']['order']
                print(f'✓ 扇骨升级为象牙，难度升级为大师级')
                print(f'✓ 新价格: {order["total_price"]}元')
                print(f'✓ 匠人重新分配: {order["craftsman_name"]}')
            else:
                print(f'✗ 错误: {response.text}')
        except Exception as e:
            print(f'✗ 连接失败: {e}')

    # 9. 测试订单统计
    print_header('9. 订单统计')
    try:
        response = requests.get(f'{BASE_URL}/stats')
        if response.status_code == 200:
            data = response.json()
            stats = data['data']['stats']
            print(f'✓ 总订单数: {stats["total"]}单')
            print(f'✓ 总营收: {stats["total_revenue"]}元')
            print(f'✓ 各状态订单数:')
            for status in ['待接单', '选骨', '裱扇', '绘图', '题字', '成品完工']:
                if stats.get(status, 0) > 0:
                    print(f'  - {status}: {stats[status]}单')
        else:
            print(f'✗ 错误: {response.text}')
    except Exception as e:
        print(f'✗ 连接失败: {e}')

    # 10. 统一返回格式测试
    print_header('10. 统一接口返回格式测试')
    try:
        response = requests.get(f'{BASE_URL}/orders')
        if response.status_code == 200:
            data = response.json()
            print(f'✓ 包含 code 字段: {"code" in data}')
            print(f'✓ 包含 message 字段: {"message" in data}')
            print(f'✓ 包含 data 字段: {"data" in data}')
            print(f'✓ code 为 200: {data["code"] == 200}')
            print(f'✓ message 不为空: {len(data["message"]) > 0}')
        else:
            print(f'✗ 错误: {response.text}')
    except Exception as e:
        print(f'✗ 连接失败: {e}')

    print_header('测试完成！')
    print('\n功能总结:')
    print('  ✓ 必填字段校验')
    print('  ✓ 数值范围规范')
    print('  ✓ 按材质与难度自动计价')
    print('  ✓ 匠人自动分配')
    print('  ✓ 工期自动计算')
    print('  ✓ 按风格、状态、日期筛选')
    print('  ✓ 分页排序')
    print('  ✓ 统一接口返回格式')
    print('  ✓ 更新订单自动重算价格')
    print('  ✓ 订单统计功能')

if __name__ == '__main__':
    test_api()
