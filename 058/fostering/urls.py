from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PetViewSet, RoomViewSet, OrderViewSet, FeedingRecordViewSet

router = DefaultRouter()
router.register(r'pets', PetViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'feeding-records', FeedingRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
