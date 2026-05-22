from rest_framework import serializers
from .models import Customer, WholesaleOrder, WholesaleOrderItem, Settlement


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class WholesaleOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_unit = serializers.CharField(source='product.unit', read_only=True)

    class Meta:
        model = WholesaleOrderItem
        fields = '__all__'


class WholesaleOrderSerializer(serializers.ModelSerializer):
    items = WholesaleOrderItemSerializer(many=True, required=False)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = WholesaleOrder
        fields = '__all__'
        read_only_fields = ['order_no', 'created_at', 'updated_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        wholesale_order = WholesaleOrder.objects.create(**validated_data)
        total_amount = 0
        for item_data in items_data:
            item = WholesaleOrderItem.objects.create(wholesale_order=wholesale_order, **item_data)
            total_amount += item.subtotal
        wholesale_order.total_amount = total_amount
        wholesale_order.save()
        return wholesale_order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        instance = super().update(instance, validated_data)
        
        if items_data is not None:
            instance.items.all().delete()
            total_amount = 0
            for item_data in items_data:
                item = WholesaleOrderItem.objects.create(wholesale_order=instance, **item_data)
                total_amount += item.subtotal
            instance.total_amount = total_amount
            instance.save()
        
        return instance


class SettlementSerializer(serializers.ModelSerializer):
    order_no = serializers.CharField(source='wholesale_order.order_no', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Settlement
        fields = '__all__'
        read_only_fields = ['settlement_no', 'created_at']
