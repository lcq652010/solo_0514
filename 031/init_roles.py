#!/usr/bin/env python
"""
初始化用户角色脚本
使用方法: python manage.py shell < init_roles.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_management.settings')
django.setup()

from django.contrib.auth.models import User
from hotel.models import UserProfile


def create_user_with_role(username, password, role, email='', real_name='', phone=''):
    """创建用户并分配角色"""
    try:
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        UserProfile.objects.create(
            user=user,
            role=role,
            real_name=real_name,
            phone=phone
        )
        print(f'✓ 成功创建用户: {username} ({role})')
        return user
    except Exception as e:
        print(f'✗ 创建用户失败 {username}: {e}')
        return None


def main():
    print('=' * 50)
    print('开始初始化用户角色...')
    print('=' * 50)

    create_user_with_role(
        username='admin',
        password='admin123',
        role='admin',
        email='admin@hotel.com',
        real_name='系统管理员',
        phone='13800138000'
    )

    create_user_with_role(
        username='receptionist',
        password='receptionist123',
        role='receptionist',
        email='receptionist@hotel.com',
        real_name='前台接待',
        phone='13800138001'
    )

    create_user_with_role(
        username='housekeeper',
        password='housekeeper123',
        role='housekeeper',
        email='housekeeper@hotel.com',
        real_name='客房服务员',
        phone='13800138002'
    )

    print('=' * 50)
    print('用户角色初始化完成!')
    print('=' * 50)
    print('\n登录账号:')
    print('  管理员: admin / admin123')
    print('  前台: receptionist / receptionist123')
    print('  客房: housekeeper / housekeeper123')


if __name__ == '__main__':
    main()
