from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hospital.models import *
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = '初始化测试数据'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化测试数据...')

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write('超级管理员创建成功: admin / admin123')

        dept1, _ = Department.objects.get_or_create(name='内科', description='宠物内科诊疗')
        dept2, _ = Department.objects.get_or_create(name='外科', description='宠物外科诊疗')
        dept3, _ = Department.objects.get_or_create(name='皮肤科', description='宠物皮肤疾病诊疗')
        dept4, _ = Department.objects.get_or_create(name='牙科', description='宠物口腔及牙科诊疗')
        self.stdout.write('科室数据初始化完成')

        for i in range(1, 4):
            if not User.objects.filter(username=f'user{i}').exists():
                user = User.objects.create_user(f'user{i}', f'user{i}@example.com', '123456')
                staff_role = 'doctor' if i == 1 else 'receptionist' if i == 2 else 'admin'
                Staff.objects.create(
                    user=user,
                    name=f'张医生' if i == 1 else f'李前台' if i == 2 else f'王管理员',
                    role=staff_role,
                    phone=f'1380013800{i}',
                    department=dept1 if i == 1 else None
                )
        self.stdout.write('员工账号初始化完成')

        doctor1, _ = Doctor.objects.get_or_create(
            name='张医生',
            defaults={
                'department': dept1,
                'title': '主任医师',
                'phone': '13800138001'
            }
        )
        Doctor.objects.get_or_create(
            name='李医生',
            defaults={
                'department': dept2,
                'title': '副主任医师',
                'phone': '13800138002'
            }
        )
        Doctor.objects.get_or_create(
            name='王医生',
            defaults={
                'department': dept3,
                'title': '主治医师',
                'phone': '13800138003'
            }
        )
        Doctor.objects.get_or_create(
            name='赵医生',
            defaults={
                'department': dept4,
                'title': '主治医师',
                'phone': '13800138004'
            }
        )
        self.stdout.write('医生数据初始化完成')

        owner1, _ = Owner.objects.get_or_create(
            name='陈先生',
            defaults={
                'phone': '13900139001',
                'address': '北京市朝阳区xxx街道'
            }
        )
        owner2, _ = Owner.objects.get_or_create(
            name='林女士',
            defaults={
                'phone': '13900139002',
                'address': '北京市海淀区xxx街道'
            }
        )
        owner3, _ = Owner.objects.get_or_create(
            name='黄先生',
            defaults={
                'phone': '13900139003',
                'address': '北京市西城区xxx街道'
            }
        )
        self.stdout.write('主人数据初始化完成')

        Pet.objects.get_or_create(
            name='豆豆',
            owner=owner1,
            defaults={
                'species': '金毛犬',
                'breed': '犬科',
                'gender': 'male',
                'age': 3,
                'weight': 25.5,
                'description': '金黄色长毛，性格温顺'
            }
        )
        Pet.objects.get_or_create(
            name='咪咪',
            owner=owner2,
            defaults={
                'species': '英短蓝猫',
                'breed': '猫科',
                'gender': 'female',
                'age': 2,
                'weight': 4.2,
                'description': '蓝灰色短毛，眼睛橘色'
            }
        )
        Pet.objects.get_or_create(
            name='旺财',
            owner=owner3,
            defaults={
                'species': '泰迪',
                'breed': '犬科',
                'gender': 'male',
                'age': 1,
                'weight': 3.5,
                'description': '棕色卷毛，活泼好动'
            }
        )
        self.stdout.write('宠物数据初始化完成')

        Medicine.objects.get_or_create(
            name='阿莫西林胶囊',
            defaults={
                'category': 'antibiotic',
                'specification': '0.25g*24粒',
                'unit': '盒',
                'price': 25.00,
                'stock': 100,
                'manufacturer': '华北制药',
                'expiry_date': timezone.now().date() + timedelta(days=365)
            }
        )
        Medicine.objects.get_or_create(
            name='布洛芬片',
            defaults={
                'category': 'anti_inflammatory',
                'specification': '0.1g*100片',
                'unit': '瓶',
                'price': 15.00,
                'stock': 50,
                'manufacturer': '东北制药',
                'expiry_date': timezone.now().date() + timedelta(days=500)
            }
        )
        Medicine.objects.get_or_create(
            name='复合维生素B',
            defaults={
                'category': 'vitamin',
                'specification': '100片',
                'unit': '瓶',
                'price': 12.00,
                'stock': 80,
                'manufacturer': '民生药业',
                'expiry_date': timezone.now().date() + timedelta(days=730)
            }
        )
        Medicine.objects.get_or_create(
            name='红霉素软膏',
            defaults={
                'category': 'external',
                'specification': '10g',
                'unit': '支',
                'price': 8.00,
                'stock': 200,
                'manufacturer': '马应龙药业',
                'expiry_date': timezone.now().date() + timedelta(days=365)
            }
        )
        self.stdout.write('药品数据初始化完成')

        self.stdout.write(self.style.SUCCESS('所有测试数据初始化完成！'))
        self.stdout.write('登录账号:')
        self.stdout.write('  管理员: admin / admin123 (超级管理员)')
        self.stdout.write('  医生: user1 / 123456 (医生角色)')
        self.stdout.write('  前台: user2 / 123456 (前台角色)')
        self.stdout.write('  管理员: user3 / 123456 (管理员角色)')
