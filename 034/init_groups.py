#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema_system.settings')
django.setup()

from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType


def init_groups():
    group_names = ['管理员', '售票员', '检票员']
    
    for name in group_names:
        group, created = Group.objects.get_or_create(name=name)
        if created:
            print(f'✅ 创建用户组: {name}')
        else:
            print(f'ℹ️  用户组已存在: {name}')
    
    print('\n用户组初始化完成！')
    print('\n请在Django后台将用户添加到相应用户组以分配权限。')


if __name__ == '__main__':
    init_groups()
