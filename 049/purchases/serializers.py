from rest_framework import serializers
from .models import Supplier, PurchaseOrder, PurchaseOrderItem


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_unit = serializers.CharField(source='product.unit', read_only=True)

    class Meta:
        model = PurchaseOrderItem
        fields = '__all__'


class PurchaseOrderSerializer(serializers.ModelSerializer):
    items = PurchaseOrderItemSerializer(many=True, required=False)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        read_only_fields = ['order_no', 'created_at', 'updated_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        purchase_order = PurchaseOrder.objects.create(**validated_data)
        total_amount = 0
        for item_data in items_data:
            item = PurchaseOrderItem.objects.create(purchase_order=purchase_order, **item_data)
            total_amount += item.subtotal
        purchase_order.total_amount = total_amount
        purchase_order.save()
        return purchase_order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        instance = super().update(instance, validated_data)
        
        if items_data is not None:
            instance.items.all().delete()
            total_amount = 0
            for item_data in items_data:
                item = PurchaseOrderItem.objects.create(purchase_order=instance, **item_data)
                total_amount += item.subtotal
            instance.total_amount = total_amount
            instance.save()
        
        return instance
