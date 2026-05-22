from django.db import models
from django.utils import timezone
from datetime import datetime, date


class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name='部门名称')
    description = models.TextField(blank=True, verbose_name='部门描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Employee(models.Model):
    emp_id = models.CharField(max_length=20, unique=True, verbose_name='员工编号')
    name = models.CharField(max_length=50, verbose_name='姓名')
    gender = models.CharField(max_length=10, choices=[('男', '男'), ('女', '女')], verbose_name='性别')
    phone = models.CharField(max_length=20, verbose_name='手机号')
    email = models.EmailField(verbose_name='邮箱')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='所属部门')
    position = models.CharField(max_length=50, verbose_name='职位')
    hire_date = models.DateField(verbose_name='入职日期')
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='基本工资')
    is_active = models.BooleanField(default=True, verbose_name='是否在职')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '员工'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.emp_id} - {self.name}'


class AttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ('normal', '正常'),
        ('late', '迟到'),
        ('early_leave', '早退'),
        ('absent', '旷工'),
    ]
    EXCEPTION_TYPE_CHOICES = [
        ('none', '无异常'),
        ('missing_checkin', '缺签到'),
        ('missing_checkout', '缺签退'),
        ('late', '迟到'),
        ('early_leave', '早退'),
        ('absent', '旷工'),
        ('work_hours_abnormal', '工时异常'),
        ('multi_exception', '多异常'),
    ]

    attendance_no = models.CharField(max_length=30, unique=True, verbose_name='考勤编号')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='员工')
    check_in = models.DateTimeField(null=True, blank=True, verbose_name='签到时间')
    check_out = models.DateTimeField(null=True, blank=True, verbose_name='签退时间')
    attendance_date = models.DateField(verbose_name='考勤日期')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='normal', verbose_name='考勤状态')
    work_hours = models.DecimalField(max_digits=4, decimal_places=2, default=0, verbose_name='工作时长')
    late_minutes = models.IntegerField(default=0, verbose_name='迟到分钟数')
    early_leave_minutes = models.IntegerField(default=0, verbose_name='早退分钟数')
    is_exception = models.BooleanField(default=False, verbose_name='是否异常')
    exception_type = models.CharField(max_length=30, choices=EXCEPTION_TYPE_CHOICES, default='none', verbose_name='异常类型')
    exception_desc = models.TextField(blank=True, verbose_name='异常描述')
    remark = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '打卡记录'
        verbose_name_plural = verbose_name
        unique_together = ['employee', 'attendance_date']

    def __str__(self):
        return f'{self.attendance_no} - {self.employee.name}'

    def check_and_mark_exception(self):
        exceptions = []
        self.late_minutes = 0
        self.early_leave_minutes = 0

        if not self.check_in and not self.check_out:
            self.status = 'absent'
            exceptions.append('旷工')
            self.exception_type = 'absent'
        else:
            if self.check_in:
                work_start = self.check_in.replace(hour=9, minute=0, second=0)
                if self.check_in.time() > datetime.strptime('09:00', '%H:%M').time():
                    late_delta = (datetime.combine(self.attendance_date, self.check_in.time()) - 
                                  datetime.combine(self.attendance_date, 
                                                   datetime.strptime('09:00', '%H:%M').time()))
                    self.late_minutes = int(late_delta.total_seconds() // 60)
                    if self.late_minutes > 0:
                        exceptions.append(f'迟到{self.late_minutes}分钟')

            if self.check_out:
                work_end = datetime.strptime('18:00', '%H:%M').time()
                if self.check_out.time() < work_end:
                    early_delta = datetime.combine(self.attendance_date, work_end) - \
                                  datetime.combine(self.attendance_date, self.check_out.time())
                    self.early_leave_minutes = int(early_delta.total_seconds() // 60)
                    if self.early_leave_minutes > 0:
                        exceptions.append(f'早退{self.early_leave_minutes}分钟')

            if not self.check_in:
                exceptions.append('缺签到')
            if not self.check_out:
                exceptions.append('缺签退')

            if self.check_in and self.check_out:
                work_duration = (self.check_out - self.check_in).total_seconds() / 3600
                if work_duration < 4:
                    exceptions.append(f'工时异常({work_duration:.1f}小时)')

        if exceptions:
            self.is_exception = True
            self.exception_desc = '; '.join(exceptions)
            if len(exceptions) > 1:
                self.exception_type = 'multi_exception'
            elif '缺签到' in exceptions and not self.check_out:
                self.exception_type = 'missing_checkin'
            elif '缺签退' in exceptions:
                self.exception_type = 'missing_checkout'
            elif '迟到' in exceptions[0]:
                self.exception_type = 'late'
            elif '早退' in exceptions[0]:
                self.exception_type = 'early_leave'
            elif '工时异常' in exceptions[0]:
                self.exception_type = 'work_hours_abnormal'
        else:
            self.is_exception = False
            self.exception_type = 'none'
            self.exception_desc = ''

    def save(self, *args, **kwargs):
        if not self.attendance_no:
            today = date.today()
            date_str = today.strftime('%Y%m%d')
            last_record = AttendanceRecord.objects.filter(
                attendance_no__startswith=f'ATT{date_str}'
            ).order_by('-attendance_no').first()
            if last_record:
                last_num = int(last_record.attendance_no[-4:])
                new_num = last_num + 1
            else:
                new_num = 1
            self.attendance_no = f'ATT{date_str}{new_num:04d}'

        self.check_and_mark_exception()
        super().save(*args, **kwargs)


class LeaveRequest(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('annual', '年假'),
        ('sick', '病假'),
        ('personal', '事假'),
        ('marriage', '婚假'),
        ('maternity', '产假'),
        ('other', '其他'),
    ]
    STATUS_CHOICES = [
        ('pending', '待审批'),
        ('approved', '已批准'),
        ('rejected', '已拒绝'),
    ]

    leave_no = models.CharField(max_length=30, unique=True, verbose_name='请假编号')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='员工')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES, verbose_name='请假类型')
    start_date = models.DateField(verbose_name='开始日期')
    end_date = models.DateField(verbose_name='结束日期')
    start_time = models.TimeField(default='09:00:00', verbose_name='开始时间')
    end_time = models.TimeField(default='18:00:00', verbose_name='结束时间')
    days = models.DecimalField(max_digits=4, decimal_places=1, verbose_name='请假天数')
    reason = models.TextField(verbose_name='请假原因')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='审批状态')
    approver = models.CharField(max_length=50, blank=True, verbose_name='审批人')
    approve_remark = models.TextField(blank=True, verbose_name='审批备注')
    approve_time = models.DateTimeField(null=True, blank=True, verbose_name='审批时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='申请时间')

    class Meta:
        verbose_name = '请假申请'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.leave_no} - {self.employee.name}'

    def save(self, *args, **kwargs):
        if not self.leave_no:
            today = date.today()
            date_str = today.strftime('%Y%m%d')
            last_record = LeaveRequest.objects.filter(
                leave_no__startswith=f'LEA{date_str}'
            ).order_by('-leave_no').first()
            if last_record:
                last_num = int(last_record.leave_no[-4:])
                new_num = last_num + 1
            else:
                new_num = 1
            self.leave_no = f'LEA{date_str}{new_num:04d}'
        super().save(*args, **kwargs)


