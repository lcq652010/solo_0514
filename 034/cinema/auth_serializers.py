from rest_framework import serializers
from django.contrib.auth.models import User, Group

class UserSerializer(serializers.ModelSerializer):
    group_names = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()
    is_seller = serializers.SerializerMethodField()
    is_checker = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'is_active', 'date_joined', 'group_names', 'is_admin', 
                  'is_seller', 'is_checker']
        read_only_fields = ['date_joined']

    def get_group_names(self, obj):
        return [group.name for group in obj.groups.all()]

    def get_is_admin(self, obj):
        return obj.groups.filter(name='管理员').exists()

    def get_is_seller(self, obj):
        return obj.groups.filter(name='售票员').exists()

    def get_is_checker(self, obj):
        return obj.groups.filter(name='检票员').exists()

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    groups = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'groups']

    def validate_groups(self, value):
        valid_groups = ['管理员', '售票员', '检票员']
        for group_name in value:
            if group_name not in valid_groups:
                raise serializers.ValidationError(
                    f'无效的用户组: {group_name}，可选值: {valid_groups}'
                )
        return value

    def create(self, validated_data):
        group_names = validated_data.pop('groups')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(
            password=password,
            is_active=True,
            **validated_data
        )

        for group_name in group_names:
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('原密码不正确')
        return value

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']
