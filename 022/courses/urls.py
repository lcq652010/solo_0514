from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    CourseViewSet, ChapterViewSet, VideoViewSet, OrderViewSet,
    EnrollmentViewSet, LearningProgressViewSet, RegisterView,
    UserInfoView, DashboardStatsView, role_based_filter_example
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'chapters', ChapterViewSet)
router.register(r'videos', VideoViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'progress', LearningProgressViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/user/', UserInfoView.as_view(), name='user_info'),
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard_stats'),
    path('admin/filter-example/', role_based_filter_example, name='filter_example'),
]
