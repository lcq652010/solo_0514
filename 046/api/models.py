from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models import Avg, Count
import uuid


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', '管理员'),
        ('aunt', '家政员'),
        ('customer', '客户'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer', verbose_name='用户角色')
    phone = models.CharField(max_length=20, verbose_name='手机号', blank=True)
    avatar = models.URLField(verbose_name='头像', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.username} - {self.get_role_display()}'


class Customer(models.Model):
    GENDER_CHOICES = [
        ('male', '男'),
        ('female', '女'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='关联用户', related_name='customer_profile')
    name = models.CharField(max_length=50, verbose_name='姓名')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='性别', blank=True)
    phone = models.CharField(max_length=20, verbose_name='联系电话')
    address = models.CharField(max_length=200, verbose_name='住址', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'customer'
        verbose_name = '客户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_order_count(self):
        return self.orders.count()

    def get_completed_order_count(self):
        return self.orders.filter(status='completed').count()


class Aunt(models.Model):
    GENDER_CHOICES = [
        ('male', '男'),
        ('female', '女'),
    ]
    STATUS_CHOICES = [
        ('available', '空闲'),
        ('busy', '服务中'),
        ('rest', '休息'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='关联用户', related_name='aunt_profile', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name='姓名')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='性别')
    age = models.IntegerField(verbose_name='年龄')
    phone = models.CharField(max_length=20, verbose_name='联系电话')
    id_card = models.CharField(max_length=18, verbose_name='身份证号', unique=True)
    avatar = models.URLField(verbose_name='头像', blank=True, null=True)
    skills = models.ManyToManyField('Service', verbose_name='擅长技能')
    experience = models.IntegerField(verbose_name='工作年限', default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name='状态')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0, verbose_name='评分')
    total_orders = models.IntegerField(verbose_name='完成订单数', default=0)
    total_reviews = models.IntegerField(verbose_name='评价数', default=0)
    address = models.CharField(max_length=200, verbose_name='住址', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='入职时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'aunt'
        verbose_name = '阿姨信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def update_rating(self):
        avg_rating = Review.objects.filter(aunt=self).aggregate(avg=Avg('rating'))['avg'] or 5.0
        self.rating = round(avg_rating, 1)
        self.total_reviews = Review.objects.filter(aunt=self).count()
        self.save()

    def update_order_count(self):
        self.total_orders = Order.objects.filter(aunt=self, status='completed').count()
        self.save()


class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name='服务名称')
    description = models.TextField(verbose_name='服务描述', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='服务价格')
    duration = models.IntegerField(verbose_name='服务时长(小时)', default=1)
    image = models.URLField(verbose_name='服务图片', blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'service'
        verbose_name = '服务项目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', '待派单'),
        ('servicing', '服务中'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
        ('archived', '已归档'),
    ]
    order_no = models.CharField(max_length=32, unique=True, verbose_name='订单号', editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name='客户', related_name='orders', null=True)
    customer_name = models.CharField(max_length=50, verbose_name='客户姓名')
    customer_phone = models.CharField(max_length=20, verbose_name='客户电话')
    customer_address = models.CharField(max_length=200, verbose_name='服务地址')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, verbose_name='服务项目')
    aunt = models.ForeignKey(Aunt, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='服务阿姨', related_name='orders')
    service_date = models.DateField(verbose_name='服务日期')
    service_time = models.TimeField(verbose_name='服务时间')
    duration = models.IntegerField(verbose_name='服务时长(小时)', default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总金额')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='订单状态')
    completed_at = models.DateTimeField(verbose_name='完成时间', null=True, blank=True)
    remark = models.TextField(verbose_name='备注', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='下单时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'order'
        verbose_name = '订单'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.order_no

    def save(self, *args, **kwargs):
        if not self.order_no:
            self.order_no = self.generate_order_no()
        if self.service and not self.total_price:
            self.total_price = self.service.price * self.duration
        super().save(*args, **kwargs)

    @staticmethod
    def generate_order_no():
        date_str = timezone.now().strftime('%Y%m%d%H%M%S')
        unique_id = str(uuid.uuid4().hex[:6]).upper()
        return f'ORD{date_str}{unique_id}'

    def complete_order(self):
        if self.status == 'servicing':
            self.status = 'completed'
            self.completed_at = timezone.now()
            self.save()
            if self.aunt:
                self.aunt.status = 'available'
                self.aunt.save()
                self.aunt.update_order_count()
            return True
        return False

    def archive_order(self):
        if self.status == 'completed':
            self.status = 'archived'
            self.save()
            return True
        return False


class Review(models.Model):
    RATING_CHOICES = [
        (1, '1星'),
        (2, '2星'),
        (3, '3星'),
        (4, '4星'),
        (5, '5星'),
    ]
    order = models.OneToOneField(Order, on_delete=models.CASCADE, verbose_name='关联订单', related_name='review')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='评价客户', null=True)
    aunt = models.ForeignKey(Aunt, on_delete=models.CASCADE, verbose_name='评价阿姨', related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES, default=5, verbose_name='评分')
    content = models.TextField(verbose_name='评价内容', blank=True)
    is_anonymous = models.BooleanField(default=False, verbose_name='是否匿名')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='评价时间')

    class Meta:
        db_table = 'review'
        verbose_name = '评价'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.order.order_no} - {self.rating}星'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.aunt.update_rating()


