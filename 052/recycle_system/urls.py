from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from recycle import views

router = DefaultRouter()
router.register(r'items', views.ItemViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'quality-checks', views.QualityCheckViewSet)
router.register(r'settlements', views.SettlementViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
