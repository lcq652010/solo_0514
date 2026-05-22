from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Q
from .models import UserProfile, Customer, Device, RepairOrder, Notification, ArchivedOrder


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['role', 'phone', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': True, 'allow_blank': False, 'error_messages': {'required': '客户姓名不能为空', 'blank': '客户姓名不能为空'}},
            'phone': {'required': True, 'allow_blank': False, 'error_messages': {'required': '联系电话不能为空', 'blank': '联系电话不能为空'}},
        }
    
    def validate_phone(self, value):
        if len(value) < 7 or len(value) > 20:
            raise serializers.ValidationError('电话号码长度应在7-20位之间')
        return value


class DeviceSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    
    class Meta:
        model = Device
        fields = '__all__'
        extra_kwargs = {
            'customer': {'required': True, 'error_messages': {'required': '必须选择所属客户'}},
            'device_type': {'required': True, 'error_messages': {'required': '设备类型不能为空'}},
            'brand': {'required': True, 'allow_blank': False, 'error_messages': {'required': '品牌不能为空', 'blank': '品牌不能为空'}},
            'model': {'required': True, 'allow_blank': False, 'error_messages': {'required': '型号不能为空', 'blank': '型号不能为空'}},
        }


class RepairOrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    customer_phone = serializers.CharField(source='customer.phone', read_only=True)
    device_info = serializers.SerializerMethodField()
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = RepairOrder
        fields = '__all__'
        read_only_fields = ['order_number', 'created_by', 'created_at', 'updated_at']
        extra_kwargs = {
            'customer': {'required': True, 'error_messages': {'required': '必须选择客户'}},
            'device': {'required': True, 'error_messages': {'required': '必须选择设备'}},
            'fault_description': {'required': True, 'allow_blank': False, 'error_messages': {'required': '故障描述不能为空', 'blank': '故障描述不能为空'}},
        }
    
    def get_device_info(self, obj):
        return f'{obj.device.brand} {obj.device.model}'
    
    def validate_estimated_cost(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError('预估费用不能为负数')
        if value is not None and value > 999999.99:
            raise serializers.ValidationError('预估费用超出最大限制')
        return value
    
    def validate_actual_cost(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError('实际费用不能为负数')
        if value is not None and value > 999999.99:
            raise serializers.ValidationError('实际费用超出最大限制')
        return value
    
    def validate(self, data):
        if 'device' in data and 'customer' in data:
            device = data['device']
            customer = data['customer']
            if device.customer_id != customer.id:
                raise serializers.ValidationError({'device': '该设备不属于所选客户'})
        
        if 'assigned_to' in data and data['assigned_to']:
            engineer = data['assigned_to']
            if engineer.profile.role != 'engineer':
                raise serializers.ValidationError({'assigned_to': '只能将工单分配给工程师角色的用户'})
            
            if self.instance is None:
                active_orders = RepairOrder.objects.filter(
                    assigned_to=engineer,
                    status__in=['pending', 'diagnosing', 'repairing', 'waiting_parts']
                ).count()
            else:
                active_orders = RepairOrder.objects.filter(
                    ~Q(id=self.instance.id),
                    assigned_to=engineer,
                    status__in=['pending', 'diagnosing', 'repairing', 'waiting_parts']
                ).count()
            
            if active_orders >= 10:
                raise serializers.ValidationError({'assigned_to': f'该工程师当前已有{active_orders}个活跃工单，派单数量已达上限'})
        
        return data
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class ArchivedOrderSerializer(serializers.ModelSerializer):
    archived_by_name = serializers.CharField(source='archived_by.username', read_only=True)
    
    class Meta:
        model = ArchivedOrder
        fields = '__all__'


class RepairOrderListSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    device_info = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = RepairOrder
        fields = ['id', 'order_number', 'customer_name', 'device_info', 'status', 'status_display', 'created_at', 'completed_at']
    
    def get_device_info(self, obj):
        return f'{obj.device.brand} {obj.device.model}'
