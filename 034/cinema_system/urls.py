from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cinema.views import (
    MovieViewSet, HallViewSet, ScheduleViewSet, SeatViewSet, OrderViewSet,
    CheckTicketView, OrderStatisticsView, AuthView, LogoutView,
    UserViewSet, GroupViewSet, get_permissions
)

router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'halls', HallViewSet)
router.register(r'schedules', ScheduleViewSet)
router.register(r'seats', SeatViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/login/', AuthView.as_view(), name='login'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/auth/permissions/', get_permissions, name='get_permissions'),
    path('api/check-ticket/', CheckTicketView.as_view(), name='check-ticket'),
    path('api/order-statistics/', OrderStatisticsView.as_view(), name='order-statistics'),
]
