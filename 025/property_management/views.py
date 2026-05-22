from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .serializers import UserSerializer, LoginSerializer
from .utils import get_user_role


class AuthViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'], permission_classes=[])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            user_data = UserSerializer(user).data
            user_data['role'] = get_user_role(user)
            return Response({
                'token': token.key,
                'user': user_data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except:
            pass
        return Response({'message': '登出成功'})

    @action(detail=False, methods=['get'])
    def current_user(self, request):
        user_data = UserSerializer(request.user).data
        user_data['role'] = get_user_role(request.user)
        return Response(user_data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.request.query_params.get('username')
        email = self.request.query_params.get('email')
        is_staff = self.request.query_params.get('is_staff')
        is_active = self.request.query_params.get('is_active')

        if username:
            queryset = queryset.filter(username__contains=username)
        if email:
            queryset = queryset.filter(email__contains=email)
        if is_staff is not None:
            queryset = queryset.filter(is_staff=(is_staff == 'true'))
        if is_active is not None:
            queryset = queryset.filter(is_active=(is_active == 'true'))
        return queryset
