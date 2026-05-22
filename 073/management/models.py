from django.db import models
from django.utils import timezone
import uuid
from datetime import datetime, date
from django.core.exceptions import ValidationError


class SubjectHourConfig(models.Model):
    id = models.BigAutoField(primary_key=True)
    subject_name = models.CharField(max_length=100, unique=True, verbose_name='培训科目名称')
    max_daily_hours = models.FloatField(default=4.0, verbose_name='单日最大学时(小时)')
    description = models.TextField(blank=True, verbose_name='说明')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'subject_hour_config'
        verbose_name = '科目学时配置'
        verbose_name_plural = '科目学时配置'
    
    def __str__(self):
        return f"{self.subject_name} (单日上限:{self.max_daily_hours}小时)"


class Student(models.Model):
    GENDER_CHOICES = [
        ('male', '男'),
        ('female', '女'),
    ]
    STATUS_CHOICES = [
        ('studying', '学习中'),
        ('completed', '已完成'),
        ('suspended', '暂停'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='姓名')
    id_card = models.CharField(max_length=18, unique=True, verbose_name='身份证号')
    phone = models.CharField(max_length=11, verbose_name='手机号')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='性别')
    age = models.IntegerField(verbose_name='年龄')
    address = models.CharField(max_length=200, blank=True, verbose_name='地址')
    license_type = models.CharField(max_length=10, verbose_name='报考车型')
    enrollment_date = models.DateField(default=timezone.now, verbose_name='报名日期')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='studying', verbose_name='状态')
    total_hours = models.FloatField(default=0, verbose_name='总学时')
    completed_hours = models.FloatField(default=0, verbose_name='已完成学时')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'student'
        verbose_name = '学员'
        verbose_name_plural = '学员'
    
    def __str__(self):
        return self.name


class Coach(models.Model):
    GENDER_CHOICES = [
        ('male', '男'),
        ('female', '女'),
    ]
    STATUS_CHOICES = [
        ('available', '可用'),
        ('busy', '忙碌'),
        ('off_duty', '休息'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='姓名')
    id_card = models.CharField(max_length=18, unique=True, verbose_name='身份证号')
    phone = models.CharField(max_length=11, verbose_name='手机号')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='性别')
    age = models.IntegerField(verbose_name='年龄')
    license_number = models.CharField(max_length=50, unique=True, verbose_name='教练证号')
    teach_type = models.CharField(max_length=50, verbose_name='教学车型')
    experience = models.IntegerField(default=0, verbose_name='教学年限')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'coach'
        verbose_name = '教练'
        verbose_name_plural = '教练'
    
    def __str__(self):
        return self.name


class Vehicle(models.Model):
    STATUS_CHOICES = [
        ('available', '可用'),
        ('in_use', '使用中'),
        ('maintenance', '维修中'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    plate_number = models.CharField(max_length=20, unique=True, verbose_name='车牌号')
    vehicle_type = models.CharField(max_length=50, verbose_name='车型')
    brand = models.CharField(max_length=50, verbose_name='品牌')
    color = models.CharField(max_length=30, verbose_name='颜色')
    purchase_date = models.DateField(verbose_name='购买日期')
    mileage = models.FloatField(default=0, verbose_name='行驶里程(公里)')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name='状态')
    current_coach = models.ForeignKey(Coach, on_delete=models.SET_NULL, null=True, blank=True, related_name='vehicles', verbose_name='当前教练')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'vehicle'
        verbose_name = '车辆'
        verbose_name_plural = '车辆'
    
    def __str__(self):
        return self.plate_number


class CoachSchedule(models.Model):
    id = models.BigAutoField(primary_key=True)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='schedules', verbose_name='教练')
    schedule_date = models.DateField(verbose_name='排班日期')
    start_time = models.TimeField(verbose_name='开始时间')
    end_time = models.TimeField(verbose_name='结束时间')
    is_booked = models.BooleanField(default=False, verbose_name='是否已预约')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'coach_schedule'
        verbose_name = '教练排班'
        verbose_name_plural = '教练排班'
        unique_together = ['coach', 'schedule_date', 'start_time', 'end_time']
    
    def __str__(self):
        return f"{self.coach.name} - {self.schedule_date}"


