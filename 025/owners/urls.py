from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BuildingViewSet, HouseViewSet, OwnerViewSet

router = DefaultRouter()
router.register(r'buildings', BuildingViewSet)
router.register(r'houses', HouseViewSet)
router.register(r'owners', OwnerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
