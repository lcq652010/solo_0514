import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=200, verbose_name='影片名称')
    poster = models.URLField(max_length=500, blank=True, verbose_name='海报链接')
    description = models.TextField(verbose_name='影片简介')
    duration = models.IntegerField(verbose_name='时长(分钟)')
    genre = models.CharField(max_length=100, verbose_name='类型')
    director = models.CharField(max_length=100, verbose_name='导演')
    actors = models.TextField(verbose_name='主演')
    release_date = models.DateField(verbose_name='上映日期')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, verbose_name='评分')
    is_showing = models.BooleanField(default=True, verbose_name='是否上映')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'movie'
        verbose_name = '影片'
        verbose_name_plural = '影片'

    def __str__(self):
        return self.title

class Hall(models.Model):
    name = models.CharField(max_length=100, verbose_name='影厅名称')
    total_rows = models.IntegerField(verbose_name='总行数')
    total_cols = models.IntegerField(verbose_name='总列数')
    total_seats = models.IntegerField(verbose_name='总座位数')
    is_3d = models.BooleanField(default=False, verbose_name='是否3D厅')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'hall'
        verbose_name = '影厅'
        verbose_name_plural = '影厅'

    def __str__(self):
        return self.name

class Schedule(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='影片')
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, verbose_name='影厅')
    show_time = models.DateTimeField(verbose_name='放映时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='票价')
    is_active = models.BooleanField(default=True, verbose_name='是否有效')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'schedule'
        verbose_name = '排期'
        verbose_name_plural = '排期'

    def __str__(self):
        return f'{self.movie.title} - {self.hall.name} - {self.show_time}'

class Seat(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, verbose_name='影厅')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, verbose_name='排期', null=True, blank=True)
    row_number = models.IntegerField(verbose_name='行号')
    col_number = models.IntegerField(verbose_name='列号')
    seat_code = models.CharField(max_length=20, verbose_name='座位编号')
    is_available = models.BooleanField(default=True, verbose_name='是否可用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'seat'
        verbose_name = '座位'
        verbose_name_plural = '座位'
        unique_together = ['hall', 'schedule', 'row_number', 'col_number']

    def __str__(self):
        return f'{self.hall.name} - {self.seat_code}'

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', '待检票'),
        ('checked', '已检票'),
        ('completed', '已完结'),
        ('refunded', '已退票'),
    ]

    order_no = models.CharField(max_length=32, unique=True, verbose_name='订单号')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, verbose_name='排期')
    seats = models.ManyToManyField(Seat, verbose_name='座位')
    seat_codes = models.TextField(verbose_name='座位编号列表')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总价')
    customer_name = models.CharField(max_length=100, verbose_name='顾客姓名')
    customer_phone = models.CharField(max_length=20, verbose_name='顾客电话')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='订单状态')
    
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                               related_name='sold_orders', verbose_name='售票员')
    ticket_checked_at = models.DateTimeField(null=True, blank=True, verbose_name='检票时间')
    ticket_checked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                          related_name='checked_orders', verbose_name='检票员')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完结时间')
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                     related_name='completed_orders', verbose_name='完结操作人')
    refund_at = models.DateTimeField(null=True, blank=True, verbose_name='退票时间')
    refund_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                  related_name='refunded_orders', verbose_name='退票操作人')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'order'
        verbose_name = '订单'
        verbose_name_plural = '订单'

    def __str__(self):
        return self.order_no

    def save(self, *args, **kwargs):
        if not self.order_no:
            self.order_no = self.generate_order_no()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_order_no():
        date_str = timezone.now().strftime('%Y%m%d%H%M%S')
        random_str = str(uuid.uuid4().hex)[:8].upper()
        return f'TK{date_str}{random_str}'
