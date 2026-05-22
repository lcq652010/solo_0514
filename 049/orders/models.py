from django.db import models
from django.utils import timezone
from products.models import Product


class Customer(models.Model):
    customer_code = models.CharField('客户编号', max_length=50, unique=True)
    name = models.CharField('客户名称', max_length=200)
    contact_person = models.CharField('联系人', max_length=100, blank=True, null=True)
    phone = models.CharField('联系电话', max_length=50, blank=True, null=True)
    address = models.CharField('地址', max_length=500, blank=True, null=True)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = '客户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class WholesaleOrder(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', '待出库'),
        ('delivering', '配送中'),
        ('completed', '已完成'),
        ('cancelled', '已作废'),
    ]

    order_no = models.CharField('订单编号', max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='客户')
    total_amount = models.DecimalField('总金额', max_digits=12, decimal_places=2, default=0)
    status = models.CharField('状态', max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    delivery_address = models.CharField('配送地址', max_length=500, blank=True, null=True)
    delivery_fee = models.DecimalField('配送费', max_digits=10, decimal_places=2, default=0)
    remark = models.TextField('备注', blank=True, null=True)
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '批发订单'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.order_no

    def save(self, *args, **kwargs):
        if not self.order_no:
            self.order_no = self.generate_order_no()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_order_no():
        from django.db.models import Max
        date_str = timezone.now().strftime('%Y%m%d')
        prefix = f'WO{date_str}'
        max_no = WholesaleOrder.objects.filter(order_no__startswith=prefix).aggregate(Max('order_no'))['order_no__max']
        if max_no:
            seq = int(max_no[-4:]) + 1
        else:
            seq = 1
        return f'{prefix}{seq:04d}'


class WholesaleOrderItem(models.Model):
    wholesale_order = models.ForeignKey(WholesaleOrder, related_name='items', on_delete=models.CASCADE, verbose_name='批发订单')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    quantity = models.DecimalField('数量', max_digits=10, decimal_places=2)
    unit_price = models.DecimalField('单价', max_digits=10, decimal_places=2)
    subtotal = models.DecimalField('小计', max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = '批发订单明细'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.wholesale_order.order_no} - {self.product.name}'

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class Settlement(models.Model):
    SETTLEMENT_STATUS_CHOICES = [
        ('unpaid', '未结算'),
        ('paid', '已结算'),
    ]

    settlement_no = models.CharField('结算单号', max_length=50, unique=True)
    wholesale_order = models.OneToOneField(WholesaleOrder, on_delete=models.CASCADE, verbose_name='关联订单')
    total_amount = models.DecimalField('结算金额', max_digits=12, decimal_places=2)
    status = models.CharField('状态', max_length=20, choices=SETTLEMENT_STATUS_CHOICES, default='unpaid')
    payment_method = models.CharField('支付方式', max_length=50, blank=True, null=True)
    settled_at = models.DateTimeField('结算时间', blank=True, null=True)
    remark = models.TextField('备注', blank=True, null=True)
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = '出库结算'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.settlement_no

    def save(self, *args, **kwargs):
        if not self.settlement_no:
            self.settlement_no = self.generate_settlement_no()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_settlement_no():
        from django.db.models import Max
        date_str = timezone.now().strftime('%Y%m%d')
        prefix = f'ST{date_str}'
        max_no = Settlement.objects.filter(settlement_no__startswith=prefix).aggregate(Max('settlement_no'))['settlement_no__max']
        if max_no:
            seq = int(max_no[-4:]) + 1
        else:
            seq = 1
        return f'{prefix}{seq:04d}'