class Overtime(models.Model):
    OVERTIME_TYPE_CHOICES = [
        ('weekday', '工作日加班'),
        ('weekend', '周末加班'),
        ('holiday', '节假日加班'),
    ]
    STATUS_CHOICES = [
        ('pending', '待审批'),
        ('approved', '已批准'),
        ('rejected', '已拒绝'),
    ]
    DISCREPANCY_TYPE_CHOICES = [
        ('none', '无差异'),
        ('less', '打卡时长不足'),
        ('more', '打卡时长超出'),
        ('no_record', '无打卡记录'),
    ]

    overtime_no = models.CharField(max_length=30, unique=True, verbose_name='加班编号')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='员工')
    overtime_type = models.CharField(max_length=20, choices=OVERTIME_TYPE_CHOICES, verbose_name='加班类型')
    overtime_date = models.DateField(verbose_name='加班日期')
    start_time = models.TimeField(verbose_name='开始时间')
    end_time = models.TimeField(verbose_name='结束时间')
    hours = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='申报加班时长')
    actual_hours = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name='实际打卡时长')
    hours_discrepancy = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name='时长差异')
    discrepancy_type = models.CharField(max_length=20, choices=DISCREPANCY_TYPE_CHOICES, default='none', verbose_name='差异类型')
    has_discrepancy = models.BooleanField(default=False, verbose_name='是否有差异')
    reason = models.TextField(verbose_name='加班原因')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='审批状态')
    approver = models.CharField(max_length=50, blank=True, verbose_name='审批人')
    approve_remark = models.TextField(blank=True, verbose_name='审批备注')
    approve_time = models.DateTimeField(null=True, blank=True, verbose_name='审批时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='登记时间')

    class Meta:
        verbose_name = '加班登记'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.overtime_no} - {self.employee.name}'

    def calculate_actual_hours(self):
        try:
            attendance = AttendanceRecord.objects.get(
                employee=self.employee,
                attendance_date=self.overtime_date
            )
            if attendance.check_out:
                actual_start = datetime.combine(self.overtime_date, self.start_time)
                actual_end = datetime.combine(self.overtime_date, self.end_time)

                check_out_dt = attendance.check_out.replace(tzinfo=None)

                overtime_start = max(
                    datetime.combine(self.overtime_date, datetime.strptime('18:00', '%H:%M').time()),
                    actual_start
                )
                overtime_end = min(check_out_dt, actual_end)

                if overtime_end > overtime_start:
                    actual_hours = (overtime_end - overtime_start).total_seconds() / 3600
                    return round(actual_hours, 2)
            return None
        except AttendanceRecord.DoesNotExist:
            return None

    def check_hours_discrepancy(self):
        actual_hours = self.calculate_actual_hours()

        if actual_hours is None:
            self.actual_hours = None
            self.hours_discrepancy = None
            self.discrepancy_type = 'no_record'
            self.has_discrepancy = True
        else:
            self.actual_hours = actual_hours
            discrepancy = float(self.hours) - actual_hours
            self.hours_discrepancy = round(discrepancy, 2)

            if abs(discrepancy) < 0.01:
                self.discrepancy_type = 'none'
                self.has_discrepancy = False
            elif discrepancy > 0:
                self.discrepancy_type = 'less'
                self.has_discrepancy = True
            else:
                self.discrepancy_type = 'more'
                self.has_discrepancy = True

    def save(self, *args, **kwargs):
        if not self.overtime_no:
            today = date.today()
            date_str = today.strftime('%Y%m%d')
            last_record = Overtime.objects.filter(
                overtime_no__startswith=f'OVT{date_str}'
            ).order_by('-overtime_no').first()
            if last_record:
                last_num = int(last_record.overtime_no[-4:])
                new_num = last_num + 1
            else:
                new_num = 1
            self.overtime_no = f'OVT{date_str}{new_num:04d}'

        self.check_hours_discrepancy()
        super().save(*args, **kwargs)


