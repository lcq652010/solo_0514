from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.db.models import Q
from .models import Supplier, PurchaseOrder, PurchaseOrderItem
from .serializers import SupplierSerializer, PurchaseOrderSerializer, PurchaseOrderItemSerializer
from inventory.services import InventoryService
from accounts.permissions import SupplierManagePermission, WarehouseManagePermission


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), SupplierManagePermission()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        is_active = self.request.query_params.get('is_active')
        
        if name:
            queryset = queryset.filter(Q(name__icontains=name) | Q(contact_person__icontains=name))
        if is_active is not None:
            queryset = queryset.filter(is_active=(is_active.lower() == 'true'))
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        self.validate_supplier_data(serializer.validated_data)
        serializer.save()

    def perform_update(self, serializer):
        self.validate_supplier_data(serializer.validated_data)
        serializer.save()

    def validate_supplier_data(self, data):
        if not data.get('supplier_code'):
            raise ValidationError({'supplier_code': ['供应商编号为必填项']})
        if not data.get('name'):
            raise ValidationError({'name': ['供应商名称为必填项']})


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'confirm_receipt']:
            return [IsAuthenticated(), WarehouseManagePermission()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()
        order_status = self.request.query_params.get('status')
        supplier_id = self.request.query_params.get('supplier')
        order_no = self.request.query_params.get('order_no')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if order_status:
            queryset = queryset.filter(status=order_status)
        if supplier_id:
            queryset = queryset.filter(supplier_id=supplier_id)
        if order_no:
            queryset = queryset.filter(order_no__icontains=order_no)
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)
        
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        self.validate_order_data(serializer.validated_data)
        serializer.save()

    def perform_update(self, serializer):
        if serializer.instance.status != 'pending':
            raise ValidationError({'error': ['只有待入库的订单才能修改']})
        self.validate_order_data(serializer.validated_data)
        serializer.save()

    def validate_order_data(self, data):
        if not data.get('supplier'):
            raise ValidationError({'supplier': ['供应商为必填项']})

    @action(detail=True, methods=['post'])
    def confirm_receipt(self, request, pk=None):
        purchase_order = self.get_object()
        if purchase_order.status != 'pending':
            return Response(
                {'error': '只有待入库的订单才能确认入库'},
                status=status.HTTP_400_BAD_REQUEST
            )

        items = purchase_order.items.all()
        if not items.exists():
            return Response(
                {'error': '订单明细为空，无法入库'},
                status=status.HTTP_400_BAD_REQUEST
            )

        for item in items:
            if item.quantity <= 0:
                return Response(
                    {'error': f'商品 {item.product.name} 入库数量必须大于0'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if item.unit_price < 0:
                return Response(
                    {'error': f'商品 {item.product.name} 单价不能为负数'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        try:
            with transaction.atomic():
                for item in items:
                    InventoryService.stock_in(
                        product=item.product,
                        quantity=item.quantity,
                        related_order_no=purchase_order.order_no,
                        remark=f'采购订单入库'
                    )

                purchase_order.status = 'completed'
                purchase_order.save()

            return Response({'message': '入库成功'})
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        purchase_order = self.get_object()
        if purchase_order.status == 'completed':
            return Response(
                {'error': '已入库的订单不能作废'},
                status=status.HTTP_400_BAD_REQUEST
            )
        purchase_order.status = 'cancelled'
        purchase_order.save()
        return Response({'message': '订单已作废'})
