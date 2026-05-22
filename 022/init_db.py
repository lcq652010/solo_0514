import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course_platform.settings')
django.setup()

from django.contrib.auth.models import User
from courses.models import Course, Chapter, Video, UserProfile, Order, Enrollment


def init_demo_data():
    print("开始创建演示数据...")

    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            first_name='系统',
            last_name='管理员'
        )
        profile = UserProfile.objects.get(user=admin)
        profile.role = 'admin'
        profile.save()
        print(f"创建管理员用户: admin / admin123")
    else:
        admin = User.objects.get(username='admin')
        profile = UserProfile.objects.get(user=admin)
        if profile.role != 'admin':
            profile.role = 'admin'
            profile.save()
        print("管理员用户已存在")

    if not User.objects.filter(username='teacher').exists():
        teacher = User.objects.create_user(
            username='teacher',
            email='teacher@example.com',
            password='teacher123',
            first_name='张',
            last_name='老师'
        )
        profile = UserProfile.objects.get(user=teacher)
        profile.role = 'instructor'
        profile.bio = '资深全栈开发工程师，10年开发经验，精通Python、Java等多种编程语言。'
        profile.save()
        print(f"创建讲师用户: teacher / teacher123")
    else:
        teacher = User.objects.get(username='teacher')
        profile = UserProfile.objects.get(user=teacher)
        if profile.role != 'instructor':
            profile.role = 'instructor'
            profile.save()
        print("讲师用户已存在")

    if not User.objects.filter(username='student').exists():
        student = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='student123',
            first_name='李',
            last_name='学生'
        )
        profile = UserProfile.objects.get(user=student)
        profile.role = 'student'
        profile.save()
        print(f"创建学生用户: student / student123")
    else:
        student = User.objects.get(username='student')
        profile = UserProfile.objects.get(user=student)
        if profile.role != 'student':
            profile.role = 'student'
            profile.save()
        print("学生用户已存在")

    course_data = [
        {
            'title': 'Python 全栈开发实战',
            'description': '从零开始学习 Python，掌握 Django、Flask 等主流框架，成为全栈开发工程师。',
            'price': 299.00,
            'original_price': 599.00,
            'chapters': [
                {
                    'title': '第一章：Python 基础入门',
                    'videos': [
                        {'title': '1.1 Python 简介与环境搭建', 'duration': 1800},
                        {'title': '1.2 变量与数据类型', 'duration': 2400},
                        {'title': '1.3 流程控制语句', 'duration': 2100},
                    ]
                },
                {
                    'title': '第二章：函数与模块',
                    'videos': [
                        {'title': '2.1 函数定义与调用', 'duration': 1900},
                        {'title': '2.2 模块与包管理', 'duration': 2200},
                    ]
                }
            ]
        },
        {
            'title': 'Django 项目实战教程',
            'description': '深入学习 Django 框架，从 MTV 模式到 RESTful API 开发，完整项目实战。',
            'price': 399.00,
            'original_price': 799.00,
            'chapters': [
                {
                    'title': '第一章：Django 入门',
                    'videos': [
                        {'title': '1.1 Django 介绍与安装', 'duration': 1500},
                        {'title': '1.2 创建第一个 Django 项目', 'duration': 2000},
                    ]
                }
            ]
        }
    ]

    for course_info in course_data:
        if not Course.objects.filter(title=course_info['title']).exists():
            course = Course.objects.create(
                title=course_info['title'],
                description=course_info['description'],
                price=course_info['price'],
                original_price=course_info['original_price'],
                instructor=teacher,
                status='published'
            )
            print(f"创建课程: {course.title}")

            for chapter_info in course_info['chapters']:
                chapter = Chapter.objects.create(
                    course=course,
                    title=chapter_info['title'],
                    order=list(course_info['chapters']).index(chapter_info) + 1
                )
                print(f"  创建章节: {chapter.title}")

                for video_info in chapter_info['videos']:
                    video = Video.objects.create(
                        chapter=chapter,
                        title=video_info['title'],
                        duration=video_info['duration'],
                        video_url=f'https://example.com/videos/{course.id}/{chapter.id}/{video_info["title"]}.mp4',
                        order=list(chapter_info['videos']).index(video_info) + 1
                    )
                    print(f"    创建视频: {video.title}")
        else:
            print(f"课程已存在: {course_info['title']}")

    print("\n演示数据创建完成！")
    print("\n测试账号汇总:")
    print("  管理员: admin / admin123 (后台: http://127.0.0.1:8000/admin/)")
    print("  讲师: teacher / teacher123")
    print("  学生: student / student123")


if __name__ == '__main__':
    init_demo_data()
