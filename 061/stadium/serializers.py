from rest_framework import serializers
from django.contrib.auth.models import User
from .models import VenueType, Venue, Booking, TimeSlot, Payment
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class VenueTypeSerializer(serializers.ModelSerializer):
    sport_type_display = serializers.CharField(source='get_sport_type_display', read_only=True)

    class Meta:
        model = VenueType
        fields = '__all__'


class VenueSerializer(serializers.ModelSerializer):
    venue_type_name = serializers.CharField(source='venue_type.name', read_only=True)
    sport_type = serializers.CharField(source='venue_type.sport_type', read_only=True)
    sport_type_display = serializers.CharField(source='venue_type.get_sport_type_display', read_only=True)
    size_display = serializers.CharField(source='get_size_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Venue
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class VenueAvailabilitySerializer(serializers.Serializer):
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()


class BookingSerializer(serializers.ModelSerializer):
    venue_name = serializers.CharField(source='venue.name', read_only=True)
    venue_capacity = serializers.IntegerField(source='venue.capacity', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    duration_hours = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    verification_status_display = serializers.CharField(source='get_verification_status_display', read_only=True)
    booking_type_display = serializers.CharField(source='get_booking_type_display', read_only=True)
    group_discount = serializers.SerializerMethodField()
    actual_duration_display = serializers.SerializerMethodField()
    billing_duration_display = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['booking_no', 'created_at', 'updated_at', 'total_amount', 
                          'verification_status', 'verification_time', 'actual_duration_minutes',
                          'billing_duration_minutes', 'actual_start_time', 'actual_end_time']

    def get_duration_hours(self, obj):
        if obj.start_time and obj.end_time:
            duration = obj.end_time - obj.start_time
            return round(duration.total_seconds() / 3600, 2)
        return 0

    def get_group_discount(self, obj):
        return obj.get_group_discount()

    def get_actual_duration_display(self, obj):
        if obj.actual_duration_minutes:
            hours = obj.actual_duration_minutes // 60
            minutes = obj.actual_duration_minutes % 60
            if hours > 0:
                return f'{hours}小时{minutes}分钟'
            return f'{minutes}分钟'
        return None

    def get_billing_duration_display(self, obj):
        if obj.billing_duration_minutes:
            hours = obj.billing_duration_minutes // 60
            minutes = obj.billing_duration_minutes % 60
            if hours > 0:
                return f'{hours}小时{minutes}分钟'
            return f'{minutes}分钟'
        return None

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError('结束时间必须晚于开始时间')
        if data['start_time'] < timezone.now():
            raise serializers.ValidationError('预约时间不能早于当前时间')

        duration = data['end_time'] - data['start_time']
        hours = duration.total_seconds() / 3600
        if hours < 0.5:
            raise serializers.ValidationError('预约时长最少为30分钟')
        if hours > 8:
            raise serializers.ValidationError('单次预约时长最多为8小时')

        venue = data['venue']
        instance = self.instance

        overlapping_slots = venue.check_time_overlap(
            data['start_time'],
            data['end_time'],
            exclude_booking_id=instance.id if instance else None
        )
        if overlapping_slots:
            conflict_info = '; '.join([
                f"{slot['start_time'].strftime('%H:%M')}-{slot['end_time'].strftime('%H:%M')}({slot['contact_name']})"
                for slot in overlapping_slots
            ])
            raise serializers.ValidationError(f'该时段已被预约，冲突时段: {conflict_info}')

        temp_booking = Booking(**data)
        if instance:
            temp_booking = instance
            for key, value in data.items():
                setattr(temp_booking, key, value)
        
        is_valid, message = temp_booking.check_people_capacity()
        if not is_valid:
            raise serializers.ValidationError(message)

        return data

    def create(self, validated_data):
        booking = Booking(**validated_data)

        is_valid, message = booking.check_max_booking_hours()
        if not is_valid:
            raise serializers.ValidationError(message)

        booking.save()
        return booking

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        is_valid, message = instance.check_max_booking_hours()
        if not is_valid:
            raise serializers.ValidationError(message)

        instance.save()
        return instance


class ScanQrCodeSerializer(serializers.Serializer):
    venue_code = serializers.CharField(help_text='场地编号')
    action = serializers.ChoiceField(choices=['check_in', 'check_out'], help_text='操作类型：入场或离场')
    booking_no = serializers.CharField(required=False, help_text='预约单号（离场时需要）')


class CurrentUsageSerializer(serializers.Serializer):
    booking_no = serializers.CharField()
    venue_name = serializers.CharField()
    start_time = serializers.DateTimeField()
    duration_minutes = serializers.IntegerField()
    current_amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class BookingCheckInSerializer(serializers.Serializer):
    booking_no = serializers.CharField()


class BookingCheckOutSerializer(serializers.Serializer):
    booking_no = serializers.CharField()


class BookingVerifySerializer(serializers.Serializer):
    booking_no = serializers.CharField()
    id_card = serializers.CharField(max_length=18)


class TimeSlotCheckSerializer(serializers.Serializer):
    venue_id = serializers.IntegerField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()


class TimeSlotSerializer(serializers.ModelSerializer):
    venue_name = serializers.CharField(source='venue.name', read_only=True)

    class Meta:
        model = TimeSlot
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    booking_no = serializers.CharField(source='booking.booking_no', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['payment_no', 'created_at']


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['booking', 'amount', 'payment_method']


class DashboardStatsSerializer(serializers.Serializer):
    total_venues = serializers.IntegerField()
    today_bookings = serializers.IntegerField()
    active_bookings = serializers.IntegerField()
    today_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
