from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from django.db.models import Q, Sum
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Room, Guest, Order
from .serializers import (
    RoomSerializer, GuestSerializer, OrderSerializer,
    OrderCreateSerializer, CheckInSerializer, CheckOutSerializer,
    UserSerializer, UserCreateSerializer, RoomCleanSerializer
)
from .permissions import IsReceptionist, IsHousekeeper, IsAdmin, get_user_role


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    pagination_class = StandardPagination
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response({
            'code': 200,
            'message': '获取用户信息成功',
            'data': serializer.data
        })


class AuthView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({
                'code': 400,
                'message': '用户名和密码不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            serializer = UserSerializer(user)
            return Response({
                'code': 200,
                'message': '登录成功',
                'data': serializer.data
            })
        else:
            return Response({
                'code': 401,
                'message': '用户名或密码错误'
            }, status=status.HTTP_401_UNAUTHORIZED)

    @permission_classes([permissions.IsAuthenticated])
    def delete(self, request):
        logout(request)
        return Response({
            'code': 200,
            'message': '登出成功'
        })


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all().order_by('room_number')
    serializer_class = RoomSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]
        elif self.action in ['mark_clean', 'mark_dirty']:
            permission_classes = [IsHousekeeper | IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        room_number = self.request.query_params.get('room_number')
        room_type = self.request.query_params.get('room_type')
        status = self.request.query_params.get('status')
        clean_status = self.request.query_params.get('clean_status')
        floor = self.request.query_params.get('floor')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if room_number:
            queryset = queryset.filter(room_number__icontains=room_number)
        if room_type:
            queryset = queryset.filter(room_type=room_type)
        if status:
            queryset = queryset.filter(status=status)
        if clean_status:
            queryset = queryset.filter(clean_status=clean_status)
        if floor:
            queryset = queryset.filter(floor=floor)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    @action(detail=False, methods=['get'])
    def available(self, request):
        rooms = Room.objects.filter(status='available', clean_status='clean')
        page = self.paginate_queryset(rooms)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(rooms, many=True)
        return Response({
            'code': 200,
            'message': '获取可用房间成功',
            'data': serializer.data
        })

    @action(detail=True, methods=['post'])
    def mark_clean(self, request, pk=None):
        room = self.get_object()
        room.clean_status = 'clean'
        room.last_clean_time = timezone.now()
        room.cleaned_by = request.user
        room.save()

        serializer = self.get_serializer(room)
        return Response({
            'code': 200,
            'message': '房间已标记为已清洁',
            'data': serializer.data
        })

    @action(detail=True, methods=['post'])
    def mark_dirty(self, request, pk=None):
        room = self.get_object()
        room.clean_status = 'dirty'
        room.save()

        serializer = self.get_serializer(room)
        return Response({
            'code': 200,
            'message': '房间已标记为待清洁',
            'data': serializer.data
        })


class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all().order_by('-create_time')
    serializer_class = GuestSerializer
    pagination_class = StandardPagination
    permission_classes = [IsReceptionist | IsAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        phone = self.request.query_params.get('phone')
        id_card = self.request.query_params.get('id_card')
        gender = self.request.query_params.get('gender')

        if name:
            queryset = queryset.filter(name__icontains=name)
        if phone:
            queryset = queryset.filter(phone__icontains=phone)
        if id_card:
            queryset = queryset.filter(id_card__icontains=id_card)
        if gender:
            queryset = queryset.filter(gender=gender)

        return queryset

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': 201,
                'message': '登记成功',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'code': 400,
            'message': '登记失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-create_time')
    serializer_class = OrderSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'cancel']:
            permission_classes = [IsReceptionist | IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        order_number = self.request.query_params.get('order_number')
        guest_name = self.request.query_params.get('guest_name')
        guest_phone = self.request.query_params.get('guest_phone')
        room_number = self.request.query_params.get('room_number')
        order_status = self.request.query_params.get('status')
        check_in_date_from = self.request.query_params.get('check_in_date_from')
        check_in_date_to = self.request.query_params.get('check_in_date_to')

        if order_number:
            queryset = queryset.filter(order_number__icontains=order_number)
        if guest_name:
            queryset = queryset.filter(guest__name__icontains=guest_name)
        if guest_phone:
            queryset = queryset.filter(guest__phone__icontains=guest_phone)
        if room_number:
            queryset = queryset.filter(room__room_number__icontains=room_number)
        if order_status:
            queryset = queryset.filter(status=order_status)
        if check_in_date_from:
            queryset = queryset.filter(check_in_date__gte=check_in_date_from)
        if check_in_date_to:
            queryset = queryset.filter(check_in_date__lte=check_in_date_to)

        return queryset

    def perform_destroy(self, instance):
        room = instance.room
        room.status = 'available'
        room.save()
        instance.delete()

    @action(detail=False, methods=['get'])
    def pending(self, request):
        orders = Order.objects.filter(status='pending')
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(orders, many=True)
        return Response({
            'code': 200,
            'message': '获取待入住订单成功',
            'data': serializer.data
        })

    @action(detail=False, methods=['get'])
    def checked_in(self, request):
        orders = Order.objects.filter(status='checked_in')
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(orders, many=True)
        return Response({
            'code': 200,
            'message': '获取已入住订单成功',
            'data': serializer.data
        })

    @action(detail=False, methods=['get'])
    def checked_out(self, request):
        orders = Order.objects.filter(status='checked_out')
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(orders, many=True)
        return Response({
            'code': 200,
            'message': '获取已退房订单成功',
            'data': serializer.data
        })

    @action(detail=False, methods=['get'])
    def cancelled(self, request):
        orders = Order.objects.filter(status='cancelled')
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(orders, many=True)
        return Response({
            'code': 200,
            'message': '获取已取消订单成功',
            'data': serializer.data
        })

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status not in ['pending', 'checked_in']:
            return Response({
                'code': 400,
                'message': '该订单状态不允许取消'
            }, status=status.HTTP_400_BAD_REQUEST)

        room = order.room
        room.status = 'available'
        room.save()

        order.status = 'cancelled'
        order.save()

        serializer = self.get_serializer(order)
        return Response({
            'code': 200,
            'message': '取消成功',
            'data': serializer.data
        })


class CheckInView(APIView):
    permission_classes = [IsReceptionist | IsAdmin]

    def post(self, request):
        serializer = CheckInSerializer(data=request.data)
        if serializer.is_valid():
            order_id = serializer.validated_data['order_id']
            order = Order.objects.get(id=order_id)

            if order.room.clean_status != 'clean':
                return Response({
                    'code': 400,
                    'message': '房间未清洁，无法入住'
                }, status=status.HTTP_400_BAD_REQUEST)

            order.status = 'checked_in'
            order.actual_check_in = timezone.now()
            order.checked_in_by = request.user
            order.save()

            room = order.room
            room.status = 'occupied'
            room.save()

            order_serializer = OrderSerializer(order)
            return Response({
                'code': 200,
                'message': '入住成功',
                'data': {
                    'order_number': order.order_number,
                    'actual_check_in': order.actual_check_in,
                    'guest_name': order.guest.name,
                    'room_number': order.room.room_number,
                    'order_info': order_serializer.data
                }
            }, status=status.HTTP_200_OK)
        return Response({
            'code': 400,
            'message': '入住失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class CheckOutView(APIView):
    permission_classes = [IsReceptionist | IsAdmin]

    def post(self, request):
        serializer = CheckOutSerializer(data=request.data)
        if serializer.is_valid():
            order_id = serializer.validated_data['order_id']
            order = Order.objects.get(id=order_id)

            actual_check_out = timezone.now()
            overtime_info = order.calculate_overtime_fee(actual_check_out)

            order.status = 'checked_out'
            order.actual_check_out = actual_check_out
            order.actual_days = overtime_info['actual_days']
            order.overtime_hours = overtime_info['overtime_hours']
            order.overtime_fee = overtime_info['overtime_fee']
            order.total_amount = overtime_info['total_amount']
            order.refund_amount = max(0, float(order.deposit) - float(order.total_amount))
            order.checked_out_by = request.user
            order.save()

            room = order.room
            room.status = 'available'
            room.clean_status = 'dirty'
            room.save()

            order_serializer = OrderSerializer(order)
            return Response({
                'code': 200,
                'message': '退房成功',
                'data': {
                    'order_number': order.order_number,
                    'actual_check_out': actual_check_out,
                    'days': order.days,
                    'actual_days': order.actual_days,
                    'daily_price': order.daily_price,
                    'total_amount': order.total_amount,
                    'overtime_hours': order.overtime_hours,
                    'overtime_fee': order.overtime_fee,
                    'deposit': order.deposit,
                    'refund_amount': order.refund_amount,
                    'guest_name': order.guest.name,
                    'room_number': order.room.room_number,
                    'order_info': order_serializer.data
                }
            }, status=status.HTTP_200_OK)
        return Response({
            'code': 400,
            'message': '退房失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class StatisticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        total_rooms = Room.objects.count()
        available_rooms = Room.objects.filter(status='available').count()
        occupied_rooms = Room.objects.filter(status='occupied').count()
        reserved_rooms = Room.objects.filter(status='reserved').count()
        dirty_rooms = Room.objects.filter(clean_status='dirty').count()

        total_orders = Order.objects.count()
        pending_orders = Order.objects.filter(status='pending').count()
        checked_in_orders = Order.objects.filter(status='checked_in').count()
        checked_out_orders = Order.objects.filter(status='checked_out').count()
        cancelled_orders = Order.objects.filter(status='cancelled').count()

        today = timezone.now().date()
        today_check_in = Order.objects.filter(check_in_date=today).count()
        today_check_out = Order.objects.filter(check_out_date=today).count()

        total_amount = Order.objects.filter(status='checked_out').aggregate(total=Sum('total_amount'))['total'] or 0
        total_overtime_fee = Order.objects.filter(status='checked_out').aggregate(total=Sum('overtime_fee'))['total'] or 0

        return Response({
            'code': 200,
            'message': '获取统计信息成功',
            'data': {
                'rooms': {
                    'total': total_rooms,
                    'available': available_rooms,
                    'occupied': occupied_rooms,
                    'reserved': reserved_rooms,
                    'dirty': dirty_rooms,
                },
                'orders': {
                    'total': total_orders,
                    'pending': pending_orders,
                    'checked_in': checked_in_orders,
                    'checked_out': checked_out_orders,
                    'cancelled': cancelled_orders,
                    'total_amount': float(total_amount),
                    'total_overtime_fee': float(total_overtime_fee),
                },
                'today': {
                    'check_in': today_check_in,
                    'check_out': today_check_out,
                }
            }
        })
