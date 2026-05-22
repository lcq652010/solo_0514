from django.db import models
from owners.models import Owner
from bills.models import Bill


class Payment(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name='缴费业主')
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, null=True, blank=True, verbose_name='关联账单')
    payment_no = models.CharField(max_length=50, unique=True, verbose_name='支付单号')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='支付金额')
    payment_method = models.CharField(max_length=20, choices=[
        ('alipay', '支付宝'),
        ('wechat', '微信支付'),
        ('bank', '银行卡'),
        ('cash', '现金'),
        ('other', '其他')
    ], verbose_name='支付方式')
    status = models.CharField(max_length=20, choices=[
        ('pending', '待支付'),
        ('success', '支付成功'),
        ('failed', '支付失败'),
        ('refunded', '已退款')
    ], default='pending', verbose_name='支付状态')
    transaction_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='第三方交易号')
    paid_time = models.DateTimeField(null=True, blank=True, verbose_name='支付完成时间')
    operator = models.CharField(max_length=50, blank=True, null=True, verbose_name='操作人')
    remarks = models.TextField(blank=True, null=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '缴费记录'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return f'{self.payment_no} - {self.amount}元'
