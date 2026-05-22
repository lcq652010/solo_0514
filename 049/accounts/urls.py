from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, StockAlertMessageViewSet, user_login

router = DefaultRouter()
router.register(r'users', UserProfileViewSet)
router.register(r'stock-alerts', StockAlertMessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', user_login, name='user_login'),
]
