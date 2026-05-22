#!/usr/bin/env python
import os
import django
from datetime import datetime, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

from hr_system.models import Department, Position, Employee, Attendance, Leave, Overtime, Salary


def init_test_data():
    print('开始初始化测试数据...')

    print('1. 创建部门...')
    dept1 = Department.objects.create(name='技术部', desc='负责产品开发和技术维护')
    dept2 = Department.objects.create(name='人事部', desc='负责人力资源管理')
    dept3 = Department.objects.create(name='财务部', desc='负责财务管理')
    dept4 = Department.objects.create(name='市场部', desc='负责市场营销和销售')
    departments = [dept1, dept2, dept3, dept4]
    print(f'   创建了 {len(departments)} 个部门')

    print('2. 创建职位...')
    pos1 = Position.objects.create(name='Python开发工程师', base_salary=15000, department=dept1)
    pos2 = Position.objects.create(name='前端开发工程师', base_salary=14000, department=dept1)
    pos3 = Position.objects.create(name='人事专员', base_salary=8000, department=dept2)
    pos4 = Position.objects.create(name='财务会计', base_salary=9000, department=dept3)
    pos5 = Position.objects.create(name='市场经理', base_salary=12000, department=dept4)
    positions = [pos1, pos2, pos3, pos4, pos5]
    print(f'   创建了 {len(positions)} 个职位')

    print('3. 创建员工...')
    first_names = ['张', '李', '王', '刘', '陈', '杨', '赵', '黄', '周', '吴']
    last_names = ['伟', '芳', '娜', '秀英', '敏', '静', '丽', '强', '磊', '洋']
    
    employees = []
    for i in range(10):
        name = random.choice(first_names) + random.choice(last_names)
        dept = random.choice(departments)
        pos = random.choice([p for p in positions if p.department == dept] + [random.choice(positions)])
        
        employee = Employee.objects.create(
            name=name,
            gender=random.choice(['male', 'female']),
            phone=f'1{random.randint(3000000000, 9999999999)}',
            email=f'test{i+1}@example.com',
            id_card=f'{random.randint(100000000000000000, 999999999999999999)}',
            department=dept,
            position=pos,
            hire_date=datetime(2023, random.randint(1, 12), random.randint(1, 28)).date(),
            base_salary=pos.base_salary,
            address=f'上海市浦东新区测试街道{i+1}号'
        )
        employees.append(employee)
    print(f'   创建了 {len(employees)} 个员工')

    print('4. 创建考勤记录...')
    today = datetime.now().date()
    for i in range(30):
        date = today - timedelta(days=i)
        if date.weekday() >= 5:
            continue
            
        for employee in employees:
            if random.random() < 0.9:
                check_in_hour = random.choices([8, 9, 10], [0.6, 0.3, 0.1])[0]
                check_in_min = random.randint(0, 59)
                check_in = datetime.combine(date, datetime.min.time()) + timedelta(hours=check_in_hour, minutes=check_in_min)
                
                check_out_hour = random.choices([17, 18, 19, 20], [0.1, 0.7, 0.15, 0.05])[0]
                check_out_min = random.randint(0, 59)
                check_out = datetime.combine(date, datetime.min.time()) + timedelta(hours=check_out_hour, minutes=check_out_min)
                
                Attendance.objects.create(
                    employee=employee,
                    date=date,
                    check_in=check_in,
                    check_out=check_out
                )
    
    today_attendance = Attendance.objects.filter(date=today).count()
    print(f'   创建了 {Attendance.objects.count()} 条考勤记录（今日 {today_attendance} 条）')

    print('5. 创建请假记录...')
    leave_types = ['sick', 'personal', 'annual', 'marriage', 'maternity']
    for _ in range(15):
        employee = random.choice(employees)
        leave_type = random.choice(leave_types)
        start_date = today - timedelta(days=random.randint(0, 30))
        days = random.randint(1, 5)
        end_date = start_date + timedelta(days=days-1)
        
        leave = Leave.objects.create(
            employee=employee,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            reason=f'{["身体不适", "家庭事务", "年假休息", "结婚", "生育"][leave_types.index(leave_type)]}',
            status=random.choice(['pending', 'approved', 'rejected'])
        )
        if leave.status != 'pending':
            leave.approver = random.choice([e for e in employees if e.id != employee.id])
            leave.approval_remark = '已审批'
            leave.save()
    print(f'   创建了 {Leave.objects.count()} 条请假记录')

    print('6. 创建加班记录...')
    overtime_types = ['weekday', 'weekend', 'holiday']
    for _ in range(20):
        employee = random.choice(employees)
        overtime_type = random.choice(overtime_types)
        date = today - timedelta(days=random.randint(0, 30))
        
        overtime = Overtime.objects.create(
            employee=employee,
            overtime_type=overtime_type,
            date=date,
            start_time=datetime.strptime('18:30', '%H:%M').time(),
            end_time=datetime.strptime(f'{random.randint(20, 22)}:{random.randint(0, 59):02d}', '%H:%M').time(),
            reason='项目赶工',
            status=random.choice(['pending', 'approved', 'rejected'])
        )
        if overtime.status != 'pending':
            overtime.approver = random.choice([e for e in employees if e.id != employee.id])
            overtime.approval_remark = '已审批'
            overtime.save()
    print(f'   创建了 {Overtime.objects.count()} 条加班记录')

    print('7. 生成薪资记录...')
    current_year = today.year
    current_month = today.month
    
    for employee in employees:
        salary = Salary.objects.create(
            employee=employee,
            year=current_year,
            month=current_month,
            base_salary=employee.base_salary,
            bonus=random.randint(0, 1000)
        )
    print(f'   生成了 {Salary.objects.count()} 条薪资记录')

    print('\n测试数据初始化完成！')
    print(f'\n数据统计：')
    print(f'  - 部门：{Department.objects.count()} 个')
    print(f'  - 职位：{Position.objects.count()} 个')
    print(f'  - 员工：{Employee.objects.count()} 人')
    print(f'  - 考勤记录：{Attendance.objects.count()} 条')
    print(f'  - 请假记录：{Leave.objects.count()} 条')
    print(f'  - 加班记录：{Overtime.objects.count()} 条')
    print(f'  - 薪资记录：{Salary.objects.count()} 条')


if __name__ == '__main__':
    init_test_data()