from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, StockAlertMessage


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active']
        read_only_fields = ['id']


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'username', 'email', 'role', 'role_display', 'phone', 'department', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES)
    phone = serializers.CharField(required=False, allow_blank=True)
    department = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role', 'phone', 'department']

    def create(self, validated_data):
        role = validated_data.pop('role')
        phone = validated_data.pop('phone', '')
        department = validated_data.pop('department', '')
        
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(
            user=user,
            role=role,
            phone=phone,
            department=department
        )
        return user


class StockAlertMessageSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_code = serializers.CharField(source='product.product_code', read_only=True)
    alert_level_display = serializers.CharField(source='get_alert_level_display', read_only=True)

    class Meta:
        model = StockAlertMessage
        fields = '__all__'
        read_only_fields = ['created_at', 'read_at']
