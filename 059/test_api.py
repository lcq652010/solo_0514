import requests
import json

BASE_URL = 'http://localhost:5000/api'

def test_get_options():
    print("=== 获取所有工艺选项 ===")
    response = requests.get(f'{BASE_URL}/options')
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        options = response.json()
        print(f"胎体材质 ({len(options['body_materials'])}种): {options['body_materials']}")
        print(f"尺寸规格 ({len(options['size_specs'])}种): {options['size_specs']}")
        print(f"漆面工艺 ({len(options['lacquer_processes'])}种): {options['lacquer_processes']}")
        print(f"纹样图案 ({len(options['decorative_patterns'])}种): {options['decorative_patterns']}")

def test_create_order():
    print("\n=== 创建订单 ===")
    order_data = {
        'customer_name': '王师傅',
        'customer_phone': '13700137000',
        'customer_address': '苏州市姑苏区xxx街道',
        'teacup_style': '荷叶形茶托',
        'body_material': '楠木',
        'size_spec': '荷叶形-15cm',
        'lacquer_process': '描金',
        'decorative_pattern': '荷花莲花',
        'lacquer_color': '暗红色',
        'painting_details': '采用描金工艺绘制荷花，花瓣层次分明，金线勾勒',
        'polishing_requirements': '打磨至4000目，使用推光工艺，手感温润',
        'special_requirements': '底部落款：姑苏漆艺',
        'quantity': 3
    }
    response = requests.post(f'{BASE_URL}/orders', json=order_data)
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
    return result.get('order_no')

def test_get_order(order_no):
    print(f"\n=== 获取订单详情 {order_no} ===")
    response = requests.get(f'{BASE_URL}/orders/{order_no}')
    print(f"状态码: {response.status_code}")
    order = response.json()
    print(f"\n=== 各工序工艺依据 ===")
    print(f"【制胎工序】")
    print(f"  胎体材质: {order['body_material']}")
    print(f"  尺寸规格: {order['size_spec']}")
    print(f"  茶托样式: {order['teacup_style']}")
    print(f"\n【上漆工序】")
    print(f"  漆面工艺: {order['lacquer_process']}")
    print(f"  漆色: {order['lacquer_color']}")
    print(f"\n【莳绘工序】")
    print(f"  纹样图案: {order['decorative_pattern']}")
    print(f"  绘制细节: {order['painting_details']}")
    print(f"\n【打磨工序】")
    print(f"  打磨要求: {order['polishing_requirements']}")

def test_workflow(order_no):
    print(f"\n=== 模拟订单生产流程 ===")
    statuses = ['待接单', '制胎', '刮灰', '上漆', '莳绘', '打磨', '推光', '完工']
    
    for status in statuses:
        response = requests.put(f'{BASE_URL}/orders/{order_no}/status', json={'status': status})
        print(f"更新到 [{status}]: {'成功' if response.status_code == 200 else '失败'}")

if __name__ == '__main__':
    try:
        test_get_options()
        order_no = test_create_order()
        if order_no:
            test_get_order(order_no)
            test_workflow(order_no)
        print("\n=== 测试完成 ===")
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到服务器，请先运行 python app.py 启动服务器！")
    except Exception as e:
        print(f"错误: {e}")
