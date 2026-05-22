from django.db import models
from django.utils import timezone


class ProductCategory(models.Model):
    name = models.CharField('分类名称', max_length=100, unique=True)
    description = models.TextField('描述', blank=True, null=True)
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Product(models.Model):
    product_code = models.CharField('商品编号', max_length=50, unique=True)
    name = models.CharField('商品名称', max_length=200)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='商品分类')
    specification = models.CharField('规格', max_length=100, blank=True, null=True)
    unit = models.CharField('单位', max_length=20, default='kg')
    purchase_price = models.DecimalField('采购价', max_digits=10, decimal_places=2)
    wholesale_price = models.DecimalField('批发价', max_digits=10, decimal_places=2)
    min_stock = models.IntegerField('最低库存预警', default=10)
    description = models.TextField('描述', blank=True, null=True)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.product_code} - {self.name}'