class OrderArchive(models.Model):
    order_no = models.CharField(max_length=32, verbose_name='订单号')
    customer_name = models.CharField(max_length=50, verbose_name='客户姓名')
    customer_phone = models.CharField(max_length=20, verbose_name='客户电话')
    service_name = models.CharField(max_length=100, verbose_name='服务名称')
    aunt_name = models.CharField(max_length=50, verbose_name='阿姨姓名', blank=True)
    service_date = models.DateField(verbose_name='服务日期')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总金额')
    rating = models.IntegerField(verbose_name='评分', null=True)
    review_content = models.TextField(verbose_name='评价内容', blank=True)
    original_order_id = models.IntegerField(verbose_name='原订单ID')
    created_at = models.DateTimeField(verbose_name='下单时间')
    completed_at = models.DateTimeField(verbose_name='完成时间')
    archived_at = models.DateTimeField(auto_now_add=True, verbose_name='归档时间')

    class Meta:
        db_table = 'order_archive'
        verbose_name = '订单归档'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'归档订单: {self.order_no}'

    @classmethod
    def archive_from_order(cls, order):
        review = Review.objects.filter(order=order).first()
        archive = cls.objects.create(
            order_no=order.order_no,
            customer_name=order.customer_name,
            customer_phone=order.customer_phone,
            service_name=order.service.name,
            aunt_name=order.aunt.name if order.aunt else '',
            service_date=order.service_date,
            total_price=order.total_price,
            rating=review.rating if review else None,
            review_content=review.content if review else '',
            original_order_id=order.id,
            created_at=order.created_at,
            completed_at=order.completed_at
        )
        order.archive_order()
        return archive


class AuntStatistics(models.Model):
    aunt = models.OneToOneField(Aunt, on_delete=models.CASCADE, verbose_name='阿姨', related_name='statistics')
    total_orders = models.IntegerField(verbose_name='总订单数', default=0)
    completed_orders = models.IntegerField(verbose_name='完成订单数', default=0)
    cancelled_orders = models.IntegerField(verbose_name='取消订单数', default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='总金额', default=0)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0, verbose_name='平均评分')
    total_reviews = models.IntegerField(verbose_name='评价数', default=0)
    good_reviews = models.IntegerField(verbose_name='好评数(4-5星)', default=0)
    medium_reviews = models.IntegerField(verbose_name='中评数(3星)', default=0)
    bad_reviews = models.IntegerField(verbose_name='差评数(1-2星)', default=0)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'aunt_statistics'
        verbose_name = '阿姨统计'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.aunt.name} - 统计数据'

    def refresh(self):
        orders = Order.objects.filter(aunt=self.aunt)
        reviews = Review.objects.filter(aunt=self.aunt)
        
        self.total_orders = orders.count()
        self.completed_orders = orders.filter(status__in=['completed', 'archived']).count()
        self.cancelled_orders = orders.filter(status='cancelled').count()
        self.total_amount = orders.filter(status__in=['completed', 'archived']).aggregate(
            total=models.Sum('total_price')
        )['total'] or 0
        
        self.total_reviews = reviews.count()
        if self.total_reviews > 0:
            self.avg_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 5.0
            self.good_reviews = reviews.filter(rating__gte=4).count()
            self.medium_reviews = reviews.filter(rating=3).count()
            self.bad_reviews = reviews.filter(rating__lte=2).count()
        
        self.save()
