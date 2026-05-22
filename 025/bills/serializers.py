from rest_framework import serializers
from .models import FeeStandard, Bill, MeterReading


class FeeStandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeStandard
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': True, 'error_messages': {'required': '费用名称不能为空'}},
            'fee_type': {'required': True, 'error_messages': {'required': '费用类型不能为空'}},
            'unit_price': {'required': True, 'error_messages': {'required': '单价不能为空'}}
        }

    def validate_unit_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('单价必须大于0')
        return value


class BillSerializer(serializers.ModelSerializer):
    house_info = serializers.SerializerMethodField()
    owner_name = serializers.CharField(source='owner.name', read_only=True)
    full_room_number = serializers.SerializerMethodField()

    class Meta:
        model = Bill
        fields = '__all__'
        extra_kwargs = {
            'house': {'required': True, 'error_messages': {'required': '所属房屋不能为空'}},
            'owner': {'required': True, 'error_messages': {'required': '所属业主不能为空'}},
            'bill_type': {'required': True, 'error_messages': {'required': '账单类型不能为空'}},
            'title': {'required': True, 'error_messages': {'required': '账单标题不能为空'}},
            'amount': {'required': True, 'error_messages': {'required': '金额不能为空'}},
            'billing_month': {'required': True, 'error_messages': {'required': '账单月份不能为空'}},
            'start_date': {'required': True, 'error_messages': {'required': '计费开始日期不能为空'}},
            'end_date': {'required': True, 'error_messages': {'required': '计费结束日期不能为空'}},
            'unit_price': {'required': True, 'error_messages': {'required': '单价不能为空'}},
            'due_date': {'required': True, 'error_messages': {'required': '缴费截止日期不能为空'}}
        }

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('金额必须大于0')
        return value

    def validate_unit_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('单价必须大于0')
        return value

    def get_house_info(self, obj):
        return {
            'id': obj.house.id,
            'building': obj.house.building.name,
            'room_number': obj.house.room_number
        }

    def get_full_room_number(self, obj):
        return f'{obj.house.building.name} {obj.house.room_number}'


class MeterReadingSerializer(serializers.ModelSerializer):
    house_info = serializers.SerializerMethodField()
    full_room_number = serializers.SerializerMethodField()

    class Meta:
        model = MeterReading
        fields = '__all__'
        extra_kwargs = {
            'house': {'required': True, 'error_messages': {'required': '所属房屋不能为空'}},
            'reading_type': {'required': True, 'error_messages': {'required': '抄表类型不能为空'}},
            'current_reading': {'required': True, 'error_messages': {'required': '当前读数不能为空'}},
            'previous_reading': {'required': True, 'error_messages': {'required': '上次读数不能为空'}},
            'usage': {'required': True, 'error_messages': {'required': '用量不能为空'}},
            'reading_date': {'required': True, 'error_messages': {'required': '抄表日期不能为空'}},
            'billing_month': {'required': True, 'error_messages': {'required': '账单月份不能为空'}}
        }

    def validate_current_reading(self, value):
        if value < 0:
            raise serializers.ValidationError('当前读数不能为负数')
        return value

    def validate_previous_reading(self, value):
        if value < 0:
            raise serializers.ValidationError('上次读数不能为负数')
        return value

    def validate_usage(self, value):
        if value <= 0:
            raise serializers.ValidationError('用量必须大于0')
        return value

    def get_house_info(self, obj):
        return {
            'id': obj.house.id,
            'building': obj.house.building.name,
            'room_number': obj.house.room_number
        }

    def get_full_room_number(self, obj):
        return f'{obj.house.building.name} {obj.house.room_number}'
