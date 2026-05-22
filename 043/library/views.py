from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db import transaction, models
from datetime import datetime
from .models import Book, Reader, Borrow
from .serializers import (
    BookSerializer,
    ReaderSerializer,
    BorrowSerializer,
    BorrowCreateSerializer,
    ReturnBookSerializer,
    ReportLostSerializer,
)


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-create_time')
    serializer_class = BookSerializer
    pagination_class = StandardPagination
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        title = self.request.query_params.get('title')
        if title:
            queryset = queryset.filter(title__icontains=title.strip())
        
        isbn = self.request.query_params.get('isbn')
        if isbn:
            queryset = queryset.filter(isbn__icontains=isbn.strip())
        
        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author__icontains=author.strip())
        
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__icontains=category.strip())
        
        min_copies = self.request.query_params.get('min_copies')
        if min_copies and min_copies.isdigit():
            queryset = queryset.filter(total_copies__gte=int(min_copies))
        
        max_copies = self.request.query_params.get('max_copies')
        if max_copies and max_copies.isdigit():
            queryset = queryset.filter(total_copies__lte=int(max_copies))
        
        start_date = self.request.query_params.get('start_date')
        if start_date:
            try:
                queryset = queryset.filter(create_time__date__gte=start_date)
            except (ValueError, TypeError):
                pass
        
        end_date = self.request.query_params.get('end_date')
        if end_date:
            try:
                queryset = queryset.filter(create_time__date__lte=end_date)
            except (ValueError, TypeError):
                pass
        
        return queryset
    
    def perform_destroy(self, instance):
        borrow_count = Borrow.objects.filter(book=instance, status='borrowed').count()
        if borrow_count > 0:
            raise serializers.ValidationError({'error': f'该书有 {borrow_count} 本正在借阅中，无法删除'})
        instance.delete()
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        total = Book.objects.count()
        available = Book.objects.filter(status='available').count()
        borrowed = Book.objects.filter(status='borrowed').count()
        lost = Book.objects.filter(status='lost').count()
        return Response({
            'total': total,
            'available': available,
            'borrowed': borrowed,
            'lost': lost,
        })


class ReaderViewSet(viewsets.ModelViewSet):
    queryset = Reader.objects.all().order_by('-create_time')
    serializer_class = ReaderSerializer
    pagination_class = StandardPagination
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name.strip())
        
        reader_no = self.request.query_params.get('reader_no')
        if reader_no:
            queryset = queryset.filter(reader_no__icontains=reader_no.strip())
        
        phone = self.request.query_params.get('phone')
        if phone:
            queryset = queryset.filter(phone__icontains=phone.strip())
        
        id_card = self.request.query_params.get('id_card')
        if id_card:
            queryset = queryset.filter(id_card__icontains=id_card.strip())
        
        reader_type = self.request.query_params.get('reader_type')
        if reader_type:
            queryset = queryset.filter(reader_type=reader_type)
        
        is_active = self.request.query_params.get('is_active')
        if is_active is not None and is_active != '':
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        department = self.request.query_params.get('department')
        if department:
            queryset = queryset.filter(department__icontains=department.strip())
        
        min_borrow_books = self.request.query_params.get('min_borrow_books')
        if min_borrow_books and min_borrow_books.isdigit():
            queryset = queryset.filter(max_borrow_books__gte=int(min_borrow_books))
        
        max_borrow_books = self.request.query_params.get('max_borrow_books')
        if max_borrow_books and max_borrow_books.isdigit():
            queryset = queryset.filter(max_borrow_books__lte=int(max_borrow_books))
        
        start_date = self.request.query_params.get('start_date')
        if start_date:
            try:
                queryset = queryset.filter(create_time__date__gte=start_date)
            except (ValueError, TypeError):
                pass
        
        end_date = self.request.query_params.get('end_date')
        if end_date:
            try:
                queryset = queryset.filter(create_time__date__lte=end_date)
            except (ValueError, TypeError):
                pass
        
        return queryset
    
    def perform_destroy(self, instance):
        borrow_count = Borrow.objects.filter(reader=instance, status='borrowed').count()
        if borrow_count > 0:
            raise serializers.ValidationError({'error': f'该读者有 {borrow_count} 本图书正在借阅中，无法删除'})
        instance.delete()
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        total = Reader.objects.count()
        active = Reader.objects.filter(is_active=True).count()
        inactive = Reader.objects.filter(is_active=False).count()
        return Response({
            'total': total,
            'active': active,
            'inactive': inactive,
        })
    
    @action(detail=True, methods=['get'])
    def borrow_history(self, request, pk=None):
        reader = self.get_object()
        borrows = Borrow.objects.filter(reader=reader).order_by('-borrow_date')
        
        borrow_status = request.query_params.get('status')
        if borrow_status:
            borrows = borrows.filter(status=borrow_status)
        
        is_overdue = request.query_params.get('is_overdue')
        if is_overdue is not None and is_overdue != '':
            if is_overdue.lower() == 'true':
                borrows = borrows.filter(status='borrowed', due_date__lt=datetime.now())
        
        page = self.paginate_queryset(borrows)
        if page is not None:
            serializer = BorrowSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = BorrowSerializer(borrows, many=True)
        return Response(serializer.data)


