from django.db import models
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from .models import FeeStandard, Bill, MeterReading
from .serializers import FeeStandardSerializer, BillSerializer, MeterReadingSerializer
from owners.models import House, Owner


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class FeeStandardViewSet(viewsets.ModelViewSet):
    queryset = FeeStandard.objects.all().order_by('-create_time')
    serializer_class = FeeStandardSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        fee_type = self.request.query_params.get('fee_type')
        is_active = self.request.query_params.get('is_active')
        if fee_type:
            queryset = queryset.filter(fee_type=fee_type)
        if is_active is not None:
            queryset = queryset.filter(is_active=(is_active == 'true'))
        return queryset


class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all().order_by('-create_time')
    serializer_class = BillSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        owner_id = self.request.query_params.get('owner_id')
        house_id = self.request.query_params.get('house_id')
        room_number = self.request.query_params.get('room_number')
        building_id = self.request.query_params.get('building_id')
        bill_type = self.request.query_params.get('bill_type')
        status_filter = self.request.query_params.get('status')
        billing_month = self.request.query_params.get('billing_month')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if owner_id:
            queryset = queryset.filter(owner_id=owner_id)
        if house_id:
            queryset = queryset.filter(house_id=house_id)
        if room_number:
            queryset = queryset.filter(house__room_number__contains=room_number)
        if building_id:
            queryset = queryset.filter(house__building_id=building_id)
        if bill_type:
            queryset = queryset.filter(bill_type=bill_type)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if billing_month:
            queryset = queryset.filter(billing_month=billing_month)
        if start_date:
            queryset = queryset.filter(create_time__gte=start_date)
        if end_date:
            queryset = queryset.filter(create_time__lte=f'{end_date} 23:59:59')
        return queryset

    @action(detail=False, methods=['get'])
    def by_owner(self, request):
        owner_id = request.query_params.get('owner_id')
        status_filter = request.query_params.get('status')
        if owner_id:
            bills = self.queryset.filter(owner_id=owner_id)
            if status_filter:
                bills = bills.filter(status=status_filter)
            page = self.paginate_queryset(bills)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(bills, many=True)
            return Response(serializer.data)
        return Response({'error': 'owner_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def by_house(self, request):
        house_id = request.query_params.get('house_id')
        if house_id:
            bills = self.queryset.filter(house_id=house_id)
            page = self.paginate_queryset(bills)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(bills, many=True)
            return Response(serializer.data)
        return Response({'error': 'house_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        billing_month = request.query_params.get('billing_month')
        query = self.queryset
        if billing_month:
            query = query.filter(billing_month=billing_month)
        
        total_amount = query.aggregate(total=models.Sum('amount'))['total'] or 0
        paid_amount = query.filter(status='paid').aggregate(total=models.Sum('amount'))['total'] or 0
        unpaid_amount = query.filter(status='unpaid').aggregate(total=models.Sum('amount'))['total'] or 0
        
        return Response({
            'total_amount': total_amount,
            'paid_amount': paid_amount,
            'unpaid_amount': unpaid_amount,
            'total_count': query.count(),
            'paid_count': query.filter(status='paid').count(),
            'unpaid_count': query.filter(status='unpaid').count(),
        })

    @action(detail=False, methods=['post'])
    def generate_property_fees(self, request):
        billing_month = request.data.get('billing_month')
        fee_standard_id = request.data.get('fee_standard_id')
        
        if not billing_month or not fee_standard_id:
            return Response({'error': 'billing_month and fee_standard_id are required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            fee_standard = FeeStandard.objects.get(id=fee_standard_id, fee_type='property')
        except FeeStandard.DoesNotExist:
            return Response({'error': 'Invalid fee standard'}, status=status.HTTP_400_BAD_REQUEST)
        
        year, month = map(int, billing_month.split('-'))
        start_date = date(year, month, 1)
        end_date = start_date + relativedelta(months=1) - timedelta(days=1)
        due_date = end_date + timedelta(days=15)
        
        houses = House.objects.filter(status='owned')
        created_count = 0
        
        for house in houses:
            existing_bill = Bill.objects.filter(
                house=house,
                bill_type='property',
                billing_month=billing_month
            ).first()
            
            if existing_bill:
                continue
            
            owner = Owner.objects.filter(house=house, status='normal').first()
            if not owner:
                continue
            
            amount = house.area * fee_standard.unit_price
            
            Bill.objects.create(
                house=house,
                owner=owner,
                bill_type='property',
                title=f'{billing_month}物业费',
                amount=amount,
                billing_month=billing_month,
                start_date=start_date,
                end_date=end_date,
                unit_price=fee_standard.unit_price,
                due_date=due_date
            )
            created_count += 1
        
        return Response({'created_count': created_count, 'message': f'成功生成{created_count}条物业费账单'})

    @action(detail=False, methods=['post'])
    def generate_utility_fees(self, request):
        billing_month = request.data.get('billing_month')
        
        if not billing_month:
            return Response({'error': 'billing_month is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        meter_readings = MeterReading.objects.filter(billing_month=billing_month)
        created_count = 0
        
        for reading in meter_readings:
            bill_type = reading.reading_type
            try:
                fee_standard = FeeStandard.objects.get(fee_type=bill_type, is_active=True)
            except FeeStandard.DoesNotExist:
                continue
            
            existing_bill = Bill.objects.filter(
                house=reading.house,
                bill_type=bill_type,
                billing_month=billing_month
            ).first()
            
            if existing_bill:
                continue
            
            owner = Owner.objects.filter(house=reading.house, status='normal').first()
            if not owner:
                continue
            
            amount = reading.usage * fee_standard.unit_price
            
            year, month = map(int, billing_month.split('-'))
            start_date = date(year, month, 1)
            end_date = start_date + relativedelta(months=1) - timedelta(days=1)
            due_date = end_date + timedelta(days=15)
            
            Bill.objects.create(
                house=reading.house,
                owner=owner,
                bill_type=bill_type,
                title=f'{billing_month}{"水费" if bill_type == "water" else "电费"}',
                amount=amount,
                billing_month=billing_month,
                start_date=start_date,
                end_date=end_date,
                usage=reading.usage,
                unit_price=fee_standard.unit_price,
                due_date=due_date
            )
            created_count += 1
        
        return Response({'created_count': created_count, 'message': f'成功生成{created_count}条水电费账单'})


class MeterReadingViewSet(viewsets.ModelViewSet):
    queryset = MeterReading.objects.all().order_by('-reading_date')
    serializer_class = MeterReadingSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        house_id = self.request.query_params.get('house_id')
        room_number = self.request.query_params.get('room_number')
        building_id = self.request.query_params.get('building_id')
        reading_type = self.request.query_params.get('reading_type')
        billing_month = self.request.query_params.get('billing_month')

        if house_id:
            queryset = queryset.filter(house_id=house_id)
        if room_number:
            queryset = queryset.filter(house__room_number__contains=room_number)
        if building_id:
            queryset = queryset.filter(house__building_id=building_id)
        if reading_type:
            queryset = queryset.filter(reading_type=reading_type)
        if billing_month:
            queryset = queryset.filter(billing_month=billing_month)
        return queryset

    @action(detail=False, methods=['get'])
    def by_house(self, request):
        house_id = request.query_params.get('house_id')
        reading_type = request.query_params.get('type')
        if house_id:
            readings = self.queryset.filter(house_id=house_id)
            if reading_type:
                readings = readings.filter(reading_type=reading_type)
            page = self.paginate_queryset(readings)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(readings, many=True)
            return Response(serializer.data)
        return Response({'error': 'house_id is required'}, status=status.HTTP_400_BAD_REQUEST)
