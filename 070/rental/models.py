from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta


class Institution(models.Model):
    name = models.CharField(max_length=200, verbose_name='机构名称')
    contact_person = models.CharField(max_length=100, verbose_name='联系人')
    contact_phone = models.CharField(max_length=20, verbose_name='联系电话')
    address = models.TextField(verbose_name='地址')
    business_license = models.CharField(max_length=100, verbose_name='营业执照号')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '租赁机构'
        verbose_name_plural = '租赁机构'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Device(models.Model):
    DEVICE_STATUS_CHOICES = [
        ('available', '可租赁'),
        ('rented', '已租赁'),
        ('calibrating', '校准中'),
        ('maintenance', '维修中'),
        ('retired', '已报废'),
    ]

    DEVICE_TYPE_CHOICES = [
        ('monitor', '监护仪'),
        ('ventilator', '呼吸机'),
        ('ultrasound', '超声设备'),
        ('ecg', '心电图机'),
        ('xray', 'X光机'),
        ('other', '其他'),
    ]

    USE_DEPARTMENT_CHOICES = [
        ('emergency', '急诊科'),
        ('icu', 'ICU'),
        ('operating', '手术室'),
        ('internal', '内科'),
        ('surgical', '外科'),
        ('pediatric', '儿科'),
        ('obstetrics', '妇产科'),
        ('radiology', '放射科'),
        ('cardiology', '心内科'),
        ('neurology', '神经科'),
        ('other', '其他科室'),
    ]

    name = models.CharField(max_length=200, verbose_name='设备名称')
    device_type = models.CharField(max_length=50, choices=DEVICE_TYPE_CHOICES, verbose_name='设备类型')
    use_department = models.CharField(max_length=50, choices=USE_DEPARTMENT_CHOICES, default='other', verbose_name='使用科室')
    model = models.CharField(max_length=100, verbose_name='型号')
    serial_number = models.CharField(max_length=100, unique=True, verbose_name='序列号')
    manufacturer = models.CharField(max_length=200, verbose_name='生产厂家')
    manufacture_date = models.DateField(verbose_name='生产日期')
    purchase_date = models.DateField(verbose_name='采购日期')
    daily_rental_fee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='日租金')
    calibration_cycle_days = models.IntegerField(default=365, verbose_name='校准周期(天)')
    last_calibration_date = models.DateField(null=True, blank=True, verbose_name='上次校准日期')
    next_calibration_date = models.DateField(null=True, blank=True, verbose_name='下次校准日期')
    status = models.CharField(max_length=20, choices=DEVICE_STATUS_CHOICES, default='available', verbose_name='状态')
    description = models.TextField(blank=True, verbose_name='设备描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '医疗设备'
        verbose_name_plural = '医疗设备'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.model} ({self.serial_number})'

    def save(self, *args, **kwargs):
        if self.last_calibration_date:
            self.next_calibration_date = self.last_calibration_date + timedelta(days=self.calibration_cycle_days)
        super().save(*args, **kwargs)

    def needs_calibration(self):
        if not self.next_calibration_date:
            return True
        return timezone.now().date() >= self.next_calibration_date

    def get_calibration_days_remaining(self):
        if self.next_calibration_date:
            days_remaining = (self.next_calibration_date - timezone.now().date()).days
            return days_remaining
        return None

    def get_calibration_status(self):
        days_remaining = self.get_calibration_days_remaining()
        if days_remaining is None:
            return 'expired'
        elif days_remaining <= 0:
            return 'expired'
        elif days_remaining <= 7:
            return 'urgent'
        elif days_remaining <= 30:
            return 'warning'
        else:
            return 'normal'

    def can_be_rented(self):
        return self.status == 'available' and self.get_calibration_status() != 'expired'

    def start_rental(self):
        if self.can_be_rented():
            self.status = 'rented'
            self.save()
            return True
        return False

    def end_rental(self):
        if self.status == 'rented':
            self.status = 'available'
            self.save()
            return True
        return False

    def start_calibration(self):
        if self.status in ['available', 'maintenance']:
            self.status = 'calibrating'
            self.save()
            return True
        return False

    def complete_calibration(self, calibration_date=None):
        if self.status == 'calibrating':
            self.status = 'available'
            if calibration_date:
                self.last_calibration_date = calibration_date
            self.save()
            return True
        return False

    def start_maintenance(self):
        if self.status in ['available', 'rented']:
            self.status = 'maintenance'
            self.save()
            return True
        return False

    def complete_maintenance(self):
        if self.status == 'maintenance':
            self.status = 'available'
            self.save()
            return True
        return False

    def retire(self):
        if self.status != 'rented':
            self.status = 'retired'
            self.save()
            return True
        return False

    def get_total_rental_days(self, start_date=None, end_date=None):
        rentals = self.rental_set.filter(status__in=['active', 'returned', 'completed'])
        if start_date:
            rentals = rentals.filter(actual_start_date__gte=start_date)
        if end_date:
            rentals = rentals.filter(actual_end_date__lte=end_date)
        
        total_days = 0
        for rental in rentals:
            if rental.actual_days:
                total_days += rental.actual_days
        return total_days

    def get_utilization_rate(self, days=30):
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)
        
        total_rental_days = self.get_total_rental_days(start_date, end_date)
        effective_days = min(days, (end_date - self.purchase_date).days + 1)
        effective_days = max(effective_days, 1)
        
        utilization_rate = (total_rental_days / effective_days) * 100
        return round(utilization_rate, 2)

    def get_total_rental_revenue(self, start_date=None, end_date=None):
        rentals = self.rental_set.filter(status__in=['returned', 'completed'])
        if start_date:
            rentals = rentals.filter(actual_start_date__gte=start_date)
        if end_date:
            rentals = rentals.filter(actual_end_date__lte=end_date)
        
        total_revenue = 0
        for rental in rentals:
            if rental.actual_total:
                total_revenue += float(rental.actual_total)
        return round(total_revenue, 2)


