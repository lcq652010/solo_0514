from django.db import models
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from datetime import datetime
from .models import Payment
from .serializers import PaymentSerializer
from bills.models import Bill


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by('-create_time')
    serializer_class = PaymentSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        owner_id = self.request.query_params.get('owner_id')
        room_number = self.request.query_params.get('room_number')
        building_id = self.request.query_params.get('building_id')
        payment_method = self.request.query_params.get('payment_method')
        status_filter = self.request.query_params.get('status')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if owner_id:
            queryset = queryset.filter(owner_id=owner_id)
        if room_number:
            queryset = queryset.filter(bill__house__room_number__contains=room_number)
        if building_id:
            queryset = queryset.filter(bill__house__building_id=building_id)
        if payment_method:
            queryset = queryset.filter(payment_method=payment_method)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if start_date:
            queryset = queryset.filter(paid_time__gte=start_date)
        if end_date:
            queryset = queryset.filter(paid_time__lte=f'{end_date} 23:59:59')
        return queryset

    def generate_payment_no(self):
        return f'PAY{datetime.now().strftime("%Y%m%d%H%M%S")}'

    @action(detail=False, methods=['get'])
    def by_owner(self, request):
        owner_id = request.query_params.get('owner_id')
        status_filter = request.query_params.get('status')
        if owner_id:
            payments = self.queryset.filter(owner_id=owner_id)
            if status_filter:
                payments = payments.filter(status=status_filter)
            page = self.paginate_queryset(payments)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(payments, many=True)
            return Response(serializer.data)
        return Response({'error': 'owner_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def create_payment(self, request):
        bill_ids = request.data.get('bill_ids', [])
        payment_method = request.data.get('payment_method', 'other')
        operator = request.data.get('operator', '')

        if not bill_ids:
            return Response({'error': 'bill_ids is required'}, status=status.HTTP_400_BAD_REQUEST)

        bills = Bill.objects.filter(id__in=bill_ids)
        if not bills.exists():
            return Response({'error': 'No valid bills found'}, status=status.HTTP_400_BAD_REQUEST)

        paid_bills = bills.filter(status='paid')
        if paid_bills.exists():
            paid_bill_titles = [b.title for b in paid_bills]
            return Response({
                'error': '存在已缴费账单，请勿重复支付',
                'paid_bills': paid_bill_titles
            }, status=status.HTTP_400_BAD_REQUEST)

        unpaid_bills = bills.filter(status='unpaid')
        if not unpaid_bills.exists():
            return Response({'error': '没有待缴费账单'}, status=status.HTTP_400_BAD_REQUEST)

        total_amount = unpaid_bills.aggregate(total=models.Sum('amount'))['total'] or 0

        if total_amount <= 0:
            return Response({'error': '缴费金额必须大于0'}, status=status.HTTP_400_BAD_REQUEST)

        owner = unpaid_bills.first().owner

        payment = Payment.objects.create(
            owner=owner,
            payment_no=self.generate_payment_no(),
            amount=total_amount,
            payment_method=payment_method,
            status='success',
            operator=operator,
            paid_time=datetime.now()
        )

        unpaid_bills.update(status='paid')
        payment.bill = unpaid_bills.first()
        payment.save()

        serializer = self.get_serializer(payment)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        query = self.queryset.filter(status='success')
        if start_date:
            query = query.filter(paid_time__gte=start_date)
        if end_date:
            query = query.filter(paid_time__lte=f'{end_date} 23:59:59')
        
        total_amount = query.aggregate(total=models.Sum('amount'))['total'] or 0
        
        by_method = {}
        for method in ['alipay', 'wechat', 'bank', 'cash', 'other']:
            method_total = query.filter(payment_method=method).aggregate(
                total=models.Sum('amount')
            )['total'] or 0
            by_method[method] = method_total
        
        return Response({
            'total_amount': total_amount,
            'total_count': query.count(),
            'by_method': by_method
        })
