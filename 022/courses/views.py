from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.db.models import Q, Count, Sum
from django.db import transaction
from .models import Course, Chapter, Video, Order, Enrollment, LearningProgress, UserProfile
from .serializers import (
    CourseSerializer, CourseListSerializer, ChapterSerializer, VideoSerializer,
    OrderSerializer, EnrollmentSerializer, LearningProgressSerializer,
    ChapterProgressSerializer, UserSerializer, UserRegisterSerializer
)
from .filters import (
    EnrollmentFilter, OrderFilter, CourseFilter, 
    LearningProgressFilter, ChapterFilter, VideoFilter, UserProfileFilter
)
from .permissions import (
    IsStudent, IsInstructor, IsAdmin, IsInstructorOrAdmin,
    IsCourseInstructor, IsOwnOrder, IsOwnEnrollment, IsEnrolledStudent
)


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'code': 200,
                'message': '注册成功',
                'data': {
                    'user': UserSerializer(user).data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            'code': 400,
            'message': '注册失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardPagination
    filterset_class = CourseFilter
    ordering_fields = ['created_at', 'price', 'students_count', 'title']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        elif self.action in ['update', 'partial_update', 'destroy', 'publish']:
            return [IsCourseInstructor()]
        return [IsInstructorOrAdmin()]

    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        return CourseSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'profile') and user.profile.is_instructor:
            if not user.profile.is_admin:
                queryset = queryset.filter(instructor=user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'code': 400,
                'message': '数据校验失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response({
            'code': 200,
            'message': '课程创建成功',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsCourseInstructor])
    def publish(self, request, pk=None):
        course = self.get_object()
        course.status = 'published'
        course.save()
        return Response({
            'code': 200,
            'message': '课程已上架',
            'data': CourseSerializer(course).data
        })

    @action(detail=True, methods=['post'], permission_classes=[IsCourseInstructor])
    def offline(self, request, pk=None):
        course = self.get_object()
        course.status = 'offline'
        course.save()
        return Response({
            'code': 200,
            'message': '课程已下架',
            'data': CourseSerializer(course).data
        })

    @action(detail=True, methods=['get'], permission_classes=[IsEnrolledStudent | IsCourseInstructor])
    def chapters_with_progress(self, request, pk=None):
        course = self.get_object()
        enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
        if not enrollment and not (hasattr(request.user, 'profile') and request.user.profile.is_instructor and course.instructor == request.user):
            return Response({
                'code': 403,
                'message': '未报名该课程'
            }, status=status.HTTP_403_FORBIDDEN)
        chapters = course.chapters.all()
        serializer = ChapterProgressSerializer(
            chapters,
            many=True,
            context={'enrollment_id': enrollment.id if enrollment else None}
        )
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'enrollment_id': enrollment.id if enrollment else None,
                'progress': enrollment.progress if enrollment else 0,
                'status': enrollment.get_status_display() if enrollment else None,
                'chapters': serializer.data
            }
        })


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    pagination_class = StandardPagination
    filterset_class = ChapterFilter
    permission_classes = [IsInstructorOrAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'profile') and user.profile.is_instructor and not user.profile.is_admin:
            queryset = queryset.filter(course__instructor=user)
        return queryset


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    pagination_class = StandardPagination
    filterset_class = VideoFilter
    permission_classes = [IsInstructorOrAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'profile') and user.profile.is_instructor and not user.profile.is_admin:
            queryset = queryset.filter(chapter__course__instructor=user)
        return queryset


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = StandardPagination
    filterset_class = OrderFilter
    ordering_fields = ['created_at', 'price', 'paid_at']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['create']:
            return [IsStudent()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if hasattr(user, 'profile') and user.profile.is_admin:
            return queryset
        elif hasattr(user, 'profile') and user.profile.is_instructor:
            return queryset.filter(course__instructor=user)
        return queryset.filter(user=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'code': 400,
                'message': '下单失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response({
            'code': 200,
            'message': '订单创建成功',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsOwnOrder])
    def pay(self, request, pk=None):
        order = self.get_object()
        if order.status != 'pending':
            return Response({
                'code': 400,
                'message': '订单状态错误，当前状态无法支付'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if order.price < 0:
            return Response({
                'code': 400,
                'message': '订单金额异常'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            order.mark_as_paid()
        return Response({
            'code': 200,
            'message': '支付成功',
            'data': OrderSerializer(order).data
        })

    @action(detail=True, methods=['post'], permission_classes=[IsOwnOrder])
    def refund(self, request, pk=None):
        order = self.get_object()
        if order.status != 'paid':
            return Response({
                'code': 400,
                'message': '只有已支付订单可以退款'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            order.status = 'refunded'
            order.save()
            enrollment = Enrollment.objects.filter(order=order).first()
            if enrollment:
                enrollment.status = 'refunded'
                enrollment.save()
        return Response({
            'code': 200,
            'message': '退款成功',
            'data': OrderSerializer(order).data
        })

    @action(detail=True, methods=['post'], permission_classes=[IsOwnOrder])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status != 'pending':
            return Response({
                'code': 400,
                'message': '只有待支付订单可以取消'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'cancelled'
        order.save()
        return Response({
            'code': 200,
            'message': '订单已取消',
            'data': OrderSerializer(order).data
        })


class EnrollmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    pagination_class = StandardPagination
    filterset_class = EnrollmentFilter
    ordering_fields = ['enrolled_at', 'progress', 'completed_at']
    ordering = ['-enrolled_at']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if hasattr(user, 'profile') and user.profile.is_admin:
            return queryset
        elif hasattr(user, 'profile') and user.profile.is_instructor:
            return queryset.filter(course__instructor=user)
        return queryset.filter(user=user)


class LearningProgressViewSet(viewsets.ModelViewSet):
    queryset = LearningProgress.objects.all()
    serializer_class = LearningProgressSerializer
    pagination_class = StandardPagination
    filterset_class = LearningProgressFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if hasattr(user, 'profile') and user.profile.is_admin:
            return queryset
        elif hasattr(user, 'profile') and user.profile.is_instructor:
            return queryset.filter(enrollment__course__instructor=user)
        return queryset.filter(enrollment__user=user)

    @action(detail=False, methods=['post'], permission_classes=[IsStudent])
    def update_progress(self, request):
        enrollment_id = request.data.get('enrollment_id')
        video_id = request.data.get('video_id')
        last_position = request.data.get('last_position', 0)
        is_completed = request.data.get('is_completed', False)

        if not enrollment_id:
            return Response({
                'code': 400,
                'message': '报名记录ID不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)
        if not video_id:
            return Response({
                'code': 400,
                'message': '视频ID不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)
        if last_position < 0:
            return Response({
                'code': 400,
                'message': '观看位置不能为负数'
            }, status=status.HTTP_400_BAD_REQUEST)

        enrollment = Enrollment.objects.filter(id=enrollment_id, user=request.user).first()
        if not enrollment:
            return Response({
                'code': 403,
                'message': '报名记录不存在或无权限'
            }, status=status.HTTP_403_FORBIDDEN)

        with transaction.atomic():
            progress, created = LearningProgress.objects.update_or_create(
                enrollment=enrollment,
                video_id=video_id,
                defaults={
                    'last_position': last_position,
                    'is_completed': is_completed,
                    'watch_time': last_position
                }
            )
        return Response({
            'code': 200,
            'message': '进度更新成功',
            'data': LearningProgressSerializer(progress).data
        })


class UserInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'user': UserSerializer(request.user).data,
                'role': profile.role,
                'role_display': profile.get_role_display(),
                'avatar': profile.avatar,
                'phone': profile.phone,
                'bio': profile.bio
            }
        })

    def put(self, request):
        profile = UserProfile.objects.get(user=request.user)
        profile.avatar = request.data.get('avatar', profile.avatar)
        profile.phone = request.data.get('phone', profile.phone)
        profile.bio = request.data.get('bio', profile.bio)
        profile.save()
        return Response({
            'code': 200,
            'message': '更新成功',
            'data': {
                'user': UserSerializer(request.user).data,
                'role': profile.role,
                'role_display': profile.get_role_display(),
                'avatar': profile.avatar,
                'phone': profile.phone,
                'bio': profile.bio
            }
        })


class DashboardStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        enrollments = Enrollment.objects.filter(user=user)
        orders = Order.objects.filter(user=user)
        
        total_amount = sum(order.price for order in orders.filter(status='paid'))
        
        stats = {
            'total_courses': enrollments.count(),
            'learning_courses': enrollments.filter(status='learning').count(),
            'completed_courses': enrollments.filter(status='completed').count(),
            'not_started_courses': enrollments.filter(status='not_started').count(),
            'total_orders': orders.count(),
            'paid_orders': orders.filter(status='paid').count(),
            'pending_orders': orders.filter(status='pending').count(),
            'total_amount': float(total_amount),
            'total_watch_time': enrollments.aggregate(Sum('total_watch_time'))['total_watch_time__sum'] or 0
        }
        
        if hasattr(user, 'profile') and user.profile.is_instructor:
            taught_courses = Course.objects.filter(instructor=user)
            student_enrollments = Enrollment.objects.filter(course__instructor=user)
            student_orders = Order.objects.filter(course__instructor=user, status='paid')
            
            stats.update({
                'taught_courses_count': taught_courses.count(),
                'published_courses': taught_courses.filter(status='published').count(),
                'total_students': student_enrollments.values('user').distinct().count(),
                'total_revenue': float(sum(order.price for order in student_orders)),
                'completed_enrollments': student_enrollments.filter(status='completed').count()
            })
        
        if hasattr(user, 'profile') and user.profile.is_admin:
            stats.update({
                'all_courses_count': Course.objects.count(),
                'all_users_count': User.objects.count(),
                'all_orders_count': Order.objects.count(),
                'all_enrollments_count': Enrollment.objects.count(),
                'total_platform_revenue': float(Order.objects.filter(status='paid').aggregate(Sum('price'))['price__sum'] or 0)
            })
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': stats
        })


@api_view(['GET'])
@permission_classes([IsAdmin])
def role_based_filter_example(request):
    course_id = request.query_params.get('course_id')
    student_id = request.query_params.get('student_id')
    status = request.query_params.get('status')
    
    queryset = Enrollment.objects.all()
    
    if course_id:
        queryset = queryset.filter(course_id=course_id)
    if student_id:
        queryset = queryset.filter(user_id=student_id)
    if status:
        queryset = queryset.filter(status=status)
    
    result = list(queryset.values(
        'id', 'course__title', 'user__username', 'status', 
        'progress', 'enrolled_at', 'completed_at'
    ))
    
    return Response({
        'code': 200,
        'message': '筛选成功',
        'count': len(result),
        'data': result
    })
