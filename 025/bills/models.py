from django.db import models
from owners.models import House, Owner


class FeeStandard(models.Model):
    name = models.CharField(max_length=100, verbose_name='费用名称')
    fee_type = models.CharField(max_length=20, choices=[
        ('property', '物业费'),
        ('water', '水费'),
        ('electricity', '电费'),
        ('other', '其他费用')
    ], verbose_name='费用类型')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    unit = models.CharField(max_length=20, verbose_name='单位', default='元/㎡')
    description = models.TextField(blank=True, null=True, verbose_name='说明')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '收费标准'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Bill(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, verbose_name='所属房屋')
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name='所属业主')
    bill_type = models.CharField(max_length=20, choices=[
        ('property', '物业费'),
        ('water', '水费'),
        ('electricity', '电费'),
        ('other', '其他费用')
    ], verbose_name='账单类型')
    title = models.CharField(max_length=200, verbose_name='账单标题')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='金额')
    billing_month = models.CharField(max_length=7, verbose_name='账单月份', help_text='格式：YYYY-MM')
    start_date = models.DateField(verbose_name='计费开始日期')
    end_date = models.DateField(verbose_name='计费结束日期')
    usage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='用量(吨/度)')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    status = models.CharField(max_length=20, choices=[
        ('unpaid', '未缴费'),
        ('paid', '已缴费'),
        ('overdue', '已逾期')
    ], default='unpaid', verbose_name='状态')
    due_date = models.DateField(verbose_name='缴费截止日期')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '账单'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return f'{self.title} - {self.amount}元'


class MeterReading(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, verbose_name='所属房屋')
    reading_type = models.CharField(max_length=20, choices=[
        ('water', '水表'),
        ('electricity', '电表')
    ], verbose_name='抄表类型')
    current_reading = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='当前读数')
    previous_reading = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='上次读数')
    usage = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='用量')
    reading_date = models.DateField(verbose_name='抄表日期')
    billing_month = models.CharField(max_length=7, verbose_name='账单月份')
    operator = models.CharField(max_length=50, verbose_name='抄表人')
    remarks = models.TextField(blank=True, null=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '抄表记录'
        verbose_name_plural = verbose_name
        ordering = ['-reading_date']

    def __str__(self):
        return f'{self.get_reading_type_display()} - {self.house}'
