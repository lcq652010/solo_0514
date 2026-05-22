from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta

from .models import (
    Exhibition,
    Booth,
    Company,
    Booking,
    ConstructionDemand,
    ProgressTracker,
    Payment,
    Builder,
    ConstructionConfirm,
    ProgressStepTemplate,
    ProgressStep,
)
from .serializers import (
    ExhibitionSerializer,
    BoothSerializer,
    CompanySerializer,
    BookingSerializer,
    ConstructionDemandSerializer,
    ProgressTrackerSerializer,
    PaymentSerializer,
    BuilderSerializer,
    ConstructionConfirmSerializer,
    ProgressStepTemplateSerializer,
    ProgressStepSerializer,
)


class ExhibitionViewSet(viewsets.ModelViewSet):
    queryset = Exhibition.objects.all()
    serializer_class = ExhibitionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class BuilderViewSet(viewsets.ModelViewSet):
    queryset = Builder.objects.all()
    serializer_class = BuilderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        specialty = self.request.query_params.get('specialty')
        is_active = self.request.query_params.get('is_active')
        
        if specialty:
            queryset = queryset.filter(specialty=specialty)
        if is_active is not None:
            queryset = queryset.filter(is_active=(is_active.lower() == 'true'))
        return queryset

    @action(detail=False, methods=['get'])
    def available(self, request):
        specialty = request.query_params.get('specialty')
        builders = Builder.objects.filter(is_active=True)
        if specialty:
            builders = builders.filter(specialty=specialty)
        serializer = self.get_serializer(builders, many=True)
        return Response(serializer.data)


class ProgressStepTemplateViewSet(viewsets.ModelViewSet):
    queryset = ProgressStepTemplate.objects.all()
    serializer_class = ProgressStepTemplateSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        step_type = self.request.query_params.get('step_type')
        if step_type:
            queryset = queryset.filter(step_type=step_type)
        return queryset


