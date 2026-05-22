from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
from datetime import timedelta


class VenueType(models.Model):
    SPORT_TYPE_CHOICES = [
        ('badminton', '羽毛球'),
        ('basketball', '篮球'),
        ('table_tennis', '乒乓球'),
        ('tennis', '网球'),
        ('swimming', '游泳'),
        ('fitness', '健身'),
        ('yoga', '瑜伽'),
        ('other', '其他'),
    ]

    name = models.CharField(max_length=50, verbose_name='场地类型')
    sport_type = models.CharField(max_length=20, choices=SPORT_TYPE_CHOICES, default='other', verbose_name='运动类型')
    description = models.TextField(blank=True, verbose_name='描述')

    class Meta:
        verbose_name = '场地类型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Venue(models.Model):
    STATUS_CHOICES = [
        ('available', '可用'),
        ('maintenance', '维护中'),
        ('closed', '关闭'),
    ]

    SIZE_CHOICES = [
        ('small', '小型'),
        ('medium', '中型'),
        ('large', '大型'),
        ('extra_large', '超大型'),
    ]

    name = models.CharField(max_length=100, verbose_name='场地名称')
    venue_type = models.ForeignKey(VenueType, on_delete=models.CASCADE, verbose_name='场地类型')
    code = models.CharField(max_length=20, unique=True, verbose_name='场地编号')
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, default='medium', verbose_name='场地大小')
    capacity = models.IntegerField(default=1, verbose_name='容纳人数')
    area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='场地面积(㎡)')
    max_booking_hours_per_day = models.DecimalField(max_digits=4, decimal_places=1, default=4, verbose_name='单日最长预约时长(小时)')
    min_billing_minutes = models.IntegerField(default=30, verbose_name='最小计费时长(分钟)')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name='状态')
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='每小时价格')
    qr_code = models.TextField(blank=True, verbose_name='场地二维码')
    description = models.TextField(blank=True, verbose_name='描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '场地'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.name} ({self.code})'

    def is_available(self, start_time, end_time, exclude_booking_id=None):
        queryset = Booking.objects.filter(
            venue=self,
            status__in=['pending', 'in_use'],
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        if exclude_booking_id:
            queryset = queryset.exclude(id=exclude_booking_id)
        return not queryset.exists()

    def check_time_overlap(self, start_time, end_time, exclude_booking_id=None):
        overlapping_bookings = Booking.objects.filter(
            venue=self,
            status__in=['pending', 'in_use'],
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        if exclude_booking_id:
            overlapping_bookings = overlapping_bookings.exclude(id=exclude_booking_id)

        overlapping_slots = []
        for booking in overlapping_bookings:
            overlapping_slots.append({
                'booking_no': booking.booking_no,
                'start_time': booking.start_time,
                'end_time': booking.end_time,
                'contact_name': booking.contact_name
            })
        return overlapping_slots

    def get_available_slots(self, date):
        pass


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', '待使用'),
        ('in_use', '使用中'),
        ('timeout', '已超时'),
        ('completed', '已完结'),
        ('cancelled', '已取消'),
    ]

    VERIFICATION_STATUS_CHOICES = [
        ('unverified', '未核验'),
        ('verified', '已核验'),
        ('failed', '核验失败'),
    ]

    BOOKING_TYPE_CHOICES = [
        ('individual', '个人预约'),
        ('group', '团体预约'),
    ]

    booking_no = models.CharField(max_length=32, unique=True, verbose_name='预约单号')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, verbose_name='场地')
    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPE_CHOICES, default='individual', verbose_name='预约类型')
    people_count = models.IntegerField(default=1, verbose_name='预约人数')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    actual_start_time = models.DateTimeField(null=True, blank=True, verbose_name='实际入场时间')
    actual_end_time = models.DateTimeField(null=True, blank=True, verbose_name='实际离场时间')
    actual_duration_minutes = models.IntegerField(null=True, blank=True, verbose_name='实际使用时长(分钟)')
    billing_duration_minutes = models.IntegerField(null=True, blank=True, verbose_name='计费时长(分钟)')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='总金额')
    contact_name = models.CharField(max_length=50, verbose_name='联系人')
    contact_phone = models.CharField(max_length=20, verbose_name='联系电话')
    id_card = models.CharField(max_length=18, blank=True, verbose_name='身份证号')
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS_CHOICES, default='unverified', verbose_name='核验状态')
    verification_time = models.DateTimeField(null=True, blank=True, verbose_name='核验时间')
    check_in_method = models.CharField(max_length=50, blank=True, verbose_name='入场方式')
    check_out_method = models.CharField(max_length=50, blank=True, verbose_name='离场方式')
    remarks = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '预约订单'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.booking_no

    def save(self, *args, **kwargs):
        if not self.booking_no:
            self.booking_no = self.generate_booking_no()
        super().save(*args, **kwargs)

    def generate_booking_no(self):
        date_str = timezone.now().strftime('%Y%m%d')
        uuid_str = str(uuid.uuid4()).replace('-', '')[:8].upper()
        return f'BK{date_str}{uuid_str}'

    def get_duration_hours(self):
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            return round(duration.total_seconds() / 3600, 2)
        return 0

    def get_actual_duration_minutes(self):
        if self.actual_start_time and self.actual_end_time:
            duration = self.actual_end_time - self.actual_start_time
            return int(duration.total_seconds() / 60)
        return 0

    def get_billing_duration_minutes(self):
        actual_minutes = self.get_actual_duration_minutes()
        min_billing = self.venue.min_billing_minutes
        return max(actual_minutes, min_billing)

    def calculate_amount(self):
        if self.actual_start_time and self.actual_end_time:
            billing_minutes = self.get_billing_duration_minutes()
            billing_hours = billing_minutes / 60
            return round(float(self.venue.price_per_hour) * billing_hours, 2)
        elif self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            hours = duration.total_seconds() / 3600
            min_hours = self.venue.min_billing_minutes / 60
            return round(float(self.venue.price_per_hour) * max(hours, min_hours), 2)
        return 0

    def check_timeout(self):
        if self.status == 'pending' and timezone.now() > self.end_time:
            self.status = 'timeout'
            self.total_amount = self.calculate_amount()
            self.save()
        return self.status

    def check_in(self, method='scan'):
        if self.status == 'pending':
            self.actual_start_time = timezone.now()
            self.status = 'in_use'
            self.check_in_method = method
            self.save()
            return True, f'入场成功，入场时间：{self.actual_start_time.strftime("%Y-%m-%d %H:%M:%S")}'
        return False, f'入场失败，当前状态：{self.get_status_display()}'

    def check_out(self, method='scan'):
        if self.status == 'in_use':
            self.actual_end_time = timezone.now()
            self.actual_duration_minutes = self.get_actual_duration_minutes()
            self.billing_duration_minutes = self.get_billing_duration_minutes()
            self.status = 'completed'
            self.total_amount = self.calculate_amount()
            self.check_out_method = method
            self.save()
            
            actual_hours = round(self.actual_duration_minutes / 60, 2)
            billing_hours = round(self.billing_duration_minutes / 60, 2)
            
            return True, {
                'message': '离场成功，已自动结算',
                'actual_duration_minutes': self.actual_duration_minutes,
                'actual_duration_hours': actual_hours,
                'billing_duration_minutes': self.billing_duration_minutes,
                'billing_duration_hours': billing_hours,
                'min_billing_minutes': self.venue.min_billing_minutes,
                'total_amount': float(self.total_amount),
                'used_min_billing': self.actual_duration_minutes < self.venue.min_billing_minutes
            }
        return False, f'离场失败，当前状态：{self.get_status_display()}'

    def verify_id_card(self):
        if not self.id_card:
            self.verification_status = 'failed'
            return False, '身份证号不能为空'

        if len(self.id_card) != 18:
            self.verification_status = 'failed'
            return False, '身份证号格式不正确'

        self.verification_status = 'verified'
        self.verification_time = timezone.now()
        self.save()
        return True, '核验通过'

    def check_people_capacity(self):
        if self.people_count > self.venue.capacity:
            return False, f'人数超出场地容量上限，该场地最多容纳{self.venue.capacity}人，当前预约{self.people_count}人'
        if self.people_count < 1:
            return False, '预约人数不能少于1人'
        return True, '人数符合要求'

    def get_group_discount(self):
        if self.booking_type == 'group':
            capacity_ratio = self.people_count / self.venue.capacity
            if capacity_ratio >= 0.8:
                return 0.15
            elif capacity_ratio >= 0.5:
                return 0.1
            elif capacity_ratio >= 0.3:
                return 0.05
        return 0

    @staticmethod
    def get_user_daily_booking_hours(user, date):
        start_of_day = timezone.datetime.combine(date, timezone.datetime.min.time())
        end_of_day = timezone.datetime.combine(date, timezone.datetime.max.time())

        bookings = Booking.objects.filter(
            user=user,
            start_time__gte=start_of_day,
            end_time__lte=end_of_day,
            status__in=['pending', 'in_use', 'completed']
        )

        total_hours = 0
        for booking in bookings:
            duration = booking.end_time - booking.start_time
            total_hours += duration.total_seconds() / 3600

        return round(total_hours, 2)

    def check_max_booking_hours(self):
        date = self.start_time.date()
        current_hours = self.get_user_daily_booking_hours(self.user, date)
        new_hours = self.get_duration_hours()

        existing_booking = Booking.objects.filter(id=self.id).first()
        if existing_booking:
            current_hours -= existing_booking.get_duration_hours()

        total_hours = current_hours + new_hours
        max_hours = float(self.venue.max_booking_hours_per_day)

        if total_hours > max_hours:
            return False, f'单日预约时长已达上限，当前已预约{current_hours}小时，本场次{new_hours}小时，最大允许{max_hours}小时'
        return True, '预约时长符合要求'


