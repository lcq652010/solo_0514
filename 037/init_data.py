#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'milky_tea.settings')
django.setup()

from api.models import Category, Product, User


def init_data():
    print('开始初始化数据...')
    
    print('\n=== 创建测试用户 ===')
    users_data = [
        {
            'username': 'admin',
            'email': 'admin@example.com',
            'password': 'admin123',
            'role': 'admin',
            'is_superuser': True,
            'is_staff': True,
        },
        {
            'username': 'cashier',
            'email': 'cashier@example.com',
            'password': 'cashier123',
            'role': 'cashier',
            'is_superuser': False,
            'is_staff': False,
        },
        {
            'username': 'maker',
            'email': 'maker@example.com',
            'password': 'maker123',
            'role': 'maker',
            'is_superuser': False,
            'is_staff': False,
        },
    ]
    
    for user_data in users_data:
        if not User.objects.filter(username=user_data['username']).exists():
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                role=user_data['role'],
                is_superuser=user_data['is_superuser'],
                is_staff=user_data['is_staff'],
            )
            print(f'创建用户: {user.username} - 角色: {user.get_role_display()} - 密码: {user_data["password"]}')
        else:
            print(f'用户已存在: {user_data["username"]}')

    categories_data = [
        {'name': '奶茶系列', 'description': '经典奶茶饮品'},
        {'name': '果茶系列', 'description': '新鲜水果茶饮'},
        {'name': '咖啡系列', 'description': '精品咖啡饮品'},
        {'name': '甜品系列', 'description': '美味甜品小食'},
    ]

    categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(**cat_data)
        categories.append(category)
        if created:
            print(f'创建分类: {category.name}')

    products_data = [
        {
            'name': '珍珠奶茶',
            'category': categories[0],
            'price': 15.00,
            'stock': 100,
            'description': '经典珍珠奶茶，Q弹珍珠配上香浓奶茶',
            'is_available': True
        },
        {
            'name': '芋泥波波奶茶',
            'category': categories[0],
            'price': 18.00,
            'stock': 80,
            'description': '绵密芋泥配上波波，口感丰富',
            'is_available': True
        },
        {
            'name': '杨枝甘露',
            'category': categories[1],
            'price': 22.00,
            'stock': 50,
            'description': '芒果西柚椰奶完美搭配',
            'is_available': True
        },
        {
            'name': '柠檬茶',
            'category': categories[1],
            'price': 12.00,
            'stock': 120,
            'description': '清爽柠檬，解腻首选',
            'is_available': True
        },
        {
            'name': '美式咖啡',
            'category': categories[2],
            'price': 18.00,
            'stock': 60,
            'description': '经典美式咖啡，提神醒脑',
            'is_available': True
        },
        {
            'name': '拿铁咖啡',
            'category': categories[2],
            'price': 22.00,
            'stock': 70,
            'description': '丝滑拿铁，奶香浓郁',
            'is_available': True
        },
        {
            'name': '焦糖布丁',
            'category': categories[3],
            'price': 10.00,
            'stock': 40,
            'description': '香甜滑嫩的焦糖布丁',
            'is_available': True
        },
        {
            'name': '芒果班戟',
            'category': categories[3],
            'price': 16.00,
            'stock': 30,
            'description': '新鲜芒果配上奶油班戟',
            'is_available': True
        },
    ]

    for prod_data in products_data:
        product, created = Product.objects.get_or_create(
            name=prod_data['name'],
            defaults=prod_data
        )
        if created:
            print(f'创建商品: {product.name} - ¥{product.price} - 库存: {product.stock}')

    print('数据初始化完成!')


if __name__ == '__main__':
    init_data()