class BorrowViewSet(viewsets.ModelViewSet):
    queryset = Borrow.objects.all().order_by('-borrow_date')
    serializer_class = BorrowSerializer
    pagination_class = StandardPagination
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        book_title = self.request.query_params.get('book_title')
        if book_title:
            queryset = queryset.filter(book__title__icontains=book_title.strip())
        
        book_isbn = self.request.query_params.get('book_isbn')
        if book_isbn:
            queryset = queryset.filter(book__isbn__icontains=book_isbn.strip())
        
        reader_name = self.request.query_params.get('reader_name')
        if reader_name:
            queryset = queryset.filter(reader__name__icontains=reader_name.strip())
        
        reader_no = self.request.query_params.get('reader_no')
        if reader_no:
            queryset = queryset.filter(reader__reader_no__icontains=reader_no.strip())
        
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        borrow_no = self.request.query_params.get('borrow_no')
        if borrow_no:
            queryset = queryset.filter(borrow_no__icontains=borrow_no.strip())
        
        operator = self.request.query_params.get('operator')
        if operator:
            queryset = queryset.filter(operator__icontains=operator.strip())
        
        is_overdue = self.request.query_params.get('is_overdue')
        if is_overdue is not None and is_overdue != '':
            if is_overdue.lower() == 'true':
                queryset = queryset.filter(status='borrowed', due_date__lt=datetime.now())
            elif is_overdue.lower() == 'false':
                queryset = queryset.filter(
                    models.Q(status='returned') | 
                    models.Q(status='lost') | 
                    (models.Q(status='borrowed') & models.Q(due_date__gte=datetime.now()))
                )
        
        min_fine = self.request.query_params.get('min_fine')
        if min_fine and min_fine.replace('.', '').isdigit():
            queryset = queryset.filter(fine_amount__gte=float(min_fine))
        
        max_fine = self.request.query_params.get('max_fine')
        if max_fine and max_fine.replace('.', '').isdigit():
            queryset = queryset.filter(fine_amount__lte=float(max_fine))
        
        borrow_start_date = self.request.query_params.get('borrow_start_date')
        if borrow_start_date:
            try:
                queryset = queryset.filter(borrow_date__date__gte=borrow_start_date)
            except (ValueError, TypeError):
                pass
        
        borrow_end_date = self.request.query_params.get('borrow_end_date')
        if borrow_end_date:
            try:
                queryset = queryset.filter(borrow_date__date__lte=borrow_end_date)
            except (ValueError, TypeError):
                pass
        
        due_start_date = self.request.query_params.get('due_start_date')
        if due_start_date:
            try:
                queryset = queryset.filter(due_date__date__gte=due_start_date)
            except (ValueError, TypeError):
                pass
        
        due_end_date = self.request.query_params.get('due_end_date')
        if due_end_date:
            try:
                queryset = queryset.filter(due_date__date__lte=due_end_date)
            except (ValueError, TypeError):
                pass
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create':
            return BorrowCreateSerializer
        return super().get_serializer_class()
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        book = serializer.validated_data['book']
        reader = serializer.validated_data['reader']
        
        book.available_copies -= 1
        if book.available_copies <= 0:
            book.status = 'borrowed'
        book.save()
        
        borrow = Borrow.objects.create(**serializer.validated_data)
        borrow.save()
        
        output_serializer = BorrowSerializer(borrow)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def unpaid_fines_list(self, request):
        """
        获取所有未缴纳罚款的借阅记录列表
        """
        queryset = Borrow.objects.filter(fine_amount__gt=0, fine_paid=False).order_by('-borrow_date')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    @transaction.atomic
    def return_book(self, request, pk=None):
        borrow = self.get_object()
        
        if borrow.status != 'borrowed':
            return Response(
                {'error': '该借阅记录不是借出状态，无法归还'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ReturnBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        operator = serializer.validated_data.get('operator', '')
        remarks = serializer.validated_data.get('remarks', '')
        fine_per_day = float(request.data.get('fine_per_day', 0.5))
        
        try:
            borrow.return_book(operator=operator, remarks=remarks, fine_per_day=fine_per_day)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        output_serializer = BorrowSerializer(borrow)
        return Response(output_serializer.data)
    
    @action(detail=True, methods=['post'])
    @transaction.atomic
    def report_lost(self, request, pk=None):
        borrow = self.get_object()
        
        if borrow.status != 'borrowed':
            return Response(
                {'error': '该借阅记录不是借出状态，无法报失'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ReportLostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        operator = serializer.validated_data.get('operator', '')
        remarks = serializer.validated_data.get('remarks', '')
        
        try:
            borrow.report_lost_book(operator=operator, remarks=remarks)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        output_serializer = BorrowSerializer(borrow)
        return Response(output_serializer.data)
    
    @action(detail=False, methods=['post'])
    def batch_calculate_fines(self, request):
        """
        批量计算所有借阅中图书的逾期罚款
        """
        fine_per_day = float(request.data.get('fine_per_day', 0.5))
        updated_count = Borrow.calculate_all_overdue_fines(fine_per_day=fine_per_day)
        return Response({
            'message': '批量计算逾期罚款完成',
            'updated_count': updated_count,
            'fine_per_day': fine_per_day
        })
    
    @action(detail=True, methods=['get'])
    def fine_detail(self, request, pk=None):
        """
        获取借阅记录的罚款详情
        """
        borrow = self.get_object()
        borrow.calculate_overdue_fine(auto_save=True)
        
        return Response({
            'borrow_no': borrow.borrow_no,
            'book_title': borrow.book.title,
            'reader_name': borrow.reader.name,
            'reader_no': borrow.reader.reader_no,
            'borrow_date': borrow.borrow_date,
            'due_date': borrow.due_date,
            'return_date': borrow.return_date,
            'status': borrow.status,
            'status_display': borrow.get_status_display(),
            'is_overdue': borrow.is_overdue(),
            'overdue_days': borrow.get_overdue_days(),
            'fine_amount': borrow.fine_amount,
            'fine_paid': borrow.fine_paid,
            'fine_per_day': 0.5
        })
    
    @action(detail=True, methods=['post'])
    @transaction.atomic
    def pay_fine(self, request, pk=None):
        """
        缴纳罚款
        """
        borrow = self.get_object()
        
        if borrow.fine_amount <= 0:
            return Response(
                {'error': '该借阅记录没有需要缴纳的罚款'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if borrow.fine_paid:
            return Response(
                {'error': '该借阅记录的罚款已缴纳'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        borrow.fine_paid = True
        borrow.save()
        
        return Response({
            'message': '罚款缴纳成功',
            'borrow_no': borrow.borrow_no,
            'fine_amount': borrow.fine_amount
        })
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        total = Borrow.objects.count()
        borrowed = Borrow.objects.filter(status='borrowed').count()
        returned = Borrow.objects.filter(status='returned').count()
        lost = Borrow.objects.filter(status='lost').count()
        
        overdue_count = 0
        total_fine = 0.0
        unpaid_fine = 0.0
        paid_fine = 0.0
        
        for borrow in Borrow.objects.all():
            fine = borrow.calculate_overdue_fine()
            if borrow.status == 'borrowed' and fine > 0:
                overdue_count += 1
                total_fine += fine
                if not borrow.fine_paid:
                    unpaid_fine += fine
            elif borrow.fine_amount > 0:
                total_fine += borrow.fine_amount
                if borrow.fine_paid:
                    paid_fine += borrow.fine_amount
                else:
                    unpaid_fine += borrow.fine_amount
        
        return Response({
            'total': total,
            'borrowed': borrowed,
            'returned': returned,
            'lost': lost,
            'overdue_count': overdue_count,
            'total_fine': round(total_fine, 2),
            'unpaid_fine': round(unpaid_fine, 2),
            'paid_fine': round(paid_fine, 2),
        })
    
    @action(detail=False, methods=['get'])
    def overdue_list(self, request):
        now = datetime.now()
        overdue_borrows = Borrow.objects.filter(
            status='borrowed',
            due_date__lt=now
        ).order_by('due_date')
        serializer = BorrowSerializer(overdue_borrows, many=True)
        return Response(serializer.data)
