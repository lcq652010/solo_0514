from rest_framework import serializers
from .models import Building, House, Owner


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': True, 'error_messages': {'required': '楼栋名称不能为空'}},
            'address': {'required': True, 'error_messages': {'required': '楼栋地址不能为空'}},
            'total_floors': {'required': True, 'error_messages': {'required': '总楼层数不能为空'}}
        }

    def validate_total_floors(self, value):
        if value <= 0:
            raise serializers.ValidationError('总楼层数必须大于0')
        return value


class HouseSerializer(serializers.ModelSerializer):
    building_name = serializers.CharField(source='building.name', read_only=True)

    class Meta:
        model = House
        fields = '__all__'
        extra_kwargs = {
            'building': {'required': True, 'error_messages': {'required': '所属楼栋不能为空'}},
            'room_number': {'required': True, 'error_messages': {'required': '房间号不能为空'}},
            'floor': {'required': True, 'error_messages': {'required': '楼层不能为空'}},
            'area': {'required': True, 'error_messages': {'required': '面积不能为空'}}
        }

    def validate_area(self, value):
        if value <= 0:
            raise serializers.ValidationError('面积必须大于0')
        return value

    def validate_floor(self, value):
        if value <= 0:
            raise serializers.ValidationError('楼层必须大于0')
        return value


class OwnerSerializer(serializers.ModelSerializer):
    house_info = serializers.SerializerMethodField()
    full_room_number = serializers.SerializerMethodField()

    class Meta:
        model = Owner
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': True, 'error_messages': {'required': '业主姓名不能为空'}},
            'phone': {'required': True, 'error_messages': {'required': '联系电话不能为空'}},
            'id_card': {'required': True, 'error_messages': {'required': '身份证号不能为空'}},
            'house': {'required': True, 'error_messages': {'required': '所属房屋不能为空'}}
        }

    def validate_phone(self, value):
        if len(value) < 11:
            raise serializers.ValidationError('联系电话格式不正确')
        return value

    def validate_id_card(self, value):
        if len(value) not in [15, 18]:
            raise serializers.ValidationError('身份证号格式不正确')
        return value

    def get_house_info(self, obj):
        return {
            'id': obj.house.id,
            'building': obj.house.building.name,
            'room_number': obj.house.room_number,
            'area': str(obj.house.area)
        }

    def get_full_room_number(self, obj):
        return f'{obj.house.building.name} {obj.house.room_number}'
