from django.db import models
from django.contrib.auth.models import User


class Building(models.Model):
    name = models.CharField(max_length=100, verbose_name='楼栋名称')
    address = models.CharField(max_length=200, verbose_name='地址')
    total_floors = models.IntegerField(verbose_name='总楼层数')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '楼栋'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class House(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name='所属楼栋')
    room_number = models.CharField(max_length=20, verbose_name='房间号')
    floor = models.IntegerField(verbose_name='楼层')
    area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='面积(㎡)')
    house_type = models.CharField(max_length=50, verbose_name='房屋类型', default='住宅')
    status = models.CharField(max_length=20, choices=[
        ('empty', '空置'),
        ('owned', '已入住'),
        ('rented', '已出租')
    ], default='empty', verbose_name='状态')

    class Meta:
        verbose_name = '房屋'
        verbose_name_plural = verbose_name
        unique_together = ('building', 'room_number')

    def __str__(self):
        return f'{self.building.name} {self.room_number}'


class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='关联用户')
    name = models.CharField(max_length=50, verbose_name='姓名')
    phone = models.CharField(max_length=20, verbose_name='联系电话')
    id_card = models.CharField(max_length=18, verbose_name='身份证号')
    house = models.ForeignKey(House, on_delete=models.CASCADE, verbose_name='所属房屋')
    move_in_date = models.DateField(null=True, blank=True, verbose_name='入住日期')
    status = models.CharField(max_length=20, choices=[
        ('normal', '正常'),
        ('moved_out', '已迁出')
    ], default='normal', verbose_name='状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '业主'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
