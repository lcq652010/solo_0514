from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum, Q
from datetime import date, datetime

from .models import VenueType, Venue, Booking, TimeSlot, Payment
from .serializers import (
    UserSerializer, VenueTypeSerializer, VenueSerializer,
    BookingSerializer, BookingCheckInSerializer, BookingCheckOutSerializer,
    BookingVerifySerializer, TimeSlotCheckSerializer, VenueAvailabilitySerializer,
    ScanQrCodeSerializer, CurrentUsageSerializer,
    TimeSlotSerializer, PaymentSerializer, PaymentCreateSerializer,
    DashboardStatsSerializer
)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class VenueTypeViewSet(viewsets.ModelViewSet):
    queryset = VenueType.objects.all()
    serializer_class = VenueTypeSerializer


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        venue_type_id = self.request.query_params.get('venue_type')
        sport_type = self.request.query_params.get('sport_type')
        size = self.request.query_params.get('size')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if venue_type_id:
            queryset = queryset.filter(venue_type_id=venue_type_id)
        if sport_type:
            queryset = queryset.filter(venue_type__sport_type=sport_type)
        if size:
            queryset = queryset.filter(size=size)
        if min_price:
            queryset = queryset.filter(price_per_hour__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_hour__lte=max_price)

        return queryset

    @action(detail=False, methods=['get'])
    def filter_by_availability(self, request):
        start_time_str = request.query_params.get('start_time')
        end_time_str = request.query_params.get('end_time')
        sport_type = request.query_params.get('sport_type')
        size = request.query_params.get('size')

        if not start_time_str or not end_time_str:
            return Response({'error': '请提供开始时间和结束时间'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
            end_time = datetime.fromisoformat(end_time_str.replace('Z', '+00:00'))
        except ValueError:
            return Response({'error': '时间格式错误'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Venue.objects.filter(status='available')

        if sport_type:
            queryset = queryset.filter(venue_type__sport_type=sport_type)
        if size:
            queryset = queryset.filter(size=size)

        available_venues = []
        for venue in queryset:
            if venue.is_available(start_time, end_time):
                available_venues.append(venue)

        serializer = VenueSerializer(available_venues, many=True)
        return Response({
            'count': len(available_venues),
            'venues': serializer.data
        })

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        venue = self.get_object()
        start_date_str = request.query_params.get('start_date', timezone.now().date().isoformat())
        end_date_str = request.query_params.get('end_date', start_date_str)

        try:
            start_date = datetime.fromisoformat(start_date_str).date()
            end_date = datetime.fromisoformat(end_date_str).date()
        except ValueError:
            return Response({'error': '日期格式错误'}, status=status.HTTP_400_BAD_REQUEST)

        start_datetime = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
        end_datetime = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))

        bookings = Booking.objects.filter(
            venue=venue,
            status__in=['pending', 'in_use'],
            start_time__lt=end_datetime,
            end_time__gt=start_datetime
        )

        booked_slots = []
        for booking in bookings:
            booked_slots.append({
                'booking_no': booking.booking_no,
                'start_time': booking.start_time,
                'end_time': booking.end_time,
                'status': booking.get_status_display(),
                'contact_name': booking.contact_name
            })

        return Response({
            'venue': VenueSerializer(venue).data,
            'date_range': {'start': start_date.isoformat(), 'end': end_date.isoformat()},
            'booked_slots': booked_slots,
            'is_available_now': len(booked_slots) == 0
        })

    @action(detail=True, methods=['post'], serializer_class=VenueAvailabilitySerializer)
    def check_time_slot(self, request, pk=None):
        venue = self.get_object()
        serializer = VenueAvailabilitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        start_time = serializer.validated_data['start_time']
        end_time = serializer.validated_data['end_time']

        overlapping_slots = venue.check_time_overlap(start_time, end_time)

        return Response({
            'venue_id': venue.id,
            'venue_name': venue.name,
            'is_available': len(overlapping_slots) == 0,
            'overlapping_slots': overlapping_slots
        })


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        user_id = self.request.query_params.get('user')
        venue_id = self.request.query_params.get('venue')
        date_filter = self.request.query_params.get('date')
        verification_status = self.request.query_params.get('verification_status')

        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if venue_id:
            queryset = queryset.filter(venue_id=venue_id)
        if date_filter:
            queryset = queryset.filter(start_time__date=date_filter)
        if verification_status:
            queryset = queryset.filter(verification_status=verification_status)

        for booking in queryset:
            booking.check_timeout()

        return queryset

    @action(detail=False, methods=['post'], serializer_class=BookingVerifySerializer)
    def verify(self, request):
        serializer = BookingVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            booking = Booking.objects.get(booking_no=serializer.validated_data['booking_no'])
        except Booking.DoesNotExist:
            return Response({'error': '预约不存在'}, status=status.HTTP_404_NOT_FOUND)

        booking.id_card = serializer.validated_data['id_card']
        is_valid, message = booking.verify_id_card()

        return Response({
            'success': is_valid,
            'message': message,
            'booking': BookingSerializer(booking).data
        })

    @action(detail=False, methods=['post'], serializer_class=ScanQrCodeSerializer)
    def scan_qrcode(self, request):
        serializer = ScanQrCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        venue_code = serializer.validated_data['venue_code']
        action = serializer.validated_data['action']
        booking_no = serializer.validated_data.get('booking_no')

        try:
            venue = Venue.objects.get(code=venue_code)
        except Venue.DoesNotExist:
            return Response({'error': '场地不存在'}, status=status.HTTP_404_NOT_FOUND)

        if action == 'check_in':
            pending_bookings = Booking.objects.filter(
                venue=venue,
                status='pending',
                verification_status='verified'
            )
            if not pending_bookings.exists():
                return Response({'error': '该场地当前没有已核验的待入场预约'}, status=status.HTTP_400_BAD_REQUEST)
            
            if pending_bookings.count() > 1:
                return Response({
                    'error': '检测到多个待入场预约，请明确指定预约单号',
                    'pending_bookings': BookingSerializer(pending_bookings, many=True).data
                }, status=status.HTTP_400_BAD_REQUEST)
            
            booking = pending_bookings.first()
            is_success, message = booking.check_in(method='scan')
            if is_success:
                return Response({
                    'success': True,
                    'message': message,
                    'action': 'check_in',
                    'booking': BookingSerializer(booking).data
                })
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)

        elif action == 'check_out':
            if not booking_no:
                in_use_bookings = Booking.objects.filter(venue=venue, status='in_use')
                if not in_use_bookings.exists():
                    return Response({'error': '该场地当前没有正在使用的预约'}, status=status.HTTP_400_BAD_REQUEST)
                if in_use_bookings.count() > 1:
                    return Response({
                        'error': '检测到多个正在使用的预约，请明确指定预约单号',
                        'in_use_bookings': BookingSerializer(in_use_bookings, many=True).data
                    }, status=status.HTTP_400_BAD_REQUEST)
                booking = in_use_bookings.first()
            else:
                try:
                    booking = Booking.objects.get(booking_no=booking_no, venue=venue)
                except Booking.DoesNotExist:
                    return Response({'error': '预约不存在'}, status=status.HTTP_404_NOT_FOUND)

            is_success, result = booking.check_out(method='scan')
            if is_success:
                return Response({
                    'success': True,
                    'message': result['message'],
                    'action': 'check_out',
                    'actual_duration_minutes': result['actual_duration_minutes'],
                    'actual_duration_hours': result['actual_duration_hours'],
                    'billing_duration_minutes': result['billing_duration_minutes'],
                    'billing_duration_hours': result['billing_duration_hours'],
                    'min_billing_minutes': result['min_billing_minutes'],
                    'total_amount': result['total_amount'],
                    'used_min_billing': result['used_min_billing'],
                    'booking': BookingSerializer(booking).data
                })
            return Response({'error': result}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], serializer_class=BookingCheckInSerializer)
    def check_in(self, request):
        serializer = BookingCheckInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            booking = Booking.objects.get(booking_no=serializer.validated_data['booking_no'])
        except Booking.DoesNotExist:
            return Response({'error': '预约不存在'}, status=status.HTTP_404_NOT_FOUND)

        if booking.verification_status != 'verified':
            return Response({'error': '请先完成实名核验'}, status=status.HTTP_400_BAD_REQUEST)

        is_success, message = booking.check_in(method='manual')
        if is_success:
            return Response({
                'success': True,
                'message': message,
                'booking': BookingSerializer(booking).data
            })
        return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], serializer_class=BookingCheckOutSerializer)
    def check_out(self, request):
        serializer = BookingCheckOutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            booking = Booking.objects.get(booking_no=serializer.validated_data['booking_no'])
        except Booking.DoesNotExist:
            return Response({'error': '预约不存在'}, status=status.HTTP_404_NOT_FOUND)

        is_success, result = booking.check_out(method='manual')
        if is_success:
            return Response({
                'success': True,
                'message': result['message'],
                'actual_duration_minutes': result['actual_duration_minutes'],
                'actual_duration_hours': result['actual_duration_hours'],
                'billing_duration_minutes': result['billing_duration_minutes'],
                'billing_duration_hours': result['billing_duration_hours'],
                'min_billing_minutes': result['min_billing_minutes'],
                'total_amount': result['total_amount'],
                'used_min_billing': result['used_min_billing'],
                'booking': BookingSerializer(booking).data
            })
        return Response({'error': result}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def current_usage(self, request, pk=None):
        booking = self.get_object()
        
        if booking.status != 'in_use':
            return Response({'error': '预约不在使用中'}, status=status.HTTP_400_BAD_REQUEST)

        current_time = timezone.now()
        duration = current_time - booking.actual_start_time
        duration_minutes = int(duration.total_seconds() / 60)
        
        min_billing = booking.venue.min_billing_minutes
        billing_minutes = max(duration_minutes, min_billing)
        billing_hours = billing_minutes / 60
        current_amount = round(float(booking.venue.price_per_hour) * billing_hours, 2)

        return Response({
            'booking_no': booking.booking_no,
            'venue_name': booking.venue.name,
            'actual_start_time': booking.actual_start_time,
            'current_time': current_time,
            'duration_minutes': duration_minutes,
            'duration_hours': round(duration_minutes / 60, 2),
            'min_billing_minutes': min_billing,
            'billing_duration_minutes': billing_minutes,
            'billing_duration_hours': round(billing_hours, 2),
            'price_per_hour': float(booking.venue.price_per_hour),
            'current_amount': current_amount,
            'will_use_min_billing': duration_minutes < min_billing
        })

    @action(detail=False, methods=['get'])
    def venue_active_bookings(self, request):
        venue_id = request.query_params.get('venue_id')
        if not venue_id:
            return Response({'error': '请提供场地ID'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            venue = Venue.objects.get(id=venue_id)
        except Venue.DoesNotExist:
            return Response({'error': '场地不存在'}, status=status.HTTP_404_NOT_FOUND)

        active_bookings = Booking.objects.filter(venue=venue, status='in_use')
        result = []
        
        for booking in active_bookings:
            current_time = timezone.now()
            duration = current_time - booking.actual_start_time
            duration_minutes = int(duration.total_seconds() / 60)
            min_billing = booking.venue.min_billing_minutes
            billing_minutes = max(duration_minutes, min_billing)
            billing_hours = billing_minutes / 60
            current_amount = round(float(booking.venue.price_per_hour) * billing_hours, 2)
            
            result.append({
                'booking_no': booking.booking_no,
                'contact_name': booking.contact_name,
                'contact_phone': booking.contact_phone,
                'people_count': booking.people_count,
                'booking_type': booking.booking_type,
                'actual_start_time': booking.actual_start_time,
                'duration_minutes': duration_minutes,
                'current_amount': current_amount,
                'check_in_method': booking.check_in_method
            })

        return Response({
            'venue_id': venue.id,
            'venue_name': venue.name,
            'venue_code': venue.code,
            'active_count': len(result),
            'active_bookings': result
        })

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.status in ['pending']:
            booking.status = 'cancelled'
            booking.save()
            return Response({'message': '取消成功', 'booking': BookingSerializer(booking).data})
        return Response({'error': '只能取消待使用的预约'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], serializer_class=TimeSlotCheckSerializer)
    def check_time_conflict(self, request):
        serializer = TimeSlotCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            venue = Venue.objects.get(id=serializer.validated_data['venue_id'])
        except Venue.DoesNotExist:
            return Response({'error': '场地不存在'}, status=status.HTTP_404_NOT_FOUND)

        start_time = serializer.validated_data['start_time']
        end_time = serializer.validated_data['end_time']

        overlapping_slots = venue.check_time_overlap(start_time, end_time)

        return Response({
            'venue_id': venue.id,
            'venue_name': venue.name,
            'is_available': len(overlapping_slots) == 0,
            'overlapping_slots': overlapping_slots
        })

    @action(detail=False, methods=['get'])
    def user_daily_hours(self, request):
        user_id = request.query_params.get('user_id')
        date_str = request.query_params.get('date', timezone.now().date().isoformat())

        if not user_id:
            return Response({'error': '请提供用户ID'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
            check_date = datetime.fromisoformat(date_str).date()
        except User.DoesNotExist:
            return Response({'error': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({'error': '日期格式错误'}, status=status.HTTP_400_BAD_REQUEST)

        total_hours = Booking.get_user_daily_booking_hours(user, check_date)

        return Response({
            'user_id': user_id,
            'username': user.username,
            'date': date_str,
            'total_hours': total_hours
        })


class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        venue_id = self.request.query_params.get('venue')
        date_filter = self.request.query_params.get('date')

        if venue_id:
            queryset = queryset.filter(venue_id=venue_id)
        if date_filter:
            queryset = queryset.filter(date=date_filter)

        return queryset


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentCreateSerializer
        return PaymentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        booking_id = self.request.query_params.get('booking')

        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if booking_id:
            queryset = queryset.filter(booking_id=booking_id)

        return queryset

    @action(detail=True, methods=['post'])
    def confirm_payment(self, request, pk=None):
        payment = self.get_object()
        if payment.status == 'pending':
            payment.status = 'paid'
            payment.paid_at = timezone.now()
            payment.save()
            return Response({'message': '支付成功', 'payment': PaymentSerializer(payment).data})
        return Response({'error': '该支付已处理'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        payment = self.get_object()
        if payment.status == 'paid':
            payment.status = 'refunded'
            payment.save()
            return Response({'message': '退款成功', 'payment': PaymentSerializer(payment).data})
        return Response({'error': '只能对已支付的订单退款'}, status=status.HTTP_400_BAD_REQUEST)


class DashboardViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def stats(self, request):
        today = date.today()

        total_venues = Venue.objects.count()
        today_bookings = Booking.objects.filter(created_at__date=today).count()
        active_bookings = Booking.objects.filter(status='in_use').count()

        today_payments = Payment.objects.filter(
            status='paid',
            paid_at__date=today
        ).aggregate(total=Sum('amount'))
        today_revenue = today_payments['total'] or 0

        data = {
            'total_venues': total_venues,
            'today_bookings': today_bookings,
            'active_bookings': active_bookings,
            'today_revenue': today_revenue
        }

        serializer = DashboardStatsSerializer(data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recent_bookings(self, request):
        bookings = Booking.objects.all()[:10]
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