class AttendanceStatistics(models.Model):
    statistic_no = models.CharField(max_length=30, unique=True, verbose_name='统计编号')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='员工')
    year = models.IntegerField(verbose_name='年份')
    month = models.IntegerField(verbose_name='月份')
    work_days = models.IntegerField(default=0, verbose_name='应出勤天数')
    actual_days = models.IntegerField(default=0, verbose_name='实际出勤天数')
    late_times = models.IntegerField(default=0, verbose_name='迟到次数')
    early_leave_times = models.IntegerField(default=0, verbose_name='早退次数')
    absent_days = models.IntegerField(default=0, verbose_name='旷工天数')
    leave_days = models.DecimalField(max_digits=4, decimal_places=1, default=0, verbose_name='请假天数')
    overtime_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='加班总时长')
    total_work_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='总工作时长')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '考勤统计'
        verbose_name_plural = verbose_name
        unique_together = ['employee', 'year', 'month']

    def __str__(self):
        return f'{self.statistic_no} - {self.employee.name} - {self.year}年{self.month}月'

    def save(self, *args, **kwargs):
        if not self.statistic_no:
            today = date.today()
            date_str = today.strftime('%Y%m%d')
            last_record = AttendanceStatistics.objects.filter(
                statistic_no__startswith=f'STA{date_str}'
            ).order_by('-statistic_no').first()
            if last_record:
                last_num = int(last_record.statistic_no[-4:])
                new_num = last_num + 1
            else:
                new_num = 1
            self.statistic_no = f'STA{date_str}{new_num:04d}'
        super().save(*args, **kwargs)


