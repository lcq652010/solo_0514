from rest_framework import serializers
from .models import Pet, Room, Order, FeedingRecord
from django.utils import timezone
from datetime import timedelta


class PetSerializer(serializers.ModelSerializer):
    species_display = serializers.CharField(source='get_species_display', read_only=True)
    size_display = serializers.CharField(source='get_size_display', read_only=True)
    is_vaccine_valid = serializers.BooleanField(read_only=True)
    days_until_vaccine_expiry = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Pet
        fields = '__all__'
        read_only_fields = ['created_at']
    
    def validate_age(self, value):
        if value < 0:
            raise serializers.ValidationError('年龄不能为负数')
        return value
    
    def validate_weight(self, value):
        if value <= 0:
            raise serializers.ValidationError('体重必须大于0')
        return value


class RoomSerializer(serializers.ModelSerializer):
    room_type_display = serializers.CharField(source='get_room_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    suitable_size_display = serializers.CharField(source='get_suitable_size_display', read_only=True)
    available_capacity = serializers.IntegerField(read_only=True)
    has_capacity = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Room
        fields = '__all__'
    
    def validate_daily_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('日租金必须大于0')
        return value
    
    def validate_max_pets(self, value):
        if value < 1:
            raise serializers.ValidationError('最大容纳宠物数至少为1')
        return value
    
    def validate_overtime_multiplier(self, value):
        if value < 1:
            raise serializers.ValidationError('超时费用倍率不能小于1')
        return value


class FeedingRecordSerializer(serializers.ModelSerializer):
    pet_name = serializers.CharField(source='order.pet.name', read_only=True)
    room_number = serializers.CharField(source='order.room.room_number', read_only=True)
    
    class Meta:
        model = FeedingRecord
        fields = '__all__'
        read_only_fields = ['created_at']


class FeedingRecordBatchItemSerializer(serializers.Serializer):
    record_date = serializers.DateField()
    morning_feeding = serializers.BooleanField(default=False)
    morning_notes = serializers.CharField(allow_blank=True, required=False)
    afternoon_feeding = serializers.BooleanField(default=False)
    afternoon_notes = serializers.CharField(allow_blank=True, required=False)
    evening_feeding = serializers.BooleanField(default=False)
    evening_notes = serializers.CharField(allow_blank=True, required=False)
    health_notes = serializers.CharField(allow_blank=True, required=False)
    created_by = serializers.CharField()


class FeedingRecordBatchSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    records = FeedingRecordBatchItemSerializer(many=True)


class OrderSerializer(serializers.ModelSerializer):
    pet_name = serializers.CharField(source='pet.name', read_only=True)
    pet_species = serializers.CharField(source='pet.species', read_only=True)
    pet_breed = serializers.CharField(source='pet.breed', read_only=True)
    pet_size = serializers.CharField(source='pet.size', read_only=True)
    pet_size_display = serializers.CharField(source='pet.get_size_display', read_only=True)
    owner_name = serializers.CharField(source='pet.owner_name', read_only=True)
    owner_phone = serializers.CharField(source='pet.owner_phone', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    room_type = serializers.CharField(source='room.room_type', read_only=True)
    room_type_display = serializers.CharField(source='room.get_room_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    reminder_status_display = serializers.CharField(source='get_reminder_status_display', read_only=True)
    days_until_checkout = serializers.IntegerField(read_only=True)
    is_near_checkout = serializers.BooleanField(read_only=True)
    stay_duration_days = serializers.IntegerField(read_only=True)
    feeding_records = FeedingRecordSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['order_no', 'created_at', 'updated_at', 'actual_days', 
                           'overtime_days', 'base_amount', 'overtime_amount', 
                           'total_amount', 'checkout_date', 'reminder_sent_at']
    
    def validate_expected_days(self, value):
        if value <= 0:
            raise serializers.ValidationError('预计寄养天数必须大于0')
        return value


class OrderDetailSerializer(serializers.ModelSerializer):
    pet = PetSerializer(read_only=True)
    room = RoomSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    reminder_status_display = serializers.CharField(source='get_reminder_status_display', read_only=True)
    days_until_checkout = serializers.IntegerField(read_only=True)
    is_near_checkout = serializers.BooleanField(read_only=True)
    stay_duration_days = serializers.IntegerField(read_only=True)
    feeding_records = FeedingRecordSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['order_no', 'created_at', 'updated_at']


class OrderCheckinSerializer(serializers.Serializer):
    pass


class OrderCheckoutSerializer(serializers.Serializer):
    pass


class OrderCompleteSerializer(serializers.Serializer):
    pass


class OrderCancelSerializer(serializers.Serializer):
    pass


class OrderAutoAssignRoomSerializer(serializers.Serializer):
    pass


class ReminderOrderSerializer(serializers.ModelSerializer):
    pet_name = serializers.CharField(source='pet.name', read_only=True)
    owner_name = serializers.CharField(source='pet.owner_name', read_only=True)
    owner_phone = serializers.CharField(source='pet.owner_phone', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    days_until_checkout = serializers.IntegerField(read_only=True)
    expected_checkout_date = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_no', 'pet_name', 'owner_name', 'owner_phone', 
                 'room_number', 'expected_checkout_date', 'days_until_checkout',
                 'reminder_status']


class OrderMarkReminderSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=['sent', 'confirmed'], default='sent')
