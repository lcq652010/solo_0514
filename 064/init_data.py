import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from attendance_app.models import Department, Employee


def init_data():
    dept1, _ = Department.objects.get_or_create(
        name='技术部',
        defaults={'description': '负责产品研发和技术支持'}
    )
    dept2, _ = Department.objects.get_or_create(
        name='人事部',
        defaults={'description': '负责人力资源管理'}
    )
    dept3, _ = Department.objects.get_or_create(
        name='财务部',
        defaults={'description': '负责财务管理'}
    )

    Employee.objects.get_or_create(
        emp_id='EMP001',
        defaults={
            'name': '张三',
            'gender': '男',
            'phone': '13800138001',
            'email': 'zhangsan@example.com',
            'department': dept1,
            'position': '高级工程师',
            'hire_date': date(2020, 1, 15),
            'base_salary': 15000,
            'is_active': True
        }
    )

    Employee.objects.get_or_create(
        emp_id='EMP002',
        defaults={
            'name': '李四',
            'gender': '女',
            'phone': '13800138002',
            'email': 'lisi@example.com',
            'department': dept1,
            'position': '前端工程师',
            'hire_date': date(2021, 3, 10),
            'base_salary': 12000,
            'is_active': True
        }
    )

    Employee.objects.get_or_create(
        emp_id='EMP003',
        defaults={
            'name': '王五',
            'gender': '男',
            'phone': '13800138003',
            'email': 'wangwu@example.com',
            'department': dept2,
            'position': '人事经理',
            'hire_date': date(2019, 6, 1),
            'base_salary': 13000,
            'is_active': True
        }
    )

    Employee.objects.get_or_create(
        emp_id='EMP004',
        defaults={
            'name': '赵六',
            'gender': '女',
            'phone': '13800138004',
            'email': 'zhaoliu@example.com',
            'department': dept3,
            'position': '财务主管',
            'hire_date': date(2020, 11, 20),
            'base_salary': 14000,
            'is_active': True
        }
    )

    print('初始化数据创建成功！')


if __name__ == '__main__':
    init_data()
