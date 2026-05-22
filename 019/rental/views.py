from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.utils import timezone
from .models import Car, Customer, Order
from .serializers import (
    CarSerializer,
    CustomerSerializer,
    OrderSerializer,
    OrderPickUpSerializer,
    OrderReturnSerializer,
    OrderCancelSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        brand_filter = self.request.query_params.get('brand')
        model_filter = self.request.query_params.get('model')
        car_type_filter = self.request.query_params.get('car_type')
        plate_number_filter = self.request.query_params.get('plate_number')
        min_daily_rent = self.request.query_params.get('min_daily_rent')
        max_daily_rent = self.request.query_params.get('max_daily_rent')

        if status_filter:
            if ',' in status_filter:
                status_list = status_filter.split(',')
                queryset = queryset.filter(status__in=status_list)
            else:
                queryset = queryset.filter(status=status_filter)
        if brand_filter:
            queryset = queryset.filter(brand__icontains=brand_filter)
        if model_filter:
            queryset = queryset.filter(model__icontains=model_filter)
        if car_type_filter:
            queryset = queryset.filter(car_type__icontains=car_type_filter)
        if plate_number_filter:
            queryset = queryset.filter(plate_number__icontains=plate_number_filter)
        if min_daily_rent:
            queryset = queryset.filter(daily_rent__gte=min_daily_rent)
        if max_daily_rent:
            queryset = queryset.filter(daily_rent__lte=max_daily_rent)

        return queryset.order_by('-id')

    @action(detail=False, methods=['get'])
    def available(self, request):
        available_cars = Car.objects.filter(status='available')
        page = self.paginate_queryset(available_cars)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(available_cars, many=True)
        return Response(serializer.data)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        name_filter = self.request.query_params.get('name')
        phone_filter = self.request.query_params.get('phone')
        gender_filter = self.request.query_params.get('gender')

        if name_filter:
            queryset = queryset.filter(name__icontains=name_filter)
        if phone_filter:
            queryset = queryset.filter(phone__icontains=phone_filter)
        if gender_filter:
            queryset = queryset.filter(gender=gender_filter)

        return queryset.order_by('-id')

    @action(detail=False, methods=['get'])
    def search(self, request):
        keyword = request.query_params.get('keyword', '')
        customers = Customer.objects.all()
        if keyword:
            customers = customers.filter(
                Q(name__icontains=keyword) |
                Q(phone__icontains=keyword) |
                Q(id_card__icontains=keyword)
            )
        page = self.paginate_queryset(customers)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(customers, many=True)
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        customer_name = self.request.query_params.get('customer_name')
        customer_phone = self.request.query_params.get('customer_phone')
        car_brand = self.request.query_params.get('car_brand')
        car_model = self.request.query_params.get('car_model')
        car_type = self.request.query_params.get('car_type')
        plate_number = self.request.query_params.get('plate_number')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        is_overdue = self.request.query_params.get('is_overdue')

        if status_filter:
            if ',' in status_filter:
                status_list = status_filter.split(',')
                queryset = queryset.filter(status__in=status_list)
            else:
                queryset = queryset.filter(status=status_filter)
        if customer_name:
            queryset = queryset.filter(customer__name__icontains=customer_name)
        if customer_phone:
            queryset = queryset.filter(customer__phone__icontains=customer_phone)
        if car_brand:
            queryset = queryset.filter(car__brand__icontains=car_brand)
        if car_model:
            queryset = queryset.filter(car__model__icontains=car_model)
        if car_type:
            queryset = queryset.filter(car__car_type__icontains=car_type)
        if plate_number:
            queryset = queryset.filter(car__plate_number__icontains=plate_number)
        if start_date:
            queryset = queryset.filter(start_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(end_date__lte=end_date)
        if is_overdue == 'true':
            today = timezone.now().date()
            queryset = queryset.filter(status='picked_up', end_date__lt=today)

        return queryset.order_by('-id')

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        from django.db.models import Sum, Count

        total_orders = Order.objects.count()
        pending_orders = Order.objects.filter(status='pending').count()
        picked_up_orders = Order.objects.filter(status='picked_up').count()
        returned_orders = Order.objects.filter(status='returned').count()
        cancelled_orders = Order.objects.filter(status='cancelled').count()

        today = timezone.now().date()
        overdue_orders = Order.objects.filter(
            status='picked_up',
            end_date__lt=today
        ).count()

        total_revenue = Order.objects.filter(
            status='returned'
        ).aggregate(Sum('actual_amount'))['actual_amount__sum'] or 0

        total_overtime_fee = Order.objects.filter(
            status='returned'
        ).aggregate(Sum('overtime_fee'))['overtime_fee__sum'] or 0

        return Response({
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'picked_up_orders': picked_up_orders,
            'returned_orders': returned_orders,
            'cancelled_orders': cancelled_orders,
            'overdue_orders': overdue_orders,
            'total_revenue': float(total_revenue),
            'total_overtime_fee': float(total_overtime_fee),
        })

    @action(detail=False, methods=['post'], serializer_class=OrderPickUpSerializer)
    def pick_up(self, request):
        serializer = OrderPickUpSerializer(data=request.data)
        if serializer.is_valid():
            try:
                order = Order.objects.get(id=serializer.validated_data['order_id'])
                if order.pick_up_car():
                    return Response({
                        'message': '取车成功',
                        'order': OrderSerializer(order).data
                    })
                else:
                    return Response({
                        'message': '取车失败，订单状态不正确'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except Order.DoesNotExist:
                return Response({
                    'message': '订单不存在'
                }, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], serializer_class=OrderReturnSerializer)
    def return_car(self, request):
        serializer = OrderReturnSerializer(data=request.data)
        if serializer.is_valid():
            try:
                order = Order.objects.get(id=serializer.validated_data['order_id'])
                if order.return_car():
                    return Response({
                        'message': '还车成功',
                        'order': OrderSerializer(order).data
                    })
                else:
                    return Response({
                        'message': '还车失败，订单状态不正确'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except Order.DoesNotExist:
                return Response({
                    'message': '订单不存在'
                }, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], serializer_class=OrderCancelSerializer)
    def cancel(self, request):
        serializer = OrderCancelSerializer(data=request.data)
        if serializer.is_valid():
            try:
                order = Order.objects.get(id=serializer.validated_data['order_id'])
                if order.cancel_order():
                    return Response({
                        'message': '取消订单成功',
                        'order': OrderSerializer(order).data
                    })
                else:
                    return Response({
                        'message': '取消订单失败，订单状态不正确'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except Order.DoesNotExist:
                return Response({
                    'message': '订单不存在'
                }, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def pending(self, request):
        orders = Order.objects.filter(status='pending')
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def picked_up(self, request):
        orders = Order.objects.filter(status='picked_up')
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def returned(self, request):
        orders = Order.objects.filter(status='returned')
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def cancelled(self, request):
        orders = Order.objects.filter(status='cancelled')
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
