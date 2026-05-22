from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('customer', '前台用户'),
        ('photographer', '摄影师'),
        ('admin', '管理员'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='关联用户')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer', verbose_name='角色')
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='联系电话')
    avatar = models.CharField(max_length=500, null=True, blank=True, verbose_name='头像URL')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'user_profile'
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class Package(models.Model):
    name = models.CharField(max_length=200, verbose_name='套餐名称')
    description = models.TextField(verbose_name='套餐描述')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    days = models.IntegerField(verbose_name='拍摄天数')
    photos_count = models.IntegerField(verbose_name='精修照片数量')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'package'
        verbose_name = '套餐'
        verbose_name_plural = '套餐'

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='关联用户')
    name = models.CharField(max_length=100, verbose_name='客户姓名')
    phone = models.CharField(max_length=20, verbose_name='联系电话')
    email = models.EmailField(null=True, blank=True, verbose_name='邮箱')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='地址')
    wechat = models.CharField(max_length=100, null=True, blank=True, verbose_name='微信号')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'customer'
        verbose_name = '客户'
        verbose_name_plural = '客户'

    def __str__(self):
        return self.name


class Photographer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='关联用户')
    name = models.CharField(max_length=100, verbose_name='摄影师姓名')
    phone = models.CharField(max_length=20, verbose_name='联系电话')
    level = models.CharField(max_length=50, verbose_name='级别')
    description = models.TextField(null=True, blank=True, verbose_name='简介')
    is_active = models.BooleanField(default=True, verbose_name='是否在职')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'photographer'
        verbose_name = '摄影师'
        verbose_name_plural = '摄影师'

    def __str__(self):
        return self.name


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', '待确认'),
        ('confirmed', '已确认'),
        ('cancelled', '已取消'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='客户')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, verbose_name='套餐')
    photographer = models.ForeignKey(Photographer, on_delete=models.CASCADE, verbose_name='摄影师')
    appointment_date = models.DateField(verbose_name='预约日期')
    appointment_time = models.TimeField(verbose_name='预约时间')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    note = models.TextField(null=True, blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'appointment'
        verbose_name = '客户预约'
        verbose_name_plural = '客户预约'

    def __str__(self):
        return f"{self.customer.name} - {self.appointment_date}"


def generate_order_number():
    today = datetime.now()
    prefix = today.strftime('%Y%m%d')
    last_order = Order.objects.filter(order_number__startswith=prefix).order_by('-order_number').first()
    if last_order:
        last_num = int(last_order.order_number[-4:])
        new_num = str(last_num + 1).zfill(4)
    else:
        new_num = '0001'
    return f"{prefix}{new_num}"


class PhotoSelection(models.Model):
    order = models.OneToOneField('Order', on_delete=models.CASCADE, verbose_name='订单')
    selected_count = models.IntegerField(default=0, verbose_name='已选照片数量')
    total_count = models.IntegerField(default=0, verbose_name='总照片数量')
    is_completed = models.BooleanField(default=False, verbose_name='是否完成选片')
    selected_at = models.DateTimeField(null=True, blank=True, verbose_name='选片完成时间')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'photo_selection'
        verbose_name = '照片选片'
        verbose_name_plural = '照片选片'

    def __str__(self):
        return f"{self.order.order_number} - 选片"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', '待拍摄'),
        ('shooting', '拍摄中'),
        ('selected', '已选片'),
        ('completed', '已完成'),
    ]
    order_number = models.CharField(max_length=20, unique=True, default=generate_order_number, verbose_name='订单编号')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='客户')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, verbose_name='套餐')
    photographer = models.ForeignKey(Photographer, on_delete=models.CASCADE, verbose_name='摄影师')
    shoot_date = models.DateField(verbose_name='拍摄日期')
    shoot_time = models.TimeField(verbose_name='拍摄时间')
    location = models.CharField(max_length=200, verbose_name='拍摄地点')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='订单状态')
    deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='定金')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总金额')
    is_settled = models.BooleanField(default=False, verbose_name='是否已结算')
    note = models.TextField(null=True, blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'order'
        verbose_name = '拍摄订单'
        verbose_name_plural = '拍摄订单'

    def __str__(self):
        return self.order_number

    @property
    def remaining_amount(self):
        return self.total_amount - self.deposit

    def start_shooting(self):
        self.status = 'shooting'
        self.save()

    def finish_shooting(self):
        self.status = 'selected'
        PhotoSelection.objects.get_or_create(order=self)
        self.save()

    def complete_order(self):
        self.status = 'completed'
        self.save()

    def auto_settle(self, payment_method='线下支付'):
        if not Settlement.objects.filter(order=self).exists() and self.remaining_amount > 0:
            Settlement.objects.create(
                order=self,
                balance_amount=self.remaining_amount,
                payment_method=payment_method,
                remark='拍摄完成自动结算'
            )
            self.is_settled = True
            self.save()
            return True
        return False


@receiver(post_save, sender=PhotoSelection)
def update_order_status_on_selection(sender, instance, created, **kwargs):
    if instance.is_completed and instance.order.status != 'completed':
        instance.order.status = 'selected'
        instance.order.save()


class Settlement(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='settlement', verbose_name='订单')
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='尾款金额')
    payment_method = models.CharField(max_length=50, verbose_name='支付方式')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='支付时间')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'settlement'
        verbose_name = '尾款结算'
        verbose_name_plural = '尾款结算'

    def __str__(self):
        return f"{self.order.order_number} - 结算"


@receiver(post_save, sender=Settlement)
def update_order_settled_status(sender, instance, created, **kwargs):
    if created and not instance.order.is_settled:
        instance.order.is_settled = True
        instance.order.save()
