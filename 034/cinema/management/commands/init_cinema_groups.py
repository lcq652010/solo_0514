from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = '初始化电影院管理系统的用户组（管理员、售票员、检票员）'

    def handle(self, *args, **options):
        group_names = ['管理员', '售票员', '检票员']

        for name in group_names:
            group, created = Group.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ 创建用户组: {name}'))
            else:
                self.stdout.write(self.style.WARNING(f'ℹ️  用户组已存在: {name}'))

        self.stdout.write('\n用户组初始化完成！')
        self.stdout.write('\n请在Django后台将用户添加到相应用户组以分配权限。')
        self.stdout.write('''
权限说明:
  - 管理员: 系统所有权限，包括用户管理
  - 售票员: 查看影片/影厅/排期，创建订单、退票、完结订单、查看统计
  - 检票员: 查看影片/影厅/排期，执行检票操作
''')
