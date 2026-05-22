import re
from rest_framework import serializers
from .models import Shop, Product, Rider, Order, OrderItem, DeliveryTracking


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    shop_name = serializers.CharField(source='shop.name', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError('商品价格不能为负数')
        if value > 99999:
            raise serializers.ValidationError('商品价格超出合理范围')
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('库存不能为负数')
        return value


class RiderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rider
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class DeliveryTrackingSerializer(serializers.ModelSerializer):
    rider_name = serializers.CharField(source='rider.name', read_only=True)

    class Meta:
        model = DeliveryTracking
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    tracking_records = DeliveryTrackingSerializer(many=True, read_only=True)
    shop_name = serializers.CharField(source='shop.name', read_only=True)
    rider_name = serializers.CharField(source='rider.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError('商品数量必须大于0')
        if value > 999:
            raise serializers.ValidationError('商品数量超出合理范围')
        return value


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True, required=True)

    class Meta:
        model = Order
        fields = ['shop', 'customer_name', 'customer_phone', 'customer_address', 'remark', 'items']

    def validate_customer_name(self, value):
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError('用户昵称至少需要2个字符')
        if len(value) > 50:
            raise serializers.ValidationError('用户昵称不能超过50个字符')
        return value

    def validate_customer_phone(self, value):
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('请输入正确的手机号码')
        return value

    def validate_customer_address(self, value):
        if not value or len(value.strip()) < 5:
            raise serializers.ValidationError('配送地址至少需要5个字符')
        if len(value) > 200:
            raise serializers.ValidationError('配送地址不能超过200个字符')
        if not re.search(r'[省市县区路街号村镇园]', value):
            raise serializers.ValidationError('请输入详细的配送地址（包含省/市/区/路/街等信息）')
        return value

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError('订单至少需要包含一个商品')
        if len(value) > 50:
            raise serializers.ValidationError('单次下单商品种类不能超过50种')
        return value

    def validate(self, attrs):
        items_data = attrs.get('items', [])
        
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            
            if not product.is_available:
                raise serializers.ValidationError(f'商品 {product.name} 已下架')
            
            if product.stock < quantity:
                raise serializers.ValidationError(f'商品 {product.name} 库存不足，当前库存: {product.stock}')
        
        return attrs

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        total_amount = 0
        order_items = []

        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            subtotal = product.price * quantity
            total_amount += subtotal
            order_items.append({
                'product': product,
                'quantity': quantity,
                'price': product.price,
                'subtotal': subtotal
            })

        if total_amount <= 0:
            raise serializers.ValidationError('订单总金额必须大于0')
        if total_amount > 99999:
            raise serializers.ValidationError('订单金额超出合理范围')

        validated_data['total_amount'] = total_amount
        order = Order.objects.create(**validated_data)

        for item_data in order_items:
            product = item_data['product']
            product.stock -= item_data['quantity']
            product.save()
            OrderItem.objects.create(order=order, **item_data)

        return order
