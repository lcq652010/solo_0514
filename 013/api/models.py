import uuid
from django.db import models
from django.utils import timezone


class Shop(models.Model):
    name = models.CharField(max_length=100, verbose_name='店铺名称')
    address = models.CharField(max_length=200, verbose_name='店铺地址')
    phone = models.CharField(max_length=20, verbose_name='联系电话')
    description = models.TextField(blank=True, verbose_name='店铺描述')
    is_open = models.BooleanField(default=True, verbose_name='是否营业')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'shop'
        verbose_name = '店铺'
        verbose_name_plural = '店铺'

    def __str__(self):
        return self.name


class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products', verbose_name='所属店铺')
    name = models.CharField(max_length=100, verbose_name='商品名称')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    image = models.URLField(blank=True, verbose_name='商品图片')
    description = models.TextField(blank=True, verbose_name='商品描述')
    category = models.CharField(max_length=50, verbose_name='分类')
    is_available = models.BooleanField(default=True, verbose_name='是否上架')
    stock = models.IntegerField(default=0, verbose_name='库存')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'product'
        verbose_name = '商品'
        verbose_name_plural = '商品'

    def __str__(self):
        return self.name


class Rider(models.Model):
    name = models.CharField(max_length=50, verbose_name='骑手姓名')
    phone = models.CharField(max_length=20, verbose_name='联系电话')
    id_card = models.CharField(max_length=18, unique=True, verbose_name='身份证号')
    vehicle_type = models.CharField(max_length=20, choices=[
        ('electric', '电动车'),
        ('motorcycle', '摩托车'),
        ('bicycle', '自行车'),
    ], verbose_name='交通工具')
    is_available = models.BooleanField(default=True, verbose_name='是否在岗')
    current_order_count = models.IntegerField(default=0, verbose_name='当前订单数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'rider'
        verbose_name = '骑手'
        verbose_name_plural = '骑手'

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', '待接单'),
        ('delivering', '配送中'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]

    order_no = models.CharField(max_length=32, unique=True, verbose_name='订单号')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='orders', verbose_name='店铺')
    rider = models.ForeignKey(Rider, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders', verbose_name='骑手')
    customer_name = models.CharField(max_length=50, verbose_name='顾客姓名')
    customer_phone = models.CharField(max_length=20, verbose_name='顾客电话')
    customer_address = models.CharField(max_length=200, verbose_name='配送地址')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单总金额')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='订单状态')
    remark = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='下单时间')
    accepted_at = models.DateTimeField(null=True, blank=True, verbose_name='接单时间')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    cancelled_at = models.DateTimeField(null=True, blank=True, verbose_name='取消时间')

    class Meta:
        db_table = 'order'
        verbose_name = '订单'
        verbose_name_plural = '订单'
        ordering = ['-created_at']

    def __str__(self):
        return self.order_no

    def save(self, *args, **kwargs):
        if not self.order_no:
            self.order_no = self.generate_order_no()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_order_no():
        import random
        from django.utils import timezone
        now = timezone.now()
        date_str = now.strftime('%Y%m%d%H%M%S')
        random_str = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        return f'FD{date_str}{random_str}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='订单')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    quantity = models.IntegerField(default=1, verbose_name='数量')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='小计')

    class Meta:
        db_table = 'order_item'
        verbose_name = '订单项'
        verbose_name_plural = '订单项'

    def __str__(self):
        return f'{self.order.order_no} - {self.product.name}'


class DeliveryTracking(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tracking_records', verbose_name='订单')
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE, verbose_name='骑手')
    status = models.CharField(max_length=50, verbose_name='状态')
    description = models.CharField(max_length=200, verbose_name='描述')
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True, verbose_name='纬度')
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True, verbose_name='经度')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='时间')

    class Meta:
        db_table = 'delivery_tracking'
        verbose_name = '配送跟踪'
        verbose_name_plural = '配送跟踪'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.order.order_no} - {self.status}'
