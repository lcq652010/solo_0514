from rest_framework import serializers
from .models import Inventory, StockRecord, StockAlert


class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_unit = serializers.CharField(source='product.unit', read_only=True)
    product_code = serializers.CharField(source='product.product_code', read_only=True)
    min_stock = serializers.IntegerField(source='product.min_stock', read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Inventory
        fields = '__all__'


class StockRecordSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    record_type_display = serializers.CharField(source='get_record_type_display', read_only=True)

    class Meta:
        model = StockRecord
        fields = '__all__'


class StockAlertSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    alert_type_display = serializers.CharField(source='get_alert_type_display', read_only=True)

    class Meta:
        model = StockAlert
        fields = '__all__'
