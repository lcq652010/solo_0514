#!/usr/bin/env python
"""
汽车租赁管理系统功能测试
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_rental_system.settings')
django.setup()

from datetime import date, timedelta
from decimal import Decimal
from rental.models import Car, Customer, Order
from rental.utils import validate_id_card, validate_phone, validate_driver_license


def test_identity_validation():
    """测试身份信息校验"""
    print("=" * 60)
    print("1. 身份信息校验测试")
    print("=" * 60)
    
    # 手机号测试
    test_phones = [
        ("13800138000", True, "有效手机号"),
        ("12345678901", False, "无效手机号"),
        ("1380013800", False, "长度不足"),
    ]
    print("\n手机号校验:")
    for phone, expected, desc in test_phones:
        is_valid, msg = validate_phone(phone)
        status = "✓ 通过" if is_valid == expected else "✗ 失败"
        print(f"  {phone}: {status} - {msg}")
    
    # 身份证测试
    print("\n身份证校验:")
    test_ids = [
        ("110101199003070812", True, "有效身份证"),
        ("11010119900307081", False, "长度不足"),
    ]
    for id_card, expected, desc in test_ids:
        is_valid, msg = validate_id_card(id_card)
        status = "✓ 通过" if is_valid == expected else "✗ 失败"
        print(f"  {id_card}: {status} - {msg}")


def test_car_management():
    """测试车辆管理"""
    print("\n" + "=" * 60)
    print("2. 车辆管理测试")
    print("=" * 60)
    
    # 清理旧数据
    Car.objects.all().delete()
    
    # 创建测试车辆
    car1 = Car.objects.create(
        plate_number="京A12345",
        brand="奔驰",
        model="E300L",
        car_type="豪华轿车",
        color="黑色",
        seats=5,
        daily_rent=Decimal('800.00'),
        overtime_rate=Decimal('1.5'),
        status='available'
    )
    
    car2 = Car.objects.create(
        plate_number="京B67890",
        brand="宝马",
        model="530Li",
        car_type="豪华轿车",
        color="白色",
        seats=5,
        daily_rent=Decimal('750.00'),
        overtime_rate=Decimal('1.5'),
        status='available'
    )
    
    car3 = Car.objects.create(
        plate_number="京C11111",
        brand="丰田",
        model="汉兰达",
        car_type="SUV",
        color="银色",
        seats=7,
        daily_rent=Decimal('400.00'),
        overtime_rate=Decimal('1.5'),
        status='available'
    )
    
    print(f"\n已创建测试车辆: {Car.objects.count()} 辆")
    
    # 测试按车型筛选
    suv_cars = Car.objects.filter(car_type__icontains='SUV')
    print(f"按车型筛选(SUV): {suv_cars.count()} 辆")
    
    # 测试按价格范围筛选
    expensive_cars = Car.objects.filter(daily_rent__gte=700)
    print(f"按价格筛选(>=700): {expensive_cars.count()} 辆")
    
    # 测试多状态筛选
    available_cars = Car.objects.filter(status__in=['available', 'rented'])
    print(f"多状态筛选(可租用+已出租): {available_cars.count()} 辆")


def test_customer_management():
    """测试客户管理"""
    print("\n" + "=" * 60)
    print("3. 客户管理测试")
    print("=" * 60)
    
    # 清理旧数据
    Customer.objects.all().delete()
    
    customer1 = Customer.objects.create(
        name="张三",
        gender="male",
        phone="13800138001",
        id_card="110101199001011234",
        driver_license="110101199001011234",
        address="北京市朝阳区",
        email="zhangsan@example.com"
    )
    
    customer2 = Customer.objects.create(
        name="李四",
        gender="female",
        phone="13800138002",
        id_card="110101199202025678",
        driver_license="110101199202025678",
        address="北京市海淀区",
        email="lisi@example.com"
    )
    
    print(f"\n已创建测试客户: {Customer.objects.count()} 人")
    
    # 测试按姓名筛选
    zhang_customer = Customer.objects.filter(name__icontains='张')
    print(f"按姓名筛选(张): {zhang_customer.count()} 人")
    
    # 测试按手机号筛选
    phone_customer = Customer.objects.filter(phone__icontains='13800138001')
    print(f"按手机号筛选: {phone_customer.count()} 人")


def test_order_management():
    """测试订单管理、时段冲突、超时费用计算"""
    print("\n" + "=" * 60)
    print("4. 订单管理测试")
    print("=" * 60)
    
    # 清理旧数据
    Order.objects.all().delete()
    
    car = Car.objects.first()
    customer = Customer.objects.first()
    
    today = date.today()
    
    # 创建订单1
    order1 = Order.objects.create(
        car=car,
        customer=customer,
        start_date=today,
        end_date=today + timedelta(days=3),
        pickup_location="总店",
        return_location="总店",
        rental_days=3,
        total_amount=car.daily_rent * 3,
        deposit=Decimal('1000.00'),
        status='pending'
    )
    
    print(f"\n创建订单: {order1.order_no}")
    print(f"  租期: {order1.start_date} ~ {order1.end_date} ({order1.rental_days} 天)")
    print(f"  预计金额: {order1.total_amount} 元")
    
    # 测试时段冲突检查
    conflict_order = Order(
        car=car,
        customer=customer,
        start_date=today + timedelta(days=1),
        end_date=today + timedelta(days=5),
        pickup_location="总店",
        return_location="总店",
        rental_days=4,
        total_amount=car.daily_rent * 4,
        deposit=Decimal('1000.00'),
        status='pending'
    )
    
    # 检查时段冲突
    existing_orders = Order.objects.filter(
        car=car,
        status__in=['pending', 'picked_up'],
        start_date__lte=conflict_order.end_date,
        end_date__gte=conflict_order.start_date
    )
    
    print(f"\n时段冲突测试:")
    print(f"  已有订单时段: {order1.start_date} ~ {order1.end_date}")
    print(f"  新订单时段: {conflict_order.start_date} ~ {conflict_order.end_date}")
    print(f"  检测到冲突订单: {existing_orders.count()} 个")
    
    # 测试取车操作
    print(f"\n取车操作测试:")
    print(f"  取车前车辆状态: {car.get_status_display()}")
    success = order1.pick_up_car()
    if success:
        print(f"  ✓ 取车成功")
        print(f"  实际取车时间: {order1.actual_start_date}")
        car.refresh_from_db()
        print(f"  取车后车辆状态: {car.get_status_display()}")
    
    # 测试还车操作（含超时费用计算）
    print(f"\n还车结算测试:")
    print(f"  预订还车日期: {order1.end_date}")
    
    # 模拟还车
    success = order1.return_car()
    if success:
        print(f"  ✓ 还车成功")
        print(f"  实际还车时间: {order1.actual_end_date}")
        print(f"  实际租赁天数: {order1.actual_rental_days} 天")
        print(f"  超时天数: {order1.overtime_days} 天")
        print(f"  基础租金: {order1.base_rental} 元")
        print(f"  超时费用: {order1.overtime_fee} 元")
        print(f"  实际结算金额: {order1.actual_amount} 元")
        car.refresh_from_db()
        print(f"  还车后车辆状态: {car.get_status_display()}")
    
    # 测试多条件筛选
    print(f"\n多条件筛选测试:")
    
    # 按客户姓名筛选
    customer_orders = Order.objects.filter(customer__name__icontains='张')
    print(f"  按客户姓名筛选(张): {customer_orders.count()} 个订单")
    
    # 按车辆品牌筛选
    brand_orders = Order.objects.filter(car__brand__icontains='奔驰')
    print(f"  按车辆品牌筛选(奔驰): {brand_orders.count()} 个订单")
    
    # 按车型筛选
    car_type_orders = Order.objects.filter(car__car_type__icontains='轿车')
    print(f"  按车型筛选(轿车): {car_type_orders.count()} 个订单")
    
    # 按状态多选筛选
    status_orders = Order.objects.filter(status__in=['pending', 'returned'])
    print(f"  按状态多选项筛选: {status_orders.count()} 个订单")


def test_statistics():
    """测试统计功能"""
    print("\n" + "=" * 60)
    print("5. 统计功能测试")
    print("=" * 60)
    
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    picked_up_orders = Order.objects.filter(status='picked_up').count()
    returned_orders = Order.objects.filter(status='returned').count()
    
    total_revenue = Order.objects.filter(status='returned').aggregate(
        total=models.Sum('actual_amount')
    )['total'] or 0
    
    total_overtime_fee = Order.objects.filter(status='returned').aggregate(
        total=models.Sum('overtime_fee')
    )['total'] or 0
    
    print(f"\n统计数据:")
    print(f"  总订单数: {total_orders}")
    print(f"  待取车: {pending_orders}")
    print(f"  已取车: {picked_up_orders}")
    print(f"  已还车: {returned_orders}")
    print(f"  总营收: {total_revenue} 元")
    print(f"  总超时费: {total_overtime_fee} 元")


def main():
    print("\n" + "=" * 60)
    print("汽车租赁管理系统 - 功能测试")
    print("=" * 60)
    
    try:
        test_identity_validation()
        test_car_management()
        test_customer_management()
        test_order_management()
        test_statistics()
        
        print("\n" + "=" * 60)
        print("✓ 所有测试完成!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ 测试出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    from django.db import models
    main()