def generate_appointment_number():
    now = datetime.now()
    date_str = now.strftime('%Y%m%d')
    uuid_str = str(uuid.uuid4().hex)[:6].upper()
    return f"AP{date_str}{uuid_str}"


class TrainingAppointment(models.Model):
    STATUS_CHOICES = [
        ('pending', '待确认'),
        ('confirmed', '已确认'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    appointment_number = models.CharField(max_length=20, unique=True, default=generate_appointment_number, verbose_name='预约单号')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='appointments', verbose_name='学员')
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='appointments', verbose_name='教练')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='appointments', verbose_name='车辆')
    schedule = models.ForeignKey(CoachSchedule, on_delete=models.CASCADE, related_name='appointments', verbose_name='排班')
    appointment_date = models.DateField(verbose_name='预约日期')
    start_time = models.TimeField(verbose_name='开始时间')
    end_time = models.TimeField(verbose_name='结束时间')
    training_subject = models.CharField(max_length=100, verbose_name='培训科目')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    notes = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'training_appointment'
        verbose_name = '培训预约'
        verbose_name_plural = '培训预约'
    
    def __str__(self):
        return self.appointment_number
    
    def check_time_overlap(self, existing_start, existing_end, new_start, new_end):
        """检查两个时间段是否重叠"""
        return not (new_end <= existing_start or new_start >= existing_end)
    
    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError({'start_time': '开始时间必须早于结束时间'})
        
        if self.status != 'cancelled':
            coach_conflicts = TrainingAppointment.objects.filter(
                coach=self.coach,
                appointment_date=self.appointment_date,
                status__in=['pending', 'confirmed']
            ).exclude(id=self.id)
            
            for conflict in coach_conflicts:
                if self.check_time_overlap(conflict.start_time, conflict.end_time, 
                                          self.start_time, self.end_time):
                    raise ValidationError({
                        'coach': f'该教练在 {conflict.start_time}-{conflict.end_time} 时段已有预约'
                    })
            
            vehicle_conflicts = TrainingAppointment.objects.filter(
                vehicle=self.vehicle,
                appointment_date=self.appointment_date,
                status__in=['pending', 'confirmed']
            ).exclude(id=self.id)
            
            for conflict in vehicle_conflicts:
                if self.check_time_overlap(conflict.start_time, conflict.end_time,
                                          self.start_time, self.end_time):
                    raise ValidationError({
                        'vehicle': f'该车辆在 {conflict.start_time}-{conflict.end_time} 时段已有预约'
                    })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class StudentSubjectStats(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='subject_stats', verbose_name='学员')
    subject_name = models.CharField(max_length=100, verbose_name='培训科目')
    total_effective_hours = models.FloatField(default=0, verbose_name='总有效学时(小时)')
    required_hours = models.FloatField(default=0, verbose_name='要求学时(小时)')
    can_schedule_exam = models.BooleanField(default=False, verbose_name='可约考')
    exam_scheduled = models.BooleanField(default=False, verbose_name='已约考')
    exam_passed = models.BooleanField(default=False, verbose_name='已通过')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'student_subject_stats'
        verbose_name = '学员科目学时统计'
        verbose_name_plural = '学员科目学时统计'
        unique_together = ['student', 'subject_name']
    
    def __str__(self):
        return f"{self.student.name} - {self.subject_name} - {self.total_effective_hours}小时"
    
    def update_hours(self, added_hours):
        self.total_effective_hours += added_hours
        self.total_effective_hours = round(self.total_effective_hours, 2)
        if self.total_effective_hours >= self.required_hours and self.required_hours > 0:
            self.can_schedule_exam = True
        self.save()