class Rental(models.Model):
    RENTAL_STATUS_CHOICES = [
        ('pending', '待审批'),
        ('approved', '已批准'),
        ('active', '租赁中'),
        ('returned', '已归还'),
        ('completed', '已完成'),
        ('renewed', '已续租'),
        ('cancelled', '已取消'),
    ]

    rental_no = models.CharField(max_length=20, unique=True, verbose_name='租赁单号', editable=False)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, verbose_name='租赁机构')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='租赁设备')
    parent_rental = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='renewals', verbose_name='原租赁记录')
    contact_person = models.CharField(max_length=100, verbose_name='联系人')
    contact_phone = models.CharField(max_length=20, verbose_name='联系电话')
    start_date = models.DateField(verbose_name='租赁开始日期')
    end_date = models.DateField(verbose_name='租赁结束日期')
    actual_start_date = models.DateField(null=True, blank=True, verbose_name='实际开始日期')
    actual_end_date = models.DateField(null=True, blank=True, verbose_name='实际结束日期')
    estimated_days = models.IntegerField(verbose_name='预计租赁天数')
    actual_days = models.IntegerField(null=True, blank=True, verbose_name='实际租赁天数')
    daily_fee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='日租金')
    estimated_total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='预计总金额')
    actual_total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='实际总金额')
    overtime_days = models.IntegerField(default=0, verbose_name='逾期天数')
    overtime_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='逾期费用')
    status = models.CharField(max_length=20, choices=RENTAL_STATUS_CHOICES, default='pending', verbose_name='状态')
    application_notes = models.TextField(blank=True, verbose_name='申请备注')
    approval_notes = models.TextField(blank=True, verbose_name='审批备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='申请时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '租赁记录'
        verbose_name_plural = '租赁记录'
        ordering = ['-created_at']

    def __str__(self):
        return self.rental_no

    def generate_rental_no(self):
        date_str = datetime.now().strftime('%Y%m%d')
        last_rental = Rental.objects.filter(rental_no__startswith=f'RE{date_str}').order_by('-rental_no').first()
        if last_rental:
            sequence = int(last_rental.rental_no[-4:]) + 1
        else:
            sequence = 1
        return f'RE{date_str}{sequence:04d}'

    def save(self, *args, **kwargs):
        if not self.rental_no:
            self.rental_no = self.generate_rental_no()
        if self.start_date and self.end_date:
            self.estimated_days = (self.end_date - self.start_date).days + 1
            self.estimated_total = self.estimated_days * self.daily_fee
        super().save(*args, **kwargs)

    def get_rental_days_remaining(self):
        if self.status != 'active':
            return None
        today = timezone.now().date()
        if self.actual_end_date:
            end_date = self.actual_end_date
        else:
            end_date = self.end_date
        days_remaining = (end_date - today).days
        return max(0, days_remaining)

    def get_rental_countdown_status(self):
        days_remaining = self.get_rental_days_remaining()
        if days_remaining is None:
            return None
        elif days_remaining == 0:
            return 'overdue'
        elif days_remaining <= 1:
            return 'urgent'
        elif days_remaining <= 3:
            return 'warning'
        else:
            return 'normal'

    def calculate_actual_fee(self, return_date=None):
        if not self.actual_start_date:
            return None, None, None, None
        
        if return_date:
            actual_end = return_date
        else:
            actual_end = timezone.now().date()
        
        actual_days = (actual_end - self.actual_start_date).days + 1
        actual_days = max(1, actual_days)
        
        planned_end = self.end_date
        overtime_days = max(0, (actual_end - planned_end).days)
        
        overtime_fee = overtime_days * self.daily_fee * 1.5
        overtime_fee = round(overtime_fee, 2)
        
        normal_days = actual_days - overtime_days
        normal_fee = normal_days * self.daily_fee
        
        actual_total = normal_fee + overtime_fee
        
        return actual_days, overtime_days, overtime_fee, actual_total

    def approve(self, approval_notes=''):
        if self.status == 'pending':
            self.status = 'approved'
            self.approval_notes = approval_notes
            self.save()
            return True
        return False

    def start(self, actual_start_date=None):
        if self.status == 'approved' and self.device.start_rental():
            if actual_start_date:
                self.actual_start_date = actual_start_date
            else:
                self.actual_start_date = timezone.now().date()
            self.status = 'active'
            self.save()
            return True
        return False

    def renew(self, renewal_days, new_daily_fee=None):
        if self.status != 'active':
            return None, '只有租赁中的记录可以续租'
        
        today = timezone.now().date()
        new_start_date = self.end_date + timedelta(days=1)
        new_end_date = new_start_date + timedelta(days=renewal_days - 1)
        
        if new_start_date <= today:
            new_start_date = today + timedelta(days=1)
            new_end_date = new_start_date + timedelta(days=renewal_days - 1)
        
        new_rental = Rental.objects.create(
            rental_no=self.generate_rental_no(),
            institution=self.institution,
            device=self.device,
            parent_rental=self,
            contact_person=self.contact_person,
            contact_phone=self.contact_phone,
            start_date=new_start_date,
            end_date=new_end_date,
            daily_fee=new_daily_fee or self.daily_fee
        )
        
        self.status = 'renewed'
        self.save()
        
        return new_rental, '续租成功'

    def return_device(self, return_date=None, inspector=''):
        if self.status == 'active':
            if return_date:
                actual_end = return_date
            else:
                actual_end = timezone.now().date()
            
            actual_days, overtime_days, overtime_fee, actual_total = self.calculate_actual_fee(actual_end)
            
            self.actual_end_date = actual_end
            self.actual_days = actual_days
            self.overtime_days = overtime_days
            self.overtime_fee = overtime_fee
            self.actual_total = actual_total
            self.status = 'returned'
            self.device.end_rental()
            self.save()
            return True
        return False

    def complete(self):
        if self.status == 'returned':
            self.status = 'completed'
            self.save()
            return True
        return False

    def cancel(self):
        if self.status in ['pending', 'approved']:
            self.status = 'cancelled'
            self.save()
            return True
        return False


class Calibration(models.Model):
    CALIBRATION_STATUS_CHOICES = [
        ('scheduled', '已安排'),
        ('in_progress', '进行中'),
        ('completed', '已完成'),
        ('failed', '未通过'),
    ]

    device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='设备')
    calibration_date = models.DateField(verbose_name='校准日期')
    calibrator = models.CharField(max_length=100, verbose_name='校准人员')
    calibration_agency = models.CharField(max_length=200, verbose_name='校准机构')
    certificate_no = models.CharField(max_length=100, blank=True, verbose_name='校准证书号')
    status = models.CharField(max_length=20, choices=CALIBRATION_STATUS_CHOICES, default='scheduled', verbose_name='状态')
    calibration_result = models.TextField(blank=True, verbose_name='校准结果')
    next_calibration_date = models.DateField(verbose_name='下次校准日期')
    notes = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '校准记录'
        verbose_name_plural = '校准记录'
        ordering = ['-calibration_date']

    def __str__(self):
        return f'{self.device.name} - {self.calibration_date}'

    def start_calibration(self):
        if self.status == 'scheduled' and self.device.start_calibration():
            self.status = 'in_progress'
            self.save()
            return True
        return False

    def complete_calibration(self, calibration_result='', next_calibration_date=None):
        if self.status == 'in_progress':
            self.status = 'completed'
            self.calibration_result = calibration_result
            if next_calibration_date:
                self.next_calibration_date = next_calibration_date
            self.device.complete_calibration(self.calibration_date)
            self.save()
            return True
        return False

    def fail_calibration(self, calibration_result=''):
        if self.status == 'in_progress':
            self.status = 'failed'
            self.calibration_result = calibration_result
            self.device.start_maintenance()
            self.save()
            return True
        return False


