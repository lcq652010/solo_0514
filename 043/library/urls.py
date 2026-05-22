from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, ReaderViewSet, BorrowViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'readers', ReaderViewSet, basename='reader')
router.register(r'borrows', BorrowViewSet, basename='borrow')

urlpatterns = [
    path('', include(router.urls)),
]
