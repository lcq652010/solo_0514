from django.db import models
from django.utils import timezone
from products.models import Product


class Supplier(models.Model):
    supplier_code = models.CharField('供应商编号', max_length=50, unique=True)
    name = models.CharField('供应商名称', max_length=200)
    contact_person = models.CharField('联系人', max_length=100, blank=True, null=True)
    phone = models.CharField('联系电话', max_length=50, blank=True, null=True)
    address = models.CharField('地址', max_length=500, blank=True, null=True)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = '供应商'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', '待入库'),
        ('completed', '已入库'),
        ('cancelled', '已作废'),
    ]

    order_no = models.CharField('采购单号', max_length=50, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='供应商')
    total_amount = models.DecimalField('总金额', max_digits=12, decimal_places=2, default=0)
    status = models.CharField('状态', max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    remark = models.TextField('备注', blank=True, null=True)
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '采购订单'
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
        prefix = f'PO{date_str}'
        max_no = PurchaseOrder.objects.filter(order_no__startswith=prefix).aggregate(Max('order_no'))['order_no__max']
        if max_no:
            seq = int(max_no[-4:]) + 1
        else:
            seq = 1
        return f'{prefix}{seq:04d}'


class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, related_name='items', on_delete=models.CASCADE, verbose_name='采购订单')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    quantity = models.DecimalField('数量', max_digits=10, decimal_places=2)
    unit_price = models.DecimalField('单价', max_digits=10, decimal_places=2)
    subtotal = models.DecimalField('小计', max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = '采购订单明细'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.purchase_order.order_no} - {self.product.name}'

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)
