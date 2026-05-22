from rest_framework import serializers
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Package, Customer, Photographer, Appointment, Order, Settlement, PhotoSelection, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'role')

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(**validated_data)
        user.userprofile.role = role
        user.userprofile.save()
        return user


class PhotoSelectionSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source='order.order_number', read_only=True)

    class Meta:
        model = PhotoSelection
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class PackageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, error_messages={'required': '套餐名称不能为空'})
    price = serializers.DecimalField(
        required=True, 
        max_digits=10, 
        decimal_places=2, 
        min_value=0,
        error_messages={
            'required': '套餐价格不能为空',
            'min_value': '套餐价格不能为负数'
        }
    )
    days = serializers.IntegerField(
        required=True, 
        min_value=1,
        error_messages={
            'required': '拍摄天数不能为空',
            'min_value': '拍摄天数至少为1天'
        }
    )
    photos_count = serializers.IntegerField(
        required=True, 
        min_value=1,
        error_messages={
            'required': '精修照片数量不能为空',
            'min_value': '精修照片数量至少为1张'
        }
    )

    class Meta:
        model = Package
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class CustomerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, error_messages={'required': '客户姓名不能为空'})
    phone = serializers.CharField(required=True, error_messages={'required': '联系电话不能为空'})

    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate_phone(self, value):
        if len(value) < 7:
            raise serializers.ValidationError('电话号码格式不正确')
        return value


class PhotographerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, error_messages={'required': '摄影师姓名不能为空'})
    phone = serializers.CharField(required=True, error_messages={'required': '联系电话不能为空'})
    level = serializers.CharField(required=True, error_messages={'required': '摄影师级别不能为空'})

    class Meta:
        model = Photographer
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class AppointmentSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    package_name = serializers.CharField(source='package.name', read_only=True)
    photographer_name = serializers.CharField(source='photographer.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    customer = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Customer.objects.all(),
        error_messages={'required': '请选择客户'}
    )
    package = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Package.objects.all(),
        error_messages={'required': '请选择套餐'}
    )
    photographer = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Photographer.objects.all(),
        error_messages={'required': '请选择摄影师'}
    )
    appointment_date = serializers.DateField(required=True, error_messages={'required': '请选择预约日期'})
    appointment_time = serializers.TimeField(required=True, error_messages={'required': '请选择预约时间'})

    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate(self, data):
        photographer = data.get('photographer')
        appointment_date = data.get('appointment_date')
        appointment_time = data.get('appointment_time')
        instance = self.instance

        conflict = Appointment.objects.filter(
            Q(photographer=photographer) &
            Q(appointment_date=appointment_date) &
            Q(appointment_time=appointment_time) &
            Q(status__in=['pending', 'confirmed'])
        )
        if instance:
            conflict = conflict.exclude(id=instance.id)
        
        if conflict.exists():
            raise serializers.ValidationError('该摄影师在当前时间段已有预约')

        order_conflict = Order.objects.filter(
            Q(photographer=photographer) &
            Q(shoot_date=appointment_date) &
            Q(shoot_time=appointment_time) &
            Q(status__in=['pending', 'shooting'])
        )
        if order_conflict.exists():
            raise serializers.ValidationError('该摄影师在当前时间段已有拍摄订单')

        return data


class OrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    package_name = serializers.CharField(source='package.name', read_only=True)
    photographer_name = serializers.CharField(source='photographer.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    remaining_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    photo_selection = PhotoSelectionSerializer(source='photoselection', read_only=True)

    customer = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Customer.objects.all(),
        error_messages={'required': '请选择客户'}
    )
    package = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Package.objects.all(),
        error_messages={'required': '请选择套餐'}
    )
    photographer = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Photographer.objects.all(),
        error_messages={'required': '请选择摄影师'}
    )
    shoot_date = serializers.DateField(required=True, error_messages={'required': '请选择拍摄日期'})
    shoot_time = serializers.TimeField(required=True, error_messages={'required': '请选择拍摄时间'})
    location = serializers.CharField(required=True, error_messages={'required': '请填写拍摄地点'})
    total_amount = serializers.DecimalField(
        required=True,
        max_digits=10,
        decimal_places=2,
        min_value=0,
        error_messages={
            'required': '请填写订单总金额',
            'min_value': '订单总金额不能为负数'
        }
    )
    deposit = serializers.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        min_value=0,
        default=0,
        error_messages={'min_value': '定金不能为负数'}
    )

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('order_number', 'created_at', 'updated_at', 'is_settled')

    def validate(self, data):
        total_amount = data.get('total_amount', 0)
        deposit = data.get('deposit', 0)
        
        if deposit > total_amount:
            raise serializers.ValidationError('定金不能大于订单总金额')

        photographer = data.get('photographer')
        shoot_date = data.get('shoot_date')
        shoot_time = data.get('shoot_time')
        instance = self.instance

        order_conflict = Order.objects.filter(
            Q(photographer=photographer) &
            Q(shoot_date=shoot_date) &
            Q(shoot_time=shoot_time) &
            Q(status__in=['pending', 'shooting'])
        )
        if instance:
            order_conflict = order_conflict.exclude(id=instance.id)
        
        if order_conflict.exists():
            raise serializers.ValidationError('该摄影师在当前时间段已有拍摄订单')

        appointment_conflict = Appointment.objects.filter(
            Q(photographer=photographer) &
            Q(appointment_date=shoot_date) &
            Q(appointment_time=shoot_time) &
            Q(status__in=['pending', 'confirmed'])
        )
        if appointment_conflict.exists():
            raise serializers.ValidationError('该摄影师在当前时间段已有预约')

        return data


class SettlementSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    balance_amount = serializers.DecimalField(
        read_only=True,
        max_digits=10,
        decimal_places=2
    )
    payment_method = serializers.CharField(required=True, error_messages={'required': '请选择支付方式'})

    class Meta:
        model = Settlement
        fields = '__all__'
        read_only_fields = ('created_at', 'balance_amount')
