import re
from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from .models import Item, Order, OrderItem, QualityCheck, Settlement, ItemCategory, OrderStatus, UserRole, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['role', 'role_display', 'phone']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'is_staff', 'is_active', 'profile']
        read_only_fields = ['username', 'is_staff', 'is_active']


class ItemSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'name', 'category', 'category_display', 'description', 'quantity', 'estimated_price', 'created_by', 'created_by_name', 'created_at', 'updated_at']
        read_only_fields = ['created_by']

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('物品名称不能为空')
        if len(value.strip()) < 2:
            raise serializers.ValidationError('物品名称至少需要2个字符')
        return value.strip()

    def validate_category(self, value):
        if not value:
            raise serializers.ValidationError('物品分类不能为空')
        if value not in [c[0] for c in ItemCategory.choices]:
            raise serializers.ValidationError('无效的物品分类')
        return value

    def validate_quantity(self, value):
        if value is None:
            raise serializers.ValidationError('数量不能为空')
        if value < 1:
            raise serializers.ValidationError('数量必须大于0')
        if value > 1000:
            raise serializers.ValidationError('数量不能超过1000')
        return value

    def validate_estimated_price(self, value):
        if value is None:
            return 0
        if value < 0:
            raise serializers.ValidationError('预估价格不能为负数')
        if value > 100000:
            raise serializers.ValidationError('预估价格不能超过100000')
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_category = serializers.CharField(source='item.category', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'item', 'item_name', 'item_category', 'quantity', 'unit_price', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    order_items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    recycler_name = serializers.CharField(source='recycler.username', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_no', 'customer_name', 'customer_phone', 'address', 'pickup_time', 'status', 'status_display', 'total_amount', 'created_by', 'created_by_name', 'recycler', 'recycler_name', 'picked_up_at', 'warehoused_at', 'completed_at', 'remark', 'order_items', 'created_at', 'updated_at']
        read_only_fields = ['order_no', 'status', 'total_amount', 'created_by', 'picked_up_at', 'warehoused_at', 'completed_at', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    items = serializers.ListField(child=serializers.DictField(), write_only=True)
    auto_warehouse = serializers.BooleanField(default=False, write_only=True)
    auto_settle = serializers.BooleanField(default=False, write_only=True)

    class Meta:
        model = Order
        fields = ['customer_name', 'customer_phone', 'address', 'pickup_time', 'remark', 'items', 'recycler', 'auto_warehouse', 'auto_settle']

    def validate_customer_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('客户姓名不能为空')
        if len(value.strip()) < 2:
            raise serializers.ValidationError('客户姓名至少需要2个字符')
        if len(value.strip()) > 50:
            raise serializers.ValidationError('客户姓名不能超过50个字符')
        return value.strip()

    def validate_customer_phone(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('联系电话不能为空')
        value = value.strip()
        pattern = r'^1[3-9]\d{9}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError('请输入有效的手机号码')
        return value

    def validate_address(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('回收地址不能为空')
        if len(value.strip()) < 5:
            raise serializers.ValidationError('回收地址至少需要5个字符')
        if len(value.strip()) > 200:
            raise serializers.ValidationError('回收地址不能超过200个字符')
        return value.strip()

    def validate_pickup_time(self, value):
        if not value:
            raise serializers.ValidationError('上门时间不能为空')
        if value < timezone.now():
            raise serializers.ValidationError('上门时间不能早于当前时间')
        return value

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError('回收物品列表不能为空')
        if len(value) < 1:
            raise serializers.ValidationError('至少需要添加一件回收物品')
        if len(value) > 50:
            raise serializers.ValidationError('单次回收物品不能超过50件')
        
        valid_categories = [c[0] for c in ItemCategory.choices]
        for idx, item_data in enumerate(value):
            if 'name' not in item_data or not item_data['name'].strip():
                raise serializers.ValidationError(f'第{idx + 1}件物品名称不能为空')
            if len(item_data['name'].strip()) < 2:
                raise serializers.ValidationError(f'第{idx + 1}件物品名称至少需要2个字符')
            
            if 'category' not in item_data or not item_data['category']:
                raise serializers.ValidationError(f'第{idx + 1}件物品分类不能为空')
            if item_data['category'] not in valid_categories:
                raise serializers.ValidationError(f'第{idx + 1}件物品分类无效')
            
            quantity = item_data.get('quantity', 1)
            if quantity < 1:
                raise serializers.ValidationError(f'第{idx + 1}件物品数量必须大于0')
            if quantity > 1000:
                raise serializers.ValidationError(f'第{idx + 1}件物品数量不能超过1000')
            
            estimated_price = item_data.get('estimated_price', 0)
            if estimated_price < 0:
                raise serializers.ValidationError(f'第{idx + 1}件物品预估价格不能为负数')
            if estimated_price > 100000:
                raise serializers.ValidationError(f'第{idx + 1}件物品预估价格不能超过100000')
        
        return value

    def validate(self, data):
        pickup_time = data.get('pickup_time')
        if pickup_time:
            time_window_start = pickup_time - timedelta(hours=1)
            time_window_end = pickup_time + timedelta(hours=1)
            
            conflict_orders = Order.objects.filter(
                pickup_time__gte=time_window_start,
                pickup_time__lte=time_window_end,
                status__in=[OrderStatus.PENDING_PICKUP, OrderStatus.PICKED_UP]
            )
            
            if self.instance:
                conflict_orders = conflict_orders.exclude(id=self.instance.id)
            
            if conflict_orders.exists():
                raise serializers.ValidationError({
                    'pickup_time': '该时间段已有预约，请选择其他时间（前后1小时内不能重复预约）'
                })
        
        return data

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        auto_warehouse = validated_data.pop('auto_warehouse', False)
        auto_settle = validated_data.pop('auto_settle', False)
        user = self.context['request'].user
        
        order = Order.objects.create(**validated_data)
        order.created_by = user
        order.save()
        
        total_amount = 0
        for item_data in items_data:
            item = Item.objects.create(
                name=item_data['name'].strip(),
                category=item_data['category'],
                description=item_data.get('description', '').strip(),
                quantity=item_data.get('quantity', 1),
                estimated_price=item_data.get('estimated_price', 0),
                created_by=user
            )
            order_item = OrderItem.objects.create(
                order=order,
                item=item,
                quantity=item.quantity,
                unit_price=item.estimated_price or 0
            )
            total_amount += order_item.subtotal
        
        order.total_amount = total_amount
        order.save()

        if auto_warehouse:
            order.status = OrderStatus.PICKED_UP
            order.picked_up_at = timezone.now()
            order.save()
            order.auto_warehouse(user)
            
            if auto_settle:
                order.auto_settle(user)
        
        return order


class QualityCheckSerializer(serializers.ModelSerializer):
    result_display = serializers.CharField(source='get_result_display', read_only=True)
    order_no = serializers.CharField(source='order.order_no', read_only=True)

    class Meta:
        model = QualityCheck
        fields = ['id', 'order', 'order_no', 'checker', 'check_time', 'result', 'result_display', 'actual_amount', 'issue_description', 'created_at']
        read_only_fields = ['check_time', 'created_at']

    def validate_checker(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('质检人姓名不能为空')
        if len(value.strip()) < 2:
            raise serializers.ValidationError('质检人姓名至少需要2个字符')
        return value.strip()

    def validate_result(self, value):
        if not value:
            raise serializers.ValidationError('质检结果不能为空')
        if value not in [QualityCheck.CHECK_PASS, QualityCheck.CHECK_FAIL]:
            raise serializers.ValidationError('无效的质检结果')
        return value

    def validate_actual_amount(self, value):
        if value is None:
            raise serializers.ValidationError('实际金额不能为空')
        if value < 0:
            raise serializers.ValidationError('实际金额不能为负数')
        if value > 1000000:
            raise serializers.ValidationError('实际金额不能超过1000000')
        return value


class SettlementSerializer(serializers.ModelSerializer):
    order_no = serializers.CharField(source='order.order_no', read_only=True)

    class Meta:
        model = Settlement
        fields = ['id', 'order', 'order_no', 'settle_time', 'settle_amount', 'operator', 'remark']
        read_only_fields = ['settle_time']

    def validate_operator(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('操作员姓名不能为空')
        if len(value.strip()) < 2:
            raise serializers.ValidationError('操作员姓名至少需要2个字符')
        return value.strip()

    def validate_settle_amount(self, value):
        if value is None:
            raise serializers.ValidationError('结算金额不能为空')
        if value < 0:
            raise serializers.ValidationError('结算金额不能为负数')
        if value > 1000000:
            raise serializers.ValidationError('结算金额不能超过1000000')
        return value


class EstimateSerializer(serializers.Serializer):
    estimated_prices = serializers.ListField(child=serializers.DictField())
    auto_warehouse = serializers.BooleanField(default=False)
    auto_settle = serializers.BooleanField(default=False)

    def validate_estimated_prices(self, value):
        if not value:
            raise serializers.ValidationError('估价列表不能为空')
        for idx, price_data in enumerate(value):
            if 'price' not in price_data:
                raise serializers.ValidationError(f'第{idx + 1}个估价缺少price字段')
            price = price_data['price']
            if price < 0:
                raise serializers.ValidationError(f'第{idx + 1}个估价不能为负数')
            if price > 100000:
                raise serializers.ValidationError(f'第{idx + 1}个估价不能超过100000')
        return value


class PickupSerializer(serializers.Serializer):
    auto_warehouse = serializers.BooleanField(default=False)
    auto_settle = serializers.BooleanField(default=False)


class WarehouseSerializer(serializers.Serializer):
    checker = serializers.CharField(max_length=100)
    result = serializers.ChoiceField(choices=QualityCheck.CHECK_RESULT)
    actual_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    issue_description = serializers.CharField(required=False, allow_blank=True)
    auto_settle = serializers.BooleanField(default=False)

    def validate_checker(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('质检人姓名不能为空')
        if len(value.strip()) < 2:
            raise serializers.ValidationError('质检人姓名至少需要2个字符')
        return value.strip()

    def validate_actual_amount(self, value):
        if value < 0:
            raise serializers.ValidationError('实际金额不能为负数')
        if value > 1000000:
            raise serializers.ValidationError('实际金额不能超过1000000')
        return value


class CompleteSerializer(serializers.Serializer):
    operator = serializers.CharField(max_length=100)
    remark = serializers.CharField(required=False, allow_blank=True)

    def validate_operator(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('操作员姓名不能为空')
        if len(value.strip()) < 2:
            raise serializers.ValidationError('操作员姓名至少需要2个字符')
        return value.strip()


class AssignRecyclerSerializer(serializers.Serializer):
    recycler_id = serializers.IntegerField()

    def validate_recycler_id(self, value):
        try:
            user = User.objects.get(id=value)
            if user.profile.role != UserRole.RECYCLER:
                raise serializers.ValidationError('该用户不是回收员')
        except User.DoesNotExist:
            raise serializers.ValidationError('用户不存在')
        return value
