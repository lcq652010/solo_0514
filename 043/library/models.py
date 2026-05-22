from django.db import models
from datetime import datetime, timedelta
import uuid


class Book(models.Model):
    BOOK_STATUS_CHOICES = [
        ('available', '可借'),
        ('borrowed', '已借出'),
        ('lost', '已遗失'),
    ]
    
    isbn = models.CharField(max_length=20, unique=True, verbose_name='ISBN')
    title = models.CharField(max_length=200, verbose_name='书名')
    author = models.CharField(max_length=100, verbose_name='作者')
    publisher = models.CharField(max_length=100, verbose_name='出版社')
    publish_date = models.DateField(verbose_name='出版日期')
    category = models.CharField(max_length=50, verbose_name='分类')
    location = models.CharField(max_length=50, verbose_name='馆藏位置')
    total_copies = models.IntegerField(default=1, verbose_name='总册数')
    available_copies = models.IntegerField(default=1, verbose_name='可借册数')
    status = models.CharField(max_length=20, choices=BOOK_STATUS_CHOICES, default='available', verbose_name='状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='录入时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'book'
        verbose_name = '图书'
        verbose_name_plural = '图书'
    
    def __str__(self):
        return f'{self.title} - {self.isbn}'
    
    def delete(self, *args, **kwargs):
        borrow_count = Borrow.objects.filter(book=self, status='borrowed').count()
        if borrow_count > 0:
            raise ValueError(f'该书有 {borrow_count} 本正在借阅中，无法删除')
        super().delete(*args, **kwargs)


class Reader(models.Model):
    READER_TYPE_CHOICES = [
        ('student', '学生'),
        ('teacher', '教师'),
        ('staff', '教职工'),
        ('other', '其他'),
    ]
    
    reader_no = models.CharField(max_length=20, unique=True, verbose_name='读者证号')
    name = models.CharField(max_length=50, verbose_name='姓名')
    gender = models.CharField(max_length=10, choices=[('male', '男'), ('female', '女')], verbose_name='性别')
    phone = models.CharField(max_length=20, verbose_name='联系电话')
    email = models.EmailField(blank=True, null=True, verbose_name='邮箱')
    id_card = models.CharField(max_length=18, unique=True, verbose_name='身份证号')
    reader_type = models.CharField(max_length=20, choices=READER_TYPE_CHOICES, default='student', verbose_name='读者类型')
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name='院系/部门')
    max_borrow_days = models.IntegerField(default=30, verbose_name='最大借阅天数')
    max_borrow_books = models.IntegerField(default=10, verbose_name='最大借阅册数')
    register_date = models.DateField(auto_now_add=True, verbose_name='办证日期')
    expire_date = models.DateField(verbose_name='有效期至')
    is_active = models.BooleanField(default=True, verbose_name='是否有效')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'reader'
        verbose_name = '读者'
        verbose_name_plural = '读者'
    
    def __str__(self):
        return f'{self.name} - {self.reader_no}'
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.reader_no:
            prefix = 'R'
            today = datetime.now().strftime('%Y%m%d')
            last_reader = Reader.objects.filter(reader_no__startswith=prefix + today).order_by('-reader_no').first()
            if last_reader:
                last_num = int(last_reader.reader_no[-4:])
                new_num = str(last_num + 1).zfill(4)
            else:
                new_num = '0001'
            self.reader_no = prefix + today + new_num
        
        if not self.expire_date:
            self.expire_date = datetime.now().date() + timedelta(days=365)
        
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        borrow_count = Borrow.objects.filter(reader=self, status='borrowed').count()
        if borrow_count > 0:
            raise ValueError(f'该读者有 {borrow_count} 本图书正在借阅中，无法删除')
        super().delete(*args, **kwargs)


