from rest_framework import serializers
from django.db.models import Q
from .models import Product, Member, PurchaseOrder, PurchaseItem, SalesOrder, SalesItem, StockLog, PointsLog, User


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'role_display', 'phone', 'is_active', 'date_joined']
        read_only_fields = ['date_joined']
        extra_kwargs = {
            'username': {'required': True, 'error_messages': {'required': '用户名不能为空'}},
            'role': {'required': True, 'error_messages': {'required': '角色不能为空'}},
        }


class ProductSerializer(serializers.ModelSerializer):
    """商品序列化器"""
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    stock_status = serializers.SerializerMethodField()
    stock_status_display = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': True, 'allow_blank': False, 'error_messages': {'required': '商品名称不能为空', 'blank': '商品名称不能为空'}},
            'category': {'required': True, 'error_messages': {'required': '商品分类不能为空'}},
            'price': {'required': True, 'error_messages': {'required': '售价不能为空'}},
            'cost_price': {'required': True, 'error_messages': {'required': '成本价不能为空'}},
        }

    def get_stock_status(self, obj):
        """获取库存状态: low-库存不足, normal-库存正常, sufficient-库存充足"""
        if obj.stock <= 0:
            return 'out_of_stock'
        elif obj.stock < 10:
            return 'low'
        elif obj.stock < 50:
            return 'normal'
        else:
            return 'sufficient'

    def get_stock_status_display(self, obj):
        """获取库存状态显示文本"""
        status_map = {
            'out_of_stock': '缺货',
            'low': '库存不足',
            'normal': '库存正常',
            'sufficient': '库存充足'
        }
        return status_map.get(self.get_stock_status(obj), '未知')

    def validate_price(self, value):
        """校验售价合法性"""
        if value <= 0:
            raise serializers.ValidationError('售价必须大于0')
        if value > 999999.99:
            raise serializers.ValidationError('售价超出最大限制')
        return value

    def validate_cost_price(self, value):
        """校验成本价合法性"""
        if value < 0:
            raise serializers.ValidationError('成本价不能为负数')
        if value > 999999.99:
            raise serializers.ValidationError('成本价超出最大限制')
        return value

    def validate_stock(self, value):
        """校验库存合法性"""
        if value < 0:
            raise serializers.ValidationError('库存不能为负数')
        return value

    def validate(self, data):
        """联合校验"""
        if 'price' in data and 'cost_price' in data:
            if data['price'] < data['cost_price']:
                raise serializers.ValidationError({'price': '售价不能低于成本价'})
        return data


class MemberSerializer(serializers.ModelSerializer):
    """会员序列化器"""

    class Meta:
        model = Member
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': True, 'allow_blank': False, 'error_messages': {'required': '会员姓名不能为空', 'blank': '会员姓名不能为空'}},
            'phone': {'required': True, 'allow_blank': False, 'error_messages': {'required': '手机号不能为空', 'blank': '手机号不能为空'}},
        }

    def validate_phone(self, value):
        """校验手机号格式"""
        if len(value) < 11:
            raise serializers.ValidationError('手机号格式不正确')
        if not value.isdigit():
            raise serializers.ValidationError('手机号必须为数字')
        return value

    def validate_points(self, value):
        """校验积分合法性"""
        if value < 0:
            raise serializers.ValidationError('积分不能为负数')
        return value


class PurchaseItemSerializer(serializers.ModelSerializer):
    """采购明细序列化器"""
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = PurchaseItem
        fields = '__all__'


class PurchaseOrderSerializer(serializers.ModelSerializer):
    """采购订单序列化器"""
    items = PurchaseItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = '__all__'


class SalesItemSerializer(serializers.ModelSerializer):
    """销售明细序列化器"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_id = serializers.CharField(source='product.product_id', read_only=True)

    class Meta:
        model = SalesItem
        fields = '__all__'


class SalesOrderSerializer(serializers.ModelSerializer):
    """销售订单序列化器"""
    items = SalesItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    member_name = serializers.CharField(source='member.name', read_only=True)
    member_phone = serializers.CharField(source='member.phone', read_only=True)

    class Meta:
        model = SalesOrder
        fields = '__all__'


class StockLogSerializer(serializers.ModelSerializer):
    """库存日志序列化器"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = StockLog
        fields = '__all__'


class PointsLogSerializer(serializers.ModelSerializer):
    """积分日志序列化器"""
    member_name = serializers.CharField(source='member.name', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = PointsLog
        fields = '__all__'


class SalesItemCreateSerializer(serializers.Serializer):
    """销售商品创建序列化器"""
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class SalesOrderCreateSerializer(serializers.Serializer):
    """创建销售订单序列化器"""
    member_id = serializers.IntegerField(required=False, allow_null=True)
    items = SalesItemCreateSerializer(many=True)
    points_used = serializers.IntegerField(default=0, min_value=0)
    cashier = serializers.CharField(default='收银员')
    remark = serializers.CharField(required=False, allow_blank=True)


class PurchaseItemCreateSerializer(serializers.Serializer):
    """采购商品创建序列化器"""
    product_id = serializers.IntegerField(required=True, error_messages={'required': '商品ID不能为空'})
    quantity = serializers.IntegerField(min_value=1, error_messages={'min_value': '采购数量必须大于0', 'required': '采购数量不能为空'})
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True, error_messages={'required': '单价不能为空'})

    def validate_unit_price(self, value):
        """校验单价合法性"""
        if value <= 0:
            raise serializers.ValidationError('单价必须大于0')
        if value > 999999.99:
            raise serializers.ValidationError('单价超出最大限制')
        return value


class PurchaseOrderCreateSerializer(serializers.Serializer):
    """创建采购订单序列化器"""
    supplier = serializers.CharField(max_length=100, required=True, error_messages={'required': '供应商不能为空', 'blank': '供应商不能为空'})
    items = PurchaseItemCreateSerializer(many=True, required=True, error_messages={'required': '采购商品列表不能为空'})
    remark = serializers.CharField(required=False, allow_blank=True)

    def validate_items(self, value):
        """校验商品列表"""
        if not value or len(value) == 0:
            raise serializers.ValidationError('至少选择一个采购商品')
        
        product_ids = [item['product_id'] for item in value]
        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError('存在重复商品')
        return value


class SalesItemCreateSerializer(serializers.Serializer):
    """销售商品创建序列化器"""
    product_id = serializers.IntegerField(required=True, error_messages={'required': '商品ID不能为空'})
    quantity = serializers.IntegerField(min_value=1, error_messages={'min_value': '销售数量必须大于0', 'required': '销售数量不能为空'})


class SalesOrderCreateSerializer(serializers.Serializer):
    """创建销售订单序列化器"""
    member_id = serializers.IntegerField(required=False, allow_null=True)
    items = SalesItemCreateSerializer(many=True, required=True, error_messages={'required': '商品列表不能为空'})
    points_used = serializers.IntegerField(default=0, min_value=0, error_messages={'min_value': '使用积分不能为负数'})
    cashier = serializers.CharField(default='收银员')
    remark = serializers.CharField(required=False, allow_blank=True)

    def validate_items(self, value):
        """校验商品列表"""
        if not value or len(value) == 0:
            raise serializers.ValidationError('至少选择一个商品')
        
        product_ids = [item['product_id'] for item in value]
        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError('存在重复商品')
        return value


class StockAdjustSerializer(serializers.Serializer):
    """库存调整序列化器"""
    quantity = serializers.IntegerField(required=True, error_messages={'required': '调整数量不能为空'})
    remark = serializers.CharField(required=False, allow_blank=True)