class DamageRecord(models.Model):
    DAMAGE_TYPE_CHOICES = [
        ('appearance', '外观损坏'),
        ('function', '功能故障'),
        ('accessory', '配件丢失'),
        ('other', '其他'),
    ]

    DAMAGE_LEVEL_CHOICES = [
        ('minor', '轻微'),
        ('moderate', '中等'),
        ('severe', '严重'),
    ]

    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, verbose_name='租赁记录')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='设备')
    inspector = models.CharField(max_length=100, verbose_name='检查人员')
    damage_type = models.CharField(max_length=20, choices=DAMAGE_TYPE_CHOICES, verbose_name='损坏类型')
    damage_level = models.CharField(max_length=20, choices=DAMAGE_LEVEL_CHOICES, verbose_name='损坏程度')
    damage_description = models.TextField(verbose_name='损坏描述')
    estimated_repair_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='预估维修费用')
    images = models.TextField(blank=True, verbose_name='损坏图片')
    needs_maintenance = models.BooleanField(default=True, verbose_name='是否需要维修')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '损耗记录'
        verbose_name_plural = '损耗记录'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.device.name} - {self.get_damage_type_display()}'


class MaintenanceRecord(models.Model):
    MAINTENANCE_STATUS_CHOICES = [
        ('pending', '待维修'),
        ('in_progress', '维修中'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]

    MAINTENANCE_TYPE_CHOICES = [
        ('damage', '损坏维修'),
        ('preventive', '预防性维护'),
        ('calibration_failure', '校准未通过维修'),
        ('other', '其他'),
    ]

    device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='设备')
    damage_record = models.OneToOneField(DamageRecord, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='关联损耗记录')
    maintenance_type = models.CharField(max_length=20, choices=MAINTENANCE_TYPE_CHOICES, verbose_name='维修类型')
    status = models.CharField(max_length=20, choices=MAINTENANCE_STATUS_CHOICES, default='pending', verbose_name='维修状态')
    reporter = models.CharField(max_length=100, verbose_name='报修人')
    report_date = models.DateField(auto_now_add=True, verbose_name='报修日期')
    maintenance_person = models.CharField(max_length=100, blank=True, verbose_name='维修人员')
    start_date = models.DateField(null=True, blank=True, verbose_name='开始维修日期')
    complete_date = models.DateField(null=True, blank=True, verbose_name='完成维修日期')
    maintenance_content = models.TextField(verbose_name='维修内容')
    maintenance_result = models.TextField(blank=True, verbose_name='维修结果')
    parts_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='零件费用')
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='人工费用')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='总费用')
    notes = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '维修记录'
        verbose_name_plural = '维修记录'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.device.name} - {self.get_maintenance_type_display()}'

    def save(self, *args, **kwargs):
        self.total_cost = self.parts_cost + self.labor_cost
        super().save(*args, **kwargs)

    def start_maintenance(self, maintenance_person='', start_date=None):
        if self.status == 'pending':
            self.maintenance_person = maintenance_person
            if start_date:
                self.start_date = start_date
            else:
                self.start_date = timezone.now().date()
            self.status = 'in_progress'
            self.device.start_maintenance()
            self.save()
            return True
        return False

    def complete_maintenance(self, maintenance_result='', parts_cost=None, labor_cost=None, complete_date=None):
        if self.status == 'in_progress':
            self.maintenance_result = maintenance_result
            if parts_cost is not None:
                self.parts_cost = parts_cost
            if labor_cost is not None:
                self.labor_cost = labor_cost
            if complete_date:
                self.complete_date = complete_date
            else:
                self.complete_date = timezone.now().date()
            self.status = 'completed'
            self.device.complete_maintenance()
            self.save()
            return True
        return False


