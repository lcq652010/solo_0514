from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
import random


class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name='部门名称')
    desc = models.TextField(blank=True, null=True, verbose_name='部门描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'department'
        verbose_name = '部门'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=100, verbose_name='职位名称')
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='基本工资')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='所属部门')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'position'
        verbose_name = '职位'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Employee(models.Model):
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女'),
    )
    STATUS_CHOICES = (
        ('active', '在职'),
        ('resigned', '离职'),
    )

    employee_id = models.CharField(max_length=20, unique=True, verbose_name='工号')
    name = models.CharField(max_length=100, verbose_name='姓名')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='性别')
    phone = models.CharField(max_length=20, verbose_name='手机号')
    email = models.EmailField(max_length=100, verbose_name='邮箱')
    id_card = models.CharField(max_length=18, verbose_name='身份证号')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name='部门')
    position = models.ForeignKey(Position, on_delete=models.PROTECT, verbose_name='职位')
    hire_date = models.DateField(verbose_name='入职日期')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='状态')
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='基本工资')
    address = models.TextField(blank=True, null=True, verbose_name='住址')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='头像')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'employee'
        verbose_name = '员工档案'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.employee_id} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.employee_id:
            self.employee_id = self.generate_employee_id()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_employee_id():
        prefix = 'EMP'
        today = datetime.now().strftime('%Y%m%d')
        while True:
            suffix = str(random.randint(1000, 9999))
            employee_id = f"{prefix}{today}{suffix}"
            if not Employee.objects.filter(employee_id=employee_id).exists():
                return employee_id


class Attendance(models.Model):
    STATUS_CHOICES = (
        ('normal', '正常'),
        ('late', '迟到'),
        ('early_leave', '早退'),
        ('absent', '旷工'),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='员工')
    date = models.DateField(verbose_name='日期')
    check_in = models.DateTimeField(blank=True, null=True, verbose_name='签到时间')
    check_out = models.DateTimeField(blank=True, null=True, verbose_name='签退时间')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='normal', verbose_name='考勤状态')
    work_hours = models.DecimalField(max_digits=4, decimal_places=2, default=0, verbose_name='工作时长')
    remark = models.TextField(blank=True, null=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'attendance'
        unique_together = ('employee', 'date')
        verbose_name = '考勤记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.employee.name} - {self.date}"

    def calculate_status(self):
        standard_start = datetime.combine(self.date, datetime.strptime('09:00', '%H:%M').time())
        standard_end = datetime.combine(self.date, datetime.strptime('18:00', '%H:%M').time())
        
        if not self.check_in and not self.check_out:
            self.status = 'absent'
            self.work_hours = 0
            return

        late_threshold = standard_start + timedelta(minutes=30)
        early_threshold = standard_end - timedelta(minutes=30)

        is_late = False
        is_early = False

        if self.check_in:
            check_in_time = self.check_in.replace(tzinfo=None)
            if check_in_time > late_threshold:
                is_late = True
            if check_in_time > standard_end:
                self.status = 'absent'
                self.work_hours = 0
                return

        if self.check_out:
            check_out_time = self.check_out.replace(tzinfo=None)
            if check_out_time < early_threshold:
                is_early = True

        if self.check_in and self.check_out:
            delta = self.check_out - self.check_in
            self.work_hours = round(delta.total_seconds() / 3600, 2)

        if is_late and is_early:
            self.status = 'absent'
        elif is_late:
            self.status = 'late'
        elif is_early:
            self.status = 'early_leave'
        else:
            self.status = 'normal'

    def save(self, *args, **kwargs):
        self.calculate_status()
        super().save(*args, **kwargs)


class Leave(models.Model):
    TYPE_CHOICES = (
        ('sick', '病假'),
        ('personal', '事假'),
        ('annual', '年假'),
        ('marriage', '婚假'),
        ('maternity', '产假'),
    )
    STATUS_CHOICES = (
        ('pending', '待审批'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
        ('cancelled', '已撤销'),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='员工')
    leave_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='请假类型')
    start_date = models.DateField(verbose_name='开始日期')
    end_date = models.DateField(verbose_name='结束日期')
    days = models.IntegerField(verbose_name='请假天数')
    reason = models.TextField(verbose_name='请假原因')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='审批状态')
    approver = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True, 
                                 related_name='approved_leaves', verbose_name='审批人')
    approval_remark = models.TextField(blank=True, null=True, verbose_name='审批备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'leave'
        verbose_name = '请假申请'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.employee.name} - {self.get_leave_type_display()}"

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            self.days = (self.end_date - self.start_date).days + 1
        super().save(*args, **kwargs)


class Overtime(models.Model):
    TYPE_CHOICES = (
        ('weekday', '工作日加班'),
        ('weekend', '周末加班'),
        ('holiday', '节假日加班'),
    )
    STATUS_CHOICES = (
        ('pending', '待审批'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
        ('cancelled', '已撤销'),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='员工')
    overtime_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='加班类型')
    date = models.DateField(verbose_name='加班日期')
    start_time = models.TimeField(verbose_name='开始时间')
    end_time = models.TimeField(verbose_name='结束时间')
    hours = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='加班时长')
    reason = models.TextField(verbose_name='加班原因')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='审批状态')
    approver = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True,
                                 related_name='approved_overtimes', verbose_name='审批人')
    approval_remark = models.TextField(blank=True, null=True, verbose_name='审批备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'overtime'
        verbose_name = '加班登记'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.employee.name} - {self.date}"

    def save(self, *args, **kwargs):
        if self.start_time and self.end_time:
            start = datetime.combine(self.date, self.start_time)
            end = datetime.combine(self.date, self.end_time)
            delta = end - start
            self.hours = round(delta.total_seconds() / 3600, 2)
        super().save(*args, **kwargs)


