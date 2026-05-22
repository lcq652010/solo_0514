from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
import random
import string


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('student', '学员'),
        ('instructor', '讲师'),
        ('admin', '管理员'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='用户')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student', verbose_name='角色')
    avatar = models.URLField(max_length=500, blank=True, verbose_name='头像')
    phone = models.CharField(max_length=20, blank=True, verbose_name='手机号')
    bio = models.TextField(blank=True, verbose_name='个人简介')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}'

    @property
    def is_student(self):
        return self.role == 'student'

    @property
    def is_instructor(self):
        return self.role == 'instructor'

    @property
    def is_admin(self):
        return self.role == 'admin'


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


from django.db.models.signals import post_save
post_save.connect(create_user_profile, sender=User)


class Course(models.Model):
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已上架'),
        ('offline', '已下架'),
    ]

    title = models.CharField(max_length=200, verbose_name='课程标题')
    description = models.TextField(verbose_name='课程描述')
    cover = models.URLField(max_length=500, blank=True, verbose_name='封面图片')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='原价')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taught_courses', verbose_name='讲师')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='状态')
    total_duration = models.IntegerField(default=0, verbose_name='总时长(秒)')
    students_count = models.IntegerField(default=0, verbose_name='学员数量')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters', verbose_name='所属课程')
    title = models.CharField(max_length=200, verbose_name='章节标题')
    order = models.IntegerField(default=0, verbose_name='排序')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.course.title} - {self.title}'


class Video(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='videos', verbose_name='所属章节')
    title = models.CharField(max_length=200, verbose_name='视频标题')
    video_url = models.URLField(max_length=500, verbose_name='视频地址')
    duration = models.IntegerField(default=0, verbose_name='时长(秒)')
    order = models.IntegerField(default=0, verbose_name='排序')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


def generate_order_no():
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f'ORD{timestamp}{random_str}'


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('refunded', '已退款'),
        ('cancelled', '已取消'),
    ]

    order_no = models.CharField(max_length=32, default=generate_order_no, unique=True, verbose_name='订单号')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='用户')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='orders', verbose_name='课程')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='购买价格')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='订单状态')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.order_no

    def mark_as_paid(self):
        self.status = 'paid'
        self.paid_at = timezone.now()
        self.course.students_count += 1
        self.course.save()
        self.save()
        Enrollment.objects.get_or_create(
            user=self.user,
            course=self.course,
            defaults={'order': self}
        )


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('not_started', '未开始'),
        ('learning', '学习中'),
        ('completed', '已完结'),
        ('refunded', '已退款'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments', verbose_name='用户')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments', verbose_name='课程')
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='关联订单')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started', verbose_name='学习状态')
    progress = models.FloatField(default=0.0, verbose_name='学习进度(%)')
    total_watch_time = models.IntegerField(default=0, verbose_name='总观看时长(秒)')
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name='报名时间')
    last_watched_at = models.DateTimeField(null=True, blank=True, verbose_name='最后观看时间')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')

    class Meta:
        verbose_name = '报名记录'
        verbose_name_plural = verbose_name
        unique_together = ['user', 'course']
        ordering = ['-enrolled_at']

    def __str__(self):
        return f'{self.user.username} - {self.course.title}'

    def calculate_progress(self):
        total_videos = Video.objects.filter(chapter__course=self.course).count()
        if total_videos == 0:
            return 0.0, 0
        watched_videos = LearningProgress.objects.filter(
            enrollment=self,
            is_completed=True
        ).count()
        progress = round((watched_videos / total_videos) * 100, 2)
        return progress, watched_videos, total_videos

    def update_progress(self, auto_complete=True):
        progress, watched_videos, total_videos = self.calculate_progress()
        self.progress = progress
        
        if auto_complete and progress >= 100 and self.status != 'completed':
            self.status = 'completed'
            self.completed_at = timezone.now()
            self.trigger_course_completion()
        elif progress > 0 and self.status == 'not_started':
            self.status = 'learning'
        elif progress < 100 and self.status == 'completed':
            self.status = 'learning'
            self.completed_at = None
            
        self.save()
        return progress

    def trigger_course_completion(self):
        from django.db.models.signals import post_save
        post_save.send(sender=self.__class__, instance=self, created=False)

    def mark_as_completed(self):
        self.progress = 100.0
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()


class LearningProgress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='progresses', verbose_name='报名记录')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='progresses', verbose_name='视频')
    watch_time = models.IntegerField(default=0, verbose_name='观看时长(秒)')
    last_position = models.IntegerField(default=0, verbose_name='最后观看位置(秒)')
    is_completed = models.BooleanField(default=False, verbose_name='是否完成')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    last_watched_at = models.DateTimeField(auto_now=True, verbose_name='最后观看时间')
    watch_count = models.IntegerField(default=0, verbose_name='观看次数')

    class Meta:
        verbose_name = '学习进度'
        verbose_name_plural = verbose_name
        unique_together = ['enrollment', 'video']

    def __str__(self):
        return f'{self.enrollment.user.username} - {self.video.title}'

    def auto_mark_complete(self, threshold=0.9):
        if self.video.duration > 0 and self.last_position >= self.video.duration * threshold:
            if not self.is_completed:
                self.is_completed = True
                self.completed_at = timezone.now()
            return True
        return False

    def save(self, *args, update_fields=None, **kwargs):
        is_new = self.pk is None
        
        if is_new:
            self.watch_count = 1
        else:
            self.watch_count += 1
        
        self.auto_mark_complete()
        
        super().save(*args, update_fields=update_fields, **kwargs)
        
        self.enrollment.last_watched_at = timezone.now()
        self.enrollment.total_watch_time += 5
        self.enrollment.save(update_fields=['last_watched_at', 'total_watch_time'])
        self.enrollment.update_progress()
