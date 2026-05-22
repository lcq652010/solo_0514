from django.db import models
from django.utils import timezone
from products.models import Product


class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name='商品')
    quantity = models.DecimalField('库存数量', max_digits=10, decimal_places=2, default=0)
    last_updated = models.DateTimeField('最后更新时间', auto_now=True)

    class Meta:
        verbose_name = '库存信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.product.name} - {self.quantity} {self.product.unit}'

    @property
    def is_low_stock(self):
        return self.quantity < self.product.min_stock


class StockRecord(models.Model):
    RECORD_TYPE_CHOICES = [
        ('in', '入库'),
        ('out', '出库'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    record_type = models.CharField('记录类型', max_length=10, choices=RECORD_TYPE_CHOICES)
    quantity = models.DecimalField('变动数量', max_digits=10, decimal_places=2)
    before_quantity = models.DecimalField('变动前数量', max_digits=10, decimal_places=2)
    after_quantity = models.DecimalField('变动后数量', max_digits=10, decimal_places=2)
    related_order_no = models.CharField('关联单号', max_length=50, blank=True, null=True)
    remark = models.TextField('备注', blank=True, null=True)
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = '库存变动记录'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.product.name} - {self.get_record_type_display()}'


class StockAlert(models.Model):
    ALERT_TYPE_CHOICES = [
        ('low', '库存不足'),
        ('normal', '库存正常'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    alert_type = models.CharField('预警类型', max_length=10, choices=ALERT_TYPE_CHOICES)
    current_quantity = models.DecimalField('当前库存', max_digits=10, decimal_places=2)
    min_stock = models.IntegerField('最低库存预警')
    is_handled = models.BooleanField('是否已处理', default=False)
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    handled_at = models.DateTimeField('处理时间', blank=True, null=True)

    class Meta:
        verbose_name = '库存预警'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.product.name} - {self.get_alert_type_display()}'
