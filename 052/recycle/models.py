import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserRole(models.TextChoices):
    CUSTOMER_SERVICE = 'customer_service', '客服'
    RECYCLER = 'recycler', '回收员'
    ADMIN = 'admin', '管理员'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='用户')
    role = models.CharField(max_length=30, choices=UserRole.choices, default=UserRole.CUSTOMER_SERVICE, verbose_name='角色')
    phone = models.CharField(max_length=20, blank=True, verbose_name='联系电话')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'

    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class ItemCategory(models.TextChoices):
    ELECTRONICS = 'electronics', '电子产品'
    FURNITURE = 'furniture', '家具'
    METAL = 'metal', '金属'
    PAPER = 'paper', '纸品'
    PLASTIC = 'plastic', '塑料'
    CLOTHING = 'clothing', '衣物'
    OTHER = 'other', '其他'


class OrderStatus(models.TextChoices):
    PENDING_PICKUP = 'pending_pickup', '待上门'
    PICKED_UP = 'picked_up', '已回收'
    WAREHOUSED = 'warehoused', '已入库'
    COMPLETED = 'completed', '已完成'


class Item(models.Model):
    name = models.CharField(max_length=200, verbose_name='物品名称')
    category = models.CharField(max_length=50, choices=ItemCategory.choices, verbose_name='物品分类')
    description = models.TextField(blank=True, verbose_name='物品描述')
    quantity = models.IntegerField(default=1, verbose_name='数量')
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='估价')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_items', verbose_name='创建人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '物品'
        verbose_name_plural = '物品'

    def __str__(self):
        return self.name


def generate_order_no():
    date_str = timezone.now().strftime('%Y%m%d')
    uuid_str = str(uuid.uuid4())[:8].upper()
    return f'RC{date_str}{uuid_str}'


class Order(models.Model):
    order_no = models.CharField(max_length=32, default=generate_order_no, unique=True, verbose_name='回收单号')
    customer_name = models.CharField(max_length=100, verbose_name='客户姓名')
    customer_phone = models.CharField(max_length=20, verbose_name='联系电话')
    address = models.CharField(max_length=500, verbose_name='回收地址')
    pickup_time = models.DateTimeField(verbose_name='上门时间')
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING_PICKUP, verbose_name='订单状态')
    items = models.ManyToManyField(Item, through='OrderItem', verbose_name='回收物品')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='总金额')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_orders', verbose_name='创建人')
    recycler = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_orders', verbose_name='回收员')
    picked_up_at = models.DateTimeField(null=True, blank=True, verbose_name='回收时间')
    warehoused_at = models.DateTimeField(null=True, blank=True, verbose_name='入库时间')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    remark = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '回收订单'
        verbose_name_plural = '回收订单'
        ordering = ['-created_at']

    def __str__(self):
        return self.order_no

    def auto_warehouse(self, checker=None):
        if self.status != OrderStatus.PICKED_UP:
            return False, '订单状态不是已回收，无法自动入库'
        
        with transaction.atomic():
            QualityCheck.objects.create(
                order=self,
                checker=checker.username if checker else '系统自动',
                result=QualityCheck.CHECK_PASS,
                actual_amount=self.total_amount,
                issue_description='回收完成自动入库，系统默认通过'
            )
            self.status = OrderStatus.WAREHOUSED
            self.warehoused_at = timezone.now()
            self.save()
        return True, '自动入库完成'

    def auto_settle(self, operator=None):
        if self.status != OrderStatus.WAREHOUSED:
            return False, '订单状态不是已入库，无法自动结算'
        
        try:
            quality_check = self.quality_check
            settle_amount = quality_check.actual_amount
        except QualityCheck.DoesNotExist:
            settle_amount = self.total_amount

        with transaction.atomic():
            Settlement.objects.create(
                order=self,
                settle_amount=settle_amount,
                operator=operator.username if operator else '系统自动',
                remark='质检完成自动结算'
            )
            self.status = OrderStatus.COMPLETED
            self.completed_at = timezone.now()
            self.save()
        return True, '自动结算完成'


from django.db import transaction


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='订单')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='物品')
    quantity = models.IntegerField(default=1, verbose_name='数量')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='单价')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='小计')

    class Meta:
        verbose_name = '订单项'
        verbose_name_plural = '订单项'

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class QualityCheck(models.Model):
    CHECK_PASS = 'pass'
    CHECK_FAIL = 'fail'
    CHECK_RESULT = [
        (CHECK_PASS, '通过'),
        (CHECK_FAIL, '不通过'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='quality_check', verbose_name='订单')
    checker = models.CharField(max_length=100, verbose_name='质检人')
    check_time = models.DateTimeField(auto_now_add=True, verbose_name='质检时间')
    result = models.CharField(max_length=20, choices=CHECK_RESULT, verbose_name='质检结果')
    actual_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='实际金额')
    issue_description = models.TextField(blank=True, verbose_name='问题描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '入库质检'
        verbose_name_plural = '入库质检'

    def __str__(self):
        return f'{self.order.order_no} - 质检'


class Settlement(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='settlement', verbose_name='订单')
    settle_time = models.DateTimeField(auto_now_add=True, verbose_name='结算时间')
    settle_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='结算金额')
    operator = models.CharField(max_length=100, verbose_name='操作员')
    remark = models.TextField(blank=True, verbose_name='备注')

    class Meta:
        verbose_name = '订单结算'
        verbose_name_plural = '订单结算'

    def __str__(self):
        return f'{self.order.order_no} - 结算'
