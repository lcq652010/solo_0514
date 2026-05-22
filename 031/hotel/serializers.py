from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Room, Guest, Order, UserProfile
from datetime import datetime, date
from django.db.models import Q


class UserProfileSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['role', 'role_display', 'phone', 'real_name', 'create_time', 'update_time']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)
    role_display = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'profile', 'role_display']
        read_only_fields = ['id']

    def get_role_display(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.get_role_display()
        return None


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, required=True)
    real_name = serializers.CharField(required=False, max_length=50)
    phone = serializers.CharField(required=False, max_length=20)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'role', 'real_name', 'phone']

    def create(self, validated_data):
        role = validated_data.pop('role')
        real_name = validated_data.pop('real_name', None)
        phone = validated_data.pop('phone', None)
        password = validated_data.pop('password')

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        UserProfile.objects.create(
            user=user,
            role=role,
            real_name=real_name,
            phone=phone
        )

        return user


class RoomSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    room_type_display = serializers.CharField(source='get_room_type_display', read_only=True)
    clean_status_display = serializers.CharField(source='get_clean_status_display', read_only=True)
    cleaned_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = '__all__'
        extra_kwargs = {
            'room_number': {'required': True, 'error_messages': {'required': '房间号不能为空'}},
            'room_type': {'required': True, 'error_messages': {'required': '房间类型不能为空'}},
            'price': {'required': True, 'error_messages': {'required': '房间价格不能为空'}},
            'floor': {'required': True, 'error_messages': {'required': '楼层不能为空'}},
            'capacity': {'required': True, 'error_messages': {'required': '容纳人数不能为空'}},
        }

    def get_cleaned_by_name(self, obj):
        if obj.cleaned_by:
            if hasattr(obj.cleaned_by, 'profile') and obj.cleaned_by.profile.real_name:
                return obj.cleaned_by.profile.real_name
            return obj.cleaned_by.username
        return None

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('房间价格必须大于0')
        if value > 99999:
            raise serializers.ValidationError('房间价格不能超过99999')
        return value

    def validate_capacity(self, value):
        if value <= 0:
            raise serializers.ValidationError('容纳人数必须大于0')
        if value > 10:
            raise serializers.ValidationError('容纳人数不能超过10人')
        return value

    def validate_floor(self, value):
        if value <= 0:
            raise serializers.ValidationError('楼层必须大于0')
        if value > 100:
            raise serializers.ValidationError('楼层不能超过100层')
        return value


class RoomCleanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['clean_status']


