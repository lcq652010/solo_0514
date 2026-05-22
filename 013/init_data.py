import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery.settings')
django.setup()

from api.models import Shop, Product, Rider


def init_data():
    print('开始初始化数据...')

    if not Shop.objects.exists():
        shop1 = Shop.objects.create(
            name='美味快餐店',
            address='北京市朝阳区建国路88号',
            phone='010-12345678',
            description='主营各种快餐美食，美味又实惠',
            is_open=True
        )
        print(f'创建店铺: {shop1.name}')

        shop2 = Shop.objects.create(
            name='香满园餐厅',
            address='北京市海淀区中关村大街1号',
            phone='010-87654321',
            description='正宗川菜，麻辣鲜香',
            is_open=True
        )
        print(f'创建店铺: {shop2.name}')

        products_data = [
            {'name': '红烧肉', 'price': 38.00, 'category': '热菜', 'stock': 50},
            {'name': '宫保鸡丁', 'price': 32.00, 'category': '热菜', 'stock': 60},
            {'name': '鱼香肉丝', 'price': 28.00, 'category': '热菜', 'stock': 45},
            {'name': '米饭', 'price': 2.00, 'category': '主食', 'stock': 200},
            {'name': '可乐', 'price': 5.00, 'category': '饮品', 'stock': 100},
        ]

        for pd in products_data:
            Product.objects.create(shop=shop1, **pd)
            print(f'创建商品: {pd["name"]}')

        products_data2 = [
            {'name': '麻婆豆腐', 'price': 22.00, 'category': '热菜', 'stock': 40},
            {'name': '水煮鱼', 'price': 58.00, 'category': '热菜', 'stock': 30},
            {'name': '回锅肉', 'price': 42.00, 'category': '热菜', 'stock': 35},
            {'name': '担担面', 'price': 18.00, 'category': '主食', 'stock': 50},
            {'name': '雪碧', 'price': 5.00, 'category': '饮品', 'stock': 100},
        ]

        for pd in products_data2:
            Product.objects.create(shop=shop2, **pd)
            print(f'创建商品: {pd["name"]}')

    if not Rider.objects.exists():
        riders_data = [
            {'name': '张三', 'phone': '13800138001', 'id_card': '110101199001010001', 'vehicle_type': 'electric'},
            {'name': '李四', 'phone': '13800138002', 'id_card': '110101199001010002', 'vehicle_type': 'electric'},
            {'name': '王五', 'phone': '13800138003', 'id_card': '110101199001010003', 'vehicle_type': 'motorcycle'},
        ]

        for rd in riders_data:
            Rider.objects.create(**rd)
            print(f'创建骑手: {rd["name"]}')

    print('数据初始化完成!')


if __name__ == '__main__':
    init_data()
