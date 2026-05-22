from django.contrib import admin
from django.db.models import Count, Sum
from .models import Course, Chapter, Video, Order, Enrollment, LearningProgress, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role_display', 'phone', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    raw_id_fields = ['user']
    readonly_fields = ['created_at', 'updated_at']

    def role_display(self, obj):
        return obj.get_role_display()
    role_display.short_description = '角色'


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'price', 'original_price', 'status', 'students_count', 'total_duration', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description', 'instructor__username', 'instructor__email']
    raw_id_fields = ['instructor']
    readonly_fields = ['students_count', 'created_at', 'updated_at']
    list_per_page = 20


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'video_count', 'created_at']
    list_filter = ['course', 'created_at']
    search_fields = ['title', 'course__title']
    raw_id_fields = ['course']
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(video_count=Count('videos'))

    def video_count(self, obj):
        return obj.video_count
    video_count.short_description = '视频数量'


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'chapter', 'course_name', 'duration', 'order', 'created_at']
    list_filter = ['chapter__course', 'created_at']
    search_fields = ['title', 'chapter__title', 'chapter__course__title']
    raw_id_fields = ['chapter']
    list_per_page = 20

    def course_name(self, obj):
        return obj.chapter.course.title
    course_name.short_description = '课程'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_no', 'user', 'course', 'price', 'status', 'created_at', 'paid_at']
    list_filter = ['status', 'created_at', 'paid_at']
    search_fields = ['order_no', 'user__username', 'user__email', 'course__title']
    readonly_fields = ['order_no', 'created_at', 'updated_at', 'paid_at']
    raw_id_fields = ['user', 'course']
    list_per_page = 20
    date_hierarchy = 'created_at'


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'instructor_name', 'status_display', 'progress_display', 'total_watch_time', 'enrolled_at', 'last_watched_at']
    list_filter = ['status', 'enrolled_at', 'last_watched_at']
    search_fields = ['user__username', 'user__email', 'course__title', 'course__instructor__username']
    readonly_fields = ['enrolled_at', 'last_watched_at', 'completed_at']
    raw_id_fields = ['user', 'course', 'order']
    list_per_page = 20
    date_hierarchy = 'enrolled_at'

    def status_display(self, obj):
        return obj.get_status_display()
    status_display.short_description = '学习状态'

    def progress_display(self, obj):
        return f'{obj.progress}%'
    progress_display.short_description = '学习进度'

    def instructor_name(self, obj):
        return obj.course.instructor.username
    instructor_name.short_description = '讲师'


@admin.register(LearningProgress)
class LearningProgressAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'course_name', 'video', 'last_position_display', 'is_completed', 'watch_count', 'watch_time_display', 'last_watched_at']
    list_filter = ['is_completed', 'last_watched_at']
    search_fields = ['enrollment__user__username', 'enrollment__course__title', 'video__title']
    readonly_fields = ['last_watched_at']
    raw_id_fields = ['enrollment', 'video']
    list_per_page = 20

    def user_name(self, obj):
        return obj.enrollment.user.username
    user_name.short_description = '学员'

    def course_name(self, obj):
        return obj.enrollment.course.title
    course_name.short_description = '课程'

    def watch_time_display(self, obj):
        if obj.watch_time >= 3600:
            return f'{obj.watch_time // 3600}h {(obj.watch_time % 3600) // 60}m'
        elif obj.watch_time >= 60:
            return f'{obj.watch_time // 60}m {obj.watch_time % 60}s'
        return f'{obj.watch_time}s'
    watch_time_display.short_description = '观看时长'

    def last_position_display(self, obj):
        if obj.video.duration > 0:
            percent = (obj.last_position / obj.video.duration) * 100
            return f'{obj.last_position}s ({percent:.1f}%)'
        return f'{obj.last_position}s'
    last_position_display.short_description = '观看位置'
