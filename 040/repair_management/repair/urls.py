from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'customers', views.CustomerViewSet)
router.register(r'devices', views.DeviceViewSet)
router.register(r'repair-orders', views.RepairOrderViewSet)
router.register(r'notifications', views.NotificationViewSet, basename='notification')
router.register(r'archived-orders', views.ArchivedOrderViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('current-user/', views.current_user, name='current-user'),
    path('dashboard-stats/', views.dashboard_stats, name='dashboard-stats'),
]
