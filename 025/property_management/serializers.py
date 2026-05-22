from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'role']

    def get_role(self, obj):
        if obj.is_superuser:
            return 'super_admin'
        if obj.is_staff:
            return 'admin'
        if hasattr(obj, 'repairworker') and obj.repairworker and obj.repairworker.id:
            return 'worker'
        if hasattr(obj, 'owner') and obj.owner and obj.owner.id:
            return 'owner'
        return 'user'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, error_messages={'required': '用户名不能为空'})
    password = serializers.CharField(required=True, error_messages={'required': '密码不能为空'})

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('用户名或密码错误')
        if not user.is_active:
            raise serializers.ValidationError('用户已被禁用')
        attrs['user'] = user
        return attrs
