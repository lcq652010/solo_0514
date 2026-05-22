from rest_framework import serializers
from .models import RepairWorker, Repair, RepairLog


class RepairWorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairWorker
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': True, 'error_messages': {'required': '维修人员姓名不能为空'}},
            'phone': {'required': True, 'error_messages': {'required': '联系电话不能为空'}},
            'skill': {'required': True, 'error_messages': {'required': '技能专长不能为空'}}
        }


class RepairSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.name', read_only=True)
    house_info = serializers.SerializerMethodField()
    full_room_number = serializers.SerializerMethodField()
    worker_name = serializers.CharField(source='worker.name', read_only=True)
    worker_phone = serializers.CharField(source='worker.phone', read_only=True)

    class Meta:
        model = Repair
        fields = '__all__'
        extra_kwargs = {
            'owner': {'required': True, 'error_messages': {'required': '报修业主不能为空'}},
            'house': {'required': True, 'error_messages': {'required': '所属房屋不能为空'}},
            'repair_type': {'required': True, 'error_messages': {'required': '报修类型不能为空'}},
            'title': {'required': True, 'error_messages': {'required': '报修标题不能为空'}},
            'description': {'required': True, 'error_messages': {'required': '问题描述不能为空'}},
            'contact_person': {'required': True, 'error_messages': {'required': '联系人不能为空'}},
            'contact_phone': {'required': True, 'error_messages': {'required': '联系电话不能为空'}}
        }

    def get_house_info(self, obj):
        return {
            'id': obj.house.id,
            'building': obj.house.building.name,
            'room_number': obj.house.room_number
        }

    def get_full_room_number(self, obj):
        return f'{obj.house.building.name} {obj.house.room_number}'


class RepairLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairLog
        fields = '__all__'
        extra_kwargs = {
            'repair': {'required': True, 'error_messages': {'required': '关联工单不能为空'}},
            'action': {'required': True, 'error_messages': {'required': '操作类型不能为空'}},
            'description': {'required': True, 'error_messages': {'required': '操作描述不能为空'}},
            'operator': {'required': True, 'error_messages': {'required': '操作人不能为空'}}
        }
