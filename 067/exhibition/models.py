from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import uuid


class Exhibition(models.Model):
    name = models.CharField(max_length=200, verbose_name='展会名称')
    start_date = models.DateField(verbose_name='开始日期')
    end_date = models.DateField(verbose_name='结束日期')
    location = models.CharField(max_length=200, verbose_name='举办地点')
    description = models.TextField(blank=True, verbose_name='展会描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '展会'
        verbose_name_plural = verbose_name
        ordering = ['-start_date']

    def __str__(self):
        return self.name


class Builder(models.Model):
    SPECIALTY_CHOICES = [
        ('standard', '标准展位搭建'),
        ('premium', '豪华展位搭建'),
        ('custom', '特装展位搭建'),
        ('wood', '木结构特装'),
        ('aluminum', '铝料特装'),
        ('truss', '桁架搭建'),
    ]

    name = models.CharField(max_length=200, verbose_name='搭建商名称')
    contact_person = models.CharField(max_length=100, verbose_name='联系人')
    phone = models.CharField(max_length=50, verbose_name='联系电话')
    email = models.EmailField(verbose_name='邮箱')
    specialty = models.CharField(max_length=50, choices=SPECIALTY_CHOICES, verbose_name='擅长类别')
    company_level = models.IntegerField(default=1, verbose_name='优先级')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '搭建商'
        verbose_name_plural = verbose_name
        ordering = ['company_level', '-created_at']

    def __str__(self):
        return f'{self.name} ({self.get_specialty_display()})'


class Booth(models.Model):
    BOOTH_TYPE_CHOICES = [
        ('standard', '标准展位'),
        ('premium', '豪华展位'),
        ('corner', '转角展位'),
        ('custom', '特装展位'),
    ]

    STATUS_CHOICES = [
        ('available', '可预订'),
        ('reserved', '已预订'),
        ('paid', '已付款'),
        ('occupied', '已入驻'),
    ]

    ZONE_CHOICES = [
        ('A', 'A区'),
        ('B', 'B区'),
        ('C', 'C区'),
        ('D', 'D区'),
        ('E', 'E区'),
    ]

    exhibition = models.ForeignKey(Exhibition, on_delete=models.CASCADE, related_name='booths', verbose_name='所属展会')
    booth_number = models.CharField(max_length=50, verbose_name='展位编号')
    zone = models.CharField(max_length=10, choices=ZONE_CHOICES, default='A', verbose_name='所属区域')
    booth_type = models.CharField(max_length=20, choices=BOOTH_TYPE_CHOICES, verbose_name='展位类型')
    area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='展位面积(㎡)')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='展位价格(元)')
    location_desc = models.CharField(max_length=200, blank=True, verbose_name='位置描述')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '展位'
        verbose_name_plural = verbose_name
        unique_together = ['exhibition', 'booth_number']
        ordering = ['zone', 'booth_number']

    def __str__(self):
        return f'{self.exhibition.name} - {self.zone}区{self.booth_number}'

    def clean(self):
        if self.pk:
            existing = Booth.objects.filter(
                exhibition=self.exhibition,
                booth_number=self.booth_number
            ).exclude(pk=self.pk)
            if existing.exists():
                raise ValidationError(f'该展会下已存在展位编号 {self.booth_number}')


class Company(models.Model):
    name = models.CharField(max_length=200, verbose_name='企业名称')
    contact_person = models.CharField(max_length=100, verbose_name='联系人')
    phone = models.CharField(max_length=50, verbose_name='联系电话')
    email = models.EmailField(verbose_name='邮箱')
    address = models.CharField(max_length=300, verbose_name='企业地址')
    industry = models.CharField(max_length=100, blank=True, verbose_name='所属行业')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '企业'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.name


