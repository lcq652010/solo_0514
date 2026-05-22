from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('reception', '前台'),
        ('engineer', '工程师'),
        ('admin', '管理员'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='reception')
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Customer(models.Model):
    name = models.CharField(max_length=100, verbose_name='客户姓名')
    phone = models.CharField(max_length=20, verbose_name='联系电话')
    email = models.EmailField(blank=True, null=True, verbose_name='邮箱')
    address = models.TextField(blank=True, null=True, verbose_name='地址')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '客户'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.name} - {self.phone}'


class Device(models.Model):
    TYPE_CHOICES = (
        ('phone', '手机'),
        ('tablet', '平板'),
        ('laptop', '笔记本'),
        ('desktop', '台式机'),
        ('other', '其他'),
    )
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='devices', verbose_name='所属客户')
    device_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='设备类型')
    brand = models.CharField(max_length=50, verbose_name='品牌')
    model = models.CharField(max_length=100, verbose_name='型号')
    serial_number = models.CharField(max_length=100, blank=True, null=True, verbose_name='序列号')
    description = models.TextField(blank=True, null=True, verbose_name='设备描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '设备'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.brand} {self.model} - {self.get_device_type_display()}'


class RepairOrder(models.Model):
    STATUS_CHOICES = (
        ('pending', '待受理'),
        ('diagnosing', '检测中'),
        ('repairing', '维修中'),
        ('waiting_parts', '待配件'),
        ('completed', '已完成'),
        ('picked_up', '已取机'),
        ('archived', '已归档'),
        ('cancelled', '已取消'),
    )
    
    order_number = models.CharField(max_length=50, unique=True, verbose_name='工单号')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='repair_orders', verbose_name='客户')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='repair_orders', verbose_name='设备')
    fault_description = models.TextField(verbose_name='故障描述')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='assigned_orders', verbose_name='分配工程师')
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='预估费用')
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='实际费用')
    diagnosis_result = models.TextField(blank=True, null=True, verbose_name='检测结果')
    repair_solution = models.TextField(blank=True, null=True, verbose_name='维修方案')
    parts_used = models.TextField(blank=True, null=True, verbose_name='使用配件')
    remarks = models.TextField(blank=True, null=True, verbose_name='备注')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_orders', verbose_name='创建人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    completed_at = models.DateTimeField(blank=True, null=True, verbose_name='完成时间')
    picked_up_at = models.DateTimeField(blank=True, null=True, verbose_name='取机时间')
    archived_at = models.DateTimeField(blank=True, null=True, verbose_name='归档时间')
    
    class Meta:
        verbose_name = '维修工单'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.order_number} - {self.customer.name}'
    
    def save(self, *args, **kwargs):
        if self.pk:
            old_order = RepairOrder.objects.filter(pk=self.pk).first()
            if old_order and old_order.status != 'completed' and self.status == 'completed':
                self.completed_at = timezone.now()
                Notification.create_repair_completed_notification(self)
            if old_order and old_order.status != 'picked_up' and self.status == 'picked_up':
                self.picked_up_at = timezone.now()
            if old_order and old_order.status != 'archived' and self.status == 'archived':
                self.archived_at = timezone.now()
        super().save(*args, **kwargs)


class Notification(models.Model):
    TYPE_CHOICES = (
        ('repair_completed', '维修完成'),
        ('order_assigned', '工单分配'),
        ('status_changed', '状态变更'),
        ('system', '系统通知'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name='接收用户')
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICES, verbose_name='通知类型')
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    related_order = models.ForeignKey(RepairOrder, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='相关工单')
    is_read = models.BooleanField(default=False, verbose_name='已读')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '通知'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.title} - {self.user.username}'
    
    @classmethod
    def create_repair_completed_notification(cls, repair_order):
        users = User.objects.filter(profile__role__in=['admin', 'reception'])
        for user in users:
            cls.objects.create(
                user=user,
                notification_type='repair_completed',
                title=f'工单{repair_order.order_number}已完成',
                content=f'客户{repair_order.customer.name}的设备{repair_order.device.brand} {repair_order.device.model}已维修完成，请通知客户取机。',
                related_order=repair_order
            )
    
    @classmethod
    def create_order_assigned_notification(cls, repair_order, engineer):
        cls.objects.create(
            user=engineer,
            notification_type='order_assigned',
            title='您有新的维修工单',
            content=f'工单{repair_order.order_number}已分配给您，请及时处理。',
            related_order=repair_order
        )


class ArchivedOrder(models.Model):
    original_order_id = models.IntegerField(verbose_name='原工单ID')
    order_number = models.CharField(max_length=50, verbose_name='工单号')
    customer_name = models.CharField(max_length=100, verbose_name='客户姓名')
    customer_phone = models.CharField(max_length=20, verbose_name='客户电话')
    device_info = models.CharField(max_length=200, verbose_name='设备信息')
    fault_description = models.TextField(verbose_name='故障描述')
    repair_solution = models.TextField(blank=True, null=True, verbose_name='维修方案')
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='实际费用')
    picked_up_at = models.DateTimeField(verbose_name='取机时间')
    archived_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='归档人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='归档时间')
    
    class Meta:
        verbose_name = '归档工单'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.order_number} - 已归档'
    
    @classmethod
    def archive_from_repair_order(cls, repair_order, archived_by):
        archived = cls.objects.create(
            original_order_id=repair_order.id,
            order_number=repair_order.order_number,
            customer_name=repair_order.customer.name,
            customer_phone=repair_order.customer.phone,
            device_info=f'{repair_order.device.brand} {repair_order.device.model}',
            fault_description=repair_order.fault_description,
            repair_solution=repair_order.repair_solution,
            actual_cost=repair_order.actual_cost,
            picked_up_at=repair_order.picked_up_at,
            archived_by=archived_by
        )
        repair_order.status = 'archived'
        repair_order.archived_at = timezone.now()
        repair_order.save()
        return archived