class ProgressStepViewSet(viewsets.ModelViewSet):
    queryset = ProgressStep.objects.all()
    serializer_class = ProgressStepSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        construction_id = self.request.query_params.get('construction_id')
        status = self.request.query_params.get('status')
        
        if construction_id:
            queryset = queryset.filter(construction_id=construction_id)
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    @action(detail=True, methods=['post'])
    def report(self, request, pk=None):
        step = self.get_object()
        report_content = request.data.get('report_content', '')
        reported_by = request.data.get('reported_by', '')
        status = request.data.get('status', 'in_progress')
        progress_percent = request.data.get('progress_percent', step.progress_percent)

        step.report_content = report_content
        step.reported_by = reported_by
        step.status = status
        step.progress_percent = int(progress_percent)
        
        if status == 'completed':
            step.progress_percent = 100
            step.reported_at = timezone.now()
        
        step.save()

        if step.status == 'completed':
            construction = step.construction
            total_steps = construction.steps.count()
            completed_steps = construction.steps.filter(status='completed').count()
            if total_steps > 0 and total_steps == completed_steps:
                construction.status = 'completed'
                construction.save()

        serializer = self.get_serializer(step)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def init_steps(self, request):
        construction_id = request.data.get('construction_id')
        step_type = request.data.get('step_type', 'standard')

        if not construction_id:
            return Response(
                {'error': '请提供 construction_id 参数'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            construction = ConstructionDemand.objects.get(id=construction_id)
        except ConstructionDemand.DoesNotExist:
            return Response(
                {'error': '搭建需求不存在'},
                status=status.HTTP_404_NOT_FOUND
            )

        templates = ProgressStepTemplate.objects.filter(step_type=step_type).order_by('step_order')
        if not templates.exists():
            templates = ProgressStepTemplate.objects.filter(step_type='standard').order_by('step_order')

        with transaction.atomic():
            ProgressStep.objects.filter(construction=construction).delete()
            
            for template in templates:
                ProgressStep.objects.create(
                    construction=construction,
                    step_name=template.step_name,
                    step_desc=template.step_desc,
                    step_order=template.step_order,
                    progress_percent=0,
                    status='pending'
                )

        steps = ProgressStep.objects.filter(construction=construction).order_by('step_order')
        serializer = self.get_serializer(steps, many=True)
        return Response(serializer.data)


class BoothViewSet(viewsets.ModelViewSet):
    queryset = Booth.objects.all()
    serializer_class = BoothSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        exhibition_id = self.request.query_params.get('exhibition_id')
        zone = self.request.query_params.get('zone')
        booth_type = self.request.query_params.get('booth_type')
        status = self.request.query_params.get('status')
        min_area = self.request.query_params.get('min_area')
        max_area = self.request.query_params.get('max_area')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if exhibition_id:
            queryset = queryset.filter(exhibition_id=exhibition_id)
        if zone:
            queryset = queryset.filter(zone=zone)
        if booth_type:
            queryset = queryset.filter(booth_type=booth_type)
        if status:
            queryset = queryset.filter(status=status)
        if min_area:
            queryset = queryset.filter(area__gte=min_area)
        if max_area:
            queryset = queryset.filter(area__lte=max_area)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    @action(detail=False, methods=['get'])
    def available(self, request):
        queryset = self.get_queryset().filter(status='available')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_exhibition(self, request):
        exhibition_id = request.query_params.get('exhibition_id')
        if not exhibition_id:
            return Response(
                {'error': '请提供 exhibition_id 参数'},
                status=status.HTTP_400_BAD_REQUEST
            )
        booths = Booth.objects.filter(exhibition_id=exhibition_id)
        serializer = self.get_serializer(booths, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def zones(self, request):
        exhibition_id = request.query_params.get('exhibition_id')
        queryset = self.get_queryset()
        if exhibition_id:
            queryset = queryset.filter(exhibition_id=exhibition_id)
        zones = queryset.values('zone').distinct()
        return Response([{'zone': z['zone']} for z in zones])


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        industry = self.request.query_params.get('industry')
        if name:
            queryset = queryset.filter(name__icontains=name)
        if industry:
            queryset = queryset.filter(industry__icontains=industry)
        return queryset


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        exhibition_id = self.request.query_params.get('exhibition_id')
        company_id = self.request.query_params.get('company_id')
        status = self.request.query_params.get('status')
        zone = self.request.query_params.get('zone')
        booth_type = self.request.query_params.get('booth_type')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if exhibition_id:
            queryset = queryset.filter(booth__exhibition_id=exhibition_id)
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        if status:
            queryset = queryset.filter(status=status)
        if zone:
            queryset = queryset.filter(booth__zone=zone)
        if booth_type:
            queryset = queryset.filter(booth__booth_type=booth_type)
        if start_date:
            queryset = queryset.filter(booking_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(booking_date__lte=end_date)

        return queryset

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            booth_id = request.data.get('booth')
            booth = Booth.objects.select_for_update().get(id=booth_id)

            if booth.status != 'available':
                return Response(
                    {'error': '该展位已被预订或不可用'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            active_bookings = Booking.objects.filter(
                booth=booth,
                status__in=['pending', 'confirmed', 'deposit_paid', 'balance_paid']
            )
            if active_bookings.exists():
                return Response(
                    {'error': f'展位 {booth} 已被占用，无法重复预订'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            booth.status = 'reserved'
            booth.save()

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.status in ['balance_paid', 'completed']:
            return Response(
                {'error': '已支付尾款的订单无法取消'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            booking.status = 'cancelled'
            booking.save()
            booth = booking.booth
            booth.status = 'available'
            booth.save()

        return Response({'status': '订单已取消'})

    @action(detail=False, methods=['get'])
    def by_company(self, request):
        company_id = request.query_params.get('company_id')
        if not company_id:
            return Response(
                {'error': '请提供 company_id 参数'},
                status=status.HTTP_400_BAD_REQUEST
            )
        bookings = Booking.objects.filter(company_id=company_id)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        exhibition_id = request.query_params.get('exhibition_id')
        queryset = self.get_queryset()
        if exhibition_id:
            queryset = queryset.filter(booth__exhibition_id=exhibition_id)
        
        total = queryset.count()
        pending = queryset.filter(status='pending').count()
        confirmed = queryset.filter(status='confirmed').count()
        deposit_paid = queryset.filter(status='deposit_paid').count()
        balance_paid = queryset.filter(status='balance_paid').count()
        cancelled = queryset.filter(status='cancelled').count()
        
        return Response({
            'total': total,
            'pending': pending,
            'confirmed': confirmed,
            'deposit_paid': deposit_paid,
            'balance_paid': balance_paid,
            'cancelled': cancelled,
        })


class ConstructionConfirmViewSet(viewsets.ModelViewSet):
    queryset = ConstructionConfirm.objects.all()
    serializer_class = ConstructionConfirmSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        construction_id = self.request.query_params.get('construction_id')
        confirm_status = self.request.query_params.get('confirm_status')
        
        if construction_id:
            queryset = queryset.filter(construction_id=construction_id)
        if confirm_status:
            queryset = queryset.filter(confirm_status=confirm_status)
        return queryset

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        confirm = self.get_object()
        confirm_status = request.data.get('confirm_status', 'confirmed')
        company_remark = request.data.get('company_remark', '')
        confirmed_by = request.data.get('confirmed_by', '')

        confirm.confirm_status = confirm_status
        confirm.company_remark = company_remark
        confirm.confirmed_by = confirmed_by

        if confirm_status == 'confirmed':
            confirm.confirmed_at = timezone.now()
            confirm.construction.status = 'plan_confirmed'
            confirm.construction.save()

        confirm.save()
        serializer = self.get_serializer(confirm)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def generate_doc(self, request, pk=None):
        confirm = self.get_object()
        construction = confirm.construction
        booking = construction.booking
        company = booking.company
        booth = booking.booth

        doc_content = {
            'confirm_number': confirm.confirm_number,
            'plan_version': confirm.plan_version,
            'created_at': confirm.created_at,
            'order_number': booking.order_number,
            'company': {
                'name': company.name,
                'contact_person': company.contact_person,
                'phone': company.phone,
            },
            'booth': {
                'number': booth.booth_number,
                'zone': booth.zone,
                'type': booth.get_booth_type_display(),
                'area': str(booth.area),
            },
            'builder': {
                'name': construction.builder.name if construction.builder else '',
                'contact_person': construction.builder.contact_person if construction.builder else '',
            },
            'plan_desc': construction.plan_desc,
            'confirm_status': confirm.get_confirm_status_display(),
            'company_remark': confirm.company_remark,
            'confirmed_at': confirm.confirmed_at,
            'confirmed_by': confirm.confirmed_by,
        }

        return Response(doc_content)


class ConstructionDemandViewSet(viewsets.ModelViewSet):
    queryset = ConstructionDemand.objects.all()
    serializer_class = ConstructionDemandSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        exhibition_id = self.request.query_params.get('exhibition_id')
        status = self.request.query_params.get('status')
        builder_id = self.request.query_params.get('builder_id')
        company_id = self.request.query_params.get('company_id')

        if exhibition_id:
            queryset = queryset.filter(booking__booth__exhibition_id=exhibition_id)
        if status:
            queryset = queryset.filter(status=status)
        if builder_id:
            queryset = queryset.filter(builder_id=builder_id)
        if company_id:
            queryset = queryset.filter(booking__company_id=company_id)

        return queryset

    @action(detail=True, methods=['post'])
    def submit_plan(self, request, pk=None):
        demand = self.get_object()
        plan_desc = request.data.get('plan_desc', '')
        
        demand.plan_desc = plan_desc
        demand.status = 'plan_submitted'
        demand.save()

        ConstructionConfirm.objects.create(
            construction=demand,
            plan_version='V1.0',
            confirm_status='pending'
        )

        return Response({'status': '方案已提交，等待企业确认'})

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        demand = self.get_object()
        demand.status = 'approved'
        demand.review_remark = request.data.get('remark', '')
        demand.save()
        return Response({'status': '需求已批准'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        demand = self.get_object()
        demand.status = 'rejected'
        demand.review_remark = request.data.get('remark', '')
        demand.save()
        return Response({'status': '需求已拒绝'})

    @action(detail=True, methods=['post'])
    def start_construction(self, request, pk=None):
        demand = self.get_object()
        demand.status = 'in_progress'
        demand.save()
        return Response({'status': '已开始施工'})

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        demand = self.get_object()
        demand.status = 'completed'
        demand.save()
        return Response({'status': '搭建已完成'})

    @action(detail=True, methods=['post'])
    def reassign_builder(self, request, pk=None):
        demand = self.get_object()
        builder_id = request.data.get('builder_id')
        if not builder_id:
            return Response(
                {'error': '请提供 builder_id 参数'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            builder = Builder.objects.get(id=builder_id, is_active=True)
            demand.builder = builder
            demand.save()
            return Response({'status': '搭建商已重新分配', 'builder': builder.name})
        except Builder.DoesNotExist:
            return Response(
                {'error': '指定的搭建商不存在或未启用'},
                status=status.HTTP_404_NOT_FOUND
            )


class ProgressTrackerViewSet(viewsets.ModelViewSet):
    queryset = ProgressTracker.objects.all()
    serializer_class = ProgressTrackerSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        construction_id = self.request.query_params.get('construction_id')
        if construction_id:
            queryset = queryset.filter(construction_id=construction_id)
        return queryset

    @action(detail=False, methods=['get'])
    def by_construction(self, request):
        construction_id = request.query_params.get('construction_id')
        if not construction_id:
            return Response(
                {'error': '请提供 construction_id 参数'},
                status=status.HTTP_400_BAD_REQUEST
            )
        progresses = ProgressTracker.objects.filter(construction_id=construction_id)
        serializer = self.get_serializer(progresses, many=True)
        return Response(serializer.data)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        booking_id = self.request.query_params.get('booking_id')
        payment_type = self.request.query_params.get('payment_type')
        payment_method = self.request.query_params.get('payment_method')
        
        if booking_id:
            queryset = queryset.filter(booking_id=booking_id)
        if payment_type:
            queryset = queryset.filter(payment_type=payment_type)
        if payment_method:
            queryset = queryset.filter(payment_method=payment_method)
        
        return queryset

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            payment = serializer.instance
            booking = payment.booking

            if payment.payment_type == 'deposit':
                booking.status = 'deposit_paid'
                booking.booth.status = 'paid'
                booking.booth.save()
            elif payment.payment_type == 'balance':
                booking.status = 'balance_paid'

            booking.save()

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'])
    def by_booking(self, request):
        booking_id = request.query_params.get('booking_id')
        if not booking_id:
            return Response(
                {'error': '请提供 booking_id 参数'},
                status=status.HTTP_400_BAD_REQUEST
            )
        payments = Payment.objects.filter(booking_id=booking_id)
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        exhibition_id = request.query_params.get('exhibition_id')
        queryset = self.get_queryset()
        if exhibition_id:
            queryset = queryset.filter(booking__booth__exhibition_id=exhibition_id)
        
        total_amount = sum(payment.amount for payment in queryset)
        deposit_result = queryset.filter(payment_type='deposit').aggregate(total=Sum('amount'))
        balance_result = queryset.filter(payment_type='balance').aggregate(total=Sum('amount'))
        
        deposit_total = float(deposit_result['total'] or 0)
        balance_total = float(balance_result['total'] or 0)
        
        return Response({
            'total_amount': float(total_amount),
            'deposit_total': deposit_total,
            'balance_total': balance_total,
        })


class SalesDashboardViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def overview(self, request):
        exhibition_id = request.query_params.get('exhibition_id')
        
        booths = Booth.objects.all()
        bookings = Booking.objects.all()
        
        if exhibition_id:
            booths = booths.filter(exhibition_id=exhibition_id)
            bookings = bookings.filter(booth__exhibition_id=exhibition_id)

        total_booths = booths.count()
        booked_booths = booths.filter(status__in=['reserved', 'paid', 'occupied']).count()
        available_booths = booths.filter(status='available').count()

        booking_result = bookings.aggregate(total=Sum('total_amount'))
        total_sales = float(booking_result['total'] or 0)

        return Response({
            'total_booths': total_booths,
            'booked_booths': booked_booths,
            'available_booths': available_booths,
            'booking_rate': round(booked_booths / total_booths * 100, 2) if total_booths > 0 else 0,
            'total_sales': total_sales,
        })

    @action(detail=False, methods=['get'])
    def by_zone(self, request):
        exhibition_id = request.query_params.get('exhibition_id')
        
        booths = Booth.objects.all()
        if exhibition_id:
            booths = booths.filter(exhibition_id=exhibition_id)

        zones = booths.values('zone').annotate(
            total=Count('id'),
            booked=Count('id', filter=Q(status__in=['reserved', 'paid', 'occupied'])),
            available=Count('id', filter=Q(status='available')),
            sales=Sum('booking__total_amount')
        ).order_by('zone')

        result = []
        for zone in zones:
            booking_rate = round(zone['booked'] / zone['total'] * 100, 2) if zone['total'] > 0 else 0
            result.append({
                'zone': zone['zone'],
                'zone_name': dict(Booth.ZONE_CHOICES).get(zone['zone'], zone['zone']),
                'total': zone['total'],
                'booked': zone['booked'],
                'available': zone['available'],
                'booking_rate': booking_rate,
                'sales': float(zone['sales'] or 0),
            })

        return Response(result)

    @action(detail=False, methods=['get'])
    def by_booth_type(self, request):
        exhibition_id = request.query_params.get('exhibition_id')
        
        booths = Booth.objects.all()
        if exhibition_id:
            booths = booths.filter(exhibition_id=exhibition_id)

        types = booths.values('booth_type').annotate(
            total=Count('id'),
            booked=Count('id', filter=Q(status__in=['reserved', 'paid', 'occupied'])),
            available=Count('id', filter=Q(status='available')),
            sales=Sum('booking__total_amount')
        ).order_by('booth_type')

        result = []
        for t in types:
            booking_rate = round(t['booked'] / t['total'] * 100, 2) if t['total'] > 0 else 0
            result.append({
                'booth_type': t['booth_type'],
                'booth_type_name': dict(Booth.BOOTH_TYPE_CHOICES).get(t['booth_type'], t['booth_type']),
                'total': t['total'],
                'booked': t['booked'],
                'available': t['available'],
                'booking_rate': booking_rate,
                'sales': float(t['sales'] or 0),
            })

        return Response(result)

    @action(detail=False, methods=['get'])
    def sales_trend(self, request):
        exhibition_id = request.query_params.get('exhibition_id')
        days = int(request.query_params.get('days', 7))

        bookings = Booking.objects.all()
        if exhibition_id:
            bookings = bookings.filter(booth__exhibition_id=exhibition_id)

        trend_data = []
        for i in range(days - 1, -1, -1):
            date = timezone.now().date() - timedelta(days=i)
            day_bookings = bookings.filter(booking_date__date=date)
            daily_sales = day_bookings.aggregate(total=Sum('total_amount'))['total'] or 0
            
            trend_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'booking_count': day_bookings.count(),
                'sales': float(daily_sales),
            })

        return Response(trend_data)

    @action(detail=False, methods=['get'])
    def payment_stats(self, request):
        exhibition_id = request.query_params.get('exhibition_id')
        
        payments = Payment.objects.all()
        if exhibition_id:
            payments = payments.filter(booking__booth__exhibition_id=exhibition_id)

        by_type = payments.values('payment_type').annotate(
            count=Count('id'),
            amount=Sum('amount')
        )

        by_method = payments.values('payment_method').annotate(
            count=Count('id'),
            amount=Sum('amount')
        )

        return Response({
            'by_type': [
                {
                    'type': t['payment_type'],
                    'type_name': dict(Payment.PAYMENT_TYPE_CHOICES).get(t['payment_type'], t['payment_type']),
                    'count': t['count'],
                    'amount': float(t['amount'] or 0),
                } for t in by_type
            ],
            'by_method': [
                {
                    'method': m['payment_method'],
                    'method_name': dict(Payment.PAYMENT_METHOD_CHOICES).get(m['payment_method'], m['payment_method']),
                    'count': m['count'],
                    'amount': float(m['amount'] or 0),
                } for m in by_method
            ],
        })
