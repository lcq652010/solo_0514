from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.name', read_only=True)
    bill_title = serializers.CharField(source='bill.title', read_only=True)
    bill_type = serializers.CharField(source='bill.bill_type', read_only=True)
    full_room_number = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = '__all__'
        extra_kwargs = {
            'owner': {'required': True, 'error_messages': {'required': '缴费业主不能为空'}},
            'amount': {'required': True, 'error_messages': {'required': '支付金额不能为空'}},
            'payment_method': {'required': True, 'error_messages': {'required': '支付方式不能为空'}}
        }

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('支付金额必须大于0')
        return value

    def get_full_room_number(self, obj):
        if obj.bill:
            return f'{obj.bill.house.building.name} {obj.bill.house.room_number}'
        return ''
