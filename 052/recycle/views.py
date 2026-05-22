from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Item, Order, OrderItem, QualityCheck, Settlement, OrderStatus, ItemCategory, UserRole, UserProfile
from .serializers import (
    ItemSerializer,
    OrderSerializer,
    OrderCreateSerializer,
    QualityCheckSerializer,
    SettlementSerializer,
    EstimateSerializer,
    PickupSerializer,
    WarehouseSerializer,
    CompleteSerializer,
    AssignRecyclerSerializer,
    UserSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.profile.role == UserRole.ADMIN


class IsAdminOrSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.profile.role == UserRole.ADMIN:
            return True
        return obj == request.user


def get_role_permissions(user):
    role = user.profile.role
    return {
        'can_create_order': role in [UserRole.CUSTOMER_SERVICE, UserRole.ADMIN],
        'can_edit_order': role in [UserRole.CUSTOMER_SERVICE, UserRole.ADMIN],
        'can_delete_order': role in [UserRole.ADMIN],
        'can_pickup': role in [UserRole.RECYCLER, UserRole.ADMIN],
        'can_warehouse': role in [UserRole.RECYCLER, UserRole.ADMIN],
        'can_estimate': role in [UserRole.CUSTOMER_SERVICE, UserRole.ADMIN],
        'can_complete': role in [UserRole.ADMIN],
        'can_assign_recycler': role in [UserRole.CUSTOMER_SERVICE, UserRole.ADMIN],
        'can_manage_users': role in [UserRole.ADMIN],
    }


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.query_params.get('role')
        if role:
            queryset = queryset.filter(profile__role=role)
        return queryset.order_by('-date_joined')

    @action(detail=False, methods=['get'])
    def recyclers(self, request):
        recyclers = User.objects.filter(profile__role=UserRole.RECYCLER)
        serializer = self.get_serializer(recyclers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        permissions = get_role_permissions(request.user)
        return Response({
            'user': serializer.data,
            'permissions': permissions
        })


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        name = self.request.query_params.get('name')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if category and category in [c[0] for c in ItemCategory.choices]:
            queryset = queryset.filter(category=category)
        if name:
            queryset = queryset.filter(name__icontains=name)
        if min_price:
            queryset = queryset.filter(estimated_price__gte=min_price)
        if max_price:
            queryset = queryset.filter(estimated_price__lte=max_price)
        
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        role = user.profile.role

        customer_name = self.request.query_params.get('customer_name')
        status = self.request.query_params.get('status')
        item_category = self.request.query_params.get('item_category')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        phone = self.request.query_params.get('phone')
        created_by = self.request.query_params.get('created_by')
        recycler = self.request.query_params.get('recycler')
        
        if customer_name:
            queryset = queryset.filter(customer_name__icontains=customer_name)
        if phone:
            queryset = queryset.filter(customer_phone__icontains=phone)
        if status and status in [s[0] for s in OrderStatus.choices]:
            queryset = queryset.filter(status=status)
        if item_category and item_category in [c[0] for c in ItemCategory.choices]:
            queryset = queryset.filter(items__category=item_category).distinct()
        if start_date:
            queryset = queryset.filter(pickup_time__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(pickup_time__date__lte=end_date)
        if created_by:
            queryset = queryset.filter(created_by_id=created_by)
        if recycler:
            queryset = queryset.filter(recycler_id=recycler)

        if role == UserRole.RECYCLER:
            queryset = queryset.filter(Q(recycler=user) | Q(recycler__isnull=True))

        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        user = self.request.user
        role = user.profile.role
        if role not in [UserRole.CUSTOMER_SERVICE, UserRole.ADMIN]:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('您没有权限创建订单')
        serializer.save(created_by=user)

    def perform_update(self, serializer):
        user = self.request.user
        role = user.profile.role
        if role not in [UserRole.CUSTOMER_SERVICE, UserRole.ADMIN]:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('您没有权限编辑订单')
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        role = user.profile.role
        if role != UserRole.ADMIN:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('您没有权限删除订单')
        instance.delete()

    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        user = request.user
        role = user.profile.role
        queryset = self.get_queryset()

        if role == UserRole.RECYCLER:
            queryset = queryset.filter(recycler=user)
        elif role == UserRole.CUSTOMER_SERVICE:
            queryset = queryset.filter(created_by=user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], serializer_class=AssignRecyclerSerializer)
    def assign_recycler(self, request, pk=None):
        order = self.get_object()
        user = request.user
        role = user.profile.role

        if role not in [UserRole.CUSTOMER_SERVICE, UserRole.ADMIN]:
            return Response({'error': '您没有权限分配回收员'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        recycler_id = serializer.validated_data['recycler_id']
        recycler = User.objects.get(id=recycler_id)
        
        order.recycler = recycler
        order.save()

        return Response({
            'message': '回收员分配成功',
            'order_no': order.order_no,
            'recycler': recycler.username
        })

    @action(detail=True, methods=['post'], serializer_class=EstimateSerializer)
    def estimate(self, request, pk=None):
        order = self.get_object()
        user = request.user
        role = user.profile.role

        if role not in [UserRole.CUSTOMER_SERVICE, UserRole.ADMIN]:
            return Response({'error': '您没有权限进行估价'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        estimated_prices = serializer.validated_data['estimated_prices']
        auto_warehouse = serializer.validated_data.get('auto_warehouse', False)
        auto_settle = serializer.validated_data.get('auto_settle', False)

        with transaction.atomic():
            total_amount = 0
            order_items = list(OrderItem.objects.filter(order=order))
            
            if len(estimated_prices) != len(order_items):
                return Response(
                    {'error': f'估价数量({len(estimated_prices)})与物品数量({len(order_items)})不匹配'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            for idx, order_item in enumerate(order_items):
                price = estimated_prices[idx].get('price', 0)
                order_item.unit_price = price
                order_item.save()
                order_item.item.estimated_price = price
                order_item.item.save()
                total_amount += order_item.subtotal

            order.total_amount = total_amount
            order.save()

        return Response({
            'message': '估价完成',
            'order_no': order.order_no,
            'total_amount': str(order.total_amount)
        })

    @action(detail=True, methods=['post'], serializer_class=PickupSerializer)
    def pickup(self, request, pk=None):
        order = self.get_object()
        user = request.user
        role = user.profile.role

        if role not in [UserRole.RECYCLER, UserRole.ADMIN]:
            return Response({'error': '您没有权限进行回收操作'}, status=status.HTTP_403_FORBIDDEN)

        if order.status != OrderStatus.PENDING_PICKUP:
            return Response({'error': '订单状态不允许回收'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        auto_warehouse = serializer.validated_data.get('auto_warehouse', False)
        auto_settle = serializer.validated_data.get('auto_settle', False)

        with transaction.atomic():
            order.status = OrderStatus.PICKED_UP
            order.picked_up_at = timezone.now()
            if not order.recycler and role == UserRole.RECYCLER:
                order.recycler = user
            order.save()

            if auto_warehouse:
                order.auto_warehouse(user)
                if auto_settle:
                    order.auto_settle(user)

        return Response({
            'message': '已完成回收',
            'order_no': order.order_no,
            'status': order.get_status_display()
        })

    @action(detail=True, methods=['post'], serializer_class=WarehouseSerializer)
    def warehouse(self, request, pk=None):
        order = self.get_object()
        user = request.user
        role = user.profile.role

        if role not in [UserRole.RECYCLER, UserRole.ADMIN]:
            return Response({'error': '您没有权限进行入库操作'}, status=status.HTTP_403_FORBIDDEN)

        if order.status != OrderStatus.PICKED_UP:
            return Response({'error': '订单状态不允许入库'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        auto_settle = serializer.validated_data.get('auto_settle', False)

        with transaction.atomic():
            QualityCheck.objects.create(
                order=order,
                checker=serializer.validated_data['checker'],
                result=serializer.validated_data['result'],
                actual_amount=serializer.validated_data['actual_amount'],
                issue_description=serializer.validated_data.get('issue_description', '')
            )

            order.status = OrderStatus.WAREHOUSED
            order.warehoused_at = timezone.now()
            order.save()

            if auto_settle:
                order.auto_settle(user)

        return Response({
            'message': '已完成入库质检',
            'order_no': order.order_no,
            'status': order.get_status_display()
        })

    @action(detail=True, methods=['post'], serializer_class=CompleteSerializer)
    def complete(self, request, pk=None):
        order = self.get_object()
        user = request.user
        role = user.profile.role

        if role != UserRole.ADMIN:
            return Response({'error': '您没有权限进行结算操作'}, status=status.HTTP_403_FORBIDDEN)

        if order.status != OrderStatus.WAREHOUSED:
            return Response({'error': '订单状态不允许结算'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            try:
                quality_check = QualityCheck.objects.get(order=order)
                settle_amount = quality_check.actual_amount
            except QualityCheck.DoesNotExist:
                settle_amount = order.total_amount

            Settlement.objects.create(
                order=order,
                settle_amount=settle_amount,
                operator=serializer.validated_data['operator'],
                remark=serializer.validated_data.get('remark', '')
            )

            order.status = OrderStatus.COMPLETED
            order.completed_at = timezone.now()
            order.save()

        return Response({
            'message': '已完成订单结算',
            'order_no': order.order_no,
            'status': order.get_status_display(),
            'settle_amount': str(settle_amount)
        })


class QualityCheckViewSet(viewsets.ModelViewSet):
    queryset = QualityCheck.objects.all()
    serializer_class = QualityCheckSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        result = self.request.query_params.get('result')
        checker = self.request.query_params.get('checker')
        order_no = self.request.query_params.get('order_no')
        
        if result:
            queryset = queryset.filter(result=result)
        if checker:
            queryset = queryset.filter(checker__icontains=checker)
        if order_no:
            queryset = queryset.filter(order__order_no__icontains=order_no)
        
        return queryset.order_by('-check_time')


class SettlementViewSet(viewsets.ModelViewSet):
    queryset = Settlement.objects.all()
    serializer_class = SettlementSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        operator = self.request.query_params.get('operator')
        order_no = self.request.query_params.get('order_no')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if operator:
            queryset = queryset.filter(operator__icontains=operator)
        if order_no:
            queryset = queryset.filter(order__order_no__icontains=order_no)
        if start_date:
            queryset = queryset.filter(settle_time__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(settle_time__date__lte=end_date)
        
        return queryset.order_by('-settle_time')