class TimeSlot(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, verbose_name='场地')
    date = models.DateField(verbose_name='日期')
    start_time = models.TimeField(verbose_name='开始时间')
    end_time = models.TimeField(verbose_name='结束时间')
    is_available = models.BooleanField(default=True, verbose_name='是否可用')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')

    class Meta:
        verbose_name = '时段'
        verbose_name_plural = verbose_name
        unique_together = ['venue', 'date', 'start_time', 'end_time']

    def __str__(self):
        return f'{self.venue.name} {self.date} {self.start_time}-{self.end_time}'


class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('refunded', '已退款'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('wechat', '微信支付'),
        ('alipay', '支付宝'),
        ('cash', '现金'),
        ('card', '银行卡'),
    ]

    payment_no = models.CharField(max_length=32, unique=True, verbose_name='支付单号')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, verbose_name='预约订单')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='支付金额')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending', verbose_name='支付状态')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name='支付方式')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')
    transaction_id = models.CharField(max_length=100, blank=True, verbose_name='交易流水号')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '支付记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.payment_no

    def save(self, *args, **kwargs):
        if not self.payment_no:
            self.payment_no = self.generate_payment_no()
        super().save(*args, **kwargs)

    def generate_payment_no(self):
        date_str = timezone.now().strftime('%Y%m%d')
        uuid_str = str(uuid.uuid4()).replace('-', '')[:8].upper()
        return f'PY{date_str}{uuid_str}'