class GuestSerializer(serializers.ModelSerializer):
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)

    class Meta:
        model = Guest
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': True, 'error_messages': {'required': '客人姓名不能为空'}},
            'id_card': {'required': True, 'error_messages': {'required': '身份证号不能为空'}},
            'phone': {'required': True, 'error_messages': {'required': '手机号不能为空'}},
            'gender': {'required': True, 'error_messages': {'required': '性别不能为空'}},
        }

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('客人姓名不能为空')
        if len(value) > 50:
            raise serializers.ValidationError('客人姓名不能超过50个字符')
        return value.strip()

    def validate_id_card(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('身份证号不能为空')
        if len(value) not in [15, 18]:
            raise serializers.ValidationError('身份证号长度不正确，应为15或18位')
        return value.strip()

    def validate_phone(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('手机号不能为空')
        if len(value) < 7 or len(value) > 20:
            raise serializers.ValidationError('手机号长度应在7-20位之间')
        return value.strip()


class OrderSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    guest_name = serializers.CharField(source='guest.name', read_only=True)
    guest_phone = serializers.CharField(source='guest.phone', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    room_type = serializers.CharField(source='room.get_room_type_display', read_only=True)
    checked_in_by_name = serializers.SerializerMethodField()
    checked_out_by_name = serializers.SerializerMethodField()
    overtime_info = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['order_number', 'total_amount', 'overtime_hours', 'overtime_fee', 'actual_days', 'refund_amount']
        extra_kwargs = {
            'guest': {'required': True, 'error_messages': {'required': '客人不能为空'}},
            'room': {'required': True, 'error_messages': {'required': '房间不能为空'}},
            'check_in_date': {'required': True, 'error_messages': {'required': '入住日期不能为空'}},
            'check_out_date': {'required': True, 'error_messages': {'required': '退房日期不能为空'}},
        }

    def get_checked_in_by_name(self, obj):
        if obj.checked_in_by:
            if hasattr(obj.checked_in_by, 'profile') and obj.checked_in_by.profile.real_name:
                return obj.checked_in_by.profile.real_name
            return obj.checked_in_by.username
        return None

    def get_checked_out_by_name(self, obj):
        if obj.checked_out_by:
            if hasattr(obj.checked_out_by, 'profile') and obj.checked_out_by.profile.real_name:
                return obj.checked_out_by.profile.real_name
            return obj.checked_out_by.username
        return None

    def get_overtime_info(self, obj):
        if obj.status == 'checked_in':
            return obj.calculate_overtime_fee()
        return None

    def validate(self, attrs):
        check_in_date = attrs.get('check_in_date')
        check_out_date = attrs.get('check_out_date')
        room = attrs.get('room')
        deposit = attrs.get('deposit', 0)

        if check_in_date and check_out_date:
            if check_in_date > check_out_date:
                raise serializers.ValidationError({'check_out_date': '退房日期不能早于入住日期'})
            if check_in_date < date.today():
                raise serializers.ValidationError({'check_in_date': '入住日期不能早于今天'})

            days = (check_out_date - check_in_date).days
            if days > 90:
                raise serializers.ValidationError({'check_out_date': '最长预订天数不能超过90天'})

        if room:
            if room.status not in ['available', 'reserved']:
                raise serializers.ValidationError({'room': '该房间当前不可用'})

        if deposit is not None and deposit < 0:
            raise serializers.ValidationError({'deposit': '押金不能为负数'})
        if deposit is not None and deposit > 100000:
            raise serializers.ValidationError({'deposit': '押金不能超过100000'})

        instance = self.instance
        if instance and room and check_in_date and check_out_date:
            conflicting_orders = Order.objects.filter(
                room=room,
                status__in=['pending', 'checked_in']
            ).exclude(id=instance.id).filter(
                Q(check_in_date__lte=check_out_date) & Q(check_out_date__gte=check_in_date)
            )
            if conflicting_orders.exists():
                raise serializers.ValidationError({'room': '该房间在所选时段已被预订'})

        return attrs


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['guest', 'room', 'check_in_date', 'check_out_date', 'deposit', 'remark']
        extra_kwargs = {
            'guest': {'required': True, 'error_messages': {'required': '客人不能为空'}},
            'room': {'required': True, 'error_messages': {'required': '房间不能为空'}},
            'check_in_date': {'required': True, 'error_messages': {'required': '入住日期不能为空'}},
            'check_out_date': {'required': True, 'error_messages': {'required': '退房日期不能为空'}},
        }

    def validate(self, attrs):
        check_in_date = attrs['check_in_date']
        check_out_date = attrs['check_out_date']
        room = attrs['room']
        deposit = attrs.get('deposit', 0)

        if check_in_date > check_out_date:
            raise serializers.ValidationError({'check_out_date': '退房日期不能早于入住日期'})
        if check_in_date < date.today():
            raise serializers.ValidationError({'check_in_date': '入住日期不能早于今天'})

        days = (check_out_date - check_in_date).days
        if days <= 0:
            days = 1
        if days > 90:
            raise serializers.ValidationError({'check_out_date': '最长预订天数不能超过90天'})

        if room.status not in ['available', 'reserved']:
            raise serializers.ValidationError({'room': '该房间当前不可用'})

        conflicting_orders = Order.objects.filter(
            room=room,
            status__in=['pending', 'checked_in']
        ).filter(
            Q(check_in_date__lte=check_out_date) & Q(check_out_date__gte=check_in_date)
        )
        if conflicting_orders.exists():
            raise serializers.ValidationError({'room': '该房间在所选时段已被预订'})

        if deposit < 0:
            raise serializers.ValidationError({'deposit': '押金不能为负数'})
        if deposit > 100000:
            raise serializers.ValidationError({'deposit': '押金不能超过100000'})

        attrs['days'] = days
        attrs['daily_price'] = room.price
        attrs['total_amount'] = room.price * days

        return attrs

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        room = validated_data['room']
        room.status = 'reserved'
        room.save()
        return order


class CheckInSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(
        required=True,
        error_messages={'required': '订单ID不能为空'}
    )

    def validate_order_id(self, value):
        if value <= 0:
            raise serializers.ValidationError('订单ID必须大于0')
        try:
            order = Order.objects.get(id=value)
        except Order.DoesNotExist:
            raise serializers.ValidationError('订单不存在')

        if order.status != 'pending':
            raise serializers.ValidationError('该订单状态不允许入住，当前状态为待入住才可办理入住')

        return value


class CheckOutSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(
        required=True,
        error_messages={'required': '订单ID不能为空'}
    )

    def validate_order_id(self, value):
        if value <= 0:
            raise serializers.ValidationError('订单ID必须大于0')
        try:
            order = Order.objects.get(id=value)
        except Order.DoesNotExist:
            raise serializers.ValidationError('订单不存在')

        if order.status != 'checked_in':
            raise serializers.ValidationError('该订单状态不允许退房，当前状态为已入住才可办理退房')

        return value
