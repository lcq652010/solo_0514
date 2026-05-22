from django.core.management.base import BaseCommand
from rental.models import Car, Customer
from datetime import date


class Command(BaseCommand):
    help = 'Initialize test data'

    def handle(self, *args, **options):
        self.stdout.write('Initializing test data...')

        cars_data = [
            {
                'plate_number': '京A12345',
                'brand': '大众',
                'model': '帕萨特',
                'color': '黑色',
                'seats': 5,
                'daily_rent': 300,
                'status': 'available'
            },
            {
                'plate_number': '京B67890',
                'brand': '丰田',
                'model': '凯美瑞',
                'color': '白色',
                'seats': 5,
                'daily_rent': 350,
                'status': 'available'
            },
            {
                'plate_number': '京C11111',
                'brand': '奔驰',
                'model': 'E级',
                'color': '银色',
                'seats': 5,
                'daily_rent': 800,
                'status': 'available'
            },
            {
                'plate_number': '京D22222',
                'brand': '宝马',
                'model': '5系',
                'color': '黑色',
                'seats': 5,
                'daily_rent': 750,
                'status': 'available'
            },
            {
                'plate_number': '京E33333',
                'brand': '奥迪',
                'model': 'A6L',
                'color': '黑色',
                'seats': 5,
                'daily_rent': 700,
                'status': 'available'
            },
        ]

        for car_data in cars_data:
            Car.objects.get_or_create(
                plate_number=car_data['plate_number'],
                defaults=car_data
            )

        customers_data = [
            {
                'name': '张三',
                'gender': 'male',
                'phone': '13800138001',
                'id_card': '110101199001011234',
                'driver_license': '110101199001011234',
                'address': '北京市朝阳区',
                'email': 'zhangsan@example.com'
            },
            {
                'name': '李四',
                'gender': 'female',
                'phone': '13800138002',
                'id_card': '110101199202025678',
                'driver_license': '110101199202025678',
                'address': '北京市海淀区',
                'email': 'lisi@example.com'
            },
            {
                'name': '王五',
                'gender': 'male',
                'phone': '13800138003',
                'id_card': '110101198803039012',
                'driver_license': '110101198803039012',
                'address': '北京市西城区',
                'email': 'wangwu@example.com'
            },
        ]

        for customer_data in customers_data:
            Customer.objects.get_or_create(
                phone=customer_data['phone'],
                defaults=customer_data
            )

        self.stdout.write(self.style.SUCCESS('Test data initialized successfully!'))