class ReturnAcceptance(models.Model):
    ACCEPTANCE_STATUS_CHOICES = [
        ('pending', '待验收'),
        ('passed', '验收通过'),
        ('failed', '验收未通过'),
    ]

    rental = models.OneToOneField(Rental, on_delete=models.CASCADE, verbose_name='租赁记录')
    return_date = models.DateField(verbose_name='归还日期')
    inspector = models.CharField(max_length=100, verbose_name='验收人员')
    appearance_check = models.BooleanField(default=True, verbose_name='外观检查')
    function_check = models.BooleanField(default=True, verbose_name='功能检查')
    accessory_check = models.BooleanField(default=True, verbose_name='配件检查')
    status = models.CharField(max_length=20, choices=ACCEPTANCE_STATUS_CHOICES, default='pending', verbose_name='验收状态')
    issues_found = models.TextField(blank=True, verbose_name='发现问题')
    damage_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='损坏赔偿费用')
    acceptance_notes = models.TextField(blank=True, verbose_name='验收备注')
    damage_record = models.OneToOneField(DamageRecord, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='关联损耗记录')
    maintenance_record = models.OneToOneField(MaintenanceRecord, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='关联维修记录')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '归还验收'
        verbose_name_plural = '归还验收'

    def __str__(self):
        return f'{self.rental.rental_no} - 验收'

    def create_damage_record(self, damage_type, damage_level, damage_description, estimated_repair_cost=0):
        damage_record = DamageRecord.objects.create(
            rental=self.rental,
            device=self.rental.device,
            inspector=self.inspector,
            damage_type=damage_type,
            damage_level=damage_level,
            damage_description=damage_description,
            estimated_repair_cost=estimated_repair_cost,
            needs_maintenance=True
        )
        self.damage_record = damage_record
        self.save()
        return damage_record

    def create_maintenance_record(self, maintenance_type='damage', reporter='', maintenance_content=''):
        if not self.damage_record:
            return None
        
        maintenance_record = MaintenanceRecord.objects.create(
            device=self.rental.device,
            damage_record=self.damage_record,
            maintenance_type=maintenance_type,
            reporter=reporter or self.inspector,
            maintenance_content=maintenance_content or self.damage_record.damage_description
        )
        self.maintenance_record = maintenance_record
        self.save()
        return maintenance_record


