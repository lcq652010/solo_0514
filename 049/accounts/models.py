from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('order_clerk', '开单员'),
        ('warehouse_manager', '库管'),
        ('boss', '老板'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    role = models.CharField('角色', max_length=30, choices=ROLE_CHOICES, default='order_clerk')
    phone = models.CharField('手机号', max_length=20, blank=True, null=True)
    department = models.CharField('部门', max_length=100, blank=True, null=True)
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '用户档案'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}'

    @property
    is_order_clerk(self):
        return self.role == 'order_clerk'

    @property
    is_warehouse_manager(self):
        return self.role == 'warehouse_manager'

    @property
    is_boss(self):
        return self.role == 'boss'


class Permission:
    ORDER_MANAGE = 'order_manage'
    WAREHOUSE_MANAGE = 'warehouse_manage'
    VIEW_REPORTS = 'view_reports'
    USER_MANAGE = 'user_manage'
    PRODUCT_MANAGE = 'product_manage'
    SUPPLIER_MANAGE = 'supplier_manage'
    CUSTOMER_MANAGE = 'customer_manage'
    SETTLEMENT_MANAGE = 'settlement_manage'

    ROLE_PERMISSIONS = {
        'order_clerk': [
            ORDER_MANAGE,
            PRODUCT_MANAGE,
            CUSTOMER_MANAGE,
        ],
        'warehouse_manager': [
            WAREHOUSE_MANAGE,
            PRODUCT_MANAGE,
            SUPPLIER_MANAGE,
        ],
        'boss': [
            ORDER_MANAGE,
            WAREHOUSE_MANAGE,
            VIEW_REPORTS,
            USER_MANAGE,
            PRODUCT_MANAGE,
            SUPPLIER_MANAGE,
            CUSTOMER_MANAGE,
            SETTLEMENT_MANAGE,
        ]
    }

    @classmethod
    def get_role_permissions(cls, role):
        return cls.ROLE_PERMISSIONS.get(role, [])

    @classmethod
    def has_permission(cls, role, permission):
        return permission in cls.get_role_permissions(role)


class StockAlertMessage(models.Model):
    ALERT_LEVEL_CHOICES = [
        ('warning', '警告'),
        ('danger', '危险'),
    ]

    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, verbose_name='商品')
    alert_level = models.CharField('预警级别', max_length=20, choices=ALERT_LEVEL_CHOICES, default='warning')
    current_quantity = models.DecimalField('当前库存', max_digits=10, decimal_places=2)
    min_stock = models.IntegerField('预警线')
    message = models.TextField('预警消息')
    is_read = models.BooleanField('已读', default=False)
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    read_at = models.DateTimeField('阅读时间', blank=True, null=True)

    class Meta:
        verbose_name = '库存预警消息'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.product.name} - {self.get_alert_level_display()}'
