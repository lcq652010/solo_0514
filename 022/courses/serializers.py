from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from .models import Course, Chapter, Video, Order, Enrollment, LearningProgress


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'
        extra_kwargs = {
            'title': {'required': True, 'allow_blank': False},
            'video_url': {'required': True, 'allow_blank': False},
            'chapter': {'required': True},
        }

    def validate_duration(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError('视频时长不能为负数')
        return value

    def validate_order(self, value):
        if value < 0:
            raise serializers.ValidationError('排序值不能为负数')
        return value


class ChapterSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = '__all__'
        extra_kwargs = {
            'title': {'required': True, 'allow_blank': False},
            'course': {'required': True},
        }

    def validate_order(self, value):
        if value < 0:
            raise serializers.ValidationError('排序值不能为负数')
        return value


class CourseSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['instructor', 'students_count', 'total_duration']
        extra_kwargs = {
            'title': {'required': True, 'allow_blank': False},
            'description': {'required': True, 'allow_blank': False},
            'price': {'required': True},
        }

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError('课程价格不能为负数')
        return value

    def validate_original_price(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError('原价不能为负数')
        return value

    def create(self, validated_data):
        validated_data['instructor'] = self.context['request'].user
        return super().create(validated_data)


class CourseListSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'cover', 'price', 'original_price', 'instructor', 'students_count', 'status', 'created_at']


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    course = CourseListSerializer(read_only=True)
    course_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['order_no', 'user', 'price', 'status', 'paid_at', 'created_at', 'updated_at']

    def validate_course_id(self, value):
        try:
            course = Course.objects.get(id=value)
        except Course.DoesNotExist:
            raise serializers.ValidationError('课程不存在')
        
        if course.status != 'published':
            raise serializers.ValidationError('该课程未上架，无法购买')
        
        return value

    def validate(self, attrs):
        user = self.context['request'].user
        course_id = attrs.get('course_id')
        
        existing_enrollment = Enrollment.objects.filter(
            user=user,
            course_id=course_id,
            status__in=['not_started', 'learning', 'completed']
        ).first()
        
        if existing_enrollment:
            raise serializers.ValidationError('您已购买该课程，请勿重复购买')
        
        existing_pending_order = Order.objects.filter(
            user=user,
            course_id=course_id,
            status='pending'
        ).first()
        
        if existing_pending_order:
            raise serializers.ValidationError(f'您已有待支付的订单，订单号：{existing_pending_order.order_no}')
        
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        course_id = validated_data.pop('course_id')
        course = Course.objects.get(id=course_id)
        validated_data['user'] = self.context['request'].user
        validated_data['course'] = course
        validated_data['price'] = course.price
        
        if course.price < 0:
            raise serializers.ValidationError('课程价格异常，请联系管理员')
        
        return super().create(validated_data)


class EnrollmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    student_name = serializers.CharField(source='user.username', read_only=True)
    student_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = '__all__'

    def get_student_full_name(self, obj):
        if obj.user.first_name or obj.user.last_name:
            return f"{obj.user.first_name}{obj.user.last_name}"
        return obj.user.username


class LearningProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningProgress
        fields = '__all__'
        read_only_fields = ['enrollment']
        extra_kwargs = {
            'video': {'required': True},
        }

    def validate_last_position(self, value):
        if value < 0:
            raise serializers.ValidationError('观看位置不能为负数')
        return value

    def validate_watch_time(self, value):
        if value < 0:
            raise serializers.ValidationError('观看时长不能为负数')
        return value

    def create(self, validated_data):
        enrollment_id = self.context['request'].data.get('enrollment_id')
        if not enrollment_id:
            raise serializers.ValidationError('报名记录ID不能为空')
        try:
            enrollment = Enrollment.objects.get(id=enrollment_id)
        except Enrollment.DoesNotExist:
            raise serializers.ValidationError('报名记录不存在')
        validated_data['enrollment'] = enrollment
        return super().create(validated_data)


class VideoProgressSerializer(serializers.ModelSerializer):
    is_watched = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'title', 'duration', 'order', 'is_watched', 'progress', 'video_url']

    def get_is_watched(self, obj):
        enrollment_id = self.context.get('enrollment_id')
        if enrollment_id:
            return LearningProgress.objects.filter(
                enrollment_id=enrollment_id,
                video=obj,
                is_completed=True
            ).exists()
        return False

    def get_progress(self, obj):
        enrollment_id = self.context.get('enrollment_id')
        if enrollment_id:
            progress = LearningProgress.objects.filter(
                enrollment_id=enrollment_id,
                video=obj
            ).first()
            if progress:
                return progress.last_position
        return 0


class ChapterProgressSerializer(serializers.ModelSerializer):
    videos = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = ['id', 'title', 'order', 'videos']

    def get_videos(self, obj):
        enrollment_id = self.context.get('enrollment_id')
        videos = obj.videos.all()
        return VideoProgressSerializer(videos, many=True, context={'enrollment_id': enrollment_id}).data


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6, required=True)
    password_confirm = serializers.CharField(write_only=True, min_length=6, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
        extra_kwargs = {
            'username': {'required': True, 'allow_blank': False},
            'email': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': '两次输入的密码不一致'})
        
        if User.objects.filter(email=attrs.get('email', '')).exists():
            raise serializers.ValidationError({'email': '该邮箱已被注册'})
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
