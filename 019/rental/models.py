import uuid
from django.db import models
from django.utils import timezone
from decimal import Decimal


class Car(models.Model):
    STATUS_CHOICES = [
        ('available', '可租用'),
        ('rented', '已出租'),
        ('maintenance', '维修中'),
    ]

    id = models.AutoField(primary_key=True)
    plate_number = models.CharField(max_length=20, unique=True, verbose_name='车牌号')
    brand = models.CharField(max_length=50, verbose_name='品牌')
    model = models.CharField(max_length=50, verbose_name='型号')
    car_type = models.CharField(max_length=50, blank=True, null=True, verbose_name='车型')
    color = models.CharField(max_length=30, verbose_name='颜色')
    seats = models.IntegerField(verbose_name='座位数')
    daily_rent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='日租金')
    overtime_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('1.5'), verbose_name='超时费率')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name='状态')
    image = models.URLField(blank=True, null=True, verbose_name='车辆图片')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'car'
        verbose_name = '车辆'
        verbose_name_plural = '车辆管理'

    def __str__(self):
        return f"{self.brand} {self.model} ({self.plate_number})"

    def update_status(self, new_status):
        if self.status != new_status:
            self.status = new_status
            self.save(update_fields=['status', 'updated_at'])
            return True
        return False


class Customer(models.Model):
    GENDER_CHOICES = [
        ('male', '男'),
        ('female', '女'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='姓名')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='性别')
    phone = models.CharField(max_length=20, unique=True, verbose_name='手机号')
    id_card = models.CharField(max_length=18, unique=True, verbose_name='身份证号')
    driver_license = models.CharField(max_length=20, unique=True, verbose_name='驾驶证号')
    address = models.TextField(blank=True, null=True, verbose_name='地址')
    email = models.EmailField(blank=True, null=True, verbose_name='邮箱')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'customer'
        verbose_name = '客户'
        verbose_name_plural = '客户管理'

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', '待取车'),
        ('picked_up', '已取车'),
        ('returned', '已还车'),
        ('cancelled', '已取消'),
    ]

    id = models.AutoField(primary_key=True)
    order_no = models.CharField(max_length=32, unique=True, editable=False, verbose_name='订单编号')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='车辆')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='客户')
    start_date = models.DateField(verbose_name='取车日期')
    end_date = models.DateField(verbose_name='还车日期')
    pickup_location = models.CharField(max_length=100, verbose_name='取车地点')
    return_location = models.CharField(max_length=100, verbose_name='还车地点')
    rental_days = models.IntegerField(verbose_name='租赁天数')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='预计总金额')
    deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='押金')
    actual_start_date = models.DateTimeField(blank=True, null=True, verbose_name='实际取车时间')
    actual_end_date = models.DateTimeField(blank=True, null=True, verbose_name='实际还车时间')
    actual_rental_days = models.IntegerField(blank=True, null=True, verbose_name='实际租赁天数')
    overtime_days = models.IntegerField(default=0, verbose_name='超时天数')
    base_rental = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name='基础租金')
    overtime_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='超时费用')
    actual_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name='实际结算金额')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='订单状态')
    remarks = models.TextField(blank=True, null=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'order'
        verbose_name = '订单'
        verbose_name_plural = '订单管理'
        ordering = ['-created_at']

    def __str__(self):
        return self.order_no

    def save(self, *args, **kwargs):
        if not self.order_no:
            self.order_no = self.generate_order_no()
        if not self.rental_days:
            self.rental_days = (self.end_date - self.start_date).days
        if not self.total_amount and hasattr(self, 'car') and self.car_id:
            self.total_amount = self.rental_days * self.car.daily_rent
        super().save(*args, **kwargs)

    def generate_order_no(self):
        date_str = timezone.now().strftime('%Y%m%d%H%M%S')
        unique_id = str(uuid.uuid4().hex)[:6].upper()
        return f"CR{date_str}{unique_id}"

    def pick_up_car(self):
        if self.status == 'pending':
            self.status = 'picked_up'
            self.actual_start_date = timezone.now()
            self.car.update_status('rented')
            self.save(update_fields=['status', 'actual_start_date', 'updated_at'])
            return True
        return False

    def return_car(self):
        if self.status == 'picked_up':
            self.status = 'returned'
            self.actual_end_date = timezone.now()
            self._calculate_rental_fee()
            self.car.update_status('available')
            self.save(update_fields=[
                'status', 'actual_end_date', 'actual_rental_days',
                'overtime_days', 'base_rental', 'overtime_fee',
                'actual_amount', 'updated_at'
            ])
            return True
        return False

    def _calculate_rental_fee(self):
        if not self.actual_start_date or not self.actual_end_date:
            return

        actual_start = self.actual_start_date.date()
        actual_end = self.actual_end_date.date()
        self.actual_rental_days = (actual_end - actual_start).days + 1

        expected_end = self.end_date

        if actual_end <= expected_end:
            self.overtime_days = 0
            self.base_rental = self.actual_rental_days * self.car.daily_rent
            self.overtime_fee = Decimal('0')
        else:
            normal_days = (expected_end - actual_start).days + 1
            self.overtime_days = (actual_end - expected_end).days

            if normal_days < 0:
                normal_days = 0

            self.base_rental = normal_days * self.car.daily_rent
            overtime_rate = self.car.overtime_rate if hasattr(self.car, 'overtime_rate') else Decimal('1.5')
            self.overtime_fee = self.overtime_days * (self.car.daily_rent * overtime_rate)

        self.actual_amount = self.base_rental + self.overtime_fee

    def cancel_order(self):
        if self.status == 'pending':
            self.status = 'cancelled'
            self.save(update_fields=['status', 'updated_at'])
            return True
        return False

    @property
    def is_overdue(self):
        if self.status == 'picked_up':
            today = timezone.now().date()
            return today > self.end_date
        return False

    @property
    def overdue_days(self):
        if self.status == 'picked_up' and self.is_overdue:
            today = timezone.now().date()
            return (today - self.end_date).days
        return 0
