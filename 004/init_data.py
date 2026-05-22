"""
初始化测试数据脚本
"""
import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_supermarket.settings')
django.setup()

from supermarket.models import Product, Member


def init_products():
    """初始化商品数据"""
    products_data = [
        {'name': '可口可乐', 'category': 'drink', 'price': 3.50, 'cost_price': 2.50, 'stock': 100, 'unit': '瓶'},
        {'name': '农夫山泉', 'category': 'drink', 'price': 2.00, 'cost_price': 1.20, 'stock': 200, 'unit': '瓶'},
        {'name': '统一泡面', 'category': 'food', 'price': 5.50, 'cost_price': 3.50, 'stock': 80, 'unit': '桶'},
        {'name': '乐事薯片', 'category': 'snack', 'price': 8.00, 'cost_price': 5.00, 'stock': 50, 'unit': '袋'},
        {'name': '笔记本', 'category': 'stationery', 'price': 15.00, 'cost_price': 8.00, 'stock': 30, 'unit': '本'},
        {'name': '中性笔', 'category': 'stationery', 'price': 2.00, 'cost_price': 0.80, 'stock': 200, 'unit': '支'},
        {'name': '牙膏', 'category': 'daily', 'price': 12.00, 'cost_price': 6.00, 'stock': 40, 'unit': '支'},
        {'name': '毛巾', 'category': 'daily', 'price': 18.00, 'cost_price': 10.00, 'stock': 25, 'unit': '条'},
    ]

    for i, data in enumerate(products_data, 1):
        product_id = f'SP{str(i).zfill(4)}'
        Product.objects.get_or_create(
            product_id=product_id,
            defaults=data
        )
    print(f"商品数据初始化完成，共 {len(products_data)} 条")


def init_members():
    """初始化会员数据"""
    members_data = [
        {'name': '张三', 'phone': '13800138001', 'points': 100},
        {'name': '李四', 'phone': '13800138002', 'points': 250},
        {'name': '王五', 'phone': '13800138003', 'points': 50},
    ]

    for i, data in enumerate(members_data, 1):
        member_id = f'M{str(i).zfill(6)}'
        Member.objects.get_or_create(
            member_id=member_id,
            defaults=data
        )
    print(f"会员数据初始化完成，共 {len(members_data)} 条")


if __name__ == '__main__':
    print("开始初始化测试数据...")
    init_products()
    init_members()
    print("测试数据初始化完成！")
