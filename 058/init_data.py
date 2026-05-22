import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_fostering.settings')
django.setup()

from fostering.models import Room


def init_rooms():
    room_data = [
        {'room_number': 'S001', 'room_type': 'standard', 'suitable_size': 'small', 
         'daily_price': 60, 'overtime_multiplier': 1.2, 
         'description': '标准间-仅限小型宠物', 'max_pets': 1},
        {'room_number': 'S002', 'room_type': 'standard', 'suitable_size': 'small', 
         'daily_price': 60, 'overtime_multiplier': 1.2, 
         'description': '标准间-仅限小型宠物', 'max_pets': 1},
        {'room_number': 'S003', 'room_type': 'standard', 'suitable_size': 'small_medium', 
         'daily_price': 80, 'overtime_multiplier': 1.3, 
         'description': '标准间-中小型宠物', 'max_pets': 1},
        {'room_number': 'D001', 'room_type': 'deluxe', 'suitable_size': 'small_medium', 
         'daily_price': 120, 'overtime_multiplier': 1.5, 
         'description': '豪华间，空间更大', 'max_pets': 2},
        {'room_number': 'D002', 'room_type': 'deluxe', 'suitable_size': 'all', 
         'daily_price': 150, 'overtime_multiplier': 1.5, 
         'description': '豪华间-支持全体型', 'max_pets': 2},
        {'room_number': 'V001', 'room_type': 'vip', 'suitable_size': 'all', 
         'daily_price': 200, 'overtime_multiplier': 2.0, 
         'description': 'VIP套房，独立庭院，支持全体型', 'max_pets': 3},
    ]
    
    created_count = 0
    for data in room_data:
        if not Room.objects.filter(room_number=data['room_number']).exists():
            Room.objects.create(**data)
            created_count += 1
        else:
            room = Room.objects.get(room_number=data['room_number'])
            room.suitable_size = data['suitable_size']
            room.overtime_multiplier = data['overtime_multiplier']
            room.save()
    
    print(f"创建/更新了 {created_count} 个房间!")
    print(f"现有房间总数: {Room.objects.count()}")
    print("\n房间列表:")
    for room in Room.objects.all():
        print(f"  {room.room_number}: {room.get_room_type_display()} "
              f"[{room.get_suitable_size_display()}] - {room.daily_price}元/天 "
              f"(超时倍率: {room.overtime_multiplier})")


if __name__ == '__main__':
    init_rooms()
