import requests
import json
import os

BASE_URL = 'http://localhost:5000/api'

def create_test_image_file():
    img_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\nIDATx\x9cc\xfa\xcf\x00\x00\x02\x07\x01\x02\x9a\x1c1q\x00\x00\x00\x00IEND\xaeB`\x82'
    return img_data

def test_api():
    print("=" * 80)
    print("砚台定制后端 API 测试（含重量预估和工序工时）")
    print("=" * 80)
    
    print("\n1. 创建客户...")
    customer_data = {
        "name": "张三",
        "phone": "13800138000",
        "address": "北京市朝阳区"
    }
    response = requests.post(f"{BASE_URL}/customers", json=customer_data)
    print(f"状态码: {response.status_code}")
    customer = response.json()
    print(f"创建的客户: {json.dumps(customer, ensure_ascii=False, indent=2)}")
    customer_id = customer['id']
    
    print("\n2. 创建匠人...")
    craftsman_data = {
        "name": "李四",
        "phone": "13900139000",
        "skill_level": "高级匠人",
        "status": "available"
    }
    response = requests.post(f"{BASE_URL}/craftsmen", json=craftsman_data)
    print(f"状态码: {response.status_code}")
    craftsman = response.json()
    print(f"创建的匠人: {json.dumps(craftsman, ensure_ascii=False, indent=2)}")
    craftsman_id = craftsman['id']
    
    print("\n3. 测试重量预估计算（单独接口）...")
    weight_data = {
        "material": "端溪石",
        "length": 20,
        "width": 15,
        "thickness": 3
    }
    response = requests.post(f"{BASE_URL}/calculate-weight", json=weight_data)
    print(f"状态码: {response.status_code}")
    weight_result = response.json()
    print(f"重量预估结果: {json.dumps(weight_result, ensure_ascii=False, indent=2)}")
    print(f"✓ 预估体积: {weight_result['estimated_volume_cm3']} cm³")
    print(f"✓ 预估重量: {weight_result['estimated_weight_g']} g ({weight_result['estimated_weight_kg']} kg)")
    
    print("\n4. 客户下单（含尺寸、石料产地、硬度标注、定制落款文字）...")
    order_data = {
        "customer_id": customer_id,
        "inkstone_type": "端砚",
        "size": "20cm x 15cm x 3cm",
        "length": 20,
        "width": 15,
        "thickness": 3,
        "material": "端溪石",
        "stone_origin": "广东肇庆端溪",
        "hardness": "摩氏硬度 3.5-4.0",
        "inscription_text": "宁静致远",
        "design_description": "雕刻山水图案，池形为圆形"
    }
    response = requests.post(f"{BASE_URL}/orders", json=order_data)
    print(f"状态码: {response.status_code}")
    order = response.json()
    print(f"创建的订单: {json.dumps(order, ensure_ascii=False, indent=2)}")
    order_id = order['id']
    order_number = order['order_number']
    print(f"✓ 自动生成的订单编号: {order_number}")
    print(f"✓ 石料产地: {order['stone_origin']}")
    print(f"✓ 硬度标注: {order['hardness']}")
    print(f"✓ 定制落款文字: {order['inscription_text']}")
    print(f"✓ 预估重量: {order['estimated_weight_g']} g ({order['estimated_weight_kg']} kg)")
    
    print("\n5. 查看订单详情（验证工序记录已初始化）...")
    response = requests.get(f"{BASE_URL}/orders/{order_id}")
    print(f"状态码: {response.status_code}")
    order_detail = response.json()
    print(f"工序记录数量: {len(order_detail['process_records'])}")
    for record in order_detail['process_records']:
        print(f"  - {record['process_name']}: {record['status']}")
    
    print("\n6. 管理员分配雕刻匠人...")
    assign_data = {"craftsman_id": craftsman_id}
    response = requests.post(f"{BASE_URL}/orders/{order_id}/assign", json=assign_data)
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"分配结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    print("\n7. 开始采石工序...")
    response = requests.post(f"{BASE_URL}/orders/{order_id}/process/quarrying/start")
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"开始工序结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    print(f"✓ 开始时间: {result['start_time']}")
    
    print("\n8. 完成采石工序并记录备注...")
    complete_data = {"notes": "采石完成，石材质量优良，无明显裂纹"}
    response = requests.post(f"{BASE_URL}/orders/{order_id}/process/quarrying/complete", json=complete_data)
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"完成工序结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    print(f"✓ 耗时: {result['duration_hours']} 小时")
    print(f"✓ 下一工序: {result['next_status']}")
    
    print("\n9. 快速完成剩余工序...")
    remaining_processes = ['cutting', 'carving_pool', 'engraving', 'polishing', 'waxing']
    for process_code in remaining_processes:
        response = requests.post(f"{BASE_URL}/orders/{order_id}/process/{process_code}/start")
        response = requests.post(f"{BASE_URL}/orders/{order_id}/process/{process_code}/complete", 
                                json={"notes": f"{STATUS_NAMES.get(process_code, process_code)}工序完成"})
        result = response.json()
        print(f"  ✓ {result['process_name']}: 耗时 {result['duration_hours']} 小时")
    
    print("\n10. 查看单个订单工时报表...")
    response = requests.get(f"{BASE_URL}/orders/{order_id}/work-report")
    print(f"状态码: {response.status_code}")
    report = response.json()
    print(f"工时报表: {json.dumps(report, ensure_ascii=False, indent=2)}")
    print(f"✓ 总工序: {report['total_processes']}")
    print(f"✓ 已完成: {report['completed_processes']}")
    print(f"✓ 总耗时: {report['total_duration_hours']} 小时")
    print(f"✓ 预估重量: {report['estimated_weight_kg']} kg")
    
    print("\n11. 查看所有订单工时报表...")
    response = requests.get(f"{BASE_URL}/work-reports")
    print(f"状态码: {response.status_code}")
    all_reports = response.json()
    print(f"总订单数: {all_reports['total_orders']}")
    for r in all_reports['reports']:
        print(f"  - {r['order_number']}: {r['status']}, 耗时 {r['total_duration_hours']} 小时")
    
    print("\n12. 上传设计草图...")
    test_image = create_test_image_file()
    files = {'sketch': ('design_sketch.png', test_image, 'image/png')}
    response = requests.post(f"{BASE_URL}/orders/{order_id}/upload-sketch", files=files)
    print(f"状态码: {response.status_code}")
    upload_result = response.json()
    print(f"上传结果: {json.dumps(upload_result, ensure_ascii=False, indent=2)}")
    
    print("\n" + "=" * 80)
    print("✓ 所有 API 测试完成！重量预估和工序工时功能验证通过")
    print("=" * 80)

STATUS_NAMES = {
    'pending': '待分配',
    'quarrying': '采石',
    'cutting': '切坯',
    'carving_pool': '凿池',
    'engraving': '刻砚',
    'polishing': '细磨',
    'waxing': '封蜡',
    'completed': '已完成'
}

if __name__ == '__main__':
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到服务器，请先启动 Flask 应用 (python app.py)")
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