class Borrow(models.Model):
    BORROW_STATUS_CHOICES = [
        ('borrowed', '已借出'),
        ('returned', '已归还'),
        ('lost', '已遗失'),
    ]
    
    borrow_no = models.CharField(max_length=30, unique=True, verbose_name='借阅单号')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='图书')
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, verbose_name='读者')
    borrow_date = models.DateTimeField(auto_now_add=True, verbose_name='借阅日期')
    due_date = models.DateTimeField(verbose_name='应还日期')
    return_date = models.DateTimeField(blank=True, null=True, verbose_name='实际归还日期')
    status = models.CharField(max_length=20, choices=BORROW_STATUS_CHOICES, default='borrowed', verbose_name='借阅状态')
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='罚款金额')
    fine_paid = models.BooleanField(default=False, verbose_name='罚款已缴纳')
    operator = models.CharField(max_length=50, blank=True, null=True, verbose_name='操作员')
    remarks = models.TextField(blank=True, null=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'borrow'
        verbose_name = '借阅记录'
        verbose_name_plural = '借阅记录'
    
    def __str__(self):
        return f'{self.borrow_no} - {self.book.title} - {self.reader.name}'
    
    def save(self, *args, **kwargs):
        if not self.borrow_no:
            prefix = 'B'
            today = datetime.now().strftime('%Y%m%d%H%M%S')
            unique_id = str(uuid.uuid4().int)[:6]
            self.borrow_no = prefix + today + unique_id
        
        if not self.due_date:
            self.due_date = datetime.now() + timedelta(days=self.reader.max_borrow_days)
        
        super().save(*args, **kwargs)
    
    def calculate_overdue_fine(self, fine_per_day=0.5, auto_save=False):
        """
        计算逾期罚款
        :param fine_per_day: 每日罚款金额，默认0.5元/天
        :param auto_save: 是否自动保存到数据库
        :return: 罚款金额
        """
        fine_changed = False
        
        if self.status == 'returned' and self.return_date:
            if self.return_date > self.due_date:
                overdue_days = (self.return_date - self.due_date).days
                new_fine = overdue_days * fine_per_day
                if self.fine_amount != new_fine:
                    self.fine_amount = new_fine
                    fine_changed = True
            else:
                if self.fine_amount != 0.00:
                    self.fine_amount = 0.00
                    fine_changed = True
        elif self.status == 'borrowed':
            now = datetime.now()
            if now > self.due_date:
                overdue_days = (now - self.due_date).days
                new_fine = overdue_days * fine_per_day
                if self.fine_amount != new_fine:
                    self.fine_amount = new_fine
                    fine_changed = True
            else:
                if self.fine_amount != 0.00:
                    self.fine_amount = 0.00
                    fine_changed = True
        
        if auto_save and fine_changed:
            self.save(update_fields=['fine_amount', 'update_time'])
        
        return self.fine_amount
    
    def get_overdue_days(self):
        """
        获取逾期天数
        :return: 逾期天数，未逾期返回0
        """
        if self.status == 'returned' and self.return_date:
            if self.return_date > self.due_date:
                return (self.return_date - self.due_date).days
        elif self.status == 'borrowed':
            now = datetime.now()
            if now > self.due_date:
                return (now - self.due_date).days
        return 0
    
    def is_overdue(self):
        """
        判断是否逾期
        :return: 是否逾期
        """
        if self.status != 'borrowed':
            return False
        return datetime.now() > self.due_date
    
    @classmethod
    def calculate_all_overdue_fines(cls, fine_per_day=0.5):
        """
        批量计算所有借阅中图书的逾期罚款
        :param fine_per_day: 每日罚款金额
        :return: 更新的记录数
        """
        borrows = cls.objects.filter(status='borrowed')
        updated_count = 0
        for borrow in borrows:
            borrow.calculate_overdue_fine(fine_per_day=fine_per_day, auto_save=True)
            updated_count += 1
        return updated_count
    
    def return_book(self, operator=None, remarks=None, fine_per_day=0.5):
        """
        归还图书，自动更新借阅状态和图书状态
        :param operator: 操作员
        :param remarks: 备注
        :param fine_per_day: 每日罚款金额
        :return: 是否成功
        """
        if self.status != 'borrowed':
            raise ValueError('该借阅记录不是借出状态，无法归还')
        
        self.return_date = datetime.now()
        self.status = 'returned'
        if operator:
            self.operator = operator
        if remarks:
            self.remarks = remarks
        
        self.calculate_overdue_fine(fine_per_day=fine_per_day)
        self.save()
        
        book = self.book
        book.available_copies += 1
        
        if book.available_copies > 0:
            if book.total_copies > 1:
                if book.status != 'available':
                    book.status = 'available'
            else:
                if book.status == 'borrowed':
                    book.status = 'available'
        
        book.save()
        
        return True
    
    def report_lost_book(self, operator=None, remarks=None):
        """
        图书报失，自动更新借阅状态和图书状态
        :param operator: 操作员
        :param remarks: 备注
        :return: 是否成功
        """
        if self.status != 'borrowed':
            raise ValueError('该借阅记录不是借出状态，无法报失')
        
        self.status = 'lost'
        if operator:
            self.operator = operator
        if remarks:
            self.remarks = remarks
        self.save()
        
        book = self.book
        book.total_copies -= 1
        book.available_copies = max(0, book.available_copies - 1)
        
        if book.total_copies <= 0:
            book.status = 'lost'
        elif book.available_copies == 0 and book.total_copies > 0:
            book.status = 'borrowed'
        elif book.available_copies > 0:
            book.status = 'available'
        
        book.save()
        
        return True
