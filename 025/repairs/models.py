from django.db import models
from django.contrib.auth.models import User
from owners.models import Owner, House


class RepairWorker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='关联用户')
    name = models.CharField(max_length=50, verbose_name='姓名')
    phone = models.CharField(max_length=20, verbose_name='联系电话')
    skill = models.CharField(max_length=100, verbose_name='技能专长')
    status = models.CharField(max_length=20, choices=[
        ('available', '空闲'),
        ('busy', '忙碌'),
        ('offline', '离线')
    ], default='available', verbose_name='状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '维修人员'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Repair(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name='报修业主')
    house = models.ForeignKey(House, on_delete=models.CASCADE, verbose_name='报修房屋')
    repair_type = models.CharField(max_length=50, verbose_name='报修类型', choices=[
        ('water', '水电维修'),
        ('structure', '房屋结构'),
        ('equipment', '公共设备'),
        ('other', '其他维修')
    ])
    title = models.CharField(max_length=200, verbose_name='报修标题')
    description = models.TextField(verbose_name='问题描述')
    contact_person = models.CharField(max_length=50, verbose_name='联系人')
    contact_phone = models.CharField(max_length=20, verbose_name='联系电话')
    appointment_time = models.DateTimeField(null=True, blank=True, verbose_name='预约时间')
    images = models.TextField(blank=True, null=True, verbose_name='报修图片')
    status = models.CharField(max_length=20, choices=[
        ('pending', '待接单'),
        ('assigned', '已派单'),
        ('processing', '维修中'),
        ('completed', '已完成'),
        ('cancelled', '已取消')
    ], default='pending', verbose_name='状态')
    worker = models.ForeignKey(RepairWorker, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='维修人员')
    assign_time = models.DateTimeField(null=True, blank=True, verbose_name='派单时间')
    complete_time = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    repair_content = models.TextField(blank=True, null=True, verbose_name='维修内容')
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='维修费用')
    rating = models.IntegerField(null=True, blank=True, verbose_name='评分')
    feedback = models.TextField(blank=True, null=True, verbose_name='评价反馈')
    is_archived = models.BooleanField(default=False, verbose_name='是否已归档')
    archived_time = models.DateTimeField(null=True, blank=True, verbose_name='归档时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '报修工单'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return self.title


class RepairLog(models.Model):
    repair = models.ForeignKey(Repair, on_delete=models.CASCADE, verbose_name='关联工单')
    action = models.CharField(max_length=50, verbose_name='操作类型')
    description = models.TextField(verbose_name='操作描述')
    operator = models.CharField(max_length=50, verbose_name='操作人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')

    class Meta:
        verbose_name = '工单日志'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return f'{self.repair.title} - {self.action}'
