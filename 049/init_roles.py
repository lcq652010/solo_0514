#!/usr/bin/env python
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wholesale_system.settings')

import django
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile


def create_user(username, password, role, email='', first_name='', last_name=''):
    try:
        user = User.objects.get(username=username)
        print(f'用户 {username} 已存在')
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        print(f'创建用户: {username}')
    
    try:
        profile = UserProfile.objects.get(user=user)
        profile.role = role
        profile.save()
        print(f'更新角色: {role}')
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(
            user=user,
            role=role
        )
        print(f'创建角色: {role}')
    
    return user


if __name__ == '__main__':
    print('=' * 50)
    print('初始化用户角色')
    print('=' * 50)
    
    create_user(
        username='admin',
        password='admin123',
        role='boss',
        first_name='管理员',
        last_name=''
    )
    
    create_user(
        username='order_clerk',
        password='order123',
        role='order_clerk',
        first_name='开单员',
        last_name=''
    )
    
    create_user(
        username='warehouse',
        password='warehouse123',
        role='warehouse_manager',
        first_name='库管',
        last_name=''
    )
    
    create_user(
        username='boss',
        password='boss123',
        role='boss',
        first_name='老板',
        last_name=''
    )
    
    print('=' * 50)
    print('用户创建完成')
    print('=' * 50)
    print('\n登录账号:')
    print('  老板(admin): admin / admin123')
    print('  开单员: order_clerk / order123')
    print('  库管: warehouse / warehouse123')
    print('  老板(boss): boss / boss123')
