from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from datetime import datetime

from .models import Product, Member, PurchaseOrder, PurchaseItem, SalesOrder, SalesItem, StockLog, PointsLog, User
from .serializers import (
    ProductSerializer, MemberSerializer, UserSerializer,
    PurchaseOrderSerializer, PurchaseItemSerializer,
    SalesOrderSerializer, SalesItemSerializer,
    StockLogSerializer, PointsLogSerializer,
    SalesOrderCreateSerializer, PurchaseOrderCreateSerializer,
    StockAdjustSerializer
)
from .permissions import IsCashier, IsWarehouse, IsAdmin, IsCashierOrWarehouse


class StandardPagination(PageNumberPagination):
    """标准分页器"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductViewSet(viewsets.ModelViewSet):
    """商品管理视图集"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardPagination
    
    def get_permissions(self):
        """根据操作分配权限"""
        if self.action in ['list', 'retrieve', 'check_stock', 'low_stock_alert']:
            permission_classes = [IsCashierOrWarehouse]
        elif self.action in ['create', 'update', 'partial_update', 'destroy', 'adjust_stock']:
            permission_classes = [IsAdmin | IsWarehouse]
        else:
            permission_classes = [IsCashierOrWarehouse]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        keyword = self.request.query_params.get('keyword')
        is_active = self.request.query_params.get('is_active')
        stock_status = self.request.query_params.get('stock_status')
        min_stock = self.request.query_params.get('min_stock')
        max_stock = self.request.query_params.get('max_stock')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        barcode = self.request.query_params.get('barcode')
        supplier = self.request.query_params.get('supplier')

        if category:
            queryset = queryset.filter(category=category)
        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword) | 
                Q(product_id__icontains=keyword)
            )
        if barcode:
            queryset = queryset.filter(barcode__icontains=barcode)
        if supplier:
            queryset = queryset.filter(supplier__icontains=supplier)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        if stock_status:
            if stock_status == 'out_of_stock':
                queryset = queryset.filter(stock__lte=0)
            elif stock_status == 'low':
                queryset = queryset.filter(stock__gt=0, stock__lt=10)
            elif stock_status == 'normal':
                queryset = queryset.filter(stock__gte=10, stock__lt=50)
            elif stock_status == 'sufficient':
                queryset = queryset.filter(stock__gte=50)
        
        if min_stock is not None:
            queryset = queryset.filter(stock__gte=int(min_stock))
        if max_stock is not None:
            queryset = queryset.filter(stock__lte=int(max_stock))
        
        if min_price is not None:
            queryset = queryset.filter(price__gte=float(min_price))
        if max_price is not None:
            queryset = queryset.filter(price__lte=float(max_price))

        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        if not serializer.validated_data.get('product_id'):
            product_id = f'SP{datetime.now().strftime("%Y%m%d%H%M%S")}'
            serializer.save(product_id=product_id)
        else:
            serializer.save()

    @action(detail=True, methods=['post'])
    def adjust_stock(self, request, pk=None):
        """调整库存"""
        product = self.get_object()
        serializer = StockAdjustSerializer(data=request.data)
        if serializer.is_valid():
            quantity = serializer.validated_data['quantity']
            remark = serializer.validated_data.get('remark', '')

            stock_before = product.stock
            stock_after = stock_before + quantity

            if stock_after < 0:
                return Response(
                    {'error': '调整后库存不能为负数'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            with transaction.atomic():
                product.stock = stock_after
                product.save()

                StockLog.objects.create(
                    product=product,
                    type='adjust',
                    quantity=quantity,
                    stock_before=stock_before,
                    stock_after=stock_after,
                    remark=remark
                )

            return Response({
                'message': '库存调整成功',
                'stock_before': stock_before,
                'stock_after': stock_after
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def check_stock(self, request):
        """批量库存校验"""
        product_ids = request.query_params.getlist('product_ids')
        if not product_ids:
            return Response(
                {'error': '请提供商品ID列表'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        result = []
        for pid in product_ids:
            try:
                product = Product.objects.get(id=pid)
                result.append({
                    'product_id': product.id,
                    'product_name': product.name,
                    'current_stock': product.stock,
                    'stock_status': 'sufficient' if product.stock >= 50 else 
                                   'normal' if product.stock >= 10 else
                                   'low' if product.stock > 0 else 'out_of_stock',
                    'is_sufficient': product.stock > 0
                })
            except Product.DoesNotExist:
                result.append({
                    'product_id': int(pid),
                    'error': '商品不存在'
                })
        
        return Response(result)

    @action(detail=False, methods=['get'])
    def low_stock_alert(self, request):
        """低库存预警列表"""
        threshold = int(request.query_params.get('threshold', 10))
        low_stock_products = Product.objects.filter(stock__gt=0, stock__lt=threshold, is_active=True)
        out_of_stock_products = Product.objects.filter(stock__lte=0, is_active=True)
        
        return Response({
            'low_stock_count': low_stock_products.count(),
            'out_of_stock_count': out_of_stock_products.count(),
            'low_stock_products': ProductSerializer(low_stock_products, many=True).data,
            'out_of_stock_products': ProductSerializer(out_of_stock_products, many=True).data
        })


class MemberViewSet(viewsets.ModelViewSet):
    """会员管理视图集"""
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    pagination_class = StandardPagination
    
    def get_permissions(self):
        """根据操作分配权限：收银员和管理员可管理会员"""
        if self.action in ['list', 'retrieve', 'by_phone']:
            permission_classes = [IsCashierOrWarehouse]
        else:
            permission_classes = [IsCashier | IsAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.query_params.get('keyword')
        is_active = self.request.query_params.get('is_active')
        min_points = self.request.query_params.get('min_points')
        
        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword) |
                Q(phone__icontains=keyword) |
                Q(member_id__icontains=keyword)
            )
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        if min_points is not None:
            queryset = queryset.filter(points__gte=int(min_points))
        
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        if not serializer.validated_data.get('member_id'):
            member_id = f'M{datetime.now().strftime("%Y%m%d%H%M%S")}'
            serializer.save(member_id=member_id)
        else:
            serializer.save()

    @action(detail=False, methods=['get'])
    def by_phone(self, request):
        """根据手机号查询会员"""
        phone = request.query_params.get('phone')
        if not phone:
            return Response({'error': '请提供手机号'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            member = Member.objects.get(phone=phone, is_active=True)
            serializer = self.get_serializer(member)
            return Response(serializer.data)
        except Member.DoesNotExist:
            return Response({'error': '会员不存在'}, status=status.HTTP_404_NOT_FOUND)


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    """采购订单管理视图集"""
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    pagination_class = StandardPagination
    
    def get_permissions(self):
        """根据操作分配权限：库管和管理员可处理采购"""
        permission_classes = [IsWarehouse | IsAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        supplier = self.request.query_params.get('supplier')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if supplier:
            queryset = queryset.filter(supplier__icontains=supplier)
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)
        
        return queryset.order_by('-created_at')

    @action(detail=False, methods=['post'])
    def create_purchase(self, request):
        """创建采购订单并入库"""
        serializer = PurchaseOrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                purchase_order = PurchaseOrder.objects.create(
                    supplier=serializer.validated_data['supplier'],
                    remark=serializer.validated_data.get('remark', ''),
                    status='completed'
                )

                total_amount = 0
                for item_data in serializer.validated_data['items']:
                    product = get_object_or_404(Product, id=item_data['product_id'])
                    quantity = item_data['quantity']
                    unit_price = item_data['unit_price']
                    subtotal = quantity * unit_price
                    total_amount += subtotal

                    PurchaseItem.objects.create(
                        purchase_order=purchase_order,
                        product=product,
                        quantity=quantity,
                        unit_price=unit_price,
                        subtotal=subtotal
                    )

                    stock_before = product.stock
                    stock_after = stock_before + quantity
                    product.stock = stock_after
                    product.cost_price = unit_price
                    product.save()

                    StockLog.objects.create(
                        product=product,
                        type='purchase',
                        quantity=quantity,
                        stock_before=stock_before,
                        stock_after=stock_after,
                        related_order=purchase_order.order_no
                    )

                purchase_order.total_amount = total_amount
                purchase_order.save()

            return Response({
                'message': '采购入库成功',
                'order_no': purchase_order.order_no,
                'total_amount': total_amount
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SalesOrderViewSet(viewsets.ModelViewSet):
    """销售订单（收银）管理视图集"""
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    pagination_class = StandardPagination
    
    def get_permissions(self):
        """根据操作分配权限：收银员和管理员可处理销售"""
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsCashierOrWarehouse]
        else:
            permission_classes = [IsCashier | IsAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        cashier = self.request.query_params.get('cashier')
        member_id = self.request.query_params.get('member_id')

        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)
        if cashier:
            queryset = queryset.filter(cashier__icontains=cashier)
        if member_id:
            queryset = queryset.filter(member_id=member_id)
        
        return queryset.order_by('-created_at')

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        """收银结账"""
        serializer = SalesOrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                member = None
                member_id = serializer.validated_data.get('member_id')
                if member_id:
                    member = get_object_or_404(Member, id=member_id)

                points_used = serializer.validated_data.get('points_used', 0)
                if member and points_used > 0:
                    if member.points < points_used:
                        return Response({'error': '积分不足'}, status=status.HTTP_400_BAD_REQUEST)

                sales_order = SalesOrder.objects.create(
                    member=member,
                    points_used=points_used,
                    cashier=serializer.validated_data.get('cashier', '收银员'),
                    remark=serializer.validated_data.get('remark', ''),
                    status='completed'
                )

                total_amount = 0
                for item_data in serializer.validated_data['items']:
                    product = get_object_or_404(Product, id=item_data['product_id'])
                    quantity = item_data['quantity']

                    if product.stock < quantity:
                        return Response(
                            {'error': f'商品 {product.name} 库存不足'},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    unit_price = product.price
                    subtotal = quantity * unit_price
                    total_amount += subtotal

                    SalesItem.objects.create(
                        sales_order=sales_order,
                        product=product,
                        quantity=quantity,
                        unit_price=unit_price,
                        subtotal=subtotal
                    )

                    stock_before = product.stock
                    stock_after = stock_before - quantity
                    product.stock = stock_after
                    product.save()

                    StockLog.objects.create(
                        product=product,
                        type='sale',
                        quantity=-quantity,
                        stock_before=stock_before,
                        stock_after=stock_after,
                        related_order=sales_order.order_no
                    )

                discount_amount = points_used
                pay_amount = total_amount - discount_amount
                if pay_amount < 0:
                    pay_amount = 0

                points_earned = 0
                if member:
                    points_earned = int(pay_amount)

                    if points_used > 0:
                        points_before = member.points
                        member.deduct_points(points_used)
                        PointsLog.objects.create(
                            member=member,
                            type='use',
                            points=-points_used,
                            points_before=points_before,
                            points_after=member.points,
                            related_order=sales_order.order_no
                        )

                    if points_earned > 0:
                        points_before = member.points
                        member.add_points(pay_amount)
                        PointsLog.objects.create(
                            member=member,
                            type='earn',
                            points=points_earned,
                            points_before=points_before,
                            points_after=member.points,
                            related_order=sales_order.order_no
                        )

                sales_order.total_amount = total_amount
                sales_order.discount_amount = discount_amount
                sales_order.pay_amount = pay_amount
                sales_order.points_earned = points_earned
                sales_order.save()

            return Response({
                'message': '收银成功',
                'order_no': sales_order.order_no,
                'total_amount': total_amount,
                'discount_amount': discount_amount,
                'pay_amount': pay_amount,
                'points_earned': points_earned
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        """退款"""
        sales_order = self.get_object()
        if sales_order.status != 'completed':
            return Response({'error': '只有已完成的订单才能退款'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            sales_items = SalesItem.objects.filter(sales_order=sales_order)
            for item in sales_items:
                product = item.product
                quantity = item.quantity

                stock_before = product.stock
                stock_after = stock_before + quantity
                product.stock = stock_after
                product.save()

                StockLog.objects.create(
                    product=product,
                    type='refund',
                    quantity=quantity,
                    stock_before=stock_before,
                    stock_after=stock_after,
                    related_order=sales_order.order_no
                )

            if sales_order.member and sales_order.points_earned > 0:
                member = sales_order.member
                points_before = member.points
                member.points -= sales_order.points_earned
                if member.points < 0:
                    member.points = 0
                member.save()

                PointsLog.objects.create(
                    member=member,
                    type='adjust',
                    points=-sales_order.points_earned,
                    points_before=points_before,
                    points_after=member.points,
                    related_order=sales_order.order_no,
                    remark='退款扣减积分'
                )

            sales_order.status = 'refunded'
            sales_order.save()

        return Response({'message': '退款成功'})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """作废订单"""
        sales_order = self.get_object()
        if sales_order.status == 'refunded':
            return Response({'error': '已退款订单不能作废'}, status=status.HTTP_400_BAD_REQUEST)

        if sales_order.status == 'completed':
            with transaction.atomic():
                sales_items = SalesItem.objects.filter(sales_order=sales_order)
                for item in sales_items:
                    product = item.product
                    quantity = item.quantity

                    stock_before = product.stock
                    stock_after = stock_before + quantity
                    product.stock = stock_after
                    product.save()

                    StockLog.objects.create(
                        product=product,
                        type='refund',
                        quantity=quantity,
                        stock_before=stock_before,
                        stock_after=stock_after,
                        related_order=sales_order.order_no
                    )

        sales_order.status = 'cancelled'
        sales_order.save()
        return Response({'message': '订单已作废'})


class StockLogViewSet(viewsets.ReadOnlyModelViewSet):
    """库存日志视图集"""
    queryset = StockLog.objects.all()
    serializer_class = StockLogSerializer
    pagination_class = StandardPagination
    permission_classes = [IsWarehouse | IsAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()
        product_id = self.request.query_params.get('product_id')
        type_filter = self.request.query_params.get('type')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if product_id:
            queryset = queryset.filter(product_id=product_id)
        if type_filter:
            queryset = queryset.filter(type=type_filter)
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)
        
        return queryset.order_by('-created_at')


class PointsLogViewSet(viewsets.ReadOnlyModelViewSet):
    """积分日志视图集"""
    queryset = PointsLog.objects.all()
    serializer_class = PointsLogSerializer
    pagination_class = StandardPagination
    permission_classes = [IsCashier | IsAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()
        member_id = self.request.query_params.get('member_id')
        type_filter = self.request.query_params.get('type')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if member_id:
            queryset = queryset.filter(member_id=member_id)
        if type_filter:
            queryset = queryset.filter(type=type_filter)
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)
        
        return queryset.order_by('-created_at')


class UserViewSet(viewsets.ModelViewSet):
    """用户管理视图集（仅管理员可访问）"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardPagination
    permission_classes = [IsAdmin]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.query_params.get('keyword')
        role = self.request.query_params.get('role')
        
        if keyword:
            queryset = queryset.filter(
                Q(username__icontains=keyword) |
                Q(email__icontains=keyword)
            )
        if role:
            queryset = queryset.filter(role=role)
        
        return queryset.order_by('-date_joined')
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """获取当前用户信息"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