class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='员工')
    year = models.IntegerField(verbose_name='年份')
    month = models.IntegerField(verbose_name='月份')
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='基本工资')
    overtime_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='加班费')
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='奖金')
    deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='扣款')
    late_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='迟到扣款')
    early_leave_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='早退扣款')
    absent_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='旷工扣款')
    leave_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='请假扣款')
    work_days = models.IntegerField(default=0, verbose_name='实际出勤天数')
    late_count = models.IntegerField(default=0, verbose_name='迟到次数')
    early_leave_count = models.IntegerField(default=0, verbose_name='早退次数')
    absent_count = models.IntegerField(default=0, verbose_name='旷工天数')
    overtime_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='加班总时长')
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='实发工资')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'salary'
        unique_together = ('employee', 'year', 'month')
        verbose_name = '薪资记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.employee.name} - {self.year}年{self.month}月"

    def calculate_attendance_stats(self):
        attendances = Attendance.objects.filter(
            employee=self.employee,
            date__year=self.year,
            date__month=self.month
        )
        
        self.late_count = attendances.filter(status='late').count()
        self.early_leave_count = attendances.filter(status='early_leave').count()
        self.absent_count = attendances.filter(status='absent').count()
        normal_attendances = attendances.filter(status__in=['normal', 'late', 'early_leave'])
        self.work_days = normal_attendances.count()

    def calculate_deduction(self):
        daily_salary = self.base_salary / 21.75
        hourly_salary = daily_salary / 8
        
        if self.late_count <= 3:
            self.late_deduction = self.late_count * 30
        elif self.late_count <= 6:
            self.late_deduction = 3 * 30 + (self.late_count - 3) * 50
        else:
            self.late_deduction = 3 * 30 + 3 * 50 + (self.late_count - 6) * 100
        
        if self.early_leave_count <= 3:
            self.early_leave_deduction = self.early_leave_count * 30
        elif self.early_leave_count <= 6:
            self.early_leave_deduction = 3 * 30 + (self.early_leave_count - 3) * 50
        else:
            self.early_leave_deduction = 3 * 30 + 3 * 50 + (self.early_leave_count - 6) * 100
        
        self.absent_deduction = self.absent_count * daily_salary * 2

    def calculate_leave_deduction(self):
        from django.db.models import Q
        
        start_date = f"{self.year}-{self.month:02d}-01"
        if self.month == 12:
            end_date = f"{self.year + 1}-01-01"
        else:
            end_date = f"{self.year}-{self.month + 1:02d}-01"
        
        leaves = Leave.objects.filter(
            employee=self.employee,
            status='approved',
            start_date__lt=end_date,
            end_date__gte=start_date
        )
        
        personal_leave_days = 0
        sick_leave_days = 0
        
        for leave in leaves:
            leave_start = max(leave.start_date, datetime.strptime(start_date, '%Y-%m-%d').date())
            leave_end = min(leave.end_date, (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=1)).date())
            days_in_month = (leave_end - leave_start).days + 1
            
            if leave.leave_type == 'personal':
                personal_leave_days += days_in_month
            elif leave.leave_type == 'sick':
                sick_leave_days += days_in_month
        
        daily_salary = self.base_salary / 21.75
        sick_deduction = max(0, sick_leave_days - 2) * daily_salary * 0.3
        personal_deduction = personal_leave_days * daily_salary
        self.leave_deduction = sick_deduction + personal_deduction

    def calculate_overtime_pay(self):
        from django.db.models import Sum
        
        overtimes = Overtime.objects.filter(
            employee=self.employee,
            status='approved',
            date__year=self.year,
            date__month=self.month
        )
        
        total_hours = overtimes.aggregate(total=Sum('hours'))['total'] or 0
        self.overtime_hours = total_hours
        
        hourly_rate = float(self.base_salary) / 21.75 / 8
        overtime_pay = 0
        
        for ot in overtimes:
            if ot.overtime_type == 'weekday':
                rate = 1.5
            elif ot.overtime_type == 'weekend':
                rate = 2
            else:
                rate = 3
            overtime_pay += float(ot.hours) * hourly_rate * rate
        
        self.overtime_pay = round(overtime_pay, 2)

    def calculate_salary(self):
        self.calculate_attendance_stats()
        self.calculate_deduction()
        self.calculate_leave_deduction()
        self.calculate_overtime_pay()
        
        self.deduction = (float(self.late_deduction) + float(self.early_leave_deduction) + 
                          float(self.absent_deduction) + float(self.leave_deduction))
        self.net_salary = (float(self.base_salary) + float(self.overtime_pay) + 
                           float(self.bonus) - float(self.deduction))

    def save(self, *args, **kwargs):
        self.calculate_salary()
        super().save(*args, **kwargs)


class Payslip(models.Model):
    salary = models.OneToOneField(Salary, on_delete=models.CASCADE, verbose_name='薪资记录')
    payslip_no = models.CharField(max_length=50, unique=True, verbose_name='工资条编号')
    issued = models.BooleanField(default=False, verbose_name='是否已发放')
    issued_at = models.DateTimeField(blank=True, null=True, verbose_name='发放时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'payslip'
        verbose_name = '工资条'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.payslip_no

    def save(self, *args, **kwargs):
        if not self.payslip_no:
            self.payslip_no = self.generate_payslip_no()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_payslip_no():
        prefix = 'PAY'
        today = datetime.now().strftime('%Y%m%d')
        while True:
            suffix = str(random.randint(1000, 9999))
            payslip_no = f"{prefix}{today}{suffix}"
            if not Payslip.objects.filter(payslip_no=payslip_no).exists():
                return payslip_no