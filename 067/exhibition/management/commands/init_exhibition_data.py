from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from exhibition.models import Exhibition, Booth, Company, Builder, ProgressStepTemplate


class Command(BaseCommand):
    help = '初始化展会演示数据'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化展会数据...')

        exhibition, created = Exhibition.objects.get_or_create(
            name='2024中国国际科技博览会',
            defaults={
                'start_date': timezone.now().date() + timedelta(days=30),
                'end_date': timezone.now().date() + timedelta(days=33),
                'location': '上海国际会展中心',
                'description': '年度最大的科技展览会，汇集国内外知名科技企业'
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'创建展会: {exhibition.name}'))

            builders_data = [
                {
                    'name': '标准展位搭建有限公司',
                    'contact_person': '张工',
                    'phone': '13800138011',
                    'email': 'zhang@standard.com',
                    'specialty': 'standard',
                    'company_level': 1,
                },
                {
                    'name': '豪华展位设计公司',
                    'contact_person': '李工',
                    'phone': '13800138012',
                    'email': 'li@premium.com',
                    'specialty': 'premium',
                    'company_level': 1,
                },
                {
                    'name': '特装搭建专家',
                    'contact_person': '王工',
                    'phone': '13800138013',
                    'email': 'wang@custom.com',
                    'specialty': 'custom',
                    'company_level': 1,
                },
                {
                    'name': '木结构特装公司',
                    'contact_person': '赵工',
                    'phone': '13800138014',
                    'email': 'zhao@wood.com',
                    'specialty': 'wood',
                    'company_level': 2,
                },
                {
                    'name': '桁架搭建服务商',
                    'contact_person': '刘工',
                    'phone': '13800138015',
                    'email': 'liu@truss.com',
                    'specialty': 'truss',
                    'company_level': 2,
                },
            ]

            for builder_data in builders_data:
                Builder.objects.create(**builder_data)
            self.stdout.write(self.style.SUCCESS('创建 5 个搭建商数据'))

            standard_steps = [
                {'step_order': 1, 'step_name': '展位设计方案提交', 'progress_percent': 10},
                {'step_order': 2, 'step_name': '材料采购准备', 'progress_percent': 20},
                {'step_order': 3, 'step_name': '主体结构搭建', 'progress_percent': 30},
                {'step_order': 4, 'step_name': '展具安装摆放', 'progress_percent': 20},
                {'step_order': 5, 'step_name': '灯光音响调试', 'progress_percent': 10},
                {'step_order': 6, 'step_name': '清洁收尾验收', 'progress_percent': 10},
            ]

            premium_steps = [
                {'step_order': 1, 'step_name': '特装设计方案确认', 'progress_percent': 10},
                {'step_order': 2, 'step_name': '定制化材料定制采购', 'progress_percent': 15},
                {'step_order': 3, 'step_name': '主体钢结构搭建', 'progress_percent': 20},
                {'step_order': 4, 'step_name': '装饰装修施工', 'progress_percent': 20},
                {'step_order': 5, 'step_name': '多媒体设备安装调试', 'progress_percent': 15},
                {'step_order': 6, 'step_name': '灯光音响及效果调试', 'progress_percent': 10},
                {'step_order': 7, 'step_name': '整体清洁验收交付', 'progress_percent': 10},
            ]

            custom_steps = [
                {'step_order': 1, 'step_name': '特装设计3D效果图确认', 'progress_percent': 10},
                {'step_order': 2, 'step_name': '特殊材料定制采购', 'progress_percent': 15},
                {'step_order': 3, 'step_name': '主体结构搭建施工', 'progress_percent': 20},
                {'step_order': 4, 'step_name': '精装装修施工', 'progress_percent': 20},
                {'step_order': 5, 'step_name': '特殊设备定制安装', 'progress_percent': 15},
                {'step_order': 6, 'step_name': '灯光音响视频系统集成', 'progress_percent': 10},
                {'step_order': 7, 'step_name': '整体效果调试优化', 'progress_percent': 5},
                {'step_order': 8, 'step_name': '验收交付使用', 'progress_percent': 5},
            ]

            for step in standard_steps:
                ProgressStepTemplate.objects.create(step_type='standard', **step)
            self.stdout.write(self.style.SUCCESS('创建标准流程进度步骤模板'))

            for step in premium_steps:
                ProgressStepTemplate.objects.create(step_type='premium', **step)
            self.stdout.write(self.style.SUCCESS('创建豪华流程进度步骤模板'))

            for step in custom_steps:
                ProgressStepTemplate.objects.create(step_type='custom', **step)
            self.stdout.write(self.style.SUCCESS('创建特装流程进度步骤模板'))

            zones = ['A', 'B', 'C']
            booth_types = ['standard', 'premium', 'corner', 'custom']
            booth_prices = {
                'standard': 8000,
                'premium': 15000,
                'corner': 12000,
                'custom': 25000
            }
            booth_areas = {
                'standard': 9,
                'premium': 18,
                'corner': 12,
                'custom': 36
            }

            booth_counter = 1
            for zone in zones:
                for i in range(1, 11):
                    booth_type = booth_types[booth_counter % 4]
                    Booth.objects.create(
                        exhibition=exhibition,
                        booth_number=f'{zone}{i:02d}',
                        zone=zone,
                        booth_type=booth_type,
                        area=booth_areas[booth_type],
                        price=booth_prices[booth_type],
                        location_desc=f'{zone}区第 {i} 号展位',
                        status='available'
                    )
                    booth_counter += 1

            self.stdout.write(self.style.SUCCESS('创建 30 个展位数据 (A/B/C 三个区域)'))

            companies = [
                {
                    'name': '科技创新有限公司',
                    'contact_person': '张三',
                    'phone': '13800138001',
                    'email': 'zhangsan@tech.com',
                    'address': '北京市海淀区中关村大街1号',
                    'industry': '电子科技'
                },
                {
                    'name': '未来科技集团',
                    'contact_person': '李四',
                    'phone': '13800138002',
                    'email': 'lisi@futuretech.com',
                    'address': '上海市浦东新区张江高科技园区',
                    'industry': '人工智能'
                },
                {
                    'name': '绿色能源股份有限公司',
                    'contact_person': '王五',
                    'phone': '13800138003',
                    'email': 'wangwu@greenenergy.com',
                    'address': '杭州市西湖区文三路',
                    'industry': '新能源'
                },
            ]

            for company_data in companies:
                Company.objects.create(**company_data)

            self.stdout.write(self.style.SUCCESS('创建 3 个企业数据'))

        else:
            self.stdout.write(self.style.WARNING('展会数据已存在'))

        self.stdout.write(self.style.SUCCESS('数据初始化完成！'))
