from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter, CharFilter, DateFilter
from django.db import models, transaction
from django.utils import timezone
from datetime import timedelta
from .models import Pet, Room, Order, FeedingRecord
from .serializers import (
    PetSerializer, RoomSerializer, OrderSerializer,
    OrderDetailSerializer, FeedingRecordSerializer,
    FeedingRecordBatchSerializer, ReminderOrderSerializer,
    OrderMarkReminderSerializer
)


class PetFilter(FilterSet):
    species = CharFilter(field_name='species', lookup_expr='exact')
    breed = CharFilter(field_name='breed', lookup_expr='icontains')
    min_age = NumberFilter(field_name='age', lookup_expr='gte')
    max_age = NumberFilter(field_name='age', lookup_expr='lte')
    size = CharFilter(field_name='size', lookup_expr='exact')
    
    class Meta:
        model = Pet
        fields = ['species', 'breed', 'min_age', 'max_age', 'owner_name', 'size']


class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all().order_by('-created_at')
    serializer_class = PetSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PetFilter
    search_fields = ['name', 'breed', 'owner_name', 'owner_phone']
    ordering_fields = ['created_at', 'age', 'name', 'weight']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        vaccine_warning = self.request.query_params.get('vaccine_warning')
        if vaccine_warning:
            warning_date = timezone.now().date() + timedelta(days=7)
            queryset = queryset.filter(vaccine_expiry__lte=warning_date)
        return queryset


