from rest_framework import serializers
from .models import Category, Product, Order, OrderItem, User
from django.utils import timezone
import re


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('分类名称不能为空')
        if len(value.strip()) < 2:
            raise serializers.ValidationError('分类名称至少2个字符')
        return value.strip()


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def get_category_name(self, obj):
        return obj.category.name if obj.category else ''

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('商品名称不能为空')
        if len(value.strip()) < 2:
            raise serializers.ValidationError('商品名称至少2个字符')
        return value.strip()

    def validate_price(self, value):
        if value is None:
            raise serializers.ValidationError('商品价格不能为空')
        if value <= 0:
            raise serializers.ValidationError('商品价格必须大于0')
        if value > 99999:
            raise serializers.ValidationError('商品价格不能超过99999')
        return value

    def validate_stock(self, value):
        if value is None:
            raise serializers.ValidationError('库存数量不能为空')
        if value < 0:
            raise serializers.ValidationError('库存数量不能为负数')
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = '__all__'

    def get_product_name(self, obj):
        return obj.product.name if obj.product else ''


class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'sugar', 'ice', 'toppings']

    def validate_quantity(self, value):
        if value is None:
            raise serializers.ValidationError('商品数量不能为空')
        if value <= 0:
            raise serializers.ValidationError('商品数量必须大于0')
        if value > 100:
            raise serializers.ValidationError('单次购买数量不能超过100')
        return value

    def validate(self, attrs):
        product = attrs.get('product')
        quantity = attrs.get('quantity')

        if not product.is_available:
            raise serializers.ValidationError(f'商品「{product.name}」已下架')

        if product.stock < quantity:
            raise serializers.ValidationError(
                f'商品「{product.name}」库存不足，当前库存：{product.stock}，请求数量：{quantity}'
            )

        return attrs


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['order_no', 'take_code', 'total_amount', 'is_paid', 'paid_at', 'created_at', 'updated_at']

    def get_status_display(self, obj):
        return obj.get_status_display()


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True, required=True)

    class Meta:
        model = Order
        fields = ['customer_name', 'customer_phone', 'remark', 'items']

    def validate_customer_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('顾客姓名不能为空')
        if len(value.strip()) < 2:
            raise serializers.ValidationError('顾客姓名至少2个字符')
        return value.strip()

    def validate_customer_phone(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('联系电话不能为空')
        phone_pattern = r'^1[3-9]\d{9}$'
        if not re.match(phone_pattern, value.strip()):
            raise serializers.ValidationError('请输入有效的手机号码')
        return value.strip()

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError('订单至少包含一个商品')
        if len(value) > 50:
            raise serializers.ValidationError('单次订单商品不能超过50种')
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        total_amount = 0

        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            amount = product.price * quantity
            if amount <= 0:
                raise serializers.ValidationError(f'商品「{product.name}」金额计算异常')
            total_amount += amount

        if total_amount <= 0:
            raise serializers.ValidationError('订单总金额必须大于0')
        if total_amount > 999999:
            raise serializers.ValidationError('订单总金额不能超过999999元')

        order = Order.objects.create(total_amount=total_amount, **validated_data)

        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            OrderItem.objects.create(
                order=order,
                product=product,
                price=product.price,
                quantity=quantity,
                sugar=item_data.get('sugar', ''),
                ice=item_data.get('ice', ''),
                toppings=item_data.get('toppings', '')
            )
            product.stock -= quantity
            product.save()

        return order


class OrderPaySerializer(serializers.Serializer):
    order_no = serializers.CharField()

    def validate_order_no(self, value):
        try:
            order = Order.objects.get(order_no=value)
            if order.is_paid:
                raise serializers.ValidationError('订单已支付')
            return value
        except Order.DoesNotExist:
            raise serializers.ValidationError('订单不存在')

    def save(self):
        order = Order.objects.get(order_no=self.validated_data['order_no'])
        order.is_paid = True
        order.paid_at = timezone.now()
        order.save()
        return order


class OrderStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)

    def validate_status(self, value):
        order = self.instance
        valid_transitions = {
            'pending': ['making'],
            'making': ['ready'],
            'ready': ['completed'],
            'completed': []
        }
        if value not in valid_transitions.get(order.status, []):
            raise serializers.ValidationError(f'无法从 {order.get_status_display()} 状态转换为 {dict(Order.STATUS_CHOICES)[value]}')
        return value

    def save(self):
        order = self.instance
        order.status = self.validated_data['status']
        order.save()
        return order


class OrderVerifySerializer(serializers.Serializer):
    take_code = serializers.CharField()

    def validate_take_code(self, value):
        try:
            order = Order.objects.get(take_code=value, status='ready')
            return value
        except Order.DoesNotExist:
            raise serializers.ValidationError('取餐码无效或订单未准备好')

    def save(self):
        order = Order.objects.get(take_code=self.validated_data['take_code'], status='ready')
        order.status = 'completed'
        order.is_archived = True
        order.archived_at = timezone.now()
        order.save()
        return order


class UserSerializer(serializers.ModelSerializer):
    role_display = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'role_display', 'phone', 'is_active', 'date_joined']
        read_only_fields = ['date_joined']

    def get_role_display(self, obj):
        return obj.get_role_display()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'phone']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=validated_data.get('role', 'cashier'),
            phone=validated_data.get('phone', '')
        )
        return user
