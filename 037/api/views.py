from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from django.utils import timezone
from .models import Category, Product, Order, OrderItem, User
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    OrderSerializer,
    OrderCreateSerializer,
    OrderPaySerializer,
    OrderStatusUpdateSerializer,
    OrderVerifySerializer,
    UserSerializer,
    UserCreateSerializer
)
from .permissions import (
    CategoryPermission,
    ProductPermission,
    CashierPermission,
    MakerPermission,
    IsAdmin
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('-created_at')
    serializer_class = CategorySerializer
    permission_classes = [CategoryPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [ProductPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        name = self.request.query_params.get('name')
        category_id = self.request.query_params.get('category')
        is_available = self.request.query_params.get('is_available')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        has_stock = self.request.query_params.get('has_stock')
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if is_available is not None:
            queryset = queryset.filter(is_available=(is_available.lower() == 'true'))
        if min_price:
            try:
                queryset = queryset.filter(price__gte=float(min_price))
            except (ValueError, TypeError):
                pass
        if max_price:
            try:
                queryset = queryset.filter(price__lte=float(max_price))
            except (ValueError, TypeError):
                pass
        if has_stock and has_stock.lower() == 'true':
            queryset = queryset.filter(stock__gt=0)
        
        return queryset


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.query_params.get('role')
        username = self.request.query_params.get('username')
        
        if role:
            queryset = queryset.filter(role=role)
        if username:
            queryset = queryset.filter(username__icontains=username)
        
        return queryset


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action in ['create', 'pay', 'verify']:
            return [CashierPermission()]
        elif self.action in ['update_status', 'queue', 'notifications', 'mark_notified']:
            return [MakerPermission()]
        else:
            return [IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        order_no = self.request.query_params.get('order_no')
        status_filter = self.request.query_params.get('status')
        is_paid = self.request.query_params.get('is_paid')
        customer_name = self.request.query_params.get('customer_name')
        customer_phone = self.request.query_params.get('customer_phone')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        min_amount = self.request.query_params.get('min_amount')
        max_amount = self.request.query_params.get('max_amount')
        product_name = self.request.query_params.get('product_name')
        product_id = self.request.query_params.get('product_id')
        is_archived = self.request.query_params.get('is_archived')
        is_notified = self.request.query_params.get('is_notified')
        
        if product_name:
            queryset = queryset.filter(
                items__product__name__icontains=product_name
            ).distinct()
        if product_id:
            queryset = queryset.filter(
                items__product_id=product_id
            ).distinct()
        if order_no:
            queryset = queryset.filter(order_no__icontains=order_no)
        if status_filter:
            status_list = status_filter.split(',')
            if len(status_list) > 1:
                queryset = queryset.filter(status__in=status_list)
            else:
                queryset = queryset.filter(status=status_filter)
        if is_paid is not None:
            queryset = queryset.filter(is_paid=(is_paid.lower() == 'true'))
        if customer_name:
            queryset = queryset.filter(customer_name__icontains=customer_name)
        if customer_phone:
            queryset = queryset.filter(customer_phone__icontains=customer_phone)
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)
        if min_amount:
            try:
                queryset = queryset.filter(total_amount__gte=float(min_amount))
            except (ValueError, TypeError):
                pass
        if max_amount:
            try:
                queryset = queryset.filter(total_amount__lte=float(max_amount))
            except (ValueError, TypeError):
                pass
        if is_archived is not None:
            queryset = queryset.filter(is_archived=(is_archived.lower() == 'true'))
        if is_notified is not None:
            queryset = queryset.filter(is_notified=(is_notified.lower() == 'true'))
        
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        output_serializer = OrderSerializer(order)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], serializer_class=OrderPaySerializer)
    def pay(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        output_serializer = OrderSerializer(order)
        return Response(output_serializer.data)

    @action(detail=True, methods=['post'], serializer_class=OrderStatusUpdateSerializer)
    def update_status(self, request, pk=None):
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        output_serializer = OrderSerializer(order)
        return Response(output_serializer.data)

    @action(detail=False, methods=['post'], serializer_class=OrderVerifySerializer)
    def verify(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        output_serializer = OrderSerializer(order)
        return Response(output_serializer.data)

    @action(detail=False, methods=['get'])
    def queue(self, request):
        orders = Order.objects.filter(
            status__in=['pending', 'making', 'ready'],
            is_paid=True,
            is_archived=False
        ).order_by('created_at')
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def notifications(self, request):
        orders = Order.objects.filter(
            status='ready',
            is_paid=True,
            is_archived=False,
            is_notified=False
        ).order_by('created_at')
        serializer = self.get_serializer(orders, many=True)
        return Response({
            'count': orders.count(),
            'orders': serializer.data
        })

    @action(detail=True, methods=['post'])
    def mark_notified(self, request, pk=None):
        order = self.get_object()
        order.is_notified = True
        order.notified_at = timezone.now()
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def mark_all_notified(self, request):
        count = Order.objects.filter(
            status='ready',
            is_paid=True,
            is_archived=False,
            is_notified=False
        ).update(is_notified=True, notified_at=timezone.now())
        return Response({'marked_count': count})

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        order = self.get_object()
        if order.status != 'completed':
            return Response(
                {'error': '只有已完成的订单才能归档'},
                status=status.HTTP_400_BAD_REQUEST
            )
        order.is_archived = True
        order.archived_at = timezone.now()
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def archived(self, request):
        orders = Order.objects.filter(
            is_archived=True
        ).order_by('-archived_at')
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def detail_by_no(self, request, pk=None):
        try:
            order = Order.objects.get(order_no=pk)
            serializer = self.get_serializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({'error': '订单不存在'}, status=status.HTTP_404_NOT_FOUND)
