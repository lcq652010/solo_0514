from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django.db.models import Q
from datetime import date, timedelta, datetime
from django.contrib.auth import authenticate, login, logout
from .models import Package, Customer, Photographer, Appointment, Order, Settlement, PhotoSelection, UserProfile
from .serializers import (
    PackageSerializer, CustomerSerializer, PhotographerSerializer,
    AppointmentSerializer, OrderSerializer, SettlementSerializer,
    PhotoSelectionSerializer, UserProfileSerializer, UserRegisterSerializer, UserSerializer
)
from .permissions import IsAdmin, IsPhotographer, IsCustomer, IsOwnerOrAdmin, IsPhotographerOwnerOrAdmin, IsCustomerOwnerOrAdmin, get_user_role


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class AuthView(APIView):
    permission_classes = []

    @action(detail=False, methods=['post'])
    def post(self, request):
        action = request.query_params.get('action', 'login')
        
        if action == 'register':
            serializer = UserRegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response({
                    'message': '注册成功',
                    'user': UserSerializer(user).data
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif action == 'login':
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                profile = UserProfileSerializer(user.userprofile).data
                return Response({
                    'message': '登录成功',
                    'user': UserSerializer(user).data,
                    'profile': profile
                })
            return Response({'error': '用户名或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)
        
        elif action == 'logout':
            logout(request)
            return Response({'message': '退出成功'})
        
        return Response({'error': '无效的操作'}, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = user.userprofile
        return Response({
            'user': UserSerializer(user).data,
            'profile': UserProfileSerializer(profile).data
        })


class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all().order_by('-created_at')
    serializer_class = PackageSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name', None)
        is_active = self.request.query_params.get('is_active', None)
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        if is_active is not None:
            queryset = queryset.filter(is_active=(is_active.lower() == 'true'))
        
        return queryset

    @action(detail=False, methods=['get'])
    def active(self, request):
        active_packages = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_packages, many=True)
        return Response(serializer.data)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('-created_at')
    serializer_class = CustomerSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.query_params.get('keyword', None)
        role = get_user_role(self.request.user)
        
        if role == 'customer':
            queryset = queryset.filter(user=self.request.user)
        
        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword) |
                Q(phone__icontains=keyword) |
                Q(wechat__icontains=keyword)
            )
        
        return queryset

    @action(detail=False, methods=['get'])
    def search(self, request):
        keyword = request.query_params.get('keyword', '')
        if keyword:
            customers = self.queryset.filter(
                Q(name__icontains=keyword) |
                Q(phone__icontains=keyword) |
                Q(wechat__icontains=keyword)
            )
            serializer = self.get_serializer(customers, many=True)
            return Response(serializer.data)
        return Response([])


class PhotographerViewSet(viewsets.ModelViewSet):
    queryset = Photographer.objects.all().order_by('-created_at')
    serializer_class = PhotographerSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name', None)
        level = self.request.query_params.get('level', None)
        is_active = self.request.query_params.get('is_active', None)
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        if level:
            queryset = queryset.filter(level__icontains=level)
        if is_active is not None:
            queryset = queryset.filter(is_active=(is_active.lower() == 'true'))
        
        return queryset

    @action(detail=False, methods=['get'])
    def active(self, request):
        active_photographers = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_photographers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def schedule(self, request, pk=None):
        photographer = self.get_object()
        start_date = request.query_params.get('start_date', date.today())
        end_date = request.query_params.get('end_date', date.today() + timedelta(days=30))
        
        orders = Order.objects.filter(
            photographer=photographer,
            shoot_date__range=[start_date, end_date],
            status__in=['pending', 'shooting']
        ).values('id', 'order_number', 'shoot_date', 'shoot_time', 'status', 'customer__name')
        
        appointments = Appointment.objects.filter(
            photographer=photographer,
            appointment_date__range=[start_date, end_date],
            status='confirmed'
        ).values('id', 'appointment_date', 'appointment_time', 'customer__name')
        
        return Response({
            'photographer': photographer.name,
            'orders': list(orders),
            'appointments': list(appointments)
        })

    @action(detail=False, methods=['get'])
    def available(self, request):
        schedule_date = request.query_params.get('date', date.today())
        schedule_time = request.query_params.get('time', None)
        
        busy_photographers = Order.objects.filter(
            shoot_date=schedule_date,
            status__in=['pending', 'shooting']
        ).values_list('photographer_id', flat=True)
        
        if schedule_time:
            busy_photographers = Order.objects.filter(
                shoot_date=schedule_date,
                shoot_time=schedule_time,
                status__in=['pending', 'shooting']
            ).values_list('photographer_id', flat=True)
        
        available_photographers = self.queryset.filter(
            is_active=True
        ).exclude(id__in=busy_photographers)
        
        serializer = self.get_serializer(available_photographers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsPhotographer])
    def my_orders(self, request, pk=None):
        photographer = self.get_object()
        if photographer.user != request.user and not get_user_role(request.user) == 'admin':
            return Response({'error': '无权查看'}, status=status.HTTP_403_FORBIDDEN)
        
        status_filter = request.query_params.get('status', None)
        orders = Order.objects.filter(photographer=photographer)
        
        if status_filter:
            orders = orders.filter(status=status_filter)
        
        orders = orders.order_by('-created_at')
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = OrderSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all().order_by('-created_at')
    serializer_class = AppointmentSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.action in ['create']:
            return [IsCustomer()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()
        role = get_user_role(self.request.user)
        
        customer_name = self.request.query_params.get('customer_name', None)
        photographer_id = self.request.query_params.get('photographer_id', None)
        status = self.request.query_params.get('status', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if role == 'customer':
            try:
                customer = Customer.objects.get(user=self.request.user)
                queryset = queryset.filter(customer=customer)
            except Customer.DoesNotExist:
                queryset = queryset.none()
        elif role == 'photographer':
            try:
                photographer = Photographer.objects.get(user=self.request.user)
                queryset = queryset.filter(photographer=photographer)
            except Photographer.DoesNotExist:
                pass
        
        if customer_name:
            queryset = queryset.filter(customer__name__icontains=customer_name)
        if photographer_id:
            queryset = queryset.filter(photographer_id=photographer_id)
        if status:
            queryset = queryset.filter(status=status)
        if start_date:
            queryset = queryset.filter(appointment_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(appointment_date__lte=end_date)
        
        return queryset

    @action(detail=False, methods=['get'])
    def pending(self, request):
        pending_appointments = self.queryset.filter(status='pending')
        serializer = self.get_serializer(pending_appointments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = 'confirmed'
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = 'cancelled'
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.action in ['create']:
            return [IsCustomer()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()
        role = get_user_role(self.request.user)
        
        customer_name = self.request.query_params.get('customer_name', None)
        customer_id = self.request.query_params.get('customer_id', None)
        package_id = self.request.query_params.get('package_id', None)
        photographer_id = self.request.query_params.get('photographer_id', None)
        status = self.request.query_params.get('status', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        order_number = self.request.query_params.get('order_number', None)
        is_settled = self.request.query_params.get('is_settled', None)
        
        if role == 'customer':
            try:
                customer = Customer.objects.get(user=self.request.user)
                queryset = queryset.filter(customer=customer)
            except Customer.DoesNotExist:
                queryset = queryset.none()
        elif role == 'photographer':
            try:
                photographer = Photographer.objects.get(user=self.request.user)
                queryset = queryset.filter(photographer=photographer)
            except Photographer.DoesNotExist:
                pass
        
        if customer_name:
            queryset = queryset.filter(customer__name__icontains=customer_name)
        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
        if package_id:
            queryset = queryset.filter(package_id=package_id)
        if photographer_id:
            queryset = queryset.filter(photographer_id=photographer_id)
        if status:
            queryset = queryset.filter(status=status)
        if start_date:
            queryset = queryset.filter(shoot_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(shoot_date__lte=end_date)
        if order_number:
            queryset = queryset.filter(order_number__icontains=order_number)
        if is_settled is not None:
            queryset = queryset.filter(is_settled=(is_settled.lower() == 'true'))
        
        return queryset

    @action(detail=False, methods=['get'])
    def pending(self, request):
        orders = self.queryset.filter(status='pending')
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def shooting(self, request):
        orders = self.queryset.filter(status='shooting')
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def selected(self, request):
        orders = self.queryset.filter(status='selected')
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def completed(self, request):
        orders = self.queryset.filter(status='completed')
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsPhotographer])
    def start_shooting(self, request, pk=None):
        order = self.get_object()
        role = get_user_role(request.user)
        
        if role != 'admin' and order.photographer.user != request.user:
            return Response({'error': '只能操作自己的订单'}, status=status.HTTP_403_FORBIDDEN)
        
        order.start_shooting()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsPhotographer])
    def finish_shooting(self, request, pk=None):
        order = self.get_object()
        role = get_user_role(request.user)
        
        if role != 'admin' and order.photographer.user != request.user:
            return Response({'error': '只能操作自己的订单'}, status=status.HTTP_403_FORBIDDEN)
        
        order.finish_shooting()
        
        auto_settle = request.data.get('auto_settle', False)
        if auto_settle:
            order.auto_settle()
        
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        order = self.get_object()
        order.complete_order()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def auto_settle(self, request, pk=None):
        order = self.get_object()
        payment_method = request.data.get('payment_method', '线下支付')
        success = order.auto_settle(payment_method)
        if success:
            return Response({'message': '自动结算成功', 'order': OrderSerializer(order).data})
        return Response({'error': '结算失败，可能已结算或尾款为0'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def filter(self, request):
        orders = self.get_queryset()
        
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        keyword = request.query_params.get('keyword', '')
        if keyword:
            orders = self.queryset.filter(
                Q(order_number__icontains=keyword) |
                Q(customer__name__icontains=keyword)
            )
            serializer = self.get_serializer(orders, many=True)
            return Response(serializer.data)
        return Response([])

    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        role = get_user_role(request.user)
        orders = self.get_queryset()
        
        if role == 'customer':
            try:
                customer = Customer.objects.get(user=request.user)
                orders = orders.filter(customer=customer)
            except Customer.DoesNotExist:
                orders = orders.none()
        elif role == 'photographer':
            try:
                photographer = Photographer.objects.get(user=request.user)
                orders = orders.filter(photographer=photographer)
            except Photographer.DoesNotExist:
                pass
        
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)


class PhotoSelectionViewSet(viewsets.ModelViewSet):
    queryset = PhotoSelection.objects.all().order_by('-created_at')
    serializer_class = PhotoSelectionSerializer
    pagination_class = StandardPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        role = get_user_role(self.request.user)
        
        if role == 'customer':
            try:
                customer = Customer.objects.get(user=self.request.user)
                queryset = queryset.filter(order__customer=customer)
            except Customer.DoesNotExist:
                queryset = queryset.none()
        elif role == 'photographer':
            try:
                photographer = Photographer.objects.get(user=self.request.user)
                queryset = queryset.filter(order__photographer=photographer)
            except Photographer.DoesNotExist:
                pass
        
        order_number = self.request.query_params.get('order_number', None)
        is_completed = self.request.query_params.get('is_completed', None)
        
        if order_number:
            queryset = queryset.filter(order__order_number__icontains=order_number)
        if is_completed is not None:
            queryset = queryset.filter(is_completed=(is_completed.lower() == 'true'))
        
        return queryset

    @action(detail=True, methods=['post'])
    def complete_selection(self, request, pk=None):
        photo_selection = self.get_object()
        photo_selection.is_completed = True
        photo_selection.selected_at = datetime.now()
        photo_selection.selected_count = request.data.get('selected_count', photo_selection.selected_count)
        photo_selection.total_count = request.data.get('total_count', photo_selection.total_count)
        photo_selection.remark = request.data.get('remark', photo_selection.remark)
        photo_selection.save()
        
        photo_selection.order.status = 'selected'
        photo_selection.order.save()
        
        auto_settle = request.data.get('auto_settle', False)
        if auto_settle:
            photo_selection.order.auto_settle()
        
        serializer = self.get_serializer(photo_selection)
        return Response(serializer.data)


class SettlementViewSet(viewsets.ModelViewSet):
    queryset = Settlement.objects.all().order_by('-created_at')
    serializer_class = SettlementSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()
        role = get_user_role(self.request.user)
        
        if role == 'customer':
            try:
                customer = Customer.objects.get(user=self.request.user)
                queryset = queryset.filter(order__customer=customer)
            except Customer.DoesNotExist:
                queryset = queryset.none()
        elif role == 'photographer':
            try:
                photographer = Photographer.objects.get(user=self.request.user)
                queryset = queryset.filter(order__photographer=photographer)
            except Photographer.DoesNotExist:
                pass
        
        order_number = self.request.query_params.get('order_number', None)
        payment_method = self.request.query_params.get('payment_method', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if order_number:
            queryset = queryset.filter(order__order_number__icontains=order_number)
        if payment_method:
            queryset = queryset.filter(payment_method__icontains=payment_method)
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)
        
        return queryset

    def create(self, request, *args, **kwargs):
        order_id = request.data.get('order')
        try:
            order = Order.objects.get(id=order_id)
            if Settlement.objects.filter(order=order).exists():
                return Response(
                    {'error': '该订单已完成结算'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            balance_amount = order.remaining_amount
            if balance_amount < 0:
                return Response(
                    {'error': '尾款金额不能为负数'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            request.data['balance_amount'] = balance_amount
            return super().create(request, *args, **kwargs)
        except Order.DoesNotExist:
            return Response(
                {'error': '订单不存在'},
                status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats(request):
    role = get_user_role(request.user)
    
    if role == 'admin':
        total_orders = Order.objects.count()
        pending_orders = Order.objects.filter(status='pending').count()
        shooting_orders = Order.objects.filter(status='shooting').count()
        completed_orders = Order.objects.filter(status='completed').count()
        total_revenue = sum(order.total_amount for order in Order.objects.filter(is_settled=True))
        unsettled_count = Order.objects.filter(is_settled=False).count()
        photographers_count = Photographer.objects.filter(is_active=True).count()
        customers_count = Customer.objects.count()
        
        return Response({
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'shooting_orders': shooting_orders,
            'completed_orders': completed_orders,
            'total_revenue': total_revenue,
            'unsettled_count': unsettled_count,
            'photographers_count': photographers_count,
            'customers_count': customers_count
        })
    
    elif role == 'photographer':
        try:
            photographer = Photographer.objects.get(user=request.user)
            total_orders = Order.objects.filter(photographer=photographer).count()
            pending_orders = Order.objects.filter(photographer=photographer, status='pending').count()
            shooting_orders = Order.objects.filter(photographer=photographer, status='shooting').count()
            completed_orders = Order.objects.filter(photographer=photographer, status='completed').count()
            
            return Response({
                'total_orders': total_orders,
                'pending_orders': pending_orders,
                'shooting_orders': shooting_orders,
                'completed_orders': completed_orders
            })
        except Photographer.DoesNotExist:
            return Response({'error': '摄影师资料不存在'}, status=404)
    
    elif role == 'customer':
        try:
            customer = Customer.objects.get(user=request.user)
            total_orders = Order.objects.filter(customer=customer).count()
            pending_orders = Order.objects.filter(customer=customer, status='pending').count()
            completed_orders = Order.objects.filter(customer=customer, status='completed').count()
            
            return Response({
                'total_orders': total_orders,
                'pending_orders': pending_orders,
                'completed_orders': completed_orders
            })
        except Customer.DoesNotExist:
            return Response({'error': '客户资料不存在'}, status=404)
    
    return Response({'error': '无效的用户角色'}, status=403)