class RoomFilter(FilterSet):
    room_type = CharFilter(field_name='room_type', lookup_expr='exact')
    suitable_size = CharFilter(field_name='suitable_size', lookup_expr='exact')
    min_price = NumberFilter(field_name='daily_price', lookup_expr='gte')
    max_price = NumberFilter(field_name='daily_price', lookup_expr='lte')
    
    class Meta:
        model = Room
        fields = ['room_type', 'status', 'min_price', 'max_price', 'suitable_size']


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all().order_by('room_number')
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = RoomFilter
    search_fields = ['room_number', 'description']
    ordering_fields = ['room_number', 'daily_price', 'max_pets']
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        available_rooms = Room.objects.filter(status='available', current_pets__lt=models.F('max_pets'))
        serializer = self.get_serializer(available_rooms, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def with_capacity(self, request):
        rooms = Room.objects.filter(current_pets__lt=models.F('max_pets'))
        serializer = self.get_serializer(rooms, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def suitable_for_pet(self, request):
        pet_id = request.query_params.get('pet_id')
        if not pet_id:
            return Response({'error': '请提供宠物ID'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            pet = Pet.objects.get(id=pet_id)
        except Pet.DoesNotExist:
            return Response({'error': '宠物不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        suitable_rooms = []
        for room in Room.objects.filter(status='available', current_pets__lt=models.F('max_pets')):
            if room.is_suitable_for_pet(pet):
                suitable_rooms.append(room)
        
        serializer = self.get_serializer(suitable_rooms, many=True)
        return Response(serializer.data)


class OrderFilter(FilterSet):
    status = CharFilter(field_name='status', lookup_expr='exact')
    room_type = CharFilter(field_name='room__room_type', lookup_expr='exact')
    pet_species = CharFilter(field_name='pet__species', lookup_expr='exact')
    pet_breed = CharFilter(field_name='pet__breed', lookup_expr='icontains')
    min_expected_days = NumberFilter(field_name='expected_days', lookup_expr='gte')
    max_expected_days = NumberFilter(field_name='expected_days', lookup_expr='lte')
    checkin_date_from = DateFilter(field_name='checkin_date', lookup_expr='date__gte')
    checkin_date_to = DateFilter(field_name='checkin_date', lookup_expr='date__lte')
    expected_checkout_date_from = DateFilter(field_name='expected_checkout_date', lookup_expr='date__gte')
    expected_checkout_date_to = DateFilter(field_name='expected_checkout_date', lookup_expr='date__lte')
    
    class Meta:
        model = Order
        fields = ['status', 'room_type', 'pet_species', 'pet_breed', 
                  'min_expected_days', 'max_expected_days',
                  'checkin_date_from', 'checkin_date_to',
                  'expected_checkout_date_from', 'expected_checkout_date_to']


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = OrderFilter
    search_fields = ['order_no', 'pet__name', 'pet__owner_name']
    ordering_fields = ['created_at', 'checkin_date', 'expected_days', 'total_amount', 'expected_checkout_date']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        min_stay_days = self.request.query_params.get('min_stay_days')
        max_stay_days = self.request.query_params.get('max_stay_days')
        
        if min_stay_days or max_stay_days:
            orders_with_duration = []
            for order in queryset:
                duration = order.get_stay_duration_days()
                if duration is not None:
                    if min_stay_days and duration < int(min_stay_days):
                        continue
                    if max_stay_days and duration > int(max_stay_days):
                        continue
                    orders_with_duration.append(order.id)
            queryset = queryset.filter(id__in=orders_with_duration)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def checkin(self, request, pk=None):
        order = self.get_object()
        try:
            order.checkin()
            serializer = OrderDetailSerializer(order)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        order = self.get_object()
        try:
            order.checkout()
            serializer = OrderDetailSerializer(order)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        order = self.get_object()
        try:
            order.complete()
            serializer = OrderDetailSerializer(order)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        try:
            order.cancel()
            serializer = OrderDetailSerializer(order)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def auto_assign_room(self, request, pk=None):
        order = self.get_object()
        try:
            success, message = order.auto_assign_room()
            if success:
                serializer = OrderDetailSerializer(order)
                return Response({'success': True, 'message': message, 'order': serializer.data})
            return Response({'success': False, 'message': message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def pending_checkin(self, request):
        orders = Order.objects.filter(status='pending_checkin').order_by('-created_at')
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def in_care(self, request):
        orders = Order.objects.filter(status='in_care').order_by('-created_at')
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending_pickup(self, request):
        orders = Order.objects.filter(status='pending_pickup').order_by('-created_at')
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def completed(self, request):
        orders = Order.objects.filter(status='completed').order_by('-created_at')
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def needing_reminder(self, request):
        days_threshold = int(request.query_params.get('days', 3))
        orders = Order.get_orders_needing_reminder(days_threshold=days_threshold).order_by('expected_checkout_date')
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = ReminderOrderSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ReminderOrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_reminder(self, request, pk=None):
        order = self.get_object()
        serializer = OrderMarkReminderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        reminder_status = serializer.validated_data.get('status', 'sent')
        
        if reminder_status == 'sent':
            order.mark_reminder_sent()
        elif reminder_status == 'confirmed':
            order.reminder_status = 'confirmed'
            order.save()
        
        return Response({
            'success': True, 
            'message': f'提醒状态已更新为{order.get_reminder_status_display()}',
            'reminder_status': order.reminder_status
        })


class FeedingRecordFilter(FilterSet):
    record_date_from = DateFilter(field_name='record_date', lookup_expr='gte')
    record_date_to = DateFilter(field_name='record_date', lookup_expr='lte')
    
    class Meta:
        model = FeedingRecord
        fields = ['order', 'record_date_from', 'record_date_to', 'created_by']


class FeedingRecordViewSet(viewsets.ModelViewSet):
    queryset = FeedingRecord.objects.all().order_by('-record_date')
    serializer_class = FeedingRecordSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = FeedingRecordFilter
    search_fields = ['created_by', 'health_notes']
    ordering_fields = ['record_date', 'created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        order_id = self.request.query_params.get('order_id')
        if order_id:
            queryset = queryset.filter(order_id=order_id)
        return queryset
    
    @action(detail=False, methods=['post'])
    def batch_import(self, request):
        serializer = FeedingRecordBatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        order_id = serializer.validated_data['order_id']
        records_data = serializer.validated_data['records']
        
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'error': '订单不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        created_records = []
        errors = []
        
        with transaction.atomic():
            for record_data in records_data:
                try:
                    record_date = record_data['record_date']
                    if record_date > timezone.now().date():
                        errors.append(f'日期 {record_date}: 记录日期不能晚于今天')
                        continue
                    
                    existing = FeedingRecord.objects.filter(order=order, record_date=record_date).first()
                    if existing:
                        errors.append(f'日期 {record_date}: 该日期的记录已存在')
                        continue
                    
                    record = FeedingRecord.objects.create(
                        order=order,
                        **record_data
                    )
                    created_records.append(record)
                except Exception as e:
                    errors.append(f'日期 {record_date}: {str(e)}')
        
        result_serializer = FeedingRecordSerializer(created_records, many=True)
        
        return Response({
            'success_count': len(created_records),
            'error_count': len(errors),
            'errors': errors,
            'records': result_serializer.data
        })
