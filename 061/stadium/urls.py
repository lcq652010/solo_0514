from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'venue-types', views.VenueTypeViewSet)
router.register(r'venues', views.VenueViewSet)
router.register(r'bookings', views.BookingViewSet)
router.register(r'time-slots', views.TimeSlotViewSet)
router.register(r'payments', views.PaymentViewSet)
router.register(r'dashboard', views.DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
]