def generate_order_number():
    date_str = timezone.now().strftime('%Y%m%d')
    last_booking = Booking.objects.filter(created_at__date=timezone.now().date()).order_by('-id').first()
    sequence = 1
    if last_booking and last_booking.order_number:
        try:
            sequence = int(last_booking.order_number[-4:]) + 1
        except (ValueError, IndexError):
            pass
    return f'EX{date_str}{sequence:04d}'


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', '待确认'),
        ('confirmed', '已确认'),
        ('deposit_paid', '已付定金'),
        ('balance_paid', '已付尾款'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]

    order_number = models.CharField(max_length=20, default=generate_order_number, unique=True, verbose_name='订单号')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='bookings', verbose_name='企业')
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='bookings', verbose_name='展位')
    booking_date = models.DateTimeField(auto_now_add=True, verbose_name='预订日期')
    deposit_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='定金金额')
    balance_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='尾款金额')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='总金额')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    remark = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '展位预订'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.order_number

    def clean(self):
        if not self.pk:
            active_bookings = Booking.objects.filter(
                booth=self.booth,
                status__in=['pending', 'confirmed', 'deposit_paid', 'balance_paid']
            )
            if active_bookings.exists():
                raise ValidationError(f'展位 {self.booth} 已被预订，无法重复预订')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.clean()
            self.total_amount = self.booth.price
            self.deposit_amount = self.total_amount * 0.3
            self.balance_amount = self.total_amount * 0.7
        super().save(*args, **kwargs)


def assign_builder(booth_type):
    specialty_map = {
        'standard': 'standard',
        'premium': 'premium',
        'corner': 'standard',
        'custom': 'custom',
    }
    specialty = specialty_map.get(booth_type, 'standard')
    
    builder = Builder.objects.filter(
        specialty=specialty,
        is_active=True
    ).order_by('company_level', '-created_at').first()
    
    return builder


def generate_confirm_number():
    date_str = timezone.now().strftime('%Y%m%d')
    last_confirm = ConstructionConfirm.objects.filter(created_at__date=timezone.now().date()).order_by('-id').first()
    sequence = 1
    if last_confirm and last_confirm.confirm_number:
        try:
            sequence = int(last_confirm.confirm_number[-4:]) + 1
        except (ValueError, IndexError):
            pass
    return f'CQ{date_str}{sequence:04d}'


class ConstructionDemand(models.Model):
    STATUS_CHOICES = [
        ('submitted', '已提交'),
        ('reviewing', '审核中'),
        ('plan_submitted', '方案已提交'),
        ('plan_confirmed', '方案已确认'),
        ('approved', '已批准'),
        ('in_progress', '施工中'),
        ('completed', '已完成'),
        ('rejected', '已拒绝'),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='construction', verbose_name='预订订单')
    builder = models.ForeignKey(Builder, on_delete=models.SET_NULL, null=True, blank=True, related_name='constructions', verbose_name='分配搭建商')
    requirement_desc = models.TextField(verbose_name='搭建需求描述')
    design_file = models.FileField(upload_to='designs/', blank=True, null=True, verbose_name='设计文件')
    plan_file = models.FileField(upload_to='plans/', blank=True, null=True, verbose_name='搭建方案文件')
    plan_desc = models.TextField(blank=True, verbose_name='搭建方案描述')
    expected_complete_date = models.DateField(verbose_name='期望完成日期')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted', verbose_name='状态')
    review_remark = models.TextField(blank=True, verbose_name='审核意见')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='提交时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '搭建需求'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.booking.order_number} - 搭建需求'

    def save(self, *args, **kwargs):
        if not self.pk and not self.builder:
            booth_type = self.booking.booth.booth_type
            self.builder = assign_builder(booth_type)
        super().save(*args, **kwargs)


