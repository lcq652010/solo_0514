import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stadium_management.settings')
django.setup()

from django.contrib.auth.models import User
from stadium.models import VenueType, Venue


def init_data():
    print('开始初始化数据...')

    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print('创建管理员用户: admin / admin123')

    venue_types_data = [
        {'name': '羽毛球馆', 'sport_type': 'badminton'},
        {'name': '篮球馆', 'sport_type': 'basketball'},
        {'name': '乒乓球馆', 'sport_type': 'table_tennis'},
        {'name': '网球场', 'sport_type': 'tennis'},
        {'name': '游泳馆', 'sport_type': 'swimming'},
        {'name': '健身馆', 'sport_type': 'fitness'},
        {'name': '瑜伽馆', 'sport_type': 'yoga'},
    ]

    for vt_data in venue_types_data:
        VenueType.objects.get_or_create(
            name=vt_data['name'],
            defaults={'sport_type': vt_data['sport_type']}
        )
    print(f'创建 {len(venue_types_data)} 个场地类型')

    venue_type1 = VenueType.objects.get(name='羽毛球馆')
    venue_type2 = VenueType.objects.get(name='篮球馆')
    venue_type3 = VenueType.objects.get(name='健身馆')

    venues_data = [
        {'name': '羽毛球场1号', 'code': 'BM001', 'type': venue_type1, 'size': 'medium', 'price': 50, 'capacity': 4, 'area': 80, 'max_hours': 4},
        {'name': '羽毛球场2号', 'code': 'BM002', 'type': venue_type1, 'size': 'medium', 'price': 50, 'capacity': 4, 'area': 80, 'max_hours': 4},
        {'name': '羽毛球场3号', 'code': 'BM003', 'type': venue_type1, 'size': 'large', 'price': 60, 'capacity': 6, 'area': 120, 'max_hours': 6},
        {'name': '篮球场1号', 'code': 'BB001', 'type': venue_type2, 'size': 'large', 'price': 100, 'capacity': 10, 'area': 420, 'max_hours': 3},
        {'name': '篮球场2号', 'code': 'BB002', 'type': venue_type2, 'size': 'extra_large', 'price': 120, 'capacity': 12, 'area': 600, 'max_hours': 3},
        {'name': 'VIP健身区', 'code': 'GYM001', 'type': venue_type3, 'size': 'small', 'price': 80, 'capacity': 2, 'area': 40, 'max_hours': 2},
    ]

    for v_data in venues_data:
        Venue.objects.get_or_create(
            code=v_data['code'],
            defaults={
                'name': v_data['name'],
                'venue_type': v_data['type'],
                'size': v_data['size'],
                'price_per_hour': v_data['price'],
                'capacity': v_data['capacity'],
                'area': v_data['area'],
                'max_booking_hours_per_day': v_data['max_hours'],
                'status': 'available'
            }
        )
    print(f'创建 {len(venues_data)} 个场地')

    if not User.objects.filter(username='testuser').exists():
        User.objects.create_user('testuser', 'test@example.com', 'test123')
        print('创建测试用户: testuser / test123')

    print('数据初始化完成！')


if __name__ == '__main__':
    init_data()
