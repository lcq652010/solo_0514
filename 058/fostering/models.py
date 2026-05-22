from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import uuid
from datetime import timedelta


class Pet(models.Model):
    SPECIES_CHOICES = [
        ('dog', '狗'),
        ('cat', '猫'),
        ('other', '其他'),
    ]
    
    SIZE_CHOICES = [
        ('small', '小型'),
        ('medium', '中型'),
        ('large', '大型'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='宠物姓名')
    species = models.CharField(max_length=20, choices=SPECIES_CHOICES, verbose_name='宠物种类')
    breed = models.CharField(max_length=100, verbose_name='品种')
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, default='medium', verbose_name='体型')
    age = models.IntegerField(verbose_name='年龄')
    weight = models.FloatField(verbose_name='体重(kg)')
    owner_name = models.CharField(max_length=100, verbose_name='主人姓名')
    owner_phone = models.CharField(max_length=20, verbose_name='主人电话')
    vaccine_expiry = models.DateField(null=True, blank=True, verbose_name='疫苗有效期')
    health_status = models.TextField(blank=True, verbose_name='健康状况')
    special_requirements = models.TextField(blank=True, verbose_name='特殊要求')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '宠物'
        verbose_name_plural = '宠物'
    
    def __str__(self):
        return f'{self.name} - {self.get_species_display()}({self.get_size_display()})'
    
    def clean(self):
        if self.age < 0:
            raise ValidationError({'age': '年龄不能为负数'})
        if self.weight <= 0:
            raise ValidationError({'weight': '体重必须大于0'})
        if self.vaccine_expiry and self.vaccine_expiry < timezone.now().date():
            raise ValidationError({'vaccine_expiry': '疫苗已过期，请及时更新'})
    
    def is_vaccine_valid(self):
        if not self.vaccine_expiry:
            return False
        return self.vaccine_expiry >= timezone.now().date()
    
    def days_until_vaccine_expiry(self):
        if not self.vaccine_expiry:
            return None
        return (self.vaccine_expiry - timezone.now().date()).days