class ConstructionConfirm(models.Model):
    CONFIRM_STATUS_CHOICES = [
        ('pending', '待确认'),
        ('confirmed', '已确认'),
        ('revised', '需修改'),
    ]

    construction = models.ForeignKey(ConstructionDemand, on_delete=models.CASCADE, related_name='confirms', verbose_name='搭建需求')
    confirm_number = models.CharField(max_length=20, default=generate_confirm_number, unique=True, verbose_name='确认单编号')
    plan_version = models.CharField(max_length=50, default='V1.0', verbose_name='方案版本')
    company_remark = models.TextField(blank=True, verbose_name='企业意见')
    confirm_status = models.CharField(max_length=20, choices=CONFIRM_STATUS_CHOICES, default='pending', verbose_name='确认状态')
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name='确认时间')
    confirmed_by = models.CharField(max_length=100, blank=True, verbose_name='确认人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '搭建方案确认单'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.confirm_number} - {self.construction.booking.order_number}'


class ProgressStepTemplate(models.Model):
    STEP_TYPE_CHOICES = [
        ('standard', '标准流程'),
        ('premium', '豪华流程'),
        ('custom', '特装流程'),
    ]

    step_type = models.CharField(max_length=20, choices=STEP_TYPE_CHOICES, verbose_name='步骤类型')
    step_order = models.IntegerField(verbose_name='步骤顺序')
    step_name = models.CharField(max_length=100, verbose_name='步骤名称')
    step_desc = models.TextField(blank=True, verbose_name='步骤说明')
    progress_percent = models.IntegerField(verbose_name='完成百分比')
    is_required = models.BooleanField(default=True, verbose_name='是否必需')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '进度步骤模板'
        verbose_name_plural = verbose_name
        ordering = ['step_type', 'step_order']

    def __str__(self):
        return f'{self.get_step_type_display()} - {self.step_name}'


class ProgressStep(models.Model):
    STATUS_CHOICES = [
        ('pending', '未开始'),
        ('in_progress', '进行中'),
        ('completed', '已完成'),
        ('delayed', '已延期'),
    ]

    construction = models.ForeignKey(ConstructionDemand, on_delete=models.CASCADE, related_name='steps', verbose_name='搭建需求')
    step_name = models.CharField(max_length=100, verbose_name='步骤名称')
    step_desc = models.TextField(blank=True, verbose_name='步骤说明')
    step_order = models.IntegerField(verbose_name='步骤顺序')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    progress_percent = models.IntegerField(default=0, verbose_name='完成百分比')
    report_content = models.TextField(blank=True, verbose_name='上报内容')
    report_file = models.FileField(upload_to='progress_reports/', blank=True, null=True, verbose_name='上报附件')
    reported_at = models.DateTimeField(null=True, blank=True, verbose_name='上报时间')
    reported_by = models.CharField(max_length=100, blank=True, verbose_name='上报人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '进度步骤'
        verbose_name_plural = verbose_name
        ordering = ['step_order']

    def __str__(self):
        return f'{self.construction.booking.order_number} - {self.step_name}'


class ProgressTracker(models.Model):
    construction = models.ForeignKey(ConstructionDemand, on_delete=models.CASCADE, related_name='progresses', verbose_name='搭建需求')
    stage_name = models.CharField(max_length=100, verbose_name='阶段名称')
    description = models.TextField(verbose_name='进度描述')
    progress_percent = models.IntegerField(verbose_name='完成百分比')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '进度跟踪'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.construction.booking.order_number} - {self.stage_name}'


class Payment(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('deposit', '定金'),
        ('balance', '尾款'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('bank_transfer', '银行转账'),
        ('wechat', '微信支付'),
        ('alipay', '支付宝'),
        ('cash', '现金'),
    ]

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments', verbose_name='预订订单')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, verbose_name='付款类型')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='付款金额')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name='付款方式')
    transaction_no = models.CharField(max_length=100, blank=True, verbose_name='交易流水号')
    payment_date = models.DateTimeField(default=timezone.now, verbose_name='付款日期')
    remark = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '付款记录'
        verbose_name_plural = verbose_name
        ordering = ['-payment_date']

    def __str__(self):
        return f'{self.booking.order_number} - {self.get_payment_type_display()}'
