import django_filters
from django.db.models import Q
from .models import Enrollment, Order, Course, Video, Chapter, LearningProgress, UserProfile


class UserProfileFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(
        field_name='user__username',
        lookup_expr='icontains',
        label='用户名'
    )
    email = django_filters.CharFilter(
        field_name='user__email',
        lookup_expr='icontains',
        label='邮箱'
    )
    full_name = django_filters.CharFilter(
        method='filter_full_name',
        label='姓名'
    )
    role = django_filters.ChoiceFilter(
        choices=UserProfile.ROLE_CHOICES,
        label='角色'
    )

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'full_name', 'role']

    def filter_full_name(self, queryset, name, value):
        return queryset.filter(
            Q(user__first_name__icontains=value) |
            Q(user__last_name__icontains=value)
        )


class EnrollmentFilter(django_filters.FilterSet):
    course_name = django_filters.CharFilter(
        field_name='course__title',
        lookup_expr='icontains',
        label='课程名称'
    )
    course_id = django_filters.NumberFilter(
        field_name='course_id',
        label='课程ID'
    )
    student_name = django_filters.CharFilter(
        method='filter_student_name',
        label='学员姓名'
    )
    student_id = django_filters.NumberFilter(
        field_name='user_id',
        label='学员ID'
    )
    instructor_id = django_filters.NumberFilter(
        field_name='course__instructor_id',
        label='讲师ID'
    )
    instructor_name = django_filters.CharFilter(
        method='filter_instructor_name',
        label='讲师姓名'
    )
    status = django_filters.ChoiceFilter(
        choices=Enrollment.STATUS_CHOICES,
        label='学习状态'
    )
    enrolled_date_start = django_filters.DateFilter(
        field_name='enrolled_at',
        lookup_expr='date__gte',
        label='报名开始日期'
    )
    enrolled_date_end = django_filters.DateFilter(
        field_name='enrolled_at',
        lookup_expr='date__lte',
        label='报名结束日期'
    )
    progress_min = django_filters.NumberFilter(
        field_name='progress',
        lookup_expr='gte',
        label='最小进度(%)'
    )
    progress_max = django_filters.NumberFilter(
        field_name='progress',
        lookup_expr='lte',
        label='最大进度(%)'
    )
    completed_date_start = django_filters.DateFilter(
        field_name='completed_at',
        lookup_expr='date__gte',
        label='完成开始日期'
    )
    completed_date_end = django_filters.DateFilter(
        field_name='completed_at',
        lookup_expr='date__lte',
        label='完成结束日期'
    )
    keyword = django_filters.CharFilter(
        method='filter_keyword',
        label='关键词搜索'
    )

    class Meta:
        model = Enrollment
        fields = ['course_name', 'course_id', 'student_name', 'student_id', 
                  'instructor_id', 'instructor_name', 'status', 'progress_min', 'progress_max']

    def filter_student_name(self, queryset, name, value):
        return queryset.filter(
            Q(user__username__icontains=value) |
            Q(user__first_name__icontains=value) |
            Q(user__last_name__icontains=value)
        )

    def filter_instructor_name(self, queryset, name, value):
        return queryset.filter(
            Q(course__instructor__username__icontains=value) |
            Q(course__instructor__first_name__icontains=value) |
            Q(course__instructor__last_name__icontains=value)
        )

    def filter_keyword(self, queryset, name, value):
        return queryset.filter(
            Q(course__title__icontains=value) |
            Q(user__username__icontains=value) |
            Q(user__first_name__icontains=value) |
            Q(user__last_name__icontains=value)
        )


class OrderFilter(django_filters.FilterSet):
    course_name = django_filters.CharFilter(
        field_name='course__title',
        lookup_expr='icontains',
        label='课程名称'
    )
    course_id = django_filters.NumberFilter(
        field_name='course_id',
        label='课程ID'
    )
    student_name = django_filters.CharFilter(
        method='filter_student_name',
        label='学员姓名'
    )
    student_id = django_filters.NumberFilter(
        field_name='user_id',
        label='学员ID'
    )
    instructor_id = django_filters.NumberFilter(
        field_name='course__instructor_id',
        label='讲师ID'
    )
    instructor_name = django_filters.CharFilter(
        method='filter_instructor_name',
        label='讲师姓名'
    )
    status = django_filters.ChoiceFilter(
        choices=Order.STATUS_CHOICES,
        label='订单状态'
    )
    order_no = django_filters.CharFilter(
        lookup_expr='icontains',
        label='订单号'
    )
    price_min = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        label='最小金额'
    )
    price_max = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        label='最大金额'
    )
    order_date_start = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='下单开始时间'
    )
    order_date_end = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lte',
        label='下单结束时间'
    )
    paid_date_start = django_filters.DateTimeFilter(
        field_name='paid_at',
        lookup_expr='gte',
        label='支付开始时间'
    )
    paid_date_end = django_filters.DateTimeFilter(
        field_name='paid_at',
        lookup_expr='lte',
        label='支付结束时间'
    )
    keyword = django_filters.CharFilter(
        method='filter_keyword',
        label='关键词搜索'
    )

    class Meta:
        model = Order
        fields = ['course_name', 'course_id', 'student_name', 'student_id', 
                  'instructor_id', 'instructor_name', 'status', 'order_no']

    def filter_student_name(self, queryset, name, value):
        return queryset.filter(
            Q(user__username__icontains=value) |
            Q(user__first_name__icontains=value) |
            Q(user__last_name__icontains=value)
        )

    def filter_instructor_name(self, queryset, name, value):
        return queryset.filter(
            Q(course__instructor__username__icontains=value) |
            Q(course__instructor__first_name__icontains=value) |
            Q(course__instructor__last_name__icontains=value)
        )

    def filter_keyword(self, queryset, name, value):
        return queryset.filter(
            Q(order_no__icontains=value) |
            Q(course__title__icontains=value) |
            Q(user__username__icontains=value)
        )


class CourseFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr='icontains',
        label='课程名称'
    )
    instructor_name = django_filters.CharFilter(
        method='filter_instructor_name',
        label='讲师姓名'
    )
    instructor_id = django_filters.NumberFilter(
        field_name='instructor_id',
        label='讲师ID'
    )
    status = django_filters.ChoiceFilter(
        choices=Course.STATUS_CHOICES,
        label='课程状态'
    )
    price_min = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        label='最低价格'
    )
    price_max = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        label='最高价格'
    )
    students_min = django_filters.NumberFilter(
        field_name='students_count',
        lookup_expr='gte',
        label='最少学员数'
    )
    students_max = django_filters.NumberFilter(
        field_name='students_count',
        lookup_expr='lte',
        label='最多学员数'
    )
    created_date_start = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='date__gte',
        label='创建开始日期'
    )
    created_date_end = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='date__lte',
        label='创建结束日期'
    )
    keyword = django_filters.CharFilter(
        method='filter_keyword',
        label='关键词搜索'
    )

    class Meta:
        model = Course
        fields = ['title', 'instructor_name', 'instructor_id', 'status', 'price_min', 'price_max']

    def filter_instructor_name(self, queryset, name, value):
        return queryset.filter(
            Q(instructor__username__icontains=value) |
            Q(instructor__first_name__icontains=value) |
            Q(instructor__last_name__icontains=value)
        )

    def filter_keyword(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value) |
            Q(instructor__username__icontains=value)
        )


class LearningProgressFilter(django_filters.FilterSet):
    course_id = django_filters.NumberFilter(
        field_name='enrollment__course_id',
        label='课程ID'
    )
    course_name = django_filters.CharFilter(
        field_name='enrollment__course__title',
        lookup_expr='icontains',
        label='课程名称'
    )
    student_id = django_filters.NumberFilter(
        field_name='enrollment__user_id',
        label='学员ID'
    )
    student_name = django_filters.CharFilter(
        method='filter_student_name',
        label='学员姓名'
    )
    video_id = django_filters.NumberFilter(
        field_name='video_id',
        label='视频ID'
    )
    video_title = django_filters.CharFilter(
        field_name='video__title',
        lookup_expr='icontains',
        label='视频名称'
    )
    is_completed = django_filters.BooleanFilter(
        label='是否完成'
    )
    watch_date_start = django_filters.DateTimeFilter(
        field_name='last_watched_at',
        lookup_expr='gte',
        label='最后观看开始时间'
    )
    watch_date_end = django_filters.DateTimeFilter(
        field_name='last_watched_at',
        lookup_expr='lte',
        label='最后观看结束时间'
    )

    class Meta:
        model = LearningProgress
        fields = ['course_id', 'student_id', 'is_completed']

    def filter_student_name(self, queryset, name, value):
        return queryset.filter(
            Q(enrollment__user__username__icontains=value) |
            Q(enrollment__user__first_name__icontains=value) |
            Q(enrollment__user__last_name__icontains=value)
        )


class ChapterFilter(django_filters.FilterSet):
    course_id = django_filters.NumberFilter(
        field_name='course_id',
        label='课程ID'
    )
    course_name = django_filters.CharFilter(
        field_name='course__title',
        lookup_expr='icontains',
        label='课程名称'
    )
    title = django_filters.CharFilter(
        lookup_expr='icontains',
        label='章节名称'
    )

    class Meta:
        model = Chapter
        fields = ['course_id', 'course_name', 'title']


class VideoFilter(django_filters.FilterSet):
    course_id = django_filters.NumberFilter(
        field_name='chapter__course_id',
        label='课程ID'
    )
    chapter_id = django_filters.NumberFilter(
        field_name='chapter_id',
        label='章节ID'
    )
    title = django_filters.CharFilter(
        lookup_expr='icontains',
        label='视频名称'
    )
    duration_min = django_filters.NumberFilter(
        field_name='duration',
        lookup_expr='gte',
        label='最小时长(秒)'
    )
    duration_max = django_filters.NumberFilter(
        field_name='duration',
        lookup_expr='lte',
        label='最大时长(秒)'
    )

    class Meta:
        model = Video
        fields = ['course_id', 'chapter_id', 'title']