class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('standard', '标准间'),
        ('deluxe', '豪华间'),
        ('vip', 'VIP间'),
    ]
    
    STATUS_CHOICES = [
        ('available', '空闲'),
        ('occupied', '已占用'),
        ('cleaning', '清洁中'),
        ('maintenance', '维护中'),
    ]
    
    SUITABLE_SIZE_CHOICES = [
        ('small', '仅小型'),
        ('small_medium', '中小型'),
        ('all', '全体型'),
    ]
    
    room_number = models.CharField(max_length=20, unique=True, verbose_name='房间号')
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, verbose_name='房间类型')
    suitable_size = models.CharField(max_length=20, choices=SUITABLE_SIZE_CHOICES, default='all', verbose_name='适用体型')
    daily_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='日租金')
    overtime_multiplier = models.DecimalField(max_digits=3, decimal_places=1, default=1.5, verbose_name='超时费用倍率')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name='状态')
    description = models.TextField(blank=True, verbose_name='描述')
    max_pets = models.IntegerField(default=1, verbose_name='最大容纳宠物数')
    current_pets = models.IntegerField(default=0, verbose_name='当前宠物数')
    
    class Meta:
        verbose_name = '寄养房间'
        verbose_name_plural = '寄养房间'
    
    def __str__(self):
        return f'{self.room_number} - {self.get_room_type_display()}'
    
    def clean(self):
        if self.daily_price <= 0:
            raise ValidationError({'daily_price': '日租金必须大于0'})
        if self.overtime_multiplier < 1:
            raise ValidationError({'overtime_multiplier': '超时费用倍率不能小于1'})
        if self.max_pets < 1:
            raise ValidationError({'max_pets': '最大容纳宠物数至少为1'})
        if self.current_pets < 0:
            raise ValidationError({'current_pets': '当前宠物数不能为负数'})
        if self.current_pets > self.max_pets:
            raise ValidationError({'current_pets': '当前宠物数不能超过最大容纳数'})
    
    def has_capacity(self):
        return self.current_pets < self.max_pets
    
    def available_capacity(self):
        return max(0, self.max_pets - self.current_pets)
    
    def is_suitable_for_pet(self, pet):
        if self.suitable_size == 'all':
            return True
        elif self.suitable_size == 'small_medium':
            return pet.size in ['small', 'medium']
        elif self.suitable_size == 'small':
            return pet.size == 'small'
        return True
    
    def add_pet(self):
        if self.has_capacity():
            self.current_pets += 1
            if self.current_pets >= self.max_pets:
                self.status = 'occupied'
            return True
        return False
    
    def remove_pet(self):
        if self.current_pets > 0:
            self.current_pets -= 1
            if self.current_pets == 0 and self.status == 'occupied':
                self.status = 'available'
            return True
        return False
    
    @classmethod
    def find_suitable_room(cls, pet):
        suitable_rooms = cls.objects.filter(
            status='available',
            current_pets__lt=models.F('max_pets')
        )
        
        for room in suitable_rooms:
            if room.is_suitable_for_pet(pet):
                return room
        
        return None


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending_checkin', '待入住'),
        ('in_care', '照料中'),
        ('pending_pickup', '待接走'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]
    
    REMINDER_STATUS_CHOICES = [
        ('not_sent', '未发送'),
        ('sent', '已发送'),
        ('confirmed', '已确认'),
    ]
    
    order_no = models.CharField(max_length=32, unique=True, verbose_name='寄养单号')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name='宠物')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='寄养房间')
    checkin_date = models.DateTimeField(verbose_name='入住日期')
    expected_checkout_date = models.DateTimeField(verbose_name='预计离店日期')
    checkout_date = models.DateTimeField(null=True, blank=True, verbose_name='实际离店日期')
    expected_days = models.IntegerField(verbose_name='预计寄养天数')
    actual_days = models.IntegerField(null=True, blank=True, verbose_name='实际寄养天数')
    overtime_days = models.IntegerField(null=True, blank=True, verbose_name='超后天数')
    daily_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='日租金')
    overtime_multiplier = models.DecimalField(max_digits=3, decimal_places=1, default=1.5, verbose_name='超时费用倍率')
    base_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='基础费用')
    overtime_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='超时费用')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='总金额')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_checkin', verbose_name='订单状态')
    reminder_status = models.CharField(max_length=20, choices=REMINDER_STATUS_CHOICES, default='not_sent', verbose_name='提醒状态')
    reminder_sent_at = models.DateTimeField(null=True, blank=True, verbose_name='提醒发送时间')
    notes = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '寄养订单'
        verbose_name_plural = '寄养订单'
    
    def __str__(self):
        return self.order_no
    
    def clean(self):
        if self.expected_days <= 0:
            raise ValidationError({'expected_days': '预计寄养天数必须大于0'})
        if self.checkin_date and self.expected_checkout_date and self.expected_checkout_date < self.checkin_date:
            raise ValidationError({'expected_checkout_date': '预计离店日期不能早于入住日期'})
        if self.checkin_date and self.checkout_date and self.checkout_date < self.checkin_date:
            raise ValidationError({'checkout_date': '实际离店日期不能早于入住日期'})
    
    def save(self, *args, **kwargs):
        if not self.order_no:
            self.order_no = self.generate_order_no()
        if self.room and not self.daily_price:
            self.daily_price = self.room.daily_price
            self.overtime_multiplier = self.room.overtime_multiplier
        if self.room and not self.expected_checkout_date:
            self.expected_checkout_date = self.checkin_date + timedelta(days=self.expected_days)
        super().save(*args, **kwargs)
    
    def generate_order_no(self):
        date_str = timezone.now().strftime('%Y%m%d')
        uuid_str = str(uuid.uuid4())[:8].upper()
        return f'F{date_str}{uuid_str}'
    
    def calculate_total(self):
        if not self.checkout_date or not self.checkin_date:
            return None
        
        total_duration = self.checkout_date - self.checkin_date
        self.actual_days = max(1, total_duration.days)
        
        expected_end_date = self.expected_checkout_date
        if self.checkout_date > expected_end_date:
            overtime_duration = self.checkout_date - expected_end_date
            self.overtime_days = max(0, overtime_duration.days)
        else:
            self.overtime_days = 0
        
        normal_days = max(1, self.actual_days - self.overtime_days)
        self.base_amount = self.daily_price * normal_days
        
        if self.overtime_days > 0:
            overtime_price = self.daily_price * self.overtime_multiplier
            self.overtime_amount = overtime_price * self.overtime_days
        else:
            self.overtime_amount = 0
        
        self.total_amount = self.base_amount + self.overtime_amount
        return self.total_amount
    
    def get_days_until_checkout(self):
        if self.status != 'in_care':
            return None
        now = timezone.now()
        days_left = (self.expected_checkout_date - now).days
        return max(0, days_left)
    
    def is_near_checkout(self, days_threshold=3):
        days_left = self.get_days_until_checkout()
        return days_left is not None and days_left <= days_threshold
    
    @classmethod
    def get_orders_needing_reminder(cls, days_threshold=3):
        now = timezone.now()
        threshold_date = now + timedelta(days=days_threshold)
        return cls.objects.filter(
            status='in_care',
            reminder_status='not_sent',
            expected_checkout_date__lte=threshold_date
        )
    
    def mark_reminder_sent(self):
        self.reminder_status = 'sent'
        self.reminder_sent_at = timezone.now()
        self.save()
    
    def auto_assign_room(self):
        if self.room:
            return False, '已有房间，无需自动分配'
        
        suitable_room = Room.find_suitable_room(self.pet)
        if suitable_room:
            self.room = suitable_room
            self.daily_price = suitable_room.daily_price
            self.overtime_multiplier = suitable_room.overtime_multiplier
            self.save()
            return True, f'已自动分配房间: {suitable_room.room_number}'
        return False, '暂无合适的房间'
    
    def checkin(self):
        if self.status != 'pending_checkin':
            raise ValidationError('当前订单状态不允许入住')
        
        if not self.room:
            success, msg = self.auto_assign_room()
            if not success:
                raise ValidationError(msg)
        
        if not self.room.has_capacity():
            raise ValidationError('房间容量已满，无法入住')
        
        if not self.room.is_suitable_for_pet(self.pet):
            raise ValidationError(f'该房间不适合{self.pet.get_size_display()}型宠物')
        
        if not self.pet.is_vaccine_valid():
            days_remaining = self.pet.days_until_vaccine_expiry()
            if days_remaining is None:
                raise ValidationError('未设置疫苗有效期，请先完善宠物信息')
            elif days_remaining < 0:
                raise ValidationError(f'宠物疫苗已过期{abs(days_remaining)}天，请更新疫苗信息后再入住')
        
        self.status = 'in_care'
        self.room.add_pet()
        self.room.save()
        self.save()
    
    def checkout(self):
        if self.status != 'in_care':
            raise ValidationError('当前订单状态不允许离店')
        
        self.status = 'pending_pickup'
        self.checkout_date = timezone.now()
        self.calculate_total()
        
        if self.room:
            self.room.remove_pet()
            if self.room.current_pets == 0:
                self.room.status = 'cleaning'
            self.room.save()
        
        self.save()
    
    def complete(self):
        if self.status != 'pending_pickup':
            raise ValidationError('当前订单状态不允许完成')
        
        self.status = 'completed'
        self.save()
    
    def cancel(self):
        if self.status in ['in_care', 'completed']:
            raise ValidationError('当前订单状态不允许取消')
        
        if self.status == 'pending_checkin' and self.room:
            self.room = None
        
        self.status = 'cancelled'
        self.save()
    
    def get_stay_duration_days(self):
        if self.checkout_date and self.checkin_date:
            return (self.checkout_date - self.checkin_date).days
        if self.status == 'in_care':
            return (timezone.now() - self.checkin_date).days
        return None


class FeedingRecord(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='feeding_records', verbose_name='订单')
    record_date = models.DateField(default=timezone.now, verbose_name='记录日期')
    morning_feeding = models.BooleanField(default=False, verbose_name='早餐')
    morning_notes = models.TextField(blank=True, verbose_name='早餐备注')
    afternoon_feeding = models.BooleanField(default=False, verbose_name='午餐')
    afternoon_notes = models.TextField(blank=True, verbose_name='午餐备注')
    evening_feeding = models.BooleanField(default=False, verbose_name='晚餐')
    evening_notes = models.TextField(blank=True, verbose_name='晚餐备注')
    health_notes = models.TextField(blank=True, verbose_name='健康状况备注')
    created_by = models.CharField(max_length=100, verbose_name='记录人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '喂食记录'
        verbose_name_plural = '喂食记录'
        unique_together = ['order', 'record_date']
    
    def __str__(self):
        return f'{self.order.order_no} - {self.record_date}'
    
    def clean(self):
        if self.record_date > timezone.now().date():
            raise ValidationError({'record_date': '记录日期不能晚于今天'})
