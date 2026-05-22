from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Shop, Product, Rider, Order, OrderItem, DeliveryTracking
from .serializers import (
    ShopSerializer, ProductSerializer, RiderSerializer,
    OrderSerializer, OrderCreateSerializer, DeliveryTrackingSerializer
)


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'code': 200,
            'message': 'success',
            'data': {
                'total': self.page.paginator.count,
                'total_pages': self.page.paginator.num_pages,
                'current_page': self.page.number,
                'page_size': self.get_page_size(self.request),
                'results': data
            }
        })


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        is_open = self.request.query_params.get('is_open')
        if is_open is not None:
            queryset = queryset.filter(is_open=(is_open.lower() == 'true'))
        return queryset


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        shop_id = self.request.query_params.get('shop_id')
        if shop_id:
            queryset = queryset.filter(shop_id=shop_id)
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        is_available = self.request.query_params.get('is_available')
        if is_available is not None:
            queryset = queryset.filter(is_available=(is_available.lower() == 'true'))
        min_price = self.request.query_params.get('min_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        max_price = self.request.query_params.get('max_price')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        has_stock = self.request.query_params.get('has_stock')
        if has_stock and has_stock.lower() == 'true':
            queryset = queryset.filter(stock__gt=0)
        return queryset.order_by('-id')


class RiderViewSet(viewsets.ModelViewSet):
    queryset = Rider.objects.all()
    serializer_class = RiderSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        phone = self.request.query_params.get('phone')
        if phone:
            queryset = queryset.filter(phone__icontains=phone)
        is_available = self.request.query_params.get('is_available')
        if is_available is not None:
            queryset = queryset.filter(is_available=(is_available.lower() == 'true'))
        vehicle_type = self.request.query_params.get('vehicle_type')
        if vehicle_type:
            queryset = queryset.filter(vehicle_type=vehicle_type)
        return queryset

    @action(detail=False, methods=['get'])
    def available(self, request):
        available_riders = Rider.objects.filter(is_available=True)
        serializer = self.get_serializer(available_riders, many=True)
        return Response({
            'code': 200,
            'message': 'success',
            'data': serializer.data
        })


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        order_no = self.request.query_params.get('order_no')
        if order_no:
            queryset = queryset.filter(order_no__icontains=order_no)
        
        customer_name = self.request.query_params.get('customer_name')
        if customer_name:
            queryset = queryset.filter(customer_name__icontains=customer_name)
        
        customer_phone = self.request.query_params.get('customer_phone')
        if customer_phone:
            queryset = queryset.filter(customer_phone__icontains=customer_phone)
        
        status = self.request.query_params.get('status')
        if status:
            status_list = status.split(',')
            queryset = queryset.filter(status__in=status_list)
        
        shop_id = self.request.query_params.get('shop_id')
        if shop_id:
            queryset = queryset.filter(shop_id=shop_id)
        
        rider_id = self.request.query_params.get('rider_id')
        if rider_id:
            queryset = queryset.filter(rider_id=rider_id)
        
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(
                items__product__category__icontains=category
            ).distinct()
        
        min_amount = self.request.query_params.get('min_amount')
        if min_amount:
            queryset = queryset.filter(total_amount__gte=min_amount)
        
        max_amount = self.request.query_params.get('max_amount')
        if max_amount:
            queryset = queryset.filter(total_amount__lte=max_amount)
        
        start_date = self.request.query_params.get('start_date')
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        
        end_date = self.request.query_params.get('end_date')
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)
        
        return queryset.order_by('-created_at')

    @action(detail=True, methods=['post'])
    def assign_rider(self, request, pk=None):
        order = self.get_object()
        if order.status != 'pending':
            return Response(
                {'code': 400, 'message': '只有待接单状态的订单才能分配骑手', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )

        rider_id = request.data.get('rider_id')
        if not rider_id:
            return Response(
                {'code': 400, 'message': '请选择骑手', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            rider = Rider.objects.get(id=rider_id)
        except Rider.DoesNotExist:
            return Response(
                {'code': 404, 'message': '骑手不存在', 'data': None},
                status=status.HTTP_404_NOT_FOUND
            )

        if not rider.is_available:
            return Response(
                {'code': 400, 'message': '该骑手当前不在岗', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.rider = rider
        order.status = 'delivering'
        order.accepted_at = timezone.now()
        order.save()

        rider.current_order_count += 1
        rider.save()

        DeliveryTracking.objects.create(
            order=order,
            rider=rider,
            status='已接单',
            description='骑手已接单，正在前往店铺'
        )

        serializer = self.get_serializer(order)
        return Response({
            'code': 200,
            'message': '派单成功',
            'data': serializer.data
        })

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        order = self.get_object()
        if order.status != 'delivering':
            return Response(
                {'code': 400, 'message': '只有配送中的订单才能完成', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = 'completed'
        order.completed_at = timezone.now()
        order.save()

        if order.rider:
            order.rider.current_order_count -= 1
            order.rider.save()

        DeliveryTracking.objects.create(
            order=order,
            rider=order.rider,
            status='已完成',
            description='订单已送达，配送完成'
        )

        serializer = self.get_serializer(order)
        return Response({
            'code': 200,
            'message': '订单完成',
            'data': serializer.data
        })

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status in ['completed', 'cancelled']:
            return Response(
                {'code': 400, 'message': '该订单状态无法取消', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )

        for item in order.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()

        order.status = 'cancelled'
        order.cancelled_at = timezone.now()
        order.save()

        if order.rider:
            order.rider.current_order_count -= 1
            order.rider.save()

        serializer = self.get_serializer(order)
        return Response({
            'code': 200,
            'message': '订单已取消',
            'data': serializer.data
        })

    @action(detail=True, methods=['post'])
    def update_tracking(self, request, pk=None):
        order = self.get_object()
        if order.status != 'delivering':
            return Response(
                {'code': 400, 'message': '只有配送中的订单才能更新配送信息', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not order.rider:
            return Response(
                {'code': 400, 'message': '该订单还没有分配骑手', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )

        tracking_data = {
            'order': order,
            'rider': order.rider,
            'status': request.data.get('status', '配送中'),
            'description': request.data.get('description', ''),
            'latitude': request.data.get('latitude'),
            'longitude': request.data.get('longitude'),
        }

        tracking = DeliveryTracking.objects.create(**tracking_data)
        serializer = DeliveryTrackingSerializer(tracking)
        return Response({
            'code': 200,
            'message': '更新成功',
            'data': serializer.data
        })

    @action(detail=True, methods=['get'])
    def tracking(self, request, pk=None):
        order = self.get_object()
        tracking_records = order.tracking_records.all()
        serializer = DeliveryTrackingSerializer(tracking_records, many=True)
        return Response({
            'code': 200,
            'message': 'success',
            'data': serializer.data
        })


class DeliveryTrackingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DeliveryTracking.objects.all()
    serializer_class = DeliveryTrackingSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        order_id = self.request.query_params.get('order_id')
        if order_id:
            queryset = queryset.filter(order_id=order_id)
        rider_id = self.request.query_params.get('rider_id')
        if rider_id:
            queryset = queryset.filter(rider_id=rider_id)
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status__icontains=status)
        return queryset.order_by('-created_at')
