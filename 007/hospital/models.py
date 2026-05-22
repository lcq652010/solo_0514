from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name='科室名称')
    description = models.TextField(blank=True, verbose_name='科室描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '科室'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Staff(models.Model):
    ROLE_CHOICES = [
        ('receptionist', '前台'),
        ('doctor', '医生'),
        ('admin', '管理员'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='关联用户')
    name = models.CharField(max_length=100, verbose_name='姓名')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name='角色')
    phone = models.CharField(max_length=20, blank=True, verbose_name='联系电话')
    avatar = models.ImageField(upload_to='staff/', blank=True, verbose_name='头像')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='所属科室')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '员工'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.get_role_display()}'


class Doctor(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, null=True, blank=True, verbose_name='关联员工')
    name = models.CharField(max_length=100, verbose_name='医生姓名')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='所属科室')
    title = models.CharField(max_length=50, verbose_name='职称')
    phone = models.CharField(max_length=20, blank=True, verbose_name='联系电话')
    avatar = models.ImageField(upload_to='doctors/', blank=True, verbose_name='头像')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '医生'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.title}'


class Owner(models.Model):
    name = models.CharField(max_length=100, verbose_name='主人姓名')
    phone = models.CharField(max_length=20, verbose_name='联系电话')
    id_card = models.CharField(max_length=18, blank=True, verbose_name='身份证号')
    address = models.TextField(blank=True, verbose_name='住址')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '主人信息'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Pet(models.Model):
    GENDER_CHOICES = [
        ('male', '公'),
        ('female', '母'),
        ('unknown', '未知'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='宠物名称')
    species = models.CharField(max_length=100, verbose_name='品种')
    breed = models.CharField(max_length=100, blank=True, verbose_name='种类')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='性别')
    age = models.IntegerField(verbose_name='年龄(岁)')
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='体重(kg)')
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name='主人')
    photo = models.ImageField(upload_to='pets/', blank=True, verbose_name='照片')
    description = models.TextField(blank=True, verbose_name='特征描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建档时间')

    class Meta:
        verbose_name = '宠物档案'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.species})'


class Medicine(models.Model):
    CATEGORY_CHOICES = [
        ('antibiotic', '抗生素'),
        ('anti_inflammatory', '消炎药'),
        ('vitamin', '维生素'),
        ('external', '外用药'),
        ('other', '其他'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='药品名称')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='药品分类')
    specification = models.CharField(max_length=100, verbose_name='规格')
    unit = models.CharField(max_length=20, verbose_name='单位')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    stock = models.IntegerField(default=0, verbose_name='库存数量')
    manufacturer = models.CharField(max_length=200, blank=True, verbose_name='生产厂家')
    expiry_date = models.DateField(verbose_name='有效期')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '药品'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.specification})'


class Visit(models.Model):
    STATUS_CHOICES = [
        ('pending', '待诊'),
        ('in_progress', '诊疗中'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]
    
    visit_no = models.CharField(max_length=20, unique=True, verbose_name='就诊单号')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name='就诊宠物')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='接诊医生')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='就诊科室')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='就诊状态')
    symptom = models.TextField(verbose_name='主诉症状')
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, default=20, verbose_name='挂号费')
    treatment_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='治疗费')
    appointment_time = models.DateTimeField(verbose_name='预约时间')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='挂号时间')

    class Meta:
        verbose_name = '挂号就诊'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.visit_no:
            today = timezone.now().strftime('%Y%m%d')
            count = Visit.objects.filter(visit_no__startswith=f'V{today}').count() + 1
            self.visit_no = f'V{today}{count:04d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.visit_no


class MedicalRecord(models.Model):
    visit = models.OneToOneField(Visit, on_delete=models.CASCADE, verbose_name='就诊记录')
    chief_complaint = models.TextField(verbose_name='主诉')
    physical_exam = models.TextField(verbose_name='体格检查')
    diagnosis = models.TextField(verbose_name='诊断结果')
    treatment_plan = models.TextField(verbose_name='治疗方案')
    doctor_notes = models.TextField(blank=True, verbose_name='医生备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='填写时间')

    class Meta:
        verbose_name = '病历记录'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'病历 - {self.visit.visit_no}'


class Prescription(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, verbose_name='所属病历')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, verbose_name='药品')
    quantity = models.IntegerField(verbose_name='数量')
    dosage = models.CharField(max_length=200, verbose_name='用法用量')
    usage_instructions = models.TextField(blank=True, verbose_name='使用说明')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='开方时间')

    class Meta:
        verbose_name = '处方明细'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.medicine.name} - {self.quantity}'

    @property
    def subtotal(self):
        return self.medicine.price * self.quantity


class Charge(models.Model):
    STATUS_CHOICES = [
        ('unpaid', '未支付'),
        ('paid', '已支付'),
        ('refunded', '已退款'),
    ]
    
    PAYMENT_CHOICES = [
        ('cash', '现金'),
        ('wechat', '微信'),
        ('alipay', '支付宝'),
        ('card', '银行卡'),
    ]
    
    charge_no = models.CharField(max_length=20, unique=True, verbose_name='收费单号')
    visit = models.OneToOneField(Visit, on_delete=models.CASCADE, verbose_name='就诊记录')
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='挂号费')
    medicine_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='药品费')
    treatment_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='治疗费')
    other_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='其他费用')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总金额')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unpaid', verbose_name='支付状态')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, blank=True, verbose_name='支付方式')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '收费结算'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.charge_no:
            today = timezone.now().strftime('%Y%m%d')
            count = Charge.objects.filter(charge_no__startswith=f'C{today}').count() + 1
            self.charge_no = f'C{today}{count:04d}'
        if not self.total_amount:
            self.total_amount = self.registration_fee + self.medicine_fee + self.treatment_fee + self.other_fee
        super().save(*args, **kwargs)

    def __str__(self):
        return self.charge_no


class InventoryLog(models.Model):
    OPERATION_CHOICES = [
        ('in', '入库'),
        ('out', '出库'),
        ('refund', '退库'),
        ('adjust', '调整'),
    ]

    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, verbose_name='药品')
    operation = models.CharField(max_length=20, choices=OPERATION_CHOICES, verbose_name='操作类型')
    quantity = models.IntegerField(verbose_name='数量')
    stock_before = models.IntegerField(verbose_name='操作前库存')
    stock_after = models.IntegerField(verbose_name='操作后库存')
    related_visit = models.ForeignKey(Visit, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='关联就诊')
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='操作人')
    remark = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')

    class Meta:
        verbose_name = '库存日志'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.get_operation_display()} - {self.medicine.name}'
