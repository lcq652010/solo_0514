from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('前台', '前台'),
        ('教练', '教练'),
        ('管理员', '管理员'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='关联用户')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='前台', verbose_name='角色')
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号')
    coach = models.OneToOneField('Coach', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='关联教练')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户配置'
        verbose_name_plural = '用户配置'

    def __str__(self):
        return f'{self.user.username} - {self.role}'


class TrainingHours(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='training_hours', verbose_name='学员')
    coach = models.ForeignKey('Coach', on_delete=models.CASCADE, verbose_name='教练')
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE, verbose_name='车辆')
    subject = models.CharField(max_length=50, verbose_name='培训科目')
    date = models.DateField(default=timezone.now, verbose_name='培训日期')
    start_time = models.TimeField(verbose_name='开始时间')
    end_time = models.TimeField(verbose_name='结束时间')
    duration = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='课时时长(小时)')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '课时记录'
        verbose_name_plural = '课时记录'
        ordering = ['-date', '-start_time']

    def __str__(self):
        return f'{self.student.name} - {self.subject} - {self.duration}小时'


class TrainingArchive(models.Model):
    STATUS_CHOICES = [
        ('进行中', '进行中'),
        ('已完成', '已完成'),
        ('已归档', '已归档'),
    ]

    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='training_archives', verbose_name='学员')
    subject = models.CharField(max_length=50, verbose_name='科目')
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='总课时')
    completed_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='已完成课时')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='进行中', verbose_name='状态')
    start_date = models.DateField(auto_now_add=True, verbose_name='开始日期')
    complete_date = models.DateField(null=True, blank=True, verbose_name='完成日期')
    archive_date = models.DateField(null=True, blank=True, verbose_name='归档日期')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '培训档案'
        verbose_name_plural = '培训档案'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.student.name} - {self.subject} - {self.status}'


class Student(models.Model):
    GENDER_CHOICES = [
        ('男', '男'),
        ('女', '女'),
    ]
    LICENSE_TYPE_CHOICES = [
        ('C1', 'C1手动挡'),
        ('C2', 'C2自动挡'),
        ('B1', 'B1中型客车'),
        ('B2', 'B2大型货车'),
        ('A1', 'A1大型客车'),
        ('A2', 'A2牵引车'),
    ]
    STATUS_CHOICES = [
        ('报名中', '报名中'),
        ('学习中', '学习中'),
        ('已毕业', '已毕业'),
        ('已退学', '已退学'),
    ]

    student_id = models.CharField(max_length=20, unique=True, verbose_name='学员学号')
    name = models.CharField(max_length=50, verbose_name='姓名')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='性别')
    id_card = models.CharField(max_length=18, unique=True, verbose_name='身份证号')
    phone = models.CharField(max_length=11, verbose_name='手机号')
    email = models.EmailField(null=True, blank=True, verbose_name='邮箱')
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name='住址')
    license_type = models.CharField(max_length=10, choices=LICENSE_TYPE_CHOICES, verbose_name='报考车型')
    enrollment_date = models.DateField(default=timezone.now, verbose_name='报名日期')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='报名中', verbose_name='学员状态')
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True, verbose_name='照片')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '学员'
        verbose_name_plural = '学员'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.student_id} - {self.name}'

    def save(self, *args, **kwargs):
        if not self.student_id:
            today = datetime.date.today()
            prefix = today.strftime('%Y%m%d')
            last_student = Student.objects.filter(student_id__startswith=prefix).order_by('-student_id').first()
            if last_student:
                last_num = int(last_student.student_id[-4:])
                new_num = last_num + 1
            else:
                new_num = 1
            self.student_id = f'{prefix}{new_num:04d}'
        super().save(*args, **kwargs)


class Coach(models.Model):
    GENDER_CHOICES = [
        ('男', '男'),
        ('女', '女'),
    ]
    STATUS_CHOICES = [
        ('在职', '在职'),
        ('离职', '离职'),
        ('休假', '休假'),
    ]

    coach_id = models.CharField(max_length=20, unique=True, verbose_name='教练编号')
    name = models.CharField(max_length=50, verbose_name='姓名')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='性别')
    id_card = models.CharField(max_length=18, unique=True, verbose_name='身份证号')
    phone = models.CharField(max_length=11, verbose_name='手机号')
    license_number = models.CharField(max_length=50, verbose_name='教练证号')
    teach_type = models.CharField(max_length=10, verbose_name='教学车型')
    experience = models.IntegerField(default=0, verbose_name='教龄(年)')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='在职', verbose_name='状态')
    photo = models.ImageField(upload_to='coach_photos/', null=True, blank=True, verbose_name='照片')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '教练'
        verbose_name_plural = '教练'
        ordering = ['coach_id']

    def __str__(self):
        return f'{self.coach_id} - {self.name}'

    def save(self, *args, **kwargs):
        if not self.coach_id:
            today = datetime.date.today()
            prefix = 'JL' + today.strftime('%Y%m')
            last_coach = Coach.objects.filter(coach_id__startswith=prefix).order_by('-coach_id').first()
            if last_coach:
                last_num = int(last_coach.coach_id[-4:])
                new_num = last_num + 1
            else:
                new_num = 1
            self.coach_id = f'{prefix}{new_num:04d}'
        super().save(*args, **kwargs)


class Vehicle(models.Model):
    STATUS_CHOICES = [
        ('可用', '可用'),
        ('维修中', '维修中'),
        ('报废', '报废'),
    ]

    plate_number = models.CharField(max_length=20, unique=True, verbose_name='车牌号')
    vehicle_type = models.CharField(max_length=50, verbose_name='车型')
    license_type = models.CharField(max_length=10, verbose_name='准驾车型')
    brand = models.CharField(max_length=50, verbose_name='品牌')
    buy_date = models.DateField(verbose_name='购置日期')
    mileage = models.FloatField(default=0, verbose_name='里程数(公里)')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='可用', verbose_name='状态')
    coach = models.OneToOneField(Coach, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='分配教练')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '车辆'
        verbose_name_plural = '车辆'
        ordering = ['plate_number']

    def __str__(self):
        return self.plate_number


