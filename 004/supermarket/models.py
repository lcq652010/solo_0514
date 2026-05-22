from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid
import random


class User(AbstractUser):
    """自定义用户模型，扩展角色权限"""
    ROLE_CHOICES = [
        ('cashier', '收银员'),
        ('warehouse', '库管员'),
        ('admin', '管理员'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='cashier', verbose_name='角色')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='手机号')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
    
    def __str__(self):
        return f'{self.username} - {self.get_role_display()}'
    
    @property
    def is_cashier(self):
        return self.role == 'cashier'
    
    @property
    def is_warehouse(self):
        return self.role == 'warehouse'
    
    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser


class Product(models.Model):
    """商品模型"""
    CATEGORY_CHOICES = [
        ('food', '食品'),
        ('drink', '饮料'),
        ('snack', '零食'),
        ('daily', '日用品'),
        ('stationery', '文具'),
        ('other', '其他'),
    ]

    product_id = models.CharField(max_length=50, unique=True, verbose_name='商品编号')
    name = models.CharField(max_length=100, verbose_name='商品名称')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='商品分类')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='售价')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='成本价')
    stock = models.IntegerField(default=0, verbose_name='库存数量')
    unit = models.CharField(max_length=20, default='件', verbose_name='单位')
    barcode = models.CharField(max_length=50, blank=True, null=True, verbose_name='条形码')
    supplier = models.CharField(max_length=100, blank=True, null=True, verbose_name='供应商')
    description = models.TextField(blank=True, null=True, verbose_name='商品描述')
    is_active = models.BooleanField(default=True, verbose_name='是否上架')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.product_id} - {self.name}'


class Member(models.Model):
    """会员模型"""
    member_id = models.CharField(max_length=20, unique=True, verbose_name='会员编号')
    name = models.CharField(max_length=50, verbose_name='姓名')
    phone = models.CharField(max_length=20, unique=True, verbose_name='手机号')
    points = models.IntegerField(default=0, verbose_name='积分余额')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='累计消费')
    is_active = models.BooleanField(default=True, verbose_name='是否有效')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '会员'
        verbose_name_plural = '会员'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.member_id} - {self.name}'

    def add_points(self, amount):
        """根据消费金额增加积分，1元=1积分"""
        points = int(amount)
        self.points += points
        self.total_amount += amount
        self.save()

    def deduct_points(self, points):
        """使用积分"""
        if self.points >= points:
            self.points -= points
            self.save()
            return True
        return False


class PurchaseOrder(models.Model):
    """采购订单模型"""
    STATUS_CHOICES = [
        ('pending', '待入库'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]

    order_no = models.CharField(max_length=30, unique=True, verbose_name='采购单号')
    supplier = models.CharField(max_length=100, verbose_name='供应商')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='总金额')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    remark = models.TextField(blank=True, null=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '采购订单'
        verbose_name_plural = '采购订单'
        ordering = ['-created_at']

    def __str__(self):
        return self.order_no

    def save(self, *args, **kwargs):
        if not self.order_no:
            self.order_no = self.generate_order_no()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_order_no():
        """生成采购单号：CG + 时间戳 + 4位随机数"""
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        random_num = str(random.randint(1000, 9999))
        return f'CG{timestamp}{random_num}'


class PurchaseItem(models.Model):
    """采购明细"""
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items', verbose_name='采购订单')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    quantity = models.IntegerField(verbose_name='数量')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='小计')

    class Meta:
        verbose_name = '采购明细'
        verbose_name_plural = '采购明细'

    def __str__(self):
        return f'{self.purchase_order.order_no} - {self.product.name}'


class SalesOrder(models.Model):
    """销售订单（收银单）模型"""
    STATUS_CHOICES = [
        ('pending', '待结账'),
        ('completed', '已完成'),
        ('refunded', '已退款'),
        ('cancelled', '已作废'),
    ]

    order_no = models.CharField(max_length=30, unique=True, verbose_name='收银单号')
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='会员')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='总金额')
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='优惠金额')
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='实付金额')
    points_used = models.IntegerField(default=0, verbose_name='使用积分')
    points_earned = models.IntegerField(default=0, verbose_name='获得积分')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    cashier = models.CharField(max_length=50, default='收银员', verbose_name='收银员')
    remark = models.TextField(blank=True, null=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '销售订单'
        verbose_name_plural = '销售订单'
        ordering = ['-created_at']

    def __str__(self):
        return self.order_no

    def save(self, *args, **kwargs):
        if not self.order_no:
            self.order_no = self.generate_order_no()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_order_no():
        """生成收银单号：SK + 时间戳 + 4位随机数"""
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        random_num = str(random.randint(1000, 9999))
        return f'SK{timestamp}{random_num}'

    def complete_order(self):
        """完成订单"""
        if self.status == 'pending':
            self.status = 'completed'
            self.save()


class SalesItem(models.Model):
    """销售明细"""
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='items', verbose_name='销售订单')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    quantity = models.IntegerField(verbose_name='数量')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='小计')

    class Meta:
        verbose_name = '销售明细'
        verbose_name_plural = '销售明细'

    def __str__(self):
        return f'{self.sales_order.order_no} - {self.product.name}'


class StockLog(models.Model):
    """库存变动日志"""
    TYPE_CHOICES = [
        ('purchase', '采购入库'),
        ('sale', '销售出库'),
        ('refund', '退货入库'),
        ('adjust', '库存调整'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='变动类型')
    quantity = models.IntegerField(verbose_name='变动数量')
    stock_before = models.IntegerField(verbose_name='变动前库存')
    stock_after = models.IntegerField(verbose_name='变动后库存')
    related_order = models.CharField(max_length=30, blank=True, null=True, verbose_name='相关单号')
    remark = models.TextField(blank=True, null=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '库存日志'
        verbose_name_plural = '库存日志'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.product.name} - {self.get_type_display()}'


class PointsLog(models.Model):
    """积分变动日志"""
    TYPE_CHOICES = [
        ('earn', '获得积分'),
        ('use', '使用积分'),
        ('adjust', '积分调整'),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name='会员')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='变动类型')
    points = models.IntegerField(verbose_name='变动积分')
    points_before = models.IntegerField(verbose_name='变动前积分')
    points_after = models.IntegerField(verbose_name='变动后积分')
    related_order = models.CharField(max_length=30, blank=True, null=True, verbose_name='相关单号')
    remark = models.TextField(blank=True, null=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '积分日志'
        verbose_name_plural = '积分日志'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.member.name} - {self.get_type_display()}'