class TrainingRecord(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='training_records', verbose_name='学员')
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='training_records', verbose_name='教练')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='training_records', verbose_name='车辆')
    appointment = models.OneToOneField(TrainingAppointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='training_record', verbose_name='预约记录')
    training_date = models.DateField(default=timezone.now, verbose_name='培训日期')
    clock_in_time = models.DateTimeField(null=True, blank=True, verbose_name='打卡开始时间')
    clock_out_time = models.DateTimeField(null=True, blank=True, verbose_name='打卡结束时间')
    training_hours = models.FloatField(default=0, verbose_name='实际培训学时(小时)')
    effective_hours = models.FloatField(default=0, verbose_name='有效学时(小时)')
    exceeded_hours = models.FloatField(default=0, verbose_name='超出学时(小时)')
    training_subject = models.CharField(max_length=100, verbose_name='培训科目')
    training_content = models.TextField(blank=True, verbose_name='培训内容')
    coach_evaluation = models.TextField(blank=True, verbose_name='教练评价')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'training_record'
        verbose_name = '学时打卡记录'
        verbose_name_plural = '学时打卡记录'
    
    def __str__(self):
        return f"{self.student.name} - {self.training_date}"
    
    def calculate_effective_hours(self):
        if not self.clock_in_time or not self.clock_out_time:
            return 0, 0, 0
        
        delta = self.clock_out_time - self.clock_in_time
        training_hours = round(delta.total_seconds() / 3600, 2)
        
        subject_config = SubjectHourConfig.objects.filter(
            subject_name=self.training_subject,
            is_active=True
        ).first()
        
        max_daily = subject_config.max_daily_hours if subject_config else 4.0
        
        today_records = TrainingRecord.objects.filter(
            student=self.student,
            training_subject=self.training_subject,
            training_date=self.training_date,
            clock_out_time__isnull=False
        ).exclude(id=self.id)
        
        today_effective = sum(record.effective_hours for record in today_records)
        remaining_available = max(0, max_daily - today_effective)
        
        effective = min(training_hours, remaining_available)
        exceeded = max(0, training_hours - effective)
        
        return training_hours, effective, exceeded
    
    def save(self, *args, **kwargs):
        if self.clock_in_time and self.clock_out_time:
            self.training_hours, self.effective_hours, self.exceeded_hours = self.calculate_effective_hours()
        
        is_new = self.pk is None
        old_effective_hours = 0
        
        if not is_new:
            try:
                old_record = TrainingRecord.objects.get(pk=self.pk)
                old_effective_hours = old_record.effective_hours
            except TrainingRecord.DoesNotExist:
                pass
        
        super().save(*args, **kwargs)
        
        if self.effective_hours > 0 or old_effective_hours > 0:
            stats, created = StudentSubjectStats.objects.get_or_create(
                student=self.student,
                subject_name=self.training_subject,
                defaults={'required_hours': 0}
            )
            
            if not created and old_effective_hours > 0:
                stats.total_effective_hours -= old_effective_hours
                stats.total_effective_hours = max(0, stats.total_effective_hours)
            
            if self.effective_hours > 0:
                stats.update_hours(self.effective_hours)
            else:
                if stats.total_effective_hours >= stats.required_hours and stats.required_hours > 0:
                    stats.can_schedule_exam = True
                else:
                    stats.can_schedule_exam = False
                stats.save()


class FeeSettlement(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('unpaid', '未支付'),
        ('partial', '部分支付'),
        ('paid', '已支付'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('cash', '现金'),
        ('wechat', '微信'),
        ('alipay', '支付宝'),
        ('bank', '银行转账'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fee_settlements', verbose_name='学员')
    settlement_number = models.CharField(max_length=50, unique=True, verbose_name='结算单号')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总金额')
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='已支付金额')
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='剩余金额')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid', verbose_name='支付状态')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, verbose_name='支付方式')
    payment_date = models.DateField(null=True, blank=True, verbose_name='支付日期')
    fee_details = models.TextField(verbose_name='费用明细')
    remarks = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'fee_settlement'
        verbose_name = '培训费用结算'
        verbose_name_plural = '培训费用结算'
    
    def __str__(self):
        return self.settlement_number
    
    def save(self, *args, **kwargs):
        self.remaining_amount = self.total_amount - self.paid_amount
        if self.remaining_amount <= 0:
            self.payment_status = 'paid'
        elif self.paid_amount > 0:
            self.payment_status = 'partial'
        else:
            self.payment_status = 'unpaid'
        super().save(*args, **kwargs)