class Schedule(models.Model):
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, verbose_name='教练')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, verbose_name='车辆')
    date = models.DateField(verbose_name='排班日期')
    start_time = models.TimeField(verbose_name='开始时间')
    end_time = models.TimeField(verbose_name='结束时间')
    max_students = models.IntegerField(default=4, verbose_name='最大学员数')
    current_students = models.IntegerField(default=0, verbose_name='当前预约人数')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '教练排班'
        verbose_name_plural = '教练排班'
        ordering = ['-date', 'start_time']
        unique_together = ['coach', 'date', 'start_time', 'end_time']

    def __str__(self):
        return f'{self.coach.name} - {self.date} {self.start_time}-{self.end_time}'


class TrainingReservation(models.Model):
    STATUS_CHOICES = [
        ('待培训', '待培训'),
        ('培训中', '培训中'),
        ('已完成', '已完成'),
        ('已取消', '已取消'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='学员')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, verbose_name='排班')
    reservation_time = models.DateTimeField(auto_now_add=True, verbose_name='预约时间')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='待培训', verbose_name='预约状态')
    subject = models.CharField(max_length=20, verbose_name='培训科目')
    actual_start_time = models.DateTimeField(null=True, blank=True, verbose_name='实际开始时间')
    actual_end_time = models.DateTimeField(null=True, blank=True, verbose_name='实际结束时间')
    training_content = models.TextField(null=True, blank=True, verbose_name='培训内容')
    coach_comment = models.TextField(null=True, blank=True, verbose_name='教练点评')
    cancel_reason = models.TextField(null=True, blank=True, verbose_name='取消原因')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '练车预约'
        verbose_name_plural = '练车预约'
        ordering = ['-reservation_time']

    def __str__(self):
        return f'{self.student.name} - {self.schedule.date}'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.schedule.current_students += 1
            self.schedule.save()
        super().save(*args, **kwargs)


class ExamRegistration(models.Model):
    EXAM_TYPE_CHOICES = [
        ('科目一', '科目一'),
        ('科目二', '科目二'),
        ('科目三', '科目三'),
        ('科目四', '科目四'),
    ]
    STATUS_CHOICES = [
        ('待考试', '待考试'),
        ('已通过', '已通过'),
        ('未通过', '未通过'),
        ('已取消', '已取消'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='学员')
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES, verbose_name='考试类型')
    exam_date = models.DateField(verbose_name='考试日期')
    exam_time = models.TimeField(verbose_name='考试时间')
    exam_location = models.CharField(max_length=200, verbose_name='考试地点')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='待考试', verbose_name='考试状态')
    score = models.IntegerField(null=True, blank=True, verbose_name='考试分数')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '考试登记'
        verbose_name_plural = '考试登记'
        ordering = ['-exam_date', '-exam_time']

    def __str__(self):
        return f'{self.student.name} - {self.exam_type}'


class Payment(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('报名费', '报名费'),
        ('培训费', '培训费'),
        ('考试费', '考试费'),
        ('补考费', '补考费'),
        ('其他费用', '其他费用'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('现金', '现金'),
        ('微信', '微信'),
        ('支付宝', '支付宝'),
        ('银行卡', '银行卡'),
    ]
    STATUS_CHOICES = [
        ('待支付', '待支付'),
        ('已支付', '已支付'),
        ('已退款', '已退款'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='学员')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, verbose_name='费用类型')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='金额(元)')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name='支付方式')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='待支付', verbose_name='支付状态')
    payment_time = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')
    transaction_no = models.CharField(max_length=100, null=True, blank=True, verbose_name='交易单号')
    operator = models.CharField(max_length=50, verbose_name='经办人')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '费用缴纳'
        verbose_name_plural = '费用缴纳'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.student.name} - {self.payment_type} - {self.amount}'


class StudentArchive(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, verbose_name='学员')
    id_card_front = models.ImageField(upload_to='archive/id_card/', null=True, blank=True, verbose_name='身份证正面')
    id_card_back = models.ImageField(upload_to='archive/id_card/', null=True, blank=True, verbose_name='身份证反面')
    driver_license_application = models.ImageField(upload_to='archive/', null=True, blank=True, verbose_name='驾驶证申请表')
    physical_exam_report = models.ImageField(upload_to='archive/', null=True, blank=True, verbose_name='体检报告')
    other_materials = models.ImageField(upload_to='archive/', null=True, blank=True, verbose_name='其他材料')
    archive_no = models.CharField(max_length=50, unique=True, verbose_name='档案编号')
    archive_date = models.DateField(default=timezone.now, verbose_name='建档日期')
    is_complete = models.BooleanField(default=False, verbose_name='档案是否完整')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '学员档案'
        verbose_name_plural = '学员档案'
        ordering = ['-archive_date']

    def __str__(self):
        return f'{self.student.name} - {self.archive_no}'

    def save(self, *args, **kwargs):
        if not self.archive_no:
            today = datetime.date.today()
            prefix = 'DA' + today.strftime('%Y%m%d')
            last_archive = StudentArchive.objects.filter(archive_no__startswith=prefix).order_by('-archive_no').first()
            if last_archive:
                last_num = int(last_archive.archive_no[-4:])
                new_num = last_num + 1
            else:
                new_num = 1
            self.archive_no = f'{prefix}{new_num:04d}'
        super().save(*args, **kwargs)
