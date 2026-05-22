from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
import random
import string


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('receptionist', '前台'),
        ('housekeeper', '客房服务'),
        ('admin', '管理员'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='用户')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='receptionist', verbose_name='角色')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='手机号')
    real_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='真实姓名')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'user_profile'
        verbose_name = '用户角色'
        verbose_name_plural = '用户角色管理'

    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}'


class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('single', '单人间'),
        ('double', '双人间'),
        ('suite', '套房'),
        ('deluxe', '豪华套房'),
    ]

    STATUS_CHOICES = [
        ('available', '空闲'),
        ('occupied', '已入住'),
        ('reserved', '已预订'),
        ('maintenance', '维护中'),
    ]

    CLEAN_STATUS_CHOICES = [
        ('clean', '已清洁'),
        ('dirty', '待清洁'),
        ('cleaning', '清洁中'),
    ]

    room_number = models.CharField(max_length=10, unique=True, verbose_name='房间号')
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, verbose_name='房间类型')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格/天')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name='状态')
    clean_status = models.CharField(max_length=20, choices=CLEAN_STATUS_CHOICES, default='clean', verbose_name='清洁状态')
    floor = models.IntegerField(verbose_name='楼层')
    capacity = models.IntegerField(default=1, verbose_name='容纳人数')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    last_clean_time = models.DateTimeField(blank=True, null=True, verbose_name='最近清洁时间')
    cleaned_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='cleaned_rooms', verbose_name='清洁人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'room'
        verbose_name = '客房'
        verbose_name_plural = '客房管理'

    def __str__(self):
        return f'{self.room_number} - {self.get_room_type_display()}'


class Guest(models.Model):
    GENDER_CHOICES = [
        ('male', '男'),
        ('female', '女'),
    ]

    name = models.CharField(max_length=50, verbose_name='姓名')
    id_card = models.CharField(max_length=18, unique=True, verbose_name='身份证号')
    phone = models.CharField(max_length=20, verbose_name='手机号')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='性别')
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name='地址')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='登记时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'guest'
        verbose_name = '客人'
        verbose_name_plural = '客人管理'

    def __str__(self):
        return self.name


def generate_order_number():
    date_part = datetime.now().strftime('%Y%m%d')
    while True:
        random_part = ''.join(random.choices(string.digits, k=6))
        order_number = f'HT{date_part}{random_part}'
        if not Order.objects.filter(order_number=order_number).exists():
            return order_number


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', '待入住'),
        ('checked_in', '已入住'),
        ('checked_out', '已退房'),
        ('cancelled', '已取消'),
    ]

    order_number = models.CharField(max_length=20, unique=True, default=generate_order_number, verbose_name='订单号')
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='orders', verbose_name='客人')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='orders', verbose_name='房间')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='订单状态')
    check_in_date = models.DateField(verbose_name='入住日期')
    check_out_date = models.DateField(verbose_name='退房日期')
    actual_check_in = models.DateTimeField(blank=True, null=True, verbose_name='实际入住时间')
    actual_check_out = models.DateTimeField(blank=True, null=True, verbose_name='实际退房时间')
    days = models.IntegerField(verbose_name='入住天数')
    actual_days = models.IntegerField(default=0, verbose_name='实际入住天数')
    daily_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='日单价')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='总金额')
    overtime_hours = models.IntegerField(default=0, verbose_name='超时小时数')
    overtime_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='超时费用')
    deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='押金')
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='退款金额')
    remark = models.TextField(blank=True, null=True, verbose_name='备注')
    checked_in_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='checked_in_orders', verbose_name='登记入住人')
    checked_out_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='checked_out_orders', verbose_name='办理退房人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'order'
        verbose_name = '订单'
        verbose_name_plural = '订单管理'
        ordering = ['-create_time']

    def __str__(self):
        return self.order_number

    def calculate_overtime_fee(self, check_out_time=None):
        if check_out_time is None:
            check_out_time = datetime.now()

        expected_check_out = datetime.combine(self.check_out_date, datetime.strptime('12:00', '%H:%M').time())

        if check_out_time > expected_check_out:
            overtime_delta = check_out_time - expected_check_out
            overtime_hours = overtime_delta.total_seconds() // 3600
            if overtime_delta.total_seconds() % 3600 > 0:
                overtime_hours += 1

            overtime_hours = int(overtime_hours)
            hourly_rate = float(self.daily_price) / 24
            overtime_fee = round(overtime_hours * hourly_rate, 2)

            actual_days = (check_out_time.date() - self.check_in_date).days
            if actual_days <= 0:
                actual_days = 1

            return {
                'overtime_hours': overtime_hours,
                'overtime_fee': overtime_fee,
                'actual_days': actual_days,
                'total_amount': self.daily_price * actual_days + overtime_fee
            }

        return {
            'overtime_hours': 0,
            'overtime_fee': 0,
            'actual_days': self.days,
            'total_amount': self.daily_price * self.days
        }

    def save(self, *args, **kwargs):
        if self.daily_price and self.days and not self.actual_check_out:
            self.total_amount = self.daily_price * self.days
        super().save(*args, **kwargs)
