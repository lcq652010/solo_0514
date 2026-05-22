from rest_framework import serializers
from django.db.models import Q
from .models import Book, Reader, Borrow
from datetime import datetime, date
import re


class BookSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['create_time', 'update_time']
    
    def validate_isbn(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('ISBN不能为空')
        if len(value) < 10 or len(value) > 20:
            raise serializers.ValidationError('ISBN长度应在10-20个字符之间')
        return value.strip()
    
    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('书名不能为空')
        if len(value.strip()) < 1:
            raise serializers.ValidationError('书名长度不能少于1个字符')
        if len(value) > 200:
            raise serializers.ValidationError('书名长度不能超过200个字符')
        return value.strip()
    
    def validate_author(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('作者不能为空')
        if len(value.strip()) < 1:
            raise serializers.ValidationError('作者名称不能少于1个字符')
        return value.strip()
    
    def validate_publisher(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('出版社不能为空')
        return value.strip()
    
    def validate_publish_date(self, value):
        if not value:
            raise serializers.ValidationError('出版日期不能为空')
        if value > date.today():
            raise serializers.ValidationError('出版日期不能晚于当前日期')
        return value
    
    def validate_category(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('分类不能为空')
        return value.strip()
    
    def validate_location(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('馆藏位置不能为空')
        return value.strip()
    
    def validate_total_copies(self, value):
        if value is None:
            raise serializers.ValidationError('总册数不能为空')
        if value < 1:
            raise serializers.ValidationError('总册数不能少于1')
        if value > 10000:
            raise serializers.ValidationError('总册数不能超过10000')
        return value
    
    def validate_available_copies(self, value):
        if value is None:
            raise serializers.ValidationError('可借册数不能为空')
        if value < 0:
            raise serializers.ValidationError('可借册数不能为负数')
        return value
    
    def validate(self, data):
        if 'total_copies' in data and 'available_copies' in data:
            if data['available_copies'] > data['total_copies']:
                raise serializers.ValidationError({'available_copies': '可借册数不能大于总册数'})
        return data


class ReaderSerializer(serializers.ModelSerializer):
    reader_type_display = serializers.CharField(source='get_reader_type_display', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    
    class Meta:
        model = Reader
        fields = '__all__'
        read_only_fields = ['reader_no', 'register_date', 'create_time', 'update_time']
    
    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('姓名不能为空')
        if len(value.strip()) < 2:
            raise serializers.ValidationError('姓名长度不能少于2个字符')
        if len(value) > 50:
            raise serializers.ValidationError('姓名长度不能超过50个字符')
        return value.strip()
    
    def validate_gender(self, value):
        if not value:
            raise serializers.ValidationError('性别不能为空')
        if value not in ['male', 'female']:
            raise serializers.ValidationError('性别值不合法')
        return value
    
    def validate_phone(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('联系电话不能为空')
        phone_pattern = r'^1[3-9]\d{9}$'
        if not re.match(phone_pattern, value.strip()):
            raise serializers.ValidationError('手机号码格式不正确')
        return value.strip()
    
    def validate_email(self, value):
        if value:
            if len(value) > 100:
                raise serializers.ValidationError('邮箱长度不能超过100个字符')
        return value
    
    def validate_id_card(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('身份证号不能为空')
        value = value.strip()
        if len(value) != 18:
            raise serializers.ValidationError('身份证号必须为18位')
        id_card_pattern = r'^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$'
        if not re.match(id_card_pattern, value):
            raise serializers.ValidationError('身份证号格式不正确')
        return value
    
    def validate_reader_type(self, value):
        if not value:
            raise serializers.ValidationError('读者类型不能为空')
        if value not in ['student', 'teacher', 'staff', 'other']:
            raise serializers.ValidationError('读者类型值不合法')
        return value
    
    def validate_max_borrow_days(self, value):
        if value is None:
            raise serializers.ValidationError('最大借阅天数不能为空')
        if value < 1:
            raise serializers.ValidationError('最大借阅天数不能少于1天')
        if value > 365:
            raise serializers.ValidationError('最大借阅天数不能超过365天')
        return value
    
    def validate_max_borrow_books(self, value):
        if value is None:
            raise serializers.ValidationError('最大借阅册数不能为空')
        if value < 1:
            raise serializers.ValidationError('最大借阅册数不能少于1本')
        if value > 100:
            raise serializers.ValidationError('最大借阅册数不能超过100本')
        return value
    
    def validate_expire_date(self, value):
        if not value:
            raise serializers.ValidationError('有效期至不能为空')
        if value < date.today():
            raise serializers.ValidationError('有效期不能早于当前日期')
        return value


class BorrowSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_isbn = serializers.CharField(source='book.isbn', read_only=True)
    reader_name = serializers.CharField(source='reader.name', read_only=True)
    reader_no = serializers.CharField(source='reader.reader_no', read_only=True)
    overdue_days = serializers.SerializerMethodField()
    current_fine = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()
    
    class Meta:
        model = Borrow
        fields = '__all__'
        read_only_fields = ['borrow_no', 'borrow_date', 'create_time', 'update_time']
    
    def get_overdue_days(self, obj):
        return obj.get_overdue_days()
    
    def get_current_fine(self, obj):
        obj.calculate_overdue_fine(auto_save=False)
        return obj.fine_amount
    
    def get_is_overdue(self, obj):
        return obj.is_overdue()


class BorrowCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = ['book', 'reader', 'operator', 'remarks']
    
    def validate_book(self, value):
        if not value:
            raise serializers.ValidationError('图书不能为空')
        return value
    
    def validate_reader(self, value):
        if not value:
            raise serializers.ValidationError('读者不能为空')
        return value
    
    def validate_operator(self, value):
        if value and len(value) > 50:
            raise serializers.ValidationError('操作员名称长度不能超过50个字符')
        return value
    
    def validate_remarks(self, value):
        if value and len(value) > 500:
            raise serializers.ValidationError('备注长度不能超过500个字符')
        return value
    
    def validate(self, data):
        book = data['book']
        reader = data['reader']
        
        if book.available_copies <= 0:
            raise serializers.ValidationError({'book': '该书已无库存可借'})
        
        if book.status == 'lost':
            raise serializers.ValidationError({'book': '该图书已遗失，无法借阅'})
        
        if not reader.is_active:
            raise serializers.ValidationError({'reader': '该读者证已失效，无法借阅'})
        
        if reader.expire_date < date.today():
            raise serializers.ValidationError({'reader': '该读者证已过期，请续期后再借阅'})
        
        current_borrow_count = Borrow.objects.filter(reader=reader, status='borrowed').count()
        if current_borrow_count >= reader.max_borrow_books:
            raise serializers.ValidationError({
                'reader': f'该读者已达到最大借阅数量 {reader.max_borrow_books} 本，当前已借阅 {current_borrow_count} 本'
            })
        
        already_borrowed = Borrow.objects.filter(book=book, reader=reader, status='borrowed').exists()
        if already_borrowed:
            raise serializers.ValidationError({'book': '该读者已借阅此书，尚未归还，不能重复借阅'})
        
        overdue_count = Borrow.objects.filter(
            reader=reader,
            status='borrowed',
            due_date__lt=datetime.now()
        ).count()
        if overdue_count > 0:
            raise serializers.ValidationError({
                'reader': f'该读者有 {overdue_count} 本图书逾期未还，请先归还逾期图书'
            })
        
        return data


class ReturnBookSerializer(serializers.Serializer):
    operator = serializers.CharField(required=False, allow_blank=True)
    remarks = serializers.CharField(required=False, allow_blank=True)


class ReportLostSerializer(serializers.Serializer):
    operator = serializers.CharField(required=False, allow_blank=True)
    remarks = serializers.CharField(required=False, allow_blank=True)
