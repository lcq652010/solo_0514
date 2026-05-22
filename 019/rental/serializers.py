from rest_framework import serializers
from django.db.models import Q
from .models import Car, Customer, Order
from .utils import validate_id_card, validate_phone, validate_driver_license, validate_amount, validate_date_range


class CarSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Car
        fields = '__all__'

    def validate_daily_rent(self, value):
        is_valid, message = validate_amount(value, min_value=10, max_value=10000)
        if not is_valid:
            raise serializers.ValidationError(message)
        return value

    def validate_seats(self, value):
        if value < 2 or value > 20:
            raise serializers.ValidationError('座位数必须在2-20之间')
        return value

    def validate_overtime_rate(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError('超时费率必须在1-5倍之间')
        return value


class CustomerSerializer(serializers.ModelSerializer):
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'

    def validate_phone(self, value):
        is_valid, message = validate_phone(value)
        if not is_valid:
            raise serializers.ValidationError(message)
        return value

    def validate_id_card(self, value):
        is_valid, message = validate_id_card(value)
        if not is_valid:
            raise serializers.ValidationError(message)
        return value

    def validate_driver_license(self, value):
        is_valid, message = validate_driver_license(value)
        if not is_valid:
            raise serializers.ValidationError(message)
        return value


class OrderSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    car_info = CarSerializer(source='car', read_only=True)
    customer_info = CustomerSerializer(source='customer', read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    overdue_days = serializers.IntegerField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = [
            'order_no', 'rental_days', 'total_amount',
            'actual_rental_days', 'overtime_days',
            'base_rental', 'overtime_fee', 'actual_amount',
            'actual_start_date', 'actual_end_date'
        ]

    def validate_deposit(self, value):
        is_valid, message = validate_amount(value, min_value=0, max_value=50000)
        if not is_valid:
            raise serializers.ValidationError(message)
        return value

    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        car = attrs.get('car')

        is_valid, message = validate_date_range(start_date, end_date)
        if not is_valid:
            raise serializers.ValidationError(message)

        if car:
            existing_orders = Order.objects.filter(
                Q(car=car) &
                ~Q(status__in=['returned', 'cancelled']) &
                Q(start_date__lte=end_date) &
                Q(end_date__gte=start_date)
            )
            if self.instance:
                existing_orders = existing_orders.exclude(id=self.instance.id)
            
            if existing_orders.exists():
                raise serializers.ValidationError('该车辆在所选时段已有订单，存在时段冲突')

        return attrs


class OrderPickUpSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()


class OrderReturnSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()


class OrderCancelSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
