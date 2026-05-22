from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'members', views.MemberViewSet)
router.register(r'purchase-orders', views.PurchaseOrderViewSet)
router.register(r'sales-orders', views.SalesOrderViewSet)
router.register(r'stock-logs', views.StockLogViewSet)
router.register(r'points-logs', views.PointsLogViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