class SalaryCalculation(models.Model):
    salary_no = models.CharField(max_length=30, unique=True, verbose_name='薪资编号')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='员工')
    year = models.IntegerField(verbose_name='年份')
    month = models.IntegerField(verbose_name='月份')
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='基本工资')
    overtime_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='加班费')
    leave_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='请假扣款')
    late_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='迟到扣款')
    absent_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='旷工扣款')
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='奖金')
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='实发工资')
    remark = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '薪资核算'
        verbose_name_plural = verbose_name
        unique_together = ['employee', 'year', 'month']

    def __str__(self):
        return f'{self.salary_no} - {self.employee.name} - {self.year}年{self.month}月'

    def save(self, *args, **kwargs):
        if not self.salary_no:
            today = date.today()
            date_str = today.strftime('%Y%m%d')
            last_record = SalaryCalculation.objects.filter(
                salary_no__startswith=f'SAL{date_str}'
            ).order_by('-salary_no').first()
            if last_record:
                last_num = int(last_record.salary_no[-4:])
                new_num = last_num + 1
            else:
                new_num = 1
            self.salary_no = f'SAL{date_str}{new_num:04d}'
        super().save(*args, **kwargs)


class ApprovalLog(models.Model):
    ACTION_TYPE_CHOICES = [
        ('approve', '批准'),
        ('reject', '拒绝'),
        ('transfer', '转审'),
    ]
    RELATED_TYPE_CHOICES = [
        ('leave', '请假'),
        ('overtime', '加班'),
    ]

    log_no = models.CharField(max_length=30, unique=True, verbose_name='日志编号')
    related_type = models.CharField(max_length=20, choices=RELATED_TYPE_CHOICES, verbose_name='关联类型')
    related_id = models.IntegerField(verbose_name='关联ID')
    action_type = models.CharField(max_length=20, choices=ACTION_TYPE_CHOICES, verbose_name='操作类型')
    operator = models.CharField(max_length=50, verbose_name='操作人')
    remark = models.TextField(blank=True, verbose_name='审批意见')
    previous_status = models.CharField(max_length=20, blank=True, verbose_name='之前状态')
    new_status = models.CharField(max_length=20, verbose_name='新状态')
    next_approver = models.CharField(max_length=50, blank=True, verbose_name='下一审批人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')

    class Meta:
        verbose_name = '审批日志'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.log_no} - {self.get_action_type_display()}'

    def save(self, *args, **kwargs):
        if not self.log_no:
            today = date.today()
            date_str = today.strftime('%Y%m%d')
            last_record = ApprovalLog.objects.filter(
                log_no__startswith=f'APL{date_str}'
            ).order_by('-log_no').first()
            if last_record:
                last_num = int(last_record.log_no[-4:])
                new_num = last_num + 1
            else:
                new_num = 1
            self.log_no = f'APL{date_str}{new_num:04d}'
        super().save(*args, **kwargs)


