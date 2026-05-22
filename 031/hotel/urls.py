from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RoomViewSet, GuestViewSet, OrderViewSet,
    CheckInView, CheckOutView, StatisticsView,
    UserViewSet, AuthView
)

router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'guests', GuestViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', AuthView.as_view(), name='auth'),
    path('check-in/', CheckInView.as_view(), name='check-in'),
    path('check-out/', CheckOutView.as_view(), name='check-out'),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
]
