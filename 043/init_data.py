#!/usr/bin/env python
"""
图书馆管理系统 - 初始化数据脚本
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_management.settings')
django.setup()

from library.models import Book, Reader, Borrow
from datetime import date, timedelta

def init_books():
    """初始化图书数据"""
    books_data = [
        {
            'isbn': '9787111544937',
            'title': 'Python编程：从入门到实践',
            'author': '埃里克·马瑟斯',
            'publisher': '机械工业出版社',
            'publish_date': '2016-07-01',
            'category': '计算机',
            'location': 'A区-1架-3层',
            'total_copies': 5,
            'available_copies': 5,
        },
        {
            'isbn': '9787115428028',
            'title': '深度学习',
            'author': 'Ian Goodfellow',
            'publisher': '人民邮电出版社',
            'publish_date': '2017-08-01',
            'category': '计算机',
            'location': 'A区-2架-1层',
            'total_copies': 3,
            'available_copies': 3,
        },
        {
            'isbn': '9787560036847',
            'title': '围城',
            'author': '钱钟书',
            'publisher': '人民文学出版社',
            'publish_date': '1991-02-01',
            'category': '文学',
            'location': 'B区-1架-2层',
            'total_copies': 2,
            'available_copies': 2,
        },
        {
            'isbn': '9787020002207',
            'title': '红楼梦',
            'author': '曹雪芹',
            'publisher': '人民文学出版社',
            'publish_date': '2008-07-01',
            'category': '文学',
            'location': 'B区-3架-1层',
            'total_copies': 4,
            'available_copies': 4,
        },
    ]
    
    count = 0
    for book_data in books_data:
        if not Book.objects.filter(isbn=book_data['isbn']).exists():
            Book.objects.create(**book_data)
            count += 1
            print(f'✓ 新增图书: {book_data["title"]}')
    print(f'图书初始化完成，共新增 {count} 本图书\n')

def init_readers():
    """初始化读者数据"""
    readers_data = [
        {
            'name': '张三',
            'gender': 'male',
            'phone': '13800138001',
            'email': 'zhangsan@example.com',
            'id_card': '110101199001011001',
            'reader_type': 'student',
            'department': '计算机科学与技术学院',
            'max_borrow_days': 30,
            'max_borrow_books': 10,
            'is_active': True,
        },
        {
            'name': '李四',
            'gender': 'female',
            'phone': '13800138002',
            'email': 'lisi@example.com',
            'id_card': '110101199102021002',
            'reader_type': 'student',
            'department': '外国语学院',
            'max_borrow_days': 30,
            'max_borrow_books': 10,
            'is_active': True,
        },
        {
            'name': '王老师',
            'gender': 'male',
            'phone': '13900139001',
            'email': 'wang@example.com',
            'id_card': '110101198003032001',
            'reader_type': 'teacher',
            'department': '计算机科学与技术学院',
            'max_borrow_days': 60,
            'max_borrow_books': 20,
            'is_active': True,
        },
    ]
    
    count = 0
    for reader_data in readers_data:
        if not Reader.objects.filter(id_card=reader_data['id_card']).exists():
            Reader.objects.create(**reader_data)
            count += 1
            print(f'✓ 新增读者: {reader_data["name"]}')
    print(f'读者初始化完成，共新增 {count} 位读者\n')

def main():
    print('=' * 50)
    print('    图书馆管理系统 - 数据初始化')
    print('=' * 50)
    print()
    
    init_books()
    init_readers()
    
    print('=' * 50)
    print('    数据初始化完成！')
    print('=' * 50)
    print()
    print('提示: 请运行以下命令创建管理员账号:')
    print('  python manage.py createsuperuser')

if __name__ == '__main__':
    main()