class CompensatoryLeave(models.Model):
    STATUS_CHOICES = [
        ('pending', '待生效'),
        ('available', '可使用'),
        ('used', '已使用'),
        ('expired', '已过期'),
    ]

    cl_no = models.CharField(max_length=30, unique=True, verbose_name='调休编号')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='员工')
    source_overtime = models.ForeignKey(Overtime, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='来源加班记录')
    total_hours = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='总调休时长')
    used_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='已使用时长')
    remaining_hours = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='剩余时长')
    conversion_rate = models.DecimalField(max_digits=3, decimal_places=2, default=1.0, verbose_name='折算比例')
    overtime_hours = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='原始加班时长')
    valid_from = models.DateField(verbose_name='生效日期')
    valid_to = models.DateField(verbose_name='失效日期')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    remark = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '调休管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.cl_no} - {self.employee.name} - {self.remaining_hours}小时'

    def save(self, *args, **kwargs):
        if not self.cl_no:
            today = date.today()
            date_str = today.strftime('%Y%m%d')
            last_record = CompensatoryLeave.objects.filter(
                cl_no__startswith=f'CML{date_str}'
            ).order_by('-cl_no').first()
            if last_record:
                last_num = int(last_record.cl_no[-4:])
                new_num = last_num + 1
            else:
                new_num = 1
            self.cl_no = f'CML{date_str}{new_num:04d}'
        
        self.remaining_hours = float(self.total_hours) - float(self.used_hours)
        
        if float(self.remaining_hours) <= 0:
            self.status = 'used'
        elif date.today() > self.valid_to:
            self.status = 'expired'
        elif self.status == 'pending' and date.today() >= self.valid_from:
            self.status = 'available'
            
        super().save(*args, **kwargs)


class MonthlySummary(models.Model):
    SUMMARY_STATUS_CHOICES = [
        ('draft', '草稿'),
        ('confirmed', '已确认'),
        ('archived', '已归档'),
    ]

    summary_no = models.CharField(max_length=30, unique=True, verbose_name='汇总编号')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='部门')
    year = models.IntegerField(verbose_name='年份')
    month = models.IntegerField(verbose_name='月份')
    total_employees = models.IntegerField(default=0, verbose_name='员工总数')
    avg_attendance_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='平均出勤率')
    total_late_times = models.IntegerField(default=0, verbose_name='总迟到次数')
    total_early_leave_times = models.IntegerField(default=0, verbose_name='总早退次数')
    total_absent_days = models.IntegerField(default=0, verbose_name='总旷工天数')
    total_leave_days = models.DecimalField(max_digits=10, decimal_places=1, default=0, verbose_name='总请假天数')
    total_overtime_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='总加班时长')
    total_compensatory_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='总调休时长')
    exception_count = models.IntegerField(default=0, verbose_name='异常考勤人数')
    status = models.CharField(max_length=20, choices=SUMMARY_STATUS_CHOICES, default='draft', verbose_name='状态')
    confirmed_by = models.CharField(max_length=50, blank=True, verbose_name='确认人')
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name='确认时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '月度考勤汇总'
        verbose_name_plural = verbose_name
        unique_together = ['department', 'year', 'month']

    def __str__(self):
        return f'{self.summary_no} - {self.department.name} - {self.year}年{self.month}月'

    def save(self, *args, **kwargs):
        if not self.summary_no:
            today = date.today()
            date_str = today.strftime('%Y%m%d')
            last_record = MonthlySummary.objects.filter(
                summary_no__startswith=f'MNS{date_str}'
            ).order_by('-summary_no').first()
            if last_record:
                last_num = int(last_record.summary_no[-4:])
                new_num = last_num + 1
            else:
                new_num = 1
            self.summary_no = f'MNS{date_str}{new_num:04d}'
        super().save(*args, **kwargs)


