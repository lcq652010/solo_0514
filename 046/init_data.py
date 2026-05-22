import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'housekeeping.settings')
django.setup()

from api.models import Service, Aunt, Order, Review
from django.utils import timezone


def init_services():
    services_data = [
        {'name': '日常保洁', 'description': '家庭日常清洁服务，包括地面清扫、家具擦拭、厨房卫生间清洁等', 'price': 150.00, 'duration': 3},
        {'name': '深度保洁', 'description': '全方位深度清洁，包括擦玻璃、油烟机清洗、家具深度除尘等', 'price': 300.00, 'duration': 4},
        {'name': '月嫂服务', 'description': '专业母婴护理，新生儿护理、产妇月子照顾', 'price': 8000.00, 'duration': 24},
        {'name': '育儿嫂', 'description': '婴幼儿专业看护，辅食添加、早期教育', 'price': 6000.00, 'duration': 24},
        {'name': '老人陪护', 'description': '专业老人陪护服务，生活照料、陪伴聊天', 'price': 4000.00, 'duration': 24},
        {'name': '钟点工', 'description': '按小时计费的家政服务', 'price': 50.00, 'duration': 1},
    ]
    for data in services_data:
        Service.objects.get_or_create(name=data['name'], defaults=data)
    print('服务项目初始化完成')


def init_aunts():
    service1 = Service.objects.get(name='日常保洁')
    service2 = Service.objects.get(name='深度保洁')
    service3 = Service.objects.get(name='钟点工')

    aunts_data = [
        {
            'name': '张阿姨',
            'gender': 'female',
            'age': 45,
            'phone': '13800138001',
            'id_card': '110101197801010001',
            'experience': 8,
            'skills': [service1, service2, service3],
            'address': '北京市朝阳区'
        },
        {
            'name': '李阿姨',
            'gender': 'female',
            'age': 42,
            'phone': '13800138002',
            'id_card': '110101198102020002',
            'experience': 6,
            'skills': [service1, service3],
            'address': '北京市海淀区'
        },
        {
            'name': '王阿姨',
            'gender': 'female',
            'age': 50,
            'phone': '13800138003',
            'id_card': '110101197403030003',
            'experience': 12,
            'skills': [service1, service2],
            'address': '北京市丰台区'
        },
    ]
    for data in aunts_data:
        skills = data.pop('skills')
        aunt, created = Aunt.objects.get_or_create(id_card=data['id_card'], defaults=data)
        if created:
            aunt.skills.set(skills)
    print('阿姨信息初始化完成')


if __name__ == '__main__':
    init_services()
    init_aunts()
    print('数据初始化完成！')
