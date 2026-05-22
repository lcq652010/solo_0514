from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.db.models import Q
from .models import UserProfile, StockAlertMessage, Permission
from .serializers import (
    UserSerializer, UserProfileSerializer, UserCreateSerializer,
    StockAlertMessageSerializer
)
from .permissions import UserManagePermission


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), UserManagePermission()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.query_params.get('role')
        keyword = self.request.query_params.get('keyword')
        
        if role:
            queryset = queryset.filter(role=role)
        if keyword:
            queryset = queryset.filter(
                Q(user__username__icontains=keyword) |
                Q(user__first_name__icontains=keyword) |
                Q(user__last_name__icontains=keyword)
            )
        return queryset.order_by('-created_at')

    @action(detail=False, methods=['get'])
    def me(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = self.get_serializer(profile)
        permissions = Permission.get_role_permissions(profile.role)
        return Response({
            'profile': serializer.data,
            'permissions': permissions
        })

    @action(detail=False, methods=['post'])
    def create_user(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            profile = UserProfile.objects.get(user=user)
            return Response(UserProfileSerializer(profile).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StockAlertMessageViewSet(viewsets.ModelViewSet):
    queryset = StockAlertMessage.objects.all()
    serializer_class = StockAlertMessageSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        queryset = super().get_queryset()
        is_read = self.request.query_params.get('is_read')
        alert_level = self.request.query_params.get('alert_level')
        product_name = self.request.query_params.get('product_name')
        
        if is_read is not None:
            queryset = queryset.filter(is_read=(is_read.lower() == 'true'))
        if alert_level:
            queryset = queryset.filter(alert_level=alert_level)
        if product_name:
            queryset = queryset.filter(
                Q(product__name__icontains=product_name) |
                Q(product__product_code__icontains=product_name)
            )
        return queryset.order_by('-created_at')

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        count = StockAlertMessage.objects.filter(is_read=False).count()
        return Response({'unread_count': count})

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        alert = self.get_object()
        alert.is_read = True
        alert.read_at = timezone.now()
        alert.save()
        return Response({'message': '已标记为已读'})

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        count = StockAlertMessage.objects.filter(is_read=False).update(
            is_read=True,
            read_at=timezone.now()
        )
        return Response({'message': f'已标记 {count} 条消息为已读'})


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': '用户名和密码不能为空'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        try:
            profile = UserProfile.objects.get(user=user)
            permissions = Permission.get_role_permissions(profile.role)
            return Response({
                'token': 'authenticated',
                'user': UserSerializer(user).data,
                'profile': UserProfileSerializer(profile).data,
                'permissions': permissions
            })
        except UserProfile.DoesNotExist:
            return Response(
                {'error': '用户档案不存在'},
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            {'error': '用户名或密码错误'},
            status=status.HTTP_401_UNAUTHORIZED
        )