class LeaveBalance(models.Model):
    lb_no = models.CharField(max_length=30, unique=True, verbose_name='余额编号')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='员工')
    year = models.IntegerField(verbose_name='年度')
    annual_leave_total = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name='年假总额')
    annual_leave_used = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name='已用年假')
    annual_leave_remaining = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name='剩余年假')
    sick_leave_total = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name='病假总额')
    sick_leave_used = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name='已用病假')
    sick_leave_remaining = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name='剩余病假')
    personal_leave_total = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name='事假总额')
    personal_leave_used = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name='已用事假')
    personal_leave_remaining = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name='剩余事假')
    compensatory_leave_total = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='调休总额')
    compensatory_leave_used = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='已用调休')
    compensatory_leave_remaining = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='剩余调休')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '假期余额'
        verbose_name_plural = verbose_name
        unique_together = ['employee', 'year']

    def __str__(self):
        return f'{self.lb_no} - {self.employee.name} - {self.year}年'

    def save(self, *args, **kwargs):
        if not self.lb_no:
            today = date.today()
            date_str = today.strftime('%Y%m%d')
            last_record = LeaveBalance.objects.filter(
                lb_no__startswith=f'LVB{date_str}'
            ).order_by('-lb_no').first()
            if last_record:
                last_num = int(last_record.lb_no[-4:])
                new_num = last_num + 1
            else:
                new_num = 1
            self.lb_no = f'LVB{date_str}{new_num:04d}'
        
        self.annual_leave_remaining = float(self.annual_leave_total) - float(self.annual_leave_used)
        self.sick_leave_remaining = float(self.sick_leave_total) - float(self.sick_leave_used)
        self.personal_leave_remaining = float(self.personal_leave_total) - float(self.personal_leave_used)
        self.compensatory_leave_remaining = float(self.compensatory_leave_total) - float(self.compensatory_leave_used)
        
        super().save(*args, **kwargs)


class ArchiveRecord(models.Model):
    ARCHIVE_TYPE_CHOICES = [
        ('attendance', '考勤记录'),
        ('leave', '请假记录'),
        ('overtime', '加班记录'),
        ('salary', '薪资记录'),
        ('summary', '月度汇总'),
    ]

    archive_no = models.CharField(max_length=30, unique=True, verbose_name='归档编号')
    archive_type = models.CharField(max_length=20, choices=ARCHIVE_TYPE_CHOICES, verbose_name='归档类型')
    year = models.IntegerField(verbose_name='年份')
    month = models.IntegerField(verbose_name='月份')
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='部门')
    file_name = models.CharField(max_length=200, verbose_name='文件名')
    file_path = models.FileField(upload_to='archives/%Y/%m/', verbose_name='文件路径')
    file_size = models.IntegerField(verbose_name='文件大小(字节)')
    record_count = models.IntegerField(default=0, verbose_name='记录数')
    archived_by = models.CharField(max_length=50, verbose_name='归档人')
    remark = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='归档时间')

    class Meta:
        verbose_name = '归档记录'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.archive_no} - {self.get_archive_type_display()} - {self.year}年{self.month}月'

    def save(self, *args, **kwargs):
        if not self.archive_no:
            today = date.today()
            date_str = today.strftime('%Y%m%d')
            last_record = ArchiveRecord.objects.filter(
                archive_no__startswith=f'ARC{date_str}'
            ).order_by('-archive_no').first()
            if last_record:
                last_num = int(last_record.archive_no[-4:])
                new_num = last_num + 1
            else:
                new_num = 1
            self.archive_no = f'ARC{date_str}{new_num:04d}'
        super().save(*args, **kwargs)
