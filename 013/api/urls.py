from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'shops', views.ShopViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'riders', views.RiderViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'tracking', views.DeliveryTrackingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
