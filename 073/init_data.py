import os
import django
from datetime import date, time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'driving_school.settings')
django.setup()

from management.models import Student, Coach, Vehicle, CoachSchedule, SubjectHourConfig


def init_test_data():
    print("开始初始化测试数据...")

    print("\n0. 创建科目学时配置...")
    subjects_data = [
        {
            'subject_name': '科目二',
            'max_daily_hours': 4.0,
            'description': '场地驾驶技能培训',
        },
        {
            'subject_name': '科目三',
            'max_daily_hours': 4.0,
            'description': '道路驾驶技能培训',
        },
        {
            'subject_name': '科目一',
            'max_daily_hours': 6.0,
            'description': '理论知识培训',
        },
    ]
    
    for data in subjects_data:
        subject, created = SubjectHourConfig.objects.get_or_create(
            subject_name=data['subject_name'],
            defaults=data
        )
        if created:
            print(f"  创建科目: {subject.subject_name}")
        else:
            print(f"  科目已存在: {subject.subject_name}")

    print("\n1. 创建学员数据...")
    students_data = [
        {
            'name': '张三',
            'id_card': '110101199001011234',
            'phone': '13800138001',
            'gender': 'male',
            'age': 34,
            'address': '北京市朝阳区',
            'license_type': 'C1',
            'total_hours': 60,
            'completed_hours': 20,
        },
        {
            'name': '李四',
            'id_card': '110101199502021235',
            'phone': '13800138002',
            'gender': 'female',
            'age': 29,
            'address': '北京市海淀区',
            'license_type': 'C2',
            'total_hours': 60,
            'completed_hours': 15,
        },
        {
            'name': '王五',
            'id_card': '110101199803031236',
            'phone': '13800138003',
            'gender': 'male',
            'age': 26,
            'address': '北京市西城区',
            'license_type': 'C1',
            'total_hours': 60,
            'completed_hours': 0,
        },
    ]

    for data in students_data:
        student, created = Student.objects.get_or_create(
            id_card=data['id_card'],
            defaults=data
        )
        if created:
            print(f"  创建学员: {student.name}")
        else:
            print(f"  学员已存在: {student.name}")

    print("\n2. 创建教练数据...")
    coaches_data = [
        {
            'name': '赵教练',
            'id_card': '110101198004041237',
            'phone': '13900139001',
            'gender': 'male',
            'age': 44,
            'license_number': 'JL20200001',
            'teach_type': 'C1/C2',
            'experience': 15,
            'status': 'available',
        },
        {
            'name': '钱教练',
            'id_card': '110101198505051238',
            'phone': '13900139002',
            'gender': 'female',
            'age': 39,
            'license_number': 'JL20200002',
            'teach_type': 'C1/C2',
            'experience': 10,
            'status': 'available',
        },
    ]

    coaches = []
    for data in coaches_data:
        coach, created = Coach.objects.get_or_create(
            id_card=data['id_card'],
            defaults=data
        )
        coaches.append(coach)
        if created:
            print(f"  创建教练: {coach.name}")
        else:
            print(f"  教练已存在: {coach.name}")

    print("\n3. 创建车辆数据...")
    vehicles_data = [
        {
            'plate_number': '京A12345',
            'vehicle_type': '大众朗逸',
            'brand': '大众',
            'color': '白色',
            'purchase_date': date(2022, 1, 15),
            'mileage': 15000,
            'status': 'available',
        },
        {
            'plate_number': '京B67890',
            'vehicle_type': '丰田卡罗拉',
            'brand': '丰田',
            'color': '黑色',
            'purchase_date': date(2022, 3, 20),
            'mileage': 12000,
            'status': 'available',
        },
    ]

    vehicles = []
    for i, data in enumerate(vehicles_data):
        data['current_coach'] = coaches[i] if i < len(coaches) else None
        vehicle, created = Vehicle.objects.get_or_create(
            plate_number=data['plate_number'],
            defaults=data
        )
        vehicles.append(vehicle)
        if created:
            print(f"  创建车辆: {vehicle.plate_number}")
        else:
            print(f"  车辆已存在: {vehicle.plate_number}")

    print("\n4. 创建教练排班数据...")
    from datetime import datetime, timedelta
    today = date.today()
    
    for coach in coaches:
        for day_offset in range(7):
            schedule_date = today + timedelta(days=day_offset)
            for start_hour in [8, 10, 13, 15]:
                schedule, created = CoachSchedule.objects.get_or_create(
                    coach=coach,
                    schedule_date=schedule_date,
                    start_time=time(start_hour, 0),
                    end_time=time(start_hour + 2, 0),
                    defaults={'is_booked': False}
                )
                if created:
                    print(f"  创建排班: {coach.name} - {schedule_date} {start_hour}:00")

    print("\n测试数据初始化完成!")
    print(f"\n总计:")
    print(f"  科目配置: {SubjectHourConfig.objects.count()} 个")
    print(f"  学员: {Student.objects.count()} 人")
    print(f"  教练: {Coach.objects.count()} 人")
    print(f"  车辆: {Vehicle.objects.count()} 辆")
    print(f"  排班: {CoachSchedule.objects.count()} 条")


if __name__ == '__main__':
    init_test_data()
