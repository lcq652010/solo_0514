from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from django.db.models import Avg, Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import User, Customer, Service, Aunt, Order, Review, OrderArchive, AuntStatistics
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
    CustomerSerializer,
    CustomerRegistrationSerializer,
    ServiceSerializer,
    AuntSerializer,
    AuntStatisticsSerializer,
    OrderSerializer,
    OrderArchiveSerializer,
    ReviewSerializer,
    OrderDispatchSerializer,
    OrderStatusSerializer,
    ChangePasswordSerializer,
)
from .permissions import (
    IsAdminUser,
    IsAuntUser,
    IsCustomerUser,
    IsAdminOrReadOnly,
    IsAdminOrAunt,
    IsAdminOrCustomer,
    IsOwnerOrAdmin,
    IsAuntOwnerOrAdmin,
    IsCustomerOwnerOrAdmin,
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'page_size': self.get_page_size(self.request),
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = []

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register_customer(self, request):
        serializer = CustomerRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()
        token = Token.objects.get(user=customer.user)
        return Response({
            'token': token.key,
            'customer': CustomerSerializer(customer).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'message': '登出成功'})
        except:
            return Response({'error': '登出失败'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = UserSerializer(request.user)
        data = serializer.data
        if hasattr(request.user, 'customer_profile'):
            data['profile'] = CustomerSerializer(request.user.customer_profile).data
        elif hasattr(request.user, 'aunt_profile'):
            data['profile'] = AuntSerializer(request.user.aunt_profile).data
        return Response(data)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not request.user.check_password(serializer.validated_data['old_password']):
            return Response({'error': '原密码错误'}, status=status.HTTP_400_BAD_REQUEST)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({'message': '密码修改成功'})


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAdminUser | IsAdminOrAunt]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsOwnerOrAdmin]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        phone = self.request.query_params.get('phone')
        if phone:
            queryset = queryset.filter(phone__icontains=phone)
        return queryset


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        min_price = self.request.query_params.get('min_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        max_price = self.request.query_params.get('max_price')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        return queryset


class AuntViewSet(viewsets.ModelViewSet):
    queryset = Aunt.objects.all()
    serializer_class = AuntSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuntOwnerOrAdmin | IsAdminUser]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        service_id = self.request.query_params.get('service_id')
        if service_id:
            queryset = queryset.filter(skills__id=service_id)
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        gender = self.request.query_params.get('gender')
        if gender:
            queryset = queryset.filter(gender=gender)
        min_age = self.request.query_params.get('min_age')
        if min_age:
            queryset = queryset.filter(age__gte=min_age)
        max_age = self.request.query_params.get('max_age')
        if max_age:
            queryset = queryset.filter(age__lte=max_age)
        min_experience = self.request.query_params.get('min_experience')
        if min_experience:
            queryset = queryset.filter(experience__gte=min_experience)
        min_rating = self.request.query_params.get('min_rating')
        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)
        return queryset.distinct()

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        aunt = self.get_object()
        stats, _ = AuntStatistics.objects.get_or_create(aunt=aunt)
        stats.refresh()
        return Response(AuntStatisticsSerializer(stats).data)

    @action(detail=True, methods=['get'])
    def orders(self, request, pk=None):
        aunt = self.get_object()
        orders = Order.objects.filter(aunt=aunt)
        status = request.query_params.get('status')
        if status:
            orders = orders.filter(status=status)
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = OrderSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        aunt = self.get_object()
        reviews = Review.objects.filter(aunt=aunt)
        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = ReviewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated | IsAdminOrCustomer]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser | IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.role == 'customer' and hasattr(user, 'customer_profile'):
            queryset = queryset.filter(customer=user.customer_profile)
        elif user.role == 'aunt' and hasattr(user, 'aunt_profile'):
            queryset = queryset.filter(aunt=user.aunt_profile)

        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)

        aunt_id = self.request.query_params.get('aunt_id')
        if aunt_id:
            queryset = queryset.filter(aunt_id=aunt_id)

        customer_name = self.request.query_params.get('customer_name')
        if customer_name:
            queryset = queryset.filter(customer_name__icontains=customer_name)

        customer_phone = self.request.query_params.get('customer_phone')
        if customer_phone:
            queryset = queryset.filter(customer_phone__icontains=customer_phone)

        service_id = self.request.query_params.get('service_id')
        if service_id:
            queryset = queryset.filter(service_id=service_id)

        start_date = self.request.query_params.get('start_date')
        if start_date:
            queryset = queryset.filter(service_date__gte=start_date)
        end_date = self.request.query_params.get('end_date')
        if end_date:
            queryset = queryset.filter(service_date__lte=end_date)

        order_no = self.request.query_params.get('order_no')
        if order_no:
            queryset = queryset.filter(order_no__icontains=order_no)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        stats = queryset.aggregate(
            total_orders=Count('id'),
            total_amount=Sum('total_price'),
            pending_count=Count('id', filter=Q(status='pending')),
            servicing_count=Count('id', filter=Q(status='servicing')),
            completed_count=Count('id', filter=Q(status__in=['completed', 'archived'])),
            cancelled_count=Count('id', filter=Q(status='cancelled')),
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data['statistics'] = {
                'total_orders': stats['total_orders'] or 0,
                'total_amount': float(stats['total_amount'] or 0),
                'pending_count': stats['pending_count'] or 0,
                'servicing_count': stats['servicing_count'] or 0,
                'completed_count': stats['completed_count'] or 0,
                'cancelled_count': stats['cancelled_count'] or 0,
            }
            return response
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'results': serializer.data,
            'statistics': {
                'total_orders': stats['total_orders'] or 0,
                'total_amount': float(stats['total_amount'] or 0),
                'pending_count': stats['pending_count'] or 0,
                'servicing_count': stats['servicing_count'] or 0,
                'completed_count': stats['completed_count'] or 0,
                'cancelled_count': stats['cancelled_count'] or 0,
            }
        })

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == 'customer' and hasattr(user, 'customer_profile'):
            serializer.save(
                customer=user.customer_profile,
                customer_name=user.customer_profile.name,
                customer_phone=user.customer_profile.phone,
                customer_address=user.customer_profile.address
            )
        else:
            serializer.save()

    @action(detail=True, methods=['post'], serializer_class=OrderDispatchSerializer)
    def dispatch(self, request, pk=None):
        order = self.get_object()
        if order.status != 'pending':
            return Response(
                {'error': '只有待派单状态的订单才能派单'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(
            data=request.data,
            context={'order': order, 'request': request}
        )
        serializer.is_valid(raise_exception=True)
        aunt_id = serializer.validated_data['aunt_id']
        aunt = Aunt.objects.get(id=aunt_id)
        order.aunt = aunt
        order.status = 'servicing'
        aunt.status = 'busy'
        aunt.save()
        order.save()
        return Response(OrderSerializer(order).data)

    @action(detail=True, methods=['post'], serializer_class=OrderStatusSerializer)
    def update_status(self, request, pk=None):
        order = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_status = serializer.validated_data['status']
        
        if new_status == 'completed':
            order.complete_order()
        elif new_status == 'cancelled' and order.status != 'completed':
            if order.aunt:
                order.aunt.status = 'available'
                order.aunt.save()
            order.status = 'cancelled'
            order.save()
        else:
            order.status = new_status
            order.save()
        
        return Response(OrderSerializer(order).data)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        order = self.get_object()
        if order.status != 'servicing':
            return Response(
                {'error': '只有服务中的订单才能标记为完成'},
                status=status.HTTP_400_BAD_REQUEST
            )
        order.complete_order()
        return Response(OrderSerializer(order).data)

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        order = self.get_object()
        if order.status != 'completed':
            return Response(
                {'error': '只有已完成的订单才能归档'},
                status=status.HTTP_400_BAD_REQUEST
            )
        archive = OrderArchive.archive_from_order(order)
        return Response({
            'message': '订单归档成功',
            'archive': OrderArchiveSerializer(archive).data
        })

    @action(detail=False, methods=['post'])
    def auto_archive(self, request):
        days = int(request.query_params.get('days', 30))
        cutoff_date = timezone.now() - timedelta(days=days)
        completed_orders = Order.objects.filter(
            status='completed',
            completed_at__lte=cutoff_date
        )
        archived_count = 0
        for order in completed_orders:
            OrderArchive.archive_from_order(order)
            archived_count += 1
        return Response({
            'message': f'成功归档{archived_count}个订单',
            'archived_count': archived_count
        })

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        today = timezone.now().date()
        total_stats = Order.objects.aggregate(
            total_orders=Count('id'),
            total_amount=Sum('total_price'),
            pending_count=Count('id', filter=Q(status='pending')),
            servicing_count=Count('id', filter=Q(status='servicing')),
            completed_count=Count('id', filter=Q(status__in=['completed', 'archived'])),
            cancelled_count=Count('id', filter=Q(status='cancelled')),
        )
        today_stats = Order.objects.filter(created_at__date=today).aggregate(
            today_orders=Count('id'),
            today_amount=Sum('total_price'),
        )
        return Response({
            'total': {
                'total_orders': total_stats['total_orders'] or 0,
                'total_amount': float(total_stats['total_amount'] or 0),
                'pending_count': total_stats['pending_count'] or 0,
                'servicing_count': total_stats['servicing_count'] or 0,
                'completed_count': total_stats['completed_count'] or 0,
                'cancelled_count': total_stats['cancelled_count'] or 0,
            },
            'today': {
                'today_orders': today_stats['today_orders'] or 0,
                'today_amount': float(today_stats['today_amount'] or 0),
            }
        })


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsCustomerUser | IsAdminUser]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser | IsCustomerOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        aunt_id = self.request.query_params.get('aunt_id')
        if aunt_id:
            queryset = queryset.filter(aunt_id=aunt_id)
        order_id = self.request.query_params.get('order_id')
        if order_id:
            queryset = queryset.filter(order_id=order_id)
        min_rating = self.request.query_params.get('min_rating')
        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)
        max_rating = self.request.query_params.get('max_rating')
        if max_rating:
            queryset = queryset.filter(rating__lte=max_rating)
        return queryset

    def perform_create(self, serializer):
        order = serializer.validated_data['order']
        if order.status != 'completed':
            raise serializers.ValidationError('只有已完成的订单才能评价')
        if hasattr(self.request.user, 'customer_profile'):
            serializer.save(customer=self.request.user.customer_profile)
        else:
            serializer.save()

    def perform_update(self, serializer):
        review = serializer.save()
        review.aunt.update_rating()


class OrderArchiveViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OrderArchive.objects.all()
    serializer_class = OrderArchiveSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        order_no = self.request.query_params.get('order_no')
        if order_no:
            queryset = queryset.filter(order_no__icontains=order_no)
        customer_name = self.request.query_params.get('customer_name')
        if customer_name:
            queryset = queryset.filter(customer_name__icontains=customer_name)
        aunt_name = self.request.query_params.get('aunt_name')
        if aunt_name:
            queryset = queryset.filter(aunt_name__icontains=aunt_name)
        start_date = self.request.query_params.get('start_date')
        if start_date:
            queryset = queryset.filter(archived_at__date__gte=start_date)
        end_date = self.request.query_params.get('end_date')
        if end_date:
            queryset = queryset.filter(archived_at__date__lte=end_date)
        return queryset
