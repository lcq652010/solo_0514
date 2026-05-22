import re
from rest_framework import serializers
from django.utils import timezone
from .models import Movie, Hall, Schedule, Seat, Order

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        extra_kwargs = {
            'title': {'required': True, 'allow_blank': False, 'max_length': 200},
            'description': {'required': True, 'allow_blank': False},
            'duration': {'required': True, 'min_value': 1},
            'genre': {'required': True, 'allow_blank': False},
            'director': {'required': True, 'allow_blank': False},
            'actors': {'required': True, 'allow_blank': False},
            'release_date': {'required': True},
            'rating': {'required': True, 'min_value': 0, 'max_value': 10},
        }

    def validate_duration(self, value):
        if value <= 0:
            raise serializers.ValidationError('影片时长必须大于0分钟')
        return value

    def validate_rating(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError('评分必须在0-10之间')
        return value

class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': True, 'allow_blank': False, 'max_length': 100},
            'total_rows': {'required': True, 'min_value': 1},
            'total_cols': {'required': True, 'min_value': 1},
            'total_seats': {'required': True, 'min_value': 1},
        }

    def validate(self, data):
        if 'total_rows' in data and 'total_cols' in data:
            calculated_seats = data['total_rows'] * data['total_cols']
            if 'total_seats' in data and data['total_seats'] != calculated_seats:
                raise serializers.ValidationError(
                    f'总座位数不匹配，应为 {calculated_seats} 个座位'
                )
        if 'total_rows' in data and data['total_rows'] > 30:
            raise serializers.ValidationError('排数不能超过30排')
        if 'total_cols' in data and data['total_cols'] > 50:
            raise serializers.ValidationError('列数不能超过50列')
        return data

class ScheduleSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    hall_name = serializers.CharField(source='hall.name', read_only=True)

    class Meta:
        model = Schedule
        fields = '__all__'
        extra_fields = ['movie_title', 'hall_name']
        extra_kwargs = {
            'movie': {'required': True},
            'hall': {'required': True},
            'show_time': {'required': True},
            'end_time': {'required': True},
            'price': {'required': True},
        }

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('票价必须大于0')
        if value > 1000:
            raise serializers.ValidationError('票价不能超过1000元')
        return value

    def validate(self, data):
        if 'show_time' in data and 'end_time' in data:
            if data['show_time'] >= data['end_time']:
                raise serializers.ValidationError('结束时间必须晚于放映时间')
            if data['show_time'] < timezone.now():
                raise serializers.ValidationError('放映时间不能早于当前时间')
        
        if 'hall' in data and 'show_time' in data and 'end_time' in data:
            conflict_schedules = Schedule.objects.filter(
                hall=data['hall'],
                show_time__lt=data['end_time'],
                end_time__gt=data['show_time'],
                is_active=True
            )
            if self.instance:
                conflict_schedules = conflict_schedules.exclude(id=self.instance.id)
            if conflict_schedules.exists():
                raise serializers.ValidationError('该影厅在该时间段已有排期，存在冲突')
        
        return data

class SeatSerializer(serializers.ModelSerializer):
    hall_name = serializers.CharField(source='hall.name', read_only=True)
    schedule_movie_title = serializers.CharField(source='schedule.movie.title', read_only=True, allow_null=True)

    class Meta:
        model = Seat
        fields = '__all__'
        extra_fields = ['hall_name', 'schedule_movie_title']
        extra_kwargs = {
            'hall': {'required': True},
            'row_number': {'required': True, 'min_value': 1},
            'col_number': {'required': True, 'min_value': 1},
            'seat_code': {'required': True, 'allow_blank': False},
        }

class OrderSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='schedule.movie.title', read_only=True)
    hall_name = serializers.CharField(source='schedule.hall.name', read_only=True)
    show_time = serializers.DateTimeField(source='schedule.show_time', read_only=True)
    end_time = serializers.DateTimeField(source='schedule.end_time', read_only=True)
    ticket_price = serializers.DecimalField(source='schedule.price', max_digits=10, decimal_places=2, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    seller_name = serializers.CharField(source='seller.username', read_only=True)
    ticket_checked_by_name = serializers.CharField(source='ticket_checked_by.username', read_only=True, allow_null=True)
    completed_by_name = serializers.CharField(source='completed_by.username', read_only=True, allow_null=True)
    refund_by_name = serializers.CharField(source='refund_by.username', read_only=True, allow_null=True)

    class Meta:
        model = Order
        fields = '__all__'
        extra_fields = ['movie_title', 'hall_name', 'show_time', 'end_time', 'ticket_price',
                        'status_display', 'seller_name', 'ticket_checked_by_name',
                        'completed_by_name', 'refund_by_name']
        read_only_fields = ['order_no', 'total_price', 'seat_codes', 'seller',
                          'ticket_checked_at', 'ticket_checked_by',
                          'completed_at', 'completed_by',
                          'refund_at', 'refund_by']

class OrderCreateSerializer(serializers.ModelSerializer):
    seat_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        write_only=True,
        required=True,
        min_length=1,
        max_length=10
    )

    class Meta:
        model = Order
        fields = ['schedule', 'seat_ids', 'customer_name', 'customer_phone']
        extra_kwargs = {
            'schedule': {'required': True},
            'customer_name': {'required': True, 'allow_blank': False, 'max_length': 100},
            'customer_phone': {'required': True, 'allow_blank': False},
        }

    def validate_customer_phone(self, value):
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('请输入有效的手机号码')
        return value

    def validate_seat_ids(self, value):
        if not value:
            raise serializers.ValidationError('至少选择一个座位')
        if len(value) > 10:
            raise serializers.ValidationError('一次最多购买10张票')
        if len(value) != len(set(value)):
            raise serializers.ValidationError('不能重复选择同一个座位')
        return value

    def validate(self, data):
        schedule = data.get('schedule')
        seat_ids = data.get('seat_ids', [])

        if schedule and schedule.show_time < timezone.now():
            raise serializers.ValidationError('该场次已过期，无法购票')

        if schedule and seat_ids:
            seats = Seat.objects.filter(id__in=seat_ids, schedule=schedule)
            if seats.count() != len(seat_ids):
                raise serializers.ValidationError('部分座位不属于该排期')

            unavailable_seats = seats.filter(is_available=False)
            if unavailable_seats.exists():
                unavailable_codes = [s.seat_code for s in unavailable_seats]
                raise serializers.ValidationError(
                    f'以下座位已被占用: {", ".join(unavailable_codes)}'
                )

        return data

    def create(self, validated_data):
        seat_ids = validated_data.pop('seat_ids')
        seats = Seat.objects.filter(id__in=seat_ids, is_available=True)
        
        if seats.count() != len(seat_ids):
            raise serializers.ValidationError('部分座位已被占用')
        
        schedule = validated_data['schedule']
        
        locked_seats = Seat.objects.select_for_update().filter(id__in=seat_ids)
        unavailable_seats = locked_seats.filter(is_available=False)
        if unavailable_seats.exists():
            raise serializers.ValidationError('座位锁定失败，请重新选择')
        
        total_price = schedule.price * len(seats)
        if total_price <= 0:
            raise serializers.ValidationError('订单金额不合法')
        
        seat_codes = ','.join([seat.seat_code for seat in seats])

        order = Order.objects.create(
            schedule=schedule,
            total_price=total_price,
            seat_codes=seat_codes,
            **validated_data
        )
        order.seats.set(seats)
        
        locked_seats.update(is_available=False)
        
        return order