class Settlement(models.Model):
    SETTLEMENT_STATUS_CHOICES = [
        ('unbilled', '待结算'),
        ('billed', '已开单'),
        ('paid', '已付款'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('bank', '银行转账'),
        ('cash', '现金'),
        ('wechat', '微信支付'),
        ('alipay', '支付宝'),
    ]

    rental = models.OneToOneField(Rental, on_delete=models.CASCADE, verbose_name='租赁记录')
    acceptance = models.OneToOneField(ReturnAcceptance, on_delete=models.CASCADE, null=True, blank=True, verbose_name='验收记录')
    rental_days = models.IntegerField(verbose_name='租赁天数')
    rental_fee = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='租赁费用')
    overtime_days = models.IntegerField(default=0, verbose_name='逾期天数')
    overtime_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='逾期费用')
    damage_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='损坏赔偿')
    other_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='其他费用')
    other_fee_notes = models.TextField(blank=True, verbose_name='其他费用说明')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='总金额')
    status = models.CharField(max_length=20, choices=SETTLEMENT_STATUS_CHOICES, default='unbilled', verbose_name='状态')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, verbose_name='付款方式')
    payment_date = models.DateField(null=True, blank=True, verbose_name='付款日期')
    invoice_no = models.CharField(max_length=100, blank=True, verbose_name='发票号')
    notes = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '费用结算'
        verbose_name_plural = '费用结算'

    def __str__(self):
        return f'{self.rental.rental_no} - 结算'

    def save(self, *args, **kwargs):
        self.total_amount = self.rental_fee + self.overtime_fee + self.damage_fee + self.other_fee
        super().save(*args, **kwargs)
