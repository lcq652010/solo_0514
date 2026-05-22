import re
from django.contrib.auth import authenticate
from django.db.models import Q
from datetime import datetime, timedelta
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import User, Customer, Service, Aunt, Order, Review, OrderArchive, AuntStatistics


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'phone', 'avatar', 'created_at')
        read_only_fields = ('id', 'created_at')


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, default='customer')

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password', 'role', 'phone')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'password': '密码不一致'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('用户名或密码错误')
        attrs['user'] = user
        return attrs


class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    order_count = serializers.IntegerField(source='get_order_count', read_only=True)
    completed_order_count = serializers.IntegerField(source='get_completed_order_count', read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer()

    class Meta:
        model = Customer
        fields = ('user', 'name', 'gender', 'phone', 'address')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data.pop('confirm_password')
        user_data['role'] = 'customer'
        user = User.objects.create_user(**user_data)
        customer = Customer.objects.create(user=user, **validated_data)
        Token.objects.create(user=user)
        return customer


class AuntStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuntStatistics
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('服务价格必须大于0')
        if value > 100000:
            raise serializers.ValidationError('服务价格不能超过100000元')
        return value

    def validate_duration(self, value):
        if value <= 0:
            raise serializers.ValidationError('服务时长必须大于0')
        if value > 720:
            raise serializers.ValidationError('服务时长不能超过720小时')
        return value


class AuntSerializer(serializers.ModelSerializer):
    skills = ServiceSerializer(many=True, read_only=True)
    skill_ids = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        source='skills',
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = Aunt
        fields = '__all__'

    def validate_phone(self, value):
        if not value:
            raise serializers.ValidationError('联系电话不能为空')
        phone_pattern = r'^1[3-9]\d{9}$'
        if not re.match(phone_pattern, value):
            raise serializers.ValidationError('请输入正确的手机号码格式')
        return value

    def validate_id_card(self, value):
        if not value:
            raise serializers.ValidationError('身份证号不能为空')
        id_card_pattern = r'^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$'
        if not re.match(id_card_pattern, value):
            raise serializers.ValidationError('请输入正确的身份证号格式')
        return value

    def validate_age(self, value):
        if value < 18:
            raise serializers.ValidationError('年龄不能小于18岁')
        if value > 70:
            raise serializers.ValidationError('年龄不能大于70岁')
        return value

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('姓名不能为空')
        return value


class OrderSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)
    aunt_name = serializers.CharField(source='aunt.name', read_only=True, allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('order_no', 'created_at', 'updated_at')

    def validate_customer_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('客户姓名不能为空')
        return value.strip()

    def validate_customer_phone(self, value):
        if not value:
            raise serializers.ValidationError('客户电话不能为空')
        phone_pattern = r'^1[3-9]\d{9}$'
        if not re.match(phone_pattern, value):
            raise serializers.ValidationError('请输入正确的手机号码格式')
        return value

    def validate_customer_address(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('服务地址不能为空')
        return value.strip()

    def validate_duration(self, value):
        if value <= 0:
            raise serializers.ValidationError('服务时长必须大于0')
        if value > 24:
            raise serializers.ValidationError('单次服务时长不能超过24小时')
        return value

    def validate_total_price(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError('总金额不能为负数')
        if value is not None and value > 100000:
            raise serializers.ValidationError('总金额不能超过100000元')
        return value

    def validate_service_date(self, value):
        from django.utils import timezone
        today = timezone.now().date()
        if value < today:
            raise serializers.ValidationError('服务日期不能早于今天')
        return value

    def validate(self, attrs):
        if 'service' in attrs and 'duration' in attrs:
            expected_price = attrs['service'].price * attrs['duration']
            if 'total_price' in attrs and attrs['total_price'] is not None:
                if abs(attrs['total_price'] - expected_price) > 0.01:
                    raise serializers.ValidationError(
                        f'总金额计算有误，应为: {expected_price}元'
                    )
        return attrs


class ReviewSerializer(serializers.ModelSerializer):
    order_no = serializers.CharField(source='order.order_no', read_only=True)
    aunt_name = serializers.CharField(source='aunt.name', read_only=True)
    rating_display = serializers.CharField(source='get_rating_display', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('created_at',)

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError('评分必须在1-5之间')
        return value


class OrderDispatchSerializer(serializers.Serializer):
    aunt_id = serializers.IntegerField()

    def validate_aunt_id(self, value):
        try:
            Aunt.objects.get(id=value, status='available')
        except Aunt.DoesNotExist:
            raise serializers.ValidationError('该阿姨不可用或不存在')
        return value

    def validate(self, attrs):
        order = self.context.get('order')
        aunt_id = attrs.get('aunt_id')
        
        if order and aunt_id:
            existing_orders = Order.objects.filter(
                aunt_id=aunt_id,
                status='servicing'
            )
            if existing_orders.exists():
                raise serializers.ValidationError('该阿姨已有正在进行的订单，派单冲突')
            
            service_datetime = datetime.combine(order.service_date, order.service_time)
            end_datetime = service_datetime + timedelta(hours=order.duration)
            
            conflict_orders = Order.objects.filter(
                aunt_id=aunt_id,
                status__in=['pending', 'servicing'],
                service_date=order.service_date
            ).exclude(id=order.id)
            
            for conflict_order in conflict_orders:
                conflict_start = datetime.combine(conflict_order.service_date, conflict_order.service_time)
                conflict_end = conflict_start + timedelta(hours=conflict_order.duration)
                if (service_datetime < conflict_end and end_datetime > conflict_start):
                    raise serializers.ValidationError(f'该阿姨在同一时间段已有订单: {conflict_order.order_no}')
        
        return attrs


class OrderStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)


class OrderArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderArchive
        fields = '__all__'


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=6)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': '两次输入的新密码不一致'})
        return attrs
