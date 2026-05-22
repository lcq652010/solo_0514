from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import random
import time


class User(AbstractUser):
    ROLE_CHOICES = (
        ('cashier', '收银员'),
        ('maker', '制作员'),
        ('admin', '管理员'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='cashier', verbose_name='角色')
    phone = models.CharField(max_length=20, blank=True, verbose_name='联系电话')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.username} - {self.get_role_display()}'


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='分类名称')
    description = models.TextField(blank=True, verbose_name='分类描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='商品名称')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='所属分类')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    stock = models.IntegerField(default=0, verbose_name='库存数量')
    image = models.URLField(blank=True, verbose_name='商品图片')
    description = models.TextField(blank=True, verbose_name='商品描述')
    is_available = models.BooleanField(default=True, verbose_name='是否上架')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', '待制作'),
        ('making', '制作中'),
        ('ready', '待取餐'),
        ('completed', '已完成'),
    )

    order_no = models.CharField(max_length=20, unique=True, verbose_name='订单号')
    customer_name = models.CharField(max_length=100, verbose_name='顾客姓名')
    customer_phone = models.CharField(max_length=20, verbose_name='顾客电话')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单总金额')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='订单状态')
    is_paid = models.BooleanField(default=False, verbose_name='是否已支付')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')
    take_code = models.CharField(max_length=4, verbose_name='取餐码')
    is_notified = models.BooleanField(default=False, verbose_name='是否已提醒')
    is_archived = models.BooleanField(default=False, verbose_name='是否已归档')
    notified_at = models.DateTimeField(null=True, blank=True, verbose_name='提醒时间')
    archived_at = models.DateTimeField(null=True, blank=True, verbose_name='归档时间')
    remark = models.TextField(blank=True, verbose_name='订单备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.order_no

    def save(self, *args, **kwargs):
        if not self.order_no:
            self.order_no = self.generate_order_no()
        if not self.take_code:
            self.take_code = self.generate_take_code()
        
        if self.pk is not None:
            old_order = Order.objects.filter(pk=self.pk).first()
            if old_order and old_order.status != self.status:
                if old_order.status == 'making' and self.status == 'ready':
                    from django.utils import timezone
                    self.is_notified = False
                    self.notified_at = None
                if self.status == 'completed':
                    from django.utils import timezone
                    self.is_archived = True
                    self.archived_at = timezone.now()
        
        super().save(*args, **kwargs)

    @staticmethod
    def generate_order_no():
        timestamp = str(int(time.time()))
        random_num = str(random.randint(1000, 9999))
        return f'NT{timestamp}{random_num}'

    @staticmethod
    def generate_take_code():
        return str(random.randint(1000, 9999))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='所属订单')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    quantity = models.IntegerField(default=1, verbose_name='数量')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    sugar = models.CharField(max_length=50, blank=True, verbose_name='糖度')
    ice = models.CharField(max_length=50, blank=True, verbose_name='冰度')
    toppings = models.CharField(max_length=200, blank=True, verbose_name='配料')

    class Meta:
        verbose_name = '订单项'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.order.order_no} - {self.product.name}'
