from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import Movie, Hall, Schedule, Seat, Order
from .serializers import (
    MovieSerializer, HallSerializer, ScheduleSerializer,
    SeatSerializer, OrderSerializer, OrderCreateSerializer
)
from .auth_serializers import (
    UserSerializer, UserCreateSerializer, ChangePasswordSerializer,
    LoginSerializer, GroupSerializer
)
from .permissions import (
    IsAdmin, IsSeller, IsChecker,
    MoviePermission, HallPermission, SchedulePermission,
    OrderPermission, SeatPermission
)


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class AuthView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        from django.contrib.auth import authenticate
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        
        if not user:
            return Response(
                {'error': '用户名或密码错误'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.is_active:
            return Response(
                {'error': '账号已被禁用'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            request.auth.delete()
        except:
            pass
        return Response({'message': '登出成功'})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    pagination_class = StandardPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.request.query_params.get('username')
        group = self.request.query_params.get('group')
        
        if username:
            queryset = queryset.filter(username__icontains=username)
        if group:
            queryset = queryset.filter(groups__name=group)
        
        return queryset.order_by('-date_joined')

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        
        return Response({'message': '密码修改成功'})

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        user = self.get_object()
        if user == request.user:
            return Response(
                {'error': '不能禁用自己的账号'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.is_active = not user.is_active
        user.save()
        
        return Response({
            'message': f'账号已{"启用" if user.is_active else "禁用"}',
            'is_active': user.is_active
        })


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdmin]


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = StandardPagination
    permission_classes = [MoviePermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.query_params.get('title')
        genre = self.request.query_params.get('genre')
        is_showing = self.request.query_params.get('is_showing')
        director = self.request.query_params.get('director')
        min_rating = self.request.query_params.get('min_rating')
        max_rating = self.request.query_params.get('max_rating')
        
        if title:
            queryset = queryset.filter(title__icontains=title)
        if genre:
            queryset = queryset.filter(genre__icontains=genre)
        if is_showing is not None:
            queryset = queryset.filter(is_showing=(is_showing.lower() == 'true'))
        if director:
            queryset = queryset.filter(director__icontains=director)
        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)
        if max_rating:
            queryset = queryset.filter(rating__lte=max_rating)
        
        return queryset.order_by('-created_at')

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def showing(self, request):
        movies = Movie.objects.filter(is_showing=True)
        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)


class HallViewSet(viewsets.ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    pagination_class = StandardPagination
    permission_classes = [HallPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        hall_no = self.request.query_params.get('hall_no')
        is_3d = self.request.query_params.get('is_3d')
        is_active = self.request.query_params.get('is_active')
        min_seats = self.request.query_params.get('min_seats')
        max_seats = self.request.query_params.get('max_seats')
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        if hall_no:
            queryset = queryset.filter(name__icontains=hall_no)
        if is_3d is not None:
            queryset = queryset.filter(is_3d=(is_3d.lower() == 'true'))
        if is_active is not None:
            queryset = queryset.filter(is_active=(is_active.lower() == 'true'))
        if min_seats:
            queryset = queryset.filter(total_seats__gte=min_seats)
        if max_seats:
            queryset = queryset.filter(total_seats__lte=max_seats)
        
        return queryset.order_by('name')

    @action(detail=True, methods=['post'])
    def generate_seats(self, request, pk=None):
        hall = self.get_object()
        created_count = 0
        
        for row in range(1, hall.total_rows + 1):
            for col in range(1, hall.total_cols + 1):
                seat_code = f'{row}排{col}座'
                _, created = Seat.objects.get_or_create(
                    hall=hall,
                    schedule=None,
                    row_number=row,
                    col_number=col,
                    defaults={'seat_code': seat_code, 'is_available': True}
                )
                if created:
                    created_count += 1
        
        return Response({
            'message': '座位生成成功',
            'created_count': created_count
        }, status=status.HTTP_200_OK)


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    pagination_class = StandardPagination
    permission_classes = [SchedulePermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        movie_title = self.request.query_params.get('movie_title')
        movie_id = self.request.query_params.get('movie_id')
        hall_id = self.request.query_params.get('hall_id')
        hall_name = self.request.query_params.get('hall_name')
        hall_no = self.request.query_params.get('hall_no')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        date = self.request.query_params.get('date')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        is_active = self.request.query_params.get('is_active')
        status_filter = self.request.query_params.get('status')
        
        if movie_title:
            queryset = queryset.filter(movie__title__icontains=movie_title)
        if movie_id:
            queryset = queryset.filter(movie_id=movie_id)
        if hall_id:
            queryset = queryset.filter(hall_id=hall_id)
        if hall_name:
            queryset = queryset.filter(hall__name__icontains=hall_name)
        if hall_no:
            queryset = queryset.filter(hall__name__icontains=hall_no)
        if date:
            queryset = queryset.filter(show_time__date=date)
        if start_date:
            queryset = queryset.filter(show_time__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(show_time__date__lte=end_date)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if is_active is not None:
            queryset = queryset.filter(is_active=(is_active.lower() == 'true'))
        else:
            queryset = queryset.filter(is_active=True)
        
        if status_filter == 'upcoming':
            queryset = queryset.filter(show_time__gt=timezone.now())
        elif status_filter == 'ongoing':
            queryset = queryset.filter(
                show_time__lte=timezone.now(),
                end_time__gt=timezone.now()
            )
        elif status_filter == 'ended':
            queryset = queryset.filter(end_time__lt=timezone.now())
        
        return queryset.order_by('show_time')

    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def seats(self, request, pk=None):
        schedule = self.get_object()
        seats = Seat.objects.filter(hall=schedule.hall, schedule=schedule)
        
        if not seats.exists():
            for row in range(1, schedule.hall.total_rows + 1):
                for col in range(1, schedule.hall.total_cols + 1):
                    seat_code = f'{row}排{col}座'
                    Seat.objects.create(
                        hall=schedule.hall,
                        schedule=schedule,
                        row_number=row,
                        col_number=col,
                        seat_code=seat_code,
                        is_available=True
                    )
            seats = Seat.objects.filter(hall=schedule.hall, schedule=schedule)
        
        is_available = request.query_params.get('is_available')
        if is_available is not None:
            seats = seats.filter(is_available=(is_available.lower() == 'true'))
        
        page = self.paginate_queryset(seats)
        if page is not None:
            serializer = SeatSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data)


class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    pagination_class = StandardPagination
    permission_classes = [SeatPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        hall_id = self.request.query_params.get('hall_id')
        schedule_id = self.request.query_params.get('schedule_id')
        is_available = self.request.query_params.get('is_available')
        row_number = self.request.query_params.get('row_number')
        
        if hall_id:
            queryset = queryset.filter(hall_id=hall_id)
        if schedule_id:
            queryset = queryset.filter(schedule_id=schedule_id)
        if is_available is not None:
            queryset = queryset.filter(is_available=(is_available.lower() == 'true'))
        if row_number:
            queryset = queryset.filter(row_number=row_number)
        
        return queryset.order_by('row_number', 'col_number')


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = StandardPagination
    permission_classes = [OrderPermission]

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        order_no = self.request.query_params.get('order_no')
        status_param = self.request.query_params.get('status')
        movie_id = self.request.query_params.get('movie_id')
        movie_title = self.request.query_params.get('movie_title')
        hall_id = self.request.query_params.get('hall_id')
        hall_name = self.request.query_params.get('hall_name')
        hall_no = self.request.query_params.get('hall_no')
        schedule_id = self.request.query_params.get('schedule_id')
        customer_name = self.request.query_params.get('customer_name')
        customer_phone = self.request.query_params.get('customer_phone')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        min_amount = self.request.query_params.get('min_amount')
        max_amount = self.request.query_params.get('max_amount')
        
        if order_no:
            queryset = queryset.filter(order_no__icontains=order_no)
        if status_param:
            status_list = status_param.split(',')
            queryset = queryset.filter(status__in=status_list)
        if movie_id:
            queryset = queryset.filter(schedule__movie_id=movie_id)
        if movie_title:
            queryset = queryset.filter(schedule__movie__title__icontains=movie_title)
        if hall_id:
            queryset = queryset.filter(schedule__hall_id=hall_id)
        if hall_name:
            queryset = queryset.filter(schedule__hall__name__icontains=hall_name)
        if hall_no:
            queryset = queryset.filter(schedule__hall__name__icontains=hall_no)
        if schedule_id:
            queryset = queryset.filter(schedule_id=schedule_id)
        if customer_name:
            queryset = queryset.filter(customer_name__icontains=customer_name)
        if customer_phone:
            queryset = queryset.filter(customer_phone__icontains=customer_phone)
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)
        if min_amount:
            queryset = queryset.filter(total_price__gte=min_amount)
        if max_amount:
            queryset = queryset.filter(total_price__lte=max_amount)
        
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        order = self.get_object()
        
        if order.status in ['completed', 'refunded']:
            return Response(
                {'error': '该订单状态不允许退票'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if order.schedule.show_time < timezone.now():
            return Response(
                {'error': '场次已开始，无法退票'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            order.status = 'refunded'
            order.refund_at = timezone.now()
            order.refund_by = request.user
            order.save()
            
            order.seats.update(is_available=True)
        
        return Response({
            'message': '退票成功',
            'order_no': order.order_no,
            'refund_at': order.refund_at,
            'refund_by': order.refund_by.username
        })

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        order = self.get_object()
        
        if order.status != 'checked':
            return Response(
                {'error': '只有已检票的订单才能完结'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = 'completed'
        order.completed_at = timezone.now()
        order.completed_by = request.user
        order.save()
        
        return Response({
            'message': '订单已完结',
            'order_no': order.order_no,
            'completed_at': order.completed_at
        })


class CheckTicketView(APIView):
    permission_classes = [IsChecker]

    def post(self, request):
        order_no = request.data.get('order_no')
        
        if not order_no:
            return Response(
                {'error': '请提供订单号'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            order = Order.objects.get(order_no=order_no)
        except Order.DoesNotExist:
            return Response(
                {'error': '订单不存在'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if order.status == 'checked':
            return Response(
                {'error': '该订单已检票，请勿重复检票'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if order.status == 'refunded':
            return Response(
                {'error': '该订单已退票，无法检票'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if order.status == 'completed':
            return Response(
                {'error': '该订单已完结'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if order.schedule.end_time < timezone.now():
            return Response(
                {'error': '该场次已结束，无法检票'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            order.status = 'checked'
            order.ticket_checked_at = timezone.now()
            order.ticket_checked_by = request.user
            order.save()
        
        return Response({
            'message': '检票成功',
            'order_no': order.order_no,
            'movie_title': order.schedule.movie.title,
            'hall_name': order.schedule.hall.name,
            'show_time': order.schedule.show_time,
            'end_time': order.schedule.end_time,
            'seat_codes': order.seat_codes,
            'customer_name': order.customer_name,
            'checked_at': order.ticket_checked_at,
            'checked_by': order.ticket_checked_by.username
        })


class OrderStatisticsView(APIView):
    permission_classes = [IsAdmin | IsSeller]

    def get(self, request):
        movie_id = request.query_params.get('movie_id')
        hall_id = request.query_params.get('hall_id')
        schedule_id = request.query_params.get('schedule_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        orders = Order.objects.all()
        
        if movie_id:
            orders = orders.filter(schedule__movie_id=movie_id)
        if hall_id:
            orders = orders.filter(schedule__hall_id=hall_id)
        if schedule_id:
            orders = orders.filter(schedule_id=schedule_id)
        if start_date:
            orders = orders.filter(created_at__date__gte=start_date)
        if end_date:
            orders = orders.filter(created_at__date__lte=end_date)
        
        total_orders = orders.count()
        pending_orders = orders.filter(status='pending').count()
        checked_orders = orders.filter(status='checked').count()
        completed_orders = orders.filter(status='completed').count()
        refunded_orders = orders.filter(status='refunded').count()
        
        total_revenue = orders.exclude(status='refunded').aggregate(
            total=models.Sum('total_price')
        )['total'] or 0
        
        today = timezone.now().date()
        today_orders = orders.filter(created_at__date=today)
        today_total = today_orders.count()
        today_revenue = today_orders.exclude(status='refunded').aggregate(
            total=models.Sum('total_price')
        )['total'] or 0
        
        return Response({
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'checked_orders': checked_orders,
            'completed_orders': completed_orders,
            'refunded_orders': refunded_orders,
            'total_revenue': float(total_revenue),
            'today_orders': today_total,
            'today_revenue': float(today_revenue)
        })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_permissions(request):
    user = request.user
    is_admin = user.groups.filter(name='管理员').exists()
    is_seller = user.groups.filter(name='售票员').exists() or is_admin
    is_checker = user.groups.filter(name='检票员').exists() or is_admin
    
    return Response({
        'is_admin': is_admin,
        'is_seller': is_seller,
        'is_checker': is_checker,
        'permissions': {
            'movie': {
                'create': is_admin,
                'edit': is_admin,
                'delete': is_admin,
                'view': True
            },
            'hall': {
                'create': is_admin,
                'edit': is_admin,
                'delete': is_admin,
                'view': True
            },
            'schedule': {
                'create': is_admin,
                'edit': is_admin,
                'delete': is_admin,
                'view': True
            },
            'order': {
                'create': is_seller,
                'edit': is_seller,
                'refund': is_seller,
                'complete': is_seller,
                'view': True
            },
            'ticket': {
                'check': is_checker
            },
            'user': {
                'manage': is_admin
            }
        }
    })
